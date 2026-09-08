#!/usr/bin/env python3
"""Judge the frozen CLEF eHealth TAR panel with open-weight models under the protocol fixed in
scale_prereg.py. Runs on one GPU via vLLM. No network access is needed once the model is cached
and the inputs are present.

Design notes that matter for reproducibility, not style:

  * Decoding is pinned by scale_prereg.py (temperature 0, top_p 1, max_tokens 1024, seed). At
    temperature 0 a parse failure is DETERMINISTIC, so it is recorded on one attempt; the retry
    budget applies only to transient GPU/loader failures. This is stated in the pre-registration
    amendment to R3.
  * The strict parser is the ONLY parser. A non-matching reply becomes label=null. There is no
    fallback pattern anywhere in this file, deliberately.
  * Qwen3 ships a thinking mode. It is disabled through the chat template and the setting is
    written into the run manifest, because an earlier arm in this project was truncated before
    its score line by a reasoning preamble.
  * Every run writes a manifest recording the resolved HuggingFace commit sha, quantisation,
    vLLM/torch versions and GPU name. An arm without a manifest is not reportable (R5).

Usage
    python code/scale_judge.py --arm qwen3-8b --condition A
    python code/scale_judge.py --arm qwen3-32b --condition C   # needs an 80 GB card in bf16
    python code/scale_judge.py --arm qwen3-8b --condition A --guided     # only per R2
    python code/scale_judge.py --arm qwen3-4b --condition A --limit 64   # smoke test

Paths default to the repository layout (data/..., labels/...), so run from the repository root.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
# The protocol constants live in prereg/, one level up from code/. Importing them rather than
# copying them means a run cannot silently disagree with its own pre-registration.
for _p in (os.path.join(_ROOT, "prereg"), _HERE, _ROOT):
    if _p not in sys.path:
        sys.path.append(_p)
try:
    from scale_prereg import BINARISE_AT, MAX_TOKENS, SEED, TEMPERATURE, TOP_P
except ModuleNotFoundError as _exc:
    raise SystemExit(
        f"cannot import the pre-registration: {_exc}\n"
        f"  looked in {os.path.join(_ROOT, 'prereg')}, {_HERE}, {_ROOT}\n"
        f"  scale_prereg.py must be importable - this script reads its decoding parameters "
        f"and binarisation threshold from it rather than restating them.")

STRICT = re.compile(r"##\s*final\s*score\s*:?\s*([0-3])", re.I)

# Arm name -> HuggingFace repo. Revisions are RESOLVED AT RUN TIME and written to the manifest
# rather than pinned here, because pinning a sha we have never resolved would be a claim we
# cannot support. The manifest is what makes a run reproducible.
ARMS = {
    # qwen3 - not gated. Parameter counts are safetensors totals from the HuggingFace API.
    "qwen3-1.7b":             "Qwen/Qwen3-1.7B",
    "qwen3-4b":               "Qwen/Qwen3-4B",
    "qwen3-8b":               "Qwen/Qwen3-8B",
    "qwen3-14b":              "Qwen/Qwen3-14B",
    "qwen3-32b":              "Qwen/Qwen3-32B",
    # llama - gated with MANUAL approval; accept the licence on each model page first.
    "llama-3.2-1b-instruct":  "meta-llama/Llama-3.2-1B-Instruct",
    "llama-3.2-3b-instruct":  "meta-llama/Llama-3.2-3B-Instruct",
    "llama-3.1-8b-instruct":  "meta-llama/Llama-3.1-8B-Instruct",
    # gemma - gated with MANUAL approval. NOTE the architecture change within the ladder:
    # gemma-3-1b-it is Gemma3ForCausalLM while 4b and 12b are Gemma3ForConditionalGeneration,
    # i.e. multimodal checkpoints used here on text only. Disclosed in the pre-registration as a
    # within-family confound between scale and architecture that this design does not resolve.
    "gemma-3-1b-it":          "google/gemma-3-1b-it",
    "gemma-3-4b-it":          "google/gemma-3-4b-it",
    "gemma-3-12b-it":         "google/gemma-3-12b-it",
    "gemma-3-27b-it":         "google/gemma-3-27b-it",
}

FAMILY = {"qwen3": "qwen3", "llama": "llama", "gemma": "gemma"}

# safetensors parameter totals from the HuggingFace API, used for the log(params) fits
PARAMS = {"qwen3-1.7b": 2_031_739_904, "qwen3-4b": 4_022_468_096,
          "qwen3-8b": 8_190_735_360, "qwen3-14b": 14_768_307_200,
          "qwen3-32b": 32_762_123_264,
          "llama-3.2-1b-instruct": 1_235_814_400, "llama-3.2-3b-instruct": 3_212_749_824,
          "llama-3.1-8b-instruct": 8_030_261_248,
          "gemma-3-1b-it": 999_885_952, "gemma-3-4b-it": 4_300_079_472,
          "gemma-3-12b-it": 12_187_325_040, "gemma-3-27b-it": 27_432_406_640}

# Guided decoding target: the protocol's output contract is a single line. The regex is the same
# shape the strict parser accepts, so a guided run cannot produce a string the parser rejects.
GUIDED_REGEX = r"## final score: [0-3]"

# Approximate bf16 weight footprint in GB, from published parameter counts. Used only to refuse
# an arm that cannot fit, so an over-estimate is the safe direction.
WEIGHT_GB = {k: round(v * 2 / 2**30, 1) for k, v in PARAMS.items()}


def build_prompts(panel_csv, abstracts_jsonl, topics_json, prompt_txt, criteria_txt, condition,
                  limit=None):
    """One prompt per panel row. Substitution is positional and literal - the template's three
    tokens are replaced and nothing else is touched, so a template edit cannot silently change
    the semantics of a run."""
    import csv

    # The abstracts file is the one input the repository does NOT ship - PubMed text is fetched,
    # not redistributed - so a missing abstracts file means the fetch step has not been run, and
    # that deserves its own message rather than the generic one.
    if not os.path.exists(abstracts_jsonl):
        raise SystemExit(
            f"missing input: {abstracts_jsonl}\n"
            f"  This file is NOT shipped in the repository. PubMed abstract text is fetched\n"
            f"  rather than redistributed, so it has to be built once before any judging:\n"
            f"\n"
            f"      python code/fetch_abstracts.py --pmids data/pmids_panel.txt "
            f"--out {abstracts_jsonl}\n"
            f"\n"
            f"  In the notebook that is the cell above the smoke test. It takes about a minute\n"
            f"  for 2,017 records and is cached for the rest of the session.")
    for path in (panel_csv, topics_json, prompt_txt):
        if not os.path.exists(path):
            raise SystemExit(f"missing input: {path}\n"
                             f"  These ship with the repository, so this usually means the "
                             f"working directory is wrong.\n"
                             f"  Run from the repository root (cwd is {os.getcwd()}), or pass "
                             f"explicit --panel --topics --prompt paths.")
    if condition == "C" and not os.path.exists(criteria_txt):
        raise SystemExit(f"condition C needs the criteria block but {criteria_txt} is missing")

    template = open(prompt_txt).read()
    for tok in ("{criteria_block}", "{question}", "{passage}"):
        if tok not in template:
            raise SystemExit(f"prompt template is missing {tok} - refusing to run")

    criteria = open(criteria_txt).read() if condition == "C" else ""
    topics = json.load(open(topics_json))
    abstracts = {}
    with open(abstracts_jsonl) as fh:
        for line in fh:
            if line.strip():
                rec = json.loads(line)
                abstracts[str(rec["pmid"])] = rec

    rows, missing = [], 0
    with open(panel_csv) as fh:
        for r in csv.DictReader(fh):
            topic, pmid = str(r["topic"]), str(r["pmid"])
            rec = abstracts.get(pmid)
            if rec is None:
                missing += 1
                continue
            passage = (rec.get("title") or "") + "\n" + (rec.get("abstract") or "")
            text = (template.replace("{criteria_block}", criteria)
                            .replace("{question}", (topics.get(topic) or {}).get("title", ""))
                            .replace("{passage}", passage))
            rows.append(dict(topic=topic, pmid=pmid, human=int(r.get("human", 0)), prompt=text,
                             title_only=not (rec.get("abstract") or "").strip()))
            if limit and len(rows) >= limit:
                break
    return rows, missing


def resolve_revision(repo):
    """Record what we actually loaded. Returns None rather than guessing if the hub is
    unreachable - a missing sha is reported, never invented."""
    try:
        from huggingface_hub import HfApi
        return HfApi().model_info(repo).sha
    except Exception as exc:  # noqa: BLE001 - the reason is written to the manifest
        return f"UNRESOLVED: {type(exc).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=sorted(ARMS))
    ap.add_argument("--condition", required=True, choices=("A", "C"))
    # Precision is pinned at bf16 by the pre-registration. There is deliberately NO
    # quantisation flag: a size that does not fit in bf16 is reported as not attempted rather
    # than run at a lower precision, because that would mix precision with scale.
    ap.add_argument("--dtype", default="bfloat16", choices=("bfloat16",),
                    help="bf16 only, fixed by scale_prereg.py")
    ap.add_argument("--guided", action="store_true",
                    help="constrain output to the score line. Per R2 this is a DIFFERENT "
                         "harness and must be declared; use only when free generation fell "
                         "below the registered strict-parse floor.")
    ap.add_argument("--panel", default="data/panel_sample.csv")
    ap.add_argument("--abstracts", default="clef_abstracts.jsonl")
    ap.add_argument("--topics", default="data/clef_topics.json")
    ap.add_argument("--prompt", default="data/elig_prompt.txt")
    ap.add_argument("--criteria", default="data/crit_block_C.txt")
    ap.add_argument("--outdir", default="labels")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    args = ap.parse_args()

    repo = ARMS[args.arm]
    tag = f"{args.arm}_{args.condition}" + ("_guided" if args.guided else "")
    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, f"scale_labels_{tag}.jsonl")
    man_path = os.path.join(args.outdir, f"scale_manifest_{tag}.json")

    rows, missing = build_prompts(args.panel, args.abstracts, args.topics, args.prompt,
                                 args.criteria, args.condition, args.limit)
    print(f"[{tag}] rows {len(rows)} | abstracts missing {missing} | "
          f"title-only {sum(r['title_only'] for r in rows)}", flush=True)
    if not rows:
        raise SystemExit("no rows built - check the input paths")

    from vllm import LLM, SamplingParams
    import torch

    is_qwen3 = args.arm.startswith("qwen3")
    family = next((f for f in FAMILY if args.arm.startswith(f)), "unknown")
    # Refuse loudly rather than let vLLM OOM halfway through a 2,025-row run.
    need_gb = WEIGHT_GB[args.arm]
    have_gb = (torch.cuda.get_device_properties(0).total_memory / 2**30
               if torch.cuda.is_available() else 0.0)
    if have_gb and need_gb > have_gb * args.gpu_memory_utilization:
        raise SystemExit(
            f"{args.arm} needs about {need_gb:.0f} GB in bf16 and this device offers "
            f"{have_gb:.0f} GB ({have_gb * args.gpu_memory_utilization:.0f} GB usable at "
            f"utilisation {args.gpu_memory_utilization}).\n"
            f"  Per the pre-registration this arm is NOT RUN and is reported as not attempted. "
            f"Do NOT quantise it to make it fit - that would mix precision with scale.")

    # trust_remote_code is deliberately NOT set. Two separate reasons, kept distinct:
    #   1. None of the arms in ARMS needs it - all are natively supported by transformers.
    #   2. Passing it here did nothing anyway. transformers reported, verbatim: "The argument
    #      `trust_remote_code` is to be used with Auto classes. It has no effect here and is
    #      ignored." That is, the flag IS meant for Auto classes and would take effect there;
    #      it has no effect at THIS call site. (An earlier version of this comment inverted
    #      that warning, claiming the flag is ignored for Auto classes. It is not.)
    llm = LLM(model=repo, dtype=args.dtype, seed=SEED, max_model_len=args.max_model_len,
              gpu_memory_utilization=args.gpu_memory_utilization)

    sp_kwargs = dict(temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_TOKENS, seed=SEED)
    if args.guided:
        # vLLM moved guided decoding between versions; try the current field, fall back to the
        # older one, and refuse rather than run unconstrained if neither exists.
        try:
            from vllm.sampling_params import GuidedDecodingParams
            sp_kwargs["guided_decoding"] = GuidedDecodingParams(regex=GUIDED_REGEX)
        except Exception:
            try:
                sp_kwargs["guided_regex"] = GUIDED_REGEX
            except Exception:
                raise SystemExit("--guided requested but this vLLM exposes no guided decoding "
                                 "API; refusing to fall back to free generation silently")
    sp = SamplingParams(**sp_kwargs)

    tok = llm.get_tokenizer()
    chat_kwargs = dict(tokenize=False, add_generation_prompt=True)
    if is_qwen3:
        chat_kwargs["enable_thinking"] = False   # R6
    texts = [tok.apply_chat_template([{"role": "user", "content": r["prompt"]}], **chat_kwargs)
             for r in rows]

    t0 = time.time()
    outs = llm.generate(texts, sp)
    wall = time.time() - t0

    n_strict = n_null = 0
    with open(out_path, "w") as fh:
        for r, o in zip(rows, outs):
            gen = o.outputs[0]
            m = STRICT.search(gen.text or "")
            label = int(m.group(1)) if m else None
            n_strict += label is not None
            n_null += label is None
            fh.write(json.dumps(dict(
                topic=r["topic"], pmid=r["pmid"], label=label,
                in_tokens=len(o.prompt_token_ids), out_tokens=len(gen.token_ids),
                finish_reason=gen.finish_reason, title_only=r["title_only"],
                raw=(gen.text or "")[:200] if label is None else None)) + "\n")

    strict_rate = n_strict / len(rows)
    manifest = dict(
        arm=args.arm, family=family, params=PARAMS.get(args.arm),
        condition=args.condition, guided=bool(args.guided),
        hf_repo=repo, hf_revision=resolve_revision(repo), dtype=args.dtype,
        quantisation="none",
        thinking_disabled=bool(is_qwen3),
        temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_TOKENS, seed=SEED,
        binarise_at=BINARISE_AT, max_model_len=args.max_model_len,
        rows=len(rows), strict_parsed=n_strict, nulls=n_null,
        strict_parse_rate=round(strict_rate, 4),
        abstracts_missing=missing, title_only=sum(r["title_only"] for r in rows),
        out_tokens_median=sorted(len(o.outputs[0].token_ids) for o in outs)[len(outs) // 2],
        out_tokens_max=max(len(o.outputs[0].token_ids) for o in outs),
        wall_seconds=round(wall, 1), rows_per_second=round(len(rows) / wall, 2),
        gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        torch=torch.__version__, python=platform.python_version(),
        vllm=__import__("vllm").__version__,
        # transformers version is load-bearing, not incidental: vLLM 0.11.0 declares
        # transformers>=4.55.2 with no upper bound, and transformers 5.x removed
        # Tokenizer.all_special_tokens_extended, which vLLM 0.11.0 calls. A run whose
        # transformers major version is not recorded cannot be reproduced.
        transformers=__import__("transformers").__version__,
        limit_applied=args.limit)
    json.dump(manifest, open(man_path, "w"), indent=1)

    print(f"[{tag}] strict {n_strict}/{len(rows)} = {strict_rate:.4f} | nulls {n_null} | "
          f"out_tok med {manifest['out_tokens_median']} max {manifest['out_tokens_max']} | "
          f"{manifest['rows_per_second']:.1f} rows/s", flush=True)
    if strict_rate < 0.95 and not args.guided:
        print(f"[{tag}] strict parse rate {strict_rate:.4f} is BELOW the registered floor 0.95. "
              f"Per R2 this arm must be re-run with --guided, AND one arm that passed must also "
              f"be run guided so the harness effect can be bounded. Do NOT mix free and guided "
              f"labels within an arm.", flush=True)
    print(f"[{tag}] wrote {out_path} and {man_path}", flush=True)


if __name__ == "__main__":
    main()

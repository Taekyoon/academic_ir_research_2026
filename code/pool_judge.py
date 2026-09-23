#!/usr/bin/env python3
"""Judge the WHOLE CLEF 2017 abstract-level pool with one open-weight arm.

WHY A SEPARATE SCRIPT INSTEAD OF scale_judge.py. That script judges the frozen 2,025-pair
panel in ONE llm.generate call and writes its output file once, at the end. At 117,562 pairs
that is the wrong shape twice over: a Colab disconnect loses the entire run, and every
completion is held in memory until the last one finishes. This script keeps the registered
pieces by IMPORTING them from scale_judge - the arm map, the prompt builder, the guided
patterns, the head-and-tail clipper - and changes only the execution shape: fixed-size
batches, append after every batch, and resume by (topic, pmid).

WHAT IT DOES NOT CHANGE. Decoding comes from scale_prereg.py (temperature, top_p, max_tokens,
seed) exactly as in scale_judge.py. Precision is bf16 with no quantisation flag. The guided
target is the permissive pattern, and the binding check runs on the real output rather than on
a probe batch: a completion that finished with 'stop' without ending at the score line proves
the constraint was not applied to it, and a non-binding completion that nevertheless produced
a label is counted separately because only that kind can contaminate a rate.

Usage
    python code/pool_judge.py --arm qwen3-8b --condition C --guided \
        --pairs data/pool_pairs.csv --abstracts clef_abstracts.jsonl
    python code/pool_judge.py --arm qwen3-8b --condition C --guided --shard 0 --num-shards 4
    python code/pool_judge.py --arm qwen3-8b --condition C --guided --limit 256   # smoke test

Resume is automatic: rerunning the same command skips the (topic, pmid) pairs already in the
output file. Shards are disjoint by a stable hash of the pair, so shards may be run in any
order, on separate sessions, and concatenated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (os.path.join(_ROOT, "prereg"), _HERE, _ROOT):
    if _p not in sys.path:
        sys.path.append(_p)

from scale_prereg import BINARISE_AT, MAX_TOKENS, SEED, TEMPERATURE, TOP_P
from scale_judge import (ARMS, FAMILY, GUIDED_REGEX, GUIDED_REGEX_STRICT, PARAMS, STRICT,
                         _clip, build_prompts, resolve_revision)

TAIL = re.compile(r"##[ ]?final score: [0-3]$")


def shard_of(topic, pmid, num_shards):
    """Stable, order-independent assignment. A hash rather than a slice so that a partially
    finished shard can be resumed without knowing how the rows were ordered."""
    h = hashlib.sha1(f"{topic}|{pmid}".encode()).hexdigest()
    return int(h[:8], 16) % num_shards


def done_keys(path):
    keys = set()
    if not os.path.exists(path):
        return keys
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                keys.add((str(rec["topic"]), str(rec["pmid"])))
            except Exception:
                continue
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=sorted(ARMS))
    ap.add_argument("--condition", required=True, choices=("A", "C"))
    ap.add_argument("--dtype", default="bfloat16", choices=("bfloat16",),
                    help="bf16 only, fixed by scale_prereg.py")
    ap.add_argument("--guided", action="store_true")
    ap.add_argument("--guided-strict", action="store_true")
    ap.add_argument("--pairs", default="data/pool_pairs.csv")
    ap.add_argument("--abstracts", default="clef_abstracts.jsonl")
    ap.add_argument("--topics", default="data/clef_topics.json")
    ap.add_argument("--prompt", default="data/elig_prompt.txt")
    ap.add_argument("--criteria", default="data/crit_block_C.txt")
    ap.add_argument("--outdir", default="labels")
    ap.add_argument("--shard", type=int, default=None)
    ap.add_argument("--num-shards", type=int, default=1)
    ap.add_argument("--batch-size", type=int, default=2048,
                    help="rows per llm.generate call; output is appended after each")
    ap.add_argument("--limit", type=int, default=None, help="smoke test only")
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    args = ap.parse_args()

    if args.guided and args.guided_strict:
        raise SystemExit("choose one of --guided / --guided-strict")

    tag = f"{args.arm}_{args.condition}"
    if args.guided_strict:
        tag += "_guidedstrict"
    elif args.guided:
        tag += "_guided"
    if args.shard is not None:
        tag += f"_shard{args.shard}of{args.num_shards}"
    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, f"pool_labels_{tag}.jsonl")
    man_path = os.path.join(args.outdir, f"pool_manifest_{tag}.json")

    rows, missing = build_prompts(args.pairs, args.abstracts, args.topics, args.prompt,
                                  args.criteria, args.condition, limit=None)
    if args.shard is not None:
        rows = [r for r in rows if shard_of(r["topic"], r["pmid"], args.num_shards) == args.shard]
    have = done_keys(out_path)
    todo = [r for r in rows if (r["topic"], r["pmid"]) not in have]
    if args.limit:
        todo = todo[:args.limit]
    print(f"[{tag}] pairs {len(rows):,} | abstract missing {missing:,} | already done "
          f"{len(have):,} | to judge {len(todo):,}", flush=True)
    if not todo:
        print(f"[{tag}] nothing to do", flush=True)
        return

    from vllm import LLM, SamplingParams
    repo = ARMS[args.arm]
    rev = resolve_revision(repo)
    llm = LLM(model=repo, dtype=args.dtype, seed=SEED, max_model_len=args.max_model_len,
              gpu_memory_utilization=args.gpu_memory_utilization)
    sp_kwargs = dict(temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_TOKENS, seed=SEED)
    if args.guided or args.guided_strict:
        target = GUIDED_REGEX_STRICT if args.guided_strict else GUIDED_REGEX
        try:
            from vllm.sampling_params import GuidedDecodingParams
            sp_kwargs["guided_decoding"] = GuidedDecodingParams(regex=target)
        except Exception:
            try:
                sp_kwargs["guided_regex"] = target
            except Exception:
                raise SystemExit("this vLLM exposes no guided-decoding API; refusing to fall "
                                 "back to free generation silently")
    sp = SamplingParams(**sp_kwargs)

    # THE PROMPT IS NOT WHAT build_prompts RETURNS. scale_judge.py applies the model's chat
    # template to that text and, for qwen3, disables the thinking mode through the template.
    # The first version of this script imported build_prompts and skipped this step, which was
    # not a style difference: qwen3-8b then emitted a thinking block on every row and ran to
    # max_tokens, giving out_tokens median 1024 (= the cap) on 256 of 256 smoke rows, a strict
    # parse rate of 0.969 against the registered floor of 1.000, and 2.85 rows/s against the
    # 34.25 measured for this arm on the panel. The file's own docstring records that an
    # earlier arm in this project was truncated the same way. The setting goes in the manifest
    # because a run that does not record it cannot be compared with one that does.
    is_qwen3 = args.arm.startswith("qwen3")
    tok = llm.get_tokenizer()
    chat_kwargs = dict(tokenize=False, add_generation_prompt=True)
    if is_qwen3:
        chat_kwargs["enable_thinking"] = False

    n_strict = n_null = n_nonbinding = n_nonbinding_labelled = n_truncated = 0
    out_tokens = []
    t0 = time.time()
    with open(out_path, "a") as fh:
        for i in range(0, len(todo), args.batch_size):
            chunk = todo[i:i + args.batch_size]
            texts = [tok.apply_chat_template([{"role": "user", "content": r["prompt"]}],
                                             **chat_kwargs) for r in chunk]
            outs = llm.generate(texts, sp)
            for r, o in zip(chunk, outs):
                g = o.outputs[0]
                text = g.text or ""
                m = STRICT.search(text)
                label = int(m.group(1)) if m else None
                n_strict += label is not None
                n_null += label is None
                out_tokens.append(len(g.token_ids or []))
                n_truncated += g.finish_reason == "length"
                # The binding check inspects completions that finished with 'stop'. If every
                # completion was truncated instead, it inspects nothing and reports binding for
                # the wrong reason - which is what happened on the first smoke run, where
                # n_nonbinding was 0 because no completion ever finished. Truncation is counted
                # separately so the manifest cannot report a vacuous pass.
                if (args.guided or args.guided_strict) and g.finish_reason == "stop" \
                        and not TAIL.search(text.rstrip()):
                    n_nonbinding += 1
                    n_nonbinding_labelled += label is not None
                fh.write(json.dumps(dict(
                    topic=r["topic"], pmid=r["pmid"], human=r["human"],
                    title_only=r["title_only"], label=label,
                    eligible=None if label is None else int(label >= BINARISE_AT),
                    finish_reason=g.finish_reason,
                    raw=None if label is not None else _clip(text))) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            el = time.time() - t0
            print(f"  {min(i + args.batch_size, len(todo)):,}/{len(todo):,} "
                  f"| {(i + len(chunk)) / max(el, 1e-9):.2f} rows/s "
                  f"| strict {n_strict / max(n_strict + n_null, 1):.4f}", flush=True)

    wall = time.time() - t0
    med = sorted(out_tokens)[len(out_tokens) // 2] if out_tokens else None
    manifest = dict(
        arm=args.arm, family=FAMILY[args.arm.split("-")[0]], params=PARAMS.get(args.arm),
        condition=args.condition, guided=bool(args.guided),
        guided_strict=bool(args.guided_strict),
        harness="guided" if args.guided else ("guided_strict" if args.guided_strict else "free"),
        repo=repo, revision=rev, dtype=args.dtype, seed=SEED,
        temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_TOKENS, binarise_at=BINARISE_AT,
        max_model_len=args.max_model_len, shard=args.shard, num_shards=args.num_shards,
        batch_size=args.batch_size, pairs_in_scope=len(rows), judged_this_call=len(todo),
        abstract_missing=missing, strict_parsed=n_strict, nulls=n_null,
        strict_parse_rate=n_strict / max(n_strict + n_null, 1),
        out_tokens_median=med, out_tokens_max=max(out_tokens) if out_tokens else None,
        wall_seconds=round(wall, 1), rows_per_second=round(len(todo) / max(wall, 1e-9), 2),
        thinking_disabled=bool(is_qwen3),
        n_truncated=n_truncated, truncation_rate=n_truncated / max(len(out_tokens), 1),
        n_nonbinding=n_nonbinding, n_nonbinding_labelled=n_nonbinding_labelled,
        constraint_binding=(None if n_truncated == len(out_tokens) else n_nonbinding == 0),
        vllm=__import__("vllm").__version__,
        # transformers is load-bearing rather than incidental: vLLM 0.11.0 declares
        # transformers>=4.55.2 with no upper bound and 5.x removes an API it calls, so a run
        # that does not record the major version cannot be reproduced.
        transformers=__import__("transformers").__version__,
        python=platform.python_version())
    json.dump(manifest, open(man_path, "w"), indent=1)
    print(json.dumps(manifest, indent=1), flush=True)
    if n_truncated:
        print(f"\n*** {n_truncated:,} of {len(out_tokens):,} completions hit max_tokens "
              f"({n_truncated / max(len(out_tokens), 1):.1%}). Truncation on this scale is the "
              f"documented signature of the thinking mode being left on or the chat template "
              f"not being applied; it collapses throughput and puts the strict parse rate "
              f"below its floor. constraint_binding is reported as null rather than true when "
              f"nothing finished with 'stop', because the binding check would otherwise pass "
              f"by inspecting no completions at all.", flush=True)
    if n_nonbinding:
        print(f"\n*** CONSTRAINT DID NOT BIND on {n_nonbinding:,} completions "
              f"({n_nonbinding_labelled:,} of them produced a label). Amendment 6 puts a "
              f"non-binding arm OUT of the guided comparison set; only labelled non-binding "
              f"rows can contaminate a rate.", flush=True)


if __name__ == "__main__":
    main()

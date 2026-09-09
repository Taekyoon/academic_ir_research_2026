# Judge-supplied denominators in high-recall retrieval — code and labels

Reproduction material for a study of what happens to **recall** when the relevant-document
count in its denominator is supplied by a language model rather than by human assessors.

Precision is computed from what a system returned. Recall is not: it needs the number of
relevant documents in the collection, which is a judgement about documents the system never
returned. This repository holds the pre-registrations, the judge labels, and the analysis code
for measuring when that judge-supplied denominator is usable and when it is not.

---

## What is here

| | |
|---|---|
| `prereg/` | **12 pre-registration files.** Each fixes its thresholds, its falsification conditions and its reporting rules in source **before** the corresponding labels existed. Verdict lines are printed by the analysis scripts, not chosen after seeing the numbers. |
| `labels/` | **52 label files, 23,722 judgements.** Every judge label the study produced, keyed by topic and document id. |
| `code/analysis/` | Analysis scripts. Deterministic given the labels — no GPU and no API access needed. |
| `code/scale_judge.py` | Open-weight judging under the protocol in `prereg/scale_prereg.py`. Precision is **bf16 with no quantisation option** — a size that does not fit is reported as not attempted rather than run at a lower precision, so the ladder varies scale alone. Writes a manifest per run recording the resolved HuggingFace commit sha, the harness (free / guided / guided-strict), and the serving-stack versions. |
| `code/fetch_abstracts.py` | PMIDs to PubMed titles and abstracts. See **Data** below for why this is a script and not a file. |
| `data/` | Frozen samples (document ids, expert labels, strata, weights), topic metadata, and the two judging prompts verbatim. |
| `notebooks/run_colab.ipynb` | The judging run on a single GPU. |
| `scripts/` | Fetchers for the two upstream collections. |

## Reproducing

The analysis is separable from the judging. Most results can be reproduced with no GPU.

```bash
# 1 · upstream collections (not vendored - see Data)
bash scripts/fetch_clef.sh
bash scripts/fetch_trec_rag.sh

# 2 · analysis from the shipped labels - no GPU, no API keys
python code/analysis/census_analyse.py
python code/analysis/stoprule_run.py
python code/analysis/bpref_run.py

# 3 · re-produce labels with open weights - one 40 GB GPU
python code/fetch_abstracts.py --pmids data/pmids_panel.txt --out clef_abstracts.jsonl
python code/scale_judge.py --arm qwen3-8b  --condition A            # free generation
python code/scale_judge.py --arm qwen3-14b --condition C --guided   # constrained
```

`notebooks/run_colab.ipynb` runs the whole ladder one family per cell, resumable, purging each
arm's weights once both its conditions are written.

Read the matching `prereg/*_prereg.py` before interpreting any script's output. The
pre-registration states what the thresholds are, why they were set where they were, and what
each outcome licenses.

## Data — what is redistributed and what is not

**Redistributed here.** The judge labels are ours and are released with the code. The frozen
samples carry PubMed ids, expert labels, stratum membership and sampling weights.

**Not redistributed: PubMed abstract text.** The CLEF eHealth TAR collection itself ships only
PMIDs — its topic files carry a title, a boolean query and a document id list, with no abstract
text. This repository follows that convention: `code/fetch_abstracts.py` retrieves abstracts
from PubMed on demand. It keeps publisher-copyrighted text out of the repository and makes each
abstract's provenance explicit. About 7% of records have a title and no abstract body; those
rows are judged on the title and the judging script flags them `title_only` so the effect is
reportable rather than hidden.

**Not redistributed: the upstream collections.**

| Collection | Licence | How to get it |
|---|---|---|
| CLEF eHealth TAR 2017–2019 (topics, qrels, participant runs) | **MIT** (github.com/CLEF-TAR/tar) | `scripts/fetch_clef.sh` |
| TREC RAG 2024 (NIST qrels, released UMBRELA qrels) | **no licence file upstream** | `scripts/fetch_trec_rag.sh`; check the TREC data terms before use |

CLEF is MIT and could have been vendored; it is fetched instead so the provenance stays visible
and the version is the upstream one rather than a copy. TREC RAG is fetched because its data
repository carries no licence file, so we do not redistribute it.

## The open-weight ladder

Three ladders rather than one, because a single-family trend can be read as a property of that
family. Reproducibility of a **scale** trend means the trend recurs when the pretraining data,
the tokenizer and the post-training recipe all change.

| family | sizes | span | gating |
|---|---|---|---|
| Qwen3 | 1.7B · 4B · 8B · 14B | 7.3x | open |
| Llama | 3.2-1B · 3.2-3B · 3.1-8B | 6.5x | manual approval |
| Gemma | 3-1b · 3-4b · 3-12b | 12.2x | manual approval |

Parameter counts are the safetensors totals from the HuggingFace API, and the bf16 footprints are
derived from them. The device ceiling is **fixed at a 40 GB A100** by `scale_prereg.py` amendment
4, so Qwen3-32B (61 GB) and gemma-3-27b-it (51 GB) are out of scope by declaration rather than
discovered unreachable mid-run, and **no claim is made about the 27–32B range** — extrapolating a
four-point fit past its largest point is the error the withdrawn projection already made.

Two properties of the design are disclosed rather than discovered in the fit: the ladders top out
at different sizes (14B / 8B / 12b), so the Llama slope is the least constrained at the top; and
the Gemma ladder mixes `Gemma3ForCausalLM` at 1b with `Gemma3ForConditionalGeneration` at 4b and
12b, which confounds scale with architecture inside that family.

### Where it stands

**Free generation, one uniform harness, 8 of 10 arms** (Llama-3.2-1B and 3.2-3B not run). Four
arm-conditions cleared the registered 0.95 strict-parse floor. On the three Qwen3 sizes that did,
Youden J rises monotonically — and the pass is the finding, because J rises on the back of
sensitivity (+0.230 in condition A) while the false-positive rate is flat or rising (+0.076 in A,
−0.015 in C), and the admissibility gate is a condition on the false-positive rate. Usable topics
stay flat at 1 → 1 and 4 → 2 of 30.

**Cross-family replication is not yet evaluable.** Fitting a slope needs three clean sizes per
family; Qwen3 has three, Gemma one, Llama none. What blocked it was output-format compliance, not
judging quality, which is why guided decoding became the primary basis for every open arm rather
than a remedy applied only to the arms that failed.

### The harness, and one failure worth reading before you re-run

Guided decoding comes in two flavours and the choice is substantive. **Permissive**
(`[\s\S]*##[ ]?final score: [0-3]`) lets the model reason and only forbids stopping before a
valid score line, so it changes the output contract and nothing else. **Strict**
(`--guided-strict`) permits the score line alone, which for a model that emits a few hundred
reasoning tokens before answering deletes that computation — those labels are of a different
procedure and are never pooled with permissive ones.

The first guided attempt failed instructively. Its target required `## final score: ` **with** a
space while the prompt specifies `##final score:` **without** one. The strict parser tolerates
both, so labels parsed normally — but an enforced automaton could never be satisfied by the
model's natural output, so constrained arms emitted their answer and then burned tokens to the
cap looking for an accepting state (Qwen3-14B fell from 19.6 to 1.01 rows/s). Worse, the
constraint silently bound on only 8 of 16 arm-conditions, and nothing in the parse rates revealed
it, because the arms it missed simply looked like the free run.

Two guards came out of that and both are in the code. `scale_judge.py` runs an **enforcement
probe** on eight rows before judging: under a binding automaton every completion must end at the
score line, so one that stops elsewhere aborts the arm rather than producing 2,025 labels under a
harness that is not active — and the error message forbids falling back to free generation under
a `--guided` label, because the manifest would then record a run that did not happen. Cell 9b of
the notebook applies the **same-run rule** (amendment 6): the manifest fields that define an
execution — harness, dtype, seed, temperature, max_tokens, transformers version, GPU — are
checked for equality across a comparison set, and an inequality **voids the set** instead of
becoming a caveat.

## How this study is put together

Two conventions run through every experiment and are worth knowing before reading the code.

**Thresholds are fixed before the data exists.** Each `prereg/*_prereg.py` was written before
its labels were produced, and the analysis scripts print the verdict rather than leaving it to
the writer. Where a pre-registration had to be amended, the amendment is in the same file, dated
relative to what data existed at the time, with the reason.

**A comparison set is one execution.** Amendment 6 of `scale_prereg.py`: every comparison is
made among arms from one identical run — same harness, decoding parameters, seed, prompts,
session. A set that fails the equality check is void, not caveated.

**Negative results are reported.** Several pre-registered hypotheses were falsified and the
files say so: a structural proxy for evidential sufficiency, inter-judge disagreement as a
reliability signal, a prevalence-corrected estimator, and a claim that a judge-supplied
denominator rewards retrieval depth. The pre-registrations that failed are in `prereg/`
alongside the ones that held, and so are the amendments that withdrew a projection after the
capability axis came out non-monotone.

**Amendment numbering in `scale_prereg.py`.** The first amendment is inline and unnumbered, in
harness rule R3; the numbered sequence then starts at **3**, because the number was aligned with
the amendment sequence of `condC_prereg.py` when it was written. There is no amendment 1 or 2 in
this file and none has been removed — the gap is a numbering slip, recorded here rather than
closed by renumbering, since amendments 3–6 are referenced by number in the notebook and in the
commit history.

## Licence

Code and labels in this repository: MIT (see `LICENSE`). Upstream collections keep their own
terms as listed above. PubMed abstract text is not covered by this licence and is not
redistributed.

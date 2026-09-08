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
| `code/scale_judge.py` | Open-weight judging under the protocol in `prereg/scale_prereg.py`. Writes a manifest per run recording the resolved HuggingFace commit sha, quantisation and serving-stack versions. |
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

# 3 · re-produce labels with open weights - one GPU
python code/fetch_abstracts.py --pmids data/pmids_panel.txt --out clef_abstracts.jsonl
python code/scale_judge.py --arm qwen3-8b --condition A
```

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

## How this study is put together

Two conventions run through every experiment and are worth knowing before reading the code.

**Thresholds are fixed before the data exists.** Each `prereg/*_prereg.py` was written before
its labels were produced, and the analysis scripts print the verdict rather than leaving it to
the writer. Where a pre-registration had to be amended, the amendment is in the same file, dated
relative to what data existed at the time, with the reason.

**Negative results are reported.** Several pre-registered hypotheses were falsified and the
files say so: a structural proxy for evidential sufficiency, inter-judge disagreement as a
reliability signal, a prevalence-corrected estimator, and a claim that a judge-supplied
denominator rewards retrieval depth. The pre-registrations that failed are in `prereg/`
alongside the ones that held.

## Licence

Code and labels in this repository: MIT (see `LICENSE`). Upstream collections keep their own
terms as listed above. PubMed abstract text is not covered by this licence and is not
redistributed.

"""PRE-REGISTERED design for the cross-lineage judge panel.
Written and frozen BEFORE any label from a non-OpenAI judge exists.

Why this exists. Every judge measurement in this project so far used one pretraining lineage
(OpenAI), so two claims were left unsupportable: (a) whether the DIRECTION of denominator
overcounting is model-robust under expert eligibility criteria, and (b) whether judge errors
are independent ACROSS lineages, which is the whole question behind "just use more judges".
Same-lineage dependence was measured at 4.5x (two prompts of one model) and 2.6x (two
OpenAI-family models); cross-lineage was untested and could not be tested on the OpenAI key.

SAMPLE, frozen in panel_sample.csv before any new label: 2,025 pairs over 30 topics, drawn
from the condition A sample, stratified on the human label at up to 40 per stratum per topic
(825 eligible, 1,200 non-eligible). Every judge sees the IDENTICAL pairs - required for the
dependence measurement. Disclosed in advance: 5 of 30 topics have fewer than 10 eligible
documents in the panel, so their per-topic sensitivity is unstable and they must not be
dropped after seeing results.

PROMPT: identical text for every model, elig_prompt.txt, condition A form (review title, no
concept block). No per-model prompt tuning. Binarisation at >=2, as everywhere else in this
project. Decoding: temperature 0 and top_p 1 wherever the API accepts them; frequency_penalty
0.5 only on the OpenAI-compatible endpoints that accept it. Per-API differences are recorded
per row rather than harmonised away, because harness differences moving labels is itself one
of this project's findings.

LINEAGES (one model each; Groq returned HTTP 403 / Cloudflare 1010 and is excluded):
  openai      gpt-4o-mini                              (labels already exist)
  google      gemini-3-flash-preview
  anthropic   claude-haiku-4-5                          (via host.llm in a sub-agent frame)
  alibaba     qwen/qwen3-30b-a3b-instruct-2507          (OpenRouter)
  mistral     mistralai/mistral-small-24b-instruct-2501 (OpenRouter)
  meta        meta-llama/llama-3.3-70b-instruct         (OpenRouter)
  deepseek    deepseek/deepseek-chat                    (OpenRouter)
"""

# ---------------------------------------------------------------------------
# H-D1  Are judge errors independent ACROSS pretraining lineages?
#
# Registered quantity: for each subset S of judges, the rate at which ALL of them call a
# human-NON-eligible document eligible (the AND-ensemble false-positive rate), against the
# product of their individual rates (the independence prediction).
#
# DECISIVE CONDITION AGAINST THIS PROJECT'S OWN POSITION. The project currently claims that
# multiplicity cannot fix the denominator. If the AND ensemble over the available cross-lineage
# judges reaches
#         fp_AND <= 0.0199
# (the rate a denominator within 2x requires at CLEF's median eligibility rate of 0.0195),
# then multiplicity DOES fix the denominator, the earlier conclusion is OVERTURNED, and that
# is what gets reported. No reframing.
H_D1 = dict(
    quantity="AND-ensemble false-positive rate vs product of marginals",
    report_at_k=[2, 3, 4, 5, 6],
    overturn_if="fp_AND <= 0.0199 for any available lineage subset",
    threshold=0.0199,
    also_report="whether the dependence factor grows with k, which decides whether adding "
                "lineages keeps buying anything",
)

# ---------------------------------------------------------------------------
# H-M1  Is the DIRECTION of denominator overcounting model-robust under eligibility criteria?
#
# Per lineage, the per-topic relative bias of the judge-reconstructed denominator, using the
# frozen stratum weights and the exact human denominator from qrel_abs_test.txt.
H_M1 = dict(
    quantity="median per-topic relative bias of the reconstructed denominator, per lineage",
    robust_if="at least 5 of 6 lineages have a POSITIVE median",
    model_dependent_if="3 or fewer of 6 have a positive median, in which case every E1 "
                       "magnitude and direction claim must be scoped to named models",
    also_report="spread of the per-lineage medians, since the OpenAI-family comparison on web "
                "passages already showed a 5x spread (GPT-4o +0.085 vs gpt-4o-mini +0.410)",
)

# ---------------------------------------------------------------------------
# H-C1  Output-contract transfer. Not a hypothesis - a documented failure mode of this project
# (a Claude-family judge emitted reasoning despite the prompt forbidding it; max_tokens=16
# truncated replies; a JSON instruction collided with the score line). Registered as a
# reporting obligation: the STRICT "##final score: N" parse rate is reported PER MODEL, and
# models below 90% are reported as such rather than rescued with a looser pattern or dropped.
H_C1 = dict(strict_pattern=r"##\s*final\s*score\s*:?\s*([0-3])",
            report="per-model strict parse rate; no loose fallback; no silent exclusion",
            flag_below=0.90)

TARGET_FP = 0.0199
P_MEDIAN = 0.0195
BINARISE_AT = 2
N_PAIRS = 2025
N_TOPICS = 30
UNSTABLE_TOPICS_DISCLOSED = 5      # fewer than 10 eligible in the panel

if __name__ == "__main__":
    import json
    print(json.dumps(dict(H_D1=H_D1, H_M1=H_M1, H_C1=H_C1, TARGET_FP=TARGET_FP,
                          N_PAIRS=N_PAIRS, N_TOPICS=N_TOPICS), indent=1))

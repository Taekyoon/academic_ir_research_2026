"""PRE-REGISTERED design for the CLEF transfer of the denominator experiment.
Written and frozen BEFORE any judge label on CLEF exists.

Why the sample is STRATIFIED here and was not on TREC RAG. CLEF eligibility is rare
(p median 0.0195 at abstract level). A simple random sample of 70 per topic would contain
about 1.4 eligible documents, which cannot estimate sensitivity. So the sample takes ALL
eligible documents plus a random sample of the non-eligible, and records the stratum
weights so unbiased pool-level quantities are recoverable:
    R_hat = n_elig_stratum_total * (se estimated in the eligible stratum) ... etc.
Sensitivity is estimated inside the eligible stratum, specificity inside the non-eligible
stratum, and any pool-level rate is reweighted by N_stratum / n_sampled_stratum.

HYPOTHESES CARRIED OVER FROM THE TREC RAG RUN, tested here in a new domain
(expert eligibility criteria instead of web topical relevance):
  H-E1  the judge overcounts the denominator (relative bias > 0)
  H-E3  Rogan-Gladen correction of the judge does not beat a plain human subsample
Both were TRUE on TREC RAG. The transfer question is whether they hold when the judgment
task is eligibility against a review protocol rather than topical relevance.

FALSIFICATION / REPORTING RULES, fixed now:
  * If E1's relative bias is <= 0 on CLEF, H-E1 does NOT transfer and that is reported as a
    domain-dependence finding, not explained away.
  * If E3 beats E2 on relative RMSE at any n with bias within +/-0.05, H-E3 does NOT transfer
    and the judge IS usable as an auxiliary variable in the sparse regime. Reported as such.
  * Sensitivity and specificity are reported per topic with their stratum sample sizes; no
    topic is dropped for having few eligible documents without saying how many were dropped.

GRADE MAPPING, fixed now: CLEF qrels are binary (0/1). The UMBRELA-style 0-3 judge output is
binarised at >=2 for the primary analysis, matching the instrument paper's own convention and
our TREC RAG primary. The >=1 variant is reported as a secondary and is NOT used to rescue a
null, for the reason established on TREC RAG: at >=1 the agreement measure collapses onto the
base rate.
"""
SEED = 20260905
N_NONELIG_PER_TOPIC = 100     # random draw from the non-eligible stratum
LEVEL = "abs"                 # abstract screening is primary; content level is secondary
BINARISE_AT = 2


# ---------------------------------------------------------------------------
# AMENDMENT, written before any CLEF judge label exists (no result has been seen).
#
# What the CLEF distribution actually provides per topic. The 30 topic files carry
# "Topic:", "Title:" and then "Query:" followed by the review's raw database search
# strategy in Ovid syntax, 2,885-10,569 lines each. Structured eligibility criteria are
# NOT distributed: a numbered facet list parsed for exactly 1 of 30 topics (CD007431).
# So the judge can be given the review TITLE, which for a Cochrane diagnostic-test-accuracy
# review is a compressed PICO statement, but not the protocol's inclusion and exclusion
# criteria.
#
# DECLARED CONFOUND AND ITS DIRECTION. The CLEF human assessors screened with the full
# review protocol; the judge receives the title only. Any judge-human disagreement is
# therefore part information asymmetry and not purely judge capability, and the asymmetry
# is expected to push the judge toward PERMISSIVENESS, because a criterion it cannot see
# is a criterion it cannot apply. That is the same direction as H-E1, so a positive E1
# result under title-only information is NOT attributable to the judge alone.
#
# SECONDARY CONDITION, fixed now, to BOUND that asymmetry rather than assume it.
# Condition A (primary): question = review title.
# Condition B (secondary, on a fixed 600-pair subsample stratified the same way): question
#   = review title PLUS the deduplicated concept vocabulary extracted from the review's own
#   search strategy (the heads of `exp X/` and `X.tw.` style terms, capped). B gives the
#   judge more of what the human had.
# Reported comparison: relative bias of E1 under A and under B. If B's bias is materially
# lower, the A result is reported as an upper bound on judge overcounting rather than as a
# judge property. If A and B agree, the asymmetry is bounded and E1 stands as a judge
# property. Either outcome is reported.
#
# The 600-pair subsample for condition B is drawn and frozen in the same cell that writes
# this amendment, before any label exists.
N_COND_B = 600


# ---------------------------------------------------------------------------
# HARNESS NOTE, recorded before any usable CLEF label exists.
#
# The first CLEF prompt draft ended with BOTH "Produce a JSON array of scores ... Example:
# [{"O": 1}]" and "##final score: ". The model followed the JSON instruction and returned
# well-formed '[{"O": N}]' on all 132 requests (out_tok = 7 every time, zero truncation),
# so the strict "##final score" parser recorded 132 nulls out of 132. The fault was the
# prompt, not the model, and the labels were recoverable - but they were DISCARDED to
# clef_labels_A_v1_jsonformat.jsonl.discarded rather than mixed in, because they come from
# a different prompt version than the rest of the run.
#
# The prompt ending was then aligned to the UMBRELA paper's own format instruction
# ("Final score must be an integer value only ... in the format of: ##final score: score
# without providing any reasoning"), so the CLEF run and the TREC RAG run share one output
# contract and remain comparable.
#
# This is the THIRD instance in this project of the same failure mode: changing the judging
# harness for a new model family or a new domain changes the output contract, and a strict
# parser then fails silently. The first was a Claude-family judge emitting step-by-step
# reasoning despite the prompt forbidding it; the second was max_tokens=16 truncating replies
# before the score line so a loose fallback captured intermediate scores. It belongs in the
# paper as evidence that "swap the judge" is not a parameter change.

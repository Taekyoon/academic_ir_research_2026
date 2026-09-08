"""PRE-REGISTERED scope test, written before any nDCG value was computed.

THE QUESTION, from the user's annotation on the abstract: the abstract opens by claiming
"retrieval systems increasingly report recall", and asks whether that premise holds — nDCG is
what much of IR actually reports, and a paper may never measure recall at all. So:

  Does the denominator problem reach nDCG, or is it specific to recall-family measures?

WHY IT MIGHT NOT REACH nDCG. nDCG@k normalises by the ideal DCG computed from the BEST-GRADED
documents available in the judgment set. If a judge inflates relevance, both the observed DCG and
the ideal DCG rise, so the inflation partially cancels in the ratio. Recall has no such
normaliser: its denominator is the count of relevant documents and the inflation enters raw. If
that reasoning is right, nDCG should be materially LESS disturbed by judge substitution than
recall on the same documents.

WHY IT MIGHT REACH nDCG ANYWAY. Cancellation is only exact if the inflation is uniform in rank.
This project has already measured that judge false positives are NOT uniform in rank (0.258 in a
run's top 100 vs 0.153 elsewhere), and nDCG is rank-weighted, so inflation concentrated at the
top could disturb it more than the cancellation removes.

DESIGN. Identical to the bpref experiment so the numbers are directly comparable: one fixed
judged document set, the same 27 CLEF 2017 participant runs, the same 30 topics, three label
conditions (human expert qrels / judge labels on the same documents / a random-deletion control),
scored with pytrec_eval so the values are trec_eval's own. The outcome is the Kendall tau of the
27-run ranking against the ranking under human labels — the same statistic reported for recall
and bpref, so the three measures can be placed side by side.

Two nDCG variants, both reported, never pooled:
  BINARY   judge grades binarised at >=2 to 0/1, matching the human qrels' binary scale. This is
           the apples-to-apples comparison and is PRIMARY.
  GRADED   judge grades 0-3 used directly as gains against human 0/1. This is what a practitioner
           using a graded judge would actually do, and is SECONDARY.

DECISION RULE, fixed here.
  Let d = tau(nDCG@k) - tau(recall) under judge substitution, at each cutoff k, primary variant.
  d >= +0.10  -> "SCOPE TO RECALL-FAMILY": nDCG is materially more robust, so the abstract must
                 say that the problem is specific to measures whose denominator is a count of
                 relevant documents, and must not claim it for ranking measures.
  d <= +0.02  -> "REACHES nDCG TOO": the claim generalises to nDCG and the abstract may speak of
                 reported recall AND ranking quality.
  in between  -> "PARTIAL": report the numbers, scope the abstract to recall-family, and state
                 that nDCG is only partially protected.

CUTOFFS. k in {10, 20, 100, 1000} plus untruncated nDCG. Reported for all; the decision uses the
MEDIAN of d over the four cutoffs so a single cutoff cannot decide it.

DISCLOSED IN ADVANCE.
  - Human qrels here are binary, so nDCG's graded machinery has nothing to grade on the reference
    side. This is a property of the collection, not a choice, and it means the GRADED variant
    compares a graded system-side against a binary reference.
  - The judged document set is a stratified sample that oversamples relevant documents, so its
    prevalence is far above the pool's and the 1/p amplification is weak here. This test therefore
    answers "same documents, different labels", exactly as the bpref experiment did, and NOT "how
    much does the real pool move". Any comparison to the full-pool tau values (recall 0.609-0.661
    in judge_consequence.json) is a basis error.
  - Runs are NOT truncated to the judged set; each condition supplies its own qrels and the
    measures handle unjudged documents by their own definitions.
"""

D_SCOPE_TO_RECALL = 0.10
D_REACHES_NDCG = 0.02
CUTOFFS = (10, 20, 100, 1000)
BINARISE_AT = 2
DELETION_RATES = (0.25, 0.50, 0.75)
DELETION_DRAWS = 3
SEED = 20260908

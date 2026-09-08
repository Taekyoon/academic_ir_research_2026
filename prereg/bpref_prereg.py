"""PRE-REGISTERED test of the claim in object_changed_ko.md section 2.

CLAIM UNDER TEST
  bpref's robustness comes from IGNORING unjudged documents. It therefore protects against
  INCOMPLETENESS but not against label ERROR: when a judge labels the documents, bpref inherits
  the judge's mistakes wholesale. Until now this was an argument from bpref's definition, with
  no measurement behind it. This file fixes the test before any bpref value has been computed.

DESIGN
  One fixed document set, three label conditions, same 27 participant runs, same 30 topics.

    H       human expert qrels (CLEF 2017 abstract-level)
    J_best  the strongest judge arm available on those documents
    J_worst the weakest judge arm available on those documents

  and a CONTROL that exercises the property bpref was designed for:

    D25 / D50 / D75   human labels with 25 / 50 / 75 percent of the JUDGMENTS DELETED at random
                      (deleted documents become unjudged, which is exactly the condition bpref
                      claims robustness to)

  Every condition is scored on runs restricted to the SAME document universe, so completeness is
  held constant across H, J_best and J_worst and varies only in D25/D50/D75. That separation is
  the whole point: if bpref were robust to error the way it is robust to absence, the judge
  conditions would move it no more than deletion does.

METRICS
  bpref and, for reference on the identical set, recall. Computed with pytrec_eval (the trec_eval
  binding) rather than a local reimplementation, so the numbers are the field's own.

  Systems are ranked by the mean metric over topics; conditions are compared by Kendall tau
  against condition H.

DECISION RULE, fixed here before any output exists
  Let tau_J = min(tau(H, J_best), tau(H, J_worst)) and tau_D50 = tau(H, D50).

  W1  CLAIM WITHDRAWN if tau_J >= 0.85. bpref would then be substantially preserving the human
      ranking under judge labels, and section 2's assertion that it "inherits label error
      wholesale" is too strong and must be rewritten.

  W2  CLAIM WITHDRAWN if tau_J >= tau_D50. bpref would be no more disturbed by label error than
      by deleting half the judgments, i.e. error and absence would be equivalent to it, which is
      the opposite of the claim.

  S1  CLAIM SUPPORTED if tau_J < 0.85 AND tau_D50 - tau_J >= 0.10. bpref then tolerates deletion
      markedly better than it tolerates error, which is the asserted asymmetry.

  Anything else is AMBIGUOUS and gets reported as such, with no rewrite of section 2 in either
  direction.

GUARD
  G1  If the deletion control itself destroys the ranking (tau_D50 < 0.70), then this document
      set is too small for bpref to be stable at all and NO conclusion may be drawn about the
      judge conditions from it. Report the guard and stop.

DISCLOSED IN ADVANCE
  - The judged document set is the frozen stratified sample, which OVERSAMPLES eligible documents
    relative to the real pool. Prevalence inside it is therefore higher than the pool's, which
    WEAKENS the 1/p amplification. This makes the test conservative: the judge conditions are
    being given an easier setting than the operational one.
  - Restricting runs to the judged set preserves relative order but changes absolute ranks. This
    is standard condensed-list evaluation and is applied identically to every condition.
  - bpref is computed unweighted on the sample. The stratum weights that reconstruct pool
    quantities are NOT applied, because bpref has no weighted form in trec_eval. This test
    therefore answers "same documents, different labels", not "the real pool".
  - Deletion is applied to the JUDGMENT SET, not to the runs, and uses seed 20260907. Three
    independent draws per rate are averaged so a single unlucky draw cannot decide the verdict.

WHAT THIS TEST CANNOT DO
  It cannot show what bpref would do if a judge labelled the ENTIRE pool, because we do not have
  judge labels on the entire pool. The definitional argument in section 2 covers that case; this
  test covers the weaker, measurable version of it.
"""

# AMENDMENT 1 - written before any bpref value existed. The judge labels themselves pre-date this
# file (they were produced for earlier experiments) but no bpref, and no ranking under bpref, has
# been computed from them. Reason for amending: the two available label sets trade documents
# against arm coverage, and neither alone satisfies the design above.
#
#   UNIVERSE A  the 4,787-pair stratified sample. 4,762 labels, 30 topics, median 144 documents
#               per topic, every topic carrying both classes. Only ONE judge arm exists on it
#               (gpt-4o-mini, condition A - the WEAKEST arm measured). Primary universe, chosen
#               because bpref stability depends on documents per topic.
#
#   UNIVERSE B  the 2,025-pair frozen panel. Median 80 documents per topic, but carries the full
#               grade ladder, so J_best = opus_C (fp 0.031) and J_worst = haiku_A (fp 0.085) can
#               bracket the effect as the design requires.
#
# The decision rule is evaluated on UNIVERSE B, because it is the one with J_best and J_worst.
# UNIVERSE A is reported alongside as the larger-document check; if the two universes disagree in
# VERDICT, that disagreement is reported and section 2 is NOT rewritten in either direction.
#
# Runs are NOT truncated to the judged set. Each condition supplies its own qrels and bpref is
# left to handle unjudged documents by its own definition, which is the behaviour under test.

TAU_WITHDRAW = 0.85
TAU_GAP_REQUIRED = 0.10
GUARD_D50_MIN = 0.70
DELETION_RATES = (0.25, 0.50, 0.75)
DELETION_DRAWS = 3
SEED = 20260907
BINARISE_AT = 2          # judge grades >= 2 count as eligible, matching every earlier condition

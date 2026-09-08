"""PRE-REGISTERED controlled test. Two questions, one design, no LLM calls.

WHY THIS DESIGN
  Two things we could not do with real judge labels:

  (a) SEPARATE sensitivity from specificity. Every real arm moves both at once, so the
      "better judge, worse bpref" observation in two_games_ko.md is confounded - opus_C has both
      a lower false-positive rate AND a lower sensitivity than haiku_A.

  (b) REACH THE SPARSE REGIME. Both stratified samples oversample eligible documents, so the
      prevalence there is ~0.28-0.40 rather than the pool's ~0.02, and the 1/p amplification that
      the whole argument rests on is largely absent. The bpref experiment therefore ran in the
      one regime where the effect is weak.

  Flipping REAL human labels fixes both. For a target (se, sp) we keep each human-eligible
  document eligible with probability se, and flip each human-non-eligible document to eligible
  with probability 1-sp. That gives exact control over both error rates, on the REAL pool with
  its REAL prevalence, scored on the REAL participant runs.

WHAT IS SIMULATED AND WHAT IS NOT
  Simulated: the judge's error rates. Real: the documents, the pool sizes, the prevalence, the
  human ground truth, and the 27 runs being ranked.

  The simulation assumes errors are INDEPENDENT of rank. We measured that this is false for a
  real judge - inside a run's top 100 the false-positive rate is 0.258 against 0.153 overall.
  So the independent-error grid is the OPTIMISTIC case, and a second condition below injects the
  measured rank dependence. If a metric fails under the optimistic case it fails for real judges.

Q1 - IS bpref A GUARDRAIL AGAINST JUDGE ERROR?  (the reading to be tested)
  Claim: reporting bpref instead of recall protects a system ranking from judge label error,
  because bpref has no unbounded 1/p denominator term.

  Measure d = tau_bpref - tau_recall at every grid cell, both against human qrels.

  SUPPORTED   if median d >= +0.05 over the cells with sp <= 0.97 (the operationally relevant
              range - our best real arm sits at sp 0.969).
  REFUTED     if median d <= -0.05 over those cells, i.e. bpref is WORSE.
  NEITHER     if |median d| < 0.05: the two metrics are equally disturbed and bpref is not a
              guardrail, but not a liability either. This is reported as "no protection", NOT as
              support.

Q2 - WHICH ERROR RATE DOES EACH METRIC CARE ABOUT?
  At fixed sp, sweep se; at fixed se, sweep sp. Report for each metric the range of tau induced
  by each sweep. This is descriptive - there is no pass/fail - and it is what decides whether the
  two_games account (recall cares about sp via the denominator, bpref cares about se via the
  omitted-document mechanism) survives contact with a controlled design.

  The two_games account predicts: recall's tau is driven mainly by sp, bpref's mainly by se.
  If instead both are driven by the same rate, the two_games explanation is wrong and
  two_games_ko.md must be corrected.

GUARDS
  G1  The cell (se=1.0, sp=1.0) reproduces the human qrels exactly, so tau must be 1.000 for both
      metrics. Anything else means the harness is broken and no result may be read.
  G2  The measured denominator bias at each cell must track (se-1) + (1-sp)(1-p)/p. If it does
      not, the label-flipping is not producing the intended error rates.

FIXED BEFORE RUNNING
  Grid, draw count, seed, metrics, and the Q1 thresholds above. The rank-dependent condition uses
  the measured 0.258 / 0.153 split and is reported separately, never pooled with the grid.

DISCLOSED
  - Recall is computed with the SIMULATED qrels supplying the denominator, which is exactly the
    operational error under study.
  - bpref sees flipped labels as judgments, not as holes; a document the simulated judge drops
    from eligible becomes judged-non-eligible, not unjudged. That is what a judge labelling the
    pool actually does, and it is the case the definitional argument in object_changed_ko.md
    section 2 covers but our earlier experiment could not reach.
"""

SE_GRID = (0.60, 0.80, 1.00)
SP_GRID = (0.90, 0.95, 0.97, 0.99, 1.00)
DRAWS = 5
SEED = 20260907
D_THRESHOLD = 0.05
SP_RELEVANT_MAX = 0.97
RANKDEP = {"top100_fp": 0.258, "elsewhere_fp": 0.153, "top_k": 100}

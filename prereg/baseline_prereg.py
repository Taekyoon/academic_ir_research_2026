"""Baseline board - PRE-REGISTRATION.

Fixed BEFORE any B6 / B7 / B8 value exists. This file is the authoritative copy of the
verdict criteria; `baseline_design_en.md` is the engineering description and loses to this
file wherever the two disagree.

WHAT THIS FILE DOES NOT REGISTER
--------------------------------
Three comparisons are already measured and are carried as PRIOR RESULTS. Re-registering
them would be a post-hoc registration:

  * B0 vs B1  - judge-only does not beat an uninformative guess. Decided on |log error|
                (16 of 30 topics, Wilcoxon p = 0.839), source denominator_baselines.csv.
                Carried on its own metric; the board re-plots both on RMSE without
                re-deciding the comparison.
  * B2        - the exhaustive-census identity is exact (54 rows, deviation 0): variance
                removed, bias unchanged. Source census_identity.csv, census_prereg.py.
  * B3 vs B4/B5 - SRSWOR is preferred at every sample size. Source greg_faithful.csv,
                greg_prereg.py.

THE PRIMARY METRIC IS FIXED AND SINGULAR
----------------------------------------
RMSE(Rhat, R) over bootstrap replicates, then the MEDIAN across topics at each n.
|log error| is NOT used in this experiment. Reporting any registered verdict below on a
different error metric voids that verdict.
"""

# ---------------------------------------------------------------- design constants

COLLECTION      = "CLEF eHealth TAR 2017, abstract-level qrels"
N_TOPICS_EXPECTED = 30
JUDGE_LABELS    = "labels/clef_labels_gpt-4o-mini_A.jsonl"   # condition A, grade >= 2
BINARISATION    = 2            # judge grade >= 2 counts as eligible
# AMENDMENT 2, made AFTER the anchoring run and disclosed as such. Two changes, neither of
# which touches a threshold.
#
# (a) SCALING. The metric above said RMSE(Rhat, R) without stating absolute or relative. The
#     anchoring run showed the two disagree on the floor: on relative error the uninformative
#     guess (0.630) beats a 100-document expert subsample (0.692); on absolute error it does
#     not (26.0 against 22.6). RELATIVE is primary, because topic R ranges 2 to 460 so
#     absolute error is dominated by the large topics and the registered median-across-topics
#     aggregation is only coherent on a scale-free quantity. This choice runs AGAINST the
#     board's constructive story - relative is the scaling on which the zero-cost guess is
#     hardest to beat. Absolute is reported alongside and never substituted.
# (b) GRID. n* came out at 10, the first grid point, for the whole collection and for every
#     band on both scalings, so the registered grid locates it only as "at or below 10". The
#     grid is extended downward for resolution. The comparison rule, the 0.90 ratio and the
#     four-of-six requirement are unchanged; with eight points the requirement remains
#     four-of-six evaluated on the six original points, so the added points cannot change a
#     verdict.
METRIC_SCALING  = "relative"                  # primary; "absolute" reported alongside
N_GRID          = (3, 5, 10, 20, 30, 50, 75, 100)   # 10..100 inherited from greg_faithful.csv
N_GRID_REGISTERED_SUBSET = (10, 20, 30, 50, 75, 100) # the six points verdicts are counted on

# The inherited column does NOT reproduce under this definition: greg_faithful.csv rmse_E2 is
# relative but aggregated near the MEAN (ratio 0.88-0.99 to our mean, 0.64-0.70 to our
# median), consistent with it having run on the stratum-weighted pseudo-population. The three
# sampling estimators are therefore RECOMPUTED here, and the design document's claim that
# they need no recomputation is withdrawn.
BOOTSTRAP_REPS  = 1000
SEED            = 20260921

# Topics with R == 0 are excluded from RMSE and the exclusion is written to
# baseline_verdict.json. No other exclusion is permitted.
EXCLUDE_IF_R_ZERO = True

# n* = smallest n in N_GRID at which a method's median RMSE falls strictly below the B0
# point. Where no n in N_GRID qualifies, n* is the string below - never a large number.
NSTAR_NOT_REACHED = "not reached at n <= 100"

# Relevance-rate bands. Boundaries are INHERITED measurements, not new claims, and are
# properties of this collection and this judge arm.
# AMENDED. BAND_COUNTABLE was registered as the constant 0.090. That is the wrong shape:
# the countable boundary is a closed form, p* = (1-sp)/(t + 1 - se + 1 - sp), whose tolerance
# t is an input the evaluator supplies and whose se/sp come from a chosen arm. Over six arms
# and four tolerances p* spans 0.0189 to 0.1565 and the countable topic count spans 2 to 16
# of 30, so a registered constant would smuggle in two undeclared choices. The value 0.090
# is the instantiation (arm haiku_A, t = 0.5); haiku_A has the LOWEST specificity of the six
# arms, so it is the conservative case and the earlier label "best arm" was wrong.
BAND_TOLERANCE   = 0.5       # the registered DEFAULT t; any band table must state its own t
BAND_ARM         = "haiku_A" # the arm whose se/sp instantiate p*; must be stated with it
def band_countable(se, sp, t=BAND_TOLERANCE):
    """Rogan-Gladen crossing where relative bias of R-hat reaches tolerance t."""
    return (1.0 - sp) / (t + 1.0 - se + 1.0 - sp)
BAND_COUNTABLE   = 0.090     # = band_countable(0.6412, 0.9149, 0.5), retained for continuity
BAND_AUXILIARY   = 0.0088    # judge reduces the human sample at or above this; a DERIVED
                             # crossing of Var(y - p_hat) = Var(y), not a chosen tolerance


# AMENDMENT 3, made AFTER the anchoring run's own verification and disclosed as such.
# POOL EXHAUSTION. For topics whose pool is smaller than the budget, the draw covers the
# whole pool, so R-hat equals R exactly and the error is 0. Those zeros were entering the
# median. A procedure that has judged the entire pool is a census, not a sample, and its
# actual spend is N rather than n. Such topic-budget cells are therefore EXCLUDED from the
# sampling curves and logged in baseline_curves.csv under the column `exhausted`.
# Affected: 1 topic at n = 75 (CD010860, N = 94) and 2 at n = 100 (that topic plus CD008760,
# N = 64). Effect on the relative median: +0.0099 at n = 75 and +0.0378 at n = 100. It does
# not change n*, and it WIDENS the gap by which the uninformative guess leads the subsample
# at n = 100 (0.6304 against 0.7302 rather than 0.6924), so the defect had understated the
# finding rather than produced it.
EXCLUDE_POOL_EXHAUSTED = True

# AMENDMENT 4, fixed BEFORE any full-pool label exists.
# (a) AUXILIARY VARIABLE. The model-assisted, Bayesian and stratified procedures need the
#     judge's label on every pool document; it exists for 4,762 of 117,562 (4.05 per cent). The pool
#     will be judged COMPLETELY with an open-weight model at bfloat16 on one A100 40GB.
#     Scoping the board to completely judged topics was the alternative and is rejected.
#     The strata in panel_sample.csv are NOT usable for the stratified procedure: they are the
#     expert label itself (eligible <-> relevance 1 and non-eligible <-> relevance 0, no
#     off-diagonal cell), so stratifying on them would be stratifying on the answer.
# (b) DECLARED PREDICTIONS. Both run against the constructive claim.
#     P1  Fewer countable topics, not more. Open-weight p* range (0.1373-0.3361) does not
#         overlap proprietary (0.0286-0.0902); countable band predicted to fall from
#         4 topics to 3 or fewer, empty for 4 of 8 arm-conditions.
#     P2  Shrinkage toward a collection constant lowers error, not judge information. On the
#         pseudo-population GREG met the 0.90 margin at 0/6 budgets and Bayesian kappa=10 at
#         4/6; the zero-cost constant is not improved on at any tested budget on the
#         registered scaling. Mechanism: median P(no eligible document in the sample) = 0.82 at
#         n = 10 and 0.96 in the sparsest band.
#     A prediction that fails is reported as a failed prediction, not deleted.
# (c) GRID, second extension. The grid stops at 100 while the median topic needs about 613
#     for a +/-50 per cent denominator, and only 11 of 30 topics reach 0.50 relative error within
#     100. The grid may be extended upward for resolution. Verdicts remain counted on the six
#     originally registered points, so no added point can change a verdict.
FULL_POOL_JUDGE = "open-weight, bfloat16, single A100 40GB"
STRATA_FROM = "judge binary decision"   # NOT panel_sample.csv stratum, which is the expert label

# AMENDMENT 5, fixed BEFORE any H-B6 value exists. Disclosed as an amendment rather than
# presented as original: the registration fixed H-B6's threshold and its strata (the judge's
# binary decision, never the expert label) but left the ALLOCATION of the budget between strata
# free. An allocation left free is a parameter H-B6 could be satisfied by searching, which is
# the same defect Amendment 4 closed for the band tolerance, so it is fixed here.
#
# PRIMARY. Proportional allocation with at least one unit in every non-empty stratum:
#   n_h = max(1, round(n * N_h / N)) for each non-empty stratum, largest-remainder adjusted to
#   sum to n, then capped at N_h with any remainder spilled to the other stratum.
# The minimum of one is not decoration. Under pure proportional allocation the judge-eligible
# stratum holds about 7 per cent of the pool, so at the small budgets this work is about it
# draws ZERO units in most topics, the stratified estimator then counts only the other stratum,
# and what would be measured is an estimator that ignores the stratum stratification exists to
# reach. That is a property of the allocation rather than of stratification, and reporting it as
# the H-B6 verdict would test the wrong thing.
#
# SECONDARY, reported in the sensitivity grid and never substituted for the primary:
#   pure proportional (no minimum), and Neyman allocation n_h proportional to N_h * s_h with
#   s_h the within-stratum standard deviation of the JUDGE's label - never of the expert label,
#   which would be allocating on the answer.
# A verdict that holds only under some allocations is reported as CONDITIONAL ON ALLOCATION and
# may not be described as support, exactly as a tolerance-dependent band verdict may not.
HB6_ALLOCATION          = "proportional_min1"
HB6_ALLOCATION_GRID     = ("proportional_min1", "proportional", "neyman_judge")
HB6_GRID_REPORT_REQUIRED = True
HB6_STRATA_FROM         = "judge_binary"   # never the expert label

# AMENDMENT 6, at closure. Correction of AMENDMENT 2(b)'s stated rationale, not of its content.
# 2(b) justified adding the two budgets below the inherited grid with the claim that the added
# points "cannot change a verdict". That is true of WHICH points are counted - the verdict is
# scored on the six registered budgets and the two added ones are excluded from the count - and
# FALSE of their VALUES: per-cell seeding changed the draws at every budget, so the six counted
# points moved when the grid was extended. No verdict moved with them. The pre-amendment values
# are recorded in baseline_anchor_en.md sections 2 and 5, and in
# closure_certification_en.md; they are not restated here because this amendment corrects a
# rationale rather than a value.
#
# This amendment corrects a rationale. It does not alter N_GRID, N_GRID_REGISTERED_SUBSET, any
# threshold, or any verdict, and it is disclosed rather than edited into 2(b) so that the
# original wording stays readable.

# ---------------------------------------------------------------- H-B6

# Stratification beats SRSWOR at equal human budget.
#
# Test: median RMSE of B6 <= 0.90 * median RMSE of B3, at the same n.
# SUPPORTED if that holds at >= 4 of the 6 grid points.
# NOT SUPPORTED otherwise. A result between (holds at 2 or 3) is reported as PARTIAL and
# may not be described as support.
HB6_RATIO          = 0.90
HB6_MIN_GRIDPOINTS = 4

# ---------------------------------------------------------------- H-B7

# Hybrid pooling with a DEPTH split beats SRSWOR at equal human budget.
# The human budget for B7 is the number of documents judged by a human in the shallow
# depths; the judge labels the remainder. Budgets are matched by COUNT, not by depth.
HB7_RATIO          = 0.90
HB7_MIN_GRIDPOINTS = 4

# Fidelity disclosure, registered so it cannot be quietly dropped: the SIGIR 2026 full text
# has not been read. B7 is "depth-split hybrid pooling as we understand it" and every
# reported B7 result must carry that qualifier.
HB7_FIDELITY_DISCLOSURE = "full text unread; reimplementation from summary"

# Harness guard, from a failure already suffered in this project: the participant-runs
# directory contains a non-run binary file which parsed as spurious topics and, being
# alphabetically first, silently degraded a rank-dependent condition. Every file must parse
# as `topic-id 0 pmid rank score run-id`; rejects are written to
# baseline_rejected_runs.csv with a reason. A stage that rejects zero files AND reads fewer
# than MIN_RUNS runs is an ERROR, not a pass.
MIN_RUNS = 20

# ---------------------------------------------------------------- H-B8 (optional)

# MTC-style adaptive selection beats SRSWOR at equal human budget.
# Registered now so that running it later is not a post-hoc addition. If it is not run,
# baseline_verdict.json records "NOT ATTEMPTED" and no claim about it may appear anywhere.
HB8_RATIO          = 0.90
HB8_MIN_GRIDPOINTS = 4
HB8_IS_ADAPTATION  = True   # Carterette 2006 targets confidence bounds on ranking metrics,
                            # not a count. Any report must state this is an adaptation.

# ---------------------------------------------------------------- H-BAND (the load-bearing one)

# The selection rule has content: allocating method by relevance-rate band beats the best
# single fixed method applied to every topic.
#
# BANDED is constructed by, for each topic, using the method the band assigns; BEST_FIXED is
# the single method with the lowest median RMSE across all topics at that n.
#
# SUPPORTED if median RMSE of BANDED <= 0.90 * median RMSE of BEST_FIXED at >= 4 of 6 grid
# points.
#
# FALSIFIED if BEST_FIXED is <= BANDED at every grid point. On falsification the paper's
# constructive claim reduces to "nothing beats random sampling", the band table becomes
# DESCRIPTIVE ONLY, and the selection rule may not be presented as a contribution.
HBAND_RATIO          = 0.90
HBAND_MIN_GRIDPOINTS = 4

# TOLERANCE IS NOT A FREE PARAMETER OF H-BAND.
# The countable boundary is p* = band_countable(se, sp, t), so leaving t open would let
# H-BAND be satisfied by searching it: over the six arms and four tolerances already
# tabulated in band_boundary_sensitivity.csv, p* spans 0.0189 to 0.1565 and the countable
# topic count spans 2 to 16 of 30. Therefore:
#   1. The band assignment under test is FIXED to (BAND_ARM, BAND_TOLERANCE) above.
#   2. The verdict is recomputed over the whole arm x tolerance grid and written to
#      baseline_band_sensitivity.csv. This is a REQUIRED output, not an optional check.
#   3. If H-BAND holds at the registered instantiation but not across the grid, the verdict
#      is reported as CONDITIONAL ON t, never as support.
#   4. Changing BAND_ARM or BAND_TOLERANCE after any RMSE has been computed is a new
#      registration, not an amendment to this one.
HBAND_GRID_REPORT_REQUIRED = True

# ---------------------------------------------------------------- reporting obligations

# 1. Every verdict echoes the threshold it was tested against into baseline_verdict.json.
# 2. The countable boundary is reported as the function band_countable(se, sp, t) with its
#    instantiation named; the auxiliary boundary is reported as a derived crossing of
#    Var(y - p_hat) = Var(y). They are not presented as a matched pair of thresholds.
# 5. Any topic count per band carries the (arm, t) that produced it.
# 3. A method's absence from a band is reported as "not assessed", never as a loss.
# 4. Prior results (see the docstring) are plotted and labelled as prior; they are not
#    re-tested and their verdicts are not restated as new findings.

REGISTERED_AT = "2026-09-21, before any B6/B7/B8 value existed"

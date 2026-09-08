"""PRE-REGISTERED, written before any census quantity was computed.

QUESTION, in the user's words: is there an approach that judges the WHOLE pool instead of
sampling it?

The answer splits three ways, and only the third is an open empirical question. This file fixes
the tests before any number exists.

--------------------------------------------------------------------------------------------
C1  IS THE PROJECTION IDENTITY EXACT UNDER A CENSUS?

Everything the project has reported about the denominator runs through
    R-hat = R*se + (N-R)*(1-sp)
estimated from a stratified SAMPLE, so both the judge count and the two rates carried sampling
error - the 40-document non-eligible strata gave fp confidence intervals wide enough (0 to 624
false positives on one topic) that the project could not tell whether a disagreement between the
identity and the labels was real.

Under a census none of that error exists: every pool document carries both a human label and a
judge label, so se and sp are POPULATION quantities and the judge's relevant count is an
observed integer. The identity should then hold EXACTLY. TREC RAG 2024 supplies exactly this
situation - the released UMBRELA qrels cover the same pairs the NIST assessors judged.

Registered outcome. Compute, per topic and per binarisation threshold, the maximum absolute
difference between the observed census judge count and R*se_census + (N-R)*(1-sp_census).
    max abs difference <= 1e-6  -> "IDENTITY EXACT": a census removes all ESTIMATION error and
        what remains is pure bias, computable in closed form with no sample at all.
    otherwise -> report the discrepancy; the identity is not the right description of a census
        count and the project's framing needs revision.
This is a verification, not a discovery: the point is that it must be checked on real data
rather than asserted, because every earlier check was confounded by sampling error.

--------------------------------------------------------------------------------------------
C2  DOES A CENSUS REMOVE THE PROBLEM?

If C1 holds, the census judge count still carries the bias term (se-1) + (1-sp)*(1-p)/p, which
does not contain the sample size and therefore cannot be reduced by judging more documents.
Registered outcome: report, over the census topics, the relative denominator bias and the count
of topics whose census denominator lands within +/-50% of truth. No threshold - this is the
descriptive answer to "does a census fix it".

--------------------------------------------------------------------------------------------
C3  DOES A CENSUS RESCUE THE CORRECTED ESTIMATOR?  (the genuinely open question)

Earlier the project pre-registered and rejected a prevalence-corrected estimator: it lost to a
plain human subsample at every subsample size. But in that test the JUDGE COUNT was itself
estimated from the same small sample, so the correction inherited two sources of variance.
Under a census the judge count is exact and the only remaining variance is in se and sp. That is
a different estimator and it has never been tested.

Design, at human-subsample sizes n in {10, 20, 30, 50, 75, 100} per topic, 400 replicates:
    E_human    N * rate_human(subsample)                       - unbiased, high variance
    E_census   Rogan-Gladen correction of the EXACT census count using se, sp from the same
               subsample:  (R_hat_census - N*(1-sp)) / (se - (1-sp))

DECISION RULE, fixed in advance and IDENTICAL to the earlier sampled comparison so the two are
comparable:
    E_census is preferred over E_human at a given n only if
      (a) its relative RMSE over topics is LOWER than E_human's at the same n, and
      (b) its relative bias is within +/-0.05.
    If E_census does not beat E_human, the constructive proposal stays "pay for a probability
    sample" and the census adds precision to the DIAGNOSIS but not to the estimate.
    If it does beat E_human, the constructive proposal CHANGES: judge the whole pool, then buy a
    small human sample for calibration only - and the price list must be recomputed.
Unstable replicates (estimated se <= 1-sp, denominator non-positive) are counted and reported,
not silently dropped.

--------------------------------------------------------------------------------------------
DISCLOSED
  - The census is over the HUMAN-JUDGED POOL, not the whole corpus. Documents no system
    retrieved are outside it. So "census" here means "every document that was judged", which is
    the strongest census available from a released collection and is what a reviewer screening
    a retrieved pool actually faces.
  - Rows with n_outside_human_pool > 0 are excluded from C1, because for those the released
    judge file covers pairs the humans did not judge and the identity's inputs are undefined.
  - TREC RAG is a WEB-PASSAGE collection with a base relevance rate far above CLEF's. C2's
    answer is therefore reported per threshold and alongside the CLEF prevalence range, not
    generalised.
  - Two binarisation thresholds are reported separately (>=1, the distributed recipe's default,
    and >=2, the UMBRELA paper's own convention). They are never mixed.
"""

IDENTITY_TOL = 1e-6
SUBSAMPLE_SIZES = (10, 20, 30, 50, 75, 100)
N_REPS = 400
SEED = 20260908
BIAS_TOL = 0.05
USABLE_BAND = 0.5
THRESHOLDS = (1, 2)

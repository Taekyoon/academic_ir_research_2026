"""PRE-REGISTERED comparison: does a MODEL-ASSISTED estimator using the LLM judge as the
auxiliary variable beat a plain human random subsample at the same cost?

Motivation. Di Nunzio (WWW 2026, doi 10.1145/3774905.3795598) states our problem verbatim - true
recall is unknown without judging everything and sampling to estimate it is prohibitively costly
at low prevalence - and answers it with two estimators, named in the abstract as (i) a Bayesian
prevalence estimator treating the ranker as an informative prior updated by a random sample and
(ii) a model-assisted estimator, specifically a generalized regression estimator (GREG) with a
Horvitz-Thompson residual correction, combining calibrated ranker probabilities with design-based
adjustment. The paper's full text is behind bot protection on both ACM DL and the Padua
repository, so this is NOT a reproduction of their estimator. It is the standard GREG/HT
estimator from survey sampling, with one deliberate substitution: their auxiliary variable is a
RANKER score, ours is the LLM JUDGE's label - the instrument this project critiques.

WHY THIS MATTERS TO OUR CLAIM, stated before running it. GREG is design-unbiased no matter how
biased the auxiliary is; bias in the judge enters only through the residual term, which the
probability sample corrects. So the correct reading of our own result may be narrower than we
have been stating: "an LLM judge cannot COUNT the denominator" is a statement about using the
judge ALONE (our E1). It does not follow that the judge is useless for ESTIMATING the
denominator. If GREG with the judge as auxiliary beats a plain human subsample at equal n, then
our price list is an overestimate and the constructive part of our paper must change.

ESTIMATORS, all targeting R = the number of truly eligible documents in a topic's judged pool.
  E1  judge alone      R_hat = sum over pool of 1[judge grade >= 2]          (no human labour)
  E2  human SRS        R_hat = N * mean(y) over a simple random sample       (design-unbiased)
  E4  GREG + HT        R_hat = beta_hat * X_total + (N/n) * sum(y_i - beta_hat * x_i)
                       with x_i = 1[judge grade >= 2], X_total = sum of x over the pool,
                       beta_hat fitted on the sample. Design-unbiased for any beta_hat.

DECISION RULE, fixed before any output of this computation exists:
  E4 is PREFERRED over E2 at a given n only if
    (a) relative RMSE over topics is LOWER than E2 at the same n, AND
    (b) relative bias is within +/- 0.05.
  If E4 does not beat E2, report that the judge adds nothing as an auxiliary and the price list
  stands. If E4 DOES beat E2, report the reduced price list and narrow our claim to E1 only -
  do not explain the result away.

SECONDARY, also fixed now: report the variance-reduction ratio var(E4)/var(E2) against each
topic's eligibility rate p, to test whether the judge's usefulness as an auxiliary itself decays
with prevalence. Registered expectation: it DOES decay, because the judge's false-positive
contribution grows as 1/p while its true-positive contribution does not.

SIMULATION ASSUMPTION, disclosed: judge labels exist only on the frozen stratified sample, not on
the whole pool. Each topic's pool is therefore reconstructed as a pseudo-population by expanding
each sampled document by its stratum weight, so a document's judge label stands in for the
unsampled documents its stratum weight represents. Prevalence of the pseudo-population equals
the pool's by construction. This assumption is what makes X_total computable and it is the main
threat to the result.
"""
N_REPS = 400
SEED = 20260906
SUBSAMPLE_SIZES = [10, 20, 30, 50, 75, 100]
PREFER_E4_IF = "rel_RMSE(E4) < rel_RMSE(E2) at same n AND |rel_bias(E4)| <= 0.05"
BINARISE_AT = 2

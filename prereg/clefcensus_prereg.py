"""PRE-REGISTERED CLEF census. Written before any new census label existed.

WHAT THIS ADDS over the TREC RAG census already run. That census settled three things - the
projection identity is exact under a census (max abs diff 0.00 over 54 rows), the bias does not
shrink (relative bias +0.411 / +0.258 median), and an error-free judge count does not rescue the
corrected estimator. But it was a WEB-PASSAGE collection at relevance rate 0.25-0.54, i.e. the
dense regime and a "relevant" criterion rather than an expert eligibility criterion. This
experiment carries the same questions into CLEF eHealth TAR 2017: expert eligibility, and
relevance rates 0.036-0.202.

--------------------------------------------------------------------------------------------
THE STRUCTURAL FACT THAT DEFINES THE SCOPE, established before designing this

The stratified panel capped the eligible stratum at 40 per topic. Five of these six topics have
FEWER than 40 eligible documents, so the panel already contains every eligible document in the
pool:

    topic      pool   R   eligible in panel   non-eligible in panel -> census
    CD008760     64  12          12 = all              40 ->  52
    CD010860     94   7           7 = all              40 ->  87
    CD010705    114  23          23 = all              40 ->  91
    CD010896    169   6           6 = all              40 -> 163
    CD010775    241  11          10 of 11              40 -> 230
    CD010772    316  47          40 of 47              40 -> 269

So SENSITIVITY is already a census quantity on four of six topics, and the census buys almost
nothing there. What it buys is SPECIFICITY: the non-eligible denominator grows from 40 to
52-269. That is precisely the quantity whose sample confidence interval was unusable - on one
topic 0/40 false positives gave a 95% interval of 0 to 624 false positives. The experiment is
therefore targeted at the one rate the project could not pin down, and its scope should be
stated that way rather than as "a census of everything".

--------------------------------------------------------------------------------------------
X1  DOES THE SAMPLED SPECIFICITY MATCH THE POPULATION SPECIFICITY?

This is the primary question and it is an audit of the project's own apparatus. Every
denominator number in this project came from a 40-document non-eligible stratum. Here the
population value becomes available.

Registered outcome, per topic and pooled over the six:
    |sp_sample - sp_census| <= 0.02  on at least 5 of 6 topics  -> "APPARATUS VALIDATED": the
        sampled rates are usable and the project's numbers stand as reported.
    |sp_sample - sp_census| > 0.05  on 3 or more topics  -> "APPARATUS NOT VALIDATED": every
        per-topic sampled specificity in the project must be reported with its interval and the
        point estimates withdrawn.
    anything else -> "PARTIAL", reported as such, no promotion either way.
Reported either way, including if it goes against the project. The sampled sp is recomputed from
the frozen panel rows for these six topics; the census sp is computed on the full non-eligible
set.

X2  DOES THE DENOMINATOR VERDICT CHANGE?
For each topic, is the pool "usable" (|relative bias| <= 0.5) under the sampled rates and under
the census rates? Report the 2x2 of agreements and disagreements. No threshold; this is the
decision-level consequence of X1.

X3  DOES THE BIAS-PREVALENCE RELATION HOLD AT CENSUS?
Spearman rho(relevance rate, relative bias) over the six census topics, reported beside the
30-topic sampled value of -0.688. Six points is too few for inference and the correlation is
reported as descriptive only, with the p-value shown but not used for any decision.

--------------------------------------------------------------------------------------------
RISK MITIGATIONS, fixed here

M1  A PARTIAL CENSUS IS NOT A CENSUS. Frames are ordered so each frame completes WHOLE topics,
    smallest pool first. If quota runs out, the result is a complete census on some topics
    rather than a partial census on all six. Topics that do not complete are reported as not
    attempted, never as measured.

M2  HARNESS REUSE MUST BE VERIFIED. 338 of the 998 pool documents already carry opus_C labels
    from the panel run. Reusing them is only valid if the harness is identical. Before the main
    run, 30 already-labelled documents are RE-JUDGED with the new harness and exact-grade
    agreement is computed. Agreement >= 0.95 -> reuse the 338. Below that -> discard them and
    judge all 998, and report the disagreement as a harness-drift finding.

M3  COST ESTIMATES HAVE BEEN WRONG TWICE (once by 2.6x). A 16-row pilot measures tokens per row
    before frames are sized, and frames are sized from the measured value with 30% headroom.

M4  MISSING ABSTRACTS. 8.3% of the frozen sample has a title but no abstract body. The same rate
    applies to the new documents, so this is a property of both sample and census and not a
    confound between them - but the per-topic count of title-only documents is reported, and X1
    is recomputed excluding them as a robustness check.

--------------------------------------------------------------------------------------------
DISCLOSED LIMITS
  - THE SIX TOPICS ARE DENSER THAN CLEF'S MEDIAN. Relevance rates 0.036-0.202 against a
    30-topic median of 0.0195. This is not a sampling choice but a structural one:
    rho(pool size, relevance rate) = -0.647, so small pools ARE dense pools. The very sparsest
    topics cannot be censused at any budget, and that is itself a reportable result rather than
    a limitation to apologise for.
  - PER-TOPIC SENSITIVITY IS COARSE. With R = 6, 7, 11, 12, 23, 47 the population sensitivity
    takes values in multiples of 1/R, so at CD010896 the grid is 0.167 wide. Statements about
    sensitivity are made only at pooled level.
  - THE EXPECTED VALUE OF THIS EXPERIMENT IS AN AUDIT, NOT A HEADLINE. If X1 validates the
    apparatus, the finding is "the sampled rates were sound", which is a confirmation and must
    not be dressed up as a discovery.
"""

TOPICS = ["CD008760", "CD010860", "CD010705", "CD010896", "CD010775", "CD010772"]
SP_MATCH_TOL = 0.02
SP_FAIL_TOL = 0.05
N_MATCH_REQUIRED = 5
N_FAIL_TRIGGER = 3
REUSE_AGREEMENT_MIN = 0.95
REUSE_CHECK_N = 30
USABLE_BAND = 0.5
BINARISE_AT = 2
PILOT_ROWS = 16
SEED = 20260908

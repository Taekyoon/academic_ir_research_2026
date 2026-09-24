# Experiment record — the baseline board for the recall denominator

**Purpose.** To establish whether the number that recall is divided by can be obtained from a
language model's judgments, and if it cannot, what obtaining it another way costs.

**Status: closed with no further measurement.** The declaration, in the words
the third certification fixed:

> "The hypothesis verification of the baseline board is closed with no further measurement: H-BAND is withdrawn as a registration defect found by audit and is neither supported nor falsified, H-B6 is not supported, H-B7 and H-B8 are not attempted with no verdict, the plan's null hypothesis is measured against but is not a registered verdict, and the declared predictions close as recorded clause by clause in baseline_verdict.json, which echoes the threshold each was tested against."

It rests on `closure_certification_3_en.md`, which cleared fourteen of sixteen blockers and named
the two that remained, and on those two being cleared afterwards — the registration pointer moved
to v9 and a mechanism claim removed from `user_benefit.csv`. **Those two edits were not themselves
re-certified.** This document replaces the working plan it grew
out of. The working plan reached its twenty-sixth version, twenty-five revisions after the original, and carried statements that its own later
sections falsified; rather than patch again, the record is written once in the state the
hypothesis verification actually ended in. Verdicts live in `baseline_verdict.json`; the
authoritative thresholds live in `prereg/baseline_prereg.py`, which is authoritative wherever it
and this document disagree; the admissible form of this closure was ruled in
`closure_ruling_en.md` and audited in `closure_certification_en.md`.

---

## 0. Problem setup

Recall needs a denominator — the number of relevant documents in a collection — and that number is
a judgment about documents no system returned. Where it cannot be had, high-recall evaluation is
built to avoid needing it. A language model changes what it costs to obtain, not whether it can be
obtained, so the question is whether the labels it produces support the quantity that is then
divided by them.

The instrument is CLEF eHealth TAR 2017 at the abstract level: **30 topics**,
**117,562 topic-document pairs**, expert qrels as truth. It was chosen because the
eligibility rate varies across topics by a factor of **694** —
0.00029 to 0.2018, median 0.0195 — which is the span the argument
needs. The collection is the measuring environment, not the object of study.

Three arms of judge labels are in play and no statement about "the judge" may stand unqualified:
`qwen3-8b`, condition C, permissive guided decoding, bfloat16, one A100 40GB produced the pool-wide labels; `haiku_A`, condition A, tolerance 0.5 supplies the band assignment; `gpt-4o-mini`, condition A is
the registered `JUDGE_LABELS`, a stratified sample of 4,762 pairs rather than a census.

**Two arms, and one pair of look-alike numbers that are not comparable.** The board's
judge-only reference point comes from the registered `JUDGE_LABELS` arm (`gpt-4o-mini`, condition A, per-topic
rates se 0.8486 and sp 0.8794); it is a **relative error** of **4.126**, the median of
`|(R̂_judge − R)/R|`, and not an over-count ratio. The arm later run over the whole pool
(`qwen3-8b`, condition C) over-counts the denominator by a factor of **4.006**, which is
`1 + rel_bias`. The two figures resemble each other and **must not be compared**: they are
neither the same quantity nor the same arm. On one convention the arms read
**5.126 against 4.006** as over-count factors, 27.9% apart. What the board does
mix by design is the source: every reference point and every derived budget threshold is on the
former arm, every auxiliary variable on the latter.

**Bias identity.** `R̂ = R·se + (N−R)(1−sp)` is a definition, not an estimate, and it is the
Rogan–Gladen relation applied to the recall denominator rather than a new formula. The relative
bias it implies is amplified by the inverse of the eligibility rate, which is why the same judge
is usable on dense topics and not on sparse ones.

## 1. Hypotheses and their dispositions

All four registered hypotheses and both declared predictions are closed. None required further
measurement to close.

**Band selection** *(primary, `HBAND`)* — *"The selection rule has content: allocating method by relevance-rate band beats the best
single fixed method applied to every topic. BANDED is constructed by, for each topic, using the
method the band assigns; BEST_FIXED is the single method with the lowest median RMSE across all
topics at that n."*
**WITHDRAWN as a registration defect found by audit. Neither supported nor falsified, and never
tested.** Three independent defects, each recorded in `baseline_verdict.json`. No map from band to procedure is registered anywhere, so the
banded procedure is not a determinate object and a three-band-by-nine-procedure assignment is a
larger free parameter than the tolerance the anti-search clause protects. And `BEST_FIXED` is
defined *at that budget*, while three of the board's procedures have no value at a budget and two
others have no curve at all — so the comparator population cannot be identified without choosing
it after seeing which procedures ran. And the registered comparison does not state whether a band
that assigns a zero-budget procedure spends nothing or spends `n`, so the budget axis the
comparison runs along is undefined for part of the assignment space. Because the hypothesis was never tested, the FALSIFIED
branch did not fire and its consequence text does not apply.

**Stratification** *(`HB6`)* — *"Stratification beats SRSWOR at equal human budget"*, scored as
*"median RMSE of B6 <= 0.90 * median RMSE of B3, at the same n"*, SUPPORTED at four or more of six
grid points. **NOT SUPPORTED**: 1 of 6 at the registered primary allocation,
2 of 6 and 1 of 6 at the two sensitivity allocations, so the verdict is not
conditional on allocation.

**Depth-partitioned pooling** *(`HB7`)* — **NOT ATTEMPTED, no verdict.** Nothing may be said about
this procedure in either direction, including that it is untested in a way that implies a result.

**Adaptive selection** *(`HB8`)* — **NOT ATTEMPTED**, recorded in `baseline_verdict.json` as the
registration requires.

**Null hypothesis** — *"No procedure attains a lower RMSE than simple random sampling at equal
budget."* **Measured against; not closed as a registered verdict.** The shrinkage estimator at
prior weight 50 attains at most 0.90 times random sampling at 6 of the 6 registered budgets, which
is the measurement this hypothesis asks for as worded here. But this null is registered in the
working plan only: `baseline_prereg.py` states no null hypothesis, places the
random-sampling-against-estimators comparison under *what this file does not register*, and forbids
restating those verdicts as new findings. The prior weight is also a free parameter no registration
fixes, and the comparison against the zero-cost constant is not an equal-budget statement.

**Declared prediction 1** — fewer countable topics, not more. **FALSIFIED WITH THE DIRECTION
REVERSED** for the arm that was run: the boundary measured pool-wide is **0.0706** against a
predicted 0.1373 to 0.3361, and the countable band **widens** from 4 topics to
5. The clause about eight arm-conditions is **NOT DECIDED** — only the registered arm was run
over the pool, and the other seven still carry panel-measured rates.

**Declared prediction 2** — shrinkage toward a collection constant, not information from the judge.
Two clauses **HOLD** (the model-assisted estimator at 0 of 6, unchanged from the
pseudo-population; the shrinkage arm at prior weight 10 at 5 of 6 in-run and 4 of 6 against the anchoring
realisation of the comparator, at or above the predicted 4 on either). One is **FALSIFIED and closed as conditional on an unregistered prior weight**: the
zero-cost constant at 0.6304 is improved on from `n` = 5. The registered mechanism clause —
*"median P(no eligible document in the sample) = 0.82 at n = 10 and 0.96 in the sparsest band"* —
is **NOT MEASURED**; the judge-derived against judge-free shrinkage-target comparison reported in
§6 is an unregistered substitute for it and does not close it.

## 2. Method

For one topic, each procedure receives the pool of size `N`, the judge's label on every pool
document, and a budget of `n` expert judgments; it returns a single number `R̂`. The expert qrels
supply the true `R`, so the error is observed directly rather than estimated. Six steps.

1. Fix the topic set and the pool: every topic with `R` > 0, every pair with an abstract.
2. Draw `n` documents without replacement and reveal only their expert labels.
3. Each procedure computes `R̂` from what it is allowed to see.
4. Repeat 1,000 times per topic and budget, seeded per cell so that a procedure added later
   sees the same draws.
5. Reduce within a topic to relative RMSE — `sqrt(mean((R̂ − R)² )) / R` — the registered metric.
6. Reduce across topics by the **median**, and compare procedures at equal `n`.

**Scaling.** The registered metric is relative. The absolute scaling reverses the ordering at the
largest budget, and the choice of relative was made after both were seen to disagree; it is
conservative for every claim the board makes, and it is a permanent disclosure rather than a
resolved question (§9).

**The two smallest budgets were added after the anchoring run.** Amendment 2(b) extended the
inherited grid downward to 3 and 5; the verdicts are scored on the six registered budgets only,
but `n*` = 5 and the budget at which the floor is cleared both fall on an added point. Amendment 6
records what 2(b)'s own rationale got wrong about this (§9).

**Exclusions.** `EXCLUDE_IF_R_ZERO` fired on **no topic** — the minimum is `R` = 2, so all
30 are retained. `EXCLUDE_POOL_EXHAUSTED` removed **3 cells** where `n` reaches the pool
size: `CD008760` at n = 75, `CD008760` at n = 100, `CD010860` at n = 100.

## 3. Procedures compared

Nine procedures, in three groups by what they consume.

**Consume no expert judgments.** The judge's own projection of the denominator; an uninformative
guess that reports the collection's median `R` for every topic; and an exhaustive judge census.
These are points, not curves — they have no value at a budget.

**Consume expert judgments only.** A random expert subsample, which is the registered comparator
for every other procedure and the only estimator on the board that is unbiased by construction.

**Consume both.** A model-assisted estimator and a Bayesian shrinkage estimator at two prior
weights, both transcribed from the lineage of the earlier faithful implementation rather than
rewritten, so that only the population and the aggregation changed; a stratified subsample whose
strata are the judge's binary decision; depth-partitioned hybrid pooling; and adaptive selection.
The last two have no curve.

The three procedures that consume both were blocked until the pool had a judge label on every
document, which it now does.

## 4. Data

One dataset is the experiment. CLEF eHealth TAR 2017 abstract-level qrels supply `N`, `R` and the
truth; the pool-wide judge labels supply the auxiliary variable; the registered stratified sample
supplies the judge-only projection, which is therefore a **projection on 29 of 30 topics and not a
census**; and 27 participant runs with ranks, the count recorded in `judge_consequence.json`, would be needed only by depth-partitioned pooling,
which was not attempted.

**Abstracts.** 99,304 unique PubMed records back the 117,562 pairs — the distinct `pmid` count in `clef2017_abs_test.qrels` — fewer than the pairs, because a
record can belong to several topics. **117,553 pairs were labelled**; the remaining 9 have no
abstract record and are absent from the labels, 0.008 per cent of the pool.

## 5. Execution

The board requires **no new judgments and no accelerator**: the labels, the sampling frame and the
expert qrels all exist, and the dependencies are numerical only. The pool-wide judging run that
produced the auxiliary variable did need one card and is recorded in `pool_results_en.md`.

## 6. Results

**The pool-wide judging run.** The registered arm labelled 117,553 of 117,562 pairs at a strict parse
rate of **1.0000** with zero nulls, and every completion finished at the score line, so truncation
was zero and the constraint-binding check inspected real completions rather than passing on an
empty set. Pool-wide the arm reads **se 0.6419, sp 0.9348**, and the denominator it implies
over-counts by a median factor of **4.006**, over-counting on **29 of 30** topics.

**Why declared prediction 1 failed in the opposite direction.** Its inputs were rates measured on
the frozen stratified panel, and that panel's non-eligible stratum is twice as hard as the pool:
false-positive rate **0.1292** on panel pairs against **0.0645** outside, from one run and one set
of labels. Run-to-run variation on the same pairs is **0.0025** — four-grade label agreement
0.9906, binarised 0.9960 — so composition outweighs execution by a factor of 26. Sensitivity moves
the other way, 0.6764 inside against 0.6143 outside, so the panel shifts both rates. The
registered band instantiation was measured on that same panel, so **the registered boundary is
exposed in a known direction**; correcting it is a new registration, not an amendment, and the
band assignment stands as registered for anything already counted.

**The probability-sample procedures, on the registered metric.** Ratios to the random expert
subsample at the six registered budgets:

| procedure | n = 10 | 20 | 30 | 50 | 75 | 100 | meets 0.90 |
|---|---|---|---|---|---|---|---|
| model-assisted | 0.944 | 0.938 | 0.947 | 0.960 | 0.933 | 0.922 | **0 of 6** |
| shrinkage, prior weight 10 | 0.513 | 0.674 | 0.755 | 0.849 | 0.882 | 0.920 | **5 of 6** |
| shrinkage, prior weight 50 | 0.280 | 0.390 | 0.444 | 0.548 | 0.628 | 0.703 | **6 of 6** |
| stratified, judge strata | 0.889 | 0.950 | 0.928 | 0.957 | 0.965 | 0.951 | **1 of 6** |

These are a recomputation of the three sampling estimators under the registered metric on the real
population; no prior verdict is restated as a finding. The earlier numbers were computed on a
stratum-weighted pseudo-population rebuilt from a 4.05 per cent sample and aggregated by the
mean where the registered metric takes the median.

**The floor.** The shrinkage arm at prior weight 50 goes below the zero-cost constant at 0.6304
from **`n` = 5** (0.6270, reaching 0.5130 at a hundred judgments) — the first board row
ever to do so. **This is conditional on the prior weight**: at weight 10 the constant is never
beaten within the grid. It also costs bias, median relative bias running to
0.077 against 0.008 for random sampling, so a practitioner who needs an unbiased
count is not served by it.

**What the judge's part in that actually is** — an unregistered substitute for prediction 2's
mechanism clause, not a closure of it. Replacing the judge-derived shrinkage target with a
judge-free collection constant is **worse by 20 per cent at `n` = 3 and better by
6 per cent at `n` = 100**, crossing between 20 and 30 judgments. The judge buys a
topic-specific prior mean at small budgets and nothing beyond that.

**Why stratification does not pay, and the correct scope of that explanation.** The judge's
sensitivity of 0.6419 leaves **35.8 per cent of the eligible documents in the stratum
holding 92.6 per cent of the pool** — 108,822 documents at an internal rate of
0.0061 against 8,731 at 0.1365. The weighted within-stratum variance therefore falls
only 7.5%, and the design effect for the standard deviation — the quantity an RMSE
inherits — is 0.96166, a reduction of 3.8 per cent. That figure is a pooled, large-sample design effect for the standard deviation of a
proportional-allocation sample mean; **it explains why the typical gain is a few per cent and does
not bound the registered quantity**, which is a median of per-topic relative RMSE at integer
budgets where allocation is not exactly proportional. Per topic the variance ratio has median
0.9213 over the range 0.5886 to 0.9994, a variance reduction of 7.9 per cent at the median topic and therefore an RMSE gain of 4.01 per cent. Whether
an allocation outside the registered grid could reach ten per cent is **unmeasured**.

Two bases are reported wherever a ratio is quoted, because they differ: the **ratio of medians**,
which the registered test uses, never falls below 0.7536 at any registered budget under any
of the three allocations, and the median of per-topic ratios, the other basis, never below 0.8605.

**The derived reported quantity.** `n*`, the smallest budget at which a procedure's curve falls
below the judge-only reference, is **5 on both scalings** collection-wide. Per band it depends on a
choice the registration does not make — whether the reference is the collection-wide point or that
band's own — and the two readings disagree: 3 / 3 / 20 against 5 / 3 / 3 in the order auxiliary, countable, uninformative. Both are recorded in
`baseline_nstar.csv`; **neither per-band reading is registered** — the registration fixes `n*` against *the B0 point* and registers no per-band quantity under either reference — so the collection-wide reading is carried as the primary presentation and the per-band reading as a disclosure of the ambiguity.

## 7. Conclusions

**The denominator a language-model judge produces is not usable at this collection's eligibility
rates, and it is easy to beat.** Five expert judgments per topic bring the error below it; three do
not.

**The binding reference is not the judge but a constant.** On the registered metric no budget in
the grid attains a lower error than an uninformative guess until a shrinkage estimator is used, and that estimator's
advantage is conditional on a prior weight no registration fixes.

**The same labels attain a lower error than random sampling as a prior mean and fail as a partition.** A prior mean has
only to locate a topic's rate; a partition has to separate eligible documents from ineligible ones,
and a sensitivity of 0.6419 cannot. The difference is a property of the judge, not of either
procedure.

**The eligibility rate dominates the budget.** Moving a topic from the sparsest band to the densest
reduces error more than raising the budget from three judgments to a hundred within a band.

**The most transferable finding is methodological.** A scaling convention left unstated in a
pre-registration reversed the ordering of a zero-cost procedure and a hundred expert judgments, and
a conveniently drawn validation sample understated the judge's specificity by enough to move a
topic between bands. Both are properties of evaluation practice rather than of this collection.

**What does not follow.** No statement that a selection rule works — band selection was withdrawn
untested. Nothing about depth-partitioned pooling or adaptive selection in either direction. No
ordering among the sampling procedures beyond the registered comparator. No collection-wide census
statement: the exhaustive check was possible on four topics. And no unqualified sentence about
"the judge", because three arms are in play (§0).

## 8. Outputs

| file | what it holds |
|---|---|
| `baseline_verdict.json` | every verdict with the threshold it was tested against, the arms in play, the exclusions |
| `baseline_nstar.csv` | `n*` collection-wide and per band, both reference readings, band labels carrying their instantiation |
| `baseline_band_sensitivity.csv` | the arm-by-tolerance grid; the verdict column reads *not assessed*, never a loss, because band selection was withdrawn untested |
| `baseline_rejected_runs.csv` | *stage not attempted* — deliberately not an empty file, which together with zero runs read would be an ERROR under the registered harness guard |
| `baseline_board.png` | the board: five curves over four procedures — the shrinkage estimator contributes two, one per prior weight — and three points, the two not-attempted procedures absent rather than shown as losses |
| `baseline_points.csv`, `baseline_curves.csv`, `board_estimators*.csv`, `board_stratified*.csv` | the measured values behind every figure above |
| `pool_results_en.md`, `board_estimators_en.md`, `board_stratified_en.md`, `baseline_anchor_en.md` | the per-stage records |
| `closure_ruling_en.md`, `closure_certification_en.md` | what closure was admissible, and whether it was discharged |

## 9. Permanent disclosures

These are not open questions. They travel with every number this record reports.

- **The relative scaling was chosen after both scalings were seen to disagree.** It is
  conservative for every claim made here; the absolute scaling reverses the ordering at the
  largest budget.
- **Amendment 2(b)'s stated rationale overclaims.** *"The added points cannot change a verdict"*
  is true of which points are counted and false of their values: per-cell seeding changed the
  draws at every budget, so the six registered points moved. The verdicts did not. The
  pre-amendment values are recorded in `baseline_anchor_en.md` sections 2 and 5 and in
  `closure_certification_en.md`, which is where Amendment 6 points.
- **Amendment 5's priority cannot be corroborated by the store.** It states it was fixed before
  any stratified value existed, and it was, but the pre-registration version carrying it and the
  first values were saved in one call. What can be checked instead is that the verdict does not
  turn on the allocation.
- **The first pre-registration's unnumbered amended block carries no timing disclosure** of its
  own, and it created the constants the later anti-search clause governs. No verdict depends on
  them, since band selection is withdrawn untested; a future registration of band selection may
  not inherit them without restating their provenance.
- **The auxiliary boundary and the estimator definitions are inherited from `greg_prereg.py`,**
  which carries no registration-integrity clause of its own.
- **Store-versus-repository drift is unverified.** No registration copy was reachable from the
  granted paths at closure, so the one recorded difference is carried from the earlier audit
  rather than re-checked.
- **Three reporting obligations live outside this board** — the phase-one SECONDARY analysis, the
  synthetic-judge G2 condition, and a correlation test with no registered home — and are closed at
  the standing recorded in `hypothesis_standing_audit.md`, not here.

## 10. What is closed and what is not

**Closed.** All four registered hypotheses, both declared predictions, and the derived quantity.
No further measurement was required, and none was performed to reach these dispositions.

**Not closed, and deliberately left so.** Prediction 2's registered mechanism clause is a
probability that was never recomputed on the pool; the eight-arm clause of prediction 1 needs the
remaining seven arm-conditions run over the pool; and a correct band instantiation needs rates
measured on a pool-representative sample rather than on the frozen panel. Each is a new
registration, not an amendment, and none of them is a prerequisite for the claims this record
makes.

**Available and not claimed.** The price of a usable denominator: a median of **613 expert
judgments** per topic for a denominator good to plus or minus fifty per cent, with **11 of 30
topics** reaching half the relative error within a hundred judgments.

## 11. What a reader of this closure must be told

Five things the record did not state until closure. None changes a disposition; all five change how
a number should be read.

- **The word *registered* names two arms.** The registered `JUDGE_LABELS` arm is `gpt-4o-mini`, condition A, a
  stratified sample of 4,762 pairs; it supplies the judge-only reference point and every `n*`.
  The arm registered for the pool run is `qwen3-8b`, condition C, and it supplies every auxiliary
  variable. §1 and §6 use *the registered arm* in the second sense.
- **The band split is not fixed.** The 4 / 18 / 8 split holds only at (BAND_ARM = haiku_A, condition A, BAND_TOLERANCE = 0.5). Over the
  24-point arm-by-tolerance grid the countable boundary `p*` spans 0.018905 to
  0.156463, and `baseline_verdict.json` and `baseline_nstar.csv` now carry that span
  wherever the split appears.
- **The per-band readings of `n*` lead differently across canonical copies.** This record and
  `baseline_nstar.csv` lead with the collection-wide reference; `baseline_verdict.json` leads with
  each band's own. Neither is registered — the registration fixes `n*` against *the B0 point* and
  registers no per-band quantity — so the disagreement is a presentation difference, not a
  contradiction.
- **The prior judge-only-against-uninformative comparison is named three ways.** The registration
  docstring, the closure ruling and the consolidation index each word it differently; the standing
  that governs is **INCONCLUSIVE**, decided on `|log error|`, which is a metric the board excludes
  from its own comparisons.
- **Four figures behind prediction 1's failure are brief-sourced and cannot be reproduced from the
  store**: the run-to-run false-positive difference 0.0025, the two label agreements 0.9906 and
  0.9960, and the strict parse rate 1.0000. The composition gap they are compared against does
  reproduce, and their ratio of about 26 follows from it, but the four figures themselves rest on
  `pool_results_en.md` rather than on a table. Reproducing them needs a second label run on the
  same 2,025 pairs, or the completions, and neither is in the store.

---

## Appendix A. The two band boundaries are different kinds of object

They must never be presented as a matched pair. The **countable** boundary is an inversion of the
bias identity at a tolerance the evaluator supplies: `p* = (1 − sp)/(t + 1 − se + 1 − sp)`, whose
value is 0.0902 at the registered instantiation (`haiku_A`, condition A, tolerance 0.5) and **0.0706** when the
pool-measured rates of the arm that was actually run are substituted. The **auxiliary** boundary
0.0088 is a derivation: the cited authors state a variance condition for their own estimator's
gain, an inequality that does not follow from the identity, and the crossing value comes from
putting the judge's labels into their own simulation. Reported as a closed form with its arguments
exposed, never as a constant.

## Appendix A2. Prior results carried, on their own metrics

| comparison | standing at closure |
|---|---|
| judge-only projection against the uninformative estimator | carried as prior, on `|log error|` only — the metric the board forbids — 16 of 30 topics, not significant; **INCONCLUSIVE**, and excluded from the board's own comparisons |
| the exhaustive judge census | carried as prior: identity exact over 54 rows, variance eliminated and bias unchanged, on the four topics where a census was possible |
| the three sampling estimators | recomputed under the registered metric on the real population (§6); no prior verdict is restated |

## Appendix B. Sources

`clef2017_abs_test.qrels`, `baseline_inputs.csv`, `baseline_curves.csv`, `baseline_points.csv`,
`pool_topic_rates.csv`, `pool_band_shift.csv`, `board_estimators.csv`,
`board_estimators_collection.csv`, `board_stratified.csv`, `board_stratified_srswor.csv`,
`board_stratified_grid.csv`, `price_across_regimes.csv`, `greg_prevalence_vs_quality.json`,
`baseline_nstar.csv`, `baseline_verdict.json`, `prereg/baseline_prereg.py`,
`closure_ruling_en.md`, `closure_certification_en.md`, `hypothesis_standing_audit.md`.

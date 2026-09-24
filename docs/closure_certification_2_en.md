# Second certification of the closure — refused

Referee certification of the rewritten closure record, checked against `experiment_plan_en.md`
**v30** (the §0 paragraph of v29 was withdrawn mid-certification and replaced; I certify v30),
`baseline_prereg.py` v8 — authoritative wherever it and the record disagree — the five declared
outputs, the four stage briefs, the consolidation index, and the thirteen value tables behind them.
No experiment was run, no result was computed as a new finding and no document was repaired.

The plan is a new document, so nothing was carried forward from the certification of v26: every
number in v30 was recomputed from the file it claims to come from, including the ones the rewrite
introduced. Where a figure could not be recomputed from what I was given, it is reported as
unverifiable rather than as checked.

**Verdict: the hypothesis verification still cannot be declared closed.** Fourteen of the sixteen
blockers are cleared, and the rewrite is a better record than the document it replaces: all four
forbidden wordings and all five stale sentences are gone, the band-conditioned recommendation is
deleted rather than restated, seven permanent disclosures are collected in one place, and the two
mandated entries missing from `baseline_verdict.json` are present and transcribed from the right
source. But two of the sixteen are not cleared, three of the claims made for this work are not
borne out by the files, and the rewrite introduced four defects of its own — one of them a
variance-versus-standard-deviation confusion that contradicts the stage brief it came from, in the
very paragraph whose subject is a scale confusion that brief had already corrected once.

---

## 1. What was claimed against what the files show

Seven claims were made for this work. Checked one by one.

| claim | finding |
|---|---|
| 1. Two mandated entries added; five empty thresholds filled; H-B8 self-contradiction removed; derived quantity given its band instantiation; stratified entry given its allocation counts; scaling statement added | **six of seven.** The H-B8 self-contradiction is **still present verbatim** |
| 2. Four forbidden wordings and five stale sentences gone by rewriting | **borne out.** Zero occurrences of *superseded*, *survives*, *strengthens*, *decides*, *falsifies*, "None of the four", "All four hypotheses", "does not exist", "seven risks" in v30 |
| 3. Band-conditioned practitioner recommendation deleted, not restated | **borne out.** Zero occurrences in v30 |
| 4. Seven permanent disclosures in one section | **borne out.** §9, seven bullets |
| 5. Amendment 6 corrects Amendment 2(b)'s rationale and nothing else; pre-amendment values not restated because not reproducible from the store | **admissible as an amendment; the stated reason is false.** The pre-amendment values are in `baseline_anchor_en.md` §2 and §5 |
| 6. Base-mixing hazard disclosed | **borne out in v30, after the v29 version of it was withdrawn as itself an instance of the hazard** |
| 7. Absolute reference corrected to its source; the two band readings distinguished as registered and disclosure | **first half borne out** (130.151515). **Second half creates a new disagreement**: no per-band `n*` is a registered quantity under either reference |

Two notes on the account of the correction I was given. The §0 replacement is real and material, and
my own independent check had reached the same finding: `4.126` from `baseline_inputs.csv` is the
median of `|(R̂−R)/R|`, while `4.006` is `1 + rel_bias` on the pool arm, so the withdrawn paragraph
compared a relative error against an over-count ratio and called the two near-identical; on the
over-count convention the arms read **5.126 against 4.006**, 27.9 per cent apart, which I recomputed
and which v30 now states. The second described correction, however, did not occur between the two
versions I was given: v29 and v30 are byte-identical outside the §0 paragraph, and the §6 sentence
already read "3 / 3 / 20 against 5 / 3 / 3 in the order auxiliary, countable, uninformative" in v29,
with the collection-wide reading already named as the registered one. That account is inaccurate; it
does not change any verdict here, because the sentence it describes was correct as given in both.

One further discrepancy of record: I was told four of the five declared outputs had been revised.
The store holds two versions of `baseline_verdict.json` and two of `baseline_nstar.csv`, and a
**single** version of `baseline_band_sensitivity.csv`, `baseline_rejected_runs.csv` and
`baseline_board.png`. Two were revised, not four. Those three were the ones I had already
discharged, so the substance is unaffected.

---

## 2. The fifteen recording obligations

**1. `baseline_verdict.json` — partly discharged.** The two entries that were missing are present
and correct. `EXCLUDE_IF_R_ZERO` records `fired_on_topics` 0, `topics_retained` 30, `minimum_R` 2 —
I confirmed the minimum `R` is 2 over the 30 rows of `baseline_inputs.csv`. The Amendment 3 cells
record `CD008760 at n=75`, `CD008760 at n=100`, `CD010860 at n=100`, which is exactly the set the
`exhausted` flag carries in `baseline_curves.csv`, and the entry names that flag as its source
"not the amendment's prose" — correctly, since the amendment's prose names `CD010860` at `n` = 75
and a pool of 94 is not exhausted by a budget of 75. The five pointer thresholds are filled, the
`H-B6` entry now carries `allocation_counts` {1, 2, 1} and a note recording that pure proportional
is PARTIAL on its own and still below the registered 4, the `n*` entry carries a
`band_instantiation` field, and a `_scaling` key states that every verdict is on the registered
relative scaling with no absolute counterpart.

Four defects remain, three of them the ones this work claims to have removed or introduced:

- The `H-B8` entry still ends **"The recording obligation is unmet until baseline_verdict.json
  exists."** The self-contradiction is in the file that is being contradicted. It was claimed
  removed; it is not.
- The `n*` entry still ends "with every band label carrying (haiku_A, t = 0.5); **that file does not
  exist**" of `baseline_nstar.csv`, which exists and does carry them.
- `H-B8`'s `threshold_as_registered` still reads "same threshold, optional procedure" rather than
  the registered pair `HB8_RATIO` = 0.90 and `HB8_MIN_GRIDPOINTS` = 4. Reporting obligation 1 asks
  the verdict to echo the threshold it was tested against.
- `_registration` reads **"prereg/baseline_prereg.py v7 (Amendments 2-5)"**. The authoritative file
  is now v8 and carries Amendment 6. New drift, created by the same work that added the amendment.

**2. `baseline_nstar.csv` — discharged as transcription; one designation defect.** Every value
recomputed from `baseline_curves.csv` and `baseline_points.csv`: `n*` = 5 on both scalings
(4.1850 relative and 143.9479 absolute at `n` = 3, against B0 4.125854 and 130.151515; 2.9773 and
105.9851 at `n` = 5); per band against that band's own B0, 3 countable / 5 auxiliary / 3
uninformative; per band against the collection-wide B0, 3 / 3 / 20; band-own references 1.6023 /
2.9417 / 27.0848 against the file's 1.602 / 2.942 / 27.085; band sizes 4 / 18 / 8. The absolute
reference is now **130.151515**, its source value, correcting the 130.200 I recorded.

The defect is the new `registered_quantity` column. It is `True` on the three per-band rows measured
against the collection-wide B0 and `False` on the three measured against each band's own B0. The
registration says only *"n\* = smallest n in N_GRID at which a method's median RMSE falls strictly
below the B0 point"*; it registers **no** per-band `n*` under either reference. So marking three
per-band rows registered is an overreach, and marking the other three unregistered demotes the
reading my ruling assigned as the disposition — "per-band `n*` of 3 (countable), 5 (auxiliary) and
3 (uninformative), each against the judge-only point within that band" — which
`baseline_verdict.json` still carries as the `n*` disposition without any disclosure label. The
file, the verdict record and §6 of the plan now give three different accounts of which per-band
reading is registered, and the registration supports none of them.

**3. `baseline_band_sensitivity.csv` — discharged as to the file; partly as to the citation.**
Unchanged since my first certification and still sound: 24 rows over six arms and four tolerances,
`p_star` reproducing the registered closed form `(1 − sp)/(t + 1 − se + 1 − sp)` to 9.7e-17 at every
row, span 0.018905 to 0.156463 and countable count 2 to 16 of 30 — the registered sensitivity
statement exactly — and `hband_verdict` reading "not assessed - H-BAND withdrawn untested" at every
row, so it is not a grid of a verdict on a repopulated comparator.

The citation half is now moot in the place it was written for and open in a new one: the 4 / 18 / 8
split does not appear anywhere in v30, so there is nothing to attach the sensitivity to. But
Appendix A quotes two instantiations of `p*` (0.0902 and 0.0706) and §1 quotes per-band topic counts
(4 widening to 5) with no statement of the span the anti-search clause attaches to them.

**4. `baseline_rejected_runs.csv` — discharged.** Unchanged: one row, `parse_status` "stage not
attempted", `runs_read` 0, `min_runs` 20, `guard_state` "not triggered - stage never entered", with
a reason naming the registered error condition. Explicitly not the empty file that, with zero runs
read, the registration defines as an error rather than a pass.

**5. `baseline_board.png` — discharged.** Unchanged. I read the figure: four procedures as curves
(random subsample, model-assisted, shrinkage at both prior weights, stratified), the judge-only
projection and the uninformative guess as reference lines and the judge census as a point, at values
consistent with the tables at every point I checked (subsample ≈ 4.19 at `n` = 3 falling to 0.72 at
100; shrinkage at weight 50 from 0.639 to 0.513; weight 10 peaking near 1.14 at `n` = 10; judge-only
4.126; constant 0.630; census 0.085). The caption names all three arms with their prompt conditions,
records `B7` and `B8` as NOT ATTEMPTED "reported as not assessed rather than as a loss", and records
band selection as WITHDRAWN and not plotted. One notation slip travels the other way: §8 of v30
calls it "four curves, three points" where five curves are plotted for four procedures — the figure
title itself says "four procedures with curves", which is right.

**6. Reporting obligation 3, "not assessed", never a loss — discharged.** The sensitivity file's
verdict column, the figure caption, and §8's row for the sensitivity file. The rewrite dropped the
Appendix B band table altogether, so no band cell survives that could read as a loss.

**7. Amendment 5's priority claim — discharged.** §9 bullet 3 states the claim, states that the
pre-registration version carrying it and the first values were saved in one call so the store cannot
corroborate the order, and names the substitute check: the verdict does not turn on the allocation.
The allocation insensitivity is in `baseline_verdict.json` as 1, 2, 1 of 6, and I reproduced all
three counts from `board_stratified_grid.csv` and independently from `board_stratified.csv` against
`board_stratified_srswor.csv`.

**8. The unnumbered `AMENDED` block's timing — discharged** in the second form my ruling allowed.
§9 bullet 4 records that it carries no timing disclosure of its own, that it created the constants
the later anti-search clause governs, that no verdict depends on them because band selection is
withdrawn untested, and that a future registration may not inherit them without restating their
provenance.

**9. Amendment 2(a) must sit with the verdicts — discharged.** The `_scaling` key of
`baseline_verdict.json` now carries the whole disclosure, including the half that was missing: every
verdict is on the registered relative scaling and **no absolute-scaling counterpart exists**. §2 and
§9 of v30 carry it too.

**10. Amendment 2(b)'s rationale — discharged as a correction; see §5 on its stated reason.**
Amendment 6 of the pre-registration and §9 bullet 2 both record that "the added points cannot change
a verdict" is true of which points are counted and false of their values. I re-verified the fact
from `baseline_curves.csv`: the counted points moved to 2.2447 at `n` = 10 and 1.0268 at `n` = 50.

**11. Every statement about "the judge" names the arm and prompt condition — discharged in the plan
and the briefs, open in `user_benefit.csv`.** See §5(e).

**12. Registration-integrity clause propagation — discharged.** §9 bullet 5: the auxiliary boundary
and the estimator definitions are inherited from `greg_prereg.py`, which carries no
registration-integrity clause of its own. I confirmed the inheritance numerically —
`greg_prevalence_vs_quality.json` gives `crossing_prevalence` 0.008837, which is `BAND_AUXILIARY` =
0.0088.

**13. Canonical-home drift — discharged, all five items.** Both duplicated paragraphs, "None of the
four is decided", "All four hypotheses", the mis-ordered seventh risk bullet and the two sentences
denying the discharge are absent from v30; §9 is now a disclosures section rather than a risks
section with a stray bullet.

**14. Store-versus-repository drift — discharged, and independently re-verified this session.** §9
bullet 6 records it as unverified. I walked both granted paths rather than carrying the earlier
finding: the read-write repository exists and has a `.git` directory, and of 49,016 files it contains
no copy of any of the fourteen registrations — the only `prereg`-named files are six worktree copies
of `_PREREG_ctext_floor.md`, which is not one of them. The comparison `prereg_audit.csv` describes
still cannot be made from here, so the one recorded difference is correctly carried rather than
re-checked.

**15. The three out-of-plan reporting obligations — discharged.** §9 bullet 7 names all three — the
phase-one SECONDARY analysis, the synthetic-judge G2 condition, and a correlation test with no
registered home — and closes them at the standing recorded in `hypothesis_standing_audit.md`. They
are now recorded *with* the closure rather than deferred to the audit by a blanket reference.

---

## 3. The nine forbidden moves, rechecked in v30

**1. Retrofitting the band-to-procedure map — closed.** No map appears anywhere in v30. §1 states
that none is registered and that a three-band-by-nine-procedure assignment is a larger free
parameter than the tolerance the anti-search clause protects; §10 records that a correct band
instantiation is a new registration, not an amendment.

**2. Restating an unregistered comparison as a verdict — closed in the plan, moved to the
consolidation index.** Zero occurrences of *superseded*, *survives*, *strengthens* or *falsifies* in
v30; Appendix A2 row 3 reads "recomputed under the registered metric on the real population; no
prior verdict is restated". But the `greg_prereg.py` thread in `consolidation_sources.csv` now reads
**"SUPERSEDED — closed under the registered joint rule and recomputed on the pool..."**. The
overstatement I flagged there is fixed and the joint rule is named; the repair introduced the one
word the closure surrenders. Two other occurrences of the word in that file are verbatim carriages
of my ruling's own surrender text and are not instances of the move.

**3. Reporting a conditional as support — closed in v30, closed in the estimator brief, still live
in `user_benefit.csv`.** §1, §6 ("**This is conditional on the prior weight**") and §7 all carry it.
`board_estimators_en.md` now carries a new §5 bullet — "No registration fixes the prior weight, so
every clause that holds at only one weight is conditional on it. The floor-clearing result is the
clearest case: it holds at 50 and not at 10" — and its §3 table row states the same, which
discharges the blocker; its §2 heading "The zero-cost floor is cleared for the first time" is left
standing unqualified, a residual rather than the blocker. `user_benefit.csv` is untouched: the row
"Stop paying where a constant is as good" still asserts "an estimate that costs nothing is not
improved on by any budget tested", which this closure records as **falsified**.

**4. Closing a hypothesis on a substituted quantity — closed in v30, still live in
`user_benefit.csv`.** §6 now reads "an unregistered substitute for prediction 2's mechanism clause,
not a closure of it", and *decides* is gone. `user_benefit.csv` still reports the registered
mechanism probability — 0.82 at `n` = 10, 0.96 in the sparsest band — as "Measured on the registered
scaling with its mechanism". Nothing recomputed it.

**5. Transplanting a failure branch's consequence — closed.** The band-conditioned recommendation is
**deleted**. §1 states that because the hypothesis was never tested the FALSIFIED branch did not
fire and its consequence text does not apply. The residual is `user_benefit.csv` row 1, which
attributes its benefit to "Band selection · null" and says it "survives every hypothesis outcome";
the substance there is admissible as description — `N` and an estimate of `p` deciding countability
— but it is the last place a band-conditioned recommendation carries standing language.

**6. Closing `H-B7` as a null result — closed, and better than in v26.** "NOT ATTEMPTED, no verdict.
Nothing may be said about this procedure in either direction, including that it is untested in a way
that implies a result." §3 of v30 no longer carries the sentence crediting the board with a
comparison against an implemented competing system; it says only that the last two procedures have
no curve. The letter-of-the-rule trap stays shut.

**7. Repopulating `BEST_FIXED` with only the procedures that have curves — closed.** §1 states the
comparator population cannot be identified without choosing it after seeing which procedures ran,
and `board_estimators_en.md` §5 retains the sentence that is the only other place the restriction is
named.

**8. Reading the pool band shift as a correction to the registered bands — closed.** §6 says the
registered boundary "is exposed in a known direction", that correcting it is a new registration and
that the band assignment stands as registered for anything already counted; §10 repeats it; no topic
is re-banded. The residual I recorded against v26 is gone: §0 names the pool arm and Appendix A
attributes the 0.0706 boundary to "the arm that was actually run", so the record no longer implies
that the measured boundary belongs to the arm the registered bands use.

**9. Switching metric or scaling to rescue a comparison — closed as to the scaling; a basis
substitution is live in two new places.** The scaling disclosure is in §2, §9 and the verdict file.
But §6's stratification paragraph quotes variance-scale reductions as standard-deviation-scale
quantities, and §1 reports the more favourable of two comparator realisations without naming it.
Both are in §5 below.

---

## 4. Every number in v30 against its source

Recomputed, not carried. Agreements are exact to the precision printed unless a note says otherwise.

| value in v30 | source | agrees |
|---|---|---|
| 30 topics; 117,562 pairs | `baseline_inputs.csv`, 30 rows, `ΣN` = 117,562 | yes |
| eligibility factor 694; 0.00029 to 0.2018; median 0.0195 | `baseline_inputs.csv` `p`: 0.000291 to 0.201754, ratio 693.8, median 0.019537 | yes |
| `JUDGE_LABELS` stratified sample of 4,762 pairs; 4.05 per cent | Amendment 4(a); 4,762 / 117,562 = 4.050% | yes |
| condition-A arm per-topic rates se 0.8486, sp 0.8794 | `baseline_inputs.csv` medians | yes |
| judge-only reference a **relative error** of 4.126, median of `\|(R̂−R)/R\|` | `baseline_inputs.csv` median `\|rel_bias\|` 4.1259; `baseline_points.csv` B0 4.125854 | yes |
| pool arm over-counts by a factor of 4.006, = `1 + rel_bias`; 29 of 30 | `pool_topic_rates.csv` median `R_llm/R` 4.0065, 29 over-counts | yes |
| on the over-count convention, 5.126 against 4.006, 27.9% apart | `baseline_inputs.csv` median `R_llm/R` 5.1259; 5.1259/4.0065 − 1 = 27.94% | yes |
| 1,000 replicates; seed per cell | `BOOTSTRAP_REPS` = 1000 | yes |
| `EXCLUDE_IF_R_ZERO` fired on no topic; minimum `R` = 2; 30 retained | `baseline_inputs.csv` min `R` = 2 | yes |
| 3 pool-exhausted cells: `CD008760` at 75 and 100, `CD010860` at 100 | `baseline_curves.csv` `exhausted` flag, 3 rows | yes |
| nine procedures, three consuming nothing, two with no curve | enumeration in §3 | yes |
| 117,553 pairs labelled; 9 absent; 0.008 per cent | `pool_results_en.md`; 9/117,562 = 0.0077% | yes |
| 99,304 unique PubMed records | no source among the files given | **unverifiable** |
| 27 participant runs | no source among the files given (`runs_read` = 0) | **unverifiable** |
| strict parse rate 1.0000, zero nulls, zero truncation | `pool_results_en.md` | yes (brief-sourced) |
| pool-wide se 0.6419, sp 0.9348 | `pool_topic_rates.csv`, `Σtp/ΣR` = 0.6419, `1 − Σfp/Σ(N−R)` = 0.9348 | yes |
| panel false-positive 0.1292 against 0.0645 outside | `pool_results_en.md`; whole-pool 0.0652 consistent with sp 0.9348 | yes (brief-sourced) |
| run-to-run 0.0025; agreement 0.9906 and 0.9960; factor 26 | `pool_results_en.md`; 0.0647/0.0025 = 25.9 | yes (brief-sourced) |
| sensitivity 0.6764 inside against 0.6143 outside | `pool_results_en.md` | yes (brief-sourced) |
| model-assisted 0.944 / 0.938 / 0.947 / 0.960 / 0.933 / 0.922, 0 of 6 | `board_estimators.csv`: 0.9444, 0.9382, 0.9466, 0.9597, 0.9330, 0.9225 | yes |
| shrinkage weight 10: 0.513 / 0.674 / 0.755 / 0.849 / 0.882 / 0.920, 5 of 6 | 0.5132, 0.6743, 0.7553, 0.8491, 0.8818, 0.9201 | yes |
| shrinkage weight 50: 0.280 / 0.390 / 0.444 / 0.548 / 0.628 / 0.703, 6 of 6 | 0.2797, 0.3905, 0.4442, 0.5482, 0.6275, 0.7035 | yes |
| stratified 0.889 / 0.950 / 0.928 / 0.957 / 0.965 / 0.951, 1 of 6 | `board_stratified.csv` against `board_stratified_srswor.csv`, `proportional_min1` | yes |
| 1 of 6, 2 of 6, 1 of 6 across the three allocations | `board_stratified_grid.csv` `met` = 1, 2, 1; reproduced from the raw files | yes |
| zero-cost constant 0.6304 | `baseline_points.csv` B1 median `R` 0.630435 | yes |
| cleared from `n` = 5 at 0.6270, reaching 0.5130 | `board_estimators.csv` `rmse_EB50` medians 0.6270 and 0.5130 | yes |
| at weight 10 the constant is never beaten in the grid | `rmse_EB10` minimum over the grid 0.6709 | yes |
| "the first board row ever to do so" | true among procedures measured on all 30 topics; the 4-topic judge census point sits at 0.085 | yes, with a scope word missing |
| median relative bias 0.077 against 0.008 | `board_estimators.csv` over the six registered budgets: max `\|bias_EB50\|` 0.0766, max `\|bias_E2\|` 0.0076 | yes |
| judge-free target worse by 20% at `n` = 3, better by 6% at `n` = 100, crossing between 20 and 30 | `board_estimators_collection.csv` against `board_estimators.csv`: +19.78%, −5.94%, sign change between `n` = 20 (+3.22%) and 30 (−1.76%) | yes |
| 35.8 per cent of eligible in the stratum holding 92.6 per cent | 665/1,857 = 0.3581; 108,822/117,553 = 0.9257 | yes |
| 108,822 documents at 0.0061 against 8,731 at 0.1365 | `board_stratified.csv` stratum sizes; 665/108,822 = 0.006111; 1,192/8,731 = 0.136525 | yes |
| "the weighted within-stratum variance falls only 7.5%" | 0.014380 against 0.015548, ratio 0.92479 | yes |
| "that figure is a design effect **for the standard deviation**" | the standard-deviation design effect is 0.96166, i.e. **3.8 per cent** | **no** |
| per-topic variance ratio median 0.9213, range 0.5886 to 0.9994 | recomputed per topic from `pool_topic_rates.csv` strata | yes |
| "implying a **7.9 per cent** gain at the median topic" | 1 − 0.9213 = 7.87% is the **variance** reduction; the gain in RMSE is 1 − √0.9213 = **4.0 per cent**, which is what `board_stratified_en.md` §3 states | **no** |
| "two bases are reported wherever a ratio is quoted" then one basis | the second basis exists: median of per-topic ratios, minimum 0.8605 | **no — announced, not reported** |
| ratio of medians never below 0.7536 | minimum over three allocations and six budgets 0.7536 (`neyman_judge`, `n` = 10) | yes |
| `n*` = 5 on both scalings | `baseline_curves.csv`: 4.1850 and 143.9479 at `n` = 3 against 4.125854 and 130.151515; 2.9773 and 105.9851 at `n` = 5 | yes |
| 3 / 3 / 20 against 5 / 3 / 3 in the order auxiliary, countable, uninformative | collection-wide B0: 3, 3, 20; band-own B0: 5, 3, 3 | yes |
| "the collection-wide reading is the registered one" | the registration registers no per-band `n*` under either reference | **no** |
| "five expert judgments bring the error below it; three do not" | 2.9773 at `n` = 5 and 4.1850 at `n` = 3 against 4.125854 | yes |
| no budget in the grid beats the constant until a shrinkage estimator is used | over the six budgets the minima are 0.7292 subsample, 0.6726 model-assisted, 0.6709 weight-10, 0.6831 stratified, all above 0.6304; weight 50 below at all six | yes |
| "moving a topic from the sparsest band to the densest reduces error more than raising the budget from three judgments to a hundred within a band" | on ratios: band move 7.4× to 7.8×, within-band 3→100 5.8× to 6.6×. On differences it fails in the sparsest band (4.53 against 8.01 at `n` = 10) | yes on the ratio basis; **basis unstated** |
| boundary 0.0706 against predicted 0.1373 to 0.3361; countable band 4 to 5 | `pool_band_shift.csv`; recomputed from the closed form with pool rates; band counts 4/18/8 at 0.0902 and 5/17/8 at 0.0706 | yes |
| `p*` = 0.0902 at the registered instantiation | `band_countable(0.6412, 0.9149, 0.5)` = 0.09016 | yes |
| auxiliary boundary 0.0088 | `greg_prevalence_vs_quality.json` `crossing_prevalence` 0.008837 | yes |
| 16 of 30 topics, not significant, on `\|log error\|` | pre-registration docstring, Wilcoxon `p` = 0.839 | yes (registered) |
| identity exact over 54 rows, 4 topics | pre-registration docstring and `baseline_verdict.json` | yes (registered) |
| 613 expert judgments; 11 of 30 topics | `price_across_regimes.csv` `n_med` 613.0; 11 topics reach relative error below 0.50 at some budget ≤ 100 | yes |
| "the working plan was patched twenty-six times" | 30 stored versions; the last working-plan version was 26, so 25 patches followed the original | overstated by one |
| "four curves, three points" (§8) | five curves for four procedures | notation only |

Two figures I could not recompute and do not carry as checked: the 99,304 unique PubMed records and
the 27 participant runs have no source among the thirteen tables, the five outputs, the four briefs
or the pre-registration. They are reported as unverifiable.

---

## 5. The three questions put to me

### (e) Do the arm conventions discharge the obligation, or satisfy its letter?

**Discharged in the four briefs; satisfied in substance in the plan; undischarged in
`user_benefit.csv`.**

The obligation was that no board statement about "the judge" stand unqualified, because the board
mixes three arms and the registration names one. A stated convention discharges it when the document
also names the arm it is *not* talking about, because that is what stops a sentence from travelling.
Two briefs do exactly that: `board_estimators_en.md` declares `qwen3-8b` condition C and then states
that "the judge-only reference point of the board comes from a **different** arm (`gpt-4o-mini`,
condition A) and is named wherever it is used"; `baseline_anchor_en.md` declares `gpt-4o-mini`
condition A and states that this is **not** the pool arm. `pool_results_en.md` declares the pool arm
and undertakes to name the panel explicitly wherever a panel-measured rate is meant, which it does.
`board_stratified_en.md` declares the pool arm with its rates and adds "no statement here transfers
to another arm". All four are genuine discharges, not letter-satisfaction.

v30 is stronger than v26 and still not airtight. §0 names all three arms with their prompt
conditions and states the rule; §6 attributes the strata and the auxiliary variable to "the
registered arm" whose rates are quoted; §7 closes with "no unqualified sentence about 'the judge',
because three arms are in play (§0)". But §7 also contains "a sensitivity of 0.6419 cannot. The
difference is a property of the judge, not of either procedure" — a statement about "the judge"
whose arm is recoverable only from the rate quoted in the preceding clause, in the same section that
forbids exactly that form. The purpose is met by a reader of the whole section and not by the
sentence, which is the sentence a paper quotes.

`user_benefit.csv` has no convention line and was not revised. Its first row still gives "a
judge-derived denominator is over-counted by a median factor of 5.1 (28 of 30 topics over-count)"
with no arm named. That figure is now consistent with v30's corrected convention — I get 5.1259 with
28 of 30 from `baseline_inputs.csv`, against 4.0065 with 29 of 30 from `pool_topic_rates.csv` — so
the number is right and the arm is still missing, which is the whole content of the obligation.

### (f) Is Amendment 6 an admissible way to correct a rationale?

**Admissible in form, and it alters nothing it claims not to. Its stated reason for one omission is
false.**

It is admissible. It is appended at closure rather than edited into 2(b), so the original wording
stays readable — I confirmed that Amendment 2(b) still contains "so the added points cannot change a
verdict" verbatim. It carries its own timing disclosure ("at closure"), so it does not repeat the
defect of the unnumbered `AMENDED` block. And it alters nothing it disclaims: `N_GRID` is still
(3, 5, 10, 20, 30, 50, 75, 100), `N_GRID_REGISTERED_SUBSET` still (10, 20, 30, 50, 75, 100), and
every threshold constant — `HB6_RATIO`, `HB6_MIN_GRIDPOINTS`, the `HB7`, `HB8` and `HBAND` pairs,
`BAND_TOLERANCE`, `BAND_ARM`, `BAND_COUNTABLE`, `BAND_AUXILIARY` — is unchanged. Correcting a
rationale after the values exist is disclosed as such, which is the only thing that makes it an
amendment rather than a rewrite.

The defect is its reason: "The pre-amendment values are recorded in closure_certification_en.md and
are not restated here, because **they were not reproducible from the store at closure**." They are in
the store, in one of the four stage briefs of this very closure: `baseline_anchor_en.md` §2
tabulates the pre-amendment relative medians at all six registered budgets — 2.261, 1.575, 1.298,
0.991, 0.794, 0.692 — and §5 gives the pre-amendment `n` = 100 subsample as 0.6924. The
post-amendment counterparts are in `baseline_curves.csv`, where I recomputed 2.2447, 1.5797, 1.2950,
1.0268, 0.8205, 0.7206. An amendment whose subject is an inaccurate rationale should not carry one.

There is a second thing this amendment's subject makes visible, and it is a blocker in its own
right. The two budgets Amendment 2(b) added, `n` = 3 and `n` = 5, are not among the six points
verdicts are counted on — and **two of v30's headline numbers live on one of them**: `n*` = 5, and
the zero-cost floor cleared "from `n` = 5". v30 never lists the grid, never says it was extended
downward after the anchoring run, and never says that `n` = 5 is an added point. A reader sees a
results table whose budgets start at 10 and a derived quantity of 5, with no account of where it
came from.

### (g) The certification

**The hypothesis verification cannot be declared closed. The declaration sentence is withheld.**

Fourteen of the sixteen blockers are cleared: the `R` = 0 exclusion and the Amendment 3 cells are
recorded from the right source (1, 2); all four forbidden wordings are gone (3, 4, 5, 6); the plan no
longer denies its own discharge and all five canonical-home drifts are repaired (7, 8); the arms are
named in the plan (9); Amendment 2(b)'s overclaim, the `greg_prereg.py` integrity gap, the
unverifiable repository comparison, the three out-of-plan obligations and the scaling disclosure are
all recorded with the closure (10, 11, 12, 13, 14). Blocker 15 is half cleared and blocker 16 is
three-quarters cleared, and neither counts as cleared. Four new defects were introduced by the
rewrite, and three claims made for the work are not borne out.

Remaining blockers, each with the smallest action that clears it. None requires a run, and none
requires relaxing anything the closure claims.

1. **`baseline_verdict.json`'s `H-B8` entry contradicts the file's existence.** Delete the final
   sentence of its `surrendered` field.
2. **Its `n*` entry says `baseline_nstar.csv` does not exist.** Delete the clause "; that file does
   not exist".
3. **Its `_registration` names v7 (Amendments 2-5).** Change to v8 (Amendments 2-6).
4. **Its `H-B8` threshold is not the registered pair.** Write `HB8_RATIO` = 0.90 and
   `HB8_MIN_GRIDPOINTS` = 4.
5. **v30 §1 presents a paraphrase of the primary hypothesis as a quotation.** It reads *"Choosing the
   estimator by a topic's band attains a lower RMSE of `R̂` than the single best fixed estimator
   applied to every topic."* The registered sentence is *"The selection rule has content: allocating
   method by relevance-rate band beats the best single fixed method applied to every topic."*
   Substitute the registered sentence.
6. **v30 §1 says "Two independent defects" where the ruling and `baseline_verdict.json` record
   three.** The dropped ground is that the registration does not state whether a band assigned a
   zero-budget procedure spends nothing or spends `n`, which is the one ground that is not curable by
   disclosure. Restore it, or say "two of the three recorded in `baseline_verdict.json`".
7. **v30 §6 calls a variance-scale reduction a design effect for the standard deviation.** Replace
   "That figure is a pooled, large-sample design effect for the standard deviation" with the
   standard-deviation figure, 3.8 per cent, or label 7.5 per cent as the variance reduction it is.
8. **v30 §6 converts the per-topic variance ratio into a "7.9 per cent gain".** The gain in RMSE at
   the median topic is 4.0 per cent — the figure `board_stratified_en.md` §3 gives after its own
   correction of this same confusion. Replace 7.9 with 4.0, keeping 0.9213 as the variance ratio.
9. **v30 §6 announces two bases and reports one.** Add the second: the median of per-topic ratios
   never falls below 0.8605.
10. **v30 §1 reports prior weight 10 at "5 of 6, better than the predicted 4" with no comparator
    realisation named.** Against the anchoring realisation it is 4 of 6 — equal to the predicted 4,
    not better. The ruling's surrender for that clause requires the realisation be named: write "5 of
    6 in-run, 4 of 6 against the anchoring realisation, at or above the predicted 4 on either".
11. **v30 reports `n*` = 5 and the floor cleared from `n` = 5 without disclosing that `n` = 5 is a
    budget Amendment 2(b) added after the anchoring run and is not one of the six points verdicts are
    counted on.** One sentence in §2 or §9.
12. **`baseline_nstar.csv` marks three per-band rows as registered quantities.** The registration
    registers no per-band `n*` under either reference. Set `registered_quantity` to False on all six
    band rows, leaving it True on the two collection rows, and align §6 of the plan and the `n*`
    entry of `baseline_verdict.json` with that.
13. **Amendment 6's reason for omitting the pre-amendment values is false.** Replace "because they
    were not reproducible from the store at closure" with a pointer to `baseline_anchor_en.md` §2
    and §5, which record them.
14. **`user_benefit.csv` is untouched and still carries forbidden moves 3 and 4.** Correct the "Stop
    paying where a constant is as good" row, which asserts a clause this closure records as falsified
    and reports the `P2` mechanism probability as measured; and name the arm in the row that gives an
    over-count factor of 5.1.
15. **`consolidation_sources.csv` labels a prior-result thread "SUPERSEDED".** Replace the label with
    "RECOMPUTED under the registered metric"; the body of the row is already correct.
16. **`consolidation_sources.csv` still leads the CLEF census row "APPARATUS VALIDATED (robustness
    variant)".** That run's own output verdict is "INCONCLUSIVE — census incomplete", with validation
    only under a declared variant on 4 of 6 topics. Restore the standing and keep the variant as the
    qualifier.

**When those are cleared**, the declaration is unchanged from the one I set out in the first
certification, because nothing in this round moved a disposition:

> The hypothesis verification of the baseline board is closed with no further measurement: `H-BAND`
> is withdrawn as a registration defect found by audit and is neither supported nor falsified,
> `H-B6` is not supported, `H-B7` and `H-B8` are not attempted with no verdict, the plan's null
> hypothesis is measured against but is not a registered verdict, and the declared predictions close
> as recorded clause by clause in `baseline_verdict.json`, which echoes the threshold each was tested
> against.

That sentence commits the paper to: advancing no constructive claim for band selection in either
direction, and reporting the band table as description only at `(haiku_A, t = 0.5)`; saying nothing
whatever about depth-partitioned hybrid pooling or adaptive selection, including that they are
untested in a way that implies a result; reporting the random-sampling comparison as a recomputation
of a prior result rather than as a falsification, with the prior weight named and the bias it buys
stated; leaving `P2`'s registered mechanism clause as not measured unless the hypergeometric
computation on inputs in hand is elected; naming the arm and prompt condition wherever the judge's
labels are described; reporting every count with the comparator realisation it was computed against
where two realisations exist; and carrying the relative-scaling choice, the grid extension, the two
unverifiable timing disclosures and the unreachable registration copies as disclosures rather than as
resolved questions.

---

## 6. Scope of this certification

- All fifteen recording obligations, all nine forbidden moves and all sixteen blockers were checked;
  none was sampled.
- v30 was checked as a new document. Every number in it was recomputed from the file it cites, in
  the table at §4, including the ones the rewrite introduced. v29 and v30 are byte-identical outside
  the §0 paragraph, so the checks apply to both except where §4 says otherwise.
- Registered statements are quoted verbatim from `baseline_prereg.py` v8 and are not subject to the
  notation and informality checks applied to the plan's own prose.
- Conditional dispositions stay conditional: the zero-cost-floor clause remains falsified and
  conditional on an unregistered prior weight, and `H-B6` remains not supported and not conditional
  on allocation.
- Two figures could not be recomputed from what I was given and are reported as unverifiable, not as
  checked: the 99,304 unique PubMed records and the 27 participant runs.
- Six figures are brief-sourced rather than table-sourced — the panel false-positive and sensitivity
  splits, the run-to-run variation, the two label-agreement rates and the strict parse rate. Each is
  internally consistent with a table I did recompute (the 0.0652 pool false-positive rate against
  the sp 0.9348 I derived from `pool_topic_rates.csv`), but the panel's own 2,025 pairs are not in
  the files given, so those are certified as consistent rather than as independently reproduced.
- The store-versus-repository comparison was re-attempted this session rather than carried: the
  granted repository holds no copy of any registration, so it remains unverifiable from here.
- No experiment was run, no document was repaired, and no disposition was changed.

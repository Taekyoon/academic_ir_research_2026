# Third certification of the closure — refused, on two blockers

Referee certification of `experiment_plan_en.md` **v31** against `baseline_prereg.py` **v9**, which is
authoritative wherever the two disagree, together with the five declared outputs, the four stage
briefs, the consolidation index, the practitioner deliverable, and the sixteen value tables behind
them — now including `panel_sample.csv`, whose absence forced two declared deviations last time. No
experiment was run, no result was computed as a new finding, and no document was repaired.

Sixteen blockers were claimed cleared. **Fourteen are cleared. Two are not**, and one of the two is
the same class of defect that the work creating it also repaired elsewhere. Every number in v31 was
recomputed from the file it claims to come from, including the six figures that were previously
certified only as internally consistent; two of those six are now verified against their source by
an over-determined identity, and four remain brief-sourced because the files that would decide them
are not in the store.

**Verdict: the hypothesis verification still cannot be declared closed.** The remaining distance is
two edits — one token in `baseline_verdict.json` and one clause in `user_benefit.csv`. Neither
requires a run, a recomputation, or any weakening of what the closure claims.

---

## 1. What was claimed against what the files show

Thirteen corrections were claimed. Checked one by one, against the files rather than against the
account of them.

| claim | finding |
|---|---|
| Primary hypothesis quoted verbatim instead of paraphrased | **borne out.** Both registered sentences appear in v31 §1 character-for-character after whitespace normalisation |
| Third withdrawal ground restored | **borne out.** v31 §1 now reads "Three independent defects" and states the zero-budget-spend ground |
| Variance-versus-standard-deviation error corrected to 7.5 % variance against 3.8 % standard deviation | **borne out and independently recomputed.** Ratio 0.924786, design effect for the standard deviation 0.961658 |
| Per-topic figure corrected to 7.9 % variance and 4.01 % RMSE | **borne out.** Median per-topic variance ratio 0.9213; 1 − 0.9213 = 7.87 %, 1 − √0.9213 = 4.01 % |
| Second ratio basis added at 0.8605 | **borne out.** Median of per-topic ratios, minimum 0.8605 at `neyman_judge`, `n` = 10 |
| Prior-weight-10 count given both comparator realisations | **borne out.** 5 of 6 in-run, 4 of 6 against the anchoring realisation, both recomputed |
| Downward grid extension disclosed where the derived quantity and the floor budget fall on an added point | **borne out.** New §2 paragraph, naming Amendment 2(b) and both affected quantities |
| Claim that a per-band reading is registered withdrawn | **borne out in all three places.** v31 §6, `baseline_nstar.csv`, and the registration agree that no per-band `n*` is registered |
| Patch count and curve count corrected | **borne out.** 31 stored plan versions, the working plan's last being 26 — "twenty-five revisions after the original"; the figure carries five curves over four procedures |
| Sources named for the unique-record count and the participant-run count | **borne out, and both now verify.** 99,304 distinct `pmid` in `clef2017_abs_test.qrels`; `n_runs` = 27 in `judge_consequence.json` |
| `baseline_verdict.json`: H-B8 self-contradiction and stale non-existence clause deleted, H-B8 threshold written as its registered constants | **borne out, three of three** |
| `baseline_verdict.json`: registration pointer moved to v9 | **not borne out.** The file reads `"prereg/baseline_prereg.py v8 (Amendments 2-6)"`. The authoritative file is v9 |
| `baseline_nstar.csv`: all six band rows marked as disclosure | **borne out.** `registered_quantity` is `False` on all six band rows and `True` on the two collection rows |
| Registration: Amendment 6's false reason replaced by a pointer | **borne out.** v8 → v9 differs in exactly that comment and in nothing else; every threshold constant is byte-identical |
| `user_benefit.csv`: zero-cost row made conditional on the prior weight, arm named on the refusal row | **one of two.** The conditional is now stated in full. The row still reports prediction 2's registered mechanism probability as measured |
| `consolidation_sources.csv`: surrendered word replaced, census standing restored | **borne out, both.** Zero occurrences of `SUPERSEDED`; the CLEF census row now leads "INCONCLUSIVE — census incomplete" |

Two notes of record. First, the v8 → v9 bump is real and is the correct form: the diff is confined to
Amendment 6's stated reason, which now points at `baseline_anchor_en.md` sections 2 and 5 where the
pre-amendment values actually sit. Second, that bump is what makes the pointer claim false: the
pointer was moved from v7 to v8 while the registration itself moved from v8 to v9, so the verdict
file now names the one version whose Amendment 6 still carries the reason blocker 13 was raised to
remove. The defect is the same one, one version along, created by the same work that cleared it.

---

## 2. The sixteen blockers, rechecked

**1. `H-B8`'s `surrendered` field contradicted the file's existence — CLEARED.** It now reads
"Nothing the registration promised - it anticipated exactly this closure." The sentence "The
recording obligation is unmet until baseline_verdict.json exists" does not occur anywhere in the
file.

**2. The `n*` entry said `baseline_nstar.csv` does not exist — CLEARED.** It now ends "Nothing, once
transcribed into baseline_nstar.csv with every band label carrying (haiku_A, t = 0.5)." Zero
occurrences of "does not exist" in the file.

**3. `_registration` named a superseded version — NOT CLEARED.** It named v7 (Amendments 2-5) and
now names **v8 (Amendments 2-6)**, while the authoritative registration is **v9**. The action I
named is performed and the defect is not gone: the pointer is stale again, and it points at the
version whose Amendment 6 states that the pre-amendment values "were not reproducible from the store
at closure" — the false reason v9 removes. The thresholds are unaffected: I diffed v8 against v9 and
confirmed `N_GRID`, `N_GRID_REGISTERED_SUBSET` and every one of `HB6_RATIO`,
`HB6_MIN_GRIDPOINTS`, `HB7_RATIO`, `HB8_RATIO`, `HB8_MIN_GRIDPOINTS`, `HBAND_RATIO`,
`HBAND_MIN_GRIDPOINTS`, `BAND_TOLERANCE`, `BAND_COUNTABLE`, `BAND_AUXILIARY`, `MIN_RUNS` and
`BOOTSTRAP_REPS` are identical, so no verdict is misreported by it. What is misreported is which
registration the closure was certified against.

**4. `H-B8`'s threshold was not the registered pair — CLEARED.** It now reads "HB8_RATIO = 0.90 at
HB8_MIN_GRIDPOINTS = 4; optional procedure", which is the registered pair with the optionality kept
as a qualifier rather than as a substitute.

**5. The primary hypothesis was paraphrased as a quotation — CLEARED.** v31 §1 now carries both
registered sentences. I checked them as exact substrings of the registration after whitespace
normalisation and comment-marker stripping: *"The selection rule has content: allocating method by
relevance-rate band beats the best single fixed method applied to every topic."* and *"BANDED is
constructed by, for each topic, using the method the band assigns; BEST_FIXED is the single method
with the lowest median RMSE across all topics at that n."* Both match. The paraphrase that stood in
v30 — "Choosing the estimator by a topic's band attains a lower RMSE of `R̂` than…" — is gone.

**6. The third withdrawal ground was dropped — CLEARED.** v31 §1 reads "Three independent defects,
each recorded in `baseline_verdict.json`" and states the restored ground: the registered comparison
"does not state whether a band that assigns a zero-budget procedure spends nothing or spends `n`, so
the budget axis the comparison runs along is undefined for part of the assignment space." That is the
ground my ruling identified as the one not curable by disclosure, and the verdict file carries all
three.

**7. A variance-scale reduction was called a design effect for the standard deviation — CLEARED.**
v31 §6 now separates them: the weighted within-stratum variance "falls only 7.5 %, and the design
effect for the standard deviation — the quantity an RMSE inherits — is 0.96166, a reduction of
3.8 per cent." Recomputed from the strata of `board_stratified.csv` against `pool_topic_rates.csv`:
`p` = 0.015797, Var(y) = 0.015548, weighted within-stratum 0.014378, ratio 0.924786 (a 7.5 %
fall), square root 0.961658 (a 3.8 % reduction). Both figures and the label on each are right.

**8. A variance ratio was converted into a 7.9 per cent "gain" — CLEARED.** v31 §6 now reads "median
0.9213 over the range 0.5886 to 0.9994, a variance reduction of 7.9 per cent at the median topic and
therefore an RMSE gain of 4.01 per cent." Recomputed per topic from the pool strata: median 0.9213,
minimum 0.5886, maximum 0.9994; 1 − 0.9213 = 0.0787 and 1 − √0.9213 = 0.0401.

**9. Two bases were announced and one reported — CLEARED.** The second basis is now stated: "the
median of per-topic ratios, the other basis, never below 0.8605." Recomputed over three allocations
and six registered budgets: the minimum median-of-ratios is 0.8605 (`neyman_judge`, `n` = 10) and the
minimum ratio-of-medians is 0.7536 (same cell). Both quoted values are the true minima.

**10. Prior weight 10 was reported at "5 of 6, better than the predicted 4" with no realisation
named — CLEARED.** v31 §1 now reads "at 5 of 6 in-run and 4 of 6 against the anchoring realisation
of the comparator, at or above the predicted 4 on either". Recomputed: against `rmse_E2` in the same
run the margin is met at 10, 20, 30, 50 and 75 (5 of 6); against the anchoring realisation in
`baseline_curves.csv` at 10, 20, 30 and 50 (4 of 6). The wording is exactly what the ruling's
surrender required. A residual, not the blocker: the §6 table still prints "5 of 6" in its
`meets 0.90` column without the realisation, which is coherent for a table of in-run ratios and is
disclosed two sections earlier.

**11. `n*` = 5 and the floor cleared from `n` = 5 with no disclosure that 5 is an added point —
CLEARED.** v31 §2 now carries a paragraph of its own: Amendment 2(b) "extended the inherited grid
downward to 3 and 5; the verdicts are scored on the six registered budgets only, but `n*` = 5 and
the budget at which the floor is cleared both fall on an added point." Verified against the
registration: `N_GRID` = (3, 5, 10, 20, 30, 50, 75, 100) and `N_GRID_REGISTERED_SUBSET` =
(10, 20, 30, 50, 75, 100).

**12. `baseline_nstar.csv` marked three per-band rows as registered quantities — CLEARED, and the
three accounts now agree.** `registered_quantity` is `False` on all six band rows and `True` on the
two collection rows; each band row's disclosure states that the registration "fixes n\* against 'the
B0 point' and registers no per-band quantity under either reference". v31 §6 says **"neither
per-band reading is registered"** and carries the collection-wide reading as the primary
presentation. The registration supports that: it registers `n*` against "the B0 point" and nothing
per band. One divergence travels with it and is reported in §3 below: the `n*` entry of
`baseline_verdict.json` still quotes the band-own reading (3 / 5 / 3) as its disposition, where the
plan and the CSV make the collection-wide reading (3 / 3 / 20) primary. Neither document claims
either is registered, so nothing is over-claimed, but two canonical copies lead with different
numbers.

**13. Amendment 6's reason for omitting the pre-amendment values was false — CLEARED.** v9 replaces
"because they were not reproducible from the store at closure" with "The pre-amendment values are
recorded in baseline_anchor_en.md sections 2 and 5, and in closure_certification_en.md; they are not
restated here because this amendment corrects a rationale rather than a value." I confirmed the v8 →
v9 diff touches nothing else, and that `baseline_anchor_en.md` §2 and §5 do hold those values.

**14. `user_benefit.csv` carried forbidden moves 3 and 4 — NOT CLEARED. One of the two is fixed.**
Move 3 is cleared: the "Stop paying where a constant is as good" row now states that the zero-cost
estimate "was not improved on by any budget in the grid until a shrinkage estimator was used: at
prior weight 50 it is cleared from n = 5 (0.6270 against 0.6304), and at prior weight 10 it is never
cleared within the grid. The prior weight is a free parameter no registration fixes, so the statement
is conditional on it." That is the conditional stated in full, and the falsified clause is gone.
The arm is also now named on the refusal row: "median relative error 4.126 on the registered
JUDGE_LABELS arm (gpt-4o-mini, condition A), which is a relative error and not an over-count ratio".

Move 4 is **live, verbatim and unrevised**. The same row's *satisfied by the anchoring run* column
still reads "**Measured on the registered scaling with its mechanism**: the guess at 0.630 against
0.721 for the best tested budget, **explained by a median probability 0.82 of catching no eligible
document at n = 10**", and its *evidence* column still gives "median probability 0.82 at n = 10, and
0.96 in the sparsest band" as the mechanism. Those two figures are the pseudo-population values
quoted in prediction 2's own registration text. This closure records that clause as **NOT MEASURED**
— in v31 §1, in `baseline_verdict.json`, and in my ruling — and nothing in the store recomputed it
on the pool. A practitioner-facing deliverable therefore asserts as measured the one registered
quantity the closure says was never measured.

**15. `consolidation_sources.csv` labelled a prior-result thread "SUPERSEDED" — CLEARED.** The
`greg_prereg.py` row now reads "RECOMPUTED under the registered metric — closed under the registered
joint rule and recomputed on the pool: the model-assisted estimator meets the margin at 0 of 6, the
shrinkage arm at 6 of 6 conditional on prior weight 50". The word `SUPERSEDED` occurs zero times in
the file; the two surviving lower-case occurrences are a quotation of v24's inadmissible wording,
labelled as inadmissible, and a carriage of my ruling's own text about `greg_faithful.csv`. Neither
is an instance of the move.

**16. The CLEF census row led "APPARATUS VALIDATED (robustness variant)" — CLEARED.** It now reads
"INCONCLUSIVE — census incomplete (robustness variant); the run's own output verdict, not an
apparatus validation", which is that run's own standing with the variant kept as the qualifier. The
file also now carries a `ruling_standing` column recording, on all twenty-eight closed-thread rows,
that the original wording is retained in `evidence_ledger.csv` — which is the disclosed resolution of
the divergence I reported, rather than a silent conforming of one copy to the other.

---

## 3. The fifteen recording obligations

**1. `baseline_verdict.json` — discharged except for the registration pointer.** Three of the four
defects I recorded against it are repaired (blockers 1, 2, 4). The two mandated entries remain
correct and re-verified this session: `EXCLUDE_IF_R_ZERO` records `fired_on_topics` 0,
`topics_retained` 30, `minimum_R` 2, and the minimum `R` over the 30 rows of `baseline_inputs.csv`
is 2; the Amendment 3 cells record `CD008760` at `n` = 75, `CD008760` at `n` = 100 and `CD010860` at
`n` = 100, which is exactly the set the `exhausted` flag carries in `baseline_curves.csv`, and the
entry names that flag as its source rather than the amendment's prose. The `_scaling` key still
carries both halves of Amendment 2(a). The one open item is `_registration` = v8 against an
authoritative v9.

Two stale cross-references also survive inside the file and are reported rather than counted as
blockers, because each states a surrender that stands whatever the plan now says: the null-hypothesis
entry surrenders "The word 'falsifies', **which section 6 still uses**" and the P2(a) entry
surrenders "the plan's 'its model-assisted verdict survives the change'". Neither string occurs in
v31 — I searched — so both clauses describe a superseded plan version as if it were current.

**2. `baseline_nstar.csv` — discharged.** Every value recomputed from `baseline_curves.csv`,
`baseline_points.csv` and `baseline_inputs.csv`: `n*` = 5 on both scalings (4.1850 relative and
143.9479 absolute at `n` = 3 against B0 4.125854 and 130.151515; 2.9773 and 105.9851 at `n` = 5);
per band against the collection-wide B0, 3 auxiliary / 3 countable / 20 uninformative; per band
against each band's own B0, 5 / 3 / 3; band-own references 2.9417 / 1.6023 / 27.0848 against the
file's 2.942 / 1.602 / 27.085; band sizes 18 / 4 / 8. The designation defect is cleared (blocker 12)
and every band row carries `(BAND_ARM = haiku_A, condition A, BAND_TOLERANCE = 0.5)`, which is
reporting obligation 5.

**3. `baseline_band_sensitivity.csv` — discharged as to the file; partly as to the citation.**
Re-verified from scratch: 24 rows over six arms and four tolerances, `p_star` reproducing the
registered closed form `(1 − sp)/(t + 1 − se + 1 − sp)` to 9.7e-17 at every row, span 0.018905 to
0.156463, countable count 2 to 16 of 30 — the registered sensitivity statement exactly — and
`hband_verdict` reading "not assessed - H-BAND withdrawn untested" at every row, so the file is not a
grid of a verdict on a repopulated comparator. The citation half stays partly open: my ruling asked
that the span be cited wherever the 4 / 18 / 8 split appears, and the split appears in
`baseline_verdict.json`'s `H-BAND` entry and in `baseline_nstar.csv`'s band sizes without it. A
reader of the registration is told the span; a reader of the verdict record is not.

**4. `baseline_rejected_runs.csv` — discharged.** Unchanged and still sound: one row,
`parse_status` "stage not attempted", `runs_read` 0, `min_runs` 20, `guard_state` "not triggered -
stage never entered", with a reason naming the registered error condition explicitly. It is not the
empty file that, with zero runs read, the registration defines as an error rather than a pass.

**5. `baseline_board.png` — discharged, and §8's description is now accurate.** I read the figure
again: five curves (random expert subsample, model-assisted, Bayesian at both prior weights,
stratified) over four procedures, plus the judge-only projection and uninformative guess as reference
lines and the judge census as a point. v31 §8 now says "five curves over four procedures — the
shrinkage estimator contributes two, one per prior weight — and three points", which matches the
figure and its title. The plotted values agree with the tables at every point I checked: subsample
4.185 at `n` = 3 falling to 0.7206 at 100, shrinkage at weight 50 from 0.6388 to 0.5130, weight 10
peaking at 1.1431 at `n` = 10, judge-only 4.1259, constant 0.6304, census 0.0851. The caption names
all three arms with their prompt conditions, records `B7` and `B8` as NOT ATTEMPTED "reported as not
assessed rather than as a loss", and records band selection as WITHDRAWN and not plotted.

**6. Reporting obligation 3, "not assessed", never a loss — discharged.** The sensitivity file's
verdict column, the figure caption, §8's row for the sensitivity file, and §8's row for the board
figure ("the two not-attempted procedures absent rather than shown as losses"). No band cell reads as
a loss anywhere.

**7. Amendment 5's priority claim — discharged.** v31 §9 bullet 3 states the claim, states that the
store cannot corroborate the order because the registration version carrying it and the first values
were saved in one call, and names the substitute check. I reproduced the substitute:
`board_stratified_grid.csv` gives `met` = 1, 2, 1 with `best_ratio` 0.888819, 0.875984, 0.753553, and
I derived the same three counts independently from `board_stratified.csv` against
`board_stratified_srswor.csv`. The verdict does not turn on the allocation.

**8. The unnumbered `AMENDED` block's timing — discharged** in the second form my ruling allowed.
v31 §9 bullet 4 records that it carries no timing disclosure, that it created the constants the later
anti-search clause governs, that no verdict depends on them because band selection is withdrawn
untested, and that a future registration may not inherit them without restating their provenance.

**9. Amendment 2(a) must sit with the verdicts — discharged.** The `_scaling` key states that every
verdict is on the registered relative scaling, that no absolute-scaling counterpart exists, and that
the choice was made after both scalings were seen to disagree. v31 §2 and §9 carry it too.

**10. Amendment 2(b)'s rationale — discharged, and the correction's own defect is now repaired.**
Amendment 6 of v9 and v31 §9 bullet 2 both record that "the added points cannot change a verdict" is
true of which points are counted and false of their values. Re-verified from `baseline_curves.csv`:
the counted points sit at 2.2447 at `n` = 10 and 1.0268 at `n` = 50 against the pre-amendment 2.2609
and 0.9909 recorded in `baseline_anchor_en.md` §2. One residual of wording: v31 §9 bullet 2 still
points only at `closure_certification_en.md` for the pre-amendment values, where the registration now
points at `baseline_anchor_en.md` §2 and §5 as well. Both pointers are true; the plan's is the
narrower one.

**11. Every statement about "the judge" names the arm and prompt condition — discharged in the plan
and the briefs, still partly open in `user_benefit.csv`.** v31 §0 names all three arms with their
prompt conditions and states the rule; the four briefs each declare their arm and name the arm they
are *not* speaking about; `baseline_verdict.json` carries a `_judge_arms_in_play` block with the
obligation quoted. `user_benefit.csv` now names the arm on the refusal row, which was the blocker.
Two residuals remain in that file, which has no convention line of its own: the row "Spend five
judgments instead of judging the pool" describes 4.13 as "the judge's count over the whole pool",
where 4.126 is the registered `JUDGE_LABELS` arm's projection from a 4.05 per cent sample — a
projection on 29 of 30 topics, as v31 §4 says — and the refusal row's *evidence* cell still gives the
over-count factor 5.1 with no arm in the cell itself. A third residual sits in v31 §7: "a sensitivity
of 0.6419 cannot. The difference is a property of the judge, not of either procedure", whose arm is
recoverable only from the rate in the preceding clause, in the section that closes by forbidding
exactly that form.

**12. Registration-integrity clause propagation — discharged.** v31 §9 bullet 5 records that the
auxiliary boundary and the estimator definitions are inherited from `greg_prereg.py`, which carries
no registration-integrity clause of its own. I re-confirmed the inheritance numerically:
`greg_prevalence_vs_quality.json` gives `crossing_prevalence` 0.008837039650394578, which is
`BAND_AUXILIARY` = 0.0088.

**13. Canonical-home drift — discharged for every item I recorded, with one new instance reported.**
The two duplicated paragraphs, "None of the four is decided", "All four hypotheses", the mis-ordered
seventh risk bullet and the two sentences denying the discharge are all absent from v31 — zero
occurrences, searched. The new instance is the `n*` per-band reading, where `baseline_verdict.json`
leads with 3 / 5 / 3 and the plan and CSV lead with 3 / 3 / 20 (§2, obligation 2 above).

**14. Store-versus-repository drift — discharged as a disclosure, and re-attempted this session
rather than carried.** v31 §9 bullet 6 records it as unverified. I walked both granted paths again:
the read-write repository holds 67,678 files and a `.git` directory, and a case-insensitive search
returns exactly six worktree copies of `_PREREG_ctext_floor.md`, which is not one of the fourteen
registrations. No copy of any registration is reachable, so the comparison `prereg_audit.csv`
describes still cannot be made from here and the one recorded difference is correctly carried rather
than re-checked.

**15. The three out-of-plan reporting obligations — discharged.** v31 §9 bullet 7 names the
phase-one SECONDARY analysis, the synthetic-judge G2 condition and the correlation test with no
registered home, and closes all three at the standing recorded in `hypothesis_standing_audit.md`,
with the closure rather than by a blanket deferral.

---

## 4. The nine forbidden moves, rechecked in v31

**1. Retrofitting the band-to-procedure map — closed.** No map appears anywhere in v31. §1 states
that none is registered and that a three-band-by-nine-procedure assignment is a larger free parameter
than the tolerance the anti-search clause protects; §10 records that a correct band instantiation is a
new registration, not an amendment.

**2. Restating an unregistered comparison as a verdict — closed in the plan, closed in the
consolidation index.** Zero occurrences of *superseded*, *survives*, *strengthens*, *falsifies* or
*decides* in v31, and zero of `SUPERSEDED` in `consolidation_sources.csv`; the `greg_prereg.py`
thread now reads "RECOMPUTED under the registered metric" and carries the prior-weight condition.
v31 §6 states that the ratio table is "a recomputation of the three sampling estimators under the
registered metric on the real population; no prior verdict is restated as a finding". One divergence
of standing travels rather than blocks and is named in §7 below: Appendix A2 row 1 labels the prior
judge-only-against-uninformative comparison **INCONCLUSIVE**, where the registration's own docstring
records that prior verdict as "judge-only does not beat an uninformative guess" on 16 of 30 topics
with Wilcoxon `p` = 0.839, and `baseline_verdict.json` carries the ruling's "CARRIED AS PRIOR, ON ITS
OWN METRIC ONLY". The plan's label is the more conservative of the three and is stamped with the
forbidden metric, so it under-claims rather than over-claims, but three documents give it three
different names and none says so.

**3. Reporting a conditional as support — closed, including in `user_benefit.csv`.** v31 §1, §6
("**This is conditional on the prior weight**") and §7 all carry it; `board_estimators_en.md` §5 and
§3 carry it; and the deliverable row now states the conditional in full. This is the move that was
live in that file for three rounds and is now closed.

**4. Closing a hypothesis on a substituted quantity — closed in the plan, LIVE in
`user_benefit.csv`.** v31 §1 and §6 both label the judge-derived-against-judge-free comparison "an
unregistered substitute for prediction 2's mechanism clause, not a closure of it", and §1 records the
mechanism clause as NOT MEASURED. The deliverable still reports the registered mechanism probability
— 0.82 at `n` = 10, 0.96 in the sparsest band — as "Measured on the registered scaling with its
mechanism". Nothing recomputed it. This is blocker 14 and the reason certification is refused.

**5. Transplanting a failure branch's consequence — closed.** The band-conditioned recommendation
stays deleted; v31 §1 states that because the hypothesis was never tested the FALSIFIED branch did
not fire and its consequence text does not apply. The residual is unchanged and admissible:
`user_benefit.csv` row 1 attributes its benefit to "Band selection · null" and says it "survives
every hypothesis outcome", which is description — `N` and an estimate of `p` deciding countability —
but it is the last place band-selection standing language appears.

**6. Closing `H-B7` as a null result — closed.** "NOT ATTEMPTED, no verdict. Nothing may be said
about this procedure in either direction, including that it is untested in a way that implies a
result." §3 credits the board with no comparison against an implemented competing system, and the
`baseline_rejected_runs.csv` letter-of-the-rule trap stays shut.

**7. Repopulating `BEST_FIXED` with only the procedures that have curves — closed.** v31 §1 states
that the comparator population cannot be identified without choosing it after seeing which procedures
ran, and `board_estimators_en.md` §5 retains the sentence that is the only other place the
restriction is named.

**8. Reading the pool band shift as a correction to the registered bands — closed.** §6 says the
registered boundary "is exposed in a known direction", that correcting it is a new registration and
that the band assignment stands as registered for anything already counted; §10 repeats it; no topic
is re-banded; Appendix A attributes the 0.0706 boundary to "the pool-measured rates of the arm that
was actually run".

**9. Switching metric or scaling to rescue a comparison — closed.** The scaling disclosure sits in
§2, §9 and the verdict file; the variance-versus-standard-deviation confusion is repaired with both
figures and their correct labels; both ratio bases are now reported with their minima; and the
prior-weight-10 count names both comparator realisations. The one basis still unstated is §7's
qualitative claim that moving a topic between bands beats raising the budget, which holds on the
ratio basis (band move 7.4× to 7.8×, within-band 3 → 100 5.8× to 6.6×) and fails on differences in
the sparsest band; §7 makes no numeric claim there, so it is a residual rather than a substitution.

---

## 5. Every number in v31 against its source

Recomputed this session, not carried from the certification of v30. Agreements are exact to the
precision printed unless a note says otherwise.

| value in v31 | source | agrees |
|---|---|---|
| 30 topics; 117,562 pairs | `baseline_inputs.csv`, 30 rows, `ΣN` = 117,562 | yes |
| eligibility factor 694; 0.00029 to 0.2018; median 0.0195 | `baseline_inputs.csv` `p` 0.000291 to 0.201754, ratio 693.83, median 0.019537 | yes |
| `JUDGE_LABELS` a stratified sample of 4,762 pairs; 4.05 per cent | Amendment 4(a); 4,762 / 117,562 = 4.051 % | yes |
| condition-A arm per-topic rates se 0.8486, sp 0.8794 | `clef_condA_bias.csv` medians 0.848571, 0.879444 | yes |
| judge-only reference a **relative error** of 4.126, median of \|(R̂−R)/R\| | `baseline_inputs.csv` median \|rel_bias\| 4.125854; `baseline_points.csv` B0 4.125854 | yes |
| pool arm over-counts by a factor of 4.006, = 1 + rel_bias; 29 of 30 | `pool_topic_rates.csv` median `R_llm/R` 4.006494, 29 topics over-count | yes |
| on one convention 5.126 against 4.006, 27.9 % apart | `baseline_inputs.csv` median `R_llm/R` 5.125854; 5.125854/4.006494 − 1 = 27.94 % | yes |
| 1,000 replicates, seeded per cell | `BOOTSTRAP_REPS` = 1000, `SEED` = 20260921 | yes (registered) |
| `EXCLUDE_IF_R_ZERO` fired on no topic; minimum `R` = 2; 30 retained | `baseline_inputs.csv` min `R` = 2 | yes |
| 3 pool-exhausted cells: `CD008760` at 75 and 100, `CD010860` at 100 | `baseline_curves.csv` `exhausted` flag, 3 rows, exactly those cells | yes |
| grid extended downward to 3 and 5; verdicts on six registered budgets; `n*` = 5 and the floor budget fall on an added point | `N_GRID` and `N_GRID_REGISTERED_SUBSET` | yes (registered) |
| nine procedures, three consuming nothing, two with no curve | enumeration in §3, consistent with the figure and tables | yes |
| **99,304 unique PubMed records**, the distinct `pmid` count in the qrels | `clef2017_abs_test.qrels`: 117,562 rows, 30 topics, **99,304** distinct `pmid` | **yes — previously unverifiable, now verified** |
| **27 participant runs**, the count recorded in `judge_consequence.json` | `judge_consequence.json` `n_runs` = **27** | **yes — previously unverifiable, now verified** |
| 117,553 pairs labelled; 9 absent; 0.008 per cent | stratum totals 108,822 + 8,731 = 117,553; 9/117,562 = 0.0077 % | yes |
| strict parse rate 1.0000, zero nulls, zero truncation | `pool_results_en.md` | brief-sourced; not independently reproducible |
| pool-wide se 0.6419, sp 0.9348 | `pool_topic_rates.csv`, `Σtp/ΣR` = 0.641896, `1 − Σfp/Σ(N−R)` = 0.934838 | yes |
| panel false-positive 0.1292 against 0.0645 outside | `panel_sample.csv` gives 1,200 non-eligible panel pairs; that split implies a pool rate of 0.065171 against the measured 0.065162 | **yes — now verified by identity** |
| sensitivity 0.6764 inside against 0.6143 outside | `panel_sample.csv` gives 825 eligible panel pairs; that split implies a pool se of 0.641889 against the measured 0.641896 | **yes — now verified by identity** |
| panel strata are the expert label itself, no off-diagonal cell | `panel_sample.csv` crosstab: 1,200/0 and 0/825 | yes (registered statement, now checkable) |
| run-to-run 0.0025; agreement 0.9906 and 0.9960; factor 26 | `pool_results_en.md`; the composition gap 0.1292 − 0.0645 = 0.0647 verifies, and 0.0647/0.0025 = 25.9 | composition verified; the three run-to-run figures remain brief-sourced |
| model-assisted 0.944 / 0.938 / 0.947 / 0.960 / 0.933 / 0.922, 0 of 6 | `board_estimators.csv` `rmse_E4` over `rmse_E2`: 0.9444, 0.9382, 0.9466, 0.9597, 0.9330, 0.9225 | yes |
| shrinkage weight 10: 0.513 / 0.674 / 0.755 / 0.849 / 0.882 / 0.920, 5 of 6 | 0.5132, 0.6743, 0.7553, 0.8491, 0.8818, 0.9201 | yes |
| weight 10 at 4 of 6 against the anchoring realisation | against `baseline_curves.csv` medians: 0.5093, 0.6563, 0.7479, 0.8002, 0.9005, 0.9310 → 4 | yes |
| shrinkage weight 50: 0.280 / 0.390 / 0.444 / 0.548 / 0.628 / 0.703, 6 of 6 | 0.2797, 0.3905, 0.4442, 0.5482, 0.6275, 0.7035 | yes |
| stratified 0.889 / 0.950 / 0.928 / 0.957 / 0.965 / 0.951, 1 of 6 | `board_stratified.csv` against `board_stratified_srswor.csv`, `proportional_min1` | yes |
| 1 of 6, 2 of 6, 1 of 6 across the three allocations | `board_stratified_grid.csv` `met` = 1, 2, 1; reproduced from the raw files | yes |
| zero-cost constant 0.6304 | `baseline_points.csv` B1 median `R` 0.630435 | yes |
| cleared from `n` = 5 at 0.6270, reaching 0.5130 | `board_estimators.csv` `rmse_EB50` medians 0.6270 at 5 and 0.5130 at 100; 0.6388 at `n` = 3 is above the constant | yes |
| at weight 10 the constant is never beaten within the grid | `rmse_EB10` minimum over the whole grid 0.6709 | yes |
| "the first board row ever to do so" | true among procedures measured on all 30 topics; the 4-topic judge census point sits at 0.0851 | yes, with a scope word missing |
| median relative bias 0.077 against 0.008 | over the six registered budgets, max \|`bias_EB50`\| 0.0766, max \|`bias_E2`\| 0.0076 | yes |
| judge-free target worse by 20 % at `n` = 3, better by 6 % at `n` = 100, crossing between 20 and 30 | `board_estimators_collection.csv` against `board_estimators.csv`: +19.78 %, −5.94 %, sign change between 20 (+3.22 %) and 30 (−1.76 %) | yes |
| 35.8 per cent of eligible in the stratum holding 92.6 per cent | 665/1,857 = 0.3581, i.e. 1 − se; 108,822/117,553 = 0.9257 | yes |
| 108,822 documents at 0.0061 against 8,731 at 0.1365 | `board_stratified.csv` stratum sizes; 665/108,822 = 0.006111; 1,192/8,731 = 0.136525 | yes |
| weighted within-stratum variance falls only 7.5 % | 0.014378 against 0.015548, ratio 0.924786 | yes |
| design effect for the standard deviation 0.96166, a reduction of 3.8 per cent | √0.924786 = 0.961658; 1 − 0.961658 = 3.83 % | **yes — the v30 error is corrected** |
| per-topic variance ratio median 0.9213, range 0.5886 to 0.9994 | recomputed per topic from the `pool_topic_rates.csv` strata | yes |
| a variance reduction of 7.9 per cent and therefore an RMSE gain of 4.01 per cent | 1 − 0.9213 = 7.87 %; 1 − √0.9213 = 4.01 % | **yes — the v30 error is corrected** |
| ratio of medians never below 0.7536 | minimum over three allocations × six budgets 0.753553 (`neyman_judge`, `n` = 10) | yes |
| median of per-topic ratios never below 0.8605 | minimum over the same grid 0.8605 (same cell) | **yes — the announced second basis is now reported** |
| `n*` = 5 on both scalings | 4.1850 and 143.9479 at `n` = 3 against 4.125854 and 130.151515; 2.9773 and 105.9851 at `n` = 5 | yes |
| 3 / 3 / 20 against 5 / 3 / 3 in the order auxiliary, countable, uninformative | collection-wide B0: 3, 3, 20; band-own B0 (2.9417, 1.6023, 27.0848): 5, 3, 3 | yes |
| neither per-band reading is registered; the registration fixes `n*` against *the B0 point* | `baseline_prereg.py` `NSTAR_NOT_REACHED` block, which registers no per-band quantity | yes (registered) |
| "five expert judgments bring the error below it; three do not" | 2.9773 at `n` = 5 and 4.1850 at `n` = 3 against 4.125854 | yes |
| no budget in the grid attains a lower error than the constant until a shrinkage estimator is used | minima over the six budgets: 0.7292 subsample, 0.6726 model-assisted, 0.6709 weight-10, 0.6831 stratified, all above 0.6304; weight 50 below at all six | yes |
| boundary 0.0706 against predicted 0.1373 to 0.3361; countable band 4 widening to 5 | `pool_band_shift.csv` 0.070578; recomputed from the closed form with pool rates; 4 topics at `p` ≥ 0.090158 and 5 at `p` ≥ 0.070578 | yes |
| `CD010860` crossing in | `baseline_inputs.csv` `p` = 0.074468 | yes |
| `p*` = 0.0902 at the registered instantiation | `band_countable(0.6412, 0.9149, 0.5)` = 0.090158 | yes |
| auxiliary boundary 0.0088 | `greg_prevalence_vs_quality.json` `crossing_prevalence` 0.008837 | yes |
| 16 of 30 topics, not significant, on \|log error\| | registration docstring, Wilcoxon `p` = 0.839 | yes (registered) |
| identity exact over 54 rows, 4 topics | registration docstring and `baseline_verdict.json` | yes (registered) |
| 613 expert judgments; 11 of 30 topics reaching half the relative error | `price_across_regimes.csv` `n_med` 613.0; 11 topics reach relative error ≤ 0.50 at some budget ≤ 100, median first budget 75 | yes |
| "the working plan reached its twenty-sixth version, twenty-five revisions after the original" | 31 stored versions of the file; the last working-plan version was 26 | **yes — the v30 overstatement is corrected** |
| §8: "five curves over four procedures … and three points" | the figure: five curves, four procedures, two reference lines and one point | **yes — the v30 notation slip is corrected** |
| "a projection on 29 of 30 topics and not a census" | the 4,762-pair `JUDGE_LABELS` file is not among the sources given | **unverifiable** |

---

## 6. What the corrections introduced

Three new items. One is a blocker, two travel.

**1. The registration pointer is stale again.** `baseline_verdict.json` `_registration` was moved
from v7 to v8 in the same work that moved the registration from v8 to v9, so the closure's verdict
record names the version whose Amendment 6 still carries the false reason. This is the third round in
which a version bump and its pointer have moved out of step. It is blocker A in §7.

**2. A doubled em dash in v31 §4.** "back the 117,562 pairs — the distinct `pmid` count in
`clef2017_abs_test.qrels` — — fewer than the pairs". Notation only, in the plan's own prose, and it
does not touch a claim.

**3. §9 bullet 2 now points at a narrower set of locations than the registration does** for the
pre-amendment values: the plan names `closure_certification_en.md` alone where Amendment 6 names
`baseline_anchor_en.md` §2 and §5 as well. Both statements are true; the plan's is the less useful
one.

Nothing in this round moved a disposition, relaxed a threshold, restated a prior verdict as a
finding, or converted a conditional into support. The two corrections that repaired scale confusions
are correct in both directions, which is the thing that most needed checking: 7.5 per cent is
labelled a variance fall and 3.8 per cent a standard-deviation reduction; 7.9 per cent is labelled a
variance reduction and 4.01 per cent an RMSE gain.

---

## 7. The certification

**The hypothesis verification cannot be declared closed. The declaration sentence is withheld for
the third time.**

Fourteen of the sixteen blockers are cleared, and the record is now materially sound: the primary
hypothesis is quoted from the registration rather than paraphrased, all three withdrawal grounds are
stated, both scale confusions are repaired with both figures correctly labelled, both ratio bases are
reported with their true minima, the added-point provenance of `n*` = 5 is disclosed, the per-band
`n*` reading is labelled a disclosure in all three places that carry it, the two figures that were
unverifiable last round now verify against named sources, two of the six brief-sourced figures verify
by identity, and the two consolidation-index defects and three of the four verdict-file defects are
gone.

Two blockers remain. Neither requires a run.

**A. `baseline_verdict.json` `_registration` names `prereg/baseline_prereg.py v8 (Amendments 2-6)`
while the authoritative registration is v9.** *Smallest action:* change `v8` to `v9`. I verified that
no threshold, grid or verdict differs between the two versions, so nothing else moves with it.

**B. `user_benefit.csv`, row "Stop paying where a constant is as good", reports prediction 2's
registered mechanism probability as measured.** The *satisfied by the anchoring run* cell reads
"Measured on the registered scaling with its mechanism … explained by a median probability 0.82 of
catching no eligible document at n = 10", and the *evidence* cell gives 0.82 at `n` = 10 and 0.96 in
the sparsest band as the mechanism. The closure records that clause as NOT MEASURED. *Smallest
action:* delete "with its mechanism" and the clause "explained by a median probability 0.82 of
catching no eligible document at n = 10" from the *satisfied* cell, and in the *evidence* cell label
0.82 and 0.96 as the registration's own pseudo-population values, never recomputed on the pool.

**When those two are cleared**, the declaration is unchanged from the one I set out in the first
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
stated; leaving prediction 2's registered mechanism clause as not measured unless the hypergeometric
computation on inputs in hand is elected; naming the arm and prompt condition wherever the judge's
labels are described; reporting every count with the comparator realisation it was computed against
where two realisations exist; reporting `n*` = 5 with the disclosure that 5 is a budget Amendment
2(b) added after the anchoring run and is not one of the six points verdicts are counted on; and
carrying the relative-scaling choice, the grid extension, the two unverifiable timing disclosures and
the unreachable registration copies as disclosures rather than as resolved questions.

### What a reader of the closure must be told and is not

Five things. None of them is a blocker; each travels with the closure and should be stated in it.

1. **Two arms are called "registered" in one record.** v31 §0 defines the registered `JUDGE_LABELS`
   as `gpt-4o-mini` condition A, while §6 and §1 call the pool-judging arm "the registered arm".
   `FULL_POOL_JUDGE` registered only "open-weight, bfloat16, single A100 40GB" — neither arm nor
   prompt condition — so the arm that produced the auxiliary variable, the strata and the pool-wide
   rates was free when the run was chosen. No document says this in the same place as the phrase.
2. **The per-band `n*` reading differs between canonical copies.** `baseline_verdict.json` leads with
   3 / 5 / 3 against each band's own reference; v31 §6 and `baseline_nstar.csv` lead with 3 / 3 / 20
   against the collection-wide reference. Neither is registered, both are recorded, and no document
   notes that the two records lead with different numbers.
3. **The prior judge-only-against-uninformative comparison has three different names.** The
   registration's docstring says "judge-only does not beat an uninformative guess"; the ruling and
   `baseline_verdict.json` say "CARRIED AS PRIOR, ON ITS OWN METRIC ONLY"; v31 Appendix A2 says
   **INCONCLUSIVE**. The plan's is the most conservative reading of a Wilcoxon `p` = 0.839 on 16 of
   30 topics, but it is a re-characterisation of a prior verdict and is not disclosed as one.
4. **Four of the figures behind the reason prediction 1 failed are brief-sourced only.** The
   run-to-run false-positive difference 0.0025, the four-grade agreement 0.9906, the binarised
   agreement 0.9960 and the strict parse rate 1.0000 cannot be reproduced from anything in the store
   that was given to me. The composition effect they are compared against — 0.0647 — does reproduce,
   and so does the panel/pool split itself, so the *direction* of the explanation is verified and the
   factor of 26 is not.
5. **The arm-by-tolerance span is not cited where the band split appears.** `baseline_verdict.json`
   and `baseline_nstar.csv` report 4 / 18 / 8 without the sensitivity that `baseline_band_sensitivity.csv`
   holds — `p*` from 0.018905 to 0.156463 and the countable count from 2 to 16 of 30. A reader of the
   registration is told; a reader of the verdict record is not.

### Items reported as unverifiable

- **"A projection on 29 of 30 topics"** — the 4,762-pair `JUDGE_LABELS` file is not among the sources
  given, so the 29 cannot be recomputed. *Travels; does not block.* It is a disclosure that weakens
  the reference point rather than a claim resting on it.
- **The three run-to-run figures and the strict parse rate** — no second set of labels on the same
  pairs and no completions file exists among the sources. The nearest stored table,
  `guided_failure_agreement.csv`, measures a different comparison and gives 0.9975 and 0.9995 for
  `qwen3-8b` condition C, so it neither confirms nor contradicts the quoted pair. *Travel; do not
  block.*
- **Store-versus-repository drift** — re-attempted this session on both granted paths; no copy of any
  of the fourteen registrations is reachable. *Travels; does not block*, and is already disclosed in
  v31 §9.
- **Amendment 5's priority and the unnumbered `AMENDED` block's timing** — not evidenceable from the
  store; both are disclosed as such, and no verdict turns on either. *Travel; do not block.*

---

## 8. Scope of this certification

- All sixteen blockers, all fifteen recording obligations and all nine forbidden moves were checked;
  none was sampled.
- Every number in v31 was recomputed from the file it cites, in the table at §5, including the six
  that were certified only as internally consistent last time. Two of those six became verifiable
  when `panel_sample.csv` supplied the panel's composition (1,200 non-eligible and 825 eligible
  pairs), and they verify as the unique decomposition consistent with the pool aggregates. Four did
  not: `panel_sample.csv` carries one label column, the `gpt-4o-mini` grades, and no second run of
  the pool arm, so the run-to-run figures and the parse rate remain brief-sourced.
- Registered statements are quoted verbatim from `baseline_prereg.py` v9 and are not subject to the
  notation and informality checks applied to the plan's own prose. One quotation differs from the
  registration in sentence-initial capitalisation only — v31 §9 renders "so the added points cannot
  change a verdict" as *"The added points cannot change a verdict"* — which is quotation practice,
  not a deviation.
- Conditional dispositions stay conditional: the zero-cost-floor clause remains falsified and
  conditional on an unregistered prior weight, `H-B6` remains not supported and not conditional on
  allocation, and prediction 2's mechanism clause remains not measured.
- Where the plan and the registration disagree, the registration governed. They disagree nowhere on a
  threshold, a grid or a verdict.
- No experiment was run, no result was computed as a new finding, no document was repaired, and no
  disposition was changed.

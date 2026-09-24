# Certification of the closure — refused

Referee certification of the work claimed to discharge `closure_ruling_en.md`, checked against
`experiment_plan_en.md` v26, `baseline_prereg.py` v7 (authoritative wherever it and the plan
disagree), the five newly created outputs, and the value tables behind them. No experiment was run,
no result was computed as a new finding and no document was repaired. Every transcription named
below was recomputed from the file it claims to come from; where I could not recompute a figure
from the sources named in the brief, I say so.

**Verdict: the hypothesis verification cannot be declared closed.** Four of the five declared
outputs are sound and one is incomplete; two of the nine forbidden moves are still live in v26 in
their original words, a third is live in a new place, and eight of the fifteen recording
obligations are open or only partly discharged. The blockers are listed in §5 with the smallest
action that clears each. None of them requires an experiment.

---

## 1. The fifteen recording obligations

### 1. `baseline_verdict.json` — **partly discharged**

The file exists and carries 17 entries (16 dispositions plus the out-of-plan scope statement), each
with a `threshold_as_registered` field. Checked item by item against what the ruling required it to
carry:

- **`H-B6` NOT SUPPORTED with the threshold echoed and all three allocation counts** — present. The
  threshold is echoed as values ("median RMSE of B6 <= 0.90 x median RMSE of B3 at >= 4 of the 6
  grid points") rather than as the constant names `HB6_RATIO` / `HB6_MIN_GRIDPOINTS`, which meets
  reporting obligation 1 as written. The three counts 1, 2 and 1 of 6 reproduce exactly from
  `board_stratified_grid.csv` (`met` = 1.0, 2.0, 1.0; best ratios 0.888819, 0.875984, 0.753553).
  One omission of substance: the same source file labels the pure-proportional cell **PARTIAL**,
  which is the registered label for a 2-of-6 result, and the entry reports the count without that
  label. The verdict is unaffected — the primary allocation governs and no allocation reaches 4 —
  but the registration's own label for a reported cell is dropped.
- **`H-B7` NOT ATTEMPTED** — present, with the registered ratio and gridpoint constants named.
- **`H-B8` NOT ATTEMPTED** — present. The registration's mandated entry now has a home.
- **`H-BAND` WITHDRAWN with the three grounds** — present, all three (no registered map; `BEST_FIXED`
  unidentifiable because two of the nine procedures have no median RMSE at any budget; the
  zero-budget-band spend unstated), with the instantiation `(haiku_A, t = 0.5)` and 4 / 18 / 8.
- **The `R` = 0 topic exclusion** — **absent.** `EXCLUDE_IF_R_ZERO` requires that the exclusion be
  "written to baseline_verdict.json"; the file contains no such record in any form. The content is
  available and I verified it: `baseline_inputs.csv` has 30 topics with minimum `R` = 2, so the
  correct entry is that the rule fired on no topic and all 30 are retained. A rule that excluded
  nothing still has to be recorded as having excluded nothing.
- **The Amendment 3 pool-exhausted cells** — **absent.** Verified from `baseline_curves.csv`: three
  cells over two topics — `CD008760` (`N` = 64) at `n` = 75 and `n` = 100, and `CD010860` (`N` = 94)
  at `n` = 100. Note for whoever writes the entry: **the registration's own prose for this amendment
  is wrong** and must not be transcribed. Amendment 3 reads "1 topic at `n` = 75 (CD010860, N = 94)
  and 2 at `n` = 100 (that topic plus CD008760, N = 64)"; a pool of 94 is not exhausted by a budget
  of 75, and the curves file flags `CD008760` at that cell. The counts (one cell at 75, two at 100)
  are right and the topic named at `n` = 75 is not.
- **The `P1` and `P2` clause verdicts with their registered wordings** — present, all six clauses,
  each quoting the registered wording verbatim.

Two further defects, both of the letter-not-purpose kind. Five of the seventeen entries (Appendix B
rows 1 to 3, the §0 "Established" table, the out-of-plan statement) fill `threshold_as_registered`
with "see closure_ruling_en.md section 3" rather than the threshold. For at least three of those the
registered basis exists and is quotable — |log error| with 16 of 30 and Wilcoxon `p` = 0.839 plus the
metric-voiding rule for row 1, `IDENTITY_TOL` = 1e-6 for row 2, and `greg_prereg.py`'s joint rule
(lower relative RMSE **and** |bias| within ±0.05) for row 3 — so the field points at the ruling where
it could carry the threshold. And two entries assert states the file's own existence falsifies: the
`H-B8` entry ends "The recording obligation is unmet until baseline_verdict.json exists", and the `n*`
entry ends "that file does not exist" of `baseline_nstar.csv`. Both files now exist.

### 2. `baseline_nstar.csv` — **discharged**, with one rounding note and one addition

Every value recomputed from `baseline_curves.csv` and `baseline_points.csv`:

| claim | file | recomputed | agrees |
|---|---|---|---|
| collection `n*`, relative | 5 | 5 (median 4.185 at `n` = 3 against B0 4.125854; 2.9773 at `n` = 5) | yes |
| collection `n*`, absolute | 5 | 5 (143.95 at `n` = 3 against B0 130.151515; 105.99 at `n` = 5) | yes |
| per band against that band's own B0 | countable 3, auxiliary 5, uninformative 3 | 3 / 5 / 3 | yes |
| per band against the collection-wide B0 | countable 3, auxiliary 3, uninformative 20 | 3 / 3 / 20 | yes |
| band-own B0 reference values | 1.602 / 2.942 / 27.085 | 1.6023 / 2.9417 / 27.0848 | yes |

The ruling's disposition is the per-band reading 3 / 5 / 3 "each against the judge-only point within
that band", and that is what rows 5 to 7 carry. Every band row carries
`(BAND_ARM = haiku_A, condition A, BAND_TOLERANCE = 0.5)`, satisfying reporting obligation 5; the two
collection rows correctly carry none, having no band label to qualify.

Two observations. The absolute reference is written **130.200** where `baseline_points.csv` has
**130.151515** — a one-decimal rounding presented to three decimals, matching §6 of the plan but not
the source. And the file adds a second reading of `n*` (per band against the collection-wide B0,
3 / 3 / 20) that the ruling did not authorise: the obligation was transcription only. I recomputed
it and it is correct, it is disclosed in the file as an ambiguity in how the registration defines
"the B0 point", and it produces no verdict — so it is admissible. It is nonetheless a new quantity
rather than a transcription, and the ambiguity it discloses is one the ruling did not name.

### 3. `baseline_band_sensitivity.csv` — **discharged as to the file; partly as to the citation**

24 rows over six arms and four tolerances. The `hband_verdict` column reads
"not assessed - H-BAND withdrawn untested" at **every** row, so the file is not a grid of a verdict
computed on a repopulated comparator, which the ruling forbade, and it satisfies reporting
obligation 3 in the place that obligation most matters. I recomputed the whole grid: `p_star`
reproduces the registered closed form `(1 - sp)/(t + 1 - se + 1 - sp)` at every row (maximum
deviation 1e-16), and all 24 (countable, auxiliary, uninformative) triples reproduce from
`baseline_inputs.csv` given each row's `p_star` and the registered auxiliary boundary 0.0088. The
span 0.018905 to 0.156463 and the countable count 2 to 16 of 30 match the registered sensitivity
statement exactly.

The second half of the discharge — citing the descriptive sensitivity "wherever the 4 / 18 / 8 split
appears" — is met at §0 (via appendix A), appendix A and §9 of v26, and not at §7, where "4 / 18 / 8
stands for every verdict already counted" appears with no sensitivity citation.

### 4. `baseline_rejected_runs.csv` — **discharged**

One row: `parse_status` = "stage not attempted", `runs_read` = 0, `min_runs` = 20, `guard_state` =
"not triggered - stage never entered", with a reason naming the registered error condition. This is
the disposition the ruling required and is explicitly not the empty file that, together with zero
runs read, the registration defines as an error rather than a pass.

### 5. `baseline_board.png` — **discharged**

Exists; four procedures as curves (random subsample, model-assisted, Bayesian at both prior weights,
stratified) and three as points (judge-only projection, uninformative guess, judge census on 4
topics), consistent with `baseline_curves.csv` and `baseline_points.csv` at the values I spot-checked
(B0 ≈ 4.13, B1 ≈ 0.63, subsample 4.185 at `n` = 3, Bayesian 50 from 0.627 to 0.513). The caption
carries more of the ruling's disclosures than the plan does: the pool-wide arm and prompt condition
by name, the judge-only projection as the condition-A stratified projection on 29 of 30 topics,
`B7` and `B8` as NOT ATTEMPTED "reported as not assessed rather than as a loss", and band selection
as WITHDRAWN and not plotted.

### 6. Reporting obligation 3, "not assessed", never a loss — **discharged**

All three places it can appear now say it: the sensitivity file's verdict column, the figure caption,
and Appendix B of v26, where both `B7` and `B8` read "**not assessed — NOT ATTEMPTED**".

### 7. Amendment 5's priority claim — **discharged**

v26 records it twice, in §6 with the stratification result and again in the new appendix A2: the
amendment states it was fixed before any value existed, the pre-registration version carrying it and
the first values were saved in one call, so the store cannot evidence the order. Both places carry
the insensitivity (1, 2, 1 of 6, and 0, 1, 1 against the anchoring realisation).

### 8. The unnumbered `AMENDED` block's timing — **discharged**

Appendix A2 records that the block created `BAND_ARM` and `BAND_TOLERANCE` — the constants the later
anti-search clause governs — and carries no timing disclosure relative to the first RMSE, and that
the absence is recorded so a future registration cannot inherit those constants without restating
their provenance. That is the second of the two forms the ruling allowed.

### 9. Amendment 2(a) must sit with the verdicts — **partly discharged**

v26 §6 result 2 reports the absolute-scaling reversal beside the relative figures, and §7 states that
every verdict inherits the choice. What is still missing is the part that makes the disclosure bite:
that **every verdict counted is a relative-scaling verdict with no absolute-scaling counterpart**,
which remains only in `board_stratified_en.md` §5. And `baseline_verdict.json`, which is now the
machine-readable home of the verdicts, carries no scaling disclosure in any entry.

### 10. Amendment 2(b)'s rationale overclaims — **open**

Neither v26 nor `baseline_verdict.json` records the correction. I re-verified the fact from
`baseline_curves.csv`: the counted points themselves moved under per-cell seeding — median relative
error 2.2447 at `n` = 10 and 1.0268 at `n` = 50, against the 2.2609 and 0.9909 of the earlier
realisation. v26 repeats only the true half ("verdicts stay on the six registered points", §2 step 5
and §10 item 8); the amendment's stronger claim that the added points "cannot change a verdict" is
still uncorrected, and no verdict crossing is at stake, which is precisely why the correction is
cheap.

### 11. Every board statement about "the judge" must name the arm and prompt condition — **partly discharged**

Discharged in the two new files: `baseline_verdict.json` opens with a `_judge_arms_in_play` block
naming all three (pool-wide `qwen3-8b` condition C; band assignment `haiku_A` condition A; registered
`JUDGE_LABELS` `gpt-4o-mini` condition A), and the figure caption names them too. **Not discharged in
the plan.** v26 contains no occurrence of "qwen3", "condition C" or "gpt-4o-mini". §4 and §5 say "one
open-weight arm" and "an open-weight model"; §6 attributes the pool-wide `se` 0.6419 and `sp` 0.9348
(both of which I reproduced from `pool_topic_rates.csv`), the strata and the auxiliary variable to
"the registered arm". So the document that carries the board's prose never says that the arm supplying
the strata and the auxiliary variable is on a **different prompt condition** from the arm supplying
the band assignment — which is the whole content of the obligation. The same gap is live in
`user_benefit.csv`, whose first row states "a judge-derived denominator is over-counted by a median
factor of 5.1" with no arm named (that figure is the condition-A projection basis: I get 5.126 with
28 of 30 over-counting from `baseline_inputs.csv`, against 4.0065 with 29 of 30 from
`pool_topic_rates.csv`, and v26 §6 correctly quotes 4.006 for the pool arm — two true numbers for two
different arms, one of them unlabelled).

### 12. Registration-integrity clause propagation — **partly discharged**

The two carriages are disclosed: `baseline_verdict.json`'s out-of-plan entry records that
`BAND_AUXILIARY` = 0.0088 is inherited from `greg_prereg.py`'s secondary analysis and that the
estimator definitions are transcribed from the lineage of `greg_faithful.csv`, a file the plan calls
superseded and not carried. What is not recorded anywhere is the fact the obligation is about: that
`greg_prereg.py` is one of six registrations carrying **no integrity clause at all**, so the board's
auxiliary boundary and estimator family are inherited from a registration with no bar on post-hoc
revision. v26 contains no occurrence of "integrity".

### 13. Canonical-home drift reported in v24 — **partly discharged, two of five**

- The two duplicated paragraphs are gone: the §1 "Undecidable as registered, and not for the reason
  this section guards against" block and the `P2` "The registered mechanism clause is that
  probability" block each appear **exactly once** in v26. Discharged.
- §7 still opens "**None of the four is decided.**" two paragraphs before reporting stratification as
  not supported, and its subsidiary paragraph still calls stratification "Untested". The sentence has
  also multiplied: §10's preamble now reads "The four hypotheses are undecided, so the experiment
  continues." Open.
- §1 still says "All four hypotheses are directional and share one threshold" in a section that
  enumerates five objects. Open.
- §9 is still titled "The seven risks that matter" with six bullets, the companion-files line, and
  then the seventh bullet. That seventh bullet — "**The auxiliary variable does not yet exist over the
  pool**" — is now also contradicted by §3, §4 and §6 of the same document, which report that it does.
  Open, and worse than in v24.
- **New drift created by the discharge itself.** §1 states "`baseline_verdict.json` does not exist"
  and "`baseline_band_sensitivity.csv`, a required output, does not exist yet". Both files now exist.
  The plan denies the discharge it is supposed to record.

### 14. Store-versus-repository drift — **open, and still unverifiable**

Not recorded in v26 (no occurrence of "repository" or "prereg_audit"). I re-checked the granted host
paths in this session rather than carrying the earlier finding: neither `/Users/seohyunwon/project/cartograph`
nor the read-only reading folder contains any `*prereg*` file, and no `origin/prereg` ref resolves in
that repository. So the comparison `prereg_audit.csv` describes still cannot be made from here, and
the obligation is discharged by recording that, not by performing it.

### 15. Two reporting obligations outside the live plan, and the homeless test — **partly discharged in letter only**

`phase1_falsification.py`'s SECONDARY ("reported either way", reported nowhere),
`synthjudge_prereg.py`'s guard G2 (inputs exist, tracking check stated nowhere) and the correlation
test `synthjudge_results_ko.md` §5 withdraws with no registration file to withdraw it from are named
in **none** of the closure documents: v26 has no occurrence of "phase1" or "synthjudge", and neither
does `consolidation_sources.csv`. The only carrier is `baseline_verdict.json`'s blanket "closed at
the standing recorded in `hypothesis_standing_audit.md`". The audit does record all three, so the
letter is met by reference; the purpose — recording them **with** the closure so they are not left
open — is not.

---

## 2. The nine forbidden moves, rechecked in v26

**1. Retrofitting the band-to-procedure map and calling it an amendment — closed.** No map appears
anywhere in v26. The §1 sentence "the band assignment under test is **fixed to the registered
instantiation**" survives, but it is now immediately followed by the paragraph stating that no map
from band to procedure is registered, which removes the false implication the ruling objected to.
§10 item 7's reasoning against a restricted run is intact, and appendix A2 closes the amendment
precedent that would have been used.

**2. Restating an unregistered comparison as a verdict — still live, in two of the three named
places.** The word *falsifies* is gone from §6, which now reads "That is the measurement the plan's
null hypothesis asks for, not a registered verdict". But Appendix B row 3 still reads
"**superseded by §6** — on the pool the Bayesian arm is preferred and the model-assisted one is not",
and §3 still reads "Its model-assisted verdict survives the change and its Bayesian verdict
strengthens (§6)". These are the exact words `baseline_verdict.json`'s own Appendix-B-row-3 entry
quotes as **inadmissible** and surrenders. The closure therefore contains a file declaring a wording
forbidden and a document still using it.

**3. Reporting a conditional as support — closed in v26, live outside it.** §6 names prior weight 50
and the bias it buys; §1's third qualification and §7's caveat state the conditionality. Outside v26:
`board_estimators_en.md` §2 is still headed "The zero-cost floor is cleared for the first time" and
still calls it "the first board row to answer the question the plan says a practitioner actually
asks", with the weight named but the conditionality nowhere; and `user_benefit.csv`'s row "Stop paying
where a constant is as good" still asserts "an estimate that costs nothing is not improved on by any
budget tested" — a clause this same closure records as **falsified** in `P2` (c).

**4. Closing a hypothesis on a substituted quantity — still live.** §6 still says a judge-free variant
of the Bayesian arm "is what **decides** the mechanism half of prediction 2", two sections after §1
declares that same quantity an unregistered substitute that does not close the clause; and §1's own
`P2` verdict paragraph still narrates the substitute as splitting the claim at `n` = 30. The
disclosure was added and the claim it contradicts was left in place. Outside v26, `user_benefit.csv`
still reports the registered mechanism probability (0.82 at `n` = 10) as "measured on the registered
scaling with its mechanism", which is the assertion the ruling called out: nothing recomputed it.

**5. Transplanting a failure branch's consequence — closed in Appendix B, still live in §7.** Both
Appendix B rows now state that the branch did not fire and its consequence text does not apply. But
§7 still reads "The sharper recommendation §7 anticipated — *do not buy expert judgments unless the
topic's band warrants it* — survives, with the caveat that its floor now depends on an unregistered
prior weight." The caveat that was added answers move 3. The objection was move 5: this is a
band-conditioned recommendation surviving on evidence that never tested band selection. **Satisfied in
letter, not in purpose.**

**6. Closing `H-B7` as a null result — closed.** Appendix B records NOT ATTEMPTED with no statement in
either direction; §6 says not run; `baseline_rejected_runs.csv` records the stage as not attempted
rather than as an empty file, so the letter-of-the-rule trap the ruling named is shut. Residual: §3's
sentence that `B7` "is required for the comparison to be against an implemented system rather than a
description" still stands unmarked, and that credit is what the disposition surrenders.

**7. Repopulating `BEST_FIXED` with only the procedures that have curves — closed.** §10 item 7 keeps
the reasoning verbatim, `board_estimators_en.md` §5 still carries the sentence the ruling identified
as the only place the restriction is named, and §1 now states the comparator ambiguity outright.

**8. Reading the pool run's band shift as a correction to the registered bands — substantially closed,
with one residual.** §7 keeps "likely too high ... too narrow" but now adds that it cannot be
corrected inside this registration and that 4 / 18 / 8 stands for every verdict already counted; §9's
first risk states the direction is known and the magnitude for `haiku_A` unmeasured. No topic is
re-banded anywhere. The residual is a consequence of obligation 11 being open: because v26 never names
the pool arm, it never says that the measured 0.0706 boundary belongs to a **different arm** than the
one the registered bands use.

**9. Switching metric or scaling to rescue a comparison — closed as to disclosure.** §6 result 2
reports the absolute-scaling reversal at `n` = 100 (25.5 against 26.0) in the same breath as the
relative result, and §7 states that every verdict inherits the choice. The missing half is recorded
under obligation 9 above.

---

## 3. The five new files against the ruling's own dispositions

**Does each verdict carry the threshold it was tested against?** Every entry has the field; three
kinds of filling. Six declared-prediction clauses correctly read "declared prediction, no registered
threshold". Four registered objects carry real thresholds, of which only `H-B7` names the registered
constants. Five entries defer to "see closure_ruling_en.md section 3" where a threshold exists and
could be quoted, and `H-B8` reads "same threshold, optional procedure" rather than the registered 0.90
and 4 of 6. Reporting obligation 1 asks the verdict to **echo** the threshold; a pointer is a thin
echo.

**Is every band label carrying its instantiation?** Yes in `baseline_nstar.csv` (all band rows), yes
in `baseline_band_sensitivity.csv` (arm and tolerance are columns), yes in the `H-BAND` verdict entry,
yes in the figure caption. One miss: the `n*` entry of `baseline_verdict.json` states the per-band
3 / 5 / 3 without the `(arm, t)` in that sentence — it appears only in the entry's surrender clause,
which is one of the two stale clauses noted above.

**Is anything recorded as a loss that the ruling requires be recorded as not assessed?** No, in all
four places where the temptation exists: the sensitivity grid, the figure, Appendix B and the rejected
runs file. The converse error exists once, outside the five files: `user_benefit.csv` records as
*measured* the `P2` mechanism quantity that the ruling closes as **not measured**.

**New-file defects, consolidated.** (i) the `R` = 0 exclusion is missing; (ii) the Amendment 3
pool-exhausted cells are missing, and the registration's prose for them names the wrong topic at
`n` = 75; (iii) five thresholds are replaced by a pointer and `H-B8`'s is not the registered pair;
(iv) two entries assert that files which now exist do not; (v) `baseline_nstar.csv` writes 130.200 for
a source value of 130.151515; (vi) it adds an unauthorised second `n*` reading, correct and disclosed
but not a transcription; (vii) the `H-B6` entry omits the registered label PARTIAL that
`board_stratified_grid.csv` assigns to the pure-proportional cell it reports; (viii) the `n*` entry's
band figures do not carry `(arm, t)` in the sentence that states them.

---

## 4. The consolidation index

**Faithful on the layer the ruling wrote, unfaithful in four rows on the layer it did not.**

All ten §6 permissions and all ten §7 surrenders are present, one row each, in the ruling's own terms
and with their qualifications intact — including the three that are easiest to lose: permission 1's
"with the arm and prompt condition named", permission 3's "conditional on an unregistered prior weight,
and with the bias it buys stated", and permission 6's "explicitly not as evidence that band selection
works". All seventeen dispositions are carried from `baseline_verdict.json` verbatim. The three
silences the closure requires hold: no row in the index claims anything about band selection working,
about depth-partitioned hybrid pooling, or about adaptive selection.

Four rows in the 28-row evidence-ledger layer restate out-of-plan standings more strongly than the
standing the ruling closes them at, and two of them would license a claim the ruling forbids:

1. The row "is the judge's denominator better than a collection constant" reports "no advantage over
   30 topics (16 of 30, Wilcoxon p = 0.839)" **without naming the metric**, and routes it to paper
   sections §4 and §7 where the board's relative-error figures live. Surrender 8 forbids exactly this
   joint reading: that verdict is decided on |log error|, which the pre-registration bars from this
   experiment, and on the registered relative metric the same two procedures read 4.126 against
   0.6304.
2. The row for the model-assisted estimator reads "not preferred — loses to E2 at every sample size".
   The registered rule is a joint one, and on relative RMSE alone `E4` is **below** `E2` at `n` = 10 in
   the source the row cites; what defeats it there is the ±0.05 bias clause. The row states a stronger
   fact than the registration decides.
3. The CLEF census row leads with "APPARATUS VALIDATED (robustness variant)" and is typed as holding,
   where that run's own output verdict is "INCONCLUSIVE — census incomplete", with validation only
   under a declared variant on 4 of 6 topics. The variant is named in parentheses; the standing is
   nonetheless inverted.
4. The open-weight row reports "H-S3 holds across two lineages" with no prompt condition named. The
   standing audit records `H-S3` as conditional — the 40-of-63 floor is met on condition A and failed
   on condition C by `qwen3-1.7b` at 32 — and records that the earlier closure ledger had made this
   same unqualified statement. The defect has been carried forward rather than corrected.

A fifth, weaker case: the `P2` ledger row names κ = 50 for the floor-clearing but does not mark the
clause conditional; the disposition row does, so the index is internally inconsistent rather than
wrong.

---

## 5. Certification

**The hypothesis verification cannot be declared closed.** The declaration sentence is withheld.

Remaining blockers, each with the smallest action that clears it. None requires a run.

1. **`baseline_verdict.json` omits the `R` = 0 exclusion.** Add one key recording that the rule fired
   on no topic and all 30 are retained, transcribed from `baseline_inputs.csv` (minimum `R` = 2).
2. **`baseline_verdict.json` omits the Amendment 3 pool-exhausted cells.** Add one key listing the
   three cells from `baseline_curves.csv` — `CD008760` at `n` = 75 and 100, `CD010860` at `n` = 100 —
   and not from the amendment's prose, which names the wrong topic at `n` = 75.
3. **Forbidden move 2 is live in v26 Appendix B row 3.** Replace "superseded by §6 — on the pool the
   Bayesian arm is preferred and the model-assisted one is not" with the recomputation wording
   `baseline_verdict.json` already contains.
4. **Forbidden move 2 is live in v26 §3.** Delete "Its model-assisted verdict survives the change and
   its Bayesian verdict strengthens" and state instead that the three sampling estimators were
   recomputed under the registered metric and the recomputation disagrees with the prior result.
5. **Forbidden move 4 is live in v26 §6.** Replace "is what **decides** the mechanism half of
   prediction 2" with §1's own wording: an unregistered substitute that does not close the clause.
6. **Forbidden move 5 is live in v26 §7.** Delete the clause "*do not buy expert judgments unless the
   topic's band warrants it* — survives", or restate the recommendation without the band condition.
7. **v26 §1 denies the discharge.** Two sentence edits: `baseline_verdict.json` and
   `baseline_band_sensitivity.csv` now exist; say what they record instead of that they are missing.
8. **Obligation 13's three unrepaired drifts.** Delete "None of the four is decided" from §7 and "The
   four hypotheses are undecided" from §10; make §1's "All four hypotheses" match the five objects it
   enumerates; move §9's seventh bullet above the companion-files line and correct it, since the
   auxiliary variable now exists over the pool.
9. **Obligation 11 is undischarged in the plan.** Name the pool arm and its prompt condition once in
   §4 or §6 of v26, and note that it is a different prompt condition from the arm that fixes the
   bands — the figure caption already carries the sentence that is needed.
10. **Obligation 10 is unrecorded.** One sentence with the verdicts: the per-cell-seeded re-run moved
    the six counted points themselves (2.2609 to 2.2447 at `n` = 10; 0.9909 to 1.0268 at `n` = 50), no
    verdict crosses a threshold and `n*` is unchanged.
11. **Obligation 12 is unrecorded.** One sentence: the board's auxiliary boundary and estimator family
    are inherited from `greg_prereg.py`, which carries no registration-integrity clause and therefore
    no bar on post-hoc revision.
12. **Obligation 14 is unrecorded.** One sentence: store-versus-repository drift could not be
    re-verified because no registration copy is reachable from the granted paths, re-checked at
    closure.
13. **Obligation 15's three items are named nowhere.** Name `phase1_falsification.py`'s SECONDARY,
    `synthjudge_prereg.py`'s G2 and the homeless correlation test in the closure record, each with its
    standing, rather than deferring all three to the audit by reference.
14. **Obligation 9 is half-met.** Put the sentence "every verdict counted is a relative-scaling verdict
    and none has an absolute-scaling counterpart" with the verdicts — in `baseline_verdict.json` or §6
    — rather than only in `board_stratified_en.md` §5.
15. **Two companion documents still carry moves 3 and 4.** In `board_estimators_en.md` §2, mark the
    floor-clearing conditional on prior weight 50 and state that at weight 10 the constant is never
    improved on; in `user_benefit.csv`, correct the "Stop paying where a constant is as good" row,
    which both asserts a clause the closure records as falsified and reports the `P2` mechanism
    probability as measured, and name the arm in the row that gives an over-count factor of 5.1.
16. **Four rows of the consolidation index depart from the standing they are closed at.** Add the
    metric to the |log error| row and remove it from the board sections; soften the model-assisted row
    to the registered joint rule; restore "INCONCLUSIVE — census incomplete" as the CLEF census
    standing; and qualify `H-S3` by prompt condition.

**When those are cleared**, the declaration the project should use is:

> The hypothesis verification of the baseline board is closed with no further measurement: `H-BAND` is
> withdrawn as a registration defect found by audit and is neither supported nor falsified, `H-B6` is
> not supported, `H-B7` and `H-B8` are not attempted with no verdict, the plan's null hypothesis is
> measured against but is not a registered verdict, and the declared predictions close as recorded
> clause by clause in `baseline_verdict.json`, which echoes the threshold each was tested against.

That sentence commits the paper to: advancing no constructive claim for band selection, in either
direction, and reporting the band table as description only at `(haiku_A, t = 0.5)`; saying nothing
whatever about depth-partitioned hybrid pooling or adaptive selection, including that they are
untested in a way that implies a result; reporting the random-sampling comparison as a recomputation
of a prior result rather than as a falsification, with the prior weight named and the bias it buys
stated; leaving `P2`'s registered mechanism clause as not measured unless the hypergeometric
computation on inputs in hand is elected; naming the arm and prompt condition wherever the judge's
labels are described; and carrying the relative-scaling choice, the two unverifiable timing
disclosures and the unreachable repository copy as disclosures rather than as resolved questions.

---

## 6. Scope of this certification

- All fifteen recording obligations and all nine forbidden moves were checked; none was sampled.
- Every transcription claim was recomputed from the file it cites: `n*` and the per-band `n*` on both
  readings, the band counts across all 24 sensitivity rows and the closed form behind them, the
  estimator margin counts (model-assisted 0 of 6; Bayesian κ = 10 at 5 of 6 in-run and 4 of 6 against
  the `baseline_curves.csv` comparator; κ = 50 at 6 of 6), the zero-cost constant 0.6304 and the
  0.6270 and 0.5130 that clear it, the κ = 10 minimum 0.6709, the three allocation counts, the
  pool-wide `se` 0.6419 and `sp` 0.9348, and the over-count factors 4.006 with 29 of 30 (pool arm) and
  5.126 with 28 of 30 (projection basis).
- Two figures quoted in the closure could not be recomputed from the sources named in the brief and
  are carried from the ruling rather than re-verified here: the re-scoring of the stratified counts
  against the anchoring comparator (0, 1 and 1 of 6), which needs `board_stratified.csv`, and the
  35.8 / 92.6 per cent stratum composition.
- One check could not be completed, unchanged: no registration copy is reachable from the granted host
  paths, so store-versus-repository drift remains unverifiable from here.
- A discrepancy worth recording for whoever writes the missing entries: `baseline_points.csv` puts the
  `n` = 100 random subsample at 0.730187 relative and 25.313759 absolute, where `baseline_curves.csv`
  gives 0.7206 and 25.4674. This is the known multiplicity of realisations of the registered
  comparator, not a new defect, and v26 §6 quotes the curves values; the absolute-scaling reversal at
  `n` = 100 holds on either realisation.

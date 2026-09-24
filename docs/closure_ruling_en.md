# Ruling on the admissible closure of the hypothesis verification

Referee ruling on `experiment_plan_en.md` v24 against `baseline_prereg.py` v7, which is
authoritative wherever the two disagree. No experiment was run, no result was computed and no
document was repaired. Registered statements are quoted verbatim. This ruling is about what
closure is admissible, not about what would be interesting to measure next.

---

## 1. Closure is possible with zero further runs

**Ruling: yes.** Every registered object of the live plan has an admissible disposition that
requires no new measurement. The minimum set of runs that closure requires is **empty**.

That is not a statement that nothing more could be measured. It is the statement that for each
registered object there exists a closing form that is true on the evidence in hand, and the price
of taking it is a list of things the paper must surrender — set out in §7 below. The single
consideration that makes the empty set correct is this: **an undecided hypothesis has an honest
closing disposition, and that disposition is not a verdict.** `H-B7` closes as not attempted,
`H-B8` closes as not attempted, `H-BAND` closes as withdrawn. None of those three is a finding,
and none of them can be converted into a finding by any amount of further reasoning over the
curves that exist.

Three distinctions do the work here and must not be collapsed.

**A recording act is not a run.** `baseline_verdict.json`, `baseline_nstar.csv` and
`baseline_board.png` do not exist, and all three are registered or plan-declared outputs. Producing
them consumes no judgments, draws no sample and cannot change a verdict: `n*` = 5 is already
measured, the `H-B6` ratios are already in `board_stratified_grid.csv`, and the thresholds to be
echoed are already fixed in `baseline_prereg.py`. These are §6 obligations, not runs, and closure
is blocked until they are discharged.

**A computation on data in hand is not the same as an unmeasured quantity.** Exactly one registered
clause in the live plan sits in this middle position, and it should be named plainly rather than
buried. `P2`'s registered mechanism clause — "Mechanism: median P(no eligible document in the
sample) = 0.82 at n = 10 and 0.96 in the sparsest band" — has never been recomputed on the pool,
but recomputing it needs no new judgments, no GPU and no labels: it is a hypergeometric quantity in
`N` and `R`, both of which are in `baseline_inputs.csv`, evaluated over the registered 4 / 18 / 8
bands. The project may elect to close that clause as decided at the cost of one CPU-only
computation, or it may close it as **not measured**. Both are admissible. The second is what this
ruling assigns, because closure was elected; the first remains available and is the only place in
the live plan where the choice is real.

**An unrun hypothesis does not inherit its own failure branch.** `Appendix B` of the plan tabulates,
for each of the four registered tests, the consequence "if it fails". For `H-B7` that consequence
reads "the nearest competing proposal is reproduced without advantage", and for band selection "the
selection rule is not advanced as a contribution and the band assignment is reported as
description". The second half of the band-selection row survives a withdrawal; the `H-B7` row does
not survive a non-attempt, because a procedure that was never implemented was not reproduced. The
asymmetry is not a technicality. It is the difference between a null result and a gap, and the
paper's treatment of the nearest competing proposal turns on it.

### Why no run is forced

Each candidate for a forced run, and why it is not one:

| Candidate run | Why it is not required for closure |
|---|---|
| Step 6 — band selection against the best single fixed procedure | It cannot be run as registered at all (§2). A run would not close `H-BAND`; it would produce a verdict on a different hypothesis. A run that cannot close the object is not a minimum requirement for closing it. |
| `H-B7` — depth-partitioned hybrid pooling | The registration sets a threshold for `H-B7` but no not-run branch. Absence of a not-run branch creates no obligation to run: it means the closing disposition is *not attempted, no verdict*, and that every consequence of failure is forfeited along with the verdict. |
| `H-B8` — adaptive selection | The registration explicitly provides the zero-run closure: "If it is not run, baseline_verdict.json records \"NOT ATTEMPTED\" and no claim about it may appear anywhere." |
| `P2` mechanism clause | Closable as *not measured*; optionally elevatable by a computation on existing inputs. Neither is a run. |
| `haiku_A`'s pool-wide `se`/`sp` | Needed by the **new registration** §10 item 2 contemplates, not by closure of this one. The registered band assignment stands at 4 / 18 / 8 for everything already counted; the known-direction bias is a disclosure, not a correction. |
| `baseline_band_sensitivity.csv` | A REQUIRED output whose subject is the `H-BAND` verdict. Withdrawal removes the subject (§6). The descriptive content already exists in `band_boundary_sensitivity.csv`. |

---

## 2. The primary hypothesis

**Registered statement, verbatim** (`baseline_prereg.py` v7, section `H-BAND (the load-bearing
one)`):

> "The selection rule has content: allocating method by relevance-rate band beats the best single
> fixed method applied to every topic."

> "BANDED is constructed by, for each topic, using the method the band assigns; BEST_FIXED is the
> single method with the lowest median RMSE across all topics at that n."

> "SUPPORTED if median RMSE of BANDED <= 0.90 \* median RMSE of BEST_FIXED at >= 4 of 6 grid points."

> "FALSIFIED if BEST_FIXED is <= BANDED at every grid point. On falsification the paper's
> constructive claim reduces to \"nothing beats random sampling\", the band table becomes DESCRIPTIVE
> ONLY, and the selection rule may not be presented as a contribution."

### Ruling: a new registration is NOT admissible as a route to closing this hypothesis. The honest closure is withdrawal as a registration defect found by audit.

Three independent grounds, each sufficient on its own.

**First, the comparator cannot be identified, and restricting it is not a repair.** `BEST_FIXED` is
defined over the board's procedures as "the single method with the lowest median RMSE across all
topics at that n". Two of the nine — `B7` and `B8` — have no value at any `n`. A new registration
that defines `BEST_FIXED` over the seven procedures that do have values is not fixing an ambiguity;
it is choosing the comparator population by reference to which procedures happen to have been run,
after every curve is visible. And the excluded procedure is the one the plan itself identifies as
the most likely occupant of the position: §3 describes `B7` as "the nearest competing proposal" and
says it "is required for the comparison to be against an implemented system rather than a
description". Lowering a bar by removing its most plausible occupant, after seeing the field, is the
defect the anti-search clause exists to prevent. The plan's own §10 item 7 reaches this conclusion
and this ruling concurs with it verbatim: "a restricted run would show the answer before the
comparator exists, and the registered verdict could no longer be claimed."

**Second, the assignment is a free parameter of a directional hypothesis, and the curves are
already visible.** `baseline_prereg.py` protects the tolerance against search on an explicit
rationale — "leaving t open would let H-BAND be satisfied by searching it" — while leaving open a
strictly larger parameter: the map from band to procedure, unregistered in the pre-registration and
unregistered in the plan. Three bands over nine procedures is 729 settings, and every per-band curve
now exists. Whoever fixes the map now chooses the object under test with the answer in view.

There is exactly one assignment that would **not** be a choice made against the curves, and it
should be recorded because it is the only version of this hypothesis that could ever have been
registered honestly. §0 of the plan carries a column titled *What the judge supports*: countable —
"judge labels serve as the denominator"; auxiliary only — "judge reduces the expert sample but
cannot supply the count"; uninformative — "judge contributes nothing to the count". That column is a
map, written before any board curve existed, and its middle entry is not arbitrary: `BAND_AUXILIARY`
= 0.0088 is registered as "a DERIVED crossing of Var(y - p_hat) = Var(y)", which is the condition for
the model-assisted estimator's advantage, so the auxiliary band's procedure is fixed by the boundary's
own derivation. A new registration may fix the map **only** to what that column licenses. Any other
map is search. This matters even though the ruling is withdrawal: it is the reason the defect is a
defect of *registration* rather than of the idea.

**Third, and decisively, that one non-searched map does not test the registered comparison.** Under
it the countable band is assigned the judge-only projection, which spends nothing, so `BANDED` spends
`n` on 26 of 30 topics and 0 on 4. The registered comparison is "at >= 4 of 6 grid points" against a
fixed procedure spending `n` on all 30. A banded procedure that wins partly by spending less is not
tested at equal budget, and the registration nowhere states whether a band assigned a zero-budget
procedure spends nothing or spends `n` on the assigned procedure. This is a **third** undecidability
in `H-BAND`, distinct from the two the standing audit found, and it is not curable by disclosure: it
changes what the hypothesis claims.

Add to these a precondition that has drifted in a known direction. `BAND_ARM = haiku_A`'s `se`/`sp`
were measured on the frozen 2,025-pair panel; the pool run shows that panel's non-eligible stratum
carries twice the pool's false-positive rate (0.1292 against 0.0645), with run-to-run variation on
the same pairs at 0.0025 — composition outweighing noise 26-fold. `pool_results_en.md` §3 states the
consequence: the registered boundary is too high and the countable band as registered too narrow,
with the magnitude for `haiku_A` unmeasured because that arm was never run over the pool. A new
registration written today would inherit a band assignment its own authors have shown to be wrong
in a known direction, and §10 item 2 already rules that correcting it requires `haiku_A`'s pool-wide
rates — a measurement, which closure has elected not to make.

### What withdrawal is, and what it is not

`H-BAND` closes as **WITHDRAWN — undecidable as registered, defect found by audit**. It is
**neither supported nor falsified**, and the distinction carries two consequences the paper must
observe.

The two consequences of the FALSIFIED branch that survive a withdrawal are the ones that concern
standing: the band table becomes description only, and the selection rule may not be presented as a
contribution. The consequence that does **not** survive is the first clause of that branch — "the
paper's constructive claim reduces to \"nothing beats random sampling\"". It fails twice over: the
branch did not fire, and its content is now contradicted by §6, where the Bayesian arm at prior
weight 50 meets the 0.90 margin at 6 of 6 registered budgets. The falsification branch's consequence
sentence may not be transplanted onto the withdrawal.

Conversely, withdrawal is a **stronger** admission than falsification in one respect and must not be
softened into the weaker one. A falsified selection rule is a rule that was tested and did not work.
A withdrawn one was never a determinate object: the paper proposed a rule, registered a threshold
for it, and did not register the rule. That is what the closure says, and it is the finding.

### If the project later elects the new registration

It would be a new registration of a new experiment, not a closure of this one. It must fix, at
minimum: the map from band to procedure, restricted to what §0's *What the judge supports* column
licenses; the candidate population of `BEST_FIXED`, stated exhaustively and including `B7`, which
requires running `B7` first; whether a band assigned a zero-budget procedure spends nothing or
spends `n`, and if the former, that the comparison is no longer at equal budget and the hypothesis
is restated accordingly; and `haiku_A`'s band inputs, estimated on a pool-representative sample. It
must disclose that it was written after every per-band curve existed, and that the plan's §10 item 7
had already ruled a restricted run inadmissible. It may not conclude that the registered `H-BAND` of
this experiment was supported, may not present its verdict as this paper's primary result, and may
not describe a verdict obtained on a comparator population missing `B7` and `B8` as a comparison
against the best single fixed procedure.

---

## 3. Closing disposition of every registered hypothesis and declared prediction

Exact closing words, and whether the disposition needs further measurement. Nothing in this table
requires a run.

### `H-BAND` — band selection (primary)

**WITHDRAWN as a registration defect found by audit.** No map from band to procedure was registered
— not in `baseline_prereg.py` and not in `experiment_plan_en.md` — so `BANDED` was never a
determinate object; `BEST_FIXED` cannot be identified, because two of the nine board procedures have
no median RMSE at any budget; and the registered comparison does not state whether a band assigned a
zero-budget procedure spends nothing or spends `n`. `H-BAND` is therefore **neither supported nor
falsified**. The selection rule is not advanced as a contribution and the band table is reported as
description only, at the registered instantiation `(haiku_A, t = 0.5)` giving 4 / 18 / 8.

*Requires further measurement:* no. *Surrenders:* the paper's primary constructive claim, and with
it any statement that band selection works, does not work, or was tested.

### `H-B6` — stratification (subsidiary)

**NOT SUPPORTED.** "Stratification beats SRSWOR at equal human budget" is scored on "median RMSE of
B6 <= 0.90 \* median RMSE of B3, at the same n. SUPPORTED if that holds at >= 4 of the 6 grid
points." It holds at **1 of 6** under the registered primary allocation (`proportional_min1`),
against the 4 required; at 2 of 6 under pure proportional and 1 of 6 under Neyman on the judge's
label, so the verdict is **not conditional on allocation** within the registered grid. Strata were
the judge's binary decision, never the expert label, and the comparator was computed in the same run.
Re-scoring against the anchoring run's realisation of the same registered comparator moves the counts
to 0, 1 and 1 of 6 — further from support, not nearer.

*Requires further measurement:* no. *Surrenders:* the absolute-scaling counterpart; the graded
four-level strata variant, which the registration excludes; any allocation outside the registered
grid, which Amendment 5 forbids choosing after these values; and any claim that no allocation could
reach the margin — `board_stratified_en.md` §3 corrects its own first statement of this and the
correction must travel.

### `H-B7` — depth-partitioned pooling (subsidiary)

**NOT ATTEMPTED. No verdict.** "Hybrid pooling with a DEPTH split beats SRSWOR at equal human
budget" was not run: the participant runs are not in the workspace and the SIGIR 2026 full text is
unread. The registration provides **no not-run branch** for `H-B7`, so no consequence of its failure
may be reported. Nothing is claimed about depth-partitioned hybrid pooling in either direction, and
the registered fidelity disclosure — "full text unread; reimplementation from summary" — attaches to
the plan's description of the procedure rather than to any result.

*Requires further measurement:* no, to close as not attempted. *Surrenders:* the comparison against
the nearest competing proposal as an implemented system, which §3 states the board requires; any
sentence of the form "the nearest competing proposal is reproduced without advantage"; and the
`Appendix B` failure-consequence row, which may not be reported.

### `H-B8` — adaptive selection (optional subsidiary)

**NOT ATTEMPTED**, recorded as such in `baseline_verdict.json` as the registration requires: "If it
is not run, baseline_verdict.json records \"NOT ATTEMPTED\" and no claim about it may appear
anywhere." No claim about adaptive selection appears anywhere in the paper, including that it is
untested in a way that implies a result.

*Requires further measurement:* no. *Surrenders:* nothing the registration promised — the
registration anticipated exactly this closure. The recording obligation is unmet until the file
exists.

### Null hypothesis (`experiment_plan_en.md` §1 only)

**MEASURED AGAINST; NOT CLOSED AS A REGISTERED VERDICT.** "No procedure attains a lower RMSE than
simple random sampling at equal budget" is improved on as a measurement: the Bayesian estimator at
prior weight 50 attains median relative RMSE at most 0.90 times simple random sampling at **6 of the
6** registered budgets, and at prior weight 10 at 5 of 6 in-run (4 of 6 against the anchoring
comparator). But `baseline_prereg.py` registers no null hypothesis, places "B3 vs B4/B5 - SRSWOR is
preferred at every sample size" under "WHAT THIS FILE DOES NOT REGISTER", and its reporting
obligation 4 states that prior results "are not re-tested and their verdicts are not restated as new
findings". The honest closing form is **a prior result overturned on recomputation under the
registered metric, disclosed as such**, and conditional on a prior weight no registration in the
store fixes.

*Requires further measurement:* no. *Surrenders:* the word *falsifies*, which §6 still uses; the
zero-cost-floor comparison as an equal-budget statement, since `n` = 5 against `n` = 0 is not equal
budget; and the floor-clearing clause as unconditional, since at prior weight 10 the constant is
never improved on (minimum 0.6709).

### Declared prediction `P1`, operative clause — the arm that was run

**FALSIFIED, WITH THE DIRECTION REVERSED.** "countable band predicted to fall from 4 topics to 3 or
fewer" against an open-weight `p*` range of 0.1373 to 0.3361: measured pool-wide the boundary is
**0.0706** — below the predicted interval and below the registered 0.0902 — and the countable band
**widens** from 4 topics to 5, `CD010860` at `p` = 0.0745 crossing in. Reported as a failed
prediction, not deleted, as the registration requires, and the reason is the result: panel
non-eligible false-positive rate 0.1292 against 0.0645 outside the panel, one run and one set of
labels, run-to-run variation 0.0025.

*Requires further measurement:* no. *Surrenders:* nothing beyond what the falsification itself
costs — the prediction's inputs were panel-measured rates, and the same defect is inherited by the
registered band instantiation.

### Declared prediction `P1`, grid-wide clause

**NOT DECIDED.** "empty for 4 of 8 arm-conditions" was never evaluated: only the registered arm was
run over the pool, and the other seven arm-conditions in `predicted_band_shift.csv` still carry
panel-measured rates — the measurement basis this same run showed to be biased.

*Requires further measurement:* no, to close as not decided. *Surrenders:* any grid-wide statement
about open-weight arms and the countable band, including the direction.

### Declared prediction `P2`, clause (a) — model-assisted

**HOLDS.** "GREG met the 0.90 margin at 0/6 budgets": on the pool the model-assisted estimator meets
it at **0 of 6** registered budgets, ratios 0.944 / 0.938 / 0.947 / 0.96 / 0.933 / 0.922. Reported as
a prior result reproduced under the registered metric, never as a new finding.

*Requires further measurement:* no. *Surrenders:* the language of supersession — the plan's "its
model-assisted verdict survives the change" restates a prior verdict and must be reworded.

### Declared prediction `P2`, clause (b) — Bayesian at κ = 10

**HOLDS.** "Bayesian kappa=10 at 4/6": on the pool it meets the margin at **5 of 6** against the
in-run comparator and at **4 of 6** against the anchoring run's realisation of the same registered
procedure — at or above the registered 4 on either realisation.

*Requires further measurement:* no. *Surrenders:* the word *strengthens*, which restates a prior
verdict; the count must be reported with the comparator realisation named, since the two differ.

### Declared prediction `P2`, clause (c) — the zero-cost constant

**FALSIFIED, AND CLOSED AS CONDITIONAL ON AN UNREGISTERED PRIOR WEIGHT.** "the zero-cost constant is
not improved on at any tested budget on the registered scaling": the constant at 0.6304 is improved
on from `n` = 5 by the Bayesian arm at prior weight 50 (0.6270, reaching 0.5130 at a hundred
judgments). At prior weight 10 it is never improved on. No registration in the store fixes the prior
weight, so this clause is closed as **conditional, never as support**, on the same principle
Amendment 5 states for allocation and the `H-BAND` clause states for tolerance.

*Requires further measurement:* no. *Surrenders:* the floor-clearing result as a headline; it may be
reported only with the prior weight named and the bias it buys stated — median relative bias to
0.077 against 0.008 for the random subsample.

### Declared prediction `P2`, registered mechanism clause

**NOT MEASURED.** The registered mechanism is "median P(no eligible document in the sample) = 0.82 at
n = 10 and 0.96 in the sparsest band", and nothing recomputes it on the pool. The judge-derived
against judge-free shrinkage-target comparison reported in its place — crossing at `n` = 30, 20 per
cent better below and 6 per cent worse above — is an **unregistered substitute quantity**, declared as
one, and it does not close this clause.

*Requires further measurement:* no, to close as not measured. *Surrenders:* the mechanism half of
`P2`. Note for the record that this is the one registered clause in the live plan whose registered
form could be moved from *not measured* to *decided* by a computation on inputs already in hand —
a hypergeometric quantity in `N` and `R` over the registered bands, consuming no judgments. If the
project elects that computation, the clause closes as decided; if not, it closes as above, and the
substitute must not be presented as the mechanism resolving.

### `n*` — registered reported quantity

**REPORTED.** `n*` = **5** on both scalings collection-wide, with per-band `n*` of 3 (countable), 5
(auxiliary) and 3 (uninformative), each against the judge-only point within that band; at `n` = 3 the
subsample is still above it, 4.185 against 4.126. Reported with the disclosure that the reference
point is a projection of stratum rates on 29 of 30 topics and a measured census on only 4, and with
the registered fallback string "not reached at n <= 100" unused because a grid point qualifies.

*Requires further measurement:* no. *Surrenders:* nothing, once transcribed into
`baseline_nstar.csv` with every band label carrying `(haiku_A, t = 0.5)`; that file does not exist.

### `Appendix B` row 1 — judge-only against the uninformative estimator

**CARRIED AS PRIOR, ON ITS OWN METRIC ONLY.** Decided on |log error| — 16 of 30 topics, Wilcoxon
`p` = 0.839 — and `baseline_prereg.py` states "|log error| is NOT used in this experiment. Reporting
any registered verdict below on a different error metric voids that verdict." On the board's
registered relative metric the same two procedures read 4.126 against 0.6304, a factor of 6.5, and
that comparison is **untested**. The prior tie and the board figures may not be read together, and
the prior verdict may not be restated as a board finding.

*Requires further measurement:* no. *Surrenders:* any joint reading of §0's "Established" row with
§6's figures.

### `Appendix B` row 2 — the exhaustive judge census

**CARRIED AS PRIOR.** Identity exact over 54 rows at 1e-6; variance eliminated, bias unchanged. On
this board the judge census is an apparatus check on the 4 topics small enough to be censused — the
small dense ones — and licenses no collection-wide statement.

*Requires further measurement:* no. *Surrenders:* any collection-wide census claim.

### `Appendix B` row 3 — random sampling against the two model-assisted estimators

**CARRIED AS PRIOR AND NOT RE-TESTED.** The row as it currently stands in v24 — "**superseded by
§6** — on the pool the Bayesian arm is preferred and the model-assisted one is not" — is
**inadmissible**: reporting obligation 4 forbids restating a prior verdict as a new finding, and the
docstring places this exact comparison under what the file does not register. The admissible form is
that the three sampling estimators were **recomputed** under the registered metric, as the same file
mandates ("The three sampling estimators are therefore RECOMPUTED here"), and that the recomputation
disagrees with the prior result — reported as a recomputation, not as a supersession or a new verdict.

*Requires further measurement:* no. *Surrenders:* the words *superseded*, *survives* and
*strengthens* wherever they attach to a prior-result verdict.

### §0 "Established" table — six carried findings

**CARRIED AS SETTING, NOT AS VERDICTS OF THIS EXPERIMENT.** Each row must name the metric and the
collection it was decided on. Row 2, "The judge does not clear an uninformative estimator", is
decided on |log error| and may not be quoted beside §6's relative-error figures. Rows 3 to 6
(absolute recall, the stopping-rule guarantee, field ordering, the single best system) are decided
under their own registrations at the standing recorded in `hypothesis_standing_audit.md` and are
unchanged by this closure.

*Requires further measurement:* no. *Surrenders:* nothing, provided each row travels with its metric.

### Out-of-plan registrations (scope statement)

**CLOSED AT THE STANDING RECORDED IN `hypothesis_standing_audit.md`.** The thirteen registrations
outside the live board are not objects of this closure and this ruling changes none of their
standings. Two carriages into the live board must be disclosed: `BAND_AUXILIARY` = 0.0088 is
inherited from `greg_prereg.py`'s secondary analysis (crossing prevalence 0.008837), and
`board_estimators.py`'s estimator definitions are transcribed from the lineage of `greg_faithful.csv`
— a file the plan describes as "superseded and not carried". Transcription is the conservative choice
and the expansion-estimator agreement check supports it, but the plan cannot both not carry that file
and take its estimator definitions from it without saying so.

*Requires further measurement:* no. *Surrenders:* nothing, given the disclosure.

---

## 4. What must not be done in closing

Nine moves would make the closure unsound. Each is named with the place in the current documents
where it is already a live temptation.

**1. Retrofitting the band-to-procedure map and calling it an amendment.** Fixing the assignment now,
with every per-band curve visible, under the authority of the file's own amendment practice.
*Live at:* `experiment_plan_en.md` §1, which states "the band assignment under test is **fixed to the
registered instantiation, `(haiku_A, t = 0.5)`**" — true of the arm and tolerance and false of the
assignment, so the sentence reads as if the map were registered; and §10 item 7, "It is technically
possible today". The precedent that would be used is `baseline_prereg.py`'s unnumbered `AMENDED`
block, which created `BAND_ARM` and `BAND_TOLERANCE` and is the one amendment in the file carrying no
timing disclosure, while its own rule governs exactly those constants.

**2. Restating an unregistered comparison as a verdict.** *Live at:* §6, "it falsifies the null
hypothesis of §1" — the word survives in §6 although §1 now carries the three qualifications that
retract it; `Appendix B` row 3's "**superseded by §6**"; and §3's "Its model-assisted verdict survives
the change and its Bayesian verdict strengthens". All three restate a comparison
`baseline_prereg.py` positively declines to register.

**3. Reporting a conditional as support.** *Live at:* §6 result 3 and §7's null paragraph, where the
zero-cost-floor clearing is stated without the prior weight that alone produces it;
`board_estimators_en.md` §2, "the first board row to answer the question the plan says a practitioner
actually asks"; and `user_benefit.csv` row "Spend five judgments instead of judging the pool", which
carries the result with no weight qualification at all.

**4. Closing a hypothesis on a substituted quantity.** *Live at:* `user_benefit.csv` row "Stop paying
where a constant is as good", whose *satisfied by the anchoring run* column reads "Measured on the
registered scaling with its mechanism: ... explained by a median probability 0.82 of catching no
eligible document at n = 10". Those figures are the pseudo-population values quoted in `P2`'s own
registration text; nothing recomputed them on the pool, so the practitioner-facing deliverable
asserts as measured a quantity that was never measured. Also §6, "A judge-free variant of the
Bayesian arm ... is what **decides** the mechanism half of prediction 2", which §1 now correctly
labels an unregistered substitute while §6 still says *decides*.

**5. Transplanting a failure branch's consequence onto an unrun or withdrawn hypothesis.** *Live at:*
`Appendix B`'s "If it fails" column for depth-partitioned pooling and for band selection; and §7's
"The sharper recommendation §7 anticipated — *do not buy expert judgments unless the topic's band
warrants it* — survives", which is a band-selection recommendation surviving on evidence that never
tested band selection.

**6. Closing `H-B7` as a null result.** Writing that depth-partitioned hybrid pooling does not beat
random sampling, or that the nearest competing proposal was reproduced without advantage. *Live at:*
`Appendix B` and §3's "required for the comparison to be against an implemented system rather than a
description" — the temptation being to keep the sentence's credit while the procedure has no curve.
The related letter-of-the-rule trap: `baseline_rejected_runs.csv` with zero rows plus zero runs read
would be exactly the state `baseline_prereg.py` calls "an ERROR, not a pass".

**7. Repopulating `BEST_FIXED` with only the procedures that have curves.** *Live at:*
`board_estimators_en.md` §5, "the primary comparison still cannot be run until the depth-partitioned
and adaptive procedures have curves" — the temptation is to drop that sentence at closure, since it
is the only place the restriction is named; and §10 item 7, whose own reasoning would have to be
overridden.

**8. Reading the pool run's band shift as a correction to the registered bands.** *Live at:* §7,
"the registered boundary is likely too high and the countable band as registered too narrow", stated
more assertively than `pool_results_en.md` §5's own disclosure that this "follows from the mechanism,
not from a measurement of that arm". No topic may be re-banded, and 4 / 18 / 8 stands for everything
already counted; the measured 0.0706 boundary belongs to `qwen3-8b` condition C, not to `haiku_A`.

**9. Switching metric or scaling to rescue a comparison.** *Live at:* §6 result 2, where the absolute
scaling reverses the board's headline at `n` = 100 (25.5 against 26.0), and `user_benefit.csv`'s
*still short* column, which records it. Relative is primary under Amendment 2 and absolute "is
reported alongside and never substituted"; |log error| is forbidden outright. Every verdict counted
is a relative-scaling verdict with no absolute-scaling counterpart, and `board_stratified_en.md` §5
is currently the only place that says so.

---

## 5. Recording obligations to be discharged before closure

Registered outputs that do not exist, mandated entries with no home, and disclosures that must travel.
None of these is a run.

1. **`baseline_verdict.json` does not exist**, and reporting obligation 1 — "Every verdict echoes the
   threshold it was tested against into baseline_verdict.json" — is therefore unmet for **every**
   verdict counted so far. It must be created and must carry, at minimum: `H-B6` NOT SUPPORTED with
   `HB6_RATIO` = 0.90 and `HB6_MIN_GRIDPOINTS` = 4 echoed and all three allocation counts;
   `H-B7` NOT ATTEMPTED; `H-B8` **NOT ATTEMPTED**, which is a registration mandate currently with
   nowhere to live; `H-BAND` WITHDRAWN with the three grounds; the `R` = 0 topic exclusion, which
   `EXCLUDE_IF_R_ZERO` requires be "written to baseline_verdict.json"; the Amendment 3
   pool-exhausted cells; and the `P1` and `P2` clause verdicts with their registered wordings.
2. **`baseline_nstar.csv` does not exist.** `n*` = 5 and the per-band 3 / 5 / 3 are already measured;
   transcription only, with every band label carrying `(haiku_A, t = 0.5)` per reporting obligation 5.
3. **`baseline_band_sensitivity.csv` does not exist**, and it is registered as "a REQUIRED output,
   not an optional check". *Ruling:* its registered subject is the `H-BAND` verdict recomputed over
   the arm × tolerance grid. Withdrawal removes the subject, so the obligation is discharged by
   recording the withdrawal in `baseline_verdict.json` and by citing the descriptive sensitivity that
   already exists — `band_boundary_sensitivity.csv`, `p*` spanning 0.0189 to 0.1565 and the countable
   count 2 to 16 of 30 — wherever the 4 / 18 / 8 split appears. It may **not** be discharged by
   producing a grid of a verdict computed on a repopulated comparator.
4. **`baseline_rejected_runs.csv` does not exist.** Its subject is the `H-B7` loader guard. Discharge
   by recording *stage not attempted* — explicitly **not** by an empty file, which together with zero
   runs read is the state the registration defines as an error rather than a pass.
5. **`baseline_board.png` does not exist**, a §8 declared output. Produce it or record its absence.
6. **Reporting obligation 3 is live on the band table:** "A method's absence from a band is reported
   as \"not assessed\", never as a loss." With `B7` and `B8` having no curve, every band entry for
   them reads *not assessed*.
7. **Amendment 5's priority claim cannot be corroborated by the store.** The pre-registration version
   carrying it and the first `H-B6` values were saved in one call at the same millisecond, so the
   claim rests on author disclosure alone. Disclose at closure. The verdict is unaffected — it is NOT
   SUPPORTED under all three allocations and under both comparator realisations.
8. **The unnumbered `AMENDED` block in `baseline_prereg.py` carries no timing disclosure** while it
   created the constants its own new-registration rule governs. Record its timing relative to the
   first RMSE, or record that the timing cannot be evidenced from the store.
9. **Amendment 2(a)'s scaling choice is inherited by every verdict** and "this choice was made after
   seeing that the two disagree". It is conservative for the board's claims, and the disclosure must
   sit with the verdicts rather than only in `board_stratified_en.md` §5.
10. **Amendment 2(b)'s stated rationale overclaims and should be corrected at closure.** "the added
    points cannot change a verdict" is true of which points are counted and false of their values:
    the per-cell-seeded re-run moved the six original points themselves, 2.2609 to 2.2447 at `n` = 10
    and 0.9909 to 1.0268 at `n` = 50. No verdict crosses a threshold and `n*` is unaffected.
11. **Every board statement about "the judge" must name the arm and the prompt condition.** The board
    mixes three: `JUDGE_LABELS` registers `gpt-4o-mini_A`; the band assignment uses `haiku_A`
    condition A panel rates; the pool run, and therefore the auxiliary variable and the strata, is
    `qwen3-8b` **condition C**. `FULL_POOL_JUDGE` registered neither arm nor condition, so both were
    free when the run was chosen.
12. **Registration-integrity clause propagation.** Six of the fourteen registrations carry no
    integrity clause — `census_prereg.py`, `stoprule_prereg.py`, `synthjudge_prereg.py`,
    `bpref_prereg.py`, `greg_prereg.py`, `clefcensus_prereg.py`. Two of those feed the live board:
    `greg_prereg.py` supplies `BAND_AUXILIARY` and the estimator family. Propagate a clause, or record
    that the board's auxiliary boundary and estimator definitions are inherited from a registration
    with no bar on post-hoc revision.
13. **Canonical-home drift in `experiment_plan_en.md` v24, reported not repaired.** Two paragraphs are
    duplicated verbatim — the §1 "Undecidable as registered, and not for the reason this section
    guards against" block, and the `P2` "The registered mechanism clause is that probability" block.
    §7 still opens "**None of the four is decided.**" two paragraphs before reporting stratification
    as not supported. §1 says "All four hypotheses" of a list that enumerates five objects. §9 is
    titled "The seven risks that matter" and its seventh bullet falls after the companion-files line.
14. **Store-versus-repository drift is unverified at closure.** `prereg_audit.csv` compares each
    registration's store copy against a repository copy and records one difference in
    `panel_prereg.py` (an r-string prefix, one byte, no rule or threshold text affected); that
    repository is not reachable from the granted paths, so neither that difference nor any new drift
    could be re-verified in this session or the last.
15. **Two registered reporting obligations outside the live plan remain unmet** and should be recorded
    with the closure rather than left open: `phase1_falsification.py`'s SECONDARY, registered with
    "reported either way" and reported in no stored output; and `synthjudge_prereg.py`'s guard G2,
    whose inputs exist but whose tracking check against the closed form is stated nowhere. A third
    item has no canonical home at all: the correlation test `synthjudge_results_ko.md` §5 withdraws as
    "a test that cannot fail" appears in no registration file in the store.

---

## 6. What the paper may claim

1. The size of the denominator error a language-model judge produces on this collection, as a
   description, with the arm and prompt condition named: median relative error 4.126 for the
   judge-only projection, and pool-wide over-counting by a median factor of 4.006 with 29 of 30
   topics over-counting.
2. That stratifying on the judge's binary decision does **not** beat simple random sampling at equal
   expert budget on the registered metric — 1 of 6 registered budgets under the registered primary
   allocation, 2 of 6 and 1 of 6 under the two registered secondaries — with the comparator computed
   in the same run, and with stratum composition explaining the magnitude of the typical gain
   (35.8 per cent of eligible documents remain in the stratum holding 92.6 per cent of the pool) but
   not establishing a ceiling.
3. That the **same** judge labels on the **same** pool do beat random sampling when used as a
   shrinkage target rather than as a partition — reported as a recomputation of a prior result under
   the registered metric, conditional on an unregistered prior weight, and with the bias it buys
   stated. This contrast, two registered procedures on one auxiliary variable with opposite verdicts,
   is the sharpest statement the board produced about what a judge's labels are for.
4. That the model-assisted estimator meets the 0.90 margin at 0 of 6 registered budgets on the pool
   as it did on the pseudo-population — labelled as a prior result reproduced, not as a new finding.
5. `n*` = 5 on both scalings, per band 3 / 5 / 3, against a judge-only reference point that is a
   projection on 29 of 30 topics.
6. That the relevance-rate bands separate by roughly an order of magnitude at equal budget — 0.674
   against 5.207 at `n` = 10, 0.196 against 1.533 at `n` = 100 — as a descriptive property of this
   collection and this judge configuration, and **explicitly not** as evidence that band selection
   works.
7. The price of a usable denominator: a median 613 expert judgments for ±50 per cent, only 11 of 30
   topics reaching 0.50 relative error within `n` = 100 at a median budget of 75, and an estimate
   still off by about 298 per cent at `n` = 5 — so reaching the judge's reference point is not the
   same as producing a usable estimate.
8. `P1` falsified with its direction reversed for the arm that was run, and the mechanism behind the
   failure: a stratified panel's non-eligible stratum carries twice the pool's false-positive rate,
   26 times the run-to-run variation on the same pairs.
9. The transferable methodological finding: a scaling convention left unstated in a pre-registration
   reversed the ordering of a zero-cost procedure and a hundred expert judgments, and the choice had
   to be made after the disagreement was visible. This holds independently of how any of the four
   hypotheses resolved.
10. That the paper's own pre-flight gate has a measurably fallible third input — a conveniently drawn
    sample understates specificity by enough to move a topic between bands — with the direction known
    and the magnitude for `haiku_A` unmeasured.

## 7. What the paper must surrender

1. **The primary constructive claim.** Band selection is not advanced as a contribution and the band
   table is description only — surrendered as **withdrawn and never tested**, not as falsified, and
   without the falsification branch's consequence sentence.
2. **Everything about depth-partitioned hybrid pooling**, including that it lacks advantage, that it
   was reproduced, and that the board compares against an implemented competing system.
3. **Everything about adaptive selection** — "no claim about it may appear anywhere."
4. **The word *falsifies* for the null hypothesis**, the zero-cost comparison as an equal-budget
   statement, and the floor-clearing clause as unconditional support.
5. **`P1`'s grid-wide clause** — no statement about the countable band across the eight
   arm-conditions, in either direction.
6. **`P2`'s registered mechanism clause**, unless the project elects the computation named in §3; the
   judge-free-prior comparison is an unregistered substitute and may not stand in for it.
7. **Any unqualified sentence of the form "the judge's labels do X."** Three arms and two prompt
   conditions are in one board and the registration names one.
8. **Any absolute-scaling ordering claim**, and any joint reading of the |log error| prior result with
   board figures.
9. **Any collection-wide census statement** — the census comparison covers 4 topics, and those are
   the small dense ones.
10. **Any cross-collection generalisation**, and any claim that questions the expert qrels the board
    takes as truth while relying on them as truth.

---

## 8. Scope of this ruling

- The registered objects of the live plan were taken to be `H-BAND`, `H-B6`, `H-B7`, `H-B8`, the plan's
  null hypothesis, and declared predictions `P1` and `P2` — decomposed into the clauses the
  registrations themselves separate, giving sixteen dispositions including the carried prior results
  and `n*`. The thirteen registrations outside the live board are closed at the standing recorded in
  `hypothesis_standing_audit.md`; this ruling changes none of them and adds only the two carriage
  disclosures in §3.
- Every verdict quoted was read from that run's own stored output or from the authoritative
  pre-registration, not from the plan's restatement of it. No quantity was computed in this session
  and no document was repaired.
- The absence of the five registered outputs named in §5 was verified against the artifact store in
  this session: `baseline_verdict.json`, `baseline_nstar.csv`, `baseline_band_sensitivity.csv`,
  `baseline_rejected_runs.csv` and `baseline_board.png` are absent.
- One check could not be completed, unchanged from the standing audit: the repository copy that
  `prereg_audit.csv` compares against is not reachable from the granted host paths, so
  store-versus-repository drift could not be re-verified.

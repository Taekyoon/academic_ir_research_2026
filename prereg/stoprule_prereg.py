"""PRE-REGISTERED, written before any of these three quantities was computed.

Three measurements, all LLM-free, all on materials already in hand: the 27 public CLEF eHealth
TAR 2017 participant runs, the abstract-level expert qrels, and the judge error rates already
measured on the frozen panel.

--------------------------------------------------------------------------------------------
E1  THE STOPPING RULE, ON REAL EXAMINATION ORDERS

Why. The project currently reports "a recall-target stopping rule cannot fire on 28 of 30
topics". That number is a DEDUCTION: it is R/R-hat >= target, computed from two numbers, with no
examination order, no run, and no rule implementation in it. An auditor-grade reader is entitled
to say it is arithmetic dressed in TAR vocabulary. E1 replaces it with a measurement on the
axes TAR itself uses - reliability against cost.

Design. A participant run's ranking IS the reading order: a screener works down it. At depth k
the screener has found rels_found(k) relevant documents and believes recall is
rels_found(k) / R_denominator. The target-recall rule stops at the first k where that belief
reaches TARGET. Two conditions over the same 27 runs and 30 topics:

    CONTROL     R_denominator = the true expert count R  (what an oracle would use)
    TREATMENT   R_denominator = R-hat = R*se + (N-R)*(1-sp), the judge's projected count

At the stopping depth we record the two quantities the TAR contract is written in:
    reliability = TRUE recall actually achieved there  (rels_found(k) / R)
    cost        = k, documents examined
plus whether the rule fired at all within the run's own depth.

WHICH RULE, and why not the published ones. We implement the canonical TARGET-RECALL rule -
stop when estimated recall reaches the target - and NOT Cormack & Grossman's CAL heuristics,
Yang's Quant/QuantCI, Stevenson's point-process methods, Boetje's SAFE or Fletcher & Stevenson's
EVPI rule. Those are refinements of HOW to locate the stopping point efficiently; the
target-recall rule is the CONTRACT itself, and its only input is the denominator. Implementing
five published rules from prose, without their sampling machinery, would risk misrepresenting
them - worse than not running them. This is a scope limit, declared here, not a claim that the
refinements would behave the same way. What E1 can say is whether the contract is honourable
when the denominator comes from a judge.

Registered outcome. Report the paired difference in reliability at the stop, over run-topic
pairs where BOTH conditions fire.
    median(reliability_control - reliability_treatment) >= 0.10  -> "CONTRACT BROKEN": the judge
        denominator makes screeners stop materially short of the recall they believe they have.
    <= 0.02  -> "CONTRACT SURVIVES": the deduction overstated the operational damage and the
        28/30 sentence must be softened or dropped from the abstract.
    in between -> "PARTIAL", reported as such, no promotion.
Also reported, not part of the rule: the fire rate in each condition, and the cost difference.

--------------------------------------------------------------------------------------------
E2  wss_95 UNDER A JUDGE DENOMINATOR

Why. object_changed_ko.md argues that wss_95 depends on R because it must locate the rank at
which 95% recall is reached. That is an argument from the metric's definition; it has never been
computed. E2 computes it, so the claim stops being a deduction.

Design. wss@r = 1 - (rank at which recall r is reached) / N, per the campaign's own results
files. Recompute for all 27 runs under both denominators and compare the run RANKINGS by
Kendall tau, the same statistic already reported for recall and NCG.

Registered outcome. tau(wss_95 under R, wss_95 under R-hat) is reported beside the existing
recall tau of 0.649. No threshold: this is a descriptive addition closing a stated gap.

--------------------------------------------------------------------------------------------
E3  DOES DEPTH GET REWARDED

Why. pipeline_overview.png and judge_role_ko.md both state that a judge denominator rewards
depth, because a run earns credit at weight (1-sp) for every non-relevant document it retrieves.
The mechanism is written in judge_consequence.py's own comment, and the direction matches the
measurements, but the correlation between a run's depth and its rank movement has never been
computed - it is flagged "미확인" in the figure.

Design. For each of the 27 runs, depth = total documents returned over the 30 topics, and
rank_change = rank under the judge denominator minus rank under the true denominator (positive =
looks better under the judge). Spearman correlation between the two.

Registered outcome. rho > 0 with p < 0.05 confirms the stated mechanism; otherwise the "depth is
rewarded" sentence must be removed from the figure and the note, since it would then be an
unsupported mechanism claim.

--------------------------------------------------------------------------------------------
DISCLOSED FOR ALL THREE
  - The judge rates are the 30-topic POOLED se/sp from the opus_C row of
    opus_results_paired_fixedweights.csv (se 0.6202, sp 0.9686), applied to each topic's own
    N and R. They are not per-topic measured rates; per-topic specificity pins at 1.000 in 14 of
    30 topics on a 40-document non-eligible stratum, which is why pooled rates are used.
  - Rules operate on each run's OWN returned list. A run that truncates cannot fire beyond its
    own depth, and that is treated as "did not fire", not as missing data.
  - Only abstract-level qrels are used. The content level exists and gives a denominator roughly
    three times smaller; mixing the two would be a basis error.
"""

TARGET_RECALL = 0.95
D_CONTRACT_BROKEN = 0.10
D_CONTRACT_SURVIVES = 0.02
WSS_TARGET = 0.95
ARM = "opus_C"
E3_ALPHA = 0.05

"""PRE-REGISTERED design for CONDITION C. Fixed BEFORE any condition C label exists.

QUESTION. The 63 hard-core documents - called eligible by all four lineages and non-eligible by
the expert - are 41.3% reviews and meta-analyses against 11.1% of ordinary non-eligible documents
and 1.7% of genuinely eligible ones. That raises a COMPETING EXPLANATION for the whole project:
the judge may not be miscalibrated at all, it may simply never have been given the study-design
exclusion rule, which lives in the review protocol and not in the condition A prompt.

Condition C puts that rule in the prompt and measures what it fixes.

DESIGN. Within-judge paired comparison. Same judge (claude-haiku-4-5-20251001, the lowest
false-positive judge of the four at 0.0842, so the hardest case for a filter to improve),
same frozen 2,025-pair panel, same decoding, same strict parsing. The ONLY difference is that
the prompt's {criteria_block} placeholder, empty in condition A, now carries a domain-generic
statement of the diagnostic-test-accuracy design rule (crit_block_C.txt). It is IDENTICAL for
all 30 topics - no topic-specific information is added, so this tests the design filter and not
extra topical hints. Verified programmatically that condition C's prompt differs from condition
A's by exactly that insertion.

WHY THE JUDGE CHOICE IS CONSERVATIVE AND WHAT THAT COSTS. Haiku has the least room to improve,
so a null result here is weaker evidence than a null on a permissive judge would be. Declared
in advance: if condition C shows little effect, the honest reading is "little effect on the
best judge", and the OpenAI-family replication is required before generalising. That
replication is blocked today - the key's daily quota resets in about 31 hours.
"""

BASELINE_A = dict(fp=0.0842, se=0.6445, bias_median=0.2650, within_50pct=11, n_topics=30)
ORACLE     = dict(fp=0.0588, bias_median=0.0350, within_50pct=13)
# ORACLE = perfect exclusion of every PubMed Review/Meta-Analysis label. A prompt-based filter
# cannot see those labels, so ORACLE is the CEILING condition C is measured against.

PRIMARY = dict(
    quantity="topics whose reconstructed denominator lands within +/-50% of the expert count",
    baseline=11, oracle_ceiling=13, n_topics=30,
)

# --- The condition that would demote this project's own framing -----------------------------
DOMINANCE_IF = ("condition C puts >= 20 of 30 topics within +/-50%. Then prompt "
                "underspecification, not prevalence, is the dominant explanation; the "
                "prevalence framing is demoted to secondary and the claim is rewritten. "
                "This is reported as-is, with no reframing.")
PREVALENCE_SURVIVES_IF = ("condition C puts <= 15 of 30 topics within +/-50%. Then the "
                          "design filter is a real but partial effect and prevalence remains "
                          "the primary account.")
AMBIGUOUS_IF = ("16 to 19 of 30. Reported as ambiguous. Neither account is promoted or "
                "demoted on this evidence.")

# --- Guards, declared so a gain cannot be claimed that is really a trade --------------------
SENSITIVITY_GUARD = ("if sensitivity falls below 0.50 (from 0.6445), the filter is also cutting "
                     "genuinely eligible studies and any false-positive gain must be reported "
                     "as a TRADE, not an improvement")
CEILING_GUARD = ("if condition C's false-positive rate beats the oracle's 0.0588, that cannot "
                 "be the design filter working better than perfect label-based exclusion - it "
                 "means the prompt is also excluding eligible studies. Check sensitivity before "
                 "interpreting.")
ALSO_REPORT = [
    "false-positive rate and sensitivity, A vs C, on the identical pairs",
    "per-topic denominator bias: median, |median|, and the full distribution",
    "how many of the 63 hard-core documents condition C reclassifies below the >=2 threshold",
    "STRICT parse rate (the harness failure mode of this project), reported not rescued",
    "whether the improvement concentrates in the sparse topics or the dense ones - if the "
    "filter only helps where p is already high, it does not address the claim at all",
]
BINARISE_AT = 2
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1000   # measured necessary in condition A: replies run 320-645 output tokens

if __name__ == "__main__":
    import json
    print(json.dumps(dict(PRIMARY=PRIMARY, DOMINANCE_IF=DOMINANCE_IF,
                          PREVALENCE_SURVIVES_IF=PREVALENCE_SURVIVES_IF,
                          AMBIGUOUS_IF=AMBIGUOUS_IF, BASELINE_A=BASELINE_A,
                          ORACLE=ORACLE, SENSITIVITY_GUARD=SENSITIVITY_GUARD), indent=1))


# ============================================================================================
# AMENDMENT 1 - added BEFORE any condition C label and before any Sonnet label of either
# condition existed. Reason for amending rather than starting a new registration: the user asked
# that the capability grade be examined alongside condition C, and the scoped claim's limitation
# #4 is exactly that capability grade and pretraining lineage are entangled because the panel ran
# one model per lineage.
#
# DESIGN BECOMES 2x2, all four cells on the IDENTICAL frozen 2,025-pair panel:
#
#                     condition A (title only)      condition C (+ design criteria)
#   Haiku 4.5         ALREADY MEASURED               to be run
#   Sonnet 4.5        to be run                      to be run
#
# Sonnet 4.5 (claude-sonnet-4-5-20250929) is chosen over Sonnet 5 deliberately: it is the SAME
# GENERATION as claude-haiku-4-5-20251001, so the contrast isolates capability grade within one
# lineage and one generation. Sonnet 5 would confound generation with capability.
#
# EXECUTION. Six frames, one per existing 338-row slice, each running all THREE new arms on its
# own slice. Every arm therefore shares its frame's conditions, so a per-frame anomaly cannot be
# mistaken for an arm effect. Measured cost from a 16-row pilot: 1,091 tokens/row for condition A
# and 1,179 for condition C, so three arms x 338 rows is about 1.2M tokens per frame against the
# 2.0M ceiling. The pilot also showed 2/16 and 1/16 transient API errors, so retries are required
# and the per-arm completion count must be reported, not assumed.
#
# NEW REGISTERED QUESTIONS, with thresholds fixed here:
#
# H-CAP  Does upgrading capability grade substitute for supplying the criteria?
#        Compare Sonnet-A against Haiku-C on the primary quantity (topics within +/-50%).
#        If Sonnet-A >= Haiku-C, capability substitutes for specification, and the paper must
#        say the fault is the judge's capability rather than the prompt's content.
#        If Haiku-C > Sonnet-A, specification matters more than capability grade.
#
# H-INT  Is there an interaction? Registered prediction, made before seeing any label: the
#        criteria block helps the WEAKER judge more, because Haiku-A's false-positive rate
#        (0.0842) leaves more room than Sonnet-A's is likely to. Stated so that the opposite
#        result - criteria helping the stronger judge more - is recorded as a surprise rather
#        than absorbed.
#
# H-CEIL The oracle ceiling (fp 0.0588, 13/30 topics) applies to EVERY cell of the 2x2. No cell
#        may be read as beating perfect label-based exclusion without first checking sensitivity
#        against the SENSITIVITY_GUARD below.
#
# The DOMINANCE / PREVALENCE_SURVIVES / AMBIGUOUS thresholds above are evaluated on the BEST
# cell of the 2x2, not on Haiku-C alone. If the best cell reaches >= 20/30 the prevalence
# framing is demoted regardless of which cell achieved it.
#
# UNCHANGED: binarisation at >=2, strict "##final score" parsing only, no loose fallback, the
# frozen panel, and the reporting obligations in ALSO_REPORT.

SONNET = "claude-sonnet-4-5-20250929"
CELLS = ["haiku-A (already measured)", "haiku-C", "sonnet-A", "sonnet-C"]
H_CAP  = "Sonnet-A >= Haiku-C on topics within +/-50% => capability substitutes for specification"
H_INT  = "registered prediction: the criteria block helps the WEAKER judge more"
EVALUATE_THRESHOLDS_ON = "the best cell of the 2x2, not Haiku-C alone"


# ============================================================================================
# AMENDMENT 2 - written BEFORE any Opus label of either condition existed. Pilot data that DID
# exist at writing time: 16 rows per condition, strict parse 32/32, output median 9 tokens, zero
# refusals, input-dominated cost ~4,170 (A) / ~4,265 (C) tokens per row. No label from the full
# panel had been produced.
#
# Reason for amending: scaling_threat_ko.md extrapolates a SINGLE measured capability step
# (Haiku 4.5 -> Sonnet 4.5) and its whole projection rests on that step's ratios holding. A third
# grade turns a 1-point extrapolation into a 2-point trend and can distinguish geometric from
# saturating. The design becomes 2x3, all cells on the IDENTICAL frozen 2,025-pair panel:
#
#                      condition A (title only)   condition C (+ design criteria)
#   Haiku 4.5          MEASURED  fp .0851 se .6412  MEASURED  fp .0466 se .6017
#   Sonnet 4.5         MEASURED  fp .0529 se .6153  MEASURED  fp .0278 se .5573
#   Opus 4.5           this amendment              this amendment
#
# Grade choice: claude-opus-4-5-20251101 is the SAME 4.5 generation as the other two, so the axis
# stays capability and does not confound generation. Opus 5 was available and deliberately NOT
# used for that reason.
# Basis note: the 2x2 numbers above are on the 1,927-pair four-arm intersection. Adding two arms
# changes that intersection, so ALL comparisons must be recomputed on the new common row set and
# the paired table reported alongside per-arm coverage. Values from the old basis must not be
# carried into the new tables.

FP_STEP_OBSERVED = 0.621     # fp(Sonnet_A) / fp(Haiku_A)
SE_STEP_OBSERVED = 0.9596    # se(Sonnet_A) / se(Haiku_A)

# --- H-SAT: is the capability axis geometric or saturating? -----------------------------------
# r = fp(Opus_A) / fp(Sonnet_A), compared against the previous step's 0.621.
H_SAT = {
 "geometric_confirmed_if": "r <= 0.70  -> the projection in scaling_threat_ko.md stands as an "
                           "exposure estimate; the capability threat is real at the stated rate",
 "saturating_if":          "r >= 0.85  -> the axis is flattening, the projection OVERSTATES the "
                           "threat, and the claim is more robust to scaling than reported",
 "ambiguous_if":           "0.70 < r < 0.85 -> report the two-point trend and draw no conclusion "
                           "about the functional form",
}

# --- H-SE: is the specificity-for-sensitivity trade intrinsic to capability? ------------------
# This one can go AGAINST the current writeup and must be reported either way.
H_SE = {
 "trade_continues_if": "se(Opus_A) < se(Sonnet_A) -> the joint projection's turnover at se=0.5 "
                       "stands, and the sensitivity wall remains the load-bearing argument",
 "trade_not_intrinsic_if": "se(Opus_A) >= se(Sonnet_A) -> the trade was NOT a property of "
                           "capability. The optimistic curve becomes the right one, the turnover "
                           "argument is withdrawn, and the scaling threat is LARGER than reported. "
                           "Report this as a weakening of our own position, not as noise.",
}

# --- H-CAP3: does capability keep substituting for specification? ----------------------------
H_CAP3 = ("compare within(Opus_A) against within(Haiku_C) and within(Sonnet_C) on the NEW paired "
          "basis; capability continues to substitute only if Opus_A >= the better of the two")

# --- H-INT3: does the criteria block still reverse sign at the top grade? --------------------
H_INT3 = ("registered prediction, from the Haiku +3 / Sonnet -2 pattern: the criteria block costs "
          "Opus MORE than it cost Sonnet, i.e. within(Opus_C) - within(Opus_A) <= -2. If instead "
          "it helps Opus, the stacking account is wrong and must be revised.")

# --- unchanged registered decision lines -----------------------------------------------------
DOMINANCE_IF = "best cell of the 2x3 >= 20/30 -> demote the prevalence framing and rewrite"
PREVALENCE_SURVIVES_IF = "best cell <= 15/30"
AMBIGUOUS_IF = "16-19/30 -> neither promote nor demote"
SENSITIVITY_GUARD = "any arm with se < 0.50 cannot be read as an improvement whatever its fp"
ORACLE_FP = 0.0588           # perfect publication-type exclusion, computed before condition C ran
HARDCORE_N = 63              # documents all four earlier lineages called eligible and experts did not

# --- pre-declared reporting rules ------------------------------------------------------------
REPORT_RULES = [
 "Opus refusals, if any, get the same directional-missingness treatment as Sonnet's: observed, "
 "worst (all refused counted eligible), best (none), and MAR-within-stratum. The pilot saw zero, "
 "so a nonzero rate in the full run is itself reportable.",
 "Report the hard-core release count for both new arms out of 63.",
 "If Opus_A beats Sonnet_A on fp but the two-point trend is saturating, BOTH facts are reported; "
 "the favourable one is not reported alone.",
 "No threshold in this file may be revised after seeing a label.",
]

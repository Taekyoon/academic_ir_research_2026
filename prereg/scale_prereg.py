r"""PRE-REGISTERED open-weight scale ladder. Written before any open-weight label existed.

WHY THIS AXIS AND NOT THE ONE WE ALREADY RAN. The project measured a capability axis across
Haiku 4.5 -> Sonnet 4.5 -> Opus 4.5 and it came out NON-MONOTONE, which invalidated a projection
that had been built on a single measured capability step (scaling_threat_ko.md, withdrawn). But
those three models differ in more than capability - different training data, different
post-training, and we could not separate scale from the rest. Within one open-weight family the
only thing that varies is parameter count, so this is the capability axis the earlier experiment
could not isolate.

Second reason: every label in this project so far comes from a proprietary API with an unknown
serving configuration. Nobody outside can rerun the judging step. Open weights with pinned
revisions and pinned decoding parameters make that step reproducible, which is what the
companion repository is for.

--------------------------------------------------------------------------------------------
DESIGN

Sample. The SAME frozen 2,025-pair stratified panel used for the four-lineage comparison
(panel_sample.csv), so every new arm is directly comparable to gpt-4o-mini, Qwen3-30B-A3B,
Mistral-Small-24B, Haiku-4.5, Sonnet-4.5 and Opus-4.5 without any new sampling.

Conditions. The SAME two prompts: A (review title only) and C (title + the generic
study-design criteria block). No new prompt is written.

Arms. Qwen3 dense ladder, 4 points spanning 8x:
    qwen3-4b, qwen3-8b, qwen3-14b, qwen3-32b
plus one LINEAGE CONTROL at a single scale:
    llama-3.1-8b-instruct
The control exists so that an 8B result cannot be read as a property of Qwen specifically. The
existing Qwen3-30B-A3B panel arm is an MoE point and is reported beside the dense ladder, never
inside it - active parameters are not comparable to dense parameter count.

Total judgements: 5 arms x 2 conditions x 2,025 pairs = 20,250.

--------------------------------------------------------------------------------------------
H-S1  IS THE JUDGE'S DISCRIMINATION MONOTONE IN SCALE, WITHIN ONE FAMILY?

Measure Youden J = se - fp at the registered binarisation (grade >= 2) for each of the four
dense Qwen sizes, condition A and condition C separately.
    J is non-decreasing across 4B -> 8B -> 14B -> 32B in BOTH conditions
        -> "MONOTONE": scale is a usable axis, and H-S2's projection may be reported.
    otherwise
        -> "NON-MONOTONE": the earlier non-monotone finding is not an artifact of comparing
           different model families, it survives within a family. The projection in H-S2 is
           then NOT reported, exactly as the earlier one was withdrawn.
This ordering is the GATE on the projection. It is registered here so the projection cannot be
reported on the strength of a pattern chosen after seeing it.

H-S2  DOES SCALE REACH THE GATE?  (the falsifiable form of the paper's claim on a new axis)

The paper argues the required specificity grows as 1/p, so a constant improvement in the judge
cannot keep up. On a scale axis that predicts: the number of USABLE topics
(|relative denominator bias| <= 0.5) stays roughly flat as scale grows, even while fp falls.
    usable topics at 32B exceeds usable topics at 4B by <= 2 of 30
        -> "ARITHMETIC HOLDS ON THE SCALE AXIS".
    usable topics at 32B exceeds usable topics at 4B by >= 6 of 30
        -> "CLAIM WEAKENED BY SCALE": scale substantially fixes the denominator, the paper's
           central argument does not survive the scale axis, and the claim must be rescoped to
           small judges. Reported as such. This is the outcome that would hurt most and it is
           registered with the same weight as the other.
    3 to 5 -> "PARTIAL", reported, no promotion either way.
If and only if H-S1 is MONOTONE, additionally fit log(fp) ~ log(parameters) over the four dense
points and report the extrapolated parameter count at which fp would meet the per-topic required
specificity. That number is reported as an extrapolation with its fit quality, never as a
prediction, and the fit is shown.

H-S3  DOES THE HARD CORE SURVIVE?

63 documents were called eligible by all four proprietary lineages against expert judgement
(panel_hardcore.json), against 0.9 expected under independence. Compute how many of those 63
each open arm also calls eligible.
    the four dense Qwen arms each call >= 40 of 63 eligible
        -> "HARD CORE IS NOT A FAMILY ARTIFACT": it is shared across proprietary and
           open-weight lineages, so it points at the criterion rather than at any judge.
    <= 20 for two or more arms
        -> "PARTLY A FAMILY ARTIFACT": the earlier 71x dependence multiplier is inflated by
           relatedness among the proprietary arms and must be reported with that caveat.

H-O1  LINEAGE CONTROL AT 8B

Compare llama-3.1-8b to qwen3-8b on se, fp and usable topics. Registered as descriptive: a
single control point cannot separate lineage from scale, and no threshold is set. It exists to
stop an 8B claim being read as a Qwen property.

--------------------------------------------------------------------------------------------
HARNESS RULES, fixed here because this project has had labels moved by harness changes THREE
times (a too-small output cap manufacturing labels via a loose fallback pattern; a prompt
carrying two contradictory output instructions; a decoding parameter mismatched against the
instrument paper).

R1  FREE GENERATION FIRST. Every arm is run with unconstrained decoding and the STRICT parser
    only: re.search(r"##\s*final\s*score\s*:?\s*([0-3])", text, re.I). Strict parse rate is
    measured and reported per arm before anything else is computed.

R2  GUIDED DECODING IS A DIFFERENT HARNESS. If an arm's strict parse rate is below 0.95, that
    arm is re-run with guided decoding constraining the output to the score line. When that
    happens, ONE arm that already passed at >= 0.95 is ALSO run guided, and the exact-grade
    agreement between its free and guided labels is reported as the bound on how much the
    harness change moves labels. Guided and free labels are never mixed within an arm.

R3  NO FALLBACK PARSER, EVER. A row that does not match the strict pattern is recorded as
    label=null and counted. It is never filled by a looser pattern, by the first digit in the
    text, or by a default.

    AMENDMENT, written before any label existed: an earlier draft of this file said "after 3
    attempts", copied from the API-based runs. That is wrong here. At temperature 0 the decode
    is deterministic, so re-running an identical prompt returns an identical string and a parse
    failure cannot be retried away. Therefore: a parse failure is recorded on ONE attempt, and
    the 3-attempt retry applies only to TRANSIENT failures (OOM, CUDA error, loader error),
    which are counted separately from parse failures. Reporting a parse failure as "failed
    after 3 attempts" would have overstated the effort behind the null.

R4  DECODING PARAMETERS ARE PINNED AND IDENTICAL ACROSS ARMS: temperature 0, top_p 1,
    max_tokens 1024, seed 20260908. max_tokens is set high because a Claude-family arm was
    previously truncated before its score line at 400; 1024 is non-binding for models that
    emit a score directly and prevents the same failure.

R5  MODEL IDENTITY IS PINNED BY REVISION. The HuggingFace repo id AND commit sha are recorded
    for every arm, plus quantisation (none / awq / gptq / bnb-4bit) and the serving stack
    version. An arm whose sha is not recorded is not reportable.

R6  THINKING MODES OFF. Qwen3 ships a thinking mode; it is disabled explicitly and the setting
    is recorded, because a reasoning preamble is what truncated the earlier Claude arm.

--------------------------------------------------------------------------------------------
DISCLOSED

  - PRECISION IS FIXED AT bf16 FOR EVERY ARM. No quantisation of any kind - no AWQ, no GPTQ,
    no bitsandbytes 4-bit. An earlier draft of this file allowed 4-bit for the largest size
    with a precision control at 14B; that is WITHDRAWN. Precision is now held constant by
    construction, so the ladder varies parameter count and nothing else and the confound the
    earlier draft tried to measure cannot arise.

    THE CONSEQUENCE, registered here rather than discovered mid-run: bf16 needs about 2 bytes
    per parameter, so a size that does not fit the available GPU is NOT RUN. It is reported as
    not attempted and is absent from every table - never substituted by a quantised run at the
    same nominal size. Approximate weight footprints from published parameter counts, before
    KV cache and activations:

        qwen3-4b    ~8 GB      qwen3-14b   ~30 GB
        qwen3-8b    ~16 GB     qwen3-32b   ~66 GB
        llama-3.1-8b-instruct  ~16 GB

    So the reachable ladder is a property of the device: 4B and 8B on a 24 GB card, up to 14B
    on 40 GB, all four only on 80 GB. H-S1's monotonicity judgement is made over whichever
    dense sizes actually ran and the number of points is stated with the verdict - a
    three-point ladder (4B, 8B, 14B) still spans 3.5x and is reported as three points, not
    presented as the registered four.
  - PER-TOPIC SPECIFICITY PINS AT 1.000 on a 40-document non-eligible stratum. The census
    experiment bounded this: on six topics the sampled point estimate matched the population
    value within 0.0233, and the pin biases the denominator toward UNDER-count, i.e.
    conservatively for this paper's direction. Pooled rates are used for anything cross-arm.
  - THE PANEL'S TOPICS ARE BIOMEDICAL SYSTEMATIC-REVIEW SCREENING at prevalence 0.0003-0.202.
    Nothing here extends to open-domain question answering.
  - 30B-A3B IS NOT A LADDER POINT. It is MoE; active parameters are 3B and total 30B, and
    neither is comparable to a dense count. It is reported beside the ladder.
  - A NULL ON H-S2 IS NOT EVIDENCE FOR THE PAPER unless the arms actually differ in fp. If fp
    is flat across the ladder the experiment has not tested the arithmetic, only reproduced a
    constant judge, and that is what is reported.
"""

DENSE_LADDER = [("qwen3-4b", 4.0e9), ("qwen3-8b", 8.0e9),
                ("qwen3-14b", 14.0e9), ("qwen3-32b", 32.0e9)]
LINEAGE_CONTROL = "llama-3.1-8b-instruct"
MOE_BESIDE = "qwen3-30b-a3b"
CONDITIONS = ("A", "C")
BINARISE_AT = 2
USABLE_BAND = 0.5
STRICT_PARSE_MIN = 0.95
HARD_CORE_SURVIVES = 40
HARD_CORE_ARTIFACT = 20
USABLE_GAIN_HOLDS = 2
USABLE_GAIN_WEAKENS = 6
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 1024
SEED = 20260908
N_PAIRS = 2025

# ============================================================================================
# AMENDMENT 3 - CROSS-FAMILY LADDERS. Written before any Llama or Gemma label existed. Labels
# that DID exist at writing time: qwen3-4b and qwen3-8b, conditions A and C, from run 1 on an
# L4 (scale_run1_ko.md). No label from any other family or size existed.
#
# WHY. Run 1 could not evaluate H-S1 or H-S2 at all: the L4 admitted only two dense sizes and
# one of them (4B) fell below the registered strict-parse floor, leaving ONE clean point. But
# the deeper problem is that a single-family ladder cannot answer the question it was built for.
# If the Qwen3 ladder shows a trend, a reviewer can say it is a Qwen property. Reproducibility
# of a SCALE trend means the trend recurs when the pretraining data, tokenizer and post-training
# recipe all change - i.e. across families. So the design becomes three ladders, not one.
#
# ARMS. Every size whose bf16 weights fit the device, per family. Parameter counts are the
# safetensors totals reported by the HuggingFace API, not estimates:
#
#   qwen3   Qwen3-1.7B (2.03B, 3.8 GB)   Qwen3-4B (4.02B, 7.5 GB)
#           Qwen3-8B (8.19B, 15.3 GB)    Qwen3-14B (14.77B, 27.5 GB)
#           Qwen3-32B (32.76B, 61.0 GB - 80 GB device only)
#   llama   Llama-3.2-1B-Instruct (1.24B, 2.3 GB)   Llama-3.2-3B-Instruct (3.21B, 6.0 GB)
#           Llama-3.1-8B-Instruct (8.03B, 15.0 GB)
#           (Llama-3.3-70B is 131.4 GB in bf16 and is out of reach on any single A100.)
#   gemma   gemma-3-1b-it (1.00B, 1.9 GB)   gemma-3-4b-it (4.30B, 8.0 GB)
#           gemma-3-12b-it (12.19B, 22.7 GB)
#           gemma-3-27b-it (27.43B, 51.1 GB - 80 GB device only)
#
# On a 40 GB A100 that is 4 + 3 + 3 = 10 arms, spans 7.3x / 6.5x / 12.2x. On 80 GB it is 12.
# Conditions A and C as before, same frozen 2,025-pair panel, so 40,500 or 48,600 judgements.
#
# --------------------------------------------------------------------------------------------
# H-S1 IS RESTATED PER FAMILY. Youden J = se - fp is tested for monotonicity WITHIN each family
# separately, and the verdict is reported per family with its point count. A family with fewer
# than three clean points is reported as "not testable", not merged with another family to reach
# three. The registered gate on H-S2's projection now reads: the projection may be reported only
# for a family whose own J is monotone.
#
# H-X1  DOES THE SCALE TREND REPLICATE ACROSS FAMILIES?  (the new primary question)
#
# For each family fit log(fp) ~ log(parameters) over its clean arms and take the slope b_fam.
# The slope is the quantity that is comparable across families; the intercept is not, because
# families differ in absolute calibration for reasons that have nothing to do with scale.
#     all three slopes negative AND the ratio max|b|/min|b| <= 3
#         -> "TREND REPLICATES": improvement with scale is a property of scale, not of a family.
#     any slope non-negative, or the ratio > 3
#         -> "TREND IS FAMILY-DEPENDENT": scale does not have a family-independent effect on the
#            judge's false-positive rate, and no single scaling statement may be made. This is
#            the outcome that would force the paper to drop scale as an axis entirely, and it is
#            registered with the same weight.
# Reported with the fit quality per family and the point count. Three or four points is a weak
# fit and the slope is reported with its standard error; it is never presented as a law.
#
# H-X2  DOES THE GATE VERDICT AGREE ACROSS FAMILIES AT COMPARABLE SCALE?
#
# At the ~8B band (Qwen3-8B, Llama-3.1-8B) and the ~4B band (Qwen3-4B, Llama-3.2-3B,
# gemma-3-4b-it), compare usable topics out of 30.
#     the band spread in usable topics is <= 2 -> "SCALE DOMINATES FAMILY at that band"
#     >= 6                                     -> "FAMILY DOMINATES SCALE at that band", and the
#                                                 cross-family comparison, not the ladder, is
#                                                 what the paper should report.
# Bands are named here, before any label exists, so a band cannot be chosen afterwards to suit
# the result. gemma has no 8B release, so the ~8B band has two members and that is stated with
# the number rather than filled by substituting gemma-3-12b-it.
#
# --------------------------------------------------------------------------------------------
# DISCLOSED, in addition to everything above
#
#   - LLAMA AND GEMMA ARE GATED WITH MANUAL APPROVAL ("gated": "manual" on the HuggingFace API),
#     not merely token-gated. The licences must be accepted per model on the model page with the
#     account that owns the token. A family that cannot be downloaded is reported as NOT
#     ATTEMPTED, exactly as 14B and 32B were in run 1.
#   - THE GEMMA LADDER MIXES ARCHITECTURES. gemma-3-1b-it is Gemma3ForCausalLM while
#     gemma-3-4b-it and gemma-3-12b-it are Gemma3ForConditionalGeneration, i.e. the larger two
#     are multimodal checkpoints used here on text only. That is a within-family confound
#     between scale and architecture which this design does NOT resolve, and any gemma slope is
#     reported carrying it. It is disclosed now rather than discovered in the fit.
#   - SIZES ARE NOT ALIGNED ACROSS FAMILIES and are not forced to be. H-X1 compares slopes,
#     which does not require matched sizes; H-X2 compares two named bands and states their
#     membership. No family's ladder is re-banded after the fact to improve alignment.
#   - RUN 1 LABELS ARE REUSED for qwen3-4b and qwen3-8b under conditions A and C. They were
#     produced by the same script, prompts and pinned decoding, so they are the same harness -
#     but the transformers version differs from run 1 (run 1 predates the 4.57.6 pin), and that
#     is recorded per arm in the manifests. If qwen3-8b is re-run here, free-generation labels
#     from both runs are compared and the exact-grade agreement is reported as a harness check.
#   - THE 4B PARSE FAILURE FROM RUN 1 IS NOT CARRIED OVER. Any arm below the 0.95 strict floor is
#     excluded from every verdict here too, and R2's guided remedy applies unchanged.
#   - DOWNLOAD VOLUME is about 110 GB of weights on a 40 GB device and 222 GB on 80 GB. This is
#     an operational cost, not a scientific one, but a session that dies part-way must report
#     which arms completed rather than presenting a partial ladder as the registered design.

# ============================================================================================
# AMENDMENT 4 - THE DEVICE CEILING IS FIXED AT A100 40 GB. Written before any Llama or Gemma
# label existed, on the user's statement that only a 40 GB A100 is available.
#
# This is a DECLARED SCOPE, not a failure to report later. Qwen3-32B (61.0 GB in bf16) and
# gemma-3-27b-it (51.1 GB) are out of scope for this study and are absent from every table and
# every fit. They are not "not attempted" in the sense that 14B was in run 1 - that was a
# discovery mid-run; this is a boundary set in advance. Llama-3.3-70B (131.4 GB) was already
# out of reach on any single A100.
#
# THE LADDERS ARE THEREFORE FINAL AT:
#     qwen3   1.7B  4B  8B  14B          4 points, span 7.3x
#     llama   1B    3B  8B               3 points, span 6.5x
#     gemma   1B    4B  12B              3 points, span 12.2x
# 10 arms x 2 conditions x 2,025 pairs = 40,500 judgements, about 110 GB of weights.
#
# CONSEQUENCES that must travel with every verdict, stated now:
#   - THE LADDERS TOP OUT AT DIFFERENT SIZES (14B, 8B, 12B). H-X1 compares slopes, which does
#     not require matched endpoints, but a slope fitted over 1-14B and one fitted over 1-8B are
#     not equally constrained at the top, and llama's is the least constrained. The point count
#     and range are reported beside every slope.
#   - H-X2's ~8B BAND HAS TWO MEMBERS (Qwen3-8B, Llama-3.1-8B). gemma has no 8B release and
#     gemma-3-12b-it is NOT substituted into that band. The ~4B band has three
#     (Qwen3-4B, Llama-3.2-3B, gemma-3-4b-it).
#   - NO CLAIM IS MADE ABOUT 27B-32B SCALE. If a reviewer asks whether the trend continues, the
#     answer is that this study does not reach that range, not that the trend flattens there.
#     Extrapolating a 4-point fit past its largest point would be the same error as the
#     withdrawn projection in scaling_threat_ko.md.
#
# OPERATIONAL, and registered because a partial run must not be presented as the design:
#   - RESUMABILITY. An arm whose label file already exists with the full 2,025 rows is skipped
#     rather than re-judged, so a session that dies part-way resumes instead of restarting.
#     Skipped-as-complete and freshly-judged arms are distinguished in the manifest set.
#   - DISK. About 110 GB of weights will not co-exist with a Colab disk of typical size, so each
#     arm's weights are purged from the hub cache after its labels are written. The purge is
#     conditional on the labels existing, so a failed arm keeps its download for a retry.
#   - A SESSION THAT ENDS WITH FEWER THAN 10 ARMS reports exactly which arms completed, and the
#     per-family point counts are recomputed from what completed. A family reduced below three
#     points is reported as "not testable" for H-S1, as already registered in amendment 3.

# ============================================================================================
# AMENDMENT 5 - PERMISSIVE GUIDED DECODING BECOMES THE PRIMARY BASIS FOR EVERY OPEN ARM.
# Written before any guided label existed. Labels that DID exist at writing time: the 16 free
# arm-conditions of run 2 (scale2_results_ko.md). No guided label of any arm existed.
#
# WHY. Run 2's free-generation basis is not a common harness. Four arm-conditions parsed at 1.00
# and four parsed at 0.05-0.79, so the comparison set was decided by output-format compliance
# rather than by judging behaviour: H-S1 became testable for one family only, and H-X1 and H-X2
# could not be evaluated at all. Making the harness uniform is the fix, and R2 already named
# guided decoding as the remedy - this amendment applies it to EVERY open arm rather than only
# to the ones that failed, because a remedy applied selectively is itself a selection effect.
#
# WHICH GUIDED. Permissive: [\s\S]*## final score: [0-3]. Constrained decoding only permits the
# end-of-sequence token in an accepting state, so a model cannot stop before emitting a valid
# score line, but it may reason first. This changes the output CONTRACT and nothing else.
#
# The STRICT variant (score line only) is NOT the primary remedy and this is a substantive
# choice, not a preference. llama-3.1-8b emits a median of 235 reasoning tokens before its
# answer; forbidding prose deletes that computation, so strict-guided labels are labels of a
# different procedure and are not comparable to a free run of the same model. Strict is retained
# as --guided-strict for a declared secondary probe on one arm, reported separately, never
# pooled with permissive labels.
#
# THE PARSER IS NOT TOUCHED. STRICT stays r"##\s*final\s*score\s*:?\s*([0-3])". Changing the
# parser at the same time as the harness would make the two effects inseparable.
#
# --------------------------------------------------------------------------------------------
# H-H1  HOW MUCH DOES THE HARNESS MOVE THE LABELS?  (new, and it gates everything else)
#
# Four arm-conditions passed free generation at >= 0.95: qwen3-1.7b A and C, qwen3-8b A and C,
# qwen3-14b A and C, gemma-3-12b-it A and C. Every one of them is ALSO run guided, giving paired
# free/guided labels on identical pairs. On those pairs:
#     exact-grade agreement >= 0.95 AND |delta fp| <= 0.02 in every pair
#         -> "HARNESS EFFECT BOUNDED": the guided ladder may be compared to the free-generation
#            proprietary arms, with the measured agreement quoted as the bound.
#     agreement < 0.90 in any pair, or |delta fp| > 0.05 in any pair
#         -> "HARNESS EFFECT MATERIAL": every open-versus-proprietary comparison in the paper is
#            declared harness-confounded and the open arms are compared only to each other.
# Between those, report both numbers and make no comparison claim either way.
#
# This is registered as a GATE rather than a curiosity because the paper's open-weight claim is
# an open-versus-proprietary comparison, and that comparison survives only if H-H1 is bounded.
#
# THE CONFOUND THAT CANNOT BE REMOVED, stated now. The proprietary arms were judged through
# APIs, and no API offers regex-constrained decoding, so they cannot be re-run guided. Uniformity
# is therefore achievable WITHIN the open arms and not across the whole study. All-guided does
# not eliminate the harness confound; it relocates it to the open/proprietary boundary and makes
# it measurable there, which is why H-H1 exists.
#
# --------------------------------------------------------------------------------------------
# WHAT THIS CHANGES IN THE EXISTING HYPOTHESES
#
#   - H-S1, H-S2, H-X1, H-X2 are evaluated on the GUIDED labels, all arms, uniform harness.
#     The free-generation verdicts of run 2 stand as reported and are not overwritten: they are
#     the free-harness result and are cited as such.
#   - THE 0.95 STRICT-PARSE FLOOR STILL APPLIES. Guided decoding should make it unreachable, but
#     an arm that somehow lands below it is still excluded, and truncation at max_tokens is the
#     one way it can happen - the permissive regex forbids stopping early but not running out of
#     budget. max_tokens stays 1024 and the truncation count is reported per arm.
#   - RUN 2's SINGLE MOST INTERESTING NUMBER IS NOW TESTABLE. llama-3.1-8b's surviving free
#     labels gave fp 0.0347 (A) and 0.0164 (C) with 15/30 and 7/30 usable topics, better than
#     any judge measured in this project including Opus 4.5 - on a 54%/67% subset whose
#     selection mechanism was unmeasurable. The guided run either reproduces that on the full
#     2,025 pairs or refutes it. It is registered here as an OPEN QUESTION with no predicted
#     direction, and whichever way it comes out is reported.
#   - llama-3.2-1B and llama-3.2-3B were not run in run 2. Without them the llama ladder has one
#     point and H-X1 stays unevaluable however good the harness is, so they are part of this run.
#
# LOGGING FIX, registered because it is why llama could not be diagnosed in run 2: raw is stored
# as the first 200 AND last 200 characters of the completion rather than the head alone. 100% of
# llama's free failures hit the 200-character cap, so whether a score line followed its reasoning
# was unknowable.

# ============================================================================================
# AMENDMENT 6 - THE SAME-RUN RULE. Set by the user before the guided re-run, and it is a
# constraint on the ANALYSIS, not on the execution: every comparison must be made among arms
# that came out of ONE identical execution - same harness, same decoding parameters, same seed,
# same prompts, same session.
#
# WHY IT IS BEING WRITTEN DOWN. The first guided attempt violated it invisibly. The constraint
# bound on 8 of 16 arm-conditions and not on the other 8, so a table of "the guided run" would
# have placed constrained and unconstrained arms side by side under one column heading. Nothing
# in the strict parse rates revealed it; the arms where the constraint did not bind simply looked
# like the free run, because that is what they were.
#
# WHAT THE RULE MAKES VALID, AND WHAT IT INVALIDATES, in the material already in hand:
#
#   VALID - run 2, free generation. All 8 arms x 2 conditions went through one harness with the
#   same seed, prompts and precision in one session. Arms that fell below the 0.95 strict floor
#   are excluded, but that exclusion is an OBSERVATION MADE WITHIN that harness, not a difference
#   between harnesses. So the run-2 verdicts stand under this rule and need no re-run:
#       H-S1 qwen3 MONOTONE on 1.7B / 8B / 14B in both conditions;
#       the decomposition that J rises because sensitivity rises (+0.230 in A) while the
#       false-positive rate is flat or rising (+0.076 in A, -0.015 in C);
#       usable topics flat at 1 -> 1 and 4 -> 2 of 30.
#
#   INVALID - the guided attempt. Not one execution in the sense this rule requires, so no
#   verdict may be read off it. Its only surviving use is diagnostic: which arms the constraint
#   bound on, and the H-H1 numbers on the three arms where it did bind - and those are explicitly
#   labelled as a cross-harness measurement, which is what H-H1 is for.
#
# CONSEQUENCES FOR THE RE-RUN, registered now:
#
#   1. THE ENFORCEMENT PROBE DECIDES MEMBERSHIP, NOT THE PARSE RATE. An arm whose probe fails is
#      not in the guided comparison set at all. It is reported as "constraint did not bind" and
#      is NOT back-filled with free-generation labels, because that would rebuild the very mixed
#      basis this rule exists to forbid.
#   2. A REDUCED SET IS REPORTED AS REDUCED. If the probe passes on only some arms, the guided
#      verdicts are stated over exactly those arms with the count, and the free-generation
#      verdicts of run 2 remain the result for the full set. The two are never merged into one
#      table.
#   3. ONE SESSION PER COMPARISON SET where the disk allows it. Running families in separate
#      sessions is permitted because the harness is fixed in code and pinned in the manifest, but
#      the manifest fields that define the execution - harness, dtype, seed, temperature,
#      max_tokens, transformers version, GPU - are checked for equality across every arm in a
#      comparison set before any verdict is computed, and an inequality voids the set.
#   4. H-H1 IS RE-MEASURED. The corrected target ##[ ]?final score: [0-3] accepts the model's
#      natural output, so the constraint now reaches the decision rather than becoming
#      unsatisfiable after it. The earlier BOUNDED reading was obtained under a constraint that
#      never touched the decision and does not transfer.
#
# COST, from run 2's measured throughput: 19 minutes of GPU for the 8 existing arms at free-run
# speed, plus llama-3.2-1B and llama-3.2-3B. The corrected regex should remove the token burn
# entirely - the model can now satisfy the automaton with the output it would have produced
# anyway - so guided throughput is EXPECTED to return to free-run levels. That expectation is
# checked against the manifest, not assumed: if rows_per_second is still an order of magnitude
# below run 2, the constraint is still fighting the model and the run is stopped.

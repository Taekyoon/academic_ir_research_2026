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

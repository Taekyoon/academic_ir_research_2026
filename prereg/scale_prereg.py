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

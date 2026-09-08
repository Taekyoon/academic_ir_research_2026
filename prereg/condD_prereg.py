"""PRE-REGISTERED test of condition D. Written before any condition-D label existed.

THE QUESTION, in the user's words: if you align the judge's prompt as far as possible toward
what the expert means by eligible, does the denominator problem go away?

Condition C already tested a generic version: one paragraph naming primary-studies-only and
excluding reviews, meta-analyses, editorials, letters, comments, case reports, animal and in
vitro work. Identical text for all 30 topics. It worked in the expected direction (pooled fp
0.0618 -> 0.0314 on Opus, hard core 43/63 released) but usable topics barely moved (10 -> 11
paired) because the required specificity scales as 1/p.

Condition D is the strong version: each topic's OWN eligibility criteria, written by the authors
of that review, taken from the campaign's released protocol files.

SOURCE OF THE CRITERIA - this is the part that makes D possible at all, and it was NOT available
when C was designed. 2018-TAR/Task1/{Testing,Training}/protocols/<topic> are XML files with six
fields. 23 of the 30 panel topics have one; 22 parse cleanly (CD009647 is malformed XML and is
EXCLUDED - a lenient &-escape repair was attempted and failed). The block inserted into the
prompt uses five fields:

    type_of_study, participants, index_tests, target_conditions, reference_standards

`objective` is deliberately EXCLUDED: it restates the review's aim rather than stating a
criterion, so including it would add cost without adding eligibility information. This choice is
recorded here, before any label, so it cannot be tuned after seeing results.

Inserted block length: min 2,045 / median 3,978 / max 9,987 characters, against 526 for
condition C. So D supplies roughly 7.6x more criteria text per topic.

BASIS DISCIPLINE - the failure mode this project has hit four times.
  Conditions A and C already have labels on all 30 topics. D can only cover 22. Every C-vs-D
  comparison in the analysis MUST be recomputed on the SAME 22 topics and the SAME rows that
  carry a strict label in BOTH arms. The 30-topic figures from
  opus_results_paired_fixedweights.csv (se 0.6202, fp 0.0314, within 11/30) MUST NOT be carried
  into the D comparison table. They are a different basis and are reported separately, if at all.

PRIMARY OUTCOME is POOLED specificity, not per-topic. Reason, established earlier this session:
the non-eligible stratum is 40 documents per topic, so per-topic specificity for a good judge
pins at exactly 1.000 in 14 of 30 topics (P(zero false positives in 40 | true sp = 0.99) = 0.67),
and 8 of condition C's 12 per-topic-usable topics are such pinned estimates. Pooled specificity
rests on ~1,100 non-eligible documents over the 22 topics and does not have this defect.

REGISTERED THRESHOLDS. The requirement, computed earlier from the identity and the per-topic
prevalences, is a specificity of 0.99033 (median of the dense band) rising to 0.99949 (median of
the sparse band), max 0.99997. Condition C achieved 0.9686 pooled. So:

  H-D1  PRIMARY.
        pooled sp(D) >= 0.99   -> "GATE MOVES": per-topic criteria clear the loosest (dense-band)
                                  requirement. The admissibility boundary must be recomputed and
                                  the arithmetic-ceiling argument weakened accordingly.
        pooled sp(D) <  0.98   -> "ARITHMETIC HOLDS": a 7.6x increase in criteria text does not
                                  reach the requirement, which strengthens the claim that a
                                  constant-size prompt gain cannot track a 1/p requirement.
        0.98 <= sp(D) < 0.99   -> "AMBIGUOUS": neither promoted nor demoted. Reported as such.

  H-D2  SENSITIVITY GUARD. Condition C cost 0.041 of sensitivity against A. If se(D) < 0.50 the
        guard FIRES: a judge that misses half the eligible studies is unusable whatever its
        specificity, and any specificity gain in D is then bought with a loss that disqualifies
        it. Fired guard is reported alongside H-D1, never instead of it.

  H-D3  USABLE TOPICS, secondary. Count of topics with |relative bias| <= 0.5 using each topic's
        OWN measured rates, on the 22-topic basis, reported for C and D side by side AND with the
        count of pinned (sp == 1.000) topics given separately in the same table. A rise driven by
        pinning is not a rise.

  H-D4  HARD CORE, secondary. Of the hard-core documents (all four lineages eligible, expert
        non-eligible) that fall in these 22 topics, what fraction does D release? Condition C
        released 43/63 = 68% on the full 30. Same-topic restriction applies.

  CEILING GUARD. If fp(D) < 0.0050 - below anything measured for any arm in this project - stop
        and audit the harness before interpreting, because it is more likely a parsing or
        merge fault than a real result.

WHAT THIS CANNOT SETTLE, stated in advance.
  - 22 of 30 topics only. The 8 excluded (7 with no protocol, CD009647 malformed) are not a
    random subset - they are whichever topics the 2018 task happened to reuse - so D's pooled
    rate is not an estimate of what D would do on all 30.
  - The protocols are the FINAL review protocols. A screener at the time of screening has the
    protocol, so this is a realistic intervention, but the protocol text may reflect decisions
    settled after screening began. This inflates D's advantage if anything, which makes a
    negative result safe and a positive result in need of that caveat.
  - Single arm (Opus 4.5, the best judge measured). A null in D is therefore a null for the best
    judge, and cheaper judges are not covered.
"""

SP_GATE_MOVES = 0.99
SP_ARITHMETIC_HOLDS = 0.98
SE_FLOOR = 0.50
FP_CEILING_GUARD = 0.0050
BINARISE_AT = 2
BIAS_USABLE = 0.5
FIELDS = ["type_of_study", "participants", "index_tests", "target_conditions",
          "reference_standards"]
EXCLUDED_FIELD = "objective"
EXCLUDED_TOPICS = ["CD009647"]          # malformed XML, repair attempted and failed
N_TOPICS_EXPECTED = 22
N_ROWS_EXPECTED = 1508

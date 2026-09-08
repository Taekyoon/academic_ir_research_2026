"""Analysis of the pre-registered 2x3. Written BEFORE any Opus label was read.
The verdict lines are printed by this script, not decided after seeing the numbers.

Two bases are reported and never mixed:
  PAIRED  - rows carrying a strict label in EVERY loaded arm. Comparisons use this.
  PANEL   - all 2,025 frozen pairs, refused rows retained. Refusal-missingness uses this.
Adding the Opus arms changes the paired intersection, so nothing is carried over from the 2x2.
"""
import json, glob, itertools, numpy as np, pandas as pd
from scipy import stats

THR, TARGET = 2, 0.5
FP_STEP_OBSERVED, SE_STEP_OBSERVED = 0.621, 0.9596
PANEL = pd.read_csv("panel_sample.csv", dtype={"topic": str, "pmid": str})
pan = PANEL.copy()
Rtrue = pan.groupby("topic").apply(lambda g: float((g.weight * (g.human >= 1)).sum()),
                                   include_groups=False)
DROP = ["human", "weight", "stratum"]

ARMS = {"haiku_A":  (["panel_labels_haiku_slice*.jsonl",
                      "panel_labels_claude-haiku-4-5.jsonl"], "A", "haiku"),
        "haiku_C":  (["condC_labels_haiku_C_slice*.jsonl"], "C", "haiku"),
        "sonnet_A": (["condC_labels_sonnet_A_slice*.jsonl"], "A", "sonnet"),
        "sonnet_C": (["condC_labels_sonnet_C_slice*.jsonl"], "C", "sonnet"),
        "opus_A":   (["opus_labels_A_slice*.jsonl"], "A", "opus"),
        "opus_C":   (["opus_labels_C_slice*.jsonl"], "C", "opus")}
GRADE_ORDER = ["haiku", "sonnet", "opus"]

def load_arm(pats):
    rows = []
    for pat in pats:
        for f in sorted(glob.glob(pat)):
            for ln in open(f):
                if ln.strip(): rows.append(json.loads(ln))
    if not rows: return None
    d = pd.DataFrame(rows)
    d["topic"] = d.topic.astype(str); d["pmid"] = d.pmid.astype(str)
    d = d.drop(columns=[c for c in DROP if c in d.columns])
    if "parsed" not in d.columns: d = d.assign(parsed=d.label.notna())
    return d.drop_duplicates(["topic", "pmid"], keep="last")

RAW = {nm: load_arm(p) for nm, (p, _, _) in ARMS.items()}
missing = [nm for nm, d in RAW.items() if d is None]
for nm in missing: print(f"  !! {nm}: no labels found")
RAW = {nm: d for nm, d in RAW.items() if d is not None}

def metrics(m):
    pos = m.label >= THR
    el, ne = m.human >= 1, m.human < 1
    b = {}
    for t, g in m.assign(pos=pos).groupby("topic"):
        if t in Rtrue.index and Rtrue[t] > 0:
            b[t] = (float((g.weight * g.pos).sum()) - Rtrue[t]) / Rtrue[t]
    b = pd.Series(b)
    return dict(n=len(m), se=float(pos[el].mean()), fp=float(pos[ne].mean()),
                bias_median=float(b.median()), abs_bias_median=float(b.abs().median()),
                within=int((b.abs() < TARGET).sum()), n_topics=int(b.size)), b

LAB = {nm: (d[d.parsed & d.label.notna()].set_index(["topic", "pmid"]).label)
       for nm, d in RAW.items()}
common = None
for k in LAB.values():
    common = k.index if common is None else common.intersection(k.index)
print(f"=== PAIRED rows (strict label in all {len(LAB)} arms): {len(common)} ===")
pidx = pan.set_index(["topic", "pmid"])[["human", "weight"]]
S, B = [], {}
for nm, k in LAB.items():
    m = pidx.loc[pidx.index.intersection(common)].join(k.rename("label")).reset_index()
    r, b = metrics(m)
    r["arm"], r["condition"], r["grade"] = nm, ARMS[nm][1], ARMS[nm][2]
    S.append(r); B[nm] = b
T = pd.DataFrame(S).set_index("arm")
print(T[["grade", "condition", "n", "se", "fp", "bias_median", "abs_bias_median",
         "within", "n_topics"]].round(4).to_string())
T.to_csv("opus_results_paired.csv")
pd.DataFrame(B).to_csv("opus_bias_by_topic.csv")

# ---- H-SAT: geometric or saturating capability axis -----------------------------------------
print("\n=== H-SAT: is the capability axis geometric or saturating? ===")
if {"haiku_A", "sonnet_A", "opus_A"} <= set(T.index):
    r1 = T.loc["sonnet_A", "fp"] / T.loc["haiku_A", "fp"]
    r2 = T.loc["opus_A", "fp"] / T.loc["sonnet_A", "fp"]
    print(f"  step 1  Haiku -> Sonnet : fp ratio {r1:.3f}   (2x2 basis reported {FP_STEP_OBSERVED})")
    print(f"  step 2  Sonnet -> Opus  : fp ratio {r2:.3f}")
    if r2 <= 0.70:
        print("  GEOMETRIC CONFIRMED: r <= 0.70. The scaling projection stands as an exposure "
              "estimate at the stated rate.")
    elif r2 >= 0.85:
        print("  SATURATING: r >= 0.85. The projection OVERSTATES the capability threat and the "
              "claim is more robust to scaling than reported. Revise scaling_threat_ko.md.")
    else:
        print("  AMBIGUOUS: 0.70 < r < 0.85. Report the two-point trend, draw no conclusion about "
              "functional form.")

# ---- H-SE: is the specificity-for-sensitivity trade intrinsic? ------------------------------
    print("\n=== H-SE: is the trade intrinsic to capability? ===")
    s1 = T.loc["sonnet_A", "se"] / T.loc["haiku_A", "se"]
    s2 = T.loc["opus_A", "se"] / T.loc["sonnet_A", "se"]
    print(f"  step 1 se ratio {s1:.4f}  |  step 2 se ratio {s2:.4f}")
    if T.loc["opus_A", "se"] < T.loc["sonnet_A", "se"]:
        print("  TRADE CONTINUES: the joint projection's turnover at se=0.5 stands and the "
              "sensitivity wall remains load-bearing.")
    else:
        print("  TRADE NOT INTRINSIC: sensitivity did NOT fall. The optimistic curve is the right "
              "one, the turnover argument must be WITHDRAWN, and the scaling threat is LARGER "
              "than we reported. Report as a weakening of our own position.")

# ---- registered decision lines --------------------------------------------------------------
best = T.within.idxmax(); bw = int(T.within.max())
print(f"\n=== PRE-REGISTERED VERDICT (paired; best cell {best}, {bw}/30) ===")
if len(RAW) < 6:
    print(f"  !! INCOMPLETE 2x3 - missing {missing}. Provisional.")
if bw >= 20:
    print("  DOMINANCE: >= 20/30 -> demote the prevalence framing and rewrite the claim.")
elif bw <= 15:
    print("  PREVALENCE SURVIVES: <= 15/30.")
else:
    print("  AMBIGUOUS: 16-19/30 -> neither promote nor demote.")
for nm in T.index:
    if T.loc[nm, "se"] < 0.50:
        print(f"  SENSITIVITY GUARD fired for {nm}: se {T.loc[nm,'se']:.4f} < 0.50 -> cannot be "
              "read as an improvement whatever its fp")
    if T.loc[nm, "fp"] < 0.0588:
        print(f"  CEILING GUARD for {nm}: fp {T.loc[nm,'fp']:.4f} beats the oracle 0.0588 -> "
              f"check sensitivity ({T.loc[nm,'se']:.4f}) before interpreting")

# ---- H-CAP3 and H-INT3 ----------------------------------------------------------------------
if "opus_A" in T.index:
    rivals = {k: int(T.loc[k, "within"]) for k in ("haiku_C", "sonnet_C") if k in T.index}
    if rivals:
        bestc = max(rivals, key=rivals.get)
        oa = int(T.loc["opus_A", "within"])
        print(f"\n  H-CAP3: opus_A {oa}/30 vs best criteria cell {bestc} {rivals[bestc]}/30 -> "
              + ("capability STILL substitutes" if oa >= rivals[bestc] else "no longer substitutes"))
print("\n  H-INT3: effect of adding the criteria block, by grade")
for g in GRADE_ORDER:
    a, c = f"{g}_A", f"{g}_C"
    if a in T.index and c in T.index:
        d = int(T.loc[c, "within"]) - int(T.loc[a, "within"])
        print(f"    {g:7s} {int(T.loc[a,'within']):2d} -> {int(T.loc[c,'within']):2d}  "
              f"({d:+d} topics) | fp {T.loc[a,'fp']:.4f} -> {T.loc[c,'fp']:.4f} | "
              f"se {T.loc[a,'se']:.4f} -> {T.loc[c,'se']:.4f}")
if "opus_A" in T.index and "opus_C" in T.index:
    d = int(T.loc["opus_C", "within"]) - int(T.loc["opus_A", "within"])
    print(f"    registered prediction was opus_C - opus_A <= -2; observed {d:+d} -> "
          + ("prediction held" if d <= -2 else "prediction FAILED, the stacking account needs revision"))
print("\nwrote opus_results_paired.csv, opus_bias_by_topic.csv")

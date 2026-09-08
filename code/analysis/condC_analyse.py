"""Analysis of the pre-registered 2x2. Written BEFORE any condition C label was read.
The verdict lines are printed by this script, not decided after seeing the numbers.
"""
import json, glob, numpy as np, pandas as pd
from scipy import stats

THR, TARGET = 2, 0.5
PANEL = pd.read_csv("panel_sample.csv", dtype={"topic": str, "pmid": str})
Rtrue = PANEL.groupby("topic").apply(
    lambda g: float((g.weight * (g.human >= 1)).sum()), include_groups=False)

def load_arm(pats):
    """pats may be one glob or a list of globs - the haiku condition A labels were produced in
    two batches. Drops any column that would collide with the panel on merge (the earlier run
    stored its own copy of `human`); the panel file is the single source of truth for labels."""
    if isinstance(pats, str): pats = [pats]
    rows = []
    for pat in pats:
        for f in sorted(glob.glob(pat)):
            for ln in open(f):
                if ln.strip(): rows.append(json.loads(ln))
    if not rows: return None
    d = pd.DataFrame(rows)
    d["topic"] = d.topic.astype(str); d["pmid"] = d.pmid.astype(str)
    d = d.drop(columns=[c for c in ("human", "weight", "stratum") if c in d.columns])
    return d.drop_duplicates(["topic", "pmid"], keep="last")

def metrics(d, name):
    """se, sp/fp and per-topic denominator bias for one arm, on rows with a strict parse."""
    src = d[d.parsed & d.label.notna()]
    m = src if {"human", "weight"} <= set(src.columns) else src.merge(
        PANEL[["topic", "pmid", "human", "weight"]], on=["topic", "pmid"], how="inner")
    pos = m.label >= THR
    el, ne = m.human >= 1, m.human < 1
    se = float(pos[el].mean()) if el.any() else np.nan
    fp = float(pos[ne].mean()) if ne.any() else np.nan
    bias = {}
    for t, g in m.groupby("topic"):
        if t not in Rtrue.index or Rtrue[t] == 0: continue
        bias[t] = (float((g.weight * (g.label >= THR)).sum()) - Rtrue[t]) / Rtrue[t]
    b = pd.Series(bias)
    return dict(arm=name, n=len(m), coverage=len(m) / len(PANEL), se=se, fp=fp,
                bias_median=float(b.median()), abs_bias_median=float(b.abs().median()),
                within=int((b.abs() < TARGET).sum()), n_topics=len(b)), b

ARMS = {"haiku_A":  (["panel_labels_haiku_slice*.jsonl",
                      "panel_labels_claude-haiku-4-5.jsonl"], "A"),
        "haiku_C":  ("condC_labels_haiku_C_slice*.jsonl", "C"),
        "sonnet_A": ("condC_labels_sonnet_A_slice*.jsonl", "A"),
        "sonnet_C": ("condC_labels_sonnet_C_slice*.jsonl", "C")}
S, B = [], {}
for nm, (pat, cond) in ARMS.items():
    d = load_arm(pat)
    if d is None:
        print(f"  !! {nm}: no labels found ({pat})"); continue
    if "parsed" not in d.columns:      # the panel run stored no parsed flag
        d = d.assign(parsed=d.label.notna())
    r, b = metrics(d, nm); r["condition"] = cond
    S.append(r); B[nm] = b
T = pd.DataFrame(S).set_index("arm")

# --- PAIRED restriction: arms differ in coverage (refusals, one unparseable reply), so the
# headline comparison must run on rows where EVERY loaded arm produced a strict label.
LAB = {}
for nm, (pat, cond) in ARMS.items():
    d = load_arm(pat)
    if d is None: continue
    if "parsed" not in d.columns: d = d.assign(parsed=d.label.notna())
    k = d[d.parsed & d.label.notna()].set_index(["topic", "pmid"]).label
    LAB[nm] = k[~k.index.duplicated()]
common = None
for k in LAB.values():
    common = k.index if common is None else common.intersection(k.index)
print(f"=== PAIRED rows (strict label in all {len(LAB)} loaded arms): {len(common)} ===")
PS_, PB_ = [], {}
pan = PANEL.set_index(["topic", "pmid"])[["human", "weight"]]
for nm, k in LAB.items():
    m = pan.loc[pan.index.intersection(common)].join(k.rename("label")).reset_index()
    r, b = metrics(m.assign(parsed=True), nm)
    r["condition"] = ARMS[nm][1]; PS_.append(r); PB_[nm] = b
TP = pd.DataFrame(PS_).set_index("arm")
print(TP[["condition", "n", "se", "fp", "bias_median", "abs_bias_median",
          "within", "n_topics"]].round(4).to_string())
TP.to_csv("condC_results_paired.csv")

print("\n=== per-arm coverage (unpaired, for the record) ===")
print(T[["condition", "n", "coverage", "se", "fp", "bias_median",
         "abs_bias_median", "within", "n_topics"]].round(4).to_string())

ORACLE_FP, ORACLE_WITHIN, BASE_WITHIN = 0.0588, 13, 11
print(f"\nreference: condition A Haiku fp 0.0842 within {BASE_WITHIN}/30 | "
      f"oracle ceiling fp {ORACLE_FP} within {ORACLE_WITHIN}/30")

T, B = TP, PB_        # the registered thresholds are evaluated on the PAIRED table
if len(T):
    best = T.within.idxmax(); bw = int(T.within.max())
    print(f"\n=== PRE-REGISTERED VERDICT (paired rows; best cell: {best}, {bw}/30) ===")
    if len(LAB) < 4:
        print(f"  !! INCOMPLETE 2x2 - missing {sorted(set(ARMS) - set(LAB))}. Provisional; "
              "recompute when the missing cell lands.")
    if bw >= 20:
        print("  DOMINANCE: >= 20/30. Prompt underspecification is the dominant explanation.")
        print("  -> demote the prevalence framing to secondary and rewrite the claim.")
    elif bw <= 15:
        print("  PREVALENCE SURVIVES: <= 15/30. The design filter is real but partial.")
    else:
        print("  AMBIGUOUS: 16-19/30. Neither account is promoted or demoted.")
    for nm in T.index:
        if T.loc[nm, "se"] < 0.50:
            print(f"  SENSITIVITY GUARD fired for {nm}: se {T.loc[nm,'se']:.3f} < 0.50 "
                  "-> report any fp gain as a TRADE, not an improvement")
        if T.loc[nm, "fp"] < ORACLE_FP:
            print(f"  CEILING GUARD fired for {nm}: fp {T.loc[nm,'fp']:.4f} beats the oracle "
                  "-> check sensitivity before interpreting")
    if {"sonnet_A", "haiku_C"} <= set(T.index):
        sa, hc = int(T.loc["sonnet_A", "within"]), int(T.loc["haiku_C", "within"])
        print(f"\n  H-CAP: sonnet_A {sa}/30 vs haiku_C {hc}/30 -> "
              + ("capability SUBSTITUTES for specification" if sa >= hc
                 else "specification matters more than capability grade"))
    if {"haiku_A", "haiku_C", "sonnet_A", "sonnet_C"} <= set(T.index):
        dh = T.loc["haiku_A", "fp"] - T.loc["haiku_C", "fp"]
        ds = T.loc["sonnet_A", "fp"] - T.loc["sonnet_C", "fp"]
        print(f"  H-INT: criteria cut fp by {dh:+.4f} on Haiku and {ds:+.4f} on Sonnet -> "
              + ("as registered, helps the weaker judge more" if dh > ds
                 else "OPPOSITE to the registered prediction - record as a surprise"))

# does the gain sit where the claim needs it - in the sparse topics?
cA = pd.read_csv("clef_condA_bias.csv", dtype={"topic": str})[["topic", "p"]]
for nm, b in B.items():
    if nm == "haiku_A" or "haiku_A" not in B: continue
    j = (pd.DataFrame({"b0": B["haiku_A"], "b1": b}).join(cA.set_index("topic")).dropna())
    if len(j) > 4:
        imp = j.b0.abs() - j.b1.abs()
        rr = stats.spearmanr(j.p, imp)
        print(f"  where does {nm} help? rho(eligibility rate, |bias| reduction) = "
              f"{rr.statistic:+.3f} (p={rr.pvalue:.2g}) "
              f"[positive => helps the DENSE topics, which would not address the claim]")

# how many of the 63 hard-core documents does each arm release?
HC = pd.read_csv("panel_bias.csv") if False else None
T.to_csv("condC_results.csv")
pd.DataFrame(B).to_csv("condC_bias_by_topic.csv")
print("\nwrote condC_results.csv, condC_bias_by_topic.csv")

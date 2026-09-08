"""Registered analysis of the cross-lineage judge panel. Conditions fixed in panel_prereg.py
before any non-OpenAI label existed.

  H-C1  per-model STRICT parse rate, reported, not rescued
  H-M1  is the DIRECTION of denominator overcounting model-robust under eligibility criteria?
  H-D1  are judge errors independent ACROSS pretraining lineages?
        OVERTURN CONDITION: if any AND-ensemble reaches a false-positive rate <= 0.0199, then
        multiplicity DOES fix the denominator and this project's contrary conclusion is dropped.

Everything is computed on COMPLETE CASES - pairs where every lineage produced a parsed label -
so the ensemble arithmetic is over one common set. The complete-case count is reported.
"""
import glob
import itertools
import json
import os
import re
import sys

import numpy as np
import pandas as pd

THR = 2
TARGET_FP = 0.0199          # fp needed for a denominator within 2x at CLEF median p = 0.0195


def load_lineages():
    """-> {lineage_label: DataFrame[topic, pmid, label]}, plus the raw parse-rate table."""
    out, parse = {}, []

    # OpenAI: already judged as condition A; restrict to the panel rows.
    panel = pd.read_csv("panel_sample.csv", dtype={"topic": str, "pmid": str})
    oa = pd.DataFrame([json.loads(l) for l in open("clef_labels_gpt-4o-mini_A.jsonl")])
    oa["topic"] = oa.topic.astype(str); oa["pmid"] = oa.pmid.astype(str)
    oa = oa.merge(panel[["topic", "pmid"]], on=["topic", "pmid"])
    parse.append(dict(lineage="openai · gpt-4o-mini", rows=len(oa),
                      parsed=int(oa.label.notna().sum())))
    out["openai · gpt-4o-mini"] = oa[oa.label.notna()][["topic", "pmid", "label"]]

    FILES = {
        "alibaba · qwen3-30b": ["panel_labels_qwen_qwen3-30b-a3b-instruct-2507.jsonl"],
        "mistral · small-24b": ["panel_labels_mistralai_mistral-small-24b-instruct-2501.jsonl"],
        "anthropic · haiku-4.5": (["panel_labels_claude-haiku-4-5.jsonl"]
                                  + sorted(glob.glob("panel_labels_haiku_slice*.jsonl"))),
    }
    for name, fs in FILES.items():
        rows = []
        for f in fs:
            if os.path.exists(f) and os.path.getsize(f):
                rows += [json.loads(l) for l in open(f)]
        if not rows:
            continue
        d = pd.DataFrame(rows)
        d["topic"] = d.topic.astype(str); d["pmid"] = d.pmid.astype(str)
        d = d.drop_duplicates(["topic", "pmid"], keep="last")
        parse.append(dict(lineage=name, rows=len(d), parsed=int(d.label.notna().sum())))
        out[name] = d[d.label.notna()][["topic", "pmid", "label"]]
    P = pd.DataFrame(parse)
    P["parse_rate"] = P.parsed / P.rows
    return out, P


def main():
    panel = pd.read_csv("panel_sample.csv", dtype={"topic": str, "pmid": str})
    lin, P = load_lineages()

    print("=== H-C1 · per-model STRICT parse rate (reported, never rescued) ===")
    print(P.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    low = P[P.parse_rate < 0.90]
    print("  below the 0.90 flag:", low.lineage.tolist() or "none")

    # ---- complete cases across every lineage present -----------------------------------
    M = panel[["topic", "pmid", "human", "stratum", "weight", "pool_size"]].copy()
    names = list(lin)
    for n in names:
        M = M.merge(lin[n].rename(columns={"label": n}), on=["topic", "pmid"], how="inner")
    print(f"\n복합 완전 사례: {len(M):,} / 패널 {len(panel):,} | 계보 {len(names)}: {names}")
    if len(M) < 500:
        print("  too few complete cases to analyse; stopping.")
        return

    # ---- H-M1 · per-lineage denominator bias -------------------------------------------
    q = pd.read_csv("clef2017_abs_test.qrels", sep=r"\s+", header=None,
                    names=["topic", "it", "pmid", "label"], dtype={"topic": str, "pmid": str})
    Rtrue = q[q.label > 0].groupby("topic").size()
    Npool = q.groupby("topic").size()

    rows = []
    for n in names:
        for t, g in M.groupby("topic"):
            if t not in Rtrue.index or Rtrue[t] == 0:
                continue
            # stratum-weighted reconstruction of the judge's eligible count over the pool
            R_llm = float((g.weight * (g[n] >= THR)).sum())
            R, N = int(Rtrue[t]), int(Npool[t])
            rows.append(dict(lineage=n, topic=t, N=N, R=R, p=R / N, R_llm=R_llm,
                             rel_bias=(R_llm - R) / R))
    B = pd.DataFrame(rows)
    print("\n=== H-M1 · denominator bias per lineage (registered: robust if >=5 of 6 positive; "
          "model-dependent if <=3 of 6) ===")
    S = (B.groupby("lineage")
           .agg(topics=("topic", "nunique"), median=("rel_bias", "median"),
                mean=("rel_bias", "mean"), over=("rel_bias", lambda s: int((s > 0).sum())),
                mx=("rel_bias", "max"))
           .sort_values("median"))
    print(S.to_string(float_format=lambda v: f"{v:+.3f}"))
    npos = int((S["median"] > 0).sum())
    print(f"  lineages with a POSITIVE median: {npos}/{len(S)}")
    print(f"  spread of the per-lineage medians: {S['median'].min():+.3f} .. {S['median'].max():+.3f} "
          f"(ratio {S['median'].max()/max(S['median'].min(), 1e-9):.1f}x)")

    # ---- H-D1 · cross-lineage independence ---------------------------------------------
    ne = M[M.human < 1]                     # human-non-eligible: where false positives live
    el = M[M.human >= 1]
    marg = {n: float((ne[n] >= THR).mean()) for n in names}
    sens = {n: float((el[n] >= THR).mean()) for n in names}
    print(f"\n=== H-D1 · cross-lineage independence "
          f"(non-eligible {len(ne):,} / eligible {len(el):,}) ===")
    print("  per-lineage false-positive rate (1-specificity) and sensitivity:")
    for n in names:
        print(f"    {n:26s} fp {marg[n]:.4f} | se {sens[n]:.4f}")

    res = []
    for k in range(2, len(names) + 1):
        for combo in itertools.combinations(names, k):
            obs = float(np.logical_and.reduce([(ne[c] >= THR).values for c in combo]).mean())
            ind = float(np.prod([marg[c] for c in combo]))
            se_and = float(np.logical_and.reduce([(el[c] >= THR).values for c in combo]).mean())
            res.append(dict(k=k, subset=" + ".join(x.split(" · ")[0] for x in combo),
                            fp_and=obs, fp_indep=ind,
                            dep=obs / ind if ind else np.nan, se_and=se_and,
                            best_single_fp=min(marg[c] for c in combo)))
    D = pd.DataFrame(res).sort_values(["k", "fp_and"])
    print("\n  AND-ensemble false-positive rate vs the independence prediction:")
    print(D.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    print(f"\n  registered OVERTURN condition: any fp_AND <= {TARGET_FP}")
    hit = D[D.fp_and <= TARGET_FP]
    if len(hit):
        print("  *** CONDITION MET — multiplicity DOES fix the denominator. "
              "The project's contrary conclusion is OVERTURNED. Subsets: ***")
        print(hit.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    else:
        print(f"  not met — the lowest AND-ensemble fp is {D.fp_and.min():.4f}, "
              f"{D.fp_and.min()/TARGET_FP:.1f}x above the threshold.")

    print("\n  does the dependence factor grow with k (i.e. do extra lineages stop buying)?")
    print(D.groupby("k").agg(dep_median=("dep", "median"), fp_median=("fp_and", "median"),
                             se_median=("se_and", "median"))
           .to_string(float_format=lambda v: f"{v:.4f}"))

    B.to_csv("panel_bias.csv", index=False)
    D.to_csv("panel_dependence.csv", index=False)
    P.to_csv("panel_parse_rates.csv", index=False)
    json.dump(dict(complete_cases=len(M), lineages=names, marginals=marg, sensitivity=sens,
                   overturn_met=bool(len(hit)), min_fp_and=float(D.fp_and.min()),
                   target_fp=TARGET_FP, n_positive_median=npos, n_lineages=len(S)),
              open("panel_summary.json", "w"), indent=1)
    print("\nwrote panel_bias.csv, panel_dependence.csv, panel_parse_rates.csv, panel_summary.json")


if __name__ == "__main__":
    main()

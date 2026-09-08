"""Analysis of the pre-registered CLEF census. Written BEFORE any census label was read.
The verdict lines are printed by this script, not decided after seeing the numbers.

Two bases are kept apart and never mixed:
  SAMPLE   the frozen 2,025-pair panel rows for these six topics - eligible stratum capped at
           40, non-eligible stratum exactly 40 per topic. This is the basis every earlier
           per-topic specificity in the project used.
  CENSUS   every document in the abstract-level judged pool for the topic.

A topic enters the comparison ONLY if its census is complete (every pool document carries a
strict label, whether reused from the panel run or produced now). Incomplete topics are listed
as not attempted and never averaged in.
"""
import glob, json, os, sys
import numpy as np
import pandas as pd
from scipy import stats

sys.path.append(os.getcwd())
from clefcensus_prereg import (TOPICS, SP_MATCH_TOL, SP_FAIL_TOL, N_MATCH_REQUIRED,
                               N_FAIL_TRIGGER, USABLE_BAND, BINARISE_AT)


def load_jsonl(pats):
    rows = []
    for p in pats:
        for f in sorted(glob.glob(p)):
            for ln in open(f):
                if ln.strip():
                    rows.append(json.loads(ln))
    if not rows:
        return pd.DataFrame(columns=["topic", "pmid", "label"])
    d = pd.DataFrame(rows)
    d["topic"] = d.topic.astype(str)
    d["pmid"] = d.pmid.astype(str)
    return d[d.label.notna()].drop_duplicates(["topic", "pmid"], keep="last")


def main():
    qa, hlab = {}, {}
    for ln in open("clef2017_abs_test.qrels"):
        f = ln.split()
        if len(f) >= 4 and f[0] in TOPICS:
            qa.setdefault(f[0], set()).add(f[2])
            hlab[(f[0], f[2])] = int(f[3])

    reused = load_jsonl(["opus_labels_C_slice*.jsonl"])
    fresh = load_jsonl(["census_labels_slice*.jsonl"])
    lab = pd.concat([reused, fresh]).drop_duplicates(["topic", "pmid"], keep="last")
    lab = lab[lab.topic.isin(TOPICS)]
    L = {(r.topic, r.pmid): int(r.label) for r in lab.itertuples()}
    print(f"labels available for these six topics: {len(L):,} "
          f"(reused {len(reused[reused.topic.isin(TOPICS)]):,}, fresh {len(fresh):,})", flush=True)

    complete, incomplete, rows = [], [], []
    for t in TOPICS:
        pool = qa.get(t, set())
        got = {d for d in pool if (t, d) in L}
        if len(got) < len(pool):
            incomplete.append((t, len(pool) - len(got)))
            continue
        complete.append(t)
        N = len(pool)
        el = [d for d in pool if hlab[(t, d)] >= 1]
        ne = [d for d in pool if hlab[(t, d)] < 1]
        R = len(el)
        se_c = np.mean([L[(t, d)] >= BINARISE_AT for d in el])
        sp_c = np.mean([L[(t, d)] < BINARISE_AT for d in ne])
        Rhat_c = R * se_c + (N - R) * (1 - sp_c)
        rows.append(dict(topic=t, N=N, R=R, p=R / N, se_census=se_c, sp_census=sp_c,
                         Rhat_census=Rhat_c, bias_census=(Rhat_c - R) / R,
                         n_nonelig=len(ne)))
    C = pd.DataFrame(rows)

    print(f"\ncomplete censuses: {len(complete)}/{len(TOPICS)}  {complete}", flush=True)
    if incomplete:
        print(f"NOT attempted / incomplete (never averaged in): {incomplete}", flush=True)
    if not len(C):
        print("\nno complete census - nothing to analyse. STOP.", flush=True)
        return

    # sample-basis rates on the SAME topics, from the frozen panel
    PAN = pd.read_csv("panel_sample.csv", dtype={"topic": str, "pmid": str})
    PAN = PAN[PAN.topic.isin(complete)]
    srows = []
    for t, g in PAN.groupby("topic"):
        el, ne = g[g.human >= 1], g[g.human < 1]
        gl = [(r.topic, r.pmid) for r in g.itertuples()]
        if not all(k in L for k in gl):
            srows.append(dict(topic=t, se_sample=np.nan, sp_sample=np.nan,
                              n_ne_sample=len(ne)))
            continue
        se_s = np.mean([L[(t, r.pmid)] >= BINARISE_AT for r in el.itertuples()])
        sp_s = np.mean([L[(t, r.pmid)] < BINARISE_AT for r in ne.itertuples()])
        srows.append(dict(topic=t, se_sample=se_s, sp_sample=sp_s, n_ne_sample=len(ne)))
    S = pd.DataFrame(srows)
    M = C.merge(S, on="topic")
    M["d_sp"] = (M.sp_sample - M.sp_census).abs()
    M["d_se"] = (M.se_sample - M.se_census).abs()
    Nn, Rr = M.N, M.R
    M["Rhat_sample"] = Rr * M.se_sample + (Nn - Rr) * (1 - M.sp_sample)
    M["bias_sample"] = (M.Rhat_sample - Rr) / Rr
    M["usable_census"] = M.bias_census.abs() <= USABLE_BAND
    M["usable_sample"] = M.bias_sample.abs() <= USABLE_BAND

    print("\n=== X1 : sampled specificity vs population specificity ===", flush=True)
    print(M[["topic", "N", "R", "p", "n_ne_sample", "n_nonelig", "sp_sample", "sp_census",
             "d_sp", "se_sample", "se_census"]].round(4).to_string(index=False), flush=True)
    n_match = int((M.d_sp <= SP_MATCH_TOL).sum())
    n_fail = int((M.d_sp > SP_FAIL_TOL).sum())
    print(f"\n  topics with |sp_sample - sp_census| <= {SP_MATCH_TOL}: {n_match}/{len(M)} "
          f"(need >= {N_MATCH_REQUIRED} of 6 to validate)", flush=True)
    print(f"  topics with |sp_sample - sp_census| >  {SP_FAIL_TOL}: {n_fail}/{len(M)} "
          f"(>= {N_FAIL_TRIGGER} triggers NOT VALIDATED)", flush=True)
    print(f"  median |d_sp| = {M.d_sp.median():.4f} | max = {M.d_sp.max():.4f}", flush=True)
    if len(M) < len(TOPICS):
        print(f"  NOTE: only {len(M)} of 6 topics complete, so the registered counts "
              f"({N_MATCH_REQUIRED}/6 and {N_FAIL_TRIGGER}/6) cannot be evaluated as written; "
              f"reporting the observed counts and withholding the verdict.", flush=True)
        verdict = "INCONCLUSIVE - census incomplete"
    elif n_match >= N_MATCH_REQUIRED:
        verdict = "APPARATUS VALIDATED"
    elif n_fail >= N_FAIL_TRIGGER:
        verdict = "APPARATUS NOT VALIDATED - withdraw per-topic sampled point estimates"
    else:
        verdict = "PARTIAL - no promotion either way"
    print(f"  VERDICT: {verdict}", flush=True)

    print("\n=== X2 : does the usability verdict change ===", flush=True)
    print(M[["topic", "p", "bias_sample", "bias_census", "usable_sample",
             "usable_census"]].round(4).to_string(index=False), flush=True)
    flip = int((M.usable_sample != M.usable_census).sum())
    print(f"  topics whose verdict flips: {flip}/{len(M)}", flush=True)
    print(f"  usable under census: {int(M.usable_census.sum())}/{len(M)} | "
          f"under sample: {int(M.usable_sample.sum())}/{len(M)}", flush=True)

    print("\n=== X3 : bias vs prevalence at census (DESCRIPTIVE ONLY, n is tiny) ===", flush=True)
    if len(M) >= 3:
        rs = stats.spearmanr(M.p, M.bias_census)
        print(f"  Spearman rho(p, bias_census) = {rs.statistic:+.3f} (p = {rs.pvalue:.3f}) "
              f"over {len(M)} topics", flush=True)
        print(f"  for comparison, the 30-topic SAMPLED value is -0.688 (p = 2.6e-5)", flush=True)
        print(f"  {len(M)} points cannot support inference; reported as descriptive.", flush=True)
    else:
        print(f"  only {len(M)} topics - not reported.", flush=True)

    M.to_csv("census_clef_results.csv", index=False)
    json.dump({"verdict_X1": verdict, "n_complete": len(complete),
               "complete": complete, "incomplete": [t for t, _ in incomplete],
               "n_match": n_match, "n_fail": n_fail,
               "median_d_sp": float(M.d_sp.median()), "max_d_sp": float(M.d_sp.max()),
               "verdict_flips": flip,
               "usable_census": int(M.usable_census.sum()),
               "usable_sample": int(M.usable_sample.sum())},
              open("census_clef_results.json", "w"), indent=1, default=float)
    print("\nwrote census_clef_results.csv, census_clef_results.json", flush=True)


if __name__ == "__main__":
    main()

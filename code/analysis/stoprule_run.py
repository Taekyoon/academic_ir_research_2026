"""Runs the three pre-registered measurements in stoprule_prereg.py.
Verdict lines are printed by this script, not decided after seeing the numbers.
"""
import csv, json, os, statistics as st, sys
from collections import defaultdict

sys.path.append(os.getcwd())
from ndcg_scope_run import fetch_runs
from bpref_run import kendall_tau
from stoprule_prereg import (TARGET_RECALL, D_CONTRACT_BROKEN, D_CONTRACT_SURVIVES,
                             WSS_TARGET, ARM, E3_ALPHA)


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    rho = num / den if den else float("nan")
    if n > 2 and abs(rho) < 1:
        t = rho * ((n - 2) / (1 - rho ** 2)) ** 0.5
        # two-sided p from a t distribution, series-free normal approximation for n=27
        import math
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(t) / (2 ** 0.5))))
    else:
        p = float("nan")
    return rho, p


def load_qrels(path):
    q = defaultdict(dict)
    for ln in open(path):
        f = ln.split()
        if len(f) >= 4:
            q[f[0]][f[2]] = int(f[3])
    return dict(q)


def main():
    qrels = load_qrels("clef2017_abs_test.qrels")
    N = {t: len(v) for t, v in qrels.items()}
    R = {t: sum(1 for x in v.values() if x >= 1) for t, v in qrels.items()}

    rows = list(csv.DictReader(open("arm_rates.csv")))
    se = float(rows[0]["se"]); sp = float(rows[0]["sp"])
    print(f"judge rates ({ARM}, 30-topic pooled): se {se:.4f} sp {sp:.4f}", flush=True)
    Rhat = {t: R[t] * se + (N[t] - R[t]) * (1 - sp) for t in qrels}

    runs = fetch_runs()
    print(f"runs: {len(runs)} | topics in qrels: {len(qrels)}", flush=True)

    # ---------- E1 ----------
    recs = []
    for name, run in runs.items():
        for t, docs in run.items():
            if t not in qrels or R[t] == 0:
                continue
            found = 0
            hit_ctrl = hit_trt = None
            for k, d in enumerate(docs, 1):
                if qrels[t].get(d, 0) >= 1:
                    found += 1
                if hit_ctrl is None and found / R[t] >= TARGET_RECALL:
                    hit_ctrl = (k, found / R[t])
                if hit_trt is None and found / Rhat[t] >= TARGET_RECALL:
                    hit_trt = (k, found / R[t])
                if hit_ctrl and hit_trt:
                    break
            recs.append(dict(run=name, topic=t, depth=len(docs), N=N[t], R=R[t], Rhat=Rhat[t],
                             fired_ctrl=hit_ctrl is not None, fired_trt=hit_trt is not None,
                             k_ctrl=hit_ctrl[0] if hit_ctrl else None,
                             k_trt=hit_trt[0] if hit_trt else None,
                             rel_ctrl=hit_ctrl[1] if hit_ctrl else None,
                             rel_trt=hit_trt[1] if hit_trt else None))
    with open("stoprule_pairs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0]))
        w.writeheader(); w.writerows(recs)

    both = [r for r in recs if r["fired_ctrl"] and r["fired_trt"]]
    print(f"\n=== E1 target-recall rule at {TARGET_RECALL} on real reading orders ===", flush=True)
    print(f"  run-topic pairs: {len(recs)}", flush=True)
    print(f"  fired under TRUE R:  {sum(r['fired_ctrl'] for r in recs)}/{len(recs)}"
          f"  ({sum(r['fired_ctrl'] for r in recs)/len(recs):.1%})", flush=True)
    print(f"  fired under JUDGE R-hat: {sum(r['fired_trt'] for r in recs)}/{len(recs)}"
          f"  ({sum(r['fired_trt'] for r in recs)/len(recs):.1%})", flush=True)
    print(f"  both fired: {len(both)}", flush=True)
    if both:
        dr = [r["rel_ctrl"] - r["rel_trt"] for r in both]
        dk = [r["k_ctrl"] - r["k_trt"] for r in both]
        md = st.median(dr)
        print(f"  TRUE recall at stop  - control median {st.median([r['rel_ctrl'] for r in both]):.3f}"
              f" | treatment median {st.median([r['rel_trt'] for r in both]):.3f}", flush=True)
        print(f"  paired reliability loss: median {md:+.3f} | "
              f"q25 {st.quantiles(dr, n=4)[0]:+.3f} q75 {st.quantiles(dr, n=4)[2]:+.3f}", flush=True)
        print(f"  cost at stop (documents): control median {st.median([r['k_ctrl'] for r in both]):.0f}"
              f" | treatment median {st.median([r['k_trt'] for r in both]):.0f}"
              f" | paired median {st.median(dk):+.0f}", flush=True)
        v = ("CONTRACT BROKEN" if md >= D_CONTRACT_BROKEN else
             "CONTRACT SURVIVES" if md <= D_CONTRACT_SURVIVES else "PARTIAL")
        print(f"  thresholds: >= {D_CONTRACT_BROKEN} broken | <= {D_CONTRACT_SURVIVES} survives",
              flush=True)
        print(f"  VERDICT: {v}", flush=True)
    else:
        md, v = float("nan"), "NO PAIRS - both conditions never fire together"
        print(f"  VERDICT: {v}", flush=True)

    # ---------- E2 ----------
    def wss(run, denom):
        out = {}
        for t, docs in run.items():
            if t not in qrels or R[t] == 0:
                continue
            found, k_hit = 0, None
            for k, d in enumerate(docs, 1):
                if qrels[t].get(d, 0) >= 1:
                    found += 1
                if found / denom[t] >= WSS_TARGET:
                    k_hit = k
                    break
            out[t] = 1 - (k_hit if k_hit else N[t]) / N[t]
        return st.mean(out.values()) if out else float("nan")

    wc = {n: wss(r, R) for n, r in runs.items()}
    wt = {n: wss(r, Rhat) for n, r in runs.items()}
    tau_w = kendall_tau(wc, wt)
    print(f"\n=== E2 wss_{int(WSS_TARGET*100)} under the two denominators ===", flush=True)
    print(f"  mean wss - true R {st.mean(wc.values()):.4f} | judge R-hat {st.mean(wt.values()):.4f}",
          flush=True)
    print(f"  Kendall tau of the {len(wc)}-run ranking: {tau_w:+.3f}", flush=True)
    print(f"  (for comparison, the recall tau already reported is +0.649 at depth 500)", flush=True)

    # ---------- E3 ----------
    def rank_of(scores):
        order = sorted(scores, key=lambda n: -scores[n])
        return {n: i + 1 for i, n in enumerate(order)}
    rec_c, rec_t = {}, {}
    for n, run in runs.items():
        vc = vt = 0.0
        cnt = 0
        for t, docs in run.items():
            if t not in qrels or R[t] == 0:
                continue
            found = sum(1 for d in docs if qrels[t].get(d, 0) >= 1)
            vc += found / R[t]; vt += found / Rhat[t]; cnt += 1
        if cnt:
            rec_c[n], rec_t[n] = vc / cnt, vt / cnt
    rc, rt = rank_of(rec_c), rank_of(rec_t)
    names = sorted(rc)
    depth = {n: sum(len(v) for t, v in runs[n].items() if t in qrels) for n in names}
    chg = {n: rc[n] - rt[n] for n in names}
    rho, p = spearman([depth[n] for n in names], [chg[n] for n in names])
    print(f"\n=== E3 is depth rewarded by a judge denominator ===", flush=True)
    print(f"  runs {len(names)} | depth min {min(depth.values()):,} max {max(depth.values()):,}",
          flush=True)
    print(f"  Spearman rho(depth, rank improvement under judge) = {rho:+.3f} (p = {p:.3g})",
          flush=True)
    print(f"  registered: rho > 0 with p < {E3_ALPHA} confirms the mechanism", flush=True)
    print(f"  VERDICT: {'MECHANISM CONFIRMED' if (rho > 0 and p < E3_ALPHA) else 'NOT CONFIRMED - remove the depth sentence'}",
          flush=True)

    with open("stoprule_runs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "depth", "recall_trueR", "recall_judgeRhat", "rank_trueR",
                    "rank_judgeRhat", "rank_improvement", "wss95_trueR", "wss95_judgeRhat"])
        for n in names:
            w.writerow([n, depth[n], round(rec_c[n], 4), round(rec_t[n], 4), rc[n], rt[n],
                        chg[n], round(wc[n], 4), round(wt[n], 4)])

    json.dump({"se": se, "sp": sp, "n_pairs": len(recs), "n_both": len(both),
               "fire_ctrl": sum(r["fired_ctrl"] for r in recs),
               "fire_trt": sum(r["fired_trt"] for r in recs),
               "e1_median_reliability_loss": md, "e1_verdict": v,
               "e2_tau_wss": tau_w, "e2_mean_wss_true": st.mean(wc.values()),
               "e2_mean_wss_judge": st.mean(wt.values()),
               "e3_rho": rho, "e3_p": p},
              open("stoprule_results.json", "w"), indent=1, default=float)
    print("\nwrote stoprule_pairs.csv, stoprule_runs.csv, stoprule_results.json", flush=True)


if __name__ == "__main__":
    main()

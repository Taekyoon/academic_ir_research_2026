"""Runs the pre-registered controlled test in synthjudge_prereg.py. Verdicts printed by code."""
import itertools, json, os, random, urllib.parse, urllib.request
from collections import defaultdict

import pytrec_eval
from synthjudge_prereg import (SE_GRID, SP_GRID, DRAWS, SEED, D_THRESHOLD,
                               SP_RELEVANT_MAX, RANKDEP)

API = "https://api.github.com/repos/CLEF-TAR/tar/git/trees/master?recursive=1"
RAW = "https://raw.githubusercontent.com/CLEF-TAR/tar/master/"
MAX_RUNS_PER_TEAM = 2
MEAS = {"bpref", "recall_1000"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "*/*"}),
                                timeout=180) as r:
        return r.read()


def parse_run(text):
    order, seen = defaultdict(list), defaultdict(set)
    for ln in text.splitlines():
        p = ln.split()
        if len(p) < 3:
            continue
        t, d = p[0], p[2]
        if d in seen[t]:
            continue
        seen[t].add(d)
        order[t].append(d)
    return dict(order)


def load_pool_qrels(path):
    """CLEF qrels: topic 0 pmid label. Returns topic -> pmid -> 0/1 over the WHOLE pool."""
    q = defaultdict(dict)
    for ln in open(path):
        p = ln.split()
        if len(p) < 4:
            continue
        q[p[0]][p[2]] = 1 if int(p[3]) >= 1 else 0
    return dict(q)


def flip(human, se, sp, rng, rank_sets=None):
    """Simulated judge. rank_sets: topic -> set(docid in some run's top-k), for the
    rank-dependent condition; when given, non-eligible docs inside it flip at a higher rate."""
    out = {}
    for t, dd in human.items():
        o = {}
        hi = rank_sets.get(t, set()) if rank_sets else set()
        for d, v in dd.items():
            if v == 1:
                o[d] = 1 if rng.random() < se else 0
            else:
                fp = (RANKDEP["top100_fp"] if d in hi else RANKDEP["elsewhere_fp"]) \
                     if rank_sets else (1.0 - sp)
                o[d] = 1 if rng.random() < fp else 0
        out[t] = o
    return out


def score(qrels, runs):
    ev = pytrec_eval.RelevanceEvaluator(
        {t: dd for t, dd in qrels.items() if any(dd.values())}, MEAS)
    out = {}
    for name, order in runs.items():
        run = {t: {d: float(len(ds) - i) for i, d in enumerate(ds)}
               for t, ds in order.items() if t in qrels}
        res = ev.evaluate(run)
        if not res:
            continue
        out[name] = {m: sum(v.get(m, 0.0) for v in res.values()) / len(res) for m in MEAS}
    return out


def kendall_tau(a, b):
    ks = [k for k in a if k in b]
    conc = disc = 0
    for i, j in itertools.combinations(range(len(ks)), 2):
        x, y = a[ks[i]] - a[ks[j]], b[ks[i]] - b[ks[j]]
        if x == 0 or y == 0:
            continue
        if (x > 0) == (y > 0):
            conc += 1
        else:
            disc += 1
    return (conc - disc) / (conc + disc) if (conc + disc) else float("nan")


def main():
    human = load_pool_qrels("clef2017_abs_test.qrels")
    ps = []
    for t, dd in human.items():
        n, r = len(dd), sum(dd.values())
        if r:
            ps.append(r / n)
    ps.sort()
    print(f"pool: {len(human)} topics | docs {sum(len(v) for v in human.values()):,} | "
          f"eligible {sum(sum(v.values()) for v in human.values()):,} | "
          f"prevalence median {ps[len(ps)//2]:.4f} min {ps[0]:.5f} max {ps[-1]:.4f}", flush=True)

    tree = json.loads(get(API))["tree"]
    cand = defaultdict(list)
    for n in tree:
        p = n["path"]
        if (p.startswith("2017-TAR/participant-runs/") and n["type"] == "blob"
                and n.get("size", 0) >= 200_000
                and not os.path.basename(p).lower().startswith(("icon", "readme"))):
            cand[p.split("/")[2]].append(p)
    runs = {}
    for team, paths in sorted(cand.items()):
        for p in sorted(paths)[:MAX_RUNS_PER_TEAM]:
            try:
                o = parse_run(get(RAW + urllib.parse.quote(p)).decode("utf-8", "replace"))
            except Exception as e:
                print(f"  SKIP {p}: {type(e).__name__}", flush=True)
                continue
            # FORMAT GUARD, added after an audit. AMC/clef-finals/PROBABILITIES_1.rds is an R
            # binary; the whitespace parser turned it into 2,680 spurious "topics" and it passed
            # a bare len(o) >= 20 check. It was harmless to the grid (pytrec_eval scores only
            # topics present in the qrels, so it produced no score and was dropped, leaving 27
            # scored runs) but it was alphabetically first and so became the reference run for
            # the rank-dependent condition, whose top-k sets were therefore all empty - turning
            # that condition into a uniform fp run by accident. Require real CLEF topic ids.
            real = sum(1 for t in o if t.startswith("CD") and len(t) <= 10)
            if real >= 20:
                runs[f"{team}/{os.path.basename(p)}"] = o
            elif len(o) >= 20:
                print(f"  REJECT {p}: {len(o)} parsed topics but {real} valid CLEF ids "
                      f"- not a TREC run file", flush=True)
    print(f"runs: {len(runs)}", flush=True)

    base = score(human, runs)
    print(f"human qrels: mean bpref {sum(v['bpref'] for v in base.values())/len(base):.4f} | "
          f"mean recall {sum(v['recall_1000'] for v in base.values())/len(base):.4f}", flush=True)
    bb = {k: v["bpref"] for k, v in base.items()}
    br = {k: v["recall_1000"] for k, v in base.items()}

    rng = random.Random(SEED)
    cells = []
    print(f"\n{'se':>5s} {'sp':>5s} {'tau_bpref':>10s} {'tau_recall':>11s} {'d=b-r':>8s} "
          f"{'R_ratio':>8s}", flush=True)
    for se, sp in itertools.product(SE_GRID, SP_GRID):
        tb, tr, rr = [], [], []
        for _ in range(DRAWS):
            q = flip(human, se, sp, rng)
            s = score(q, runs)
            tb.append(kendall_tau(bb, {k: v["bpref"] for k, v in s.items()}))
            tr.append(kendall_tau(br, {k: v["recall_1000"] for k, v in s.items()}))
            nh = sum(sum(v.values()) for v in human.values())
            nj = sum(sum(v.values()) for v in q.values())
            rr.append(nj / nh)
            if se == 1.0 and sp == 1.0:
                break
        m = lambda x: sum(x) / len(x)
        cells.append(dict(se=se, sp=sp, tau_bpref=m(tb), tau_recall=m(tr),
                          d=m(tb) - m(tr), R_ratio=m(rr), draws=len(tb)))
        print(f"{se:>5.2f} {sp:>5.2f} {m(tb):>+10.3f} {m(tr):>+11.3f} "
              f"{m(tb)-m(tr):>+8.3f} {m(rr):>8.2f}", flush=True)

    g1 = [c for c in cells if c["se"] == 1.0 and c["sp"] == 1.0][0]
    print(f"\nGUARD G1 (se=1, sp=1 must reproduce human): tau_bpref {g1['tau_bpref']:+.4f} "
          f"tau_recall {g1['tau_recall']:+.4f} R_ratio {g1['R_ratio']:.4f}", flush=True)
    if abs(g1["tau_bpref"] - 1) > 1e-6 or abs(g1["tau_recall"] - 1) > 1e-6:
        print("  G1 FAILED - harness broken, no result may be read", flush=True)

    rel = [c["d"] for c in cells if c["sp"] <= SP_RELEVANT_MAX]
    rel.sort()
    md = rel[len(rel)//2]
    print(f"\nQ1 over {len(rel)} cells with sp <= {SP_RELEVANT_MAX}: median d = {md:+.3f}",
          flush=True)
    if md >= D_THRESHOLD:
        v1 = "SUPPORTED - bpref protects the ranking relative to recall"
    elif md <= -D_THRESHOLD:
        v1 = "REFUTED - bpref is MORE disturbed than recall"
    else:
        v1 = "NO PROTECTION - the two metrics are equally disturbed (not support)"
    print(f"  VERDICT Q1: {v1}", flush=True)

    print(f"\nQ2 - which rate drives which metric", flush=True)
    for lab, key, other in (("sweep se at fixed sp", "se", "sp"), ("sweep sp at fixed se", "sp", "se")):
        for metric in ("tau_bpref", "tau_recall"):
            rngs = []
            for fixed in (SP_GRID if other == "sp" else SE_GRID):
                vs = [c[metric] for c in cells if c[other] == fixed]
                if len(vs) > 1:
                    rngs.append(max(vs) - min(vs))
            if rngs:
                print(f"  {lab:22s} {metric:11s} mean induced range "
                      f"{sum(rngs)/len(rngs):.3f}", flush=True)

    # rank-dependent condition, reported separately
    # reference run = the deepest real run, so top-k is a genuine ranking rather than whatever
    # sorts first alphabetically. Asserted non-empty because an empty top-k silently degrades
    # this condition into a uniform-fp condition, which is exactly the bug the audit found.
    ref = max((r for r in runs if any(t in human for t in runs[r])),
              key=lambda r: sum(len(v) for t, v in runs[r].items() if t in human))
    top = {t: set(ds[:RANKDEP["top_k"]]) for t, ds in runs[ref].items() if t in human}
    cov = sum(len(v) for v in top.values())
    assert cov >= 20 * RANKDEP["top_k"] * 0.5, (
        f"reference run {ref} gives only {cov} top-k documents over {len(top)} topics; "
        "the rank-dependent condition would collapse to uniform fp")
    print(f"\nrank-dependent reference run: {ref} | topics {len(top)} | "
          f"top-{RANKDEP['top_k']} documents {cov:,}", flush=True)
    tb, tr = [], []
    for _ in range(DRAWS):
        q = flip(human, 0.80, None, rng, rank_sets=top)
        s = score(q, runs)
        tb.append(kendall_tau(bb, {k: v["bpref"] for k, v in s.items()}))
        tr.append(kendall_tau(br, {k: v["recall_1000"] for k, v in s.items()}))
    print(f"\nrank-dependent errors (se 0.80, fp {RANKDEP['top100_fp']} in {ref} top-"
          f"{RANKDEP['top_k']}, {RANKDEP['elsewhere_fp']} elsewhere):", flush=True)
    print(f"  tau_bpref {sum(tb)/len(tb):+.3f} | tau_recall {sum(tr)/len(tr):+.3f} | "
          f"d {sum(tb)/len(tb) - sum(tr)/len(tr):+.3f}", flush=True)

    json.dump({"n_runs": len(runs), "n_topics": len(human),
               "prevalence_median": ps[len(ps)//2], "cells": cells,
               "guard_g1": g1, "q1_median_d": md, "q1_verdict": v1,
               "rankdep": {"tau_bpref": sum(tb)/len(tb), "tau_recall": sum(tr)/len(tr),
                           "reference_run": ref}},
              open("synthjudge_results.json", "w"), indent=1, default=float)
    print("\nwrote synthjudge_results.json", flush=True)


if __name__ == "__main__":
    main()

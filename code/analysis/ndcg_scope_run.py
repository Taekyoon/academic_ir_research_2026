"""Runs the pre-registered scope test in ndcg_scope_prereg.py. Verdicts printed by this script.

Reuses bpref_run.py's universe loader and run fetcher so the document set, the topics and the
27 participant runs are bit-identical to the bpref experiment, making the taus comparable.
"""
import json, os, random, statistics as st, sys, urllib.parse
from collections import defaultdict

import pytrec_eval
sys.path.append(os.getcwd())
from bpref_run import load_universe, kendall_tau, get, parse_run, API, RAW, MAX_RUNS_PER_TEAM
from ndcg_scope_prereg import (D_SCOPE_TO_RECALL, D_REACHES_NDCG, CUTOFFS, BINARISE_AT,
                               DELETION_RATES, DELETION_DRAWS, SEED)


def fetch_runs():
    """Same fetch as bpref_run.main(), plus the format guard added later in synthjudge_run.py.
    AMC/clef-finals/PROBABILITIES_1.rds is an R binary that a whitespace parser reads as
    thousands of spurious topics and that a bare len>=20 check admits; it scores nothing (so the
    bpref run's 27 scored runs were unaffected) but it must not enter the run set."""
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
            real = sum(1 for t in o if t.startswith("CD") and len(t) <= 10)
            if real >= 20:
                runs[f"{team}/{os.path.basename(p)}"] = o
            elif len(o) >= 20:
                print(f"  REJECT {p}: {len(o)} parsed topics but {real} valid CLEF ids", flush=True)
    return runs

MEAS = {"bpref", "recall_1000"} | {f"ndcg_cut_{k}" for k in CUTOFFS} | {"ndcg"}


def score(qrels, runs, measures):
    ev = pytrec_eval.RelevanceEvaluator(qrels, measures)
    out = {}
    for name, run in runs.items():
        rr = {t: {d: float(len(ds) - i) for i, d in enumerate(ds)}
              for t, ds in run.items() if t in qrels}
        if not rr:
            continue
        res = ev.evaluate(rr)
        if not res:
            continue
        out[name] = {m: st.mean(v[m] for v in res.values() if m in v)
                     for m in next(iter(res.values()))}
    return out


def main():
    report = {"universes": {}}
    runs = fetch_runs()
    print(f"runs fetched: {len(runs)}", flush=True)

    for U in ("A", "B"):
        docs, human, judges = load_universe(U)
        n_docs = sum(len(v) for v in docs.values())
        print(f"\n{'='*72}\nUNIVERSE {U}: {len(docs)} topics, {n_docs} judged documents, "
              f"arms {sorted(judges)}", flush=True)

        qh = {t: {d: int(v) for d, v in human[t].items()} for t in human}
        sh = score(qh, runs, MEAS)
        scored = sorted(sh)
        print(f"  scored runs: {len(scored)}", flush=True)

        rows = {}
        for arm, lab in judges.items():
            # BINARY variant: judge grades already binarised at BINARISE_AT by the loader
            qb = {t: {d: int(lab[t].get(d, 0)) for d in docs[t]} for t in docs}
            sb = score(qb, runs, MEAS)
            rows[f"J:{arm}:binary"] = {
                m: kendall_tau({r: sh[r][m] for r in scored if r in sb},
                               {r: sb[r][m] for r in scored if r in sb})
                for m in MEAS}

        # deletion control, averaged over draws, for the same measures
        rng = random.Random(SEED)
        dele = {}
        for rate in DELETION_RATES:
            taus = []
            for _ in range(DELETION_DRAWS):
                qd = {}
                for t in qh:
                    keep = {d: v for d, v in qh[t].items() if rng.random() >= rate}
                    if keep:
                        qd[t] = keep
                sd = score(qd, runs, MEAS)
                taus.append({m: kendall_tau({r: sh[r][m] for r in scored if r in sd},
                                            {r: sd[r][m] for r in scored if r in sd})
                             for m in MEAS})
            dele[f"D{int(rate*100)}"] = {m: st.mean(x[m] for x in taus) for m in MEAS}

        print(f"\n  {'condition':26s}" + "".join(f"{m:>16s}" for m in
              ("recall_1000", "bpref", "ndcg", "ndcg_cut_10", "ndcg_cut_1000")), flush=True)
        for k, v in list(rows.items()) + list(dele.items()):
            print(f"  {k:26s}" + "".join(f"{v[m]:>16.3f}" for m in
                  ("recall_1000", "bpref", "ndcg", "ndcg_cut_10", "ndcg_cut_1000")), flush=True)

        # registered decision, primary variant, judge arms only
        ds = []
        for k, v in rows.items():
            for kk in CUTOFFS:
                ds.append(v[f"ndcg_cut_{kk}"] - v["recall_1000"])
        md = st.median(ds)
        if md >= D_SCOPE_TO_RECALL:
            verdict = "SCOPE TO RECALL-FAMILY - nDCG is materially more robust"
        elif md <= D_REACHES_NDCG:
            verdict = "REACHES nDCG TOO - the claim generalises to ranking measures"
        else:
            verdict = "PARTIAL - scope the abstract to recall-family, state nDCG is only partly protected"
        print(f"\n  median d = tau(nDCG@k) - tau(recall) over {len(ds)} arm-cutoff pairs: {md:+.3f}",
              flush=True)
        print(f"  thresholds: >= {D_SCOPE_TO_RECALL} scope to recall | <= {D_REACHES_NDCG} reaches nDCG",
              flush=True)
        print(f"  VERDICT (universe {U}): {verdict}", flush=True)

        report["universes"][U] = {"n_topics": len(docs), "n_docs": n_docs,
                                  "n_runs_scored": len(scored),
                                  "human": {r: sh[r] for r in scored},
                                  "judge": rows, "deletion": dele,
                                  "median_d": md, "verdict": verdict}

    json.dump(report, open("ndcg_scope_results.json", "w"), indent=1, default=float)
    print("\nwrote ndcg_scope_results.json", flush=True)


if __name__ == "__main__":
    main()

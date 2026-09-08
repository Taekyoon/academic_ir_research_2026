"""Runs the pre-registered test in bpref_prereg.py. Verdict lines are printed by this script.

Fetches the CLEF 2017 participant runs from the public CLEF-TAR repository, builds one qrels per
label condition over a fixed judged document set, and scores every run with pytrec_eval so the
bpref values are trec_eval's own rather than a local reimplementation.
"""
import csv, glob, itertools, json, math, os, urllib.request
from collections import defaultdict

import pytrec_eval
from bpref_prereg import (TAU_WITHDRAW, TAU_GAP_REQUIRED, GUARD_D50_MIN,
                          DELETION_RATES, DELETION_DRAWS, SEED, BINARISE_AT)
import random

API = ("https://api.github.com/repos/CLEF-TAR/tar/git/trees/master?recursive=1")
RAW = "https://raw.githubusercontent.com/CLEF-TAR/tar/master/"
MAX_RUNS_PER_TEAM = 2


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def parse_run(text):
    """TREC run format: topic Q0 docid rank score tag. Keep first occurrence order per topic."""
    order = defaultdict(list)
    seen = defaultdict(set)
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


def load_universe(which):
    """Return (docs, human, judges) where docs is topic -> set(pmid),
    human is topic -> pmid -> 0/1, judges is armname -> topic -> pmid -> 0/1."""
    if which == "A":
        rows = list(csv.DictReader(open("clef_judge_sample.csv")))
        docs, human = defaultdict(set), defaultdict(dict)
        for r in rows:
            t, d = str(r["topic"]), str(r["pmid"])
            docs[t].add(d)
            human[t][d] = 1 if int(r["human"]) >= 1 else 0
        arms = {"gpt-4o-mini_A": ["clef_labels_gpt-4o-mini_A.jsonl"]}
    else:
        rows = list(csv.DictReader(open("panel_sample.csv")))
        docs, human = defaultdict(set), defaultdict(dict)
        for r in rows:
            t, d = str(r["topic"]), str(r["pmid"])
            docs[t].add(d)
            human[t][d] = 1 if int(r["human"]) >= 1 else 0
        arms = {"opus_C": ["opus_labels_C_slice*.jsonl"],
                "haiku_A": ["panel_labels_haiku_slice*.jsonl",
                            "panel_labels_claude-haiku-4-5.jsonl"]}

    judges = {}
    for arm, pats in arms.items():
        lab = defaultdict(dict)
        for pat in pats:
            for f in sorted(glob.glob(pat)):
                for ln in open(f):
                    if not ln.strip():
                        continue
                    r = json.loads(ln)
                    if r.get("label") is None:
                        continue
                    t, d = str(r["topic"]), str(r["pmid"])
                    if d in docs[t]:
                        lab[t][d] = 1 if int(r["label"]) >= BINARISE_AT else 0
        judges[arm] = dict(lab)
    return dict(docs), dict(human), judges


def score(qrels, runs, measures):
    ev = pytrec_eval.RelevanceEvaluator(
        {t: {d: int(v) for d, v in dd.items()} for t, dd in qrels.items() if any(dd.values())},
        measures)
    out = {}
    for name, order in runs.items():
        run = {t: {d: float(len(ds) - i) for i, d in enumerate(ds)}
               for t, ds in order.items() if t in qrels}
        res = ev.evaluate(run)
        if not res:
            continue
        out[name] = {m: sum(v.get(m, 0.0) for v in res.values()) / len(res) for m in measures}
    return out


def kendall_tau(a, b):
    ks = [k for k in a if k in b]
    n = len(ks)
    if n < 2:
        return float("nan")
    conc = disc = 0
    for i, j in itertools.combinations(range(n), 2):
        x = (a[ks[i]] - a[ks[j]])
        y = (b[ks[i]] - b[ks[j]])
        if x == 0 or y == 0:
            continue
        if (x > 0) == (y > 0):
            conc += 1
        else:
            disc += 1
    tot = conc + disc
    return (conc - disc) / tot if tot else float("nan")


def main():
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
            if len(o) >= 20:
                runs[f"{team}/{os.path.basename(p)}"] = o
    print(f"runs fetched: {len(runs)} from {len(cand)} teams", flush=True)

    MEAS = {"bpref", "recall_1000"}
    report = {"n_runs": len(runs), "universes": {}}

    for U in ("A", "B"):
        docs, human, judges = load_universe(U)
        ndoc = sorted(len(v) for v in docs.values())
        print(f"\n{'='*78}\nUNIVERSE {U}: {len(docs)} topics, "
              f"{sum(len(v) for v in docs.values())} judged docs "
              f"(per topic min {ndoc[0]} median {ndoc[len(ndoc)//2]} max {ndoc[-1]})", flush=True)

        conds = {"H": human}
        for arm, lab in judges.items():
            conds[f"J:{arm}"] = lab
        rng = random.Random(SEED)
        for rate in DELETION_RATES:
            for draw in range(DELETION_DRAWS):
                kept = {}
                for t, dd in human.items():
                    ks = sorted(dd)
                    rng.shuffle(ks)
                    keep = ks[int(len(ks) * rate):]
                    kept[t] = {d: dd[d] for d in keep}
                conds[f"D{int(rate*100)}#{draw}"] = kept

        S = {c: score(q, runs, MEAS) for c, q in conds.items()}
        base = S["H"]
        rows = {}
        for c, sc in S.items():
            if c == "H":
                continue
            rows[c] = {
                "tau_bpref": kendall_tau({k: v["bpref"] for k, v in base.items()},
                                         {k: v["bpref"] for k, v in sc.items()}),
                "tau_recall": kendall_tau({k: v["recall_1000"] for k, v in base.items()},
                                          {k: v["recall_1000"] for k, v in sc.items()}),
                "mean_bpref": sum(v["bpref"] for v in sc.values()) / max(len(sc), 1),
                "n_scored": len(sc)}
        mb = sum(v["bpref"] for v in base.values()) / max(len(base), 1)
        print(f"  H: mean bpref {mb:.4f} over {len(base)} runs", flush=True)

        print(f"\n  {'condition':18s} {'tau(H,·) bpref':>15s} {'tau(H,·) recall':>16s} "
              f"{'mean bpref':>11s}", flush=True)
        for c in sorted(rows, key=lambda x: (x.startswith("D"), x)):
            r = rows[c]
            print(f"  {c:18s} {r['tau_bpref']:>+15.3f} {r['tau_recall']:>+16.3f} "
                  f"{r['mean_bpref']:>11.4f}", flush=True)

        # average the deletion draws
        dmean = {}
        for rate in DELETION_RATES:
            ks = [f"D{int(rate*100)}#{d}" for d in range(DELETION_DRAWS)]
            dmean[f"D{int(rate*100)}"] = sum(rows[k]["tau_bpref"] for k in ks) / len(ks)
        jt = {c: rows[c]["tau_bpref"] for c in rows if c.startswith("J:")}
        tau_J = min(jt.values())
        tau_D50 = dmean["D50"]
        print(f"\n  deletion control (mean of {DELETION_DRAWS} draws): " +
              "  ".join(f"{k} tau {v:+.3f}" for k, v in dmean.items()), flush=True)
        print(f"  judge conditions: " + "  ".join(f"{k} tau {v:+.3f}" for k, v in jt.items()),
              flush=True)
        print(f"  tau_J (worst judge arm) = {tau_J:+.3f} | tau_D50 = {tau_D50:+.3f} | "
              f"gap = {tau_D50 - tau_J:+.3f}", flush=True)

        if tau_D50 < GUARD_D50_MIN:
            verdict = "GUARD G1 - deletion control itself unstable, no conclusion"
        elif tau_J >= TAU_WITHDRAW:
            verdict = "W1 FIRED - CLAIM WITHDRAWN (bpref preserves the human ranking)"
        elif tau_J >= tau_D50:
            verdict = "W2 FIRED - CLAIM WITHDRAWN (error no worse than absence)"
        elif (tau_D50 - tau_J) >= TAU_GAP_REQUIRED:
            verdict = "S1 - CLAIM SUPPORTED (deletion tolerated, error not)"
        else:
            verdict = "AMBIGUOUS - no rewrite in either direction"
        print(f"\n  VERDICT (universe {U}): {verdict}", flush=True)
        report["universes"][U] = {"n_topics": len(docs),
                                  "n_docs": sum(len(v) for v in docs.values()),
                                  "mean_bpref_H": mb, "rows": rows,
                                  "deletion_mean": dmean, "tau_J": tau_J,
                                  "tau_D50": tau_D50, "verdict": verdict}

    json.dump(report, open("bpref_results.json", "w"), indent=1, default=float)
    print("\nwrote bpref_results.json", flush=True)


if __name__ == "__main__":
    main()

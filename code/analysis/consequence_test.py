"""Does the choice of denominator change which SYSTEM looks better?

Everything measured here is human-judged; no LLM judge is involved. CLEF TAR 2017 ships two
expert gold LEVELS over the same 30 topics and the same judged pool:
    D1  qrel_abs_test.txt      abstract screening passed   (1,857 eligible)
    D2  qrel_content_test.txt  full-text inclusion         (  607 included)
and the participant runs of 14 teams over that same pool are public. So we can re-score one
fixed set of real systems under two legitimate denominators and ask whether conclusions move.

This is the step that separates "the instrument is noisy" from "the noise changes decisions".
Reported both ways: aggregate ranking stability AND per-topic ranking stability, because the
project's thesis is precisely that the two can diverge.

Ranks are taken from ORDER OF APPEARANCE within a topic rather than a rank column, since team
file formats differ. Documents in a run that are absent from the qrels pool are kept in the
ranking (they cost depth) but can never be credited.
"""
import json, math, os, sys, time, urllib.request
from collections import defaultdict

RAW = "https://raw.githubusercontent.com/CLEF-TAR/tar/master/"
API = "https://api.github.com/repos/CLEF-TAR/tar/git/trees/master?recursive=1"
KS = [100, 500, 1000]
MAX_RUNS_PER_TEAM = 2          # keep the download polite and the comparison balanced


def get(url, tries=4, timeout=180):
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(3 * (a + 1))


def load_qrels(path):
    rel = defaultdict(set)
    pool = defaultdict(set)
    for ln in open(path):
        p = ln.split()
        if len(p) < 4:
            continue
        pool[p[0]].add(p[2])
        if p[3] != "0":
            rel[p[0]].add(p[2])
    return rel, pool


def list_runs():
    tree = json.loads(get(API))["tree"]
    cand = defaultdict(list)
    for n in tree:
        p = n["path"]
        if not p.startswith("2017-TAR/participant-runs/"):
            continue
        if n["type"] != "blob" or n.get("size", 0) < 200_000:
            continue
        if os.path.basename(p).lower().startswith(("icon", "readme")):
            continue
        team = p.split("/")[2]
        cand[team].append((p, n["size"]))
    sel = {}
    for team, files in cand.items():
        sel[team] = sorted(files)[:MAX_RUNS_PER_TEAM]
    return sel


def parse_run(text):
    """-> {topic: [docid in rank order]} keeping first occurrence only."""
    seen = defaultdict(set)
    order = defaultdict(list)
    for ln in text.splitlines():
        p = ln.split()
        if len(p) < 3:
            continue
        t = p[0]
        doc = next((f for f in p[1:] if f.isdigit() and len(f) >= 5), None)
        if doc is None or doc in seen[t]:
            continue
        seen[t].add(doc)
        order[t].append(doc)
    return order


def recall_at(order, rel, k):
    """per-topic recall@k, only for topics with at least one eligible doc"""
    out = {}
    for t, R in rel.items():
        if not R:
            continue
        got = len(set(order.get(t, [])[:k]) & R)
        out[t] = got / len(R)
    return out


def kendall_tau(a, b):
    """tau-b over the common keys of two dicts name -> score"""
    ks = sorted(set(a) & set(b))
    n = len(ks)
    if n < 3:
        return float("nan")
    conc = disc = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            da = a[ks[i]] - a[ks[j]]
            db = b[ks[i]] - b[ks[j]]
            if da == 0 and db == 0:
                tx += 1; ty += 1
            elif da == 0:
                tx += 1
            elif db == 0:
                ty += 1
            elif (da > 0) == (db > 0):
                conc += 1
            else:
                disc += 1
    n0 = n * (n - 1) / 2
    den = math.sqrt((n0 - tx) * (n0 - ty))
    return (conc - disc) / den if den else float("nan")


def main():
    rel1, pool1 = load_qrels("clef2017_abs_test.qrels")
    rel2, _ = load_qrels("clef2017_content_test.qrels")
    print(f"D1 abstract screening: {sum(len(v) for v in rel1.values()):,} eligible over "
          f"{sum(1 for v in rel1.values() if v)} topics", flush=True)
    print(f"D2 full-text inclusion: {sum(len(v) for v in rel2.values()):,} included over "
          f"{sum(1 for v in rel2.values() if v)} topics", flush=True)

    sel = list_runs()
    print(f"\nteams {len(sel)} | runs selected {sum(len(v) for v in sel.values())}", flush=True)
    per_run = {}
    for team, files in sorted(sel.items()):
        for path, size in files:
            name = f"{team}/{os.path.basename(path)}"
            try:
                txt = get(RAW + urllib.request.quote(path)).decode("utf-8", "replace")
            except Exception as e:
                print(f"  SKIP {name}: {type(e).__name__}", flush=True)
                continue
            order = parse_run(txt)
            if len(order) < 20:
                print(f"  SKIP {name}: only {len(order)} topics parsed", flush=True)
                continue
            per_run[name] = order
            print(f"  {name:44s} topics {len(order):3d}  "
                  f"median depth {sorted(len(v) for v in order.values())[len(order)//2]:>6,}",
                  flush=True)
    print(f"\nusable runs: {len(per_run)}", flush=True)

    res = {"runs": sorted(per_run), "aggregate": {}, "per_topic_tau": {}}
    for k in KS:
        agg1, agg2, pt1, pt2 = {}, {}, {}, {}
        for name, order in per_run.items():
            r1 = recall_at(order, rel1, k)
            r2 = recall_at(order, rel2, k)
            agg1[name] = sum(r1.values()) / len(r1)
            agg2[name] = sum(r2.values()) / len(r2) if r2 else float("nan")
            pt1[name], pt2[name] = r1, r2
        res["aggregate"][k] = {"D1": agg1, "D2": agg2,
                               "tau_D1_vs_D2": kendall_tau(agg1, agg2)}
        taus = []
        topics = set().union(*[set(v) for v in pt1.values()])
        for t in sorted(topics):
            a = {n: pt1[n][t] for n in per_run if t in pt1[n]}
            b = {n: pt2[n][t] for n in per_run if t in pt2[n]}
            tau = kendall_tau(a, b)
            if not math.isnan(tau):
                taus.append((t, tau))
        res["per_topic_tau"][k] = dict(taus)
        v = sorted(x[1] for x in taus)
        print(f"\n=== recall@{k} ===", flush=True)
        print(f"  aggregate Kendall tau between the two denominators: "
              f"{res['aggregate'][k]['tau_D1_vs_D2']:+.3f}", flush=True)
        print(f"  per-topic tau over {len(v)} topics: min {v[0]:+.3f} "
              f"q25 {v[len(v)//4]:+.3f} median {v[len(v)//2]:+.3f} "
              f"q75 {v[3*len(v)//4]:+.3f} max {v[-1]:+.3f}", flush=True)
        print(f"  topics where the two denominators disagree on ordering (tau < 0.5): "
              f"{sum(1 for x in v if x < 0.5)}/{len(v)}", flush=True)
        top1 = max(agg1, key=agg1.get)
        top2 = max((n for n in agg2 if not math.isnan(agg2[n])), key=lambda n: agg2[n])
        print(f"  best run under D1: {top1} ({agg1[top1]:.3f})", flush=True)
        print(f"  best run under D2: {top2} ({agg2[top2]:.3f})", flush=True)

    json.dump(res, open("consequence_test.json", "w"), indent=1)
    print("\nwrote consequence_test.json", flush=True)


if __name__ == "__main__":
    main()

"""Does swapping the human denominator for a JUDGE denominator change the system ranking?

The LLM-free control (consequence_test.py) varied the human gold LEVEL and found the ranking
of 27 CLEF participant runs essentially unchanged (aggregate Kendall tau 0.92-0.98). That was
the right control but the wrong contrast: the two human levels are nested, so they differ in
SIZE, and size scales every system equally. Composition is what can reorder systems, and
composition is what the judge changes.

Judge labels exist only on the stratified sample (4,762 of 117,562 pool documents), so the
judge-side recall of a run is ESTIMATED, not measured. The estimator uses the fact that human
labels ARE known for the whole pool: for a run's top-k set S,

    est |S and judge-eligible|  =  |S and human-eligible| * se   +  |S and human-noneligible| * (1-sp)
    est |pool and judge-eligible| =  R * se                      +  (N - R) * (1-sp)

with se and sp estimated per topic from the sample. Writing it out shows the mechanism
directly: under a judge denominator a run earns credit at weight (1-sp) for every
NON-eligible document it retrieves, so depth is rewarded and precision is not.

ASSUMPTION, stated rather than hidden: se and sp are taken as constant within a topic, i.e.
the judge's error rates do not depend on where a run ranked the document. The script tests
that assumption directly by splitting the sample on whether a run placed the document in its
top 100 and recomputing se/sp on each side.

Usage: python judge_consequence.py
"""
import json, math, os, time, urllib.request
from collections import defaultdict

RAW = "https://raw.githubusercontent.com/CLEF-TAR/tar/master/"
API = "https://api.github.com/repos/CLEF-TAR/tar/git/trees/master?recursive=1"
KS = [100, 500, 1000]
THR = 2
MAX_RUNS_PER_TEAM = 2


def get(url, tries=4):
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return r.read()
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(3 * (a + 1))


def load_qrels(path):
    rel, pool = defaultdict(set), defaultdict(set)
    for ln in open(path):
        p = ln.split()
        if len(p) < 4:
            continue
        pool[p[0]].add(p[2])
        if p[3] != "0":
            rel[p[0]].add(p[2])
    return rel, pool


def parse_run(text):
    seen, order = defaultdict(set), defaultdict(list)
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


def kendall_tau(a, b):
    ks = sorted(set(a) & set(b))
    n = len(ks)
    if n < 3:
        return float("nan")
    conc = disc = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            da, db = a[ks[i]] - a[ks[j]], b[ks[i]] - b[ks[j]]
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
    d = math.sqrt((n0 - tx) * (n0 - ty))
    return (conc - disc) / d if d else float("nan")


def main():
    rel, pool = load_qrels("clef2017_abs_test.qrels")
    lab = defaultdict(dict)          # topic -> pmid -> row
    for ln in open("clef_labels_gpt-4o-mini_A.jsonl"):
        r = json.loads(ln)
        if r.get("label") is not None:
            lab[r["topic"]][r["pmid"]] = r

    # per-topic se / sp from the stratified sample
    SESP = {}
    for t, d in lab.items():
        el = [r for r in d.values() if r["stratum"] == "eligible"]
        ne = [r for r in d.values() if r["stratum"] == "non_eligible"]
        if not el or not ne or not rel[t]:
            continue
        SESP[t] = (sum(1 for r in el if r["label"] >= THR) / len(el),
                   sum(1 for r in ne if r["label"] < THR) / len(ne),
                   len(el), len(ne))
    print(f"토픽 {len(SESP)} | se 중위 "
          f"{sorted(v[0] for v in SESP.values())[len(SESP)//2]:.3f} | sp 중위 "
          f"{sorted(v[1] for v in SESP.values())[len(SESP)//2]:.3f}", flush=True)

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
                o = parse_run(get(RAW + urllib.request.quote(p)).decode("utf-8", "replace"))
            except Exception as e:
                print(f"  SKIP {p}: {type(e).__name__}", flush=True); continue
            if len(o) >= 20:
                runs[f"{team}/{os.path.basename(p)}"] = o
    print(f"런 {len(runs)}", flush=True)

    out = {"n_runs": len(runs), "n_topics": len(SESP), "by_k": {}}
    for k in KS:
        hum, jud, pt_h, pt_j = {}, {}, defaultdict(dict), defaultdict(dict)
        for name, order in runs.items():
            hs, js = [], []
            for t, (se, sp, nel, nne) in SESP.items():
                S = set(order.get(t, [])[:k])
                R, N = len(rel[t]), len(pool[t])
                a = len(S & rel[t])
                # only POOL members can carry a judge label, so documents a run returns
                # from outside the judged pool must not earn credit at weight (1-sp).
                # Counting them was a bug that pushed one run's estimate above 1.0.
                b = len(S & pool[t]) - a
                hs.append(a / R)
                num = a * se + b * (1 - sp)
                den = R * se + (N - R) * (1 - sp)
                v = num / den if den else float("nan")
                assert not (v > 1.0000001), (
                    f"estimated judge recall {v:.3f} > 1 on {name}/{t}: "
                    f"a={a} b={b} R={R} N={N} |S|={len(S)}")
                js.append(v)
                pt_h[t][name] = a / R
                pt_j[t][name] = num / den if den else 0.0
            hum[name] = sum(hs) / len(hs)
            jud[name] = sum(js) / len(js)
        tau = kendall_tau(hum, jud)
        taus = [kendall_tau(pt_h[t], pt_j[t]) for t in SESP]
        taus = sorted(x for x in taus if not math.isnan(x))
        top_h = max(hum, key=hum.get); top_j = max(jud, key=jud.get)
        print(f"\n=== recall@{k} ===", flush=True)
        print(f"  집계 Kendall tau (사람 대 판정자 분모): {tau:+.3f}", flush=True)
        print(f"  토픽별 tau: 중위 {taus[len(taus)//2]:+.3f} "
              f"min {taus[0]:+.3f} max {taus[-1]:+.3f} | tau<0.5 토픽 "
              f"{sum(1 for x in taus if x < 0.5)}/{len(taus)}", flush=True)
        print(f"  최고 런 — 사람 분모: {top_h} ({hum[top_h]:.3f})", flush=True)
        print(f"  최고 런 — 판정자 분모: {top_j} ({jud[top_j]:.3f})", flush=True)
        rh = {n: i for i, n in enumerate(sorted(hum, key=hum.get, reverse=True))}
        rj = {n: i for i, n in enumerate(sorted(jud, key=jud.get, reverse=True))}
        moves = sorted(((abs(rh[n] - rj[n]), n, rh[n] + 1, rj[n] + 1) for n in hum),
                       reverse=True)[:5]
        print("  순위 변동 상위 5 (사람 순위 → 판정자 순위):", flush=True)
        for d, n, a_, b_ in moves:
            print(f"    {n:44s} {a_:>2} → {b_:>2}  ({d:+d}칸)", flush=True)
        out["by_k"][k] = dict(tau_aggregate=tau, tau_pertopic_median=taus[len(taus)//2],
                              tau_pertopic_min=taus[0],
                              n_topics_below_half=sum(1 for x in taus if x < 0.5),
                              top_human=top_h, top_judge=top_j,
                              human=hum, judge=jud,
                              biggest_moves=[[n, a_, b_] for _, n, a_, b_ in moves])

    print("\n=== 가정 점검: 판정자 오류율이 런의 순위 위치에 의존하는가 ===", flush=True)
    ref = sorted(runs)[0]
    top, rest = defaultdict(list), defaultdict(list)
    for t, d in lab.items():
        if t not in SESP:
            continue
        S = set(runs[ref].get(t, [])[:100])
        for pmid, r in d.items():
            (top if pmid in S else rest)[r["stratum"]].append(r)
    for nm, grp in (("런 상위 100 안", top), ("그 밖", rest)):
        el, ne = grp.get("eligible", []), grp.get("non_eligible", [])
        if el and ne:
            print(f"  {nm}: se {sum(1 for r in el if r['label']>=THR)/len(el):.3f} (n={len(el)}) "
                  f"| sp {sum(1 for r in ne if r['label']<THR)/len(ne):.3f} (n={len(ne)})", flush=True)
        else:
            print(f"  {nm}: 층 하나가 비어 계산 불가 (적격 {len(el)}, 비적격 {len(ne)})", flush=True)
    out["assumption_check_reference_run"] = ref
    json.dump(out, open("judge_consequence.json", "w"), indent=1)
    print("\nwrote judge_consequence.json", flush=True)


if __name__ == "__main__":
    main()

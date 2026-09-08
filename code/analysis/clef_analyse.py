"""Registered analysis of the CLEF eligibility transfer, plus the judge-based consequence test.

Runs the tests fixed in clef_prereg.py:
  H-E1  does the judge overcount the per-question denominator under EXPERT ELIGIBILITY?
  H-E3  does Rogan-Gladen correction of the judge beat a plain human subsample here?
  A vs B  bound the information asymmetry (title only vs title + search-strategy concepts)

and then the part the LLM-free control could not reach: re-score the 27 CLEF participant runs
under JUDGE-derived eligibility instead of human eligibility, and ask whether the system
ranking moves. Judge labels exist only on the stratified sample, not the full 117,562-document
pool (that would be 24x the daily API quota), so every judge-side quantity is a STRATIFIED
ESTIMATE with its sampling spread reported, never presented as a census.

Usage: python clef_analyse.py
Writes clef_transfer_results.json and prints the numbers.
"""
import json, math, os, random
from collections import defaultdict

THR = 2                     # binarise the 0-3 judge output at >=2, per the pre-registration
KS = [100, 500, 1000]
BOOT = 2000
random.seed(20260905)


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


def load_labels(path):
    rows = []
    for ln in open(path):
        r = json.loads(ln)
        if r.get("label") is not None:
            rows.append(r)
    return rows


def cells(rows):
    """(topic, stratum) -> list of rows"""
    c = defaultdict(list)
    for r in rows:
        c[(r["topic"], r["stratum"])].append(r)
    return c


def weights(topic, c, rel, pool):
    """stratum weight = population size / judged size, for the two strata"""
    R, N = len(rel[topic]), len(pool[topic])
    ne_pop = N - R
    n_el = len(c.get((topic, "eligible"), []))
    n_ne = len(c.get((topic, "non_eligible"), []))
    if not n_el or not n_ne:
        return None
    return R / n_el, ne_pop / n_ne, R, N


def se_sp(rows):
    el = [r for r in rows if r["stratum"] == "eligible"]
    ne = [r for r in rows if r["stratum"] == "non_eligible"]
    if not el or not ne:
        return None, None, len(el), len(ne)
    se = sum(1 for r in el if r["label"] >= THR) / len(el)
    sp = sum(1 for r in ne if r["label"] < THR) / len(ne)
    return se, sp, len(el), len(ne)


def e1(rows, rel, pool):
    """per-topic relative bias of the judge-reconstructed denominator"""
    c = cells(rows)
    out = []
    for t in sorted({r["topic"] for r in rows}):
        w = weights(t, c, rel, pool)
        if w is None:
            continue
        w_el, w_ne, R, N = w
        if R == 0:
            continue
        R_llm = (sum(1 for r in c[(t, "eligible")] if r["label"] >= THR) * w_el
                 + sum(1 for r in c[(t, "non_eligible")] if r["label"] >= THR) * w_ne)
        s, p_, nel, nne = se_sp(c[(t, "eligible")] + c[(t, "non_eligible")])
        out.append(dict(topic=t, N=N, R=R, R_llm=R_llm, rel_bias=(R_llm - R) / R,
                        p=R / N, se=s, sp=p_, n_el=nel, n_ne=nne))
    return out


def med(v):
    """True median. An earlier version returned v[len(v)//2], which for an even-length
    list is the upper of the two middle values, not their mean - it reported +4.395
    instead of +4.126 for the 30-topic condition A bias."""
    v = sorted(v)
    n = len(v)
    if not n:
        return float("nan")
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def e3(rows, rel, pool, grid=(10, 20, 30, 50, 100, 200)):
    """E2 (human subsample only) vs E3 (Rogan-Gladen corrected judge), CLEF version.

    The sample here is stratified on the human label, so a SIMPLE random subsample of the
    pool is drawn by resampling the strata back to their population proportions before
    each estimator is formed. That keeps E2 an honest simple-random-sample estimator.
    """
    c = cells(rows)
    res = defaultdict(lambda: {"E2": [], "E3": [], "unstable": 0, "n": 0})
    for t in sorted({r["topic"] for r in rows}):
        w = weights(t, c, rel, pool)
        if w is None:
            continue
        w_el, w_ne, R, N = w
        if R == 0:
            continue
        el, ne = c[(t, "eligible")], c[(t, "non_eligible")]
        R_llm = (sum(1 for r in el if r["label"] >= THR) * w_el
                 + sum(1 for r in ne if r["label"] >= THR) * w_ne)
        p_true = R / N
        for n in grid:
            for _ in range(200):
                # draw n pool members at their true prevalence, using the judged rows as
                # the source of each stratum's label pair
                k_el = sum(1 for _ in range(n) if random.random() < p_true)
                k_ne = n - k_el
                s_el = [random.choice(el) for _ in range(k_el)] if k_el else []
                s_ne = [random.choice(ne) for _ in range(k_ne)] if k_ne else []
                sub = s_el + s_ne
                e2v = N * (len(s_el) / n)
                res[n]["E2"].append((e2v - R) / R)
                if not s_el or not s_ne:
                    res[n]["unstable"] += 1
                    res[n]["n"] += 1
                    continue
                se_h = sum(1 for r in s_el if r["label"] >= THR) / len(s_el)
                sp_h = sum(1 for r in s_ne if r["label"] < THR) / len(s_ne)
                den = se_h - (1 - sp_h)
                if abs(den) < 0.05:
                    res[n]["unstable"] += 1
                else:
                    e3v = min(max((R_llm - N * (1 - sp_h)) / den, 0), N)
                    res[n]["E3"].append((e3v - R) / R)
                res[n]["n"] += 1
    return res


def rmse(v):
    return math.sqrt(sum(x * x for x in v) / len(v)) if v else float("nan")


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
    out = {}

    print("=== 조건별 판정자 특성 (≥2 이진화) ===")
    conds = {}
    for cond, f in [("A", "clef_labels_gpt-4o-mini_A.jsonl"),
                    ("B", "clef_labels_gpt-4o-mini_B.jsonl")]:
        if not os.path.exists(f):
            print(f"  {cond}: 파일 없음"); continue
        rows = load_labels(f)
        conds[cond] = rows
        s, p_, nel, nne = se_sp(rows)
        print(f"  {cond}: 라벨 {len(rows):,} | 민감도 {s:.3f} (n={nel}) | 특이도 {p_:.3f} (n={nne})")
        out[f"judge_{cond}"] = dict(n=len(rows), se=s, sp=p_, n_el=nel, n_ne=nne)

    print("\n=== H-E1: 판정자 분모의 상대 편향 ===")
    for cond, rows in conds.items():
        b = e1(rows, rel, pool)
        v = [x["rel_bias"] for x in b]
        out[f"e1_{cond}"] = b
        print(f"  {cond}: 토픽 {len(b)} | 중위 {med(v):+.3f} | 평균 {sum(v)/len(v):+.3f} "
              f"| 과대 {sum(1 for x in v if x > 0)}/{len(v)} | 최대 {max(v):+.1f}")
    if "A" in conds and "B" in conds:
        ba = {x["topic"]: x["rel_bias"] for x in out["e1_A"]}
        bb = {x["topic"]: x["rel_bias"] for x in out["e1_B"]}
        both = sorted(set(ba) & set(bb))
        d = [bb[t] - ba[t] for t in both]
        print(f"\n  A vs B 대조 ({len(both)} 공통 토픽): B−A 중위 {med(d):+.3f}")
        print(f"    B가 더 관대한 토픽 {sum(1 for x in d if x > 0)}/{len(both)}")
        print("    → B는 판정자에게 정보를 더 준 조건. B의 편향이 A보다 낮으면 A는 상한이고,"
              " 비슷하면 정보 비대칭이 한정되어 E1은 판정자 속성으로 보고된다.")
        out["a_vs_b"] = dict(n_topics=len(both), median_diff=med(d),
                             b_more_permissive=sum(1 for x in d if x > 0))

    print("\n=== H-E3: 판정자 보정이 사람 부표본을 이기는가 ===")
    if "A" in conds:
        r3 = e3(conds["A"], rel, pool)
        print(f"  {'n':>5} {'E2 편향':>9} {'E2 RMSE':>9} {'E3 편향':>9} {'E3 RMSE':>9} {'불안정':>8}")
        e3tab = {}
        for n in sorted(r3):
            d = r3[n]
            e2b = sum(d["E2"]) / len(d["E2"]) if d["E2"] else float("nan")
            e3b = sum(d["E3"]) / len(d["E3"]) if d["E3"] else float("nan")
            frac = d["unstable"] / max(d["n"], 1)
            print(f"  {n:>5} {e2b:>+9.3f} {rmse(d['E2']):>9.3f} {e3b:>+9.3f} "
                  f"{rmse(d['E3']):>9.3f} {frac:>7.1%}")
            e3tab[n] = dict(E2_bias=e2b, E2_rmse=rmse(d["E2"]),
                            E3_bias=e3b, E3_rmse=rmse(d["E3"]), unstable=frac)
        out["e3"] = e3tab
        print("  사전 등록: E3는 같은 n에서 RMSE가 E2보다 낮고 편향이 ±0.05 안일 때만 선호")
        for n, v in e3tab.items():
            win = v["E3_rmse"] < v["E2_rmse"] and abs(v["E3_bias"]) <= 0.05
            print(f"    n={n}: {'E3 선호' if win else 'E3 선호 안 됨'}")

    print("\n=== 판정자 qrels로 결과 영향 시험 (층화 추정) ===")
    if "A" in conds and os.path.exists("consequence_test.json"):
        c = cells(conds["A"])
        jrel = {}          # topic -> set of sampled docs the judge calls eligible
        jw = {}            # topic -> (w_el, w_ne, R, N)
        for t in sorted({r["topic"] for r in conds["A"]}):
            w = weights(t, c, rel, pool)
            if w is None or len(rel[t]) == 0:
                continue
            jw[t] = w
            jrel[t] = {r["pmid"] for r in c[(t, "eligible")] + c[(t, "non_eligible")]
                       if r["label"] >= THR}
        smp = {t: {r["pmid"]: r for r in c[(t, "eligible")] + c[(t, "non_eligible")]}
               for t in jw}
        prev = json.load(open("consequence_test.json"))
        names = prev["runs"]
        print(f"  런 {len(names)} | 추정 가능한 토픽 {len(jw)}")
        print("  주의: 판정자 라벨은 층화 표본에만 존재하므로 아래는 census가 아니라 추정치")
        out["judge_consequence"] = dict(n_runs=len(names), n_topics=len(jw),
                                        note="stratified estimate, not a census")
    json.dump(out, open("clef_transfer_results.json", "w"), indent=1, default=str)
    print("\nwrote clef_transfer_results.json")


if __name__ == "__main__":
    main()

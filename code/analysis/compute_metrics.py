"""Depth-wise realised recall R(k) and structural signal S(k) per CLEF topic.
S(k) is computed from the retrieved prefix ONLY -- gold is never an input to S."""
import json, csv
from collections import defaultdict

DEPTHS = [25, 50, 100, 150, 200, 300, 400, 500, 750, 1000, 1250, 1500, 2000]
seqs = json.load(open("sequences.json"))
refs = json.load(open("refs_for_sequences.json"))
fx   = {t["topic"]: t for t in json.load(open("clef-2018t1.json"))}

class UF:
    def __init__(s): s.p = {}
    def find(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def union(s, a, b):
        ra, rb = s.find(a), s.find(b)
        if ra != rb: s.p[ra] = rb

rows = []
for key, D in sorted(seqs.items()):
    year, topic = key.split("|")
    if year != "2018t1": continue
    gold = {w.rsplit("/", 1)[-1] for w in fx[topic]["gold_oaids"]}
    n_gold = len(gold)

    uf = UF()
    ref_owners = defaultdict(list)   # ref -> docs in prefix citing it
    partners = defaultdict(set)      # doc -> coupling partners
    hits = 0; norefs = 0
    dset = set()
    ptr = 0
    for k in DEPTHS:
        while ptr < min(k, len(D)):
            w = D[ptr]; ptr += 1
            dset.add(w)
            if w in gold: hits += 1
            rw = refs.get(w) or []
            if not rw: norefs += 1
            uf.find(w)
            for r in rw:
                own = ref_owners[r]
                for o in own:
                    partners[w].add(o); partners[o].add(w)
                    uf.union(w, o)
                own.append(w)
        n = len(dset)
        if n == 0: continue
        edges = sum(len(v) for v in partners.values()) // 2
        comp = defaultdict(int)
        for w in dset: comp[uf.find(w)] += 1
        sizes = sorted(comp.values(), reverse=True)
        rows.append(dict(
            year=year, topic=topic, k=k, n_examined=n, n_gold=n_gold,
            hits=hits, realised_recall=round(hits / n_gold, 6),
            coupling_edges=edges,
            edge_density=round(2 * edges / (n * (n - 1)), 6) if n > 1 else 0.0,
            coupled_frac=round(sum(1 for w in dset if partners.get(w)) / n, 6),
            n_components=len(sizes), giant_frac=round(sizes[0] / n, 6),
            singleton_frac=round(sum(1 for s in sizes if s == 1) / n, 6),
            refs_missing_frac=round(norefs / n, 6),
        ))
        if n >= len(D): break

with open("metrics_by_depth.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"rows={len(rows)}  topics={len({r['topic'] for r in rows})}")
fin = [r for r in rows if r["n_examined"] == max(x["n_examined"] for x in rows if x["topic"] == r["topic"])]
print(f"final-depth recall: min={min(r['realised_recall'] for r in fin):.3f} "
      f"median={sorted(r['realised_recall'] for r in fin)[len(fin)//2]:.3f} "
      f"max={max(r['realised_recall'] for r in fin):.3f}")
print(f"final-depth giant_frac: min={min(r['giant_frac'] for r in fin):.3f} "
      f"max={max(r['giant_frac'] for r in fin):.3f}")
print(f"refs_missing_frac at final depth: min={min(r['refs_missing_frac'] for r in fin):.3f} "
      f"max={max(r['refs_missing_frac'] for r in fin):.3f}")

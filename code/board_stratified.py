#!/usr/bin/env python3
r"""Stratified subsample on judge-defined strata - registered hypothesis H-B6.

H-B6 asserts that stratifying the expert budget on the judge's BINARY decision attains a lower
relative RMSE of R-hat than simple random sampling without replacement at equal budget, by a
factor of at least HB6_RATIO at HB6_MIN_GRIDPOINTS or more of the six registered budgets.

Two things the registration fixes and this file obeys. The strata come from the judge's binary
decision and never from the expert label: the frozen panel's strata ARE the expert label, so
using them would be stratifying on the answer. And the comparator is the expansion estimator
under simple random sampling computed in the same run, not a curve carried from elsewhere.

One thing the registration left free and Amendment 5 fixes BEFORE any value here exists: the
allocation of the budget between strata. Primary is proportional allocation with at least one
unit in every non-empty stratum; pure proportional and Neyman-on-the-judge's-label are reported
in the sensitivity grid and never substituted for the primary. A verdict holding only under some
allocations is reported as conditional on allocation.

Estimator, the standard stratified expansion form:

    R_hat = sum_h  N_h * (r_h / n_h)

over strata that received at least one unit; a stratum that received none contributes nothing,
which is why the minimum of one is part of the primary rule rather than a convenience.

Usage
    python board_stratified.py --labels <pool labels jsonl> --qrels <abs qrels> \
        [--reps 1000] [--out board_stratified.csv]
"""
import argparse
import json

import numpy as np
import pandas as pd

SEED = 20260921
N_GRID = (3, 5, 10, 20, 30, 50, 75, 100)
N_GRID_REGISTERED_SUBSET = (10, 20, 30, 50, 75, 100)
BOOTSTRAP_REPS = 1000
BINARISE_AT = 2
EXCLUDE_IF_R_ZERO = True
EXCLUDE_POOL_EXHAUSTED = True
HB6_RATIO = 0.90
HB6_MIN_GRIDPOINTS = 4
HB6_ALLOCATION = "proportional_min1"
HB6_ALLOCATION_GRID = ("proportional_min1", "proportional", "neyman_judge")


def cell_rng(topic, n, tag, seed=SEED):
    return np.random.default_rng([seed, abs(hash(topic)) % (2 ** 31), n,
                                  abs(hash(tag)) % (2 ** 31)])


def allocate(n, sizes, sds, rule):
    """Split budget n across strata of the given sizes. Returns integer counts summing to n
    (or to the total population where n exceeds it), each capped at its stratum size."""
    sizes = np.asarray(sizes, float)
    live = sizes > 0
    if rule == "neyman_judge":
        w = sizes * np.asarray(sds, float)
        if w.sum() <= 0:
            w = sizes.copy()
    else:
        w = sizes.copy()
    w = np.where(live, w, 0.0)
    raw = n * w / w.sum()
    base = np.floor(raw).astype(int)
    if rule == "proportional_min1":
        base = np.where(live & (base < 1), 1, base)
    # largest-remainder adjustment, then cap at stratum size and spill the excess
    while base.sum() != n:
        if base.sum() < n:
            frac = np.where(live & (base < sizes), raw - base, -np.inf)
            if not np.isfinite(frac).any():
                break
            base[int(np.argmax(frac))] += 1
        else:
            cut = np.where(base > (1 if rule == "proportional_min1" else 0), base - raw, -np.inf)
            if not np.isfinite(cut).any():
                break
            base[int(np.argmax(cut))] -= 1
    over = base > sizes
    if over.any():
        spill = int((base[over] - sizes[over]).sum())
        base = np.minimum(base, sizes).astype(int)
        for _ in range(spill):
            room = np.where(live & (base < sizes), sizes - base, -np.inf)
            if not np.isfinite(room).any():
                break
            base[int(np.argmax(room))] += 1
    return base.astype(int)


def run(D, reps=BOOTSTRAP_REPS, rule=HB6_ALLOCATION):
    rows = []
    for t, g in D.groupby("topic"):
        y = g.y.values.astype(float)
        s = (g.label.values >= BINARISE_AT).astype(int)      # judge's binary decision
        N = len(y)
        R = int(y.sum())
        if EXCLUDE_IF_R_ZERO and R == 0:
            continue
        idx_h = [np.flatnonzero(s == h) for h in (0, 1)]
        sizes = [len(i) for i in idx_h]
        sds = [float(np.std(g.label.values[i])) if len(i) else 0.0 for i in idx_h]
        for n in N_GRID:
            if EXCLUDE_POOL_EXHAUSTED and n >= N:
                continue
            nh = allocate(n, sizes, sds, rule)
            rng = cell_rng(t, n, rule)
            est = np.empty(reps)
            for i in range(reps):
                tot = 0.0
                for h in (0, 1):
                    if nh[h] <= 0 or sizes[h] == 0:
                        continue
                    pick = rng.choice(idx_h[h], size=int(nh[h]), replace=False)
                    tot += sizes[h] * y[pick].mean()
                est[i] = tot
            rows.append(dict(topic=t, n=n, N=N, R=R, p=R / N, rule=rule,
                             n_stratum0=int(nh[0]), n_stratum1=int(nh[1]),
                             N_stratum0=sizes[0], N_stratum1=sizes[1],
                             bias=(est.mean() - R) / R,
                             rmse=np.sqrt(((est - R) ** 2).mean()) / R,
                             rmse_abs=np.sqrt(((est - R) ** 2).mean())))
    return pd.DataFrame(rows)


def srswor(D, reps=BOOTSTRAP_REPS):
    """The comparator, computed in the same run rather than carried from another."""
    rows = []
    for t, g in D.groupby("topic"):
        y = g.y.values.astype(float)
        N, R = len(y), int(g.y.sum())
        if EXCLUDE_IF_R_ZERO and R == 0:
            continue
        for n in N_GRID:
            if EXCLUDE_POOL_EXHAUSTED and n >= N:
                continue
            rng = cell_rng(t, n, "srswor")
            est = np.array([N * y[rng.choice(N, size=n, replace=False)].mean()
                            for _ in range(reps)])
            rows.append(dict(topic=t, n=n, N=N, R=R,
                             rmse=np.sqrt(((est - R) ** 2).mean()) / R))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--qrels", required=True)
    ap.add_argument("--reps", type=int, default=BOOTSTRAP_REPS)
    ap.add_argument("--out", default="board_stratified.csv")
    args = ap.parse_args()

    L = pd.DataFrame([json.loads(l) for l in open(args.labels) if l.strip()])
    L["topic"] = L.topic.astype(str)
    L["pmid"] = L.pmid.astype(str)
    L = L[L.label.notna()].drop_duplicates(["topic", "pmid"], keep="last")
    Q = pd.read_csv(args.qrels, sep=r"\s+", header=None,
                    names=["topic", "z", "pmid", "rel"], dtype={"topic": str, "pmid": str})
    Q["rel"] = Q.rel.astype(int)
    D = L[["topic", "pmid", "label"]].merge(Q[["topic", "pmid", "rel"]],
                                            on=["topic", "pmid"], how="inner")
    D["y"] = (D.rel >= 1).astype(int)
    if len(D) != len(L):
        raise SystemExit(f"{len(L) - len(D)} labelled pairs have no qrels row; refusing")
    print(f"population {len(D):,} pairs, {D.topic.nunique()} topics", flush=True)

    C = srswor(D, reps=args.reps)
    comp = C.groupby("n").rmse.median()
    parts = []
    for rule in HB6_ALLOCATION_GRID:
        F = run(D, reps=args.reps, rule=rule)
        parts.append(F)
        med = F.groupby("n").rmse.median()
        ratio = (med / comp).loc[list(N_GRID_REGISTERED_SUBSET)]
        met = int((ratio <= HB6_RATIO).sum())
        verdict = ("SUPPORTED" if met >= HB6_MIN_GRIDPOINTS else
                   "PARTIAL" if met >= 2 else "NOT SUPPORTED")
        print(f"\n[{rule}] median relative RMSE\n{med.round(4).to_string()}")
        print(f"[{rule}] ratio to SRSWOR at the registered budgets "
              f"{np.round(ratio.values, 3).tolist()} -> {met}/6 {verdict}"
              + ("" if rule == HB6_ALLOCATION else "   (secondary: sensitivity only)"), flush=True)
    A = pd.concat(parts, ignore_index=True)
    A.to_csv(args.out, index=False)
    C.to_csv(args.out.replace(".csv", "_srswor.csv"), index=False)
    print(f"\nrows {len(A)} | wrote {args.out} and {args.out.replace('.csv', '_srswor.csv')}",
          flush=True)


if __name__ == "__main__":
    main()

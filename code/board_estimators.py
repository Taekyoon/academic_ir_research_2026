#!/usr/bin/env python3
r"""Recompute the probability-sample procedures of the baseline board on the REAL pool.

WHY THIS FILE EXISTS. Numbers for the model-assisted and Bayesian estimators existed in
greg_faithful.csv, but the script that produced them was never committed, and the numbers
themselves cannot be carried into the board for two reasons found later: they were computed on a
stratum-weighted PSEUDO-population rebuilt from a 4.05 per cent stratified sample, and they were
aggregated across topics by the MEAN where the registered metric takes the median. Both are fixed
here by running the same estimators on the pool itself, now that the judge's label exists on every
pool document.

THE ESTIMATORS ARE NOT REDEFINED HERE. They are transcribed from the lineage of
greg_faithful.csv so that the only thing that changes is the population and the aggregation:

    E2  expansion            R_hat = N * mean(y_sample)
    E4  model-assisted       R_hat = m_soft + (N / n) * sum(y_sample - phat_sample)
    EB  Bayesian shrinkage   R_hat = N * (kappa * p0 + r) / (kappa + n)

where phat is a leave-one-topic-out logistic fit of expert eligibility on the judge's graded
label, m_soft = sum(phat) over the topic's population, p0 = m_soft / N and r = sum(y_sample).
E4 is the difference form that uses the known auxiliary total; EB shrinks the sample rate toward
the auxiliary-implied rate p0 with prior weight kappa.

WHAT IS REGISTERED AND NOT DECIDED HERE. These three procedures carry no registered hypothesis of
their own; they supply board rows and the comparator the primary hypothesis needs. What this run
does bear on is declared prediction 2 of the plan's section 1 - that shrinkage toward a collection
constant is what lowers error rather than information from the judge - which was stated on the
pseudo-population figures and is now recomputed on the pool.

Usage
    python board_estimators.py --labels <pool labels jsonl> --qrels <abs qrels> \
        [--reps 1000] [--out board_estimators.csv]
"""
import argparse
import json
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

# Registered constants, read from prereg/baseline_prereg.py rather than restated from memory.
SEED = 20260921
N_GRID = (3, 5, 10, 20, 30, 50, 75, 100)
N_GRID_REGISTERED_SUBSET = (10, 20, 30, 50, 75, 100)
BOOTSTRAP_REPS = 1000
METRIC_SCALING = "relative"
EXCLUDE_IF_R_ZERO = True
EXCLUDE_POOL_EXHAUSTED = True
KAPPAS = (10, 50)


def cell_rng(topic, n, seed=SEED):
    """One stream per (topic, budget) so a value does not depend on which grid was requested.

    The anchoring run showed that a single stream makes every value depend on grid order; this
    is the same fix, and it is why the E2 column here is comparable with baseline_curves.csv.
    """
    return np.random.default_rng([seed, abs(hash(topic)) % (2 ** 31), n])


def loto_phat(D):
    """Leave-one-topic-out logistic fit of expert eligibility on the judge's graded label.

    Leave-one-topic-out rather than in-sample: the auxiliary variable must not be calibrated on
    the topic whose denominator it is then used to estimate, or the estimator is scored on a fit
    that saw the answer. No stratum weights are needed here - the pool is the population, not a
    sample of it, which is the whole point of re-running on it.
    """
    out = pd.Series(np.nan, index=D.index)
    for t in sorted(D.topic.unique()):
        tr = D[D.topic != t]
        f = sm.GLM(tr.y, sm.add_constant(tr[["label"]].astype(float)),
                   family=sm.families.Binomial()).fit()
        te = D.loc[D.topic == t, ["label"]].astype(float)
        out.loc[D.topic == t] = f.predict(sm.add_constant(te, has_constant="add"))
    return out


def run(D, reps=BOOTSTRAP_REPS, prior="judge"):
    """prior='judge' shrinks toward the auxiliary-implied rate m_soft/N; prior='collection'
    shrinks toward a judge-free constant.

    The two are the discriminating pair for declared prediction 2, which claims that shrinkage
    toward a collection constant lowers the error rather than information from the judge. With
    prior='judge' the shrinkage target carries the judge's calibrated labels, so a win there does
    not by itself support that claim. The collection prior is the leave-one-topic-out median of
    the true relevance rate over the other topics - judge-free, and the same kind of quantity the
    uninformative guess already uses as a board row.
    """
    rows = []
    ptrue = D.groupby("topic").y.mean()
    for t, g in D.groupby("topic"):
        y = g.y.values.astype(float)
        ph = g.phat.values.astype(float)
        N = len(y)
        R = int(y.sum())
        if EXCLUDE_IF_R_ZERO and R == 0:
            continue
        m_soft = ph.sum()
        p0 = m_soft / N if prior == "judge" else float(ptrue.drop(t).median())
        for n in N_GRID:
            if EXCLUDE_POOL_EXHAUSTED and n >= N:
                continue
            rng = cell_rng(t, n)
            e2 = np.empty(reps)
            e4 = np.empty(reps)
            eb = {k: np.empty(reps) for k in KAPPAS}
            for i in range(reps):
                idx = rng.choice(N, size=n, replace=False)
                ys, ps = y[idx], ph[idx]
                r = ys.sum()
                e2[i] = N * ys.mean()
                e4[i] = m_soft + (N / n) * (ys - ps).sum()
                for k in KAPPAS:
                    eb[k][i] = N * (k * p0 + r) / (k + n)
            rec = dict(topic=t, n=n, N=N, R=R, p=R / N, m_soft=m_soft, p0=p0, prior=prior)
            for nm, a in [("E2", e2), ("E4", e4)] + [(f"EB{k}", eb[k]) for k in KAPPAS]:
                # Relative scaling is the registered primary metric; absolute is carried
                # alongside and never substituted.
                rec[f"bias_{nm}"] = (a.mean() - R) / R
                rec[f"rmse_{nm}"] = np.sqrt(((a - R) ** 2).mean()) / R
                rec[f"rmse_abs_{nm}"] = np.sqrt(((a - R) ** 2).mean())
            rec["var_ratio_E4_E2"] = np.var(e4) / np.var(e2) if np.var(e2) > 0 else np.nan
            rows.append(rec)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--qrels", required=True)
    ap.add_argument("--reps", type=int, default=BOOTSTRAP_REPS)
    ap.add_argument("--out", default="board_estimators.csv")
    ap.add_argument("--prior", choices=("judge", "collection"), default="judge")
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
        raise SystemExit(f"{len(L) - len(D)} labelled pairs have no qrels row; the population "
                         f"would be silently smaller than the labels. Refusing to continue.")
    print(f"population {len(D):,} pairs, {D.topic.nunique()} topics, "
          f"{int(D.y.sum()):,} eligible ({D.y.mean():.4f})", flush=True)

    D["phat"] = loto_phat(D)
    if D.phat.isna().any():
        raise SystemExit("leave-one-topic-out calibration left NaNs")
    print(f"auxiliary calibrated: phat {D.phat.min():.4f} to {D.phat.max():.4f}", flush=True)

    F = run(D, reps=args.reps, prior=args.prior)
    F.to_csv(args.out, index=False)
    cols = [c for c in F.columns if c.startswith("rmse_") and not c.startswith("rmse_abs")]
    med = F.groupby("n")[cols].median()
    med.to_csv(args.out.replace(".csv", "_median.csv"))
    print(f"\nmedian across topics, relative RMSE (registered metric):\n"
          f"{med.round(4).to_string()}", flush=True)
    print(f"\nrows {len(F)} | topics {F.topic.nunique()} | wrote {args.out} and "
          f"{args.out.replace('.csv', '_median.csv')}", flush=True)


if __name__ == "__main__":
    main()

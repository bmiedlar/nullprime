"""Train/test accuracy of standard learners on the null and contrast splits.

    python -m nullprime.certify                      # 10-digit, B=1000, 5 seeds
    python -m nullprime.certify --lo 1e14 --hi 1e15 --filter-below 10000
"""
import argparse
import math
import platform
import statistics

import numpy as np
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .generate import contrast_split, features, null_split, small_primes


def learners(seed):
    return {
        "logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)),
        "random forest (400)": RandomForestClassifier(n_estimators=400, random_state=seed, n_jobs=-1),
        "gradient boosting": HistGradientBoostingClassifier(random_state=seed),
        "k-nearest (15)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15)),
        "MLP (256,128)": make_pipeline(StandardScaler(),
                                       MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=900, random_state=seed)),
    }


def run(rows, smalls, seed):
    X = np.array([features(n, smalls) for n, _ in rows], dtype=float)
    y = np.array([label for _, label in rows])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    out = {}
    for name, clf in learners(seed).items():
        clf.fit(Xtr, ytr)
        out[name] = (clf.score(Xtr, ytr), clf.score(Xte, yte), len(yte))
    return out


def summarize(results):
    """Mean over seeds; 95% interval on pooled held-out accuracy."""
    lines = []
    for name in results[0]:
        train = statistics.mean(r[name][0] for r in results)
        tests = [r[name][1] for r in results]
        n = sum(r[name][2] for r in results)
        p = statistics.mean(tests)
        half = 1.96 * math.sqrt(p * (1 - p) / n)
        lines.append(f"  {name:>20}   train {train:.3f}   test {p:.3f} ± {half:.3f}   "
                     f"(seeds {min(tests):.3f}–{max(tests):.3f})")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3000, help="samples per class")
    ap.add_argument("--lo", type=float, default=1e9)
    ap.add_argument("--hi", type=float, default=1e10)
    ap.add_argument("--filter-below", type=int, default=1000)
    ap.add_argument("--seeds", type=int, default=5)
    a = ap.parse_args()
    lo, hi = int(a.lo), int(a.hi)
    smalls = small_primes(a.filter_below)

    print(f"NullPrime certificate · [{a.lo:.0e}, {a.hi:.0e}) · filter < {a.filter_below} · "
          f"{a.n}+{a.n} per split · {a.seeds} seeds")
    print(f"python {platform.python_version()} · numpy {np.__version__} · scikit-learn {sklearn.__version__}\n")
    for label, build in (("null (filtered)", lambda s: null_split(a.n, lo, hi, a.filter_below, s)),
                         ("contrast (unfiltered)", lambda s: contrast_split(a.n, lo, hi, s))):
        results = [run(build(seed), smalls, seed) for seed in range(a.seeds)]
        print(label)
        print("\n".join(summarize(results)))
        print()
    print("chance = 0.500")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

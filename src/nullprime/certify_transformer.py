"""The certificate for a sequence model: a small transformer that reads each number as digit tokens, trained from
scratch on the same null and contrast splits as `certify.py`.

    python -m nullprime.certify_transformer                    # 10-digit, B=1000, 5 seeds
    python -m nullprime.certify_transformer --lo 1e14 --hi 1e15 --filter-below 10000
"""
import argparse
import math
import platform
import statistics

import torch
from torch import nn

from nullprime.generate import contrast_split, null_split

DIGITS = 16          # left-padded with a pad token, so every number is the same length


def encode(rows):
    x = torch.full((len(rows), DIGITS), 10, dtype=torch.long)          # 10 = pad
    for i, (n, _) in enumerate(rows):
        d = [int(c) for c in str(n)]
        x[i, DIGITS - len(d):] = torch.tensor(d)
    y = torch.tensor([label for _, label in rows], dtype=torch.float32)
    return x, y


class DigitTransformer(nn.Module):
    def __init__(self, dim=64, layers=2, heads=4):
        super().__init__()
        self.token = nn.Embedding(11, dim)
        self.position = nn.Parameter(torch.randn(DIGITS, dim) * 0.02)
        block = nn.TransformerEncoderLayer(dim, heads, dim_feedforward=4 * dim, dropout=0.1, batch_first=True)
        self.encoder = nn.TransformerEncoder(block, layers)
        self.head = nn.Linear(dim, 1)

    def forward(self, x):
        h = self.encoder(self.token(x) + self.position)
        return self.head(h.mean(dim=1)).squeeze(-1)


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return ((model(x) > 0).float() == y).float().mean().item()


def run(rows, seed, epochs, test_share=0.3):
    torch.manual_seed(seed)
    g = torch.Generator().manual_seed(seed)
    x, y = encode(rows)
    order = torch.randperm(len(rows), generator=g)
    cut = int(len(rows) * (1 - test_share))
    tr, te = order[:cut], order[cut:]
    model = DigitTransformer()
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        model.train()
        for batch in torch.randperm(len(tr), generator=g).split(128):
            idx = tr[batch]
            opt.zero_grad()
            loss_fn(model(x[idx]), y[idx]).backward()
            opt.step()
    return accuracy(model, x[tr], y[tr]), accuracy(model, x[te], y[te]), len(te)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3000, help="samples per class")
    ap.add_argument("--lo", type=float, default=1e9)
    ap.add_argument("--hi", type=float, default=1e10)
    ap.add_argument("--filter-below", type=int, default=1000)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--threads", type=int, default=2)
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    lo, hi = int(a.lo), int(a.hi)
    print(f"Digit transformer · [{a.lo:.0e}, {a.hi:.0e}) · filter < {a.filter_below} · {a.n}+{a.n} per split · "
          f"{a.seeds} seeds · {a.epochs} epochs")
    print(f"python {platform.python_version()} · torch {torch.__version__}\n")
    for label, build in (("null (filtered)", lambda s: null_split(a.n, lo, hi, a.filter_below, s)),
                         ("contrast (unfiltered)", lambda s: contrast_split(a.n, lo, hi, s))):
        results = [run(build(seed), seed, a.epochs) for seed in range(a.seeds)]
        train = statistics.mean(r[0] for r in results)
        tests = [r[1] for r in results]
        p, n = statistics.mean(tests), sum(r[2] for r in results)
        print(f"{label:<24} train {train:.3f}   test {p:.3f} ± {1.96 * math.sqrt(p * (1 - p) / n):.3f}   "
              f"(seeds {min(tests):.3f}-{max(tests):.3f})")
    print("chance = 0.500")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

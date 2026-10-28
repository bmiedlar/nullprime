"""NullPrime splits.

null      coprime to every prime below B; balanced prime/composite
contrast  same range, unfiltered; balanced
easy      composites with a factor of 13 or less
"""
import random

EASY_MAX_FACTOR = 13


def small_primes(limit):
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i, v in enumerate(sieve) if v]


_WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n):
    """Deterministic Miller-Rabin for n < 3.3e24."""
    if n < 2:
        return False
    for p in _WITNESSES:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _WITNESSES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def smallest_factor(n, limit):
    for p in small_primes(limit):
        if n % p == 0:
            return p
    return None


def _balanced(rng, lo, hi, n_per_class, keep):
    primes, comps = [], []
    while len(primes) < n_per_class or len(comps) < n_per_class:
        n = rng.randrange(lo, hi) | 1
        if not keep(n):
            continue
        bucket = primes if is_prime(n) else comps
        if len(bucket) < n_per_class:
            bucket.append(n)
    rows = [(n, 1) for n in primes] + [(n, 0) for n in comps]
    rng.shuffle(rows)
    return rows


def null_split(n_per_class, lo, hi, filter_below, seed):
    smalls = small_primes(filter_below)
    keep = lambda n: all(n % p for p in smalls)
    return _balanced(random.Random(seed), lo, hi, n_per_class, keep)


def contrast_split(n_per_class, lo, hi, seed):
    return _balanced(random.Random(seed), lo, hi, n_per_class, lambda n: True)


def easy_split(n, lo, hi, seed):
    rng = random.Random(seed)
    smalls = small_primes(EASY_MAX_FACTOR + 1)
    rows, seen = [], set()
    while len(rows) < n:
        p = rng.choice(smalls)
        k = rng.randrange(lo // p + 1, hi // p)
        m = p * k
        if m in seen or not (lo <= m < hi):
            continue
        seen.add(m)
        rows.append((m, 0))
    return rows


def features(n, smalls, n_residues=40, n_digits=12):
    """Trailing digits and residues mod the first small primes. On the null split the residues carry no signal
    by construction; they stay in so a learner has something to overfit."""
    digits = [int(c) for c in str(n)][-n_digits:]
    digits = [0] * (n_digits - len(digits)) + digits
    return digits + [n % p for p in smalls[:n_residues]]


def feature_names(smalls, n_residues=40, n_digits=12):
    return [f"d{i}" for i in range(n_digits)] + [f"mod{p}" for p in smalls[:n_residues]]

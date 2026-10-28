from nullprime.generate import (EASY_MAX_FACTOR, contrast_split, easy_split, is_prime, null_split, small_primes,
                                smallest_factor)


def trial_division(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def test_miller_rabin_matches_trial_division():
    assert all(is_prime(n) == trial_division(n) for n in range(0, 20000))
    for n in (1_000_000_007, 999_999_937, 1_000_000_011, 4_295_098_369, 10_000_000_019):
        assert is_prime(n) == trial_division(n)


def test_null_split_is_filtered_balanced_and_correct():
    rows = null_split(200, 10**9, 10**10, 1000, seed=1)
    smalls = small_primes(1000)
    assert sum(label for _, label in rows) == 200 and len(rows) == 400
    assert all(all(n % p for p in smalls) for n, _ in rows)
    assert all(is_prime(n) == bool(label) for n, label in rows[:40])
    assert len({n for n, _ in rows}) == len(rows)


def test_contrast_split_is_balanced_and_mostly_small_factor_composites():
    rows = contrast_split(200, 10**9, 10**10, seed=1)
    assert sum(label for _, label in rows) == 200
    comps = [n for n, label in rows if label == 0]
    assert sum(smallest_factor(n, 1000) is not None for n in comps) > 0.8 * len(comps)


def test_easy_split_has_checkable_small_factor():
    rows = easy_split(300, 10**9, 10**10, seed=1)
    assert all(label == 0 and 10**9 <= n < 10**10 for n, label in rows)
    assert all(smallest_factor(n, EASY_MAX_FACTOR + 1) is not None for n, _ in rows)


def test_seeded_and_deterministic():
    assert null_split(50, 10**9, 10**10, 1000, seed=7) == null_split(50, 10**9, 10**10, 1000, seed=7)


def test_standalone_generator_matches_package():
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location("make_numbers", pathlib.Path(__file__).parents[1] / "make_numbers.py")
    mn = importlib.util.module_from_spec(spec); spec.loader.exec_module(mn)
    assert all(mn.is_prime(n) == is_prime(n) for n in range(0, 20000))
    rows = mn.make(40, 15, seed=3)
    assert len(rows) == 40 and sum(p for _, p in rows) == 20
    assert all(10**14 <= n < 10**15 and all(n % p for p in small_primes(10000)) and mn.is_prime(n) == p for n, p in rows)

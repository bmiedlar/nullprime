from nullprime.llm_eval import items, parse, parse_plain, prompt
from nullprime.plain_rules import claimed_factors, classify


def test_parse_structured():
    p = parse("Let me think...\nVERDICT: COMPOSITE\nCONFIDENCE: 85\nFACTOR: 7")
    assert p == {"verdict": "COMPOSITE", "confidence": 85, "factors": [7], "structured": True}


def test_parse_bold_none_and_last_verdict():
    p = parse("**VERDICT:** PRIME\n**CONFIDENCE:** 60\n**FACTOR:** NONE")
    assert (p["verdict"], p["confidence"], p["factors"]) == ("PRIME", 60, [])
    assert parse("VERDICT: PRIME\n...on reflection...\nVERDICT: COMPOSITE")["verdict"] == "COMPOSITE"
    assert parse("I believe it is prime.")["structured"] is False
    assert parse("")["verdict"] is None


def test_prompts():
    assert "CANNOT DETERMINE" not in prompt(11, "forced")
    assert "CANNOT DETERMINE" in prompt(11, "abstain")
    assert prompt(432558702875843, "plain") == "Is 432558702875843 prime?"


def test_items_fixed_and_balanced():
    a, b = items(), items()
    assert a == b and len(a) == 450
    null = [r for r in a if r[3] == "null"]
    assert len(null) == 300 and sum(r[2] for r in null) == 150


def test_plain_verdicts():
    assert classify("Yes, 2,041,477,297 is prime.") == "PRIME"
    assert classify("No. 1,726,544,221 is composite.") == "COMPOSITE"
    assert classify("I can’t reliably determine it by inspection.") == "CANNOT DETERMINE"
    assert classify("I can't give you a definitive answer by hand.") == "CANNOT DETERMINE"
    assert classify("It might be prime, or it might not.") is None


def test_plain_factors_ignore_negations():
    n = 7688173373
    assert claimed_factors(r"No. \(7{,}688{,}173{,}373 = 1{,}009 \times 7{,}619{,}597\)", n) == [1009, 7619597]
    assert claimed_factors("It is not divisible by 3, 7 or 11.", n) == []
    assert claimed_factors("It's even, so it's divisible by 2.", 10) == [2]


def test_parse_plain_confidence():
    assert parse_plain("Yes, 11 is prime.", 11)["confidence"] == 100
    assert parse_plain("It is probably prime.", 11)["confidence"] == 70
    assert parse_plain("I can't tell without a computer.", 11)["confidence"] is None


def test_v2_patterns_match_and_skip_conditionals():
    from nullprime import plain_rules as p
    assert p.COMPOSITE_V2.search("No, 4650710203 is not prime.")
    assert p.PRIME_V2.search("Yes, it is prime.")
    assert not p.PRIME_V2.search("This prints True if it is prime.")
    assert b"\x08" not in open(p.__file__, "rb").read()


def test_famous_items_are_labeled_correctly():
    from nullprime.generate import is_prime
    from nullprime.llm_eval import famous_items
    rows = famous_items()
    assert len(rows) == 24 and famous_items() == rows
    assert all(is_prime(n) == bool(label) for _, n, label, _ in rows)
    assert sum(1 for r in rows if r[3] == "control") == 12


def test_false_factor_claims():
    from nullprime.plain_rules import false_factor_claim
    assert false_factor_claim(r"No. It is divisible by 7: \[ 3776739727 = 7 \times 539534247. \]", 3776739727)
    assert false_factor_claim("Bottom line: 7748033141 = 13×596771779, so it is composite.", 7748033141)
    assert not false_factor_claim("= 3 × 2954020986 + 1. Actually, that leaves a remainder.", 8862062959)
    assert not false_factor_claim("It is not divisible by 3, 7 or 11.", 8862062959)
    assert not false_factor_claim("9365056201 = 7 × 1337865171 + 4", 9365056201)
    assert not false_factor_claim("It's even, so it is divisible by 2: 10 = 2 × 5.", 10)

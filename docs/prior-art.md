# Prior art and what's new

Compiled 2026-10-16. **Check every citation against the paper
itself before publishing.** The grokking and arithmetic background items were listed from memory, not checked.

## Closest prior art

- **Lowry-Duda, "Studying number theory with deep learning" (2025, arXiv 2502.10335).** Inputs: residues mod the
  first 100 primes. "All the predictive power" for μ(n) comes from divisibility by a square (mostly mod 2 and 3).
  Models can't separate μ=1 from μ=−1, and the paper challenges readers to beat 51%. **Same phenomenon, for μ(n)
  instead of primality.** NullPrime packages that observation as a deliberate, balanced control.
- **Charton, "Learning the greatest common divisor" (ICLR 2024, arXiv 2308.15594).** Transformers learn GCD from
  divisors built from small primes. This is the signal NullPrime removes.
- **Zhang et al., "Understanding deep learning requires rethinking generalization" (ICLR 2017, arXiv 1611.03530).**
  Memorize random labels, test at chance. NullPrime reproduces this with *deterministic, checkable* labels: no
  injected noise.
- Contrast: **Chatterjee & Sudijono (2024, arXiv 2409.12446).** Minimum-description-length networks provably learn
  primality *from n itself*. Learnable from n, not from our features.

## Parity (the cousin, and the difference)

Shalev-Shwartz et al. 2017 (1703.07950); Barak et al. NeurIPS 2022 (2207.08799); Abbe & Sandon 2020 (2001.02992).
Parity is a *function of the features*: hard, but learnable. In NullPrime the label is **not a function of the
features**: the Bayes rate is 50%. Impossible on information grounds, not on computational ones.

## Abstention and "known unknowns"

SQuAD 2.0 (1806.03822) · SelfAware, Yin et al. 2023 (2305.18153) · KUQ, Amayuelas et al. 2023 (2305.13712) ·
Kadavath et al. 2022 (2207.05221) · R-Tuning, NAACL 2024 (2311.09677) · **AbstentionBench**, Kirichenko et al.,
NeurIPS 2025 (2506.09038): reasoning fine-tuning cuts abstention by about 24%.
None use **in-distribution synthetic unknowables**. Their unanswerability comes from missing context, a false
premise, subjectivity or the future. A NullPrime question is well-posed, has a definite answer, and the answer
can be checked by program. It also comes with a matched easy split.

## Tool-use decisions

MetaTool, ICLR 2024 (2310.03128) · ToolBeHonest 2024 (2406.20015) · **When2Call**, NAACL 2025 (2504.18851) ·
SMART, ACL Findings 2025 (2502.11435) · Toolformer 2023 (2302.04761). These mostly test overuse or impossible
tools. NullPrime gives the reverse case: a question that *should* trigger a tool call, paired with an easy split
where answering directly is right.

## LLM primality: the known flawed study

- **Chen, Zaharia & Zou, "How is ChatGPT's behavior changing over time?"** (2023, arXiv 2307.09009). v1 used 500
  numbers, *all prime*; GPT-4 fell from 97.6% to 2.4%.
- **Narayanan & Kapoor (AI Snake Oil, Jul 2023):** with an all-prime set, accuracy measures how often a model says
  "yes", so the drop is a behavior drift. The models also only *appear* to check divisors.
- **v3 (Oct 2023)** balanced it: 500 primes + 500 composites from [1000, 20000]. But ~77% of those composites have
  a factor of 2, 3 or 5, so the answer is guessable from the last digit or the digit sum. The numbers are also small
  enough to memorize.
- **NullPrime fixes each flaw:**
  - Balanced classes, so a constant answer scores exactly 50%.
  - No factor below B, so there are no shortcuts.
  - 10- and 15-digit numbers can't be memorized and can't be trial-divided in your head.
  - The easy split keeps "trivially composite" separate.
  - Fabricated factors are measured, so "pretends to check divisors" becomes a number.

## Framing rule (from this review)

**Given the features, the uncertainty is aleatoric (irreducible), not epistemic.** More data never helps. Say
"irreducible given the representation". If an "epistemic" method flags NullPrime as epistemic, report that as a
finding about the method, not as a success.

## What's new: claim exactly this

The phenomena aren't new. The contribution is the combination:
1. A balanced, filtered dataset with deterministic, checkable labels that provably carry no feature signal: a
   ready-made negative control.
2. A matched easy/hard split that isolates the shortcut.
3. An LLM protocol measuring, on the same items, calibration, confident wrong answers, fabricated factors,
   abstention and tool choice.

## Must-cite

Zhang et al. 2017 · Charton 2024 · Lowry-Duda 2025 · Chen, Zaharia & Zou 2023 + Narayanan & Kapoor 2023 ·
Barak et al. 2022 · AbstentionBench 2025 · Kadavath et al. 2022 · When2Call 2025.

## Name

No collision found on PyPI, npm, Hugging Face, or the web. GitHub was checked by web search only, so search it
directly before creating the repo. Backup names: CoprimeNull, BlindPrime.

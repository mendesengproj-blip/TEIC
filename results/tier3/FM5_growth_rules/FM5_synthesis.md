# FM5 — growth-rule FORMS: the e7 dimensional death generalises

> Charter: `docs/prompts/FM5_GROWTH_RULES.md` (kill criteria pre-registered).
> Item 14 (Seção 6) of `RESEARCH_MAP.md` / FM5 of `FUTURE_EXPERIMENTS.md`.
> Data/code: `FM5_growth_rules.py`, `FM5_growth_rules.json`. Run jun/2026.

## Verdict: **DEATH GENERALISES** — no rule form yields manifold-like d*≈4

T3A/T3B killed dimensional emergence for the **e7 rule** (binary weight, d*≈1.43,
non-manifold). T3A-3 swept its **coupling** w_meet (all d≈1.3, none →4). FM5 closes the
remaining axis — the **functional FORM** of the rule, graded by the number of connected
components of the chosen past-ideal (a genuine extension: the binary e7 form cannot tell
2 components from 10).

| Rule form | weight w(nc) | d_int | d_glob | r | manifold? | near 4? |
|---|---|---|---|---|---|---|
| R0 binary (e7) | w_meet if nc≥2 else 1 | 1.395±0.10 | 2.30 | 0.41 | no | no |
| R1 penalise 0.33 | 0.33^(nc−1) | 1.402±0.08 | 2.39 | 0.38 | no | no |
| R1 penalise 0.6 | 0.6^(nc−1) | 1.297±0.08 | 2.14 | 0.45 | no | no |
| R2 reward ×2 | 2^(nc−1) | 1.371±0.06 | 2.40 | 0.37 | no | no |
| R2 reward ×3 | 3^(nc−1) | 1.419±0.11 | 2.30 | 0.41 | no | no |
| R2 reward ×5 | 5^(nc−1) | 1.310±0.18 | 1.90 | 0.56 | no | no |

- **G0 PASS:** R0 reproduces T3A's d*≈1.43 and its non-manifold signature (d_int≠d_glob).
- **Every form** stays at d_int≈1.3–1.4 with d_int≠d_glob (non-manifold); **none** is
  manifold-like, **none** approaches 4. The pre-registered death criterion ("all forms
  d far from 4 and/or non-manifold") is met.

## The instructive surprise (honest)

The hypothesis was that **rewarding** components (R2, c>1) would favour wide-antichain
pasts and push d **up**. It did the **opposite**: the strongest reward (×5) gave the
**lowest** d_int (1.31) and the **highest** ordering fraction (r=0.56) — i.e. a *more*
chain-like, *more* ordered causet. Strongly up-weighting multi-component pasts in the
MCMC does not build a wide manifold; it drives a different ordered structure. So the
rule designed to reach high d fails most clearly — strengthening the negative: the
dimensional death is not a fine-tuning artefact of the e7 form, it is robust across the
component-graded family in **both** directions.

## Scope / honesty
Tests the **component-graded subfamily** (a genuine form-extension of the binary e7
rule), **not** the full Rideout–Sorkin/CSG family parametrised by the coupling sequence
t_n — that remains a larger future step. The MCMC ideal sampler and the connected-
component bookkeeping are validated **rule-independently** by the T3V gate (only the
Metropolis acceptance ratio w_new/w_old changes; detailed balance holds for any w(nc)).
No d=4 target in the generator; fixed seeds; guard `test_no_circularity.py` passes.

## RESEARCH_MAP update
- Seção 6 item 14 (FM5): [NUNCA TENTADO] → **EXECUTADO**; the e7 dimensional death
  (T3A/T3B, a [MORTO]) is now shown **robust to the rule form**, not just the coupling.
  Residual: the full CSG coupling-sequence family (larger, optional).

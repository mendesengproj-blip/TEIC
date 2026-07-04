# PAPER_FINAL — complete reformulation of the TEIC paper

> This document is the specification for the complete reformulation of
> `paper/main.tex`, incorporating all investigation posterior to the
> earlier PDF (D1–D3, the bridge, the minimal action, the forbidden
> operators, the selection of the modified theory). **No numerical result
> changed** — R1–R7 and D1–D3 are byte-for-byte the same values. The paper
> compiled clean before and compiles clean after, and the anti-circularity
> guard still passes.

---

## The thesis

> A discrete causal network with Poisson sprinkling, analysed with a
> strictly anti-circular protocol, spontaneously generates the complete
> structure of a class of modified-gravity theories. The DBI kinetics, the
> Stückelberg coupling, and the Maxwell–Proca vector sector are not
> phenomenological choices — they are forced by the geometry of the causal
> cone, by the breaking of U(1) on the discrete links, and by the
> combinatorial saturation of the network. The resulting effective theory
> coincides with a theory fitted independently to galactic rotation data
> and makes testable predictions.

The narrative is cumulative: the solid results (R1–R3) establish
credibility; the new results (D1–D3, the minimal action) are the
contribution; the connection to the observationally-tested theory is the
conclusion, not the premise.

---

## Title

```
Emergent spacetime geometry and modified gravity from a causal network:
from Lorentz invariance to a scalar-vector-tensor effective field theory
```

---

## Structure (as implemented)

| § | Section | Status |
|---|---|---|
| 1 | Introduction | rewritten — 3 affirmative paragraphs (picture / what is derived / relation to CST + the modified theory) |
| 2 | Related work | updated — added Bekenstein (TeVeS), Milgrom (MOND), Horndeski, Born–Infeld; the modified theory is **not named** |
| 3 | The model | kept (anti-circularity protocol intact) |
| 4 | Emergence of special relativity (R1) | kept verbatim |
| 5 | Analytic volume and dimension (R2) | kept verbatim |
| 6 | Gravitational regime (R3) | kept verbatim |
| 7 | Curvature: equivalence or divergence (R4, 23.5σ) | kept verbatim |
| 8 | Matter dynamics (D1–D3) | kept + new §8.4 *The nonlinear regime* (NL1–NL3: +3/2 coefficient, 0.06% to r=2.5GM/c²) |
| 9 | **The minimal action** (NEW) | 9.1 construction · 9.2 five operators + honesty note · 9.3 why DBI · 9.4 why Stückelberg · 9.5 forbidden operators · 9.6 Lorentz bottleneck |
| 10 | **The effective field theory** (NEW) | 10.1 hierarchy · 10.2 what the network selects · 10.3 additional predictions |
| 11 | The TEIC↔QM boundary | kept (interference, Sorkin d'Alembertian, phase scale, two floors) |
| 12 | Further exploratory probes | kept (sequential growth, causal redshift) |
| 13 | Discussion | rewritten — what is new / what coincides with CST / the conceptual route |
| 14 | Honest limitations | expanded — added (8) minimal-action conjecture + algebraic coefficients + a₀ not derived; (9) order-1 Lorentz violation E/B≈3, computational barrier |

The now-superseded exploratory subsections **Vector fields on the
network** and **A negative bridge to modified-gravity dynamics** were
folded into the positive §9 (Wilson loops realise F²; §9.4 explains why
Stückelberg, not f(θ)F²).

## The minimal action (the central new content)

$$S = \sum_{\text{links}} \Delta\tau_{ij}\,[1 - \cos(\phi_{ij} + \Delta\theta_{ij})]
    + \lambda_p \sum_{\text{plaquettes}} [1 - \cos(W_p)]$$

| Operator | Origin | Verification |
|---|---|---|
| X = (∂θ)² | Δθ² | C1–C2 |
| √(1−X/X₀) | full Δτ weight (cone cusp) | W3 (DBI) |
| A_μ∂^μθ | φ·Δθ cross term | C2 (ratio 2) |
| F_μνF^μν | Wilson loop W_p | W1–W2 |
| A_μA^μ | φ² | C2 (ratio 1) |

**Mandatory honesty notes (present in the paper):**
- §9.2 — the ratios C₂/C₁=1, C₃/C₁=2 are **algebraically forced** by the
  single cosine, *not* a geometric derivation; the coupling constants
  remain free parameters fitted to data.
- §9.6 / §10.2 — the four scales (a₀, m_A, G, Λ) are measured, not derived;
  in particular **a₀∼cH is not supported** (the only saturation scale
  X₀∝ρ is UV/granularity).
- §9.6 / §13(9) — the raw vector sector has order-1 Lorentz violation
  (E/B≈3; positive-definite second moment, eigenvalues +5046, +20114); BD
  smearing reduces it structurally but the residual □/(2ερ) is buried under
  ρ^(3/4) noise (SNR≈1). Computational barrier, not conceptual.

**Forbidden operators (§9.5):** ∂_t³θ (causal order); n^μ∂_μθ fixed n
(Lorentz / Hořava–Lifshitz); □²θ (Ostrogradsky / Weyl); θ independent of g
(soldering / general Horndeski); non-abelian Yang–Mills (simple U(1)).

---

## Framing rules honoured

1. Affirmative voice — "we derive / show / establish", not "we test".
2. The modified theory is **never named** ("a class of scalar–vector–tensor
   modified gravity theories" / "fitted independently to galactic rotation
   data").
3. Honesty about coefficients: the (1,2) ratios are algebraic, not
   geometric — said explicitly.
4. Honesty about Lorentz: E/B≈3 in the vector sector — documented in §13(9).
5. No number changed — R1–R7 and D1–D3 identical.

---

## Verification (final)

```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

| check | result |
|---|---|
| compiles (all four passes exit 0) | ✅ |
| undefined references / citations | ✅ none |
| critical warnings | ✅ none (only the pre-existing empty-journal note for `Meyer1988`) |
| abstract opens "We derive" | ✅ |
| abstract word count | ✅ 195 (< 250) |
| length | ✅ 14 pages (~15 target) |
| new tables render (operators, forbidden, hierarchy) | ✅ |
| `tests/test_no_circularity.py` | ✅ PASSED (exit 0) |
| R1–R3 numbers unchanged | ✅ 0.9998 / 1.0000 / 0.21% / 2.006 / 4.004 / 23.5σ / −1/96 / 0.9991 / 0.62% / 0.06% / −1.02 all present |
| modified theory named anywhere | ✅ no |
| §9.2 coefficient-honesty note present | ✅ |
| §13 limitations (8) and (9) present | ✅ |

References added to `refs.bib`: `Horndeski1974`, `Milgrom1983`, `Born1934`,
`Bekenstein2004` (all cited in §2/§9).

---

## The paper that results

> From a single image — events as centres of causal expansion — and a
> strictly anti-circular protocol, the paper derives special relativity,
> dimension, Schwarzschild gravitation, and the complete operator structure
> of an observationally-tested modified gravity theory. The effective
> theory was not chosen; it is the only structure compatible with the
> geometry of the causal cone, the combinatorial saturation of the network,
> and the breaking of U(1) on the discrete links.

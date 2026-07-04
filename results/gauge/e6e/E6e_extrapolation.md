# E6e — Curvature extrapolation of E6c (analytic, no new Monte Carlo)

> Reads `results/gauge/e6c/E6c_1_curvature_scan.json` and fits curves to the measured
> frac_B(R̂) and b²/e²(R̂). Code: `E6e_extrapolation.py`. Data: `E6e_extrapolation.json`.
> Figure: `E6e_extrapolation.png`. Run jun/2026. Does NOT modify any earlier campaign.

## Input data (E6c, h=4, N=2000, pooled 3 seeds)

| R̂ | R_dS | 1/R̂ | frac_B | ±err | b²/e² |
|---|---|---|---|---|---|
| ∞ (Mink.) | — | 0 | 0.00255 | 0.00030 | 0.112 |
| 16 | 13.45 | 0.0625 | 0.00273 | 0.00031 | 0.228 |
| 8 | 6.73 | 0.125 | 0.00326 | 0.00034 | 0.480 |
| 4 | 3.36 | 0.25 | 0.00531 | 0.00044 | 0.814 |
| 3 | 2.52 | 0.333 | 0.00749 | 0.00052 | 0.903 |
| 2 | 1.68 | 0.5 | 0.01169 | 0.00064 | 0.968 |

**Honesty correction to the charter's premise.** The charter feared "only one positive point
(R̂=2)". In fact E6c has **five** finite-curvature points with small binomial errors and a
clean monotone signal, so the fit is **well-conditioned** (max parameter uncertainty 17%, far
below the 50% ill-conditioning flag). The "rodar 2-3 pontos antes de extrapolar" contingency
is therefore NOT the situation we are in — though a couple of points at R̂<2 would still firm
up the law (below).

## Models and fits

Two treatments. **Direct**: fit frac_B(R̂) on the 5 finite points. **Excess**: fit the
curvature-INDUCED part Δ = frac_B(R̂) − frac_B(∞) (the Minkowski floor 0.00255 is the
flat-space E6b tail, curvature-independent; power/quadratic through the origin cannot
represent it, so the excess is the physically clean target). Weighted by binomial errors.

```
                       R²      χ²_red   max σ_rel   params                R̂ @ frac=(0.05, 0.10, 0.50)
DIRECT frac_B:
  power  a(1/R̂)^α     0.958    3.96      8%        a=0.019, α=0.81        0.30, 0.13, 0.02
  exp    a·e^(−bR̂)    0.751   18.09     10%        a=0.011, b=0.128       — , — , —   (saturates < 0.05)
  quad   a(1/R̂)²      0.575   37.36      4%        a=0.057                1.07, 0.75, 0.34
EXCESS Δ = frac − floor   (the physically clean fit):
  power  a(1/R̂)^α     0.997    0.23     17%        a=0.031, α=1.73        0.78, 0.51, 0.20
  exp    a·e^(−bR̂)    0.995    0.68     19%        a=0.028, b=0.568       — , — , —   (saturates < 0.05)
  quad   a(1/R̂)²      0.984    0.74      5%        a=0.039                0.91, 0.63, 0.28
```

**Best fit: the curvature excess Δ ∝ (1/R̂)^1.73, R²=0.997** — i.e. the magnetic fraction
that curvature ADDS scales as roughly **(1/R̂)² = the curvature H²** (the fixed-exponent
quadratic gives R²=0.984, statistically as good given the errors). This is the physically
expected leading-order curvature correction. Both power and quadratic are well-conditioned.

## Extrapolation to O(10%)

Reading the R̂ that yields frac_B = 0.10 across the well-fitting (power, quad; direct + excess)
models:

```
  direct power : R̂ ≈ 0.13      excess power : R̂ ≈ 0.51
  direct quad  : R̂ ≈ 0.75      excess quad  : R̂ ≈ 0.63
  -> median R̂ ≈ 0.57,  full range 0.13 – 0.75
```

Every model that can reach 0.10 puts it at **R̂ < 1** — i.e. curvature radius **below the mean
spacing ℓ**. For the three targets (excess fits, the cleanest):

```
  frac_B = 0.05  ->  R̂ ≈ 0.78 – 0.91
  frac_B = 0.10  ->  R̂ ≈ 0.51 – 0.63
  frac_B = 0.50  ->  R̂ ≈ 0.20 – 0.28
```

**The exponential model is the pessimistic outlier:** with R²≈0.99 it fits the points almost
as well but is **bounded above by its amplitude a≈0.028** — under an exponential-in-R̂ law,
frac_B can **never exceed ~3%** at any curvature. So one of the two best-fitting functional
forms says O(10%) is reachable only at R̂≈0.5–0.6, and the other says it is **unreachable at
any curvature**. Both readings agree on the operative conclusion (below).

## b²/e² (per-cell magnetic content)

The mean per-cell b²/e² reaches **1** (the *average* diamond on the light cone, E²=B²) at
**R̂ ≈ 1.9–2.2** (power/exp fits) — essentially at the R̂=2 already measured. Yet frac_B is
only ~1.2% there: the b²/e² distribution is tight just below 1 with a thin spacelike tail, so
the *mean* crossing the light cone does not make a large *fraction* of cells magnetic. Pushing
a large fraction over requires far stronger curvature than pushing the mean over — consistent
with the frac_B extrapolation landing at R̂<1.

## Physical scale  [EXTERNO/ASSUMIDO]

R̂ = R_dS/ℓ with ℓ = ρ^(−1/4) the mean spacing. Identifying the **discreteness scale with the
Planck scale** (ℓ ≡ ℓ_Planck) — the standard causal-set assumption, declared external — makes
R̂ the curvature radius in Planck units. Then **R̂ < 1 means a curvature radius below the
Planck length**: the de Sitter radius is sub-Planckian and the continuum/sprinkling
approximation is at or beyond its validity floor (curvature varies appreciably within one
fundamental cell). The required R̂ ≈ 0.5–0.6 for O(10%) is therefore **near-/sub-Planckian**.

## What this means (carried to the synthesis)

O(10%) needs R̂ ≈ 0.5–0.6 (< 1, sub-Planckian); O(50%) needs R̂ ≈ 0.2–0.3 (trans-Planckian).
The observable universe has R̂ astronomically large, where frac_B = the flat tail ≈ 0. So the
curvature mechanism, though real and cleanly ∝1/R̂², delivers an O(1) magnetic sector only at
Planck-scale curvature — a **physical frontier**, not merely a technical one. The fit is
well-conditioned, so this is not the "need more points" branch; a confirmatory E6e at
R̂=1.5,1.0,0.5 would verify the ∝1/R̂² law inside the valid continuum regime but would confirm
a Planck-scale requirement, not bring the photon within reach. Verdict in `E6e_synthesis.md`.

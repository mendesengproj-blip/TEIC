# E6e — CURVATURE EXTRAPOLATION: what R̂ would give an O(1) photon?

> ANALYTIC task — no new Monte Carlo. Extends E6c. Executed jun/2026. Results in
> `results/gauge/e6e/`. Result goes to RESEARCH_MAP.md. Modifies no earlier campaign.

## Goal

Use E6c's measured frac_B(R̂) and b²/e²(R̂) to estimate the curvature R̂ that would give
frac_B ≈ O(10%), and decide whether that R̂ is physically reasonable (sub-Planckian, worth a
full E6e MC) or trans-Planckian (a physical, not merely technical, frontier). Fit three
models (power, exponential, quadratic in 1/R̂²), pick the lowest-residual, extrapolate to
frac_B = 0.05, 0.10, 0.50. **If a fit is ill-conditioned (parameters uncertain >50%), report
that and name the extra R̂ that would resolve it — do NOT extrapolate with false precision.**

## Pre-registered criterion

```
SUCCESS  : frac_B~O(10%) at R̂≈0.5–5 (sub-Planckian, not absurd) -> run full E6e MC at R̂<2.
DEATH    : frac_B~O(10%) needs R̂<0.1 (trans-Planckian) -> physical frontier, E6 closes.
INCONCL. : fit ill-conditioned (params >100% / too few points) -> name the extra R̂ needed.
(Charter Passo 4: R̂~0.1–1 for O(10%) -> [FRONTEIRA FÍSICA], sub-/near-Planckian.)
```

## Outcome — [FRONTEIRA FÍSICA]

The fit is **well-conditioned** (E6c has 5 clean finite points, σ_rel≤17% — not the feared
single point). The curvature **excess** Δfrac_B = frac_B − Minkowski floor fits
**∝(1/R̂)^1.73, R²=0.997 ≈ H²** (quadratic R²=0.984). Extrapolation: **O(10%) needs R̂≈0.5–0.6**
(range 0.13–0.75), O(50%) R̂≈0.2–0.3, O(5%) R̂≈0.8–0.9 — **all R̂<1** (curvature radius below
the mean spacing ℓ ≡ ℓ_Planck, **[EXTERNO/ASSUMIDO]**). The exponential model (R²≈0.99)
**saturates at ~3%** → under that reading O(10%) is unreachable at any curvature. Mean b²/e²
reaches 1 at R̂≈1.9–2.2 (≈ the measured R̂=2), yet frac_B is only ~1.2% there.

**Verdict [FRONTEIRA FÍSICA]:** not the hard structural death (R̂≪0.1), but the O(1) magnetic
sector via curvature needs **Planck-scale curvature**; the observable universe (R̂ enormous)
has frac_B≈0, so this mechanism **does not explain the photons of the low-curvature observable
universe**. A full E6e MC at R̂<2 is **not recommended** as a photon search (the analytic answer
is already Planck-scale); a small confirmatory run at R̂=1.5,1.0 would only verify the ∝1/R̂²
law inside the valid continuum. The live problem returns to an O(1) magnetic 2-cell at **low**
curvature (anisotropic/inhomogeneous geometry, or a new 2-cell) — height, isotropic curvature,
and order-coupling are all exhausted. Full analysis: `results/gauge/e6e/E6e_synthesis.md`.

## Deliverables

```
results/gauge/e6e/
  E6e_extrapolation.py    — fit (3 models, weighted) + conditioning + extrapolation + figure
  E6e_extrapolation.json  — fit parameters, R², uncertainties, extrapolated R̂
  E6e_extrapolation.png   — frac_B vs curvature with fits + extrapolation; b²/e² panel
  E6e_extrapolation.md    — analysis
  E6e_synthesis.md        — verdict and recommendation
RESEARCH_MAP.md           — E6 row updated with the required-R̂ estimate
```

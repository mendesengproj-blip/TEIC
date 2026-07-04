# LV1 — the E/B split is not a preferred-frame effect at the plaquette level

**Task.** Test whether the per-plaquette electric dominance behind W2's E/B ≈ 3 is a
frame statement at all. Generator `LV1_invariant.py`, data `LV1_invariant_data.json`.
Ensemble identical to W2/AB2: ρ=12, extent 4⁴, margin 0.25, 20 seeds, 12 941 plaquettes.

## The exact structure of a causal plaquette

For a causal-diamond loop (p, j, l, k) the closed-quadrilateral identity gives

$$\Omega \;=\; \tfrac12\,(l-p)\wedge(k-j)\;=\;\tfrac12\,d_1\wedge d_2,$$

with **d₁ timelike-future** (p ≺ j ≺ l is a causal chain) and **d₂ spacelike** (j, k are
mutually spacelike by construction of the loop). So every causal plaquette is a *simple*
bivector spanning a *timelike plane*, and the Lorentz invariant

$$I=\tfrac12\,\Omega_{\mu\nu}\Omega^{\mu\nu}=b^2-e^2
=\tfrac14\big[(d_1\!\cdot\!d_1)(d_2\!\cdot\!d_2)-(d_1\!\cdot\!d_2)^2\big]<0$$

is **strictly negative** (timelike·spacelike < 0). Equivalently e² − b² = (proper area)²
> 0: electric dominance per plaquette, **in every frame**, by causality alone.

## Measured (12 941 plaquettes, nothing inserted)

| quantity | value | meaning |
|---|---|---|
| max \|Pf(Ω)\|/(e²+b²) | 7.6×10⁻¹⁶ | every bivector exactly simple (identity) |
| frac(I ≥ 0) | **0.0000** (max I = −1.1×10⁻⁴) | timelike plane without exception |
| dominance r=(e²−b²)/(e²+b²) | median 0.39, [q05 0.09, q95 0.89] | invariant, broad |
| ensemble E/B | **2.987 ± 0.028** | reproduces W2 (2.97), AB2 (3.25) |

## Verdict

**PASS (theorem confirmed exactly).** The per-plaquette part of the "Lorentz violation"
is not a violation: e² > b² holds pointwise, invariantly, because causal loops span
timelike planes. A Lorentz-*invariant* ensemble of such plaquettes still has every
member electric-dominated; E/B = 1 was never the LI expectation for *positive* plane
weights (this is BD1's positive-definiteness diagnosis seen from the invariant side).
The genuine LV question is therefore **where the ensemble weights come from** (LV2:
boost covariance; LV3: orbit truncation) and **what the full action sees** (LV4).

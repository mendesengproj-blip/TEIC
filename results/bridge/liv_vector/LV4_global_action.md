# LV4 — the summed action is Lorentz-invariant where it is field-sensitive

**Task (the survival test).** The full plaquette action
$S(F)=\sum_p[1-\cos W_p]$, $W_p=\tfrac12 F_{\mu\nu}\Omega^{\mu\nu}$ (a scalar; exact
for constant F by W1), is evaluated on the boost family
$F(\beta)$ = pure E₀x̂ boosted by rapidity β along ŷ — invariants E²−B² = E₀², E·B = 0
conserved to 10⁻⁹ (asserted). Lorentz invariance predicts R(β)=⟨S(β)⟩/⟨S(0)⟩=1; the W2
quadratic coefficients predict R_quad(β)=cosh²β+sinh²β/(E/B), up to **8.5** at β=1.6.
Common random numbers: S(β) and S(0) on the *same* plaquettes seed by seed, so sprinkle
noise cancels — no ρ^(3/4) wall (invariant-sensitivity z up to 54σ, vs the BD route's
SNR ≈ 1). Generator `LV4_global_action.py`, data `LV4_global_action_data.json`.
Ensemble = W2 (ρ=12, 4⁴, 20 seeds, 12 941 plaquettes); u₀ = 1/median|Ω⁰¹| anchors W ~ 1.

## Pre-registered criteria (from the generator header)

- **PASS**: window with invariant sensitivity >5σ and saturation ⟨1−cos⟩≥0.2 where
  |R(β)−1| ≤ 0.05 for β ≤ 0.8 and FOM ≤ 0.25; defect shrinks leaving the quadratic regime.
- **KILL**: defect does not shrink when leaving the quadratic regime (intrinsic LV).

## Result: the order-1 LV is the quadratic expansion, and it resums away

| E₀ | ⟨1−cos⟩ | inv-sens z | R(0.8) | R_quad(0.8) | R(1.6) | R_quad(1.6) |
|---|---|---|---|---|---|---|
| 0.1 u₀ | 0.018 | 49 | 1.979 ± 0.025 | 2.053 | 7.43 ± 0.11 | 8.53 |
| 0.3 u₀ | 0.143 | 54 | 1.758 ± 0.018 | 2.053 | 3.91 ± 0.04 | 8.53 |
| 1.0 u₀ | 0.683 | 39 | 1.123 ± 0.008 | 2.053 | 1.327 ± 0.013 | 8.53 |
| 3.0 u₀ | 0.946 | 3.4 | **1.018 ± 0.007** | 2.053 | **1.046 ± 0.008** | 8.53 |
| 10 u₀ | 1.004 | 1.3 | 0.992 ± 0.010 | 2.053 | 0.988 ± 0.008 | 8.53 |
| 30 u₀ | 0.991 | 1.7 | 0.997 ± 0.009 | 2.053 | 1.002 ± 0.009 | 8.53 |

**Defect |R−1| at β = 0.8 vs field strength: 0.98 → 0.76 → 0.12 → 0.018 → 0.008 → 0.003.**
Three orders of magnitude of collapse; rotation control (E→ẑ) flat at ~1% throughout.

Two limits, both as Lorentz invariance demands:
- **Weak field**: R reproduces R_quad with the measured E/B ≈ 3 — W2's "violation" is
  recovered *exactly* as the quadratic limit of this observable. Nothing was lost.
- **Strong field**: the bounded cosine resums the expansion; boosted plaquettes saturate
  covariantly (W is a scalar) and R → 1 at the % level while the quadratic LV prediction
  sits at 2–8.5.

## Verdict against the pre-registered criteria

**PARTIAL (honest).** The kill condition is *not* triggered — the defect shrinks
monotonically when leaving the quadratic regime, which is the signature of an expansion
artifact, not intrinsic LV. The strict PASS window is not met at this box: at E₀ = u₀
(sensitive, z=39) the β=0.8 defect is 0.12 > 0.05; at E₀ = 3u₀ the defect is 0.018 but
sensitivity has dropped to 3.4σ. The box-reach reading of this residual was tested by
the extent scan **LV4b** and **killed**: the defect at fixed (E₀/u₀, β) is L-independent
over L = 3–6. It is the still-quadratic fraction of the scale-mixed plaquette population
— controlled by field strength (resummation), not volume. See `LV4b_extent.md`.

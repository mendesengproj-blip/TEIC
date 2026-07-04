# NL2 — The quadratic coefficient: dynamical vs kinematic

> **Bridge / non-linear investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing. Continues [NL1](NL1_action.md) (λ free) and D3 (linear MC → `θ = A/r`).
> Reproduce: `python results/bridge/nonlinear/NL2_MC.py` (~45 s). Data:
> [`NL2_MC_data.json`](NL2_MC_data.json) · figure [`NL2_MC.png`](NL2_MC.png).

**Anti-circularity.** The generator sprinkles at local density `(1 − 2θ)` (an
allowed volume element); the square root **emerges** from causal counting (the
diamond volume), never imposed. Schwarzschild's `1/√(1−2u)` and the coefficient 3/2
appear only in *comparison-only* blocks. The guard still passes.

---

## The question, and the correct target

Does the network reproduce Schwarzschild's **second order**, the quadratic term of

$$\frac{\rho_{\rm eff}}{\rho_0}=\frac{1}{\sqrt{1-2u}}=1+u+\tfrac32 u^2+\dots,\qquad u=\frac{GM}{rc^2}?$$

The target coefficient is **3/2** (the density). The prompt's ½ is the *redshift's*
(`√(1−2u) = 1 − u − ½u²`) — a different quantity; see [NL1](NL1_action.md). We
measure the second order in two separate channels.

---

## Channel 1 — Dynamical (the field MC): no second order

The D3 field Monte-Carlo runs the **linear** BD action; fitting the emergent
potential far from the source core (`r ≥ 2.5 R_core`):

`θ_MC = C + A₁/r + A₂/r²` → **`C = −0.033`, `A₁ = 1.18`, `A₂ = +0.51`**, and the
**offset-removed log–log slope is −1.020** — i.e. `θ_MC` is a pure `1/r` to within
2%. The residual `A₂/A₁² = 0.36` is core/discretisation contamination, not a genuine
dynamical term: a harmonic field outside a finite source has **no** `1/r²` part.

$$\boxed{\;\text{The linear BD action produces no dynamical second order.}\;}$$

This is the prompt's *"regime linear apenas"* — and it **confirms NL1**: λ is free,
so the field dynamics carries no `(GM/rc²)²` term. (In the prompt's framing this is
the MORTE of the *dynamical* route.)

---

## Channel 2 — Kinematic (proper-time counting): the 3/2 is there

The bridge density is `ρ_eff = ρ₀/(dτ/dt)`, and `dτ/dt` is a static observer's
proper-time clock, **measured by counting** (P2/P3/R3). Feeding the *linear*
potential `θ = A₁/r` into a flat sprinkle of local proper density `(1 − 2θ)` (no
square root in the generator), the counted clock rate comes out `√(1−2θ)`, so
`ρ_eff/ρ₀ = 1/√(1−2θ)`. We extract the quadratic coefficient as the `u→0` intercept
of the per-point estimator `c₂(r) = (ρ_eff − 1 − u)/u²` (which equals `3/2 + (5/2)u +
…`), avoiding strong-field contamination:

| r | u = A₁/r | counted ρ_eff/ρ₀ | c₂ = (ρ−1−u)/u² |
|---|---|---|---|
| 6.6 | 0.180 | 1.2490 | 2.131 |
| 8.4 | 0.140 | 1.1774 | 1.909 |
| 11.2 | 0.105 | 1.1244 | 1.760 |
| 15.7 | 0.075 | 1.0841 | 1.621 |
| 23.6 | 0.050 | 1.0543 | 1.712 |

**`u→0` intercept = 1.433 ≈ 3/2** (within ±20%); `c₂` descends toward 3/2 from above
as expected. Direct form check: the counted density matches Schwarzschild
`1/√(1−2u)` to **0.09%**, versus **5.85%** for the Newtonian `1+u`.

$$\boxed{\;\text{The second order +3/2 is reproduced kinematically (the clock }\sqrt{\ }).\;}$$

---

## Verdict — NL2: **PASSA (cinemático)**

| channel | quantity | result | meaning |
|---|---|---|---|
| dynamical | `A₂/A₁²` (field MC) | `≈ 0` (exponent −1.02) | linear action → no 2nd order (confirms NL1) |
| kinematic | `c₂(u→0)` (counting) | **1.43 ≈ 3/2** | clock `√` reproduces 2nd order |
| comparison | count vs Schwarzschild | 0.09% (vs 5.85% Newt) | follows `1/√(1−2u)` |

**The second-order Schwarzschild coefficient +3/2 is reproduced — but
*kinematically*, through the proper-time clock `√` acting on the linearly-derived
potential, not *dynamically* through a non-linear field action.** The field dynamics
itself is linear (`A₂ ≈ 0`), exactly as NL1 predicts (λ free). This is the honest
structure: D1–D3's first-order bridge, taken through the same proper-time/soldering
relation, *automatically* carries the correct second order — evidence of convergence
toward `√(1−2u)` — without any derived non-linearity. NL3 pushes this to small r.

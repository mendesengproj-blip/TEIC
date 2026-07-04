# BRIDGE_NONLINEAR — beyond the weak field: the second order of Schwarzschild

> **Independent investigation.** This does **not** modify R1–R3 or e6–e11, and is
> not part of the TEIC paper. It continues [`BRIDGE_DYNAMICS.md`](BRIDGE_DYNAMICS.md)
> (D1–D3, first order) and [`BRIDGE_RHO.md`](BRIDGE_RHO.md) (P1–P3, kinematic).
> All artefacts live in [`results/bridge/nonlinear/`](results/bridge/nonlinear/).

**Central rule (anti-circularity).** Schwarzschild, `G`, `GM/r`, and `√(1−2M/r)`
enter **only in the final comparison** — never in the generator. The generators
sprinkle at the volume element `(1 − 2θ)` (no square root); the `√` of the clock
**emerges** from causal counting. The main guard (`tests/test_no_circularity.py`)
still **passes**.

---

## The question

D1–D3 established the bridge at **first order**: `ρ_eff/ρ₀ = 1 + GM/rc²`,
`θ = GM/rc²`. Schwarzschild's density is

$$\frac{\rho_{\rm eff}}{\rho_0}=\frac{1}{\sqrt{1-2u}}=1+u+\tfrac32 u^2+\tfrac52 u^3+\dots,\qquad u=\frac{GM}{rc^2}.$$

Does the non-linear theory capture the **second order**, the `(3/2)u²` term? (The
correct coefficient is **+3/2** — the density's; the prompt's ½ is the *redshift's*,
`√(1−2u) = 1 − u − ½u²`, a different quantity. See NL1.)

Three tasks: NL1 analytic (decides if the non-linear coefficient λ is geometric or
free); NL2/NL3 numerical (independent of NL1).

---

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **NL1** — non-linear action (analytic) | is λ fixed by the BD action? | **λ LIVRE** — the smeared BD action is *quadratic*; it contains no `φ³`/`(∇θ)²` term. `λθ²` gives a *log*, not `1/r²`; the gradient coupling `λ(∇θ)²` gives `1/r²` and matches 3/2 at `λ=3`, but λ is **not** fixed by BD. Geometric non-linearity lives in the `−½Rφ` back-reaction (open frontier). |
| **NL2** — quadratic coefficient (MC) | measure `A₂/A₁²` | **PASSA (cinemático)** — *dynamical* `A₂ ≈ 0` (linear action, exponent −1.02, confirms NL1); *kinematic* `c₂(u→0) = 1.43 ≈ 3/2` (count vs Schwarzschild **0.09%** vs Newtonian 5.85%). |
| **NL3** — profile at small r | which curve fits ρ(r)? | **PASSA** — counted density follows full Schwarzschild to **0.06%** (vs Newtonian 17%, truncated 11%); 2nd-order gap fully captured; right sign; horizon left open. |

Detail per task:
[`NL1_action.md`](results/bridge/nonlinear/NL1_action.md) ·
[`NL2_quadratic.md`](results/bridge/nonlinear/NL2_quadratic.md) ·
[`NL3_profile.md`](results/bridge/nonlinear/NL3_profile.md).

---

## The result — and what kind of result it is

> **The bridge density converges to Schwarzschild `ρ₀/√(1−2u)` beyond the weak
> field — reproducing the +3/2 second-order coefficient and the full profile to
> 0.06% at small r — but *kinematically*, through the proper-time clock `√` acting
> on the linearly-derived potential, NOT *dynamically* through a derived non-linear
> action.**

The honest anatomy, order by order:

| | first order | second (and higher) order |
|---|---|---|
| **dynamical** (BD field action) | `θ = GM/rc²` derived (D1–D3) | **absent** — the action is linear (NL1: λ free; NL2: `A₂≈0`) |
| **kinematic** (proper-time clock `√`) | `ρ_eff/ρ₀ = 1 + u` | **`1/√(1−2u)`**, carrying `3/2 u²` and beyond (NL2/NL3) |

The non-linearity of `ρ_eff(r)` is the **clock**, not the field: the same
proper-time/soldering relation `ρ_eff = ρ₀/(dτ/dt)` that gave first order
*automatically* carries the correct second order (and the whole `√`), because the
diamond-volume counting produces `√(1−2θ)` exactly (P2/P3, corr ≈ 1.0). The field
that sources it remains linear.

---

## Consistency with D3 / R3 / P2 (required, and met)

- Far-field `θ_MC = A₁/r` with offset-removed exponent **−1.02** — identical to D3.
- Kinematic counting reproduces P2's `ρ_eff = ρ₀/√(1−2θ)` (the same estimator as
  R3's clock rate, inverted), now applied to the *emergent* linear potential rather
  than the imposed Schwarzschild profile (P2/P3).
- The first-order coefficient is unit (`A₁ = M` in calibrated units), as in D1–D3.

---

## What this does — and does not — change for the paper

**Strengthened (publishable):** *the bridge density `ρ₀/√(1−2GM/rc²)` is reproduced
beyond first order — the +3/2 second-order coefficient and the full small-r profile
(to 0.06%) — by free Monte-Carlo (no ansatz), via the proper-time clock acting on
the dynamically-derived linear potential.* The TEIC→DEV scalar bridge is
**dynamically derived at first order and kinematically convergent to all orders of
Schwarzschild** in the perturbative (sub-horizon) regime.

**Not claimed (honest bottleneck, precisely located):**
1. **A *dynamical* derivation of the non-linearity.** λ is free (NL1); the BD action
   is quadratic and carries no `(GM/rc²)²` term. The genuine geometric non-linearity
   is the `−½Rφ` curvature back-reaction — the causal-set Einstein / Regge sector —
   the **open frontier**, not contained in the action as used.
2. **The horizon.** `r → 2M` (`u → 1/2`) needs `ρ₀ → ∞` (the diamond shrinks,
   per-shell counts vanish): `N ≫ tractable`. Left explicitly **open**; no horizon
   claim. NL3 stops at `r ≥ 2.5 M`.

So the second order is *evidence of convergence*, obtained kinematically — exactly
the goal the prompt set ("evidência de convergência, não a solução exata"), with the
mechanism (clock, not field) identified honestly.

---

## Reproduce

```bash
python results/bridge/nonlinear/NL1_action.py     # lambda geometric or free? ~3 s
python results/bridge/nonlinear/NL2_MC.py         # A2/A1^2: dynamical vs kinematic; ~45 s
python results/bridge/nonlinear/NL3_profile.py    # small-r profile vs 3 curves; ~30 s
python tests/test_no_circularity.py               # guard still passes (exit 0)
```

Outputs (seeded, self-describing): `NL1_action_data.json`, `NL2_MC_data.json`,
`NL3_profile_data.json`, and figures `NL2_MC.png`, `NL3_profile.png` in
`results/bridge/nonlinear/`.

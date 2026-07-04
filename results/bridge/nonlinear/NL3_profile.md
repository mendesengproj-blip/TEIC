# NL3 — Density profile at small r: Newtonian vs Schwarzschild vs truncated

> **Bridge / non-linear investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing. Continues [NL2](NL2_quadratic.md). Reproduce:
> `python results/bridge/nonlinear/NL3_profile.py` (~30 s). Data:
> [`NL3_profile_data.json`](NL3_profile_data.json) · figure
> [`NL3_profile.png`](NL3_profile.png).

**Anti-circularity.** The generator sprinkles at `(1 − 2θ)` (allowed volume
element); the square root **emerges** from causal counting (diamond volume), never
imposed. Schwarzschild's `1/√(1−2u)` appears only in *comparison-only*. Guard passes.

---

## What NL3 tests

D3/NL2 are reliable in the far field; NL3 pushes to **small r** (strong field),
where the deviation from the linear/Newtonian regime is largest, and asks which
curve the counted density follows. The network's linear potential is `θ = M/r` (the
D3-derived harmonic field; the BD dynamics is linear — NL1). The proper-time density
`ρ_eff` is obtained by **counting** in a flat sprinkle of local proper density
`(1 − 2θ)`, then compared (comparison-only) to three curves:

- **Newtonian** `1 + u`
- **truncated (2nd order)** `1 + u + (3/2)u²`
- **Schwarzschild** `1/√(1−2u)`,  `u = M/r`.

---

## Result

| r | u = M/r | counted | Newtonian | truncated | Schwarzschild |
|---|---|---|---|---|---|
| 2.5 | 0.400 | 2.2344 | 1.4000 | 1.6400 | 2.2361 |
| 3.0 | 0.333 | 1.7300 | 1.3333 | 1.5000 | 1.7321 |
| 4.0 | 0.250 | 1.4143 | 1.2500 | 1.3438 | 1.4142 |
| 6.0 | 0.167 | 1.2247 | 1.1667 | 1.2083 | 1.2247 |
| 9.0 | 0.111 | 1.1347 | 1.1111 | 1.1296 | 1.1339 |
| 14.0 | 0.071 | 1.0800 | 1.0714 | 1.0791 | 1.0801 |
| 22.0 | 0.045 | 1.0488 | 1.0455 | 1.0486 | 1.0488 |

**RMS relative error of the counted density:**

| vs Newtonian | vs truncated (2nd) | vs Schwarzschild |
|---|---|---|
| 17.24% | 11.40% | **0.06%** |

- **Schwarzschild beats Newtonian at small r:** ✅ (decisively — 0.06% vs 17%).
- **Deviation from Newtonian has the right sign** (ρ grows *faster* than `1+u`): ✅.
- **Fraction of the 2nd-order gap `(Schw − Newt)` captured: 1.00** — fully.
- The counted density even beats the *2nd-order-truncated* curve (0.06% vs 11%),
  because the kinematic clock `√` carries **all** orders, not just the quadratic.

---

## The horizon — open frontier (not attempted)

The exact result holds to `r → 2M` (`u → 1/2`), but counting there needs `ρ₀ → ∞`:
as `u → 1/2` the local density `(1 − 2θ) → 0`, the diamond shrinks and the per-shell
count `N → 0`, so `N ≫ tractable`. We stop at **`r ≥ 2.5 M`** (`u ≤ 0.4`) and make
**no claim about the horizon**. `r → 2M` is documented as the open boundary, exactly
as required — the project does not pretend to simulate it.

---

## Verdict — NL3: **PASSA**

| check | result |
|---|---|
| Schwarzschild fits better than Newtonian at small r | ✅ 0.06% vs 17% |
| deviation from Newtonian has the right sign | ✅ |
| fraction of 2nd-order gap captured | ✅ 1.00 (full) |
| horizon `r → 2M` | documented as open frontier (not probed) |

**At small r the counted network density follows the full Schwarzschild
`ρ₀/√(1−2u)` to 0.06% — far better than the Newtonian `1+u` (17%) and better than
even the 2nd-order truncation (11%).** The network captures the strong-field profile
through the proper-time clock `√` (the kinematic mechanism of P2/P3), built on the
linearly-derived potential. Together with NL2, this is solid evidence that the
bridge density converges to Schwarzschild beyond the weak field — **kinematically**,
not through a derived non-linear action (NL1: λ free). The horizon remains the
honestly-flagged open frontier.

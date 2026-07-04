# R2 — Gauge current around the vortex and the centrifuge criterion

**Task.** Measure the gauge current `J_μ = Δτ·sin(φ+Δθ)` (θ=0 ⇒ `J = Δτ sin φ`) around a
winding-1 vortex: does it circulate, is it concentrated near the core, and is the causal
angular momentum `L = circulation·ξ` enough (`L/(ρξ²) > 1`) to redistribute the density?

## Results (10 seeds)

| Quantity | Value |
|---|---|
| core size ξ (half-max of action density) | 1.50 ± 0.00 |
| tangential circulation at ξ | **+0.570 ± 0.012** (circulates ✓) |
| `\|J\|` core → far | 1.058 → 0.001 (decays outward ✓) |
| **L/(ρξ²)** | **0.380 ± 0.008** (centrifuge criterion >1: **no**) |

- The vortex carries a **genuine circulating gauge current** (circulation 0.57, well above
  noise), and `|J|` is concentrated at the core and decays outward — the expected vortex
  current structure.
- The **rough centrifuge criterion is sub-threshold**: `L/(ρξ²) = 0.38 < 1`.

## The honest nuance

R1's dynamical relaxation gives **full** core depletion, yet this simple angular-momentum
estimate says the current is *not* obviously strong enough (0.38). There is no contradiction:
the depletion in R1 is driven by **minimising the action energy** `Σρ[1−cos(u)]` (the density
avoids the high-`[1−cos]` core), which is related to but stronger than the literal
"centrifuge" picture the heuristic `L/(ρξ²)` captures. The criterion being order-1 (0.38, within
a factor ~3 of threshold) is consistent with a real but not overwhelming effect; the proper
energy minimisation then realises it as a depletion whose depth is set by the stiffness K.

## Verdict (R2)

> **The current circulates (definite); the heuristic centrifuge criterion is sub-threshold
> (0.38).** The vortex carries real causal angular momentum, of the same order as the
> inertia, and the depletion R1 measures comes from the action-energy minimisation it drives
> — not a clean super-threshold centrifuge.

## Output
`R2_current.py`, `R2_current.json`, `R2_current.png`.

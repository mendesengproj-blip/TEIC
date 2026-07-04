# R4 — Redefine |Φ| = ρ_eff and repeat PE4: does the core pin now?

**Task.** PE4 used `|Φ| = ρ_Poisson` (the fixed substrate) and found **no core** (dip
−0.003, σ_core undefined). R4 redefines `|Φ_i| = ρ_eff(r_i)`, the **dynamical** back-reaction
density (R1), at the natural stiffness K=1, and repeats the PE4 core measurement over 20 seeds.

## Results (20 seeds, K=1)

`|Φ_eff|(r⊥)`:

| r⊥ | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 5.5 | 6.5 | 7.5 | 8.5 | 9.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| `\|Φ_eff\|` | 0.00 | 0.00 | 0.00 | 0.00 | 0.08 | 0.40 | 0.68 | 0.91 | 1.08 | 1.20 |

| Quantity | R4 (|Φ|=ρ_eff) | PE4 (|Φ|=ρ_Poisson) |
|---|---|---|
| **\|Φ\|(0)** | **0.000 ± 0.000** | ~1 (flat) |
| coherence length ξ_eff | 6.5 ± 0.0 | — |
| **σ_core** | **3.73 ± 0.01** (defined 100%) | undefined 100% |

**`|Φ_eff|(0) → 0`** and **σ_core is well-defined and constant** across all 20 seeds — a genuine
vortex core profile (zero at the centre, recovering to 1 far away). This is exactly the
abelian-Higgs core PE4 lacked, and it pins (constant width).

(See `R4_closure.png`: the `|Φ_eff|` profile rises from 0 at the core to the far-field value,
with ξ_eff ≈ 6.5.)

## Verdict (R4)

> **With the dynamical ρ_eff, |Φ|(0) → 0 and σ_core is constant — the core pins.** The single
> change from PE4 (Veredito C: no core) is replacing the fixed Poisson substrate density with
> the dynamical back-reaction density. That one change closes the magnitude sector: the vortex
> now has a real, pinned core in `|Φ| = ρ_eff`.

## Output
`R4_closure.py`, `R4_closure.json`, `R4_closure.png`.

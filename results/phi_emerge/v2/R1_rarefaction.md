# R1 — Does the vortex deplete the effective causal density at the core?

**Task.** Two faithful measures of ρ_eff around a winding-W vortex core, distinguishing the
**kinematic link count** from the **dynamical back-reaction** (the distinction the prompt
asks for: ρ_Poisson(nodes, PE4) vs ρ_eff(links/flux)).

## Results (20 seeds headline, 8 for the K/ρ scans)

**T scan (W=1, K=1):**

| T (ticks) | kinematic link-flux dip | dynamical back-reaction dip |
|---|---|---|
| 10 | +0.000 | +1.000 |
| 50 | +0.000 | +1.000 |
| 100 | +0.000 | +1.000 |
| 200 | +0.000 | +1.000 |

- **Kinematic link flux is FLAT (dip = 0.000)** at every T: the vortex does *not* change the
  causal-link **count** on a regular lattice — just as ρ_Poisson(nodes) was flat in PE4.
- **The dynamical back-reaction density depletes FULLY (dip = 1.000, |Φ|(0)→0)** at the
  natural stiffness K=1: the causal density, relaxed under the minimal action sourced by the
  vortex gauge energy `[1−cos(u)]` (the same D1–D3 geometry-sector relaxation), redistributes
  away from the high-action core.

**Stiffness K scan (the depth ~ 1/K law):**

| K | 0.5 | 1.0 | 2.0 | 4.0 | 8.0 | 16.0 |
|---|---|---|---|---|---|---|
| dynamical dip | 1.000 | 1.000 | 1.000 | 1.000 | 0.515 | 0.259 |

**Full depletion (|Φ|(0)→0) for K ≲ 5–8; partial for stiffer geometry.** The depth scales as
1/K (the Poisson response), so whether the core fully empties depends on the geometry
stiffness K — a free parameter (like the DEV's K). The background-density scan (ρ_factor =
1,5,20 at K=4) stays saturated-full (denser network → stronger source → deeper dip).

## Verdict (R1)

> **Rarefaction exists — as a dynamical back-reaction, not a kinematic effect.** The vortex
> leaves the causal-link *count* unchanged (kinematic, flat), but the causal density — *if it
> is the dynamical geometry field of the bridge (D1–D3)* — depletes at the core, fully
> (|Φ|(0)→0) for natural/soft stiffness K≲5. The dip is robust in sign for all K; its depth
> ~1/K. This is the mechanism PE4 lacked, and it is conditional on promoting ρ from PE4's
> fixed Poisson substrate to the dynamical density.

## Output
`v2_core.py`, `R1_rarefaction.py`, `R1_rarefaction.json`, `R1_rarefaction.png`.

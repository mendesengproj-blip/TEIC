# PHI_EMERGE_V2 — Causal rarefaction at the vortex core

PHI_EMERGE (Veredito C) found that `Φ = ρ·e^{iφ̄}` reproduces the **phase** of an abelian-Higgs
field (a density-dependent gauge mass `m_A ∝ √ρ`) but not the **magnitude**: `|Φ| = ρ_Poisson`
(the fixed node-count substrate) does not dip at a vortex core (PE4: dip −0.003, σ_core
undefined). PE4_V2 tests the sharper hypothesis: does the vortex's circulating gauge current
deplete the **effective** causal density `ρ_eff` (the link flux / dynamical back-reaction, not
the static node count) — the mechanism that would close `Φ = ρ·e^{iφ̄}` without an added potential?

Code/data: `results/phi_emerge/v2/`. 20 seeds for R1 and R4. Anti-circularity: `ρ_eff` is a
count / an action-minimising density; no complex literal; the superfluid analogy appears only
in COMPARISON ONLY blocks. The guard passes over the whole tree.

## Scorecard

```
R1 — Rarefação ρ_eff(0) < ρ_eff(∞):     SIM (dinâmica, dip 1.000; cinemática PLANA 0.000)
R2 — Corrente J_μ circulante:            SIM (circulação 0.570 ± 0.012)
R2 — L/(ρξ²) > 1:                        NÃO (= 0.38, sub-limiar)
R3 — Dip ∝ W:                            SIM, |Δρ(0)| ∝ W^1.05 (≈ linear)
R4 — |Φ_efetivo|(0) → 0:                 SIM (0.00 ± 0.00)
R4 — σ_núcleo = constante:               SIM (3.73 ± 0.01, definido em 100% das sementes)
```

## VEREDITO: **B** — rarefação existe e pina o núcleo, como back-reaction condicional

> **The rarefaction exists and drives `|Φ_eff|(0) → 0` with a constant-width pinned core at the
> natural stiffness — but only for the DYNAMICAL causal density (the D1–D3 geometry sector),
> not PE4's fixed Poisson substrate, and with the depth set by the (free) geometry stiffness K
> (full for K ≲ 5). It is a REDUCED fourth ingredient (promote ρ to the dynamical density the
> bridge already has, and the vortex does the rest), not "no ingredient" (A).**

## The chain (and exactly where it is conditional)

```
sprinkle (geometry) → gauge phase φ → vortex W=1 (topology S¹)
   → circulating gauge current J  ......................... R2: circulation 0.57 ✓ (but L/(ρξ²)=0.38)
   → action [1−cos(u)] peaks at the core
   → causal density relaxes away from the core ............ R1: dynamical dip 1.000 ✓ (kinematic FLAT)
   → depletion ∝ winding number .......................... R3: |Δρ(0)| ∝ W^1.05 ✓
   → |Φ_eff| = ρ_eff → 0 at the core, pinned ............. R4: |Φ|(0)=0, σ_core=3.73 const ✓
```

Every arrow is verified. The chain **closes** — *provided* two conditions, which is why the
verdict is B not A:

1. **ρ must be dynamical.** The vortex does **not** change the causal-link *count* (R1
   kinematic flux is flat, exactly like PE4's node count). The depletion appears only when the
   density is allowed to **relax under the minimal action** — the same relaxation that gives
   D1–D3 their Newtonian `GM/r`. Promoting ρ from PE4's fixed substrate to this dynamical
   density is the single step that turns the flat PE4 profile into the pinned R4 core.
2. **The stiffness K must be soft.** The depth scales as 1/K — full (`|Φ|(0)→0`) for K ≲ 5,
   partial above. K is free (like the DEV's K), so the full closure is a soft-stiffness
   statement.

## Relation to the prior verdicts

- **CR_ABELIAN_HIGGS (Veredito A):** added a complex scalar with its own `|Φ|²|D_μΦ|²` kinetic
  term — the magnitude was a genuine fourth ingredient. Honest and correct.
- **PHI_EMERGE (Veredito C):** the composition `ρ·e^{iφ̄}` emerges in its *phase* (gauge mass)
  but not its *magnitude* (no core in the fixed-substrate ρ).
- **PE4_V2 (Veredito B):** the *magnitude* sector closes too — `|Φ_eff|(0)→0`, pinned core —
  **if** ρ is the dynamical geometry density and the stiffness is soft. The fourth ingredient
  is not eliminated but **reduced**: from "add a complex scalar" to "let the causal density
  back-react, as the bridge's D1–D3 already do."

> The open question is now precisely located and is **not** about the gauge/topology sector
> (settled) but about the **geometry sector**: is the causal density that enters `|Φ|=ρ` the
> fixed sprinkling substrate (then PE4/Veredito C/D) or the dynamical field that relaxes under
> the minimal action (then PE4_V2/Veredito B → A)? The bridge's own D1–D3 treat it as
> dynamical. If that is accepted as part of the minimal theory, the magnitude core emerges and
> the vortex pins — a reduced-axiom closure, reported here as B with the A-conditions met in
> the dynamical/soft-stiffness regime, and **not** overclaimed as the unconditional A.

## Triple verification for A — not asserted

A would require an *unconditional* closure. The closure here is conditional (dynamical ρ + soft
K) and the kinematic count is flat, so A is **not** claimed. The A-conditions (`|Φ|(0)→0`,
σ_core constant, dip ∝ W) are individually met and reported with their conditions.

## Per-task detail
`results/phi_emerge/v2/R1_rarefaction.md` … `R5_synthesis.md`, with `v2_core.py`, JSON, and
figures (`R1_rarefaction.png`, `R2_current.png`, `R4_closure.png`). Reproduce each with
`python results/phi_emerge/v2/R<n>_*.py`.

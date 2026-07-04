# E6c — CURVED GEOMETRY: does spatial curvature furnish the magnetic 2-cell?

> Extension of E6 / E6b along "Direction A" (geometry). Pre-registered charter.
> Executed jun/2026. Results in `results/gauge/e6c/`. Result goes to RESEARCH_MAP.md,
> **not** to any paper. Does NOT modify E6, E6b, or E7.

## Context and motivation

E6 (E6_3b) and E6b mapped the obstacle to the BD-gauge `E²−B²` photon with precision: on a
**flat** Poisson causal set the causal-diamond 2-complex is essentially all **electric**
(timelike area bivector). Height-2 diamonds are exactly electric (`frac_B=0.0000`); the
"taller diamond" route (E6b) gives only a non-growing ~0.25% magnetic tail. The missing
ingredient is a **spacelike 2-cell with O(1) magnetic fraction**.

E6c tests an orthogonal route: **spatial curvature**. In a curved background the two
ascending geodesics bounding a causal diamond bend, so its area bivector need not stay locked
to the straight timelike tip→tip extent and can acquire spacelike (`A^{ij}`) content.

## Construction

Background: **de Sitter dS₄**, flat slicing, `ds² = −dτ² + e^{2Hτ}dx²`, `H=1/R_dS`.

- **Causal order** from the conformal coordinates `(η, x)`, `η=−(1/H)e^{−Hτ}` — de Sitter is
  conformally flat, so `p<q ⇔ (η_q−η_p)>|x_q−x_p|`, the SAME Minkowski order as E6/E6b. Fed
  to `causal_link_graph` unchanged.
- **Control design:** sprinkle a **cubic conformal box** of side `L_x=(1/H)(1−e^{−HL})`, so
  the causal-set ENSEMBLE (and 2h-gon diamond statistics) is identical to E6b at every
  curvature; curvature is the only variable. `L_x → L` as `H→0`.
- **E/B split** from the **5D hyperboloid embedding** `−X0²+ΣXi²=R²` (flat-slicing
  parametrisation). The area bivector `A^{μν}=½Σ_c X_c∧X_{c+1}` is fed to `e6_bd_core`'s
  `polygon_bivectors` VERBATIM (works in any D; here D=5): `e²=Σ(A^{0i})²`, `b²=Σ(A^{ij})²`,
  B-type iff `b²>e²`. Curvature enters **only** through the bent embedding.

Reuses `e6_bd_core` (E/B physics) and `e6b_diamond_height_core` (2h-gon topology) UNCHANGED;
only the geometry (sprinkle + embedding) is new. Curvature radius `R̂=R_dS/ℓ`, `ℓ=ρ^{−1/4}`.

## Mandatory gate (pre-registered)

```
R_dS = ∞ (Minkowski) MUST reproduce E6b:
   h=2  frac_B ≈ 0      (Wilson-hi < 0.001)
   h=3  frac_B ≈ 0.0024
If the gate fails, the run is INVALID and no curved verdict is issued.
```
Enforced by construction (R̂=∞ branches to the exact E6b sprinkle, same RNG) and checked.

## Sweep & kill criterion (pre-registered)

```
Sweep R̂ = ∞, 16, 8, 4, 3, 2  (∞→Planckian);  N = 500/1000/2000;  h = 2,3,4;  3 seeds.

DEATH    : frac_B < 0.001 across the WHOLE sweep (every R_dS, best-sampled cell)
           -> curvature does NOT furnish the magnetic sector
           -> E6 flips [FRONTEIRA-TÉCNICA] -> [FRONTEIRA-ESTRUTURAL]; THEN run E6d.
SUCCESS  : frac_B > 0.01 at some R_dS with significance (Wilson-lo > 0.01)
           -> curvature opens the magnetic sector; report minimal R_dS ("curvature radius").
           -> E6d may be unnecessary.
INCONCL. : small non-zero, doesn't clear 0.001/0.01 robustly -> report honestly.
```

## Outcome (jun/2026) — GATE PASS; SUCCESS (marginal, curvature-extreme)

Gate PASS (Minkowski = E6b exactly). `frac_B` rises **monotonically** with curvature at
every height; per-cell `b²/e²` rises ~8.6× (0.11→0.97). At R̂=2 (R_dS≈1.68ℓ), h=4:
`frac_B=0.01169`, **Wilson-lo 0.0105 > 0.01**, N-stable, 28k plaquettes — the pre-registered
SUCCESS criterion fires. Caveats stated plainly: marginal (1.17%), trans-Planckian curvature
only, mean diamond still electric (`b²/e²=0.97<1`); the magnetic sector is a ~1.2% tail at
the light-cone edge, not yet O(1). h=2 stays exactly electric at all curvatures
(curvature-immune). **DEATH did NOT fire → E6 stays [FRONTEIRA-TÉCNICA] (refined upward),
E6d NOT triggered.** Full analysis: `results/gauge/e6c/E6c_synthesis.md`.

## Deliverables

```
results/gauge/e6c/
  E6c_literature.md          — precedent (de Sitter CST, conformal flatness, gauge on causets)
  e6c_curved_core.py         — geometry (de Sitter sprinkle + 5D embedding); reuses E6/E6b
  E6c_1_curvature_scan.py    — sweep + gate + pre-registered verdict + figure
  E6c_1_curvature_scan.json  — numerical data
  E6c_1_curvature_scan.png   — frac_B vs curvature, b²/e² vs curvature
  E6c_synthesis.md           — synthesis with verdict
RESEARCH_MAP.md              — E6 row updated
```

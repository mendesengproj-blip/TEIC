# FL3-2 — Collision Dynamics

Frontal collision, **v = 0.5c, b = 0** (8 vacuum seeds), evolved with the validated fast
geodesic velocity-Verlet (`fl3_core.chiral_evolve_fast`, dt/dx = 0.012 from FL3-V). Each
block records the global charge B(t), the energies E2/E4/E_field/E_total, and the
**radiation-proof topological-matter content** Q_top(t) = ∫|smoothed b| dx³.

## What happens
At t ≈ 0.7 the two solitons overlap and the field energy **halves** (E_field 627 → ~250),
releasing the topological gradient energy. Q_top — the amount of localized matter — drops
from **1.63 (two solitons) to ~0.02 within t ≈ 0.7** and stays there. The global charge
B_total never leaves 0 (|B|_max = 0.068 over all seeds and times).

| seed | scenario | Q_top: start → late | Q_top peak/Q₀ | E_field drop | \|B\|max |
|---|---|---|---|---|---|
| 0 (showcase) | annihilation | 1.63 → 0.020 | 0.023 | 50% | 0.049 |
| 1–7 | annihilation | 1.63 → ~0.021 | ~0.024 | 51% | ≤0.068 |

**Scenario counts: annihilation 8 / 8.** No seed shows Q_top rising (creation would need
Q_top → ~4); every seed shows it collapsing to ~1% of the two-soliton value.

## The radiation trap (why a naïve count misleads)
A first pass counted **energy-density** peaks and found them rising to 30–48 "peaks" — which
*looks* like creation. It is not: those are ripples of the **magnon radiation burst** the
annihilation releases. The global charge stays 0 and the smoothed baryon matter Q_top goes
to zero, so no solitons are present — only turbulent radiation. The verdict therefore rests
on Q_top (smoothed baryon density) and the conserved B, never on the energy-peak count. The
field figure (`FL3_2_dynamics.png`) shows the baryon-density mid-plane going from two clean
±1 cores to structureless speckle.

## Energy bookkeeping (honest)
E_field drops ~50% at the collision (physical: bound gradient energy released). E_total is
**not** conserved during the burst — it swings 637 → 804 → 735 (a **+26%** numerical
excursion) as the stiff 4-derivative Skyrme term on a coarse grid plus the boundary clamp
mishandle the high-gradient radiation. This does **not** affect the verdict: creation would
require Q_top to *rise* and would require ~50× more energy than is present; a numerical
*surplus* of 26% that still produces no creation only reinforces the conclusion. The robust
observables (topological B, smoothed matter Q_top) are unaffected by the energy drift.

## Reading
The collision realises **annihilation**: B=+1 and B=−1 merge, their topological structure
cancels, and the bound energy radiates away as magnons (E2 quanta). This is exactly what the
energy budget demands — KE_collision = 10.1 is **1.8%** of the 2 M_Sk c² = 548 needed to
create a new pair (FL3-5). B_total stays 0 and no new matter appears → the pre-registered
death criterion is met.

Anti-circularity: B = current determinant; c = measured E2 magnon speed; M_Sk = SU3 energy
functional. "pair production" is COMPARISON ONLY.

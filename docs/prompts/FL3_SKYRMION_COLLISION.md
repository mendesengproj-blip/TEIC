# FL3 — Skyrmion Collision: Matter Creation from a Causal-Lattice Collision

> Charter (pre-registered). Tests whether a Skyrmion(B=+1) colliding with an
> anti-Skyrmion(B=-1) **creates** an additional pair — the lattice analogue of
> pair production. Results in `results/matter/fl3/`. Modifies no earlier campaign.

## Question
Does a high-energy SU(2) collision of a Skyrmion + anti-Skyrmion produce new
topological charge (`N_Skyrmions: 2 → 4`, `B_total` conserved at 0)?

## Anti-circularity anchors (NOT inserted as constants)
- **B** is the discrete Pontryagin index = current-determinant of the quaternion
  field U (`su2_core.baryon_number`). No physical label feeds it.
- **c = 0.9797 ≈ 0.98** is the magnon group speed MEASURED in
  `results/vacuum_structure/orientation/e2/E2_2_dispersion.json` (ω = ck, Verdict A).
- **M_Sk** is the lattice energy functional of the relaxed Skyrmion
  (`su2_core.chiral_energy`; radial mass ≈ 146 for e_sk=1, SU3).
- "pair production", "e⁺e⁻", "LHC" are COMPARISON ONLY.

## Pre-registered death criterion
`B_total` stays at 0 **and** `N_peaks` does not increase after the collision
= **Verdict B** (annihilation) or **Verdict C** (elastic). Parameters are NOT to
be tuned to force creation.

## Verdicts
- **A — CREATION**: N_Skyrmions 2→4, B_total conserved, E_thresh ≈ 2 M_Sk c².
- **B — ANNIHILATION**: B=+1 and B=-1 annihilate to radiation; no new pair.
- **C — ELASTIC**: solitons scatter/pass without annihilation or creation.

## Tasks
- **FL3-V** gate: unitarity, B conserved for isolated Skyrmion, causal propagation ≤ c.
- **FL3-1** initial data: boosted hedgehog(B=+1) + anti-hedgehog(B=-1).
- **FL3-2** dynamics: geodesic leapfrog SU(2); measure B(t), E(t), N_peaks(t).
- **FL3-3** analysis: classify scenario; does N_peaks rise after collision?
- **FL3-4** phase diagram (v,b) — only if FL3-3 shows creation.
- **FL3-5** E=mc²: check E_collision ≥ 2 M_Sk c² — only if creation.
- **FL3-6** honest synthesis + verdict.

## Protocol
Gate first. Start frontal: v = 0.5c, b = 0. Vary (v,b) only if the gate passes
and the frontal collision is inconclusive. 20 vacuum seeds for the ensemble.

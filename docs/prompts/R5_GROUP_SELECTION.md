# R5 -- Colour-group selection: why SU(3), not SU(N≥4)?

> Roadmap item R5 / RESEARCH_MAP Section 6 #5. Cheap, analytical campaign.
> Closes the logical hole flagged by the map: the programme proves SU(2) minimal
> for matter (MIN3) but had **never** explained why the colour group is SU(3)
> specifically rather than SU(4)/SU(5). N=3 is an *input* to `su3_core` (FL1
> assumed it, then measured confinement/octet/Skyrmion); R5 asks what pure group
> theory / topology selects, and where the selection's requirement comes from.
> Anti-circularity: no TEIC lattice result enters; N is the free input.

## Verdict: **B -- MINIMAL selection (not unique, requirement imported)**

| Hypothesis (pre-registered) | Kill criterion | Outcome |
|---|---|---|
| **H_reality**: SU(3) = min. simple group with *complex* fundamental | SU(2) complex, or SU(3) real, or smaller complex | **SURVIVES** — SU(2) pseudoreal, SU(3) first complex |
| **H_anomaly**: SU(3) = min. group with nonzero cubic d^abc | d≠0 at SU(2), or d=0 at SU(3) | **SURVIVES** — 0 at SU(2), nonzero from SU(3) |
| **H_uniqueness**: an invariant flips at N=3 \| N=4 | every selector ON at 3 is also ON at 4 | **KILLED** — single boundary N=2\|3 only |
| **H_topology**: a physical π_k (k≤5) separates SU(3) from SU(4) | π₃,π₄,π₅ equal for SU(3),SU(4) | **KILLED** — none separates 3 from 4 |

## Honest bottom line

There **is** a real minimality theorem: **SU(3) is the smallest simple compact
Lie group whose fundamental representation is complex** (3 ≠ 3̄), equivalently the
smallest with a nonzero symmetric cubic invariant d^abc. These two criteria turn
on at the *same* place — su(2) is the unique simple algebra with a self-conjugate
fundamental and no cubic invariant; everything from su(3) up has both
(R5-1, machine-exact for N=2..8).

But three honest limits make this a **B, not an A**:

1. **Topology does not select.** π₃=ℤ for every simple group (Bott) — the very
   property that gave SU(2) its baryon charge is blind to N. π₄,π₅ only separate
   SU(2) from N≥3, never 3 from 4. The single homotopy group that *does* separate
   3 from 4 (π₆ = ℤ₆ vs 0) is physically inert in 3+1D (R5-2).

2. **Minimality ≠ uniqueness.** SU(4),SU(5),… are equally complex, anomalous and
   confining; SU(3) wins only as the *smallest* group past the N=2|3 boundary.

3. **The requirement is imported.** "The fundamental must be complex" (a
   constituent colour charge that distinguishes matter from antimatter) is a
   phenomenological/structural input — exactly like d=3. The causal network never
   measures N; FL1 assumed it.

This is the **group-space analogue of DS1-3** ("d=3 by structural exclusion"):
the observed value is the *minimal consistent* point of a choice space, a
*selection*, not a dynamical *emergence*.

## Status changes

- **RESEARCH_MAP §3.2 / Section 6 #5 / roadmap R5:** [NUNCA TENTADO] → **[SÓLIDO]
  (structural selection), with declared import.** Colour group = minimal simple
  group with complex fundamental / cubic anomaly; topology does not distinguish;
  complex-charge requirement external (phenomenological), like d=3.
- Does **not** change FL1's status (FL1 stands on measured confinement/octet).
  R5 closes the *logical hole*, it does not add a measured fact about the lattice.
- Mirrors and extends **MIN3** (SU(2) minimal for matter → SU(3) minimal for
  distinguishable colour charge); both "minimal consistent, not derived".

## Artefacts

| File | Content | Reproduce |
|---|---|---|
| `results/foundations/r5_group/r5_group_core.py` | su(N) generators, d^abc, reality of fundamental | `python r5_group_core.py` |
| `results/foundations/r5_group/R5_1_invariants.py` / `.md` / `R5_invariants.json` | invariants table N=2..8, boundary analysis | `python R5_1_invariants.py` |
| `results/foundations/r5_group/R5_2_topology.py` / `.md` / `R5_topology.json` | homotopy table + distinguish-test | `python R5_2_topology.py` |
| `results/foundations/r5_group/R5_3_synthesis.md` | full honest synthesis | — |

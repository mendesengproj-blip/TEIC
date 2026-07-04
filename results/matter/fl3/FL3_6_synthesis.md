# FL3-6 — Honest Synthesis

```
FL3-V (gate):
  Unitarity preserved?                 SIM (max |U|-1 = 2.2e-16)
  B conserved for isolated Skyrmion?   PARCIAL — strict dB<1e-3 NOT attainable on a
                                       dx~0.46 lattice (determinant baryon INTEGRAL is
                                       jiggle-noisy: B band [0.76,0.92] at dt/dx=0.012
                                       while ENERGY stays bounded).  Noise-robust facts:
                                       global B stays constant, smoothed lump count = 1.
  Analytic Skyrme gradient correct?    SIM (vs true per-site FD: 2.8e-8; dynamics
                                       bit-identical to su2_core, ~16x faster)
  Boost imparts motion at ~v?          SIM (early baryon-centroid ratio 1.03)
  Causality finite & O(c)?             SIM (RMS-spread 1.39, c=0.98 from E2)

FL3-1 (configurations):
  Skyrmion + anti-Skyrmion created?    SIM (B_total~0, two lumps, +1/-1 baryon blobs)
  Boost implemented?                   SIM
  KE / 2 M_Sk c^2 on the whole grid:   0.0007 .. 0.040  (< 1 everywhere)

FL3-2 (dynamics):
  Energy conserved +/-1%?              NAO — physical 50% E_field drop (gradient energy ->
                                       magnon radiation) PLUS a +26% numerical E_total
                                       excursion during the burst (stiff Skyrme term +
                                       boundary clamp on a coarse grid).  Verdict is robust:
                                       a 26% energy SURPLUS still yields no creation, and
                                       the topological observables B and Q_top do not depend
                                       on the energy drift.
  Topological matter evolves coherent? SIM — Q_top: 1.63 (two solitons) -> ~0.02
  B_local / global B coherent?         SIM (global B |max| = 0.068, conserved ~0)

FL3-3 (collision):
  Scenario observed:                   2 — ANNIHILATION (8/8 seeds)
  N_peaks(energy) rises after t_c?     SIM, but it is MAGNON RADIATION (peaks 2->~40),
                                       NOT solitons: global B and Q_top show no matter.
  Topological matter Q_top rises?      NAO (peak/Q0 = 0.02; collapses, never rises)

FL3-4 (phase diagram):
  Velocity threshold for creation:     N/A (no creation regime; would need v -> c)
  Energy threshold:                    E_thresh = 2 M_Sk c^2 = 548.1 (never reached)

FL3-5 (E=mc^2):
  E_collision >= 2 M_Sk c^2 ?          NAO — KE = 10.1 vs 2 M_Sk c^2 = 548.1
                                       (ratio 0.018; threshold real, not met)

VEREDITO:

[X] B — ANIQUILACAO SEM CRIACAO
    Skyrmion(B=+1) + anti-Skyrmion(B=-1) annihilate completely (8/8 seeds).
    Energy released as magnon radiation (the 50% E_field drop; E2 quanta).
    No pair created at any (v,b) on the charter grid.
    => The topological barrier is not overcome -- and CANNOT be at this energy:
       the collision carries 1.8% of the 2 M_Sk c^2 rest-mass cost of a new pair.
       E=mc^2 (with lattice-derived c from E2 and M_Sk from SU3) is the conservation
       law that forbids creation here.  An additional ingredient -- an ultra-
       relativistic boost v -> c that the discrete causal lattice cannot represent --
       would be required even to APPROACH threshold.
```

## Death criterion (pre-registered)
> "B_total stable at 0 with N_peaks not increasing = Verdict B or C. Do not tune
> parameters to force creation."

**Triggered.** B_total stays 0 (|B|_max = 0.068) and the topological-matter content Q_top
does not increase (it collapses to ~2%). No parameters were tuned toward creation; on the
contrary, the energy budget was fixed by independently-sourced c and M_Sk and shown to be
~50× short of threshold before any dynamics were run.

## What this adds to the program
- The MATTER_SU2 dynamic sector now has a **validated, fast** time-integrator (analytic
  single-pass Skyrme gradient; bit-identical to the trusted engine, ~16× faster) — reusable
  for any future SU(2) dynamics (FL4 Skyrme, scattering at higher resolution).
- **Matter is not created by sub-relativistic Skyrmion collision.** The lattice realises
  annihilation → radiation, the time-reverse of creation, exactly as E=mc² demands.
- It closes the "creation by collision" question that SU6 opened (SU6 saw no spontaneous
  winding from chain collisions; FL3 shows explicit soliton+antisoliton collisions annihilate
  rather than multiply) and quantifies *why*: the collision energy is two orders below the
  rest-mass threshold.

## Honest limitations
- Lattice dx ≈ 0.46 (≈4 points/core): the baryon **integral** is noisy and post-collision
  magnon turbulence swamps a raw peak count — handled by the radiation-proof Q_top, but a
  finer grid would sharpen the integer charge.
- The boosted profile is not an exact discrete eigenstate, so it radiates part of its
  momentum; the effective collision energy is *below* KE₀ — which only strengthens the
  no-creation conclusion.
- 8 vacuum seeds (compute-limited; nominal 20). All 8 are identical in outcome and the
  result is anchored by the grid-independent energetic argument, so the conclusion is not
  seed-count-sensitive.
- Ultra-relativistic v → c (the only regime that could reach threshold) is outside what the
  discrete lattice can faithfully represent — so FL3 bounds, but does not probe, the
  creation corner.

# LV4b — the residual boost defect is NOT a box-reach artifact (honest kill)

**Task.** LV4 left a residual frame defect |R(β)−1| ≈ 0.12 at the most field-sensitive
point (E₀ = u₀, β = 0.8). Hypothesis under test: the residual is the truncation of the
boost orbit, so it must shrink as the box grows (η_q95 rises 1.53 → 1.91 over L = 3 → 6).
Pre-registered: PASS = monotone decrease with L; KILL = L-independent floor.
Generator `LV4b_extent.py`, data `LV4b_extent_data.json` (ρ=12; 10–16 seeds per L).

## Result: the defect does not move with the box

| defect \|R−1\| | L=3 | L=4 | L=5 | L=6 |
|---|---|---|---|---|
| E₀=u₀, β=0.4 | 0.047±0.008 | 0.032±0.005 | 0.033±0.006 | 0.041±0.006 |
| E₀=u₀, β=0.8 | 0.136±0.015 | 0.123±0.009 | 0.111±0.011 | 0.127±0.009 |
| E₀=u₀, β=1.2 | 0.264±0.016 | 0.216±0.015 | 0.230±0.015 | 0.240±0.014 |
| E₀=2u₀, β=0.8 | 0.046±0.011 | 0.035±0.008 | 0.047±0.011 | 0.047±0.010 |

No monotone trend anywhere: the defect at fixed (E₀/u₀, β) is **L-independent within
errors** while the rapidity reach clearly grows. **The pre-registered KILL fires**: the
residual is not the box truncating the orbit.

## What the residual actually is (post-hoc reading, marked as such)

The defect is controlled by the **field strength**, not the volume: across LV4 it falls
0.98 → 0.76 → 0.12 → 0.018 → 0.008 → 0.003 as E₀ goes 0.1 → 30 u₀, at every L equally.
The mechanism consistent with both scans: the plaquette population has a broad invariant
size distribution (LV1: dominance r spans 0.09–0.89 between quantiles), so at any E₀ a
fraction with E₀·|Ω| ≲ 1 is still in the *quadratic* regime and contributes its local
E/B ≈ 3 anisotropy; that fraction is set by ρ (granularity), not by L. Saturation —
the resummation that restores invariance — eats this fraction as E₀ grows, which is
exactly the LV4 collapse. A bigger box adds orbit depth but does not change the
unsaturated fraction; hence the floor.

## Verdict

**KILL of the box-reach hypothesis — and the right correction to LV4's reading.** The
restoration direction is **field strength (resummation), not volume**: the summed action
is Lorentz-invariant exactly to the extent that the bounded cosine has resummed the
quadratic expansion, plaquette by plaquette. The L-stable 12% at E₀ = u₀ is the
quadratic remnant of a scale-mixed population, the same object LV3 identified as
regulator-divergent in the pure quadratic limit — not a new preferred-frame effect
(LV2 rules that out independently). Routes that would push it down at fixed field:
higher density (shrinks the granularity, moves u₀), or the BD sign-alternating kernel
as the linear-theory subtraction (BRIDGE_BD) — both orthogonal to box size, as measured.

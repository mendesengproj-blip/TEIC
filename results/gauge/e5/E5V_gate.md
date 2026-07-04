# E5-V — U(1) gauge engine validation gate (synthesis)

> Pre-registered in `E5_PHOTON_LINK_SECTOR.md`. Code: `e5_core.py` (engine),
> `E5V_gate.py` (G1-G3), `E5V_gate_fss.py` (corrected G3). Data: `E5V_gate.json`,
> `E5V_gate_fss.json`. Run jun/2026.

## Results

| Gate | Test | Result |
|---|---|---|
| **G1** | gauge invariance: random local transform leaves plaquette holonomies fixed | **PASS** — max\|Δcos\| = 1.8×10⁻¹⁵ (4D and 3D), machine precision |
| **G2** | 4D U(1) deconfinement at β_c≈1.01 (specific-heat peak) | **PASS** — peak at **β = 1.00** |
| **G3** | 3D-confines / 4D-transition contrast (finite-size scaling) | **INCONCLUSIVE** |

## Honest account of G3

The original G3 compared specific-heat peak *heights at a single volume*, which
**cannot** distinguish a phase transition from a crossover — that needs finite-size
scaling. Corrected to FSS (does the 4D peak grow with volume?), the measurement at
the volumes a pure-Python engine affords (3⁴→4⁴ for 4D; 4³→6³ for 3D) gives:

```
4D U(1) peak/plaq: 3^4=1.36e-3 -> 4^4=6.53e-4   (x0.48)
3D U(1) peak/plaq: 4^3=6.73e-3 -> 6^3=1.26e-3   (x0.19)
```

The 4D peak shrinks *less* than the 3D one (weakly consistent with 4D being more
transition-like), but **neither peak grows** — the clean FSS signature of a true
transition is not resolved at these tiny volumes. Reported as INCONCLUSIVE, not
forced to a pass.

## Status and consequence

- The engine is **gauge-invariant (exact)** and **reproduces the known 4D U(1)
  deconfinement transition at β_c≈1.0** (G1, G2) — the decisive validations that the
  U(1) gauge dynamics is correct.
- The 3D/4D FSS contrast (G3) is **unresolved** at pure-Python volumes.
- Additionally, E5-1 (confinement on the causal set) requires a **Wilson-loop
  area-law** observable that has **not yet been built or validated**; G2 validated
  the average-plaquette/specific-heat route, not the Wilson-loop route.

**Pre-registered protocol decision:** the charter says "if any gate fails, STOP." G3
is not a clean pass, and the confinement observable E5-1 needs is not yet validated.
Therefore E5-1 (the causal-set U(1) confinement scan) is **gated** pending: (a) a
faster engine (vectorised/checkerboard Metropolis, or a compiled inner loop) to
reach the volumes that resolve FSS, and (b) a validated Wilson-loop area-law
estimator. No causal-set photon claim is made until those are in place.

This is the honest stopping point for E5 in this session: the charter, the gauge
engine, gauge-invariance, and the known 4D transition are established; the
causal-set measurement awaits the engineering above.

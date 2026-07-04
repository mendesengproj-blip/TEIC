# E6d — Synthesis: does the ferromagnet AMPLIFY E6c's magnetic sector? — NO (falsified)

> Direct extension of E6c along "Direction B" (coupling). Code: `e6d_coupling_core.py`
> (coupling on E6c's curved substrate; reuses E6c geometry + E6/E6b E/B physics VERBATIM),
> `E6d_coupling.py` (sweep + gates + verdict). Data: `E6d_coupling.json`. Figure:
> `E6d_coupling.png`. Gates: `E6d_gate.md`. Analysis: `E6d_coupling.md`. Literature:
> `E6d_literature.md`. Run jun/2026. **Result goes to RESEARCH_MAP, not to a paper.**
> Does NOT modify E6/E6b/E6c.

## The question

E6c gave the first positive photon-sector signal: de Sitter curvature (R̂=2, h=4) furnishes
a B-type (magnetic) fraction ≈1.17% — above the 1% threshold but far from the O(1) a real
emergent photon needs. E6d asks whether **coupling the ordered orientation ferromagnet (E1,
O(3) field n⃗∈S²) to the gauge bivector** — `Φ=A+λ(n⃗_i×n⃗_j)·ê_z`, the Meissner-style
condensate↔gauge coupling — **AMPLIFIES** that 1.17% toward O(1) on the **curved** substrate.

The coupling is realised exactly inside E6's geometric E/B classifier: the internal–internal
component of the augmented (7D) area bivector equals `½λ²Σ(n×n')·ê_z`, the internal axes are
spacelike (magnetic channel), and `λ=0` returns E6c bit-for-bit. So the construction is a
faithful, gate-anchored embedding of the prompt's coupling. (Details: `E6d_coupling.md`.)

## Gates (pre-registered)

| Gate | Meaning | Result |
|---|---|---|
| **G0** | λ=0 reproduces E6c (R̂=2,h=4) bit-for-bit | **PASS** (0.01169 = E6c, per run <1e-12) |
| **G1** | λ=0 phase-independent (coupling OFF) | **PASS** |
| **G2** | rise REQUIRES ferromagnetic order | **FAIL** (disordered amplifies *more*) |

## Results (pooled N=2000, 3 seeds, ≈28k plaquettes/cell; substrate R̂=2, h=4)

```
            λ=0      λ=0.5    λ=1.0    λ=2.0      |M|
disordered  0.01169  0.01119  0.04382  0.27152    0.03
J_c         0.01169  0.00925  0.03166  0.20497    0.56
2J_c        0.01169  0.00882  0.01563  0.09879    0.82     <- most ordered = LEAST magnetic
```
Mean `b²/e²` stays **< 1** at every λ and phase (≤0.986): the typical diamond remains
electric even maximally coupled; frac_B is only the spacelike-tail fraction.

Three decisive facts:

1. **frac_B rises with λ — but as spacelike NOISE, not amplification.** A `b²=Σ(Ã^{ij})²`
   observable is inflated by ANY internal field variance; at λ=2 the internal coordinates
   rival the geometric embedding, tipping 10–27% of cells spacelike. Generic variance, not a
   coherent magnetic sector.
2. **The rise ANTI-requires order (G2 FAIL).** At λ=2: `disordered 0.272 > J_c 0.205 >
   2J_c 0.099`. The DISORDERED field gives the largest magnetic fraction, the deep-ordered
   the smallest. Coherent texture (nearly-parallel neighbours) sweeps little internal
   bivector area; disordered texture sweeps a lot. **More order ⇒ less magnetic.**
3. **Weak coupling + order even SUPPRESSES below baseline** (λ=0.5, 2J_c: 0.0088 < 0.0117) —
   the ordered ferromagnet slightly *erodes* the curvature-made magnetic fraction.

## Verdict (against the pre-registered criterion)

```
PRE-REGISTERED:
  SUCCESS      frac_B>0.05 AND grows with λ on the ORDERED curved substrate (needs order)
  DEATH        frac_B<0.02 across the whole sweep -> coupling doesn't amplify; document output
  INCONCLUSIVE frac_B grows but stays in [0.02,0.05]

MEASURED  ->  DEATH (amplification hypothesis FALSIFIED).
  - NOT SUCCESS: although frac_B numerically exceeds 0.05 at large λ, it FAILS the mechanism
    test G2 — the rise is sourced by DISORDER (a spacelike-noise artefact), and ferromagnetic
    ORDER SUPPRESSES it (disordered > J_c > 2J_c). The pre-registered SUCCESS explicitly
    requires the effect to come from the ORDERED ferromagnet (J>J_c); it comes from the
    opposite. G2 exists precisely to reject this artefact, and it fires.
  - The literal >0.05 is reported honestly and explicitly attributed to spacelike noise, not
    suppressed — but it is NOT the hypothesised amplification, so it cannot count as success.
  - The hypothesis "the ordered ferromagnet amplifies E6c's curvature signal toward O(1)" is
    FALSIFIED: the ordered condensate does not amplify — it weakens — the magnetic sector.
```

## Physical reading

The Meissner/Anderson–Higgs intuition (a coherent condensate amplifies the magnetic
response) **does not transfer** to this causal-set construction, because the magnetic-channel
observable `Σ(Ã^{ij})²` is fed by the **incoherence** of the orientation texture — which
ferromagnetic ordering removes. The coupling produces a **disorder-controlled spacelike-noise
background anti-correlated with the order parameter**, not an emergent photon magnetic sector.
**E6c's curvature signal (1.17%) remains the only genuine, order-independent magnetic content
in the program; the ferromagnet does not add to it.**

## What this changes for E6 / RESEARCH_MAP

- **E6d is a [MORTO] for the orientation↔gauge amplification route** (Direction B):
  pre-registered, gate-anchored, falsified (G2 fail + order-suppression sign). It does NOT
  change E6's [FRONTEIRA TÉCNICA] status — it closes one of the two candidate amplifiers and
  leaves E6c's curvature route as the live one.
- The open problem is unchanged and sharpened: an **O(1)** magnetic fraction (mean `b²/e²>1`)
  must come from the **geometry/curvature** sector (E6c showed it grows there, monotonically),
  NOT from coupling the orientation order parameter. Candidate next steps remain on the
  curvature side — stronger/anisotropic/inhomogeneous curvature — not the ferromagnet.

## Anti-circularity

No relativistic literal inserted: the causal order is the conformal de Sitter light cone
(E6c), the E/B split uses only the embedding time column, `c` is never used. G0 reproduces
E6c bit-for-bit as a construction anchor (checked <1e-12 per run). The coupling identity
`Ã^{(5)(6)}=½λ²Σ(n×n')·ê_z` is verified numerically. The verdict is reached by the
pre-registered gates: the supra-threshold frac_B is reported in full and explicitly diagnosed
as a disorder artefact (G2), not inflated into a false success nor hidden. `e6_bd_core`,
the E6b core, and `e6c_curved_core` are reused, not modified; E6/E6b/E6c/E7 code untouched.

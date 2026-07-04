# E6d — Gates G0 / G1 / G2

> Pre-registered validation gates for the orientation↔gauge coupling on E6c's curved
> substrate (R̂=2, h=4). Checked against the measured data (`E6d_coupling.json`). Code:
> `e6d_coupling_core.py` (self-test) and `E6d_coupling.py` (`verdict()`), jun/2026.

The coupling is `Φ=A+λ(n⃗_i×n⃗_j)·ê_z`, realised inside E6's geometric E/B classifier by
augmenting the 5D de Sitter embedding with internal axes `λ(n·e1, n·e2)`. The internal–
internal area-bivector component then equals `½λ²Σ(n_c×n_{c+1})·ê_z` (the prompt's coupling),
the internal axes are spacelike → they feed the magnetic channel `b²`, and at `λ=0` the
augmented bivector collapses to the pure 5D E6c bivector.

## G0 — λ=0 on the curved substrate reproduces E6c (bit-for-bit) — **PASS**

At λ=0 the internal columns vanish, so `polygon_bivectors` sees exactly the 5D de Sitter
embedding of E6c. Checked per run: `|frac_B(λ=0) − frac_B^{E6c}| < 1e-12` for every (N, seed,
phase). Pooled N=2000: `frac_B(λ=0) = 0.01169` = E6c's R̂=2,h=4 value exactly. The coupling
is OFF when λ=0, by construction.

## G1 — λ=0 is phase-independent (orientation OFF) — **PASS**

At λ=0 the orientation field does not enter, so the disordered, J_c, and 2J_c runs give the
**identical** geometric fraction for each (N, seed) — confirmed to `<1e-12`. (Pooled N=2000:
all three phases read 0.01169 at λ=0.) This isolates that any λ>0 change is the coupling, not
a re-sprinkle.

## G2 — λ>0 with a DISORDERED ferromagnet must NOT amplify — **FAIL (decisive)**

G2 is the mechanism discriminator: if the magnetic rise is the hypothesised *ferromagnetic*
amplification, it must REQUIRE order, so the disordered control (J=0.02, |M|≈0.03) should
stay near the λ=0 baseline. It does **not**:

```
phase=disordered (|M|≈0.03), N=2000, pooled:
   λ=0.0  frac_B=0.01169   (baseline)
   λ=0.5  frac_B=0.01119
   λ=1.0  frac_B=0.04382
   λ=2.0  frac_B=0.27152   <-- 23× the baseline, with NO order present
```

The disordered field amplifies frac_B **more** than the ordered field (see below), so the
rise is a **spacelike-noise artefact**: any random internal vector field of magnitude λ
inflates `b²=Σ(Ã^{ij})²`. G2 FAILS → the rise is NOT the hypothesised order-sourced effect.

## Order-dependence (the decisive table) — order SUPPRESSES the magnetic fraction

At fixed λ=2, increasing ferromagnetic order **lowers** frac_B (the opposite of the
hypothesis):

```
λ=2.0, N=2000, pooled:
   disordered (|M|≈0.03)  frac_B = 0.27152
   J_c        (|M|≈0.56)  frac_B = 0.20497
   2J_c       (|M|≈0.82)  frac_B = 0.09879     <-- most ordered = least magnetic
```

Physical reason: coherent (ordered) texture has nearly-parallel neighbouring spins, so the
swept internal bivector area `n_c×n_{c+1}` is small; disordered texture sweeps large random
area. Hence **more order ⇒ less magnetic content** — anti-amplification, not Meissner.

## Gate summary

| Gate | Meaning | Result |
|---|---|---|
| G0 | λ=0 reproduces E6c bit-for-bit | **PASS** |
| G1 | λ=0 phase-independent (coupling OFF) | **PASS** |
| G2 | rise requires ORDER (disordered flat) | **FAIL** |
| — | order-dependence sign | **order SUPPRESSES** |

G0/G1 validate the construction; G2's failure (with the order-suppression sign) **falsifies
the amplification hypothesis** — the verdict in `E6d_synthesis.md`.

# E6d — Coupling analysis: what the orientation↔gauge coupling actually produces

> Companion to `E6d_synthesis.md`. The measurement (`E6d_coupling.py`, data
> `E6d_coupling.json`, figure `E6d_coupling.png`) on E6c's curved substrate (R̂=2, h=4),
> jun/2026. Reuses `polygon_bivectors` / `height_h_plaquettes` (E6/E6b) and `desitter_sprinkle`
> (E6c) VERBATIM; only the augmentation (the coupling) is new.

## Construction recap

Coupling `Φ_{ij}=A_{ij}+λ(n⃗_i×n⃗_j)·ê_z`. Realised by augmenting each event's 5D de Sitter
embedding `X_c` with two spacelike internal axes `λ(n_c·e1, n_c·e2)` (`{e1,e2}⊥ê_z`). The
augmented area bivector `Ã^{μν}=½Σ_c X̃_c∧X̃_{c+1}` (D=7) has:

- internal–internal `Ã^{(5)(6)} = ½λ²Σ_c (n_c×n_{c+1})·ê_z` — **exactly the prompt's coupling**
  (verified to 1e-11 in the core self-test);
- time–internal `Ã^{0,5}, Ã^{0,6}` → feed `e²` (electric);
- space–internal `Ã^{k,5}, Ã^{k,6}` → feed `b²` (magnetic).

E/B split and B-type test (`b²>e²`) are unchanged from E6. `λ=0` ⇒ exactly E6c.

## The measured λ-response (pooled N=2000, 3 seeds; P_tot ≈ 28k/cell)

```
            λ=0      λ=0.1    λ=0.5    λ=1.0    λ=2.0     |M|
disordered  0.01169  0.01112  0.01119  0.04382  0.27152   0.03
J_c         0.01169  0.01101  0.00925  0.03166  0.20497   0.56
2J_c        0.01169  0.01122  0.00882  0.01563  0.09879   0.82
```
`b²/e²` (mean per cell) rises from 0.968 (λ=0) to ≤0.986 (λ=2) — **the mean stays < 1 at all
λ and all phases**: even maximally coupled, the *typical* diamond remains electric; frac_B is
the fraction of cells in the spacelike tail.

## Three facts

1. **frac_B does rise with λ — but it is spacelike NOISE.** Appending an internal vector
   field of magnitude λ inflates `b²=Σ(Ã^{ij})²` (a sum of squares) regardless of physics.
   At λ=2 the internal coordinates (~O(2)) rival the geometric embedding (~R_dS=1.68), so a
   large minority (≈10–27%) of cells tip spacelike. This is generic variance, not a photon.

2. **The rise does NOT require order — it ANTI-requires it (G2 FAIL).** At λ=2 the
   *disordered* field gives the LARGEST frac_B (0.272), the deep-ordered field the SMALLEST
   (0.099): `disordered > J_c > 2J_c`. Coherent (ordered) texture has nearly-parallel
   neighbouring spins → small swept internal area `n_c×n_{c+1}` → little magnetic content;
   incoherent (disordered) texture sweeps large random area. So **more order ⇒ less magnetic**.

3. **At weak coupling order even SUPPRESSES below baseline.** At λ=0.5, 2J_c gives
   frac_B=0.0088 < the E6c baseline 0.0117 — the ordered texture's small, smooth internal
   area slightly *reduces* the spacelike fraction the curvature had produced.

## Interpretation

The Meissner/Higgs analogy (coherent condensate amplifies the magnetic response) is **not
realised** here, because the quantity that grows is sourced by the **incoherence** of the
orientation texture, which ordering removes. The orientation–gauge coupling, as posed, adds
magnetic-channel **variance** proportional to the texture's disorder — the exact opposite of
what a condensate-driven amplification needs. The literature warning (`E6d_literature.md`)
is borne out: a `Σ(Ã^{ij})²` observable cannot distinguish a coherent magnetic sector from
disordered spacelike noise, and the ordered ferromagnet supplies *less* of the latter.

What the coupling "produces", then, is **not** an amplified photon magnetic sector but a
**disorder-controlled spacelike-noise background**, anti-correlated with the order parameter.
E6c's curvature signal (1.17%) remains the only genuine, order-independent magnetic content;
the ferromagnet does not add to it and at weak coupling slightly erodes it.

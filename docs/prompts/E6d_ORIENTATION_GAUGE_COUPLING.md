# E6d — ORIENTATION↔GAUGE COUPLING: does the ferromagnet amplify E6c's magnetic sector?

> Extension of E6/E6b/E6c along "Direction B" (coupling). Pre-registered charter, executed
> jun/2026 (run despite E6c's success, by request). Results in `results/gauge/e6d/`. Result
> goes to RESEARCH_MAP.md, **not** to a paper. Does NOT modify E6, E6b, or E6c.

## Context

E6c gave the first positive photon-sector signal: de Sitter curvature (R̂=2, h=4) furnishes
a B-type (magnetic) fraction ≈1.17% — above 1% but far from O(1). E6d tests whether COUPLING
the ordered orientation ferromagnet (E1, O(3) field n⃗∈S²) to the gauge bivector AMPLIFIES
that 1.17% toward O(1) on the **curved** substrate (Meissner/Anderson–Higgs analogy: a
coherent condensate amplifying the magnetic response).

## Construction

Substrate = E6c's curved geometry (R̂=2, h=4), NOT flat. Coupling
`Φ_{ij}=A_{ij}+λ(n⃗_i×n⃗_j)·ê_z`, ê_z=⟨n⃗⟩. Realised exactly inside E6's geometric E/B
classifier: augment each event's 5D de Sitter embedding with internal axes `λ(n·e1, n·e2)`,
`{e1,e2}⊥ê_z`. Then the internal–internal area-bivector component is
`Ã^{(5)(6)}=½λ²Σ(n_c×n_{c+1})·ê_z` (the prompt's coupling, verified to 1e-11); the internal
axes are spacelike → magnetic channel; `λ=0` ⇒ E6c bit-for-bit. The orientation field lives
on the SAME causal link graph as the diamonds (E1/E2). `polygon_bivectors` /
`height_h_plaquettes` / `desitter_sprinkle` reused VERBATIM; only the augmentation is new.

## Gates (pre-registered)

```
G0 : λ=0 on the curved substrate reproduces E6c (frac_B≈0.0117) — bit-for-bit.
G1 : λ=0 any J reproduces E6c (coupling OFF).
G2 : λ>0 with a DISORDERED ferromagnet (J<J_c) stays ≈ G1 — i.e. the effect REQUIRES order.
```
On this graph (mean degree ≈65, dense) J_c≈0.05; used J=0.02 (disordered, |M|≈0.03), J_c=0.05
(|M|≈0.43), 2J_c=0.10 (deep-ordered, |M|≈0.82).

## Kill criterion (pre-registered)

```
SUCCESS      : frac_B > 0.05 AND grows with λ on the curved ORDERED substrate (needs order).
DEATH        : frac_B < 0.02 across the whole (λ,J) sweep -> no amplification; document output.
INCONCLUSIVE : frac_B grows but stays in [0.02, 0.05].
```

## Outcome (jun/2026) — [MORTO], amplification hypothesis FALSIFIED

**G0/G1 PASS** (λ=0 ⇒ E6c, per-run <1e-12). **G2 FAILS decisively.** frac_B does rise with λ
(up to 0.27 at λ=2), exceeding 0.05 — but the rise is sourced by **disorder**, not order:
at λ=2, `disordered 0.272 > J_c 0.205 > 2J_c 0.099` (more order = LESS magnetic), and at
λ=0.5 order even suppresses below baseline (0.0088<0.0117). Mean `b²/e²` stays <1 (≤0.986)
everywhere. The Meissner-style amplification is NOT realised: a `b²=Σ(Ã^{ij})²` observable is
inflated by any internal-field variance, and coherent (ordered) texture sweeps LESS internal
area than disordered. **The ordered ferromagnet does not amplify E6c's signal — it weakens
it.** The supra-threshold frac_B is reported honestly as a spacelike-noise artefact (G2),
not a success. **E6 stays [FRONTEIRA TÉCNICA]; the curvature route (E6c) is the only live one
toward an O(1) magnetic fraction.** Full analysis: `results/gauge/e6d/E6d_synthesis.md`.

## Deliverables

```
results/gauge/e6d/
  E6d_literature.md      — order-parameter↔gauge coupling in CST; the Meissner caveat
  e6d_coupling_core.py   — coupling on E6c substrate; reuses E6c geometry + E6/E6b E/B physics
  E6d_coupling.py        — sweep + gates G0/G1/G2 + pre-registered verdict + figure
  E6d_coupling.json      — numerical data
  E6d_coupling.png       — frac_B vs λ (per phase) and b²/e² vs λ
  E6d_gate.md            — gates G0/G1/G2 with the data
  E6d_coupling.md        — what the coupling actually produces
  E6d_synthesis.md       — synthesis with verdict
RESEARCH_MAP.md          — E6 row updated
```

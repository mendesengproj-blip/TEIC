# E6c — Literature: curvature, de Sitter causal sets, and the magnetic 2-cell

> Precedent search done before running E6c (jun/2026), to place the curved-geometry test
> in the CST literature and confirm the specific question (does background curvature furnish
> spacelike gauge 2-cells?) is novel. Posture as in E6/E6b/E7: no relativistic literal
> inserted; the geometry is used only to define the causal order and the area bivector.

## What exists

1. **de Sitter sprinklings are standard CST.** The "everpresent Λ" program
   (Ahmed–Dodelson–Greene–Sorkin 2004; Sorkin) sprinkles causal sets into de Sitter and
   FRW backgrounds to compute fluctuations of the cosmological constant. The TEIC program
   itself uses de Sitter sprinklings in the LAMBDA campaigns (L1–L3, LD). So sprinkling a
   **de Sitter causal set** is well-trodden — what is new here is reading the **gauge
   E/B (area-bivector) split** off it.

2. **de Sitter is conformally flat.** dS_4 in the flat (inflationary) slicing has metric
   `a(η)² (−dη² + dx²)` with conformal time `η = −(1/H) e^{−Hτ}`. The light-cone causal
   order depends only on the conformal class, so the de Sitter causal order in `(η, x)` is
   **identical to the Minkowski order** in those coordinates. This is textbook (Hawking–
   Ellis); E6c exploits it so the causal-set ENSEMBLE is curvature-independent and the gate
   (H→0 = E6b) is exact and continuous. Curvature enters only through the **embedding**.

3. **5D hyperboloid embedding of dS_4.** `−X0² + X1² + X2² + X3² + X4² = R²` with the
   standard flat-slicing parametrisation is textbook. It gives a curvature-aware set of
   coordinates in which the area bivector `A^{μν}=½Σ_c X_c∧X_{c+1}` can be split into
   electric (`A^{0i}`) and magnetic (`A^{ij}`) parts by exactly the E6 rule — now in D=5.

4. **Gauge fields on causal sets** (Sverdlov 0807.2066; Sverdlov–Bombelli 0905.1506)
   build U(1)/Yang–Mills **actions** via holonomies on causal diamonds — the conceptual
   ancestor of E5/E6/E7. None of them builds a BD-smoothed gauge **operator**, and none
   asks whether **background curvature** changes the electric/magnetic content of the
   diamond 2-cells. (Confirmed in E6_literature.md / E7_literature.md: all BD/Dowker–Glaser
   operators are scalar-only.)

## The gap E6c fills

E6/E6b established the obstruction to the BD-gauge `E²−B²` photon precisely: on a **flat**
Poisson causal set the diamond 2-complex is almost entirely **electric** (height-2 exactly,
taller 2h-gons up to a non-growing ~0.25% tail). The missing ingredient is a **spacelike
(magnetic) 2-cell with O(1) magnetic fraction**. E6b tested the "taller diamond" route and
ruled it out. **E6c tests an orthogonal route: spatial curvature.** The physical intuition
is concrete — in a curved background the two ascending geodesics that bound a causal diamond
**bend**, so the diamond's area bivector need no longer be locked to the straight timelike
tip→tip extent, and can acquire spacelike content. No prior CST work measures the
curvature-dependence of the gauge E/B fraction; this is the novel test.

**Pre-registered, before measurement:** the question is whether curvature raises `frac_B`
through the E6b floor (0.001) and to the success threshold (0.01), and whether it does so
only at extreme (Planckian) curvature or already at mild curvature — with the mandatory
gate that R_dS→∞ reproduce E6b exactly.

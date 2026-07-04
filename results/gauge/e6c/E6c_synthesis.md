# E6c — Curved geometry: does background curvature furnish the magnetic 2-cell?

> Direct extension of E6 (E6_3b) and E6b. Code: `e6c_curved_core.py` (de Sitter geometry —
> conformal-flat sprinkle for the causal ORDER + 5D hyperboloid embedding for the E/B split;
> reuses `../e6/e6_bd_core.py` and `../e6b/e6b_diamond_height_core.py` VERBATIM for the E/B
> physics and the 2h-gon topology), `E6c_1_curvature_scan.py` (sweep + gate + figure). Data:
> `E6c_1_curvature_scan.json`. Figure: `E6c_1_curvature_scan.png`. Literature first:
> `E6c_literature.md`. Run jun/2026. **Pre-registered gate + kill criterion** checked
> against the measured data. **Result goes to RESEARCH_MAP, not to any paper.**

## The question, and why it is well-posed

E6/E6b nailed the obstruction to the BD-gauge `E²−B²` photon: on a **flat** Poisson causal
set the causal-diamond 2-complex is essentially all **electric** (timelike area bivector,
`b²<e²`). Height-2 diamonds are 100% electric (`frac_B = 0.0000` exact); the "taller
diamond" route (E6b, 2h-gons h≤6) only yields a non-growing ~0.25% magnetic tail whose
per-cell `b²/e²` *shrinks* with height. The missing ingredient is a **spacelike (magnetic)
2-cell with O(1) magnetic fraction**.

E6c tests an **orthogonal** route the flat scan could not reach: **spatial curvature**. In a
curved background the two ascending geodesics bounding a causal diamond **bend**, so the
diamond's area bivector need not stay locked to the straight timelike tip→tip extent and can
acquire spacelike (`A^{ij}`) content. We use **de Sitter dS₄** (flat slicing), which is

- **conformally flat** → the causal ORDER in conformal coords `(η, x)` is exactly the
  Minkowski order of E6/E6b. We sprinkle a **cubic conformal box**, so the causal-set
  ENSEMBLE (hence the 2h-gon diamond statistics) is **identical to E6b at every curvature** —
  no aspect-ratio collapse, the curvature is the *only* variable;
- embeddable on the **5D hyperboloid** `−X0²+X1²+X2²+X3²+X4²=R²`, whose area bivector feeds
  `e6_bd_core` VERBATIM (the E/B split already works in any dimension; here D=5). Curvature
  enters **only** through the bent embedding. As `R_dS→∞` the embedding → the flat 4D
  bivector of E6b (`X0→τ, Xk→x_k, X4→const`), so the Minkowski limit is reproduced exactly.

Curvature radius is reported as `R̂ = R_dS / ℓ`, in units of the mean spacing `ℓ=ρ^{−1/4}`;
`R̂=∞` is Minkowski (the gate), `R̂=2` is curvature radius ≈ 2 lattice spacings (extreme,
trans-Planckian). No relativistic literal is inserted: the order is the sprinkling's own
conformal light cone, the E/B split uses only the embedding time column — identical to E6/E6b.

## Mandatory gate (R_dS = ∞ must reproduce E6b) — **PASS**

```
h=2  frac_B = 0.00000  (Wilson-hi 0.00013 < 0.001)   ✓  E6 exact zero reproduced
h=3  frac_B = 0.00243  (in [0.001, 0.0045])          ✓  E6b value reproduced
```
The R̂=∞ branch is byte-for-byte the E6b sprinkle (same RNG), so the gate holds by
construction; it is also checked numerically. Without this PASS no curved verdict would be
issued.

## Results (R̂ = ∞ → 2, heights h=2,3,4, N≈500/1000/2000, 3 seeds, ρ=2)

Pooled over seeds at the decisive N≈2000 (P_tot ≈ 28k–30k per cell — well-sampled, not the
4-cell tail E6b warned about). `wlo/whi` = 95% Wilson bounds; `b²/e²` = mean per-cell
magnetic content.

```
  R̂    h   P_tot    nB   frac_B    wlo      whi     b²/e²
  ∞    2   30000     0  0.00000  0.00000  0.00013  0.222     <- E6 exact zero (gate)
  ∞    3   30000    73  0.00243  0.00194  0.00306  0.142     <- E6b reproduced (gate)
  ∞    4   27502    70  0.00255  0.00202  0.00321  0.112
 16    3   30000    82  0.00273  0.00220  0.00339  0.260
 16    4   27887    76  0.00273  0.00218  0.00341  0.228
  8    3   30000    96  0.00320  0.00262  0.00391  0.510
  8    4   27887    91  0.00326  0.00266  0.00400  0.480
  4    3   30000   128  0.00427  0.00359  0.00507  0.827
  4    4   27887   148  0.00531  0.00452  0.00623  0.814
  3    3   30000   163  0.00543  0.00466  0.00633  0.910
  3    4   27887   209  0.00749  0.00655  0.00858  0.903
  2    2   30000     0  0.00000  0.00000  0.00013  0.970     <- h=2 STILL exactly electric
  2    3   30000   204  0.00680  0.00593  0.00780  0.970
  2    4   27887   326  0.01169  0.01049  0.01302  0.968     <- crosses 0.01, Wilson-lo>0.01
```

Four facts, all decisive:

1. **Curvature genuinely furnishes magnetic content — the opposite of the height scan.**
   `frac_B` rises **monotonically** with curvature at every height (h=4: 0.0026→0.0273×10⁻¹
   ... → 0.0117 as R̂: ∞→2), and the per-cell `b²/e²` rises **8.6×** (h=4: 0.11→0.97;
   h=3: 0.14→0.97). Where taller diamonds did *nothing* (E6b: tail flat/declining), bending
   the diamond steadily tilts its area bivector toward spacelike. This is a real, clean,
   monotone curvature effect.

2. **The pre-registered SUCCESS criterion fires — but marginally, only at extreme
   curvature.** At R̂=2 (R_dS≈1.68ℓ), h=4: `frac_B = 0.01169` with **Wilson-lo = 0.01049 >
   0.01** on 27 887 plaquettes — a statistically significant exceedance of the 0.01 success
   threshold, and **N-stable** (frac_B = 0.0084→0.0116→0.0117 for N=500→1000→2000,
   saturating just above 0.01; *not* a low-statistics fluctuation). This is the single
   decisive cell that clears the bar, and it sits at the most extreme curvature tested.

3. **The height-2 exact zero is CURVATURE-IMMUNE.** Unlike taller cells, `frac_B(h=2) =
   0.00000` at **every** curvature, including R̂=2 where `b²/e²` reaches 0.97. A height-2
   diamond always contains the timelike tip→tip extent, which no amount of curvature tips
   spacelike — a sharper structural statement than E6b's "exact only at h=2": it is exact at
   h=2 *for all curvatures*.

4. **The typical diamond is still electric.** Even at R̂=2 the mean `b²/e²` saturates at
   0.97 < 1 — the *average* diamond remains (barely) electric; the magnetic sector is a
   ~1.2% tail of cells that tip over, not an O(1) magnetic fraction. Curvature pushes the
   bivector population to the very edge of the light cone (E²≈B²) but does not invert it.

## Verdict (against the pre-registered criterion)

```
PRE-REGISTERED:
  GATE      R_dS=∞ reproduces E6b                       -> REQUIRED before any verdict
  SUCCESS   frac_B > 0.01 at some R_dS, Wilson-lo>0.01   -> report minimal R_dS ("curv. radius")
  DEATH     frac_B < 0.001 across the WHOLE sweep        -> [FRONTEIRA-ESTRUTURAL], run E6d
  INCONCL.  small non-zero, doesn't clear 0.001/0.01     -> report honestly

MEASURED  ->  GATE PASS;  SUCCESS (marginal, curvature-extreme).
  - Gate PASS: Minkowski reproduces E6b (h2=0.0000, h3=0.0024) exactly.
  - SUCCESS by the letter of the criterion: R̂=2 (R_dS≈1.68ℓ), h=4, frac_B=0.01169,
    Wilson-lo 0.0105 > 0.01, N-stable, 28k plaquettes.
  - DEATH did NOT fire: frac_B is everywhere ≫ 0.001 (the floor) — far from a clean death.
  - Honest calibration: the crossing is MARGINAL (1.17%, just over threshold) and reached
    ONLY at trans-Planckian curvature (R_dS ≈ 2 lattice spacings); the mean diamond stays
    electric (b²/e²=0.97<1). What is robust and large is the monotone b²/e²(curvature)
    trend, a genuine proof-of-principle that curvature tilts the bivector toward spacelike —
    not a fully-formed O(1) magnetic sector.
```

**Physical reading.** E6c is the first of the two E6-follow-up routes to give a *positive*
signal. Where E6b showed taller diamonds do not help (the tail does not grow), E6c shows
**curvature does help, monotonically** — the area bivector of a bent causal diamond acquires
real spacelike content, and at extreme curvature the magnetic fraction crosses the
pre-registered 0.01 threshold with statistical significance. But the win is **marginal and
extreme-curvature-only**: a usable, O(1) magnetic sector (`b²/e²>1` on a finite fraction of
cells) is *approached but not reached* — the population saturates at the light cone (E²≈B²)
rather than inverting. So curvature is a genuine ingredient toward the BD-gauge photon, not
the complete answer on its own.

## What this changes for E6 / RESEARCH_MAP

- **The DEATH criterion did NOT fire**, so E6 does **not** flip to [FRONTEIRA-ESTRUTURAL],
  and **E6d (orientation↔gauge coupling) is NOT triggered** — per the prompt's sequencing
  ("Se E6c tiver SUCESSO: E6d pode não ser necessária"). The curved-geometry route is alive.
- E6 is **refined upward**, not killed: the E6/E6b statement "no usable magnetic sector on
  the bare substrate" is now qualified as **flat-space-specific**. Under curvature the
  magnetic fraction grows monotonically and **crosses 0.01 at trans-Planckian curvature** —
  the obstruction is *curvature-liftable*, though only marginally at the curvatures tested.
- The sharpened open problem: get an **O(1)** magnetic fraction (mean `b²/e²>1`) rather than
  a ~1% tail at the light-cone edge — e.g. at still stronger curvature, with anisotropic /
  inhomogeneous curvature, or via the E6d coupling. The "spacelike 2-cell" that E6/E6b
  declared missing is now shown to **exist and grow with curvature**; what remains is making
  it the typical cell, not the tail.

## Anti-circularity

No relativistic literal inserted: the causal order is the sprinkling's own conformal light
cone (de Sitter is conformally flat — a true geometric fact, not an imposed frame), and the
E/B split uses only the embedding time column, identical to E6/E6b; `c` is never used (this
campaign measures only the bivector-signature fraction). The Minkowski limit reproduces
E6b's exact 0.0000 (h=2) and 0.0024 (h=3) as a bit-for-bit gate, checked numerically before
any curved verdict. The verdict is the pre-registered SUCCESS branch, reached by measurement
and reported **with its marginality and curvature-extremity stated plainly**, not inflated to
"photon solved" nor deflated to a death. The decisive cell is well-sampled (28k plaquettes,
N-stable) — explicitly contrasted with E6b's 4-cell fluctuation caveat. `e6_bd_core` and the
E6b core are reused, not modified; E6/E6b/E7 code untouched.

# E6-3 — BD-gauge LORENTZIAN operator: gates H1/H2 (FRONTIER, precisely diagnosed)

> Pre-registered in `E6_BD_GAUGE.md` and the E6_BD_GAUGE_LORENTZIAN prompt. Code:
> `e6_bd_core.py` (operator), `E6_3_bd_lorentzian.py` (gates + figure),
> `E6_3b_eb_population.py` (the why). Data: `E6_3_bd_lorentzian.json`,
> `E6_3b_eb_population.json`. Figure: `E6_3_bd_lorentzian.png` (the central diagnostic
> λ(k,ω)). Literature first: `E6_literature.md`. Run jun/2026.

## What was built (the open construction the charter named)

The indefinite-signature gauge operator `M_L = Bᵀ diag(w) B` on the height-2
causal-diamond plaquettes. Each plaquette's **area bivector** `A^{μν} = ½ Σ_c x_c∧x_{c+1}`
is computed from the four vertices; it is split **E-type** (timelike bivector,
`A^{0i}`-dominant → electric, `e²=Σ(A^{0i})²`) vs **B-type** (spacelike,
`A^{ij}`-dominant → magnetic, `b²=Σ(A^{ij})²`), and the two enter the quadratic form with
opposite signs via `w_P=(b²−e²)/(b²+e²)` (the normalised Minkowski signature). This is the
1-form analogue of the alternating BD scalar weights — the *"Hodge star / 2-cell weight"*
the charter flagged as open, and which `E6_literature.md` confirmed **does not exist** in
the literature (all BD/Dowker–Glaser operators are scalar; Sverdlov–Bombelli give a gauge
*action*, not a smeared operator, and no Lorentzian dispersion).

## Results

```
STAGE 0  (validation, open 4D lattice 8^4, free-Maxwell answer KNOWN):
  E/B split exact: 9408 electric (time-plane) + 9408 magnetic (space-plane) cells
  symbol zero crossing follows omega = c·k,  c = 1.05  (dev 3%)   -> PASS
  => the operator + symbol method correctly recovers the photon where Maxwell holds.

H1  (gauge invariance, causal sprinkling N=224):
  |B G| = 0.0 (exact),  |M_L (G lam)| / |M_L| = 5.7e-16          -> PASS (machine prec.)
  Confirmed AUTOMATIC for the indefinite signature: F_P=(d theta)_P, BG=0 (=discrete
  d^2=0), so M_L(G lam)=Bᵀ W (B G) lam = 0 for ANY weights, even negative ones. The
  central worry of a Lorentzian gauge action -- that the indefinite signature might
  break gauge invariance -- is structurally answered NO.

H2  (dispersion, causal sprinkling):
  norm-mode   c = nan,  zero crossings = 0/6
  sharp-mode  c = nan,  zero crossings = 0/6
  euclid control (= E6-2): no crossing (stays positive)          -> H2 does NOT pass

WHY (E6-3b, 9 sprinklings, rho 0.5-1.0, N up to 626, P up to 20000):
  fraction of B-type (spacelike/magnetic) plaquettes = 0.0000  (EXACTLY, every run)
  max signature weight = -0.040  (always < 0, i.e. always electric)
  mean w ~ -0.65
```

## The precise diagnosis (sharper than "non-locality")

**Every height-2 causal diamond is electric.** A diamond `i→a→k→b→i` has `i` as its
unique past tip and `k` as its unique future tip; `i` and `k` are timelike-separated, so
the enclosed area bivector *always* contains that timelike past-tip→future-tip extent and
is `A^{0i}`-dominant (`b²<e²`). Across 9 independent sprinklings the B-type fraction is
**exactly 0** and the weight never reaches 0 (max −0.04). **The magnetic (spacelike)
2-cells that the indefinite `E²−B²` operator must balance the electric ones against are
absent from the causal order's height-2 complex.**

Consequently the symbol is `λ(k,ω) ≈ −E²(ω) ∝ −ω²` — a single-signed (everywhere
negative) surface with no `k²` magnetic term to create a `k²−ω²` zero locus. It has a
maximum at ω≈0 and **never crosses zero**, so there is no `ω=ck` light cone. This is *not*
the Euclidean-action failure of E6-2 (positive-definite, min at ω=0); it is the
complementary, opposite-sign failure of an operator that is correctly indefinite but has
an **empty magnetic sector**. The figure shows all three side by side: the lattice (clean
red/blue with the zero crossing on ω=k), the causal norm operator (all blue, no crossing),
and the Euclidean control (all red, no crossing).

This refines the E5/E6-1 "non-locality" framing: the obstruction is concretely that the
**height-2 causal-diamond 2-complex carries only timelike 2-cells**. (It is consistent
with E6-1's large harmonic sector — the complex is far from a manifold triangulation —
but the H2 obstruction is the more specific statement: no spacelike plaquettes exist to
furnish the `B²` term.)

## Verdict (pre-registered outcome: "FRONTEIRA TÉCNICA — H1 PASS, H2 FAIL")

```
H1 (gauge invariance):           PASS  (5.7e-16; automatic for indefinite signature)
STAGE 0 (method validation):     PASS  (lattice c=1.05, exact E/B split)
H2 (omega=ck zero crossing):     FAIL on the causal set  (0/6 crossings)
  reason IDENTIFIED:             height-2 causal diamonds are 100% electric
                                 (B-type fraction = 0.0000, structural across seeds);
                                 no spacelike 2-cells -> no B^2 term -> no light cone.
H3 (polarisation):               NOT RUN -- pre-registered as gated behind H2; H2 did
                                 not pass, so per protocol H3 is not reached.

[FRONTIER, technical] The BD-gauge Lorentzian operator is gauge-invariant by
construction (and the indefinite signature does NOT spoil that), and it reproduces the
free photon omega=ck on a regular 4D lattice. But on the bare causal set it cannot
propagate, for a now-precise reason: the causal order's height-2 diamond plaquettes are
all electric (timelike bivectors), so the magnetic half of E^2-B^2 is empty. Signature
solved; the missing piece is a SPACELIKE 2-cell construction, not a different weighting.
```

## What this rules out, and the concrete next direction

- It is **not** a weighting problem: `norm`, `sharp`, and `raw` all fail identically,
  because there is genuinely no magnetic content to weight. A "different E/B separation"
  (Fase E option) cannot help.
- It is **not** a finite-size accident: B-type fraction is exactly 0 from N=199 to 626.
- The **specific open construction** this campaign isolates: a causal-set **spacelike
  2-cell** (a plaquette whose area bivector is spacelike), e.g. built from pairs of
  events sharing a common past and common future at comparable "time" rather than the
  height-2 timelike diamond. Whether such cells can be defined Lorentz-invariantly on a
  sprinkling (without a preferred frame to call events "simultaneous") is the genuine
  research frontier — and the reason this is hard is itself the measured content of E6-3.
  This is original information for the CST literature, which (per `E6_literature.md`) has
  no BD gauge operator and has never measured this.

## Anti-circularity

No relativistic literal inserted: the E/B split uses only the embedding time column (the
sprinkling's own causal/time direction); `c` is the *fitted* slope of the lattice zero
crossing (1.05), never inserted; the causal-set H2 used the identical machinery. The
verdict is the pre-registered FRONTIER branch, reached by measurement, not adjusted to
escape an outcome. E4/E5/E7 untouched. The most defensible published photon statement
remains E4's (orientational order + relativistic scalar Goldstone; the photon located
structurally but not propagating in the gauge-link sector).

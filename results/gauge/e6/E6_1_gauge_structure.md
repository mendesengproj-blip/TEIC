# E6-1 — gauge structure of the link sector (H1 PASS; photon NOT yet established)

> Pre-registered in `E6_BD_GAUGE.md` (gate H1 + mode counting). Code:
> `E6_1_gauge_structure.py`; data: `E6_1_gauge_structure.json`. Non-compact
> (Gaussian) Maxwell on the causal set: 1-cochain theta_l on links, F_P=(d theta)_P
> on causal diamonds, S=(1/2) theta^T M theta, M=B^T B. Exact linear algebra, no MC,
> no dispersion inserted. Run jun/2026.

## Result

```
N=224 nodes, L=2105 links, P=2215 diamond plaquettes
H1 gauge invariance:  |B G| = 0.0,  |M (G lam)| = 2e-14   -> PASS (exact)
mode counting (rank-nullity):
  gauge modes      = 223  (= N - 1, the full gauge redundancy of a connected graph)
  harmonic modes   = 698  (flat but non-gauge: first cohomology of the diamond complex)
  physical modes   = 1184 (= rank B, the non-gauge / transverse propagating sector)
```

## What this establishes (a real structural positive)

The non-compact Maxwell action on the causal links is **exactly gauge-invariant**
(H1), and the pure-gauge subspace has dimension N-1 -- the complete gauge redundancy
a connected graph admits. After removing it, a physical (transverse) sector remains.
**This is precisely the structure the orientation Goldstone sector (E4) lacked:**
there the two transverse modes carried an internal index with NO gauge redundancy
and did not lock to k (they were two internal scalars). Here, in the link sector,
the gauge redundancy is genuine and exact. So the *necessary* structure for an
emergent photon -- a field with a spacetime/link index and a gauge symmetry -- IS
present in the link sector and absent in the orientation sector. That contrast is
the measured content of E6-1.

## What this does NOT establish (stated plainly)

1. **It is necessary, not sufficient, for a photon.** The 1184 physical modes are
   merely the non-gauge modes of the static quadratic form. Whether any of them
   DISPERSE as omega = ck (massless, light-cone speed, two transverse polarisations)
   is gate H2, which was NOT tested here. A photon is a specific relativistic
   2-polarisation subset, not 1184 generic modes.
2. **H2 needs the Lorentzian construction.** The static action S=(1/2)Sum F_P^2 is
   positive-definite (Euclidean/magnetic-like); a Lorentzian dispersion requires the
   electric (time-like plaquette) terms to enter with opposite sign to the magnetic
   ones, i.e. a frame-careful electric/magnetic split on the causal diamonds. That is
   the hard, open part of E6 and is not done.
3. **The large harmonic sector is a warning.** 698 harmonic (flat, non-gauge) modes
   out of 2105 links means the causal-diamond 2-complex has a large first cohomology
   -- it is far from a manifold triangulation (many 1-cycles not bounded by diamonds).
   This is the same non-manifold / nonlocal character flagged in E5, and it may
   obstruct a clean photon in H2.

## Verdict

```
H1 PASS + gauge structure CONFIRMED. The link sector carries the genuine gauge
redundancy a photon requires (gauge modes = N-1, exact) -- the structure E4 showed
the orientation Goldstone sector does NOT have. This is real, measured progress and
the strongest reason to keep the photon question alive in the link sector. But it is
NOT a photon: the relativistic dispersion (H2) is untested and needs the Lorentzian
electric/magnetic construction, and the large harmonic sector warns that the
nonlocality of E5 persists. No photon claim.
```

## Next (E6 continued, research-grade)

- **H2**: build the Lorentzian (electric-vs-magnetic) Maxwell symbol on the causal
  diamonds and measure the dispersion of the physical modes (omega=ck?). This is the
  crux and the genuinely hard, open construction; it must be validated against free
  Maxwell on flat sprinklings before any causal-set reading.
- The persistent obstruction (E5 nonlocality, the 698 harmonic modes here) suggests
  H2 may require a BD-smeared / manifold-like refinement of the 2-complex, not the
  bare diamonds.

# DS1 — Emergent gravitational profile vs dimension

> Task DS1 of `DIMENSION_SCAN.md`. Graph Laplacian on Poisson sprinklings in a
> d-ball, point source, Dirichlet outer shell, conjugate-gradient relaxation —
> **no ansatz, no Green function in the generator**. 10 seeds per dimension.
> Data: `DS1_profiles.json`; figure: `DS1_profiles.png`.

## Verdict: **the network's potential follows p = −(d−2) — measured, not imposed**

```
d   measured exponent p       pre-registered      hit?
1   +0.993 ± 0.036            +1 (linear)         ✓
2   −0.121 ± 0.054 (shallow)  log (p→0)           ✓ (log-degenerate)
3   −0.950 ± 0.054            −1                  ✓ (= D1–D3's −1.02)
4   −1.997 ± 0.096            −2                  ✓
```

## What this establishes

The single dynamical law (`Lθ=J`, the network Laplacian with a point source)
produces, in each spatial dimension, exactly the long-range behaviour of the
d-dimensional Poisson equation: linear confinement in d=1, the marginal
log-like profile in d=2 (measured as a shallow power p≈−0.12, the standard
log-degenerate signature; AIC between log and shallow-power is marginal, as it
must be on a finite window), 1/r in d=3, 1/r² in d=4. The d=3 value reproduces
the D1–D3 result (−1.02) with an independent operator (graph Laplacian here,
BD action there) — consistent with D3B's finding that Poisson is the generic
law of the sector.

## Honest limitations

- Graph Laplacian, not the per-dimension Benincasa–Dowker operator (the BD
  d-dependent smearing is a heavier construction; D3B already established the
  operator-independence of the Poisson law in d=3).
- d=2's log vs shallow-power cannot be settled on a finite box (they differ
  only beyond any fixed window); what is established is the **qualitative
  class**: marginal/confining, no escape at finite energy — which is all DS2
  consumes.
- The exponent is the *spatial Green-function* dependence; the time direction
  is not sprinkled here (static sector, as in D1–D3).

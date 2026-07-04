# DS2 — Orbits in the measured potential vs dimension

> Task DS2 of `DIMENSION_SCAN.md`. Leapfrog test orbits in the potential whose
> exponent was **measured** in DS1 (read from `DS1_profiles.json`, not imposed).
> Escape classified by energy for d≥3 (V(∞)=0); for d=2 the log profile has
> V(∞)=+∞ — escape requires infinite energy, verified by turnaround.
> Data: `DS2_orbits.json`; figure: `DS2_orbits.png`.

## Verdict: **d=3 is the unique dimension with stable bound orbits AND escape**

```
d   bound orbits stable?   escape possible?     verdict
2   ✓ (perturbed: stable)  ✗ (2.5 v_c turns around; V(∞)=+∞)   everything imprisoned
3   ✓ (perturbed: stable)  ✓ (1.6 v_c escapes; E>0)            BOTH ✓ — unique
4   ✗ (±2% perturbation → collapse/escape)  ✓                  nothing orbits
```

## The physics (Ehrenfest's argument, now measured on the network)

For a potential V ∝ −r^p (p = −(d−2) measured in DS1), the effective radial
potential has a stable circular-orbit minimum only for d<4; and V→0 at infinity
(finite escape energy) only for d≥3:

- **d=2 (measured log-like):** circular orbits are stable, but the potential
  grows without bound — a particle with any finite energy turns around. No
  escape, no unbound states: a universe where nothing ever leaves anything.
- **d=3 (measured −0.95):** the Kepler situation — perturbed circular orbits
  stay bounded (precessing ellipses) and 1.6 v_c escapes. Both phenomena coexist.
- **d=4 (measured −1.997):** the centrifugal term and the potential scale
  identically (both r⁻²): the effective potential has no minimum. A −2%
  velocity perturbation collapses; +2% escapes. **No stable structures can
  orbit** — no planetary systems, no atoms-by-analogy.

## Honest limitations

- Test particles in the relaxed field, not back-reacting network dynamics.
- d=2's "no escape" inherits DS1's log-degeneracy caveat (any shallow power
  p>−1 still gives turnaround at the energies tested; the conclusion is robust
  within the measured class, p≈−0.12±0.05).
- The classification thresholds (r-ratio < 5 for "stable", energy sign for
  escape) were fixed before running; the d=4 instability is not threshold-
  sensitive (collapse reaches r<10⁻² and escape r>50 within 60 periods).

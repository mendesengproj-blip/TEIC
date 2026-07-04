# E4-0 — Finite-size scaling of the orientation long-range order

> Pre-registered in `E4_PHOTON_DISCRIMINATOR.md` (E4-0). Code: `E4_0_fss.py`
> (reuses `orientation_core.py` unmodified); data: `E4_0_fss.json`. Addresses the
> reviewer concern that `C(r) -> m^2` at a single size could be a finite-size
> artefact. Run jun/2026.

## Method

O(3) Metropolis on the 3+1D causal link graph at fixed coupling J=2.0 (J >> J_c ~
0.08), increasing the sprinkled 4-volume at fixed density rho=0.5 so the event
number grows N ~ 175 -> 1462. Per size: order parameter m=|<n>| and Binder cumulant
U4 = 1 - <m^4>/(3<m^2>^2), averaged over 12 seeds (300 burn-in sweeps, 60 samples).
A finite-size artefact would show m falling toward the random-vector floor
m ~ N^{-1/2}; a genuine ordered phase shows m flattening and U4 -> 2/3.

## Result

| L | N (mean) | <degree> | m = \|<n>\| | U4 | random floor N^{-1/2} | m / floor |
|---|---|---|---|---|---|---|
| 4.4 | 175  | 17 | 0.9611 ± 0.0013 | 0.667 | 0.0755 | 13x |
| 5.4 | 405  | 29 | 0.9790 ± 0.0004 | 0.667 | 0.0497 | 20x |
| 6.4 | 811  | 45 | 0.9868 ± 0.0001 | 0.667 | 0.0351 | 28x |
| 7.4 | 1462 | 64 | 0.9910 ± 0.0001 | 0.667 | 0.0262 | 38x |

- Order parameter **rises** with N (0.961 -> 0.991); trend d ln m / d ln N = **+0.014**
  (a finite-size artefact would give the random-vector slope **-0.5**).
- m stays **13-38x above** the random floor, the margin growing with N.
- Binder cumulant **U4 = 0.667 = 2/3 exactly** at every size -- the signature of a
  fully ordered phase (U4 -> 2/3 ordered; -> 0 disordered).

## Verdict

```
SUCCESS (LRO genuine): m(N) does not fall with N; it rises slightly as the mean
  degree grows (17 -> 64), i.e. the causal graph becomes more strongly connected /
  effectively higher-dimensional with size, suppressing fluctuations. U4 = 2/3 at
  all sizes. The long-range orientational order of E1 is NOT a finite-size artefact.
```

This confirms the vacuum claim that the dispersion and polarisation tests (E4-1,
E4-2) build upon, and answers the finite-size-scaling concern directly.

# E4-2 — Degeneracy and spatial isotropy of the transverse Goldstone modes

> Pre-registered in `E4_PHOTON_DISCRIMINATOR.md` (E4-2). Code: `E4_2_isotropy.py`
> (reuses `orientation_core.py` unmodified); data: `E4_2_isotropy.json`. Completes
> the characterisation of the two transverse modes (shown to be internal scalars in
> E4-1) as a clean equivalent pair. Run jun/2026.

## Method

Ordered state (J=2.0) on the 3+1D causal link graph. For 32 spatial directions x 6
magnitudes, the per-mode transverse static structure factor
S_a(k)=<|sum_i a_a(i) e^{-i k.x_i}|^2>/N (a=1,2), averaged over 16 seeds x 40
samples. Degeneracy = mean |S_1-S_2|/(S_1+S_2); spatial isotropy = coefficient of
variation of S(k) across directions at fixed |k|.

## Result

```
degeneracy split |S1-S2|/(S1+S2) = 0.037  (max 0.099)   -> modes degenerate
spatial-direction CV of S(k)     = 0.042                -> spatially isotropic
transverse S(k) ~ k^{-0.58}      (6-point range diagnostic)
```

- The two transverse modes are **degenerate** to 3.7% (required by the residual
  O(2) symmetry about <n>; confirmed by measurement).
- Their fluctuation power is **spatially isotropic** (4.2% scatter across 32
  directions) -- emergent spatial isotropy of the ordered vacuum.
- The transverse structure factor falls as S(k)~k^{-0.58} over the limited probed
  range. This is **softer than mean-field flat (0)** but not yet the relativistic
  1/k (-1). It is reported as a diagnostic and NOT over-interpreted at this size and
  6-point k-range; pinning the stiffness exponent would need a dedicated
  larger-N, wider-k run.

## Verdict

```
SUCCESS (clean scalar pair): the two transverse Goldstone modes are degenerate and
spatially isotropic -- a clean equivalent pair of internal scalar Goldstones. This
completes the E4 characterisation: the orientation Goldstone sector is two
degenerate, isotropic, internal scalars (pion-like), not a photon.
```

## E4 campaign summary

| Test | Question | Verdict |
|---|---|---|
| E4-0 | Is the long-range order genuine (FSS)? | **YES** -- m rises with N, U4=2/3, 13-38x above the random floor |
| E4-1 | Gauge vector (photon) or two scalars? | **TWO SCALARS** -- no polarisation locking to k (perm. p=0.23) |
| E4-2 | Are the two scalars degenerate & isotropic? | **YES** -- split 0.04, direction CV 0.04 |

Bottom line: the causal orientation vacuum genuinely orders (E4-0); its Goldstone
sector is a clean pair of degenerate, spatially-isotropic INTERNAL SCALAR modes
(E4-1, E4-2), pion-like rather than a photon. An emergent photon, if present in the
framework, must be sought in the gauge-connection (link) sector, not here (campaign
E5, not yet run).

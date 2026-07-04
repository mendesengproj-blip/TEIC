# DS4 — The topological barrier, measured: 2D unwinds, 3D is blocked

> Task DS4 of `DIMENSION_SCAN.md`. The SAME deformation family
> U_s = exp(iF(r) n̂_s·σ), n̂_s = normalize((1−s)·r̂_⊥ + s·ẑ), applied in 2D and
> 3D; quaternion engine from `su2_core` (real arithmetic), B from
> `su2_core.baryon_number`. Data: `DS4_topology.json`; figure: `DS4_topology.png`.

## Verdict: **π₂(S³)=0 vs π₃(S³)=ℤ, measured as energetics** — the 2D hedgehog unwinds smoothly to the vacuum; the 3D unwinding attempt hits a singular barrier whose peak grows under refinement

```
2D:  E(path) decreases monotonically to vacuum; peak density never exceeds
     ~1× its start (smooth_unwinding = true)
3D:  B(s): 1 → 0 jump at the singular configuration s ≈ 1/2 (B_jumps = true)
     peak energy density at the barrier: grows ×1.86 from n=61 → n=81
     (diverges under refinement — a genuine topological wall, not lattice noise)
```

## What the test does

In 2D, r̂_⊥=(r̂ₓ,r̂_y,0) is everywhere orthogonal to ẑ, so the interpolated
axis (1−s)r̂+sẑ never vanishes: the path U_s is smooth all the way, and the
second stage F→(1−t)F carries the configuration to the vacuum with bounded,
decreasing energy. **A 2D "hedgehog" is not protected** — π₂(S³)=0 realised as
an explicit, measured unwinding path.

In 3D, the south ray (r̂=−ẑ) forces the interpolated axis through zero at
s=1/2: the configuration is singular there, the discrete winding B jumps from
1 to 0 across it, and the peak energy density at the jump grows with grid
refinement (×1.86 for 61→81; bounded on any finite lattice, divergent in the
limit). **The B=1 sector is walled off** — π₃(S³)=ℤ realised as a measured
barrier, not cited as a theorem.

## Why this matters for the dimensional scan

Conserved particle number needs a protected integer charge. DS4 shows, with
one family and one engine, that the protection exists in d=3 and not in d=2.
Combined with DS3 (no stable size for d≠3) and Paper II's π₁/π₃ classification
(d≥4 has no integer charge for SU(2) textures), the topological leg of the
selection closes: **integer-charged point matter is a d=3 phenomenon.**

## Honest limitations

- One deformation family: the 3D result shows *this* path is blocked with a
  refinement-growing barrier (and any unwinding path must cross B∈ℤ
  discontinuously — the jump location moves, the jump does not).
- The 2D object here is the S²-valued texture inherited from the 3D hedgehog
  ansatz (the natural dimensional reduction), not the U(1) vortex of CR_3D
  (whose π₁ protection is a different, already-measured story).

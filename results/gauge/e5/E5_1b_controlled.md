# E5-1b — controlled-geometry FSS attempt: OBSTRUCTED by causal-set nonlocality

> Attempt to fix the E5-1 confound (uncontrolled diamond plaquette geometry across
> sizes) with a Lorentz-invariant proper-time cutoff tau_max
> (`e5_local.LocalCausalGraph`). Code: `E5_1b_controlled.py`. Run jun/2026, stopped
> early because the control check failed for a principled reason (below).

## The idea (and why it was reasonable)

E5-1's finite-size scaling was confounded because the diamond plaquette count grew
much faster than the event number (the Poisson causal set's mean degree grows with
box size). The proposed fix: keep only causal links with proper time
tau_ij <= tau_max. Proper time is a Lorentz scalar, so the cutoff is
Lorentz-invariant; the hope was that a fixed tau_max gives each bulk event a
fixed-volume causal neighbourhood, holding the local geometry constant while N grows.

## What happened (control check, before any physics)

```
rho=0.4, tau_max=3.0:
  L=5: N=250   links=4328    <deg>=34.6   plaq/link=0.67
  L=6: N=519   links=15721   <deg>=60.6   plaq/link=1.27
  L=7: N=961   links=44318   <deg>=92.2   plaq/link=0.45
  L=8: N=1640  links=108763  <deg>=132.6  plaq/link=0.18
  geometry CV: degree 0.46 -> STILL DRIFTING
```

The mean degree still GROWS with box size (34.6 -> 132.6), so the geometry is NOT
controlled. The fix failed.

Quantified: fitting log(degree) vs log(L) over L=5,6,7,8 gives
**degree ~ L^2.9** -- a fast power-law divergence, not a constant. This is the
obstruction turned into a measured statement (the "infinite-volume" argument below,
confirmed by data): a fixed proper-time cutoff does not bound the neighbourhood.

## Why it failed -- a principled obstruction, not a bug

The reasoning behind the fix was wrong. The region {future of an event, proper time
tau <= tau_max} in (3+1)D Minkowski has **infinite 4-volume**: the hyperboloid
tau^2 = t^2 - r^2 = tau_max^2 extends to arbitrarily large spatial separation r
(with matching large t) under Lorentz boosts. So bounding proper time does NOT bound
the neighbourhood volume; as the box grows, more of that infinite region is captured
and the degree grows without bound. This is precisely the well-known **tension
between Lorentz invariance, discreteness, and locality** in causal set theory (the
same nonlocality that forces the Benincasa-Dowker d'Alembertian to use nonlocal
alternating-shell weights): **a fixed-volume, Lorentz-invariant local neighbourhood
does not exist.** Any Lorentz-invariant cutoff fails to localise; any localising
cutoff (coordinate time, distance) breaks Lorentz invariance.

## Consequence for E5 (honest)

A clean finite-size scaling of the U(1) confinement/deconfinement transition on a
causal set, with controlled \emph{and} Lorentz-invariant local geometry, is
**fundamentally obstructed** by causal-set nonlocality. The naive Wilson action on
the bare causal diamonds inherits the unbounded-degree (mean-field/nonlocal)
character of the substrate -- the same character that, in the scalar sector (E2),
forced the relativistic dispersion to be carried by the Benincasa-Dowker operator
rather than the bare graph Laplacian.

This points to the real form the E5 photon test must take: not a naive Wilson theory
on bare diamonds, but a **Benincasa-Dowker-smeared gauge construction** (the gauge
analogue of how E2 recovered the relativistic scalar), OR an explicitly
Lorentz-breaking localisation accepted as a regulator. Both are substantial,
separate constructions.

## Status

- E5-1 (bare diamonds, E5-1 + this E5-1b): the confinement/deconfinement question is
  **not decidable** with the naive bare-diamond Wilson construction, because (i) the
  geometry cannot be controlled Lorentz-invariantly and (ii) the bare substrate is
  nonlocal/mean-field.
- The U(1) engine itself remains fully validated (G1+G2+G3) and U(1) gauge theory is
  gauge-invariant on the causal diamonds (E5-1 step 0) -- those positives stand.
- No photon claim, no confinement claim. The emergent-photon question in the link
  sector requires a BD-smeared gauge construction (future work), mirroring the
  scalar sector.

This is the honest frontier: the same nonlocality that the BD operator was invented
to tame in the scalar sector reappears as the obstruction in the gauge sector.

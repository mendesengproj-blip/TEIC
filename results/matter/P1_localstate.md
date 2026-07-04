# P1 — localized stable state? (refaz T20)

**Verdict: C** — no localized stable rest-state (death criterion met). A sourced lump
delocalizes over the light cone.

## Question
T20's "particles" were hand-drawn helices. The correct question: does the network
support a state that is localized, stable, and moves coherently? We do not draw one;
we source a localized lump and let the network's own dynamics propagate it.

## Method (ρ=22, T=10, X=16, σ₀=1.6, 20 seeds)
A localized lump `θ(x)=exp(−x²/2σ₀²)` is sourced in an early thin slab and propagated
by the causal-set retarded kernel `K=½C` (Johnston 2008 — the network's massless `□`
dynamics, not inserted). The spatial width σ(t) of |θ| is measured at later slabs and
fit to `σ(t)~t^p` (p≈0 stable, p≈½ diffusive, p≈1 ballistic light-cone).

## Results

| t | σ(t) |
|---|---|
| 2.5 | 2.00 ± 0.01 |
| 3.6 | 2.38 ± 0.01 |
| 4.7 | 2.88 ± 0.02 |
| 5.8 | 3.40 ± 0.02 |
| 6.8 | 3.97 ± 0.02 |
| 7.9 | 4.53 ± 0.02 |
| 9.0 | 5.11 ± 0.03 |

- Growth exponent **p = 0.76 ± 0.01** (between diffusive ½ and ballistic 1).
- Central/mean flatness: **5.32 → 1.92** (profile flattens toward a plateau).

## What it means
The lump **delocalizes**: σ grows as ~t^0.76 and the peak flattens into the light-cone
plateau characteristic of the 2D massless retarded Green's function (½ inside the
cone). The free network scalar has **no localized particle-like rest-state** —
consistent with M1 (no rest inertia) and with a massless field having no rest frame.

**Limitation (stated honestly):** a genuine *non-dispersing wavepacket* would require
Cauchy (initial-data) evolution with `θ̇`, which the retarded kernel alone does not
provide. What is established is that the free scalar sector, under its own retarded
dynamics, does not hold a lump together.

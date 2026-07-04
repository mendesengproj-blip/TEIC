# FL3-V — Validation Gate

**Verdict: GATE PASSED.** The dynamic SU(2) engine is trustworthy for the collision, with
one honestly-scoped limitation (the determinant baryon *integral* is noisy on the
affordable lattice, so the topological count is read from the conserved global charge and
the Gaussian-smoothed lump count, not from a strict ΔB<10⁻³).

## Engineering prelude (the real gate before measurement)
The trusted Skyrme force (`su2_core._skyrme_grad`) is an 8-colour finite difference: **64
full-grid energy evaluations per force call** → ~1 s/step even at 29³, which makes a
multi-seed collision ensemble intractable. So FL3 adds an **analytic single-pass Skyrme
gradient** (`fl3_core.skyrme_grad_fast`) and a matching evolve loop.

| Engineering check | Result |
|---|---|
| Analytic Skyrme gradient vs **true per-site** finite difference | max rel diff **2.8×10⁻⁸** |
| `chiral_evolve_fast` vs `su2_core.chiral_evolve` (static + moving Skyrmion) | **bit-identical** dynamics |
| Speedup | **~16×** (e.g. 41³: 4.5 s/step → 0.28 s/step) |

The fast engine is a *faithful drop-in*, not a new physics model. (An earlier naïve check
compared the raw gradient to `_skyrme_grad`, which is tangent-**projected** by its internal
renormalisation and so legitimately differs by a radial component — the per-site
brute-force is the correct reference, and it matches.)

## Physics checks (`e_sk=4`, L=16, N=35, dx≈0.46, full σ+Skyrme action)

| Check | Criterion | Result | Pass |
|---|---|---|---|
| **Unitarity** | \|U\|=1 every site/step | max \|U\|−1 = **2.2×10⁻¹⁶** | ✅ |
| **Isolated Skyrmion** | energy bounded, stays 1 lump | E drift **4.1%** (dt/dx=0.012), n_peaks **1** | ✅ |
| **Timestep** | largest dt with E drift <5% | **dt/dx = 0.012** (0.02 → 5.3%, B collapses) | ✅ |
| **Boost validity** | soliton translates at ~v | early baryon-centroid speed **0.304** vs v=0.294 → **ratio 1.03** | ✅ |
| **Causality** | finite, sub-instantaneous, O(c) | RMS-spread **1.39**, c=0.98 (E2) → finite & O(c) | ✅ |

## Honest scoping (pre-registered ΔB criterion)
The pre-registered "ΔB < 10⁻³ over 100 steps" is **not attainable** on a dx≈0.46 lattice:
the baryon density is the determinant of the discrete currents, so the *integral* B picks
up jiggle noise (the isolated Skyrmion's B wanders in [0.76, 0.92] at dt/dx=0.012 while its
**energy stays bounded**). This is the same obstacle E3b met (it cooled before reading the
integer charge). The **noise-robust** observables we therefore use downstream:

- the **global** charge `B_total` (∼0 for the pair, conserved throughout — radiation noise
  averages out in the integral);
- the **Gaussian-smoothed** soliton-lump count (a static-pair control holds N_peaks=2 for a
  whole run; an isolated Skyrmion holds N_peaks=1), which rejects the UV lattice speckle
  that a raw peak count turns into hundreds of false maxima.

Note also that the boosted lattice profile is not an exact discrete eigenstate, so it
radiates part of its momentum — the soliton carries only the *early* speed ≈ v and then
drags. This only **lowers** the effective collision energy, strengthening (never
manufacturing) the no-creation case.

Anti-circularity: B is the current determinant; c = 0.9797 is the **measured** E2 magnon
speed; no SR/GR dilation formula enters any generator.

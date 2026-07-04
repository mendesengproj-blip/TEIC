# E5-1 — first U(1) gauge scan on the causal set (EXPLORATORY, INCONCLUSIVE)

> Pre-registered in `E5_PHOTON_LINK_SECTOR.md` (E5-1). Code: `E5_1_confinement.py`
> using the validated fast engine (`e5_fast.py`) + causal-diamond plaquettes
> (`e5_core.causal_diamond_plaquettes`). Data: `E5_1_confinement.json`. Run jun/2026.
>
> NOTE: the JSON stored an automated verdict "DECONFINEMENT-LIKE" from a too-loose
> threshold; this synthesis is the corrected, authoritative reading (INCONCLUSIVE).
> The verdict logic in the script was corrected accordingly; the expensive MC
> (572 s) was not re-run, but the numbers below are deterministic from the stored
> data.

## Engine status going in (all validated)

G1 gauge invariance (exact), G2 4D U(1) beta_c~1.0, G3 finite-size scaling (fast
engine: 4D C/N_plaq grows with volume, slope +0.44; 3D flat, +0.01) -- the engine
reproduces known U(1) lattice-gauge physics. Fast engine validated against the slow
one (E5V_fss2, e5_fast).

## Result

Step 0 -- diamond gauge invariance: max|Δcos| = 1.8×10⁻¹⁵ (n=230, 2139 plaquettes):
the causal-diamond plaquette construction is **genuinely gauge-invariant** (closed
loops). This is a real, clean positive: U(1) gauge theory is well-defined on the
causal Hasse graph.

Step 1 -- average plaquette + specific heat vs beta, two causal-set sizes:

| L_box | events | plaquettes | C/N_plaq peak | peak β |
|---|---|---|---|---|
| 4.6 | 224 | 1 626  | 0.704 | 2.6 |
| 5.6 | 492 | 14 462 | 2.339 | 2.0 |

C/N_plaq peak grew ×3.32 between the two sizes.

## Why this is INCONCLUSIVE (the confound, stated plainly)

The automated "deconfinement-like" call was over-stated. Two problems:

1. **Uncontrolled plaquette geometry.** The diamond count grew ×8.9 (1626→14462)
   while the event number grew only ×2.2 (224→492). Since
   C/N_plaq = β²·N_plaq·Var(⟨cos⟩), it scales with N_plaq by construction, so a
   raw "peak grew ×3.32" conflates a possible transition with the exploding,
   uncontrolled plaquette geometry.
2. **The normalised exponent is intermediate.** A first-order transition would give
   C/N_plaq ∝ N_plaq (exponent ≈1); a crossover gives ≈0. Here
   ln(3.32)/ln(8.9) ≈ **0.55** — squarely between, and from only **two** sizes with
   changing geometry. It neither establishes nor excludes a deconfined phase.

## Verdict

```
INCONCLUSIVE (exploratory). The causal-set U(1) gauge theory is well-defined and
gauge-invariant (clean positive), but whether it has a deconfinement transition
(Coulomb phase -> possible photon) or only a crossover (confines -> no photon) is
NOT decided by this 2-size scan with uncontrolled diamond geometry. No photon claim;
no confinement claim. E5-2 (the actual photon dispersion/polarisation test) stays
gated until E5-1 is solid.
```

## What a solid E5-1 needs

1. **Controlled plaquette geometry across sizes** -- fix the diamond density /
   mean plaquettes-per-link so the FSS compares like with like (the dominant fix).
2. **>= 3-4 sizes** with several seeds, to fit the C/N_plaq ∝ N_plaq^p exponent.
3. **A Wilson-loop area-law estimator** on the causal graph (or a monopole-density
   diagnostic) -- the direct confinement observable, still to be built and validated.

## Honest bottom line for E5

Established this session: the U(1) gauge engine is fully validated (G1+G2+G3, fast
engine), and U(1) gauge theory is well-defined and gauge-invariant on the causal
Hasse graph (diamond plaquettes). NOT established: whether that theory deconfines
(hosts a photon) or confines. The emergent-photon question in the link sector
remains open -- now on a validated footing, with the specific next steps above.

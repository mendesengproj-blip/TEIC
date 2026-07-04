# INV2 — reproduction of the critical experiments

> Reproduce before judging. `python results/audit/t14_t21/INV2_reproduce.py` (~6 s).
> The GE measurement functions are re-implemented **verbatim** and re-run with **20
> independent seeds** (originals: single seed 42, or unseeded; no error bars). $\gamma$
> is computed only in a `COMPARISON ONLY` block, never fed into a measurement.

The four reproductions map to the central claim "matter = causal connectivity".

---

## R-REL — T18/T19 "Special relativity emerges" → **does not hold up**

The measured quantity is the number of causal links between a Gaussian blob at $t=0$ and
the **same blob hand-translated** by $(\Delta t, v\,\Delta t)$. $v$ is imposed by hand.

| comparison | RMSE (20 seeds) |
|---|---|
| rate$(v)$/rate$(0)$ vs $1/\gamma=\sqrt{1-v^2}$ | **0.202** |
| $E=1/\text{rate}$ vs $\gamma$ (T19) | **1.352** |
| rate$(v)$ vs **pure Gaussian overlap** $e^{-a v^2}$, $a=0.52$ | **0.003** |

- The measured curve is a **Gaussian-blob overlap**, which fits $e^{-av^2}$ ~70× better
  than it fits $1/\gamma$. There is no Lorentz factor here.
- The (poor) match to $1/\gamma$ **depends on the arbitrary blob width** $\sigma$:
  RMSE vs $1/\gamma$ = 0.167, 0.198, 0.333 for $\sigma=0.05,0.1,0.2$. A derivation
  cannot depend on a free knob.
- T18A even plots this **decreasing** overlap against the **increasing** $\gamma$ and
  labels it "emergence of the Lorentz factor" — internally inconsistent with T18BC/T19,
  which use the inverse.

**Verdict:** not circular (γ not injected), but **not a derivation** — a one-parameter
coincidence over a limited $v$-range. Contrast TEIC R1 (Poisson sprinkling, invariant
proper time, isotropy/CV test, no imposed $v$): a genuine emergence test this is not.

---

## R-MASS — T15/T16 "mass = ⟨k⟩" → **real correlation, near-tautological, not universal**

Cost/⟨k⟩ over 20 seeds (GE claimed a stable 0.24–0.29 from single shots):

| dim, n | ⟨k⟩ | cost/⟨k⟩ |
|---|---|---|
| 2, 100 | 24.6±1.8 | 0.311±0.031 |
| 2, 300 | 75.2±2.8 | 0.284±0.014 |
| 3, 100 | 11.3±1.1 | 0.305±0.040 |
| 3, 300 | 34.1±2.1 | 0.245±0.017 |
| 4, 100 | 4.6±0.9 | **0.418**±0.076 |
| 4, 300 | 14.3±0.9 | 0.260±0.016 |

- Full range **0.245–0.418**, not 0.24–0.29: GE under-reported the spread (single shots).
- "Transport cost" (links per event in a Δt-window) and ⟨k⟩ (links per event) **both
  count causal links per event**. Their ratio being $O(1)$ is **near-tautological**, not
  a discovered law of mass. No tie to inertial mass (F=ma) or Lorentz invariance.

**Verdict:** a genuine (if almost definitional) correlation; the "universal mass law"
is overstated.

---

## R-GRAV — T17B "Schwarzschild 1/r from connectivity" → **circular (coded Poisson)**

The GE solver **hard-codes** $\frac1{r^2}\frac{d}{dr}(r^2\frac{d\theta}{dr})=\alpha k(r)$.
Feeding **any** centrally-peaked source — connectivity-like or arbitrary — the exterior
$|\text{corr}|$ with $1/r$ is essentially 1:

| source | corr with 1/r |
|---|---|
| connectivity-like peak | −1.000 |
| arbitrary Gaussian | −0.998 |
| arbitrary top-hat | −1.000 |
| arbitrary triangle | −1.000 |

(The sign is the potential-well convention; $|\text{corr}|\approx1$ regardless.)

**Verdict:** the $1/r$ is the **3D Poisson Green's function** that was coded in, not a
property of connectivity. This **rediscovers TEIC's own D1–D3** ($\nabla^2\theta=J\to1/r$)
— which TEIC did far more rigorously (corr **0.9991**, unconstrained MC, *no* hard-coded
Poisson; see `BRIDGE_DYNAMICS.md`, `BRIDGE_D3_AUDIT.md`).

---

## R-PART — T20/T21BIS "spin / Pauli exclusion" → **hand-built structures, interpretation**

`k_total` of two helices vs separation: 7.7, 8.0, 13.0, 15.3, 15.5, 15.4 — saturates
near 15 (GE's "Pauli ≈15" reproduced). But the "fermion" is a **deterministic hand-drawn
helix** (the `winding` argument is unused), "exclusion" is the link-count of two fixed
curves overlapping, and "spin-1/2" (T20) is rotating a blob with an `arctan2` $z$-offset
and printing path counts with **no $2\pi$-vs-$4\pi$ periodicity test**. No
spin-statistics, no antisymmetry, no Dirac, no error bars.

**Verdict:** measured numbers are real but describe **imposed** structures; the
particle-physics labels are interpretation, not derivation.

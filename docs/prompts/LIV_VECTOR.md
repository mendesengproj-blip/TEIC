# LIV_VECTOR — the vector-sector Lorentz violation, located and disarmed

> **Independent investigation.** Does **not** modify R1–R3 or e6–e11, and is not part
> of the TEIC paper. Continues [`BRIDGE_WILSON.md`](BRIDGE_WILSON.md) (W2: E/B ≈ 3 in
> the emergent $F^2$) and [`BRIDGE_BD.md`](BRIDGE_BD.md) (BD smearing: right mechanism,
> SNR ≈ 1 wall). This is the **survival obligation** of `ROADMAP_REVOLUCAO.md`,
> attacked by the global-observable route. Artefacts in
> [`results/bridge/liv_vector/`](results/bridge/liv_vector/).

**Anti-circularity (obeyed).** No Lorentz/dispersion formula enters any generator.
Loops are built from causal relations only (`wilson_core.causal_diamond_loops`,
unchanged from W2). Boosts appear only as analysis transformations of *measured*
bivectors (LV2) and as the parametrization of probe-field families at fixed invariants
(LV4); the plaquette selection never sees the probe field. Kill criteria pre-registered
in each generator header. Main-pipeline guard untouched.

---

## The threat this answers

W2 found the emergent $F^2$ Lorentz-violating at order 1 (E/B = 2.97; AB2: 3.25 ± 0.10);
observational LIV limits are brutal, so an intrinsic preferred frame kills the EFT
sector — exactly what differentiates TEIC from CST. BD smearing removed the anisotropy
mechanism but could not demonstrate restoration (ρ^{3/4} variance, SNR ≈ 1).

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **LV1** — per-plaquette invariant | is E/B a frame effect pointwise? | **NO — exact theorem.** Every causal plaquette is $\Omega=\frac12(l-p)\wedge(k-j)$: a simple bivector on a **timelike plane**, so $e^2-b^2 = (\text{proper area})^2 > 0$ **in every frame** (12 941/12 941, $I<0$ without exception; simplicity at $10^{-16}$). Electric dominance is **causality**, not a preferred frame. |
| **LV2** — boost covariance | does the ensemble have a preferred frame? | **NO.** Bin-by-bin, the population at rapidity η equals the boost of the rest population (median size-controlled z = 0.36; one 3σ bin at the truncation edge, flagged). E/B(η) falls 19 → 1.6; the global "3" is the rapidity-weighted average of **one LI orbit truncated by the box**. |
| **LV3** — cutoff scan | is "3" a regulator number? | **YES.** E/B strictly monotone in the reach $L\rho^{1/4}$ (3.34 → 2.69; L and ρ interleave on one axis); cumulative curves collapse across boxes (≤8%); the Euclidean weight grows ~cosh 2η with truncation depth while $e^2-b^2$ is invariant content. |
| **LV4** — summed action | is the **global** observable LI? | **The LV resums away.** $S=\sum_p[1-\cos W_p]$, $W_p$ scalar; paired seeds kill the SNR wall (invariant sensitivity up to 54σ). Weak field: R(β) reproduces the quadratic LV prediction (up to 8.5×) — W2 recovered as expansion limit. Strong field: **boost defect 0.98 → 0.003**. Strict 5%-while-sensitive window not met ⇒ **PARTIAL** by pre-registration. |
| **LV4b** — extent scan | is the residual the box reach? | **KILL (honest).** Defect at fixed (E₀/u₀, β) is L-independent over L = 3–6 while η_q95 grows. The residual is the **still-quadratic fraction** of the scale-mixed population — controlled by field strength (resummation), not volume. |

## The honest bottom line

**No intrinsic Lorentz violation was found anywhere in the vector sector. The order-1
"violation" lives entirely in the observable, in two identified layers — but the
sharpest pre-registered closure criterion was not met, and that is reported as such.**

- **The per-plaquette layer is a theorem, not a violation (LV1).** Causal loops span
  timelike planes; $e^2>b^2$ is Lorentz-*invariant* electric dominance. Asking E/B = 1
  of positive plane weights was never the LI expectation — this is BD1's
  positive-definiteness diagnosis seen from the invariant side, now exact.

- **The ensemble is covariant (LV2) and the coefficient anisotropy is the regulator
  (LV3).** The network supplies one boost orbit; the box decides how much of it is
  summed. "3" is the truncation depth of this class of boxes, moving monotonically
  with the reach and with nothing else.

- **The right observable restores invariance nonperturbatively (LV4).** The bounded
  cosine resums the expansion plaquette by plaquette ($W$ is a scalar), collapsing the
  boost defect by three orders of magnitude — with the W2 anisotropy recovered exactly
  as its weak-field limit, so nothing was hidden. The paired-seed design delivers the
  SNR the BD route lacked (40–54σ field sensitivity vs SNR ≈ 1).

- **What remains open, precisely (LV4 PARTIAL + LV4b kill).** At the most
  field-sensitive point the defect floors at ~12%, set by the unsaturated fraction of
  the granularity-fixed size distribution — independent of box size. A single regime
  that is simultaneously LI at <5% *and* field-sensitive at >5σ was not exhibited at
  accessible sizes. Routes that act on the floor: higher density (moves the
  granularity), or the BD sign-alternating kernel as the linear-theory subtraction of
  the same quadratic remnant.

## Where this leaves the chain

```
TEIC causal network
  → every causal plaquette: timelike plane, e² > b²    invariant theorem      ✓ (LV1)
  → plaquette ensemble: boost-covariant                no preferred frame     ✓ (LV2)
  → quadratic F² coefficient: E/B ≈ 3                  = box-truncated orbit  ✓ (LV3)
  → summed action S[F]: depends on invariants only     defect 0.98 → 0.003    ✓ (LV4)
  → residual 12% at peak sensitivity                   = unsaturated fraction ✗→ density / BD kernel
```

The survival threat changes status: from *"order-1 LV unresolved (SNR ≈ 1) — the EFT
sector dies without restoration"* to *"no preferred frame in the network; the LV is an
artifact of the quadratic expansion under a frame-fixed regulator; the global action is
invariant where saturated, with a quantified, understood, density-controlled remnant."*
The forward prediction of `PREDICTIONS.md` (photon dispersion exactly null on average)
stands on LV2's covariance, now measured rather than conjectured.

---

## Artefacts

| file | content |
|---|---|
| [`results/bridge/liv_vector/LV1_invariant.md`](results/bridge/liv_vector/LV1_invariant.md) | timelike-plane theorem; simplicity; invariant dominance |
| [`results/bridge/liv_vector/LV2_covariance.md`](results/bridge/liv_vector/LV2_covariance.md) | rapidity-binned E/B vs boosted rest population |
| [`results/bridge/liv_vector/LV3_cutoff.md`](results/bridge/liv_vector/LV3_cutoff.md) | reach scan; curve collapse; Euclidean weight = truncation depth |
| [`results/bridge/liv_vector/LV4_global_action.md`](results/bridge/liv_vector/LV4_global_action.md) | summed-action boost test; resummation collapse |
| [`results/bridge/liv_vector/LV4b_extent.md`](results/bridge/liv_vector/LV4b_extent.md) | residual ≠ box reach (pre-registered kill) |

Shared primitives in `liv_core.py`; figure `LIV_restoration.png`. Reproduce:

```
python results/bridge/liv_vector/LV1_invariant.py
python results/bridge/liv_vector/LV2_covariance.py
python results/bridge/liv_vector/LV3_cutoff.py
python results/bridge/liv_vector/LV4_global_action.py
python results/bridge/liv_vector/LV4b_extent.py
python results/bridge/liv_vector/make_figures.py
```

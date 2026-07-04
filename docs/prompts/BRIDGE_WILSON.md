# BRIDGE_WILSON — Wilson loops and the hidden quartic

> **Independent investigation.** Does **not** modify R1–R3 or e6–e11, and is not part
> of the TEIC paper. Continues [`BRIDGE_COEFFICIENTS.md`](BRIDGE_COEFFICIENTS.md)
> (C1–C4), whose C4 found the link-only action **misses** the Maxwell term $F^2$. All
> artefacts live in [`results/bridge/wilson/`](results/bridge/wilson/).

**Anti-circularity (obeyed).** $F^2$ and the quartic **emerge from coarse-graining** —
they are never inserted. The only object built is the loop holonomy
$W=\oint A_\mu dx^\mu$ (a sum of link phases); that $W\to\iint F$ by Stokes is
*verified* (W1), then coarse-grained (W2). No SR/GR dilation factor, no $GM/r$, no DEV
in any generator. The DEV enters only in W4. Main-pipeline guard untouched.

---

## The gap this closes

C4 showed: a single link carries only the local phase $\phi=A_\mu e^\mu$, which gives
$A^2$ — but $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$ needs the phase summed
**around a plaquette**. Without plaquettes, $F^2$ is absent and the vector $A$ is
auxiliary. This investigation adds the plaquette term
$$S=\sum_{\rm links}\Delta\tau[1-\cos(\phi+\Delta\theta)]+\lambda_p\sum_{\rm plaq}[1-\cos W_p]$$
and asks whether $F^2$ emerges and coexists with the quartic.

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **W1** — holonomy → F | does $W/\text{area}\to F_{\mu\nu}$? | **PASSA** — exact for constant $F$ ($10^{-12}$, any scale), $O(\text{area})$ otherwise; loop $W$ **gauge-invariant** while link phases are **not**; works on real causal diamonds (corr 1.0000). |
| **W2** — coarse-graining | measure $C_F$, $C_q$; coexist/conflict/suppress? | **(a) COEXIST.** $F^2$ **emerges** (Maxwell form, θ-term $=0\pm$ by parity); quartic **survives** ($C_q\ne0$, sign $<0$ = DBI). Disjoint sums of distinct operators. **But** emergent $F^2$ is **Lorentz-violating**: $E/B=2.97\pm0.03$ (= C1's anisotropy resurfacing). $C_F=\lambda_p\Pi/4$ free. |
| **W3** — strong field | regime map | bounded $\cos$ ⇒ **no explosion**; both channels **saturate**; distinct operators ⇒ **no cancellation**. Weak: $X+F^2$. Strong: DBI (links) + plaquette saturation ($F^2$). Hierarchy set by $\lambda_p$. |
| **W4** — vs DEV | operators, ratios, predictions | **FORM-COMPLETE, calibration- & Lorentz-open.** Every DEV operator now emerges (C4 gap closed) + locked ratios $(1,2)$ + extra quartics. $\lambda_p$ free (= DEV's free $K$); order-1 LV unresolved; $a_0$ scale UV not $cH$. |

---

## The honest bottom line

**Wilson loops are the right mechanism, and they close the structural gap — but they
also re-import the same Lorentz-violation problem the link sector had.**

- **W1 settles the mechanism.** The holonomy reproduces $F_{\mu\nu}$ exactly; the
  gauge-invariance of the loop (vs the gauge-dependence of a single link) is precisely
  why plaquettes carry $F$ and links carry $A^2$. The "missing $F^2$" was a real but
  **fixable** omission: it lives on loops, not links.

- **W2 settles coexistence.** $F^2$ (plaquettes) and the quartic $(A\!\cdot\!\partial\theta)^2$
  (link 4th order) are **disjoint sums of distinct operators** — they add without
  cancelling (case **a**). The emergent $F^2$ has the correct Maxwell tensor structure
  with **no spurious θ-term** (parity-protected). The honest expectation —
  *"the quartic does not disappear; $F^2$ dominates where it matters"* — is **confirmed**:
  the quartic survives as a strong-field residual, and $F^2$ dominates wherever
  $\lambda_p$ is large.

- **The new problem (honest).** The raw-plaquette $F^2$ is **Lorentz-violating**:
  electric-plane and magnetic-plane area² differ by $\approx3\times$ ($E/B=2.97$),
  exactly mirroring the link anisotropy $a_t/a_x=3.38$ of C1. The single Maxwell
  coefficient splits into unequal $C_E E^2$ and $C_B B^2$. This is the causal-set
  **link/plaquette non-locality**, not a new pathology — and its cure is the **same**
  one D1 used: the non-local Benincasa–Dowker kernel, not raw nearest neighbours.

- **W4 places the result.** With plaquettes the bridge is **form-complete**: every DEV
  operator ($X$, $F^2$, $A^2$, $A\!\cdot\!\partial\theta$, DBI) now emerges from causal
  links + loops, with the Stückelberg ratios $(1,2)$ locked and genuine extra quartics.
  What stays open is **calibration** (the gauge weight $\lambda_p$ is free, exactly as
  the DEV's $K$ is free) and **Lorentz restoration** (order-1 LV at the raw level).

## Where this leaves the chain

```
TEIC causal network
  → S = Σ Δτ[1−cos(φ+Δθ)]                     links: X, √(1−X/X₀), A∂θ, (A∂θ)²   ✓
  → + λ_p Σ[1−cos W_p]   (this work)          plaquettes: F_μν F^μν              ✓ (form)
  → coarse-graining                            ALL DEV operators present          ✓
  → DEV                                         + extra quartics; weight λ_p free;
                                                + order-1 LV (raw) → BD kernel    ← next layer
```

**The bridge form is now complete.** The remaining, clearly-identified next layer is
**not** a missing operator but a missing *mechanism*: the non-local (Benincasa–Dowker)
construction that restores Lorentz invariance and would fix both the link anisotropy
(C1) and the $E/B$ split (W2), turning the raw preferred-frame action into a covariant
one. The gauge kinetic weight $\lambda_p$ and the acceleration scale $a_0$ remain
external, as in the DEV.

---

## Artefacts

| file | content |
|---|---|
| [`results/bridge/wilson/W1_holonomy.md`](results/bridge/wilson/W1_holonomy.md) | holonomy → F (Stokes), gauge invariance |
| [`results/bridge/wilson/W2_coarse_graining.md`](results/bridge/wilson/W2_coarse_graining.md) | $C_F$, $C_q$, coexistence, $E/B$ LV |
| [`results/bridge/wilson/W3_strong_field.md`](results/bridge/wilson/W3_strong_field.md) | saturation regime map |
| [`results/bridge/wilson/W4_dev_comparison.md`](results/bridge/wilson/W4_dev_comparison.md) | term-by-term vs DEV, new predictions, status |

Each `.md` has a matching `.py` generator and `_data.json`; shared primitives in
`wilson_core.py`; figures `W1_holonomy.png`, `W3_strong_field.png`. Reproduce:

```
python results/bridge/wilson/W1_holonomy.py
python results/bridge/wilson/W2_coarse_graining.py
python results/bridge/wilson/W3_strong_field.py
python results/bridge/wilson/W4_dev_comparison.py
python results/bridge/wilson/make_figures.py
```

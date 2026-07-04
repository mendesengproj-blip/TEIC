# C2 — The decisive test: are C₃/C₁ and C₂/C₁ clean numbers?

**Task.** Extract $C_1,C_2,C_3$ from the C1 moments **without any fit**, compute the
ratios $C_3/C_1$ and $C_2/C_1$, and decide whether they are clean numbers fixed by
geometry (**real structure**) or free numbers needing adjustment (**reverse
engineering**). Generator: `C2_ratios.py` (consumes `C1_moments_data.json`; the DEV
appears only in a marked COMPARISON block).

## The coefficients

The quadratic sector coarse-grains to

$$S_2=\tfrac12\,n_{\text{links}}\!\int (A_\mu+\partial_\mu\theta)(A_\nu+\partial_\nu\theta)\,M2^{\mu\nu},
\qquad M2^{\mu\nu}=\kappa\,g^{\mu\nu}+\lambda\,u^\mu u^\nu .$$

Because $\phi$ and $\Delta\theta$ live inside **one** cosine, the bilinear is a
**perfect square** in the single covector $w_\mu=A_\mu+\partial_\mu\theta$. The
Lorentz-invariant ($\kappa$) part expands as

$$\frac{\kappa\,n}{2}\,(A+\partial\theta)^2=\frac{\kappa n}{2}\big[A^2+2\,A\!\cdot\!\partial\theta+(\partial\theta)^2\big]
\;\Rightarrow\;
\boxed{C_1=C_2=\frac{\kappa n}{2},\quad C_3=\kappa n}.$$

## Result — the ratios

| | from symbolic square | 1+1D (measured) | 3+1D (measured) | DEV |
|---|---|---|---|---|
| $\kappa$ | — | −0.2334 | −0.9938 | — |
| $C_1=C_2$ | $\kappa n/2$ | −54.14 | −872.69 | $F_1$ / $-m_A^2/2$ |
| $C_3$ | $\kappa n$ | −108.27 | −1745.37 | $\gamma$ |
| **$C_2/C_1$** | **1** | **1.000000** | **1.000000** | $(-m_A^2/2)/F_1$ = **free** |
| **$C_3/C_1$** | **2** | **2.000000** | **2.000000** | $\gamma/F_1$ = **free** |

The ratios are **exactly 1 and 2**, **identical in 1+1D and 3+1D** even though
$\kappa$ differs by ~4×. They are clean — and the geometry-invariance is the proof
of *why* they are clean.

## The honest reading — clean, but not for the reason hoped

This is the crux of the whole investigation, reported straight:

> **The ratios 1 and 2 are NOT a discovery of the causal geometry. They are an
> algebraic identity of the single-cosine (Stückelberg) form.** Any symmetric link
> measure $M2^{\mu\nu}$ whatsoever — Euclidean, Lorentzian, anisotropic — gives
> $C_2/C_1=1$ and $C_3/C_1=2$, because all three coefficients come from contracting
> the *same* tensor with the *same* perfect square $(A+\partial\theta)^2$. The
> Poisson averages cancel out of the ratio entirely.

So, mapped onto the prompt's three cases:

- It is **not** "razões que dependem de ajuste" — the numbers are not tunable.
- It is **not** a geometric derivation either — the geometry never had a chance to
  *fix* the ratio; the ratio was set the moment $\theta$ was put inside the gauge
  field's cosine as a Stückelberg phase.
- What the geometry **does** genuinely output is the **scale** $\kappa$ (and
  $n_{\text{links}}$), plus the order-1 **Lorentz-violating** coefficient $\lambda$
  measured in C1. Those are the real, falsifiable geometric predictions — and the
  $\lambda$ one is uncomfortably large.

The cleanness of 1 and 2 is therefore **structural by construction**, a
self-consistency of the ansatz, not independent evidence that the minimal action is
the true microscopic law.

## Comparison with the DEV — clean ratios ≠ DEV

Current DEV scalar/vector Lagrangian (`docs/DEV_bridge_future.md`, eq. 1):

$$\mathcal L_{\rm DEV}=F(X,\theta)-\tfrac K4 F_{\mu\nu}F^{\mu\nu}-\tfrac{m_A^2}{2}A_\mu A^\mu+\gamma\,A_\mu\nabla^\mu\theta .$$

Here $F_1$ (kinetic), $m_A^2$ (mass) and $\gamma$ (coupling) are **independent free
parameters** fit to galaxy/cosmology data. Their ratios are *not* 1 and 2.

The minimal action's $(1,2)$ is exactly the **gauge-invariant Proca/Stückelberg
point** of that parameter space — the special case where gauge invariance ties the
vector mass and the scalar–vector coupling to the scalar kinetic term. The generic
DEV does **not** sit at that point.

## Verdict (C2)

> **CLEAN RATIOS (1, 2), but ≠ the generic DEV.** The minimal action reproduces the
> *gauge-invariant Stückelberg/Proca special case* of the DEV's scalar–vector
> sector — a **sister theory**, not the full DEV. The cleanness is structural by
> construction (one cosine), **not** a derivation of the DEV from causal geometry.
> The genuine geometric output is the scale $\kappa$ and an **order-1 Lorentz
> violation** $\lambda$ (the open tension flagged in C1).

This is the prompt's case *"razões limpas ≠ DEV: a ação mínima tem estrutura
própria, mas não é exatamente a DEV; pode ser uma teoria irmã,"* qualified by the
honest note that the limpidez itself is algebraic, not geometric.

## Output

- `C2_ratios.py`, `C2_ratios_data.json`.

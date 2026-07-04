# C4 — The anti-reverse-engineering test (fourth order)

**Task.** Expand the one-line action to **fourth** order, list *every* operator it
predicts, and compare term by term with the DEV: does the minimal action predict
exactly the DEV, **extra** terms, or **miss** terms? Generator:
`C4_completeness.py` (sympy; DEV only in the marked COMPARISON block).

## The expansion

$$1-\cos u=\tfrac12u^2-\tfrac1{24}u^4+\dots,\qquad u=(A_\mu+\partial_\mu\theta)\,e^\mu .$$

Coefficients $\{\tfrac12,-\tfrac1{24}\}$ are pure Taylor numbers (no fit). Every
power of $u$ is a power of the **single** gauge-invariant covector
$w_\mu=A_\mu+\partial_\mu\theta$.

- **Order $u^2$** (×½): $u^2=w_0^2e_t^2+2w_0w_1e_te_x+w_1^2e_x^2$ → after
  $\langle\Delta\tau\,e e\rangle$, the C1/C2 quadratic sector. LI operator ratios
  $(\partial\theta)^2:A\!\cdot\!\partial\theta:A^2=\mathbf{1:2:1}$ (the square).
- **Order $u^4$** (×$-\tfrac1{24}$): $u^4=(w\!\cdot\!e)^4$ → the **full perfect
  fourth power** $(A+\partial\theta)^4$, contracted with the 4th moment
  $\langle\Delta\tau\,eeee\rangle$. The $w$-monomials (1+1D bookkeeping; structure
  is dimension-independent) are

  | $w_0$ power | $w_1$ power | $e$-factor |
  |---|---|---|
  | 4 | 0 | $e_t^4$ |
  | 3 | 1 | $4e_t^3e_x$ |
  | 2 | 2 | $6e_t^2e_x^2$ |
  | 1 | 3 | $4e_te_x^3$ |
  | 0 | 4 | $e_x^4$ |

  i.e. the operators $(\partial\theta)^4,\ A\!\cdot\!\partial\theta\,(\partial\theta)^2,\
  A^2(\partial\theta)^2,\ (A\!\cdot\!\partial\theta)^2,\ A^3\!\cdot\!\partial\theta,\ A^4$.

## Term-by-term comparison with the DEV

DEV: $\mathcal L=F(X,\theta)-\tfrac K4F^2-\tfrac{m_A^2}{2}A^2+\gamma A\!\cdot\!\partial\theta$,
with $F(X)=F_0+F_1X+F_2X^2+\dots$ ($X=(\partial\theta)^2$). **All three cases occur
simultaneously, for different operators:**

| operator | minimal action | DEV | verdict |
|---|---|---|---|
| $(\partial\theta)^2,\,A^2,\,A\!\cdot\!\partial\theta$ | from $u^2$, ratio 1:2:1 | $F_1,\,m_A^2,\,\gamma$ (free) | structure ✓, calibration free (C2) |
| $(\partial\theta)^4$ | from $u^4$ | $F_2X^2$ / DBI | **MATCH** (DEV coeff free) |
| $A^4,A^3\partial\theta,A^2(\partial\theta)^2,(A\!\cdot\!\partial\theta)^2$ | from $u^4$ | absent (DEV vector sector ≤ quadratic in $A$) | **EXTRA** (new prediction) |
| $(A_0+\partial_0\theta)^{2n}$ | from $\lambda$ part of every even moment | absent (DEV is covariant) | **EXTRA** (Lorentz-violating) |
| $F_{\mu\nu}F^{\mu\nu}$ | **not produced by links** | $-\tfrac K4F^2$ | **MISSING** |

## The three findings, stated honestly

1. **MATCH.** The quartic kinetic term $(\partial\theta)^4$ predicted by the $u^4$
   piece is exactly the $X^2$ term of the DEV's $F(X)$ / DBI expansion. Structural
   agreement (the DEV coefficient is free, so this is consistency, not a number
   match).

2. **EXTRA — genuine new predictions.** The minimal action predicts the *full*
   gauge-invariant quartic self-interaction $(A+\partial\theta)^4$:
   $A^4,\ A^3\partial\theta,\ A^2(\partial\theta)^2,\ (A\!\cdot\!\partial\theta)^2$.
   These are **absent** from the DEV, whose vector sector is at most quadratic in
   $A$. They are testable predictions of TEIC beyond the DEV:
   - regime: **strong-field / large-$w$** — where $A_\mu+\partial_\mu\theta$ is not
     small, i.e. near sources and at network-density gradients. The leading new
     effect is a quartic Stückelberg self-coupling $\sim(A+\partial\theta)^4$ with
     coefficient fixed (relative to the quadratic) at $-\tfrac1{12}$ of
     $\langle\Delta\tau\,eeee\rangle/\langle\Delta\tau\,ee\rangle$ — a *prediction*,
     not a free parameter, once the quadratic scale is set.
   - Plus a tower of **Lorentz-violating** operators $(A_0+\partial_0\theta)^{2n}$
     whose size is set by the order-1 anisotropy $\lambda$ measured in C1.

3. **MISSING — the Maxwell term.** The link sum $\sum_{\text{links}}\cos(\cdot)$
   produces **no plaquette / no curl**, so $F_{\mu\nu}F^{\mu\nu}$ is **not generated
   at all**. Without it the vector $A$ is **auxiliary**: its equation of motion sets
   $A_\mu=-\partial_\mu\theta$ (pure gauge), collapsing the whole vector sector.
   The Maxwell kinetic term must come from a **separate plaquette term**
   $\sum_{\text{loops}}\cos(\text{flux})$ (Wilson loops; Sverdlov–Bombelli 2009),
   not from links. So the "five-term $S_{\text{eff}}$" of the prompt is really
   **four link terms + one plaquette term**: the $C_2'F^2$ coefficient lives on
   loops, outside the one-line link action.

## Verdict (C4)

> The minimal action is **neither exactly the DEV nor pure reverse engineering.** It
> **matches** the DEV's scalar self-interaction, **predicts extra** gauge-invariant
> quartic (and Lorentz-violating) operators the DEV lacks, and **misses** the Maxwell
> $F^2$ term (which requires plaquettes). The extra quartics are concrete new
> predictions; the missing $F^2$ is a structural limit of a link-only action.

## Output

- `C4_completeness.py`, `C4_completeness_data.json`.

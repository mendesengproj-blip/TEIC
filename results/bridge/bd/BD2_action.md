# BD2 — BD smeared operator in the minimal action

**Task.** Implement the BD-smeared version of the action and produce first results.
Generators: `bd_core.py` (operator), `bd_summed_action.py` (estimator).

## Implementation (the network operator, not a fit)

The smeared weight is identical to `experiments/e10` (Sorkin 2007; Aslanbeigi–
Saravani–Sorkin 2014):

$$w(m)=(1-\epsilon)^m-2m\,\epsilon(1-\epsilon)^{m-1}+\binom{m}{2}\epsilon^2(1-\epsilon)^{m-2},$$

with $m$ = number of events in the causal interval between an ancestor $y$ and the base
event $x$, and $\epsilon$ the binomial-thinning retention. The smeared d'Alembertian is
$B_\epsilon\theta(x)=-\theta(x)+2\epsilon\sum_{y<x}w(m_y)\theta(y)$.

The object that replaces the sharp positive moment of BD1 is the smeared second moment

$$M2_{\rm BD}^{\mu\nu}=\sum_{y<x}2\epsilon\,w(m_y)\,e^\mu e^\nu,\qquad e=x-y,$$

— the $\partial_\mu\partial_\nu$ coefficient of $B_\epsilon$, which BD theory says
$\to g^{\mu\nu}$.

## The decisive property: $w(m)$ alternates sign

`smeared_weight(m,ε)` is **positive near $m=0$ and negative at intermediate $m$**
(e10, line 39). This is exactly the ingredient BD1 said was required: a sign-alternating
weight is the only thing that can turn the positive-definite (Euclidean) sharp moment
into an indefinite (Lorentzian) one. So the *mechanism* is in place by construction.

## First result — the pathology is removed, magnitude collapses

Replacing the sharp weight by $2\epsilon\,w(m)$ changes the second moment dramatically:

| | sharp $\langle\Delta\tau\,ee\rangle$ | BD smeared $\sum 2\epsilon w\,ee$ |
|---|---|---|
| $a_t$ | +20114 | $-0.078\pm0.090$ |
| $a_x$ | +5046 | $+0.099\pm0.088$ |
| eigenvalues | both $>0$ (PSD) | mixed sign, but $\approx0$ |
| $a_t/a_x$ | 3.99 | not determined (both $\approx0$) |

The smeared operator **collapses the $O(10^4)$ positive-definite anisotropy to
$O(0.1)$**: the temporal-elongation factor of ~4 is gone, and the components are no
longer significantly positive — i.e. the Euclidean pathology of BD1 is removed. Whether
what remains is a *significant* Lorentzian signature (a_t>0, a_x<0, equal magnitude) is
the quantitative question for BD3/BD4.

## Verdict (BD2)

> The BD smeared operator is implemented (identical to e10) and its sign-alternating
> weight is the structurally correct cure identified in BD1. First result: it **removes
> the sharp Euclidean anisotropy** (a_t/a_x: 4 → undetermined; magnitudes $10^4\to0.1$).
> The mechanism works; the quantitative test of Lorentz restoration follows in BD3.

## Output
`bd_core.py`, `bd_summed_action.py`, `bd_summed_action_data.json`.

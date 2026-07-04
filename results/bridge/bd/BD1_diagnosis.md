# BD1 — Diagnosis: the source of the order-1 Lorentz violation

**Task.** Decompose the W2 anisotropy (E/B≈3) and C1 anisotropy (a_t/a_x≈3.4), find
which component carries the factor, and trace it back to the action. Generator:
`BD1_diagnosis.py`.

## The exact structural fact

The sharp action $S=\sum_{\rm links}\Delta\tau[1-\cos(\phi+\Delta\theta)]$ is a sum of
**positive** terms ($\Delta\tau\ge0$, $1-\cos\ge0$). Its coarse-grained second moment

$$M2^{\mu\nu}=\langle\Delta\tau\,e^\mu e^\nu\rangle=\sum \underbrace{\Delta\tau}_{\ge0}\,\underbrace{(e\otimes e)}_{\rm PSD}$$

is therefore **positive-definite** — a sum of a non-negative scalar times positive-
semidefinite rank-1 matrices. Measured (ρ=40, 1+1D, causal past of bulk events):

$$M2=\begin{pmatrix}+20114&\\&+5046\end{pmatrix},\qquad
\text{eigenvalues }\{+5046,\ +20114\}>0,\qquad a_t/a_x=3.99.$$

A Lorentz-invariant kinetic tensor must be $\propto g^{\mu\nu}=\mathrm{diag}(+,-)$,
which is **indefinite** (one negative eigenvalue). **A positive-definite matrix can
never be proportional to an indefinite one.** So the sharp action's quadratic form is
intrinsically **Euclidean**, and the "anisotropy" is exactly this Euclidean-vs-
Lorentzian mismatch — not a tunable defect.

## Two sources, one root

1. **Temporal elongation of the causal cone.** $a_t=\langle\Delta\tau\,\Delta t^2\rangle$
   dominates $a_x=\langle\Delta\tau\,\Delta x^2\rangle$ by ≈4× because causal links are
   timelike — every link has $\Delta t>|\Delta x|$, so $\Delta t^2$ is systematically
   larger. This is the factor that appears as $a_t/a_x\approx3.4$ (C1) and, through the
   plaquette areas built from those links, as $E/B\approx2.97$ (W2). Electric planes
   (containing the time edge) inherit the temporal excess; magnetic (purely spatial)
   planes do not.
2. **All-positive weighting.** Even if the cone were symmetric, $\sum(\text{positive})
   (e\otimes e)$ stays positive-definite. The relative minus sign of $g^{\mu\nu}$ — the
   light cone in the kinetic term — cannot arise from positive weights.

Context (read only, consistent): C1 `a_t/a_x` (3+1D) $=3.38$; W2 `E/B` $=2.97$.

## The cure this points to

An **indefinite** form requires a **sign-alternating** weight. The Benincasa–Dowker
smeared weight $w(m)$ (e10: positive near $m=0$, negative at intermediate $m$) is the
**only** network operator that alternates sign by construction — hence the only one that
can produce a Lorentzian (indefinite) second moment, $M2_{\rm BD}=\sum 2\epsilon\,w(m)\,
e^\mu e^\nu\to g^{\mu\nu}$. BD2 implements it; BD3/BD4 test whether the indefinite
signature actually emerges.

## Verdict (BD1)

> The order-1 Lorentz violation is **diagnosed exactly**: the sharp action is a sum of
> positive terms, so its second moment is positive-definite (Euclidean) and *cannot* be
> $\propto g^{\mu\nu}$; the magnitude (a_t/a_x≈4, E/B≈3) is the temporal elongation of
> causal links. The cure must be a **sign-alternating** weight — the BD smeared
> operator.

## Output
`BD1_diagnosis.py`, `BD1_diagnosis_data.json`.

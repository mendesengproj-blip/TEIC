# C1 — Poisson averages over causal links

**Task.** Measure, with no fit and no SR/GR formula, the Δτ-weighted moments of
causal-link vectors that feed every coefficient of the minimal action

$$S=\sum_{\text{links}}\Delta\tau_{ij}\,[1-\cos(\phi_{ij}+\Delta\theta_{ij})],\qquad
\phi+\Delta\theta=(A_\mu+\partial_\mu\theta)\,e^\mu,\quad e^\mu=q-p.$$

"Links $L_0$ (sem intermediários)" = **covering relations** $p\prec q$ with no event
between them (Hasse-diagram links). Generator: `C1_moments.py` (only
`causal_core.sprinkle_box` + bare Minkowski cones; no dilation factor, no metric,
no DEV).

## What was computed

For Poisson sprinklings in 1+1D and 3+1D, over **bulk** links (midpoint kept ≥25 %
inside every face, so the distribution is box-cutoff, not boundary-truncated):

1. $\langle\Delta\tau\rangle$ — mean link proper time
2. $M2^{\mu\nu}=\langle\Delta\tau\,e^\mu e^\nu\rangle$ — the **second moment tensor**
3. $\langle\Delta\tau\,e^\mu e^\nu e^\rho\rangle$ — third moment (causal asymmetry)
4. $n_{\text{links}}$ — bulk link density
5. decomposition $M2^{\mu\nu}=\kappa\,g^{\mu\nu}+\lambda\,u^\mu u^\nu$
   (signature $(+,-,\dots)$, $u$=time direction): $\kappa=-a_x$, $\lambda=a_t+a_x$
   with $a_t=\langle\Delta\tau\,\Delta t^2\rangle$, $a_x=\langle\Delta\tau\,\Delta x^2\rangle$.

## Numbers (reproducible, fixed seeds)

| quantity | 1+1D (ρ=60, 5×5, 60 real.) | 3+1D (ρ=10, 4⁴, 30 real.) |
|---|---|---|
| bulk links | 173 991 | 843 035 |
| $\langle\Delta\tau\rangle$ | 0.1490 | 0.6217 |
| $n_{\text{links}}$ density | 463.98 | 1756.32 |
| $a_t=\langle\Delta\tau\,\Delta t^2\rangle$ | **+0.2401** | **+3.3606** |
| $a_x=\langle\Delta\tau\,\Delta x^2\rangle$ | **+0.2334** | **+0.9938** |
| max off-diagonal | 2.1e−3 | 1.0e−2 |
| $\kappa$ (isotropic) | −0.2334 | −0.9938 |
| $\lambda$ (anisotropic) | +0.4735 | +4.3544 |
| **anisotropy $\lambda/|\kappa|$** | **2.029** | **4.382** |
| $a_t/a_x$ | 1.029 | 3.382 |
| $\langle\Delta\tau\,\Delta t^3\rangle$ | +0.564 | +8.80 |
| $\langle\Delta\tau\,\Delta x^3\rangle$ | −0.008 (≈0) | −0.010 (≈0) |

## The decisive structural fact

$M2^{\mu\nu}$ is **diagonal with all-positive entries**:

$$M2_{1+1}\approx\begin{pmatrix}0.240&0\\0&0.233\end{pmatrix},\qquad
M2_{3+1}\approx\begin{pmatrix}3.36&&&\\&0.99&&\\&&0.99&\\&&&0.99\end{pmatrix}.$$

It is therefore **Euclidean-like ($\propto\delta^{\mu\nu}$), not Lorentzian
($\propto g^{\mu\nu}$)** — a Lorentz-invariant result would require $a_x=-a_t<0$,
which is impossible for positive Δτ-weighted squares. Consequences:

- **Spatial isotropy is clean** — the three spatial diagonals in 3+1D are equal to
  <0.5 %, off-diagonals vanish, $\langle\Delta\tau\,\Delta x^3\rangle\approx0$.
- **Time–space anisotropy is large and irreducible.** $\lambda/|\kappa|$ is of order
  unity (≈2 in 1+1D) and *grows with dimension* (≈4.4 in 3+1D, where the time–time
  moment is 3.4× the space–space). The Lorentz-violating part $\lambda u^\mu u^\nu$
  is the **majority** of the tensor (LV fraction $\lambda/(\lambda+|\kappa|)$ = 0.67
  in 1+1D, 0.81 in 3+1D).
- **It is finite, not a divergence.** The 1+1D box-size scan (fixed ρ, growing
  spatial extent X) shows $\lambda/|\kappa|$ *converging*:

  | X | 3 | 5 | 8 | 12 | 16 |
  |---|---|---|---|---|---|
  | $\lambda/|\kappa|$ | 2.077 | 2.039 | 2.033 | 2.033 | 2.033 |

  So the anisotropy is a genuine, IR-stable property of the Δτ-weighted link
  ensemble — not an artefact of the cutoff. (`C1_anisotropy.png`.)

## Reading against Rule 4 (consistency with R1)

Rule 4 asked that the anisotropic part be small because **R1 proved Lorentz
invariance**. It is **not** small — it dominates. This is **not** a contradiction
of R1, and the reason matters:

- R1 established Lorentz invariance through the **chain-length / interval-volume
  proper time** and **fixed-τ count isotropy** — *scalar, counting* observables,
  which are genuinely Lorentz invariant.
- $M2^{\mu\nu}$ is a different object: the **second moment of raw link vectors**.
  Its non-Lorentz-invariance is the well-known **causal-set link non-locality** —
  individual covering-relation vectors do not transform simply; recovering Lorentz
  covariance requires the *non-local layered smearing* of the Benincasa–Dowker
  d'Alembertian (exactly what **D1** used), not raw nearest links.

**Honest consequence for the minimal action.** Taken *literally* over raw causal
links, $S=\sum_{\text{links}}\Delta\tau[1-\cos(\cdot)]$ inherits this anisotropy:
its coarse-grained quadratic form is a **Euclidean-like (preferred-frame) norm** of
$A_\mu+\partial_\mu\theta$, carrying an order-1 Lorentz-violating piece. The
Lorentz-invariant sector is real (coefficient $\kappa$), but it is accompanied by a
comparably large LV sector (coefficient $\lambda$). The cure is structural and known
(use the BD non-local kernel as in D1), and is flagged here rather than hidden.

This anisotropy does **not** affect the coefficient *ratios* tested in C2 — those
follow from the perfect-square (single-cosine) form within each operator pair and
are blind to the tensor's signature.

## Output

- `C1_moments.py` — generator
- `C1_moments_data.json` — all numbers above
- `C1_anisotropy.png` — Euclidean-like tensor + IR-convergence of the anisotropy

→ proceeds to **C2** (ratios), which consumes $\kappa$ and $n_{\text{links}}$.

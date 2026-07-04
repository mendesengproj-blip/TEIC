# BRIDGE_COEFFICIENTS — the coefficients of the minimal action: the decisive test

> **Independent investigation.** This does **not** modify R1–R3 or e6–e11, and is
> not part of the TEIC paper. It continues [`BRIDGE_RHO.md`](BRIDGE_RHO.md) (P1–P3),
> [`BRIDGE_DYNAMICS.md`](BRIDGE_DYNAMICS.md) (D1–D3),
> [`BRIDGE_NONLINEAR.md`](BRIDGE_NONLINEAR.md) (NL1–NL3) and the internal record in
> [`docs/DEV_bridge_future.md`](docs/DEV_bridge_future.md). All artefacts live in
> [`results/bridge/coefficients/`](results/bridge/coefficients/).

**The golden rule (obeyed).** No coefficient is adjusted to match the DEV. Every
coefficient comes out of Poisson averages over causal links, with **no fit** and **no
SR/GR formula** in any generator. The DEV enters **only** in the final comparison
(C2, C4), in clearly-marked `COMPARISON ONLY` blocks. The main pipeline's
anti-circularity guard is untouched (all new code lives under `results/`).

---

## The conjecture under test

A symbolic analysis proposed that the microscopic action is the one-liner

$$S=\sum_{\text{links}}\Delta\tau_{ij}\,[1-\cos(\phi_{ij}+\Delta\theta_{ij})],\qquad
\phi+\Delta\theta=(A_\mu+\partial_\mu\theta)\,e^\mu,$$

which expands ($1-\cos u\approx u^2/2$) into a five-term effective Lagrangian
$C_1X+C_2A^2+C_2'F^2+C_3A_\mu\partial^\mu\theta+\rho\sqrt{1-X/X_0}$. The **form** was
derived knowing the destination; the **coefficients** were not computed. The decisive
question: are the ratios $C_3/C_1$, $C_2/C_1$ **clean numbers fixed by geometry**
(real structure) or **free numbers needing adjustment** (reverse engineering)?

---

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **C1** — link moments | measure $\langle\Delta\tau\rangle$, $M2^{\mu\nu}=\langle\Delta\tau\,e^\mu e^\nu\rangle$, 3rd moment, $n_{\rm links}$; decompose $M2=\kappa g+\lambda u u$ | **DONE — with a flag.** Spatial isotropy clean (<0.5 %), but $M2$ is **Euclidean-like** ($\propto\delta^{\mu\nu}$, all-positive diagonal), **not** $\propto g^{\mu\nu}$. The Lorentz-violating part is **order 1 and dominant** ($\lambda/|\kappa|=2.03$ in 1+1D, $4.38$ in 3+1D) and **converges** with box size (not a divergence). |
| **C2** — the ratios | extract $C_1,C_2,C_3$, no fit; compute $C_3/C_1$, $C_2/C_1$; compare DEV | **CLEAN (1, 2), but ≠ DEV — and clean by algebra, not geometry.** $C_2/C_1=1$, $C_3/C_1=2$ exactly, identical in 1+1D and 3+1D. They are forced by the **single-cosine perfect square**, independent of the Poisson numbers. The DEV's analogues ($m_A^2/F_1$, $\gamma/F_1$) are **free**. |
| **C3** — the scale $X_0$ | measure $\Delta\tau_{\min}(\rho)$, infer $X_0\propto\rho^p$ | **$X_0\propto\rho^{1}$, dimension-independent** ($p=1.10$ in 1+1D, $1.01$ in 3+1D, $r^2>0.999$). Set by the light-cone sliver ($\Delta\tau_{\min}\propto\rho^{-1/2}$), **not** the lattice scale $\rho^{-1/D}$. ⇒ $X_0$ is **UV/granularity**, so the $a_0\sim cH$ link is **not** supported. |
| **C4** — completeness | 4th-order expansion; term-by-term vs DEV | **ALL THREE cases at once.** **Matches** $(\partial\theta)^4\leftrightarrow$ DEV $F(X)$; **predicts extra** gauge-invariant quartics $(A+\partial\theta)^4$ and LV operators the DEV lacks; **misses** $F_{\mu\nu}F^{\mu\nu}$ (needs plaquettes, not links). |

---

## The decisive answer, stated honestly

**Are the ratios fixed by the geometry (real structure) or do they depend on
adjustment (reverse engineering)?**

> **Neither, strictly.** The ratios $C_2/C_1=1$ and $C_3/C_1=2$ are **clean and not
> adjustable** — so it is *not* reverse engineering of free numbers. But they are
> **not fixed by the causal geometry** either: they are an **algebraic identity** of
> writing $\phi$ and $\Delta\theta$ inside a *single* cosine (i.e. of declaring
> $\theta$ the Stückelberg phase of $A$). *Any* symmetric link measure gives 1 and 2;
> the Poisson averages cancel out of the ratio. The geometry's genuine, falsifiable
> output is only the **overall scale** $\kappa$ and the **order-1 Lorentz violation**
> $\lambda$.

So the headline is **structural conjecture, not derivation**: the form *and* the
relative coefficients of the Lorentz-invariant sector are real and clean, but they are
self-consistency of the ansatz, not something the network independently selected. And
the clean $(1,2)$ is the **gauge-invariant Stückelberg/Proca special case** of the
DEV's scalar–vector sector — a **sister theory**, since the DEV's $m_A^2$ and $\gamma$
are free parameters that do not sit at $(1,2)$.

This places the result squarely in the prompt's case *"razões limpas ≠ DEV"*, with the
added honesty that the limpidez is algebraic, and with two substantive findings beyond
the ratio question:

- **A real tension (C1).** Taken literally over raw links, the action's quadratic form
  is Euclidean-like / preferred-frame, with an order-1 Lorentz-violating piece. This is
  the known causal-set **link non-locality**; it does not contradict R1 (which used
  scalar chain/volume proper time), and the cure is the **BD non-local kernel used in
  D1** — flagged, not hidden.
- **New predictions (C4).** Gauge-invariant quartic self-interactions
  $(A+\partial\theta)^4$ that the DEV does not contain, with coefficients fixed
  relative to the quadratic sector — testable in the strong-field / steep-density-
  gradient regime.

---

## Where this leaves the chain

```
causal network  →  S = Σ Δτ[1−cos(φ+Δθ)]  →  DEV ?
  P1–P3  ρ(r) kinematics                                  ✓
  D1–D3  dynamics, Newtonian ρ(r)                         ✓
  NL/DBI √ forced by the cone                             ✓ (form)
  minimal action, all terms in one line                  ✓ (form)
  COEFFICIENTS — are the RATIOS fixed?                    ← this test
```

- The **form** of the Lorentz-invariant sector and its **internal ratios** (1, 2) are
  real and clean — but algebraically forced, so they are **structural conjecture with
  the calibration (scale $\kappa$, $a_0$, $G$, $\Lambda$) open**, not a
  first-principles derivation of the DEV.
- The link action alone is **incomplete** (no $F^2$ kinetic term → auxiliary vector;
  needs a plaquette term) and **not manifestly Lorentz invariant** at the raw-link
  level (order-1 $\lambda$).

Both outcomes are publishable; the honest statement is: **the one-line action gives
the gauge-invariant Proca/Stückelberg structure of a DEV-sister theory, with clean
ratios that are structural-by-construction rather than geometrically derived, plus new
quartic predictions and an open Lorentz-violation/$F^2$ gap.**

---

## Artefacts

| file | content |
|---|---|
| [`results/bridge/coefficients/C1_moments.md`](results/bridge/coefficients/C1_moments.md) | link moments, $M2$ tensor, anisotropy |
| [`results/bridge/coefficients/C2_ratios.md`](results/bridge/coefficients/C2_ratios.md) | the decisive ratio test + DEV comparison |
| [`results/bridge/coefficients/C3_scale.md`](results/bridge/coefficients/C3_scale.md) | $X_0\propto\rho$ measurement |
| [`results/bridge/coefficients/C4_completeness.md`](results/bridge/coefficients/C4_completeness.md) | 4th-order expansion, term-by-term vs DEV |

Each `.md` has a matching `.py` generator and `_data.json`; figures
`C1_anisotropy.png`, `C3_powerlaw.png`. Reproduce with fixed seeds:

```
python results/bridge/coefficients/C1_moments.py
python results/bridge/coefficients/C2_ratios.py
python results/bridge/coefficients/C3_scale.py
python results/bridge/coefficients/C4_completeness.py
python results/bridge/coefficients/make_figures.py
```

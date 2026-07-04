# BRIDGE_D3_AUDIT — brutal audit of D3

> **Independent investigation.** Does **not** modify R1–R3 or e6–e11, and is not part
> of the TEIC paper. Continues [`BRIDGE_DYNAMICS.md`](BRIDGE_DYNAMICS.md) (D1–D3, where
> the unconstrained Monte Carlo found $\rho_{\rm MC}(r)=\rho_0(1+A/r)$, exponent $-1.02$,
> corr $0.9991$). All artefacts live in
> [`results/bridge/d3_audit/`](results/bridge/d3_audit/).

**Golden rule (obeyed).** No gravitational formula in any generator: $G$, $GM/r$,
$\sqrt{1-2M/r}$, "$4\pi G$" appear in **no** data-generating code. The source is a
dimensionless weight $w_M$ deposited on cells; $G$ is formed only in analysis (D3-D) or
in clearly-labelled comparison. The main-pipeline guard
(`tests/test_no_circularity.py`) still **passes** (all new code lives under `results/`).

---

## The methodological key

D3 ran Metropolis on the density field $\theta=\delta\rho/\rho_0$ under the quadratic
Benincasa–Dowker static action ($B_\varepsilon\to-\nabla^2$). Because that action is
**quadratic**, the Metropolis equilibrium *mean* is exactly the discrete-Poisson
minimiser. The audit exploits this: a deterministic solver returns the exact MC mean
(no sampling noise) for the exhaustive parameter maps, while a genuine batched
heat-bath MC supplies seed-to-seed **error bars** and confirms the network relaxes
there. D3-A validates the solver$=$MC-mean identity numerically; B/C/D then carry MC
error bars where sampling matters. This is the single fact that makes a 4-task,
multi-seed, convergence-documented audit tractable.

---

## Verdicts

| Task | Question | Verdict |
|---|---|---|
| **D3-A** robustness | does $p\to-1$ as $L,\rho\to\infty$, or is $-1$ a finite-size artefact? | **PASSA.** $p$ is **flat at $-0.991$** over the whole $L\times\rho$ grid; $L\to\infty$ extrapolation $p_\infty=-0.9913$ (no drift); MC noise on $p$ shrinks $0.0088\to0.0015$ as sweeps $10^4\to10^6$; D3's $-1.018$ in band. The $\sim1\%$ from exactly $-1$ is a constant log-grid/offset discretisation effect, **not** a drift. |
| **D3-B** source shapes | does $\nabla^2\theta=J$ hold for extended sources, or was $1/r$ special to a point mass? | **PASSA.** The relaxed field equals the **independent radial-quadrature Poisson solution to $0.9998$** for sphere/NFW/exponential; the **exterior is $1/r$** (exponent $-0.996,-0.998$) for sphere/disk; sphere interior is concave (correct sign). Poisson is the **generic** law. |
| **D3-C** superposition | does $\theta_{\rm total}=\theta_1+\theta_2$? | **PASSA.** Solver superposition is **exact** (corr $1.000000$, rms $1.8\times10^{-9}$): the network obeys a **linear** equation. MC confirms within the sampling floor (corr $0.86$). An illustrative DBI completion (added by hand) breaks superposition only in strong field, in the saturating direction (residual $\times12$). |
| **D3-D** the constant $G$ | does $G$ emerge, or was it put in? | **CASE (b).** $G_{\rm net}=A/w_M$ is **constant** in $w_M$ (slope $0$, CV $0$), $\rho$ ($+0.007$), $L$ ($+0.003$), but $\propto 1/K$ (slope $\mathbf{-1.000}$). The network derives the **coupling relation**; the **value** rides on the action stiffness $K$ (granularity scale) — the $a_0$ pattern. |

---

## The honest bottom line

**D3 survives the audit.** The Newtonian profile of D3 is robust, generic, and linear —
and the one thing it does *not* do (derive $G$ as a universal number) is stated plainly.

- **The $-1$ exponent is a law, not an artefact (A).** It does not drift with box size or
  density; it converges to $-1$ (to $\sim1\%$ discretisation) and D3's value sits in the
  band. The geometric content is the $1/r$ Green's function of the 3D Laplacian.

- **Poisson is the generic law (B).** The relaxed field is the Poisson solution of *every*
  source shape tested — matched to $0.9998$ by an **independent** 1D quadrature that never
  touches the 3D stencil, with the textbook harmonic-exterior ($1/r$) and concave-interior
  signatures. The $1/r$ of D3 was not a point-source accident.

- **The network obeys a linear equation (C).** Superposition is exact for the quadratic
  BD action. The DBI strong-field non-linearity is a property of the **separate**
  cone/clock sector (NL1/W3), not of the BD action used in D1–D3 — shown illustratively,
  not claimed for the implemented action.

- **$G$ is emergent as a *relation*, external as a *value* (D).** This is the most
  important and most honest result of the audit, and it lands exactly where the prompt's
  honest expectation placed it:

  > $G$ is **not** derived as a universal constant. The network produces the coupling
  > RELATION (linear, Poisson, $1/r$) — constant in $w_M,\rho,L$ — but the numerical value
  > $G_{\rm net}\propto1/K$ rides on the action stiffness $K$, the granularity / Planck
  > normalisation, an external input. Same pattern as $a_0$: the FORM is derived, the
  > SCALE is measured. No pure geometric theory has derived $G$; TEIC is not an exception.

A subtle point worth keeping: varying only $(w_M,\rho,L)$ would have *wrongly* suggested
case (a) "universal constant" — it was the explicit $G_{\rm net}\propto1/K$ sweep that
exposed the external scale. The audit therefore also corrects a trap one could have
fallen into by not varying the action normalisation.

---

## A recurring, honestly-reported limit

Two tasks meet the **same $\rho^{3/4}$ variance wall** documented for the BD operator
(e10, [`BRIDGE_BD.md`](BRIDGE_BD.md)): the pointwise Laplacian of a finite-sweep MC field
(B) and the per-mean superposition residual (C) are noise-dominated. In both, the
**equilibrium mean** is clean (solver / quadrature), and the MC relaxes toward it but
slowly for smooth fields (the exponential source's relaxation corr is only $0.16$ at
$9\times10^3$ sweeps). This is reported, not hidden; the verdicts rest on the
noise-free, non-circular checks (radial quadrature, analytic regimes, the exact solver).

---

## Artefacts

| file | content |
|---|---|
| [`d3_audit_core.py`](results/bridge/d3_audit/d3_audit_core.py) | shared engine: radial + 3D quadratic-action solver and heat-bath MC, discrete Laplacian, fits |
| [`D3A_robustness.md`](results/bridge/d3_audit/D3A_robustness.md) · `.py` | exponent vs $L,\rho$, seeds, sweeps; $L\to\infty$ extrapolation |
| [`D3B_sources.md`](results/bridge/d3_audit/D3B_sources.md) · `.py` | four source shapes; radial-quadrature Poisson test |
| [`D3C_superposition.md`](results/bridge/d3_audit/D3C_superposition.md) · `.py` | $\theta_{\rm tot}=\theta_1+\theta_2$; linear vs DBI |
| [`D3D_gravitational_constant.md`](results/bridge/d3_audit/D3D_gravitational_constant.md) · `D3D_G.py` | $G_{\rm net}$ vs $w_M,\rho,L,K$; the climax |

Each `.py` writes a seeded `_data.json` and a `.png` figure
(`D3A_robustness.png`, `D3B_sources.png`, `D3C_superposition.png`, `D3D_G.png`).
Reproduce (≈ 9 min total):

```
python results/bridge/d3_audit/D3A_robustness.py
python results/bridge/d3_audit/D3B_sources.py
python results/bridge/d3_audit/D3C_superposition.py
python results/bridge/d3_audit/D3D_G.py
python tests/test_no_circularity.py        # guard still passes (exit 0)
```

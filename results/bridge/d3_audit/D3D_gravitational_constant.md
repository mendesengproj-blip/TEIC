# D3-D — does $G$ emerge, or was it put in? (the critical task)

> Brutal audit of D3, task D — the climax. Independent of R1–R3 / e6–e11. Reproduce:
> `python results/bridge/d3_audit/D3D_G.py` (~18 s).

## The precise question
D3 measured the **exponent** ($-1$, from the 3D Laplacian geometry). It did **not**
measure the **amplitude**, where a coupling constant lives. Define the network's
effective coupling
$$G_{\rm net}=\frac{\text{amplitude of the }1/r\text{ well}}{\text{source weight}}=\frac{A}{w_M}.$$
Measure $G_{\rm net}$ while varying the source weight $w_M$, the density $\rho$, the box
$L$, and — crucially — the action stiffness $K$. The source is a dimensionless weight;
$G$ appears nowhere in the generator (this task asks whether the network *itself* carries
a coupling).

## The three possibilities
- **(a)** $G_{\rm net}=$ const, independent of *everything* → universal, extraordinary.
- **(b)** $G_{\rm net}$ depends on the granularity scale → form derived, value external
  (the $a_0$ pattern).
- **(c)** $G_{\rm net}=f(w_M)$ non-linear → the coupling is not Poisson.

## Result

| swept variable | log-log slope | meaning |
|---|---|---|
| source weight $w_M$ | $-0.000$ (CV $=0$) | $G_{\rm net}$ **constant** → linear (rules out **c**) |
| network density $\rho$ | $+0.007$ | independent of granularity/resolution |
| box size $L$ | $+0.003$ | stable for large box |
| **action stiffness $K$** | $\mathbf{-1.000}$ | $G_{\rm net}\propto 1/K$ |

Reference point: $G_{\rm net}=0.981$ (solver) $=0.980\pm0.011$ (MC, 20 seeds) — agree.

## Verdict — **case (b)**
$G_{\rm net}$ is **constant in $(w_M,\rho,L)$** but **rides on the action stiffness $K$**
($G_{\rm net}\propto 1/K$, slope $-1.0000$). The network produces the **coupling
relation** — a linear, Poisson-form law (amplitude $\propto w_M$, exponent $-1$) — but
the numerical **value** $G_{\rm net}=\mathcal{O}(1/K)$ is set by $K$, the action
normalisation (the granularity / Planck scale), which is an **input**.

> **$G$ is not derived as a universal constant.** The network derives the FORM and the
> LINEARITY of the gravitational coupling (Poisson, $1/r$), but the value of $G$ rides on
> the granularity normalisation $K$ — an external scale. This is exactly the same pattern
> as $a_0$: the form is derived, the scale is measured. No pure geometric theory has
> derived $G$; TEIC is not an exception.

The constancy in $(w_M,\rho,L)$ is real and rules out cases **(c)** and a
granularity-dependent **(b′)** ($\delta\approx0$ for $\rho$); but the explicit
$G_{\rm net}\propto1/K$ sweep is what forbids calling this case **(a)** (universal): had
we only varied $w_M,\rho,L$ we would have wrongly concluded "universal constant". Varying
the action normalisation exposes the external scale.

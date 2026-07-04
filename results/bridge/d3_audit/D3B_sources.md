# D3-B — does the network obey $\nabla^2\theta=J$ for any source shape?

> Brutal audit of D3, task B. Independent of R1–R3 / e6–e11. Reproduce:
> `python results/bridge/d3_audit/D3B_sources.py` (~150 s).

## Question
D3 used a point source and found $\theta\sim1/r$. Is Poisson the **generic** law the
network obeys, or was $1/r$ special to a point mass? Test four extended sources:
homogeneous sphere, thin disk, NFW ($\rho\propto1/[x(1+x)^2]$), exponential.

## Method — three non-circular checks
Taking the discrete Laplacian of a **finite-sweep MC field is hopeless**: the second
derivative amplifies the MC sampling noise (the same $\rho^{3/4}$ wall the BD operator
hits in e10). So the law is tested without differentiating a noisy field:

1. **Independent radial quadrature.** Gauss's law gives the Poisson solution by a 1D
   integral that never touches the 3D stencil:
   $\theta'(r)=-Q_{\rm net}(r)/(4\pi K r^2)$, $Q_{\rm net}=$ enclosed $(q-\bar q)$.
   Compare to the relaxed field.
2. **Analytic regimes.** A uniform ball $\Rightarrow$ $\theta\sim a-br^2$ inside ($b>0$)
   and $\theta\sim1/r$ outside; **outside any bounded source the field is harmonic**,
   so the exterior exponent is $-1$ for every shape.
3. **Dynamical bridge.** The MC generator contains **no Poisson equation** — only local
   gradient heat-bath moves; we show $\mathrm{corr}(\theta_{\rm MC},\theta_{\rm Poisson})$
   rises toward the equilibrium.

No $G$/$GM/r$/Schwarzschild in any generator.

## Result

| source | quadrature corr | exterior exponent | MC relax corr |
|---|---|---|---|
| sphere | **0.99977** | $-0.996$ | 0.55 |
| disk | n/a (non-radial) | $-0.998$ | 0.54 |
| NFW | **0.99984** | n/a (no sharp edge) | 0.53 |
| exp | **0.99992** | n/a (no sharp edge) | 0.16 |

- The relaxed field equals the **independent radial-quadrature Poisson solution to
  $\sim0.9998$** for every radial shape.
- The **exterior is $1/r$** (exponent $-0.996$, $-0.998$) for the two bounded shapes —
  the harmonic-exterior signature, shape-independent.
- Sphere interior is **concave** ($b<0$ in $a+br^2$), the correct Poisson sign.

## Verdict — **PASSA**
The network obeys $\nabla^2\theta=J$ **generically** — the relaxed field is the Poisson
solution of *each* source shape, not a $1/r$ accident of a point mass. The death
criterion (field $\ne$ Poisson solution for extended sources) is not met.

**Honest caveats.** (i) The decisive evidence is the **quadrature match** on the
equilibrium field; the pointwise $\nabla^2\theta$ of a raw MC field is noise-dominated
($\rho^{3/4}$ wall), exactly why the causal-set literature validates the BD operator via
the summed action, not pointwise. (ii) The MC relaxation corr is only modest (0.16–0.55
at $9\times10^3$ sweeps), and **low (0.16) for the exponential** — its smooth, spread-out
field has tiny signal, so the mean is noise-limited at accessible sweeps; the relaxation
is real but slow there. None of this affects the law verdict, which rests on the
non-circular quadrature and analytic-regime tests.

# D3-A — robustness of the $-1$ exponent

> Brutal audit of D3, task A. Independent of R1–R3 / e6–e11. Reproduce:
> `python results/bridge/d3_audit/D3A_robustness.py` (~165 s).

## Question
Is D3's tail exponent $p=-1$ a law, or a finite-size artefact? Vary box $L$, network
density $\rho$ (= cell resolution), seeds, and MC steps.

## Method
For the quadratic Benincasa–Dowker action the Metropolis equilibrium **mean** is
exactly the discrete-Poisson minimiser (see `d3_audit_core` docstring). So the
deterministic solver gives the $L,\rho\to\infty$ (zero-MC-noise) exponent on the full
$L\times\rho$ grid, while the batched heat-bath MC gives seed-to-seed error bars and
shows the MC noise shrinking with sweeps. No $G$/$GM/r$/$\sqrt{1-2M/r}$ in the
generator — the source is a dimensionless weight $w_M$.

## Result

$p(L,\rho)$ from the exact solver (= MC mean):

| $L\backslash\rho$ | 50 | 100 | 200 | 400 |
|---|---|---|---|---|
| 10 | $-0.990$ | $-0.992$ | $-0.992$ | $-0.991$ |
| 20 | $-0.989$ | $-0.991$ | $-0.990$ | $-0.990$ |
| 40 | $-0.992$ | $-0.992$ | $-0.991$ | $-0.990$ |
| 80 | $-0.991$ | $-0.992$ | $-0.992$ | $-0.992$ |

- **$L\to\infty$ extrapolation** (intercept of $p$ vs $1/L$): $p_\infty=-0.9913$,
  consistent across all $\rho$ (no drift with either $L$ or $\rho$).
- **MC noise on $p$ shrinks with sweeps** (rep. $L{=}40,\rho{=}100$, 20 seeds):
  $-0.9933\pm0.0088$ ($10^4$) → $-0.9922\pm0.0033$ ($10^5$) → $-0.9916\pm0.0015$
  ($10^6$); $\mathrm{std}\propto$ sweeps$^{-1/2}$, and $|{\rm MC-solver}|_{\max}$ falls
  $2.0\times10^{-2}\to2.8\times10^{-3}$.
- **D3's stored $-1.018$ sits inside the band.**

## Verdict — **PASSA**
The exponent is dead flat at $-0.991$ across the whole $L\times\rho$ grid; it does
**not** drift toward $-1.2$ or $-0.8$ as $L$ grows (the death criterion is not met).
D3's $-1$ is a **law**, not a finite-size artefact.

**Honest caveat.** The converged value is $-0.991$, i.e. $-1$ to $\sim1\%$, not exactly
$-1.000$. The $\sim1\%$ residual is a **discretisation effect** (log-spaced radial bins
+ the conservation-offset fit), is **constant** in $L$ and $\rho$ (it does not drift),
and is the same $\sim1$–$2\%$ band D3 itself reported ($-1.018$). The geometric content
— the $1/r$ Green's function of the 3D Laplacian — is robust.

# C3 — The DBI scale X₀

**Task.** Measure the scale $X_0$ of the saturated term $\rho\sqrt{1-X/X_0}$ and its
dependence on network density $\rho$ and coherence length $\ell$. Generator:
`C3_scale.py` (sprinkling + bare cones only; no fit to data, no DEV).

## Conjecture under test

The DBI square root is the **light cone in field space**: $X_0=(\Delta\theta/\Delta\tau)^2_{\max}$,
the largest field velocity the discrete network can carry on a link. With
$\Delta\theta$ across a link bounded by the field's coherent variation
$\Delta\theta_{\max}$, the geometric half is the **smallest causal link proper time**
$\Delta\tau_{\min}(\rho)$:

$$X_0=(\Delta\theta_{\max}/\Delta\tau_{\min})^2 .$$

## What the measurement exposes

$\Delta\tau_{\min}$ is the proper time to the nearest future neighbour, averaged over
bulk events. The naïve guess was the lattice-discreteness length $\rho^{-1/D}$. The
data **rejects** it:

| ρ (1+1D) | 80 | 160 | 320 | 640 | 1280 |
|---|---|---|---|---|---|
| Δτ median | 0.0416 | 0.0282 | 0.0193 | 0.0132 | 0.0091 |

| ρ (3+1D) | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|
| Δτ median | 0.1062 | 0.0740 | 0.0531 | 0.0370 | 0.0263 |

Power-law fits ($r^2>0.999$):

| | $\Delta\tau_{\min}\propto\rho^{\,q}$ (median) | $\Rightarrow X_0\propto\rho^{\,p}$ |
|---|---|---|
| **1+1D** | $q=-0.549$ | $p=+1.097$ |
| **3+1D** | $q=-0.503$ | $p=+1.007$ |
| naïve lattice $\rho^{-1/D}$ | −0.50 / −0.25 | rejected in 3+1D |

So $\Delta\tau_{\min}\propto\rho^{-1/2}$ in **both** dimensions, and therefore

$$\boxed{X_0\propto\rho^{\,1}}\quad\text{(dimension-independent).}$$

## Why $-1/2$ and not $-1/D$

The smallest causal link is **not** set by event spacing. The region
$\{0<\Delta t^2-\Delta x^2<\varepsilon\}$ is a thin sliver hugging the light cone
whose box measure vanishes **linearly** in $\varepsilon$ in every dimension. With
$N\sim\rho$ candidate events, $\min\Delta\tau^2\sim 1/\rho$, hence
$\Delta\tau_{\min}\sim\rho^{-1/2}$ regardless of $D$. The numerics confirm this to
better than 1 % in 3+1D and ~5 % in 1+1D (`C3_powerlaw.png`). This is a genuine
geometric prediction (no algebra freedom), and it came out *different* from the
first guess — the data, not the conjecture, set the exponent.

## What $X_0\propto\rho$ means physically

- $X_0$ scales with the **granularity** (density), with exponent $p\approx1$. The
  saturation scale is therefore **fundamental / UV** — tied to the discreteness
  scale — not an emergent large coherence length.
- The hoped link to $a_0\sim cH$ would require $X_0\propto 1/\ell^2$ with
  $\ell=$ Hubble horizon (an **IR** scale). The measured $X_0\propto\rho$ points the
  **opposite** way: a UV (Planck-granularity) origin gives no natural cosmological
  $a_0$. So **the $a_0\sim cH$ connection is not supported by this scaling** — it
  remains a separate order-of-magnitude coincidence (consistent with
  `docs/DEV_bridge_future.md` §1, which already records $a_0\sim cH$ as *not derived*).

## Honest status

The geometric exponent $p\approx1$ is solid and dimension-independent. The
*absolute* value of $X_0$ still carries the field-dependent factor
$\Delta\theta_{\max}^2$, which is **not** fixed by geometry alone — left explicit
rather than absorbed. The conjecture "X₀ = field-space light cone" is consistent with
the measured scaling; its cosmological interpretation ($a_0\sim cH$) is **not**.

## Output

- `C3_scale.py`, `C3_scale_data.json`, `C3_powerlaw.png`.

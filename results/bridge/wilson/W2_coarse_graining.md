# W2 — Action with plaquettes: does F² emerge and coexist with the quartic?

**Task.** Extend the action to
$S=\sum_{\rm links}\Delta\tau[1-\cos(\phi+\Delta\theta)]+\lambda_p\sum_{\rm plaq}[1-\cos W_p]$,
coarse-grain both sums, measure the coefficients $C_F$ (Maxwell) and $C_q$ (quartic),
and decide whether they **coexist** (a), **conflict** (b), or whether the plaquette
**suppresses** the quartic (c). Generator: `W2_coarse_graining.py`.

**Anti-circularity.** $F^2$ is not inserted. The plaquette term is
$\lambda_p\sum[1-\cos W_p]$ with $W_p$ the holonomy of W1; at 2nd order
$\tfrac{\lambda_p}2\sum W_p^2=\tfrac{\lambda_p}8 F_{\mu\nu}F_{\rho\sigma}\sum\Omega_p^{\mu\nu}\Omega_p^{\rho\sigma}$,
so $F^2$ **emerges** iff the plaquette bivector moment has Maxwell structure. The DEV
appears only in W4.

## Measured coefficients (no fit)

| | 1+1D (ρ=120, 6²) | 3+1D (ρ=12, 4⁴) |
|---|---|---|
| link $\kappa$ | −0.2133 | −0.9555 |
| $n_{\rm links}$ | 1064.3 | 2364.1 |
| $C_1=C_2=\kappa n/2$ | −113.5 | −1129.5 |
| $C_3=\kappa n$ | −227.0 | −2259.0 |
| $C_q$ (link 4th order) | **−355.6** | **−8407.1** |
| $n_{\rm plaq}$ (total) | 107 204 | 7 840 |
| $\Pi=\langle\text{area}^2\rangle$ density | 654.4 | 272.3 |
| $C_F=\lambda_p\,\Pi/4$ | $\lambda_p\cdot163.6$ | $\lambda_p\cdot68.07$ |

## The three findings

**1. F² emerges (form).** The plaquette quadratic term produces a term built from
$F_{\mu\nu}F_{\rho\sigma}\langle\Omega^{\mu\nu}\Omega^{\rho\sigma}\rangle$. The
**off-Maxwell (parity-odd, $F\wedge F$ / θ-term) component vanishes**: the signed
cross $\langle\Omega^{01}\Omega^{23}\rangle=+0.013\pm0.009$, consistent with zero (as
parity requires for a Poisson sprinkle). So the emergent tensor structure is the pure
$F_{\mu\nu}F^{\mu\nu}$ Maxwell channel — no spurious θ-term. **This fixes C4's
"missing F²".**

**2. The quartic survives — coexistence (case a).** $C_q$ is finite and nonzero in
both dimensions, with the sign $<0$ that drives the DBI saturation (W3). It comes from
the **link** 4th order; $F^2$ comes from the **plaquette** sum. They are **disjoint
sums of distinct operators** — $(A\cdot\partial\theta)^2$ vs $(\partial A)^2$ — so they
add without cancelling. Adding plaquettes leaves the entire link sector
($C_1,C_2,C_3,C_q$) untouched. **Answer: (a) coexist harmoniously.**

**3. The emergent Maxwell term is Lorentz-violating.** In 3+1D the plaquette area²
splits by orientation:

$$\langle(\Omega^{0i})^2\rangle_{\rm electric}=1.663,\qquad
\langle(\Omega^{ij})^2\rangle_{\rm magnetic}=0.560,\qquad
\boxed{E/B=2.970\pm0.031}.$$

A Lorentz-invariant $-\tfrac14F_{\mu\nu}F^{\mu\nu}$ requires the **same** coefficient
for $E^2=F_{0i}^2$ and $B^2=F_{ij}^2$ (ratio 1). The measured ratio is ≈3: the
emergent term is effectively $C_E E^2 - C_B B^2$ with $C_E/C_B\approx3$. This is the
**same preferred-frame anisotropy** found for links in C1 (there $a_t/a_x=3.38$): the
arrow of time makes time-containing planes "larger". The plaquette sector inherits the
causal-set non-locality exactly as the link sector did.

## What is fixed by geometry and what is free

- The **form** ($F_{\mu\nu}F^{\mu\nu}$, gauge-invariant, no θ-term): fixed — emerges.
- The **overall weight** $C_F=\lambda_p\Pi/4$: **free**, because $\lambda_p$ (and the
  plaquette-counting convention that sets $\Pi$) are free. So $C_F/C_3\sim\lambda_p$ is
  a tunable ratio — exactly like the DEV's $F^2$ coefficient $K$ being an independent
  parameter (W4).
- The **E/B split** $\approx3$: a geometric prediction — and an honest **problem**
  (order-1 Lorentz violation), the same one flagged in C1, cured by the same
  non-local (Benincasa–Dowker) smearing rather than raw nearest links/plaquettes.

## Verdict (W2)

> $F^2$ **emerges** from the plaquette term with the correct gauge-invariant Maxwell
> form (no θ-term), **coexisting** harmoniously with the surviving quartic (case a) —
> they are disjoint sums of distinct operators. The relative weight $C_F/C_3$ is
> **free** ($\sim\lambda_p$, like the DEV's $K$). But the emergent Maxwell term is
> **Lorentz-violating** at the raw-plaquette level ($E/B\approx3$), the C1 anisotropy
> resurfacing — fixed only by the BD non-local construction, flagged honestly.

## Output
`W2_coarse_graining.py`, `W2_coarse_graining_data.json`.

# BD3 — Coarse-graining with the BD smeared operator

**Task.** Redo the C1–C4 coarse-graining with $B_\epsilon$: the moments (BD3a),
coefficient ratios (BD3b), and the Lorentz signature / E-B test (BD3c). Generator:
`bd_summed_action.py` — using the **summed-action** estimator that BD use precisely
because it beats the $\rho^{3/4}$ pointwise variance (e10), summing over many bulk
events with error bars across realisations.

## BD3a / BD3c — the Lorentz signature (dispersion)

The cleanest Lorentz test is the dispersion sign: for a purely spatial probe
$\cos(kx)$ and temporal probe $\cos(kt)$, the global Rayleigh quotient
$\lambda=\sum_x\phi\,(B_\epsilon\phi)/\sum_x\phi^2$ should give $\lambda_{\rm space}>0$
and $\lambda_{\rm time}<0$ (i.e. $\Box=\partial_t^2-\partial_x^2$, **opposite signs**).

Result (ρ=30, box 8×14, ε=0.4, 30 realisations, ~250 bulk events each):

| k | $\lambda_{\rm space}$ (want >0) | $\lambda_{\rm time}$ (want <0) | Lorentzian? |
|---|---|---|---|
| 0.4 | $-0.034\pm0.036$ | $-0.015\pm0.044$ | no |
| 0.6 | $-0.058\pm0.030$ | $+0.015\pm0.021$ | **wrong sign** |
| 0.8 | $-0.004\pm0.032$ | $+0.006\pm0.026$ | ≈0 |

Summed second moment: $a_t=-0.078\pm0.090$, $a_x=+0.099\pm0.088$.

**Honest reading.** Every quantity is **consistent with zero** within ~1–2σ. Where the
signs are "opposite" they are *opposite to the Lorentzian ordering* (space negative,
time positive). The summation cut the variance ~10× (SEM $0.03$–$0.09$ vs $0.3$–$0.9$
pointwise — the expected $1/\sqrt N$), **but the smeared signal is proportionally tiny**
($\sim\Box/(2\epsilon\rho_{\rm eff})$, exactly as e10 documents), so SNR ≈ 1. The
Lorentzian signature is **not resolved** at accessible scales.

So BD3c does **not** reach E/B = 1.00 ± 0.05. What it shows is weaker but true: the
sharp Euclidean anisotropy (a_t/a_x≈4) is **gone** (BD2), and what replaces it is
consistent with the isotropic/indefinite target but buried under the BD variance wall.

## BD3b — the coefficient ratios

The ratios $C_2/C_1=1$, $C_3/C_1=2$ are **unchanged** by smearing. They follow from the
Stückelberg perfect square $(A+\partial\theta)^2$ (C2 task) — an *algebraic* identity in
the combination $A_\mu+\partial_\mu\theta$, independent of the measure or the operator
used to weight links. Smearing changes the *scale* and the *signature* of the second
moment, not the 1:2:1 split. So BD3b is a pass by construction (nothing to re-fit).

## Verdict (BD3)

> BD smearing **removes the Euclidean anisotropy** but does **not** positively restore
> the Lorentzian signature at accessible network sizes: λ_space, λ_time and a_t, a_x are
> all consistent with zero (and where nonzero, mis-ordered). The summed action delivers
> the expected $\sqrt N$ variance gain, yet the smeared signal $\sim\Box/(2\epsilon\rho)$
> is buried — the documented BD/Glaser wall. Ratios 1:2 hold (algebra). **E/B = 1 is not
> demonstrated.**

## Output
`bd_summed_action.py`, `bd_summed_action_data.json`, `BD_sharp_vs_smeared.png`.

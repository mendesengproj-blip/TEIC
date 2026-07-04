# BD4 — Determination of ε

**Task.** Scan ε, find the value $\epsilon_0$ that restores Lorentz (E/B → 1), and
measure its scaling with ρ. Generator: `bd_summed_action.py` (ε scan, k=0.6).

## Result — there is no magic ε₀

| ε | $\lambda_{\rm space}$ (want >0) | $\lambda_{\rm time}$ (want <0) | $a_t$ | $a_x$ | Lorentz? |
|---|---|---|---|---|---|
| 0.2 | $-0.029\pm0.022$ | $+0.033\pm0.013$ | $-0.07\pm0.14$ | $+0.28\pm0.13$ | no |
| 0.3 | $-0.021\pm0.030$ | $+0.019\pm0.020$ | $+0.08\pm0.19$ | $+0.32\pm0.19$ | no |
| 0.5 | $+0.003\pm0.052$ | $-0.006\pm0.045$ | $+0.36\pm0.40$ | $+0.50\pm0.39$ | no |
| 0.7 | $-0.002\pm0.102$ | $-0.052\pm0.083$ | $+0.52\pm0.65$ | $+0.61\pm0.65$ | no |

**No ε gives the Lorentzian signature.** At every ε, $\lambda_{\rm space}$ and
$\lambda_{\rm time}$ are consistent with zero (and where nonzero, mis-ordered), and the
second-moment components never separate into $a_t>0,\,a_x<0$ of equal magnitude. There
is no minimum-of-E/B to locate, because E/B never resolves away from "consistent with
1-or-anything" within errors.

## What ε actually is — a bias-variance knob

The scan exposes the true role of ε, correcting the premise that it is a hidden
network constant to be fit:

- **The error bars grow monotonically with ε** (a_x SEM: $0.13\to0.19\to0.39\to0.65$
  from ε=0.2→0.7). Larger ε puts more weight on the sign-alternating tail of $w(m)$,
  which is exactly where the variance lives. So more smearing ⇒ *more* noise, not a
  cleaner signal.
- The continuum/Lorentz limit is **not** a special ε but $\epsilon\rho_{\rm eff}\to\infty$
  with ε small enough to control variance (e10, T1b: the discreteness bias shrinks with
  effective density $\epsilon\rho$). At fixed accessible ρ the two requirements conflict
  — small ε ⇒ bias, large ε ⇒ variance — and SNR ≈ 1 in between, for all ε.

So ε is **not** a derived geometric constant; it is the smearing scale of a bias-variance
trade-off. The prompt's hypothesis ($\epsilon\propto\rho^{-\delta}$ as a structural
constant) is **not** what the data show: ε is a regulator, and the limit that matters is
$\epsilon\rho\to\infty$ — a *computational-scale* statement, not a value of ε.

## Verdict (BD4)

> **No ε₀ restores Lorentz.** ε is a bias-variance regulator (error grows with ε; the
> physical limit is $\epsilon\rho\to\infty$), not a hidden network constant. At
> accessible ρ the smeared signal is buried at every ε. (`BD_sharp_vs_smeared.png`,
> right panel.)

## Output
`bd_summed_action.py`, `bd_summed_action_data.json` (`eps_scan`), `BD_sharp_vs_smeared.png`.

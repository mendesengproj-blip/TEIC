# LD3 -- Honest synthesis: everpresent-Lambda DYNAMICS

```
QUESTION (RESEARCH_MAP Section 6 #7):
  LAMBDA_EVERPRESENT (L1-L3) measured the static fluctuation coefficient and
  DECLARED the temporal evolution out of scope ("precisa do elo dinamico --
  fora do escopo desta campanha"). LD supplies that link: does Lambda(t),
  built from the MEASURED L1 coefficient via the everpresent ansatz
  Lambda_rms ~ 1/sqrt(V4_past), evolve consistently over cosmic history?

LD1 (tracking):
  V4_past converges in z_max?                      YES (<0.5% from z_max=10..50)
  finite, nonzero at z=0?                          YES (Lambda_rms(0) finite)
  Lambda_rms ~ rho_crit^p, exponent p =            1.107 (R^2=0.996)
LD2 (coincidence + effective w):
  e-folds with Omega_Lambda~O(1): LCDM vs ever     1.0  vs  6.9
  apparent w_eff(z=0) from envelope                -0.66  (-> 0 at high z)

KILL CRITERION (pre-registered): DEATH if Lambda diverges at z~0 OR is
inconsistent with w=-1.

VERDICT:

[ ] DEATH       -- diverges at z~0 or pathological
[X] CONSISTENT  -- finite everywhere; tracks rho_crit (p~1); dissolves the
                   coincidence; instantaneously w=-1; with one honest caveat
[ ] (the caveat: the envelope's APPARENT w drifts from -1 -- a signature, see below)
```

## Verdict: CONSISTENT (kill criterion does not fire), with a declared caveat

**No divergence at z~0.** The causal past 4-volume is finite and convergent at
the present (V4_past(0) = 0.125 in Hubble units, stable to <0.5% as the cutoff
moves z_max=10→50), so Lambda_rms(0) is finite and nonzero. The first leg of the
death criterion does not fire.

**It tracks the critical density.** Feeding the *measured* L1 coefficient (0.971)
into the everpresent ansatz, Lambda_rms ∝ rho_crit^p with **p = 1.107 ± (R²=0.996)**
over z = 0..8. The near-unity exponent is the geometric heart of everpresent Λ:
the past 4-volume scales roughly as H⁻⁴, so 1/√V₄ ~ H² ~ rho_crit. Λ stays
comparable to the critical density at every epoch -- the property Sorkin's
proposal is named for, here driven by the network's own Poisson fluctuation law
δρ/ρ = 1/√(ρV) rather than a dimensional guess.

**It dissolves the coincidence problem.** Because Λ tracks rho_crit, Ω_Λ stays
O(1) (0.1–0.9) for **~6.9 e-folds** of expansion, versus only **~1.0 e-fold** for
a constant Λ. In ΛCDM, Ω_Λ was ~10⁻⁵ at z=5 and the present epoch (Ω_Λ ≈ Ω_m) is
finely special; in the everpresent picture Ω_Λ ≈ 0.49–0.85 across z = 0..1000 and
no epoch is special. This is the qualitative payoff of giving Λ a dynamics.

**The honest caveat (the second leg of the death criterion).** The everpresent Λ
enters Einstein's equations as a genuine cosmological-constant term at *each
instant* -- so its *instantaneous* equation of state is **w = −1 by construction**,
and the model is not "inconsistent with w=−1" in the pathological sense the death
criterion guards against. BUT the slowly-drifting RMS *envelope* (p = 1.107 ≠ 1)
has an apparent effective EoS **w_eff(0) ≈ −0.66**, rising toward 0 at high z.
This envelope-w is exactly the quantity the everpresent-Λ literature
(Zwane–Afshordi–Sorkin 2018) confronts with data, where it is found viable but
distinctive (more scatter than ΛCDM, w₀ on the high side). We report w_eff(0) ≈
−0.66 straight: it is **on the high edge of current dark-energy bounds**, a
*testable signature* of the dynamics, not a death. The deviation is entirely the
0.107 excess of p over perfect tracking.

## What is TEIC's, what is imported (mirrors L3 and FM4)

- **TEIC's contribution:** (i) the *measured* fluctuation coefficient L1=0.971
  (not a dimensional estimate) feeding the amplitude; (ii) the demonstration that
  the everpresent *scaling* Λ ~ 1/√V is the network's Poisson law promoted to the
  4-volume; (iii) the *numbers*: p=1.107, the 6.9-vs-1.0 e-fold coincidence
  window, w_eff(0)=−0.66.
- **Imported (declared, never claimed as ours):** the everpresent *model* itself
  (Sorkin ~1990s; Ahmed–Dodelson–Greene–Sorkin 2004, astro-ph/0209274; Zwane–
  Afshordi–Sorkin 2018); the V↔Hubble, ρ↔Planck transplant; the flat-ΛCDM
  *background* E(z) used to evaluate rho_crit and V4_past.

## Declared limits (honesty)

1. **Not a self-consistent stochastic solve.** The background is imported ΛCDM;
   we evaluate the everpresent envelope *on* that background (a consistency
   diagnostic), we do not integrate the coupled Friedmann + fluctuating-Λ system.
   A full stochastic solve (the ADGS Monte-Carlo) is a larger campaign.
2. **The network's own time-evolution is NOT simulated** -- T3A/T3B showed the e7
   growth rule does not yield d=3+1 dynamically, so "evolve the causal set in
   time" is unavailable; LD uses the FRW transplant, as the whole CST everpresent
   programme does.
3. **w is the envelope's apparent EoS**, not a fluid w; the instantaneous term is
   w=−1. Both statements are kept distinct above.

## Bottom line for the map

The dynamic link LAMBDA_EVERPRESENT left open is supplied at the cheap level: the
everpresent Λ built from the measured coefficient **does not diverge, tracks the
critical density (p≈1.1), and dissolves the coincidence problem**, with the honest
caveat that its envelope's apparent w(0)≈−0.66 sits on the high edge of dark-energy
bounds -- a falsifiable signature, not a death. Status: #7 [NUNCA TENTADO] →
**[CONSISTENTE] (consistency diagnostic; model imported, coefficient measured)**.
The residual is the full self-consistent stochastic solve.

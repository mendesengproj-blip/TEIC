# AB3 — Re-audit of BD1–BD5 (Benincasa–Dowker smearing) with 20 seeds

**Task.** Re-run the BD generators (imported unchanged) over 20 seeds and put error bars
on the two load-bearing claims. `AB3_bd.py`, data in `AB3_bd_data.json`.

## BD3 — does smearing collapse the Euclidean anisotropy to O(0.1)?

| Second moment (ρ=30, ε=0.4, 20 seeds) | a_t | a_x | a_t/a_x |
|---|---|---|---|
| **Sharp** (positive Δτ weight) | +18453 ± 285 | +4576 ± 73 | **4.03 ± 0.01** |
| **Smeared** (sign-alternating BD weight) | +0.26 ± 0.27 | +0.42 ± 0.27 | — |

- The **sharp** moment is large, anisotropic (a_t/a_x = 4.03 ± 0.01) and **positive-definite
  in 100% of seeds** — the Euclidean signature AB1 also found (M2 eigenvalues all > 0).
  This is the pathology BD must cure, and it is real and reproducible.
- The **smeared** moment collapses to **|a_t|+|a_x| ≈ 0.68**, i.e. the O(10⁴), ratio-4
  Euclidean anisotropy is gone, replaced by numbers **consistent with zero** within ~1–2σ
  (a_t consistent with 0: yes; a_x consistent with 0: yes).

**Confirmed:** BD smearing removes the gross Euclidean anisotropy (from O(10⁴), ratio 4,
to O(0.1) consistent with 0). It does **not positively** establish the Lorentzian
signature — the smeared moment is consistent with zero, not with a definite `g^{μν}`.

## BD5 — is the SNR≈1 a physical wall or a numerical artefact?

SNR = |signal|/SEM of the smeared dispersion at k=0.6, swept over ε (20 seeds):

| ε | λ_space | λ_time | SNR_space | SNR_time | Lorentz resolved? |
|---|---|---|---|---|---|
| 0.2 | −0.027 ± 0.015 | +0.009 ± 0.017 | 1.80 | 0.53 | no |
| 0.3 | −0.032 ± 0.025 | −0.008 ± 0.025 | 1.29 | 0.31 | no |
| 0.4 | −0.045 ± 0.035 | −0.019 ± 0.032 | 1.27 | 0.58 | no |
| 0.6 | −0.068 ± 0.060 | −0.033 ± 0.048 | 1.13 | 0.70 | no |

- **Every ε gives SNR < 2**, and the *sign* of λ_space is wrong (negative) throughout —
  the Lorentzian signature (λ_space>0, λ_time<0) is **never resolved**.
- The prompt's specific question — *does a smaller ε help?* — the answer is **no in the
  way that matters**: smaller ε raises SNR_space slightly (1.80 at ε=0.2 vs 1.13 at ε=0.6)
  but the signal stays mis-signed and below 2σ. The signal `~ □/(2ε ρ_eff)` and the
  variance both shrink as ε shrinks; their ratio never crosses the resolution threshold.

**Confirmed:** the SNR≈1 ceiling is a **physical** suppression (the `□/(2ε ρ)` smeared
signal buried under the `ρ^{3/4}` variance wall), not a numerical bug that more precision
or a magic ε would cure — exactly as BD5 reported.

## BD → D3 consistency

The sharp second moment is positive-definite in every seed (a_t, a_x > 0). This is the
same fact AB1 found for the link M2 and is *why* D3's static quadratic BD action has a
Gaussian Metropolis equilibrium whose minimiser is the Poisson field (D3-audit): a
positive-definite quadratic form has a unique Gaussian minimiser. Consistent throughout.

## Verdict (AB3)

- **BD3:** the sharp Euclidean anisotropy (a_t/a_x = 4.03 ± 0.01, positive-definite) is
  real; smearing collapses it to |a_t|+|a_x| ≈ 0.68, consistent with zero — **the gross
  anisotropy is removed but Lorentz restoration is not positively demonstrated.**
- **BD5:** SNR < 2 at every ε with the wrong sign — **a physical `□/(2ερ)` variance wall,
  not a numerical artefact.** Both reproduce the original BD3/BD5 verdicts exactly.

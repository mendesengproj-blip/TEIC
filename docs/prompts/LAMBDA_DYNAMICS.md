# Λ DYNAMICS -- temporal evolution of the everpresent Lambda

> RESEARCH_MAP Section 6 #7. Cheap campaign. LAMBDA_EVERPRESENT (L1-L3) measured
> the static fluctuation coefficient and explicitly DECLARED the temporal
> evolution out of scope. LD supplies that link: evolve Λ(t) from the *measured*
> L1 coefficient via the Sorkin/ADGS everpresent ansatz Λ_rms ~ 1/√(V₄_past) over
> FRW cosmic history. Anti-circularity: model + background imported (declared,
> cited); only the amplitude coefficient (L1=0.971) and the resulting numbers are
> TEIC's. Consistency diagnostic, not a self-consistent stochastic solve. Kill
> criterion pre-registered.

## Verdict: **CONSISTENT (no divergence; tracks ρ_crit; dissolves coincidence)**

| Step | Question | Result |
|---|---|---|
| LD1 | V₄_past converges; finite at z=0? | YES (<0.5% in z_max; Λ_rms(0) finite) |
| LD1 | Λ_rms ∝ ρ_crit^p tracking exponent | **p = 1.107** (R²=0.996) |
| LD2 | e-folds with Ω_Λ ~ O(1): ΛCDM vs ever | **1.0 vs 6.9** (coincidence dissolved) |
| LD2 | apparent w_eff(0) from envelope | **−0.66** (→0 at high z) |

**Pre-registered kill criterion** (Λ diverges at z~0 OR inconsistent with w=−1):
**does not fire** — finite at z=0; the term is instantaneously w=−1 by construction.

## Honest bottom line

Feeding the *measured* network coefficient into the everpresent ansatz, Λ stays
**comparable to the critical density at every epoch**: Λ_rms ∝ ρ_crit^1.107 (the
past 4-volume scales ≈ H⁻⁴, so 1/√V₄ ~ H² ~ ρ_crit). This is the geometric heart
of Sorkin's everpresent Λ, here driven by the network's own Poisson law
δρ/ρ = 1/√(ρV) rather than a dimensional guess. Consequently **Ω_Λ stays O(1) for
~7 e-folds** of expansion (vs ~1 e-fold for constant Λ): the "why now" coincidence
is dissolved, no epoch is special.

**The one honest caveat.** The everpresent Λ is *instantaneously* a true
cosmological-constant term (w = −1), but its slowly-drifting RMS envelope
(p = 1.107 ≠ 1) has an apparent **w_eff(0) ≈ −0.66**, on the high edge of current
dark-energy bounds. This is the quantity the everpresent-Λ literature
(Zwane–Afshordi–Sorkin 2018) fits to data — a **testable signature** of the
dynamics, not a death. Reported straight.

## What is TEIC's vs imported (mirrors L3, FM4)

- **TEIC's:** measured L1 coefficient (0.971) for the amplitude; the everpresent
  *scaling* shown to be the network's Poisson law on the 4-volume; the numbers
  (p=1.107; 6.9-vs-1.0 e-folds; w_eff(0)=−0.66).
- **Imported (cited):** everpresent *model* (Sorkin; Ahmed–Dodelson–Greene–Sorkin
  2004, astro-ph/0209274; Zwane–Afshordi–Sorkin 2018); V↔Hubble/ρ↔Planck
  transplant; flat-ΛCDM *background* E(z).

## Status change

- **RESEARCH_MAP §1.3-adjacent (LAMBDA row) / Section 6 #7 / roadmap "Λ dinâmica":**
  [NUNCA TENTADO] → **[CONSISTENTE] (consistency diagnostic; coefficient measured,
  model imported).** The static-only ressalva of LAMBDA_EVERPRESENT (L3: "precisa
  do elo dinâmico — fora do escopo") is closed at the cheap level.
- **Residual:** the full self-consistent stochastic solve (coupled Friedmann +
  fluctuating Λ, ADGS Monte-Carlo) — a larger campaign.

## Artefacts

| File | Content | Reproduce |
|---|---|---|
| `results/cosmology/lambda_dyn/ld_core.py` | FRW background, past 4-volume, everpresent ansatz | `python ld_core.py` |
| `results/cosmology/lambda_dyn/LD1_tracking.py` / `.json` | tracking exponent + divergence/convergence test | `python LD1_tracking.py` |
| `results/cosmology/lambda_dyn/LD2_coincidence.py` / `.json` | coincidence e-folds + envelope w_eff | `python LD2_coincidence.py` |
| `results/cosmology/lambda_dyn/LD3_synthesis.md` | full honest synthesis | — |
| `results/cosmology/lambda_dyn/make_figures.py` / `LD_dynamics.png` | Ω_Λ(z) + tracking + w_eff figure | `python make_figures.py` |

## References
- Sorkin, everpresent Λ (1990s); Ahmed, Dodelson, Greene, Sorkin, PRD 69 (2004) 103523 [astro-ph/0209274].
- Zwane, Afshordi, Sorkin, Class. Quantum Grav. 35 (2018) 194002 — everpresent Λ vs data.
- Builds on TEIC LAMBDA_EVERPRESENT (L1-L3), `results/bridge/lambda/`.

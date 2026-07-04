# KR-PTA -- Direct search for the m_A line in pulsar-timing data

> RESEARCH_MAP Section 6 #10. Cheap, public-data campaign. HQ3 established only
> *theoretical* consistency (the m_A Khmelnitsky-Rubakov line lands in the PTA
> band; amplitude "grazes the threshold"). KR-PTA confronts that prediction with
> the PTAs' **published direct searches** -- has the line been looked for and
> excluded? Anti-circularity: m_A window from Paper II/FM4 (SPARC), not tuned to
> PTA; KR model and PTA limits taken from the literature with references; this is
> a TEST, kill criterion pre-registered (KR2).

## Verdict: **CONSISTENT (not excluded) -- the line is below current PTA reach**

| Step | Question | Result |
|---|---|---|
| KR1 | m_A KR line in the PTA band? | YES, m_A ~ 6e-24..1.2e-22 eV (f = 3e-9..6e-8 Hz) |
| KR1 | h_c, residual at m=1e-23 eV (f=1) | h_c ≈ 2.7e-15; δt ≈ 25 ns (KR Eq 21) |
| KR2 | published grav. search excludes 100% DM in window? | **NO** (f_max = 2.5 → 2160) |
| KR2 | PPTA reaches f_max=1 at... | m ~ 2.6e-24 eV, **below** the window low edge |
| KR2 | Lyman-α forces m_A subdominant in band? | YES (needs m ≳ 1e-21 eV for 100% DM) |

**Pre-registered kill criterion** (PTA grav. search excludes f=1 across the whole
window AND m_A required ~100% DM there): **does not fire.**

## Honest bottom line

The cleanest published gravitational (Khmelnitsky-Rubakov) direct search,
**PPTA-2018** (Porayko et al., arXiv:1810.03227), limits the local ULDM density to
ρ < 6 GeV/cm³ (95 %) at m ≤ 1e-23 eV — a fraction limit **f_max ≈ 15**, i.e. it
does not exclude even 100 % local-DM ULDM there. Because the KR strain ∝ ρ/m²,
the limit reaches f_max = 1 only near **m ~ 2.6e-24 eV, just below the HQ3 overlap
window**; across the whole window the published search allows the maximal line.
NANOGrav-15yr (arXiv:2306.16219) ran the same gravitational search and also found
nothing, improving the reach only modestly.

Independently, **fuzzy-DM structure bounds (Lyman-α / high-z) require m ≳ 1e-21 eV
for ULDM to be ~100 % of DM** — two decades above the PTA band — so in the PTA
band m_A is necessarily subdominant (FM4's "Lyman → subdominante"), and its KR
line sits far below current PTA sensitivity. The non-detection is exactly what the
m_A picture predicts: **no tension, no detection, no exclusion.**

This upgrades HQ3 from "consistent in principle (grazes the threshold)" to
**"confronted with the actual direct searches: not excluded, below threshold; PTA
is a genuine FUTURE probe of the high-mass tail of the m_A window."**

### Declared limits
- No bespoke matched-filter line search on raw residuals (uses the collaborations'
  published exclusion curves; a dedicated search is a larger campaign and is not
  needed for falsification). This is the one residual left open.
- PPTA limit extrapolated by a single white-noise scaling (ρ_lim ∝ m²) from the
  quoted benchmark; at the low-mass edge (f < 1/T_span) the true sensitivity is
  *worse*, so the CONSISTENT verdict is conservative (real limits are weaker).
- ρ_local = 0.4 GeV/cm³ (KR Eq 21 normalised to 0.3, carried explicitly).

## Status change

- **RESEARCH_MAP HQ3 row / Section 6 #10:** the "busca direta nos dados PTA NUNCA
  feita" residual is **closed at the level public data allow** → KR-PTA executed,
  verdict CONSISTENT. HQ3's [FRACO]/[IDENTIFICADO] status is unchanged in kind,
  sharpened: the m_A line is not excluded and is predicted undetectable now.

## Artefacts

| File | Content | Reproduce |
|---|---|---|
| `results/cosmology/kr_pta/kr_pta_core.py` | KR signal model + PTA limit benchmark | `python kr_pta_core.py` |
| `results/cosmology/kr_pta/KR1_signal.py` / `.json` | m_A line across the band | `python KR1_signal.py` |
| `results/cosmology/kr_pta/KR2_confront.py` / `.json` | confrontation + kill criterion | `python KR2_confront.py` |
| `results/cosmology/kr_pta/KR3_synthesis.md` | full honest synthesis | — |
| `results/cosmology/kr_pta/make_figures.py` / `KR_pta.png` | strain + fraction-limit figure | `python make_figures.py` |

## References
- Khmelnitsky & Rubakov, JCAP 02 (2014) 019 [arXiv:1309.5888] — KR signal, Eqs 12/21/22.
- Porayko et al. (PPTA), PRD 98 (2018) 102002 [arXiv:1810.03227] — gravitational limit benchmark.
- NANOGrav 15yr, [arXiv:2306.16219] — search for new physics (gravitational ULDM).

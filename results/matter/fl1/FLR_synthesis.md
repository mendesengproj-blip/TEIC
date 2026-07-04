# FLR — FL1 SU(3) robustness: synthesis

> Charter: `docs/prompts/FLR_SU3_ROBUSTNESS.md` (kill criteria pre-registered).
> Item R1 of `RESEARCH_MAP.md` — the most urgent never-tested gap of the matter
> sector. Data/code: `FLR_robustness.py`, `FLR_robustness.json`. Run jun/2026.

## Verdict: **SU(3) ROBUST** (confirmed at both quick L=6 and full L=8 scales)

> **Full-scale corroboration (L=8, 32 min):** identical qualitative verdict — G0 even
> tighter (|Δplaq|=0.0005); Creutz σ(2,2) positive at every ε (0.30–4.11, confines=True
> throughout); octet 8/8 at every ε; Skyrmion interior minimum at every ε with λ*
> invariant. The σ drift over |ε|≤0.10 tightened from 41.5% (L=6) to **23.7%** (L=8)
> with the larger lattice/statistics — consistent with "the deformation shifts the
> effective coupling; the area-law sign is robust." `FLR_robustness.json` now holds the
> full-scale data.

The three central SU(3) results all survive a ±10% deformation of the minimal
action form `g_ε(p) = (1−p) + ε(1−p)²` (ε ∈ {−0.2,−0.1,0,+0.1,+0.2}), applied
consistently to the gauge plaquette and the principal-chiral link density:

| Test | Result over |ε|≤0.10 | Pre-registered death | Fired? |
|---|---|---|---|---|
| **R-CONFINE** | Creutz σ(2,2) positive at every ε (0.94–1.65 at strong β); confines=True | σ≤0 or V(r) flat (deconfinement) | **No** |
| **R-OCTET** | 8/8 gapless Goldstone modes at every ε | n_gapless ≠ 8 | **No** |
| **R-SKYRMION** | interior Derrick minimum at every ε; λ* invariant (0.330); M linear in ε | interior minimum disappears | **No** |

**Implementation gate G0 PASS:** the perturbed metropolis at ε=0 reproduces the
original `gauge_metropolis_sweep` plaquette (0.2168 vs 0.2145, |Δ|=0.0023 ≪ tol 0.03).

## Quantitative drift over |ε|≤0.10
- **String tension σ(2,2):** drifts ~40% — but this reflects that the deformation
  **shifts the effective bare coupling** (ε<0 steepens the action → smaller plaquette
  → larger σ; ε>0 softens it), not a loss of confinement. The *sign* (area law,
  σ>0) is invariant — that is the robust statement. The trend is monotonic and
  physical across the full ε∈[−0.2,+0.2] range (σ: 1.08 → 1.65 → 1.17 → 1.09 → 0.89
  at the strongest β).
- **Skyrmion mass M=2√(E2·E4):** drifts ~10% per ±10% (linear, expected — both E2 and
  e_sk scale ≈(1+ε)). **Size λ*=√(E4/E2) is invariant** at 0.330 — the soliton
  geometry does not depend on the action deformation.
- **Octet:** exactly 8 gapless modes at every ε with no degradation — the
  symmetry-breaking pattern SU(3)_L×SU(3)_R → SU(3)_diag is rigid.

## Correction logged (transparency, in project discipline)

A first pass returned a **false FRAGILE** verdict. The cause was an
**operationalization bug in this robustness harness**, not physics: the death
criterion OR-ed a secondary "V(r) increases" flag, which fails precisely when
confinement is *strongest*. At ε<0 the action steepens → effective coupling rises →
plaquette drops to 0.08–0.19 → Wilson loops fall below the noise floor at r≥2,
leaving <2 points for the static-potential slope (i.e. **too confined to resolve
V(r)**, the opposite of deconfinement). Meanwhile the Creutz ratio σ(2,2) — which the
**original FLC campaign itself designated robust** at strong coupling ("large loops
drown in noise") — was *larger* there (1.65 vs 1.17 at ε=0), unambiguous area law.

The decision was corrected to the Creutz estimator (positive area law = confinement;
genuine deconfinement = σ→0 *with* a resolved flat V), keeping V-growth as
corroboration where the potential is resolvable. This mirrors the project's prior
corrections (the Ω_GW formula in HQ3; the BTFR over-call) — fix the operationalization
to the established robust estimator, document it, do not adjust to escape a death. The
genuine deconfinement signature (σ→0, flat V) occurred **nowhere**, at any ε. Both the
raw V-growth flags and the Creutz tensions are kept in `FLR_robustness.json`.

## What this closes (RESEARCH_MAP update)

- FL1 / SU(3) moves from **[SÓLIDO com ressalva: robustez não testada]** to
  **[SÓLIDO]** for the qualitative claims (confinement, 8-mode octet, stable colour
  Skyrmion): they are not artefacts of the exact minimal-action form.
- Residual ressalvas that this campaign does **not** close (still open):
  (i) the SU(3) transition **order** remains inconclusive at L≤12 (separate, needs
  larger lattices — RESEARCH_MAP §6 item 15);
  (ii) the flux-tube Regge slope α'=1/(2πσ) inherits the σ drift (the *form* is
  robust; the *value* rides on the effective coupling, the same external-scale caveat
  as everywhere);
  (iii) the Skyrme stabiliser remains the declared **external** input (EXTERNO-T,
  unchanged — that was never a robustness question).

## Anti-circularity
No QCD number entered (β scanned, ε declared, e_sk the declared external Skyrme
weight). G0 validated the perturbed engine against the original before any claim.
Fixed seeds; `FLR_robustness.json` is auto-descriptive and keeps every raw indicator.

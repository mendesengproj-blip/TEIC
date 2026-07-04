# OCTET_SPECTROSCOPY — Quantitative Spectroscopy of the SU(3) Meson Octet

> Charter (pre-registered BEFORE running). Item **#11** of `RESEARCH_MAP.md`
> Seção 6 ("Espectroscopia quantitativa do octeto", FL1-D follow-up; urgência
> BAIXA, dificuldade MÉDIA, pré-requisito `su3_core`). This is the quantitative
> upgrade of FL1 Phase D2, which established **8/8 Goldstone modes gapless**
> *qualitatively* but left one number unexplained: a ~10% spread between the
> off-diagonal generators (`dE/k² ≈ 3545–3849`) and `λ8` (`≈ 4000`).
>
> Reuses the FL1 engine `results/matter/fl1/su3_core.py` (Gell-Mann generators,
> chiral energy, causal substrate). Generator:
> `results/matter/fl1/OS_octet_spectroscopy.py`. No new QCD number enters; the
> octet is the Goldstone sector of the measured SU(3) vacuum.

## Question

The ordered SU(3) vacuum (FL1 Phase B) breaks `SU(3)_L × SU(3)_R → SU(3)_diag`,
leaving 8 Goldstone bosons. The unbroken **SU(3)_V acts on them as the adjoint
(octet) — an irreducible representation.** The only SU(3)_V-invariant rank-2
tensor on the broken directions is the Killing metric `∝ δ_ab`, so the stiffness
tensor `ρ_s,ab = ρ_s δ_ab` is forced: **all 8 modes must be exactly degenerate,
with a single stiffness ρ_s and a single speed c.** Quantitative questions:

1. Is the octet **exactly degenerate** (single ρ_s), as the unbroken symmetry
   demands — or do the 8 modes genuinely split?
2. What is the **numerical value** of the octet stiffness ρ_s, the dispersion
   ω(k), and the small-k speed c (in lattice units)?
3. What was the **D2 ~10% spread** — physical splitting, or a measurement
   artifact?

## Pre-registered predictions (theory, derived BEFORE measuring)

- **P1 (exact degeneracy).** Linearising `E = −J Σ (1/3)Re Tr(U_i U_j†)` around
  the ordered vacuum gives `E_quad = (J/3) Σ_<ij> Σ_a (φ_i^a − φ_j^a)²` — the 8
  generators **decouple into 8 identical graph-Laplacian quadratic forms**. The
  harmonic stiffness is therefore generator-independent to machine precision, on
  *any* substrate (cubic or causal). The octet is exactly degenerate at tree level.
- **P2 (universal static stiffness).** A uniform single-generator helical twist
  `U_i = exp(i k·x_i λ_a) U_0` costs `1 − (1/3)Re Tr(exp(i k λ_a))` per link.
  Pre-computed exactly: `dE/k² = 1/3 − k²/36 + O(k⁴)`, **identical for every
  generator** (root = Cartan to ≥ k⁴). One octet stiffness, no splitting.
- **P3 (D2 anomaly = torus seam).** The D2 protocol applies the twist on a
  **periodic** L³ torus. A diagonal (Cartan) twist closes on the torus only if
  `exp(−2πi n λ_a) = I`. For roots and `λ3` (integer eigenvalues) it does; for
  **`λ8` (eigenvalues ±1/√3, −2/√3 — irrational) it does NOT** (`|exp−I| = 1.94`),
  leaving a boundary seam that inflates its measured stiffness. Removing the seam
  (open boundary along the twist axis) must collapse all 8 onto a single value.

## Kill criteria (pre-registered)

```
OS1 dies if: the 8 harmonic stiffnesses are NOT equal within numerical tolerance
  (relative spread > 1e-6) on the cubic lattice -- would mean the ordered vacuum
  does not realise the SU(3)_V octet (a bug, or the symmetry is not SU(3)_V).

OS2 dies if: the seam-free static stiffness has no finite k->0 limit -- either a
  GAP (dE/k^2 -> infinity) or no stiffness (dE/k^2 -> 0) -- contradicting a
  linearly-dispersing gapless Goldstone octet.

OS3 dies if: after removing the torus seam (open boundary), the generator-to-
  generator spread of the static stiffness REMAINS > 1%.  Then the D2 anomaly is
  physical splitting, not an artifact, and the "single octet" claim needs revision.
```

Each task reports its kill check as a result, pass or fail, with no tuning after
the fact. Verdicts are filled ONLY after the run (project rule).

## Tasks

- **OS1 — Harmonic degeneracy theorem (deterministic).** Perturb the ordered
  vacuum by a small single-generator pattern `φ_i^a = ε ψ_i` (same spatial ψ for
  every generator a); measure `ΔE/ε²` per generator, on the cubic lattice AND on
  the Poisson causal substrate. Verify the 8 values coincide (P1) and equal the
  graph-Laplacian quadratic form. Output: per-generator stiffness, max relative
  spread.
- **OS2 — Quantitative spectrum (cubic anchor).** Seam-free helical-twist
  stiffness `dE/k²` over a k-grid → octet stiffness ρ_s (k→0) and the `−k²/36`
  shape (P2). Magnon dispersion `ω(k)=√((2J/3)·μ(k))` along Γ→X→M, small-k speed
  c, and isotropy (axis vs face-diagonal). The causal-substrate dispersion *shape*
  is inherited from the single-scalar magnon (E2) — cited, not re-derived; the
  octet-specific causal claim (degeneracy) is OS1.
- **OS3 — D2 reconciliation.** (a) Reproduce the D2 periodic-torus protocol →
  recover the λ8 outlier. (b) Diagnose: per-generator torus-closure defect
  `|exp(−2πi n λ_a) − I|`. (c) Fix: open boundary along the twist axis → all 8
  collapse. Pre-registered: seam-free spread < 1% (P3).

## Anti-circularity

`su3_core` is reused unchanged; no fit target. The octet stiffness and dispersion
are MEASURED; the predictions P1–P3 are derived from group theory + the cosine
action alone, before the run. No QCD number enters. Lattice units throughout
(scale not derived — same caveat as all of FL1). Determinístico (fixed seeds).

*Reprodução:* `python results/matter/fl1/OS_octet_spectroscopy.py`.

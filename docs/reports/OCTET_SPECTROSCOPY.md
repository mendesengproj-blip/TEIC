# OCTET_SPECTROSCOPY — Quantitative Spectrum of the SU(3) Meson Octet

> Item **#11** of `RESEARCH_MAP.md` Seção 6 (FL1-D follow-up; urgência BAIXA,
> dificuldade MÉDIA, pré-requisito `su3_core`). Charter (pre-registered):
> [`docs/prompts/OCTET_SPECTROSCOPY.md`](docs/prompts/OCTET_SPECTROSCOPY.md).
> Generator + data: `results/matter/fl1/OS_octet_spectroscopy.{py,json,png}`.
> Engine reused unchanged: `results/matter/fl1/su3_core.py`. Lattice units; no QCD
> number enters. Deterministic (fixed seeds), numpy 2.4.4 / scipy 1.17.1.

## ✅ VEREDITO: **OCTET SPECTROSCOPY COMPLETE — single exactly-degenerate octet; D2 anomaly resolved**

The 8 Goldstone bosons of the ordered SU(3) vacuum form **one exactly degenerate
octet** of the unbroken SU(3)_V — a single stiffness ρ_s, a single linear isotropic
dispersion ω = c|k|, gapless. The ~10% root-vs-λ8 spread that FL1 Phase D2 reported
qualitatively is **not physical**: it is a torus-closure seam of the single diagonal
generator λ8 (irrational Cartan eigenvalues), and vanishes when the seam is removed.

| Task | Question | Result | Kill? | Verdict |
|---|---|---|---|---|
| **OS1** | Is the octet exactly degenerate (harmonic)? | 8 generators decouple into **identical** (J/3)·graph-Laplacian forms; per-generator spread **4.3×10⁻⁸ (cubic)**, **4.5×10⁻⁸ (causal)**; form-match 2.9×10⁻⁸ | no | **PASS** — exact degeneracy on cubic AND causal substrate (P1) |
| **OS2** | What is ρ_s, ω(k), c? | ρ_s(per link) = **0.3326 ≈ 1/3**, curvature **−0.0256 ≈ −1/36**; gapless ω(Γ)=0; **c = √(2/3) = 0.8165**; isotropy 2×10⁻⁶ | no | **PASS** — single octet stiffness, linear isotropic gapless dispersion (P2) |
| **OS3** | Was the D2 spread physical? | D2 torus: spread 1.82, **λ8/others = 2.82×**; closure defect **λ8 = 1.94 vs 0** for all others; open-BC fix → spread **9.2×10⁻⁶** | no | **PASS** — D2 anomaly = λ8 torus seam; not splitting (P3) |

---

## The central result (P1): the octet is exactly degenerate

Linearising the chiral energy `E = −J Σ_<ij> (1/3) Re Tr(U_i U_j†)` around the ordered
vacuum gives
```
E_quad = (J/3) Σ_<ij> Σ_a (φ_i^a − φ_j^a)²
```
— the 8 broken generators **decouple into 8 identical graph-Laplacian quadratic
forms**. This is the rigorous content of FL1-D2's "8/8 gapless": the unbroken SU(3)_V
acts on the Goldstones as the adjoint (octet), an *irreducible* representation, so the
only invariant rank-2 stiffness tensor is `ρ_s δ_ab` — a **single** stiffness, forced
by symmetry. Measured per-generator spread is at machine precision (4×10⁻⁸) on **both**
the cubic lattice and the Poisson causal substrate, and the harmonic stiffness matches
`(J/3)·graph-Laplacian` to 3×10⁻⁸. The octet degeneracy is therefore exact and
substrate-independent, not an approximate "8/8 found".

## The quantitative spectrum (P2)

A uniform single-generator helical twist `U_i = exp(i k·x_i λ_a) U_0` costs, per link,
`1 − (1/3) Re Tr(exp(i k λ_a)) = (k²/3)(1 − k²/12 + …)`, **identical for every
generator** (root = Cartan, verified to ≥ k⁴ analytically and on the lattice). The
seam-free fit gives the octet stiffness `ρ_s(per link) = 0.3326 ≈ 1/3` with curvature
`−0.0256 ≈ −1/36` (the continuum shape). The magnon dispersion
`ω(k) = √((2J/3) μ(k))` is gapless at Γ, linear at small k with speed `c = √(2/3) =
0.8165` (lattice units), and isotropic to 2×10⁻⁶ (axis vs face-diagonal). The octet
dispersion is 8 identical copies of this single branch; the *causal-substrate* shape is
the single-scalar magnon question already settled in E2 (cited, not re-derived) — the
octet-specific causal claim is the degeneracy (OS1).

## The D2 reconciliation (P3): the λ8 torus seam

FL1-D2 applied the twist on a **periodic** L³ torus. A diagonal (Cartan) twist closes
on the torus only if `exp(−2πi n λ_a) = I`. Roots and λ3 (integer eigenvalues) close
exactly; **λ8 (eigenvalues ±1/√3, −2/√3 — irrational) does not** (`|exp − I| = 1.94`),
leaving a boundary seam that inflates its measured stiffness by **2.8×**. This is the
entire D2 anomaly: at fixed k the other 7 generators are identical to the digit, and
only λ8 is the outlier. Removing the seam (open boundary along the twist axis, bulk
links only) collapses all 8 onto a single value to **9.2×10⁻⁶**. The D2 spread was a
torus-closure artifact of one diagonal generator, **not** a physical splitting of the
octet.

---

## Honest bottom line

- **What is new (quantitative upgrade over FL1-D2):** the octet is proven **exactly
  degenerate** (single ρ_s) by harmonic decoupling, on cubic *and* causal substrates;
  the stiffness ρ_s ≈ 1/3 (per link) and speed c = √(2/3) are measured; and the one
  unexplained number in D2 (the ~10% λ8 spread) is diagnosed and removed as a
  torus-closure seam. FL1-D2 goes from "8/8 gapless (qualitative, 10% unexplained)" to
  "single exactly-degenerate octet, spectrum measured, anomaly resolved".
- **What is unchanged / external (declared):** the overall lattice→GeV scale is **not
  derived** (same caveat as all of FL1) — ρ_s, c are in lattice units. The chiral limit
  is exact here (massless octet); explicit quark-mass splitting (π vs K vs η) is **not**
  in this model (it requires an external symmetry-breaking term, not present). The
  causal-substrate *dispersion shape* (ω∝k vs the non-locality issues) is inherited from
  E2, not re-established here — only the degeneracy is shown on the causal graph.
- **No kill triggered.** All three pre-registered predictions (P1 exact degeneracy, P2
  universal stiffness, P3 D2 = seam) confirmed.

## Artefacts (reproduce)

| File | Content | Reproduce |
|---|---|---|
| `docs/prompts/OCTET_SPECTROSCOPY.md` | charter (pre-registered predictions + kill criteria) | — |
| `results/matter/fl1/OS_octet_spectroscopy.py` | generator (OS1/OS2/OS3) | `python results/matter/fl1/OS_octet_spectroscopy.py` |
| `results/matter/fl1/OS_octet_spectroscopy.json` | all measured numbers | (written by the run) |
| `results/matter/fl1/OS_octet_spectroscopy.png` | octet collapse + dispersion | `python results/matter/fl1/OS_make_figures.py` |

*Anti-circularity:* `su3_core` reused unchanged, no fit target; predictions P1–P3
derived from group theory + the cosine action before the run; `tests/test_no_circularity.py`
green. Lattice units throughout.

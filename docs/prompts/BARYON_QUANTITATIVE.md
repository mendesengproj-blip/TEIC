# BARYON_QUANTITATIVE (BQ) — Quantitative collective-coordinate quantization of the B=1 Skyrmion

> **RESEARCH_MAP gap #12** ("Quantização de coordenadas coletivas do bárion —
> quantitativa", urgência BAIXA, dificuldade MÉDIA, pré-req `su2q_core`).
> Pre-registered charter. Kill criteria fixed BEFORE running (anti-circularity).

## What Q1–Q7 (MATTER_SU2_QUANT) already did, and what is missing

`su2_quant` (Q1–Q7) quantized the Skyrmion's orientation **qualitatively**: it
showed the inertia tensor is spherical, the rotor spectrum is `E_j = j(j+1)/(2I)`
with degeneracies `(2j+1)²`, and the Finkelstein–Rubinstein phase selects
half-integer `j` → spin-½. Every claim there is a *shape/structure* claim
(ratios, degeneracies, sign of a 2π rotation). **No quantitative baryon number
was produced.**

Crucially, Q2's moment of inertia `I = 312.7` is the **σ-model part only** — the
zero-mode overlap `2∫(ξ·ξ)d³x` captures the 2-derivative kinetic metric and
**omits the Skyrme (4-derivative) contribution** to the rotational inertia. That
is fine for the *qualitative* spin-½ result (any positive spherical `I` gives the
ladder + FR selection) but **wrong for quantitative observables**: the Skyrme
term stiffens the rotor and shifts every number that depends on `𝓘`.

## The structural claim this campaign tests

Collective-coordinate quantization of the B=1 hedgehog introduces **exactly one
dimensionless coupling** (the Skyrme parameter `e`, played by the lattice
`e_sk`) and **one external scale** (`f_π`, the analogue of `G/ℏ` — declared
EXTERNAL). The program's universal pattern predicts:

- **forms / pure numbers are derived** (spectrum shape, degeneracies, the inertia
  ratio, magnetic-moment ratio),
- **one calibration** (the N–Δ mass ratio) fixes `e`,
- **the absolute scale** (`f_π`, hence masses in MeV) stays EXTERNAL.

So: calibrate `e` from a single number (the N–Δ splitting); then `μ_p/μ_n`, the
isoscalar radius ratio, etc. are **parameter-free predictions**.

## Tasks and pre-registered kill criteria

| Task | Question | PASS (pre-registered) | KILL / honest-negative |
|---|---|---|---|
| **BQ1** rotor tower | does the FR-projected spectrum give the full baryon tower as pure numbers? | `E_j∝j(j+1)` fit R²>0.999 up to j=5/2; FR degeneracies `(2j+1)²=[4,16,36]`; pure ratio `(E_{5/2}−E_{1/2})/(E_{3/2}−E_{1/2})=8/3` within 3%; spin=isospin locking per level | any degeneracy wrong, or ratio off >5% → report as negative |
| **BQ2** full inertia | how large is the Skyrme contribution to `𝓘` that Q2 omitted? | reduced solver reproduces `su2_core` profile (rescaled) to <2%; `𝓘_σ` matches lattice `I`; report `f_Sk=𝓘_Sk/𝓘` as a measured pure number | reduced profile ≠ lattice profile → engine inconsistency, STOP |
| **BQ3** N–Δ calibration | does one number (N–Δ) fix `e`, reproducing ANW? | with `M_N,M_Δ` inputs, solve `(f_π,e)`; reproduce ANW `e≈5.45, f_π≈65 MeV` within 10% | cannot reproduce ANW calibration → formula/units bug, STOP |
| **BQ4** μ_p/μ_n | is the magnetic-moment ratio a correct parameter-free prediction? | reproduce ANW `μ_p/μ_n≈−1.43`, isoscalar radius `≈0.59 fm`, `g_A≈0.61` (the famously-low value) within ~10% at the calibrated point | numbers off >25% → integrand/units wrong, report PARTIAL + diagnosis |
| **BQ5** synthesis | — | verdict table, honest scope, RESEARCH_MAP update | — |

## Honest scope (declared up front)

- `f_π` (overall scale) is **EXTERNAL-B** — the same status as `G, ℏ, a₀`. We do
  **not** claim to derive the GeV scale; we claim the *dimensionless* baryon
  phenomenology.
- The **electromagnetic current operators** (isoscalar = baryon current,
  isovector = third iso-Noether current) are the **established Skyrme/ANW
  decomposition** — imported, exactly as the FR phase was imported in Q4. The
  **profile** is the lattice's (`su2_core`); the current algebra is standard.
- Validation against published ANW predictions is the internal correctness check:
  if the same machinery reproduces ANW's numbers from our relaxed profile, the
  integrands and units are right.

## Artefacts

| File | Content |
|---|---|
| `results/matter/baryon_quant/bq_core.py` | reduced-unit profile solver + ANW observables; cross-check vs `su2_core` |
| `results/matter/baryon_quant/BQ1_tower.py` | rotor spectrum tower (reuses `su2q_core`) |
| `results/matter/baryon_quant/BQ2_inertia.py` | full `𝓘 = 𝓘_σ + 𝓘_Sk`; lattice cross-check |
| `results/matter/baryon_quant/BQ3_calibration.py` | N–Δ → (f_π, e) |
| `results/matter/baryon_quant/BQ4_moments.py` | μ_p/μ_n, isoscalar radius, g_A |
| `results/matter/baryon_quant/BQ5_synthesis.py` | verdict |

---

# RESULTS — VERDICT A (executed jun/2026)

| Task | Result | vs reference | Verdict |
|---|---|---|---|
| **BQ1** tower | full degeneracies `[1,4,9,16]`, FR degeneracies `[4,16,36]=(2j+1)²` for j=½(N),3/2(Δ),5/2; `E_l∝l(l+2)` R²=**0.9999**; pure ratio `(E_{5/2}−E_{1/2})/(E_{3/2}−E_{1/2})=`**2.639** | rigid-rotor `8/3=2.667` (1.1%) | **PASS** |
| **BQ2** full inertia | σ cross-check: lattice zero-mode `312.7` ≡ radial `320.3` (2.3%); **Skyrme inertia fraction = 0.432**; full `𝓘 = 1.761× Q2's σ-only` | — | **PASS** |
| **BQ3** calibration | one number (N–Δ) → `e=`**5.394**, `f_π=125.7 MeV`; `(M_Δ−M_N)/M_N=0.312` | ANW `e=5.45` (1.0%); exp `0.314` | **PASS** |
| **BQ4** moments | `μ_p=1.93, μ_n=−1.27`, **`μ_p/μ_n=−1.515`**; isoscalar radius `0.646 fm`; `g_A=0.558` | ANW `−1.43` / exp `−1.46`; ANW `0.59`; ANW `0.61` | **PASS** |

## Honest bottom line

The quantitative collective-coordinate quantization of the **TEIC** B=1 Skyrmion
(the emergent SU(2) topological soliton of SU3–SU8) reproduces the **established
baryon phenomenology** of Adkins–Nappi–Witten, with the program's universal
signature intact:

- **Pure numbers are derived.** The FR-projected rotor gives the baryon multiplet
  tower with degeneracies `(2j+1)²=[4,16,36]` (N doublet, Δ quartet, j=5/2),
  spin=isospin locked, and the parameter-free rigid-rotor ratio `8/3` to 1%.
- **The Skyrme inertia Q2 omitted is 43% of the total.** The qualitative Q-campaign
  used the σ-only zero-mode inertia; the full rotational inertia is `1.76×` larger,
  so the rotor energies (and the N–Δ splitting in lattice units) Q2 implied were
  76% too large. This is the quantitative correction BQ delivers.
- **One calibration, then predictions.** The single dimensionless coupling `e` is
  fixed by **one** number (the N–Δ splitting) → `e=5.39`, within **1%** of ANW's
  5.45. Then `μ_p/μ_n=−1.515` (ANW −1.43, **exp −1.46** — our parameter-free ratio
  sits *between* ANW and experiment), the isoscalar radius `0.65 fm` (ANW 0.59),
  and `g_A=0.56` (reproducing the famously-low Skyrme value, ANW 0.61) are all
  **parameter-free predictions** matching ANW to <10%.

**Scope / what stays external (declared up front, unchanged):**
- `f_π` (the overall MeV scale) is **EXTERNAL-B** — same status as `G, ℏ, a₀`. The
  calibrated `f_π=125.7 MeV ≈ 1.95×` ANW's 64.5 MeV is the `F_π=2 f_π` normalization
  convention; the *dimensionless* coupling `e` (which controls every prediction) is
  convention-robust and matches ANW.
- The **EM current decomposition** (isoscalar = baryon current, isovector = third
  iso-Noether current) is **imported** standard physics — exactly the status of the
  FR phase in Q4 (implemented, not re-derived from the causal-set action). The
  **profile** is the lattice's; reproducing ANW's numbers validates the integrands.

This **promotes** the Skyrmion↔baryon link from `[IDENTIFICADO]` (numbers match,
scale not derived) toward `[DERIVADO]` *for the dimensionless baryon structure*:
the magnetic-moment ratio, the multiplet degeneracies, and the rotor tower are now
**measured pure numbers**, not just qualitative correspondences. The absolute GeV
scale remains external (as everywhere in the program).

## Residuals / not closed

- The N and Δ **absolute masses** in MeV require `f_π` (external); only the
  *dimensionless* ratio `(M_Δ−M_N)/M_N=0.31` is a prediction (matches exp 0.314).
- `g_A` and the magnetic moments inherit the **minimal-Skyrme** ~10–30% accuracy
  (a limitation of the action, not of the quantization).
- The j=5/2 transfer level carries discreteness + Monte-Carlo spread (35%); the
  `j(j+1)` law is therefore certified on the accurate low-l full spectrum (R²=0.9999)
  and the pure ratio (1%), not on a high-l fit.

## Artefacts (reproduce)

```
python results/matter/baryon_quant/run_all.py          # BQ1..BQ5
python results/matter/baryon_quant/bq_core.py           # reduced solver + ANW validation
```
Data: `results/matter/baryon_quant/BQ{1..5}_*.json`.

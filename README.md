# Theory of Expanding Informational Causality (TEIC)

A research programme testing whether the physics we observe — special relativity,
gravitation, matter, and their cross-relations — can **emerge by measurement** from a
single discrete substrate: a Poisson sprinkling of events carrying their causal order
(a *causal set*), equipped with one internal orientation field. Every data-generating
module runs under an **anti-circularity guard** that forbids inserting any relativistic
or quantum expression into the code; relativity, when it appears, is an *output* of
counting on the network, never an input.

The programme is deliberately honest: kill criteria are pre-registered before each
campaign, negatives are reported as negatives, and each claim is tagged
**[Derived]** (measured under the guard), **[Identified]** (matched to a known object
by quantum numbers, not absolute scale), or **[External]** (an input, declared rather
than hidden).

## Status

| Paper (`paper/submission/`) | Topic | Venue | Status |
|---|---|---|---|
| `btfr_mnras` | Redshift evolution of the baryonic Tully–Fisher relation (pre-registered test of a₀ ∝ H(z)) | MNRAS | **Submitted — under review** (do not modify) |
| `goldstone_prd` | Spontaneous orientational order + relativistic scalar Goldstone modes (photon = Goldstone excluded by measurement) | Phys. Rev. D | Submission-ready |
| `matter_gravity_prd` | Topological matter (SU(2) Skyrmion) + emergent Newtonian gravity; a soliton that sources its own field | Phys. Rev. D | Submission-ready |
| `su3_prd` | SU(3) colour ferromagnetism: confinement, the meson octet, and the order of the transition | Phys. Rev. D | Submission-ready |
| `photon_arc_cqg` | Indefinite-signature BD gauge operator (new to CST) + divergent-valency proposition + the obstruction map for an emergent photon | Gen. Relativ. Gravit. | **Submitted — under review** (do not modify) |
| `ferromagneto_prl` | Dimensionless structure across four domains: forms derive, absolute scales do not | Phys. Rev. Lett. | Submission-ready |

Each folder is self-contained (`.tex` + bibliography + figures + cover letter) and
compiles with `pdflatex → bibtex → pdflatex ×2`.

## What we found

- **[Derived]** Special relativity and Schwarzschild dilation emerge from chain/volume
  counting on the network, with no dilation formula in the generator (R1–R3; SR corr
  0.9998–1.0000, Schwarzschild to 0.21%). These reproduce **causal set theory** and we
  claim no novelty for them.
- **[Derived]** The orientation field spontaneously orders, genuinely (finite-size
  scaling: order parameter rises with N, Binder cumulant U₄ = 2/3 throughout), and its
  Goldstone modes disperse relativistically through the causal wave operator
  (`PAPER_GOLDSTONE_PRD`).
- **[Derived]** A localised source in the causal-density field relaxes to a Newtonian
  1/r potential obeying a linear Poisson law for every source shape; the soliton's
  **own** energy-density profile, fed into the relaxer, sources that field with exterior
  exponent −0.992 and coupling constant to five digits (`PAPER_MATTER_GRAVITY`).
- **[Derived]** Stable point-like matter forces the internal group to SU(2) by
  elimination; the resulting Skyrmion is a B = 1, spin-½ fermion with measured exchange
  statistics, and — after a single N–Δ calibration — reproduces the **dimensionless**
  baryon phenomenology (μ_p/μ_n, radius, multiplet degeneracies) parameter-free
  (`PAPER_MATTER_GRAVITY`).
- **[Derived]** An SU(3) field on the same substrate orders into a **colour
  ferromagnet** with genuine long-range order, a stable colour Skyrmion
  (π₃(SU(3)) = ℤ, B = +1), a linearly confining static potential (σ > 0 from the
  Creutz ratio), and the eight Goldstone modes forming **one exactly degenerate
  pseudoscalar octet** — forced by the unbroken SU(3)_V, not postulated (`su3_prd`).
- **[Structural]** Across four domains that were not built to agree (gravity, baryon +
  colour, deep-MOND, collapse), the substrate fixes **forms and dimensionless ratios**
  but never the lattice→SI conversion: G, ℏ, a₀, f_π each need exactly one external
  calibration, and the cheapest transmutation mechanism is measurably absent — the
  substrate is mean-field, with a structural reason (`ferromagneto_prl`).
- **[External]** A pre-registered, parameter-free prediction for the redshift evolution
  of the baryonic Tully–Fisher relation, a₀ ∝ H(z), tested against current data
  (`btfr_mnras`).

## What we tried and did not find

- **The photon is not a Goldstone mode.** The two transverse orientation modes are
  internal **scalars**, not a gauge vector — their polarisation does not lock to the
  wavevector (permutation p = 0.23). The naive "photon = magnon" identification is
  **excluded by measurement** and retracted (`PAPER_GOLDSTONE_PRD`).
- **No emergent photon in any sector tested.** An indefinite-signature Benincasa–Dowker
  gauge operator (new to CST) reproduces free Maxwell on a lattice but fails on the
  causet: causal diamonds are 100% electric (B-type fraction = 0.0000, stable to
  N = 2000). Curvature is the only lever that supplies a magnetic sector, but an O(1)
  photon then needs sub-Planckian curvature — the mechanism is real but does not explain
  the photons of the low-curvature universe (`PAPER_PHOTON_ARC_CQG`).
- **Spacetime dimension does not emerge from sequential growth** (e7 / Tier 3): the grown
  causets are non-manifold (d* ≈ 1.43); the growth rule is a valid Rideout–Sorkin member
  but does not flow to 3+1D.
- **Other closed negatives:** absolute ℏ from geometry, the Born rule, spontaneous Skyrme
  dominance (impossible by a Cauchy–Schwarz theorem), and a spontaneous vacuum condensate.

## Reproducibility

All results are reproducible from fixed seeds. The **anti-circularity guard**
(`tests/test_no_circularity.py`) tokenises every data-generating module and fails if a
Lorentz factor, a gravitational-redshift square root, or an undeclared complex literal
appears in generator code. It runs automatically on every push via GitHub Actions
(`.github/workflows/ci.yml`) — the closest available form of independent verification
before other groups reproduce the results.

```bash
pip install -r requirements.txt
pytest tests/            # guard + unit tests; exit 0 = clean
```

### Reproducing specific results

The full campaign tree ships in this repository: every generator, its emitted
`*.json` verdict (run parameters + numbers embedded), and the pre-registered
charters with kill criteria (`docs/prompts/`). Per paper:

```bash
# Geometry baseline, all papers' floor (e1..e11: SR, dimension, 1/r, curvature,
# the causal d'Alembertian, growth, redshift, phase scaling)
python experiments/run_all.py

# goldstone_prd — order, dispersion, the photon exclusion + robustness
python results/vacuum_structure/orientation/e4/E4_0_fss.py        # finite-size scaling
python results/vacuum_structure/orientation/e4/E4_1_locking.py    # polarisation (photon dies)
python results/vacuum_structure/orientation/e4/E4_R_robustness.py

# photon_arc_cqg — the B-type (magnetic) fraction is structurally zero across N
python results/gauge/e6/E6_3b_eb_population.py
python results/gauge/e6/E6_3c_eb_Nscan.py

# matter_gravity_prd — the soliton sources its own field; baryon quantization
python results/matter/mg/MG1_skyrmion_gravity.py
python results/matter/baryon_quant/run_all.py                     # BQ1..BQ5 suite

# su3_prd — colour ordering, confinement, octet (FL1) + order of the transition
python results/matter/fl1/run_all.py                              # FLA..FLD + octet suite
python docs/campaigns/SU3_ORDEM_TRANSICAO/OT_transition_order.py

# btfr_mnras — prediction, data confrontation (public catalogues)
python results/falsification/btfr_v2/run_all.py
python results/falsification/btfr_v3/V3_confront.py
```

Long campaigns (the finite-size scalings, the L=32 parallel tempering) ship with the
`*.json` written by the original runs, so every quoted number can be checked against
its recorded run before re-executing. Same command → same numbers, from fixed seeds.

### Companion repository

The two axiomatic manuscripts the papers cite as companions — the deductive core
(*What a Lorentz-invariant discrete order can carry*) and the string-net complement —
live with their own pre-registered campaign record at
**<https://github.com/mendesengproj-blip/causal-substrate-core>**.

### Building the papers

```bash
cd paper/submission/goldstone_prd
pdflatex PAPER_GOLDSTONE_PRD && bibtex PAPER_GOLDSTONE_PRD && pdflatex PAPER_GOLDSTONE_PRD && pdflatex PAPER_GOLDSTONE_PRD
```
(Compiled PDFs are not tracked — regenerate from the `.tex` sources.)

## Layout

```
README.md, STATUS.md         this file + claim-by-claim status
TEIC.md, PREDICTIONS.md      living theory summary + falsifiable predictions
RESEARCH_MAP.md              the full campaign map (history of what was tried)
src/                         causal_core, chain, volume, curved (generators — NO relativity)
                             validation.py (the ONLY place SR/GR formulas live)
experiments/                 e1..e11 geometry experiments + run_all.py
results/                     all campaign code + emitted json verdicts + figures,
                             grouped by sector: vacuum_structure/ (orientation,
                             Goldstone), matter/ (SU(2)/SU(3), baryon, MG gravity),
                             gauge/ (E5–E7), falsification/ (BTFR), cosmology/,
                             cmb/, foundations/, bridge/, predictions/, audit/, ...
docs/prompts/                campaign charters (pre-registered kill criteria)
docs/campaigns/              later campaigns (generators + RESULTADO records)
docs/reports/, docs/audits/  analysis reports and audit records
tests/                       test_no_circularity.py + test_no_scale_literal.py (the
                             guards), test_core.py
paper/submission/            the six manuscripts (self-contained: tex + bib + figures
                             + cover letter each)
.github/workflows/ci.yml     the guards as CI, on every push
requirements.txt             pinned dependencies (Python 3.12)
LICENSE                      MIT
```

## Project rules (invariant)

Kill criteria pre-registered before running · negative reported as negative ·
anti-circularity guard on every generator · external scales declared, not hidden.

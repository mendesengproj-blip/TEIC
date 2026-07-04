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
| `photon_arc_cqg` | Systematic map of *where and why a photon is hard* in CST + a new indefinite-signature gauge operator (informative negative) | Class. Quantum Grav. | Submission-ready |
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

### Reproducing the geometry baseline

```bash
# e1..e11: SR from chain counting, dimension/volume, Newtonian relaxation,
# curvature, the causal d'Alembertian, growth dynamics, redshift, phase scaling
python experiments/run_all.py
```

Each experiment writes a self-describing `*.json` (into `results/data/`, created on
first run), embedding the run parameters and the numeric verdict. Same command → same
numbers, from fixed seeds.

### The campaign archive

The headline numbers of each paper come from dedicated campaign generators (finite-size
scaling, polarisation locking, the B-fraction scan, the Skyrmion–gravity sourcing, the
SU(3) transition study). Those scripts, their pre-registered charters with kill
criteria, and the raw `*.json`/figure outputs form the full research archive —
substantially larger than this repository — and are **available from the author on
request** (and will accompany a data deposit). This repository carries the reproducible
core: the substrate engine, the canonical geometry experiments, the guards, and the
complete manuscripts with their figures.

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

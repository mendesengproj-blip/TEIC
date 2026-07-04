# MG1 — the Skyrmion as a direct source of gravity: synthesis

> Charter: `docs/prompts/MG1_MATTER_SOURCES_GRAVITY.md` (kill criteria pre-registered).
> Item R2 of `RESEARCH_MAP.md` — the central gap of `PAPER_MATTER_GRAVITY.tex` (Sec.
> VII). Data/code: `MG1_skyrmion_gravity.py`, `.json`, `.png`. Run jun/2026.

## Verdict: **MATTER → GRAVITY DERIVED** (the form; absolute G_net stays external)

The SU(2)/colour Skyrmion's **own** relaxed energy-density profile ε(r), fed as the
literal source into the static Benincasa–Dowker relaxer of D1–D3, produces
θ(r) = G_net·M/r:

| Test | Result | Death? |
|---|---|---|
| **G0** (solver vs D3) | A=0.980 (D3 1.028), C=−0.028 (exact), exponent −0.990 (D3 −1.018) | no — solver reproduces the BD minimum |
| **M-EXPOENTE** | exterior exponent **−0.992** for every e_sk (target −1±0.10) | no |
| **M-LINEARIDADE** | G_net = A/M = **0.9307** constant to 5 digits over M=175→218 (CV 0.0%) | no |
| **M-GNET** | G_net(Skyrmion) 0.93069 vs G_net(top-hat, same M) 0.93086 — **0.0% diff** | no |

So the soliton's concentrated profile does **not** corrupt the Poisson exterior (the
genuine numerical risk: discreteness + conservation offset + compactness on the grid),
the well amplitude **is** the soliton's own mass M=E2+E4, and the coupling is the same
universal G_net as a generic source. The link in Sec. VII moves from a
**composition of two separately measured laws** to a **single direct measurement**:
the object whose mass we measured sources the field with that mass.

## Honest scope — what this does and does not add

- **Closes** the "natural next step" the paper itself named: use the *real* soliton
  profile as the literal source, not a generic weight. The exterior exponent (−0.99),
  the linearity A∝M, and the shape-independence vs top-hat are now measured for the
  Skyrmion's own ε(r). This promotes Sec. VII's central claim from [FRACO]/composition
  to [SÓLIDO] **for the form**.
- **Does not** change the external status of the absolute coupling: G_net here
  (0.9307) is grid/normalisation-dependent and rides on the action stiffness K
  (G_net∝1/K, D3D) — **[EXTERNO]**, unchanged. The soliton mass is in lattice units.
- **Honest caveat (so we do not overclaim):** the near-exact A∝M and the top-hat match
  are, in part, Gauss's law — the Laplace/Poisson exterior depends only on the total
  enclosed charge. That is *why* the paper's shape-independence over 4 extended
  profiles held, and MG1 confirms it holds for the soliton too **and** that the
  exponent is not corrupted. It is a genuine consistency test passed, not a new force
  law. A fully independent further step (larger campaign, not done here) would source
  the **3D lattice Skyrmion's measured energy density on an actual causal sprinkling**
  into a 3D BD relaxer; MG1 does the radial composition, which is the faithful and
  declared next step. The radial reduction is exact for the embedded hedgehog (the B=1
  soliton is the SU(2) hedgehog, Sec. VII), so this is the right object.

## RESEARCH_MAP update
- Seção 3.3 (matéria→gravidade) and roadmap **R2**: [FRACO]/composição → **[SÓLIDO]
  (forma)**; G_net absoluto permanece [EXTERNO]. Residual: 3D-lattice-on-causal-sprinkling
  version (larger, optional — the radial composition suffices for the paper's claim).

## Anti-circularity
No relativistic expression in the generator (BD action, shell measure r^{d-1}, free
coupling κ — never G; d=3 geometric input). G, M, Schwarzschild only in COMPARISON
ONLY. e_sk the declared external Skyrme stabiliser. G0 validated the exact solver
against the D3 Metropolis engine before any claim. Guard `test_no_circularity.py`
passes. Fixed grid/seed; `MG1_skyrmion_gravity.json` auto-descriptive.

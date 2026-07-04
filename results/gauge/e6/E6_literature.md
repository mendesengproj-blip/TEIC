# E6 — Literature scan: a BD-type operator for the gauge field on causal sets

> Pre-implementation step required by the charter (`E6_BD_GAUGE.md` §6.5 and the
> E6_BD_GAUGE_LORENTZIAN prompt: "ler a literatura e registrar o que existe e o que
> não existe ANTES de escrever código"). The question E6-3 attacks — a
> Benincasa–Dowker-style, indefinite-signature (E²−B²) operator for the U(1) gauge
> 1-form — is read against what the literature already provides. Run jun/2026 via
> WebSearch/WebFetch. Sources at the bottom. Complements `../e7/E7_literature.md`
> (which covered the gauge ACTION line, Sverdlov & Sverdlov–Bombelli, and the 4D
> compact-U(1) phase anchor); this file focuses on the BD/d'Alembertian OPERATOR
> line and whether it has ever been extended off the scalar.

## 1. The Benincasa–Dowker / Dowker–Glaser operator line — scalar only

**Benincasa & Dowker (2010), "The Scalar Curvature of a Causal Set."** Introduced the
discrete, retarded, Lorentz-invariant d'Alembertian `B` acting on a **scalar field**
on a causal set: `(Bφ)(x) = (4/√6 ℓ²)[ −½φ(x) + Σ_layers c_k Σ_{y∈L_k} φ(y) ]`, where
the `L_k` are "inclusive order-interval layers" (the k-th nested past of x by element
count) and the `c_k` are **alternating-sign** coefficients `(1, −9, 16, −8)` in 4D.
The alternation is the whole mechanism: it cancels the divergent mean-field
(constant-mode) contribution so that the smeared sum converges to the local □ in the
continuum. The mean over Poisson sprinklings, `⟨Bφ⟩ → □φ − ½Rφ`, gives the scalar
curvature estimator and thence the Benincasa–Dowker (BD) action.

**Dowker & Glaser (2013), "Causal set d'Alembertians for various dimensions"
(arXiv:1305.2588, CQG).** The paper the prompt named. It generalises the BD operator
to **arbitrary dimension d**: for each d it fixes the number of layers and the
alternating layer coefficients `a_i^{(d)}` (and an overall `b_d`) so that the discrete
operator is Lorentz-invariant on a causet and its Poisson mean approximates the
**scalar** Minkowski d'Alembertian; the dimension-dependent constants are tabulated
for d = 2,…,7, and the advanced/retarded Green's functions follow by Fourier analysis.
A "smeared" (mesoscale ε) version damps the sprinkling fluctuations.

**The decisive negative for E6.** Both papers — and the whole BD/BDG/Dowker–Glaser
line that follows (Glaser–Surya; Belenchia–Benincasa–Dowker continuum-limit proofs;
the 2024–2025 "BDG actions by quantum counting" work) — define the operator on a
**SCALAR field only**. There is **no Benincasa–Dowker operator for a vector field, a
gauge connection, a 1-form, or any p-form** in the literature this scan found. The
alternating layer weights act on `φ(y)` (a number per element); they were never
extended to an object carrying a spacetime/link index or a gauge redundancy. The very
construction E6-3 needs — alternating BD-type smearing of the field strength of a
gauge 1-form, with an indefinite (E²−B²) signature — is **absent**. This matches the
charter's up-front honesty flag: *"there is no standard Benincasa–Dowker gauge
operator."*

## 2. The gauge-field line on causal sets — action, not BD operator, not dispersion

(Carried over and re-verified from `../e7/E7_literature.md`.)

- **Sverdlov, "Gauge Fields in Causal Set Theory" (arXiv:0807.2066, 2008)** and
  **Sverdlov & Bombelli, "Dynamics for causal sets with matter fields" (arXiv:0905.1506,
  2009).** These construct U(1)/Yang–Mills on a causal set by attaching **holonomies to
  pairs of causally related events** and writing a **Lagrangian / action** from parallel
  transport around causal diamonds, causal relations and timelike volumes. This is the
  conceptual ancestor of E5/E6-1's link-angle + diamond-plaquette construction.
- **What they are:** an **ACTION** construction. The 2009 paper writes the gauge matter
  Lagrangian on the causet; it does **not** build a discrete d'Alembertian-style
  *operator* for the gauge field (no alternating-layer smearing), and it does **not**
  measure a dispersion relation or a confinement/Coulomb phase.
- **What is therefore missing:** (i) a BD-style **smeared** gauge operator that tames the
  causal-set non-locality the way the scalar BD operator does (the E5/E6-1 obstruction:
  unbounded mean degree ∝ L^2.9, large harmonic sector); (ii) any demonstration of a
  **Lorentzian (indefinite-signature) gauge propagation** ω=ck on a sprinkled causet.
  E6-2 already showed the *naive* `½ΣF_P²` action is positive-definite (Euclidean),
  minimised at ω≈0 — so the action line, as written, does not give a photon either.

## 3. What is genuinely new in E6-3 (and what it must be gated against)

**New (not in the literature):**
1. An **indefinite-signature gauge operator** on causal-diamond plaquettes, built by
   splitting plaquettes into **E-type** (timelike area bivector, A^{0i}-dominant) and
   **B-type** (spacelike bivector, A^{ij}-dominant) using the plaquette's area bivector,
   with opposite signs → `S = Σ_E(±) F_E² ∓ Σ_B F_B²`, the 1-form analogue of the BD
   scalar operator's alternating weights. This is the "Hodge star / 2-cell weight" the
   charter flagged as the open construction.
2. Reading the operator's **symbol λ(k,ω)** for a *zero crossing* tracking ω=ck (an
   indefinite operator has a zero locus, not a minimum) — distinct from E6-2, which (for
   the Euclidean action) could only look for a minimum, found at ω≈0.

**Must be gated against known continuum results before any causal-set reading
(non-negotiable, per charter §3 and the BD precedent):** the BD scalar operator is only
trusted because its Poisson mean provably → □. E6-3 has **no such theorem**; its
correctness is itself part of the research. So the operator is validated on **flat
Poisson sprinklings of Minkowski** where the free-Maxwell answer is known: H1
(gauge invariance, machine precision — automatic since F=dθ, but checked), H2 (the
symbol's zero crossing must follow ω=ck with c≈1, the light-cone speed *not* inserted),
H3 (two transverse polarisations locked to k). If H2 fails, the construction does not
represent Maxwell and no causal-set number is trustworthy — exactly the discipline the
scalar BD line earned by proving its continuum limit.

## 4. Honest prior

The literature gives **no precedent and no theorem** for a BD-type gauge operator, only
(a) the scalar BD/Dowker–Glaser operators (which E6-3 imitates structurally) and (b) the
Sverdlov–Bombelli gauge *action* (which E6-2 showed is Euclidean as written). The E5/E6-1
obstruction — non-locality (degree ∝ L^2.9) and a large harmonic sector (698/2105 modes)
of the diamond 2-complex — is a concrete reason a clean photon may **not** emerge even
with the right signature: the indefinite split fixes the *signature* but not necessarily
the *non-locality*. The most likely near-term outcome remains **partial** (H1 trivially,
H2 hard), and a frontier/technical verdict — documenting precisely *why* the diamond
2-complex does or does not furnish the Lorentzian cancellation — is itself the original
contribution, since this object has never been built or measured.

## Sources

- [Dowker & Glaser, *Causal set d'Alembertians for various dimensions* (arXiv:1305.2588, 2013)](https://arxiv.org/abs/1305.2588)
- [Benincasa & Dowker, *The Scalar Curvature of a Causal Set*, PRL 104, 181301 (2010) (arXiv:1001.2725)](https://arxiv.org/abs/1001.2725)
- [Belenchia, Benincasa, Dowker, *The continuum limit of a 4-dimensional causal set scalar d'Alembertian* (arXiv:1510.04656)](https://arxiv.org/pdf/1510.04656)
- [Sverdlov, *Gauge Fields in Causal Set Theory* (arXiv:0807.2066, 2008)](https://arxiv.org/pdf/0807.2066)
- [Sverdlov & Bombelli, *Dynamics for causal sets with matter fields* (arXiv:0905.1506, 2009)](https://arxiv.org/pdf/0905.1506)
- [*On the continuum limit of Benincasa-Dowker-Glaser causal set action* (arXiv:2007.13192)](https://arxiv.org/pdf/2007.13192)

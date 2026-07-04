# E7 — Literature scan: gauge theory & the Coulomb phase on causal sets

> Pre-measurement step required by the charter (`E7_COULOMB_PHASE.md`, "CONEXÃO COM A
> LITERATURA — verificar antes de medir"). Done before interpreting any number, so the
> measurement is read against what is and is not already known. Run jun/2026 via
> WebSearch/WebFetch. Sources listed at the bottom.

## 1. Gauge fields on causal sets — what exists

**Sverdlov, "Gauge Fields in Causal Set Theory" (arXiv:0807.2066, 2008).**
Constructs U(1) and SU(n) Yang–Mills on a causal set by attaching **holonomies to
pairs of causally related events** (a group element per causal relation / per causal
"edge"), with the gauge dynamics written in terms of **parallel transport around causal
diamonds**, causal relations, and timelike distances/volumes. This is the conceptual
ancestor of exactly what E5 built: U(1) link angles on the causal graph, plaquette
holonomies on height-2 causal diamonds. Key point for us: the paper is a **Lagrangian /
action construction** — it writes down *how* to define the field and its action on the
causet — it does **not** run a Monte-Carlo measurement of the confinement/Coulomb phase
structure of that action on a sprinkled Poisson causet.

**Sverdlov & Bombelli, "Dynamics for causal sets with matter fields: A Lagrangian-based
approach" (arXiv:0905.1506, 2009).** The 2009 companion the charter named as the entry
point. Extends the Lagrangian-based programme to scalar **and** gauge matter on causal
sets, building the matter actions from causal relations and volumes. Again: a
construction of the action, not a numerical phase-structure study.

**What this means for E7.** The object we are measuring (U(1) Wilson holonomies on
causal diamonds) is *consistent with* the Sverdlov–Bombelli line — it is a concrete,
sprinkling-based realisation of their gauge-on-causet idea. But **the specific question
E7 asks — is the U(1) sector on a Poisson causal set in an area-law (confining) or
perimeter-law (Coulomb) phase — does not appear to have been measured in that
literature.** The CST gauge papers stop at the action; the Monte-Carlo
confinement/Coulomb determination on a sprinkled causet is, as far as this scan found,
**not in the literature.** That makes the *measurement* itself (whatever the verdict)
a small original contribution, and it is consistent with E5's own charter note that "no
standard Benincasa–Dowker gauge operator exists."

> Caveat on the WebFetch summary: an automated read of 0807.2066 returned a sentence
> claiming the paper "investigates Coulomb phase and confinement." Treat this with
> caution — the abstract and the body are an *action construction*, and no MC phase
> diagram is reported there. We do not lean on that claim; the honest statement is the
> one above (construction yes, phase measurement no).

## 2. The known anchor: compact U(1) on a regular 4D lattice

This is the textbook result E5's G2 already reproduced and that E7's gate re-checks:

- **4D compact U(1) Wilson gauge theory has a genuine confinement→Coulomb phase
  transition** at **β_c ≈ 1.01** (Guth 1980; Jersák et al.; DeGrand–Toussaint). For
  **β < β_c** the theory **confines**: the Wilson loop obeys an **area law**
  ⟨W(C)⟩ ~ exp(−σ·Area), σ>0. For **β > β_c** it is in the **Coulomb phase**: the
  Wilson loop obeys a **perimeter law** ⟨W(C)⟩ ~ exp(−μ·Perimeter), and a massless
  photon exists. Recent work (Phys. Rev. D 110, 034518, 2024) refines the transition as
  weakly first-order with a tricritical point, critical exponents near 3D O(2) — detail
  that does not change the area-vs-perimeter dichotomy we use.
- **Strong-coupling theorem (Wilson 1974):** for **any compact gauge group**, in the
  strong-coupling region the Wilson loop has an **area law** — confinement is the
  generic strong-coupling behaviour; a Coulomb/deconfined phase is the *non-trivial*
  thing that must appear at weak coupling for a photon to exist.
- **3D compact U(1) confines at ALL β** (Polyakov 1977): monopole plasma, permanent
  area law, **no Coulomb phase, no massless photon**. This is the contrast that makes
  the 4D Coulomb phase non-generic and dimension-dependent.

**Consistency check on E5.** E5's G2 found the specific-heat peak of the *same engine*
on a regular 4D lattice at **β = 1.00**, squarely on the known β_c ≈ 1.01. So the engine
reproduces the canonical 4D number — the gate is meaningful.

## 3. The implication framing for E7

The literature sharpens the stakes exactly as the charter set them:

- A Coulomb (perimeter-law) phase is **not guaranteed** to exist on the causal substrate.
  In 3D compact U(1) it does not exist at any β. Whether the Poisson causal set's U(1)
  sector has one is an open, dimension-and-locality–sensitive question.
- E5-1b already measured that the bare causal diamonds inherit an **unbounded mean degree
  (deg ∝ L^2.9)** — a *mean-field / non-local* substrate. Mean-field compact U(1) is in
  its confining (strong-coupling-like) regime unless a weak-coupling Coulomb phase opens;
  non-locality tends to *favour* confinement-like (area-law) behaviour, not against it.
  So the literature's prior, combined with E5-1b, leans toward **confining** — but that
  is a prior, not a measurement. E7 measures it.

## Sources

- [Sverdlov, *Gauge Fields in Causal Set Theory* (arXiv:0807.2066)](https://arxiv.org/pdf/0807.2066)
- [Sverdlov & Bombelli, *Dynamics for causal sets with matter fields* (arXiv:0905.1506)](https://arxiv.org/pdf/0905.1506)
- [*Four-dimensional pure compact U(1) gauge theory on a spherical lattice*, Phys. Rev. D 54, 6909 (1996) (arXiv:hep-lat/9606013)](https://arxiv.org/pdf/hep-lat/9606013)
- [*Tricriticality in 4D U(1) Lattice Gauge Theory*, Phys. Rev. D 110, 034518 (2024) (arXiv:2404.15907)](https://arxiv.org/abs/2404.15907)
- [*Existence of Confinement Phase in Quantum Electrodynamics* (arXiv:hep-th/9803133)](https://arxiv.org/pdf/hep-th/9803133)

# E5_PHOTON_LINK_SECTOR — is the emergent photon in the U(1) link-connection sector?

> PRE-REGISTERED charter, written BEFORE running E5. Saved at repo root per
> convention. Follows E4, which showed (by measurement) that the orientation
> Goldstone modes are internal SCALARS, not a gauge vector, and pointed -- by
> elimination -- to the gauge-connection (link-variable) sector as the only place an
> emergent photon could originate. E5 tests that sector. Anti-circularity unchanged:
> no relativistic/quantum literal in any generator; "photon" only in synthesis.

---

## 1. Why the link sector, and why a photon CAN live here (unlike E4)

E4 established that the orientation field carries an INTERNAL index decoupled from
spacetime, so its Goldstone modes are scalars: no gauge redundancy, no locking to k.
A photon needs (i) a field carrying a spacetime/link index, (ii) a gauge redundancy,
and (iii) a deconfined (Coulomb) phase hosting a massless transverse vector. A U(1)
CONNECTION on the causal links supplies (i) and (ii) by construction: a phase
theta_ij on each Hasse link, with the action depending only on gauge-invariant
plaquette holonomies. Whether (iii) holds -- a deconfined Coulomb phase with a
massless photon -- is the empirical question. Unlike E4, the answer is NOT forbidden
by symmetry: 4D U(1) lattice gauge theory is KNOWN to have a Coulomb phase at weak
coupling (Guth 1980), so an emergent photon is physically possible here.

## 2. The honest prior (recorded before running)

There is a specific reason to doubt a Coulomb phase EXISTS on the causal set:
deconfinement in U(1) is controlled by monopole (dis)condensation (Polyakov). The
SU(2)/U(1) vacuum studies already in this programme reported a Wilson-loop AREA LAW
(confinement) with monopoles present at all resolved couplings, U(1) confinement
being weaker than SU(2) but still present. If monopoles stay condensed at all
accessible couplings on the causal graph, U(1) CONFINES and there is NO massless
photon -- the photon would then be excluded from BOTH sectors (E4 scalars + E5
confinement), a clean, strong, honest negative for the whole framework. The opposite
outcome (a deconfined Coulomb phase at weak coupling) would be the first positive
location of an emergent photon. We genuinely do not know which; that is the right
state for a pre-registered test.

## 3. The construction (stated, with its known difficulty)

- Field: U(1) phase theta_ij in (-pi,pi] on each undirected Hasse link.
- Plaquettes: a causal set has no elementary square. We use the natural height-2
  CAUSAL DIAMONDS: for events i < k joined by >= 2 distinct length-2 link paths
  i->a->k and i->b->k, the oriented loop i->a->k->b->i is a plaquette, with holonomy
  theta_P = theta_ia + theta_ak - theta_bk - theta_ib. (This is the irregular-graph
  analogue of a plaquette; its definition is a modelling choice, flagged as such.)
- Wilson action: S = beta * sum_P [1 - cos(theta_P)].
- Gauge invariance: a local shift theta_ij -> theta_ij + (lam_j - lam_i) leaves every
  closed-loop holonomy invariant (checked as an engineering gate).

## 4. ENGINEERING GATE (mandatory, before any causal-set physics)

The engine must reproduce KNOWN U(1) lattice-gauge results on a REGULAR 4D periodic
lattice, with the SAME machinery used on the causal set:
  G1. Gauge invariance: random local gauge transforms leave all plaquette holonomies
      and Wilson loops invariant to machine precision.
  G2. Known transition: 4D U(1) Wilson gauge theory has a deconfinement transition at
      beta_c ~ 1.01. The average plaquette <cos theta_P>(beta) must show the known
      crossover (strong-coupling/confined below, Coulomb above), and the static
      potential must switch from area-law (confined) to Coulomb (1/r) across it.
  G3. 3D control: 4D U(1) is Coulomb at weak coupling, but 3D U(1) confines at ALL
      couplings (Polyakov) -- the engine must reproduce that contrast.
If the engine fails any gate, STOP: no causal-set number is trustworthy.

## 5. Tasks and pre-registered decisions

### E5-V -- gate (G1-G3 above). Output: E5V_gate.{py,md,json}.

### E5-1 -- U(1) confinement scan on the causal set.
Build the U(1) gauge field on the causal Hasse graph; scan beta; measure the
Wilson-loop scaling (string tension sigma(beta) via loops binned by area/perimeter)
and the average plaquette. 20 seeds.
PRE-REGISTERED DECISION:
  CONFINED (photon dies in the link sector too): sigma(beta) > 0 (area law) at all
    accessible beta, with no crossover to a perimeter/Coulomb law. Combined with E4,
    the emergent photon is then excluded from every sector tested.
  DECONFINED (photon candidate): sigma(beta) -> 0 at weak coupling (a Coulomb phase
    appears), with a perimeter-law Wilson loop. Proceed to E5-2.
Output: E5_1_confinement.{py,md,json,png}.

### E5-2 -- the photon, IF deconfined (only if E5-1 finds a Coulomb phase).
In the deconfined phase, measure the gauge-field excitation dispersion (via the
causal wave operator on the link field) and its polarisation: a photon requires
omega = ck, massless, TWO TRANSVERSE polarisations LOCKED to k (the E4-1 locking
test, now expected to PASS because the field carries a link index).
PRE-REGISTERED DECISION:
  PHOTON: omega=ck, massless, 2 transverse polarisations, polarisation locks to k
    (permutation test passes). The emergent photon is located.
  NOT A PHOTON: gapped, or no k-locking. Report what it is.
Output: E5_2_photon.{py,md,json,png}.

### E5-3 -- synthesis + verdict (A photon / B partial / C confined-no-photon).
Output: E5_3_synthesis.md.

## 6. Protocol

1. E5-V (gate) BEFORE any causal-set measurement; reproduce 4D beta_c~1.01 and the
   3D-confines / 4D-deconfines contrast, or stop.
2. E5-1 before E5-2; E5-2 runs only if a Coulomb phase exists.
3. 20 seeds; pre-registered decisions above are not adjusted to escape an outcome.
4. The plaquette = causal-diamond definition is a modelling choice; its robustness
   (alternative loop definitions) is part of the honest reporting.
5. Anti-circularity: the gauge dynamics uses only cos(theta_P); c (if measured in
   E5-2) is a free fit parameter, never inserted.

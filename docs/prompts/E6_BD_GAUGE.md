# E6_BD_GAUGE — the emergent photon via a BD-smeared gauge construction (CHARTER)

> PRE-REGISTERED charter for the genuine next step after E4 (orientation Goldstones
> are scalars, not a photon) and E5 (U(1) Wilson theory on bare causal diamonds is
> obstructed: the substrate is nonlocal/mean-field, and no Lorentz-invariant local
> geometry exists -- degree ~ L^2.9 measured). This charter is documented so the
> path is concrete; it is RESEARCH-GRADE and is NOT to be implemented as a quick
> artefact. Honest flag up front: there is no standard "Benincasa-Dowker gauge
> operator"; the construction below is novel, and its very existence/correctness is
> part of the research, so it must be gated hard against known continuum results
> before any causal-set number is trusted. Estimated effort: a dedicated campaign.

## 1. Why this is the only honest route left for the photon

- E4: the orientation Goldstones carry an INTERNAL index decoupled from spacetime
  => scalars, not a gauge vector. Photon excluded from that sector by measurement.
- E5: a U(1) CONNECTION on the links carries a spacetime index + gauge redundancy
  (the right structure), but the bare-diamond Wilson action inherits the causal-set
  nonlocality (mean-field, unbounded degree), so confinement/deconfinement and any
  relativistic photon cannot be cleanly settled there.
- The scalar sector (E2) faced the SAME nonlocality and resolved it with the smeared
  Sorkin-Benincasa-Dowker (SBD) d'Alembertian. The gauge analogue is to build the
  gauge dynamics from an SBD-type nonlocal-but-Lorentz-invariant operator, so the
  emergent excitation can be a genuine relativistic massless vector.

## 2. The construction (discrete exterior calculus on the causal set)

- Gauge field A: a 1-cochain, A_ij = -A_ji on causal links (the connection).
- Field strength F: the discrete coboundary (dA) on causal "plaquettes"/2-cells.
- SBD-smeared Maxwell action: instead of the bare Wilson sum over diamonds, use a
  nonlocal, alternating-shell-weighted 2-cochain inner product
  S[A] ~ sum over causal 2-cells with SBD layer weights of (dA)^2, designed so that
  (i) it is gauge-invariant (S[A+dlam]=S[A], lam a 0-cochain), and (ii) it converges
  to the continuum Maxwell action (1/4) F_{mu nu}F^{mu nu} as rho -> infinity,
  taming the nonlocality exactly as the scalar SBD operator does.
- This requires defining the causal-set analogues of d (coboundary) and the Hodge
  star / 2-cell weights -- the open construction.

## 3. MANDATORY validation gates (before any causal-set physics)

  H1 gauge invariance: S[A+dlam] = S[A] for random 0-cochains lam (machine precision).
  H2 continuum limit: on Poisson sprinklings of FLAT (3+1)D Minkowski, the free
     excitation must disperse as omega = ck (light cone, c not inserted), be
     MASSLESS, and have exactly TWO TRANSVERSE polarisations LOCKED to k
     (k.epsilon=0) -- the photon kinematics the bare graph could not give. Validate
     the SBD-gauge operator reproduces these against the known free-Maxwell answer.
  H3 Coulomb law: a static point source must produce a 1/r potential (Coulomb),
     not confinement, in the weak-coupling phase.
If any gate fails, STOP: the construction does not represent Maxwell and no
causal-set result is trustworthy.

## 4. Pre-registered decisions (only if gates pass)

  PHOTON (success): the SBD-gauge excitation on the causal set is massless, omega=ck,
    two transverse polarisations locked to k, with a Coulomb (deconfined) phase. The
    emergent photon is located in the link sector. This would be the positive that
    E4/E5 could not reach.
  NOT A PHOTON / CONFINED: gapped, or no k-locking, or confining at all couplings.
    Report it as the measured outcome; combined with E4, the photon would then be
    absent from every constructed sector, and the framework does not produce
    electromagnetism.

## 5. Honest risk assessment (recorded)

- The discrete exterior calculus + SBD-smeared gauge action on a Poisson causal set
  is at the research frontier of causal set theory; a correct, gauge-invariant,
  continuum-converging construction may be subtle or may not exist in simple form.
- Even if H1-H3 pass on flat sprinklings, the causal-set photon would be a
  KINEMATIC photon (free Maxwell); deriving the gauge COUPLING to matter and a
  conserved charge is a further, separate step (as flagged for the scalar sector).
- This charter commits to the gates and the honest verdict, not to a positive
  outcome. The most likely near-term result is partial (H1 doable; H2 hard).

## 6. Protocol

1. H1 (gauge invariance) first -- cheap, decisive for whether the action is even a
   gauge action.
2. H2 (continuum free-photon) is the crux and the hard part; needs the SBD 2-cell
   weights, validated against free Maxwell on flat sprinklings.
3. H3 (Coulomb) only after H2.
4. Causal-set physics only after all gates pass.
5. Pre-registered decisions not adjusted to escape an outcome; the nonlocality
   obstruction of E5 is the reason this construction (not bare Wilson) is required.

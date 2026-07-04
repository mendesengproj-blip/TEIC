# E4_PHOTON_DISCRIMINATOR — is the orientation Goldstone a photon, or two scalars?

> PRE-REGISTERED charter, written BEFORE running E4. Saved at repo root per
> project convention. Continues E1 (orientation ferromagnet) and E2 (BD-symbol
> dispersion). Reuses `orientation_core.py` (O(3) Metropolis + C(r) + transverse
> structure factor) and, where noted, `e2/e2_core.py`. Does NOT modify any prior
> campaign. Anti-circularity discipline unchanged: no relativistic/quantum literal
> in any generator; "photon"/"magnon" appear only in synthesis.
>
> MOTIVE. The draft paper PAPER_PHOTON_PRD identifies the transverse O(3) Goldstone
> mode with the photon. Reviewer-style scrutiny (and a close reading of the E2
> source) exposes two gaps that retoric cannot close and that we therefore test by
> measurement:
>   (G1) the dispersion omega=ck measured in E2 is the SYMBOL of the causal
>        d'Alembertian B_eps on a SCALAR probe (a Benincasa-Dowker geometric
>        property), not the dynamical dispersion of the vector field delta-n
>        (whose retarded propagation e2_core documents as numerically unstable);
>   (G2) the two Goldstone modes of O(3)->O(2) carry an INTERNAL index on S^2, with
>        no a-priori relation to the spatial wavevector k; a photon A_mu carries a
>        SPACETIME index locked to k (k.A=0). The bare action
>        S = J sum_links dtau [1 - n_i . n_j] has a GLOBAL internal O(3) symmetry
>        decoupled from the spacetime Lorentz symmetry, so on symmetry grounds the
>        internal polarisation is expected to be isotropic and k-independent.
>
> HONEST PRE-STATEMENT OF EXPECTATION (recorded before running, so the result
> cannot be reverse-justified). On the symmetry argument above we EXPECT E4-1 to
> find NO internal<->spatial locking, i.e. the two modes behave as two decoupled
> relativistic SCALARS, not as a gauge vector. If so, the honest outcome is that
> the naive "photon" identification is FALSIFIED, and the defensible result becomes
> "spontaneous orientational order on a causal set + a relativistic Goldstone
> (scalar) sector". A surprise (genuine locking) would, conversely, give the photon
> identification a dynamical basis it currently lacks. Either outcome is publishable
> and decided by data, not wording.

---

## E4-0 — Finite-size scaling of the long-range order (reviewer point 3)

QUESTION. E1 reported C(r) -> C_inf = m^2 > 0 at a single system size. Is the
long-range order genuine, or a finite-size artefact?

METHOD. At fixed coupling J = 2.0 (deep in the ordered phase, J >> J_c ~ 0.08),
build the causal link graph of a 3+1D Poisson sprinkle at increasing event number
N (by increasing the sprinkled 4-volume at fixed density rho, and cross-checking at
fixed volume with increasing rho). Measure, over >= 12 seeds per size:
  * the order parameter m(N) = |<n>| (equilibrium average);
  * the Binder cumulant U4(N) = 1 - <m^4> / (3 <m^2>^2).
A true ordered phase has m(N) approaching a non-zero constant and U4 -> 2/3 as N
grows; a disordered/artefact phase has m(N) -> 0 (consistent with the Gaussian
value m ~ N^{-1/2}) and U4 -> 0.

PRE-REGISTERED DECISION.
  DEATH (the order was an artefact): m(N) falls toward zero with increasing N,
    consistent with the random-vector floor m ~ N^{-1/2}, AND U4 -> 0. The E1
    long-range-order claim would be retracted.
  SUCCESS: m(N) flattens to a non-zero plateau (or extrapolates to m_inf > 0) and
    U4 stays near 2/3. The order is genuine.
  PARTIAL: trend positive but sizes too small to extrapolate; report and enlarge.

Output: results/vacuum_structure/orientation/e4/E4_0_fss.{py,md,json,png}.

---

## E4-1 — Polarisation locking: gauge vector vs two scalars (DECISIVE for "photon")

QUESTION. Do the two transverse Goldstone modes carry a polarisation that locks to
the spatial wavevector k (the signature of a transverse gauge vector, k.A = 0), or
is their internal polarisation isotropic and independent of k (two decoupled
scalars)?

METHOD. In the ordered state (J = 2.0), build the internal transverse frame
(e1, e2) perpendicular to <n> (as in orientation_core.transverse_components). For a
set of spatial wavevectors k (varying both magnitude and DIRECTION khat), form the
complex transverse amplitudes
    tilde-n_a(k) = sum_i (n_i . e_a) [cos(k.x_i) - i sin(k.x_i)],   a in {1,2},
and the 2x2 Hermitian polarisation tensor P_ab(k) = < tilde-n_a tilde-n_b^* >.
Define a locking anisotropy A(k): the fractional dependence of the eigenvector
orientation of P_ab on khat, measured as the correlation between the principal
polarisation direction and the spatial direction khat across the k-sphere. (Real
arithmetic: the complex amplitude is formed from separate cos/sin sums in the
estimator module, which is NOT a network generator; no complex literal enters the
spin dynamics.)

PRE-REGISTERED DECISION.
  PHOTON (gauge vector): A(k) is significantly > 0 and the power concentrates in
    the spatial-transverse projector (delta_ij - k_i k_j/k^2); the polarisation
    tracks khat. This would give the photon identification a dynamical basis.
  DEATH OF THE PHOTON (two scalars): A(k) ~ 0 within error; P_ab ~ isotropic
    (proportional to the identity, eigenvalues equal), independent of khat. The two
    modes are decoupled internal scalars; the "photon" identification is dropped
    and the paper is reframed around relativistic scalar Goldstones.
  Threshold fixed in advance: |A| < 3 sigma_A => no locking (scalars);
  |A| > 5 sigma_A with the transverse-projector structure => locking (vector).

Output: results/vacuum_structure/orientation/e4/E4_1_locking.{py,md,json,png}.

---

## E4-2 — Spatial isotropy and Goldstone degeneracy (supports the honest result)

QUESTION (only the parts not already settled by E4-1). Is the propagation isotropic
in space (omega(k) independent of khat), and are the two transverse Goldstone modes
degenerate (equal dispersion)? Both are required for "two relativistic scalars" to
be a clean statement.

METHOD. Reuse the E2 BD-symbol estimator (e2_core) generalised to direction-
resolved k, and the two transverse components from E4-1. Compare omega(k) across
directions and across the two modes.

PRE-REGISTERED DECISION.
  SUCCESS: omega(k) direction-independent within error AND the two modes
    degenerate => clean "two relativistic scalar Goldstones".
  PARTIAL/FAIL: anisotropy or non-degeneracy => report it; it would itself be a
    constraint on emergent spatial isotropy.

Output: results/vacuum_structure/orientation/e4/E4_2_isotropy.{py,md,json,png}.

---

## Protocol

1. E4-0 first (it validates the vacuum the other tests assume).
2. E4-1 is the decisive photon discriminator; run after E4-0 passes.
3. E4-2 only sharpens the honest fallback; run last.
4. >= 12 seeds for E4-0; >= 8 for E4-1/E4-2. Errors from seed scatter (SEM).
5. Pre-registered decisions above are not to be adjusted to escape an outcome.
6. The paper's framing follows the verdict: if E4-1 kills the photon, the title and
   claim change to the scalar-Goldstone result, with E4-1 reported as the killing
   measurement (a result, not a hidden negative).

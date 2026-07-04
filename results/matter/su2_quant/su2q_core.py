"""su2q_core.py -- shared engine for MATTER_SU2_QUANT (Q1-Q7).

MATTER_SU2 ended at Verdict B: a stable point Skyrmion (B=1) exists classically, but its
spin is undefined because spin-1/2 is a QUANTUM (Finkelstein-Rubinstein) phase invisible
to a classical field.  This campaign quantises the Skyrmion's collective (rotational)
coordinate -- a rigid rotor on SU(2) ~= S^3 -- and applies the FR constraint to derive
the spin spectrum.

The physics (Adkins-Nappi-Witten):
  * the orientation of the Skyrmion is a coordinate A in SU(2); rotating it costs zero
    energy (a zero mode), so the low-energy dynamics is a free particle on S^3 with a
    moment of inertia I (Q1, Q2);
  * quantising gives the rigid-rotor spectrum E_j = j(j+1)/(2I), j = 0, 1/2, 1, ... (Q3);
  * for B=1 the Finkelstein-Rubinstein constraint forces the wavefunction to be ODD under
    A -> -A (a 2pi rotation), selecting HALF-INTEGER j only -> ground state j = 1/2 (Q4).

ANTI-CIRCULARITY: SU(2) is unit quaternions (4 reals), products via su2_core (Hamilton,
no Pauli, no complex literal).  The FR phase is a topological count of antipodal crossings
on S^3; the spin j is read from an energy spectrum.  "spin"/"fermion"/"boson"/"proton"
appear ONLY in COMPARISON ONLY notes; nothing is inserted by hand.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s   # noqa: E402  (quaternions, Skyrmion, energy, baryon)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

PI = np.pi


# =========================================================================== #
# The classical Skyrmion (reuse SU3) and its rotational zero modes
# =========================================================================== #
def skyrmion(e_sk=4.0, N=41, L=16.0, rmax=14.0, nr=360):
    """Relax the radial profile (su2_core) and build the 3D hedgehog U_0 with B=1.
    Returns (U0, dx, M_Sk, E2, E4)."""
    r, dr = s.radial_grid(rmax=rmax, n=nr)
    F, E2r, E4r = s.radial_relax(r, dr, e_sk)
    prof = s.profile_from_radial(F, r)
    xs = np.linspace(-L / 2, L / 2, N)
    dx = float(xs[1] - xs[0])
    U0 = s.hedgehog_field(xs, xs, xs, profile=prof)
    E2, E4, M = s.chiral_energy(U0, dx, e_sk)
    return U0, dx, M, E2, E4, xs


def iso_rotate(U, A):
    """Global SU(2) (iso)rotation U -> A U A^dag (an exact symmetry of the lattice
    chiral energy: 1/2 Tr and the current cross-products are conjugation-invariant)."""
    return s.q_mul(s.q_mul(A, U), s.q_conj(A))


def rotation_quat(axis_index, angle):
    """SU(2) element exp(i (angle/2) sigma_a): a rotation by PHYSICAL angle ``angle``
    about axis a.  The half-angle is the SU(2) double cover."""
    e = np.zeros(3); e[axis_index] = 1.0
    return s.q_from_axis_angle(e, 0.5 * angle)


def zero_mode(U0, axis_index):
    """Rotational zero mode xi_a = d/d(angle) [A U0 A^dag] at angle=0, with the PHYSICAL
    rotation angle.  Analytically xi_a = [T_a, U0] (quaternion commutator), T_a = (0, e_a/2).
    xi_a is tangent to S^3 at each site (xi_a . U0 = 0)."""
    T = np.zeros(4); T[1 + axis_index] = 0.5            # T_a = (0, e_a/2)
    Tq = np.broadcast_to(T, U0.shape)
    return s.q_mul(Tq, U0) - s.q_mul(U0, Tq)


def mode_overlap(xi_a, xi_b, dx):
    """Inertia-tensor element I_ab = integral Tr[xi_a^dag xi_b] d^3x.  For quaternion-
    valued tangents, Tr[xi_a^dag xi_b] = 2 (xi_a . xi_b) (4-vector dot), so
    I_ab = 2 sum_sites (xi_a . xi_b) dx^3."""
    return 2.0 * float(np.sum(np.sum(xi_a * xi_b, axis=-1))) * dx ** 3


def inertia_tensor(U0, dx):
    """3x3 rotational inertia tensor I_ab from the three zero modes."""
    xis = [zero_mode(U0, a) for a in range(3)]
    I = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            I[a, b] = mode_overlap(xis[a], xis[b], dx)
    return I, xis


# =========================================================================== #
# Rigid rotor on S^3: spectrum by transfer-matrix diagonalisation
# =========================================================================== #
# A free particle on SU(2)=S^3 with Euclidean action S = a * sum |q_{n+1}-q_n|^2 (4-vec
# norm) has transfer operator K(q,q') = exp(-a |q-q'|^2) = exp(-a(2 - 2 q.q')).  Its
# eigenfunctions are the S^3 harmonics of degree l (l = 2j), eigenvalue lambda_l, and
# E_l - E_0 = -ln(lambda_l/lambda_0)/dt_eff.  We sample S^3 with random unit quaternions
# (uniform Haar measure) and diagonalise the symmetric kernel matrix.

def sample_s3(M, rng):
    """M uniform (Haar) random unit quaternions on S^3."""
    q = rng.standard_normal((M, 4))
    return s.q_normalize(q)


def transfer_spectrum(points, a, n_levels=8, fr=False):
    """Eigenvalues of the transfer kernel on the sampled S^3 points.

    K_ij     = exp(-a |q_i - q_j|^2) = exp(-a (2 - 2 q_i.q_j))
    K_anti_ij= exp(-a |q_i + q_j|^2) = exp(-a (2 + 2 q_i.q_j))   (q_j -> -q_j antipode)

    fr=False: diagonalise K -> eigenvalues for ALL degrees l (j = l/2 = 0,1/2,1,...).
    fr=True : diagonalise K - K_anti -> acts as 2K on ODD functions (l odd = half-integer
              j) and 0 on EVEN (integer j): the Finkelstein-Rubinstein projection for B=1.

    Returns (lambdas_desc, E_levels) with E_l - E_0 = -ln(lambda_l/lambda_0) (dt absorbed)."""
    G = points @ points.T                                # q_i . q_j
    K = np.exp(-a * (2.0 - 2.0 * G))
    if fr:
        Kanti = np.exp(-a * (2.0 + 2.0 * G))
        Kmat = K - Kanti
    else:
        Kmat = K
    Kmat = 0.5 * (Kmat + Kmat.T)
    w = np.linalg.eigvalsh(Kmat)
    w = np.sort(w)[::-1]                                  # descending
    w = w[w > 1e-12]
    lam0 = w[0]
    E = -np.log(np.maximum(w[:n_levels], 1e-300) / lam0)
    return w[:n_levels], E


def degeneracy_groups(lambdas, tol=0.04):
    """Group nearly-degenerate eigenvalues (relative gap < tol) -> list of multiplicities
    and representative eigenvalues, to read off the (l+1)^2 = (2j+1)^2 degeneracies."""
    groups = []
    i = 0
    n = len(lambdas)
    while i < n:
        j = i + 1
        while j < n and abs(lambdas[j] - lambdas[i]) <= tol * abs(lambdas[i]):
            j += 1
        groups.append({"lambda": float(lambdas[i]), "mult": int(j - i)})
        i = j
    return groups


# =========================================================================== #
# Monte-Carlo path integral on S^3 (Q3 confirmation, Euclidean, no FR)
# =========================================================================== #
def mc_path_correlator(I_eff, n_time, n_mc, dt, rng, n_therm=200, step=0.3):
    """Metropolis sampling of closed paths q_0..q_{n-1} on S^3 with Euclidean action
    S = (I_eff/(2 dt)) sum |q_{n+1}-q_n|^2 (4-vec).  Measure the degree-1 correlator
    C(tau) = < q_t . q_{t+tau} > (a degree-1 = j=1/2 harmonic), which decays as
    exp(-(E_1 - E_0) tau).  Returns C(tau)."""
    q = sample_s3(n_time, rng)
    a = I_eff / (2.0 * dt)

    def local_action(qi, ql, qr):
        return a * ((2 - 2 * qi @ ql) + (2 - 2 * qi @ qr))

    def sweep(q):
        for n in range(n_time):
            ql = q[(n - 1) % n_time]; qr = q[(n + 1) % n_time]
            old = q[n]
            prop = s.q_normalize(old + step * rng.standard_normal(4))
            dS = (a * ((2 - 2 * prop @ ql) + (2 - 2 * prop @ qr))
                  - local_action(old, ql, qr))
            if rng.uniform() < np.exp(-dS):
                q[n] = prop
        return q

    for _ in range(n_therm):
        q = sweep(q)
    C = np.zeros(n_time)
    cnt = 0
    for _ in range(n_mc):
        q = sweep(q)
        G = q @ q.T                                      # q_t . q_{t'}
        for tau in range(n_time):
            C[tau] += np.mean([G[t, (t + tau) % n_time] for t in range(n_time)])
        cnt += 1
    return C / cnt


# =========================================================================== #
# IO
# =========================================================================== #
def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print("su2q_core smoke")
    # 1) Skyrmion + inertia
    U0, dx, M, E2, E4, xs = skyrmion(e_sk=4.0, N=31, L=14.0)
    I, xis = inertia_tensor(U0, dx)
    print(f"M_Sk={M:.2f}  I_diag={np.round(np.diag(I),3)}  "
          f"offdiag_max={np.max(np.abs(I-np.diag(np.diag(I)))):.3e}")
    # iso-rotation invariance of energy (Q1 preview)
    A = rotation_quat(1, 0.7)
    UR = iso_rotate(U0, A)
    ER = s.chiral_energy(UR, dx, 4.0)[2]
    print(f"E[U0]={M:.4f}  E[A U0 A^dag]={ER:.4f}  rel diff={abs(ER-M)/M:.2e}")
    # 2) rotor spectrum (transfer matrix) -- expect E_l ∝ l(l+2)
    pts = sample_s3(1200, rng)
    lam, E = transfer_spectrum(pts, a=2.0, n_levels=10)
    print("full spectrum E (first 10):", np.round(E, 3))
    lamF, EF = transfer_spectrum(pts, a=2.0, n_levels=10, fr=True)
    print("FR   spectrum E (first 10):", np.round(EF, 3))

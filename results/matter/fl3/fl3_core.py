"""fl3_core.py -- shared engine for FL3_SKYRMION_COLLISION.

FL3 asks whether a Skyrmion(B=+1) colliding with an anti-Skyrmion(B=-1) CREATES an
additional pair -- the causal-lattice analogue of pair production.  It reuses the
MATTER_SU2 chiral engine (su2_core): unit-quaternion SU(2) field U(x), the principal-
chiral + Skyrme energy, the geometric topological charge B (Pontryagin index), and the
geodesic velocity-Verlet (chiral_evolve) that conserves E_kin + E2 + E4 while moving each
site exactly along a great circle of S^3.

What FL3 ADDS on top of su2_core (nothing in su2_core or any earlier campaign is touched):

  * relaxed_profile : the rigorous radial Skyrme profile F(r) (su2_core.radial_relax),
    so an ISOLATED Skyrmion is a genuine energy minimum (stable in flight) -- the gate
    needs this or the "moving" Skyrmion just breathes/radiates.
  * boosted_pair    : a Skyrmion + anti-Skyrmion at +/- d/2, each given a translation
    VELOCITY by a finite-difference body angular velocity w0 = log(U0^-1 U_eps)/eps_t,
    the exact discrete velocity the leapfrog integrates (U <- U exp(dt w)).  No Lorentz
    gamma is baked into the profile; the kinetic energy is whatever the lattice carries,
    measured directly (so FL3-5's E >= 2 M c^2 test is not circular).
  * single_boosted  : one boosted Skyrmion (gate translation + dispersion tests).
  * count_peaks / count_blobs : the decisive observables.  N_peaks = local maxima of the
    energy density (each lump = one soliton); count_blobs = connected components of the
    POSITIVE and NEGATIVE baryon-density above threshold (B=+1 lumps vs B=-1 lumps).
    Creation => total blobs 2 -> 4 with B_total still 0.
  * lattice_mass    : M_Sk as the 3D lattice energy of the relaxed Skyrmion (for FL3-5).

ANTI-CIRCULARITY (inherited from su2_core, scanned by tests/test_no_circularity.py):
  B is the current determinant (no physical label); c=0.98 is MEASURED in E2; M_Sk is the
  energy functional.  "pair production", "e+e-", "LHC" are COMPARISON ONLY names.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# --- reuse the MATTER_SU2 chiral engine unchanged ---------------------------- #
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

# c = magnon group speed MEASURED in the orientation E2 dispersion (omega = ck, Verdict A).
# Loaded, never hand-set, so the boost "v = fraction of c" is anchored to a measurement.
_E2 = (ROOT / "results" / "vacuum_structure" / "orientation" / "e2" /
       "E2_2_dispersion.json")
C_MAGNON = float(json.loads(_E2.read_text())["c_fit"]) if _E2.exists() else 0.98


# =========================================================================== #
# Grid
# =========================================================================== #
def cubic_grid(L, N):
    xs = np.linspace(-L / 2.0, L / 2.0, N)
    dx = float(xs[1] - xs[0])
    return xs, dx


# =========================================================================== #
# Relaxed Skyrme profile (stable isolated soliton)
# =========================================================================== #
_PROFILE_CACHE: dict = {}


def relaxed_profile(e_sk, rmax=12.0, n=360):
    """Callable F(r) of the relaxed radial Skyrme functional (su2_core.radial_relax).
    F(0)=pi, F(inf)=0 -> B=+1.  Cached per e_sk."""
    key = (round(e_sk, 6), rmax, n)
    if key not in _PROFILE_CACHE:
        r, dr = s.radial_grid(rmax=rmax, n=n)
        F, E2, E4 = s.radial_relax(r, dr, e_sk)
        _PROFILE_CACHE[key] = (s.profile_from_radial(F, r), E2, E4)
    prof, E2, E4 = _PROFILE_CACHE[key]
    return prof


def lattice_mass(L, N, e_sk, prof=None):
    """M_Sk = 3D lattice energy of the relaxed Skyrmion centred in the box, with its B."""
    xs, dx = cubic_grid(L, N)
    if prof is None:
        prof = relaxed_profile(e_sk)
    U = s.hedgehog_field(xs, xs, xs, profile=prof)
    E2, E4, Et = s.chiral_energy(U, dx, e_sk)
    B = s.baryon_number(U, dx)
    return {"M_lattice": Et, "E2": E2, "E4": E4, "B": B, "L": L, "N": N, "dx": dx,
            "e_sk": e_sk}


# =========================================================================== #
# Boost: translation velocity as a finite-difference body angular velocity
# =========================================================================== #
def _hh(xs, center, B_sign, prof):
    return s.hedgehog_field(xs, xs, xs, profile=prof, center=center, B_sign=B_sign)


def single_boosted(xs, dx, center, v_vec, prof, B_sign=+1, eps_t=0.02):
    """One Skyrmion at ``center`` translating with velocity ``v_vec`` (3-vector, lattice
    units).  Velocity is encoded as the body angular velocity field
        w0 = log( U(0)^-1 U(eps_t) ) / eps_t ,
    where U(eps_t) is the SAME soliton with centre shifted by v_vec*eps_t -- exactly the
    discrete velocity the geodesic leapfrog integrates (U <- U exp(dt w)).  In vacuum both
    fields are the identity so w0 -> 0 there."""
    v_vec = np.asarray(v_vec, float)
    c0 = np.asarray(center, float)
    U0 = _hh(xs, tuple(c0), B_sign, prof)
    U1 = _hh(xs, tuple(c0 + v_vec * eps_t), B_sign, prof)
    w0 = s.q_log_vec(s.q_mul(s.q_conj(U0), U1)) / eps_t
    return s.q_normalize(U0), w0


def boosted_pair(xs, dx, d, v, b, prof, e_sk, eps_t=0.02,
                 B_signs=(+1, -1), seed=None, vac_noise=0.0):
    """Skyrmion(B_signs[0]) at (-d/2, -b/2, 0) moving +x with speed v, and
    anti-Skyrmion(B_signs[1]) at (+d/2, +b/2, 0) moving -x with speed v.

    The field is the quaternion PRODUCT U = U1 * U2 (vacuum=identity so far apart it is U1
    near soliton 1 and U2 near soliton 2; B_total = B1 + B2).  The velocity field is the
    finite-difference body angular velocity of the PRODUCT under the prescribed centre
    motion -- correct through the conjugation by U2, with no Lorentz gamma assumed.

    ``vac_noise`` adds a small random su(2) rotation to the vacuum (per-seed background)."""
    c1 = np.array([-d / 2.0, -b / 2.0, 0.0])
    c2 = np.array([+d / 2.0, +b / 2.0, 0.0])
    vx = np.array([v, 0.0, 0.0])

    U1 = _hh(xs, tuple(c1), B_signs[0], prof)
    U2 = _hh(xs, tuple(c2), B_signs[1], prof)
    U0 = s.q_mul(U1, U2)

    U1e = _hh(xs, tuple(c1 + vx * eps_t), B_signs[0], prof)
    U2e = _hh(xs, tuple(c2 - vx * eps_t), B_signs[1], prof)
    Ue = s.q_mul(U1e, U2e)
    w0 = s.q_log_vec(s.q_mul(s.q_conj(U0), Ue)) / eps_t

    if vac_noise > 0 and seed is not None:
        rng = np.random.default_rng(7000 + seed)
        axis = rng.standard_normal(U0.shape[:-1] + (3,))
        ang = vac_noise * rng.standard_normal(U0.shape[:-1])
        U0 = s.q_normalize(s.q_mul(U0, s.q_from_axis_angle(axis, ang)))

    return s.q_normalize(U0), w0


# =========================================================================== #
# Decisive observables: N_peaks (solitons) and baryon blobs (B=+1 vs B=-1 lumps)
# =========================================================================== #
# NOTE on robustness (see FL3-V): a boosted SU(2) field on the affordable lattice radiates
# short-wavelength noise the coarse grid cannot represent, which speckles the RAW energy and
# baryon densities (a raw peak/blob count explodes into the hundreds while the GLOBAL B
# integral stays conserved).  We therefore Gaussian-SMOOTH the density on the core scale
# before counting -- the same "cool/smear before counting the integer" trick E3b used.  A
# static-pair control then holds N_peaks=2 for the whole run, and a single Skyrmion holds
# N_peaks=1, so the smoothed count tracks genuine lumps, not lattice ripple.
SMOOTH_SIGMA = 1.0


def count_peaks(field, frac=0.30, footprint=5, sigma=SMOOTH_SIGMA):
    """Number of local maxima of a >=0 field (energy density) above frac*max after a
    Gaussian smoothing of width ``sigma`` (cells).  Each surviving maximum is one soliton
    lump.  Returns (count, list of (i,j,k) peak indices)."""
    from scipy.ndimage import maximum_filter, gaussian_filter
    f = np.asarray(field, float)
    if sigma:
        f = gaussian_filter(f, sigma, mode="nearest")
    thr = frac * float(f.max()) if f.max() > 0 else 0.0
    mx = maximum_filter(f, size=footprint, mode="nearest")
    idx = np.argwhere((f >= mx) & (f > thr))
    return int(idx.shape[0]), idx.tolist()


def count_blobs(b_density, frac=0.25, sigma=1.5):
    """Connected components of the POSITIVE and NEGATIVE baryon density above frac*|max|,
    after Gaussian smoothing (width ``sigma`` cells).  Returns (n_pos, n_neg): the number
    of B=+1 lumps and B=-1 lumps.  Creation => total (n_pos+n_neg) rises from 2 to 4 with
    the net sign content fixed."""
    from scipy.ndimage import label, gaussian_filter
    b = np.asarray(b_density, float)
    if sigma:
        b = gaussian_filter(b, sigma, mode="nearest")
    a = float(np.abs(b).max())
    if a <= 0:
        return 0, 0
    thr = frac * a
    _, n_pos = label(b > thr)
    _, n_neg = label(b < -thr)
    return int(n_pos), int(n_neg)


def energy_density_total(U, dx, e_sk):
    e2, e4 = s.chiral_energy_density(U, dx, e_sk)
    return e2 + e4


def topological_matter(b_density, dx, sigma=2.5):
    """Q_top = integral of |b| AFTER strong Gaussian smoothing (width ``sigma`` cells, well
    above the ~1-2 cell radiation wavelength).  This is the RADIATION-PROOF measure of how
    much localized topological matter is present: a single Skyrmion contributes ~1, two
    solitons ~2, a created pair would push it toward ~4, and annihilation into magnon
    radiation drives it toward ~0 (the smoothing cancels the sign-alternating radiation
    speckle that swamps a raw |b| integral or a blob count)."""
    from scipy.ndimage import gaussian_filter
    bs = gaussian_filter(np.asarray(b_density, float), sigma, mode="nearest")
    return float(np.sum(np.abs(bs)) * dx ** 3)


def soliton_diagnostics(U, dx, e_sk, frac_peak=0.30, frac_blob=0.25):
    """All decisive numbers at one instant: B (global charge), E (E2,E4,total), the
    radiation-proof topological-matter content Q_top, the smoothed lump counts."""
    e2, e4 = s.chiral_energy_density(U, dx, e_sk)
    e_tot = e2 + e4
    vol = dx ** 3
    n_peaks, _ = count_peaks(e_tot, frac=frac_peak)
    bdens = s.baryon_density(U, dx)
    n_pos, n_neg = count_blobs(bdens, frac=frac_blob)
    return {"B": s.baryon_number(U, dx),
            "E2": float(np.sum(e2) * vol), "E4": float(np.sum(e4) * vol),
            "E_field": float(np.sum(e_tot) * vol),
            "Q_top": topological_matter(bdens, dx),
            "n_peaks": n_peaks, "n_pos": n_pos, "n_neg": n_neg,
            "n_blobs": n_pos + n_neg}


# =========================================================================== #
# Fast ANALYTIC Skyrme gradient (single pass) + matching evolve loop
# =========================================================================== #
# su2_core._skyrme_grad is an 8-colour finite difference: 64 full-grid energy-density
# evaluations PER force call -> ~1 s/step even on a 29^3 grid, which makes a 20-seed
# collision ensemble intractable.  Here we differentiate the Skyrme density-sum
#   S4 = e_sk * sum_n sum_{i<j} |c_i x c_j|^2 ,   c_i = vec(U(n)^-1 U(n+i)) / dx
# analytically in ONE vectorised pass.  Validated against _skyrme_grad to ~1e-6 in
# validate_skyrme_grad() below (the engineering gate that licenses its use).
#
# Chain rule:  d|c_i x c_j|^2 / dc_i = 2 c_j x (c_i x c_j);  and c_i(n) = vec(A B)/dx with
# A=U(n)^-1=(u0,-u), B=U(n+i)=(b0,b):  c_i dx = u0 b - b0 u + u x b.  Differentiating this
# w.r.t. U(n) and U(n+i) gives the two scatter contributions below (the n+i piece is
# computed as a function of n and rolled +1 along axis i to land on site n+i).

def skyrme_grad_fast(U, dx, e_sk):
    """Ambient gradient d(S4-density-sum)/dU (per-site 4-vector), single vectorised pass."""
    _, cur = s.right_links(U, dx)
    cx, cy, cz = cur
    gxy = np.cross(cx, cy); gxz = np.cross(cx, cz); gyz = np.cross(cy, cz)
    Dx = 2.0 * (np.cross(cy, gxy) + np.cross(cz, gxz))
    Dy = 2.0 * (-np.cross(cx, gxy) + np.cross(cz, gyz))
    Dz = 2.0 * (-np.cross(cx, gxz) - np.cross(cy, gyz))
    G = np.zeros_like(U)
    u0 = U[..., 0]; uv = U[..., 1:]
    for ax, D in ((0, Dx), (1, Dy), (2, Dz)):
        Uup = np.roll(U, -1, axis=ax)           # U(n+i)
        b0 = Uup[..., 0]; bv = Uup[..., 1:]
        # contribution to gradient at site n (from c_i(n) via U(n))
        G[..., 0] += np.sum(bv * D, axis=-1) / dx
        G[..., 1:] += (-b0[..., None] * D - np.cross(D, bv)) / dx
        # contribution to gradient at site n+i (function of n, then shifted +1 along ax)
        fwd = np.empty_like(U)
        fwd[..., 0] = -np.sum(uv * D, axis=-1) / dx
        fwd[..., 1:] = (u0[..., None] * D + np.cross(D, uv)) / dx
        G += np.roll(fwd, +1, axis=ax)
    return e_sk * G


def chiral_force_fast(U, dx, e_sk):
    """Tangential acceleration = -grad(density-sum) projected onto S^3, using the ANALYTIC
    sigma staple (su2_core) + analytic Skyrme gradient.  Drop-in for su2_core.chiral_force
    but ~60x faster (no finite-difference loop)."""
    S = np.zeros_like(U)
    for ax in range(3):
        S = S + np.roll(U, -1, axis=ax) + np.roll(U, +1, axis=ax)
    g = -(2.0 / dx ** 2) * S
    if e_sk:
        g = g + skyrme_grad_fast(U, dx, e_sk)
    radial = np.sum(g * U, axis=-1, keepdims=True)
    return -(g - radial * U)


def _body_torque_fast(U, dx, e_sk):
    F = chiral_force_fast(U, dx, e_sk)
    return s.q_mul(s.q_conj(U), F)[..., 1:]


def chiral_evolve_fast(U0, w0, dx, dt, nsteps, e_sk, clamp_boundary=True, record_B=False):
    """Geodesic velocity-Verlet (identical scheme to su2_core.chiral_evolve) using the fast
    analytic force.  Returns (U, w, hist) with hist of (E_total[, B])."""
    U = s.q_normalize(U0.copy())
    w = np.asarray(w0, float).copy()
    tau = _body_torque_fast(U, dx, e_sk)
    hist = []
    for _ in range(nsteps):
        w = w + 0.5 * dt * tau
        ang = np.sqrt(np.sum(w * w, axis=-1)) * dt
        U = s.q_normalize(s.q_mul(U, s.q_from_axis_angle(w, ang)))
        if clamp_boundary:
            U = s._clamp_far(U)
        tau = _body_torque_fast(U, dx, e_sk)
        w = w + 0.5 * dt * tau
        E2, E4, Et = s.chiral_energy(U, dx, e_sk)
        Etot = Et + s.kinetic_energy(w, dx)
        hist.append((Etot, s.baryon_number(U, dx)) if record_B else (Etot,))
    return U, w, hist


def chiral_cool_fast(U, dx, e_sk, n_iter=300, rate=0.02, clamp_boundary=True):
    """Damped relaxation to the discrete LATTICE energy minimum using the fast analytic
    force (drop-in for su2_core.chiral_cool, ~60x faster).  The embedded radial profile is
    NOT a lattice minimum, so it breathes/radiates under evolution; cooling first makes the
    isolated Skyrmion a genuine static minimum (low energy drift, stable B in flight)."""
    U = s.q_normalize(U.copy())
    hist = []
    for _ in range(n_iter):
        F = chiral_force_fast(U, dx, e_sk)
        U = s.q_normalize(U + rate * F)
        if clamp_boundary:
            U = s._clamp_far(U)
        hist.append(s.chiral_energy(U, dx, e_sk)[2])
    return U, hist


def validate_skyrme_grad(N=7, e_sk=4.0, seed=0):
    """Engineering gate: the analytic Skyrme gradient must equal the TRUE per-site gradient
    of the engine's e4 density.  Reference = an explicit per-site central finite difference
    of the e4 density-sum (NOT su2_core._skyrme_grad, which is tangent-PROJECTED by its
    internal renormalisation and so legitimately differs by a radial component).  Returns
    the max rel diff vs the true gradient (should be ~1e-7)."""
    import itertools
    rng = np.random.default_rng(seed)
    xs, dx = cubic_grid(6.0, N)
    U = s.q_normalize(rng.standard_normal((N, N, N, 4)))

    def S4(Uf):
        return float(np.sum(s.chiral_energy_density(Uf, dx, e_sk)[1]))

    g_an = skyrme_grad_fast(U, dx, e_sk)
    eps = 1e-6
    g_bf = np.zeros_like(U)
    for n in itertools.product(range(N), repeat=3):
        for k in range(4):
            Up = U.copy(); Up[n + (k,)] += eps
            Um = U.copy(); Um[n + (k,)] -= eps
            g_bf[n + (k,)] = (S4(Up) - S4(Um)) / (2 * eps)
    scale = max(float(np.max(np.abs(g_bf))), 1e-30)
    return {"max_abs_diff": float(np.max(np.abs(g_bf - g_an))),
            "max_rel_diff": float(np.max(np.abs(g_bf - g_an)) / scale),
            "grad_scale": scale}


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, default=float))
    return path


if __name__ == "__main__":
    print("=" * 70)
    print("fl3_core smoke test")
    print("=" * 70)
    print(f"c (magnon, from E2)   : {C_MAGNON:.4f}")
    xs, dx = cubic_grid(L=18.0, N=45)
    prof = relaxed_profile(e_sk=4.0)
    lm = lattice_mass(18.0, 45, 4.0, prof)
    print(f"lattice M_Sk (e_sk=4) : {lm['M_lattice']:.2f}  B={lm['B']:+.3f}  dx={dx:.3f}")

    # isolated boosted Skyrmion: B and a single peak
    U, w = single_boosted(xs, dx, center=(-4, 0, 0), v_vec=(0.5 * C_MAGNON, 0, 0),
                          prof=prof, B_sign=+1)
    d0 = soliton_diagnostics(U, dx, 4.0)
    ke = s.kinetic_energy(w, dx)
    print(f"isolated boosted      : B={d0['B']:+.3f}  n_peaks={d0['n_peaks']}  "
          f"n_pos/n_neg={d0['n_pos']}/{d0['n_neg']}  KE={ke:.2f}")

    # the pair
    Up, wp = boosted_pair(xs, dx, d=8.0, v=0.5 * C_MAGNON, b=0.0, prof=prof, e_sk=4.0)
    dp = soliton_diagnostics(Up, dx, 4.0)
    print(f"pair (d=8,v=0.5c,b=0) : B_total={dp['B']:+.3f}  n_peaks={dp['n_peaks']}  "
          f"blobs +{dp['n_pos']}/-{dp['n_neg']}  KE={s.kinetic_energy(wp,dx):.2f}")

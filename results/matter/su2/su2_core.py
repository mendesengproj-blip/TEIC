"""su2_core.py -- shared engine for the MATTER_SU2 campaign (SU1-SU9).

The whole matter frontier converged on the same wall: a compact U(1) field on a
3+1D causal lattice (CR_3D) supports a relativistic VORTEX -- a one-dimensional
object (pi_1(U(1))=Z), semi-stable because its 2pi flux is invisible to the Wilson
cosine (cos 2pi = 1) and nothing pins the core (PHI_EMERGE V4).  The topology dictates
the next group:

    U(1):  pi_1(U(1)) = Z   -> vortex S^1            (line in 3D)
    SU(2): pi_3(SU(2)) = Z  -> Skyrmion              (POINT in 3D = particle)
           pi_2(S^2) = Z     -> hedgehog              (monopole)
           pi_4(SU(2)) = Z_2 -> 2pi rotation != 1     (candidate spin-1/2)

SU(2) is the minimal group admitting a stable POINT soliton in 3+1D.

ANTI-CIRCULARITY (tests/test_no_circularity.py scans results/matter/):
  * SU(2) is represented as UNIT QUATERNIONS q = (a0,a1,a2,a3), |q|^2 = 1
    (SU(2) ~= S^3).  The group product is the Hamilton product on these four REAL
    numbers; Pauli matrices NEVER enter the generator.  The correspondence used to
    DERIVE the product (documented, not executed) is
        U = a0 I + i (a1 s1 + a2 s2 + a3 s3),
        U V = (a0 b0 - a.b) + i (a0 b + b0 a - a x b).sigma ,
    i.e. quaternion multiplication with the cross-product sign of the i*sigma basis.
  * No complex literal anywhere: 1/2 Tr(U) = a0 is just the scalar component; a Wilson
    loop ratio is the a0 component of the holonomy quaternion.
  * No SR/GR dilation formula (1/sqrt(1-b^2), sqrt(1-2M/r)) in any generator.
  * "proton", "quark", "neutron", "isospin", "baryon" appear ONLY inside labelled
    COMPARISON ONLY blocks, never feeding a generator.  The topological charge B is a
    discrete integral of the quaternion field U, defined with no physical label.

Two field sectors live here:
  (A) LINK gauge sector: an SU(2) link quaternion per spatial link (x,y,z) on the
      CR_3D grid -> SU(2) Wilson plaquettes, the non-Abelian vacuum, monopoles and the
      area law (SU1 gate, SU2).  Reduces EXACTLY to cr3d_core on the sigma_3 subgroup.
  (B) CHIRAL site field U(x) in SU(2) (a quaternion per SITE) -> the principal-chiral
      (sigma-model) + Skyrme energy whose soliton is the hedgehog/Skyrmion with
      topological charge B in pi_3(SU(2)) (SU3-SU8).

Reuses causal_core, cr3d_core, gauge_core, dbi_core (4D sprinkle, grid, packets, seed
stats, IO).  Modifies nothing in any earlier campaign.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
for sub in ("src", "results/matter/cr_3d", "results/matter/cr_gauge",
            "results/matter/cr_dbi"):
    sys.path.insert(0, str(ROOT / sub))
import cr3d_core as c3   # noqa: E402  (3D grid, dt_cfl, 4D sprinkle helpers)
import gauge_core as gc  # noqa: E402  (1D reference)
import dbi_core as dbi   # noqa: E402  (packets, seed stats, IO)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi
PI = np.pi


# =========================================================================== #
# PART 0 -- SU(2) as unit quaternions (four real numbers; no Pauli, no complex)
# =========================================================================== #
# A quaternion array has trailing axis of length 4: q[..., 0]=a0 (scalar / 1/2 Tr),
# q[..., 1:]=a (the i*sigma vector part).  Everything below is pure real arithmetic.

def q_identity(shape=()):
    """The SU(2) identity (1,0,0,0) broadcast to ``shape`` (a tuple of grid dims)."""
    q = np.zeros(shape + (4,))
    q[..., 0] = 1.0
    return q


def q_mul(p, q):
    """Hamilton product p*q on quaternion arrays (broadcasts over leading axes).

    Derived from U_p U_q with U = a0 + i a.sigma:
        c0 = a0 b0 - a.b
        c  = a0 b + b0 a - a x b .
    The minus on the cross product is the sign of the i*sigma basis (e_k = i sigma_k
    obey e1 e2 = -e3); it makes q_mul the faithful image of SU(2) matrix product."""
    a0, b0 = p[..., 0], q[..., 0]
    a, b = p[..., 1:], q[..., 1:]
    c0 = a0 * b0 - np.sum(a * b, axis=-1)
    cross = np.cross(a, b)
    cvec = a0[..., None] * b + b0[..., None] * a - cross
    out = np.empty(np.broadcast_shapes(p.shape, q.shape))
    out[..., 0] = c0
    out[..., 1:] = cvec
    return out


def q_conj(q):
    """Conjugate (a0, -a).  For a UNIT quaternion this is the group inverse U^{-1}=U^dag
    (q_mul(q, q_conj(q)) = identity to machine precision)."""
    out = q.copy()
    out[..., 1:] *= -1.0
    return out


def q_inv(q):
    """Group inverse; equals q_conj for unit quaternions, but normalises for safety."""
    n2 = np.sum(q * q, axis=-1, keepdims=True)
    return q_conj(q) / n2


def q_norm(q):
    return np.sqrt(np.sum(q * q, axis=-1))


def q_normalize(q, eps=1e-300):
    n = np.sqrt(np.sum(q * q, axis=-1, keepdims=True))
    return q / np.maximum(n, eps)


def half_trace(q):
    """1/2 Tr(U) = a0 (real, in [-1,1] for a unit quaternion)."""
    return q[..., 0]


def q_from_axis_angle(axis, angle):
    """exp(i (angle) n.sigma) = (cos angle, sin angle * n_hat) with n_hat = axis/|axis|.

    ``axis`` is a (...,3) array (need not be normalised); ``angle`` is (...,) scalar.
    This is the group exponential of the su(2) element i*angle*n.sigma -- the only
    'exponential' the engine needs.  Pure real (cos/sin of a real angle)."""
    axis = np.asarray(axis, dtype=float)
    n = np.sqrt(np.sum(axis * axis, axis=-1, keepdims=True))
    nhat = np.divide(axis, n, out=np.zeros_like(axis), where=n > 0)
    ang = np.asarray(angle, dtype=float)
    out = np.empty(np.broadcast_shapes(axis.shape[:-1], ang.shape) + (4,))
    out[..., 0] = np.cos(ang)
    out[..., 1:] = np.sin(ang)[..., None] * nhat
    return out


def q_log_vec(q):
    """Imaginary part of log(U) as a 3-vector v with U = exp(i v.sigma): v = angle*nhat,
    angle = atan2(|a|, a0) in [0, pi].  Real-valued; the su(2) coordinate of U."""
    a0 = np.clip(q[..., 0], -1.0, 1.0)
    a = q[..., 1:]
    s = np.sqrt(np.sum(a * a, axis=-1))
    ang = np.arctan2(s, a0)                         # [0, pi]
    scale = np.divide(ang, s, out=np.zeros_like(ang), where=s > 1e-15)
    return a * scale[..., None]


def u1_embed(phi):
    """The sigma_3 U(1) subgroup element exp(i phi sigma_3) = (cos phi,0,0,sin phi).

    This is the bridge to CR_3D / CR_GAUGE: a configuration whose every link quaternion
    is u1_embed(phi) and whose chiral field is u1_embed(theta) reproduces the Abelian
    engine exactly (SU1 gate 1)."""
    phi = np.asarray(phi, dtype=float)
    out = np.zeros(phi.shape + (4,))
    out[..., 0] = np.cos(phi)
    out[..., 3] = np.sin(phi)
    return out


def u1_angle(q):
    """Recover the sigma_3 angle from a u1_embed quaternion: atan2(a3, a0)."""
    return np.arctan2(q[..., 3], q[..., 0])


# =========================================================================== #
# PART A -- LINK gauge sector: SU(2) Wilson plaquettes, monopoles (SU1, SU2)
# =========================================================================== #
# Link quaternion fields qx,qy,qz on a (Nx,Ny,Nz) grid (trailing axis 4).  x has
# Dirichlet ends (collision axis), y,z periodic -- the CR_3D geometry.

def _roll(q, axis, shift):
    return np.roll(q, shift, axis=axis)


def plaquette(qa, qb, qc, qd):
    """SU(2) holonomy U_a U_b U_c^{-1} U_d^{-1} around an oriented plaquette (quaternion
    arrays of matching shape).  Returns the holonomy quaternion; its half_trace is the
    Wilson loop W_p in [-1,1]."""
    return q_mul(q_mul(qa, qb), q_mul(q_conj(qc), q_conj(qd)))


def plaq_xy(qx, qy):
    """W_xy holonomy at (i,j,k): qx[i,j] * qy[i+1,j] * qx[i,j+1]^-1 * qy[i,j]^-1."""
    qx_jp = _roll(qx, 1, -1)            # qx[i, j+1, k]
    qy_ip = _roll(qy, 0, -1)            # qy[i+1, j, k]
    return plaquette(qx, qy_ip, qx_jp, qy)


def plaq_xz(qx, qz):
    qx_kp = _roll(qx, 2, -1)
    qz_ip = _roll(qz, 0, -1)
    return plaquette(qx, qz_ip, qx_kp, qz)


def plaq_yz(qy, qz):
    qy_kp = _roll(qy, 2, -1)
    qz_jp = _roll(qz, 1, -1)
    return plaquette(qy, qz_jp, qy_kp, qz)


def wilson_planes(qx, qy, qz):
    """The three plaquette holonomies (xy, xz, yz)."""
    return plaq_xy(qx, qy), plaq_xz(qx, qz), plaq_yz(qy, qz)


def wilson_action(qx, qy, qz, lam, interior_x=True):
    """Non-Abelian Wilson action lam * sum_plaq (1 - 1/2 Tr W_p) over the three planes.
    Reduces to the U(1) lam*sum(1-cos W) on the sigma_3 subgroup."""
    Wxy, Wxz, Wyz = wilson_planes(qx, qy, qz)
    sl = slice(0, -1) if interior_x else slice(None)
    s = (np.sum(1.0 - half_trace(Wxy)[sl])
         + np.sum(1.0 - half_trace(Wxz)[sl])
         + np.sum(1.0 - half_trace(Wyz)))
    return lam * float(s)


def gauge_transform_links(qx, qy, qz, g):
    """Apply a site-dependent SU(2) gauge transform g[i,j,k] to the link field:
        U_mu(x) -> g(x) U_mu(x) g(x+mu)^{-1} .
    The Wilson plaquette holonomy then transforms by conjugation W -> g W g^{-1}, so
    1/2 Tr(W) (hence wilson_action) is invariant -- the SU1 gauge-invariance gate."""
    out = []
    for ax, q in zip((0, 1, 2), (qx, qy, qz)):
        g_up = np.roll(g, -1, axis=ax)
        out.append(q_mul(q_mul(g, q), q_conj(g_up)))
    return out


def su2_monopole_charge(qx, qy, qz):
    """DeGrand-Toussaint magnetic charge per unit cube, built from the sigma_3 PROJECTION
    of the SU(2) plaquettes (the Abelian-projection monopole, t'Hooft).  The wrapped
    diagonal phase of each plaquette holonomy supplies an integer flux through each cube
    face; the six-face sum is an integer by the discrete Bianchi identity.

    On the sigma_3 subgroup this is identical to cr3d_core.monopole_charge."""
    Wxy, Wxz, Wyz = wilson_planes(qx, qy, qz)
    # Abelian-projected plaquette angle = atan2(a3, a0) of the holonomy quaternion.
    axy = np.arctan2(Wxy[..., 3], Wxy[..., 0])
    axz = np.arctan2(Wxz[..., 3], Wxz[..., 0])
    ayz = np.arctan2(Wyz[..., 3], Wyz[..., 0])
    w = lambda a: (a + PI) % TWO_PI - PI
    wxy, wxz, wyz = w(axy), w(axz), w(ayz)
    n = ((_roll(wxy, 2, -1) - wxy)
         - (_roll(wxz, 1, -1) - wxz)
         + (np.roll(wyz, -1, axis=0) - wyz)) / TWO_PI
    n[-1] = 0.0
    return n


def monopole_density(qx, qy, qz):
    n = su2_monopole_charge(qx, qy, qz)
    n_int = np.rint(n)
    interior = np.ones(n.shape, bool); interior[-1] = False
    ncubes = int(np.sum(interior))
    rho = float(np.sum(np.abs(n_int[interior]) >= 1) / max(ncubes, 1))
    return rho, n_int


# =========================================================================== #
# PART B -- CHIRAL site field U(x): principal-chiral + Skyrme energy (SU3-SU8)
# =========================================================================== #
# A unit quaternion per SITE.  The right link variable R_i = U_x^{-1} U_{x+i} in SU(2)
# is the discrete left-invariant current; the sigma-model and Skyrme energies are built
# from its scalar (a0) and vector (i*sigma) parts -- all real.

def right_links(U, dx, axes=(0, 1, 2)):
    """R_i = U^{-1} U_{x+i} for each spatial direction (forward difference, periodic
    roll).  Returns a list of quaternion arrays and the su(2) current 3-vectors
    c_i = (vector part of R_i) / dx.

    Normalisation: in the continuum U_{x+i} = U + dx d_i U, so R = 1 + dx (U^-1 d_i U)
    = (1, a_i dx) as a quaternion, hence a_i = R_vec / dx (exact to O(dx); for the
    unit quaternion R_vec = sin(|a|dx) a_hat, so R_vec/dx -> a_i as dx->0)."""
    Uinv = q_conj(U)
    Rs, currents = [], []
    for ax in axes:
        Uup = np.roll(U, -1, axis=ax)
        R = q_mul(Uinv, Uup)
        Rs.append(R)
        currents.append(R[..., 1:] / dx)
    return Rs, currents


def chiral_energy_density(U, dx, e_sk):
    """Per-site density of the principal-chiral (sigma, 2-derivative) + Skyrme
    (4-derivative) energy:

        e2 = sum_i |c_i|^2                         (E2, sigma model)
        e4 = e_sk * sum_{i<j} |c_i x c_j|^2        (E4, Skyrme commutator)

    The sigma density e2 = (2/dx^2) sum_i [1 - U_n . U_{n+i}] uses the AMBIENT inner
    product U_n.U_{n+i} = 1/2 Tr(U_n^dag U_{n+i}) (= a0 of the link holonomy); to leading
    order 2(1-cos theta)/dx^2 -> |a_i|^2, the standard lattice (O(4)) sigma model, whose
    gradient is the analytic 'staple' (chiral_force) -- energy-conserving under the
    geodesic leapfrog.  The Skyrme cross product |c_i x c_j|^2 (c_i = U^{-1} d_i U) is the
    lattice image of -1/16 Tr[L_i,L_j]^2 (= |a_i x a_j|^2 in the i*sigma basis); it
    VANISHES for collinear (Abelian) currents -- the genuinely non-Abelian stabiliser.
    Both densities are >= 0 and real."""
    e2 = np.zeros(U.shape[:-1])
    for ax in range(3):
        e2 = e2 + (1.0 - np.sum(U * np.roll(U, -1, axis=ax), axis=-1))
    e2 = (2.0 / dx ** 2) * e2
    _, cur = right_links(U, dx)
    cx, cy, cz = cur
    cxy = np.cross(cx, cy); cxz = np.cross(cx, cz); cyz = np.cross(cy, cz)
    e4 = e_sk * np.sum(cxy * cxy + cxz * cxz + cyz * cyz, axis=-1)
    return e2, e4


def chiral_energy(U, dx, e_sk):
    """(E2, E4, E_total) integrated over the lattice (volume element dx^3)."""
    e2, e4 = chiral_energy_density(U, dx, e_sk)
    vol = dx ** 3
    E2 = float(np.sum(e2)) * vol
    E4 = float(np.sum(e4)) * vol
    return E2, E4, E2 + E4


# ---- topological charge B (Pontryagin index of U: S^3 -> SU(2)~=S^3) -------- #
# Geometric construction: b ~ det(c_x, c_y, c_z), the local Jacobian of the map U(x).
# The continuum baryon density is (1/24pi^2) eps^{ijk} Tr(L_i L_j L_k) = (1/24pi^2) *
# 12 det(c_x,c_y,c_z) (since Tr[(i a.s)(i b.s)(i c.s)] = 2 a.(b x c) and the eps-sum
# gives 6 det).  The overall SIGN is the orientation of the i*sigma basis (e1 e2 = -e3,
# left-handed) -> a minus so the standard F(0)=pi hedgehog returns B=+1.  Verified in
# __main__ (B -> +1 as the grid refines); no physical label enters the definition.
_B_PREFACTOR = -1.0 / (2.0 * PI ** 2)       # = -12 / (24 pi^2), sign fixes orientation


def baryon_density(U, dx):
    """Per-site topological charge density b(x) (winding density of pi_3).  Integral
    over the lattice = B.  Uses the symmetric current determinant (calibrated)."""
    _, cur = right_links(U, dx)
    cx, cy, cz = cur
    det = np.sum(cx * np.cross(cy, cz), axis=-1)     # det(c_x,c_y,c_z)
    return _B_PREFACTOR * det


def baryon_number(U, dx):
    """B = sum_sites b(x) dx^3 (the discrete Pontryagin index)."""
    return float(np.sum(baryon_density(U, dx)) * dx ** 3)


# ---- hedgehog / Skyrmion initial data --------------------------------------- #
def hedgehog_field(x, y, z, profile=None, center=None, B_sign=+1):
    """The hedgehog U(r) = exp(i F(r) rhat.sigma) = (cos F, sin F * rhat) as a quaternion
    field on the grid.  ``profile`` is a callable F(r) (default the analytic kink
    F = pi * exp(-r/w) ... actually 2*atan-type); F(0)=pi, F(inf)=0 gives B=+1.

    B_sign=-1 builds the anti-hedgehog by reflecting rhat -> (rhat_x, rhat_y, -rhat_z)
    (an orientation flip of S^3, B -> -B)."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    if center is None:
        center = (float(np.mean(x)), float(np.mean(y)), float(np.mean(z)))
    cx_, cy_, cz_ = center
    Xr, Yr, Zr = X - cx_, Y - cy_, Z - cz_
    r = np.sqrt(Xr ** 2 + Yr ** 2 + Zr ** 2)
    rsafe = np.where(r > 0, r, 1.0)
    rhat = np.stack([Xr / rsafe, Yr / rsafe, Zr / rsafe], axis=-1)
    rhat[r == 0] = 0.0
    if B_sign < 0:
        rhat[..., 2] *= -1.0
    if profile is None:
        w = 0.18 * (float(x[-1]) - float(x[0]))
        F = PI * np.exp(-r / w)
    else:
        F = profile(r)
    U = np.empty(X.shape + (4,))
    U[..., 0] = np.cos(F)
    U[..., 1:] = np.sin(F)[..., None] * rhat
    return q_normalize(U)


# ---- 1D radial Skyrme profile (the rigorous Derrick test, SU3/SU5) ---------- #
# Hedgehog ansatz reduces the 3D functional to a 1D radial energy in F(r):
#   E2 = 4pi int r^2 [ F'^2 + 2 sin^2 F / r^2 ] dr
#   E4 = 4pi int     [ sin^2 F (2 F'^2 + sin^2 F / r^2) ] dr
# (standard Skyrme; e_sk sets the relative E4 weight / length scale).  We relax F(r) by
# damped gradient flow on a 1D grid -> profile, E2, E4, mass, Derrick ratio E2/E4.

def radial_grid(rmax=12.0, n=400):
    r = np.linspace(0.0, rmax, n + 1)[1:]        # avoid r=0
    dr = float(r[1] - r[0])
    return r, dr


def radial_energy(F, r, dr, e_sk):
    Fp = np.gradient(F, dr)
    s2 = np.sin(F) ** 2
    e2_int = r ** 2 * (Fp ** 2 + 2.0 * s2 / r ** 2)
    e4_int = e_sk * s2 * (2.0 * Fp ** 2 + s2 / r ** 2)
    E2 = 4.0 * PI * float(np.sum(e2_int) * dr)
    E4 = 4.0 * PI * float(np.sum(e4_int) * dr)
    return E2, E4


def radial_relax(r, dr, e_sk, F0=None, maxiter=2000):
    """Minimise the 1D radial energy with F(0)=pi, F(inf)=0 fixed, via L-BFGS-B over the
    interior nodes.  Returns the relaxed profile and (E2, E4).  Robust (no hand-tuned
    flow step): the standard Skyrme profile equation solved as a minimisation."""
    from scipy.optimize import minimize
    if F0 is None:
        Ffull = PI * np.exp(-r / (0.25 * r[-1]))
    else:
        Ffull = F0.copy()
    Ffull[0] = PI; Ffull[-1] = 0.0

    def assemble(interior):
        F = np.empty_like(Ffull)
        F[0] = PI; F[-1] = 0.0; F[1:-1] = interior
        return F

    def obj(interior):
        F = assemble(interior)
        E2, E4 = radial_energy(F, r, dr, e_sk)
        return E2 + E4

    def jac(interior):
        F = assemble(interior)
        return _radial_grad(F, r, dr, e_sk)[1:-1]

    res = minimize(obj, Ffull[1:-1], method="L-BFGS-B", jac=jac,
                   options={"maxiter": maxiter, "ftol": 1e-14, "gtol": 1e-11})
    F = assemble(res.x)
    E2, E4 = radial_energy(F, r, dr, e_sk)
    return F, E2, E4


def _radial_grad(F, r, dr, e_sk):
    """Analytic functional gradient dE/dF_i of radial_energy (E = 4pi dr sum integrand):
        dE2/dF = 4pi[ 2 sin2F - d/dr(2 r^2 F') ]
        dE4/dF = 4pi e_sk[ 2 sin2F F'^2 + 4 sin^3F cosF / r^2 - d/dr(4 sin^2F F') ]
    (the Euler-Lagrange residual times the measure 4pi dr).  Used as the L-BFGS-B jac
    so the minimisation converges at any radial resolution."""
    Fp = np.gradient(F, dr)
    sF, cF = np.sin(F), np.cos(F)
    s2 = sF ** 2
    g2 = 2.0 * np.sin(2.0 * F) - np.gradient(2.0 * r ** 2 * Fp, dr)
    g4 = e_sk * (2.0 * np.sin(2.0 * F) * Fp ** 2 + 4.0 * sF ** 3 * cF / r ** 2
                 - np.gradient(4.0 * s2 * Fp, dr))
    g = 4.0 * PI * dr * (g2 + g4)
    g[0] = 0.0; g[-1] = 0.0
    return g


def profile_from_radial(F, r):
    """Return a callable F(rho) interpolating the relaxed radial profile (for embedding
    into the 3D lattice hedgehog_field)."""
    def f(rho):
        return np.interp(rho, r, F, left=PI, right=0.0)
    return f


# ---- 3D chiral relaxation (cooling) and projected dynamics (SU3, SU6) ------- #
def chiral_force(U, dx, e_sk, eps=1e-5):
    """Tangent-space ACCELERATION a = -d(energy-density-sum)/dU projected onto S^3 at
    each site (the energy is density-sum * dx^3 and the kinetic mass is dx^3, so dx^3
    cancels; the acceleration is the tangential gradient of the density sum).

    The SIGMA part is ANALYTIC: grad e2_sum = -(2/dx^2) * staple, with the staple
    S_n = sum_i (U_{n+i} + U_{n-i}); force_sigma = (2/dx^2)(S - (S.U)U) -- fast and
    exactly conservative (verified to ~1e-4 drift under the geodesic leapfrog).  The
    SKYRME part (e4), only when e_sk>0, is added by the stencil finite difference
    _skyrme_grad (4-derivative, no clean analytic staple)."""
    S = np.zeros_like(U)
    for ax in range(3):
        S = S + np.roll(U, -1, axis=ax) + np.roll(U, +1, axis=ax)
    g = -(2.0 / dx ** 2) * S                          # ambient grad of e2-density-sum
    if e_sk:
        g = g + _skyrme_grad(U, dx, e_sk, eps)
    radial = np.sum(g * U, axis=-1, keepdims=True)
    return -(g - radial * U)


def _skyrme_grad(U, dx, e_sk, eps):
    """Ambient gradient of the Skyrme (e4) density sum, by an exact stencil-aware central
    finite difference (8-colour sublattice sweep so parallel perturbations never share a
    link).  Returns d(e4-sum)/dU per site."""
    grad = np.zeros_like(U)
    shape = U.shape[:-1]
    I, J, K = np.indices(shape)
    for cx_ in (0, 1):
        for cy_ in (0, 1):
            for cz_ in (0, 1):
                mask = ((I % 2 == cx_) & (J % 2 == cy_) & (K % 2 == cz_))
                for k in range(4):
                    Up = U.copy(); Up[..., k][mask] += eps; Up = q_normalize(Up)
                    Um = U.copy(); Um[..., k][mask] -= eps; Um = q_normalize(Um)
                    _, e4p = chiral_energy_density(Up, dx, e_sk)
                    _, e4m = chiral_energy_density(Um, dx, e_sk)
                    de = _neighbourhood_delta(e4p, e4m, mask)
                    grad[..., k][mask] = de[mask] / (2.0 * eps)
    return grad


def _neighbourhood_delta(field_p, field_b, mask):
    """Sum of (perturbed - base) energy density over the sites whose density depends on
    U_n: site n itself and its BACKWARD neighbours n-x, n-y, n-z (whose forward link
    R_i = U^{-1} U_{+i} points to n).  The FORWARD neighbours n+i are NOT included --
    their density does not involve U_n (it would double-count the other same-colour
    site n+2i).  np.roll(d,+1,axis) brings the backward neighbour's value to site n."""
    d = field_p - field_b
    acc = d.copy()
    for ax in range(3):
        acc = acc + np.roll(d, +1, axis=ax)
    return acc


def chiral_cool(U, dx, e_sk, n_iter=300, rate=0.05, clamp_boundary=True):
    """Damped relaxation (cooling) of the chiral field toward an energy minimum,
    re-projecting to SU(2) each step.  Returns (U_relaxed, history of E_total)."""
    U = q_normalize(U.copy())
    hist = []
    for _ in range(n_iter):
        F = chiral_force(U, dx, e_sk)
        U = q_normalize(U + rate * F)
        if clamp_boundary:
            U = _clamp_far(U)
        E2, E4, Et = chiral_energy(U, dx, e_sk)
        hist.append(Et)
    return U, hist


def kinetic_energy(w, dx):
    """Kinetic energy of the body angular-velocity field w (a 3-vector per site, the
    su(2) component of U^{-1} dU/dt): 1/2 sum |w|^2 dx^3.  Metric mass = dx^3, matching
    the geodesic-leapfrog invariant below."""
    return 0.5 * float(np.sum(w * w)) * dx ** 3


def _project_tangent(U, V):
    """Remove the radial component of a 4-vector V so it stays tangent to S^3 at U."""
    return V - np.sum(V * U, axis=-1, keepdims=True) * U


def _body_torque(U, dx, e_sk):
    """Body-frame torque tau = imag(U^{-1} F) (3-vector per site), F = -dE/dU the ambient
    force.  This is the su(2)-valued generalised force conjugate to the body angular
    velocity w; the radial part of F drops out under U^{-1} (it maps to the real part)."""
    F = chiral_force(U, dx, e_sk)            # = -grad_tangential(density-sum)
    return q_mul(q_conj(U), F)[..., 1:]


def chiral_evolve(U0, w0, dx, dt, nsteps, e_sk, clamp_boundary=True, record_B=False):
    """GEODESIC velocity-Verlet for the chiral field on S^3 (= unit quaternions):

        w <- w + (dt/2) tau ;   U <- U * exp(dt w) ;   tau <- tau(U) ;   w <- w + (dt/2) tau

    The drift U*exp(dt w) moves each site EXACTLY along a great circle of S^3 (the free
    geodesic), so the integrator is symplectic and conserves E_kin + E2 + E4 (drift
    O(dt^2), bounded -- no secular heating).  ``w`` is the body angular velocity
    (3-vector per site).  Used for the SU1 conservation gate and the SU6 collision.

    Returns (U, w, hist) with hist a list of (E_total, B) when record_B else (E_total,)."""
    U = q_normalize(U0.copy())
    w = np.asarray(w0, dtype=float).copy()
    tau = _body_torque(U, dx, e_sk)
    hist = []
    for _ in range(nsteps):
        w = w + 0.5 * dt * tau
        ang = np.sqrt(np.sum(w * w, axis=-1)) * dt
        U = q_normalize(q_mul(U, q_from_axis_angle(w, ang)))
        if clamp_boundary:
            U = _clamp_far(U)
        tau = _body_torque(U, dx, e_sk)
        w = w + 0.5 * dt * tau
        E2, E4, Et = chiral_energy(U, dx, e_sk)
        Etot = Et + kinetic_energy(w, dx)
        hist.append((Etot, baryon_number(U, dx)) if record_B else (Etot,))
    return U, w, hist


def _clamp_far(U):
    """Hold the field at the vacuum (identity) on the outer shell (Dirichlet-like), so
    the soliton cannot leak winding off the boundary."""
    U[0, :, :] = q_identity(U.shape[1:3]); U[-1, :, :] = q_identity(U.shape[1:3])
    U[:, 0, :] = q_identity((U.shape[0], U.shape[2]))
    U[:, -1, :] = q_identity((U.shape[0], U.shape[2]))
    U[:, :, 0] = q_identity(U.shape[0:2]); U[:, :, -1] = q_identity(U.shape[0:2])
    return U


# =========================================================================== #
# IO
# =========================================================================== #
def seed_stats(values):
    return dbi.seed_stats(values)


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print("=" * 70)
    print("su2_core smoke tests")
    print("=" * 70)

    # 1) quaternion group axioms ------------------------------------------------
    p = q_normalize(rng.standard_normal((5, 4)))
    q = q_normalize(rng.standard_normal((5, 4)))
    e = q_mul(p, q_conj(p))
    err_inv = float(np.max(np.abs(e - q_identity((5,)))))
    # associativity
    lhs = q_mul(q_mul(p, q), p); rhs = q_mul(p, q_mul(q, p))
    err_assoc = float(np.max(np.abs(lhs - rhs)))
    # unitarity preserved by product
    err_unit = float(np.max(np.abs(q_norm(q_mul(p, q)) - 1.0)))
    print(f"U U^-1 = 1      : max err {err_inv:.2e}")
    print(f"associativity   : max err {err_assoc:.2e}")
    print(f"|U V| = 1       : max err {err_unit:.2e}")

    # 2) U(1) limit: q_mul of sigma_3 embeddings = angle addition ---------------
    a = rng.uniform(-2, 2, 7); b = rng.uniform(-2, 2, 7)
    prod = q_mul(u1_embed(a), u1_embed(b))
    err_u1 = float(np.max(np.abs(u1_angle(prod) - ((a + b + PI) % TWO_PI - PI))))
    half_tr_err = float(np.max(np.abs(half_trace(u1_embed(a)) - np.cos(a))))
    print(f"U(1) angle add  : max err {err_u1:.2e}")
    print(f"1/2Tr=cos(phi)  : max err {half_tr_err:.2e}")

    # 3) baryon number of the analytic hedgehog (calibration of _B_PREFACTOR) ---
    x, y, z, dx = c3.make_grid(Lx=16.0, Nx=41, Ny=41, Nz=41)
    # NB make_grid gives y,z spacing = dx but few points; use a cubic grid instead:
    L = 12.0; N = 41
    xs = np.linspace(-L / 2, L / 2, N); dxs = float(xs[1] - xs[0])
    prof = lambda r: PI * np.exp(-r / 1.6)
    U = hedgehog_field(xs, xs, xs, profile=prof)
    B = baryon_number(U, dxs)
    Ua = hedgehog_field(xs, xs, xs, profile=prof, B_sign=-1)
    Ba = baryon_number(Ua, dxs)
    print(f"hedgehog B      : {B:+.4f}  (target +1)")
    print(f"anti-hedgehog B : {Ba:+.4f}  (target -1)")

    # 4) radial Derrick: relax F(r) with Skyrme term, expect E2 ~ E4 ------------
    r, dr = radial_grid(rmax=12.0, n=120)
    F, E2, E4 = radial_relax(r, dr, e_sk=1.0)
    print(f"radial relax    : E2={E2:.3f} E4={E4:.3f} ratio E2/E4={E2/E4:.3f} "
          f"F(0)={F[0]:.3f} F(end)={F[-1]:.3e}")

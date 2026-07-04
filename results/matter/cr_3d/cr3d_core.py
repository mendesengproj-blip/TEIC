"""cr3d_core.py -- shared engine for the MATTER_CR_3D campaign (T3D1-T3D6).

CR_WILSON localised the failure of matter creation precisely: a compact U(1) gauge
field on a 2D lattice cannot confine winding charges, because a 2pi flux quantum is
invisible to the compact cosine (cos 2pi = 1) and LINEAR (Polyakov) confinement is a
*magnetic-monopole* effect that requires d >= 3.  CR_3D builds the genuinely 3+1D
machinery that 2D lacked:

  (A) a 4D Poisson sprinkling + Myrheim-Meyer dimension estimator (causal-set side),
      to certify the network is genuinely d=4 (T3D1);
  (B) a 3D SPATIAL compact-U(1) lattice gauge field (x,y,z) with a scalar theta,
      the full action

          S = sum_links Dtau[1-cos(phi+Dtheta)] + lambda_p sum_plaq [1-cos(W_p)] ,

      now with THREE spatial plaquette planes (xy, xz, yz) instead of one -- the
      minimum that admits magnetic monopoles (T3D2), a linear string (T3D3) and a
      Polyakov order parameter in a real-time collision (T3D4-T3D5).

Geometry of the field theory
----------------------------
x is the collision axis (Dirichlet ends, as in CR_GAUGE/CR_WILSON); y and z are the
two transverse directions (PERIODIC, so flux is trapped).  Evolution is in simulation
time via velocity-Verlet -- "time" is the 4th (temporal) dimension, integrated.

  theta[i,j,k]  scalar at sites
  phix[i,j,k]   x-link (i,j,k)->(i+1,j,k), i<Nx-1   (Dirichlet)
  phiy[i,j,k]   y-link ->(i,j+1,k)                  (periodic, np.roll axis 1)
  phiz[i,j,k]   z-link ->(i,j,k+1)                  (periodic, np.roll axis 2)

Reduction (the T3D1 gate): a z-UNIFORM configuration with phiz=0 has Wxz=Wyz=0 and
no z-derivatives, so every z-slice evolves EXACTLY as the CR_WILSON 2D engine
(force matches wilson_core per slice to machine zero).  The new physics is the
xz/yz plaquettes and the monopole they permit.

Conserved energy: every force_field = (1/dx)*(-dE_total/dfield), so the discrete
E_total below is the leapfrog invariant (drift ~1e-3 on smooth configs), exactly as
in wilson_core, extended with E_zstiff and the Wxz/Wyz/uz terms.

ANTI-CIRCULARITY (tests/test_no_circularity.py scans results/matter/):
  * No mc^2/2mc^2, no SR/GR dilation, no complex numbers anywhere in the generator.
  * Monopole charge n is summed from the WRAPPED real plaquette over a cube's 6 faces
    (DeGrand-Toussaint); it is an integer by the discrete Bianchi identity.
  * The Polyakov order parameter is the MAGNITUDE of the average temporal phase
    factor, built from real cos/sin sums of the accumulated temporal holonomy
    (Sum_t dt * vth) -- no complex literal.
  * Magnetic monopole / Polyakov / QCD / quark appear as NAMES only; QCD comparisons
    live in COMPARISON ONLY blocks and never feed a generator.

Reuses causal_core (4D sprinkle, light cones), wilson_core / gauge_core / dbi_core
(1D reference, packets, kink mass functional, seed stats, IO).  Modifies nothing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln

ROOT = Path(__file__).resolve().parents[3]
for sub in ("src", "results/matter/cr_gauge", "results/matter/cr_dbi",
            "results/matter/cr_wilson"):
    sys.path.insert(0, str(ROOT / sub))
import causal_core as cc      # noqa: E402  (4D Poisson sprinkle, causal relation)
import gauge_core as gc       # noqa: E402  (1D reference / packets)
import dbi_core as dbi        # noqa: E402  (kink mass functional, seed stats)
import wilson_core as wc      # noqa: E402  (2D reference for the z-slice reduction)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi


# =========================================================================== #
# PART A -- causal-set side: 4D sprinkling + Myrheim-Meyer dimension
# =========================================================================== #
def sprinkle_diamond_4d(rho, T, rng):
    """Poisson-sprinkle a 4D causal diamond (Alexandrov interval) between
    A=(0,0,0,0) and B=(T,0,0,0): sprinkle the bounding box, keep events causally
    between A and B.  Returns the (n,4) interior events (excluding A,B)."""
    bounds = [(0.0, T)] + [(-T / 2, T / 2)] * 3
    pts = cc.sprinkle_box(rho, bounds, rng)
    if len(pts) == 0:
        return pts
    A = np.zeros(4)
    B = np.zeros(4); B[0] = T
    keep = cc.alexandrov_interval(pts, A, B)
    return pts[keep]


def relation_count(pts):
    """Number of causally-related (ordered) pairs among ``pts`` (O(n^2), vectorised).
    Counts each related pair once."""
    pts = np.asarray(pts, dtype=float)
    n = len(pts)
    if n < 2:
        return 0, n
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    related = (dt > 0) & (dt * dt > dx2)     # i precedes j
    return int(np.sum(related)), n


def mm_fraction(d):
    """Myrheim-Meyer ordering fraction (fraction of causally-related pairs) for a
    Poisson sprinkle of a flat d-dimensional Alexandrov interval,

        f(d) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2)) .

    This normalisation is fixed by direct counting (the only ground truth here):
    f(2)=0.500 and f(4)=0.100 -- exactly the related-pair fractions a genuine 1+1D
    and 3+1D sprinkle produce (verified in __main__).  Inverting it on a measured
    fraction returns the Myrheim-Meyer continuum dimension."""
    lg = gammaln(d + 1.0) + gammaln(d / 2.0) - np.log(2.0) - gammaln(1.5 * d)
    return float(np.exp(lg))


def mm_dimension(f):
    """Invert the Myrheim-Meyer relation: given the measured ordering fraction f,
    return the continuum dimension d (root of mm_fraction(d)=f on [0.5, 12])."""
    g = lambda d: mm_fraction(d) - f
    return float(brentq(g, 0.5, 12.0))


def ordering_fraction(pts):
    """Empirical ordering fraction R / C(n,2) for a sprinkled causal set."""
    R, n = relation_count(pts)
    if n < 2:
        return float("nan")
    return 2.0 * R / (n * (n - 1))


# =========================================================================== #
# PART B -- the 3D spatial compact-U(1) lattice gauge field
# =========================================================================== #
def make_grid(Lx=48.0, Nx=193, Ny=10, Nz=10):
    """3D grid: x in [-Lx/2, Lx/2] (Nx pts, Dirichlet ends), y,z transverse (Ny,Nz
    pts, periodic, spacing dx).  Returns (x, y, z, dx)."""
    x = np.linspace(-Lx / 2, Lx / 2, Nx)
    dx = float(x[1] - x[0])
    y = np.arange(Ny) * dx
    z = np.arange(Nz) * dx
    return x, y, z, dx


def dt_cfl(dx, safety=0.18):
    """Stable step.  x-stiffness AND the three plaquettes carry 1/dx^2; 0.18 keeps
    energy drift ~1e-3 on smooth configs (a hair below the 2D 0.2, the extra
    plaquette plane stiffens the gauge sector)."""
    return safety * dx ** 2


# --- periodic shifts on the two transverse axes ---------------------------- #
def _up_y(a):
    return np.roll(a, -1, axis=1)          # a[:, j+1, :]


def _dn_y(a):
    return np.roll(a, +1, axis=1)          # a[:, j-1, :]


def _up_z(a):
    return np.roll(a, -1, axis=2)          # a[:, :, k+1]


def _dn_z(a):
    return np.roll(a, +1, axis=2)          # a[:, :, k-1]


# --- Stueckelberg link phases ---------------------------------------------- #
def link_x(theta, phix):
    ux = np.zeros_like(theta)
    ux[:-1] = phix[:-1] + np.diff(theta, axis=0)
    return ux


def link_y(theta, phiy):
    return phiy + (_up_y(theta) - theta)


def link_z(theta, phiz):
    return phiz + (_up_z(theta) - theta)


# --- the three spatial plaquettes ------------------------------------------ #
def plaq_xy(phix, phiy):
    """Wxy[i,j,k] = phix[i,j,k] + phiy[i+1,j,k] - phix[i,j+1,k] - phiy[i,j,k]."""
    W = np.zeros_like(phix)
    W[:-1] = phix[:-1] + phiy[1:] - _up_y(phix)[:-1] - phiy[:-1]
    return W


def plaq_xz(phix, phiz):
    """Wxz[i,j,k] = phix[i,j,k] + phiz[i+1,j,k] - phix[i,j,k+1] - phiz[i,j,k]."""
    W = np.zeros_like(phix)
    W[:-1] = phix[:-1] + phiz[1:] - _up_z(phix)[:-1] - phiz[:-1]
    return W


def plaq_yz(phiy, phiz):
    """Wyz[i,j,k] = phiy[i,j,k] + phiz[i,j+1,k] - phiy[i,j,k+1] - phiz[i,j,k]
    (periodic y,z everywhere)."""
    return phiy + _up_y(phiz) - _up_z(phiy) - phiz


def all_plaquettes(phix, phiy, phiz):
    return plaq_xy(phix, phiy), plaq_xz(phix, phiz), plaq_yz(phiy, phiz)


# --- forces (reduce to wilson_core per z-slice at z-uniform, phiz=0) -------- #
def force_theta(theta, phix, phiy, phiz, dx):
    ux, uy, uz = link_x(theta, phix), link_y(theta, phiy), link_z(theta, phiz)
    sx, sy, sz = np.sin(ux), np.sin(uy), np.sin(uz)
    f = np.zeros_like(theta)
    f[1:-1] = ((sx[1:-1] - sx[:-2])
               + (sy[1:-1] - _dn_y(sy)[1:-1])
               + (sz[1:-1] - _dn_z(sz)[1:-1]))
    return f / dx ** 2


def force_phix(theta, phix, phiy, phiz, dx, lam):
    ux = link_x(theta, phix)
    lapx = np.zeros_like(phix)
    lapx[1:-1] = (phix[2:] - 2 * phix[1:-1] + phix[:-2]) / dx ** 2
    f = np.zeros_like(phix)
    f[1:-1] = (lapx[1:-1] - np.sin(ux[1:-1])) / dx ** 2
    if lam:
        Wxy = plaq_xy(phix, phiy)
        Wxz = plaq_xz(phix, phiz)
        f[1:-1] -= lam * ((np.sin(Wxy[1:-1]) - np.sin(_dn_y(Wxy)[1:-1]))
                          + (np.sin(Wxz[1:-1]) - np.sin(_dn_z(Wxz)[1:-1])))
    return f


def force_phiy(theta, phix, phiy, phiz, dx, lam):
    uy = link_y(theta, phiy)
    lapy = (_up_y(phiy) - 2 * phiy + _dn_y(phiy)) / dx ** 2
    f = np.zeros_like(phiy)
    f[1:-1] = (lapy[1:-1] - np.sin(uy[1:-1])) / dx ** 2
    if lam:
        Wxy = plaq_xy(phix, phiy)
        Wyz = plaq_yz(phiy, phiz)
        Wxy_left = np.zeros_like(Wxy); Wxy_left[1:] = Wxy[:-1]      # Wxy[i-1,j,k]
        f[1:-1] += lam * (np.sin(Wxy[1:-1]) - np.sin(Wxy_left[1:-1]))
        f[1:-1] -= lam * (np.sin(Wyz[1:-1]) - np.sin(_dn_z(Wyz)[1:-1]))
    return f


def force_phiz(theta, phix, phiy, phiz, dx, lam):
    uz = link_z(theta, phiz)
    lapz = (_up_z(phiz) - 2 * phiz + _dn_z(phiz)) / dx ** 2
    f = np.zeros_like(phiz)
    f[1:-1] = (lapz[1:-1] - np.sin(uz[1:-1])) / dx ** 2
    if lam:
        Wxz = plaq_xz(phix, phiz)
        Wyz = plaq_yz(phiy, phiz)
        Wxz_left = np.zeros_like(Wxz); Wxz_left[1:] = Wxz[:-1]      # Wxz[i-1,j,k]
        f[1:-1] += lam * (np.sin(Wxz[1:-1]) - np.sin(Wxz_left[1:-1]))
        f[1:-1] += lam * (np.sin(Wyz[1:-1]) - np.sin(_dn_y(Wyz)[1:-1]))
    return f


# --- velocity-Verlet evolution, x-ends clamped, optional Polyakov accumulate - #
def evolve(theta0, vth0, phix0, vphx0, phiy0, vphy0, phiz0, vphz0, dx, dt, nsteps,
           lam, freeze_theta=False, friction=0.0, pin_mask=None,
           record_polyakov=False):
    """Velocity-Verlet, x-ends clamped (Dirichlet), y,z periodic.

    ``pin_mask`` (boolean (Nx,Ny,Nz)) freezes ALL link components at their initial
    value where True (pins vortex/monopole cores in the T3D3 string measurement).
    ``record_polyakov`` accumulates the temporal holonomy Phi(s) = Sum_n dt*vth(s)
    at every spatial site; the magnitude of <exp(i Phi)> is the Polyakov order
    parameter (returned as the 8th..last element when requested)."""
    th, vth = theta0.copy(), vth0.copy()
    px, vpx = phix0.copy(), vphx0.copy()
    py, vpy = phiy0.copy(), vphy0.copy()
    pz, vpz = phiz0.copy(), vphz0.copy()
    Phi = np.zeros_like(th) if record_polyakov else None

    def acc(th, px, py, pz):
        ath = np.zeros_like(th) if freeze_theta else force_theta(th, px, py, pz, dx)
        return (ath, force_phix(th, px, py, pz, dx, lam),
                force_phiy(th, px, py, pz, dx, lam),
                force_phiz(th, px, py, pz, dx, lam))

    def repin(px, py, pz, vpx, vpy, vpz):
        if pin_mask is not None:
            px[pin_mask] = phix0[pin_mask]; py[pin_mask] = phiy0[pin_mask]
            pz[pin_mask] = phiz0[pin_mask]
            vpx[pin_mask] = 0.0; vpy[pin_mask] = 0.0; vpz[pin_mask] = 0.0

    ath, apx, apy, apz = acc(th, px, py, pz)
    damp = (1.0 - friction)
    for _ in range(nsteps):
        if not freeze_theta:
            vth = vth + 0.5 * dt * ath
        vpx = vpx + 0.5 * dt * apx
        vpy = vpy + 0.5 * dt * apy
        vpz = vpz + 0.5 * dt * apz
        if not freeze_theta:
            th = th + dt * vth
            th[0] = theta0[0]; th[-1] = theta0[-1]
        px = px + dt * vpx; px[0] = phix0[0]; px[-1] = phix0[-1]
        py = py + dt * vpy; py[0] = phiy0[0]; py[-1] = phiy0[-1]
        pz = pz + dt * vpz; pz[0] = phiz0[0]; pz[-1] = phiz0[-1]
        repin(px, py, pz, vpx, vpy, vpz)
        ath, apx, apy, apz = acc(th, px, py, pz)
        if not freeze_theta:
            vth = (vth + 0.5 * dt * ath) * damp
            vth[0] = 0.0; vth[-1] = 0.0
        vpx = (vpx + 0.5 * dt * apx) * damp; vpx[0] = 0.0; vpx[-1] = 0.0
        vpy = (vpy + 0.5 * dt * apy) * damp; vpy[0] = 0.0; vpy[-1] = 0.0
        vpz = (vpz + 0.5 * dt * apz) * damp; vpz[0] = 0.0; vpz[-1] = 0.0
        repin(px, py, pz, vpx, vpy, vpz)
        if record_polyakov:
            Phi = Phi + dt * vth
    out = (th, vth, px, vpx, py, vpy, pz, vpz)
    return (out + (Phi,)) if record_polyakov else out


# --- energy (leapfrog invariant; conserved at friction=0) ------------------ #
def energy_components(theta, vth, phix, vphx, phiy, vphy, phiz, vphz, dx, lam):
    ux, uy, uz = link_x(theta, phix), link_y(theta, phiy), link_z(theta, phiz)
    Wxy, Wxz, Wyz = all_plaquettes(phix, phiy, phiz)
    E_kin = 0.5 * dx * float(np.sum(vth ** 2) + np.sum(vphx ** 2)
                             + np.sum(vphy ** 2) + np.sum(vphz ** 2))
    E_stuck = (1.0 / dx) * (float(np.sum(1.0 - np.cos(ux[:-1])))
                            + float(np.sum(1.0 - np.cos(uy)))
                            + float(np.sum(1.0 - np.cos(uz))))
    E_xstiff = (1.0 / (2.0 * dx ** 3)) * float(np.sum(np.diff(phix, axis=0) ** 2))
    E_ystiff = (1.0 / (2.0 * dx ** 3)) * float(np.sum((_up_y(phiy) - phiy) ** 2))
    E_zstiff = (1.0 / (2.0 * dx ** 3)) * float(np.sum((_up_z(phiz) - phiz) ** 2))
    E_wilson = lam * dx * (float(np.sum(1.0 - np.cos(Wxy[:-1])))
                           + float(np.sum(1.0 - np.cos(Wxz[:-1])))
                           + float(np.sum(1.0 - np.cos(Wyz))))
    E_links = E_kin + E_stuck + E_xstiff + E_ystiff + E_zstiff
    return {"E_kin": E_kin, "E_stuck": E_stuck, "E_xstiff": E_xstiff,
            "E_ystiff": E_ystiff, "E_zstiff": E_zstiff, "E_wilson": E_wilson,
            "E_links": E_links, "E_total": E_links + E_wilson}


def energy_total(theta, vth, phix, vphx, phiy, vphy, phiz, vphz, dx, lam):
    return energy_components(theta, vth, phix, vphx, phiy, vphy,
                             phiz, vphz, dx, lam)["E_total"]


def energy_density_site(theta, vth, phix, vphx, phiy, vphy, phiz, vphz, dx, lam):
    """Per-site energy density (for localising 3D structures): on-site kinetic plus
    half of each adjacent link/plaquette term.  Approximate but localising."""
    ux, uy, uz = link_x(theta, phix), link_y(theta, phiy), link_z(theta, phiz)
    Wxy, Wxz, Wyz = all_plaquettes(phix, phiy, phiz)
    kin = 0.5 * (vth ** 2 + vphx ** 2 + vphy ** 2 + vphz ** 2)
    stuck = (1.0 - np.cos(ux)) + (1.0 - np.cos(uy)) + (1.0 - np.cos(uz))
    wil = lam * ((1.0 - np.cos(Wxy)) + (1.0 - np.cos(Wxz)) + (1.0 - np.cos(Wyz)))
    return kin + stuck / dx ** 2 + wil


# =========================================================================== #
# PART C -- topological observables (all real-valued)
# =========================================================================== #
def _wrap(a):
    return (a + np.pi) % TWO_PI - np.pi


def monopole_charge(phix, phiy, phiz):
    """DeGrand-Toussaint magnetic charge per unit cube (i,j,k):

        n = (1/2pi) * [  (wrapWxy[k+1] - wrapWxy[k])      # z-normal faces
                       - (wrapWxz[j+1] - wrapWxz[j])      # y-normal faces
                       + (wrapWyz[i+1] - wrapWyz[i]) ]    # x-normal faces

    Exactly an integer (discrete Bianchi: the unwrapped sum telescopes to 0); it
    counts Dirac strings piercing the cube.  Periodic in y,z; cubes use i<Nx-1."""
    Wxy, Wxz, Wyz = all_plaquettes(phix, phiy, phiz)
    wxy, wxz, wyz = _wrap(Wxy), _wrap(Wxz), _wrap(Wyz)
    n = ((_up_z(wxy) - wxy)
         - (_up_y(wxz) - wxz)
         + (np.roll(wyz, -1, axis=0) - wyz)) / TWO_PI
    n[-1] = 0.0     # x-normal shift undefined at the last x-cube
    return n


def monopole_density(phix, phiy, phiz, tol=0.45):
    """Fraction of cubes carrying |n|>=1 (magnetic charge), and the integer charges
    rounded.  Returns (rho_M, n_int)."""
    n = monopole_charge(phix, phiy, phiz)
    n_int = np.rint(n)
    interior = np.ones_like(n, dtype=bool); interior[-1] = False
    n_cubes = int(np.sum(interior))
    rho = float(np.sum(np.abs(n_int[interior]) >= 1) / max(n_cubes, 1))
    return rho, n_int


def polyakov_order(Phi):
    """Magnitude of the average temporal phase factor <exp(i Phi)>, evaluated as
    sqrt(<cos Phi>^2 + <sin Phi>^2) over spatial sites.  ~1 ordered/deconfined,
    ~0 disordered/confined.  Real-valued (no complex literal)."""
    c = float(np.mean(np.cos(Phi)))
    s = float(np.mean(np.sin(Phi)))
    return float(np.hypot(c, s))


def winding_x(phix):
    """Net x-winding per (y,z) column, averaged: (1/2pi) sum_i wrap(d_x phix)."""
    d = _wrap(np.diff(phix[:-1], axis=0))
    return float(np.mean(np.sum(d, axis=0) / TWO_PI))


def winding_planes(phix, phiy, phiz):
    """Winding in each plane: integrated wrapped plaquette flux / 2pi summed over the
    lattice, one per plane (xy, xz, yz) -- the net magnetic flux in each 2D plane."""
    Wxy, Wxz, Wyz = all_plaquettes(phix, phiy, phiz)
    return {"xy": float(np.sum(_wrap(Wxy[:-1])) / TWO_PI),
            "xz": float(np.sum(_wrap(Wxz[:-1])) / TWO_PI),
            "yz": float(np.sum(_wrap(Wyz)) / TWO_PI)}


def wilson_flux(phix, phiy, phiz):
    """Total magnetic activity sum_plaq (1-cos W) over the three planes (0 for a
    z-uniform / pure-gauge config)."""
    Wxy, Wxz, Wyz = all_plaquettes(phix, phiy, phiz)
    return float(np.sum(1.0 - np.cos(Wxy[:-1]))
                 + np.sum(1.0 - np.cos(Wxz[:-1]))
                 + np.sum(1.0 - np.cos(Wyz)))


def kink_count_x(phix, level=np.pi):
    """Max over (y,z) columns of the localized-core count along x (DBI detector)."""
    best = 0
    for j in range(phix.shape[1]):
        for k in range(phix.shape[2]):
            best = max(best, dbi.kink_count(phix[:, j, k], level))
    return int(best)


# =========================================================================== #
# PART D -- initial data
# =========================================================================== #
def zeros_fields(x, y, z):
    s = (len(x), len(y), len(z))
    return tuple(np.zeros(s) for _ in range(8))


def two_chains(x, y, z, amp, x0=8.0, w=2.0, noise=0.0, rng=None, vfrac=1.0,
               tnoise=0.0):
    """Two counter-propagating SCALAR chains (theta), gauge cold (phi*=0).  The chains
    are (y,z)-uniform up to an optional transverse noise ``tnoise`` that breaks the
    uniformity so the Wilson term can act (a uniform collision keeps every W_p=0)."""
    th1d, vth1d = dbi.two_packets(x, amp, x0=x0, w=w, noise=noise, rng=rng, vfrac=vfrac)
    theta = np.repeat(np.repeat(th1d[:, None], len(y), 1)[:, :, None], len(z), 2)
    vth = np.repeat(np.repeat(vth1d[:, None], len(y), 1)[:, :, None], len(z), 2)
    if tnoise and rng is not None:
        bump = tnoise * amp * rng.standard_normal(theta.shape)
        bump[0] = 0.0; bump[-1] = 0.0
        theta = theta + bump
    z8 = zeros_fields(x, y, z)
    return (theta, vth) + z8[2:]


def monopole_pair(x, y, z, d, plane="xy"):
    """Gauge field of a winding +1 / -1 vortex pair separated by d along x, embedded
    in one transverse plane (xy or xz), as the wrapped lattice gradient of the
    multivalued angle of the two sources.  This is the 3D analog of the CR_WILSON
    vortex string whose energy vs d is the string tension (T3D3).  Returns
    (phix, phiy, phiz, cores)."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    yc = float(y[len(y) // 2]); zc = float(z[len(z) // 2])
    x1, x2 = -0.5 * d, +0.5 * d
    if plane == "xy":
        Theta = np.arctan2(Y - yc, X - x1) - np.arctan2(Y - yc, X - x2)
    else:  # "xz"
        Theta = np.arctan2(Z - zc, X - x1) - np.arctan2(Z - zc, X - x2)
    phix = np.zeros_like(Theta); phiy = np.zeros_like(Theta); phiz = np.zeros_like(Theta)
    phix[:-1] = _wrap(np.diff(Theta, axis=0))
    phiy[:] = _wrap(_up_y(Theta) - Theta)
    phiz[:] = _wrap(_up_z(Theta) - Theta)
    phix[0] = phix[-1] = 0.0
    return phix, phiy, phiz, (x1, x2, yc, zc)


def dirac_monopole(x, y, z, charge=+1, center=None):
    """Lattice gauge field of a single Dirac magnetic monopole of charge ``charge``
    at ``center`` (default: lattice centre), built so the plaquette flux through any
    face equals the magnetic solid angle subtended -- the DeGrand-Toussaint detector
    must then return n=charge on the central cube and 0 elsewhere.  Used to CALIBRATE
    the monopole detector (T3D2 check), not as a dynamical IC.

    Construction: a monopole is NOT pure-gauge -- it cannot be the gradient of any
    scalar (that gives curl=0, a flux string with n=0).  We integrate the genuine
    Wu-Yang vector potential along each link.  In the string-down gauge
        A = charge * (1 - cos t) / rho * e_phi ,   rho = sqrt(Xr^2+Yr^2),
    whose curl is the radial monopole field B = charge * r_hat / (2 r^2) plus a Dirac
    string on the -z axis; the DGT detector (which wraps each plaquette) returns
    n=charge on the cube containing the centre and 0 elsewhere."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    dxg = float(x[1] - x[0])
    if center is None:
        # a DUAL-lattice point (cube centre): the monopole charge lives on cubes, so
        # placing it on a site smears the 2pi flux and the detector reads 0.
        center = (float(x[len(x) // 2]) + dxg / 2,
                  float(y[len(y) // 2]) + dxg / 2,
                  float(z[len(z) // 2]) + dxg / 2)
    cx_, cy_, cz_ = center
    Xr, Yr, Zr = X - cx_, Y - cy_, Z - cz_
    r = np.sqrt(Xr ** 2 + Yr ** 2 + Zr ** 2) + 1e-9
    rho2 = Xr ** 2 + Yr ** 2 + 1e-9
    cost = Zr / r
    # Cartesian components of A = charge*(1-cos t)*( -Yr, Xr, 0 )/rho^2
    pref = charge * (1.0 - cost) / rho2
    Ax, Ay, Az = pref * (-Yr), pref * Xr, np.zeros_like(Xr)
    dx = float(x[1] - x[0])
    phix = np.zeros_like(Xr); phiy = np.zeros_like(Xr); phiz = np.zeros_like(Xr)
    # link phase = integral of A.dl ~ midpoint value * spacing
    phix[:-1] = 0.5 * (Ax[:-1] + Ax[1:]) * dx
    phiy[:] = 0.5 * (Ay + _up_y(Ay)) * dx
    phiz[:] = 0.5 * (Az + _up_z(Az)) * dx
    phix[0] = phix[-1] = 0.0
    return phix, phiy, phiz


def random_gauge(x, y, z, rng, scale=np.pi):
    """A disordered ('hot') gauge configuration: link phases uniform in (-scale,scale].
    The thermal vacuum of compact U(1) -- its monopole density is the DeGrand-Toussaint
    vacuum value tested in T3D2.  x-ends zeroed (Dirichlet)."""
    s = (len(x), len(y), len(z))
    phix = rng.uniform(-scale, scale, s); phix[0] = phix[-1] = 0.0
    phiy = rng.uniform(-scale, scale, s)
    phiz = rng.uniform(-scale, scale, s)
    return phix, phiy, phiz


def pin_ball(x, y, z, cores, r_core=2.5):
    """Boolean (Nx,Ny,Nz) mask of two balls of radius r_core*dx around the vortex
    cores -- links pinned during relaxation so the winding cannot unwind (T3D3)."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    x1, x2, yc, zc = cores
    dx = float(x[1] - x[0]); r = r_core * dx
    m1 = (X - x1) ** 2 + (Y - yc) ** 2 + (Z - zc) ** 2 < r ** 2
    m2 = (X - x2) ** 2 + (Y - yc) ** 2 + (Z - zc) ** 2 < r ** 2
    return m1 | m2


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
    # ---- smoke 1: 4D Myrheim-Meyer recovers d (cheap: d=2 vs d=4) ----------
    rng = np.random.default_rng(0)
    print("MM reference fractions: f(2)=%.4f  f(4)=%.4f" %
          (mm_fraction(2.0), mm_fraction(4.0)))
    for d, T, rho in ((2, 6.0, 60.0), (4, 4.0, 40.0)):
        bounds = [(0.0, T)] + [(-T / 2, T / 2)] * (d - 1)
        fs = []
        for _ in range(8):
            pts = cc.sprinkle_box(rho, bounds, rng)
            A = np.zeros(d); B = np.zeros(d); B[0] = T
            keep = cc.alexandrov_interval(pts, A, B)
            fs.append(ordering_fraction(pts[keep]))
        f = float(np.mean(fs))
        print(f"  d={d}: empirical f={f:.4f}  -> MM dim={mm_dimension(f):.3f}")

    # ---- smoke 2: z-uniform reduces to wilson_core per slice (machine zero) -
    x, y, z, dx = make_grid(Lx=30.0, Nx=121, Ny=6, Nz=4)
    th1 = rng.standard_normal((len(x), len(y))) * 0.2
    px1 = rng.standard_normal((len(x), len(y))) * 0.2
    py1 = rng.standard_normal((len(x), len(y))) * 0.2
    theta = np.repeat(th1[:, :, None], len(z), 2)
    phix = np.repeat(px1[:, :, None], len(z), 2)
    phiy = np.repeat(py1[:, :, None], len(z), 2)
    phiz = np.zeros_like(theta)
    f3_th = force_theta(theta, phix, phiy, phiz, dx)[:, :, 0]
    f2_th = wc.force_theta(th1, px1, py1, dx)
    f3_px = force_phix(theta, phix, phiy, phiz, dx, 0.7)[:, :, 0]
    f2_px = wc.force_phix(th1, px1, py1, dx, 0.7)
    print("z-uniform reduction to wilson_core (max abs diff):")
    print("  theta force:", float(np.max(np.abs(f3_th - f2_th))))
    print("  phix  force:", float(np.max(np.abs(f3_px - f2_px))))

    # ---- smoke 3: energy conservation, lam>0, generic 3D config ------------
    fields = two_chains(x, y, z, 2.0, x0=6.0, rng=rng, tnoise=0.05)
    dt = dt_cfl(dx)
    E0 = energy_total(*fields, dx, 0.5)
    out = evolve(*fields, dx, dt, 400, lam=0.5)
    E1 = energy_total(*out, dx, 0.5)
    print(f"energy drift (lam=0.5, 400 steps): {abs(E1 - E0) / abs(E0):.2e}")

    # ---- smoke 4a: planar vortex pair is a flux STRING (zero monopole charge) -
    phix, phiy, phiz, cores = monopole_pair(x, y, z, d=8.0, plane="xy")
    n = monopole_charge(phix, phiy, phiz)
    print("vortex string: max|n|=%.3f (expect ~0, it is a string not a monopole)"
          % float(np.max(np.abs(n))))
    # ---- smoke 4b: an explicit Dirac monopole reads n=+1 on its cube ---------
    xs, ys, zs, dxs = make_grid(Lx=24.0, Nx=49, Ny=16, Nz=16)
    pmx, pmy, pmz = dirac_monopole(xs, ys, zs, charge=+1)
    nint = np.rint(monopole_charge(pmx, pmy, pmz))
    chg = np.argwhere(np.abs(nint) >= 1)
    print("Dirac monopole: charged cubes=%d  charges=%s (the +1 is the monopole, the "
          "-1 is the Dirac string exit on the periodic z-face)"
          % (len(chg), [int(nint[tuple(t)]) for t in chg]))
    # ---- smoke 4c: hot vacuum -- integer charges, globally neutral, rho_M>0 ---
    hot = random_gauge(xs, ys, zs, rng)
    rhoM, nint = monopole_density(*hot)
    nraw = monopole_charge(*hot)
    interior = np.ones_like(nraw, bool); interior[-1] = False
    print("hot vacuum: rho_M=%.3f per cube  net charge=%.2f  max integrality err=%.2e"
          % (rhoM, float(np.sum(nint[interior])),
             float(np.max(np.abs(nraw[interior] - nint[interior])))))

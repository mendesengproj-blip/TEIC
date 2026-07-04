"""wilson_core.py -- shared engine for the MATTER_CR_WILSON campaign (W1-W6).

Adds the Wilson PLAQUETTE term to the coupled action of CR_GAUGE:

    S = sum_links Dtau[1 - cos(phi + Dtheta)] + lambda_p sum_plaq [1 - cos(W_p)] ,

    W_p = phi^x_{i,j} + phi^y_{i+1,j} - phi^x_{i,j+1} - phi^y_{i,j}   (oriented square).

CR_GAUGE showed the Stueckelberg coupling transfers up to 57% of the scalar energy into
the gauge sector (G2) and that a gauge kink of rest mass 8 exists (G4), but that the
energy ends as RADIATION: the created charge disperses for want of CONFINEMENT (G3/G6).
The Wilson (magnetic / field-strength F^2) term penalises plaquettes with W_p != 0,
creating a STRING TENSION between gauge charge and anticharge -- the lattice mechanism
of confinement.  CR_WILSON asks whether, with lambda_p active, the charge created in a
collision is confined before it radiates, stabilising a kink.

Geometry
--------
A genuine 2D spatial lattice is required (a plaquette is a closed loop of 4 links).
x is the collision axis (Dirichlet ends, clamped like CR_GAUGE); y is transverse
(PERIODIC, so flux is trapped in a tube rather than leaking out a boundary).  Fields:
  theta[i,j]  scalar at sites;
  phix[i,j]   x-link (i,j)->(i+1,j), i<Nx-1;   phiy[i,j]  y-link (i,j)->(i,j+1), periodic.
The Stueckelberg link phases are ux = phix + d_x theta, uy = phiy + d_y theta.

Reduction to CR_GAUGE (W1 gate)
-------------------------------
At lambda_p=0 and a y-UNIFORM configuration (phiy=0), every plaquette is W_p=0, the y
terms vanish, and each x-row evolves EXACTLY as the 1D CR_GAUGE engine
(force matches gauge_core.force_theta / force_phi per row, to machine zero).  The
inherited per-row x-stiffness (the CR_GAUGE 1/dx^2 Laplacian, the kink's self-energy
that fixes its width and mass 8) is kept lambda_p-independent; the plaquette adds the
NEW gauge-invariant transverse coupling (confinement) on top.  A y-uniform kink has
W_p=0, so Wilson leaves its self-mass untouched (W1 check 3) -- exactly as required.

ANTI-CIRCULARITY (scanned by tests/test_no_circularity.py over results/matter/):
  * No mc^2/2mc^2, no SR/GR dilation, no complex numbers.  Winding / charge are summed
    from the REAL phase (principal branch); the string tension sigma is a fit of E(d).
  * QCD, quarks, gluons, colour confinement appear ONLY inside labelled COMPARISON ONLY
    blocks, as an analogy, never feeding a generator.

Reuses gauge_core (1D reference, packets, seed stats) and dbi_core (kink mass functional,
IO).  Modifies nothing in earlier campaigns.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_gauge"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_dbi"))
import gauge_core as gc   # noqa: E402  (1D reference for the W1 reduction check)
import dbi_core as dbi    # noqa: E402  (kink mass functional, seed stats, IO)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi


# --------------------------------------------------------------------------- #
# Grid
# --------------------------------------------------------------------------- #
def make_grid(Lx=60.0, Nx=301, Ny=12):
    """2D grid: x in [-Lx/2, Lx/2] (Nx points, Dirichlet ends), y transverse (Ny points,
    periodic, spacing dx).  Returns (x, y, dx)."""
    x = np.linspace(-Lx / 2, Lx / 2, Nx)
    dx = float(x[1] - x[0])
    y = np.arange(Ny) * dx
    return x, y, dx


def dt_cfl(dx, safety=0.2):
    """Stable step.  The x-stiffness AND the Wilson plaquette both carry 1/dx^2, so the
    gauge sector is stiff (omega_max ~ 2/dx^2); 0.2 keeps energy drift ~1e-3 on physical
    (smooth) collision configs.  Adversarial high-k noise needs a smaller factor."""
    return safety * dx ** 2


# --------------------------------------------------------------------------- #
# Link phases and plaquette (y periodic via np.roll on axis 1)
# --------------------------------------------------------------------------- #
def _roll_up(a):
    return np.roll(a, -1, axis=1)          # a[:, j+1]  (periodic y)


def _roll_dn(a):
    return np.roll(a, +1, axis=1)          # a[:, j-1]  (periodic y)


def link_x(theta, phix):
    """ux[i,j] = phix[i,j] + theta[i+1,j]-theta[i,j], for i<Nx-1 (else 0)."""
    ux = np.zeros_like(theta)
    ux[:-1, :] = phix[:-1, :] + np.diff(theta, axis=0)
    return ux


def link_y(theta, phiy):
    """uy[i,j] = phiy[i,j] + theta[i,j+1]-theta[i,j]  (periodic y)."""
    return phiy + (_roll_up(theta) - theta)


def plaquette(phix, phiy):
    """W[i,j] = phix[i,j] + phiy[i+1,j] - phix[i,j+1] - phiy[i,j], i<Nx-1 (else 0)."""
    W = np.zeros_like(phix)
    W[:-1, :] = phix[:-1, :] + phiy[1:, :] - _roll_up(phix)[:-1, :] - phiy[:-1, :]
    return W


# --------------------------------------------------------------------------- #
# Forces (reduce to gauge_core per row at lambda_p=0, y-uniform)
# --------------------------------------------------------------------------- #
def force_theta(theta, phix, phiy, dx):
    ux, uy = link_x(theta, phix), link_y(theta, phiy)
    sx, sy = np.sin(ux), np.sin(uy)
    f = np.zeros_like(theta)
    # divergence of sin(u) in x (interior rows) and y (periodic)
    f[1:-1, :] = (sx[1:-1, :] - sx[:-2, :]) + (sy[1:-1, :] - _roll_dn(sy)[1:-1, :])
    return f / dx ** 2


def force_phix(theta, phix, phiy, dx, lam):
    ux = link_x(theta, phix)
    lapx = np.zeros_like(phix)
    lapx[1:-1, :] = (phix[2:, :] - 2 * phix[1:-1, :] + phix[:-2, :]) / dx ** 2
    f = np.zeros_like(phix)
    f[1:-1, :] = (lapx[1:-1, :] - np.sin(ux[1:-1, :])) / dx ** 2
    if lam:
        W = plaquette(phix, phiy)
        f[1:-1, :] -= lam * (np.sin(W[1:-1, :]) - np.sin(_roll_dn(W)[1:-1, :]))
    return f


def force_phiy(theta, phix, phiy, dx, lam):
    uy = link_y(theta, phiy)
    lapy = (_roll_up(phiy) - 2 * phiy + _roll_dn(phiy)) / dx ** 2
    f = np.zeros_like(phiy)
    f[1:-1, :] = (lapy[1:-1, :] - np.sin(uy[1:-1, :])) / dx ** 2
    if lam:
        W = plaquette(phix, phiy)
        Wleft = np.zeros_like(W); Wleft[1:, :] = W[:-1, :]      # W[i-1,j], 0 at i=0
        f[1:-1, :] += lam * (np.sin(W[1:-1, :]) - np.sin(Wleft[1:-1, :]))
    return f


# --------------------------------------------------------------------------- #
# Symplectic evolution (velocity Verlet), x-ends clamped, optional friction
# --------------------------------------------------------------------------- #
def evolve(theta0, vth0, phix0, vphx0, phiy0, vphy0, dx, dt, nsteps, lam,
           freeze_theta=False, friction=0.0, pin_mask=None):
    """Velocity-Verlet evolution, x-ends clamped, y periodic.  ``friction`` adds linear
    damping (for relaxation to a static minimum).  ``pin_mask`` (a boolean (Nx,Ny) array)
    holds phix AND phiy fixed at their initial values where True -- used to pin vortex
    cores in the W2 string-tension measurement so the topological charge cannot unwind."""
    th, vth = theta0.copy(), vth0.copy()
    px, vpx = phix0.copy(), vphx0.copy()
    py, vpy = phiy0.copy(), vphy0.copy()

    def acc(th, px, py):
        ath = np.zeros_like(th) if freeze_theta else force_theta(th, px, py, dx)
        return ath, force_phix(th, px, py, dx, lam), force_phiy(th, px, py, dx, lam)

    def repin(px, py, vpx, vpy):
        if pin_mask is not None:
            px[pin_mask] = phix0[pin_mask]; py[pin_mask] = phiy0[pin_mask]
            vpx[pin_mask] = 0.0; vpy[pin_mask] = 0.0

    ath, apx, apy = acc(th, px, py)
    damp = (1.0 - friction)
    for _ in range(nsteps):
        if not freeze_theta:
            vth = vth + 0.5 * dt * ath
        vpx = vpx + 0.5 * dt * apx
        vpy = vpy + 0.5 * dt * apy
        if not freeze_theta:
            th = th + dt * vth
            th[0, :] = theta0[0, :]; th[-1, :] = theta0[-1, :]
        px = px + dt * vpx; px[0, :] = phix0[0, :]; px[-1, :] = phix0[-1, :]
        py = py + dt * vpy; py[0, :] = phiy0[0, :]; py[-1, :] = phiy0[-1, :]
        repin(px, py, vpx, vpy)
        ath, apx, apy = acc(th, px, py)
        if not freeze_theta:
            vth = (vth + 0.5 * dt * ath) * damp
            vth[0, :] = 0.0; vth[-1, :] = 0.0
        vpx = (vpx + 0.5 * dt * apx) * damp; vpx[0, :] = 0.0; vpx[-1, :] = 0.0
        vpy = (vpy + 0.5 * dt * apy) * damp; vpy[0, :] = 0.0; vpy[-1, :] = 0.0
        repin(px, py, vpx, vpy)
    return th, vth, px, vpx, py, vpy


# --------------------------------------------------------------------------- #
# Energy (consistent with the leapfrog; conserved at friction=0)
# --------------------------------------------------------------------------- #
def energy_components(theta, vth, phix, vphx, phiy, vphy, dx, lam):
    ux, uy = link_x(theta, phix), link_y(theta, phiy)
    W = plaquette(phix, phiy)
    E_kin = 0.5 * dx * float(np.sum(vth ** 2) + np.sum(vphx ** 2) + np.sum(vphy ** 2))
    # x-link cosine uses i<Nx-1; y-link cosine all (periodic)
    E_stuck = (1.0 / dx) * (float(np.sum(1.0 - np.cos(ux[:-1, :])))
                            + float(np.sum(1.0 - np.cos(uy))))
    E_xstiff = (1.0 / (2.0 * dx ** 3)) * float(np.sum(np.diff(phix, axis=0) ** 2))
    E_ystiff = (1.0 / (2.0 * dx ** 3)) * float(np.sum((_roll_up(phiy) - phiy) ** 2))
    E_wilson = lam * dx * float(np.sum(1.0 - np.cos(W[:-1, :])))
    return {"E_kin": E_kin, "E_stuck": E_stuck, "E_xstiff": E_xstiff,
            "E_ystiff": E_ystiff, "E_wilson": E_wilson,
            "E_links": E_kin + E_stuck + E_xstiff + E_ystiff,
            "E_total": E_kin + E_stuck + E_xstiff + E_ystiff + E_wilson}


def energy_total(theta, vth, phix, vphx, phiy, vphy, dx, lam):
    return energy_components(theta, vth, phix, vphx, phiy, vphy, dx, lam)["E_total"]


# --------------------------------------------------------------------------- #
# Topological observables on the gauge phase (real-valued)
# --------------------------------------------------------------------------- #
def winding_x(phix):
    """Net x-winding per row, averaged over y: (1/2pi) sum wrap(d_x phix), then mean_j."""
    d = np.diff(phix[:-1, :], axis=0)                 # avoid the unused last column
    d = (d + np.pi) % TWO_PI - np.pi
    return float(np.mean(np.sum(d, axis=0) / TWO_PI))


def kink_count_x(phix, level=np.pi):
    """Max over rows of the localized-core count along x (reuses the DBI detector)."""
    return int(max(dbi.kink_count(phix[:, j], level) for j in range(phix.shape[1])))


def peak_phi(phix):
    return float(np.max(np.abs(phix)))


def wilson_flux(phix, phiy):
    """Total |plaquette| flux sum_{plaq}(1-cos W) -- the magnetic activity (zero for a
    pure-gauge / y-uniform config)."""
    W = plaquette(phix, phiy)
    return float(np.sum(1.0 - np.cos(W[:-1, :])))


# --------------------------------------------------------------------------- #
# Initial data
# --------------------------------------------------------------------------- #
def zeros_fields(x, y):
    shape = (len(x), len(y))
    return (np.zeros(shape), np.zeros(shape), np.zeros(shape),
            np.zeros(shape), np.zeros(shape), np.zeros(shape))


def two_chains(x, y, amp, x0=8.0, w=2.0, noise=0.0, rng=None, vfrac=1.0, ynoise=0.0):
    """Two counter-propagating SCALAR chains (theta), gauge cold (phix=phiy=0).  The
    chains are y-uniform up to an optional small transverse noise ``ynoise`` that breaks
    y-uniformity so the Wilson term can act (a y-uniform collision keeps W_p=0)."""
    th1d, vth1d = dbi.two_packets(x, amp, x0=x0, w=w, noise=noise, rng=rng, vfrac=vfrac)
    theta = np.repeat(th1d[:, None], len(y), axis=1)
    vth = np.repeat(vth1d[:, None], len(y), axis=1)
    if ynoise and rng is not None:
        bump = ynoise * amp * rng.standard_normal((len(x), len(y)))
        bump[0, :] = 0.0; bump[-1, :] = 0.0
        theta = theta + bump
    phix = np.zeros_like(theta); vphx = np.zeros_like(theta)
    phiy = np.zeros_like(theta); vphy = np.zeros_like(theta)
    return theta, vth, phix, vphx, phiy, vphy


def kink_profile(x, x0, charge=+1):
    """A sine-Gordon kink (charge +1) or antikink (-1) centred at x0, width 1."""
    return charge * 4.0 * np.arctan(np.exp((x - x0) / 1.0)) + (0.0 if charge > 0 else TWO_PI)


def _wrap(a):
    return (a + np.pi) % TWO_PI - np.pi


def vortex_antivortex(x, y, d, yc=None):
    """Gauge field of a winding +1 vortex at x=-d/2 and a winding -1 antivortex at
    x=+d/2 (both at transverse yc), as the wrapped lattice gradient of the multivalued
    angle Theta = atan2(Y-yc, X-x1) - atan2(Y-yc, X-x2).  Returns (phix, phiy, cores).
    The branch cut joining the cores is the flux string whose energy vs d is the string
    tension (W2).  theta is left 0."""
    if yc is None:
        yc = float(y[len(y) // 2])
    X, Y = np.meshgrid(x, y, indexing="ij")
    x1, x2 = -0.5 * d, +0.5 * d
    Theta = np.arctan2(Y - yc, X - x1) - np.arctan2(Y - yc, X - x2)
    phix = np.zeros_like(Theta); phiy = np.zeros_like(Theta)
    phix[:-1, :] = _wrap(np.diff(Theta, axis=0))
    phiy[:, :] = _wrap(_roll_up(Theta) - Theta)
    phix[0, :] = phix[-1, :] = 0.0
    return phix, phiy, (x1, x2, yc)


def pin_disk(x, y, cores, r_core=2.5):
    """Boolean (Nx,Ny) mask of two disks of radius r_core (lattice units * dx) around the
    vortex cores -- the links pinned during relaxation so the winding cannot unwind."""
    X, Y = np.meshgrid(x, y, indexing="ij")
    x1, x2, yc = cores
    dx = float(x[1] - x[0])
    r = r_core * dx
    m1 = (X - x1) ** 2 + (Y - yc) ** 2 < r ** 2
    m2 = (X - x2) ** 2 + (Y - yc) ** 2 < r ** 2
    return m1 | m2


def seed_stats(values):
    return dbi.seed_stats(values)


def save_json(name, payload):
    import json
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    # smoke: lambda_p=0, y-uniform reduces to CR_GAUGE per row (machine zero)
    x, y, dx = make_grid(Lx=40.0, Nx=201, Ny=6)
    rng = np.random.default_rng(0)
    th1d = rng.standard_normal(len(x)) * 0.3
    ph1d = rng.standard_normal(len(x)) * 0.3
    theta = np.repeat(th1d[:, None], len(y), axis=1)
    phix = np.repeat(ph1d[:, None], len(y), axis=1)
    phiy = np.zeros_like(theta)
    fth = force_theta(theta, phix, phiy, dx)
    fpx = force_phix(theta, phix, phiy, dx, 0.0)
    fth1 = gc.force_theta(th1d, ph1d, dx)
    fpx1 = gc.force_phi(th1d, ph1d, dx)
    print("theta force vs CR_GAUGE per row:", float(np.max(np.abs(fth[:, 0] - fth1))))
    print("phix  force vs CR_GAUGE per row:", float(np.max(np.abs(fpx[:, 0] - fpx1))))
    # energy conservation, lambda_p>0, generic config
    th, vth, px, vpx, py, vpy = two_chains(x, y, 2.0, x0=6.0, rng=rng, ynoise=0.05)
    dt = dt_cfl(dx)
    E0 = energy_total(th, vth, px, vpx, py, vpy, dx, 0.5)
    out = evolve(th, vth, px, vpx, py, vpy, dx, dt, 600, lam=0.5)
    E1 = energy_total(*out, dx, 0.5)
    print(f"energy drift (lam=0.5, 600 steps): {abs(E1 - E0) / E0:.2e}")

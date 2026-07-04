"""v2_core.py -- shared engine for PE4_V2: causal rarefaction at the vortex core.

PHI_EMERGE (Veredito C) found that |Phi|=rho_Poisson (the bare node-count density) does
NOT dip at a gauge vortex.  PE4_V2 asks the sharper question the prompt poses: does the
EFFECTIVE causal density rho_eff -- the flux/back-reaction of causal links, NOT the static
node count -- deplete at the core?

Two faithful measures of rho_eff are computed and reported side by side:

  (K) KINEMATIC link flux (the prompt's literal definition):
        rho_eff_kin(r) = (1/Vol(r)) * sum over causal links with Dtau>0 whose position
        lies in the shell at r.  On a regular lattice every node carries the same ~6 links
        of unit Dtau, so this is FLAT -- the vortex does not change the link COUNT.  We
        report it to make the rho_Poisson(nodes) vs rho_eff(links) distinction explicit.

  (D) DYNAMICAL back-reaction (the physical hypothesis): if the causal density is the
        DYNAMICAL geometry field of the bridge (D1-D3/BD relax the density under the
        minimal action), it minimises E[rho] = sum_links rho_link * [1-cos(u_link)]
        + (K/2) sum_links (grad rho)^2  under conservation (sum rho = const).  The
        equilibrium DEPLETES rho where the gauge phase-mismatch [1-cos(u)] is large -- i.e.
        at the vortex core.  This is the SAME relaxation D3 used for a mass source, now
        sourced by the vortex.  The dip MAGNITUDE (and whether |Phi|(0)->0) is measured,
        not assumed.

ANTI-CIRCULARITY: rho_eff is a count / an action-minimising density; no relativistic
formula, no complex literal (the field is real; arg uses cos/sin sums).  'Superfluid',
'condensate', 'Abrikosov' appear ONLY inside COMPARISON ONLY blocks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "phi_emerge"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
import phi_emerge_core as pe   # noqa: E402  (grid, vortex_gauge, phibar, relax helpers)
import cr3d_core as c3         # noqa: E402  (evolve, plaquettes, _wrap)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)
TWO_PI = 2.0 * np.pi


# =========================================================================== #
# vortex setup + relaxation (gauge dynamics)
# =========================================================================== #
def make_vortex(grid, W=1):
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    phix, phiy, phiz, (xc, yc) = pe.vortex_gauge(x, y, z, n_wind=W)
    return (x, y, z, dx), (phix, phiy, phiz), (xc, yc)


def _core_pin_mask(x, y, z, xc, yc, r_pin=2.0):
    """Boolean (Nx,Ny,Nz) mask: nodes within r_pin (xy) of the vortex core AXIS (all z).
    Pinning the core during relaxation traps the winding so the vortex does not unwind to
    the trivial vacuum (the compact-lattice 2pi flux is otherwise CR_WILSON-invisible)."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    return (X - xc) ** 2 + (Y - yc) ** 2 < r_pin ** 2


def relax_vortex(grid, W, T_ticks, lam=0.7, friction=0.02, r_pin=2.0, rng=None,
                 noise=0.0):
    """Build a winding-W gauge vortex and relax it for T_ticks of velocity-Verlet
    (theta frozen, gauge cooling, CORE PINNED so the winding persists).  T_ticks=0 returns
    the initial (unrelaxed) vortex.  ``noise`` adds a seed-dependent gauge perturbation to
    the off-core links (so independent seeds give a distribution).  Returns relaxed
    (phix,phiy,phiz), grid, core."""
    (x, y, z, dx), (phix, phiy, phiz), (xc, yc) = make_vortex(grid, W)
    if noise and rng is not None:
        b = noise * rng.standard_normal(phix.shape)
        phix = phix + b; phix[0] = phix[-1] = 0.0
        phiy = phiy + noise * rng.standard_normal(phiy.shape)
    if T_ticks <= 0:
        return (phix, phiy, phiz), (x, y, z, dx), (xc, yc)
    sh = phix.shape
    z0 = [np.zeros(sh) for _ in range(8)]
    nsteps = max(int(T_ticks / c3.dt_cfl(dx)), 1)
    pin = _core_pin_mask(x, y, z, xc, yc, r_pin)
    out = c3.evolve(z0[0], z0[1], phix.copy(), np.zeros(sh), phiy.copy(), np.zeros(sh),
                    phiz.copy(), np.zeros(sh), dx, c3.dt_cfl(dx), nsteps, lam=lam,
                    freeze_theta=True, friction=friction, pin_mask=pin)
    return (out[2], out[4], out[6]), (x, y, z, dx), (xc, yc)


# =========================================================================== #
# gauge action density and current
# =========================================================================== #
def node_action_density(phix, phiy, phiz):
    """a_i = sum over links incident on node i of [1 - cos(u_link)] (theta=0, so the
    Stueckelberg phase u_link = phi_link).  Peaks at the vortex core."""
    inc = pe._incident_link_phases(phix, phiy, phiz)
    a = np.zeros_like(phix)
    for ph, valid in inc:
        a += np.where(valid, 1.0 - np.cos(ph), 0.0)
    return a


def gauge_current(phix, phiy, phiz, dtau=1.0):
    """Per-link gauge current J = Dtau * sin(u_link) for each of the three link
    directions (theta=0).  Returns (Jx, Jy, Jz)."""
    return dtau * np.sin(phix), dtau * np.sin(phiy), dtau * np.sin(phiz)


def current_magnitude_field(phix, phiy, phiz, dtau=1.0):
    """Node-centred |J| = sqrt(Jx^2+Jy^2+Jz^2) using the x/y/z link currents at the node
    (a proxy for the local causal-current intensity)."""
    Jx, Jy, Jz = gauge_current(phix, phiy, phiz, dtau)
    return np.sqrt(Jx ** 2 + Jy ** 2 + Jz ** 2)


def tangential_circulation(phix, phiy, phiz, x, y, xc, yc, radius, dtau=1.0):
    """Circulation of J around a loop of given radius about the core (xy plane, mid-z):
    sum of the tangential current component along the loop.  Nonzero => J circulates."""
    Jx, Jy, Jz = gauge_current(phix, phiy, phiz, dtau)
    Nx, Ny, Nz = phix.shape
    kz = Nz // 2
    ths = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    xs = xc + radius * np.cos(ths); ys = yc + radius * np.sin(ths)
    ix = np.clip(np.rint(xs).astype(int), 0, Nx - 1)
    iy = np.mod(np.rint(ys).astype(int), Ny)
    # tangential unit vector (-sin, cos); current sampled at the loop points
    tx, ty = -np.sin(ths), np.cos(ths)
    circ = np.mean(Jx[ix, iy, kz] * tx + Jy[ix, iy, kz] * ty)
    return float(circ)


# =========================================================================== #
# radial profiles about the core (xy plane, averaged over z)
# =========================================================================== #
def radial_profile(field, x, y, xc, yc, r_edges):
    f2d = field.mean(axis=2)
    X, Y = np.meshgrid(x, y, indexing="ij")
    r = np.sqrt((X - xc) ** 2 + (Y - yc) ** 2)
    centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    prof = np.full(len(centers), np.nan)
    rr = r.ravel(); ff = f2d.ravel()
    for k in range(len(centers)):
        sel = (rr >= r_edges[k]) & (rr < r_edges[k + 1])
        if sel.sum():
            prof[k] = ff[sel].mean()
    return centers, prof


def core_radius_xi(centers, Jprof):
    """Core size xi = radius where |J|(r) is maximal (the vortex 'healing length' proxy)."""
    Jprof = np.asarray(Jprof, float)
    ok = np.isfinite(Jprof)
    if not ok.any():
        return float("nan")
    return float(np.asarray(centers)[ok][np.argmax(Jprof[ok])])


# =========================================================================== #
# (K) kinematic causal-link flux  -- the prompt's literal rho_eff (count of links)
# =========================================================================== #
def kinematic_link_flux(phix, phiy, phiz, x, y, xc, yc, r_edges, dtau=1.0):
    """rho_eff_kin(r) = Dtau-weighted COUNT of causal links incident on each node (every
    causal link has Dtau>0, so all valid links count).  On a regular lattice the link
    count is uniform (6 interior, 5 at the x-faces), so this profile is FLAT -- the vortex
    does NOT change the kinematic link count.  This is the prompt's literal rho_eff, and
    its flatness is the point: rho_Poisson(nodes) and rho_eff(links) are both substrate
    counts that the vortex topology leaves unchanged."""
    inc = pe._incident_link_phases(phix, phiy, phiz)
    count = np.zeros_like(phix)
    for ph, valid in inc:
        count += dtau * valid.astype(float)
    return radial_profile(count, x, y, xc, yc, r_edges)


# =========================================================================== #
# (D) dynamical back-reaction density  -- minimise E[rho] under conservation
# =========================================================================== #
def _neighbour_sum(f):
    """Sum of the 6 lattice neighbours with x mirror (Neumann) and y,z periodic."""
    s = np.zeros_like(f)
    for ax in (1, 2):                       # y, z periodic
        s += np.roll(f, +1, axis=ax) + np.roll(f, -1, axis=ax)
    # x with mirror BC (Neumann): the face neighbour reflects the interior
    s[1:-1] += f[2:] + f[:-2]
    s[0] += f[1] + f[1]
    s[-1] += f[-2] + f[-2]
    return s


def relax_density(a, K=1.0, n_iter=1500):
    """Equilibrium density deviation drho that minimises E[drho] = sum drho*a +
    (K/2) sum_links (grad drho)^2 under sum drho = 0.  The minimiser solves the discrete
    Poisson equation  lap(drho) = (a - <a>) / K  (lap = sum_neighbours - 6*center).  We
    solve it by Jacobi iteration (x mirror, y,z periodic), which is unconditionally stable
    -- so the depletion DEPTH ~ 1/K is read cleanly (deeper for softer geometry).

    drho is NEGATIVE where a is large (the vortex core): events redistribute AWAY from the
    high-action region under conservation -- the D1-D3 geometry-sector relaxation, now
    sourced by the vortex instead of a mass."""
    src = (a - a.mean()) / K
    drho = np.zeros_like(a)
    for _ in range(n_iter):
        drho = (_neighbour_sum(drho) - src) / 6.0
        drho -= drho.mean()
    return drho


def dynamical_rho_eff(phix, phiy, phiz, x, y, xc, yc, r_edges, K=1.0, rho0=1.0,
                      n_iter=3000, rho_factor=1.0):
    """rho_eff_dyn = rho0 + drho where drho minimises the minimal action sourced by the
    vortex action density a (D3-style).  ``rho_factor`` scales the source (the Dtau weight
    grows with the background causal density rho, so a denser network drives a stronger
    response).  Clamped >=0.  Returns (centers, profile, field, a)."""
    a = rho_factor * node_action_density(phix, phiy, phiz)
    drho = relax_density(a, K=K, n_iter=n_iter)
    # scale: drho is in units of (action/K); normalise so the FAR field is rho0 and report
    # the relative profile.  rho_eff = rho0 * (1 + drho/|mean far drho scale|) is avoided;
    # instead keep physical drho and report rho0 + drho clamped.
    rho_eff = np.clip(rho0 + drho, 0.0, None)
    centers, prof = radial_profile(rho_eff, x, y, xc, yc, r_edges)
    return centers, prof, rho_eff, a


# =========================================================================== #
# IO
# =========================================================================== #
def save_json(name, payload):
    (OUTDIR / f"{name}.json").write_text(json.dumps(payload, indent=2))
    return OUTDIR / f"{name}.json"


if __name__ == "__main__":
    grid = (33, 28, 28)
    (phix, phiy, phiz), (x, y, z, dx), (xc, yc) = relax_vortex(grid, W=1, T_ticks=100)
    r_edges = np.arange(0.0, 11.0, 1.0)

    a = node_action_density(phix, phiy, phiz)
    cA, pA = radial_profile(a, x, y, xc, yc, r_edges)
    print("node action density a(r):", [round(v, 3) for v in pA[:6]], "(peaks at core?)")

    Jmag = current_magnitude_field(phix, phiy, phiz)
    cJ, pJ = radial_profile(Jmag, x, y, xc, yc, r_edges)
    xi = core_radius_xi(cJ, pJ)
    circ = tangential_circulation(phix, phiy, phiz, x, y, xc, yc, radius=max(xi, 2.0))
    print("|J|(r):", [round(v, 3) for v in pJ[:6]], " xi(peak)=", round(xi, 2),
          " circulation=", round(circ, 4))

    cK, pK = kinematic_link_flux(phix, phiy, phiz, x, y, xc, yc, r_edges)
    print("kinematic link flux (flat?):", [round(v, 3) for v in pK[:6]])

    cD, pD, rho_eff, _ = dynamical_rho_eff(phix, phiy, phiz, x, y, xc, yc, r_edges, K=1.0)
    print("dynamical rho_eff(r):", [round(v, 3) for v in pD[:6]],
          " dip =", round((np.nanmean(pD[-3:]) - pD[0]) / max(np.nanmean(pD[-3:]), 1e-9), 3))

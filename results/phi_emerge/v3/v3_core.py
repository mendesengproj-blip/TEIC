"""v3_core.py -- shared engine for PE4_V3: SPONTANEOUS back-reaction on vortex creation.

PE4_V2 (Veredito B) showed that when rho is the DYNAMICAL causal density (the D1-D3
geometry sector) it depletes at a vortex core -- BUT rho was relaxed to its STATIC
equilibrium given an already-present vortex (the dip was, in effect, initialised by the
equilibrium solve).  PE4_V3 asks the sharper question:

    starting from rho UNIFORM (no dip), with rho a genuinely DYNAMICAL field obeying
    box rho = J (the same wave operator D1-D3 use for gravitation), does the dip
    EMERGE SPONTANEOUSLY as a vortex is created -- on what timescale tau_dip, and does
    it reach the V2 equilibrium depth before the window closes?

The ONLY extension over the bridge's D1-D3 is to evolve rho in REAL TIME (a damped wave
field) instead of solving its static minimiser.  No new field, no new parameter: J is the
gauge-action current of the vortex (V2's source), K is the action stiffness (V2's K, here
the rho wave-speed^2), rho_fundo is the background causal density.

  rho-sector equation of motion (one-way drive, exactly like V2 -- the vortex sources rho,
  rho does not feed back into the gauge field):

      d^2 rho/dt^2  =  K * lap(rho)  -  (J_rho - <J_rho>)  -  gamma * d rho/dt

  * lap = discrete Laplacian (x mirror/Neumann, y,z periodic) -- v2._neighbour_sum.
  * J_rho(i) = vortex gauge-action density a_i = sum_links [1 - cos(u_link)] (V2's source);
    mean-subtracted so total rho is conserved (sum rho = const, the D1-D3 conservation).
  * The STATIC equilibrium (d/dt -> 0) is  K lap(rho) = J_rho - <J_rho>, IDENTICAL to V2's
    relax_density solve -- so rho(t -> inf) -> the V2 dip BY CONSTRUCTION.  The PE4_V3
    question is therefore purely DYNAMICAL: does rho reach >= 0.5 of that equilibrium
    within the post-collision window, starting from uniform?

ANTI-CIRCULARITY (same discipline as V2): rho is an action-evolving real density; J is the
real gauge action; no complex literal anywhere; no relativistic/condensate parameter is
inserted.  'Superfluid', 'Higgs', 'Cooper' appear ONLY in COMPARISON ONLY blocks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "phi_emerge" / "v2"))
sys.path.insert(0, str(ROOT / "results" / "phi_emerge"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
import v2_core as v2            # noqa: E402  (relax_vortex, node_action_density, profiles)
import phi_emerge_core as pe    # noqa: E402  (make_grid, vortex_gauge)
import cr3d_core as c3          # noqa: E402  (two_chains, evolve, links, winding)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)
TWO_PI = 2.0 * np.pi

GRID = (29, 24, 24)                 # same transverse box as V2 (dx = 1, x mirror / y,z per.)
R_EDGES = np.arange(0.0, 11.0, 1.0)


# =========================================================================== #
# discrete wave operator on the V2 lattice (dx = 1)
# =========================================================================== #
def laplacian(f):
    """6-neighbour Laplacian with x mirror (Neumann) and y,z periodic (dx = 1).  Uses the
    SAME neighbour stencil V2's static relax_density used, so the dynamical equilibrium
    coincides with the V2 minimiser."""
    return v2._neighbour_sum(f) - 6.0 * f


def _dt_stable(K, cap=0.18):
    """Explicit CFL step for the rho wave  c^2 = K  on a dx=1, 3D lattice.  Capped at the
    gauge-sector step (0.18) so soft K does not take needlessly large steps."""
    return float(min(cap, 0.4 / np.sqrt(3.0 * K + 1e-12)))


# =========================================================================== #
# (S1) dynamical rho field -- box rho = J, evolved in real time from UNIFORM
# =========================================================================== #
def evolve_rho(source, K, rho0=1.0, gamma=0.5, t_total=200.0, ramp_tau=0.0,
               record_times=None, rho_factor=1.0, src_mean=None, core_idx=None):
    """Evolve  d^2 rho/dt^2 = K lap(rho) - g(t)*(J - <J>) - gamma d rho/dt  from rho = rho0
    UNIFORM (no dip), velocity 0.  ``source`` is the vortex gauge-action field J (a 3D
    array); it is scaled by ``rho_factor`` (denser network -> stronger drive, V2 style) and
    mean-subtracted (conservation).  ``g(t) = 1 - exp(-t/ramp_tau)`` ramps the drive on as
    the vortex FORMS (ramp_tau = tau_vortex from S1); ramp_tau=0 turns it on at t=0.

    rho is a DENSITY: it is floored at 0 each step (velocity zeroed where it would go
    negative) -- the SAME physical floor V2's clip(rho0+drho,0) imposes, so the dip
    SATURATES at full depletion (|Phi|(0)->0) for soft K, matching V2's K<~5 closure.

    Returns dict: ``snapshots`` {t_record: rho_field}, ``final`` rho, ``rho0``, ``dt`` and
    the core trajectory (``traj_t``, ``traj_core``) sampled ~once per time unit (tau_dip)."""
    J = rho_factor * np.asarray(source, float)
    Jm = J.mean() if src_mean is None else src_mean
    drive = J - Jm
    dt = _dt_stable(K)
    nstep = max(int(round(t_total / dt)), 1)
    record_times = sorted(record_times or [])
    rho = np.full(J.shape, float(rho0))
    vrho = np.zeros_like(rho)
    if core_idx is None:                              # default: source peak == vortex core
        core_idx = np.unravel_index(int(np.argmax(J)), J.shape)

    def g(t):
        if ramp_tau and ramp_tau > 0:
            return 1.0 - np.exp(-t / ramp_tau)
        return 1.0

    def acc(rho_, t):
        return K * laplacian(rho_) - g(t) * drive

    snaps = {}
    traj_t, traj_core = [], []
    a = acc(rho, 0.0)
    damp = 1.0 - gamma * dt
    ri = 0
    sample_every = max(int(round(1.0 / dt)), 1)       # ~1 sample / time unit for tau_dip
    for n in range(nstep):
        t = n * dt
        vrho = vrho + 0.5 * dt * a
        rho = rho + dt * vrho
        floored = rho < 0.0                           # density floor (physical, V2's clip)
        if floored.any():
            rho[floored] = 0.0
            vrho[floored] = 0.0
            pos = rho > 0.0                            # conserve total: remove the mass the
            n_pos = int(pos.sum())                    # floor injected, from the bulk, so
            if n_pos:                                 # rho_inf stays == rho0 (no drift)
                rho[pos] -= (rho.sum() - rho0 * rho.size) / n_pos
        a = acc(rho, t + dt)
        vrho = (vrho + 0.5 * dt * a) * damp
        if n % sample_every == 0:
            traj_t.append(t + dt)
            traj_core.append(float(rho[core_idx]))
        while ri < len(record_times) and (t + dt) >= record_times[ri] - 1e-9:
            snaps[record_times[ri]] = rho.copy()
            ri += 1
    while ri < len(record_times):                     # any tail records
        snaps[record_times[ri]] = rho.copy()
        ri += 1
    return {"snapshots": snaps, "final": rho, "rho0": float(rho0), "dt": dt,
            "traj_t": traj_t, "traj_core": traj_core, "core_idx": list(core_idx)}


# =========================================================================== #
# (S1) vortex source -- the persistent W=1 gauge-action density (V2's, reproducible)
# =========================================================================== #
def vortex_action_source(grid=GRID, W=1, T_relax=100.0, rng=None, noise=0.05):
    """Build & relax a pinned winding-W gauge vortex (V2.relax_vortex) and return its node
    gauge-action density a = sum_links [1-cos(u)] (the SOURCE J_rho), the grid, and the
    core (xc,yc).  This is the structure the collision CREATES; using V2's reproducible
    vortex isolates the rho-sector dynamics (the object of PE4_V3) from the collision's
    well-studied gauge details (T3D4)."""
    (px, py, pz), (x, y, z, dx), (xc, yc) = v2.relax_vortex(grid, W=W, T_ticks=T_relax,
                                                            rng=rng, noise=noise)
    a = v2.node_action_density(px, py, pz)
    return a, (px, py, pz), (x, y, z, dx), (xc, yc)


# =========================================================================== #
# (S1) full-link gauge-action density (for the LIVE collision, theta != 0)
# =========================================================================== #
def link_action_density(theta, phix, phiy, phiz):
    """a_i = (1-cos ux)+(1-cos uy)+(1-cos uz) at each node, with the full Stueckelberg
    links u = phi + grad theta (theta NOT frozen).  Peaks at the collision-created gauge
    core; this is J_rho during a live collision."""
    ux = c3.link_x(theta, phix)
    uy = c3.link_y(theta, phiy)
    uz = c3.link_z(theta, phiz)
    return (1.0 - np.cos(ux)) + (1.0 - np.cos(uy)) + (1.0 - np.cos(uz))


# =========================================================================== #
# (S1) measure tau_vortex from a REAL gauge collision (cr3d two_chains)
# =========================================================================== #
def collision_formation(amp=18.0, lam=1.0, seed=0,
                        grid=dict(Lx=28.0, Nx=85, Ny=10, Nz=10),
                        t_collide=16.0, n_sample=40):
    """Counter-propagating scalar chains collide along x (cr3d.two_chains, full 3+1D
    action).  Track the CENTRAL gauge-action a_center(t) and the xy-winding; return the
    time series and tau_vortex = time for a_center to reach 90% of its post-collision
    plateau.  Confirms a winding gauge core is CREATED (W=1 scale) from a uniform start."""
    x, y, z, dx = c3.make_grid(**grid)
    dt = c3.dt_cfl(dx)
    rng = np.random.default_rng(7000 + seed)
    fields = c3.two_chains(x, y, z, float(amp), x0=7.0, w=2.0, noise=0.01, rng=rng,
                           tnoise=0.05)
    nstep = int(round(t_collide / dt))
    every = max(nstep // n_sample, 1)
    cen = np.abs(x) < 3.0
    ts, a_cen, wind = [], [], []
    for n in range(nstep):
        fields = c3.evolve(*fields, dx, dt, 1, lam=lam)
        if n % every == 0:
            th, vth, px, vpx, py, vpy, pz, vpz = fields
            a = link_action_density(th, px, py, pz)
            ts.append((n + 1) * dt)
            a_cen.append(float(a[cen].mean()))
            wind.append(abs(c3.winding_planes(px, py, pz)["xy"]))
    a_cen = np.asarray(a_cen); ts = np.asarray(ts); wd = np.asarray(wind)
    plateau = float(np.mean(a_cen[len(a_cen) // 2:]))      # late-window action mean
    # tau_vortex = TOPOLOGICAL formation time: when the xy-winding (the genuine vortex
    # signal, 0 -> 1) first reaches 0.5.  a_center is contaminated by the chains' transverse
    # theta-noise floor (present from t=0), so it is NOT a clean formation clock; the
    # winding is.  Reported only for seeds that actually create a winding (|W|_final>=0.5).
    w_final = float(wd[-1])
    if w_final >= 0.5:
        above = np.where(wd >= 0.5)[0]
        tau = float(ts[above[0]]) if above.size else float(ts[-1])
    else:
        tau = float("nan")
    return {"t": ts.tolist(), "a_center": a_cen.tolist(), "winding_xy": wind,
            "tau_vortex": tau, "plateau": plateau, "winding_final": w_final}


# =========================================================================== #
# (S1) point-source consistency -- box rho = M delta  ->  rho ~ -M/(4 pi K r)  (GM/r form)
# =========================================================================== #
def point_source_profile(grid=GRID, M=40.0, K=1.0, n_iter=4000):
    """Static minimiser for a POINT source at the lattice centre: solve K lap(drho) =
    M*delta - <.> (V2.relax_density) and return the radial |drho|(r).  The 3D Green's
    function of lap is 1/r, so drho ~ -M/(4 pi K r): the SAME 1/r law D2/D3 recover for a
    mass (the GM/r bridge scalar).  Returns (centers, |drho|(r), inv_r_fit_r2)."""
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    xc, yc, zc = Nx // 2, Ny // 2, Nz // 2
    a = np.zeros(grid)
    a[xc, yc, zc] = M                                   # point mass (delta source)
    drho = v2.relax_density(a, K=K, n_iter=n_iter)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    r = np.sqrt((X - x[xc]) ** 2 + (Y - y[yc]) ** 2 + (Z - z[zc]) ** 2)
    r_edges = np.arange(1.0, 9.0, 1.0)
    centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    prof = np.full(len(centers), np.nan)
    rr = r.ravel(); dd = np.abs(drho).ravel()
    for k in range(len(centers)):
        sel = (rr >= r_edges[k]) & (rr < r_edges[k + 1])
        if sel.sum():
            prof[k] = dd[sel].mean()
    # fit |drho| = A/r : regress prof vs 1/r through the resolved shells
    ok = np.isfinite(prof) & (centers >= 1.5) & (centers <= 6.5)
    invr = 1.0 / centers[ok]
    A = np.polyfit(invr, prof[ok], 1)
    pred = np.polyval(A, invr)
    ss_res = np.sum((prof[ok] - pred) ** 2)
    ss_tot = np.sum((prof[ok] - prof[ok].mean()) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    return centers, prof, r2, float(A[0])


def uniform_stability(K, gamma=0.5, rho0=1.0, t_total=200.0):
    """J = 0 sanity: with no vortex source, an initially UNIFORM rho must stay uniform.
    Returns the max deviation over the run (should be ~0 / round-off)."""
    src = np.zeros(GRID)
    out = evolve_rho(src, K=K, rho0=rho0, gamma=gamma, t_total=t_total)
    return float(np.max(np.abs(out["final"] - rho0)))


# =========================================================================== #
# observables on a rho field
# =========================================================================== #
def radial_rho(rho, x, y, xc, yc, r_edges=R_EDGES):
    return v2.radial_profile(rho, x, y, xc, yc, r_edges)


def central_dip(rho, x, y, xc, yc, r_edges=R_EDGES):
    """Absolute dip Delta rho = rho_inf - rho(0) (rho_inf = far-shell mean) and the core
    value rho(0).  Returns (Delta_rho, rho_core, rho_inf, centers, prof)."""
    centers, prof = radial_rho(rho, x, y, xc, yc, r_edges)
    rho_inf = float(np.nanmean(prof[-3:]))
    rho_core = float(prof[0])
    return rho_inf - rho_core, rho_core, rho_inf, centers, prof


def core_sigma(rho, x, y, xc, yc, rho_inf=None, half_depth=True):
    """RMS transverse width of the depleted region (deficit-weighted), at the HALF-DEPTH
    level rho_inf - 0.5*Delta rho (generalises V2's R4 sigma_core to any rho_fundo;
    coincides with V2 for rho_fundo=1, deep dip).  NaN if no dip."""
    f2d = rho.mean(axis=2)
    if rho_inf is None:
        rho_inf = float(np.nanmean(f2d))
    X, Y = np.meshgrid(x, y, indexing="ij")
    r2 = (X - xc) ** 2 + (Y - yc) ** 2
    dipmin = float(f2d.min())
    level = rho_inf - 0.5 * (rho_inf - dipmin) if half_depth else 0.5 * rho_inf
    w = np.clip(level - f2d, 0.0, None)
    W = float(w.sum())
    if W < 1e-9:
        return float("nan")
    return float(np.sqrt((w * r2).sum() / W))


def static_dip_v2(source, K, rho0=1.0, rho_factor=1.0, x=None, y=None, xc=None, yc=None,
                  n_iter=4000):
    """V2 equilibrium: drho = relax_density(rho_factor*source, K); rho_eff = rho0 + drho.
    Returns (Delta_rho_V2, rho_eff field).  This is rho(t -> inf) of evolve_rho by
    construction (same operator, same source)."""
    drho = v2.relax_density(rho_factor * np.asarray(source, float), K=K, n_iter=n_iter)
    rho_eff = np.clip(rho0 + drho, 0.0, None)
    if x is None:
        return float(np.nanmean(rho_eff) - rho_eff.min()), rho_eff
    dr, core, inf, _, _ = central_dip(rho_eff, x, y, xc, yc)
    return dr, rho_eff


# =========================================================================== #
# IO
# =========================================================================== #
def save_json(name, payload):
    (OUTDIR / f"{name}.json").write_text(json.dumps(payload, indent=2))
    return OUTDIR / f"{name}.json"


if __name__ == "__main__":
    print("v3_core smoke")
    # J=0 -> uniform stays uniform
    print("  uniform stability (J=0), max|drho| =", uniform_stability(K=1.0))
    # point source -> 1/r
    c, p, r2, A = point_source_profile(M=40.0, K=1.0)
    print(f"  point source |drho|(r): {[round(v,4) for v in p]}  1/r fit r2={r2:.4f}")
    # a vortex source + dynamical emergence vs static V2 equilibrium
    rng = np.random.default_rng(0)
    a, _, (x, y, z, dx), (xc, yc) = vortex_action_source(rng=rng)
    dV2, _ = static_dip_v2(a, K=1.0, rho0=1.0, x=x, y=y, xc=xc, yc=yc)
    out = evolve_rho(a, K=1.0, rho0=1.0, t_total=200.0, ramp_tau=8.0,
                     record_times=[10, 50, 100, 200])
    for t in (10, 50, 100, 200):
        dr, core, inf, _, _ = central_dip(out["snapshots"][t], x, y, xc, yc)
        print(f"  t={t:3d}: Delta_rho(dyn)={dr:.3f}  (V2 eq={dV2:.3f}, ratio={dr/max(dV2,1e-9):.2f})")

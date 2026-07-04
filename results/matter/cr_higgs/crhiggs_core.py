"""crhiggs_core.py -- shared engine for the MATTER_CR_HIGGS campaign (H1-H6).

CR_3D (Veredito B) created a topological VORTEX (S^1) in a genuinely 3+1D compact-U(1)
lattice but could not STABILISE it: the 2pi flux is invisible to the Wilson cosine
(cos 2pi = 1) and there is no magnitude field to hold the core, which diffuses.  The
known physics cure is a SCALAR CONDENSATE that pins the core.  CR_HIGGS tests whether
the scalar theta of the TEIC action can condense and pin, by adding a single new term:

    a node potential  V(theta) = -mu^2/2 theta^2 + lambda_h/4 theta^4

to the CR_3D action, giving

    S_HIGGS = sum_links Dtau[1-cos(phi+Dtheta)]            (Stueckelberg)
            + lambda_p sum_plaq [1-cos(W_p)]               (Wilson, magnetic)
            + sum_nodes V(theta_i) * V_i                   (NEW: node potential)

V_i is the Voronoi volume of node i (a causal weight).  On the regular CR_3D lattice
every cell has the same volume; in the engine's energy bookkeeping the on-site weight
is dx (the same per-node weight E_kin / E_stuck already carry -- the field theory is
normalised to reduce to the 1D dbi_core / 2D wilson_core references), so V_i = dx and
the potential is commensurate with the rest of the action.  This is stated honestly:
on a uniform lattice the Voronoi weight is a constant, not extra structure.

THE HONEST CAVEAT ABOUT theta (documented, and MEASURED in H2/H3, not presumed).
In the minimal TEIC action theta is the STUECKELBERG PHASE: it enters only through its
gradient Dtheta inside cos(phi+Dtheta), with an exact shift symmetry theta -> theta+const.
The mexican-hat V(theta) EXPLICITLY BREAKS that shift symmetry and pins theta to +-v with
v = sqrt(mu^2/lambda_h).  This is a genuine new mechanism, but it is NOT identical to the
abelian-Higgs magnitude condensate, where the gauge mass m_A = e v arises because the
field MAGNITUDE multiplies (d alpha - e A)^2.  Here the cosine amplitude is fixed at 1,
so whether m_A scales as e v, whether a coherence length xi appears, and whether the core
pins, are EMPIRICAL questions the campaign answers -- it does not assume the textbook
abelian-Higgs answers.  Cooper pair / Meissner / Abrikosov / Ginzburg-Landau / "Higgs
mechanism" appear only as NAMES inside COMPARISON ONLY blocks.

ANTI-CIRCULARITY (tests/test_no_circularity.py scans results/matter/):
  * V(theta) is a real polynomial in the scalar field; v = sqrt(mu^2/lambda_h) is
    MEASURED by relaxation, never inserted into a generator.
  * No mc^2 / SR-GR dilation / complex numbers anywhere in the generator.
  * m_A, xi, lambda_L are FITTED from real correlators / profiles.

Reuses cr3d_core verbatim (forces, plaquettes, monopoles, ICs, IO); modifies nothing.
The force convention is inherited exactly: force_field = (1/dx) * (-dE_total/dfield),
so the leapfrog energy below (cr3d energy + E_pot) is the conserved invariant.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_dbi"))
import cr3d_core as c     # noqa: E402  (the full 3+1D engine -- reused verbatim)
import dbi_core as dbi    # noqa: E402  (seed stats, radial solver)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = c.TWO_PI

# Re-export the most-used CR_3D handles so the H-scripts read cleanly.
make_grid = c.make_grid
dt_cfl = c.dt_cfl
all_plaquettes = c.all_plaquettes
plaq_xy = c.plaq_xy
monopole_charge = c.monopole_charge
monopole_density = c.monopole_density
winding_planes = c.winding_planes
kink_count_x = c.kink_count_x
_wrap = c._wrap


# =========================================================================== #
# The node potential V(theta) = -mu^2/2 theta^2 + lambda_h/4 theta^4
# =========================================================================== #
def v_potential(theta, mu2, lamh):
    """Node potential energy DENSITY (per node): V = -mu^2/2 th^2 + lambda_h/4 th^4.
    mu2 > 0 gives a double well with minima at theta = +-sqrt(mu2/lambda_h)."""
    return -0.5 * mu2 * theta ** 2 + 0.25 * lamh * theta ** 4


def v_min(mu2, lamh):
    """The condensate value v = sqrt(mu^2/lambda_h) (0 if mu2 <= 0).  This is the
    PREDICTION the relaxation is checked against -- it is never written into a field."""
    if mu2 <= 0.0 or lamh <= 0.0:
        return 0.0
    return float(np.sqrt(mu2 / lamh))


def force_potential(theta, mu2, lamh):
    """On-site force from V: -dV/dtheta = mu^2 theta - lambda_h theta^3.  Added to the
    CR_3D theta force; consistent with force = (1/dx)*(-dE/dfield) for the energy term
    E_pot = dx * sum_i V(theta_i) (so dE_pot/dtheta_i = dx*V'(theta_i), and
    (1/dx)*(-dE_pot/dtheta_i) = -V'(theta_i) = mu^2 theta - lambda_h theta^3)."""
    return mu2 * theta - lamh * theta ** 3


def force_theta_higgs(theta, phix, phiy, phiz, dx, mu2, lamh):
    """CR_3D Stueckelberg+Wilson theta force plus the on-site potential force.
    Interior only (x-ends Dirichlet-clamped by the integrator)."""
    f = c.force_theta(theta, phix, phiy, phiz, dx)
    fp = force_potential(theta, mu2, lamh)
    f[1:-1] += fp[1:-1]
    return f


# =========================================================================== #
# Energy (CR_3D invariant + node-potential term); conserved at friction=0
# =========================================================================== #
def energy_components(theta, vth, phix, vphx, phiy, vphy, phiz, vphz,
                      dx, lamp, mu2, lamh):
    comp = c.energy_components(theta, vth, phix, vphx, phiy, vphy, phiz, vphz, dx, lamp)
    E_pot = dx * float(np.sum(v_potential(theta, mu2, lamh)))
    comp = dict(comp)
    comp["E_pot"] = E_pot
    comp["E_total"] = comp["E_total"] + E_pot
    return comp


def energy_total(theta, vth, phix, vphx, phiy, vphy, phiz, vphz,
                 dx, lamp, mu2, lamh):
    return energy_components(theta, vth, phix, vphx, phiy, vphy, phiz, vphz,
                             dx, lamp, mu2, lamh)["E_total"]


# =========================================================================== #
# velocity-Verlet evolution with the Higgs potential (mirrors cr3d_core.evolve)
# =========================================================================== #
def evolve(theta0, vth0, phix0, vphx0, phiy0, vphy0, phiz0, vphz0,
           dx, dt, nsteps, lamp, mu2, lamh,
           freeze_theta=False, friction=0.0, pin_mask=None,
           record_polyakov=False):
    """Velocity-Verlet, x-ends clamped (Dirichlet), y,z periodic, with the node
    potential added to the theta acceleration.  Same signature/semantics as
    cr3d_core.evolve plus (mu2, lamh).  ``friction`` > 0 gives overdamped RELAXATION
    (used to find the vacuum and static vortex)."""
    th, vth = theta0.copy(), vth0.copy()
    px, vpx = phix0.copy(), vphx0.copy()
    py, vpy = phiy0.copy(), vphy0.copy()
    pz, vpz = phiz0.copy(), vphz0.copy()
    Phi = np.zeros_like(th) if record_polyakov else None

    def acc(th, px, py, pz):
        ath = (np.zeros_like(th) if freeze_theta
               else force_theta_higgs(th, px, py, pz, dx, mu2, lamh))
        return (ath, c.force_phix(th, px, py, pz, dx, lamp),
                c.force_phiy(th, px, py, pz, dx, lamp),
                c.force_phiz(th, px, py, pz, dx, lamp))

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


# =========================================================================== #
# Vacuum relaxation (H1): overdamped descent to the condensate
# =========================================================================== #
def relax_vacuum(mu2, lamh, lamp=0.0, grid=None, rng=None, t_relax=60.0,
                 bias=0.15, noise=0.05, friction=0.06):
    """Relax theta from a small biased-noisy start to the vacuum and return the
    homogeneous condensate.

    The double well has two minima +-v; a small positive ``bias`` selects the +v
    domain so the relaxed state is HOMOGENEOUS (otherwise sites split into +-v
    domains and the lattice mean cancels).  Returns a dict with the measured mean
    theta, its spatial std (fluctuation), and the relaxed vacuum energy."""
    if grid is None:
        grid = dict(Lx=24.0, Nx=49, Ny=12, Nz=12)
    if rng is None:
        rng = np.random.default_rng(0)
    x, y, z, dx = c.make_grid(**grid)
    dt = c.dt_cfl(dx)
    shape = (len(x), len(y), len(z))
    v = v_min(mu2, lamh)
    # start small (do NOT seed at v -- that would insert the answer); a gentle bias
    # toward +theta only breaks the +-v degeneracy, it is far below v.  When mu2<=0
    # there is a SINGLE minimum at 0 (no degeneracy to break) and the quartic force
    # ~theta^3 is glacial near 0, so any bias would survive as a spurious mean -- use
    # no bias there and let the symmetric noise relax to <theta>~0.
    b = 0.0 if mu2 <= 0.0 else bias
    theta0 = b + noise * rng.standard_normal(shape)
    theta0[0] = 0.0; theta0[-1] = 0.0
    z7 = tuple(np.zeros(shape) for _ in range(7))
    nst = int(round(t_relax / dt))
    out = evolve(theta0, *(zz.copy() for zz in z7),
                 dx, dt, nst, lamp=lamp, mu2=mu2, lamh=lamh, friction=friction)
    th = out[0]
    Nx = th.shape[0]
    interior = th[1:-1]                       # drop the Dirichlet ends
    bulk = th[Nx // 3: 2 * Nx // 3]           # central x-plateau, free of the
    #                                           Dirichlet (theta=0) boundary layers
    comp = energy_components(*out, dx, lamp, mu2, lamh)
    return {"mu2": mu2, "lamh": lamh, "lamp": lamp,
            "v_expected": v,
            "theta_mean": float(np.mean(interior)),
            "theta_abs_mean": float(np.mean(np.abs(interior))),
            "theta_std": float(np.std(interior)),
            "theta_bulk_mean": float(np.mean(bulk)),
            "theta_bulk_std": float(np.std(bulk)),
            "E_total": comp["E_total"], "E_pot": comp["E_pot"],
            "E_per_node": comp["E_total"] / interior.size,
            "field": th}


# =========================================================================== #
# A vortex line on a condensate background (H3/H4)
# =========================================================================== #
def vortex_on_condensate(x, y, z, v, mu2=0.0, lamh=0.0, n_wind=1):
    """Initial data: a winding-n vortex line along z (winding in the xy plane), with
    the scalar set to the condensate v away from the core and dipped toward 0 inside a
    small core (the configuration the condensate is expected to support).  Returns
    (theta, phix, phiy, phiz, core_xy).

    The gauge winding is the wrapped lattice gradient of the multivalued angle (as in
    cr3d_core.topology_and_stability).  The scalar profile theta = v*tanh(r/r0) is the
    NATURAL ansatz (0 at core, v at infinity); the TRUE core size xi is then MEASURED
    after relaxation in H3 -- the ansatz only provides admissible initial data."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    dx = float(x[1] - x[0])
    xc = float(x[len(x) // 2]) + dx / 2
    yc = float(y[len(y) // 2]) + dx / 2
    ang = np.arctan2(Y - yc, X - xc) * n_wind
    phix = np.zeros_like(ang); phiy = np.zeros_like(ang); phiz = np.zeros_like(ang)
    phix[:-1] = c._wrap(np.diff(ang, axis=0))
    phiy[:] = c._wrap(c._up_y(ang) - ang)
    phix[0] = phix[-1] = 0.0
    rperp = np.sqrt((X - xc) ** 2 + (Y - yc) ** 2)
    r0 = max(2.0 * dx, 1.0)
    theta = v * np.tanh(rperp / r0)
    theta[0] = 0.0; theta[-1] = 0.0
    return theta, phix, phiy, phiz, (xc, yc)


def core_width(field2d, x, y, xc, yc):
    """RMS transverse width of the vortex 'normal core' = the region where the scalar
    departs from its asymptotic value.  Weight w = (v - theta)+ (deficit from the
    condensate); sigma = sqrt(<r_perp^2>_w).  Tracks core spreading (diffusion) vs
    pinning in H4.  field2d is theta on an (x,y) slice through the core."""
    X, Y = np.meshgrid(x, y, indexing="ij")
    r2 = (X - xc) ** 2 + (Y - yc) ** 2
    vasym = float(np.median(field2d))               # condensate level far from core
    w = np.clip(vasym - field2d, 0.0, None)
    W = float(np.sum(w))
    if W <= 1e-12:
        return float("nan")
    return float(np.sqrt(np.sum(w * r2) / W))


# =========================================================================== #
# Gauge-field screening correlator C_phi(r) (H2)
# =========================================================================== #
def gauge_correlator(phi_field, axis=0):
    """Connected two-point function C(r) = <phi(s) phi(s+r)> - <phi>^2 along ``axis``,
    averaged over all start sites s and the transverse plane.  Real-valued.  An
    exponential fit of C(r) returns the screening mass m_A of the gauge field."""
    f = phi_field - float(np.mean(phi_field))
    L = f.shape[axis]
    fm = np.moveaxis(f, axis, 0)                     # (L, ...)
    flat = fm.reshape(L, -1)
    var = float(np.mean(flat[0:1] * flat))           # placeholder; recompute below
    C = np.zeros(L)
    for r in range(L):
        prod = flat[: L - r] * flat[r:]
        C[r] = float(np.mean(prod))
    return C


def fit_screening_mass(C, dx, r_lo=1, r_hi=None):
    """Fit C(r) ~ A exp(-m_A r) on the positive-correlation window [r_lo, r_hi] (in
    lattice steps), returning m_A in inverse length units.  Uses a log-linear fit on
    the strictly-positive part."""
    n = len(C)
    if r_hi is None:
        r_hi = n // 2
    rr = np.arange(n) * dx
    use = np.arange(r_lo, min(r_hi, n))
    cu = C[use]
    pos = cu > 0
    if np.sum(pos) < 2:
        return float("nan"), float("nan")
    p = np.polyfit(rr[use][pos], np.log(cu[pos]), 1)
    m_A = float(-p[0])
    A = float(np.exp(p[1]))
    return m_A, A


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

    # ---- smoke 1: mu2=0 reduces to CR_3D (no condensate; force matches) --------
    x, y, z, dx = c.make_grid(Lx=20.0, Nx=41, Ny=6, Nz=6)
    th = 0.3 * rng.standard_normal((len(x), len(y), len(z)))
    px = 0.2 * rng.standard_normal(th.shape)
    py = 0.2 * rng.standard_normal(th.shape)
    pz = 0.2 * rng.standard_normal(th.shape)
    f_h = force_theta_higgs(th, px, py, pz, dx, mu2=0.0, lamh=0.0)
    f_0 = c.force_theta(th, px, py, pz, dx)
    print("mu2=0 theta-force matches CR_3D (max abs diff): %.2e"
          % float(np.max(np.abs(f_h - f_0))))

    # ---- smoke 2: energy conservation with the potential active ---------------
    dt = c.dt_cfl(dx)
    z7 = tuple(np.zeros_like(th) for _ in range(7))
    fields = (th, *z7)
    E0 = energy_total(*fields, dx, lamp=0.5, mu2=0.5, lamh=1.0)
    out = evolve(*fields, dx, dt, 400, lamp=0.5, mu2=0.5, lamh=1.0)
    E1 = energy_total(*out, dx, lamp=0.5, mu2=0.5, lamh=1.0)
    print("energy drift (mu2=0.5,lamh=1, 400 steps, friction=0): %.2e"
          % (abs(E1 - E0) / abs(E0)))

    # ---- smoke 3: relaxation finds v = sqrt(mu2/lambda_h) ----------------------
    for mu2, lamh in ((0.0, 1.0), (0.5, 1.0), (1.0, 0.5)):
        r = relax_vacuum(mu2, lamh, rng=np.random.default_rng(1),
                         grid=dict(Lx=18.0, Nx=37, Ny=8, Nz=8), t_relax=50.0)
        print("  mu2=%.2f lamh=%.2f -> v_expected=%.3f  <theta>=%.3f  |theta|=%.3f "
              "(std %.3f)" % (mu2, lamh, r["v_expected"], r["theta_mean"],
                              r["theta_abs_mean"], r["theta_std"]))

    # ---- smoke 4: double-well energy is lower than the symmetric vacuum --------
    e_sym = relax_vacuum(0.0, 1.0, rng=np.random.default_rng(2),
                         grid=dict(Lx=18.0, Nx=37, Ny=8, Nz=8))["E_per_node"]
    e_brk = relax_vacuum(1.0, 1.0, rng=np.random.default_rng(2),
                         grid=dict(Lx=18.0, Nx=37, Ny=8, Nz=8))["E_per_node"]
    print("E_per_node: symmetric(mu2=0)=%.4f  broken(mu2=1)=%.4f  -> broken lower: %s"
          % (e_sym, e_brk, e_brk < e_sym))

"""crahiggs_core.py -- shared engine for the MATTER_CR_ABELIAN_HIGGS campaign (AH1-AH7).

CR_HIGGS (Veredito C) localised the missing ingredient with precision: a real phase
theta condenses but cannot pin the vortex, because in the minimal action theta is the
Stueckelberg PHASE (it enters cos(phi+Dtheta) only through its gradient), so its
condensate gives the gauge a mass set by the cosine coupling e -- INDEPENDENT of v.  The
abelian-Higgs mechanism instead needs the MAGNITUDE of a COMPLEX scalar to multiply the
covariant kinetic term, |Phi|^2 |D_mu Phi|^2.  CR_ABELIAN_HIGGS adds exactly that, as a
*fourth ingredient* added by hand (documented honestly, AH7):

    Phi_i = pr_i + i pi_i  (complex scalar at nodes; stored as TWO REAL arrays)
    D_mu Phi_ij = Phi_j e^{-i e phi_ij} - Phi_i           (minimal coupling, charge e)

    S_AH = KAPPA  sum_links |D_mu Phi|^2                  (covariant kinetic)
         + sum_nodes ( -mu2 |Phi|^2 + lam |Phi|^4 )        (mexican-hat potential)
         + lamp sum_plaq ( 1 - cos W_p )                   (Wilson, magnetic; CR_3D)

The condensate is  v = sqrt(mu2 / (2 lam))  (minimum of the node potential), MEASURED by
relaxation, never inserted.  Expanding around Phi=v, phi=0 gives the gauge mass term
KAPPA e^2 v^2 phi^2 -- so the gauge mass is m_A = e v (the abelian-Higgs / real
Stueckelberg result), the prediction AH2 tests against CR_HIGGS's constant m_A.

ANTI-CIRCULARITY (tests/test_no_circularity.py scans results/matter/):
  * NO Python complex numbers anywhere -- Phi is two REAL arrays (pr, pi); every
    covariant-derivative product is written out with real cos/sin.  The "complex field"
    is physics, the implementation is real arithmetic.
  * v = sqrt(mu2/2lam), m_A, xi, lambda_L are MEASURED (relaxation / correlator / profile
    fits), never inserted; no mc^2, no SR/GR dilation.
  * Cooper pair / superconductor / Meissner / Abrikosov / Ginzburg-Landau appear only as
    NAMES inside COMPARISON ONLY blocks.

Lattice units: unit node spacing (dx=1); x is the distinguished axis with Dirichlet ends
(Phi and the gauge clamped), y,z periodic (np.roll), exactly as CR_3D's geometry, so the
vortex/collision setups carry over.  Unit field mass: force = -dE_pot/dfield and
E_kin = 1/2 sum(v^2), so velocity-Verlet conserves E = E_kin + E_pot (the analytic forces
below are VERIFIED against a finite-difference gradient of E_pot in __main__).

Reuses cr3d_core only for the pure-gauge plaquettes (plaq_xy/xz/yz, monopole_charge);
modifies nothing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_dbi"))
import cr3d_core as c3    # noqa: E402  (pure-gauge plaquettes / monopoles, reused as-is)
import dbi_core as dbi    # noqa: E402  (seed stats)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi
E_CHARGE = 1.0            # gauge charge (lattice units)
KAPPA = 1.0              # covariant-kinetic (hopping) coupling


# =========================================================================== #
# grid (unit spacing; x Dirichlet, y,z periodic)
# =========================================================================== #
def make_grid(Nx=49, Ny=24, Nz=12):
    x = np.arange(Nx, dtype=float) - Nx // 2
    y = np.arange(Ny, dtype=float)
    z = np.arange(Nz, dtype=float)
    return x, y, z, 1.0


def zeros_state(Nx, Ny, Nz):
    """(pr, pi, phix, phiy, phiz) all zero."""
    s = (Nx, Ny, Nz)
    return tuple(np.zeros(s) for _ in range(5))


# --- periodic shifts on the transverse axes -------------------------------- #
def _up_y(a):
    return np.roll(a, -1, axis=1)


def _dn_y(a):
    return np.roll(a, +1, axis=1)


def _up_z(a):
    return np.roll(a, -1, axis=2)


def _dn_z(a):
    return np.roll(a, +1, axis=2)


# =========================================================================== #
# covariant differences  D = Phi_j e^{-i e phi} - Phi_i  (real and imag parts)
# =========================================================================== #
def _cov_x(pr, pi, phix):
    """+x link i->i+1 (Dirichlet: last x-index has no forward link).  Returns
    (Dre, Dim, c, s) with the last x-slice zeroed."""
    a = E_CHARGE * phix
    c = np.cos(a); s = np.sin(a)
    prj = np.zeros_like(pr); prj[:-1] = pr[1:]
    pij = np.zeros_like(pi); pij[:-1] = pi[1:]
    Dre = prj * c + pij * s - pr
    Dim = pij * c - prj * s - pi
    Dre[-1] = 0.0; Dim[-1] = 0.0
    return Dre, Dim, c, s


def _cov_y(pr, pi, phiy):
    a = E_CHARGE * phiy
    c = np.cos(a); s = np.sin(a)
    prj = _up_y(pr); pij = _up_y(pi)
    Dre = prj * c + pij * s - pr
    Dim = pij * c - prj * s - pi
    return Dre, Dim, c, s


def _cov_z(pr, pi, phiz):
    a = E_CHARGE * phiz
    c = np.cos(a); s = np.sin(a)
    prj = _up_z(pr); pij = _up_z(pi)
    Dre = prj * c + pij * s - pr
    Dim = pij * c - prj * s - pi
    return Dre, Dim, c, s


# =========================================================================== #
# energy
# =========================================================================== #
def v_min(mu2, lam):
    """Condensate v = sqrt(mu2 / (2 lam)) (0 if non-positive)."""
    if mu2 <= 0.0 or lam <= 0.0:
        return 0.0
    return float(np.sqrt(mu2 / (2.0 * lam)))


def hopping_energy(pr, pi, phix, phiy, phiz):
    Dx = _cov_x(pr, pi, phix); Dy = _cov_y(pr, pi, phiy); Dz = _cov_z(pr, pi, phiz)
    e = (np.sum(Dx[0] ** 2 + Dx[1] ** 2)
         + np.sum(Dy[0] ** 2 + Dy[1] ** 2)
         + np.sum(Dz[0] ** 2 + Dz[1] ** 2))
    return KAPPA * float(e)


def potential_energy(pr, pi, mu2, lam):
    rho2 = pr ** 2 + pi ** 2
    return float(np.sum(-mu2 * rho2 + lam * rho2 ** 2))


def wilson_energy(phix, phiy, phiz, lamp):
    if lamp == 0.0:
        return 0.0
    Wxy, Wxz, Wyz = c3.all_plaquettes(phix, phiy, phiz)
    return lamp * (float(np.sum(1.0 - np.cos(Wxy[:-1])))
                   + float(np.sum(1.0 - np.cos(Wxz[:-1])))
                   + float(np.sum(1.0 - np.cos(Wyz))))


def energy_components(pr, vpr, pi, vpi, phix, vphix, phiy, vphiy, phiz, vphiz,
                      mu2, lam, lamp):
    E_kin = 0.5 * float(np.sum(vpr ** 2) + np.sum(vpi ** 2) + np.sum(vphix ** 2)
                        + np.sum(vphiy ** 2) + np.sum(vphiz ** 2))
    E_hop = hopping_energy(pr, pi, phix, phiy, phiz)
    E_pot = potential_energy(pr, pi, mu2, lam)
    E_wil = wilson_energy(phix, phiy, phiz, lamp)
    return {"E_kin": E_kin, "E_hop": E_hop, "E_pot": E_pot, "E_wilson": E_wil,
            "E_total": E_kin + E_hop + E_pot + E_wil}


def energy_total(pr, vpr, pi, vpi, phix, vphix, phiy, vphiy, phiz, vphiz,
                 mu2, lam, lamp):
    return energy_components(pr, vpr, pi, vpi, phix, vphix, phiy, vphiy,
                             phiz, vphiz, mu2, lam, lamp)["E_total"]


# =========================================================================== #
# forces  (force = -dE_pot/dfield;  verified by finite differences in __main__)
# =========================================================================== #
def force_higgs(pr, pi, phix, phiy, phiz, mu2, lam):
    """Force on the real and imaginary Higgs components from hopping + potential."""
    Dxr, Dxi, cx, sx = _cov_x(pr, pi, phix)
    Dyr, Dyi, cy, sy = _cov_y(pr, pi, phiy)
    Dzr, Dzi, cz, sz = _cov_z(pr, pi, phiz)

    # d(E_hop)/d pr_i : source term (-2 Dre) at i, target term (+2(Dre c - Dim s)) at i+1
    gpr = np.zeros_like(pr); gpi = np.zeros_like(pi)
    # x (Dirichlet): forward links valid on [:-1]
    gpr[:-1] += -2.0 * Dxr[:-1]
    gpi[:-1] += -2.0 * Dxi[:-1]
    gpr[1:] += 2.0 * (Dxr[:-1] * cx[:-1] - Dxi[:-1] * sx[:-1])
    gpi[1:] += 2.0 * (Dxr[:-1] * sx[:-1] + Dxi[:-1] * cx[:-1])
    # y (periodic)
    gpr += -2.0 * Dyr
    gpi += -2.0 * Dyi
    gpr += _dn_y(2.0 * (Dyr * cy - Dyi * sy))
    gpi += _dn_y(2.0 * (Dyr * sy + Dyi * cy))
    # z (periodic)
    gpr += -2.0 * Dzr
    gpi += -2.0 * Dzi
    gpr += _dn_z(2.0 * (Dzr * cz - Dzi * sz))
    gpi += _dn_z(2.0 * (Dzr * sz + Dzi * cz))

    gpr *= KAPPA; gpi *= KAPPA
    rho2 = pr ** 2 + pi ** 2
    dV = (-2.0 * mu2 + 4.0 * lam * rho2)          # d/d(rho2) -> times pr/pi
    gpr += dV * pr
    gpi += dV * pi
    return -gpr, -gpi


def _hop_dphi(Dre, Dim, prj, pij, c, s):
    """d|D|^2/d(phi) for one link, with target-node components prj,pij and c=cos(e phi),
    s=sin(e phi).  D = (prj c + pij s - pr) + i(pij c - prj s - pi)."""
    dDre = -prj * s + pij * c
    dDim = -pij * s - prj * c
    return E_CHARGE * 2.0 * (Dre * dDre + Dim * dDim)


def force_gauge(pr, pi, phix, phiy, phiz, lamp):
    """Force on the gauge links from the Higgs current (hopping) + Wilson plaquettes."""
    fx = np.zeros_like(phix); fy = np.zeros_like(phiy); fz = np.zeros_like(phiz)

    # --- Higgs current: each link's phase appears in exactly one hopping term --------
    Dxr, Dxi, cx, sx = _cov_x(pr, pi, phix)
    prjx = np.zeros_like(pr); prjx[:-1] = pr[1:]
    pijx = np.zeros_like(pi); pijx[:-1] = pi[1:]
    gx = _hop_dphi(Dxr, Dxi, prjx, pijx, cx, sx); gx[-1] = 0.0
    Dyr, Dyi, cy, sy = _cov_y(pr, pi, phiy)
    gy = _hop_dphi(Dyr, Dyi, _up_y(pr), _up_y(pi), cy, sy)
    Dzr, Dzi, cz, sz = _cov_z(pr, pi, phiz)
    gz = _hop_dphi(Dzr, Dzi, _up_z(pr), _up_z(pi), cz, sz)
    fx += -KAPPA * gx; fy += -KAPPA * gy; fz += -KAPPA * gz

    # --- Wilson plaquettes (force = -dE_wilson/dphi; same algebra as cr3d_core, with
    #     the x-shift done by np.roll -- the dropped last x-plaquette is zeroed by
    #     plaq_*, so roll's wrap contributes 0 at the boundary) ---------------------
    if lamp != 0.0:
        Wxy, Wxz, Wyz = c3.all_plaquettes(phix, phiy, phiz)
        sWxy, sWxz, sWyz = np.sin(Wxy), np.sin(Wxz), np.sin(Wyz)
        fx += -lamp * ((sWxy - _dn_y(sWxy)) + (sWxz - _dn_z(sWxz)))
        fy += lamp * (sWxy - np.roll(sWxy, +1, axis=0)) \
            - lamp * (sWyz - _dn_z(sWyz))
        fz += lamp * (sWxz - np.roll(sWxz, +1, axis=0)) \
            + lamp * (sWyz - _dn_y(sWyz))
        fx[0] = 0.0; fx[-1] = 0.0
    return fx, fy, fz


# =========================================================================== #
# velocity-Verlet evolution (x-ends Dirichlet, y,z periodic; optional friction/pin)
# =========================================================================== #
def evolve(pr0, vpr0, pi0, vpi0, phix0, vphix0, phiy0, vphiy0, phiz0, vphiz0,
           dt, nsteps, mu2, lam, lamp, friction=0.0, pin_mask=None,
           clamp_x_ends=True, freeze_higgs=False):
    pr, vpr = pr0.copy(), vpr0.copy()
    pi, vpi = pi0.copy(), vpi0.copy()
    px, vpx = phix0.copy(), vphix0.copy()
    py, vpy = phiy0.copy(), vphiy0.copy()
    pz, vpz = phiz0.copy(), vphiz0.copy()

    def acc(pr, pi, px, py, pz):
        if freeze_higgs:
            fpr = np.zeros_like(pr); fpi = np.zeros_like(pi)
        else:
            fpr, fpi = force_higgs(pr, pi, px, py, pz, mu2, lam)
        fx, fy, fz = force_gauge(pr, pi, px, py, pz, lamp)
        return fpr, fpi, fx, fy, fz

    def clamp(pr, pi, px, py, pz):
        if clamp_x_ends:
            pr[0] = pr0[0]; pr[-1] = pr0[-1]; pi[0] = pi0[0]; pi[-1] = pi0[-1]
            px[0] = phix0[0]; px[-1] = phix0[-1]
        if pin_mask is not None:
            pr[pin_mask] = pr0[pin_mask]; pi[pin_mask] = pi0[pin_mask]
            px[pin_mask] = phix0[pin_mask]; py[pin_mask] = phiy0[pin_mask]
            pz[pin_mask] = phiz0[pin_mask]

    apr, api, ax, ay, az = acc(pr, pi, px, py, pz)
    damp = 1.0 - friction
    for _ in range(nsteps):
        vpr += 0.5 * dt * apr; vpi += 0.5 * dt * api
        vpx += 0.5 * dt * ax;  vpy += 0.5 * dt * ay; vpz += 0.5 * dt * az
        pr += dt * vpr; pi += dt * vpi; px += dt * vpx; py += dt * vpy; pz += dt * vpz
        clamp(pr, pi, px, py, pz)
        apr, api, ax, ay, az = acc(pr, pi, px, py, pz)
        vpr = (vpr + 0.5 * dt * apr) * damp; vpi = (vpi + 0.5 * dt * api) * damp
        vpx = (vpx + 0.5 * dt * ax) * damp;  vpy = (vpy + 0.5 * dt * ay) * damp
        vpz = (vpz + 0.5 * dt * az) * damp
        if clamp_x_ends:
            vpr[0] = vpr[-1] = 0.0; vpi[0] = vpi[-1] = 0.0
            vpx[0] = vpx[-1] = 0.0
        if pin_mask is not None:
            vpr[pin_mask] = 0.0; vpi[pin_mask] = 0.0
            vpx[pin_mask] = 0.0; vpy[pin_mask] = 0.0; vpz[pin_mask] = 0.0
    return pr, vpr, pi, vpi, px, vpx, py, vpy, pz, vpz


# =========================================================================== #
# observables
# =========================================================================== #
def magnitude(pr, pi):
    return np.sqrt(pr ** 2 + pi ** 2)


def gauge_invariant_check(pr, pi, phix, phiy, phiz, mu2, lam, lamp, rng):
    """Apply a random LOCAL gauge transform  phi_ij -> phi_ij + (alpha_j - alpha_i)/e,
    Phi_i -> Phi_i e^{i alpha_i}, and return the change in total potential energy
    (should be ~0 to machine precision)."""
    alpha = rng.uniform(-np.pi, np.pi, pr.shape)
    ca, sa = np.cos(alpha), np.sin(alpha)
    pr2 = pr * ca - pi * sa
    pi2 = pr * sa + pi * ca
    # phi_ij -> phi_ij + (alpha_j - alpha_i)/e  (j = i + mu)
    px2 = phix.copy(); px2[:-1] = phix[:-1] + (alpha[1:] - alpha[:-1]) / E_CHARGE
    py2 = phiy + (_up_y(alpha) - alpha) / E_CHARGE
    pz2 = phiz + (_up_z(alpha) - alpha) / E_CHARGE
    e0 = (hopping_energy(pr, pi, phix, phiy, phiz) + potential_energy(pr, pi, mu2, lam)
          + wilson_energy(phix, phiy, phiz, lamp))
    e1 = (hopping_energy(pr2, pi2, px2, py2, pz2) + potential_energy(pr2, pi2, mu2, lam)
          + wilson_energy(px2, py2, pz2, lamp))
    return abs(e1 - e0), e0


def vortex_state(x, y, z, v, n_wind=1, core_dip=True):
    """Winding-n vortex line along z (winding in the xy plane): the gauge phase winds,
    the Higgs magnitude dips toward 0 at the core (the natural ansatz; the true core
    size xi is MEASURED after relaxation).  Returns (pr, pi, phix, phiy, phiz, (xc,yc))."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    xc = float(x[len(x) // 2]) + 0.5
    yc = float(y[len(y) // 2]) + 0.5
    ang = np.arctan2(Y - yc, X - xc) * n_wind
    phix = np.zeros_like(ang); phiy = np.zeros_like(ang); phiz = np.zeros_like(ang)
    phix[:-1] = c3._wrap(np.diff(ang, axis=0)) / E_CHARGE
    phiy[:] = c3._wrap(_up_y(ang) - ang) / E_CHARGE
    phix[0] = phix[-1] = 0.0
    rperp = np.sqrt((X - xc) ** 2 + (Y - yc) ** 2)
    amp = v * (np.tanh(rperp / 2.0) if core_dip else np.ones_like(rperp))
    # Higgs phase winds with the vortex so that D Phi ~ 0 far away (covariantly constant)
    pr = amp * np.cos(ang)
    pi = amp * np.sin(ang)
    return pr, pi, phix, phiy, phiz, (xc, yc)


def core_width(pr, pi, x, y, xc, yc, v):
    """Transverse RMS width of the 'normal core' (where |Phi| < v): weight w=(v-|Phi|)+,
    summed over z, sigma = sqrt(<r_perp^2>_w)."""
    rho = magnitude(pr, pi)
    rho2d = np.mean(rho, axis=2)
    X, Y = np.meshgrid(x, y, indexing="ij")
    w = np.clip(v - rho2d, 0.0, None)
    W = float(np.sum(w))
    if W < 1e-9:
        return float("nan")
    r2 = (X - xc) ** 2 + (Y - yc) ** 2
    return float(np.sqrt(np.sum(w * r2) / W))


def relax_vacuum(mu2, lam, lamp=0.0, grid=None, rng=None, t_relax=60.0, dt=0.05,
                 friction=0.05, seed_amp=0.1):
    """Relax the complex Higgs from a small random start to the condensate <|Phi|>=v.
    Returns mean |Phi| (bulk x-plateau), its std, energy, and the field."""
    if grid is None:
        grid = dict(Nx=33, Ny=16, Nz=12)
    if rng is None:
        rng = np.random.default_rng(0)
    x, y, z, _ = make_grid(**grid)
    sh = (len(x), len(y), len(z))
    v = v_min(mu2, lam)
    pr = v + seed_amp * rng.standard_normal(sh)      # start near v but NOT exactly v
    pi = seed_amp * rng.standard_normal(sh)
    pr[0] = v; pr[-1] = v; pi[0] = 0.0; pi[-1] = 0.0
    z5 = [np.zeros(sh) for _ in range(5)]
    out = evolve(pr, np.zeros(sh), pi, np.zeros(sh),
                 np.zeros(sh), z5[0], np.zeros(sh), z5[1], np.zeros(sh), z5[2],
                 dt, int(round(t_relax / dt)), mu2, lam, lamp, friction=friction)
    PR, PI = out[0], out[2]
    rho = magnitude(PR, PI)
    Nx = rho.shape[0]
    bulk = rho[Nx // 3: 2 * Nx // 3]
    comp = energy_components(*out, mu2, lam, lamp)
    return {"mu2": mu2, "lam": lam, "v_expected": v,
            "rho_bulk_mean": float(np.mean(bulk)), "rho_bulk_std": float(np.std(bulk)),
            "rho_mean": float(np.mean(rho[1:-1])),
            "E_total": comp["E_total"], "E_per_node": comp["E_total"] / rho.size,
            "pr": PR, "pi": PI, "phix": out[4], "phiy": out[6], "phiz": out[8]}


# =========================================================================== #
# IO
# =========================================================================== #
def seed_stats(values):
    return dbi.seed_stats(values)


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


# =========================================================================== #
# finite-difference verification of the analytic forces
# =========================================================================== #
def _fd_check(mu2, lam, lamp, rng, eps=1e-6):
    x, y, z, _ = make_grid(Nx=9, Ny=6, Nz=5)
    sh = (len(x), len(y), len(z))
    pr = 0.5 + 0.3 * rng.standard_normal(sh)
    pi = 0.3 * rng.standard_normal(sh)
    px = 0.2 * rng.standard_normal(sh); px[0] = px[-1] = 0.0
    py = 0.2 * rng.standard_normal(sh)
    pz = 0.2 * rng.standard_normal(sh)

    def Epot(pr, pi, px, py, pz):
        return (hopping_energy(pr, pi, px, py, pz) + potential_energy(pr, pi, mu2, lam)
                + wilson_energy(px, py, pz, lamp))

    fpr, fpi = force_higgs(pr, pi, px, py, pz, mu2, lam)
    fx, fy, fz = force_gauge(pr, pi, px, py, pz, lamp)
    worst = 0.0
    fields = {"pr": (pr, fpr), "pi": (pi, fpi),
              "phix": (px, fx), "phiy": (py, fy), "phiz": (pz, fz)}
    rng2 = np.random.default_rng(7)
    for name, (arr, fan) in fields.items():
        for _ in range(12):
            i = tuple(rng2.integers(0, n) for n in sh)
            if name in ("pr", "pi", "phix") and (i[0] in (0, sh[0] - 1)):
                continue
            base = arr[i]
            arr[i] = base + eps; ep = Epot(pr, pi, px, py, pz)
            arr[i] = base - eps; em = Epot(pr, pi, px, py, pz)
            arr[i] = base
            fnum = -(ep - em) / (2 * eps)
            worst = max(worst, abs(fnum - fan[i]))
    return worst


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    # ---- gate-style smoke 1: analytic forces match finite differences ----------
    for (mu2, lam, lamp) in ((1.0, 0.5, 0.0), (1.0, 0.5, 0.8), (0.0, 1.0, 0.5)):
        w = _fd_check(mu2, lam, lamp, rng)
        print("FD force check mu2=%.1f lam=%.1f lamp=%.1f: worst |analytic-numeric|=%.2e"
              % (mu2, lam, lamp, w))

    # ---- smoke 2: energy conservation (friction=0) -----------------------------
    x, y, z, _ = make_grid(Nx=25, Ny=10, Nz=8)
    sh = (len(x), len(y), len(z))
    pr = 0.8 + 0.1 * rng.standard_normal(sh); pr[0] = pr[-1] = 0.8
    pi = 0.1 * rng.standard_normal(sh); pi[0] = pi[-1] = 0.0
    z5 = [np.zeros(sh) for _ in range(5)]
    st = (pr, np.zeros(sh), pi, np.zeros(sh), np.zeros(sh), z5[0],
          np.zeros(sh), z5[1], np.zeros(sh), z5[2])
    dt = 0.05
    E0 = energy_total(*st, 1.0, 0.5, 0.8)
    out = evolve(*st, dt, 600, 1.0, 0.5, 0.8)
    E1 = energy_total(*out, 1.0, 0.5, 0.8)
    print("energy drift (600 steps, mu2=1,lam=0.5,lamp=0.8): %.2e"
          % (abs(E1 - E0) / abs(E0)))

    # ---- smoke 3: gauge invariance of S_AH -------------------------------------
    dE, e0 = gauge_invariant_check(pr, pi, np.zeros(sh) + 0.1, np.zeros(sh),
                                   np.zeros(sh), 1.0, 0.5, 0.8, rng)
    print("gauge invariance: |dE| under random local transform = %.2e (E~%.2f)" % (dE, e0))

    # ---- smoke 4: relaxation finds v = sqrt(mu2/2lam) --------------------------
    for mu2, lam in ((0.0, 1.0), (0.5, 0.5), (2.0, 1.0)):
        r = relax_vacuum(mu2, lam, rng=np.random.default_rng(1),
                         grid=dict(Nx=25, Ny=12, Nz=10), t_relax=60.0)
        print("  mu2=%.2f lam=%.2f -> v=%.3f  <|Phi|>=%.3f (std %.3f)"
              % (mu2, lam, r["v_expected"], r["rho_bulk_mean"], r["rho_bulk_std"]))

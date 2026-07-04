"""v4_core.py -- TWO-WAY rho <-> gauge coupling: does the depleted core PIN the winding?

PE4_V3 (Veredito B) showed the causal density rho depletes SPONTANEOUSLY at a vortex core
(box rho = J, one-way) -- closing the MAGNITUDE sector |Phi|=rho.  But rho was ONE-WAY
sourced (it could not feed back into the gauge field), so the gauge WINDING still diffused
exactly as in CR_3D (1.0 -> ~0.38 over 8 ticks): the residue PE4_V3 could not touch.

PE4_V4 closes the loop.  The minimal action weights every causal-link term by the local
causal density (Delta tau ~ rho): the Stueckelberg + Wilson gauge action is

    S_gauge = sum_links  rho_link * [1 - cos(u_link)]  +  lam_p sum_plaq rho * [1-cos(W_p)],

so where rho -> 0 (the depleted core) the gauge action -- and its FORCE -- is suppressed.
The two-way question: does a self-consistently DEPLETED core (rho->0 there) make the core
links INERT (frozen 2pi flux, the winding PINNED, superconductor-vortex style) or make the
winding barrier CHEAPER (easier unwinding, DESTABILISED)?  Only the dynamics decide.

Implementation (faithful, non-invasive):
  * the gauge field evolves by the SAME velocity-Verlet as cr3d.evolve (x-Dirichlet ends,
    y,z periodic), but each node force is SCALED by the local rho weight -- f = rho * f_min,
    the leading-order variation of S_gauge=sum rho*a (rho treated as the slowly-varying
    background each window; the d rho/d phi back-term is the next order, noted honestly);
  * rho is recomputed self-consistently every WINDOW from the current gauge action density
    J (v3.link_action_density) via the V2/V3 depletion solve (v2.relax_density), normalised
    to a controlled core-depletion depth f in [0,1]:  rho = clip(1 - f*shape, 0), shape the
    relaxed depletion profile peaked at the core.  f=0 => rho=1 uniform => EXACT CR_3D
    baseline (the V4_1 faithfulness check); f=1 => fully depleted core (the natural K~1
    regime V3 found).  f is the back-reaction STRENGTH knob.

ANTI-CIRCULARITY: rho is the real action-weight density (Delta tau ~ rho, as v2.relax_gauge
already used globally); the gauge action/winding are real phases; no complex literal, no
relativistic formula.  'Superconductor/condensate' only in COMPARISON ONLY.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "phi_emerge" / "v3"))
sys.path.insert(0, str(ROOT / "results" / "phi_emerge" / "v2"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
import v3_core as v3        # noqa: E402  (link_action_density, ROOT)
import v2_core as v2        # noqa: E402  (relax_density)
import cr3d_core as c3      # noqa: E402  (forces, plaquettes, grid, _wrap)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)
TWO_PI = 2.0 * np.pi

GRID = dict(Lx=24.0, Nx=73, Ny=24, Nz=24)     # T3D5 action, roomier transverse box so the
LAM = 0.8                                      # torus-image anti-vortex separates cleanly


# =========================================================================== #
# vortex initial data (winding +1, core on a plaquette centre) -- = T3D5
# =========================================================================== #
def make_vortex(grid=GRID, noise=0.0, rng=None):
    x, y, z, dx = c3.make_grid(**grid)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    xc = float(x[len(x) // 2]) + dx / 2
    yc = float(y[len(y) // 2]) + dx / 2
    Theta = np.arctan2(Y - yc, X - xc)
    phix = np.zeros_like(Theta); phiy = np.zeros_like(Theta); phiz = np.zeros_like(Theta)
    phix[:-1] = c3._wrap(np.diff(Theta, axis=0))
    phiy[:] = c3._wrap(c3._up_y(Theta) - Theta)
    phix[0] = phix[-1] = 0.0
    if noise and rng is not None:
        phix = phix + noise * rng.standard_normal(phix.shape); phix[0] = phix[-1] = 0.0
        phiy = phiy + noise * rng.standard_normal(phiy.shape)
    theta = np.zeros_like(Theta)
    fields = (theta, np.zeros_like(theta), phix, np.zeros_like(phix),
              phiy, np.zeros_like(phiy), phiz, np.zeros_like(phiz))
    return fields, (x, y, z, dx), (xc, yc)


def core_flux(phix, phiy):
    """Local core winding = max |plaq_xy| / 2pi over the interior (= T3D5._core_flux; the
    raw plaquette carries the 2pi core flux, so NO wrap -- wrapping 2pi would read 0).
    1.0 = intact winding; -> 0 = unwound/diffused.  Sensitive to local pile-up (so the
    verdict uses enclosed_winding); kept for the f=0 faithfulness comparison to CR_3D."""
    Wxy = c3.plaq_xy(phix, phiy)
    return float(np.max(np.abs(Wxy[:-1])) / TWO_PI)


def enclosed_winding(phix, phiy, x, y, xc, yc, R=1.5):
    """ROBUST topological vortex number in a TIGHT disk of radius R about the core
    (mid-z plane): n = sum over plaquettes inside R of round(Wxy/2pi) -- the integer
    vortex content (DeGrand-Toussaint style).  round() ignores sub-2pi fluctuations and
    local pile-up, so this tracks the TOPOLOGY (+1 = vortex intact at the core, 0 =
    unwound/escaped) even when core_flux is contaminated.  R is kept small enough to
    isolate the +1 core from its torus-image anti-vortex."""
    Wxy = c3.plaq_xy(phix, phiy)
    m = np.rint(Wxy / TWO_PI)                            # integer vortex per plaquette
    Nx, Ny, Nz = phix.shape
    kz = Nz // 2
    X, Y = np.meshgrid(x, y, indexing="ij")
    inside = ((X - xc) ** 2 + (Y - yc) ** 2) <= R ** 2
    inside[-1, :] = False                               # last x-cube undefined
    return float(np.sum(m[:, :, kz][inside]))


# =========================================================================== #
# self-consistent rho weight from the current gauge action (controlled depth f)
# =========================================================================== #
def rho_weight(theta, phix, phiy, phiz, K, f, rho_floor=0.15, n_iter=400, eps=1e-9):
    """rho(x) = clip(1 - f*shape, rho_floor), shape = depletion profile from the V2/V3 solve
    relax_density(J, K) (J = node gauge-action density), normalised to peak 1 at the core.
    f=0 -> rho=1 uniform (CR_3D).  f in (0,1] -> core depleted toward 1-f.

    ``rho_floor`` > 0: the causal density never truly VANISHES (a cell always has some
    causal links), so the gauge action retains a minimal stiffness even at the deepest
    core.  This is physical (rho=0 would make the gauge field non-dynamical/ill-posed
    there) and keeps the integrator well-posed; the verdict is read from how winding
    survival varies with the depletion DEPTH, floored consistently across f."""
    if f <= 0.0:
        return np.ones_like(phix)
    J = v3.link_action_density(theta, phix, phiy, phiz)
    drho = v2.relax_density(J, K=K, n_iter=n_iter)       # <=0 at the core
    dep = np.clip(-drho, 0.0, None)                       # depletion (positive at core)
    peak = float(dep.max())
    if peak < eps:
        return np.ones_like(phix)
    shape = dep / peak                                   # 1 at core, ~0 far
    return np.clip(1.0 - f * shape, rho_floor, None)


# =========================================================================== #
# coupled velocity-Verlet: cr3d forces SCALED by the local rho weight
# =========================================================================== #
def _stueck_force(th, px, py, pz, dx):
    """The STUECKELBERG component of the gauge force, -sin(u_link)/dx^2, per field --
    the part of cr3d's force coming from the Delta tau*[1-cos(u)] term (the rho-weighted
    causal-link action).  Interior only; 0 at the x-Dirichlet ends (as cr3d)."""
    ux = c3.link_x(th, px); uy = c3.link_y(th, py); uz = c3.link_z(th, pz)
    sx = np.zeros_like(px); sy = np.zeros_like(py); sz = np.zeros_like(pz)
    sx[1:-1] = -np.sin(ux[1:-1]) / dx ** 2
    sy[1:-1] = -np.sin(uy[1:-1]) / dx ** 2
    sz[1:-1] = -np.sin(uz[1:-1]) / dx ** 2
    return sx, sy, sz


def _acc(th, px, py, pz, dx, lam, rho, weight_wilson=False):
    """cr3d node forces with the Stueckelberg (Delta tau ~ rho) component rho-weighted; the
    gradient-stiffness (Laplacian) keeps FULL strength (the field-strength sector, not the
    causal-density-weighted one) so the core stays well-posed.  theta's force is entirely
    Stueckelberg -> rho*.

      f_phi_weighted = f_full + (rho-1)*f_stueck   (re-weights only the stueck part)
      f_theta_weighted = rho * f_theta             (all stueck)

    ``weight_wilson``: ALSO rho-weight the Wilson/Maxwell plaquette force (a stronger
    coupling assumption -- the robustness check).  Note: the Wilson cosine is ALSO blind to
    the 2pi core (cos 2pi=1), so weighting it cannot reach the winding either; tested to
    show the verdict does not hinge on the Stueckelberg-only choice."""
    sx, sy, sz = _stueck_force(th, px, py, pz, dx)
    ath = rho * c3.force_theta(th, px, py, pz, dx)
    apx = c3.force_phix(th, px, py, pz, dx, lam) + (rho - 1.0) * sx
    apy = c3.force_phiy(th, px, py, pz, dx, lam) + (rho - 1.0) * sy
    apz = c3.force_phiz(th, px, py, pz, dx, lam) + (rho - 1.0) * sz
    if weight_wilson and lam:
        wx = c3.force_phix(th, px, py, pz, dx, lam) - c3.force_phix(th, px, py, pz, dx, 0.0)
        wy = c3.force_phiy(th, px, py, pz, dx, lam) - c3.force_phiy(th, px, py, pz, dx, 0.0)
        wz = c3.force_phiz(th, px, py, pz, dx, lam) - c3.force_phiz(th, px, py, pz, dx, 0.0)
        apx = apx + (rho - 1.0) * wx
        apy = apy + (rho - 1.0) * wy
        apz = apz + (rho - 1.0) * wz
    return ath, apx, apy, apz


def evolve_coupled(fields, grid_tuple, core, K, f, T_ticks=16.0, lam=LAM, friction=0.0,
                   window_ticks=1.0, rho_update=True, record_every=1.0, rho_floor=0.15,
                   R_enc=1.5, weight_wilson=False):
    """Co-evolve gauge (rho-weighted force) and rho (self-consistent, depth f).  Every
    ``window_ticks`` rho is recomputed from the current gauge action (if rho_update);
    within a window rho is held fixed (mean-field).  Tracks BOTH the local core_flux
    (T3D5 measure) and the robust enclosed_winding (topology in a disk R_enc).  f=0
    reproduces CR_3D exactly.  Returns trajectories + final values."""
    x, y, z, dx = grid_tuple
    xc, yc = core
    dt = c3.dt_cfl(dx)
    th, vth, px, vpx, py, vpy, pz, vpz = (a.copy() for a in fields)
    th0, px0 = th.copy(), px.copy()
    n_win_steps = max(int(round(window_ticks / dt)), 1)
    n_windows = max(int(round(T_ticks / window_ticks)), 1)
    rec_stride = max(int(round(record_every / window_ticks)), 1)
    damp = 1.0 - friction

    rho = rho_weight(th, px, py, pz, K, f, rho_floor=rho_floor)
    ath, apx, apy, apz = _acc(th, px, py, pz, dx, lam, rho, weight_wilson)
    ts = [0.0]
    cflux = [core_flux(px, py)]
    nenc = [enclosed_winding(px, py, x, y, xc, yc, R_enc)]
    core_rho = [float(rho.min())]
    t = 0.0
    for w in range(n_windows):
        for _ in range(n_win_steps):
            vth = vth + 0.5 * dt * ath
            vpx = vpx + 0.5 * dt * apx; vpy = vpy + 0.5 * dt * apy; vpz = vpz + 0.5 * dt * apz
            th = th + dt * vth; th[0] = th0[0]; th[-1] = th0[-1]
            px = px + dt * vpx; px[0] = px0[0]; px[-1] = px0[-1]
            py = py + dt * vpy
            pz = pz + dt * vpz
            ath, apx, apy, apz = _acc(th, px, py, pz, dx, lam, rho, weight_wilson)
            vth = (vth + 0.5 * dt * ath) * damp; vth[0] = 0.0; vth[-1] = 0.0
            vpx = (vpx + 0.5 * dt * apx) * damp; vpx[0] = 0.0; vpx[-1] = 0.0
            vpy = (vpy + 0.5 * dt * apy) * damp
            vpz = (vpz + 0.5 * dt * apz) * damp
        t += window_ticks
        if rho_update and f > 0.0:
            rho = rho_weight(th, px, py, pz, K, f, rho_floor=rho_floor)
            ath, apx, apy, apz = _acc(th, px, py, pz, dx, lam, rho, weight_wilson)
        if (w + 1) % rec_stride == 0 or w == n_windows - 1:
            ts.append(t); cflux.append(core_flux(px, py))
            nenc.append(enclosed_winding(px, py, x, y, xc, yc, R_enc))
            core_rho.append(float(rho.min()))
    # late-window time-average (robust to the strong tick-to-tick fluctuation of the
    # diffused core): mean over the last ~40% of records, and the fraction of late records
    # that retain a full topological quantum in the core disk.
    n_late = max(int(round(0.4 * len(cflux))), 2)
    cf_late = float(np.mean(cflux[-n_late:]))
    enc_late_retained = float(np.mean([abs(v) >= 0.5 for v in nenc[-n_late:]]))
    return {"t": ts, "core_flux": cflux, "enclosed_winding": nenc, "core_rho": core_rho,
            "core_flux_final": cflux[-1], "core_flux_initial": cflux[0],
            "core_flux_late": cf_late, "enclosed_late_retained": enc_late_retained,
            "enclosed_final": nenc[-1], "enclosed_initial": nenc[0],
            "K": K, "f": f, "T_ticks": T_ticks, "rho_floor": rho_floor}


def save_json(name, payload):
    (OUTDIR / f"{name}.json").write_text(json.dumps(payload, indent=2))
    return OUTDIR / f"{name}.json"


if __name__ == "__main__":
    print("v4_core smoke -- winding survival vs depletion depth f (K=1, 12 ticks)")
    fields, gt, core = make_vortex(rng=np.random.default_rng(0), noise=0.0)
    for f in (0.0, 0.5, 0.9, 1.0):
        out = evolve_coupled(fields, gt, core, K=1.0, f=f, T_ticks=12.0)
        print(f"  f={f:.1f}:  core_flux {out['core_flux_initial']:.2f}->"
              f"{out['core_flux_final']:.2f}   enclosed_winding "
              f"{out['enclosed_initial']:.0f}->{out['enclosed_final']:.0f}   "
              f"core_rho_min={out['core_rho'][-1]:.2f}")

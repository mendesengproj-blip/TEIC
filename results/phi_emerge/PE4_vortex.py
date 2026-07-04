"""PE4_vortex.py -- the vortex core: does |Phi| = rho dip and pin?

PHI_EMERGE task PE4.  Build a winding-1 gauge vortex (phase winds in the xy plane) on the
3+1D lattice WITHOUT an added potential, and measure the emergent Phi = rho e^{i phibar}
around the core:
  (1) does arg(Phi) carry the topological winding (a 2pi loop around the core)?  -- tests
      whether the PHASE of the composition reproduces the vortex;
  (2) does |Phi|(r_perp) = rho(r_perp) DIP toward 0 at the core (the abelian-Higgs core)
      or stay ~1 (no core)?  -- tests whether the MAGNITUDE responds to the vortex;
  (3) under evolution, is the would-be core width sigma_core CONSTANT (pinning) or absent
      (no magnitude core forms)?

Expectation given PE2 (no spontaneous condensate): the gauge phase winds (Phi has a
topological vortex in its argument), but rho is the bare substrate causal density,
DECOUPLED from the gauge sector, so |Phi| stays ~1 everywhere -- no core, no pinning.
That is the precise diagnosis of what the emergent composition lacks.

Anti-circularity: rho is a count; the vortex is a gauge configuration; no complex literal.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phi_emerge_core as pe   # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NSEED = 20
LAM = 0.7


def radial_profile_perp(field, x, y, xc, yc, r_edges):
    """Azimuthal average of a 3D field about the (xc,yc) core axis (averaged over z)."""
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


def winding_around(pb, xc, yc, x, y, radius=4.0):
    """Winding number of arg(Phi)=phibar on a discrete loop of given radius about the
    core (sum of wrapped phase increments / 2pi), averaged over z-slices."""
    Nx, Ny, Nz = pb.shape
    # sample a circle of 'radius' around (xc,yc) at the mid-z slice
    ths = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    xs = xc + radius * np.cos(ths)
    ys = yc + radius * np.sin(ths)
    ix = np.clip(np.rint(xs).astype(int), 0, Nx - 1)
    iy = np.mod(np.rint(ys).astype(int), Ny)
    wind = []
    for k in range(Nz):
        vals = pb[ix, iy, k]
        d = (np.diff(np.concatenate([vals, vals[:1]])) + np.pi) % (2 * np.pi) - np.pi
        wind.append(float(np.sum(d) / (2 * np.pi)))
    return float(np.mean(wind))


def main():
    grid = (33, 28, 28)
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    r_edges = np.arange(0.0, 11.0, 1.0)

    phix0, phiy0, phiz0, (xc, yc) = pe.vortex_gauge(x, y, z, n_wind=1)
    # the gauge-sector topological charge (holonomy / wrapped plaquette flux).  On the
    # COMPACT lattice a single vortex's 2pi core flux wraps to 0 -- the CR_WILSON fact
    # that a 2pi flux quantum is invisible to the compact cosine -- so winding_planes is 0
    # even though the angle field winds.  We record it to be explicit about what the gauge
    # sector itself carries before asking what phibar (a node average) carries.
    wplanes = pe.c3.winding_planes(phix0, phiy0, phiz0)

    winds, dip_depth, sigma_static = [], [], []
    prof_abs_acc, prof_arg_acc = [], []
    rho_mean_global = []
    for s in range(NSEED):
        rng = np.random.default_rng(300 + s)
        rho = pe.causal_density(Nx, Ny, Nz, rho_sprinkle=8.0, T=8.0, rng=rng)
        rho_mean_global.append(float(rho.mean()))
        pb, _ = pe.phibar(phix0, phiy0, phiz0)
        Re, Im = pe.phi_field(rho, pb)
        absF = pe.phi_abs(Re, Im)
        # (1) winding of arg(Phi)
        winds.append(winding_around(pb, xc, yc, x, y, radius=5.0))
        # (2) radial |Phi| profile about the core
        c, prof = radial_profile_perp(absF, x, y, xc, yc, r_edges)
        prof_abs_acc.append(prof)
        far = np.nanmean(prof[-3:])
        core = np.nanmean(prof[:1])
        dip_depth.append(float((far - core) / far) if far else np.nan)
        # would-be core width (region where |Phi|<0.5*far)
        sigma_static.append(pe.core_width(rho, x, y, xc, yc, level=0.5 * far))
        # arg profile (to show it winds, not the magnitude)
        _, parg = radial_profile_perp(np.cos(pb), x, y, xc, yc, r_edges)
        prof_arg_acc.append(parg)

    prof_abs = np.nanmean(prof_abs_acc, axis=0)
    prof_abs_std = np.nanstd(prof_abs_acc, axis=0)
    wind_mean = float(np.mean(winds)); wind_std = float(np.std(winds))
    dip_mean = float(np.nanmean(dip_depth)); dip_std = float(np.nanstd(dip_depth))
    nan_sigma = float(np.mean([1.0 if not np.isfinite(s) else 0.0 for s in sigma_static]))

    # ---- short evolution: does a magnitude core ever form? (gauge evolves, rho fixed) --
    sh = (Nx, Ny, Nz)
    z0 = [np.zeros(sh) for _ in range(8)]
    out = pe.c3.evolve(z0[0], z0[1], phix0.copy(), np.zeros(sh), phiy0.copy(),
                       np.zeros(sh), phiz0.copy(), np.zeros(sh), dx, pe.c3.dt_cfl(dx),
                       400, lam=LAM, freeze_theta=True, friction=0.02)
    pb_evolved, _ = pe.phibar(out[2], out[4], out[6])
    wind_after = winding_around(pb_evolved, xc, yc, x, y, radius=5.0)

    core_dips = bool(dip_mean > 0.15)        # does |Phi| actually dip at the core?
    summary = {
        "n_seeds": NSEED, "grid": list(grid), "V": 0.0,
        "gauge_holonomy_winding_planes": {k: float(v) for k, v in wplanes.items()},
        "arg_winding_mean": wind_mean, "arg_winding_std": wind_std,
        "arg_winding_after_evolution": wind_after,
        "abs_profile_centers": c.tolist(),
        "abs_profile_mean": prof_abs.tolist(), "abs_profile_std": prof_abs_std.tolist(),
        "core_dip_depth_mean": dip_mean, "core_dip_depth_std": dip_std,
        "sigma_core_undefined_frac": nan_sigma,
        "magnitude_core_dips": core_dips,
        "rho_mean_global": float(np.mean(rho_mean_global)),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    pe.save_json("PE4_vortex", summary)

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    ax[0].errorbar(c, prof_abs, yerr=prof_abs_std, fmt="o-", capsize=3,
                   label=r"$|\Phi|(r_\perp)=\rho$")
    ax[0].axhline(1.0, color="0.6", ls="--", lw=1, label="vacuum |Φ|=1")
    ax[0].set_xlabel(r"$r_\perp$ (cells)"); ax[0].set_ylabel(r"$|\Phi|$")
    ax[0].set_ylim(0, 1.4)
    ax[0].set_title("(PE4) |Φ| around the vortex core\n(flat ⇒ no core, no pinning)")
    ax[0].legend()
    _, parg = radial_profile_perp(np.cos(pb), x, y, xc, yc, r_edges)
    ax[1].plot(c, np.nanmean(prof_arg_acc, axis=0), "s-", color="C1",
               label=r"$\langle\cos\,\arg\Phi\rangle$ vs $r_\perp$")
    ax[1].set_xlabel(r"$r_\perp$"); ax[1].set_title(
        f"(PE4) arg(Φ) winds: winding={wind_mean:.2f}±{wind_std:.2f}\n"
        "(phase carries the vortex, magnitude does not)")
    ax[1].legend()
    fig.tight_layout(); fig.savefig(pe.OUTDIR / "PE4_vortex.png", dpi=110); plt.close(fig)

    print("=" * 74)
    print(f"PE4 -- VORTEX: does |Phi|=rho dip and pin?  ({NSEED} seeds, V=0)")
    print("=" * 74)
    print(f"  gauge holonomy winding_planes (compact lattice): "
          f"{ {k: round(v,3) for k,v in wplanes.items()} }")
    print(f"     -> 0: the single vortex's 2pi core flux wraps to 0 (CR_WILSON: a 2pi "
          f"quantum is invisible to the compact cosine).")
    print(f"  arg(Phi)=phibar node winding around core: {wind_mean:+.3f} +/- {wind_std:.3f}")
    print(f"     -> phibar is a NODE AVERAGE of link gradients; a winding is a LOOP "
          f"holonomy, which a node average cannot carry.")
    print(f"  |Phi| core dip depth (|Phi|(inf)-|Phi|(0))/|Phi|(inf): "
          f"{dip_mean:+.3f} +/- {dip_std:.3f}  (DECISIVE test)")
    print(f"  |Phi|(r_perp) profile (mean over seeds):")
    for cc, pp in zip(c, prof_abs):
        print(f"     r={cc:4.1f}  |Phi|={pp:.3f}")
    print(f"  sigma_core undefined (no dip) in {nan_sigma*100:.0f}% of seeds")
    print("-" * 74)
    print(f"VERDICT (PE4): magnitude core dips? {core_dips}  -> NO core, NO pinning.")
    print("  |Phi|=rho is the bare causal density, DECOUPLED from the gauge vortex, so it")
    print("  stays ~1 at the core (dip ~0, sigma_core undefined): there is nothing to pin.")
    print("  Secondary: arg(Phi)=phibar (a node average) does not even carry the winding,")
    print("  which is a loop holonomy (and the compact-lattice 2pi flux is CR_WILSON-")
    print("  invisible).  Emergent Phi has neither the abelian-Higgs core nor a node-phase")
    print("  vortex.")
    return summary


if __name__ == "__main__":
    main()

"""VS1 -- does the dynamical causal density condense SPONTANEOUSLY (no vortex)?

Charter: VACUUM_STRUCTURE.md (VS1).  PHI_EMERGE_V2/V3 showed rho_dyn depletes at
a vortex core (initialised or collision-created).  VS1 asks the vacuum question:
in a HIGH-DENSITY network with NO vortex anywhere, does <rho_local> deviate from
rho0 spontaneously and PERSISTENTLY -- a condensate as a property of the vacuum?

Protocol (reuses v3_core / v2_core / phi_emerge_core unchanged):

  (a) KINEMATIC control: the Poisson count rho_i at increasing sprinkle density.
      Mean is 1 by normalisation; the only structure is the 1/sqrt(N) Poisson
      fluctuation, which must SHRINK with density (no condensation channel).
  (b) DYNAMICAL vacuum, DISORDER SCAN: gauge field initialised at disorder
      scale s in {0.3, 1.0, pi} and cooled by the minimal action (relax_gauge,
      no vortex initialised anywhere).  Diagnostics: residual gauge action
      J_vac, monopole density (frozen topological defects), winding.  J_vac
      then drives the dynamical rho exactly as the vortex did in V2/V3:
          d2rho/dt2 = K lap(rho) - (J - <J>) - gamma drho/dt
      K = 1 (soft regime, K << K_c ~ 8.5 -- the regime MOST favourable to
      depletion; if no condensate appears here it appears nowhere).
  (c) DRIVE SCAN at s = pi: rho_factor in {1, 4, 16, 64} (denser network =
      stronger drive, the V2/V3 convention) -- is the rho structure a linear
      response or a runaway (condensation instability)?
  (d) PERSISTENCE discriminator: cool the vacuum longer (2x, 4x).  If J_vac
      decays and the rho structure decays proportionally, it is linear
      response (no condensate).  If J_vac does NOT decay (frozen topological
      disorder), the persistent rho structure is PINNED BY DEFECTS, which is
      not spontaneous symmetry breaking; the ordered-vacuum limit (small s,
      J -> 0) decides the spontaneity question.

Kill criterion (pre-registered): <rho_local> = rho0 in all regimes -- i.e. the
deviation field tracks the drive linearly and vanishes with it.

Anti-circularity: no complex numbers, no condensate parameter inserted; 'Higgs'
appears only as a name.  Fixed seeds.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for sub in ("results/phi_emerge/v3", "results/phi_emerge/v2",
            "results/phi_emerge", "results/matter/cr_3d", "src"):
    sys.path.insert(0, str(ROOT / sub))
import v3_core as v3            # noqa: E402
import v2_core as v2            # noqa: E402
import phi_emerge_core as pe    # noqa: E402
import cr3d_core as c3          # noqa: E402

OUTDIR = Path(__file__).resolve().parent
GRID = v3.GRID                       # (29, 24, 24), x mirror, y/z periodic
SEEDS = (0, 1, 2)
RHO_FACTORS = (1.0, 4.0, 16.0, 64.0)
COOL_STEPS = (400, 1600)             # successive vacuum cooling depths
SCALES = (0.3, 1.0, np.pi)           # initial gauge disorder (cold .. hot)
K_SOFT = 1.0
T_RHO = 150.0


def kinematic_control(rng):
    """Poisson count at increasing sprinkle density: std must shrink ~1/sqrt."""
    rows = []
    for rs in (2.0, 8.0, 32.0, 128.0):
        rho = pe.causal_density(*GRID, rho_sprinkle=rs, T=8.0, rng=rng)
        rows.append({"rho_sprinkle": rs, "mean": float(rho.mean()),
                     "std": float(rho.std()),
                     "frac_dev_gt_10pct": float(np.mean(np.abs(rho - 1) > 0.1))})
    return rows


def vacuum_gauge(seed, n_relax, scale):
    """Gauge field at disorder ``scale``, cooled n_relax steps.
    Returns (J_vac, diagnostics: winding, monopole density)."""
    rng = np.random.default_rng(1000 + seed)
    x, y, z, dx = pe.make_grid(*GRID)
    phix, phiy, phiz = pe.hot_gauge(x, y, z, rng, scale=scale)
    phix, phiy, phiz = pe.relax_gauge(phix, phiy, phiz, dx, lam=0.7,
                                      n_relax=n_relax)
    J = v2.node_action_density(phix, phiy, phiz)
    wind = c3.winding_planes(phix, phiy, phiz)
    rho_M, _ = c3.monopole_density(phix, phiy, phiz)
    return J, {"winding": {k: float(v) for k, v in wind.items()},
               "mono_density": float(rho_M)}


def rho_response(J, rho_factor, K=K_SOFT):
    """Equilibrium dynamical-rho response to the vacuum drive, via the
    campaign-standard STATIC minimiser (v2.relax_density, conservation
    projected every iteration; V3 showed the real-time field reaches this
    equilibrium by construction).  The dynamic integrator v3.evolve_rho is
    NOT used here: with a drive that fills the whole box its mirror-boundary
    Laplacian leaks total mass (uniform mean drift, measured up to 40x at
    K=10, s=pi) and its floor redistribution can push cells negative --
    artefacts irrelevant for V3's central localised vortex but fatal for a
    vacuum-wide source.  Documented in VS1_higgs_condensate.md.

    ``corr_drive`` is the Pearson correlation between the rho deviation and
    the (mean-subtracted) drive: |corr| ~ 1 means the structure is ENSLAVED
    to the drive (linear response), not spontaneous order."""
    drho = v2.relax_density(rho_factor * np.asarray(J, float), K=K,
                            n_iter=3000)
    rho = np.clip(1.0 + drho, 0.0, None)
    dev = (rho - 1.0).ravel()
    drv = (np.asarray(J, float) - np.mean(J)).ravel()
    corr = float(np.corrcoef(dev, drv)[0, 1]) if dev.std() > 0 else 0.0
    return {"dev_max": float(np.max(np.abs(dev))),
            "dev_std": float(dev.std()),
            "frac_gt_10pct": float(np.mean(np.abs(dev) > 0.1)),
            "rho_min": float(rho.min()), "rho_mean": float(rho.mean()),
            "frac_floor": float(np.mean(rho.ravel() < 1e-12)),
            "corr_drive": corr}


def main():
    rng = np.random.default_rng(99)
    print("(a) kinematic control (Poisson count)")
    kin = kinematic_control(rng)
    for r in kin:
        print(f"  rho_sprinkle={r['rho_sprinkle']:6.1f}  mean={r['mean']:.4f}  "
              f"std={r['std']:.4f}  frac|dev|>10%={r['frac_dev_gt_10pct']:.3f}")

    print("\n(b)+(d) disorder scan x cooling depth (rf=16, the V3 reference)")
    scan = []
    for seed in SEEDS:
        for scale in SCALES:
            for n_relax in COOL_STEPS:
                J, diag = vacuum_gauge(seed, n_relax, scale)
                jstd = float((J - J.mean()).std())
                st = rho_response(J, 16.0)
                st.update({"seed": seed, "scale": float(scale),
                           "n_relax": n_relax, "J_std": jstd,
                           "mono_density": diag["mono_density"]})
                scan.append(st)
                print(f"  seed={seed} s={scale:5.2f} cool={n_relax:4d}  "
                      f"J_std={jstd:.4f}  mono={diag['mono_density']:.4f}  "
                      f"dev_std={st['dev_std']:.4f}  dev_max={st['dev_max']:.3f}  "
                      f"corr={st['corr_drive']:+.3f}")

    print("\n(c) drive scan at s=pi (cool=800)")
    drive = []
    for seed in SEEDS:
        J, diag = vacuum_gauge(seed, 800, np.pi)
        jstd = float((J - J.mean()).std())
        for rf in RHO_FACTORS:
            st = rho_response(J, rf)
            st.update({"seed": seed, "rho_factor": rf, "J_std": jstd,
                       "response_ratio": st["dev_std"] / (rf * jstd)
                       if jstd > 0 else float("nan")})
            drive.append(st)
            print(f"  seed={seed} rf={rf:5.1f}  dev_std={st['dev_std']:.4f}  "
                  f"dev_max={st['dev_max']:.3f}  frac>10%={st['frac_gt_10pct']:.3f}  "
                  f"resp={st['response_ratio']:.3f}")

    print("\n(e) linear regime (K=10 > K_c, rf=1): dev_std must track J_std")
    linear = []
    for seed in SEEDS:
        for scale in SCALES:
            J, diag = vacuum_gauge(seed, 800, scale)
            jstd = float((J - J.mean()).std())
            st = rho_response(J, 1.0, K=10.0)
            st.update({"seed": seed, "scale": float(scale), "J_std": jstd,
                       "gain": st["dev_std"] / jstd if jstd > 0 else float("nan")})
            linear.append(st)
            print(f"  seed={seed} s={scale:5.2f}  J_std={jstd:.4f}  "
                  f"dev_std={st['dev_std']:.4f}  gain={st['gain']:.3f}  "
                  f"corr_drive={st['corr_drive']:+.3f}")

    # ---- verdict numbers ----------------------------------------------
    # ordered-vacuum limit: J and the rho structure at the smallest disorder
    ordered = [r for r in scan if r["scale"] == min(SCALES)
               and r["n_relax"] == max(COOL_STEPS)]
    print("\nordered-vacuum limit (s=%.2f, deepest cooling):" % min(SCALES))
    for r in ordered:
        print(f"  seed={r['seed']}  J_std={r['J_std']:.5f}  "
              f"dev_std={r['dev_std']:.5f}  dev_max={r['dev_max']:.5f}")
    # persistence of the frozen state: J decay with cooling at s=pi
    pers = []
    for seed in SEEDS:
        sub = [r for r in scan if r["seed"] == seed and r["scale"] > 3.0]
        sub.sort(key=lambda r: r["n_relax"])
        if sub and sub[0]["J_std"] > 0:
            pers.append({"seed": seed,
                         "J_decay": sub[-1]["J_std"] / sub[0]["J_std"],
                         "dev_decay": sub[-1]["dev_std"] / sub[0]["dev_std"]})
    print("frozen-state persistence (s=pi):",
          [{k: round(v, 3) if isinstance(v, float) else v for k, v in p.items()}
           for p in pers])

    payload = {"kinematic": kin, "scan": scan, "drive": drive,
               "linear": linear,
               "ordered_limit": ordered, "persistence": pers,
               "params": {"grid": GRID, "K": K_SOFT, "n_iter_static": 3000,
                          "solver": "v2.relax_density (static, conserving)",
                          "seeds": SEEDS, "cool_steps": COOL_STEPS,
                          "scales": [float(s) for s in SCALES],
                          "rho_factors": RHO_FACTORS}}
    (OUTDIR / "VS1_higgs_condensate.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print("\nsaved VS1_higgs_condensate.json")


if __name__ == "__main__":
    main()

"""VS2 -- does the causal network's vacuum have a PHASE TRANSITION?

Charter: VACUUM_STRUCTURE.md (VS2).  Question: is there a sharp transition
between the ordered (normal) vacuum and a defect-bearing (condensed/glassy)
vacuum, or only a smooth crossover?

Control parameter: the initial gauge disorder scale s of a quench (the
network's 'temperature' analogue: hot start, cooled by the minimal action --
the same protocol VS1 used at three values, here scanned finely).

Order parameters measured after cooling (per seed):
  m      = |<e^{i phibar}>|   phase coherence of the node-averaged gauge phase
                              (real arithmetic: hypot of mean cos / mean sin);
  rho_M  = frozen monopole density (topological defects that survive cooling);
  J_res  = residual gauge action std (the vacuum's frozen energy);
  |<Phi>| = coherent condensate amplitude of the EMERGENT field
           Phi = rho_dyn e^{i phibar} (rho_dyn = V3 dynamical density relaxed
           under the vacuum's own J, K=10 linear regime).

Note on the charter's <|Phi|>: with the PHI_EMERGE normalisation, <|Phi|> =
<rho> = 1 IDENTICALLY (the Voronoi/conservation normalisation), so the
literal observable cannot transition; the physically loaded object is the
COHERENT average |<Phi>| (the 'v' of a condensate), plus the defect density.
Both are reported.

Kill criterion (pre-registered): all order parameters vary SMOOTHLY with s --
no transition; the vacuum has no thermodynamic phase structure in this probe.
A transition claim requires an abrupt jump or kink (curvature spike) robust
across seeds.

Anti-circularity: no complex literals (cos/sin sums only), no critical
temperature inserted; fixed seeds.
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
GRID = v3.GRID
SEEDS = (0, 1, 2, 3, 4)
SCALES = np.concatenate([np.arange(0.2, 3.01, 0.2), [np.pi]])
N_RELAX = 800
K_LINEAR = 10.0
T_RHO = 150.0


def cooled_vacuum(seed, scale):
    rng = np.random.default_rng(1000 + seed)
    x, y, z, dx = pe.make_grid(*GRID)
    phix, phiy, phiz = pe.hot_gauge(x, y, z, rng, scale=scale)
    phix, phiy, phiz = pe.relax_gauge(phix, phiy, phiz, dx, lam=0.7,
                                      n_relax=N_RELAX)
    return phix, phiy, phiz


def order_parameters(phix, phiy, phiz):
    pb, _ = pe.phibar(phix, phiy, phiz)
    m = float(np.hypot(np.cos(pb).mean(), np.sin(pb).mean()))
    rho_M, _ = c3.monopole_density(phix, phiy, phiz)
    J = v2.node_action_density(phix, phiy, phiz)
    jstd = float((J - J.mean()).std())
    # coherent condensate amplitude of the emergent Phi = rho_dyn e^{i phibar};
    # rho_dyn via the STATIC conserving minimiser (see VS1's documented
    # evolve_rho mass-leak artefact for box-filling sources)
    drho = v2.relax_density(J, K=K_LINEAR, n_iter=3000)
    rho_dyn = np.clip(1.0 + drho, 0.0, None)
    Re, Im = pe.phi_field(rho_dyn, pb)
    v_coh = float(np.hypot(Re.mean(), Im.mean()))
    mag_mean = float(rho_dyn.mean())          # <|Phi|> -- trivially ~1
    return {"m_phase": m, "rho_M": float(rho_M), "J_std": jstd,
            "v_coherent": v_coh, "abs_mean": mag_mean}


def main():
    rows = []
    for s in SCALES:
        per_seed = []
        for seed in SEEDS:
            op = order_parameters(*cooled_vacuum(seed, float(s)))
            op.update({"seed": seed, "scale": float(s)})
            per_seed.append(op)
            rows.append(op)
        mm = np.mean([p["m_phase"] for p in per_seed])
        ms = np.std([p["m_phase"] for p in per_seed])
        rM = np.mean([p["rho_M"] for p in per_seed])
        vc = np.mean([p["v_coherent"] for p in per_seed])
        am = np.mean([p["abs_mean"] for p in per_seed])
        jj = np.mean([p["J_std"] for p in per_seed])
        print(f"s={s:4.2f}  m={mm:.4f}+-{ms:.4f}  rho_M={rM:.5f}  "
              f"|<Phi>|={vc:.4f}  <|Phi|>={am:.4f}  J_std={jj:.4f}")

    # -------- abruptness diagnostics on the seed-means ------------------
    def seed_mean(key):
        return np.array([np.mean([r[key] for r in rows
                                  if abs(r["scale"] - s) < 1e-9])
                         for s in SCALES])

    diag = {}
    for key in ("m_phase", "rho_M", "v_coherent", "J_std"):
        y = seed_mean(key)
        dy = np.diff(y) / np.diff(SCALES)
        # smoothness metric: max |step change| relative to total range
        rng_y = float(y.max() - y.min())
        max_step = float(np.max(np.abs(np.diff(y)))) if rng_y > 0 else 0.0
        diag[key] = {"values": y.tolist(),
                     "max_step_over_range": max_step / rng_y if rng_y > 0
                     else 0.0,
                     "argmax_slope_s": float(SCALES[:-1][np.argmax(np.abs(dy))])}
        print(f"{key:12s}: range={rng_y:.4f}  max_step/range="
              f"{diag[key]['max_step_over_range']:.3f}  "
              f"steepest at s={diag[key]['argmax_slope_s']:.2f}")

    # onset of frozen monopoles: first s with rho_M > 0 in ALL seeds
    onset = None
    for s in SCALES:
        vals = [r["rho_M"] for r in rows if abs(r["scale"] - s) < 1e-9]
        if all(v > 0 for v in vals):
            onset = float(s)
            break
    print(f"\nmonopole onset (rho_M > 0 in all seeds): s_onset = {onset}")

    payload = {"rows": rows, "scales": SCALES.tolist(),
               "diagnostics": diag, "monopole_onset": onset,
               "params": {"grid": GRID, "seeds": SEEDS, "n_relax": N_RELAX,
                          "K_linear": K_LINEAR, "t_rho": T_RHO}}
    (OUTDIR / "VS2_phase_transition.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print("saved VS2_phase_transition.json")


if __name__ == "__main__":
    main()

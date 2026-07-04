"""run_campaign.py -- Campaign XI driver: baseline + levers A/B/C.

For each lever and each size L it (1) builds the substrate graphs once, (2) sweeps J
to locate J_c by the chi peak, (3) reports the FSS suite (m, U4, chi, xi_2nd/L) over
the grid.  The verdict logic (xi/L trend, U4 crossing, chi_max scaling) is computed in
analyse.py from the JSON this writes.  Pre-registered in PRE_REGISTRO.md.

Usage:  python run_campaign.py [smoke|full]
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xi_suite import (  # noqa: E402
    build_bare, build_knn_cap, build_window, measure_point, locate_Jc,
)
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402


def sprinkle_clouds(L, rho, dim, n_seeds, seed0=0):
    """n_seeds point clouds in a cubic box of side L, (dim) total dims."""
    clouds = []
    for s in range(n_seeds):
        rng = np.random.default_rng(1000 + seed0 + s)
        clouds.append(sprinkle_box(rho, [(0.0, L)] * dim, rng))
    return clouds


def scan_size(graphs, Js, L_s, cfg):
    rows = [measure_point(graphs, J, L_s=L_s, **cfg) for J in Js]
    return rows


def run_lever(name, builder_of, Ls, rho, dim, Js, n_seeds, cfg, extern=None):
    """builder_of: callable(pts) -> (Graph, xs).  Returns the per-size scan + J_c."""
    t0 = time.time()
    sizes = []
    for L in Ls:
        clouds = sprinkle_clouds(L, rho, dim, n_seeds)
        graphs = [builder_of(pts) for pts in clouds]
        L_s = L  # spatial box side (cubic)
        rows = scan_size(graphs, Js, L_s, cfg)
        Jc = locate_Jc(rows)
        zc = rows[int(np.argmin([abs(r["J"] - Jc) for r in rows]))]
        sizes.append({
            "L": L, "L_s": L_s, "N_mean": rows[0]["N_mean"],
            "z_mean": zc["z_mean"], "conn_frac": zc["conn_frac"],
            "Jc": Jc, "rows": rows,
        })
        print(f"  [{name}] L={L:.2f} N~{rows[0]['N_mean']:.0f} "
              f"z={zc['z_mean']:.1f} conn={zc['conn_frac']:.2f} "
              f"Jc={Jc:.3f} xi/L@Jc={zc['xi_over_L']:.3f} U4@Jc={zc['U4']:.3f}",
              flush=True)
    return {
        "lever": name, "external_scale": extern, "dim": dim, "rho": rho,
        "Ls": list(Ls), "Js": list(Js), "n_seeds": n_seeds, "cfg": cfg,
        "sizes": sizes, "runtime_s": time.time() - t0,
    }


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    rho = 2.0
    if mode == "smoke":
        cfg = dict(n_burn=80, n_meas=30, meas_every=2)
        n_seeds = 3
        Js = [0.03, 0.06, 0.1, 0.2, 0.4]
        Ls_4d = [3.0, 3.6, 4.2]
        Ls_3d = [3.6, 4.6, 5.6]
        knn_ks = [4]
        win_ells = [1.0]
    else:
        cfg = dict(n_burn=250, n_meas=60, meas_every=2)
        n_seeds = 5
        # J grid must bracket J_c of EVERY lever AND its drift: bare Hasse (z grows
        # with N) has J_c drifting toward 0 (-> low-J points); sparse k-NN (z~5 fixed)
        # orders near J_c~0.4-0.5 -> span [0.02, 0.9].
        Js = [0.02, 0.03, 0.05, 0.07, 0.10, 0.14, 0.19, 0.26, 0.36, 0.50, 0.68, 0.90]
        Ls_4d = [4.0, 4.8, 5.6, 6.4]
        Ls_3d = [4.6, 5.8, 7.0, 8.2]
        knn_ks = [3, 6]
        win_ells = [0.8]

    out = {"mode": mode, "rho": rho, "results": {}}

    # ---- Phase 1 baseline + Lever C reference: bare Hasse (3+1)D ----
    print("== BASELINE / control: bare Hasse (3+1)D ==", flush=True)
    out["results"]["baseline_3p1"] = run_lever(
        "baseline_3p1", build_bare, Ls_4d, rho, 4, Js, n_seeds, cfg,
        extern=None)

    # ---- Lever C: bare Hasse (2+1)D -- NO inserted scale ----
    print("== Lever C: bare Hasse (2+1)D (no inserted scale) ==", flush=True)
    out["results"]["leverC_2p1"] = run_lever(
        "leverC_2p1", build_bare, Ls_3d, rho, 3, Js, n_seeds, cfg,
        extern=None)

    # ---- Lever A: k-NN cap (3+1)D -- cap k is [External] ----
    for k in knn_ks:
        key = f"leverA_knn_k{k}"
        print(f"== Lever A: k-NN cap k={k} (3+1)D  [External: k={k}] ==", flush=True)
        out["results"][key] = run_lever(
            key, (lambda kk: (lambda pts: build_knn_cap(pts, kk)))(k),
            Ls_4d, rho, 4, Js, n_seeds, cfg, extern={"type": "knn_cap_k", "value": k})

    # ---- Lever B: mesoscale window (3+1)D -- ell_k is [External] ----
    for ell in win_ells:
        key = f"leverB_win_{str(ell).replace('.', 'p')}"
        print(f"== Lever B: window ell_k={ell} (3+1)D  [External: ell_k={ell}] ==",
              flush=True)
        out["results"][key] = run_lever(
            key, (lambda e: (lambda pts: build_window(pts, e)))(ell),
            Ls_4d, rho, 4, Js, n_seeds, cfg, extern={"type": "window_ell_k", "value": ell})

    tag = "smoke" if mode == "smoke" else "full"
    (HERE / f"campaign_{tag}.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote campaign_{tag}.json")


if __name__ == "__main__":
    main()

"""MIN2 -- discrete subgroups cannot carry point matter: projection test.

A continuous map S^3 -> (discrete set) is constant, so a discrete gauge group
supports no pi_3 texture. Measured version: project the smooth B=1 hedgehog
onto the nearest element of a discrete subgroup of SU(2) -- Q8 (8 elements)
and the binary tetrahedral group 2T (24 elements) -- and measure:

  * B collapses (the volume index lives on smooth gradients; piecewise-constant
    fields have B from walls only -- non-integer, ~0);
  * the sigma energy E2 turns into DOMAIN WALLS and grows ~ 1/dx under grid
    refinement (41^3 -> 61^3: ratio ~ 61/41 = 1.49), while the smooth hedgehog's
    E2 converges (ratio ~ 1.0).

Pre-registered in MINIMALITY_SU2.md: |B_proj| < 0.2; wall-energy ratio
1.49 +- 0.15; smooth ratio 1.0 +- 0.1; B_smooth ~ 0.95 at 51^3-class grids.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s2  # noqa: E402

OUT = Path(__file__).resolve().parent
L_BOX = 16.0
GRIDS = [41, 61]


def group_Q8():
    g = []
    for k in range(4):
        for sgn in (+1.0, -1.0):
            q = np.zeros(4)
            q[k] = sgn
            g.append(q)
    return np.array(g)                                  # (8,4)


def group_2T():
    g = list(group_Q8())
    for s0 in (+0.5, -0.5):
        for s1 in (+0.5, -0.5):
            for s2 in (+0.5, -0.5):
                for s3 in (+0.5, -0.5):
                    g.append(np.array([s0, s1, s2, s3]))
    return np.array(g)                                  # (24,4)


def hedgehog(n):
    x = np.linspace(-L_BOX / 2, L_BOX / 2, n)
    dx = float(x[1] - x[0])
    U = s2.hedgehog_field(x, x, x, profile=lambda r: np.pi * np.exp(-r / 2.0))
    return U, dx


def project(U, table):
    """Nearest group element (max quaternion dot product = min geodesic angle)."""
    dots = np.tensordot(U, table, axes=([-1], [-1]))    # (...,n_g)
    idx = np.argmax(dots, axis=-1)
    return table[idx]


def e2_total(U, dx):
    e2, _ = s2.chiral_energy_density(U, dx, e_sk=0.0)
    return float(np.sum(e2)) * dx ** 3


def main():
    tables = {"Q8": group_Q8(), "2T": group_2T()}
    res = {name: {} for name in ["smooth", *tables]}
    for n in GRIDS:
        U, dx = hedgehog(n)
        res["smooth"][n] = {"B": s2.baryon_number(U, dx), "E2": e2_total(U, dx)}
        for name, tab in tables.items():
            Up = project(U, tab)
            res[name][n] = {"B": s2.baryon_number(Up, dx),
                            "E2": e2_total(Up, dx)}

    ratios = {name: res[name][GRIDS[1]]["E2"] / res[name][GRIDS[0]]["E2"]
              for name in res}
    payload = {
        "L_box": L_BOX, "grids": GRIDS,
        "results": {name: {str(n): res[name][n] for n in GRIDS}
                    for name in res},
        "E2_refinement_ratio_61_over_41": ratios,
        "pre_registered": {"wall_ratio": 61 / 41, "smooth_ratio": 1.0,
                           "B_proj_max": 0.2},
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__},
    }
    (OUT / "MIN2_discrete.json").write_text(json.dumps(payload, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
    names = list(res)
    Bs = [res[name][GRIDS[1]]["B"] for name in names]
    ax1.bar(names, Bs, color=["tab:blue", "tab:red", "tab:orange"])
    ax1.axhline(1.0, color="k", ls=":")
    ax1.set_ylabel("B (61^3)")
    ax1.set_title("topological charge: smooth vs projected")
    for name, c in zip(names, ["tab:blue", "tab:red", "tab:orange"]):
        ax2.plot(GRIDS, [res[name][n]["E2"] for n in GRIDS], "o-", color=c,
                 label=f"{name} (ratio {ratios[name]:.2f})")
    ax2.set_yscale("log")
    ax2.set_xlabel("grid n")
    ax2.set_ylabel("E2")
    ax2.set_title("refinement: walls grow ~1/dx, smooth converges")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "MIN2_discrete.png", dpi=150)

    print(json.dumps({"B_61": {name: res[name][61]["B"] for name in res},
                      "E2_ratios": ratios}, indent=2))


if __name__ == "__main__":
    main()

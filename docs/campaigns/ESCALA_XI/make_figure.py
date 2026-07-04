"""make_figure.py -- Campaign XI summary figure.

Panel A: z(N) per lever -- which substrates hold coordination fixed (k-NN) vs which
         diverge (bare/window/2+1D) -> existence of a fixed critical point.
Panel B: J_c(N) drift -- bare/window/2+1D run toward 0 (no fixed point); k-NN fixed.
Panel C: xi/L vs J for the size ladder of the positive control (criticality look).
Panel D: xi/L vs J for the size ladder of Lever A k-NN (the decisive fixed-z test).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def load():
    tag = sys.argv[1] if len(sys.argv) > 1 else "full"
    data = json.loads((HERE / f"campaign_{tag}.json").read_text())
    levers = dict(data["results"])
    pc = HERE / "validate_positive.json"
    if pc.exists():
        pcd = json.loads(pc.read_text())
        if "lever" in pcd:
            levers["POSITIVE_CONTROL_lattice3d"] = pcd
    return tag, levers


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tag, levers = load()
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))

    # Panel A: z(N)
    for key, lev in levers.items():
        Ns = [s["N_mean"] for s in lev["sizes"]]
        zs = [s["z_mean"] for s in lev["sizes"]]
        ax[0, 0].plot(Ns, zs, "o-", label=key, lw=1.5, ms=5)
    ax[0, 0].set_xscale("log"); ax[0, 0].set_yscale("log")
    ax[0, 0].set_xlabel("N (events)"); ax[0, 0].set_ylabel("coordination z")
    ax[0, 0].set_title("A. z(N): fixed (k-NN) vs diverging (Hasse/window/2+1D)")
    ax[0, 0].legend(fontsize=6, frameon=False)

    # Panel B: J_c(N)
    for key, lev in levers.items():
        Ns = [s["N_mean"] for s in lev["sizes"]]
        jc = [s["Jc"] for s in lev["sizes"]]
        ax[0, 1].plot(Ns, jc, "s-", label=key, lw=1.5, ms=5)
    ax[0, 1].set_xscale("log")
    ax[0, 1].set_xlabel("N (events)"); ax[0, 1].set_ylabel(r"$J_c$ (chi peak)")
    ax[0, 1].set_title("B. $J_c(N)$: drift to 0 = no fixed point = mean-field")
    ax[0, 1].legend(fontsize=6, frameon=False)

    # Panel C: xi/L vs J for positive control
    def xiL_panel(axp, key, title):
        if key not in levers:
            axp.set_title(title + " (absent)"); return
        lev = levers[key]
        Js = np.array(lev["Js"])
        for s in lev["sizes"]:
            L = s.get("L", s.get("m"))
            xol = [r["xi_over_L"] for r in s["rows"]]
            axp.plot(Js, xol, "o-", label=f"L={L}", lw=1.3, ms=4)
        axp.set_xscale("log")
        axp.set_xlabel("J"); axp.set_ylabel(r"$\xi_{2nd}/L$")
        axp.set_title(title); axp.legend(fontsize=7, frameon=False)

    xiL_panel(ax[1, 0], "POSITIVE_CONTROL_lattice3d",
              "C. positive control (3D lattice): genuine criticality")
    knn_key = next((k for k in levers if "knn" in k), None)
    xiL_panel(ax[1, 1], knn_key or "",
              f"D. Lever A {knn_key}: decisive fixed-z test")

    fig.tight_layout()
    fig.savefig(HERE / f"campaign_{tag}.png", dpi=130)
    print(f"wrote campaign_{tag}.png")


if __name__ == "__main__":
    main()

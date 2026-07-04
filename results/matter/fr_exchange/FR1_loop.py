"""FR1 -- the exchange loop exists on the network: closure, B(s), E(s).

Two B=1 hedgehogs at +-(d/2) on the x-axis (product ansatz); exchange path
s in [0,1]: centers rotate by pi about the midpoint (z-axis), orientations
fixed. Pre-registered (MATTER_FR_EXCHANGE.md):
  * B_total = 2 (+-0.15) and conserved along the path;
  * E(s) bounded (max/min < 1.5);
  * closure error ||U(1)-U(0)|| ~ factor-of-the-commutator ~ e^{-d/2}:
    decreases by a factor >= 2 per Delta d = +2, for d = 6, 8, 10.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fr_core as fc
from fr_core import s2

SEPARATIONS = [6.0, 8.0, 10.0]
N_STEPS = 21
E_SK = 1.0


def main():
    X, Y, Z, dx = fc.grid()
    out = {}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for d in SEPARATIONS:
        Bs, Es = [], []
        U0 = None
        for k, s in enumerate(np.linspace(0.0, 1.0, N_STEPS)):
            ang = np.pi * s
            c1 = (0.5 * d * np.cos(ang), 0.5 * d * np.sin(ang), 0.0)
            c2 = (-c1[0], -c1[1], 0.0)
            U = fc.pair(X, Y, Z, c1, c2)
            if k == 0:
                U0 = U
            Bs.append(s2.baryon_number(U, dx))
            E2, E4, Et = s2.chiral_energy(U, dx, E_SK)
            Es.append(Et)
        Uend = U
        cmax, cmean = fc.qdist(Uend, U0)
        out[d] = {"B_path": Bs, "E_path": Es,
                  "B_start": Bs[0], "B_drift_max": float(np.max(np.abs(
                      np.array(Bs) - Bs[0]))),
                  "E_max_over_min": float(np.max(Es) / np.min(Es)),
                  "closure_max": cmax, "closure_mean": cmean}
        ax1.plot(np.linspace(0, 1, N_STEPS), np.array(Es) / Es[0], "o-", ms=3,
                 label=f"d={d:.0f} (B drift {out[d]['B_drift_max']:.3f})")
    ratios = [out[SEPARATIONS[i]]["closure_max"] /
              out[SEPARATIONS[i + 1]]["closure_max"]
              for i in range(len(SEPARATIONS) - 1)]
    payload = {"separations": {str(d): out[d] for d in SEPARATIONS},
               "closure_decay_ratios_per_plus2": ratios,
               "pre_registered": {"ratio_min": 2.0, "B_total": 2.0,
                                  "E_ratio_max": 1.5}}
    fc.save_json("FR1_loop.json", payload)

    ax1.set_xlabel("s (exchange parameter)")
    ax1.set_ylabel("E(s)/E(0)")
    ax1.set_title("energy along the exchange loop (bounded)")
    ax1.legend(fontsize=8)
    cl = [out[d]["closure_max"] for d in SEPARATIONS]
    ax2.semilogy(SEPARATIONS, cl, "o-", color="tab:blue", label="closure error")
    dd = np.array(SEPARATIONS)
    ax2.semilogy(dd, cl[0] * np.exp(-(dd - dd[0]) / 2.0), "k:",
                 label=r"$\propto e^{-d/2}$")
    ax2.set_xlabel("separation d")
    ax2.set_ylabel("max |U(1)-U(0)|")
    ax2.set_title(f"loop closes asymptotically (ratios {ratios[0]:.2f}, "
                  f"{ratios[1]:.2f} per +2)")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fc.OUT / "FR1_loop.png", dpi=150)

    print(json.dumps({str(d): {"B": out[d]["B_start"],
                               "B_drift": out[d]["B_drift_max"],
                               "E_ratio": out[d]["E_max_over_min"],
                               "closure": out[d]["closure_max"]}
                      for d in SEPARATIONS} | {"decay_ratios": ratios},
                     indent=2))


if __name__ == "__main__":
    main()

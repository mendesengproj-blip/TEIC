"""HQ2_2_geff.py -- G_eff/G_N as a function of J/J_c.

Charter: HQ2_CRITICAL_FERROMAGNET.md (HQ2-2).  Reuses the c_eff(J) measured in
HQ2-1 (no new Monte-Carlo).  DEV bridge (adopted from the prompt):

    G_eff(J)/G_N = J_eff(J)/J = Z(J/J_c) = (c_eff(J)/c0)^2 .

Central question: is G_eff/G_N < 1 for some J > J_c?
  Route A (BD, J-blind): Z_A = (c_BD/c0)^2 = const ~ 1   -> no suppression.
  Route B (stiffness):   Z_B = (m(J)/m_sat)^2 < 1, smallest near J_c -> suppression.

Death criterion (pre-registered): G_eff/G_N >= 1 for all J > J_c -> Verdict C.
If Route B gives Z<1, HQ2-2 is "positive" and HQ2-3/HQ2-4 may run (protocol).
Anti-circularity: G_N never enters as a constant; Z is the measured (c_eff/c0)^2.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent


def main():
    src = OUT / "HQ2_1_jeff.json"
    if not src.exists():
        print("HQ2_1_jeff.json missing -- run HQ2-1 first.  Aborting.")
        return 1
    d = json.loads(src.read_text())
    c0 = d["c0"]
    cA = d["route_A"]["c_BD"]
    rows = d["rows"]

    print("=" * 72)
    print("HQ2-2 -- G_eff/G_N vs J/J_c   [Z = (c_eff/c0)^2]")
    print("=" * 72)
    out_rows = []
    for r in rows:
        Z_B = (r["c_eff_B"] / c0) ** 2
        Z_B_err = 2.0 * (r["c_eff_B"] / c0) * (r["c_eff_B_err"] / c0)
        Z_A = (cA / c0) ** 2
        out_rows.append({"J_over_Jc": r["J_over_Jc"], "J": r["J"], "m": r["m"],
                         "Z_B": Z_B, "Z_B_err": Z_B_err, "Z_A": Z_A})
        print(f"  J/Jc={r['J_over_Jc']:4.2f}  m={r['m']:.4f}  "
              f"G_eff/G_N(B)={Z_B:.4f}+-{Z_B_err:.4f}   (A)={Z_A:.4f}")

    Z_B_vals = [r["Z_B"] for r in out_rows]
    Z_B_min = min(Z_B_vals)
    Z_A = (cA / c0) ** 2
    routeB_suppresses = Z_B_min < 1.0
    routeA_suppresses = Z_A < 1.0 - 1e-6

    # pre-registered death vs positive
    positive = routeB_suppresses          # Route B gives the hypothesis its chance
    verdict_local = ("POSITIVE (Route B: G_eff<G_N near J_c) -> HQ2-3/4 may run"
                     if positive else
                     "DEATH (G_eff>=G_N for all J>J_c) -> Verdict C")
    print("-" * 72)
    print(f"  Route A (BD, J-blind): G_eff/G_N = {Z_A:.4f} (constant) "
          f"-> suppression: {routeA_suppresses}")
    print(f"  Route B (stiffness):   min G_eff/G_N = {Z_B_min:.4f} at "
          f"J/Jc={out_rows[int(np.argmin(Z_B_vals))]['J_over_Jc']} "
          f"-> suppression: {routeB_suppresses}")
    print(f"\n  HQ2-2: {verdict_local}")
    print("=" * 72)

    # figure
    fig, ax = plt.subplots(figsize=(8, 5.5))
    rj = np.array([r["J_over_Jc"] for r in out_rows])
    ZB = np.array([r["Z_B"] for r in out_rows])
    ZBe = np.array([r["Z_B_err"] for r in out_rows])
    o = np.argsort(rj)
    ax.errorbar(rj[o], ZB[o], yerr=ZBe[o], fmt="o-", color="tab:red", capsize=3,
                label="Route B: $(m(J)/m_{sat})^2$ (stiffness)")
    ax.axhline(Z_A, color="tab:blue", lw=1.5,
               label=f"Route A: $(c_{{BD}}/c_0)^2$={Z_A:.3f} (J-blind)")
    ax.axhline(1.0, color="k", ls="--", lw=1.2, label="$G_{eff}=G_N$")
    ax.axvline(1.0, color="0.5", ls=":", lw=1, label="$J_c$")
    ax.set_xlabel("J / J_c"); ax.set_ylabel("$G_{eff}/G_N$")
    ax.set_title("HQ2-2: critical softening suppresses G_eff (Route B) below $G_N$")
    ax.legend(fontsize=9); ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "HQ2_2_geff.png", dpi=130)
    print(f"saved {OUT/'HQ2_2_geff.png'}")

    payload = {"task": "HQ2-2", "c0": c0, "c_BD": cA, "Z_A": Z_A,
               "rows": out_rows, "Z_B_min": Z_B_min,
               "routeA_suppresses": bool(routeA_suppresses),
               "routeB_suppresses": bool(routeB_suppresses),
               "positive": bool(positive), "verdict_local": verdict_local}
    (OUT / "HQ2_2_geff.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'HQ2_2_geff.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

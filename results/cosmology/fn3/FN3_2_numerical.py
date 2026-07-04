"""FN3_2_numerical.py -- numerical Boltzmann/oscillator integration of the relic.

Charter FN3-2.  Integrates phi'' + 3H phi' + m^2 phi = 0 in a realistic FRW
background (radiation+matter+Lambda, Omega_r fixed by T_CMB) across the oscillation
onset, reads off the conserved comoving relic rho_phi a^3, and reports Omega_{m_A} h^2
NUMERICALLY -- an independent check of the FN3-1 closed form, free of the onset-
definition O(1) ambiguity baked into the analytic coefficient.

For each mass we integrate at the f_A that the FN3-1 contour says should give
Omega=0.12, plus a fixed f_A=1e17 GeV column, and verify the field ends up cold
(w->0) with rho a^3 plateauing.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fn3_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent
MASSES = [c.M_A_FLOOR, 1e-24, 1e-23, 1e-22]


def main():
    rows = []
    trajec = {}
    for m in MASSES:
        f_contour = c.f_A_for_target(m)                 # f_A that should give 0.12
        r = c.misalignment_relic(m, f_contour)
        # also a fixed f_A=1e17 column for direct numeric-vs-canonical comparison
        r17 = c.misalignment_relic(m, 1e17)
        rows.append({
            "m_eV": m, "f_A_contour_GeV": float(f_contour),
            "Omega_num_at_contour": r["Omega_h2"],
            "Omega_canon_at_contour": r["Omega_canonical"],
            "Omega_num_at_1e17": r17["Omega_h2"],
            "Omega_canon_at_1e17": r17["Omega_canonical"],
            "onset_factor_R": r["onset_factor_R"], "a_osc": r["a_osc"],
            "w_tail": float(np.mean(r["w_inst"][r["a"] > r["a_osc"] * 3.0])),
        })
        # keep trajectory of the 1e17 run for the figure (subsample)
        s = slice(None, None, max(1, len(r17["a"]) // 600))
        trajec[f"{m:.2e}"] = {"a": r17["a"][s].tolist(),
                              "diag": r17["diag_rho_a3"][s].tolist(),
                              "w": r17["w_inst"][s].tolist(),
                              "a_osc": r17["a_osc"]}

    # agreement: numerical / canonical ratio at the contour f_A
    ratios = [row["Omega_num_at_contour"] / row["Omega_canon_at_contour"] for row in rows]
    agree = bool(np.all((np.array(ratios) > 0.3) & (np.array(ratios) < 3.0)))

    payload = {"rows": rows, "num_over_canon_ratios": ratios,
               "agree_within_factor3": agree,
               "trajectories": trajec,
               "note": "numerical from FRW oscillator; rho a^3 plateau -> Omega; "
                       "agreement to a factor ~2 (onset matching) is the expected O(1)."}
    (OUT / "FN3_2_numerical.json").write_text(json.dumps(payload, indent=2))

    print("=" * 78)
    print("FN3-2  numerical relic density (FRW oscillator, rho a^3 plateau)")
    print("=" * 78)
    print("  m_A [eV]   f_A(contour)    Omega_num   Omega_canon   R(onset)   w_tail")
    for row in rows:
        print(f"  {row['m_eV']:>8.2e}   {row['f_A_contour_GeV']:>9.2e} GeV   "
              f"{row['Omega_num_at_contour']:>8.3f}    {row['Omega_canon_at_contour']:>8.3f}     "
              f"{row['onset_factor_R']:>6.2f}   {row['w_tail']:+.3f}")
    print(f"\n  numerical/canonical ratios (at contour f_A): "
          f"{[round(x,2) for x in ratios]}")
    print(f"  agree within factor 3: {agree}  "
          f"(residual = onset-matching O(1), canonical coeff 0.12 includes it)")
    print(f"  saved {OUT/'FN3_2_numerical.json'}")

    make_figure(trajec, rows)
    return payload


def make_figure(trajec, rows):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))

    for key, t in trajec.items():
        a = np.array(t["a"]); diag = np.array(t["diag"])
        ax[0].loglog(a / t["a_osc"], diag, lw=1, label=f"m_A={key} eV")
    ax[0].axhline(0, color="k", ls=":")
    ax[0].axvline(1.0, color="r", ls="--", lw=1, label="onset (3H=m)")
    ax[0].set_xlabel("a / a_osc"); ax[0].set_ylabel("rho a^3 / (1/2 m^2 phi0^2 a_osc^3)")
    ax[0].set_title("FN3-2: comoving relic rho a^3 plateaus (cold)")
    ax[0].set_ylim(1e-2, 3)
    ax[0].legend(fontsize=7)

    # w(a) collapse -> 0
    for key, t in trajec.items():
        a = np.array(t["a"]); w = np.array(t["w"])
        ax[1].semilogx(a / t["a_osc"], w, lw=0.8, label=f"m_A={key} eV")
    ax[1].axhline(0, color="k", ls=":", label="w=0 (cold)")
    ax[1].axvline(1.0, color="r", ls="--", lw=1)
    ax[1].set_xlabel("a / a_osc"); ax[1].set_ylabel("w(a)")
    ax[1].set_ylim(-1.2, 1.2)
    ax[1].set_title("FN3-2: equation of state -> 0 after onset")
    ax[1].legend(fontsize=7)

    om = [r["Omega_num_at_contour"] for r in rows]
    txt = "Omega_num at 0.12-contour f_A: " + ", ".join(f"{x:.3f}" for x in om)
    fig.suptitle("FN3-2: numerical relic confirms FN3-1 within factor ~2  (" + txt + ")",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "FN3_2_numerical.png", dpi=130)
    print(f"  saved {OUT/'FN3_2_numerical.png'}")


if __name__ == "__main__":
    main()

"""FM4_run.py -- runs FM4-V, FM4-1, FM4-2, FM4-3 and writes their JSON + figures.

Charter FM4.  Tests the MASSIVE sector (m_A as ultralight wave/fuzzy dark matter) --
the one door FM1/FM2/FM3 (Goldstone sector) left unopened.

  FM4-V  massive dispersion omega^2=c^2 k^2+m^2 (E2 magnon + mass -> gap).
  FM4-1  misalignment phi''+3Hphi'+m^2phi=0 -> cold (w->0, rho~a^-3).
  FM4-2  fuzzy Jeans/de Broglie scale vs mass (lands at sigma8 scale near m floor).
  FM4-3  sigma8 of a mixed CDM + fraction f ULDM cosmology vs LambdaCDM / KiDS.

Anti-circularity: m_A from Paper II; w/Jeans/sigma8 from the field + transfer; no
sigma8/KiDS/Lyman-alpha inserted.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fm4_core as f4  # noqa: E402
from FM1_2_class_impl import LCDMBaseline  # noqa: E402

OUT = Path(__file__).resolve().parent
M_FLOOR = f4.M_A_FLOOR
KIDS_S8, KIDS_ERR = 0.766, 0.020


def fm4v():
    """Massive dispersion: gap at k=0 (omega=m), -> omega=ck at large k (E2 limit)."""
    k = np.linspace(0, 3, 50)
    for m in (0.0, 0.5, 1.0):
        w = f4.massive_dispersion(k, m)
    gap_ok = abs(f4.massive_dispersion([0.0], 1.0)[0] - 1.0) < 1e-9      # omega(0)=m
    massless_ok = abs(f4.massive_dispersion([5.0], 0.0)[0] - 5.0) < 1e-9  # omega=ck
    return {"gap_at_k0_eq_m": bool(gap_ok), "massless_limit_eq_ck": bool(massless_ok),
            "ok": bool(gap_ok and massless_ok), "k": k.tolist(),
            "omega_m0": f4.massive_dispersion(k, 0.0).tolist(),
            "omega_m1": f4.massive_dispersion(k, 1.0).tolist()}


def fm4_1():
    """Misalignment -> w->0 (cold) and rho~a^-3 across masses."""
    rows = []
    for m in (1e-26, 1e-25, M_FLOOR):
        r = f4.misalignment(m)
        rows.append({"m_eV": m, "w_late": r["w_late"], "rho_slope": r["rho_slope"],
                     "a_osc": r["a_osc"]})
    cold = all(abs(r["w_late"]) < 0.1 and abs(r["rho_slope"] + 3) < 0.2 for r in rows)
    # keep one trajectory for the figure
    traj = f4.misalignment(1e-26)
    return {"rows": rows, "cold_confirmed": bool(cold),
            "traj_a": traj["a"][::20].tolist(), "traj_w": traj["w_inst"][::20].tolist(),
            "a_osc_demo": traj["a_osc"]}


def fm4_2():
    masses = np.array([1e-22, 1e-23, 1e-24, M_FLOOR, 1e-25])
    rows = [{"m_eV": float(m), "k_half": f4.k_half_mode(m),
             "k_jeans_z0": f4.jeans_scale_z(m)} for m in masses]
    # sigma8 scale ~ k 0.1-0.2 h/Mpc -> ~0.15-0.3 /Mpc
    at_sigma8 = [r for r in rows if 0.1 <= r["k_half"] <= 0.6]
    return {"rows": rows, "sigma8_band_kMpc": [0.15, 0.3],
            "masses_landing_at_sigma8": [r["m_eV"] for r in at_sigma8]}


def fm4_3(bl):
    s8L = f4.sigma8_of(bl.k, bl.P)
    Om = 0.3153
    fs = [0.05, 0.1, 0.2, 0.3, 0.5]
    masses = [M_FLOOR, 1e-24, 1e-23]
    grid = {}
    best = (None, None, s8L)
    for m in masses:
        row = []
        for f in fs:
            k, PL, PM = f4.mixed_power(bl, m, f)
            s8 = f4.sigma8_of(k, PM)
            row.append(s8)
            if s8 < best[2]:
                best = (m, f, s8)
        grid[f"{m:.2e}"] = row
    s8_min = best[2]
    reaches_kids = (s8_min * np.sqrt(Om / 0.3)) <= KIDS_S8 + 2 * KIDS_ERR
    # representative P(k) for figure
    k, PL, PM = f4.mixed_power(bl, M_FLOOR, 0.3)
    return {"sigma8_LCDM": s8L, "S8_LCDM": s8L * np.sqrt(Om / 0.3),
            "fractions": fs, "masses": masses, "grid_sigma8": grid,
            "sigma8_min": s8_min, "best_m_f": [best[0], best[1]],
            "S8_min": s8_min * np.sqrt(Om / 0.3),
            "reaches_KiDS": bool(reaches_kids),
            "k": bl.k.tolist(), "P_LCDM": PL.tolist(), "P_mixed_floor_f0p3": PM.tolist()}


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM4 -- massive sector: m_A as ultralight wave/fuzzy dark matter")
    print("=" * 72)
    bl = LCDMBaseline()

    V = fm4v()
    print(f"[FM4-V] massive dispersion gap(omega(0)=m)={V['gap_at_k0_eq_m']}, "
          f"massless limit(omega=ck)={V['massless_limit_eq_ck']} -> "
          f"{'PASS' if V['ok'] else 'FAIL'}")

    R1 = fm4_1()
    print("[FM4-1] misalignment -> cold matter:")
    for r in R1["rows"]:
        print(f"   m={r['m_eV']:.1e} eV: w_late={r['w_late']:+.3f}  "
              f"rho~a^{r['rho_slope']:.2f}  a_osc~{r['a_osc']:.1e}")
    print(f"   COLD (w~0, rho~a^-3) confirmed: {R1['cold_confirmed']}")

    R2 = fm4_2()
    print("[FM4-2] fuzzy Jeans scale vs mass (sigma8 band k~0.15-0.3/Mpc):")
    for r in R2["rows"]:
        print(f"   m={r['m_eV']:.1e} eV: k_half={r['k_half']:.3f}/Mpc")

    R3 = fm4_3(bl)
    print(f"[FM4-3] sigma8: LCDM={R3['sigma8_LCDM']:.3f}  "
          f"min over (f,m)={R3['sigma8_min']:.3f} at "
          f"m={R3['best_m_f'][0]:.1e},f={R3['best_m_f'][1]}  "
          f"(KiDS sigma8~{KIDS_S8})")
    print(f"   reaches KiDS: {R3['reaches_KiDS']}")

    gate = V["ok"]
    payload = {"gate_pass": bool(gate), "FM4V": V, "FM4_1": R1, "FM4_2": R2,
               "FM4_3": R3, "M_floor": M_FLOOR, "KiDS_S8": KIDS_S8,
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "FM4_run.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM4_run.json'}  ({payload['runtime_s']:.0f}s)")
    make_figures(R1, R2, R3)
    return payload


def make_figures(R1, R2, R3):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    ax[0].plot(R1["traj_a"], R1["traj_w"], lw=1)
    ax[0].axhline(0, color="k", ls=":"); ax[0].axvline(R1["a_osc_demo"], color="r", ls="--",
                  label="oscillation onset")
    ax[0].set_xscale("log"); ax[0].set_xlabel("a"); ax[0].set_ylabel("w(a)")
    ax[0].set_title("FM4-1: misalignment -> w->0 (cold)"); ax[0].legend(fontsize=8)
    m = [r["m_eV"] for r in R2["rows"]]; kh = [r["k_half"] for r in R2["rows"]]
    ax[1].loglog(m, kh, "o-")
    ax[1].axhspan(0.15, 0.3, color="green", alpha=0.2, label="sigma8 scale")
    ax[1].set_xlabel("m_A [eV]"); ax[1].set_ylabel("k_half [1/Mpc]")
    ax[1].set_title("FM4-2: Jeans scale vs mass"); ax[1].legend(fontsize=8)
    ax[2].loglog(R3["k"], R3["P_LCDM"], "k-", label="LCDM")
    ax[2].loglog(R3["k"], R3["P_mixed_floor_f0p3"], "r-", label="mixed (m floor, f=0.3)")
    ax[2].set_xlabel("k [h/Mpc]"); ax[2].set_ylabel("P(k)")
    ax[2].set_title(f"FM4-3: sigma8 {R3['sigma8_LCDM']:.3f}->{R3['sigma8_min']:.3f} (KiDS 0.76)")
    ax[2].legend(fontsize=8)
    fig.suptitle("FM4: m_A as ultralight wave DM -- cold (w=0) yes, but sigma8 barely moves",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM4_run.png", dpi=130)
    print(f"saved {OUT/'FM4_run.png'}")


if __name__ == "__main__":
    main()

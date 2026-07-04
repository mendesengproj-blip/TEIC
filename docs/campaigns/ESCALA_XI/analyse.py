"""analyse.py -- Campaign XI verdict logic (pre-registered, written before full run).

Reads campaign_{tag}.json and, per lever, computes the three pre-registered FSS
diagnostics and a verdict:

  (1) xi/L crossing : at each J, the slope d(xi/L)/d(log N) across sizes.
      mean-field/null -> slope < 0 at all J (larger system has SMALLER xi/L: xi
      tracks the cut-off/microscale, not L).  criticality -> a J where the slope is
      >= 0 (curves cross / fan out: xi tracks L).
  (2) U4 crossing   : at each J, slope d(U4)/d(log N).  A genuine 2nd-order point has
      a single J where curves cross (slope changes sign); mean-field has U4 flat
      (no scale-invariant crossing) or pinned.
  (3) chi_max scaling: x_N = d log(chi_max) / d log(N).  volume/mean-field -> x_N ~ 1
      (chi_max ∝ N); sub-volume 2nd order -> x_N < ~0.9.

Decision is on DIMENSIONLESS quantities only (xi/L, slopes, exponents).  Inserted
cut-offs (k, ell_k) are reported as [External] and never enter the divergence test.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _matrix(sizes, key):
    return np.array([[r[key] for r in s["rows"]] for s in sizes])  # (nsize, nJ)


def analyse_lever(lev):
    sizes = lev["sizes"]
    Js = np.array(lev["Js"])
    Ns = np.array([s["N_mean"] for s in sizes])
    logN = np.log(Ns)
    xiL = _matrix(sizes, "xi_over_L")
    U4 = _matrix(sizes, "U4")
    chi = _matrix(sizes, "chi")
    zc = np.array([s["z_mean"] for s in sizes])

    # pooled critical coupling = median of per-size chi-peak J_c
    Jc_sizes = np.array([s["Jc"] for s in sizes])
    Jc_pool = float(np.median(Jc_sizes))
    # band of the 3 grid J nearest J_c (the critical region; xi reliable on its
    # disordered approach), used to avoid the upward bias of max-over-all-J.
    band = np.argsort(np.abs(Js - Jc_pool))[:3]

    # (1) xi/L slope vs logN at each J
    xiL_slope = np.array([np.polyfit(logN, xiL[:, j], 1)[0] for j in range(len(Js))])
    xiL_slope_band = float(np.median(xiL_slope[band]))     # robust critical-band slope
    max_xiL_slope = float(np.max(xiL_slope))               # reported but NOT decisive
    j_best = int(np.argmax(xiL_slope))

    # (2) U4 slope vs logN; a crossing is where slope passes through 0 with U4 rising
    U4_slope = np.array([np.polyfit(logN, U4[:, j], 1)[0] for j in range(len(Js))])
    sign = np.sign(U4_slope)
    cross_js = [float(0.5 * (Js[j] + Js[j + 1]))
                for j in range(len(Js) - 1)
                if sign[j] < 0 and sign[j + 1] > 0]
    u4_crosses = bool(len(cross_js) > 0)

    # (3) chi_max scaling exponent in N
    chi_max = chi.max(axis=1)
    x_N = float(np.polyfit(logN, np.log(np.maximum(chi_max, 1e-12)), 1)[0])

    # z growth with N (mean-field substrate signature): does coordination stay
    # FIXED (a genuine fixed critical point exists) or diverge (J_c -> 0, no fixed
    # critical point => mean-field/non-geometric by construction)?
    z_slope = float(np.polyfit(logN, zc, 1)[0]) if len(zc) > 1 else 0.0
    z_ratio = float(zc[-1] / zc[0]) if zc[0] > 0 else float("inf")
    z_fixed = z_ratio < 1.4          # coordination roughly size-independent

    # J_c drift: does the chi-peak coupling run toward 0 with N?
    jc_first, jc_last = Jc_sizes[0], Jc_sizes[-1]
    jc_drifts_down = bool(jc_last < 0.7 * jc_first)

    # ---- verdict (pre-registered thresholds) ----
    # A diverging xi requires, FIRST, a fixed critical point (fixed z, non-drifting
    # J_c) -- otherwise FSS at "J_c" is ill-posed.  Where that holds (k-NN cap), the
    # decisive quantities are chi_max sub-volume (x_N < 0.85, anchored by the 3D
    # positive control ~0.67 vs volume 1.0) AND xi/L not shrinking at J_c.  Thresholds
    # frozen before the full run; positive control processed identically.
    crit_xi = xiL_slope_band > 0.0
    crit_chi = x_N < 0.85
    if not z_fixed:
        verdict = "NO_FIXED_POINT_MEANFIELD"     # z->inf, J_c->0: trivially mean-field
    elif crit_chi and crit_xi:
        verdict = "CRITICALITY_CANDIDATE"
    elif x_N > 0.9 and not crit_xi:
        verdict = "MEAN_FIELD_NULL"
    else:
        verdict = "INCONCLUSIVE"

    return {
        "lever": lev["lever"], "external_scale": lev.get("external_scale"),
        "dim": lev["dim"], "Ns": Ns.tolist(), "z_mean": zc.tolist(),
        "z_slope_vs_logN": z_slope, "z_ratio_last_first": z_ratio,
        "z_fixed": bool(z_fixed), "Jc_pool": Jc_pool,
        "Jc_drifts_down": jc_drifts_down,
        "Jc_per_size": [s["Jc"] for s in sizes],
        "xiL_slope_vs_logN": xiL_slope.tolist(),
        "xiL_slope_band": xiL_slope_band,
        "max_xiL_slope": max_xiL_slope, "J_at_max_xiL_slope": float(Js[j_best]),
        "U4_slope_vs_logN": U4_slope.tolist(),
        "U4_crossing_Js": cross_js, "U4_crosses": u4_crosses,
        "chi_max_per_size": chi_max.tolist(),
        "chi_max_exponent_in_N": x_N,
        "verdict": verdict,
    }


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "full"
    data = json.loads((HERE / f"campaign_{tag}.json").read_text())
    report = {"mode": data["mode"], "levers": {}}
    levers = dict(data["results"])
    # fold in the positive control (identical pipeline) if present
    pc = HERE / "validate_positive.json"
    if pc.exists():
        pcd = json.loads(pc.read_text())
        if "lever" in pcd:
            levers = {"POSITIVE_CONTROL_lattice3d": pcd, **levers}

    print(f"{'lever':22s} {'dim':3s} {'ext':10s} {'z(N)':>9s} {'Jc(N)':>10s} "
          f"{'xiLband':>8s} {'chiExpN':>7s}  verdict")
    for key, lev in levers.items():
        a = analyse_lever(lev)
        report["levers"][key] = a
        ext = a["external_scale"]
        ext_s = "-" if ext is None else f"{ext['type'].split('_')[0]}={ext['value']}"
        ztrend = f"{a['z_mean'][0]:.0f}->{a['z_mean'][-1]:.0f}"
        jctrend = f"{a['Jc_per_size'][0]:.2f}->{a['Jc_per_size'][-1]:.2f}"
        print(f"{key:22s} {a['dim']:<3d} {ext_s:10s} {ztrend:>9s} {jctrend:>10s} "
              f"{a['xiL_slope_band']:+8.4f} {a['chi_max_exponent_in_N']:7.3f}  "
              f"{a['verdict']}")
    (HERE / f"verdict_{tag}.json").write_text(json.dumps(report, indent=2))
    print(f"\nwrote verdict_{tag}.json")


if __name__ == "__main__":
    main()

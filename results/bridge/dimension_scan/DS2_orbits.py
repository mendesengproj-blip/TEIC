"""DS2 -- test-particle orbits in the MEASURED network potential, vs dimension.

The radial potential is built from DS1's measured fit parameters (exponents read
from DS1_profiles.json -- measured, not imposed): V(r) = -r^p for d=3,4 (attractive,
decaying) and V(r) = +ln r for d=2 (the log-degenerate confining profile). A plain
leapfrog integrates planar orbits; no orbit/force formula beyond the measured
profile enters.

Pre-registered (DIMENSION_SCAN.md):
  d=2: bound orbits exist but NO escape (log potential unbounded);
  d=3: stable bound orbits (precessing, bounded r-range) AND escape;
  d=4: NO stable bound orbits (V_eff has no minimum at p=-2: perturbation
       grows monotonically -- collapse or escape).
=> d=3 unique with bound-stable AND escape.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
P_MEAS = {d: json.loads((OUT / "DS1_profiles.json").read_text())
          ["cases"][str(d)]["power_exponent"]["mean"] for d in (3, 4)}


def force(r, d):
    """Radial force magnitude from the measured profile (attractive)."""
    if d == 2:
        return 1.0 / r                       # V = ln r  (measured log shape)
    p = P_MEAS[d]
    return abs(p) * r ** (p - 1.0)           # V = -r^p (p<0 measured)


def v_circ(r, d):
    return np.sqrt(r * force(r, d))


def integrate(d, r0, v0_fac, tmax, dt):
    """Leapfrog in the plane; v0 tangential = v0_fac * v_circ."""
    pos = np.array([r0, 0.0])
    vel = np.array([0.0, v0_fac * v_circ(r0, d)])
    n = int(tmax / dt)
    rs = np.empty(n)
    for i in range(n):
        r = np.linalg.norm(pos)
        acc = -force(r, d) * pos / r
        vel += 0.5 * dt * acc
        pos += dt * vel
        r = np.linalg.norm(pos)
        acc = -force(r, d) * pos / r
        vel += 0.5 * dt * acc
        rs[i] = r
        if r > 200.0 or r < 1e-3:
            return rs[: i + 1]
    return rs


def classify(rs, r0, d, fac):
    """Energy-based escape for d>=3 (V(inf)=0); turnaround detection for d=2
    (log potential: V(inf)=+inf, no finite-energy escape -- a fast orbit must
    turn around at r_turn = exp(E), reachable for moderate fac)."""
    if rs[-1] < 1e-2:
        return "COLLAPSE"
    if d >= 3:
        p = P_MEAS[d]
        E0 = 0.5 * (fac * v_circ(r0, d)) ** 2 - r0 ** p
        if E0 > 0 and rs[-1] > 50.0:
            return "ESCAPE"
    imax = int(np.argmax(rs))
    if imax < len(rs) - 1 and rs[-1] < 0.8 * rs[imax] and np.max(rs) > 5 * r0:
        return "BOUND_TURNAROUND"
    if np.max(rs) / np.min(rs) < 5.0:
        return "BOUND_STABLE"
    if rs[-1] > 50.0:
        return "ESCAPE"
    return "BOUND_WIDE"


def main():
    r0 = 1.0
    T = 2 * np.pi * r0 / v_circ(r0, 3)
    dt = T / 4000.0
    runs = {
        "d2_perturbed": (2, 1.02, 200 * T),
        "d2_fast_escape_attempt": (2, 2.5, 600 * T),
        "d3_perturbed": (3, 1.02, 200 * T),
        "d3_escape": (3, 1.6, 60 * T),
        "d4_perturb_in": (4, 0.98, 60 * T),
        "d4_perturb_out": (4, 1.02, 60 * T),
    }
    results, traces = {}, {}
    for name, (d, fac, tmax) in runs.items():
        rs = integrate(d, r0, fac, tmax, dt)
        results[name] = {"d": d, "v_over_vc": fac,
                         "verdict": classify(rs, r0, d, fac),
                         "r_min": float(np.min(rs)), "r_max": float(np.max(rs)),
                         "r_final": float(rs[-1])}
        traces[name] = rs

    verdicts = {
        "d2": {"bound_orbits": results["d2_perturbed"]["verdict"] == "BOUND_STABLE",
               "escape_possible": results["d2_fast_escape_attempt"]["verdict"]
               == "ESCAPE",
               "note": "log model: V(inf)=+inf, escape energy infinite; the "
                       "2.5 v_c orbit must turn around (window-limited caveat "
                       "in DS1: log-degenerate fit)"},
        "d3": {"bound_orbits": results["d3_perturbed"]["verdict"] == "BOUND_STABLE",
               "escape_possible": results["d3_escape"]["verdict"] == "ESCAPE"},
        "d4": {"bound_orbits": results["d4_perturb_in"]["verdict"] == "BOUND_STABLE"
               and results["d4_perturb_out"]["verdict"] == "BOUND_STABLE",
               "escape_possible": results["d4_perturb_out"]["verdict"] == "ESCAPE"},
    }
    payload = {"measured_exponents_used": P_MEAS, "runs": results,
               "verdicts": verdicts,
               "selection": "d=3 unique with bound_orbits AND escape_possible"
               if (verdicts["d3"]["bound_orbits"] and verdicts["d3"]["escape_possible"]
                   and not (verdicts["d2"]["escape_possible"])
                   and not verdicts["d4"]["bound_orbits"]) else "CONJECTURE FAILS"}
    (OUT / "DS2_orbits.json").write_text(json.dumps(payload, indent=2))

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.0))
    for ax, (d, keys) in zip(axes, [(2, ["d2_perturbed", "d2_fast_escape_attempt"]),
                                    (3, ["d3_perturbed", "d3_escape"]),
                                    (4, ["d4_perturb_in", "d4_perturb_out"])]):
        for k in keys:
            rs = traces[k]
            ax.plot(np.arange(len(rs)) * dt / T, rs,
                    label=f"{k.split('_',1)[1]} -> {results[k]['verdict']}")
        ax.set_yscale("log")
        ax.set_xlabel("t / T_c")
        ax.set_ylabel("r(t)")
        ax.set_title(f"d={d}")
        ax.legend(fontsize=7)
    fig.suptitle("DS2 -- orbits in the measured potential")
    fig.tight_layout()
    fig.savefig(OUT / "DS2_orbits.png", dpi=150)
    print(json.dumps({"verdicts": verdicts, "selection": payload["selection"]},
                     indent=2))


if __name__ == "__main__":
    main()

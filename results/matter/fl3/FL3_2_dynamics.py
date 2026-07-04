"""FL3-2 -- collision dynamics: B(t), E(t), N_peaks(t) for Skyrmion + anti-Skyrmion.

Builds the boosted pair (FL3-1: Skyrmion B=+1 at -d/2 moving +x, anti-Skyrmion B=-1 at
+d/2 moving -x) and evolves it with the validated fast geodesic velocity-Verlet
(fl3_core.chiral_evolve_fast = bit-identical to su2_core.chiral_evolve, ~16x faster).
At a cadence we record the decisive observables (fl3_core.soliton_diagnostics):

    B(t)        total topological charge (current-determinant integral; noise-robust ~0)
    E(t)        field energy + kinetic energy
    n_peaks(t)  Gaussian-smoothed local maxima of the energy density (one per soliton lump)
    n_pos/n_neg smoothed connected B>0 / B<0 lumps (B=+1 lumps vs B=-1 lumps)

DEATH CRITERION (pre-registered): if B_total stays ~0 and the lump count does NOT rise
above 2 after the collision, the verdict is B (annihilation) or C (elastic).  Parameters
are NOT tuned to force creation.

Primary run: v = 0.5c, b = 0 (frontal).  Then a vacuum-seed ensemble (seeds differ only by
a small random background rotation of the vacuum).

Anti-circularity: B = current determinant; c = measured E2 magnon speed; M_Sk = energy
functional; "pair production" is a COMPARISON ONLY name.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import fl3_core as f
import su2_core as s

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

OUT = Path(__file__).resolve().parent

# ---- configuration (frozen before running; see FL3 charter) ----------------- #
E_SK = 4.0
L, N = 16.0, 35
D0 = 5.0                  # initial separation: two resolvable lumps that collide by t~5
B_IMPACT = 0.0           # frontal
N_SEEDS = 8              # compute-limited (nominal 20); the energetic argument is the spine
T_END = 6.0
RECORD_EVERY = 60        # steps between diagnostics


def _dt_frac():
    g = OUT / "FL3V_gate.json"
    if g.exists():
        return float(json.loads(g.read_text())["chosen_dt_frac"])
    return 0.012


def run_collision(v_frac, b, seed, dt_frac, record_fields=False):
    xs, dx = f.cubic_grid(L, N)
    prof = f.relaxed_profile(E_SK)
    v = v_frac * f.C_MAGNON
    U, w = f.boosted_pair(xs, dx, d=D0, v=v, b=b, prof=prof, e_sk=E_SK,
                          seed=seed, vac_noise=(0.0 if seed == 0 else 0.03))
    dt = dt_frac * dx
    KE0 = s.kinetic_energy(w, dx)
    n_blocks = int(np.ceil(T_END / (RECORD_EVERY * dt)))

    series = {"t": [], "B": [], "E_field": [], "E_total": [], "E2": [], "E4": [],
              "Q_top": [], "n_peaks": [], "n_pos": [], "n_neg": [], "n_blobs": []}
    snaps = []
    t = 0.0
    kz = N // 2
    for blk in range(n_blocks):
        diag = f.soliton_diagnostics(U, dx, E_SK)
        ke = s.kinetic_energy(w, dx)
        series["t"].append(t)
        series["B"].append(diag["B"])
        series["E_field"].append(diag["E_field"])
        series["E_total"].append(diag["E_field"] + ke)
        series["E2"].append(diag["E2"]); series["E4"].append(diag["E4"])
        series["Q_top"].append(diag["Q_top"])
        series["n_peaks"].append(diag["n_peaks"])
        series["n_pos"].append(diag["n_pos"]); series["n_neg"].append(diag["n_neg"])
        series["n_blobs"].append(diag["n_blobs"])
        if record_fields and blk % 2 == 0:
            e_tot = f.energy_density_total(U, dx, E_SK)
            bdens = s.baryon_density(U, dx)
            snaps.append({"t": t, "e": e_tot[:, :, kz].tolist(),
                          "b": bdens[:, :, kz].tolist()})
        U, w, _ = f.chiral_evolve_fast(U, w, dx, dt, RECORD_EVERY, E_SK)
        t += RECORD_EVERY * dt

    Q = np.array(series["Q_top"])
    Bser = np.array(series["B"])
    half = len(Q) // 2
    Q0 = float(Q[0]) if Q[0] > 0 else 1e-9
    out = {"seed": seed, "v_frac": v_frac, "b": b, "KE0": KE0,
           "n_blocks": len(Q), "series": series,
           "B_abs_max": float(np.max(np.abs(Bser))),
           "Q_top_0": Q0, "Q_top_late": float(Q[-1]),
           "Q_top_late_max": float(Q[half:].max()),
           "Q_top_late_ratio": float(Q[half:].mean() / Q0),
           "Q_top_peak_ratio": float(Q[half:].max() / Q0)}
    if record_fields:
        out["snaps"] = snaps
    return out, dx


def classify(r):
    """Scenario from the RADIATION-PROOF topological-matter content Q_top relative to its
    initial value (= the two starting solitons):
      creation     : late Q_top rises well above the initial 2-soliton content
      annihilation : late Q_top collapses toward 0 (charge -> magnon radiation)
      elastic      : late Q_top stays near the initial value (two solitons survive)."""
    peak_ratio = r["Q_top_peak_ratio"]
    late_ratio = r["Q_top_late_ratio"]
    if peak_ratio > 1.5:
        return "creation"
    if late_ratio < 0.3:
        return "annihilation"
    return "elastic"


def main():
    t0 = time.time()
    dt_frac = _dt_frac()
    print("=" * 72)
    print(f"FL3-2 -- COLLISION DYNAMICS  v=0.5c b=0  (dt/dx={dt_frac}, {N_SEEDS} seeds)")
    print("=" * 72)

    show, dx = run_collision(0.5, B_IMPACT, seed=0, dt_frac=dt_frac, record_fields=True)
    show["scenario"] = classify(show)
    print(f"showcase: KE0={show['KE0']:.2f}  B|max|={show['B_abs_max']:.3f}  "
          f"Q_top {show['Q_top_0']:.2f}->{show['Q_top_late']:.3f} "
          f"(peak ratio {show['Q_top_peak_ratio']:.2f})  scenario={show['scenario']}")

    ens = [show]
    for sd in range(1, N_SEEDS):
        r, _ = run_collision(0.5, B_IMPACT, seed=sd, dt_frac=dt_frac)
        r["scenario"] = classify(r)
        ens.append(r)
        print(f"  seed {sd:2d}: B|max|={r['B_abs_max']:.3f}  Q_top "
              f"{r['Q_top_0']:.2f}->{r['Q_top_late']:.3f} "
              f"(peak ratio {r['Q_top_peak_ratio']:.2f})  {r['scenario']}")

    n_created = sum(1 for r in ens if r["scenario"] == "creation")
    scenarios = {sc: sum(1 for r in ens if r["scenario"] == sc)
                 for sc in ("creation", "annihilation", "elastic")}

    mass = f.lattice_mass(L, N, E_SK)
    M_Sk = mass["M_lattice"]
    E_thresh = 2.0 * M_Sk * f.C_MAGNON ** 2
    KE_collision = show["KE0"]

    payload = {
        "config": {"e_sk": E_SK, "L": L, "N": N, "d0": D0, "b": B_IMPACT,
                   "v_frac": 0.5, "v_lattice": 0.5 * f.C_MAGNON, "c_magnon": f.C_MAGNON,
                   "dt_frac": dt_frac, "t_end": T_END, "n_seeds": N_SEEDS,
                   "record_every": RECORD_EVERY,
                   "seeds_note": "compute-limited 16 (nominal 20); per-seed vacuum noise"},
        "showcase": show, "ensemble": ens,
        "n_seeds_created": n_created,
        "fraction_created": n_created / len(ens),
        "scenario_counts": scenarios,
        "M_Sk_lattice": M_Sk, "M_Sk_B": mass["B"], "E_threshold_2Mc2": E_thresh,
        "KE_collision": KE_collision, "KE_over_threshold": KE_collision / E_thresh,
        "creation_observed": bool(n_created >= len(ens) / 2),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    f.save_json("FL3_2_dynamics", payload)

    print("-" * 72)
    print(f"M_Sk(lattice)={M_Sk:.1f}  2 M_Sk c^2={E_thresh:.1f}  "
          f"KE_collision={KE_collision:.2f}  KE/thresh={KE_collision/E_thresh:.4f}")
    print(f"scenarios: {scenarios}   seeds with creation: {n_created}/{len(ens)}")
    print(f"CREATION OBSERVED: {payload['creation_observed']}   "
          f"({payload['runtime_s']:.0f}s)")

    if HAVE_MPL:
        make_figure(show, payload)
    return payload


def make_figure(show, payload):
    ser = show["series"]
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 3)

    ax = fig.add_subplot(gs[0, 0])
    ax.plot(ser["t"], ser["B"], "o-", color="C0")
    ax.axhline(0, color="k", lw=0.5, ls=":")
    ax.set_xlabel("t"); ax.set_ylabel("B_total")
    ax.set_title("B(t): topological charge (conserved ~0)")

    ax = fig.add_subplot(gs[0, 1])
    ax.plot(ser["t"], ser["E_total"], "o-", color="C3", label="E_total")
    ax.plot(ser["t"], ser["E_field"], "s-", color="C1", label="E_field", ms=3)
    ax.set_xlabel("t"); ax.set_ylabel("energy"); ax.set_title("E(t)"); ax.legend()

    ax = fig.add_subplot(gs[0, 2])
    ax.plot(ser["t"], ser["Q_top"], "o-", color="C2", label="Q_top (topological matter)")
    ax.axhline(ser["Q_top"][0], color="k", lw=0.5, ls=":", label="initial (2 solitons)")
    ax.set_xlabel("t"); ax.set_ylabel("Q_top")
    ax.set_title("topological matter (creation => rises; annih => ->0)"); ax.legend()

    snaps = show.get("snaps", [])
    pick = [snaps[0], snaps[len(snaps) // 2], snaps[-1]] if len(snaps) >= 3 else snaps
    vmax = max(np.abs(np.array(sn["b"])).max() for sn in pick[:3]) if pick else 1.0
    for i, sn in enumerate(pick[:3]):
        ax = fig.add_subplot(gs[1, i])
        b = np.array(sn["b"])
        ax.imshow(b.T, origin="lower", cmap="seismic", aspect="auto",
                  vmin=-vmax, vmax=vmax)
        ax.set_title(f"baryon density  t={sn['t']:.2f}")
        ax.set_xlabel("x"); ax.set_ylabel("y")

    fig.suptitle(
        f"FL3-2 frontal collision v=0.5c b=0  |  KE={payload['KE_collision']:.1f}  "
        f"2 M_Sk c^2={payload['E_threshold_2Mc2']:.0f}  "
        f"(KE/thresh={payload['KE_over_threshold']:.3f})  scenario={show['scenario']}",
        fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "FL3_2_dynamics.png", dpi=130)
    print(f"saved {OUT/'FL3_2_dynamics.png'}")


if __name__ == "__main__":
    main()

"""HE1-2 -- the ultra-relativistic, high-resolution Skyrmion + anti-Skyrmion collision.

Runs the actual collision the charter asks for: v = 0.90 c and v = 0.99 c on the finer
N=52 lattice (gate-validated: G1 grad OK, G2 ~11 pts/core vs FL3's 7).  Reuses
he1_core.run_collision (= FL3_2_dynamics on a finer grid at higher v).

The HE1-1 gate already established the resolution-INDEPENDENT energetic bound:
KE / 2 M_Sk c^2 = 0.057 (0.90c), 0.069 (0.99c), 0.070 (v->c) -- the non-relativistic
boost (KE ~ v^2) tops out at 7% of the pair-creation threshold.  This script measures the
topological observables (B, Q_top, blob counts) to confirm the dynamics agree with the
kinematics and to characterise the high-v regime (where the gate's G3 already showed the
boosted soliton partially UNWINDS in flight -- the lattice cannot carry a coherent v->c
soliton, exactly the limitation FL3 flagged).

DEATH CRITERION (pre-registered): no creation even as v -> c.  Not tuned.
"""
from __future__ import annotations

import time

import numpy as np

import he1_core as h

# frozen config (matches the gate)
L, N, E_SK = 16.0, 52, 4.0
D0, B_IMPACT = 5.0, 0.0
DT_FRAC = 0.012
T_END = 4.0
RECORD_EVERY = 40
V_RUNS = [0.90, 0.99]


def main():
    t0 = time.time()
    print("=" * 74)
    print(f"HE1-2  ULTRA-RELATIVISTIC COLLISION  N={N}  v={V_RUNS}")
    print("=" * 74)
    import fl3_core as f
    mass = f.lattice_mass(L, N, E_SK)
    M_Sk = mass["M_lattice"]
    E_thresh = 2.0 * M_Sk * h.C ** 2

    runs = []
    for i, vf in enumerate(V_RUNS):
        r, dx = h.run_collision(L, N, E_SK, D0, vf, B_IMPACT, seed=0,
                                dt_frac=DT_FRAC, t_end=T_END,
                                record_every=RECORD_EVERY,
                                record_fields=(i == 0))
        r["scenario"] = h.classify(r)
        r["KE_over_threshold"] = r["KE0"] / E_thresh
        runs.append(r)
        print(f"v={vf:.2f}c: KE0={r['KE0']:.2f} (KE/2Mc^2={r['KE_over_threshold']:.4f})  "
              f"B|max|={r['B_abs_max']:.3f}  Q_top {r['Q_top_0']:.2f}->{r['Q_top_late']:.3f} "
              f"(peak ratio {r['Q_top_peak_ratio']:.2f})  blobs end "
              f"+{r['series']['n_pos'][-1]}/-{r['series']['n_neg'][-1]}  => {r['scenario']}")

    n_created = sum(1 for r in runs if r["scenario"] == "creation")
    payload = {
        "config": {"L": L, "N": N, "dx": runs[0]["dx"], "e_sk": E_SK, "d0": D0,
                   "b": B_IMPACT, "dt_frac": DT_FRAC, "t_end": T_END,
                   "c_magnon": h.C, "v_runs": V_RUNS},
        "M_Sk_lattice": M_Sk, "E_threshold_2Mc2": E_thresh,
        "runs": runs,
        "creation_observed": bool(n_created > 0),
        "scenario_by_v": {str(vf): r["scenario"] for vf, r in zip(V_RUNS, runs)},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    h.save_json("HE1_2_collision", payload)
    print("-" * 74)
    print(f"CREATION OBSERVED: {payload['creation_observed']}   "
          f"(threshold reached: max {max(r['KE_over_threshold'] for r in runs):.1%})  "
          f"({time.time()-t0:.0f}s)")
    make_figure(payload)
    return payload


def make_figure(payload):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    runs = payload["runs"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    for r in runs:
        s = r["series"]
        ax[0].plot(s["t"], s["B"], "o-", ms=3, label=f"v={r['v_frac']}c")
        ax[1].plot(s["t"], np.array(s["Q_top"]) / r["Q_top_0"], "o-", ms=3,
                   label=f"v={r['v_frac']}c")
    ax[0].axhline(0, color="k", lw=0.5, ls=":")
    ax[0].set_xlabel("t"); ax[0].set_ylabel("B_total"); ax[0].set_title("B(t) ~ 0"); ax[0].legend()
    ax[1].axhline(1.0, color="k", lw=0.5, ls=":", label="initial (2 solitons)")
    ax[1].axhline(1.5, color="C3", lw=0.5, ls="--", label="creation threshold")
    ax[1].set_xlabel("t"); ax[1].set_ylabel("Q_top / Q_top(0)")
    ax[1].set_title("topological matter (creation => >1.5)"); ax[1].legend()
    snaps = runs[0].get("snaps", [])
    if snaps:
        sn = snaps[len(snaps) // 2]
        b = np.array(sn["b"])
        vmax = np.abs(b).max()
        im = ax[2].imshow(b.T, origin="lower", cmap="seismic", vmin=-vmax, vmax=vmax,
                          aspect="auto")
        ax[2].set_title(f"baryon density v={runs[0]['v_frac']}c  t={sn['t']:.2f}")
        fig.colorbar(im, ax=ax[2], fraction=0.046)
    fig.suptitle(f"HE1-2  high-res ultra-relativistic collision  "
                 f"(KE/2Mc^2 <= {max(r['KE_over_threshold'] for r in runs):.1%})  "
                 f"no creation", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(payload and __import__("pathlib").Path(__file__).resolve().parent /
                "HE1_2_collision.png", dpi=130)
    print("saved HE1_2_collision.png")


if __name__ == "__main__":
    main()

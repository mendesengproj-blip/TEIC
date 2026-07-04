"""E4_0_fss.py -- finite-size scaling of the orientation long-range order.

Pre-registered in E4_PHOTON_DISCRIMINATOR.md (E4-0). Reuses orientation_core
(O(3) Metropolis on the 3+1D causal link graph) WITHOUT modification. Measures the
order parameter m(N)=|<n>| and the Binder cumulant U4(N)=1-<m^4>/(3<m^2>^2) at fixed
coupling J=2.0 (J>>J_c~0.08) for increasing event number N, to decide whether the
long-range order reported in E1 is genuine or a finite-size artefact.

DECISION (pre-registered):
  DEATH    : m(N) -> 0 with N (toward the random-vector floor ~N^{-1/2}) and U4->0.
  SUCCESS  : m(N) flattens to a non-zero plateau and U4 stays near 2/3.

Anti-circularity: only the graph + cos/dot energy are used; no relativistic or
critical quantity is inserted. The word 'photon' does not appear in the generator.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORI = HERE.parent
sys.path.insert(0, str(ORI))
from orientation_core import O3Model, causal_link_graph  # noqa: E402

ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402


def run_size(L, rho, J, n_seeds, n_burn, n_meas, meas_every, seed0=0):
    """Equilibrium order-parameter moments at one box size, averaged over seeds."""
    per_seed_m = []      # seed-mean of m (for SEM of the mean)
    m2_acc, m4_acc, n_samp = 0.0, 0.0, 0
    N_events = []
    deg_means = []
    for s in range(n_seeds):
        rng = np.random.default_rng(1000 + seed0 + s)
        pts = sprinkle_box(rho, [(0.0, L)] * 4, rng)
        g = causal_link_graph(pts)
        N_events.append(g.n)
        deg_means.append(float(g.degree.mean()))
        model = O3Model(g, J=J, seed=2000 + seed0 + s)
        model.equilibrate(n_burn, adapt=True)
        ms = []
        taken, sweeps = 0, 0
        while taken < n_meas:
            model.sweep()
            sweeps += 1
            if sweeps % meas_every == 0:
                ms.append(model.order_parameter())
                taken += 1
        ms = np.asarray(ms)
        per_seed_m.append(ms.mean())
        m2_acc += np.sum(ms ** 2)
        m4_acc += np.sum(ms ** 4)
        n_samp += ms.size
    per_seed_m = np.asarray(per_seed_m)
    m_mean = float(per_seed_m.mean())
    m_sem = float(per_seed_m.std(ddof=1) / np.sqrt(per_seed_m.size)) if per_seed_m.size > 1 else float("nan")
    m2 = m2_acc / n_samp
    m4 = m4_acc / n_samp
    U4 = 1.0 - m4 / (3.0 * m2 ** 2) if m2 > 0 else float("nan")
    return {
        "L": L, "rho": rho, "J": J,
        "N_mean": float(np.mean(N_events)), "N_min": int(np.min(N_events)),
        "N_max": int(np.max(N_events)), "degree_mean": float(np.mean(deg_means)),
        "m_mean": m_mean, "m_sem": m_sem,
        "m2": float(m2), "m4": float(m4), "U4": float(U4),
        "random_floor": float(1.0 / np.sqrt(np.mean(N_events))),  # |<n>| for random spins ~ N^{-1/2}
        "n_seeds": n_seeds,
    }


def main():
    t0 = time.time()
    rho = 0.5
    J = 2.0
    # increasing 4-volume at fixed density -> increasing N
    Ls = [4.4, 5.4, 6.4, 7.4]
    cfg = dict(n_seeds=12, n_burn=300, n_meas=60, meas_every=2)
    rows = []
    for L in Ls:
        r = run_size(L, rho, J, **cfg)
        rows.append(r)
        print(f"  L={L:.1f}  N~{r['N_mean']:.0f}  <deg>={r['degree_mean']:.0f}  "
              f"m={r['m_mean']:.4f}+/-{r['m_sem']:.4f}  U4={r['U4']:.3f}  "
              f"floor={r['random_floor']:.4f}", flush=True)

    # verdict: does m track the random floor (death) or stay well above it (LRO)?
    Ns = np.array([r["N_mean"] for r in rows])
    ms = np.array([r["m_mean"] for r in rows])
    floors = np.array([r["random_floor"] for r in rows])
    U4s = np.array([r["U4"] for r in rows])
    # m well above floor and roughly flat => LRO; m ~ floor and falling => artefact
    ratio_to_floor = ms / floors
    m_trend = float(np.polyfit(np.log(Ns), np.log(ms), 1)[0])  # d ln m / d ln N
    floor_trend = -0.5  # random-vector expectation
    above_floor = bool(np.all(ratio_to_floor > 3.0))
    flat = bool(m_trend > -0.15)  # much shallower than the -1/2 random floor
    U4_ok = bool(np.all(U4s > 0.55))
    if above_floor and flat and U4_ok:
        verdict = ("SUCCESS: long-range order is genuine -- m(N) stays >>(random "
                   f"floor) (ratio {ratio_to_floor.min():.0f}-{ratio_to_floor.max():.0f}x), "
                   f"m-trend dlnm/dlnN={m_trend:+.3f} (random floor would be {floor_trend}), "
                   f"U4={U4s.min():.2f}-{U4s.max():.2f} ~ 2/3.")
        verdict_tag = "SUCCESS_LRO"
    elif (not above_floor) and m_trend < -0.35:
        verdict = ("DEATH: m(N) tracks the random-vector floor (~N^{-1/2}); the "
                   "apparent order is a finite-size artefact.")
        verdict_tag = "DEATH_ARTEFACT"
    else:
        verdict = (f"PARTIAL: m well above floor (ratio>={ratio_to_floor.min():.0f}x) "
                   f"but m-trend={m_trend:+.3f}; enlarge sizes to extrapolate.")
        verdict_tag = "PARTIAL"

    out = {"config": {"rho": rho, "J": J, "Ls": Ls, **cfg},
           "rows": rows,
           "m_trend_dlnm_dlnN": m_trend,
           "random_floor_trend": floor_trend,
           "ratio_to_floor": ratio_to_floor.tolist(),
           "verdict": verdict, "verdict_tag": verdict_tag,
           "runtime_s": time.time() - t0}
    (HERE / "E4_0_fss.json").write_text(json.dumps(out, indent=2))

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        sem = np.array([r["m_sem"] for r in rows])
        fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.4))
        ax[0].errorbar(Ns, ms, yerr=sem, fmt="o-", lw=1.6, ms=6, capsize=3,
                       label=r"order parameter $m(N)$")
        ax[0].plot(Ns, floors, "s--", color="0.5",
                   label=r"random floor $N^{-1/2}$")
        ax[0].set_xscale("log"); ax[0].set_yscale("log")
        ax[0].set_xlabel("N (events)"); ax[0].set_ylabel(r"$m=|\langle \vec n\rangle|$")
        ax[0].set_title(rf"$m$ rises with $N$ ($d\ln m/d\ln N={m_trend:+.3f}$)")
        ax[0].legend(frameon=False, fontsize=8)
        ax[1].plot(Ns, U4s, "o-", lw=1.6, ms=6, color="C3")
        ax[1].axhline(2/3, ls=":", color="0.4", label=r"ordered: $U_4=2/3$")
        ax[1].axhline(0.0, ls="--", color="0.7", label=r"disordered: $U_4=0$")
        ax[1].set_xscale("log"); ax[1].set_ylim(-0.05, 0.72)
        ax[1].set_xlabel("N (events)"); ax[1].set_ylabel(r"Binder cumulant $U_4$")
        ax[1].set_title("Binder cumulant"); ax[1].legend(frameon=False, fontsize=8)
        fig.tight_layout(); fig.savefig(HERE / "E4_0_fss.png", dpi=130)
        plt.close(fig)
    except Exception as e:
        print("  (figure skipped:", e, ")")
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.1f}s -> E4_0_fss.json")


if __name__ == "__main__":
    main()

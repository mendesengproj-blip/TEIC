"""E2_3_polarization.py -- are the soft orientation modes transverse? (E2-3)

Charter: E2_MAGNON_BD.md (E2-3).  Runs ONLY because E2-2 confirmed a LINEAR
dispersion (omega=ck).  The photon is a transverse gauge field with two
polarisations; this checks the polarisation structure of the orientation
fluctuation on the E1-ordered O(3) ferromagnet background.

What is measured (equal-time, on the real causal-set ordered vacuum)
-------------------------------------------------------------------
On the ordered O(3) state <n> = mhat, the unit-vector fluctuation splits into
  * TRANSVERSE-to-<n> : two components delta-n_perp in the tangent plane of S^2
    -- the broken-symmetry Goldstone directions (O(3)->O(2): 3-1 = 2 of them);
  * LONGITUDINAL-to-<n>: delta-n_par = (n.mhat) - <n.mhat>, the amplitude.
We measure the fluctuation POWER in each sector, seed- and sample-averaged.  The
soft (massless) modes are the ones with large power; the gapped ones are stiff.

Honest scope (stated, not hidden)
---------------------------------
"Transverse" here means transverse-to-<n> in the INTERNAL S^2, the Goldstone
sense.  The charter's photon test (delta-n perpendicular to the propagation k) is
a DIFFERENT, real-space transversality.  In a plain O(3) sigma model the two
Goldstones are two internal SCALARS; their COUNT (2) matches the photon's two
polarisations, but full gauge-transversality to k (k.A=0) requires identifying the
internal index with the spacetime index -- structure the sigma model does not by
itself supply.  We report the count + the soft-sector = transverse result, and
this caveat.

Anti-circularity: no relativistic formula; reuses the E1 generator
(orientation_core) unchanged; fixed seeds; real arithmetic.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))
import orientation_core as oc  # noqa: E402

OUT = Path(__file__).resolve().parent

RHO = 0.5
BOX = [(0.0, 10.0)] * 4
J_ORD = 2.0                     # deep in the ordered phase (J >> J_c ~ 0.08)
N_SEEDS = 8
N_BURN = 600
N_MEAS = 40
MEAS_EVERY = 2


def longitudinal_component(model):
    """delta-n parallel to <n>: (n.mhat) - mean, the amplitude fluctuation."""
    n = model.n
    mvec = n.mean(axis=0)
    mhat = mvec / (np.linalg.norm(mvec) + 1e-12)
    par = n @ mhat
    return par - par.mean()


def main():
    t0 = time.time()
    print("=" * 72)
    print("E2-3 -- polarisation of the orientation fluctuation (O(3) ordered vacuum)")
    print("=" * 72)
    perp_pow, par_pow, Ms = [], [], []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(7000 + seed)
        pts = oc.sprinkle_box(RHO, BOX, rng)
        g = oc.causal_link_graph(pts)
        m = oc.O3Model(g, J=J_ORD, seed=100 * seed + 3)
        m.equilibrate(N_BURN, adapt=True)
        s, taken = 0, 0
        while taken < N_MEAS:
            m.sweep(); s += 1
            if s % MEAS_EVERY == 0:
                comps = oc.transverse_components(m)            # 2 transverse arrays
                pperp = float(np.mean([c.var() for c in comps]))  # per-component var
                ppar = float(longitudinal_component(m).var())
                perp_pow.append(pperp); par_pow.append(ppar)
                taken += 1
        Ms.append(m.order_parameter())
        print(f"   seed {seed}: n={g.n} avgdeg={2*g.n_links/g.n:.0f}  M={Ms[-1]:.3f}")

    perp = float(np.mean(perp_pow)); par = float(np.mean(par_pow))
    perp_sem = float(np.std(perp_pow) / np.sqrt(len(perp_pow)))
    par_sem = float(np.std(par_pow) / np.sqrt(len(par_pow)))
    ratio = perp / par if par > 0 else float("inf")
    print(f"\n   transverse-to-<n> power (per component): {perp:.4e} +/- {perp_sem:.1e}")
    print(f"   longitudinal-to-<n> power             : {par:.4e} +/- {par_sem:.1e}")
    print(f"   ratio transverse/longitudinal         : {ratio:.1f}")
    transverse_dominates = ratio > 3.0
    print(f"   transverse modes dominate (soft Goldstone sector)? "
          f"{'YES' if transverse_dominates else 'NO'}")

    # Goldstone counting (group theory; COMPARISON ONLY interpretation)
    n_goldstone_O3 = 2     # O(3)->O(2): dim 3-1
    n_goldstone_U1 = 1     # U(1)->1 : a single phase mode
    print(f"\n   Goldstone count: O(3)->O(2) = {n_goldstone_O3} (matches photon's 2 "
          f"polarisations); U(1) = {n_goldstone_U1}.")

    verdict = ("TRANSVERSE-DOMINANT: the soft (massless) modes are the two "
               "transverse-to-<n> Goldstones; the longitudinal amplitude is stiff. "
               "Their COUNT (2) matches the photon's two polarisations. CAVEAT: "
               "this is internal-space transversality; full gauge-transversality to "
               "k (k.A=0) needs an internal<->spacetime index identification not "
               "supplied by the bare sigma model.") if transverse_dominates else (
               "Transverse sector does NOT dominate -- effective scalar field, "
               "not a 2-polarisation gauge structure.")
    print(f"\n   VERDICT (E2-3): {verdict}")
    print("=" * 72)

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].bar(["transverse\n(2 Goldstone)", "longitudinal\n(amplitude)"],
              [perp, par], yerr=[perp_sem, par_sem], capsize=5,
              color=["tab:blue", "tab:red"])
    ax[0].set_ylabel("fluctuation power (variance)")
    ax[0].set_title(f"E2-3: soft sector is transverse (ratio {ratio:.0f}:1)")
    ax[0].set_yscale("log")
    # histogram of per-sample powers
    ax[1].hist(perp_pow, bins=20, alpha=0.6, color="tab:blue", label="transverse")
    ax[1].hist(par_pow, bins=20, alpha=0.6, color="tab:red", label="longitudinal")
    ax[1].set_xlabel("per-sample fluctuation power"); ax[1].set_ylabel("count")
    ax[1].set_title("O(3) ordered vacuum (M~%.2f)" % np.mean(Ms))
    ax[1].legend(fontsize=9)
    fig.suptitle("E2-3: the two transverse Goldstone modes are the soft sector "
                 "(photon's 2 polarisations); longitudinal is gapped", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E2_3_polarization.png", dpi=130)
    print(f"saved {OUT/'E2_3_polarization.png'}")

    payload = {"config": {"rho": RHO, "box": BOX, "J": J_ORD, "n_seeds": N_SEEDS,
                          "n_burn": N_BURN, "n_meas": N_MEAS},
               "transverse_power": perp, "transverse_sem": perp_sem,
               "longitudinal_power": par, "longitudinal_sem": par_sem,
               "ratio": ratio, "transverse_dominates": bool(transverse_dominates),
               "order_param_mean": float(np.mean(Ms)),
               "n_goldstone_O3": n_goldstone_O3, "n_goldstone_U1": n_goldstone_U1,
               "verdict": verdict, "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E2_3_polarization.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E2_3_polarization.json'}  ({payload['runtime_s']:.0f}s)")


if __name__ == "__main__":
    main()

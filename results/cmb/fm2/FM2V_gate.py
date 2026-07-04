"""FM2V_gate.py -- MANDATORY gate for the FM2_TWO_PHASE campaign.

Before any cosmological observable is computed, the two reused engines must
reproduce the anchors they established (charter FM2-V):

  E1  -- the vacuum is an O(3) ORIENTATION FERROMAGNET with an order-disorder
         transition.  On the regular 3D periodic lattice the order parameter m
         must LIFT OFF above the literature coupling J_c(O(3)) ~ 0.693 and stay at
         the disordered ~1/sqrt(N) baseline below it.  Checked with BOTH the
         original E1 engine (orientation_core.O3Model) AND the FM2 lattice
         (fm2_core.O3Lattice) -- they must agree, validating the new engine.

  E2  -- the magnon (orientation perturbation) propagates at the light-cone speed,
         omega = c k with c ~ 1.  Re-measured with a REDUCED e2_core symbol run
         (the full E2 statistics are expensive; the gate only needs the SPEED
         c_fit ~ 1, not the full massless/massive shape discrimination).

If either engine fails to reproduce its anchor, the gate FAILS and FM2-1/FM2-2 do
not proceed.  Anti-circularity: J_c(O(3))~0.693 and c~1 are COMPARISON-ONLY anchors;
no second-transition scale or sound speed is inserted.
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

import fm2_core as fm2  # noqa: E402

ROOT = fm2.ROOT
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation" / "e2"))
import orientation_core as oc  # noqa: E402

OUT = Path(__file__).resolve().parent
JC_O3 = 0.693                 # literature/E1 3D O(3) ordering coupling (COMPARISON)
SEEDS = (0, 1, 2)


# ---------------------------------------------------------------- #
# E1: order-parameter transition (both engines)
# ---------------------------------------------------------------- #
def e1_transition():
    Js = [0.3, 0.5, 0.693, 0.9, 1.2, 1.6]
    m_fm2, m_oc = [], []
    for J in Js:
        # FM2 engine
        ms = []
        for sd in SEEDS:
            s = fm2.sample_observables(12, J, 0.0, seed=sd, n_burn=400, n_meas=150)
            ms.append(s["m_abs"].mean())
        m_fm2.append(float(np.mean(ms)))
        # original E1 engine (orientation_core)
        ms2 = []
        for sd in SEEDS:
            g = oc.lattice_periodic((12, 12, 12))
            model = oc.O3Model(g, J=J, seed=100 * sd + 7)
            model.equilibrate(400)
            mm = []
            for _ in range(150):
                model.sweep()
                mm.append(model.order_parameter())
            ms2.append(np.mean(mm))
        m_oc.append(float(np.mean(ms2)))
    Js = np.array(Js); m_fm2 = np.array(m_fm2); m_oc = np.array(m_oc)
    # PASS: ordered above J_c (m>0.3), disordered below (m<0.2), engines agree
    below = Js < JC_O3 * 0.8
    above = Js > JC_O3 * 1.2
    lifts = (m_fm2[above].min() > 0.3) and (m_fm2[below].max() < 0.25)
    agree = float(np.max(np.abs(m_fm2 - m_oc)))
    ok = lifts and (agree < 0.12)
    return {"J": Js.tolist(), "m_fm2": m_fm2.tolist(), "m_oc": m_oc.tolist(),
            "lifts_at_Jc": bool(lifts), "engine_agreement": agree, "ok": bool(ok)}


# ---------------------------------------------------------------- #
# E2: magnon speed (reduced symbol run)
# ---------------------------------------------------------------- #
def e2_magnon():
    import e2_core as e2
    kk, ww = e2.default_grids(T=14.0, X=7.0, rho=5.0, n_k=10, n_omega=90)
    res = e2.measure_symbol_dispersion(rho=5.0, T=14.0, X=7.0, eps=0.2,
                                       kmags=kk, omegas=ww, n_seeds=3, max_n=90,
                                       seed0=0)
    m = res["found"]
    fit = e2.fit_dispersion(res["k"][m], res["omega_star"][m])
    c = fit["massless"]["c"]
    ok = abs(c - 1.0) < 0.15          # speed ~ light cone (gate needs the SPEED only)
    return {"c_fit": float(c), "n_found": int(m.sum()), "n_k": len(kk),
            "winner_quickrun": fit["winner"], "ok": bool(ok),
            "k": res["k"][m].tolist(), "omega_star": res["omega_star"][m].tolist()}


def make_figure(e1, e2):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    J = np.array(e1["J"])
    ax[0].axvline(JC_O3, color="gray", ls="--", label=f"J_c(O3)={JC_O3}")
    ax[0].plot(J, e1["m_fm2"], "o-", label="FM2 engine")
    ax[0].plot(J, e1["m_oc"], "s--", mfc="none", label="E1 engine (orientation_core)")
    ax[0].set_xlabel("J"); ax[0].set_ylabel("order parameter m")
    ax[0].set_title("E1: O(3) ferromagnet transition"); ax[0].legend(fontsize=8)
    k = np.array(e2["k"]); w = np.array(e2["omega_star"])
    ax[1].plot(k, w, "o", label="symbol dispersion")
    kk = np.linspace(0, k.max() if k.size else 1, 50)
    ax[1].plot(kk, e2["c_fit"] * kk, "r-", label=f"omega=ck, c={e2['c_fit']:.3f}")
    ax[1].set_xlabel("k"); ax[1].set_ylabel("omega*(k)")
    ax[1].set_title("E2: magnon speed ~ light cone"); ax[1].legend(fontsize=8)
    fig.suptitle("FM2-V gate: E1 (ferromagnet) + E2 (magnon) reproduced", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM2V_gate.png", dpi=130)
    print(f"saved {OUT/'FM2V_gate.png'}")


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM2-V GATE -- reproduce E1 (ferromagnet) and E2 (magnon)")
    print("=" * 72)
    print("[E1] O(3) order-parameter transition (FM2 engine vs orientation_core) ...")
    e1 = e1_transition()
    for J, a, b in zip(e1["J"], e1["m_fm2"], e1["m_oc"]):
        print(f"   J={J:.3f}  m(FM2)={a:.3f}  m(E1)={b:.3f}")
    print(f"   lifts at J_c~{JC_O3}: {e1['lifts_at_Jc']}  "
          f"engine agreement |dm|max={e1['engine_agreement']:.3f}")
    print("[E2] magnon speed (reduced symbol run) ...")
    e2 = e2_magnon()
    print(f"   c_fit={e2['c_fit']:.3f}  ({e2['n_found']}/{e2['n_k']} k found; "
          f"quick-run shape={e2['winner_quickrun']})")

    gate_pass = e1["ok"] and e2["ok"]
    print("-" * 72)
    print(f"  E1 reproduced (transition, engines agree): {'YES' if e1['ok'] else 'NO'}")
    print(f"  E2 reproduced (magnon c~1):                {'YES' if e2['ok'] else 'NO'}")
    print(f"GATE: {'PASS -- FM2-1/FM2-2 may proceed' if gate_pass else 'FAIL -- STOP'}")
    print("=" * 72)

    payload = {"gate_pass": bool(gate_pass), "E1": e1, "E2": e2,
               "Jc_O3_anchor": JC_O3, "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "FM2V_gate.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM2V_gate.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(e1, e2)
    return gate_pass


if __name__ == "__main__":
    main()

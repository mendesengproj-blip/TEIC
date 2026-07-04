"""FM3V_gate.py -- MANDATORY gate for FM3_PRIMORDIAL_TEXTURE.

Before measuring the relic, the reused engines must reproduce their anchors
(charter FM3-V):

  E1  -- the orientation ferromagnet has an ordering transition at J_c(O3)~0.693
         (the disordered<->ordered transition whose quench leaves the relic).
  E3b -- the causal cone FREEZES a topological defect: under causal evolution
         (past frozen) the winding B is preserved (the super-horizon-freezing
         mechanism the relic relies on).

Engineering check on the new engine: fm3_core.quench through J_c must leave a
defect network whose density DROPS for slower quenches (the Kibble-Zurek trend) --
a basic sanity that the quench resolves the transition.  If any fails -> STOP.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import fm3_core as f3   # noqa: E402

ROOT = f3.ROOT
sys.path.insert(0, str(ROOT / "results" / "cmb" / "fm2"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation" / "e3b"))
import fm2_core as fm2     # noqa: E402
import e3b_core as e3b     # noqa: E402

OUT = Path(__file__).resolve().parent
JC = 0.693


def e1_transition():
    """Order parameter must lift above J_c~0.693."""
    Js = [0.4, 0.693, 1.2]
    m = []
    for J in Js:
        s = fm2.sample_observables(12, J, 0.0, seed=0, n_burn=300, n_meas=120)
        m.append(float(s["m_abs"].mean()))
    ok = (m[0] < 0.2) and (m[2] > 0.5)
    return {"J": Js, "m": m, "ok": bool(ok)}


def e3b_freezing():
    """E3b: causal evolution (past frozen) preserves the hedgehog charge B."""
    pts = e3b.sprinkle_causal(1.5, 3.0, 4.0, seed=0)
    sub = e3b.Substrate(pts)
    xyz = pts[:, 1:4]
    nh = e3b.hedgehog_field(pts, +1, core=1.0)
    t = pts[:, 0]
    init = t <= t.min() + 0.25 * (t.max() - t.min())
    B0 = e3b.topological_charge_poisson(xyz, nh)
    nf = e3b.evolve_causal(sub, nh, init, passes=2)
    Bf = e3b.topological_charge_poisson(xyz, nf)
    ok = abs(Bf - 1.0) < 0.2
    return {"B0": float(B0), "Bf": float(Bf), "ok": bool(ok)}


def kibble_sanity():
    """Defect density drops for slower quenches (basic Kibble-Zurek trend)."""
    fast, slow = [], []
    for sd in range(4):
        nf = f3.quench(16, tau_Q=4, seed=sd)
        ns = f3.quench(16, tau_Q=40, seed=sd)
        fast.append(f3.defect_count(nf)[0])
        slow.append(f3.defect_count(ns)[0])
    ok = np.mean(slow) < np.mean(fast)
    return {"n_def_fast": float(np.mean(fast)), "n_def_slow": float(np.mean(slow)),
            "ok": bool(ok)}


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM3-V GATE -- E1 transition + E3b causal freezing + Kibble sanity")
    print("=" * 72)
    e1 = e1_transition()
    print(f"[E1] m(J): {[round(x,3) for x in e1['m']]} at J={e1['J']}  -> "
          f"{'lifts at J_c' if e1['ok'] else 'FAIL'}")
    e3bf = e3b_freezing()
    print(f"[E3b] causal evolution B: {e3bf['B0']:.3f} -> {e3bf['Bf']:.3f}  -> "
          f"{'frozen (preserved)' if e3bf['ok'] else 'FAIL'}")
    kib = kibble_sanity()
    print(f"[Kibble] n_def fast quench={kib['n_def_fast']:.1f} > slow quench="
          f"{kib['n_def_slow']:.1f}  -> {'trend OK' if kib['ok'] else 'FAIL'}")

    gate = e1["ok"] and e3bf["ok"] and kib["ok"]
    print("-" * 72)
    print(f"GATE: {'PASS -- FM3-1/FM3-2 may proceed' if gate else 'FAIL -- STOP'}")
    print("=" * 72)
    payload = {"gate_pass": bool(gate), "E1": e1, "E3b_freezing": e3bf,
               "kibble_sanity": kib, "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "FM3V_gate.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM3V_gate.json'}")
    return gate


if __name__ == "__main__":
    main()

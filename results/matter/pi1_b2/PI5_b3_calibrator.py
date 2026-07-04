"""PI5 -- FQ2: the SECOND calibrator of pi_1, of KNOWN TRUE CLASS 1.
Pre-registered (FQ2_PI1_B3_CALIBRATOR.md).

THE CALIBRATOR. Axial degree-3 field (tripled azimuth) under the global
target-rotation 2pi loop. True class = B mod 2 = 3 mod 2 = 1 (Williams 1970;
suspension algebra, NO FR input). Preimage = single curve winding the s-circle
3 times (triple cover; the 3 azimuthal strands cyclically permute). Since the
true class is known, the measured class MEASURES the framing anomaly directly:
eps(3) := measured XOR 1.

PRE-REGISTERED PREDICTION: H_lin eps(n)=(n-1) mod 2 => eps(3)=0 => measured=1.
Alternative H_sat eps(n)=[n>=2] => eps(3)=1 => measured=0 (declared, accepted
as alternative-law determination, NOT death). Both keep eps(2)=1, so the PI3
FR correction stands in either case.

MANDATORY GATE (anti-aliasing, runs before any eps reading):
  G1 baryon number converges monotonically toward 3 over N in {37,49,61,73}.
  G2 preimage is one component of winding 3, for all 3 regular values.
  G3 measured class identical across the 3 regular values.
  G4 measured class identical at N=49 and N=61 (refine to 73 if not).

MACHINERY DEATH (no eps verdict; casts doubt on PI3): the gate fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc
from pi1_core import s2

L = 16.0
N_BARYON = [37, 49, 61, 73]
N_CLASS = [49, 61]          # refine to 73 only if G4 fails
NS = 48


def classify_with_winding(Vfield, label=""):
    """Class for the 3 pre-registered regular values PLUS per-component s-winding
    (mirrors pc.z2_class with the same jitter, adding preimage_windings)."""
    results = []
    for y in pc.REGULAR_VALUES:
        rng = np.random.default_rng(421)
        Vj = Vfield + pc.JITTER * rng.standard_normal(Vfield.shape)
        fb = []
        for e in np.eye(4):
            v = e - (e @ y) * y
            for u in fb:
                v = v - (v @ u) * u
            nrm = np.linalg.norm(v)
            if nrm > 1e-6:
                fb.append(v / nrm)
            if len(fb) == 3:
                break
        fbasis = np.column_stack(fb)
        ns = Vj.shape[0]
        segments, boundary = pc.extract_preimage(Vj, y)
        comps, all_closed = pc.chain_components(segments, ns)
        windings = pc.preimage_windings(segments, ns)
        parities, dots, fail = [], [], None
        for c in comps:
            p, info = pc.component_parity(segments, c, y, fbasis)
            if p is None:
                fail = info
                break
            parities.append(p)
            dots.append(info)
        ok = all_closed and not boundary and fail is None
        cls = int(sum(parities) % 2) if ok else None
        r = {"class": cls, "n_segments": len(segments),
             "n_components": len(comps), "windings": windings,
             "all_chains_closed": bool(all_closed),
             "boundary_touch": bool(boundary),
             "min_frame_dot": float(min(dots)) if dots else None,
             "frame_dot_ok": bool(dots and min(dots) >= pc.FRAME_DOT_MIN),
             "failure": fail,
             "ok": bool(ok and dots and min(dots) >= pc.FRAME_DOT_MIN)}
        results.append(r)
        print(f"  [{label}] y={np.round(y,2)} class={cls} comps={len(comps)} "
              f"wind={windings} segs={len(segments)} closed={all_closed} "
              f"mindot={None if r['min_frame_dot'] is None else round(r['min_frame_dot'],3)}",
              flush=True)
    classes = [r["class"] for r in results]
    stable = len(set(classes)) == 1 and classes[0] is not None
    # G2: exactly one component of |winding| 3, all regular values. (The sign
    # of the winding is the traversal orientation -- topologically irrelevant;
    # the triple cover is |winding|=3. Two regular values traverse with the
    # opposite orientation, hence -3; magnitude is the invariant.)
    swap3 = all(r["n_components"] == 1 and len(r["windings"]) == 1
                and r["windings"][0] is not None and abs(r["windings"][0]) == 3
                for r in results)
    return {"classes": classes, "stable": bool(stable),
            "value": classes[0] if stable else None,
            "winding3_topology": bool(swap3), "details": results}


def main():
    out = {}

    # ---- G1: baryon-number convergence toward 3 -----------------------------
    print("G1: baryon number convergence (axial B=3, expect -> 3)", flush=True)
    baryon = {}
    for N in N_BARYON:
        X, Y, Z, dx = pc.spatial_grid(L, N)
        b = float(s2.baryon_number(pc.axial_bn(X, Y, Z, 3), dx))
        baryon[N] = b
        print(f"  N={N}  B={b:.4f}", flush=True)
    bvals = [baryon[N] for N in N_BARYON]
    monotone = all(bvals[i + 1] > bvals[i] for i in range(len(bvals) - 1))
    # linear extrapolation in 1/N to the continuum
    invN = np.array([1.0 / N for N in N_BARYON])
    slope, intercept = np.polyfit(invN, bvals, 1)
    extrap = float(intercept)
    g1 = bool(monotone and 2.6 <= extrap <= 3.4 and abs(extrap - 3) < abs(extrap - 2)
              and abs(extrap - 3) < abs(extrap - 4))
    print(f"  monotone={monotone}  1/N->0 extrapolation B={extrap:.3f}  G1={g1}",
          flush=True)
    out["G1_baryon"] = {"values": baryon, "monotone": monotone,
                        "extrapolation": extrap, "pass": g1}

    # ---- class measurement at two resolutions (G2/G3/G4) --------------------
    runs = {}
    for N in N_CLASS:
        print(f"\nclass measurement: axial B=3 target-rotation 2pi loop, N={N} "
              f"(true class 1; predict measured 1 [H_lin])", flush=True)
        X, Y, Z, _ = pc.spatial_grid(L, N)
        loop = pc.loop_target_rotation(pc.axial_bn(X, Y, Z, 3), NS)
        runs[N] = classify_with_winding(loop, f"b3-N{N}")
        del loop

    g2 = all(runs[N]["winding3_topology"] for N in N_CLASS)
    g3 = all(runs[N]["stable"] for N in N_CLASS)
    vals = [runs[N]["value"] for N in N_CLASS]
    g4 = (len(set(vals)) == 1 and vals[0] is not None)
    gate_ok = bool(g1 and g2 and g3 and g4)
    measured = vals[0] if g4 else None
    eps3 = None if measured is None else int(measured ^ 1)
    law = None
    if eps3 is not None:
        law = "H_lin: eps(n)=(n-1) mod 2" if eps3 == 0 else "H_sat: eps(n)=[n>=2]"

    verdict = {
        "true_class": 1,
        "gate": {"G1_baryon": g1, "G2_winding3": g2, "G3_stable": g3,
                 "G4_converged": g4, "all_pass": gate_ok},
        "measured_class": measured,
        "eps_of_3": eps3,
        "selected_law": law,
        "predicted_measured_H_lin": 1,
        "prediction_matched": (None if measured is None else bool(measured == 1)),
        "machinery_death": not gate_ok,
        "fr_correction_status": ("undetermined (machinery death)" if not gate_ok
                                 else "eps(2)=1 stands; PI3 FR correction valid"),
    }
    out["class_runs"] = runs
    out["verdict"] = verdict
    pc.save_json("PI5_b3_calibrator.json", out)
    print("\n" + json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()

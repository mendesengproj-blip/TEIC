"""B4-genuino -- Bianchi-I anisotropy in the CAUSAL ORDER (direction-dependent light
cones): does it open the magnetic 2-cell sector at low curvature?  Stage 0 + Stage 1
(BLOCKING GATES only; per the user's decision, stop at the first verdict).

Pre-registration: docs/campaigns/FOTON_B3B4/PRE_REGISTRO_B4_GENUINO.md.

B4 ORIGINAL died (DEATH_B4_COORD_ARTIFACT): anisotropy in the EMBEDDING (X_k=e^{H_k tau}x_k)
with an ISOTROPIC causal order -- stretching x_1 trivially inflated every bivector plane
containing x_1 (b_plane[12,13] x6e4, b_plane[23] fixed).  A units artefact, not physics.

THE SURGERY (faithful B4): anisotropy enters ONLY the causal ORDER,
    p < q  <=>  dt>0  AND  dt^2 - (a^2 dx_1^2 + dx_2^2 + dx_3^2) > 0      (a dimensionless)
and the E/B classification stays in FLAT isotropic coordinates (the E6c classifier, NO
stretched coordinate).  a=1 reduces to flat Minkowski (gate).  a>1 = narrower light cone
along x_1.  If frac_B rises, it is because anisotropic cones SELECT different plaquettes
(whose flat-space area bivectors are more spacelike), NOT because any area was rescaled.

Two anti-artefact controls in Stage 1 (the B3/B4 discipline):
  * plane control: b_plane[12,13] must NOT explode vs b_plane[23] (no coordinate stretch
    exists here, so a blow-up would mean anisotropy leaked into the classifier -> ARTIFACT).
  * isotropic-order null: SAME points, ISOTROPIC (a=1) order, same flat classifier. The
    genuine effect of the anisotropic order is frac_B(a) - frac_B_iso on identical points.

c, omega, dispersion: NEVER inserted (A1 guard).  `a` is a dimensionless swept knob, not a
physical constant.  Stage 2 (gauge gate, reusing b3b_closure) and Stage 3 (dispersion) run
only if Stage 1 yields a clean candidate.

Run:  python docs/campaigns/FOTON_B3B4/b4_genuino.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
E6 = ROOT / "results" / "gauge" / "e6"
E6B = ROOT / "results" / "gauge" / "e6b"
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
for p in (str(E6B), str(E6), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from e6b_diamond_height_core import polygon_bivectors, height_h_plaquettes   # noqa: E402
from orientation_core import Graph                                           # noqa: E402
from causal_core import sprinkle_box, causal_matrix                         # noqa: E402

RHO = 2.0


def _wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return p, (c - h) / d, (c + h) / d


# ====================================================================== #
# Anisotropic causal order (the only new physics): Bianchi-I light cones
# ====================================================================== #
def causal_matrix_aniso(pts, a):
    """Strict causal order C[i,j]=(i precedes j) with a direction-dependent cone:
        dt>0  and  dt^2 > a^2 dx_1^2 + dx_2^2 + dx_3^2.
    a=1 is byte-identical to causal_core.causal_matrix (flat Minkowski)."""
    pts = np.asarray(pts, dtype=float)
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx = pts[None, :, 1:] - pts[:, None, 1:]
    w = np.ones(dx.shape[-1])
    w[0] = a * a                                   # anisotropy weight on x_1
    dx2 = np.sum((dx ** 2) * w, axis=-1)
    return (dt > 0) & (dt * dt > dx2)


def aniso_link_graph(pts, a, return_relation=False):
    """Hasse link graph (transitive reduction) of the ANISOTROPIC causal order.
    Mirrors orientation_core.causal_link_graph but with causal_matrix_aniso."""
    C = causal_matrix_aniso(pts, a)
    inter = (C.astype(np.float32) @ C.astype(np.float32)) > 0.5
    Lk = C & ~inter
    src, dst = np.nonzero(Lk)
    g = Graph(C.shape[0], np.stack([src, dst], axis=1) if src.size else np.zeros((0, 2), int))
    g.n_links = int(src.size)
    g._attach_directed(src, dst, np.asarray(pts)[:, 0])
    if return_relation:
        return g, C
    return g


def _is_strict_partial_order(C, sub=120):
    """Antisymmetry + transitivity check on a sub-block (cheap O(sub^3) sample)."""
    n = C.shape[0]
    idx = np.arange(min(sub, n))
    Cs = C[np.ix_(idx, idx)]
    antisym = not np.any(Cs & Cs.T)
    irr = not np.any(np.diag(Cs))
    # transitive: if i<j and j<k then i<k
    trans_ok = True
    reach2 = (Cs.astype(np.int8) @ Cs.astype(np.int8)) > 0
    if np.any(reach2 & ~Cs):
        trans_ok = False
    return bool(antisym and irr and trans_ok)


def measure_fracB(pts, a, h, seed, max_plaqs=8000):
    """frac_B and per-plane magnetic content for height-h plaquettes built from the
    anisotropic-order Hasse graph; bivector in FLAT coords (no stretch)."""
    g = aniso_link_graph(pts, a)
    V = height_h_plaquettes(g, h, max_plaqs=max_plaqs, max_sources=g.n,
                            paths_per_source=80, max_pairs_per_pair=4, seed=seed)
    P = int(V.shape[0])
    if P == 0:
        return {"P": 0, "n_B": 0, "frac_B": float("nan"), "b_plane": [float("nan")] * 3,
                "n": int(g.n), "n_links": int(g.n_links)}
    A, e2, b2 = polygon_bivectors(pts, V)          # FLAT classifier (E6c), no rescale
    nB = int(np.sum(b2 > e2))
    sub = A[:, 1:4, 1:4]
    b_plane = [float(np.mean(sub[:, 0, 1] ** 2)),  # 12 (contains x_1)
               float(np.mean(sub[:, 0, 2] ** 2)),  # 13 (contains x_1)
               float(np.mean(sub[:, 1, 2] ** 2))]  # 23 (no x_1)
    return {"P": P, "n_B": nB, "frac_B": nB / P, "b_plane": b_plane,
            "n": int(g.n), "n_links": int(g.n_links)}


def main():
    t0 = time.time()
    print("=" * 78)
    print("B4-genuino -- Bianchi-I in the CAUSAL ORDER: magnetic sector at low curvature?")
    print("            Stage 0 (validated reconstruction) + Stage 1 (frac_B + controls)")
    print("=" * 78)
    H_CELL = 3
    ANISO = [1.0, 2.0, 4.0, 8.0]
    N = 1500
    SEEDS = (1, 2, 3)

    out = {"campaign": "FOTON_B3B4", "experiment": "B4_genuino", "rho": RHO,
           "height": H_CELL, "aniso_grid": ANISO, "N": N,
           "stages_run": "0+1 (blocking; 2/3 not run)"}

    # ---------------- Stage 0: validated reconstruction ----------------
    rng = np.random.default_rng(12345)
    L = (N / RHO) ** 0.25
    pts0 = sprinkle_box(RHO, [(0.0, L)] * 4, rng)
    C_iso_ref = causal_matrix(pts0)
    C_a1 = causal_matrix_aniso(pts0, 1.0)
    a1_identical = bool(np.array_equal(C_iso_ref, C_a1))
    po_ok = all(_is_strict_partial_order(causal_matrix_aniso(pts0, a)) for a in ANISO)
    out["stage0_a1_identical_to_isotropic"] = a1_identical
    out["stage0_partial_order_ok"] = po_ok
    print(f"  [Stage0] a=1 order == isotropic causal_matrix: {a1_identical} | "
          f"strict partial order (all a): {po_ok}", flush=True)

    if not (a1_identical and po_ok):
        out["verdict_tag"] = "INVALID"
        out["verdict"] = ("INVALID: anisotropic order construction failed Stage 0 "
                          f"(a1_identical={a1_identical}, partial_order_ok={po_ok}).")
        _finish(out, t0)
        return 0

    # ---------------- Stage 1: frac_B(a) + plane control + isotropic-order null ----
    rows = []
    for a in ANISO:
        accP = accB = accPn = accBn = 0
        bpl = np.zeros(3)
        bpl_iso = np.zeros(3)
        for seed in SEEDS:
            rng = np.random.default_rng(100 * seed + int(10 * a))
            pts = sprinkle_box(RHO, [(0.0, L)] * 4, rng)
            r = measure_fracB(pts, a, H_CELL, seed)            # anisotropic order
            rn = measure_fracB(pts, 1.0, H_CELL, seed)         # SAME points, isotropic order (null)
            if r["P"] > 0:
                accP += r["P"]; accB += r["n_B"]; bpl += np.array(r["b_plane"])
            if rn["P"] > 0:
                accPn += rn["P"]; accBn += rn["n_B"]; bpl_iso += np.array(rn["b_plane"])
        p, lo, hi = _wilson(accB, accP)
        pn, lon, hin = _wilson(accBn, accPn)
        bpl /= len(SEEDS); bpl_iso /= len(SEEDS)
        rows.append({"aniso": a, "P_tot": accP, "frac_B": p, "wilson_lo": lo, "wilson_hi": hi,
                     "frac_B_iso_null": pn, "null_lo": lon, "null_hi": hin,
                     "b_plane_12_13_23": bpl.tolist(),
                     "b_plane_iso_12_13_23": bpl_iso.tolist()})
        print(f"  a={a:.0f}: frac_B={p:.5f} [{lo:.5f},{hi:.5f}]  "
              f"null(iso)={pn:.5f}  gap={p-pn:+.5f}  "
              f"b_plane(12,13,23)={np.round(bpl,3).tolist()}", flush=True)

    out["rows"] = rows

    # ---------------- verdict ----------------
    gate = rows[0]
    gate_ok = bool(gate["frac_B"] < 0.01)             # a=1 flat must be electric-dominated
    best = max(rows, key=lambda r: r["wilson_lo"])
    fracs = [r["frac_B"] for r in rows]
    gaps = [r["frac_B"] - r["frac_B_iso_null"] for r in rows]
    grows = bool(best["frac_B"] > gate["frac_B"] + 0.002 and best["wilson_lo"] > 0.01)
    # plane control: did stretched planes (12,13) blow up vs unstretched (23)?
    bpl0 = np.array(gate["b_plane_12_13_23"])
    bplb = np.array(best["b_plane_12_13_23"])
    stretched_blowup = float((bplb[:2].mean() + 1e-30) / (bpl0[:2].mean() + 1e-30))
    unstretched_ratio = float((bplb[2] + 1e-30) / (bpl0[2] + 1e-30))
    is_artifact = bool(stretched_blowup > 10.0 and unstretched_ratio < 2.0)
    # genuine effect of the anisotropic order: gap over the isotropic-order null on same pts
    best_gap = best["frac_B"] - best["frac_B_iso_null"]

    if not gate_ok:
        tag = "INVALID"
        verdict = (f"INVALID: isotropic gate a=1 gives frac_B={gate['frac_B']:.4f} (not the "
                   f"flat electric-dominated <0.01); classifier/reconstruction suspect.")
    elif is_artifact:
        tag = "DEATH_B4G_ARTIFACT"
        verdict = (
            f"DEATH (residual coordinate artefact): frac_B rises ({fracs[0]:.4f}->"
            f"{best['frac_B']:.4f}) BUT the stretched planes (12,13) blow up x{stretched_blowup:.0e} "
            f"while plane 23 stays x{unstretched_ratio:.2f} -- anisotropy leaked into the "
            f"classifier despite flat coords. Fix before any claim.")
    elif grows and best_gap > 0.005:
        tag = "STAGE1_CANDIDATE_B4G"
        verdict = (
            f"STAGE 1 CANDIDATE: anisotropic light cones raise frac_B to {best['frac_B']:.4f} "
            f"(Wilson-lo {best['wilson_lo']:.4f}>0.01) at a={best['aniso']:.0f}, with a genuine "
            f"gap {best_gap:+.4f} over the isotropic-order null on the SAME points, and NO plane "
            f"blow-up (stretched x{stretched_blowup:.2f}, unstretched x{unstretched_ratio:.2f}). "
            f"The magnetic sector opens from the ORDER, not a coordinate. Stage 2 (gauge gate, "
            f"reusing b3b_closure on these Hasse plaquettes) is now warranted.")
    else:
        tag = "DEATH_B4_GENUINE"
        verdict = (
            f"DEATH (genuine): anisotropy in the causal ORDER does NOT open the magnetic sector "
            f"at low curvature -- frac_B stays {fracs[0]:.4f}->{best['frac_B']:.4f} (best "
            f"Wilson-lo {best['wilson_lo']:.4f}), and the gap over the isotropic-order null is "
            f"{best_gap:+.4f} (<=0.005). Direction-dependent light cones (true Bianchi-I) do not "
            f"furnish a magnetic photon. Combined with E6c (isotropic curvature) and B3b (future "
            f"cones), the THREE low-curvature levers are exhausted: the magnetic photon stays "
            f"[FRONTEIRA], now a stronger statement. Stages 2/3 NOT run.")

    out["verdict_tag"] = tag
    out["verdict"] = verdict
    out["gate_isotropic_subthreshold"] = gate_ok
    out["stretched_plane_blowup"] = stretched_blowup
    out["unstretched_plane_ratio"] = unstretched_ratio
    out["is_coordinate_artifact"] = is_artifact
    out["best_aniso"] = best["aniso"]
    out["best_frac_B"] = best["frac_B"]
    out["best_gap_over_null"] = best_gap
    _finish(out, t0)
    return 0


def _finish(out, t0):
    out["runtime_s"] = time.time() - t0
    (HERE / "b4_genuino.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"VERDICT [{out['verdict_tag']}]:\n{out['verdict']}")
    print(f"[{out['runtime_s']:.0f}s] -> b4_genuino.json")


if __name__ == "__main__":
    raise SystemExit(main())

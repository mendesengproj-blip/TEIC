"""B4 -- anisotropic de Sitter: does anisotropy open the magnetic sector at LOW curvature?

Campaign FOTON_B3B4 (Fase 2, Frente B, photon critical path).  E6c showed isotropic
spatial curvature opens the magnetic (B-type) 2-cell sector only at PLANCKIAN curvature
(frac_B crosses 0.01 only at R_hat=2; <0.01 at low curvature R_hat>=8).  B4 tests the
other untested lever: does a controlled ANISOTROPY raise frac_B at LOW curvature, and is
there a preferential direction?

CONTROLLED ANISOTROPY (the clean isolation, parallel to E6c's curvature isolation).
E6c isolates curvature by keeping the causal ORDER conformally flat (Minkowski) and
bending only the 5D EMBEDDING used for the E/B bivector split.  B4 does the same with
anisotropy: the causal order stays the isotropic conformal Minkowski order (same diamond
topology at every anisotropy), and the embedding spatial scale factors are made
direction-dependent,
    X_k = e^{H_k tau} x_k ,   H_1 = a * H_perp ,  H_2 = H_3 = H_perp ,
with anisotropy a = H_1/H_perp.  a=1 reduces to E6c isotropic (gate); a>1 stretches the
x_1 embedding direction.  This isolates the single question: does anisotropic bending of
the diamond's embedding (at fixed causal topology) tilt its area bivector toward
spacelike, where isotropic bending (E6c) did not at low curvature?

GATE: a=1 must reproduce E6c isotropic frac_B(R_hat) (same sprinkle/topology/classifier).
Anti-circularity: order is the sprinkling's own; the bivector is real embedding geometry;
no phase inserted.  Under the A1 guard.

Run:  python docs/campaigns/FOTON_B3B4/b4_anisotropic.py
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
E6C = ROOT / "results" / "gauge" / "e6c"
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
for p in (str(E6C), str(E6), str(E6B), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from e6b_diamond_height_core import polygon_bivectors, height_h_plaquettes   # noqa: E402
from orientation_core import causal_link_graph                               # noqa: E402

RHO = 2.0


def _wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return p, (c - h) / d, (c + h) / d


def anisotropic_desitter(N, R_hat, aniso, seed, rho=RHO):
    """Conformal Minkowski order + anisotropic dS embedding.  aniso=a=H_1/H_perp.
    Returns (pts_conf, pts_embed).  R_hat=inf -> flat (aniso has no effect, gate)."""
    rng = np.random.default_rng(seed)
    ell = rho ** -0.25
    L = (N / rho) ** 0.25
    if not np.isfinite(R_hat):
        from causal_core import sprinkle_box
        pts = sprinkle_box(rho, [(0.0, L)] * 4, rng)
        return pts, pts
    R_dS = R_hat * ell
    H = 1.0 / R_dS
    eta_lo = -(1.0 / H)
    eta_hi = -(1.0 / H) * np.exp(-H * L)
    L_eta = eta_hi - eta_lo
    L_x = L_eta
    n = rng.poisson(N)
    eta = rng.uniform(eta_lo, eta_hi, size=n)
    x = rng.uniform(0.0, L_x, size=(n, 3))
    pts_conf = np.column_stack([eta, x])
    tau = -(1.0 / H) * np.log(-H * eta)
    # anisotropic spatial Hubble: H_1 = a H, H_2=H_3=H.  Embedding uses per-axis e^{H_k tau}.
    Hk = np.array([aniso * H, H, H])
    eHt_k = np.exp(np.outer(tau, Hk))                 # (n,3)
    eHt = np.exp(H * tau)                              # time/X0,X4 use the isotropic mean rate
    r2 = np.sum((eHt_k * x) ** 2, axis=1) / np.maximum(eHt ** 2, 1e-300)
    X0 = R_dS * np.sinh(H * tau) + (0.5 / R_dS) * eHt * r2
    Xk = eHt_k * x                                     # (n,3) anisotropic spatial embedding
    X4 = R_dS * np.cosh(H * tau) - (0.5 / R_dS) * eHt * r2
    pts_embed = np.column_stack([X0, Xk, X4])
    return pts_conf, pts_embed


def measure(pc, pe, h, seed, max_plaqs=8000):
    g = causal_link_graph(pc)
    V = height_h_plaquettes(g, h, max_plaqs=max_plaqs, max_sources=g.n,
                            paths_per_source=80, max_pairs_per_pair=4, seed=seed)
    P = int(V.shape[0])
    if P == 0:
        return {"P": 0, "frac_B": float("nan"), "n": int(g.n)}
    A, e2, b2 = polygon_bivectors(pe, V)
    nB = int(np.sum(b2 > e2))
    # preferential direction: magnetic content per spatial plane (12,13,23) of A^{ij}
    sub = A[:, 1:4, 1:4]
    b_plane = [float(np.mean(sub[:, 0, 1] ** 2)),    # 12
               float(np.mean(sub[:, 0, 2] ** 2)),    # 13
               float(np.mean(sub[:, 1, 2] ** 2))]    # 23
    return {"P": P, "n_B": nB, "frac_B": nB / P, "b_plane_12_13_23": b_plane,
            "n": int(g.n)}


def main():
    t0 = time.time()
    print("=" * 78)
    print("B4 -- anisotropic de Sitter: magnetic sector at LOW curvature?")
    print("=" * 78)
    R_LOW = 8.0                         # low curvature (observable-universe regime, R_hat>=8)
    H_CELL = 3                          # E6b/E6c best-sampled height
    ANISO = [1.0, 2.0, 4.0, 8.0]       # a=1 gate (isotropic) -> strong anisotropy
    N = 1500

    rows = []
    for a in ANISO:
        accP, accB = 0, 0
        bpl = np.zeros(3)
        for seed in (1, 2, 3):
            pc, pe = anisotropic_desitter(N, R_LOW, a, seed)
            r = measure(pc, pe, H_CELL, seed)
            if r["P"] > 0:
                accP += r["P"]; accB += r["n_B"]; bpl += np.array(r["b_plane_12_13_23"])
        p, lo, hi = _wilson(accB, accP)
        bpl /= 3.0
        rows.append({"aniso": a, "R_hat": R_LOW, "P_tot": accP, "frac_B": p,
                     "wilson_lo": lo, "wilson_hi": hi,
                     "b_plane_12_13_23": bpl.tolist()})
        print(f"  a={a:.0f} (R_hat={R_LOW}): P={accP:6d} frac_B={p:.5f} [{lo:.5f},{hi:.5f}]  "
              f"b_plane(12,13,23)={np.round(bpl,3).tolist()}", flush=True)

    # gate: a=1 reproduces E6c low-curvature isotropic (~0.003, <0.01)
    gate = rows[0]
    gate_ok = bool(gate["frac_B"] < 0.01)
    fracs = [r["frac_B"] for r in rows]
    grows = bool(fracs[-1] > fracs[0] + 0.002)
    best = max(rows, key=lambda r: r["wilson_lo"])
    # ---- COORDINATE-ARTEFACT CONTROL (decisive) ----
    # Stretching the x_1 embedding axis by e^{(a-1)Htau} trivially inflates every
    # bivector plane that contains x_1 (planes 12,13) while leaving the unstretched
    # plane 23 invariant.  If the magnetic rise is this artefact, b_plane[12,13] blow
    # up by orders of magnitude while b_plane[23] stays fixed -- a units effect, not
    # emergent gauge content.  Quantify it.
    bpl0 = np.array(rows[0]["b_plane_12_13_23"])
    bplb = np.array(best["b_plane_12_13_23"])
    stretched_blowup = float((bplb[:2].mean() + 1e-30) / (bpl0[:2].mean() + 1e-30))
    unstretched_ratio = float((bplb[2] + 1e-30) / (bpl0[2] + 1e-30))
    # artefact signature: stretched planes explode (>10x) while unstretched ~unchanged (<2x)
    is_coord_artifact = bool(stretched_blowup > 10.0 and unstretched_ratio < 2.0)

    if not gate_ok:
        tag = "INVALID"
        verdict = (f"INVALID: isotropic gate a=1 gives frac_B={gate['frac_B']:.4f}, not the "
                   f"E6c sub-threshold low-curvature value; construction suspect.")
    elif is_coord_artifact:
        tag = "DEATH_B4_COORD_ARTIFACT"
        verdict = (
            f"DEATH (coordinate artefact exposed): frac_B does rise with anisotropy "
            f"({fracs[0]:.4f}->{best['frac_B']:.4f}), BUT the control proves it is a "
            f"UNITS/COORDINATE artefact, not physics: the magnetic content in the stretched "
            f"planes (12,13, containing x_1) blows up x{stretched_blowup:.0e} while the "
            f"unstretched plane (23) is unchanged (x{unstretched_ratio:.2f}). This is exactly "
            f"the embedding scale factor e^{{(a-1)Htau}} inflating A^{{1j}} -- rescaling one "
            f"coordinate axis trivially tilts area bivectors toward it. The implementation "
            f"(anisotropic EMBEDDING at fixed isotropic causal ORDER) conflates a coordinate "
            f"stretch with physical anisotropy. A FAITHFUL B4 needs the anisotropy in the "
            f"CAUSAL ORDER itself (direction-dependent light cones, true Bianchi-I), which "
            f"breaks the conformal-flat trick and is a larger campaign. As implemented, "
            f"Direction A does NOT open the magnetic sector; the [FRONTIER] stands.")
    elif grows and best["wilson_lo"] > 0.01:
        tag = "SUCCESS_B4_CANDIDATE"
        verdict = (f"SUCCESS (candidate): anisotropy raises frac_B to {best['frac_B']:.4f} "
                   f"(Wilson-lo {best['wilson_lo']:.4f}>0.01) at low curvature and the rise is "
                   f"NOT a pure coordinate artefact (stretched x{stretched_blowup:.1f}, "
                   f"unstretched x{unstretched_ratio:.1f}). Needs gauge-invariance follow-up.")
    else:
        tag = "DEATH_B4"
        verdict = (f"DEATH: anisotropy does not raise frac_B above 0.01 at low curvature "
                   f"(isotropic {fracs[0]:.4f}, best Wilson-lo {best['wilson_lo']:.4f}). "
                   f"Direction A exhausted; [FRONTIER] stands.")

    out = {"campaign": "FOTON_B3B4", "experiment": "B4_anisotropic", "rho": RHO,
           "R_hat_low": R_LOW, "height": H_CELL, "rows": rows,
           "gate_isotropic_subthreshold": gate_ok, "frac_grows_with_aniso": grows,
           "stretched_plane_blowup": stretched_blowup,
           "unstretched_plane_ratio": unstretched_ratio,
           "is_coordinate_artifact": is_coord_artifact,
           "verdict": verdict, "verdict_tag": tag, "runtime_s": time.time() - t0}
    (HERE / "b4_anisotropic.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"VERDICT [{tag}]:\n{verdict}")
    print(f"[{out['runtime_s']:.0f}s] -> b4_anisotropic.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

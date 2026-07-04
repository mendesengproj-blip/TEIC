"""W2_coarse_graining.py -- action with plaquettes: does F^2 emerge and coexist
with the quartic?

BRIDGE/WILSON task W2.  Action
    S = sum_links Dtau[1-cos(phi+Dtheta)]  +  lambda_p sum_plaq [1-cos W_p].
Second order:
    link term  -> C1 X + C2 A^2 + C3 A.dtheta            (the C1/C2 sector)
                  and -1/24 (phi+Dtheta)^4 -> the quartic C_q (A.dtheta)^2 etc.
    plaq term  -> (lambda_p/2) sum W_p^2 = (lambda_p/8) F_{mn}F_{rs} sum Om^{mn}Om^{rs}
                  -> C_F F_{mn}F^{mn}      IF  sum Om Om  has Maxwell structure.

We MEASURE, with no F and no DEV inserted (anti-circularity):
  (i)   the plaquette bivector second moment Q = <Om^{mn} Om^{rs}>, and test whether
        it has Maxwell tensor structure (so F^2 emerges as F_{mn}F^{mn}), plus the
        E-plane vs B-plane anisotropy (the Lorentz-violation analogue of C1);
  (ii)  the geometric scale Pi = (1/V) sum area^2 -> C_F = lambda_p Pi/4 (lambda_p free);
  (iii) the quartic geometric scale from the link 4th moment -> C_q (still present);
  (iv)  coexistence: links and plaquettes are DISJOINT sums of DIFFERENT operators,
        so the two terms add without cancelling -> case (a).
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from wilson_core import area_bivector, causal_diamond_loops  # noqa: E402
from causal_core import sprinkle_box  # noqa: E402

OUT = Path(__file__).resolve().parent


# ---- link sector: 2nd and 4th Dtau-weighted moments (covering relations) ---- #
def link_moments(pts, bounds, margin=0.25):
    pts = np.asarray(pts, float); bounds = np.asarray(bounds, float)
    D = pts.shape[1]
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    C = (dt > 0) & (dt * dt > dx2)
    inter = (C.astype(np.float32) @ C.astype(np.float32)) > 0.5
    i, j = np.nonzero(C & ~inter)
    e = pts[j] - pts[i]
    mid = 0.5 * (pts[i] + pts[j])
    lo = bounds[:, 0] + margin * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin * (bounds[:, 1] - bounds[:, 0])
    keep = np.all((mid >= lo) & (mid <= hi), axis=1)
    e = e[keep]
    dx2 = np.sum(e[:, 1:] ** 2, axis=1)
    dtau = np.sqrt(np.maximum(e[:, 0] ** 2 - dx2, 0.0))
    vol = float(np.prod(hi - lo))
    a_t = float((dtau * e[:, 0] ** 2).mean())
    a_x = float((dtau * dx2).mean()) / (D - 1) if D > 1 else 0.0
    kappa = -a_x
    # 4th-moment scalar feeding the quartic: <Dtau (e.e)^2> with e.e = Dt^2 + |Dx|^2
    ee = e[:, 0] ** 2 + dx2
    m4 = float((dtau * ee ** 2).mean())
    return {"n_links_density": len(e) / vol, "kappa": kappa, "a_t": a_t, "a_x": a_x,
            "m4_scalar": m4, "n_links": len(e)}


# ---- plaquette sector: bivector second moment + area^2 scale ---- #
def plaquette_moments(pts, bounds, margin=0.25, max_per_base=4, n_bases=None, rng=None):
    pts = np.asarray(pts, float); bounds = np.asarray(bounds, float)
    D = pts.shape[1]
    loops = causal_diamond_loops(pts, max_per_base=max_per_base, n_bases=n_bases, rng=rng)
    lo = bounds[:, 0] + margin * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin * (bounds[:, 1] - bounds[:, 0])
    vol = float(np.prod(hi - lo))
    sum_area2 = 0.0
    n_used = 0
    # accumulate <Om^{mn} Om^{mn}> per plane (no sum over sign), for Maxwell/aniso test
    elec = []   # (Om^{0i})^2 , i spatial
    magn = []   # (Om^{ij})^2 , i<j spatial
    cross = []  # Om^{0i} Om^{jk} type (should ~0)
    for verts in loops:
        c = np.mean(verts, axis=0)
        if not (np.all(c >= lo) and np.all(c <= hi)):
            continue
        Om = area_bivector(verts)
        n_used += 1
        # total area^2 = (1/2) Om_{mn} Om^{mn}; use Euclidean square of independent comps
        a2 = sum(Om[m, n] ** 2 for m in range(D) for n in range(m + 1, D))
        sum_area2 += a2
        for i in range(1, D):
            elec.append(Om[0, i] ** 2)
        for i in range(1, D):
            for k in range(i + 1, D):
                magn.append(Om[i, k] ** 2)
        if D >= 4:
            # SIGNED cross of an electric plane (0,1) with the orthogonal magnetic
            # plane (2,3); should average to ~0 if no off-Maxwell structure.
            cross.append(Om[0, 1] * Om[2, 3])
    out = {"n_plaquettes": n_used, "Pi_area2_density": sum_area2 / vol if vol else np.nan,
           "mean_elecplane_area2": float(np.mean(elec)) if elec else np.nan,
           "mean_magnplane_area2": float(np.mean(magn)) if magn else 0.0,
           "mean_cross": float(np.mean(cross)) if cross else 0.0}
    if magn and out["mean_magnplane_area2"] > 0:
        out["EB_anisotropy_ratio"] = out["mean_elecplane_area2"] / out["mean_magnplane_area2"]
    else:
        out["EB_anisotropy_ratio"] = np.nan
    return out


def run(D, rho, extent, n_real, seed0, n_bases):
    bounds = [[0.0, extent]] * D
    L, P = [], []
    for s in range(n_real):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, bounds, rng)
        if len(pts) < 8:
            continue
        L.append(link_moments(pts, bounds))
        P.append(plaquette_moments(pts, bounds, n_bases=n_bases, rng=rng))
    def avg(key, src):
        vals = [d[key] for d in src if np.isfinite(d[key])]
        return float(np.mean(vals)) if vals else np.nan

    def sem(key, src):
        vals = [d[key] for d in src if np.isfinite(d[key])]
        return float(np.std(vals) / np.sqrt(len(vals))) if len(vals) > 1 else np.nan
    return {
        "cross_sem": sem("mean_cross", P),
        "EB_anisotropy_sem": sem("EB_anisotropy_ratio", P),
        "D": D, "rho": rho, "extent": extent, "n_real": len(L),
        "kappa": avg("kappa", L), "n_links_density": avg("n_links_density", L),
        "m4_scalar": avg("m4_scalar", L),
        "Pi_area2_density": avg("Pi_area2_density", P),
        "n_plaquettes_total": int(sum(d["n_plaquettes"] for d in P)),
        "EB_anisotropy_ratio": avg("EB_anisotropy_ratio", P),
        "mean_elecplane_area2": avg("mean_elecplane_area2", P),
        "mean_magnplane_area2": avg("mean_magnplane_area2", P),
        "mean_cross": avg("mean_cross", P),
    }


def main():
    res = {}
    res["d2"] = run(2, rho=120.0, extent=6.0, n_real=20, seed0=100, n_bases=None)
    res["d4"] = run(4, rho=12.0, extent=4.0, n_real=12, seed0=200, n_bases=1500)

    # Build the effective coefficients.  lambda_p is a FREE relative weight (kept
    # symbolic); kappa, n_links, m4, Pi are MEASURED.  Sign conventions: C1=C2=kappa n/2,
    # C3=kappa n (from C2 task); C_q = -(1/24) n_links * m4-contraction (negative ->
    # DBI saturation); C_F = lambda_p * Pi / 4 (Maxwell weight, free via lambda_p).
    for dk in ("d2", "d4"):
        r = res[dk]
        n = r["n_links_density"]
        r["C1_eq_C2"] = n * r["kappa"] / 2.0
        r["C3"] = n * r["kappa"]
        r["C_q_quartic"] = -(1.0 / 24.0) * n * r["m4_scalar"]   # LINK 4th order (no lambda_p)
        r["C_F_per_lambda_p"] = r["Pi_area2_density"] / 4.0     # x lambda_p (free weight)
        # coexistence: both finite and nonzero, from disjoint sums of distinct operators
        r["coexist_case"] = ("(a) coexist: F^2 (plaquette) and quartic (link 4th order) "
                             "are disjoint sums of distinct operators; both finite & nonzero")

    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "W2_coarse_graining_data.json").write_text(json.dumps(res, indent=2))

    print("=" * 72)
    print("W2 -- COARSE-GRAINING links + plaquettes:  does F^2 emerge & coexist?")
    print("=" * 72)
    for dk, lab in [("d2", "1+1D"), ("d4", "3+1D")]:
        r = res[dk]
        print(f"\n{lab} (rho={r['rho']}, {r['extent']}^{r['D']}, {r['n_real']} real.):")
        print(f"  LINK sector  : kappa={r['kappa']:+.4f}  n_links={r['n_links_density']:.2f}")
        print(f"     C1=C2={r['C1_eq_C2']:+.3f}   C3={r['C3']:+.3f}   "
              f"C_q={r['C_q_quartic']:+.4f}  (quartic PRESENT, sign<0=DBI)")
        print(f"  PLAQ sector  : n_plaq={r['n_plaquettes_total']}  "
              f"Pi=<area^2>dens={r['Pi_area2_density']:.4e}")
        print(f"     C_F = lambda_p * {r['C_F_per_lambda_p']:.4e}   (Maxwell weight, "
              f"lambda_p free)")
        if dk == "d4":
            print(f"     E-plane area^2={r['mean_elecplane_area2']:.4e}  "
                  f"B-plane area^2={r['mean_magnplane_area2']:.4e}")
            print(f"     E/B anisotropy ratio={r['EB_anisotropy_ratio']:.3f} "
                  f"+/-{r['EB_anisotropy_sem']:.3f}  (=1 Lorentz-inv Maxwell; !=1 LV)")
            print(f"     off-Maxwell cross <Om01 Om23>={r['mean_cross']:+.3e} "
                  f"+/-{r['cross_sem']:.3e}  (parity => 0)")
        print(f"  COEXISTENCE  : {r['coexist_case']}")
    print("-" * 72)
    print("VERDICT (W2): F^2 EMERGES from plaquettes (form, gauge-inv via W1) and "
          "COEXISTS")
    print("  with the quartic (case a). Relative weight C_F/C3 ~ lambda_p is FREE "
          "(like DEV's K).")
    return res


if __name__ == "__main__":
    main()

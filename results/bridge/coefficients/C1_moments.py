"""C1_moments.py -- Poisson averages over causal LINKS for the minimal action.

BRIDGE / COEFFICIENTS investigation (BRIDGE_COEFFICIENTS.md).  Independent of
R1-R3 and e6-e11; modifies nothing in the main pipeline.  Continues the bridge
(P1-P3 kinematics, D1-D3 dynamics, NL1-NL3 non-linear).

The conjecture under test is the one-line microscopic action

    S = sum_links  Dtau_ij * [ 1 - cos( phi_ij + Dtheta_ij ) ] ,

    Dtau_ij = sqrt(Dt^2 - |Dx|^2)   proper time of the link (causal geometry),
    phi_ij  = A_mu e^mu             gauge (Wilson) phase of the link,
    Dtheta_ij = (d_mu theta) e^mu   nodal-field difference along the link,
    e^mu = q - p = (Dt, Dx)         the link coordinate vector.

Second order, 1 - cos(u) ~ u^2/2 with u = (A_mu + d_mu theta) e^mu, coarse-grains
to

    S_eff = (1/2) * n_links * INT d^Dx  (A_mu + d_mu theta)(A_nu + d_nu theta)
                                          * <Dtau e^mu e^nu> .

So EVERYTHING in the quadratic sector is set by ONE tensor average,

    M2^{mu nu}  =  < Dtau e^mu e^nu >          (Dtau-weighted second moment),

plus the link density n_links.  C1's job is to MEASURE M2 (and the 1st and 3rd
moments) numerically from a Poisson sprinkling, with NO relativistic formula and
NO fit, and to decompose

    M2^{mu nu}  =  kappa * g^{mu nu}  +  lambda * u^mu u^nu        (u = time dir),

i.e. an isotropic (Lorentz-invariant) part kappa and an anisotropic (arrow-of-
time / Lorentz-violating) part lambda.  kappa is what feeds C1, C2, C3; lambda is
the effective Lorentz violation, which R1 says should be small.

ANTI-CIRCULARITY.  Nothing here uses sqrt(1-beta^2), a metric dilation factor, GM/r,
or any DEV coefficient.  The only inputs are bare Minkowski light cones (interval2)
and Poisson sprinkling, both already in src/causal_core.py.  The DEV enters only in
C2/C4, in clearly marked COMPARISON blocks.

"Links L0 (sem intermediarios)" = covering relations: p < q with no event z such
that p < z < q (the Hasse-diagram links).  These are the irreducible causal links
the action sums over.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from causal_core import sprinkle_box  # noqa: E402  (generator primitive, no SR/GR)

OUT = Path(__file__).resolve().parent


# --------------------------------------------------------------------------- #
# Covering relations (causal links without intermediaries) for a small set
# --------------------------------------------------------------------------- #
def causal_links(pts):
    """Return (i, j) index arrays of covering relations p_i < p_j (no intermediate).

    Bare Minkowski cones only: i < j iff Dt>0 and Dt^2 > |Dx|^2.  A relation is a
    LINK iff there is no k with i < k < j.  O(n^2) memory, O(n^3) via one BLAS
    matmul for the intermediate test -- intended for n up to a few thousand.
    """
    pts = np.asarray(pts, dtype=float)
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    C = (dt > 0) & (dt * dt > dx2)                      # strict causal order
    # intermediate[i, j] = exists k with C[i,k] and C[k,j]  (boolean via BLAS)
    inter = (C.astype(np.float32) @ C.astype(np.float32)) > 0.5
    L = C & ~inter                                     # covering relations
    i, j = np.nonzero(L)
    return i, j


def link_moments(pts, bounds, margin_frac=0.25):
    """Dtau-weighted moments of link vectors e^mu = p_j - p_i over BULK links.

    A link counts if its midpoint lies in the inner box (each face pulled in by
    margin_frac of the extent) so the link distribution is the box-cutoff one, not
    a boundary-truncated one.  Returns a dict of raw moment tensors and counts.
    """
    pts = np.asarray(pts, dtype=float)
    bounds = np.asarray(bounds, dtype=float)
    D = pts.shape[1]
    i, j = causal_links(pts)
    e = pts[j] - pts[i]                                 # (L, D) link vectors, Dt>0
    dt = e[:, 0]
    dx2 = np.sum(e[:, 1:] ** 2, axis=1)
    dtau = np.sqrt(np.maximum(dt * dt - dx2, 0.0))      # proper time of the link
    mid = 0.5 * (pts[i] + pts[j])
    lo = bounds[:, 0] + margin_frac * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin_frac * (bounds[:, 1] - bounds[:, 0])
    keep = np.all((mid >= lo) & (mid <= hi), axis=1)
    e, dtau = e[keep], dtau[keep]
    dx2 = np.sum(e[:, 1:] ** 2, axis=1) if D > 1 else np.zeros(len(e))
    inner_vol = float(np.prod(hi - lo))

    w = dtau                                            # the action weight
    m0 = float(w.mean()) if len(w) else np.nan         # <Dtau>
    # second moment tensor M2^{mu nu} = <Dtau e^mu e^nu>
    M2 = (w[:, None, None] * e[:, :, None] * e[:, None, :]).mean(axis=0)
    # third moment, fully temporal component and time-space components (asymmetry)
    m3_ttt = float((w * e[:, 0] ** 3).mean())
    m3_txx = float((w * e[:, 0] * dx2).mean()) if D > 1 else np.nan
    m3_xxx = float((w * e[:, 1] ** 3).mean()) if D > 1 else np.nan  # ~0 by isotropy
    return {
        "n_links_bulk": int(len(e)),
        "inner_vol": inner_vol,
        "n_links_density": float(len(e) / inner_vol),
        "mean_dtau": m0,
        "M2": M2.tolist(),
        "m3_ttt": m3_ttt,
        "m3_txx": m3_txx,
        "m3_xxx": m3_xxx,
        "dtau_samples": dtau,   # kept in-memory only (not serialised)
    }


def decompose_M2(M2):
    """Split M2^{mu nu} = a_t (time-time) + a_x (space-space, isotropic) into the
    covariant form kappa g^{mu nu} + lambda u^mu u^nu, signature (+,-,...,-).

    With g^{mu nu}=diag(1,-1,..,-1), u^mu=(1,0,..):
        M2^{00}=a_t=kappa+lambda ,   M2^{ii}=a_x=-kappa  (per spatial dim)
    =>  kappa = -a_x ,  lambda = a_t + a_x .
    The Lorentz-invariant magnitude is |kappa|=a_x; the LV part is lambda; the
    anisotropy ratio reported is lambda/|kappa| = (a_t+a_x)/a_x.
    """
    M2 = np.asarray(M2, dtype=float)
    D = M2.shape[0]
    a_t = float(M2[0, 0])
    a_x = float(np.mean([M2[k, k] for k in range(1, D)])) if D > 1 else np.nan
    offdiag = float(np.max(np.abs(M2 - np.diag(np.diag(M2)))))
    kappa = -a_x
    lam = a_t + a_x
    return {
        "a_t_time_time": a_t,
        "a_x_space_space": a_x,
        "max_offdiagonal": offdiag,
        "kappa_isotropic": kappa,
        "lambda_anisotropic": lam,
        "anisotropy_ratio_lambda_over_abskappa": float(lam / abs(kappa)) if a_x else np.nan,
        "a_t_over_a_x": float(a_t / a_x) if a_x else np.nan,
    }


# --------------------------------------------------------------------------- #
# Drivers
# --------------------------------------------------------------------------- #
def run_dimension(D, rho, extents, n_real, seed0, label):
    """Average link moments over n_real Poisson sprinkles in a D-dim box."""
    bounds = [[0.0, ext] for ext in extents]
    accM2, accm0, accm3 = [], [], {"ttt": [], "txx": [], "xxx": []}
    ndens, nlinks = [], []
    dtau_all = []
    for s in range(n_real):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, bounds, rng)
        if len(pts) < 5:
            continue
        m = link_moments(pts, bounds)
        if m["n_links_bulk"] < 5:
            continue
        accM2.append(np.asarray(m["M2"]))
        accm0.append(m["mean_dtau"])
        accm3["ttt"].append(m["m3_ttt"])
        accm3["txx"].append(m["m3_txx"])
        accm3["xxx"].append(m["m3_xxx"])
        ndens.append(m["n_links_density"])
        nlinks.append(m["n_links_bulk"])
        dtau_all.append(m["dtau_samples"])
    M2 = np.mean(accM2, axis=0)
    dec = decompose_M2(M2)
    dtau_all = np.concatenate(dtau_all) if dtau_all else np.array([])
    return {
        "label": label,
        "D": D,
        "rho": rho,
        "extents": list(extents),
        "n_realisations_used": len(accM2),
        "total_bulk_links": int(np.sum(nlinks)),
        "mean_dtau": float(np.mean(accm0)),
        "n_links_density": float(np.mean(ndens)),
        "M2": M2.tolist(),
        "m3_ttt": float(np.mean(accm3["ttt"])),
        "m3_txx": float(np.nanmean(accm3["txx"])),
        "m3_xxx": float(np.nanmean(accm3["xxx"])),
        "decomposition": dec,
        "dtau_p05": float(np.percentile(dtau_all, 5)) if len(dtau_all) else np.nan,
        "dtau_p50": float(np.percentile(dtau_all, 50)) if len(dtau_all) else np.nan,
    }


def main():
    results = {}

    # ---- 1+1D: main measurement + box-size (IR-cutoff) scan -----------------
    # Fixed density; vary the spatial extent to expose whether the anisotropy
    # lambda is a finite physical number or a cutoff-dependent (Lorentz-violating)
    # artefact of the link non-locality.
    d2_main = run_dimension(2, rho=60.0, extents=(5.0, 5.0), n_real=60,
                            seed0=1000, label="1+1D main (rho=60, 5x5)")
    results["d2_main"] = d2_main

    scan = []
    for X in (3.0, 5.0, 8.0, 12.0, 16.0):
        r = run_dimension(2, rho=40.0, extents=(5.0, X), n_real=20,
                          seed0=2000, label=f"1+1D scan T=5 X={X}")
        scan.append({"X": X,
                     "a_t_over_a_x": r["decomposition"]["a_t_over_a_x"],
                     "anisotropy": r["decomposition"]["anisotropy_ratio_lambda_over_abskappa"],
                     "n_links_density": r["n_links_density"]})
    results["d2_boxsize_scan"] = scan

    # ---- 3+1D: the physical case -------------------------------------------
    d4_main = run_dimension(4, rho=10.0, extents=(4.0, 4.0, 4.0, 4.0), n_real=30,
                            seed0=3000, label="3+1D main (rho=10, 4^4)")
    results["d4_main"] = d4_main

    results["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "C1_moments_data.json").write_text(json.dumps(results, indent=2))

    # ---- report ------------------------------------------------------------
    def show(r):
        d = r["decomposition"]
        print(f"\n{r['label']}")
        print(f"  realisations used      : {r['n_realisations_used']}  "
              f"(total bulk links {r['total_bulk_links']})")
        print(f"  <Dtau>                 : {r['mean_dtau']:.4f}")
        print(f"  n_links density        : {r['n_links_density']:.3f}")
        print(f"  M2 = <Dtau e e> tensor :")
        for row in r["M2"]:
            print("      [" + "  ".join(f"{v:+.4f}" for v in row) + "]")
        print(f"  a_t=<Dtau Dt^2>        : {d['a_t_time_time']:+.4f}")
        print(f"  a_x=<Dtau Dx^2>        : {d['a_x_space_space']:+.4f}")
        print(f"  off-diagonal (max|.|)  : {d['max_offdiagonal']:.4e}  (isotropy check)")
        print(f"  kappa (isotropic)      : {d['kappa_isotropic']:+.4f}")
        print(f"  lambda (anisotropic)   : {d['lambda_anisotropic']:+.4f}")
        print(f"  anisotropy lambda/|k|  : {d['anisotropy_ratio_lambda_over_abskappa']:.3f}")
        print(f"  a_t/a_x                : {d['a_t_over_a_x']:.3f}")
        print(f"  3rd moment <Dtau Dt^3> : {r['m3_ttt']:+.4f}  (arrow-of-time skew)")
        print(f"           <Dtau Dt Dx^2>: {r['m3_txx']:+.4f}")
        print(f"           <Dtau Dx^3>   : {r['m3_xxx']:+.4f}  (~0 by spatial isotropy)")

    print("=" * 72)
    print("C1 -- POISSON LINK MOMENTS  M2 = <Dtau e^mu e^nu>  (no fit, no SR/GR)")
    print("=" * 72)
    show(d2_main)
    show(d4_main)
    print("\n1+1D box-size (IR-cutoff) scan  [fixed rho, T=8, growing X]:")
    print("   X     a_t/a_x   lambda/|kappa|   n_link_dens")
    for s in scan:
        print(f"  {s['X']:4.1f}   {s['a_t_over_a_x']:6.3f}   "
              f"{s['anisotropy']:10.3f}    {s['n_links_density']:8.3f}")
    print("\n(written C1_moments_data.json)")
    return results


if __name__ == "__main__":
    main()

"""T3D1 -- the genuinely 3+1D causal network: consistency gate for CR_3D.

Five checks, each a hard gate for the rest of the campaign:

  (1) DIMENSION.  Poisson-sprinkle a 4D causal diamond, count causally-related
      pairs, invert the Myrheim-Meyer ordering fraction -> d.  Must give d~4 (and,
      as a control, d~2 for a 2D sprinkle).  Convergence is checked over
      N ~ 500..few-thousand events.
  (2) VOLUME LAW (cross-check).  <N>(tau) ~ tau^p with p~4 (the R2 estimator), an
      independent confirmation of d=4 by counting alone.
  (3) CAUSALITY.  Every causal link is future-pointing and time-like (dt>0,
      dt^2 > |dx|^2) -- no acausal link.
  (4) THETA-PURE REDUCTION.  With the gauge field off (phi=0) and a weak scalar, the
      lattice force_theta reduces to the discrete 3D Laplacian = D3's Poisson
      operator (the static weak-field limit grad^2 theta = J).
  (5) TRIVIAL GAUGE.  W_p = 0 on every plaquette for a pure-gauge / cold config.

VERDICT: SIM only if all five pass.

Anti-circularity: dimension and causality come from COUNTING causal relations of the
bare Minkowski light cone (causal_core); no relativistic dilation, no complex number.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cr3d_core as c   # noqa: E402

SEED = 31400
N_TARGETS = [500, 1000, 2000, 4000]   # convergence ladder (interior-event counts)


# --------------------------------------------------------------------------- #
def _rho_for_N(Ntarget, T, d):
    """Density so the diamond holds ~Ntarget interior events.  Diamond volume:
    d=2 -> tau^2/2, d=4 -> pi tau^4/24."""
    vol = 0.5 * T ** 2 if d == 2 else (np.pi / 24.0) * T ** 4
    return Ntarget / vol


def check_dimension(rng):
    """MM dimension vs interior-event count, for a 4D sprinkle (and a 2D control)."""
    out = {"d4": [], "d2": []}
    T4, T2 = 5.0, 7.0
    n_real = 24
    for Nt in N_TARGETS:
        rho4 = _rho_for_N(Nt, T4, 4)
        fs, ns = [], []
        for _ in range(n_real):
            pts = c.sprinkle_diamond_4d(rho4, T4, rng)
            if len(pts) >= 2:
                fs.append(c.ordering_fraction(pts)); ns.append(len(pts))
        f = float(np.mean(fs))
        out["d4"].append({"N_target": Nt, "N_mean": float(np.mean(ns)),
                          "f": f, "d_MM": c.mm_dimension(f)})
    # 2D control at the largest N
    rho2 = _rho_for_N(N_TARGETS[-1], T2, 2)
    fs2 = []
    for _ in range(n_real):
        bounds = [(0.0, T2), (-T2 / 2, T2 / 2)]
        pts = c.cc.sprinkle_box(rho2, bounds, rng)
        A = np.zeros(2); B = np.array([T2, 0.0])
        keep = c.cc.alexandrov_interval(pts, A, B)
        if len(keep) >= 2:
            fs2.append(c.ordering_fraction(pts[keep]))
    f2 = float(np.mean(fs2))
    out["d2"].append({"N_target": N_TARGETS[-1], "f": f2, "d_MM": c.mm_dimension(f2)})
    return out


def check_volume_law(rng):
    """<N>(tau) ~ C tau^p; fit p (should be 4 in 3+1D)."""
    rho, taus = 8.0, np.linspace(2.5, 5.0, 8)
    counts = []
    for T in taus:
        ns = [len(c.sprinkle_diamond_4d(rho, T, rng)) for _ in range(40)]
        counts.append(np.mean(ns))
    counts = np.array(counts)
    p, logC = np.polyfit(np.log(taus), np.log(counts), 1)
    return {"exponent": float(p), "coef": float(np.exp(logC)),
            "taus": taus.tolist(), "counts": counts.tolist()}


def check_causality(rng):
    """Sample causal links and verify each is future-pointing and time-like."""
    pts = c.sprinkle_diamond_4d(6.0, 4.0, rng)
    C = c.cc.causal_matrix(pts)              # C[i,j] = i precedes j
    ii, jj = np.nonzero(C)
    dt = pts[jj, 0] - pts[ii, 0]
    ds2 = dt ** 2 - np.sum((pts[jj, 1:] - pts[ii, 1:]) ** 2, axis=1)
    n_links = len(ii)
    bad_future = int(np.sum(dt <= 0))
    bad_timelike = int(np.sum(ds2 <= 0))
    return {"n_links": int(n_links), "acausal_past": bad_future,
            "acausal_spacelike": bad_timelike,
            "ok": bad_future == 0 and bad_timelike == 0}


def check_theta_reduction():
    """phi=0, weak theta: force_theta == discrete 3D Laplacian / dx^2 (the D3 Poisson
    operator).  Compares the cos-force sin(Dtheta)~Dtheta linearisation."""
    x, y, z, dx = c.make_grid(Lx=20.0, Nx=41, Ny=8, Nz=8)
    rng = np.random.default_rng(7)
    theta = 1e-3 * rng.standard_normal((len(x), len(y), len(z)))
    theta[0] = 0.0; theta[-1] = 0.0
    zero = np.zeros_like(theta)
    f = c.force_theta(theta, zero, zero, zero, dx)
    # discrete 3D Laplacian (x interior Dirichlet, y,z periodic), /dx^2 as in force
    lap = np.zeros_like(theta)
    lap[1:-1] = (theta[2:] - 2 * theta[1:-1] + theta[:-2])
    lap += (c._up_y(theta) - 2 * theta + c._dn_y(theta))
    lap += (c._up_z(theta) - 2 * theta + c._dn_z(theta))
    lap[0] = 0.0; lap[-1] = 0.0
    lap = lap / dx ** 2
    rel = float(np.max(np.abs(f - lap)) / (np.max(np.abs(lap)) + 1e-30))
    return {"max_rel_diff": rel, "ok": rel < 1e-3}


def check_trivial_gauge():
    """Cold / pure-gauge config -> all plaquettes 0 and zero magnetic activity."""
    x, y, z, dx = c.make_grid(Lx=16.0, Nx=33, Ny=8, Nz=8)
    rng = np.random.default_rng(3)
    # pure gauge: phi = wrapped lattice gradient of an arbitrary scalar -> W_p == 0
    lam = rng.standard_normal((len(x), len(y), len(z)))
    phix = np.zeros_like(lam); phiy = np.zeros_like(lam); phiz = np.zeros_like(lam)
    phix[:-1] = c._wrap(np.diff(lam, axis=0))
    phiy[:] = c._wrap(c._up_y(lam) - lam)
    phiz[:] = c._wrap(c._up_z(lam) - lam)
    flux = c.wilson_flux(phix, phiy, phiz)
    cold = c.wilson_flux(*[np.zeros_like(lam)] * 3)
    return {"pure_gauge_flux": float(flux), "cold_flux": float(cold),
            "ok": flux < 1e-9 and cold < 1e-30}


def main():
    rng = np.random.default_rng(SEED)
    dim = check_dimension(rng)
    vol = check_volume_law(rng)
    cau = check_causality(rng)
    thr = check_theta_reduction()
    trg = check_trivial_gauge()

    d4_last = dim["d4"][-1]["d_MM"]
    d2_ctrl = dim["d2"][-1]["d_MM"]
    ok_dim = abs(d4_last - 4.0) < 0.1 and abs(d2_ctrl - 2.0) < 0.1
    ok_vol = abs(vol["exponent"] - 4.0) < 0.15
    checks = {"dimension_d4": ok_dim, "volume_p4": ok_vol,
              "causality": cau["ok"], "theta_reduction": thr["ok"],
              "trivial_gauge": trg["ok"]}
    verdict = "SIM" if all(checks.values()) else "PARCIAL"

    payload = {"seed": SEED, "dimension": dim, "volume": vol, "causality": cau,
               "theta_reduction": thr, "trivial_gauge": trg,
               "checks": checks, "verdict": verdict}
    c.save_json("T3D1_network", payload)

    print("=" * 70)
    print("T3D1 -- 3+1D CAUSAL NETWORK")
    print("=" * 70)
    print("Myrheim-Meyer dimension vs event count (4D sprinkle):")
    for r in dim["d4"]:
        print(f"  N={r['N_mean']:6.0f}: f={r['f']:.4f}  d_MM={r['d_MM']:.3f}")
    print(f"  2D control: d_MM={d2_ctrl:.3f} (expect 2)")
    print(f"Volume law: <N> ~ tau^{vol['exponent']:.3f} (expect 4)")
    print(f"Causality: {cau['n_links']} links, "
          f"{cau['acausal_past']} acausal-past, "
          f"{cau['acausal_spacelike']} spacelike (expect 0,0)")
    print(f"theta-pure -> 3D Laplacian: max rel diff {thr['max_rel_diff']:.2e}")
    print(f"Trivial/pure gauge flux: {trg['pure_gauge_flux']:.2e} (expect 0)")
    print("-" * 70)
    print(f"VERDICT: {verdict}  {checks}")
    return payload


if __name__ == "__main__":
    main()

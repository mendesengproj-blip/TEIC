"""DS1 -- emergent gravitational profile vs spatial dimension d.

Poisson-sprinkled points in a d-ball, graph Laplacian L = D - A (neighbours
within r_c, mean degree ~ deg_target), point source at the centre with exact
finite-box compensation (sum J = 0), relax L theta = J (conjugate gradient,
no ansatz, no Green function anywhere in the generator).

The profile theta(r) is then binned and fitted OUTSIDE the generator
(analysis block) against two models: power law A r^p + C and log A ln r + C.

Pre-registered (DIMENSION_SCAN.md): d=1 linear (p=+1), d=2 log wins,
d=3 p=-1, d=4 p=-2.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse
from scipy.optimize import curve_fit
from scipy.sparse.linalg import cg
from scipy.spatial import cKDTree

OUT = Path(__file__).resolve().parent

# (d, N, target mean degree)
CASES = [(1, 4000, 24), (2, 20000, 12), (3, 40000, 14), (4, 100000, 12)]
N_SEEDS = 10
R_BALL = 1.0
FIT_HI = 0.6          # avoid boundary
N_BINS = 26


def sprinkle_ball(d, n, rng):
    """Uniform points in the unit d-ball (rejection-free: direction * radius)."""
    if d == 1:
        return rng.uniform(-1.0, 1.0, (n, 1))
    v = rng.standard_normal((n, d))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    r = rng.uniform(0.0, 1.0, n) ** (1.0 / d)
    return v * r[:, None]


def r_cut(d, n, deg):
    """Neighbour radius so the expected degree is ~deg (uniform density)."""
    if d == 1:
        return deg / n            # interval [-1,1]: frac within r_c each side = r_c
    return (deg / n) ** (1.0 / d)


R_GROUND = 0.85       # Dirichlet shell: theta = 0 for r > R_GROUND (no
                      # uniform-compensation paraboloid; system non-singular)


def relax(points, rc):
    """Build L = D - A, ground the outer shell (theta=0), solve L theta = J
    for a unit point source at the centre node. No Green function anywhere."""
    n = len(points)
    tree = cKDTree(points)
    pairs = tree.query_pairs(rc, output_type="ndarray")
    rows = np.r_[pairs[:, 0], pairs[:, 1]]
    cols = np.r_[pairs[:, 1], pairs[:, 0]]
    A = sparse.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)).tocsr()
    deg = np.asarray(A.sum(axis=1)).ravel()
    L = (sparse.diags(deg) - A).tocsr()
    r = np.linalg.norm(points, axis=1)
    src_global = int(np.argmin(r))
    # keep only the connected component of the source (Poisson fluctuations
    # leave a few isolated nodes that would make the interior block singular)
    from scipy.sparse.csgraph import connected_components
    _, labels = connected_components(A, directed=False)
    interior = np.where((r <= R_GROUND) & (labels == labels[src_global]))[0]
    touches_ground = np.any((r > R_GROUND) & (labels == labels[src_global]))
    assert touches_ground, "source component does not reach the ground shell"
    Lii = L[np.ix_(interior, interior)].tocsr()
    J = np.zeros(len(interior))
    J[int(np.where(interior == src_global)[0][0])] = 1.0
    M = sparse.diags(1.0 / Lii.diagonal())          # Jacobi preconditioner
    th_i, info = cg(Lii, J, rtol=1e-10, maxiter=20000, M=M)
    assert info == 0, f"CG did not converge (info={info})"
    theta = np.zeros(n)
    theta[interior] = th_i
    return theta, float(np.mean(deg)), info


def binned_profile(points, theta, r_lo, r_hi):
    r = np.linalg.norm(points, axis=1)
    edges = np.linspace(r_lo, r_hi, N_BINS + 1)
    mids, vals = [], []
    for i in range(N_BINS):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() >= 5:
            mids.append(0.5 * (edges[i] + edges[i + 1]))
            vals.append(float(np.mean(theta[m])))
    return np.array(mids), np.array(vals)


# COMPARISON ONLY -- model fitting against power/log shapes (analysis, not
# generation; the relaxation above contains no Green function).
def fit_models(rr, th):
    def power(r, A, p, C):
        return A * r ** p + C

    best, rss_pw = None, np.inf                     # multi-start (avoids the
    for p0 in (-2.5, -1.0, -0.3, 1.0):              # p->0 local optimum)
        try:
            pw, _ = curve_fit(power, rr, th, p0=(th[0] * rr[0] ** (-p0), p0, 0.0),
                              bounds=([-np.inf, -4.0, -np.inf],
                                      [np.inf, 3.0, np.inf]), maxfev=20000)
        except RuntimeError:
            continue
        rss = float(np.sum((power(rr, *pw) - th) ** 2))
        if rss < rss_pw:
            best, rss_pw = pw, rss
    X = np.c_[np.log(rr), np.ones_like(rr)]
    co, *_ = np.linalg.lstsq(X, th, rcond=None)
    rss_lg = float(np.sum((X @ co - th) ** 2))
    n = len(rr)
    aic_pw = n * np.log(rss_pw / n) + 2 * 3         # AIC: power has 3 params,
    aic_lg = n * np.log(rss_lg / n) + 2 * 2         # log has 2 (handles the
    return {"power_exponent": float(best[1]), "rss_power": rss_pw,   # p->0
            "log_slope": float(co[0]), "rss_log": rss_lg,            # degeneracy)
            "winner": "log" if aic_lg < aic_pw else "power"}
# END COMPARISON ONLY


def main():
    results = {}
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.0))
    for (d, n, deg_t), ax in zip(CASES, axes):
        rc = r_cut(d, n, deg_t)
        r_lo = 2.0 * rc
        fits, profs = [], []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(5000 + 97 * d + seed)
            pts = sprinkle_ball(d, n, rng)
            theta, mean_deg, info = relax(pts, rc)
            rr, th = binned_profile(pts, theta, r_lo, FIT_HI)
            fits.append(fit_models(rr, th))
            profs.append((rr, th))
        exps = [f["power_exponent"] for f in fits]
        wins = [f["winner"] for f in fits]
        results[d] = {
            "N": n, "r_c": rc, "mean_degree_first_seed": mean_deg,
            "fit_window": [r_lo, FIT_HI],
            "power_exponent": {"mean": float(np.mean(exps)),
                               "sem": float(np.std(exps, ddof=1) / np.sqrt(len(exps)))},
            "log_wins": int(sum(w == "log" for w in wins)),
            "n_seeds": N_SEEDS,
        }
        rr, th = profs[0]
        ax.plot(rr, th, "o", ms=3, color="tab:blue")
        ax.set_xscale("log")
        if d >= 3:
            ax.set_yscale("log")
        ax.set_title(f"d={d}: p={np.mean(exps):+.2f}"
                     f"{' (log wins '+str(results[d]['log_wins'])+'/10)' if d==2 else ''}")
        ax.set_xlabel("r")
        if d == 1:
            ax.set_ylabel(r"$\theta(r)$")
    fig.suptitle("DS1 -- emergent profile vs dimension (no ansatz)")
    fig.tight_layout()
    fig.savefig(OUT / "DS1_profiles.png", dpi=150)

    payload = {"cases": {str(d): results[d] for d in results},
               "pre_registered": {"1": "+1 (linear)", "2": "log",
                                  "3": "-1", "4": "-2"},
               "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                         "numpy": np.__version__,
                         "platform": platform.platform()}}
    (OUT / "DS1_profiles.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({str(d): {"p": results[d]["power_exponent"],
                               "log_wins": results[d]["log_wins"]}
                      for d in results}, indent=2))


if __name__ == "__main__":
    main()

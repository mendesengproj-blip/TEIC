"""L2 -- the network's response to a UNIFORM source is a quadratic (static
de Sitter-like) potential, with the coefficient fixed by the SAME transport
constant measured in CR1b -- a consistency loop, not a new fit.

L theta = j * 1_interior (graph Laplacian, Dirichlet shell), so in the
continuum -(2pi/15) rho rc^5 kappa * Lap(theta) = j with kappa = 1.066 the
deg=48 finite-degree correction MEASURED in CR1b. Hence
    theta(r) = beta (R_eff^2 - r^2),   beta = 15 j kappa / (12 pi rho rc^5).
Pre-registered: quadratic R^2 > 0.99; beta within 10% of the calibrated value.
5 seeds; reuses the DS1 generator by import (unmodified).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import cg
from scipy.spatial import cKDTree

HERE = Path(__file__).resolve().parent
DS1 = HERE.parent / "dimension_scan" / "DS1_profiles.py"
spec = importlib.util.spec_from_file_location("ds1", DS1)
ds1 = importlib.util.module_from_spec(spec)
sys.modules["ds1"] = ds1
spec.loader.exec_module(ds1)

N = 80_000
DEG = 48
RC = (DEG / N) ** (1.0 / 3.0)
J = 1.0
KAPPA = 0.2025 / (15.0 / (8.0 * np.pi ** 2))   # CR1b deg=48 measured constant
V_BALL = 4.0 * np.pi / 3.0
RHO = N / V_BALL
N_SEEDS = 5
R_GROUND = 0.85


def relax_uniform(points, rc):
    """L theta = J on every interior node (Dirichlet shell at R_GROUND)."""
    n = len(points)
    tree = cKDTree(points)
    pairs = tree.query_pairs(rc, output_type="ndarray")
    rows = np.r_[pairs[:, 0], pairs[:, 1]]
    cols = np.r_[pairs[:, 1], pairs[:, 0]]
    A = sparse.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)).tocsr()
    deg = np.asarray(A.sum(axis=1)).ravel()
    L = (sparse.diags(deg) - A).tocsr()
    r = np.linalg.norm(points, axis=1)
    _, labels = connected_components(A, directed=False)
    main_label = np.bincount(labels).argmax()
    interior = np.where((r <= R_GROUND) & (labels == main_label))[0]
    Lii = L[np.ix_(interior, interior)].tocsr()
    M = sparse.diags(1.0 / Lii.diagonal())
    th_i, info = cg(Lii, np.full(len(interior), J), rtol=1e-10, maxiter=30000,
                    M=M)
    assert info == 0
    theta = np.zeros(n)
    theta[interior] = th_i
    return theta, r


def main():
    beta_pred = 15.0 * J * KAPPA / (12.0 * np.pi * RHO * RC ** 5)
    betas, r2s = [], []
    prof = None
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(9000 + seed)
        pts = ds1.sprinkle_ball(3, N, rng)
        theta, r = relax_uniform(pts, RC)
        # bin and fit theta = alpha - beta r^2 on the interior window
        edges = np.linspace(2 * RC, 0.7, 25)
        mids, vals = [], []
        for i in range(len(edges) - 1):
            m = (r >= edges[i]) & (r < edges[i + 1])
            mids.append(0.5 * (edges[i] + edges[i + 1]))
            vals.append(float(np.mean(theta[m])))
        mids, vals = np.array(mids), np.array(vals)
        X = np.c_[mids ** 2, np.ones_like(mids)]
        co, *_ = np.linalg.lstsq(X, vals, rcond=None)
        fitted = X @ co
        ss_res = float(np.sum((vals - fitted) ** 2))
        ss_tot = float(np.sum((vals - vals.mean()) ** 2))
        betas.append(-float(co[0]))
        r2s.append(1.0 - ss_res / ss_tot)
        if seed == 0:
            prof = (mids, vals, co)

    beta_m = float(np.mean(betas))
    beta_sem = float(np.std(betas, ddof=1) / np.sqrt(N_SEEDS))
    ratio = beta_m / beta_pred
    payload = {
        "params": {"N": N, "deg": DEG, "rc": RC, "rho": RHO, "j": J,
                   "kappa_from_CR1b": KAPPA, "n_seeds": N_SEEDS},
        "beta": {"measured": beta_m, "sem": beta_sem,
                 "predicted_calibrated": beta_pred, "ratio": ratio},
        "quadratic_R2": {"mean": float(np.mean(r2s)), "min": float(np.min(r2s))},
        "death": bool(abs(ratio - 1.0) > 0.10 or np.min(r2s) < 0.99),
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__},
    }
    (HERE / "L2_response.json").write_text(json.dumps(payload, indent=2))

    mids, vals, co = prof
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(mids ** 2, vals, "o", ms=4, color="tab:blue", label="network (seed 0)")
    xx = np.linspace(0, mids[-1] ** 2, 50)
    ax.plot(xx, co[1] + co[0] * xx, "k-", lw=1,
            label=fr"fit: $\beta$={-co[0]:.2f}")
    ax.plot(xx, co[1] - beta_pred * (xx - 0), "g:",
            label=fr"CR1b-calibrated $\beta$={beta_pred:.2f}")
    ax.set_xlabel(r"$r^2$")
    ax.set_ylabel(r"$\theta$")
    ax.set_title(f"uniform source: quadratic response "
                 f"(ratio {ratio:.3f}, R$^2$={np.mean(r2s):.4f})")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "L2_response.png", dpi=150)

    print(json.dumps({"beta": payload["beta"],
                      "R2": payload["quadratic_R2"],
                      "death": payload["death"]}, indent=2))


if __name__ == "__main__":
    main()

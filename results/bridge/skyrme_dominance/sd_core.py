"""sd_core.py -- shared helpers for the SKYRME_DOMINANCE campaign (SD1-SD5).

Asks whether Skyrme-term dominance (net positive quartic) can emerge from the
minimal action in ANY network regime: dimension, density, link measure,
higher orders, curvature. Closes the frontier left by BRIDGE_SU2_COEFF
(verdict B: the operator emerges, the dominance does not).

Anti-circularity: pure real arithmetic (quaternions via sc_core/su2_core).
No complex numbers, no dilation formulas. The Skyrme operator is never a fit
target: every script measures first and compares against the pre-registered
addendum (docs/prompts/SKYRME_DOMINANCE.md) afterwards.

Conventions (inherited from BRIDGE_SU2_COEFF):
  * currents matrix C (3x3): rows = spatial mu, cols = isospin a; G = C C^T;
    S = (TrG)^2, K = (TrG)^2 - Tr(G^2) = sum_{mu,nu} |c_mu x c_nu|^2.
  * link energy 1 - cos(a|l_e|/2); quartic -(a^4/384)|l_e|^4 per link.
  * "cross-channel fraction" of a link direction e (unit, d components):
    kappa(e) = 1 - sum_mu (e^mu)^4  -- the fraction of the link's quartic
    weight in mu != nu channels (the charter's per-link K/S). This is NOT
    K/S of the field invariants; SD1 disentangles the two.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "bridge" / "su2_coeff"))
import sc_core as sc  # noqa: E402  (re-exports su2_core as sc.s2)

OUTDIR = Path(__file__).resolve().parent


# ---- generic d-dimensional directions --------------------------------------- #
def unit_directions(n, d, rng):
    """n unit vectors uniform on S^{d-1} (isotropic in d dimensions)."""
    v = rng.standard_normal((n, d))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def cross_channel_fraction(dirs):
    """kappa(e) = 1 - sum_mu e_mu^4 per direction; (N,) array."""
    return 1.0 - np.sum(dirs ** 4, axis=1)


# ---- field invariants in d dimensions --------------------------------------- #
def invariants_d(C):
    """(TrG, S, K) for a d x m currents matrix C (G = C C^T, d x d)."""
    G = C @ C.T
    trG = float(np.trace(G))
    trG2 = float(np.trace(G @ G))
    return trG, trG * trG, trG * trG - trG2


# ---- exact isotropic sphere moments (rational, any d) ------------------------ #
def sphere_even_moment(powers, d):
    """< prod_i e_i^(2 k_i) > on S^{d-1}: prod (2k_i - 1)!! / prod_{j<K} (d + 2j),
    K = sum k_i. Exact float; used to cross-check sympy results."""
    powers = [int(k) for k in powers]
    K = sum(powers)
    num = 1.0
    for k in powers:
        for m in range(1, 2 * k, 2):
            num *= m
    den = 1.0
    for j in range(K):
        den *= (d + 2 * j)
    return num / den


# ---- Poisson sprinkling in a causal diamond of M^{3+1} (SD3) ---------------- #
DIAMOND_T = 1.0
DIAMOND_VOL = 2.0 * np.pi / 3.0 * DIAMOND_T ** 4   # |x| <= T - |t|


def sprinkle_diamond(rho, rng):
    """Poisson sprinkling, uniform in the causal diamond between (-T,0) and
    (T,0). Returns (t, x) with t (N,), x (N,3), sorted by t. Purely
    combinatorial sampling -- no dilation formulas anywhere."""
    n = rng.poisson(rho * DIAMOND_VOL)
    r = rng.random(n)
    u = DIAMOND_T * (1.0 - (1.0 - r) ** 0.25)          # |t| ~ (T-|t|)^3
    t = u * rng.choice([-1.0, 1.0], size=n)
    e = unit_directions(n, 3, rng)
    rad = (DIAMOND_T - u) * rng.random(n) ** (1.0 / 3.0)
    x = e * rad[:, None]
    order = np.argsort(t)
    return t[order], x[order]


def causal_links(t, x):
    """Covering relations (links) of the causal order: i -> j iff i causally
    precedes j with no element in between. Returns (n_links, 2) index pairs."""
    n = len(t)
    dt = t[None, :] - t[:, None]                       # dt[i,j] = t_j - t_i
    dx2 = np.sum((x[None, :, :] - x[:, None, :]) ** 2, axis=2)
    rel = (dt > 0) & (dt ** 2 >= dx2)                  # i precedes j
    relf = rel.astype(np.float32)
    two_step = (relf @ relf) > 0.5                     # exists k: i<k<j
    link = rel & ~two_step
    return np.argwhere(link)


# ---- bookkeeping ------------------------------------------------------------- #
def seed_stats(values):
    v = np.asarray(values, dtype=float)
    return {"mean": float(np.mean(v)),
            "sem": float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
            "n_seeds": int(len(v))}


def save_json(name, payload):
    payload = dict(payload)
    payload["_meta"] = {
        "campaign": "SKYRME_DOMINANCE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
    }
    path = OUTDIR / name
    path.write_text(json.dumps(payload, indent=2))
    return path

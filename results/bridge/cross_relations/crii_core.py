"""crii_core.py -- shared primitives for CROSS_RELATIONS_II (CR3, CR4).

Pre-registered in CROSS_RELATIONS_II.md. Independent of R1-R3 / e6-e11;
modifies nothing in earlier campaigns (consumes the C1 link protocol and the
W2 plaquette protocol by reuse, not by edit).

ANTI-CIRCULARITY. No SR/GR dilation factor, no GM/r, no DEV coefficient.
Inputs are bare Minkowski cones + Poisson sprinkling (src/causal_core.py).
V_cap below is the exact Euclidean-integral volume of the truncated future
light-cone sliver {0 < tau < t, 0 < dt < H} -- Poisson void-probability
geometry, not a relativistic formula.

THE "SAME NETWORK" CONDITION (declared). CR3 and CR4 consume the SAME
sprinklings: identical seed formula, identical boxes. Any script importing
this module with the same (rho-index, seed) gets byte-identical events.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from causal_core import sprinkle_box  # noqa: E402  (generator primitive, no SR/GR)

# ---- pre-registered parameters (CROSS_RELATIONS_II.md, fixed before running) --
EXTENT = 3.2          # main box, all 4 coordinates
MARGIN_FRAC = 0.25    # bulk = inner box, each face pulled in by 0.8
H_CAP = 0.75          # future-cone time cap (< margin: cone entirely in box)
RHOS = [16.0, 27.0, 45.0, 75.0]
N_SEEDS = 8
SEED_BASE = 31000     # main box
# verification box (CR4 regulator check)
EXTENT_CHK = 2.56
H_CAP_CHK = 0.60
RHO_CHK = 45.0
SEED_BASE_CHK = 41000


def sprinkling(rho_index, seed, extent=EXTENT, seed_base=SEED_BASE):
    """The shared sprinkling for (rho-index, seed): same events for CR3 and CR4."""
    rho = RHOS[rho_index] if seed_base == SEED_BASE else RHO_CHK
    rng = np.random.default_rng(seed_base + 1000 * rho_index + seed)
    bounds = [[0.0, extent]] * 4
    return sprinkle_box(rho, bounds, rng), np.asarray(bounds, float)


def bulk_mask(pts, bounds, margin_frac=MARGIN_FRAC):
    lo = bounds[:, 0] + margin_frac * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin_frac * (bounds[:, 1] - bounds[:, 0])
    return np.all((pts >= lo) & (pts <= hi), axis=1)


def inner_volume(bounds, margin_frac=MARGIN_FRAC):
    ext = (bounds[:, 1] - bounds[:, 0]) * (1.0 - 2.0 * margin_frac)
    return float(np.prod(ext))


# --------------------------------------------------------------------------- #
# CR3 geometry: exact volume of the capped cone sliver {0 < tau < t, 0 < dt < H}
# --------------------------------------------------------------------------- #
def V_cap(t, H):
    """Exact 3+1D coordinate volume of {q: 0 < dt < H, 0 < tau(p,q) < t}.

    V = (pi/3)H^4 - (4pi/3) * I(t,H),
    I = H(2H^2-5t^2)sqrt(H^2-t^2)/8 + (3t^4/8) ln((H+sqrt(H^2-t^2))/t)  (t<H),
    I(t>=H) = 0;  leading order V ~ pi H^2 t^2 for t << H.
    Used ONLY to rescale u = rho*V(dtau_min, H), whose Exp(1) law is the
    pre-registered prediction (Poisson void probability).
    """
    t = np.asarray(t, dtype=float)
    full = (np.pi / 3.0) * H ** 4
    tt = np.minimum(t, H)
    s = np.sqrt(np.maximum(H * H - tt * tt, 0.0))
    safe_t = np.where(tt > 0, tt, 1.0)
    I = (H * (2.0 * H * H - 5.0 * tt * tt) * s / 8.0
         + (3.0 * tt ** 4 / 8.0) * np.log((H + s) / safe_t))
    I = np.where(tt > 0, I, H ** 4 / 4.0)
    return full - (4.0 * np.pi / 3.0) * I


def _self_check():
    """V_cap limits: V(0)=0, V(H)=full, leading order pi H^2 t^2."""
    H = 0.75
    assert abs(V_cap(0.0, H)) < 1e-12
    assert abs(V_cap(H, H) - (np.pi / 3.0) * H ** 4) < 1e-12
    t = 1e-3
    lead = np.pi * H * H * t * t
    assert abs(V_cap(t, H) / lead - 1.0) < 1e-3, V_cap(t, H) / lead
    # monotone
    ts = np.linspace(0, H, 200)
    assert np.all(np.diff(V_cap(ts, H)) > 0)


_self_check()


# --------------------------------------------------------------------------- #
# CR3 observable: per-bulk-event minimum link proper time within the cap
# --------------------------------------------------------------------------- #
def min_dtau_capped(pts, bounds, H=H_CAP, margin_frac=MARGIN_FRAC):
    """For each bulk event, min proper time to a future event with 0<dt<H.

    Returns (dtau_min array over events WITH a neighbour, n_truncated).
    Truncated events (no event in the cap region) are counted, not imputed --
    their expected fraction exp(-rho*(pi/3)H^4) is part of the pre-registration.
    """
    pts = np.asarray(pts, float)
    bulk = np.nonzero(bulk_mask(pts, bounds, margin_frac))[0]
    out, trunc = [], 0
    for idx in bulk:
        d = pts - pts[idx]
        dt = d[:, 0]
        s2 = dt * dt - np.sum(d[:, 1:] ** 2, axis=1)
        m = (dt > 0) & (dt < H) & (s2 > 0)
        if not np.any(m):
            trunc += 1
            continue
        out.append(np.sqrt(s2[m].min()))
    return np.asarray(out), trunc


# --------------------------------------------------------------------------- #
# CR4: covering relations (C1 protocol) -- links without intermediaries
# --------------------------------------------------------------------------- #
def causal_links(pts):
    """(i, j) covering relations p_i < p_j (no intermediate). C1 protocol."""
    pts = np.asarray(pts, dtype=float)
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    C = (dt > 0) & (dt * dt > dx2)
    Cf = C.astype(np.float32)
    inter = (Cf @ Cf) > 0.5
    L = C & ~inter
    i, j = np.nonzero(L)
    return i, j


def link_second_moment(pts, bounds, margin_frac=MARGIN_FRAC):
    """C2^{mu nu} = (1/2V_in) sum_bulk-links dtau e^mu e^nu  (C1 protocol).

    Bulk link = midpoint inside the inner box. Returns (C2 tensor 4x4, n_links).
    """
    pts = np.asarray(pts, float)
    i, j = causal_links(pts)
    e = pts[j] - pts[i]
    dtau = np.sqrt(np.maximum(e[:, 0] ** 2 - np.sum(e[:, 1:] ** 2, axis=1), 0.0))
    mid = 0.5 * (pts[i] + pts[j])
    keep = bulk_mask(mid, bounds, margin_frac)
    e, dtau = e[keep], dtau[keep]
    M2 = np.einsum("l,lm,ln->mn", dtau, e, e)
    return M2 / (2.0 * inner_volume(bounds, margin_frac)), int(keep.sum())


def plaquette_moments(pts, bounds, margin_frac=MARGIN_FRAC, max_per_base=6):
    """Pi_E = (1/V_in) sum_plaq sum_i (Om^{0i})^2 ; Pi_B with spatial pairs.

    Plaquettes = minimal causal diamonds (W2 protocol, wilson_core), base in bulk.
    """
    import importlib.util
    wpath = Path(__file__).resolve().parent.parent / "wilson" / "wilson_core.py"
    spec = importlib.util.spec_from_file_location("wilson_core", wpath)
    wc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wc)

    pts = np.asarray(pts, float)
    loops = wc.causal_diamond_loops(pts, max_per_base=max_per_base)
    lo = bounds[:, 0] + margin_frac * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin_frac * (bounds[:, 1] - bounds[:, 0])
    pe = pb = 0.0
    n_kept = 0
    for verts in loops:
        base = verts[0]
        if not (np.all(base >= lo) and np.all(base <= hi)):
            continue
        Om = wc.area_bivector(verts)
        pe += float(np.sum(Om[0, 1:] ** 2))
        pb += float(Om[1, 2] ** 2 + Om[1, 3] ** 2 + Om[2, 3] ** 2)
        n_kept += 1
    V_in = inner_volume(bounds, margin_frac)
    return pe / V_in, pb / V_in, n_kept

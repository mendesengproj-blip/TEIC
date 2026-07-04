"""xi_suite.py -- Campaign XI: can a correlation length diverge on a causal set?

ANALYSIS / DRIVER layer.  Imports the data generator orientation_core WITHOUT
modification (O3Model + causal_link_graph + structure_factor).  The ONLY thing that
changes between levers is the GRAPH handed to the verbatim Metropolis -- the "one
variable" discipline of the programme.

Anti-circularity: every quantity here is real arithmetic on the measured spins/graph.
No relativistic dilation, no complex literal, no critical temperature inserted.  Each
inserted cut-off scale (cap k, window ell_k) is recorded and labelled [External] in
the JSON; the divergence verdict only ever uses the dimensionless ratios xi/L, xi/ell.

The decisive estimator is the second-moment correlation length from the transverse
(Goldstone) structure factor S(k), measured AT the swept-located J_c, never deep in a
phase.  The decision quantity is xi_2nd / L_s and whether it grows / crosses with L.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORI = HERE.parents[2] / "results" / "vacuum_structure" / "orientation"
sys.path.insert(0, str(ORI))
from orientation_core import (  # noqa: E402
    O3Model, Graph, causal_link_graph, lattice_periodic, structure_factor,
    transverse_components, measure_correlation, fit_forms,
)
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box, causal_matrix  # noqa: E402


# ====================================================================== #
# Substrate builders -- the LEVERS.  Each returns (Graph, xs) where xs is
# the (N, d_space) spatial coordinate array used by the structure factor.
# ====================================================================== #
def build_bare(pts):
    """Baseline / Lever C: bare Hasse (covering-relation) link graph.

    For (3+1)D pts this is the mean-field control; for (2+1)D pts it IS lever C
    (lower effective dimension, NO inserted scale)."""
    g = causal_link_graph(pts)
    return g, np.asarray(pts)[:, 1:]


def build_lattice_3d(m):
    """POSITIVE CONTROL: O(3) on a periodic 3D cubic lattice -- a substrate KNOWN
    to have a genuine 2nd-order transition with diverging xi.  If the suite does not
    see xi/L crossing here, the estimator is too blunt and any null on causal sets is
    untrustworthy.  Returns (Graph, xs) with integer lattice coordinates; L_s = m."""
    g = lattice_periodic((m, m, m))
    idx = np.arange(m ** 3)
    xs = np.stack([idx // (m * m), (idx // m) % m, idx % m], axis=1).astype(float)
    return g, xs


def _causal_proper_time(pts):
    """(C, tau) where C[i,j]=i precedes j and tau[i,j]=sqrt(interval2) for the
    causal pairs (0 elsewhere).  Bare Minkowski cones only -- no dilation."""
    pts = np.asarray(pts, float)
    C = causal_matrix(pts)
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    s2 = dt * dt - dx2
    tau = np.where(C, np.sqrt(np.maximum(s2, 0.0)), np.inf)
    return C, tau


def build_knn_cap(pts, k):
    """Lever A: keep, for each event, its k nearest CAUSAL neighbours by proper
    time (smallest tau).  Hard coordination cap -> z controlled by k ([External]).
    Edges symmetrised; the verbatim Metropolis runs on the pruned graph."""
    C, tau = _causal_proper_time(pts)
    n = C.shape[0]
    order = np.argsort(tau, axis=1)[:, :k]          # (n,k) k nearest per node
    rows = np.repeat(np.arange(n), order.shape[1])
    cols = order.ravel()
    valid = np.isfinite(tau[rows, cols])            # drop nodes with <k causal nbrs
    edges = np.stack([rows[valid], cols[valid]], axis=1) if valid.any() else \
        np.zeros((0, 2), dtype=np.int64)
    g = Graph(n, edges)
    g.n_links = int(g.edges.shape[0])
    return g, np.asarray(pts)[:, 1:]


def build_window(pts, ell_k):
    """Lever B: mesoscale neighbourhood -- connect causally related i,j whose
    proper time tau_ij <= ell_k ([External]).  A graph-level proxy of the
    intermediate-non-locality (B_k) smearing: neither the bare relation (all) nor
    the Hasse links (nearest) but a proper-time band of width ell_k."""
    C, tau = _causal_proper_time(pts)
    n = C.shape[0]
    mask = np.isfinite(tau) & (tau <= ell_k)
    src, dst = np.nonzero(mask)
    edges = np.stack([src, dst], axis=1) if src.size else np.zeros((0, 2), np.int64)
    g = Graph(n, edges)
    g.n_links = int(g.edges.shape[0])
    return g, np.asarray(pts)[:, 1:]


# ====================================================================== #
# Second-moment correlation length from S(k)  (Ornstein-Zernike two-mode)
# ====================================================================== #
def structure_factor_shell(comp_list, xs, k_mag, kdirs):
    """Shell-averaged S(|k|): average |sum_i s_i e^{-i k.x_i}|^2 / N over a fixed set
    of unit directions kdirs (so |k|=k_mag), over components and samples.  Real
    arithmetic (cos/sin sums); many directions sharply reduce the single-vector
    variance that makes the two-point second-moment xi noisy."""
    xs = np.asarray(xs, float)
    N = xs.shape[0]
    acc, cnt = 0.0, 0
    for comps in comp_list:
        for s in comps:
            for d in kdirs:
                phase = k_mag * (xs @ d)            # (N,)
                re = np.cos(phase) @ s
                im = np.sin(phase) @ s
                acc += (re * re + im * im) / N
                cnt += 1
    return acc / max(cnt, 1)


def full_components(model):
    """Connected ORDER-PARAMETER fluctuation arrays (each O(3) component minus its
    mean).  The structure factor of these is the standard FSS object: a clean
    Lorentzian whose second moment is the (full) correlation length, NOT restricted
    to the Goldstone-soft transverse sector.  Real arithmetic."""
    n = model.n
    return [n[:, 0] - n[:, 0].mean(),
            n[:, 1] - n[:, 1].mean(),
            n[:, 2] - n[:, 2].mean()]


def xi_second_moment(model, xs, L_s, n_eq_samples=24, meas_every=2, which="full",
                     n_kdirs=24):
    """xi_2nd from the transverse structure factor at k_min=2pi/L_s, k2=2 k_min.

    OZ inversion S(k)=S0/(1+(k xi)^2):
        xi^2 = (S1 - S2) / (k1^2 (4 S2 - S1)),   k1=k_min, k2=2 k_min.
    Returns (xi, S1, S2, reliable).  Real arithmetic only (structure_factor cos/sin).

    Reliability flag: in the O(3) ORDERED phase the transverse modes are Goldstone
    (S(k) ~ 1/k^2 -> S1/S2 -> 4 -> denom 4*S2 - S1 -> 0), so the OZ inversion is
    SINGULAR there and xi blows up trivially -- that is the Goldstone soft mode, not
    a critical divergence.  We flag a point unreliable when the denominator is within
    8% of the Goldstone-singular value (S1 >= 3.68*S2); the estimator is trustworthy
    on the DISORDERED approach (massive, clean Lorentzian) and at J_c."""
    k_min = 2.0 * np.pi / L_s
    comp_fn = full_components if which == "full" else transverse_components
    comp_list = []
    for _ in range(n_eq_samples):
        for _ in range(meas_every):
            model.sweep()
        comp_list.append(comp_fn(model))
    # shell of unit k-directions (fixed across sizes for a fair comparison)
    d_space = xs.shape[1]
    rng = np.random.default_rng(12345)
    v = rng.standard_normal((n_kdirs, d_space))
    kdirs = v / np.linalg.norm(v, axis=1, keepdims=True)
    S1 = structure_factor_shell(comp_list, xs, k_min, kdirs)
    S2 = structure_factor_shell(comp_list, xs, 2.0 * k_min, kdirs)
    denom = k_min ** 2 * (4.0 * S2 - S1)
    reliable = (4.0 * S2 - S1) > 0.08 * (4.0 * S2)   # not in Goldstone-singular band
    if (S1 - S2) > 0 and denom > 0:
        xi = float(np.sqrt((S1 - S2) / denom))
    else:
        xi = 0.0
        reliable = False
    return xi, S1, S2, bool(reliable)


# ====================================================================== #
# Per-(size, J) measurement of the full suite
# ====================================================================== #
def measure_point(graphs, J, n_burn, n_meas, meas_every, L_s, seed0=0):
    """Average m, U4, chi, xi_2nd, z, conn_frac over seeds at one (size, J).

    graphs: list of (Graph, xs) pre-built ONCE per (size, lever) and reused across
    the J-scan, so every lever sees the SAME substrate realisations and only the
    builder (graph) differs."""
    ms, m2_acc, m4_acc, n_samp = [], 0.0, 0.0, 0
    zs, conns, Ns = [], [], []
    xis, S1s, S2s, rel = [], [], [], []
    for s, (g, xs) in enumerate(graphs):
        zs.append(float(g.degree.mean()))
        conns.append(g.connected_fraction())
        Ns.append(g.n)
        model = O3Model(g, J=J, seed=2000 + seed0 + s)
        model.equilibrate(n_burn, adapt=True)
        seed_ms = []
        taken, sweeps = 0, 0
        while taken < n_meas:
            model.sweep()
            sweeps += 1
            if sweeps % meas_every == 0:
                seed_ms.append(model.order_parameter())
                taken += 1
        seed_ms = np.asarray(seed_ms)
        ms.append(seed_ms.mean())
        m2_acc += np.sum(seed_ms ** 2)
        m4_acc += np.sum(seed_ms ** 4)
        n_samp += seed_ms.size
        # xi from a fresh measurement window (continues from equilibrated state)
        xi, S1, S2, reliable = xi_second_moment(model, xs, L_s)
        xis.append(xi); S1s.append(S1); S2s.append(S2); rel.append(reliable)
    ms = np.asarray(ms)
    m_mean = float(ms.mean())
    m2 = m2_acc / n_samp
    m4 = m4_acc / n_samp
    U4 = float(1.0 - m4 / (3.0 * m2 ** 2)) if m2 > 0 else float("nan")
    N_mean = float(np.mean(Ns))
    # chi = N Var(m) using seed-mean variance as the fluctuation estimator
    chi = float(N_mean * (m2 - m_mean ** 2))
    return {
        "J": J, "N_mean": N_mean, "z_mean": float(np.mean(zs)),
        "conn_frac": float(np.mean(conns)),
        "m": m_mean, "m2": float(m2), "m4": float(m4), "U4": U4, "chi": chi,
        "xi_2nd": float(np.mean(xis)), "xi_over_L": float(np.mean(xis)) / L_s,
        "xi_reliable_frac": float(np.mean(rel)),
        "S1": float(np.mean(S1s)), "S2": float(np.mean(S2s)),
        "L_s": L_s, "n_seeds": len(graphs),
    }


def locate_Jc(rows):
    """J_c = J of the chi peak (swept-located, no external value)."""
    Js = np.array([r["J"] for r in rows])
    chi = np.array([r["chi"] for r in rows])
    return float(Js[int(np.argmax(chi))])


# ====================================================================== #
# Self-test (smoke)
# ====================================================================== #
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    pts = sprinkle_box(2.0, [(0.0, 4.0)] * 4, rng)
    g, xs = build_bare(pts)
    print(f"bare 3+1D: N={g.n} z={g.degree.mean():.1f} links={g.n_links}")
    gk, _ = build_knn_cap(pts, k=4)
    print(f"knn k=4 : N={gk.n} z={gk.degree.mean():.1f} conn={gk.connected_fraction():.2f}")
    gw, _ = build_window(pts, ell_k=1.0)
    print(f"window 1.0: N={gw.n} z={gw.degree.mean():.1f} conn={gw.connected_fraction():.2f}")
    r = measure_point([build_bare(pts)], J=2.0, n_burn=100, n_meas=30,
                      meas_every=2, L_s=4.0)
    print(f"measure_point bare J=2: m={r['m']:.3f} U4={r['U4']:.3f} "
          f"xi/L={r['xi_over_L']:.3f} chi={r['chi']:.3f}")
    print("self-test OK")

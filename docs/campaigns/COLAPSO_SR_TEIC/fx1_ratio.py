"""fx1_ratio.py -- FX1: is the collapse rate locked to the spectral gas scale?

Tests the single novelty candidate that survived MAPA_CONVERGENCIA section (C):
the dimensionless ratio

    R_FX1 = Gamma_dec(sigma_x) / Var_bulk(lambda_M)

of the SAME causal operator M -- collapse decoherence rate (FS1) over the Dyson
Brownian Motion gas variance (FS2). Scale-free by construction (M -> c M cancels).

Frozen protocol: FX1_PRE_REGISTRO.md (2026-06-27). No new tuned parameter; reuses
validated engines. Result-first; death criteria pre-registered.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sr_teic_core as core
import fs_core as fs

HERE = Path(__file__).resolve().parent

DIMS = (2, 4)
NS = (100, 200, 400)
SIGMAS = (0.10, 0.18, 0.30)          # fraction of spatial extent (as FD2/FS1)
SEEDS = 8
EDGE_FRAC = 0.10                      # bulk window, identical to fs.gap_ratios
DX_FRAC = 0.60                        # separation = 60% of spatial extent (well-separated)


# --------------------------------------------------------------------------- #
def bulk_variance(eigs, edge_frac=EDGE_FRAC):
    """Variance of the BULK eigenvalues (drop edge_frac each end). The DBM gas
    'temperature' scale -- same bulk window FS2 used for <r>."""
    ev = np.sort(np.asarray(eigs, float))
    n = ev.size
    lo = int(np.floor(edge_frac * n))
    hi = n - lo
    ev = ev[lo:hi]
    return float(np.var(ev)), ev


def spatial_extent(pts):
    """Half-range of the spatial coordinates (cols 1:), per axis mean."""
    x = pts[:, 1:]
    return float(np.mean(x.max(axis=0) - x.min(axis=0)))


def gamma_dec_for(M, pts, sigma_abs, dx_abs):
    """Gamma_dec between two Gaussian spatial modes separated by dx_abs along axis-1,
    each of absolute width sigma_abs. Returns (Gamma_dec, cross_frac, mu1, mu2)."""
    x = pts[:, 1:]
    c = x.mean(axis=0)
    off = np.zeros_like(c); off[0] = dx_abs / 2.0
    psi1 = fs.spatial_mode(pts, sigma_abs, center=c - off)
    psi2 = fs.spatial_mode(pts, sigma_abs, center=c + off)
    Mp1 = M @ psi1; Mp2 = M @ psi2
    q1 = float(Mp1 @ Mp1); q2 = float(Mp2 @ Mp2)
    mu1 = float(psi1 @ Mp1); mu2 = float(psi2 @ Mp2)
    g = 0.5 * q1 + 0.5 * q2 - mu1 * mu2
    cross = abs(mu1 * mu2)
    total = 0.5 * q1 + 0.5 * q2
    cross_frac = cross / total if total > 0 else 0.0
    return g, cross_frac, mu1, mu2


# --------------------------------------------------------------------------- #
def stage0_scale_invariance(M, pts, sigma_abs, dx_abs):
    """G0-a: R_FX1 must be invariant under M -> 7 M (analytic; assert numerically)."""
    var1, _ = bulk_variance(np.linalg.eigvalsh(M))
    g1, _, _, _ = gamma_dec_for(M, pts, sigma_abs, dx_abs)
    M7 = 7.0 * M
    var7, _ = bulk_variance(np.linalg.eigvalsh(M7))
    g7, _, _, _ = gamma_dec_for(M7, pts, sigma_abs, dx_abs)
    R1 = g1 / var1 if var1 > 0 else np.nan
    R7 = g7 / var7 if var7 > 0 else np.nan
    return abs(R1 - R7), R1


def stage0_goe_control(N, sigma_abs, dx_abs, rng):
    """G0-c: same R on a GOE random matrix with RANDOM spatial coords (no causal
    geometry). The 'generic spectrum, generic mode' reference value."""
    G = rng.standard_normal((N, N))
    M = (G + G.T) / np.sqrt(2.0 * N)        # GOE, O(1) spectrum
    pts = rng.random((N, 2))                # random 'spatial' coords (dim-2 shape)
    var, _ = bulk_variance(np.linalg.eigvalsh(M))
    g, _, _, _ = gamma_dec_for(M, pts, sigma_abs, dx_abs)
    return g / var if var > 0 else np.nan


# --------------------------------------------------------------------------- #
def run():
    results = {"meta": {"dims": DIMS, "Ns": NS, "sigmas": SIGMAS, "seeds": SEEDS,
                        "edge_frac": EDGE_FRAC, "dx_frac": DX_FRAC},
               "stage0": {}, "primary_BD": {}, "secondary_A": {}}

    # ---- Stage 0 gate (one representative config: dim2, N=200, mid sigma) ---- #
    rng = np.random.default_rng(20260627)
    pts = core.sprinkle(200, 2, rng)
    A = core.ancestor_matrix(pts)
    Mb = fs.bd_matrix(A)
    ext = spatial_extent(pts)
    sig = SIGMAS[1] * ext; dx = DX_FRAC * ext
    dR, Rrep = stage0_scale_invariance(Mb, pts, sig, dx)
    _, cross_frac, _, _ = gamma_dec_for(Mb, pts, sig, dx)
    goe_refs = [stage0_goe_control(200, SIGMAS[1], DX_FRAC, np.random.default_rng(1000 + s))
                for s in range(SEEDS)]
    results["stage0"] = {
        "scale_invariance_absdiff": dR,
        "scale_invariance_pass": bool(dR < 1e-6),
        "cross_frac": cross_frac,
        "cross_frac_pass": bool(cross_frac < 0.20),
        "R_representative": Rrep,
        "goe_control_median": float(np.median(goe_refs)),
        "goe_control_iqr": [float(np.percentile(goe_refs, 25)),
                            float(np.percentile(goe_refs, 75))],
    }

    # ---- Physics sweep ---- #
    for op_name, op_key, build in (("BD", "primary_BD", fs.bd_matrix),
                                   ("A", "secondary_A", fs.sym_adjacency)):
        for dim in DIMS:
            for N in NS:
                for si, sfrac in enumerate(SIGMAS):
                    Rvals = []
                    for seed in range(SEEDS):
                        rng = np.random.default_rng(7000 + 100 * dim + N + 10 * si + seed)
                        pts = core.sprinkle(N, dim, rng)
                        A = core.ancestor_matrix(pts)
                        M = build(A)
                        ext = spatial_extent(pts)
                        var, _ = bulk_variance(np.linalg.eigvalsh(M))
                        g, _, _, _ = gamma_dec_for(M, pts, sfrac * ext, DX_FRAC * ext)
                        if var > 0:
                            Rvals.append(g / var)
                    key = f"dim{dim}_N{N}_sig{sfrac}"
                    results[op_key][key] = {
                        "R_median": float(np.median(Rvals)),
                        "R_iqr": [float(np.percentile(Rvals, 25)),
                                  float(np.percentile(Rvals, 75))],
                        "n": len(Rvals),
                    }

    # ---- Pre-registered death-criteria evaluation (PRIMARY, BD) ---- #
    verdict = evaluate(results["primary_BD"], results["stage0"]["goe_control_median"])
    results["verdict"] = verdict

    out = HERE / "fx1_ratio.json"
    out.write_text(json.dumps(results, indent=2))
    print_summary(results)
    return results


def evaluate(prim, goe_med):
    """Apply the 4 pre-registered death criteria to the PRIMARY operator."""
    # crit 1: variation across sigma at fixed (dim,N)
    sigma_spreads = []
    for dim in DIMS:
        for N in NS:
            rs = [prim[f"dim{dim}_N{N}_sig{s}"]["R_median"] for s in SIGMAS]
            rs = np.array(rs)
            spread = (rs.max() - rs.min()) / np.median(np.abs(rs)) if np.median(np.abs(rs)) > 0 else np.inf
            sigma_spreads.append(spread)
    max_sigma_spread = float(np.max(sigma_spreads))
    crit1_sigma_rides = max_sigma_spread > 0.20

    # crit 2: systematic dim/N drift -- compare grand medians per dim and per N
    by_dim = {dim: np.median([prim[f"dim{dim}_N{N}_sig{s}"]["R_median"]
                              for N in NS for s in SIGMAS]) for dim in DIMS}
    by_N = {N: np.median([prim[f"dim{dim}_N{N}_sig{s}"]["R_median"]
                          for dim in DIMS for s in SIGMAS]) for N in NS}
    dim_spread = abs(by_dim[2] - by_dim[4]) / np.median([by_dim[2], by_dim[4]])
    N_vals = [by_N[N] for N in NS]
    N_spread = (max(N_vals) - min(N_vals)) / np.median(np.abs(N_vals))
    crit2_dimN_drift = bool(dim_spread > 0.20 or N_spread > 0.20)

    # crit 3: matches GOE control within +/-15%
    grand = float(np.median([v["R_median"] for v in prim.values()]))
    crit3_matches_goe = abs(grand - goe_med) / abs(goe_med) < 0.15 if goe_med else False

    # crit 4: matches Lindblad identity 0.5 within +/-15%
    crit4_definitional = abs(grand - 0.5) / 0.5 < 0.15

    novelty_dies = bool(crit1_sigma_rides or crit2_dimN_drift or crit3_matches_goe or crit4_definitional)
    return {
        "R_grand_median": grand,
        "max_sigma_spread": max_sigma_spread,
        "by_dim": {str(k): float(v) for k, v in by_dim.items()},
        "by_N": {str(k): float(v) for k, v in by_N.items()},
        "dim_spread": float(dim_spread),
        "N_spread": float(N_spread),
        "goe_control_median": float(goe_med),
        "crit1_sigma_rides": bool(crit1_sigma_rides),
        "crit2_dimN_drift": crit2_dimN_drift,
        "crit3_matches_goe": bool(crit3_matches_goe),
        "crit4_definitional_half": bool(crit4_definitional),
        "NOVELTY_DIES": novelty_dies,
        "outcome": ("H_nulo/H_trivial (CLASSE GRANDE selado)" if novelty_dies
                    else "H_novidade (candidato sobrevive)"),
    }


def print_summary(r):
    s0 = r["stage0"]; v = r["verdict"]
    print("=== FX1 Stage 0 (engineering gate) ===")
    print(f"  scale-invariance |dR|={s0['scale_invariance_absdiff']:.2e} pass={s0['scale_invariance_pass']}")
    print(f"  cross_frac={s0['cross_frac']:.3f} pass={s0['cross_frac_pass']}")
    print(f"  GOE control R median={s0['goe_control_median']:.3f} IQR={s0['goe_control_iqr']}")
    print("=== FX1 PRIMARY (BD) R_FX1 = Gamma_dec / Var_bulk ===")
    for dim in DIMS:
        for N in NS:
            row = [f"{r['primary_BD'][f'dim{dim}_N{N}_sig{sg}']['R_median']:.3f}" for sg in SIGMAS]
            print(f"  dim{dim} N{N}: sig{SIGMAS} -> R = [{', '.join(row)}]")
    print("=== Death-criteria evaluation (PRIMARY) ===")
    for k in ("R_grand_median", "max_sigma_spread", "dim_spread", "N_spread",
              "goe_control_median", "crit1_sigma_rides", "crit2_dimN_drift",
              "crit3_matches_goe", "crit4_definitional_half", "NOVELTY_DIES", "outcome"):
        print(f"  {k}: {v[k]}")


if __name__ == "__main__":
    run()

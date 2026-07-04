"""FS1 -- Lindblad bridge.

Pre-registered in FS_PRE_REGISTRO.md (frozen 2026-06-22). Tests whether the
causal operator (a) generates a positive (CP / Lindblad) generator and (b) gives
a decoherence rate that scales as separation^2 (SR's localization signature,
L_hat = x_hat/sigma_x). Extends FD2 (which found the WIDTH scaling sigma_x^-2).

FS1-A (positivity): channel-rate sign census treating the operator eigenvalues as
Lindblad channel rates, for the Lorentzian (signed BD) vs Euclidean (|lambda|,
validated in c5) continuations. CP <=> all rates >= 0.

FS1-B (separation^2): Gamma_dec(Dx) between two width-sigma Gaussian spatial modes
separated by Dx, exact single-Hermitian-Lindblad off-diagonal decay rate. Fit the
separation-induced part Delta_Gamma ~ Dx^q. SURVIVE if q in [1.7,2.3], R2>=0.90.
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone

import numpy as np

import sr_teic_core as core
import c5_core as c5
import fs_core as fs

DIMS = [2, 4]
N_MAIN = 400
SEEDS = list(range(10))
SIGMAS = [0.08, 0.12, 0.18]                 # fixed coherence widths (FD2 range)
DX = np.geomspace(0.02, 0.40, 12)            # separations: spacing .. ~half system


def two_modes(pts, sigma, dx):
    """Two Gaussian modes separated by dx along the first SPATIAL axis, placed
    symmetrically about the spatial centroid."""
    x = pts[:, 1:]
    c = x.mean(axis=0)
    e = np.zeros(x.shape[1]); e[0] = 1.0
    c1 = c - 0.5 * dx * e
    c2 = c + 0.5 * dx * e
    return fs.spatial_mode(pts, sigma, c1), fs.spatial_mode(pts, sigma, c2)


def run():
    payload = {"experiment": "FS1_lindblad", "frozen": "FS_PRE_REGISTRO.md",
               "dims": DIMS, "N": N_MAIN, "seeds": SEEDS,
               "sigmas": SIGMAS, "dx": DX.tolist(), "A": {}, "B": {}}
    linesA, linesB = [], []

    for dim in DIMS:
        # accumulate over seeds
        censusL = {"min_rate_rel": [], "n_neg": [], "is_CP": []}   # Lorentzian (signed)
        censusE = {"min_rate_rel": [], "n_neg": [], "is_CP": []}   # Euclidean (|lambda|)
        # FS1-B: Gamma_dec(dx) per sigma, both operators
        GdecBD = {s: np.zeros((len(SEEDS), len(DX))) for s in SIGMAS}
        GdecAS = {s: np.zeros((len(SEEDS), len(DX))) for s in SIGMAS}

        for si, sd in enumerate(SEEDS):
            rng = np.random.default_rng(70000 * dim + sd)
            pts = core.sprinkle(N_MAIN, dim, rng)
            A = core.ancestor_matrix(pts)
            M_bd = fs.bd_matrix(A)                    # signed BD matrix
            M_as = fs.sym_adjacency(A)               # collapse operator

            # --- FS1-A: channel-rate sign census ---
            ev_signed = np.linalg.eigvalsh(M_bd)     # Lorentzian channel rates
            ev_eucl = np.abs(ev_signed)              # Euclidean continuation (c5)
            cL = fs.kossakowski_sign_census(ev_signed)
            cE = fs.kossakowski_sign_census(ev_eucl)
            for k in censusL:
                censusL[k].append(cL[k]); censusE[k].append(cE[k])

            # --- FS1-B: decoherence rate vs separation ---
            for s in SIGMAS:
                for di, dx in enumerate(DX):
                    p1, p2 = two_modes(pts, s, dx)
                    GdecBD[s][si, di] = fs.decoherence_rate(M_bd, p1, p2)
                    GdecAS[s][si, di] = fs.decoherence_rate(M_as, p1, p2)

        # ---- FS1-A summary ----
        A_summary = {
            "Lorentzian_signed": {
                "mean_min_rate_rel": float(np.mean(censusL["min_rate_rel"])),
                "mean_n_neg": float(np.mean(censusL["n_neg"])),
                "frac_CP": float(np.mean(censusL["is_CP"]))},
            "Euclidean_abs": {
                "mean_min_rate_rel": float(np.mean(censusE["min_rate_rel"])),
                "mean_n_neg": float(np.mean(censusE["n_neg"])),
                "frac_CP": float(np.mean(censusE["is_CP"]))},
        }
        cp_any = (A_summary["Lorentzian_signed"]["frac_CP"] > 0.5 or
                  A_summary["Euclidean_abs"]["frac_CP"] > 0.5)
        needs_eucl = (A_summary["Euclidean_abs"]["frac_CP"] > 0.5 and
                      A_summary["Lorentzian_signed"]["frac_CP"] <= 0.5)
        A_summary["verdict_A"] = ("SOBREVIVE-CP" if cp_any else "MORTE-nao-CP")
        A_summary["CP_requires_Euclidean_continuation"] = bool(needs_eucl)
        payload["A"][f"dim{dim}"] = A_summary
        linesA.append(f"  dim={dim}: Lorentzian frac_CP={A_summary['Lorentzian_signed']['frac_CP']:.2f} "
                      f"(min_rate_rel={A_summary['Lorentzian_signed']['mean_min_rate_rel']:+.3f}); "
                      f"Euclidean frac_CP={A_summary['Euclidean_abs']['frac_CP']:.2f} "
                      f"-> {A_summary['verdict_A']}"
                      + ("  [CP exige continuacao Euclidiana]" if needs_eucl else ""))

        # ---- FS1-B summary: fit Delta_Gamma ~ dx^q per sigma & operator ----
        B_summary = {}
        for opname, Gdict in (("M_BD", GdecBD), ("A_sym", GdecAS)):
            for s in SIGMAS:
                g = Gdict[s].mean(0)                  # mean over seeds
                g0 = float(g[0])                       # baseline (smallest dx ~ Dx->0)
                dgamma = g - g0
                # relative variation across the window
                rel_var = float((np.max(np.abs(dgamma)) / abs(g0)) if abs(g0) > 0 else np.inf)
                # fit positive-going part (dgamma may be +/-); use |dgamma|
                q, r2 = fs.fit_power(DX[1:], np.abs(dgamma[1:]))
                flat = rel_var < 0.05
                if flat:
                    verdict = "MORTE-plana (sem Dx^2)"
                elif (1.7 <= q <= 2.3) and r2 >= 0.90:
                    verdict = "SOBREVIVE (Dx^2)"
                elif r2 < 0.80:
                    verdict = f"MORTE-sem-lei (q={q:.2f},R2={r2:.2f})"
                else:
                    verdict = f"FORA-de-Dx^2 (q={q:.2f},R2={r2:.2f})"
                B_summary[f"{opname}_sigma{s}"] = {
                    "gamma0": g0, "gamma_mean": g.tolist(),
                    "q": q, "R2": r2, "rel_var": rel_var, "verdict": verdict}
                linesB.append(f"  dim={dim} {opname:6s} sigma={s:.2f}: "
                              f"q={q:+.2f} R2={r2:.2f} relvar={rel_var:.3f}  {verdict}")
        payload["B"][f"dim{dim}"] = B_summary

    # ---- overall FS1 verdict ----
    cp_ok = all(payload["A"][f"dim{d}"]["verdict_A"].startswith("SOBREVIVE") for d in DIMS)
    dx2_any = any(v["verdict"].startswith("SOBREVIVE")
                  for d in DIMS for v in payload["B"][f"dim{d}"].values())
    if cp_ok and dx2_any:
        overall = "SOBREVIVE (CP + Dx^2)"
    elif cp_ok and not dx2_any:
        overall = "PARCIAL/B (gerador CP, mas decoerencia NAO escala Dx^2)"
    elif not cp_ok and dx2_any:
        overall = "PARCIAL (Dx^2 sim, CP nao)"
    else:
        overall = "MORTE (nem CP nem Dx^2)"
    payload["verdict_FS1"] = overall

    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    (core.HERE / "fs1_lindblad.json").write_text(json.dumps(payload, indent=2))

    print("=" * 78)
    print("FS1 -- Lindblad bridge")
    print("=" * 78)
    print("FS1-A  positividade (CP):")
    print("\n".join(linesA))
    print("-" * 78)
    print("FS1-B  decoerencia vs separacao (alvo q=+2, SR):")
    print("\n".join(linesB))
    print("-" * 78)
    print(f"VEREDITO FS1: {overall}")


if __name__ == "__main__":
    run()

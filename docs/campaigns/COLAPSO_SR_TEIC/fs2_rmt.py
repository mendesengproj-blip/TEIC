"""FS2 -- Dyson Brownian Motion / Random Matrix Theory.

Pre-registered in FS_PRE_REGISTRO.md (frozen 2026-06-22). Tests whether the
spectrum of the validated causal operators exhibits Dyson eigenvalue REPULSION
(GOE, <r>=0.5307) as SR's DBM derivation requires, or Poissonian spacing
(<r>=0.38629, integrable, no repulsion).

Discriminator: consecutive level-spacing ratio <r> (Atas et al 2013),
unfolding-free. Operators: A_sym (collapse, PRIMARY), L_link (geometry),
M_BD signed (causal d'Alembertian). dim in {2,4}; N in {100,200,400}; >=12 seeds.

KILL (A_sym primary): <r> <= 0.42 stable in N -> no Dyson repulsion (MORTE).
SURVIVE: <r> >= 0.50 N-stable, seed-robust -> DBM/RMT confirmed.
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone

import numpy as np

import sr_teic_core as core
import fs_core as fs

DIMS = [2, 4]
NS = [100, 200, 400]
SEEDS = list(range(12))

OPS = (
    ("A_sym", fs.sym_adjacency),       # PRIMARY (SR collapse operator)
    ("L_link", fs.link_laplacian),     # geometry sector
    ("M_BD", fs.bd_matrix),            # causal d'Alembertian (signed)
)


def run():
    payload = {"experiment": "FS2_dyson_rmt", "frozen": "FS_PRE_REGISTRO.md",
               "R_Poisson": fs.R_POISSON, "R_GOE": fs.R_GOE,
               "dims": DIMS, "Ns": NS, "seeds": SEEDS, "by": {}}
    lines = []
    for dim in DIMS:
        for opname, opfun in OPS:
            for N in NS:
                r_all = []
                deg_total = 0
                for sd in SEEDS:
                    rng = np.random.default_rng(90000 * dim + 100 * N + sd)
                    pts = core.sprinkle(N, dim, rng)
                    A = core.ancestor_matrix(pts)
                    M = opfun(A)
                    ev = np.linalg.eigvalsh(M)
                    r, n_deg = fs.gap_ratios(ev)
                    r_all.append(r)
                    deg_total += n_deg
                r_all = np.concatenate(r_all) if r_all else np.array([])
                r_mean = float(np.mean(r_all)) if r_all.size else float("nan")
                r_sem = float(np.std(r_all) / np.sqrt(r_all.size)) if r_all.size else float("nan")
                key = f"dim{dim}_{opname}_N{N}"
                payload["by"][key] = {
                    "r_mean": r_mean, "r_sem": r_sem, "n_ratios": int(r_all.size),
                    "n_degenerate": deg_total, "class": fs.classify_r(r_mean)}
                lines.append(f"  dim={dim} {opname:7s} N={N:4d}: <r>={r_mean:.4f} "
                             f"+-{r_sem:.4f} (deg={deg_total})  {fs.classify_r(r_mean)}")
            lines.append("")

    # N-stability of the PRIMARY operator A_sym, per dim
    stab = {}
    for dim in DIMS:
        rs = [payload["by"][f"dim{dim}_A_sym_N{N}"]["r_mean"] for N in NS]
        drift = float(max(rs) - min(rs))
        stab[f"dim{dim}_A_sym"] = {"r_by_N": rs, "drift": drift,
                                   "N_stable": bool(drift < 0.03)}
    payload["N_stability_primary"] = stab

    # Verdict on the PRIMARY operator (largest N, both dims)
    verdicts = {}
    for dim in DIMS:
        rm = payload["by"][f"dim{dim}_A_sym_N{max(NS)}"]["r_mean"]
        if rm <= 0.42:
            v = "MORTE (Poisson, sem repulsao)"
        elif rm >= 0.50:
            v = "SOBREVIVE (GOE/DBM)"
        else:
            v = "INTERMEDIARIO"
        verdicts[f"dim{dim}"] = {"r_mean_maxN": rm, "verdict": v}
    payload["verdict_primary"] = verdicts

    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    (core.HERE / "fs2_rmt.json").write_text(json.dumps(payload, indent=2))

    print("=" * 78)
    print("FS2 -- Dyson Brownian Motion / RMT  (Poisson<r>=0.3863  GOE<r>=0.5307)")
    print("=" * 78)
    print("\n".join(lines))
    print("-" * 78)
    print("N-stability (PRIMARY A_sym):")
    for k, v in stab.items():
        print(f"  {k}: r_by_N={['%.4f'%x for x in v['r_by_N']]} drift={v['drift']:.4f} "
              f"N_stable={v['N_stable']}")
    print("VERDICT (primary A_sym):")
    for k, v in verdicts.items():
        print(f"  {k}: <r>={v['r_mean_maxN']:.4f} -> {v['verdict']}")


if __name__ == "__main__":
    run()

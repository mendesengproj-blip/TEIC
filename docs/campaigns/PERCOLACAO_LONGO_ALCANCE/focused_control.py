"""
focused_control.py -- completa o criterio 5 do PRE_REGISTRO: C4 da familia vs
CONTROLE ALEATORIO de mesma densidade de arestas, por sigma, no maior N medido.

Um C4 so conta como "nao-trivial" (criterio de janela) se ficar ACIMA do controle.
Reutiliza longrange_percolation VERBATIM (mesmo gerador, mesmo estimador).
"""
import json
import os

import numpy as np

import longrange_percolation as L

HERE = os.path.dirname(os.path.abspath(__file__))

SIGMAS = L.SIGMAS
N_SEEDS = 3


def run():
    out = {"observable": "C4 family vs random-density control at top N per sigma",
           "n_seeds": N_SEEDS, "rows": []}
    for sigma in SIGMAS:
        ncap = L.n_cap_for(sigma)
        n_target = max(n for n in L.LADDER if n <= ncap)
        rho = n_target / L.VOL
        dtau0 = L.dtau0_for(rho)
        c4f, c4r, zz = [], [], []
        for s in range(N_SEEDS):
            pts = L.sprinkle_box(rho, L.BOUNDS, np.random.default_rng(40_000 + s + n_target))
            n = pts.shape[0]
            edges, info, pool = L.longrange_edges(
                pts, sigma, dtau0, np.random.default_rng(50_000 + s + n_target))
            src, dst, _ = pool
            mf = L.clustering_metrics(n, edges)
            er = L.random_control_edges(src, dst, info["n_edges"],
                                        np.random.default_rng(60_000 + s + n_target))
            mr = L.clustering_metrics(n, er)
            c4f.append(mf["mean_local_square"]); c4r.append(mr["mean_local_square"])
            zz.append(mf["deg_mean"])
        fam, rnd = float(np.mean(c4f)), float(np.mean(c4r))
        row = {"sigma": sigma, "N": n_target, "z": float(np.mean(zz)),
               "C4_family": fam, "C4_random_control": rnd,
               "ratio_fam_over_rnd": fam / rnd if rnd else float("nan"),
               "above_control": bool(fam > rnd)}
        out["rows"].append(row)
        print(f"  sigma={sigma:>4} N~{n_target:>4}: z={np.mean(zz):6.1f} "
              f"C4_fam={fam:.4f} C4_rnd={rnd:.4f} ratio={fam/rnd:.3f} "
              f"{'ABOVE' if fam > rnd else 'below'}")
    n_above = sum(r["above_control"] for r in out["rows"])
    out["n_sigma_above_control"] = n_above
    out["any_above_control"] = n_above > 0
    print(f"\n  sigmas com C4 ACIMA do controle aleatorio: {n_above}/{len(SIGMAS)}")
    json.dump(out, open(os.path.join(HERE, "control_c4.json"), "w"), indent=2)
    return out


if __name__ == "__main__":
    print("=" * 60 + "\nCONTROLE DE TRIVIALITY DO C4 (criterio 5)\n" + "=" * 60)
    run()

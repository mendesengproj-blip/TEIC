"""E5_1b_controlled.py -- E5-1 redone with CONTROLLED plaquette geometry + 4 sizes.

Fixes the confound of E5-1: a Lorentz-invariant proper-time cutoff tau_max
(e5_local.LocalCausalGraph) holds the LOCAL geometry fixed (mean degree, diamonds
per link) while the event number N grows, so the finite-size scaling of the
specific heat compares like with like.

CONTROL CHECK (printed first): mean degree and plaquettes-per-link must stay
~constant across sizes; if they drift, the FSS is still confounded and we say so.

Then: C/N_plaq peak vs N over 4 sizes, fit exponent p in C/N_plaq ~ N^p.
  p ~ 1  -> first-order-like (transition / possible deconfinement -> photon candidate)
  p ~ 0  -> crossover (confines at all beta -> no photon in the link sector)
Uses the validated fast engine.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e5_core import causal_diamond_plaquettes   # noqa: E402
from e5_fast import FastU1Gauge                  # noqa: E402
from e5_local import LocalCausalGraph            # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box             # noqa: E402


def build(L_box, rho, tau_max, seed=0):
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = LocalCausalGraph(pts, tau_max)
    Lk, pl, ps = causal_diamond_plaquettes(g, max_per_pair=2, seed=seed)
    return g, pl, ps


def scan(g, pl, ps, betas, n_seeds=3, n_burn=150, n_meas=100):
    L = g.edges.shape[0]
    Nplaq = pl.shape[0]
    Cpp = np.zeros(len(betas)); meanP = np.zeros(len(betas))
    for ib, beta in enumerate(betas):
        mc = []
        for s in range(n_seeds):
            gg = FastU1Gauge(L, pl, ps, beta=beta, seed=777 * ib + s)
            gg.equilibrate(n_burn)
            mc.append(gg.measure_plaq(n_meas))
        mc = np.concatenate(mc)
        meanP[ib] = mc.mean(); Cpp[ib] = beta ** 2 * Nplaq * mc.var()
    return meanP, Cpp, Nplaq


def main():
    t0 = time.time()
    rho, tau_max = 0.4, 3.0
    Ls = [5.0, 6.0, 7.0, 8.0]
    betas = np.array([0.6, 1.0, 1.5, 2.0, 2.5, 3.0])

    rows = []
    print(f"CONTROL CHECK (rho={rho}, tau_max={tau_max}): geometry should be ~constant")
    geoms = []
    for Lb in Ls:
        g, pl, ps = build(Lb, rho, tau_max, seed=1)
        deg = g.mean_degree()
        ppl = pl.shape[0] / max(g.edges.shape[0], 1)   # plaquettes per link
        geoms.append((g, pl, ps, deg, ppl))
        print(f"  L={Lb}: N={g.n} links={g.edges.shape[0]} <deg>={deg:.1f} "
              f"plaq={pl.shape[0]} plaq/link={ppl:.2f}", flush=True)

    degs = np.array([gm[3] for gm in geoms])
    ppls = np.array([gm[4] for gm in geoms])
    deg_cv = float(degs.std() / degs.mean())
    ppl_cv = float(ppls.std() / ppls.mean())
    controlled = deg_cv < 0.15 and ppl_cv < 0.20
    print(f"  geometry CV: degree {deg_cv:.2f}, plaq/link {ppl_cv:.2f} -> "
          f"{'CONTROLLED' if controlled else 'STILL DRIFTING'}")

    print("\nFSS scan:")
    for (g, pl, ps, deg, ppl), Lb in zip(geoms, Ls):
        meanP, Cpp, Nplaq = scan(g, pl, ps, betas)
        j = int(np.argmax(Cpp))
        rows.append({"L_box": Lb, "n_events": g.n, "n_plaq": int(Nplaq),
                     "mean_degree": deg, "plaq_per_link": ppl,
                     "mean_plaq": meanP.tolist(), "C_per_plaq": Cpp.tolist(),
                     "peak_beta": float(betas[j]), "C_per_plaq_peak": float(Cpp[j])})
        print(f"  L={Lb}: N={g.n} C/N_plaq peak={Cpp[j]:.3e} at beta={betas[j]:.1f} "
              f"(<cos> {meanP.min():.2f}->{meanP.max():.2f})", flush=True)

    N = np.array([r["n_events"] for r in rows], float)
    C = np.array([r["C_per_plaq_peak"] for r in rows], float)
    expo = float(np.polyfit(np.log(N), np.log(C), 1)[0])

    if not controlled:
        verdict = (f"STILL CONFOUNDED: geometry not constant (deg CV {deg_cv:.2f}, "
                   f"plaq/link CV {ppl_cv:.2f}); retune tau_max before reading FSS.")
        tag = "CONFOUNDED"
    elif expo > 0.8:
        verdict = (f"DECONFINEMENT-LEANING: with CONTROLLED geometry, C/N_plaq ~ "
                   f"N^{expo:.2f} (first-order-like ~1) -> a transition; a photon "
                   f"candidate may exist. Next: Wilson-loop area law + E5-2 dispersion.")
        tag = "DECONFINEMENT"
    elif expo < 0.25:
        verdict = (f"CONFINING: with CONTROLLED geometry, C/N_plaq ~ N^{expo:.2f} "
                   f"(crossover-like ~0) -> the causal-set U(1) confines at all beta; "
                   f"NO massless photon in the link sector. Combined with E4 (scalars), "
                   f"the emergent photon is excluded from every sector tested.")
        tag = "CONFINING"
    else:
        verdict = (f"INCONCLUSIVE: controlled geometry but C/N_plaq ~ N^{expo:.2f} "
                   f"(between 0 and 1); more sizes/seeds or wider beta needed.")
        tag = "INCONCLUSIVE"

    out = {"rho": rho, "tau_max": tau_max, "Ls": Ls, "betas": betas.tolist(),
           "rows": rows, "deg_cv": deg_cv, "ppl_cv": ppl_cv,
           "geometry_controlled": bool(controlled),
           "C_per_plaq_exponent": expo, "verdict": verdict, "verdict_tag": tag,
           "runtime_s": time.time() - t0}
    (HERE / "E5_1b_controlled.json").write_text(json.dumps(out, indent=2))
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.0f}s -> E5_1b_controlled.json")


if __name__ == "__main__":
    main()

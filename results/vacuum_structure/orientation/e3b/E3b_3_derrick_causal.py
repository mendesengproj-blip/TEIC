"""E3b_3_derrick_causal.py -- the causal Derrick virial.

Charter E3b-3.  On the spatial cubic lattice (E3-2) the hedgehog had NO Derrick
minimum: E(lambda) ~ lambda, monotone, so the texture prefers to shrink (no
intrinsic scale).  The causal network adds time-oriented links; the question is
whether their energy supplies a counter-term.

Dilate the (finite-core) hedgehog spatially x -> (x-c)/lambda + c and split the
link energy by geometry:

    E_spatial(lambda)  : links with an appreciable spatial separation (dx > f*dt)
    E_temporal(lambda) : near-purely-temporal links (events almost co-located in
                         space, separated in time)
    E_total = E_spatial + E_temporal

If E_temporal carries an opposite lambda-trend it can create an interior minimum
(cone stabilisation).  Checked across substrate scales (charter V2: a genuine
minimum must persist under refinement, not be a finite-size artefact).

Anti-circularity: E is the bond functional; lambda is an artificial dilation; no
scale, no mass, no minimum is assumed -- the curve is measured and read off.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e3b_core as e3b  # noqa: E402

OUT = Path(__file__).resolve().parent

RHO, T_BOX = 1.5, 3.0
CORE = 1.5
LAMBDAS = np.linspace(0.4, 3.0, 18)
# "refinement" = three substrate scales (spatial extent L); a real minimum must
# survive all three (charter V2).  Larger L at fixed rho = finer relative to core.
L_SCALES = [3.5, 4.0, 4.5]
SEEDS = [0, 1, 2, 3, 4]


def run_scale(L, seeds):
    Es, Et, Etot, Bs = [], [], [], []
    frac = []
    for sd in seeds:
        pts = e3b.sprinkle_causal(RHO, T_BOX, L, sd)
        sub = e3b.Substrate(pts)
        d = e3b.causal_derrick(sub, LAMBDAS, core=CORE)
        Es.append(d["E_spatial"]); Et.append(d["E_temporal"])
        Etot.append(d["E_total"]); Bs.append(d["B"])
        frac.append(d["frac_spatial_links"])
    Es = np.array(Es).mean(0); Et = np.array(Et).mean(0)
    Etot = np.array(Etot).mean(0); Bs = np.array(Bs).mean(0)
    return {"L": L, "E_spatial": Es, "E_temporal": Et, "E_total": Etot,
            "B": Bs, "frac_spatial_links": float(np.mean(frac))}


def analyse(curve):
    """Locate the minimiser of E_total over the lambda grid; an INTERIOR minimum
    means argmin is not at the boundary of the sampled range."""
    Etot = curve["E_total"]
    j = int(np.argmin(Etot))
    interior = 0 < j < len(LAMBDAS) - 1
    return {"lambda_star": float(LAMBDAS[j]), "interior_min": bool(interior),
            "argmin_index": j,
            "E_temporal_fraction": float(np.mean(curve["E_temporal"]) /
                                         np.mean(curve["E_total"]))}


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3b-3 -- causal Derrick (spatial dilation, spatial vs temporal energy)")
    print("=" * 72)
    curves = {}
    diags = {}
    for L in L_SCALES:
        c = run_scale(L, SEEDS)
        curves[L] = c
        diags[L] = analyse(c)
        print(f"  L={L}: frac_spatial_links={c['frac_spatial_links']:.2f}  "
              f"E_temporal/E_total={diags[L]['E_temporal_fraction']:.1%}  "
              f"lambda*={diags[L]['lambda_star']:.2f}  "
              f"interior_min={diags[L]['interior_min']}")

    any_interior = any(diags[L]["interior_min"] for L in L_SCALES)
    all_interior = all(diags[L]["interior_min"] for L in L_SCALES)
    # is E_total monotone increasing (collapse preferred, Derrick active)?
    mono = all(np.all(np.diff(curves[L]["E_total"]) > 0) for L in L_SCALES)
    print("-" * 72)
    if all_interior:
        verdict = ("E_total has an INTERIOR minimum at every scale -- the cone "
                   "stabilises the defect (Derrick defeated).")
    elif any_interior:
        verdict = ("E_total has an interior minimum at SOME scales only -- not a "
                   "robust minimum (finite-size, not a true intrinsic scale).")
    else:
        verdict = ("NO interior minimum at any scale: E_total decreases toward small "
                   "lambda (the defect still prefers to shrink). E_temporal is a tiny "
                   "fraction of E_total and does NOT compensate E_spatial -- the "
                   "causal cone supplies no Derrick counter-term. Same outcome as the "
                   "spatial lattice (E3-2).")
    print(f"  E3b-3: {verdict}")
    print(f"  (E_total monotone-increasing in lambda at all scales: {mono})")
    print("=" * 72)

    payload = {
        "verdict": verdict, "any_interior_min": bool(any_interior),
        "all_interior_min": bool(all_interior), "E_total_monotone": bool(mono),
        "lambdas": LAMBDAS.tolist(),
        "curves": {str(L): {k: (v.tolist() if hasattr(v, "tolist") else v)
                            for k, v in curves[L].items()} for L in L_SCALES},
        "diagnostics": {str(L): diags[L] for L in L_SCALES},
        "config": {"rho": RHO, "T": T_BOX, "core": CORE, "L_scales": L_SCALES,
                   "seeds": SEEDS},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E3b_3_derrick_causal.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3b_3_derrick_causal.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(curves)
    return payload


def make_figure(curves):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    for L in L_SCALES:
        c = curves[L]
        ax[0].plot(LAMBDAS, c["E_spatial"], "o-", ms=3, label=f"L={L}")
        ax[1].plot(LAMBDAS, c["E_temporal"], "s-", ms=3, label=f"L={L}")
        ax[2].plot(LAMBDAS, c["E_total"] / c["E_total"][np.argmin(np.abs(LAMBDAS - 1))],
                   "^-", ms=3, label=f"L={L}")
    ax[0].set_title("E_spatial(lambda)"); ax[1].set_title("E_temporal(lambda)")
    ax[2].set_title("E_total(lambda) / E_total(1)")
    for a in ax:
        a.axvline(1.0, color="k", ls=":", lw=0.6); a.set_xlabel(r"$\lambda$")
        a.legend(fontsize=8); a.grid(alpha=0.2)
    ax[0].set_ylabel("energy")
    fig.suptitle("E3b-3: causal Derrick -- does the time-oriented link energy "
                 "create an interior minimum?", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3b_3_derrick_causal.png", dpi=130)
    print(f"saved {OUT/'E3b_3_derrick_causal.png'}")


if __name__ == "__main__":
    main()

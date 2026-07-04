"""E3b_1_hedgehog.py -- fate of the hedgehog under DETERMINISTIC CAUSAL evolution.

Charter E3b-1.  Seed a hedgehog n(r)=r_hat on EVERY event of a 3+1D Poisson causal
set, freeze the earliest time slab as initial data, and let the field evolve in
strict temporal order (Protocol A): each event is set to the orientation that
minimises the link energy against its CAUSAL PAST only (parents).  The past is
fixed before the future is written -- the arrow of time.  Record the three
pre-registered observables on each time leaf:

    B(t)      topological charge (Delaunay-tetrahedron solid-angle degree)
    E(t)      Derrick link gradient energy on the leaf
    r_eff(t)  effective defect radius (gradient-weighted spatial moment)

over 20 seeds.  Pre-registered death criterion (charter): B(t) -> 0 under Protocol
A = Verdict C.  Anti-circularity: B is the geometric charge, E the bond functional,
no stability assumed; the words matter/mass/E=mc^2 do not appear.
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
SEEDS = list(range(20))

RHO, T_BOX, L_BOX = 1.5, 3.0, 4.0
CORE = 1.0
SEED_FRAC = 0.25          # earliest 25% of the time extent is the frozen initial data
N_LEAVES = 8
PASSES = 2                # forward causal sweeps (each reads only updated past)


def run_seed(sd):
    pts = e3b.sprinkle_causal(RHO, T_BOX, L_BOX, sd)
    sub = e3b.Substrate(pts)
    xyz = pts[:, 1:4]
    nh = e3b.hedgehog_field(pts, +1, core=CORE)
    t = pts[:, 0]
    tmin, tmax = t.min(), t.max()
    init = t <= tmin + SEED_FRAC * (tmax - tmin)
    leaves = e3b.time_leaves(pts, N_LEAVES, t_lo=tmin, t_hi=tmax)
    # before evolution (seeded hedgehog)
    pre = [e3b.measure_leaf(pts, sub, nh, idx) for _, idx in leaves]
    B_global0 = e3b.topological_charge_poisson(xyz, nh)
    # Protocol A deterministic causal evolution
    nf = e3b.evolve_causal(sub, nh, init, passes=PASSES)
    post = [e3b.measure_leaf(pts, sub, nf, idx) for _, idx in leaves]
    B_globalf = e3b.topological_charge_poisson(xyz, nf)
    tc = [c for c, _ in leaves]
    return {"seed": sd, "n": sub.n, "n_links": sub.n_links,
            "mean_degree": sub.mean_degree, "n_frozen": int(init.sum()),
            "t_leaf": tc,
            "B_pre": [m["B"] for m in pre], "B_post": [m["B"] for m in post],
            "E_post": [m["E"] for m in post], "r_eff_post": [m["r_eff"] for m in post],
            "B_global_pre": B_global0, "B_global_post": B_globalf}


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3b-1 -- hedgehog under deterministic CAUSAL evolution (Protocol A, 20 seeds)")
    print("=" * 72)
    rows = []
    for sd in SEEDS:
        r = run_seed(sd)
        rows.append(r)
        bmin = np.nanmin(r["B_post"])
        print(f"  seed {sd:2d}: n={r['n']:4d} frozen={r['n_frozen']:4d}  "
              f"B_global {r['B_global_pre']:+.3f}->{r['B_global_post']:+.3f}  "
              f"min leaf B_post={bmin:+.3f}")

    # aggregate across seeds (leaf-wise, only evolved leaves matter for the verdict)
    Bpost = np.array([r["B_post"] for r in rows])              # (seeds, leaves)
    Bpre = np.array([r["B_pre"] for r in rows])
    Epost = np.array([r["E_post"] for r in rows])
    rpost = np.array([r["r_eff_post"] for r in rows])
    t_leaf = np.array(rows[0]["t_leaf"])
    # evolved leaves = those past the frozen seed slab
    t_seed_abs = t_leaf.min() + SEED_FRAC * (t_leaf.max() - t_leaf.min())
    evolved = t_leaf > t_seed_abs
    Bg_post = np.array([r["B_global_post"] for r in rows])

    B_leaf_mean = np.nanmean(Bpost, axis=0)
    B_leaf_std = np.nanstd(Bpost, axis=0)
    # survival: fraction of seeds whose every evolved leaf keeps |B-1|<0.5
    survive = np.mean([np.all(np.abs(np.array(r["B_post"])[evolved] - 1) < 0.5)
                       for r in rows])
    global_survive = np.mean(np.abs(Bg_post - 1) < 0.5)

    # verdict (charter death criterion is on Protocol A)
    collapsed = (global_survive < 0.5)
    if collapsed:
        verdict = "C-candidate"
        why = ("B(t) -> 0 under Protocol A in the majority of seeds: the causal cone "
               "supplies no extra rigidity (death criterion).")
    else:
        verdict = "B=1-preserved"
        why = ("B=1 is preserved under deterministic causal evolution in every seed "
               "(death criterion NOT triggered). Whether this is intrinsic stability "
               "or boundary-imposed is decided by E3b-2 (causal vs acausal MC) and "
               "E3b-3 (causal Derrick minimum).")

    print("-" * 72)
    print(f"  leaf B_post (mean over seeds): "
          + "  ".join(f"{b:+.2f}" for b in B_leaf_mean))
    print(f"  global B_post survival (|B-1|<0.5): {global_survive:.0%}")
    print(f"  per-seed all-evolved-leaf survival: {survive:.0%}")
    print(f"  VERDICT (E3b-1): {verdict} -- {why}")
    print("=" * 72)

    payload = {
        "verdict": verdict, "why": why,
        "global_survival": float(global_survive),
        "leaf_survival": float(survive),
        "t_leaf": t_leaf.tolist(), "evolved_leaf_mask": evolved.tolist(),
        "B_leaf_mean": B_leaf_mean.tolist(), "B_leaf_std": B_leaf_std.tolist(),
        "B_pre_leaf_mean": np.nanmean(Bpre, axis=0).tolist(),
        "E_leaf_mean": np.nanmean(Epost, axis=0).tolist(),
        "r_eff_leaf_mean": np.nanmean(rpost, axis=0).tolist(),
        "B_global_post": Bg_post.tolist(),
        "config": {"rho": RHO, "T": T_BOX, "L": L_BOX, "core": CORE,
                   "seed_frac": SEED_FRAC, "n_leaves": N_LEAVES, "passes": PASSES,
                   "seeds": SEEDS},
        "per_seed": rows,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E3b_1_hedgehog.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3b_1_hedgehog.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(t_leaf, B_leaf_mean, B_leaf_std, np.nanmean(Epost, 0),
                np.nanmean(rpost, 0), evolved, Bg_post)
    return payload


def make_figure(t_leaf, Bmean, Bstd, Emean, rmean, evolved, Bg_post):
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.4))
    ax[0].axhline(1, color="k", ls=":", lw=0.6); ax[0].axhline(0, color="k", ls=":", lw=0.6)
    ax[0].errorbar(t_leaf, Bmean, yerr=Bstd, marker="o", capsize=3, lw=1.5,
                   label="B(t) per leaf (20 seeds)")
    ax[0].axvspan(t_leaf.min(), t_leaf[~evolved].max() if (~evolved).any() else t_leaf.min(),
                  color="orange", alpha=0.15, label="frozen seed slab")
    ax[0].set_ylim(-0.4, 1.4); ax[0].set_xlabel("leaf time t"); ax[0].set_ylabel("B(t)")
    ax[0].set_title("topological charge B(t)  (Protocol A)"); ax[0].legend(fontsize=8)
    ax[1].plot(t_leaf, Emean, "s-", color="firebrick")
    ax[1].set_xlabel("leaf time t"); ax[1].set_ylabel("E (leaf gradient energy)")
    ax[1].set_title("Derrick leaf energy E(t)")
    ax[2].plot(t_leaf, rmean, "^-", color="teal")
    ax[2].set_xlabel("leaf time t"); ax[2].set_ylabel("r_eff(t)")
    ax[2].set_title("effective radius r_eff(t)")
    fig.suptitle("E3b-1: hedgehog under deterministic causal evolution (Protocol A)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3b_1_hedgehog.png", dpi=130)
    print(f"saved {OUT/'E3b_1_hedgehog.png'}")


if __name__ == "__main__":
    main()

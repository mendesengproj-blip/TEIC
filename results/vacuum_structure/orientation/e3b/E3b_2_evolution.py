"""E3b_2_evolution.py -- causal vs acausal evolution: does the arrow of time hold B?

Charter E3b-2.  E3 used ordinary Metropolis, which may "retrocede" the system to
lower-energy states, ignoring the arrow of time; its hedgehog unwound thermally in
~2700 sweeps (Verdict B, metastable).  E3b compares:

  Protocol A -- deterministic CAUSAL evolution (past frozen, future = causal
                descent against parents).  One forward pass; cannot climb barriers.
  Protocol B -- causal MONTE CARLO: cold Metropolis that CAN climb thermal
                barriers, but the seeded PAST slab is FROZEN (the past cannot be
                thermally un-written).

and, as the decisive CONTROLS that keep the claim honest:

  acausal MC -- the E3-style relaxation: nothing frozen.  Reproduces thermal
                unwinding on this substrate.
  future-MC  -- a FUTURE slab frozen instead of the past, same frozen fraction.
                If B is preserved here too, the protection is Dirichlet
                slab-pinning propagated by the links, NOT a unique time asymmetry.

Observable: cooled whole-cloud B(t) over MC sweeps (cool before measuring the
integer charge), 20 seeds; lifetime = first sweep with cooled B < 0.5 (censored if
it survives the run).  Pre-registered: B(t)->0 under Protocol A = Verdict C.
Anti-circularity: B geometric, E bond functional; no stability assumed.
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
SEED_FRAC = 0.25
MC_J = 3.0
MC_SWEEPS = 1000
RECORD = [0, 100, 200, 350, 500, 700, 1000]
COOL = 10


def _masks(pts):
    t = pts[:, 0]
    tmin, span = t.min(), t.max() - t.min()
    past = t <= tmin + SEED_FRAC * span
    future = t >= tmin + (1 - SEED_FRAC) * span
    none = np.zeros(pts.shape[0], dtype=bool)
    return past, future, none


def _lifetime(rec_t, Bseries):
    """First recorded sweep with cooled B < 0.5; else censored (> last sweep)."""
    for tt, b in zip(rec_t, Bseries):
        if tt > 0 and abs(b) < 0.5:
            return tt
    return MC_SWEEPS + 1


def run_seed(sd):
    pts = e3b.sprinkle_causal(RHO, T_BOX, L_BOX, sd)
    sub = e3b.Substrate(pts)
    xyz = pts[:, 1:4]
    nh = e3b.hedgehog_field(pts, +1, core=CORE)
    past, future, none = _masks(pts)

    # Protocol A: deterministic causal evolution (single forward sweep family)
    nA = e3b.evolve_causal(sub, nh, past, passes=2)
    B_A = e3b.topological_charge_poisson(xyz, e3b.cool_field(sub, nA, COOL))

    out = {"seed": sd, "n": sub.n, "B_protocolA": B_A}
    # Protocol B (causal MC, past frozen) + controls
    for label, mask in (("causal_pastfrozen", past),
                        ("acausal_nofreeze", none),
                        ("control_futurefrozen", future)):
        _, traj = e3b.evolve_mc_fast(sub, nh, mask, J=MC_J, n_sweeps=MC_SWEEPS,
                                     seed=1000 * sd + 17, record=RECORD,
                                     cool_steps=COOL)
        Bser = [d["B"] for d in traj]
        out[label] = {"rec_t": [d["sweep"] for d in traj], "B": Bser,
                      "lifetime": _lifetime([d["sweep"] for d in traj], Bser)}
    return out


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3b-2 -- causal vs acausal evolution (Protocol A, B, controls; 20 seeds)")
    print("=" * 72)
    rows = []
    for sd in SEEDS:
        r = run_seed(sd)
        rows.append(r)
        print(f"  seed {sd:2d}: A B={r['B_protocolA']:+.2f} | "
              f"causal life={_fmt(r['causal_pastfrozen']['lifetime'])} | "
              f"acausal life={_fmt(r['acausal_nofreeze']['lifetime'])} | "
              f"future-ctrl life={_fmt(r['control_futurefrozen']['lifetime'])}")

    def agg(label):
        Bmat = np.array([r[label]["B"] for r in rows])           # (seeds, T)
        lifes = np.array([r[label]["lifetime"] for r in rows])
        surv = float(np.mean(lifes > MC_SWEEPS))
        finite = lifes[lifes <= MC_SWEEPS]
        med = float(np.median(finite)) if finite.size else float("inf")
        return {"rec_t": RECORD, "B_mean": Bmat.mean(0).tolist(),
                "B_std": Bmat.std(0).tolist(), "survival_frac": surv,
                "median_lifetime": med, "lifetimes": lifes.tolist()}

    causal = agg("causal_pastfrozen")
    acausal = agg("acausal_nofreeze")
    future = agg("control_futurefrozen")
    A_surv = float(np.mean([abs(r["B_protocolA"] - 1) < 0.5 for r in rows]))

    # verdict logic for E3b-2
    causal_holds = causal["survival_frac"] >= 0.9
    acausal_unwinds = acausal["survival_frac"] <= 0.5
    boundary_not_arrow = future["survival_frac"] >= 0.9   # future slab works too

    print("-" * 72)
    print(f"  Protocol A (deterministic causal): B=1 survival {A_surv:.0%}")
    print(f"  Protocol B (causal, past frozen) : survival {causal['survival_frac']:.0%}  "
          f"median life={_fmt(causal['median_lifetime'])}")
    print(f"  acausal control (no freeze)      : survival {acausal['survival_frac']:.0%}  "
          f"median life={_fmt(acausal['median_lifetime'])}")
    print(f"  future-frozen control            : survival {future['survival_frac']:.0%}  "
          f"median life={_fmt(future['median_lifetime'])}")
    print("-" * 72)
    if causal_holds and acausal_unwinds:
        msg = ("Causal (past-frozen) evolution preserves B=1 while acausal MC unwinds "
               "-- the link network + a fixed boundary slab outlast free relaxation by "
               f">{MC_SWEEPS}/{acausal['median_lifetime']:.0f}x.")
        if boundary_not_arrow:
            msg += (" BUT a FUTURE-frozen slab preserves B equally well: the rigidity "
                    "is Dirichlet slab-pinning propagated by the causal links, NOT a "
                    "unique arrow-of-time effect.")
    else:
        msg = "Causal and acausal evolution behave similarly on this substrate."
    print(f"  E3b-2: {msg}")
    print("=" * 72)

    payload = {
        "protocolA_survival": A_surv,
        "causal_pastfrozen": causal, "acausal_nofreeze": acausal,
        "control_futurefrozen": future,
        "causal_holds": bool(causal_holds), "acausal_unwinds": bool(acausal_unwinds),
        "boundary_pinning_not_arrow_of_time": bool(boundary_not_arrow),
        "interpretation": msg,
        "config": {"rho": RHO, "T": T_BOX, "L": L_BOX, "core": CORE,
                   "seed_frac": SEED_FRAC, "mc_J": MC_J, "mc_sweeps": MC_SWEEPS,
                   "record": RECORD, "cool": COOL, "seeds": SEEDS},
        "per_seed": rows,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E3b_2_evolution.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3b_2_evolution.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(causal, acausal, future, A_surv)
    return payload


def _fmt(x):
    return "survived" if x > MC_SWEEPS else f"{x:.0f}"


def make_figure(causal, acausal, future, A_surv):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for d, c, lab in ((causal, "C0", "Protocol B: causal (past frozen)"),
                      (acausal, "crimson", "acausal control (no freeze)"),
                      (future, "C2", "control: future frozen")):
        ax[0].errorbar(d["rec_t"], d["B_mean"], yerr=d["B_std"], marker="o",
                       capsize=3, lw=1.4, color=c, label=lab)
    ax[0].axhline(1, color="k", ls=":", lw=0.6); ax[0].axhline(0, color="k", ls=":", lw=0.6)
    ax[0].axhline(A_surv, color="purple", ls="--", lw=1,
                  label=f"Protocol A (det. causal) B={A_surv:.2f}")
    ax[0].set_ylim(-0.4, 1.4); ax[0].set_xlabel("MC sweeps")
    ax[0].set_ylabel("cooled B(t)"); ax[0].set_title("B(t): causal vs acausal")
    ax[0].legend(fontsize=8)

    labels = ["causal\n(past)", "acausal\n(none)", "future\n(ctrl)"]
    surv = [causal["survival_frac"], acausal["survival_frac"], future["survival_frac"]]
    ax[1].bar(labels, surv, color=["C0", "crimson", "C2"])
    ax[1].set_ylim(0, 1.05); ax[1].set_ylabel("fraction of seeds with B=1 surviving")
    ax[1].set_title(f"B=1 survival @ {MC_SWEEPS} sweeps (20 seeds)")
    for i, s in enumerate(surv):
        ax[1].text(i, s + 0.02, f"{s:.0%}", ha="center", fontsize=9)
    fig.suptitle("E3b-2: the arrow of time vs free relaxation of the hedgehog",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3b_2_evolution.png", dpi=130)
    print(f"saved {OUT/'E3b_2_evolution.png'}")


if __name__ == "__main__":
    main()

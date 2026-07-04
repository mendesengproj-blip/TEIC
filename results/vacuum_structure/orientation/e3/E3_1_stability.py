"""E3_1_stability.py -- fate of the hedgehog defect under relaxation.

Charter E3-1.  From the ordered ferromagnetic state, seed a hedgehog n(r)=r_hat
and let it relax, recording the three pre-registered observables

    B(t)      topological charge (solid-angle degree)
    E(t)      Derrick gradient energy  sum (1 - n_i.n_j)
    r_eff(t)  effective defect radius  <r weighted by gradient density>

by TWO independent relaxations (charter protocol 2):

  (1) zero-temperature GRADIENT FLOW (steepest descent on S^2) -- the honest
      Derrick test: a texture that survives steepest descent is a genuine local
      energy minimum, none of the dynamics can climb a barrier.

  (2) finite-coupling MONTE CARLO over 20 seeds at cold J -- thermal fluctuations
      CAN cross a finite barrier, so MC reveals whether the defect is truly
      stable or merely metastable.  The topological charge is read after a short
      gradient-flow COOLING of each snapshot (standard lattice protocol: cooling
      removes thermal UV wrinkles that carry spurious fractional solid angle,
      without moving the integer winding).

Pre-registered scenarios (charter):
  A collapse  : B: 1->0, E monotone down, r_eff -> 0   (Derrick active, death)
  B metastable: B=1 held, finite barrier, thermal unwinding at long time
  C stable    : B=1 held indefinitely, r_eff -> r>0, no thermal unwinding

Anti-circularity: B is the geometric charge, E the bond functional; no stability
is assumed.  Death criterion B(t)->0 is scored exactly as written.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e3_core as e3  # noqa: E402

OUT = Path(__file__).resolve().parent
SEEDS = list(range(20))

L_GRAD = 24
GRAD_STEPS = 4000
GRAD_REC = 200

L_MC = 20
MC_J = [3.0, 2.0]           # cold (ordered bulk) and warmer (barrier-probing)
MC_SWEEPS = 4000
MC_REC = 200
COOL_STEPS = 30


def gradient_flow_run():
    print("  [1] zero-T gradient flow  L=%d  steps=%d" % (L_GRAD, GRAD_STEPS))
    c = e3.default_center(L_GRAD)
    traj, nf = e3.relax_gradient(e3.hedgehog(L_GRAD, +1), n_steps=GRAD_STEPS,
                                 dt=0.1, record_every=GRAD_REC, center=c)
    for s in (traj[0], traj[len(traj) // 2], traj[-1]):
        print(f"      t={s['t']:5d}  B={s['B']:+.4f}  E={s['E']:8.1f}  "
              f"r_eff={s['r_eff']:.3f}")
    return traj


def mc_run(J):
    print("  [2] Monte-Carlo  L=%d  J=%.1f  seeds=%d  sweeps=%d (cooled B)"
          % (L_MC, J, len(SEEDS), MC_SWEEPS))
    c = e3.default_center(L_MC)
    rec_t = list(range(0, MC_SWEEPS + 1, MC_REC))
    per_seed = []          # each: dict t-> (B_cooled, r_eff_cooled, E_raw)
    lifetimes = []
    for sd in SEEDS:
        n = e3.hedgehog(L_MC, +1)
        Bs, rs, Es = [], [], []
        life = None
        prev_t = 0
        for tt in rec_t:
            if tt > 0:
                _, n = e3.relax_mc(n, J=J, n_steps=tt - prev_t, seed=1000 * sd + 17,
                                   record_every=tt - prev_t, center=c)
                prev_t = tt
            Braw = e3.gradient_energy(n)
            Bc, _, rc = e3.cooled_charge(n, steps=COOL_STEPS)
            Bs.append(Bc); rs.append(rc); Es.append(Braw)
            if life is None and abs(round(Bc)) < 0.5 and tt > 0:
                life = tt
        if life is None:
            life = MC_SWEEPS + 1            # right-censored (survived the run)
        lifetimes.append(life)
        per_seed.append({"B": Bs, "r_eff": rs, "E": Es})
        print(f"      seed {sd:2d}: B_cooled {Bs[0]:+.2f}->{Bs[-1]:+.2f}  "
              f"life={'survived' if life>MC_SWEEPS else life}")
    Bmat = np.array([p["B"] for p in per_seed])            # (seeds, T)
    rmat = np.array([p["r_eff"] for p in per_seed])
    surv = np.mean([abs(round(p["B"][-1])) >= 0.5 for p in per_seed])
    finite = [l for l in lifetimes if l <= MC_SWEEPS]
    med_life = float(np.median(finite)) if finite else float("inf")
    return {"J": J, "rec_t": rec_t, "B_mean": Bmat.mean(0).tolist(),
            "B_std": Bmat.std(0).tolist(), "B_round_mean": np.round(Bmat).mean(0).tolist(),
            "r_eff_mean": rmat.mean(0).tolist(), "survival_frac": float(surv),
            "lifetimes": lifetimes, "median_lifetime": med_life,
            "per_seed_B": Bmat.tolist()}


def classify(grad, mc):
    gB0, gBf = grad[0]["B"], grad[-1]["B"]
    grf = grad[-1]["r_eff"]; gr0 = grad[0]["r_eff"]
    gEf, gE0 = grad[-1]["E"], grad[0]["E"]
    grad_collapsed = (abs(gBf) < 0.5) and (grf < 0.4 * gr0)
    grad_preserved = abs(gBf - 1) < 0.1
    # thermal unwinding: any cold-J MC seed loses the charge
    any_unwind = any(m["survival_frac"] < 1.0 for m in mc)
    all_survive_cold = mc[0]["survival_frac"] >= 0.99   # the coldest J
    if grad_collapsed:
        sc = "A"; why = "gradient flow drives B->0 and r_eff->0 (Derrick active)"
    elif grad_preserved and not any_unwind:
        sc = "C"; why = ("B=1 survives gradient flow AND every MC seed; r_eff "
                         "converges to r>0 with no thermal unwinding")
    else:
        sc = "B"; why = ("B=1 survives gradient flow (lattice regularises the "
                         "collapse) but a finite barrier is crossed thermally: "
                         "some MC seeds unwind to B=0")
    return {"scenario": sc, "why": why, "grad_B0": gB0, "grad_Bf": gBf,
            "grad_r0": gr0, "grad_rf": grf, "grad_E0": gE0, "grad_Ef": gEf,
            "grad_collapsed": bool(grad_collapsed),
            "grad_preserved": bool(grad_preserved),
            "any_thermal_unwind": bool(any_unwind),
            "cold_survival": float(mc[0]["survival_frac"])}


def make_figure(grad, mc):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    gt = [s["t"] for s in grad]
    # B(t)
    ax = axes[0]
    ax.axhline(1, color="k", ls=":", lw=0.6); ax.axhline(0, color="k", ls=":", lw=0.6)
    ax.plot(gt, [s["B"] for s in grad], "k-", lw=2, label="grad flow (T=0)")
    for m in mc:
        ax.errorbar(m["rec_t"], m["B_mean"], yerr=m["B_std"], capsize=2,
                    ms=3, marker="o", lw=1, label=f"MC J={m['J']:g} (cooled, 20 sds)")
    ax.set_xlabel("relaxation time"); ax.set_ylabel("B(t)")
    ax.set_title("topological charge B(t)"); ax.set_ylim(-0.4, 1.4)
    ax.legend(fontsize=7); ax.grid(alpha=0.25)
    # E(t)
    ax = axes[1]
    ax.plot(gt, [s["E"] for s in grad], "k-", lw=2)
    ax.set_xlabel("relaxation time"); ax.set_ylabel("E (gradient energy)")
    ax.set_title("Derrick energy E(t)  (gradient flow)"); ax.grid(alpha=0.25)
    # r_eff(t)
    ax = axes[2]
    ax.plot(gt, [s["r_eff"] for s in grad], "k-", lw=2, label="grad flow")
    for m in mc:
        ax.plot(m["rec_t"], m["r_eff_mean"], "o-", ms=3, lw=1,
                label=f"MC J={m['J']:g}")
    ax.set_xlabel("relaxation time"); ax.set_ylabel("r_eff(t)")
    ax.set_title("effective radius r_eff(t)"); ax.legend(fontsize=7); ax.grid(alpha=0.25)
    fig.suptitle("E3-1: fate of the hedgehog defect of n under relaxation",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3_1_stability.png", dpi=130)
    print(f"saved {OUT/'E3_1_stability.png'}")


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3-1 -- hedgehog stability (gradient flow + Monte Carlo, 20 seeds)")
    print("=" * 72)
    grad = gradient_flow_run()
    mc = [mc_run(J) for J in MC_J]
    verdict = classify(grad, mc)
    print("-" * 72)
    print(f"  gradient flow: B {verdict['grad_B0']:+.3f} -> {verdict['grad_Bf']:+.3f}, "
          f"r_eff {verdict['grad_r0']:.2f} -> {verdict['grad_rf']:.2f}, "
          f"E {verdict['grad_E0']:.0f} -> {verdict['grad_Ef']:.0f}")
    for m in mc:
        print(f"  MC J={m['J']:g}: survival={m['survival_frac']:.0%}  "
              f"median unwinding time={m['median_lifetime']}")
    print(f"  SCENARIO: {verdict['scenario']} -- {verdict['why']}")
    print("=" * 72)

    payload = {
        "gradient_flow": {"t": [s["t"] for s in grad],
                          "B": [s["B"] for s in grad],
                          "E": [s["E"] for s in grad],
                          "r_eff": [s["r_eff"] for s in grad]},
        "monte_carlo": mc, "verdict": verdict,
        "config": {"L_grad": L_GRAD, "grad_steps": GRAD_STEPS, "L_mc": L_MC,
                   "mc_J": MC_J, "mc_sweeps": MC_SWEEPS, "cool_steps": COOL_STEPS,
                   "seeds": SEEDS},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E3_1_stability.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3_1_stability.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(grad, mc)
    return verdict


if __name__ == "__main__":
    main()

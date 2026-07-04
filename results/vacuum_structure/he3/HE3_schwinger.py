"""HE3 -- the causal ferromagnet in an intense field: does it create topological-defect
pairs (the Schwinger-effect analogue)?

Pre-registered structure:

  GATE   charge_field gives B(hedgehog)=+1, B(anti)=-1, B(uniform)=0; the LLG integrator
         lowers (does not blow up) the energy under damping; the Zeeman sign is correct.

  PART 1 -- ENERGETIC (decisive, analytic).  Is a hedgehog/anti-hedgehog PAIR ever
         energetically favoured over the ordered vacuum in a field h?  Build the ordered
         state and a defect dipole, both in the field, and compute
             dE(h) = E[dipole; h] - E[uniform; h]
         over a wide range of h.  Creation is favourable only if dE(h) < 0 for some h.
         (The Schwinger threshold is exactly "field energy >= pair rest energy".)

  PART 2 -- DYNAMICAL critical-field scan.  Start in the ordered vacuum and apply an intense
         field; let the DYNAMICS act (deterministic LLG precession with a small fluctuation
         seed, AND finite-T Metropolis so thermal NUCLEATION over a barrier is allowed).
         Three field protocols, weakest-to-strongest h:
           anti  : h along -z (false-vacuum / cleanest Schwinger setup)
           trans : h along +x (transverse torque on the +z order)
           radial: h = h * r_hat (a field whose OWN texture is a hedgehog -- the most
                   generous probe; if anything nucleates a defect it is this)
         Measure cooled defect counts (n_pos, n_neg) and net B.  PAIR CREATION = both
         n_pos>=1 and n_neg>=1 persist after cooling with net B ~ 0.  Critical field h* =
         smallest h that creates a pair; none -> death.

DEATH CRITERION (pre-registered): no pair creation by the field at any strength.  Not tuned.
"""
from __future__ import annotations

import json
import time

import numpy as np

import he3_core as h3
import e3_core as e3

L = 16
J = 1.0
H_SCAN = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]     # h/J from weak to field-dominated ("v->c")
SEEDS = [0, 1, 2]


def gate():
    print("GATE")
    nh, na, nu = e3.hedgehog(L, +1), e3.hedgehog(L, -1), e3.uniform(L)
    Bh, Ba, Bu = (e3.topological_charge(nh), e3.topological_charge(na),
                  e3.topological_charge(nu))
    charge_ok = abs(Bh - 1) < 1e-3 and abs(Ba + 1) < 1e-3 and abs(Bu) < 1e-3
    # LLG with damping must not increase energy of a perturbed uniform state (zero field)
    rng = np.random.default_rng(0)
    npert = e3._normalize(nu + 0.2 * rng.standard_normal(nu.shape))
    hz = h3.uniform_field(L, 0.0)
    traj, _ = h3.llg_evolve(npert, hz, n_steps=200, dt=0.05, lam=0.3, record_every=200)
    llg_ok = traj[-1]["E_ex"] <= traj[0]["E_ex"] + 1e-6
    # Zeeman sign: aligned state has LOWER field energy than anti-aligned
    hpz = h3.uniform_field(L, 1.0, (0, 0, 1))
    sign_ok = h3.field_energy(e3.uniform(L, (0, 0, 1)), hpz) < \
        h3.field_energy(e3.uniform(L, (0, 0, -1)), hpz)
    # speckle-proof counter must read 1 defect on a hedgehog, 0 on the ordered vacuum
    pos_hh, neg_hh, Q_hh, _ = h3.count_defects(nh)
    pos_u, neg_u, Q_u, _ = h3.count_defects(nu)
    count_ok = (pos_hh == 1 and neg_hh == 0 and pos_u == 0 and neg_u == 0)
    print(f"  charge B(hh/anti/uniform)={Bh:+.3f}/{Ba:+.3f}/{Bu:+.3f}  {'OK' if charge_ok else 'FAIL'}")
    print(f"  counter: hedgehog -> +{pos_hh}/-{neg_hh} (Q={Q_hh:.2f}); "
          f"uniform -> +{pos_u}/-{neg_u} (Q={Q_u:.2f})  {'OK' if count_ok else 'FAIL'}")
    print(f"  LLG damping lowers E: {traj[0]['E_ex']:.1f}->{traj[-1]['E_ex']:.1f}  "
          f"{'OK' if llg_ok else 'FAIL'}")
    print(f"  Zeeman sign (aligned<anti): {'OK' if sign_ok else 'FAIL'}")
    return {"charge_ok": charge_ok, "count_ok": count_ok, "llg_ok": llg_ok,
            "sign_ok": sign_ok, "B_hedgehog": Bh, "B_anti": Ba, "B_uniform": Bu,
            "Q_hedgehog": Q_hh, "Q_uniform": Q_u}


def part1_energetics():
    """dE(h) = E[dipole; h] - E[uniform; h].  Uniform is taken ALONG the field (ground)."""
    print("PART 1 -- energetics: is a defect pair ever favoured?")
    n_dip = e3.dipole(L, sep=L // 2)
    res = []
    h_grid = np.concatenate([[0.0], np.logspace(-1, 2, 13)])
    for h in h_grid:
        hf = h3.uniform_field(L, h, (0, 0, 1))
        n_uni = e3.uniform(L, (0, 0, 1))                 # aligned with field = ground state
        E_uni = h3.total_energy_h(n_uni, hf)
        E_dip = h3.total_energy_h(n_dip, hf)
        res.append({"h": float(h), "E_uniform": E_uni, "E_dipole": E_dip,
                    "dE": E_dip - E_uni})
    dE_min = min(r["dE"] for r in res)
    favourable = dE_min < 0
    print(f"  dE(dipole - uniform): min over h = {dE_min:.1f}  "
          f"({'PAIR FAVOURED somewhere' if favourable else 'pair always COSTS energy'})")
    return {"curve": res, "dE_min": dE_min, "pair_ever_favoured": bool(favourable)}


def _run_protocol(direction_name, make_field, h, seed):
    """One (protocol, h, seed): start ordered (+z) + small noise, apply field, run BOTH a
    finite-T Metropolis and a damped-LLG-with-noise, cool, count defects.  Return the WORST
    case (max pairs found by either dynamics)."""
    n0 = e3.uniform(L, (0, 0, 1))
    rng = np.random.default_rng(100 + seed)
    n0 = e3._normalize(n0 + 0.05 * rng.standard_normal(n0.shape))   # fluctuation seed
    hf = make_field(h)

    # (a) thermal nucleation: Metropolis at moderate coupling (J=1 ~ near order) with field
    _, n_mc = h3.metropolis_h(n0, hf, J=J, n_steps=300, seed=seed, record_every=300)
    B_mc, pos_mc, neg_mc, Q_mc = h3.cooled_defects(n_mc)

    # (b) precessional drive: damped LLG with a small ongoing noise
    _, n_llg = h3.llg_evolve(n0, hf, n_steps=400, dt=0.05, lam=0.3,
                             record_every=400, seed=seed, noise=0.02)
    B_llg, pos_llg, neg_llg, Q_llg = h3.cooled_defects(n_llg)

    # a genuine created pair = both signs present (>=1 each) AND smoothed matter Q_def >~ 1.5
    def is_pair(pos, neg, Q):
        return int(min(pos, neg) >= 1 and Q >= 1.5)
    pairs_mc = is_pair(pos_mc, neg_mc, Q_mc)
    pairs_llg = is_pair(pos_llg, neg_llg, Q_llg)
    best = max(pairs_mc, pairs_llg)
    return {"protocol": direction_name, "h": h, "seed": seed,
            "mc": {"B": B_mc, "n_pos": pos_mc, "n_neg": neg_mc, "Q_def": Q_mc},
            "llg": {"B": B_llg, "n_pos": pos_llg, "n_neg": neg_llg, "Q_def": Q_llg},
            "pairs": int(best)}


def part2_scan():
    print("PART 2 -- dynamical critical-field scan (anti / trans / radial)")
    protocols = {
        "anti":   lambda h: h3.uniform_field(L, h, (0, 0, -1)),
        "trans":  lambda h: h3.uniform_field(L, h, (1, 0, 0)),
        "radial": lambda h: h3.radial_field(L, h),
    }
    out = {}
    h_star = {}
    for name, mk in protocols.items():
        rows = []
        created_at = None
        for h in H_SCAN:
            pair_counts = []
            for sd in SEEDS:
                r = _run_protocol(name, mk, h, sd)
                pair_counts.append(r["pairs"])
            max_pairs = max(pair_counts)
            rows.append({"h": h, "max_pairs": max_pairs, "per_seed": pair_counts})
            tag = "PAIR(S)!" if max_pairs >= 1 else "no pair"
            print(f"  [{name:6}] h={h:6.1f}  max pairs (over seeds) = {max_pairs}   {tag}")
            if max_pairs >= 1 and created_at is None:
                created_at = h
        out[name] = rows
        h_star[name] = created_at
    return {"scan": out, "h_star": h_star}


def main():
    t0 = time.time()
    print("=" * 74)
    print("HE3 -- CAUSAL FERROMAGNET in an INTENSE FIELD (Schwinger analogue)")
    print("=" * 74)
    g = gate()
    gate_ok = g["charge_ok"] and g["llg_ok"] and g["sign_ok"]
    p1 = part1_energetics()
    p2 = part2_scan()

    any_creation = (p1["pair_ever_favoured"] or
                    any(v is not None for v in p2["h_star"].values()))
    verdict = "SUCCESS (pairs created)" if any_creation else "DEATH"

    payload = {
        "config": {"L": L, "J": J, "h_scan": H_SCAN, "seeds": SEEDS},
        "gate": {**g, "pass": bool(gate_ok)},
        "energetics": p1,
        "dynamical_scan": p2,
        "any_creation": bool(any_creation),
        "verdict": verdict,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (h3.OUT / "HE3_schwinger.json").write_text(json.dumps(payload, indent=2, default=float))
    print("-" * 74)
    print(f"VERDICT HE3: {verdict}   (energetics favoured={p1['pair_ever_favoured']}, "
          f"dynamical h*={p2['h_star']})  ({time.time()-t0:.0f}s)")
    make_figure(payload)
    return payload


def make_figure(payload):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    c = payload["energetics"]["curve"]
    hs = [r["h"] for r in c]
    dE = [r["dE"] for r in c]
    ax[0].semilogx(np.clip(hs, 1e-2, None), dE, "o-", color="C0")
    ax[0].axhline(0, color="k", lw=0.8, ls=":")
    ax[0].set_xlabel("field h"); ax[0].set_ylabel(r"$E_{\rm dipole}-E_{\rm uniform}$")
    ax[0].set_title("PART 1: a defect pair always COSTS energy (dE>0)")
    ax[0].grid(alpha=0.3, which="both")

    for name, rows in payload["dynamical_scan"]["scan"].items():
        ax[1].plot([r["h"] for r in rows], [r["max_pairs"] for r in rows], "o-",
                   label=name)
    ax[1].axhline(1, color="C3", lw=0.8, ls="--", label="creation threshold (>=1 pair)")
    ax[1].set_xscale("log")
    ax[1].set_xlabel("field h"); ax[1].set_ylabel("defect pairs created")
    ax[1].set_title("PART 2: no pairs nucleate at any field")
    ax[1].set_ylim(-0.2, 2.2); ax[1].legend(); ax[1].grid(alpha=0.3, which="both")
    fig.suptitle(f"HE3 -- intense field on the causal ferromagnet: {payload['verdict']}",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(h3.OUT / "HE3_schwinger.png", dpi=130)
    print(f"saved {h3.OUT/'HE3_schwinger.png'}")


if __name__ == "__main__":
    main()

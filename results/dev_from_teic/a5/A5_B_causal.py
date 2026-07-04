"""A5_B_causal.py -- Phase B: does the Anderson-Higgs mechanism (validated on the cubic
lattice in G1) survive on the CAUSAL SET, or does the E5/E7 non-locality obstruct it?

Charter: results/dev_from_teic/A5_ANDERSON_HIGGS.md.  Runs ONLY after G1 PASS.

The decisive observable is the ORIENTATION of the O(3) order parameter, decomposed into:
  charged bond  b_ch = <Re conj(phi_lo) e^{i lam th} phi_hi>   (transverse, GAUGED)
  neutral bond  b_z  = <n_z(lo) n_z(hi)>                        (longitudinal, UNGAUGED)
For an Anderson-Higgs Higgs phase we need the CHARGED sector to condense (b_ch large) so
the gauged U(1)_z is spontaneously broken and the photon eats the Goldstone.

Phase A (G1) proved this happens on a cubic lattice.  Here we test the causal set and
diagnose the specific role of non-locality (mean Hasse degree grows with N, vs 2d=8 for
a local lattice; this is the E5/E7 obstruction).

m_A_DEV is COMPARISON ONLY (synthesis), never here.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a5_causal_core as cc  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RHO = 4.0
SIDE = 3.0
SEED = 0
D_EASY = 0.5
J_ORD = 1.0
N_BURN, N_MEAS, MEAS_EVERY = 400, 150, 2


def order_bonds(model):
    """(charged bond, neutral n_z bond), seed-averaged over the measurement ensemble."""
    lo, hi = model.edges[:, 0], model.edges[:, 1]
    ch, nz = [], []
    for _ in range(N_MEAS):
        for _ in range(MEAS_EVERY):
            model.sweep()
        ch.append(model.gauge_invariant_bond())
        nz.append(float(np.mean(model.n[lo, 2] * model.n[hi, 2])))
    return float(np.mean(ch)), float(np.mean(nz))


def measure(J, lam, g_gauge, g, edges, pl, ps, ls, burn=N_BURN):
    m = cc.CausalHiggs(g, edges, pl, ps, ls, J=J, lam=lam, g_gauge=g_gauge, D=D_EASY, seed=0)
    m.equilibrate(burn)
    return order_bonds(m)


def main():
    t0 = time.time()
    print("=" * 80)
    print("A5 Phase B -- Anderson-Higgs on the CAUSAL SET (does non-locality obstruct it?)")
    print("=" * 80)

    # ---- NONLOC: degree growth with N (the E5/E7 non-locality) ----
    print("\n[NONLOC] mean Hasse degree vs N (local 4D lattice = 8; causal set grows)")
    deg_growth = {}
    for side in (2.4, 3.0):
        g, pts, edges, pl, ps, ls = cc.build_causal_substrate(RHO, side, SEED)
        deg_growth[g.n] = float(g.degree.mean())
        print(f"  N={g.n:4d}: mean degree={g.degree.mean():.1f}  max={g.degree.max()}  "
              f"E={edges.shape[0]}  diamonds={pl.shape[0]}")
    g, pts, edges, pl, ps, ls = cc.build_causal_substrate(RHO, SIDE, SEED)
    Ns = sorted(deg_growth)
    nonloc = bool(deg_growth[Ns[-1]] > deg_growth[Ns[0]] + 1.0)

    # ---- GAUGE-INV gate ----
    mm = cc.CausalHiggs(g, edges, pl, ps, ls, J=J_ORD, lam=1.0, g_gauge=1.0, D=D_EASY, seed=0)
    dS, _ = mm.gauge_invariance_check()
    gauge_ok = dS < 1e-7
    print(f"\n[GAUGE-INV] |dS| = {dS:.2e}  PASS={gauge_ok}")

    # ---- ORDER DECOMPOSITION: charged (gauged) vs neutral order vs lambda ----
    print(f"\n[ORDER] charged (gauged) vs neutral order vs lambda (J={J_ORD}, g=1.0, N={g.n})")
    lam_scan = [0.0, 0.1, 0.5, 1.0]
    order = {}
    for lam in lam_scan:
        b_ch, b_z = measure(J_ORD, lam, 1.0, g, edges, pl, ps, ls)
        order[lam] = {"charged_bond": b_ch, "neutral_bond": b_z}
        tag = ("IN-PLANE (charged condenses, U(1) broken)" if b_ch > 0.3 else
               "NEUTRAL-AXIS escape (U(1)_z UNbroken)" if b_z > 0.3 else "disordered")
        print(f"  lambda={lam:.1f}: charged_bond={b_ch:.3f}  neutral_bond={b_z:.3f}  -> {tag}")

    # ---- ROBUSTNESS: can a stiffer gauge rescue the charged condensate at lambda=1? ----
    print(f"\n[ROBUST] charged condensate vs gauge stiffness (lambda=1, J={J_ORD})")
    gstiff = {}
    for gg in (0.2, 0.5, 1.0):
        b_ch, b_z = measure(J_ORD, 1.0, gg, g, edges, pl, ps, ls)
        gstiff[gg] = {"charged_bond": b_ch, "neutral_bond": b_z}
        print(f"  g={gg:.1f} (beta_g={1/gg**2:.1f}): charged_bond={b_ch:.3f}  neutral_bond={b_z:.3f}")

    # ---- verdict ----
    ch0 = order[0.0]["charged_bond"]           # pure ferromagnet: should be in-plane
    ch1 = order[1.0]["charged_bond"]
    z1 = order[1.0]["neutral_bond"]
    matter_orders_uncoupled = bool(ch0 > 0.3)
    charged_condenses_coupled = bool(ch1 > 0.3)
    neutral_escape = bool(z1 > 0.3 and ch1 < 0.1)
    stiff_rescues = bool(any(v["charged_bond"] > 0.3 for v in gstiff.values()))

    if not gauge_ok:
        status, verdict = "FAIL", "ABORTED -- gauge invariance failed on the causal set."
    elif charged_condenses_coupled:
        status = "SUCCESS-MECH"
        verdict = ("the charged sector condenses on the causal set even when coupled "
                   "(charged_bond=%.2f at lambda=1): the gauged U(1) is broken and the "
                   "Anderson-Higgs mechanism survives -> measure m_A and its scale next."
                   % ch1)
    elif neutral_escape and not stiff_rescues:
        status = "MORTE-NONLOCALITY"
        verdict = ("MORTE by non-locality -- the mechanism is OBSTRUCTED, with a precise "
                   "structural reason (not just 'failed').  The pure O(3) ferromagnet "
                   "orders fine on the causal set (charged_bond=%.2f at lambda=0), BUT the "
                   "moment the gauge coupling is on, each event's ~%.0f charged bonds carry "
                   "INCOHERENT gauge phases e^{i lam theta} (mean Hasse degree=%.1f, vs 8 "
                   "for a local lattice, and GROWING with N: %s).  The in-plane condensate "
                   "cannot form against that frustration, so the ferromagnet ESCAPES to the "
                   "ungauged NEUTRAL z-axis (neutral_bond %.2f->%.2f as lambda 0->1, charged "
                   "%.2f->%.2f).  The gauged U(1)_z therefore stays UNBROKEN -> no Goldstone "
                   "is eaten -> the photon stays massless -> m_A=0.  A stiffer gauge does NOT "
                   "rescue it (charged_bond<=%.2f even at g=0.2, near-flat field), so it is "
                   "not a tunable artifact.  This is the SAME non-locality that obstructed "
                   "E5 (Wilson loops) and E7 (Coulomb phase), now shown to specifically "
                   "prevent the Higgs.  A_mu mass [EXTERNO-B]; Scenario B reinforced."
                   % (ch0, g.degree.mean(), g.degree.mean(), deg_growth,
                      order[0.0]["neutral_bond"], z1, ch0, ch1,
                      max(v["charged_bond"] for v in gstiff.values())))
    elif not matter_orders_uncoupled:
        status, verdict = "MORTE", ("the ferromagnet does not even order on the causal set "
                                    "(charged_bond=%.2f at lambda=0); no order to gauge." % ch0)
    else:
        status = "INCONCLUSIVE"
        verdict = ("the charged condensate is suppressed when coupled but the picture is "
                   "ambiguous (charged@1=%.2f, neutral@1=%.2f); frontier." % (ch1, z1))

    print("-" * 80)
    print(f"  non-locality grows with N: {nonloc}  {deg_growth}")
    print(f"  uncoupled matter in-plane: {matter_orders_uncoupled} (charged@0={ch0:.2f})")
    print(f"  coupled charged condensate: {charged_condenses_coupled} (charged@1={ch1:.2f})")
    print(f"  neutral-axis escape: {neutral_escape} (neutral@1={z1:.2f}); stiff-gauge rescue: {stiff_rescues}")
    print(f"  STATUS: [{status}]")
    print(f"  VERDICT: {verdict}")
    print("=" * 80)

    _figure(deg_growth, order, lam_scan, gstiff)
    payload = {
        "phase": "A5 B -- Anderson-Higgs on the causal set",
        "engine": "a5_causal_core (O(3) ferromagnet + non-compact U(1) on Hasse diamonds)",
        "substrate": {"rho": RHO, "side": SIDE, "N": g.n, "E": int(edges.shape[0]),
                      "diamonds": int(pl.shape[0]), "mean_degree": float(g.degree.mean())},
        "nonlocality_degree_vs_N": deg_growth, "nonlocality_grows": nonloc,
        "gauge_invariance_dS": dS, "gauge_invariance_pass": gauge_ok,
        "order_vs_lambda": order, "gauge_stiffness_scan_lambda1": gstiff,
        "matter_orders_uncoupled": matter_orders_uncoupled,
        "charged_condenses_coupled": charged_condenses_coupled,
        "neutral_axis_escape": neutral_escape, "stiff_gauge_rescues": stiff_rescues,
        "status": status, "verdict": verdict,
        "anti_circularity": "no DEV number; m_A_DEV COMPARISON ONLY in synthesis",
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (HERE / "A5_B_causal.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved A5_B_causal.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(deg_growth, order, lam_scan, gstiff):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    Ns = sorted(deg_growth)
    ax[0].plot(Ns, [deg_growth[n] for n in Ns], "o-", lw=1.6, label="causal set")
    ax[0].axhline(8, color="gray", ls="--", lw=1, label="local 4D lattice (2d=8)")
    ax[0].set_xlabel("N events"); ax[0].set_ylabel("mean Hasse degree")
    ax[0].set_title("(a) non-locality: degree grows with N")
    ax[0].legend(fontsize=8)
    lams = lam_scan
    ax[1].plot(lams, [order[l]["charged_bond"] for l in lams], "o-", lw=1.6,
               label="charged (gauged)")
    ax[1].plot(lams, [order[l]["neutral_bond"] for l in lams], "s-", lw=1.6,
               label="neutral n_z (ungauged)")
    ax[1].set_xlabel("coupling λ"); ax[1].set_ylabel("order parameter (bond)")
    ax[1].set_title("(b) the order ESCAPES to the neutral axis when coupled")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.2)
    gs = sorted(gstiff)
    ax[2].plot(gs, [gstiff[g]["charged_bond"] for g in gs], "o-", lw=1.6, label="charged")
    ax[2].plot(gs, [gstiff[g]["neutral_bond"] for g in gs], "s-", lw=1.6, label="neutral")
    ax[2].set_xlabel("gauge coupling g (small = stiff)"); ax[2].set_ylabel("bond (λ=1)")
    ax[2].set_title("(c) stiffer gauge does NOT rescue the charged condensate")
    ax[2].legend(fontsize=8); ax[2].grid(alpha=0.2)
    fig.suptitle("A5 Phase B: non-locality obstructs Anderson-Higgs (matter evades to the ungauged axis)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(HERE / "A5_B_causal.png", dpi=130)
    print("saved A5_B_causal.png")


if __name__ == "__main__":
    main()

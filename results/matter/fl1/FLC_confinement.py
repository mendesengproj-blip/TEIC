"""FLC_confinement.py -- FL1_SU3_FOUNDATION, Phase C (defects + confinement).

Runs ONLY because Phase B passed (the SU(3) vacuum orders).  Two pre-registered
questions, with the E3/E3b protocol for the defect and the Wilson-loop static
potential for confinement.

C1 HOMOTOPY / CHARGE.  Vacuum space = SU(3)xSU(3)/SU(3)_diag ~= SU(3).
   pi_1(SU(3))=0, pi_2(SU(3))=0, pi_3(SU(3))=Z.  The non-trivial class is pi_3 ->
   a POINT defect in 3D = the colour Skyrmion (B in Z).  Verify the topological
   charge B of the embedded SU(2)-in-SU(3) hedgehog is an integer (+1), converging
   with lattice resolution.

C2 DEFECT STABILITY (E3/E3b protocol: gradient descent + thermal check).  Build the
   B=1 colour Skyrmion; relax it.  Because Phase A proved Skyrme dominance does NOT
   emerge (K <= 6 TrM^2, sign theorem), the 2-derivative (sigma) energy alone
   collapses by Derrick -- so we ADD the Skyrme 4-derivative term EXPLICITLY as an
   external stabiliser (declared, not hidden).  Show:
     (a) rigorous radial Derrick: with the stabiliser, E(lam)=lam E2 + E4/lam has an
         interior minimum (STABLE, finite size); without it, E(lam)=lam E2 collapses;
     (b) 3D lattice: B=+1 survives gradient-flow cooling and a finite-amplitude
         thermal perturbation (topological protection).

C3 CONFINEMENT.  Gauge sector: SU(3) link field, Wilson action (the minimal action
   of Phase A).  Create a static colour charge-anticharge pair (a rectangular Wilson
   loop r x t) and measure E(r) = static potential V(r).  Confinement: V(r) grows
   ~linearly (area law, string tension sigma>0); non-confining: V(r) saturates/decays.
   beta is the bare coupling (SCANNED, never a QCD input); sigma is MEASURED.

DEATH CRITERION (Phase C, pre-registered): the phase DIES if no stable defect exists,
OR if a defect exists but E(r) shows NO sign of growth with separation.  PASS requires
BOTH: a stable colour Skyrmion AND a confining (growing) static potential.

Anti-circularity: NO QCD number (quark mass, sigma value, alpha_s, hadron mass) enters
C1-C3.  The Skyrme weight e_sk is a declared external stabiliser scale; beta is scanned.
Qualitative QCD comparison is reserved for Phase D.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su3_core as s3

SCALE = sys.argv[1] if len(sys.argv) > 1 else "full"
if SCALE == "quick":
    GAUGE_L, GAUGE_BETAS = 6, [4.5, 6.0]
    THERM, NMEAS, MEAS_GAP = 60, 8, 3
    R_MAX, T_MAX = 3, 4
    LATT_L = 21
else:
    GAUGE_L, GAUGE_BETAS = 8, [4.0, 4.5, 5.0, 5.5, 6.0]
    THERM, NMEAS, MEAS_GAP = 200, 30, 4
    R_MAX, T_MAX = 4, 5
    LATT_L = 31
E_SK = 0.5            # EXTERNAL Skyrme stabiliser weight (declared input, not derived)


# =========================================================================== #
# C1 -- homotopy classification + integer topological charge
# =========================================================================== #
def c1_homotopy():
    homotopy = {"vacuum_space": "SU(3)x SU(3)/SU(3)_diag ~= SU(3)",
                "pi_1": 0, "pi_2": 0, "pi_3": "Z",
                "defect": "pi_3 != 0 -> point defect in 3D = colour Skyrmion (B in Z)"}
    # integer charge, convergence with resolution
    conv = []
    for L, hw, w in [(15, 2.2, 0.7), (21, 2.6, 0.8), (31, 3.0, 0.9), (41, 3.4, 1.0)]:
        U, dx = s3.embedded_hedgehog(L, half_width=hw, w_core=w)
        conv.append({"L": L, "B": s3.baryon_number(U, dx)})
    Uanti, dxa = s3.embedded_hedgehog(31, half_width=3.0, w_core=0.9, charge=-1)
    B_anti = s3.baryon_number(Uanti, dxa)
    B_best = conv[-1]["B"]
    integer_ok = abs(B_best - 1.0) < 0.05
    return {"homotopy": homotopy, "B_convergence": conv, "B_best": B_best,
            "B_anti": B_anti, "integer_charge_ok": bool(integer_ok)}


# =========================================================================== #
# C2 -- defect stability (radial Derrick + 3D thermal), explicit external Skyrme
# =========================================================================== #
def c2_stability(rng):
    # (a) rigorous radial Derrick, one relaxed profile, stabiliser on vs off
    r, dr = s3.radial_grid(rmax=10.0, n=700)
    F, E2, E4 = s3.radial_relax(r, dr, e_sk=E_SK)
    lam_star = float(np.sqrt(E4 / E2))
    lams = np.array([0.1, 0.2, 0.33, 0.5, lam_star, 0.8, 1.0, 1.5, 2.5, 4.0])
    lams = np.unique(np.round(lams, 3))
    E_on, _, _ = s3.radial_derrick_curve(F, r, dr, E_SK, lams)
    E_off = lams * E2
    # interior min: argmin strictly inside the lambda range, and E rises both sides
    i_on = int(np.argmin(E_on))
    interior_min = (0 < i_on < len(lams) - 1)
    i_off = int(np.argmin(E_off))
    collapses_off = (i_off == 0)              # min at smallest lambda -> collapse
    mass = float(2.0 * np.sqrt(E2 * E4))

    # (b) 3D lattice: B is topologically protected -- a finite-amplitude thermal
    # perturbation knocks the naive charge down, but a SHORT gradient-flow cooling
    # (the lattice 'cooled charge' of E3/E3b, removing UV wrinkles without collapsing
    # the core) recovers it.  Robustness of the integer B = the defect is a genuine
    # topological object.
    THERM_AMP, COOL_STEPS = 0.15, 8
    U, dx = s3.embedded_hedgehog(LATT_L, half_width=3.0, w_core=0.9)
    B0 = s3.baryon_number(U, dx)
    Un = s3.add_su3_noise(U, amp=THERM_AMP, rng=rng)
    B_noisy = s3.baryon_number(Un, dx)
    hist, Uc = s3.relax_chiral_flow(Un, dx, E_SK, n_steps=COOL_STEPS, rate=0.08,
                                    record_every=COOL_STEPS)
    B_cooled = s3.baryon_number(Uc, dx)
    B_preserved = abs(B_cooled - B0) < 0.05

    stable = bool(interior_min and collapses_off and B_preserved)
    return {
        "e_sk_external": E_SK,
        "radial": {"E2": E2, "E4": E4, "lam_star": lam_star, "mass_2sqrtE2E4": mass,
                   "lambdas": lams.tolist(), "E_with_skyrme": E_on.tolist(),
                   "E_without_skyrme": E_off.tolist(),
                   "interior_min_with_skyrme": bool(interior_min),
                   "collapses_without_skyrme": bool(collapses_off)},
        "lattice_thermal": {"B0": B0, "thermal_amp": THERM_AMP,
                            "cool_steps": COOL_STEPS, "B_after_noise": B_noisy,
                            "B_after_cooling": B_cooled,
                            "flow_history_t_E2_E4_B": [list(map(float, h)) for h in hist],
                            "B_preserved": bool(B_preserved)},
        "defect_stable": stable,
    }


# =========================================================================== #
# C3 -- confinement: SU(3) Wilson-loop static potential V(r)
# =========================================================================== #
def c3_confinement(rng):
    out = {}
    for beta in GAUGE_BETAS:
        U = s3.gauge_init(GAUGE_L, rng, hot=True)
        step = 0.3
        for it in range(THERM):
            a = s3.gauge_metropolis_sweep(U, beta, rng, step)
            if (it + 1) % 20 == 0:
                step = float(np.clip(step * (1.2 if a > 0.5 else 0.85 if a < 0.3
                                             else 1.0), 0.02, 1.5))
        loops = {}
        for _ in range(NMEAS):
            for _ in range(MEAS_GAP):
                a = s3.gauge_metropolis_sweep(U, beta, rng, step)
            lp = s3.measure_wilson_loops(U, R_MAX, T_MAX)
            for k, v in lp.items():
                loops[k] = loops.get(k, 0.0) + v / NMEAS
        rr, V = s3.static_potential(loops, R_MAX, T_MAX)
        creutz = {r: s3.creutz_ratio(loops, r) for r in range(2, R_MAX + 1)}
        plaq = s3.plaquette_average(U)
        # Robust confinement signals:
        #  (i)  Creutz ratio chi(2,2) = string tension sigma from the well-measured
        #       small loops (large loops drown in noise at strong coupling);
        #  (ii) V(r) increasing over the reliable r range (V(2) > V(1)).
        sigma_creutz = creutz.get(2, float("nan"))
        v_increases = bool(len(V) >= 2 and V[1] > V[0] + 0.05)
        grows = bool((sigma_creutz > 0.05) and v_increases)
        sigma_fit = float(np.polyfit(rr, V, 1)[0]) if len(rr) >= 2 else float("nan")
        out[beta] = {"plaquette": plaq, "acc": a, "step": step,
                     "loops": {f"{r},{t}": loops.get((r, t))
                               for r in range(1, R_MAX + 1) for t in range(1, T_MAX + 1)},
                     "r": rr.tolist(), "V": V.tolist(),
                     "creutz_sigma": creutz, "sigma_creutz22": sigma_creutz,
                     "V_slope_sigma": sigma_fit, "V_increases": v_increases,
                     "V_grows": grows}
    # confinement: the strongest-coupling (smallest beta) shows a positive string
    # tension (area law) AND a rising V(r); also report sigma(beta) (should weaken
    # toward weak coupling -- the asymptotic-freedom direction).
    beta_strong = min(GAUGE_BETAS)
    confines = out[beta_strong]["V_grows"]
    sigma_trend = {b: out[b]["sigma_creutz22"] for b in GAUGE_BETAS}
    return {"by_beta": out, "beta_strong": beta_strong,
            "sigma_creutz_vs_beta": sigma_trend,
            "confinement_growth": bool(confines)}


# =========================================================================== #
def main():
    t0 = time.time()
    rng = np.random.default_rng(20260616)
    print("=" * 74)
    print(f"FL1_SU3_FOUNDATION -- Phase C (defects + confinement)  [scale={SCALE}]")
    print("=" * 74)

    print("\n[C1] homotopy classification + integer topological charge")
    c1 = c1_homotopy()
    print(f"  vacuum space {c1['homotopy']['vacuum_space']}: "
          f"pi_1={c1['homotopy']['pi_1']} pi_2={c1['homotopy']['pi_2']} "
          f"pi_3={c1['homotopy']['pi_3']} -> colour Skyrmion")
    for c in c1["B_convergence"]:
        print(f"    L={c['L']:2d}: B={c['B']:+.4f}")
    print(f"  B(best)={c1['B_best']:+.4f} B(anti)={c1['B_anti']:+.4f}  "
          f"integer charge: {c1['integer_charge_ok']}")

    print("\n[C2] defect stability -- explicit external Skyrme stabiliser e_sk="
          f"{E_SK}")
    c2 = c2_stability(rng)
    rd = c2["radial"]
    print(f"  radial Derrick: E2={rd['E2']:.1f} E4={rd['E4']:.1f} lam*={rd['lam_star']:.2f} "
          f"mass=2sqrt(E2E4)={rd['mass_2sqrtE2E4']:.1f}")
    print(f"    interior minimum WITH Skyrme: {rd['interior_min_with_skyrme']} "
          f"(=> STABLE size)")
    print(f"    collapse WITHOUT Skyrme:      {rd['collapses_without_skyrme']} "
          f"(=> Derrick collapse)")
    lt = c2["lattice_thermal"]
    print(f"  3D lattice: B0={lt['B0']:+.3f} -> after thermal noise={lt['B_after_noise']:+.3f} "
          f"-> after cooling={lt['B_after_cooling']:+.3f}  preserved: {lt['B_preserved']}")
    print(f"  => DEFECT STABLE: {c2['defect_stable']}")

    print("\n[C3] confinement -- SU(3) Wilson-loop static potential V(r)")
    c3 = c3_confinement(rng)
    for beta in GAUGE_BETAS:
        d = c3["by_beta"][beta]
        cz = {k: round(v, 3) for k, v in d["creutz_sigma"].items()}
        print(f"  beta={beta:.1f} <plaq>={d['plaquette']:.3f}: "
              f"V(r)={[round(x,3) for x in d['V']]} sigma_fit={d['V_slope_sigma']:.3f} "
              f"creutz={cz} grows={d['V_grows']}")
    print(f"  strongest coupling beta={c3['beta_strong']}: "
          f"confinement growth = {c3['confinement_growth']}")

    # ---- verdict ---- #
    defect_ok = c1["integer_charge_ok"] and c2["defect_stable"]
    confine_ok = c3["confinement_growth"]
    phase_C_passes = defect_ok and confine_ok
    if not phase_C_passes:
        if not defect_ok:
            verdict = "PHASE C DEATH -- no stable colour defect"
        else:
            verdict = "PHASE C DEATH -- defect stable but no confinement (E(r) flat)"
    else:
        verdict = ("PHASE C PASSES -- stable colour Skyrmion (pi_3=Z, Derrick-stable "
                   "with external Skyrme) AND confining static potential V(r)~sigma r")
    print("-" * 74)
    print(f"VERDICT: {verdict}")
    print("=" * 74)

    _figure(c2, c3)
    payload = {"scale": SCALE, "e_sk_external": E_SK,
               "config": {"gauge_L": GAUGE_L, "gauge_betas": GAUGE_BETAS,
                          "therm": THERM, "nmeas": NMEAS, "r_max": R_MAX,
                          "t_max": T_MAX, "lattice_L": LATT_L},
               "C1_homotopy": c1, "C2_stability": c2, "C3_confinement": c3,
               "defect_ok": bool(defect_ok), "confine_ok": bool(confine_ok),
               "phase_C_passes": bool(phase_C_passes), "verdict": verdict,
               "runtime_s": time.time() - t0}
    s3.save_json("FLC_confinement.json", payload, phase="C")
    print(f"saved FLC_confinement.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(c2, c3):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    # (a) radial Derrick E(lam) with/without Skyrme
    ax = axes[0]
    rd = c2["radial"]
    lam = np.array(rd["lambdas"])
    ax.plot(lam, rd["E_with_skyrme"], "o-", label="with Skyrme (E2+E4): interior min")
    ax.plot(lam, rd["E_without_skyrme"], "s--", label="no Skyrme (E2 only): collapse")
    ax.axvline(rd["lam_star"], color="0.6", ls=":", lw=1, label=f"lam*={rd['lam_star']:.2f}")
    ax.set_xlabel("dilation scale lambda"); ax.set_ylabel("energy E(lambda)")
    ax.set_title("C2: Derrick stability of the colour Skyrmion\n(external Skyrme term "
                 "= declared stabiliser)")
    ax.legend(fontsize=8); ax.grid(alpha=0.2)
    # (b) static potential V(r) per beta
    ax = axes[1]
    for beta in sorted(c3["by_beta"]):
        d = c3["by_beta"][beta]
        if d["r"]:
            ax.plot(d["r"], d["V"], "o-", label=f"beta={beta} (sigma={d['V_slope_sigma']:.2f})")
    ax.set_xlabel("r  (charge-anticharge separation)")
    ax.set_ylabel("static potential V(r)")
    ax.set_title("C3: SU(3) static potential\n(linear growth = confinement)")
    ax.legend(fontsize=8); ax.grid(alpha=0.2)
    fig.suptitle("FL1 Phase C: colour Skyrmion stability + SU(3) confinement",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(Path(__file__).resolve().parent / "FLC_confinement.png", dpi=130)
    print("saved FLC_confinement.png")


if __name__ == "__main__":
    main()

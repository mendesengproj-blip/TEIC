"""FN3b_path_AC.py -- the most-promising path (A free-mass == C shared relic).

FN3b-0 found paths A (theta with a free mass) and C (new hidden chi) converge to the
SAME relic: a misalignment scalar with f=theta0*M_Pl ~ GUT scale and m in the fuzzy
band.  This script (1) measures the NATURAL theta0 on E1's lattice (orientation_core),
(2) maps the viable (m_theta, theta0) window under Omega=0.12 AND cold-by-recombination
AND Lyman-alpha AND no-overclosure, (3) reports the fine-tuning theta0_req/theta0_nat
at the minimum-tuning (Lyman-alpha floor) point.  Writes JSON + figure.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fn3b_core as b  # noqa: E402

OUT = Path(__file__).resolve().parent


def main():
    # (1) natural theta0 from the lattice (disordered -> near-critical O(3) vacuum)
    print("=" * 76)
    print("FN3b path A/C -- lattice theta0 + viable window")
    print("=" * 76)
    lat = b.lattice_theta0(L=12, J_list=(0.0, 0.04, 0.08), n_burn=150)
    print("  natural theta0 from E1 O(3) vacuum (orientation_core):")
    for r in lat:
        print(f"    J={r['J']:.2f}: order_param={r['order_param']:.3f}  "
              f"rms_component={r['rms_component']:.3f}  theta0(angle/pi)={r['theta0_angle_over_pi']:.3f}")
    theta0_nat = float(np.mean([r["rms_component"] for r in lat]))   # ~0.577 (O(1))

    # (2) window map over mass
    masses = np.logspace(-31, -19, 200)
    th_req = np.array([b.theta0_required(m) for m in masses])
    zoscs = np.array([b.z_osc(m) for m in masses])
    cold = zoscs > b.Z_REC
    lya = masses >= b.LYA_100PCT_FLOOR
    # overclosure as frozen DE at the NATURAL theta0 (only meaningful where not cold)
    overcl = np.array([b.overclosure_ratio(m, theta0_nat) for m in masses])

    viable = cold & lya & (th_req < theta0_nat)       # Omega=0.12 reachable below natural
    # minimum-tuning viable point = lightest Lyman-alpha-safe mass (largest theta0_req)
    m_best = b.LYA_100PCT_FLOOR
    th_best = b.theta0_required(m_best)
    finetune_best = th_best / theta0_nat              # required / natural

    # the DEV-theta (slip mediator) point: dead
    m_slip = b.M_SLIP_BOUND
    th_slip = b.theta0_required(m_slip)
    overcl_slip = b.overclosure_ratio(m_slip, 1.0)
    th_slip_noover = 1.0 / np.sqrt(overcl_slip)

    rows_summary = {
        "theta0_natural_lattice": theta0_nat,
        "lattice_rows": lat,
        "min_tuning_point": {
            "m_eV": m_best, "theta0_required": float(th_best),
            "finetune_req_over_natural": float(finetune_best),
            "above_death_line_1e-3": bool(th_best > 1e-3),
            "cold_by_rec": bool(b.cold_by_recombination(m_best)),
            "lya_safe": bool(b.lya_safe_100pct(m_best)),
        },
        "dev_theta_slip_mediator": {
            "m_eV": m_slip, "theta0_required_Omega012": float(th_slip),
            "z_osc": float(b.z_osc(m_slip)),
            "cold_by_rec": bool(b.cold_by_recombination(m_slip)),
            "overclosure_at_theta0_1": float(overcl_slip),
            "theta0_max_no_overclose": float(th_slip_noover),
            "dead": True,
        },
        "any_viable_window": bool(viable.any()),
        "note": ("viable = Omega=0.12 reachable below natural theta0, cold by recomb, "
                 "and Lyman-alpha-safe as 100% DM; min-tuning at the Lyman-alpha floor."),
    }
    (OUT / "FN3b_path_AC.json").write_text(json.dumps(rows_summary, indent=2, default=float))

    print(f"\n  natural theta0 (lattice mean rms component) = {theta0_nat:.3f}")
    print(f"  viable window exists: {viable.any()}")
    print(f"  min-tuning viable point: m={m_best:.1e} eV, theta0_req={th_best:.2e}  "
          f"(finetune req/nat = {finetune_best:.1e}, above 1e-3 death line: {th_best>1e-3})")
    print(f"  DEV-theta as slip mediator (m={m_slip:.1e} eV): z_osc={b.z_osc(m_slip):.1f} "
          f"(<{b.Z_REC:.0f} -> dark energy), overcloses x{overcl_slip:.1e} at theta0=1 "
          f"-> theta0<{th_slip_noover:.1e} needed -> DEAD")
    print(f"  saved {OUT/'FN3b_path_AC.json'}")

    make_figure(masses, th_req, cold, lya, theta0_nat, m_best, th_best, m_slip, th_slip)
    return rows_summary


def make_figure(masses, th_req, cold, lya, theta0_nat, m_best, th_best, m_slip, th_slip):
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.9))

    # left: theta0_req(m) vs the constraint regions
    ax[0].loglog(masses, th_req, "k-", lw=2, label=r"$\theta_0$ required ($\Omega$=0.12)")
    ax[0].axhspan(theta0_nat * 0.7, 1.0, color="green", alpha=0.12,
                  label=r"natural $\theta_0\sim\mathcal{O}(1)$ (lattice)")
    ax[0].axhline(1e-3, color="red", ls="--", lw=1.2, label=r"death line $\theta_0=10^{-3}$")
    # shade dark-energy region (not cold by recomb) and Lyman-alpha exclusion
    m_cold_thr = masses[np.argmax(cold)] if cold.any() else masses[-1]
    ax[0].axvspan(masses[0], m_cold_thr, color="purple", alpha=0.10,
                  label="dark energy (not cold by z=1100)")
    ax[0].axvspan(masses[0], b.LYA_100PCT_FLOOR, color="orange", alpha=0.08,
                  label=r"Ly$\alpha$ excludes as 100% DM")
    ax[0].axvline(b.LYA_100PCT_FLOOR, color="orange", ls=":", lw=1.2)
    ax[0].plot([m_best], [th_best], "g*", ms=15, label="min-tuning viable point")
    ax[0].plot([m_slip], [th_slip], "rx", ms=11, mew=2.5, label="DEV-θ (slip mediator): DEAD")
    ax[0].set_xlabel(r"$m_\theta$ [eV]"); ax[0].set_ylabel(r"$\theta_0$")
    ax[0].set_ylim(1e-4, 3)
    ax[0].set_title("FN3b A/C: required vs natural misalignment")
    ax[0].legend(fontsize=6.5, loc="lower left")

    # right: oscillation epoch z_osc(m) vs recombination
    zoscs = np.array([max(b.z_osc(m), 1e-1) for m in masses])
    ax[1].loglog(masses, zoscs, "b-", lw=1.6, label=r"$z_{\rm osc}$ (3H=m)")
    ax[1].axhline(b.Z_REC, color="k", ls="--", lw=1.2, label="recombination z=1100")
    ax[1].axvspan(masses[0], b.LYA_100PCT_FLOOR, color="orange", alpha=0.08)
    ax[1].axvline(b.M_SLIP_BOUND, color="red", ls=":", lw=1.2,
                  label="slip mediator bound 6.4e-30 eV")
    ax[1].set_xlabel(r"$m_\theta$ [eV]"); ax[1].set_ylabel(r"$z_{\rm osc}$")
    ax[1].set_title("FN3b A/C: cold (DM) only if it oscillates before z=1100")
    ax[1].legend(fontsize=7, loc="lower right")

    fig.suptitle("FN3b path A/C: Omega=0.12 viable only at m>~2e-21 eV with theta0~4e-3 "
                 "(mild tuning, NEW scale); DEV-theta (light) is dark energy", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "FN3b_path_AC.png", dpi=130)
    print(f"  saved {OUT/'FN3b_path_AC.png'}")


if __name__ == "__main__":
    main()

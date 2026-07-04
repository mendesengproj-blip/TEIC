"""A3_beta_stiffness.py -- does the DEV coupling beta=0.0070 come from the ferromagnet's
spin stiffness: beta = rho_s(J0)/K at the physical operating point J0?

Campaign DEV_FROM_TEIC, angle A3.  Charter: results/dev_from_teic/DEV_FROM_TEIC.md.

Background already MEASURED (build on it):
  * C1 / FM2-1: rho_s(J) (helicity modulus) measured; spans 0.25->1.16 over J=0.9->2.2.
  * MG1 / D3D: the gravity sector uses the action stiffness K (G_net = A/K, G_net ∝ 1/K);
    the lattice normalisation is K_STIFF = 1.0.
  * The program's physical vacuum / operating point is J0 = 1.0 (used throughout E1..MG1).

Hypothesis (the prompt): beta = rho_s(J0)/K, the same K as G_net = A/K.

What we do: measure rho_s(J)/K over a fine J-grid (engine fm2_core), and ask whether
beta=0.0070 is reproduced at a REASONABLE operating point J0 -- or only by fine-tuning
J0 to the critical point (where rho_s -> 0).

PRE-REGISTERED honesty (charter point 3): the comparison rho_s/K vs the dimensionless
beta requires a UNIT assumption (what is "one lattice unit" of acceleration?).  We
declare K=1 (the gravity-sector normalisation) explicitly as [ASSUMIDO]; beta is
COMPARISON ONLY.

Reading:
  A3-OPERATING  rho_s(J0=1)/K at the physical vacuum vs beta: O(beta) => candidate;
                off by a large factor => not at the operating point.
  A3-TUNE       the J0 where rho_s/K = beta: if it sits right at J_c (rho_s->0,
                fine-tuned), it is not a derivation -> [EXTERNO-B]/[INCONCLUSIVO].

Anti-circularity: beta=0.0070 only in the COMPARISON block; engine uses J, rho_s, K.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "results" / "cmb" / "fm2"))
import fm2_core as fm2  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

L = 16
J0_OPERATING = 1.0                 # the program's physical vacuum (E1..MG1)
K_STIFF = 1.0                      # gravity-sector action stiffness (MG1/D3D); [ASSUMIDO]
J_GRID = [0.70, 0.72, 0.75, 0.80, 0.85, 0.90, 1.00, 1.10, 1.30, 1.60, 1.90]
SEEDS = [0, 1, 2, 3]
N_BURN, N_MEAS = 500, 160

# ---- COMPARISON ONLY ----
BETA_DEV = 0.0070                  # DEV coupling, calibrated on SPARC (comparison point)


def rho_of_J(J):
    vals, ms = [], []
    for sd in SEEDS:
        rho, mabs = fm2.helicity_modulus_series(L, J, seed=sd, n_burn=N_BURN, n_meas=N_MEAS)
        vals.append(rho); ms.append(mabs)
    return float(np.mean(vals)), float(np.std(vals) / np.sqrt(len(SEEDS))), float(np.mean(ms))


def main():
    t0 = time.time()
    print("=" * 78)
    print("A3 -- is beta=0.0070 = rho_s(J0)/K of the TEIC ferromagnet?")
    print("=" * 78)

    Js = np.array(J_GRID, float)
    rho, sem, mabs = [], [], []
    for J in J_GRID:
        r, e, m = rho_of_J(J)
        rho.append(r); sem.append(e); mabs.append(m)
        print(f"  J={J:.2f}: rho_s={r:.4f} +- {e:.4f}   rho_s/K={r/K_STIFF:.4f}   m_abs={m:.3f}")
    rho = np.array(rho); sem = np.array(sem); mabs = np.array(mabs)
    beta_lat = rho / K_STIFF                      # rho_s/K (= rho_s since K=1)

    # ---- locate J_c: rho_s extrapolates to 0 (linear near criticality) ----
    near = (Js <= 1.0)
    cj, ci = np.polyfit(Js[near], rho[near], 1)   # rho ~ cj*J + ci
    J_c = float(-ci / cj) if cj != 0 else float("nan")

    # ---- A3-OPERATING: rho_s/K at J0=1 ----
    rho_J0 = float(np.interp(J0_OPERATING, Js, rho))
    beta_at_J0 = rho_J0 / K_STIFF
    ratio_J0 = beta_at_J0 / BETA_DEV               # COMPARISON

    # ---- A3-TUNE: the J0 where rho_s/K = beta ----
    target = BETA_DEV * K_STIFF
    # rho_s is monotone increasing in J; find J where rho_s = target by interpolation
    if rho.min() <= target <= rho.max():
        J_beta = float(np.interp(target, rho, Js))
    elif target < rho.min():
        # below the grid: linear-extrapolate toward J_c using the near-critical slope
        J_beta = float((target - ci) / cj)
    else:
        J_beta = float("nan")
    # how fine-tuned: distance from J_c relative to the operating range
    tune = float((J_beta - J_c) / (J0_OPERATING - J_c)) if np.isfinite(J_beta) else float("nan")

    # ---- verdict ----
    operating_match = bool(0.5 < ratio_J0 < 2.0)    # O(beta) at the physical vacuum?
    fine_tuned = bool(np.isfinite(tune) and tune < 0.15)   # J_beta sits within 15% of J_c
    if operating_match:
        status = "IDENTIFICADO"
        verdict = ("rho_s(J0=1)/K = %.4f is O(beta=%.4f) (ratio %.2f) at the physical "
                   "operating point -> beta is a candidate network quantity [IDENTIFICADO] "
                   "(unit map [ASSUMIDO], scale external)." % (beta_at_J0, BETA_DEV, ratio_J0))
    elif fine_tuned:
        status = "EXTERNO-B"
        verdict = ("at the physical vacuum J0=1, rho_s/K=%.3f is %.0fx the DEV beta=%.4f; "
                   "rho_s/K only equals beta at J0=%.3f, which sits right at the critical "
                   "point J_c=%.3f (tuning %.2f of the way from J_c to J0 -- near-critical, "
                   "unnatural).  No reasonable operating point gives beta; with the unit map "
                   "also [ASSUMIDO], beta stays [EXTERNO-B]." %
                   (beta_at_J0, ratio_J0, BETA_DEV, J_beta, J_c, tune))
    else:
        status = "INCONCLUSIVO"
        verdict = ("rho_s/K = beta at J0=%.3f (J_c=%.3f, tuning %.2f); neither clearly at "
                   "the operating point nor pinned to J_c.  With the unit map [ASSUMIDO], "
                   "at best a suggestive identification, not a derivation [INCONCLUSIVO]." %
                   (J_beta, J_c, tune))

    print("-" * 78)
    print(f"  J_c (rho_s->0 extrapolation) = {J_c:.3f}")
    print(f"  A3-OPERATING: rho_s(J0=1)/K = {beta_at_J0:.4f}  vs beta={BETA_DEV:.4f}  "
          f"(ratio {ratio_J0:.2f})")
    print(f"  A3-TUNE: rho_s/K = beta at J0={J_beta:.3f}  (tuning {tune:.2f} from J_c to J0)")
    print(f"  unit map K=1 declared [ASSUMIDO]; beta COMPARISON ONLY")
    print(f"  STATUS beta: [{status}]")
    print(f"  VERDICT: {verdict}")
    print("=" * 78)

    _figure(Js, rho, sem, beta_lat, J_c, J_beta, BETA_DEV)
    payload = {
        "angle": "A3 -- beta from the ferromagnet stiffness (beta = rho_s(J0)/K)",
        "engine": "fm2_core O(3) ferromagnet (E1)", "L": L, "K_stiff": K_STIFF,
        "J0_operating": J0_OPERATING, "J_grid": J_GRID, "seeds": len(SEEDS),
        "rho_s": rho.tolist(), "rho_s_sem": sem.tolist(), "m_abs": mabs.tolist(),
        "beta_lattice_rho_over_K": beta_lat.tolist(),
        "J_c_estimate": J_c,
        "rho_s_at_J0": rho_J0, "beta_at_J0": beta_at_J0, "ratio_J0_over_betaDEV": ratio_J0,
        "J0_where_rho_over_K_equals_beta": J_beta, "fine_tune_from_Jc": tune,
        "operating_match": operating_match, "fine_tuned": fine_tuned,
        "comparison_only": {"beta_DEV": BETA_DEV,
                            "unit_assumption": "K=1 (gravity-sector normalisation), [ASSUMIDO]"},
        "status_beta": status, "verdict": verdict,
        "anti_circularity": "beta only in COMPARISON block; generator uses J,rho_s,K",
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "A3_beta_stiffness.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved A3_beta_stiffness.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(Js, rho, sem, beta_lat, J_c, J_beta, beta_dev):
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 5))
    ax.errorbar(Js, beta_lat, yerr=sem, marker="o", lw=1.6, label=r"$\rho_s(J)/K$ (network)")
    ax.axhline(beta_dev, color="r", ls="--", lw=1.2, label=fr"$\beta_{{DEV}}={beta_dev}$ (COMPARISON)")
    if np.isfinite(J_c):
        ax.axvline(J_c, color="gray", ls=":", lw=1, label=fr"$J_c\approx{J_c:.2f}$")
    if np.isfinite(J_beta):
        ax.plot([J_beta], [beta_dev], "r*", ms=14)
    ax.axvline(1.0, color="k", ls="-", lw=0.8, alpha=0.5, label="operating point J0=1")
    ax.set_yscale("log")
    ax.set_xlabel("coupling J"); ax.set_ylabel(r"$\rho_s/K$  (candidate $\beta$)")
    ax.set_title("A3: beta vs the ferromagnet stiffness rho_s(J)/K\n"
                 "(beta is reached only near J_c, not at the operating point J0=1)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "A3_beta_stiffness.png", dpi=130)
    print("saved A3_beta_stiffness.png")


if __name__ == "__main__":
    main()

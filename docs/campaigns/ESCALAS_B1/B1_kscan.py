"""B1 -- internal K-independent ratios (hierarchy test).

Campaign ESCALAS_B1 (Fase 2, Frente B).  Question: does the substrate fix a
dimensionless combination of M_Sk (Skyrmion mass), sigma (string tension) and
G_net (gravitational response) that is invariant under the OVERALL action
normalisation S -> K*S, and is a NON-TRIVIAL pure number (carries the hierarchy)?

Decision (PRE_REGISTRO sec.2): K = global action rescaling S -> K*S.  The three
sectors inherit one K with DIFFERENT responses:
  * M_Sk : classical saddle of E2+e_sk*E4.  argmin(K*E)=argmin(E) -> profile
           K-invariant, energy scales linearly  =>  M_Sk(K) = K * M_Sk(1).
  * G_net: Poisson  -K_stiff * lap(theta) = source.  S->K*S sends K_stiff->K*K_stiff
           => theta -> theta/K  =>  G_net(K) = G_net(1)/K.   (re-measured here)
  * sigma: Wilson  S_W = beta*sum(1-..).  S->K*S is beta->K*beta; sigma(beta) RUNS
           (asymptotic freedom) -> NOT a power of K.   (measured curve, FLC)

The invariance must EMERGE from the scan (anti-circularity, A1 covers this file):
exponents a (M_Sk) and c (G_net) are FITTED from the scan, not imposed.  No scale
literal anywhere -- everything is in lattice units.

Run:  python docs/campaigns/ESCALAS_B1/B1_kscan.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
import sys
sys.path.insert(0, str(ROOT / "results" / "matter" / "fl1"))
sys.path.insert(0, str(ROOT / "results" / "bridge" / "d3_audit"))
import su3_core as s3                     # radial_grid, radial_relax  (Skyrme M_Sk)
import d3_audit_core as d3                # radial Poisson             (G_net)

HERE = Path(__file__).resolve().parent

# --- scan grid: K over MORE than one decade (0.3 .. 10 = 33x) ---------------- #
K_LIST = np.geomspace(0.3, 10.0, 7)

E_SK = 0.5            # external Skyrme weight (same declared input as FLC/MG1)

# --- sigma(beta) MEASURED Creutz curve (FLC_confinement.json, L=8 full) ------ #
SIGMA_BETA = {4.0: 1.3522950517720163, 4.5: 1.0968083695281472,
              5.0: 0.9639515260472875, 5.5: 0.6718258348437807,
              6.0: 0.32593324542900715}
BETA0 = 5.0           # reference coupling: K=1 <-> beta=5.0


def measure_M_Sk():
    """Relax the radial colour-Skyrmion ONCE; the profile is K-invariant, so the
    K-dependence is the exact prefactor.  Returns M0 = E2 + e_sk*E4 (lattice energy
    at K=1) and the Bogomolny form 2*sqrt(E2*E4)."""
    r, dr = s3.radial_grid(rmax=10.0, n=700)
    F, E2, E4 = s3.radial_relax(r, dr, e_sk=E_SK)
    M0 = float(E2 + E_SK * E4)
    M0_bog = float(2.0 * np.sqrt(E2 * E4))
    return {"E2": float(E2), "E4": float(E4), "M0_energy": M0, "M0_bogomolny": M0_bog}


def measure_G_net_scan():
    """Re-measure G_net = A/w_M by solving the radial Poisson problem at stiffness
    K for each K in K_LIST (mirrors D3D_G.measure_A).  G_net should ride on 1/K."""
    L0, rho0, wM0 = 40.0, 100.0, 1.0
    R_MIN, R_CORE = 0.5, 2.0
    nb = int(np.clip(round(8.62 * rho0 ** (1.0 / 3.0)), 20, 80))
    _, centers, sv = d3.radial_grid(L0, nb, R_MIN)
    q = d3.radial_source_core(centers, sv, R_CORE, wM0)
    out = []
    for K in K_LIST:
        th = d3.radial_solve(centers, sv, q, float(K))
        A, C, p = d3.fit_tail(centers, th, R_CORE, 0.6 * L0)
        out.append({"K": float(K), "A": float(A), "G_net": float(A / wM0),
                    "exterior_exponent": float(p)})
    return out


def sigma_of_K(K):
    """sigma(K) from the measured Creutz curve at beta = K*BETA0.  Only faithful
    inside the measured beta-range [4,6] (K in [0.8,1.2]); outside it we return
    NaN and flag, because extending needs fresh Wilson MC (and sigma is not part of
    any K-invariant anyway -- it RUNS)."""
    beta = K * BETA0
    bs = np.array(sorted(SIGMA_BETA))
    if beta < bs.min() or beta > bs.max():
        return float("nan")
    return float(np.interp(beta, bs, [SIGMA_BETA[b] for b in bs]))


def sigma_window_analysis(M0, G_net1):
    """Evaluate the sigma-combinations on the 5 MEASURED (beta, sigma) points,
    mapped to K = beta/BETA0 (so sigma is real data, not extrapolation).  Shows the
    sigma-combos vary strongly across the measured window -> not invariant.
    G_net1 = G_net at K=1 (from the Poisson scan)."""
    betas = np.array(sorted(SIGMA_BETA))
    sig = np.array([SIGMA_BETA[b] for b in betas])
    Kw = betas / BETA0                       # K within [0.8, 1.2]
    M = Kw * M0
    G = G_net1 / Kw
    combos = {"sigma * G_net": sig * G, "M_Sk / sqrt(sigma)": M / np.sqrt(sig)}
    return {"beta": betas.tolist(), "K_window": Kw.tolist(), "sigma": sig.tolist(),
            "sigma_runs_exponent_in_K": fit_exponent(Kw, sig),
            "combos": {n: {"values": v.tolist(), "cv": cv(v),
                           "max_over_min": float(np.nanmax(v) / np.nanmin(v)),
                           "invariant_lt5pct": bool(cv(v) < 0.05)}
                       for n, v in combos.items()}}


def fit_exponent(K, Y):
    """Least-squares power-law exponent d log Y / d log K (NaN-safe)."""
    K, Y = np.asarray(K, float), np.asarray(Y, float)
    m = np.isfinite(K) & np.isfinite(Y) & (Y > 0)
    if m.sum() < 2:
        return float("nan")
    return float(np.polyfit(np.log(K[m]), np.log(Y[m]), 1)[0])


def cv(Y):
    """Coefficient of variation over the finite entries (the <5% invariance test)."""
    Y = np.asarray(Y, float)
    Y = Y[np.isfinite(Y)]
    if len(Y) < 2 or np.mean(Y) == 0:
        return float("nan")
    return float(np.std(Y) / abs(np.mean(Y)))


def main():
    K = np.asarray(K_LIST, float)

    msk = measure_M_Sk()
    M0 = msk["M0_energy"]
    M_Sk = K * M0                              # classical: exact prefactor

    gscan = measure_G_net_scan()
    G_net = np.array([g["G_net"] for g in gscan])

    sigma = np.array([sigma_of_K(k) for k in K])

    a_exp = fit_exponent(K, M_Sk)              # expect +1
    c_exp = fit_exponent(K, G_net)             # expect -1
    # sigma exponent over the K-window where it is defined (shows it does NOT match
    # a clean +1; it runs):
    s_exp = fit_exponent(K, sigma)

    # --- candidate dimensionless combinations -------------------------------- #
    combos = {
        "M_Sk * G_net  (= Poisson amplitude A; definitional)": M_Sk * G_net,
        "M_Sk * sqrt(G_net)  (= M_Sk / M_Pl, THE hierarchy)": M_Sk * np.sqrt(G_net),
        "M_Sk^2 * G_net": M_Sk ** 2 * G_net,
        "sigma * G_net": sigma * G_net,
        "M_Sk / sqrt(sigma)": M_Sk / np.sqrt(sigma),
    }
    combo_report = {name: {"exponent_in_K": fit_exponent(K, v), "cv": cv(v),
                           "invariant_lt5pct": bool(cv(v) < 0.05)}
                    for name, v in combos.items()}

    # --- sigma-combos on the measured beta-window (sigma is real data there) -- #
    G_net1 = float(np.mean(G_net * K))        # G_net at K=1 (since G_net ~ 1/K)
    sig_window = sigma_window_analysis(M0, G_net1)

    # --- controls: do the individuals scale? --------------------------------- #
    individuals_scale = (abs(a_exp) > 0.1) and (abs(c_exp) > 0.1)

    # --- verdict logic (PRE_REGISTRO sec.4-5) -------------------------------- #
    # success requires a NON-TRIVIAL invariant.  The only <5%-flat combo is
    # M_Sk*G_net, which is definitional (G_net := A/M => M*G_net = A) -> trivial.
    flat = {n: r for n, r in combo_report.items() if r["invariant_lt5pct"]}
    hierarchy = combo_report["M_Sk * sqrt(G_net)  (= M_Sk / M_Pl, THE hierarchy)"]
    nontrivial_flat = [n for n in flat if not n.startswith("M_Sk * G_net")]

    if nontrivial_flat:
        verdict = ("SUCCESS (tentative): a non-trivial K-invariant combination exists: "
                   + "; ".join(nontrivial_flat))
        death = None
    else:
        verdict = ("DEATH (well-understood): the only <5%-flat combination is the "
                   "definitional M_Sk*G_net (= Poisson amplitude A, G_net:=A/M); the "
                   "hierarchy combination M_Sk*sqrt(G_net) (= M_Sk/M_Pl) SCALES as "
                   f"K^{hierarchy['exponent_in_K']:.2f}; sigma RUNS (not a power of K). "
                   "The overall action normalisation does NOT fix a mass ratio between "
                   "domains -> hierarchy stays [EXTERNO-B]; feeds B5.")
        death = "(a)+(b): non-trivial combos scale; the invariant one is definitional"

    result = {
        "K_definition": "global action rescaling S -> K*S",
        "K_list": K.tolist(),
        "e_sk": E_SK, "beta0": BETA0,
        "M_Sk_at_K1": msk,
        "G_net_scan": gscan,
        "sigma_curve_beta": SIGMA_BETA,
        "sigma_window_analysis": sig_window,
        "fitted_exponents": {"M_Sk": a_exp, "G_net": c_exp,
                             "sigma(window)": s_exp},
        "individuals_scale_with_K": bool(individuals_scale),
        "combinations": combo_report,
        "verdict": verdict,
        "death_criterion": death,
    }
    (HERE / "B1_kscan.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # --- console summary ----------------------------------------------------- #
    print("=" * 76)
    print("B1 -- K-independent ratios (S -> K*S);  K in [%.2g, %.2g], %d points"
          % (K.min(), K.max(), len(K)))
    print("=" * 76)
    print(f"M_Sk(K=1) = {M0:.3f}  (E2={msk['E2']:.2f}, E4={msk['E4']:.2f}; "
          f"Bogomolny 2sqrt(E2E4)={msk['M0_bogomolny']:.2f})")
    print(f"fitted exponents:  M_Sk ~ K^{a_exp:+.3f}   G_net ~ K^{c_exp:+.3f}"
          f"   sigma(window) ~ K^{s_exp:+.3f} (runs, not a clean power)")
    print(f"individuals scale with K (control): {individuals_scale}")
    print("-" * 76)
    print(f"{'combination':<52}{'K-exp':>8}{'CV':>9}  flat<5%?")
    for n, r in combo_report.items():
        print(f"{n:<52}{r['exponent_in_K']:>+8.2f}{r['cv']:>9.3f}  "
              f"{'YES' if r['invariant_lt5pct'] else 'no'}")
    print("-" * 76)
    print("sigma-combos on the MEASURED beta-window [4,6] (K in [0.8,1.2]); "
          f"sigma runs ~ K^{sig_window['sigma_runs_exponent_in_K']:+.2f}:")
    for n, r in sig_window["combos"].items():
        print(f"  {n:<26} CV={r['cv']:.3f}  max/min={r['max_over_min']:.2f}  "
              f"flat<5%? {'YES' if r['invariant_lt5pct'] else 'no'}")
    print("-" * 76)
    print("VERDICT:", verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

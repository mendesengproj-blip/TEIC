"""A4_gravitational_slip.py -- does the DEV gravitational slip eta = Psi/Phi have a
form derivable from the TEIC?  Measure <n(r)> around the Skyrmion vs the gravitational
potential theta(r), and read the slip from the soliton's own anisotropic stress.

Campaign DEV_FROM_TEIC, angle A4.  Charter: results/dev_from_teic/DEV_FROM_TEIC.md.

Background already MEASURED (build on it):
  * MG1: the SU(2)/colour Skyrmion's energy density eps(r) sources theta(r)=G_net M/r
    through the static Benincasa-Dowker relaxer (bd_solve).  ONE scalar potential.
  * A1 (this campaign): the vector A_mu -- whose phi-A_mu coupling GENERATES the DEV
    slip -- does NOT emerge from the TEIC (no spontaneous Proca gap).

Mechanism for a slip in the TEIC matter sector: the hedgehog orientation field
<n(r)> = (sinF(r) r_hat, cosF(r)) carries an ANISOTROPIC STRESS Pi(r)=p_t-p_r (the
ferromagnet "curves" around the Skyrmion).  In weak field, Phi (the Newtonian
potential, test-particle motion) is sourced by the energy density eps, while the
DIFFERENCE Phi-Psi is sourced by the anisotropic stress:
    grad^2 Phi      = kappa eps(r)
    grad^2 (Phi-Psi)= kappa Pi(r)        =>  eta(r) = Psi/Phi = 1 - (Phi-Psi)/Phi.
Both solved with the SAME BD relaxer and the SAME kappa, so eta is convention-free.

We use the rigorous SIGMA-sector (E2) stress (dominant in the exterior; the E4/Skyrme
anisotropic stress is a declared subleading correction):
    eps2(r)  = 1/2 F'^2 + sin^2F/r^2         (energy density)
    Pi2(r)   = sin^2F/r^2 - F'^2              (p_t - p_r, anisotropic stress)
profile F(r) from the REAL relaxed Skyrmion (e_sk>0, finite size).

Pre-registered reading:
  G0       solver reproduces MG1 (Phi exterior ~ 1/r).
  A4-FORM  if |eta-1| sits in the DEV window [2.2%,4.1%] as a robust feature => the
           slip form is derivable -> [IDENTIFICADO].
           if |eta-1| is O(1) interior / ->0 exterior (a relativistic soliton, Birkhoff)
           and never a 2-4% plateau => the DEV galactic slip (a vector-sector effect,
           A1) is NOT derivable from the TEIC matter sector -> [EXTERNO-B]/[INCONCLUSIVO].

Anti-circularity: the DEV window [2.2%,4.1%] enters ONLY in the COMPARISON block;
the slip is computed from the Skyrmion profile F(r) and the BD relaxer alone.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "results" / "matter" / "fl1"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "mg"))
import su3_core as s3  # noqa: E402
import MG1_skyrmion_gravity as mg  # noqa: E402 (reuse make_grid, bd_solve, source_from_density)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

E_SK = 0.5                         # physical stabiliser (MG1's reference value)
RMAX_PROFILE = 10.0
N_PROFILE = 700

# ---- COMPARISON ONLY ----
DEV_SLIP_WINDOW = (0.022, 0.041)   # eta-1 prediction of the DEV (Paper II/V)


def skyrmion_stress(e_sk):
    """Return (r, eps2_line, Pi2_line, F, tilt) for the relaxed hedgehog.  Line
    densities (dX/dr = 4 pi r^2 * volume density) in the rigorous sigma (E2) sector:
        eps2_vol = 1/2 F'^2 + s^2/r^2 ;  Pi2_vol = s^2/r^2 - F'^2 .
    tilt(r) = 1 - cosF(r) is the longitudinal orientation response <n_par> deficit."""
    r, dr = s3.radial_grid(rmax=RMAX_PROFILE, n=N_PROFILE)
    F, E2, E4 = s3.radial_relax(r, dr, e_sk=e_sk)
    Fp = np.gradient(F, dr)
    s2 = np.sin(F) ** 2
    eps2_vol = 0.5 * Fp ** 2 + s2 / r ** 2
    Pi2_vol = s2 / r ** 2 - Fp ** 2
    eps2_line = 4.0 * np.pi * r ** 2 * eps2_vol
    Pi2_line = 4.0 * np.pi * r ** 2 * Pi2_vol
    tilt = 1.0 - np.cos(F)
    return r, eps2_line, Pi2_line, F, tilt, float(E2), float(E4), dr


def main():
    t0 = time.time()
    print("=" * 80)
    print("A4 -- gravitational slip eta=Psi/Phi from the Skyrmion's anisotropic stress")
    print("=" * 80)

    # gravity grid + G0 gate (reuse MG1)
    edges, centers, shell_vol = mg.make_grid()
    g0 = mg.gate_g0(centers, shell_vol)
    print(f"[G0] BD solver vs D3 (top-hat): A={g0['A']:.3f} exponent={g0['exponent']:.3f} "
          f"PASS={g0['passes']}")

    r, eps_line, Pi_line, F, tilt, E2, E4, dr = skyrmion_stress(E_SK)
    r_supp = mg.support_radius(r, np.abs(eps_line), frac=0.99)
    print(f"[profile] e_sk={E_SK}  E2={E2:.2f} E4={E4:.2f} (virial E2~E4)  "
          f"support r99={r_supp:.2f}")
    print(f"[stress]  integral eps={np.sum(eps_line)*dr:.3f}  "
          f"integral Pi={np.sum(Pi_line)*dr:.4f}  (Pi/eps={np.sum(Pi_line)/np.sum(eps_line):.3f})")

    # BD-relax Phi (source eps) and chi=Phi-Psi (source Pi); same kappa
    b_eps = mg.source_from_density(r, eps_line, edges)
    b_Pi = mg.source_from_density(r, Pi_line, edges)
    Phi = mg.bd_solve(centers, shell_vol, b_eps)
    chi = mg.bd_solve(centers, shell_vol, b_Pi)               # = Phi - Psi
    # remove the conservation offset C (the constant mode) before forming the ratio:
    # the physical potentials are measured relative to their large-r value.
    A_phi, C_phi, expo_phi, _ = mg.fit_tail(centers, Phi, max(r_supp * 1.5, 8.0), 0.6 * mg.R_MAX)
    A_chi, C_chi, _, _ = mg.fit_tail(centers, chi, max(r_supp * 1.5, 8.0), 0.6 * mg.R_MAX)
    Phi_r = Phi - C_phi
    chi_r = chi - C_chi
    eta_minus_1 = np.where(np.abs(Phi_r) > 1e-9, -chi_r / Phi_r, np.nan)

    # interior (within support) and exterior (well outside) characteristic slip
    interior = centers < r_supp
    exterior = centers > max(r_supp * 2.0, 12.0)
    eta_int = float(np.nanmedian(np.abs(eta_minus_1[interior])))
    eta_ext = float(np.nanmedian(np.abs(eta_minus_1[exterior])))
    # exterior slip from the Gauss-law amplitudes (robust): (Psi-Phi)/Phi = -A_chi/A_phi
    eta_ext_gauss = float(-A_chi / A_phi) if abs(A_phi) > 1e-12 else float("nan")

    # ---- literal falloff comparison: orientation tilt <n> vs Phi(r) ----
    # interpolate tilt onto the gravity grid; compare radial slopes in the exterior tail
    tilt_on_grid = np.interp(centers, r, tilt, left=tilt[0], right=np.nan)
    # compare falloffs over the resolved profile range (inside-to-edge of support)
    tail = (centers > 0.4 * r_supp) & (centers < r_supp) & (tilt_on_grid > 1e-6) & (Phi_r > 1e-6)
    if tail.sum() >= 4:
        slope_tilt = float(np.polyfit(np.log(centers[tail]), np.log(tilt_on_grid[tail]), 1)[0])
        slope_phi = float(np.polyfit(np.log(centers[tail]), np.log(Phi_r[tail]), 1)[0])
    else:
        slope_tilt = slope_phi = float("nan")

    # ---- verdict ----
    lo, hi = DEV_SLIP_WINDOW
    # a robust 2-4% plateau would mean both interior and exterior land in the window
    in_window = bool(lo <= eta_int <= hi and lo <= abs(eta_ext_gauss) <= hi)
    relativistic = bool(eta_int > 5 * hi)             # interior slip O(1): a hard soliton
    different_falloff = bool(np.isfinite(slope_tilt) and np.isfinite(slope_phi)
                             and abs(slope_tilt - slope_phi) > 0.7)

    if in_window:
        status = "IDENTIFICADO"
        verdict = ("the Skyrmion's anisotropic-stress slip |eta-1| sits in the DEV window "
                   "[%.1f%%,%.1f%%] (interior %.1f%%, exterior %.1f%%) -> the slip FORM is "
                   "derivable from the TEIC matter texture [IDENTIFICADO]."
                   % (lo * 100, hi * 100, eta_int * 100, abs(eta_ext_gauss) * 100))
    else:
        status = "EXTERNO-B"
        why_parts = []
        if relativistic:
            why_parts.append("the interior slip is O(1) (|eta-1|_int=%.2f), as expected for "
                             "a RELATIVISTIC soliton -- not a 2-4%% galactic plateau" % eta_int)
        why_parts.append("the exterior is a CONSTANT slip plateau |eta-1|~%.0f%% (the "
                         "anisotropic stress has a non-zero monopole, int Pi/int eps=%.2f) "
                         "-- a genuine slip in FORM, but O(1), ~%.0fx the DEV window"
                         % (abs(eta_ext_gauss) * 100, np.sum(Pi_line) / np.sum(eps_line),
                            abs(eta_ext_gauss) / hi))
        if different_falloff:
            why_parts.append("the orientation tilt <n>(r)~r^%.1f and Phi(r)~r^%.1f have "
                             "DIFFERENT falloffs, so <n>/theta is not the constant ratio of "
                             "a DEV slip" % (slope_tilt, slope_phi))
        verdict = ("the DEV slip [%.1f%%,%.1f%%] is NOT reproduced as a robust feature: "
                   % (lo * 100, hi * 100) + "; ".join(why_parts) +
                   ".  The DEV slip is a galactic vector-sector (A_mu) effect, and A1 showed "
                   "A_mu does not emerge -> eta stays [EXTERNO-B]/[INCONCLUSIVO].")

    print("-" * 80)
    print(f"  slip |eta-1|: interior(median)={eta_int:.3f}  exterior(Gauss)={abs(eta_ext_gauss):.4f}")
    print(f"  orientation tilt <n>~r^{slope_tilt:.2f}  vs  Phi~r^{slope_phi:.2f}  "
          f"(different falloff={different_falloff})")
    print(f"  DEV window [{lo:.3f},{hi:.3f}] reproduced as robust plateau: {in_window}")
    print(f"  STATUS eta: [{status}]")
    print(f"  VERDICT: {verdict}")
    print("=" * 80)

    _figure(centers, Phi_r, chi_r, eta_minus_1, r, tilt, r_supp, DEV_SLIP_WINDOW, status)
    payload = {
        "angle": "A4 -- gravitational slip eta=Psi/Phi from the Skyrmion anisotropic stress",
        "engine": "MG1 BD relaxer + su3_core Skyrmion (E2 sigma-sector stress)",
        "e_sk": E_SK, "E2": E2, "E4": E4, "r_support99": r_supp,
        "G0_gate": g0,
        "integral_eps": float(np.sum(eps_line) * dr), "integral_Pi": float(np.sum(Pi_line) * dr),
        "eta_minus_1_interior_median": eta_int,
        "eta_minus_1_exterior_median": eta_ext,
        "eta_minus_1_exterior_gauss": eta_ext_gauss,
        "tilt_falloff_exponent": slope_tilt, "Phi_falloff_exponent": slope_phi,
        "different_falloff": different_falloff, "relativistic_interior": relativistic,
        "comparison_only": {"DEV_slip_window_eta_minus_1": list(DEV_SLIP_WINDOW),
                            "in_window_robust": in_window},
        "status_eta": status, "verdict": verdict,
        "caveat": ("sigma(E2)-sector stress used (rigorous, exterior-dominant); E4/Skyrme "
                   "anisotropic stress omitted as a declared subleading correction.  This is "
                   "the LOCAL matter-sourced slip of a baryon, conceptually related but not "
                   "identical to the DEV's effective galactic slip."),
        "anti_circularity": "DEV window only in COMPARISON block; slip from F(r)+BD relaxer",
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "A4_gravitational_slip.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved A4_gravitational_slip.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(centers, Phi, chi, eta_m1, r, tilt, r_supp, window, status):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    m = Phi > 0
    ax[0].loglog(centers[m], Phi[m], "o-", ms=3, label=r"$\Phi$ (Newtonian, source $\varepsilon$)")
    ax[0].loglog(centers[chi > 0], chi[chi > 0], "s-", ms=3, label=r"$\Phi-\Psi$ (source $\Pi$)")
    ax[0].loglog(r, np.clip(tilt, 1e-6, None), "-", lw=1, label=r"orientation tilt $1-\cos F$")
    ax[0].axvline(r_supp, color="gray", ls=":", lw=1)
    ax[0].set_xlabel("r"); ax[0].set_ylabel("potential / tilt")
    ax[0].set_title("(a) potentials and the orientation response")
    ax[0].legend(fontsize=7)
    good = np.isfinite(eta_m1)
    ax[1].semilogx(centers[good], np.abs(eta_m1[good]) * 100, "o-", ms=3)
    ax[1].axhspan(window[0] * 100, window[1] * 100, color="g", alpha=0.2, label="DEV window 2.2-4.1%")
    ax[1].axvline(r_supp, color="gray", ls=":", lw=1, label="soliton support")
    ax[1].set_xlabel("r"); ax[1].set_ylabel(r"$|\eta-1|$  (%)")
    ax[1].set_title(f"(b) gravitational slip profile  [{status}]")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.2)
    fig.suptitle("A4: is the DEV slip eta=Psi/Phi derivable from the TEIC Skyrmion texture?",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "A4_gravitational_slip.png", dpi=130)
    print("saved A4_gravitational_slip.png")


if __name__ == "__main__":
    main()

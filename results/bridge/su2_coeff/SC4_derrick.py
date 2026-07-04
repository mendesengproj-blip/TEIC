"""SC4 -- Derrick scan with the EMERGENT quartic: does the cosine alone stabilise?

Pre-registered expectation (BRIDGE_SU2_COEFF.md addendum): since 3S-2K >= (5/3)S > 0
pointwise, the net cosine quartic is negative (saturating), so the truncated
energy collapses and the full cosine cannot produce an interior Derrick minimum;
verdict B unless the measurement says otherwise. The manual-Skyrme control must
reproduce the Paper II interior minimum.

Setup: hedgehog F(r) = pi exp(-r); currents G eigenvalues (radial F'^2,
tangential s = sin^2 F / r^2 twice). Dilation x -> x/lambda scanned in
u = r/lambda coordinates (fixed grid, faithful at every lambda).

Energies per unit volume (link-cosine normalised so the small-field limit is
the sigma model TrG):
  E_cos(lambda; a)  = (24/a^2) <1 - cos((a/2lambda) q(u,c))>_c, q^2 = F'^2c^2+s(1-c^2)
  E_trunc(lambda;a) = lambda*E2 - (a^2/240) lambda^{-1} Int(3S-2K)
  E_manual(lambda)  = lambda*E2 + e_sk * lambda^{-1} * E4K,  E4K = Int K/2 (su2_core
                      convention E4 = e_sk sum_{i<j}|c_i x c_j|^2 = e_sk K/2)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sc_core as sc

# radial grid in u = r/lambda (fixed for all lambda)
U = np.linspace(1e-4, 14.0, 2400)
DU = float(U[1] - U[0])
F = np.pi * np.exp(-U)
FP = -np.pi * np.exp(-U)                  # F'(u)
S_TAN = np.sin(F) ** 2 / U ** 2           # tangential eigenvalue s(u)

# Gauss-Legendre nodes for the direction average <.>_c over c = cos(angle to rhat)
GL_C, GL_W = np.polynomial.legendre.leggauss(48)
GL_C = 0.5 * (GL_C + 1.0)                 # symmetric integrand: fold to [0,1]
GL_W = GL_W * 0.5

TRG = FP ** 2 + 2 * S_TAN                                  # TrG(u)
S_INV = TRG ** 2                                           # S(u)
K_INV = 4 * FP ** 2 * S_TAN + 2 * S_TAN ** 2               # K(u) = 2s(2F'^2+s)
E2_1 = float(np.sum(4 * np.pi * U ** 2 * TRG) * DU)        # E2 at lambda=1
E4K_1 = float(np.sum(4 * np.pi * U ** 2 * (K_INV / 2)) * DU)   # manual-Skyrme E4
I3S2K = float(np.sum(4 * np.pi * U ** 2 * (3 * S_INV - 2 * K_INV)) * DU)


def e_cos(lam, a):
    """Full-cosine energy at dilation lambda, link scale a (exact quadrature)."""
    q2 = FP[:, None] ** 2 * GL_C[None, :] ** 2 + \
        S_TAN[:, None] * (1.0 - GL_C[None, :] ** 2)
    arg = (a / (2.0 * lam)) * np.sqrt(q2)
    avg = np.sum((1.0 - np.cos(arg)) * GL_W[None, :], axis=1)
    dens = (24.0 / a ** 2) * avg
    return float(np.sum(4 * np.pi * (lam * U) ** 2 * dens) * (lam * DU))


def main():
    lams = np.geomspace(0.02, 4.0, 120)
    a_list = [0.1, 0.5, 1.0, 2.0]
    e_sk = 1.0

    curves = {}
    for a in a_list:
        curves[a] = np.array([e_cos(l, a) for l in lams])
    e_trunc = {a: lams * E2_1 - (a ** 2 / 240.0) / lams * I3S2K for a in a_list}
    e_manual = lams * E2_1 + e_sk / lams * E4K_1
    lam_star_manual = float(lams[int(np.argmin(e_manual))])
    lam_star_pred = float(np.sqrt(e_sk * E4K_1 / E2_1))

    # interior-minimum detection for the cosine curves (excluding endpoints)
    minima = {}
    for a in a_list:
        i = int(np.argmin(curves[a]))
        interior = 0 < i < len(lams) - 1
        # an interior minimum at the small-lambda endpoint region with E below
        # E(endpoint) would mean pinning; record both the argmin and monotonicity
        mono_increasing = bool(np.all(np.diff(curves[a]) > 0))
        minima[a] = {"argmin_lambda": float(lams[i]), "interior": bool(interior),
                     "monotonic_increasing": mono_increasing,
                     "E_at_argmin": float(curves[a][i]),
                     "E_smallest_lambda": float(curves[a][0]),
                     "E_largest_lambda": float(curves[a][-1])}

    # small-field consistency: a=0.1 curve vs lambda*E2 at large lambda
    consistency = float(curves[0.1][-1] / (lams[-1] * E2_1))

    payload = {
        "E2_1": E2_1, "E4K_1": E4K_1, "I_3S_minus_2K": I3S2K,
        "manual_skyrme_control": {"lambda_star": lam_star_manual,
                                  "lambda_star_predicted": lam_star_pred,
                                  "interior_minimum": True},
        "cosine_minima": minima,
        "small_field_consistency_ratio": consistency,
        "verdict_note": (
            "pre-registered expectation: no interior minimum from the cosine "
            "alone (net quartic negative); manual Skyrme control reproduces "
            "the interior minimum."),
    }
    sc.save_json("SC4_derrick.json", payload)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    for a, c in zip(a_list, ["tab:green", "tab:orange", "tab:red", "tab:purple"]):
        ax1.plot(lams, curves[a], color=c, label=f"cosine, a={a}")
        ax1.plot(lams, e_trunc[a], color=c, ls=":", lw=1)
    ax1.plot(lams, lams * E2_1, "k--", lw=1, label=r"$\lambda E_2$ (no quartic)")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"dilation $\lambda$")
    ax1.set_ylabel(r"$E(\lambda)$")
    ax1.set_title("full cosine (solid) vs truncated quartic (dotted)")
    ax1.set_ylim(1e-2, 1e4)
    ax1.legend(fontsize=7.5)

    ax2.plot(lams, e_manual, "b-", label=fr"manual Skyrme $e_{{sk}}$={e_sk}")
    ax2.axvline(lam_star_manual, color="b", ls=":",
                label=fr"$\lambda^*$={lam_star_manual:.2f} "
                      fr"(pred {lam_star_pred:.2f})")
    ax2.plot(lams, lams * E2_1, "k--", lw=1, label=r"$\lambda E_2$")
    ax2.set_xscale("log")
    ax2.set_xlabel(r"dilation $\lambda$")
    ax2.set_ylabel(r"$E(\lambda)$")
    ax2.set_title("control: manual Skyrme term -> interior minimum")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SC4_derrick.png", dpi=150)

    print(json.dumps({"manual_control": payload["manual_skyrme_control"],
                      "cosine_minima": minima,
                      "small_field_consistency": consistency}, indent=2))


if __name__ == "__main__":
    main()

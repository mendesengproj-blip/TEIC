"""make_figures -- everpresent-Lambda dynamics."""

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ld_core import lambda_rms_unnorm, rho_crit
from LD2_coincidence import (
    omega_lambda_lcdm,
    omega_lambda_everpresent,
    w_eff_envelope,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # left: coincidence -- Omega_Lambda(z)
    z = np.logspace(-2, 3, 300)
    ax1.semilogx(1 + z, [omega_lambda_lcdm(zz) for zz in z],
                 label=r"$\Lambda$CDM ($\Lambda$=const)", color="crimson")
    ax1.semilogx(1 + z, [omega_lambda_everpresent(zz) for zz in z],
                 label="everpresent (tracking, p=1.11)", color="navy")
    ax1.axhspan(0.1, 0.9, color="0.9", label=r"$\Omega_\Lambda\sim O(1)$")
    ax1.set_xlabel("1+z")
    ax1.set_ylabel(r"$\Omega_\Lambda(z)$")
    ax1.set_title("Coincidence problem: everpresent stays O(1)")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3, which="both")

    # right: tracking + effective w
    zt = np.linspace(0.01, 8, 200)
    rc = np.array([rho_crit(zz) for zz in zt])
    lr = np.array([lambda_rms_unnorm(zz) for zz in zt])
    ax2.loglog(rc, lr, color="navy",
               label=r"$\Lambda_{rms}\propto\rho_{crit}^{1.11}$")
    ax2.loglog(rc, rc * lr[0] / rc[0],
               "k--", lw=0.8, label="perfect tracking (p=1)")
    ax2.set_xlabel(r"$\rho_{crit}\propto E(z)^2$")
    ax2.set_ylabel(r"$\Lambda_{rms}\sim 1/\sqrt{V_4^{past}}$")
    ax2.set_title("Tracking of the critical density")
    ax2.legend(fontsize=8, loc="upper left")
    ax2.grid(alpha=0.3, which="both")

    # inset: w_eff(z)
    axin = ax2.inset_axes([0.58, 0.12, 0.38, 0.36])
    zw = np.linspace(0.01, 5, 120)
    axin.plot(zw, [w_eff_envelope(zz) for zz in zw], color="darkgreen")
    axin.axhline(-1, color="crimson", ls=":", lw=0.8)
    axin.set_title(r"$w_{eff}$ (envelope)", fontsize=7)
    axin.tick_params(labelsize=6)
    axin.set_xlabel("z", fontsize=6)

    fig.suptitle("Everpresent-Lambda dynamics: no divergence at z~0, tracks "
                 "rho_crit, dissolves coincidence (apparent w drifts)", fontsize=10)
    fig.tight_layout()
    out = os.path.join(HERE, "LD_dynamics.png")
    fig.savefig(out, dpi=130)
    print("wrote", out)


if __name__ == "__main__":
    main()

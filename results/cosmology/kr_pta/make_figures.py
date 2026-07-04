"""make_figures -- KR-PTA confrontation plot.

Two panels:
  (left)  KR characteristic strain h_c(m) of the m_A line at fractions f=1, 0.1,
          0.01, vs frequency, with the PTA band shaded.
  (right) max allowed ULDM fraction f_max(m) from the PPTA-2018 gravitational
          direct search across the m_A overlap window, with f=1 line.
"""

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from kr_pta_core import (
    f_signal,
    h_c,
    ppta_fraction_limit,
    RHO_LOCAL,
    M_A_PTA_LO,
    M_A_PTA_HI,
    PTA_F_LO,
    PTA_F_HI,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    masses = np.geomspace(M_A_PTA_LO, M_A_PTA_HI, 200)
    freqs = f_signal(masses)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # left: strain vs frequency
    for frac, ls in [(1.0, "-"), (0.1, "--"), (0.01, ":")]:
        ax1.loglog(freqs, h_c(masses, frac * RHO_LOCAL),
                   ls, label=f"m_A line, f={frac:g}")
    ax1.axvspan(PTA_F_LO, PTA_F_HI, color="0.85", label="PTA band")
    ax1.axhline(2e-15, color="crimson", lw=1, ls="-.",
                label="NANOGrav15 GWB ~2e-15 @1/yr")
    ax1.set_xlabel("KR line frequency f [Hz]")
    ax1.set_ylabel(r"characteristic strain $h_c$")
    ax1.set_title("KR line strain of the m_A field")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3, which="both")

    # right: PPTA fraction limit
    fmax = ppta_fraction_limit(masses)
    ax2.loglog(masses, fmax, color="navy", label="PPTA-2018 $f_{max}$ (grav.)")
    ax2.axhline(1.0, color="crimson", ls="--", label="100% local DM (f=1)")
    ax2.fill_between(masses, fmax, 1e4, where=(fmax < 1.0),
                     color="crimson", alpha=0.2, label="excluded (f>$f_{max}$)")
    ax2.set_xlabel(r"$m_A$ [eV]")
    ax2.set_ylabel(r"max allowed ULDM fraction $f_{max}$")
    ax2.set_title("Published direct-search limit vs window")
    ax2.set_ylim(0.5, 3e3)
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3, which="both")

    fig.suptitle("KR-PTA: the m_A line is below current PTA direct-search reach "
                 "across the overlap window", fontsize=10)
    fig.tight_layout()
    out = os.path.join(HERE, "KR_pta.png")
    fig.savefig(out, dpi=130)
    print("wrote", out)


if __name__ == "__main__":
    main()

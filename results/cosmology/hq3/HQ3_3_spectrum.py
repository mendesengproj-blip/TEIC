"""HQ3_3_spectrum.py -- spectral SHAPE of the m_A signal vs the NANOGrav power law.

Charter HQ3-3.  NANOGrav reports a broadband, Hellings-Downs-correlated power law with
timing-residual PSD index gamma = 13/3 (~4.33), i.e. h_c(f) ~ f^{-2/3}.  The m_A
condensate instead produces a MONOCHROMATIC line at f_GW, broadened only by the DM
velocity dispersion to a fractional width Delta f/f ~ (v/c)^2 ~ 1e-6.  This script
contrasts the two shapes quantitatively (a line is gamma -> infinity, the opposite of
a slowly-falling power law) and renders the figure.  The vector character (3
polarizations) adds an O(1) anisotropic-stress modulation but does NOT broaden the
line into a continuum -- the headline is still a line, not a SMBH-like power law.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import hq3_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent
V_DISP = 1.0e-3            # DM virial velocity v/c ~ 1e-3 -> line width (v/c)^2 ~ 1e-6
M_LINE = 1e-23            # representative in-band mass for the line illustration (eV)


def main():
    f_line = float(c.f_gw(M_LINE))
    frac_width = V_DISP ** 2                 # Delta f / f for the condensate line
    df = f_line * frac_width

    # NANOGrav power-law strain index vs the m_A "index"
    alpha_ng = (3.0 - c.NG_GAMMA) / 2.0      # h_c ~ f^alpha = f^{-2/3}
    payload = {
        "nanograv": {"gamma": c.NG_GAMMA, "h_c_index_alpha": alpha_ng,
                     "shape": "broadband power law (SMBH binaries)"},
        "m_A": {"shape": "monochromatic line", "f_GW_Hz_at_1e-23eV": f_line,
                "fractional_width_dff": frac_width, "abs_width_Hz": df,
                "effective_gamma": "infinity (line, not a continuum)"},
        "comparison": {
            "compatible_as_broadband_SGWB": False,
            "reason": "a velocity-broadened line (df/f~1e-6) cannot mimic a "
                      "gamma=13/3 power law spanning a decade in frequency",
        },
        "note": "m_A is a LINE; NANOGrav 2023 detected a CONTINUUM. Different observables.",
    }
    (OUT / "HQ3_3_spectrum.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("HQ3-3  spectral shape: m_A line vs NANOGrav power law (gamma=13/3)")
    print("=" * 74)
    print(f"  NANOGrav: broadband power law, gamma = {c.NG_GAMMA:.3f}, "
          f"h_c ~ f^{alpha_ng:+.3f}")
    print(f"  m_A     : monochromatic line at f_GW = {f_line:.3e} Hz (m=1e-23 eV)")
    print(f"            velocity broadening Delta f/f ~ (v/c)^2 = {frac_width:.1e} "
          f"-> Delta f = {df:.2e} Hz")
    print("  => incompatible as a broadband SGWB: a line is not a power law.")
    print(f"  saved {OUT/'HQ3_3_spectrum.json'}")

    make_figure(f_line, df, alpha_ng)
    return payload


def make_figure(f_line, df, alpha_ng):
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    ff = np.logspace(np.log10(c.NG_BAND_HZ[0]), np.log10(c.NG_BAND_HZ[1]), 400)

    # NANOGrav broadband power-law strain
    ax.loglog(ff, c.nanograv_hc(ff), color="navy", lw=2.2,
              label=rf"NANOGrav broadband: $h_c\propto f^{{{alpha_ng:.2f}}}$ ($\gamma$=13/3)")

    # m_A line: a sharp, narrow Lorentzian-ish spike at f_line (height = KR Psi_c)
    psi = float(c.kr_psi_amplitude(M_LINE))
    fl = np.linspace(f_line - 6 * df, f_line + 6 * df, 600)
    lor = psi / (1.0 + ((fl - f_line) / (df / 2)) ** 2)
    ax.plot(fl, lor, color="crimson", lw=2.2,
            label=rf"m_A line at $f_{{GW}}$={f_line:.1e} Hz ($\Psi_c$={psi:.1e})")
    ax.axvline(f_line, color="crimson", ls=":", lw=1)

    ax.axvspan(*c.NG_BAND_HZ, color="green", alpha=0.07)
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("characteristic strain")
    ax.set_xlim(*c.NG_BAND_HZ)
    ax.set_ylim(1e-17, 1e-13)
    ax.set_title("HQ3-3: m_A is a LINE; NANOGrav detected a CONTINUUM ($\\gamma$=13/3)")
    ax.legend(fontsize=8.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "HQ3_3_spectrum.png", dpi=130)
    print(f"  saved {OUT/'HQ3_3_spectrum.png'}")


if __name__ == "__main__":
    main()

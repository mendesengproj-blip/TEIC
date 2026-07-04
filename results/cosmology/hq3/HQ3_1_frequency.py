"""HQ3_1_frequency.py -- central frequency of the m_A signal vs the NANOGrav band.

Charter HQ3-1 (analytic, runs first).  For each m_A in the Paper II window computes
f_DM = m_A c^2/h (field) and f_GW = 2 m_A c^2/h (what a PTA sees), and asks which
masses land inside the NANOGrav band [2e-9, 1e-7] Hz.  Writes the table + the band-
producing mass range + the overlap with the Paper II window, plus a figure.

Nothing fit to NANOGrav: m_A from Paper II (galaxies + GW170817); the band is
COMPARISON ONLY.
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
MASSES = [c.M_A_FLOOR, 1e-24, 5e-24, 1e-23, 1e-22, c.M_A_CEIL]   # eV


def main():
    rows = []
    for m in MASSES:
        fdm = float(c.f_field(m))
        fgw = float(c.f_gw(m))
        in_band = bool(c.NG_BAND_HZ[0] <= fgw <= c.NG_BAND_HZ[1])
        rows.append({"m_eV": m, "f_DM_Hz": fdm, "f_GW_Hz": fgw, "in_band": in_band})

    lo_b, hi_b = c.band_mass_window()
    overlap = c.overlap_with_paper_II()

    payload = {
        "rows": rows,
        "nanograv_band_Hz": list(c.NG_BAND_HZ),
        "band_producing_mass_eV": [float(lo_b), float(hi_b)],
        "paper_II_window_eV": [c.M_A_FLOOR, c.M_A_CEIL],
        "overlap_eV": [float(overlap[0]), float(overlap[1])] if overlap else None,
        "any_mass_in_band": any(r["in_band"] for r in rows),
        "note": "f_GW = 2 m_A c^2/h = m_A c^2/(pi hbar); f=mu/pi of arXiv:2412.12975",
    }
    (OUT / "HQ3_1_frequency.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("HQ3-1  oscillation frequency of m_A vs NANOGrav band [2e-9, 1e-7] Hz")
    print("=" * 74)
    print(f"  {'m_A [eV]':>12} {'f_DM [Hz]':>13} {'f_GW [Hz]':>13}   in band?")
    for r in rows:
        print(f"  {r['m_eV']:>12.2e} {r['f_DM_Hz']:>13.3e} {r['f_GW_Hz']:>13.3e}"
              f"   {'YES' if r['in_band'] else 'no'}")
    print(f"\n  band-producing masses (f_GW in band): {lo_b:.3e} - {hi_b:.3e} eV")
    print(f"  Paper II window:                      {c.M_A_FLOOR:.2e} - {c.M_A_CEIL:.2e} eV")
    if overlap:
        print(f"  OVERLAP (Paper II AND in band):       {overlap[0]:.3e} - {overlap[1]:.3e} eV")
    print(f"  saved {OUT/'HQ3_1_frequency.json'}")

    make_figure(rows, overlap)
    return payload


def make_figure(rows, overlap):
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    mm = np.logspace(np.log10(c.M_A_FLOOR), np.log10(c.M_A_CEIL), 300)
    ax.loglog(mm, c.f_gw(mm), color="crimson", lw=2.2, label=r"$f_{\rm GW}=2m_Ac^2/h$ (PTA sees)")
    ax.loglog(mm, c.f_field(mm), color="navy", lw=1.4, ls="--", label=r"$f_{\rm DM}=m_Ac^2/h$ (field)")

    # NANOGrav band as a horizontal stripe
    ax.axhspan(*c.NG_BAND_HZ, color="green", alpha=0.13, label="NANOGrav band [2e-9, 1e-7] Hz")
    ax.axhline(c.F_YR, color="green", ls=":", lw=1, label="1/yr reference")

    # overlap mass range as a vertical stripe
    if overlap:
        ax.axvspan(overlap[0], overlap[1], color="orange", alpha=0.12,
                   label=f"overlap {overlap[0]:.1e}-{overlap[1]:.1e} eV")
    ax.axvline(c.M_A_FLOOR, color="grey", ls=":", lw=0.8)
    ax.axvline(c.M_A_CEIL, color="grey", ls=":", lw=0.8)

    # mark the sampled masses
    for r in rows:
        ax.plot(r["m_eV"], r["f_GW_Hz"], "o",
                color="crimson" if r["in_band"] else "lightgrey",
                markeredgecolor="k", ms=7, zorder=5)

    ax.set_xlabel(r"$m_A$ [eV]"); ax.set_ylabel("frequency [Hz]")
    ax.set_title("HQ3-1: m_A oscillation frequency vs NANOGrav PTA band")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_ylim(1e-11, 1e-6)
    fig.tight_layout()
    fig.savefig(OUT / "HQ3_1_frequency.png", dpi=130)
    print(f"  saved {OUT/'HQ3_1_frequency.png'}")


if __name__ == "__main__":
    main()

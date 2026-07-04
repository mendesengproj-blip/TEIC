"""A1_longitudinal_mode.py -- does the DEV vector field A_mu emerge as the MASSIVE
LONGITUDINAL mode of the TEIC orientation ferromagnet?

Campaign DEV_FROM_TEIC, angle A1.  Charter: results/dev_from_teic/DEV_FROM_TEIC.md.

Background already MEASURED (do not repeat -- build on it):
  * E1 / fm2_core: the O(3) orientation ferromagnet is the ordered vacuum (J_c~0.69
    in this beta=1 convention; J=1.0 ordered).
  * E2: the TRANSVERSE excitations are the 2 Goldstone magnons, omega=ck (massless).
  * C1 / FM2-1: the LONGITUDINAL susceptibility chi_par = S_par(k=0) shows the
    Brezin-Wallace coexistence anomaly chi_par ~ h^{-0.37..-0.5} as h->0.

The DEV has a Proca vector A_mu with an explicit mass m_A (cold dark matter FM4,
MOND screening below lambda_A, quantised vortices C6).  The hypothesis A1 tests:
  A_mu = the MASSIVE LONGITUDINAL mode of the ferromagnet (delta|<n>|, the amplitude
  mode), distinct from the massless transverse Goldstones.

What we measure (the honest, equilibrium-MC observable):  the engine is a Metropolis
ferromagnet with no real-time dynamics, so we measure the STATIC mass gap = the inverse
correlation length read from the equal-time structure factor (Ornstein-Zernike):
    S(k) = A / (k^2 + m^2)     =>   1/S(k) = (1/A) k^2 + m^2/A
For a relativistic mode omega^2 = c^2 k^2 + m^2 the static gap m IS the rest mass
omega(k->0).  We measure it separately in the LONGITUDINAL channel (n projected on the
order direction) and the TRANSVERSE channel (the 2 Goldstone components).

  m_long^2  = the candidate A_mu mass     (longitudinal / amplitude mode)
  m_trans^2 = the Goldstone gap            (must -> 0 as h -> 0: GATE G0)

Pre-registered reading:
  G0        m_trans^2 -> 0 as h->0 (transverse = Goldstone, reproduces E2/C1).
  A1-GAP    if m_long^2 -> const > 0 as h->0  => A_mu IS the massive longitudinal mode
            -> [IDENTIFICADO]/[DERIVADO].
            if m_long^2 -> 0 as h->0 (Goldstone-dressed, Brezin-Wallace)  => the
            amplitude mode is gapless in d=3, A_mu needs an EXTERNAL mass scale
            -> [EXTERNO-B] with a precise structural reason.

Anti-circularity: NO DEV/Proca number enters the generator; m_A is COMPARISON ONLY
(not used here -- A1 only asks whether a gap exists at all).  Engine = fm2_core (E1).
Fixed seeds; auto-descriptive JSON.
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
J_ORDERED = 1.0
HS = np.array([0.3, 0.1, 0.03, 0.01])     # pinning field (small h -> Goldstone limit)
SEEDS = list(range(12))
N_BURN, N_MEAS = 400, 120
MEAS_EVERY = 2
N_KSHELL_FIT = 4                          # number of smallest-|k| shells used in the OZ fit


def _kgrid(L):
    """Lattice momenta and |k| for an L^3 box (units: k = 2*pi*n/L)."""
    k1 = 2.0 * np.pi * np.fft.fftfreq(L)             # in [-pi, pi)
    KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
    kmag = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)
    return kmag


def structure_factors(L, J, h, seed, n_burn, n_meas, meas_every):
    """Accumulate the equal-time structure factors of the LONGITUDINAL (n.Mhat) and
    TRANSVERSE (n - (n.Mhat)Mhat) spin components over equilibrium configs.  The
    longitudinal/transverse split is defined per-snapshot by the instantaneous
    magnetization direction Mhat (rotation-robust)."""
    lat = fm2.O3Lattice(L, J, h, seed=seed)
    lat.equilibrate(n_burn)
    V = L ** 3
    SL = np.zeros((L, L, L))
    ST = np.zeros((L, L, L))
    taken = 0
    s = 0
    while taken < n_meas:
        lat.sweep()
        s += 1
        if s % meas_every == 0:
            n = lat.n                                  # (L,L,L,3)
            Mvec = n.reshape(-1, 3).mean(axis=0)
            Mhat = Mvec / (np.linalg.norm(Mvec) + 1e-12)
            long_field = n @ Mhat                      # (L,L,L) longitudinal projection
            trans_field = n - long_field[..., None] * Mhat  # (L,L,L,3) transverse vector
            FL = np.fft.fftn(long_field)
            SL += (FL.real ** 2 + FL.imag ** 2) / V
            for c in range(3):
                FT = np.fft.fftn(trans_field[..., c])
                ST += (FT.real ** 2 + FT.imag ** 2) / V
            taken += 1
    SL /= taken
    ST /= (2.0 * taken)            # 2 physical transverse components
    return SL, ST


def radial_bin(field, kmag, nbin_small):
    """Radially average a k-space field over |k| shells; return the smallest nbin_small
    nonzero shells as (k2, value) for the OZ fit, plus the full binned curve."""
    flat_k = kmag.ravel()
    flat_v = field.ravel()
    order = np.argsort(flat_k)
    flat_k = flat_k[order]
    flat_v = flat_v[order]
    # group by (almost) identical |k| (lattice shells are discrete)
    ks, vs = [], []
    i = 0
    n = len(flat_k)
    while i < n:
        j = i
        while j < n and flat_k[j] - flat_k[i] < 1e-6:
            j += 1
        ks.append(flat_k[i])
        vs.append(np.mean(flat_v[i:j]))
        i = j
    ks = np.array(ks)
    vs = np.array(vs)
    nz = ks > 1e-9                                     # drop k=0 (the order parameter)
    ks, vs = ks[nz], vs[nz]
    return ks, vs


def oz_gap(ks, S, nfit):
    """Ornstein-Zernike fit 1/S = alpha k^2 + beta over the smallest nfit shells;
    m^2 = beta/alpha, A = 1/alpha.  Returns (m2, A, alpha, beta)."""
    k2 = ks[:nfit] ** 2
    invS = 1.0 / S[:nfit]
    alpha, beta = np.polyfit(k2, invS, 1)
    m2 = beta / alpha if alpha > 0 else float("nan")
    return float(m2), float(1.0 / alpha if alpha > 0 else np.nan), float(alpha), float(beta)


def main():
    t0 = time.time()
    print("=" * 76)
    print("A1 -- does A_mu emerge as the MASSIVE LONGITUDINAL mode of the ferromagnet?")
    print("=" * 76)
    kmag = _kgrid(L)

    rows = {}
    for h in HS:
        SLs, STs = [], []
        for sd in SEEDS:
            SL, ST = structure_factors(L, J_ORDERED, h, sd, N_BURN, N_MEAS, MEAS_EVERY)
            SLs.append(SL)
            STs.append(ST)
        SL = np.mean(SLs, axis=0)
        ST = np.mean(STs, axis=0)
        ksL, vL = radial_bin(SL, kmag, N_KSHELL_FIT)
        ksT, vT = radial_bin(ST, kmag, N_KSHELL_FIT)
        m2L, AL, _, _ = oz_gap(ksL, vL, N_KSHELL_FIT)
        m2T, AT, _, _ = oz_gap(ksT, vT, N_KSHELL_FIT)
        rows[h] = {"m2_long": m2L, "m2_trans": m2T, "A_long": AL, "A_trans": AT,
                   "S_long_k0_shell": float(vL[0]), "S_trans_k0_shell": float(vT[0]),
                   "ks": ksL[:6].tolist(),
                   "S_long": vL[:6].tolist(), "S_trans": vT[:6].tolist()}
        print(f"  h={h:5.3f}  m2_long={m2L:+.4f} (gap_L={np.sqrt(max(m2L,0)):.3f})   "
              f"m2_trans={m2T:+.4f} (gap_T={np.sqrt(max(m2T,0)):.3f})   "
              f"ratio m2L/m2T={m2L/m2T if m2T>1e-9 else np.inf:6.2f}")

    # ---- extrapolate the gaps to h -> 0 : fit m^2 ~ c*h^p (log-log) ----
    hs = np.array(HS)
    m2L = np.array([rows[h]["m2_long"] for h in HS])
    m2T = np.array([rows[h]["m2_trans"] for h in HS])

    def loglog_slope(x, y):
        good = (y > 0) & np.isfinite(y)
        if good.sum() < 2:
            return float("nan"), float("nan")
        p, b = np.polyfit(np.log(x[good]), np.log(y[good]), 1)
        return float(p), float(np.exp(b))

    pL, cL = loglog_slope(hs, m2L)         # m2_long ~ cL h^pL
    pT, cT = loglog_slope(hs, m2T)         # m2_trans ~ cT h^pT

    # extrapolated gap at h->0: if pL > ~0.1 the longitudinal gap CLOSES (no spontaneous
    # mass); if pL ~ 0 it survives (genuine amplitude gap).
    long_gap_closes = bool(np.isfinite(pL) and pL > 0.15)
    trans_gapless = bool((not np.isfinite(pT)) or pT > 0.5 or m2T[-1] < 0.25 * m2L[-1])

    g0_pass = trans_gapless
    if long_gap_closes:
        status = "EXTERNO-B"
        verdict = (
            "A_mu does NOT emerge as a spontaneous massive mode. The longitudinal "
            "(amplitude) gap CLOSES as h->0: m_long^2 ~ h^%.2f (Goldstone-dressed, "
            "Brezin-Wallace coexistence anomaly in d=3 -- the SAME non-analyticity C1/"
            "FM2-1 measured as deep-MOND). The would-be A_mu mass is field-INDUCED "
            "(m_long ~ h^%.2f), not intrinsic; the bare O(3) ferromagnet has no Proca "
            "gap. A_mu needs an external mass scale -> [EXTERNO-B], with a precise "
            "structural reason." % (pL, pL / 2.0))
    elif np.isfinite(pL) and abs(pL) <= 0.15:
        status = "IDENTIFICADO"
        verdict = (
            "The longitudinal mode has a mass gap that SURVIVES h->0 (m_long^2 ~ h^%.2f, "
            "~flat; gap_L=%.3f at smallest h) while the transverse mode is gapless "
            "(Goldstone). A_mu is identifiable as the massive longitudinal/amplitude mode "
            "of the TEIC ferromagnet -> [IDENTIFICADO]. (Scale lattice->physical stays "
            "external.)" % (pL, np.sqrt(max(m2L[-1], 0))))
    else:
        status = "INCONCLUSIVO"
        verdict = ("Longitudinal gap trend ambiguous (m_long^2 ~ h^%.2f); cannot cleanly "
                   "separate a survived gap from a closing one. [INCONCLUSIVO]." % pL)

    print("-" * 76)
    print(f"  G0 (transverse Goldstone, m_trans^2->0): pass={g0_pass}  "
          f"(m2_trans ~ h^{pT:.2f})")
    print(f"  longitudinal gap: m2_long ~ h^{pL:.2f}  -> "
          f"{'CLOSES (no spontaneous mass)' if long_gap_closes else 'survives' if status=='IDENTIFICADO' else 'ambiguous'}")
    print(f"  STATUS A_mu: [{status}]")
    print(f"  VERDICT: {verdict}")
    print("=" * 76)

    _figure(HS, rows, m2L, m2T, pL, pT, status)

    payload = {
        "angle": "A1 -- A_mu as the massive longitudinal mode of the TEIC ferromagnet",
        "engine": "fm2_core O(3) ferromagnet (E1)", "L": L, "J": J_ORDERED,
        "hs": HS.tolist(), "seeds": len(SEEDS), "n_burn": N_BURN, "n_meas": N_MEAS,
        "n_kshell_fit": N_KSHELL_FIT,
        "per_h": {str(h): rows[h] for h in HS},
        "m2_long": m2L.tolist(), "m2_trans": m2T.tolist(),
        "exponent_long_m2_vs_h": pL, "exponent_trans_m2_vs_h": pT,
        "G0_transverse_goldstone": bool(g0_pass),
        "long_gap_closes_as_h0": long_gap_closes,
        "status_A_mu": status, "verdict": verdict,
        "method": ("static Ornstein-Zernike gap m^2 from 1/S(k)=k^2/A+m^2/A on the "
                   "smallest k shells; longitudinal=n.Mhat, transverse=2 perp comps; "
                   "equilibrium Metropolis (no real-time omega) so m is the static "
                   "mass gap = inverse correlation length = omega(k->0)."),
        "anti_circularity": "no DEV/Proca number in generator; m_A COMPARISON ONLY (unused here)",
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "A1_longitudinal_mode.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved A1_longitudinal_mode.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(HS, rows, m2L, m2T, pL, pT, status):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    hs = np.array(HS)
    ax[0].loglog(hs, np.clip(m2L, 1e-4, None), "o-", lw=1.6, label=r"$m_\parallel^2$ (longitudinal / $A_\mu$ candidate)")
    ax[0].loglog(hs, np.clip(m2T, 1e-4, None), "s-", lw=1.6, label=r"$m_\perp^2$ (transverse Goldstone)")
    hh = np.logspace(np.log10(hs.min()), np.log10(hs.max()), 40)
    if np.isfinite(pL):
        ax[0].loglog(hh, (m2L[0] / hs[0] ** pL) * hh ** pL, "k--", lw=1,
                     label=r"$m_\parallel^2\propto h^{%.2f}$" % pL)
    ax[0].set_xlabel("pinning field h  (~ gravitational gradient g)")
    ax[0].set_ylabel(r"static mass gap $m^2$ (lattice units)")
    ax[0].set_title(f"longitudinal vs transverse gap  [{status}]")
    ax[0].legend(fontsize=8)
    # right: example OZ fit at the smallest h
    h0 = HS[-1]
    ks = np.array(rows[h0]["ks"]); SL = np.array(rows[h0]["S_long"]); ST = np.array(rows[h0]["S_trans"])
    ax[1].plot(ks ** 2, 1.0 / SL, "o", label=r"$1/S_\parallel(k)$")
    ax[1].plot(ks ** 2, 1.0 / ST, "s", label=r"$1/S_\perp(k)$")
    ax[1].set_xlabel(r"$k^2$"); ax[1].set_ylabel(r"$1/S(k)$")
    ax[1].set_title(f"Ornstein-Zernike fit at h={h0}\n(intercept/slope = $m^2$)")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.2)
    fig.suptitle("A1: is the DEV vector A_mu the massive longitudinal mode of the TEIC ferromagnet?",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "A1_longitudinal_mode.png", dpi=130)
    print("saved A1_longitudinal_mode.png")


if __name__ == "__main__":
    main()

"""FM2_1_second_transition.py -- the MOND interpolation as a Goldstone response, and
the search for a SECOND transition (charter FM2-1).

We couple the O(3) orientation ferromagnet (the E1 vacuum) to an external field h
that represents the gravitational gradient g of the DEV, and measure the
longitudinal susceptibility chi_par(h) = the microscopic response that maps to the
MOND interpolation nu(g/a0).

Two questions, both pre-registered:

  (1) DOES THE FERROMAGNET REPRODUCE DEEP-MOND?  In the ordered phase of a 3D O(3)
      magnet the Goldstone (spin-wave) fluctuations make chi_par DIVERGE as
      h^{-1/2} as h->0 (Brezin-Wallace coexistence anomaly).  That exponent IS the
      deep-MOND law nu = 1/sqrt(g/a0) (a = sqrt(g_N a0)).  Measuring p in
      chi_par ~ h^{-p} and finding p ~ 1/2 would give a MICROSCOPIC ORIGIN of the
      MOND interpolation from the orientation ferromagnet (a positive result).

  (2) IS THERE A SECOND TRANSITION (the runaway cure)?  The divergence saturates at
      some h_c.  Charter death C1: if h_c is only a FINITE-SIZE cutoff (h_c -> 0 as
      L -> inf, i.e. h_c ~ 1/L^2), the divergence is SUSTAINED in the thermodynamic
      limit -> no physical second transition from the bare ferromagnet -> the FM1
      runaway persists.  A PHYSICAL second transition requires h_c to be
      L-INDEPENDENT (a real correlation-length scale, e.g. the Paper II vector mass).

Maps: h0 (where chi_par leaves the flat/Newtonian plateau) <-> g=a0 (y=1); then
a_c2/a0 = h_c/h0, tested against the observational gap (0.005, 0.016).

Anti-circularity: a0 from SPARC (mapped to h0); a_c2 measured; no sigma8 inserted.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fm2_core as fm2  # noqa: E402

OUT = Path(__file__).resolve().parent
SEEDS = list(range(20))
N_BURN, N_MEAS = 400, 160
HS = np.array([1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001])
J_ORDERED = 1.0
J_DISORDERED = 0.55
GAP = (0.005, 0.016)        # observational gap a_c2/a0 (COMPARISON)


def chi_par(L, J, h, seeds, n_burn=N_BURN, n_meas=N_MEAS):
    """Longitudinal susceptibility chi_par = V Var(m_par) (beta=1), seed-averaged.
    Returns (mean, sem, mean m_par)."""
    vals, mps = [], []
    for sd in seeds:
        s = fm2.sample_observables(L, J, h, seed=sd, n_burn=n_burn, n_meas=n_meas)
        vals.append(L ** 3 * np.var(s["m_par"]))
        mps.append(s["m_par"].mean())
    vals = np.array(vals)
    return float(vals.mean()), float(vals.std() / np.sqrt(len(seeds))), float(np.mean(mps))


def chi_curve(L, J, seeds):
    chi, sem, mp = [], [], []
    for h in HS:
        c, e, m = chi_par(L, J, h, seeds)
        chi.append(c); sem.append(e); mp.append(m)
    return np.array(chi), np.array(sem), np.array(mp)


def fit_exponent(h, chi):
    """Fit chi ~ h^{-p} in the RISING regime (h above the saturation peak).  Returns
    p and the saturation scale h_c (the h at the chi maximum)."""
    jpk = int(np.argmax(chi))                       # peak / saturation
    h_c = float(h[jpk])
    rising = h >= h[jpk]
    if rising.sum() >= 3:
        p = -np.polyfit(np.log(h[rising]), np.log(chi[rising]), 1)[0]
    else:
        p = float("nan")
    return float(p), h_c, jpk


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM2-1 -- MOND from a Goldstone response + search for a second transition")
    print("=" * 72)

    # (1) deep-MOND exponent at J ordered, L=16
    print(f"[1] chi_par(h), J={J_ORDERED} (ordered), L=16, {len(SEEDS)} seeds ...")
    chi16, sem16, mp16 = chi_curve(16, J_ORDERED, SEEDS)
    p16, hc16, jpk16 = fit_exponent(HS, chi16)
    for h, c, e in zip(HS, chi16, sem16):
        print(f"    h={h:.3f}  chi_par={c:7.3f} +- {e:5.3f}")
    print(f"    rising-regime exponent p (chi~h^-p): {p16:.3f}  "
          f"(deep-MOND => p~0.5);  saturation h_c={hc16:.3f}")

    # (2) finite-size scaling of the saturation scale h_c
    print("[2] finite-size scan of h_c (physical if L-independent) ...")
    Lscan = [10, 16, 24]
    fs_seeds = SEEDS[:8]
    hc_of_L = {}
    curves_L = {}
    for L in Lscan:
        chiL, semL, mpL = chi_curve(L, J_ORDERED, fs_seeds)
        pL, hcL, _ = fit_exponent(HS, chiL)
        hc_of_L[L] = hcL
        curves_L[L] = (chiL.tolist(), semL.tolist())
        print(f"    L={L:2d}: p={pL:.3f}  h_c={hcL:.4f}")
    # test 1/L^2 (finite-size) vs constant (physical)
    Ls = np.array(Lscan, float); hcs = np.array([hc_of_L[L] for L in Lscan])
    # fit log h_c = a - q log L ; q~2 => finite-size, q~0 => physical
    q = -np.polyfit(np.log(Ls), np.log(hcs), 1)[0]
    finite_size = q > 1.0          # h_c shrinks with L => not physical
    print(f"    h_c ~ L^-q with q={q:.2f}  "
          f"({'FINITE-SIZE (q~2) => no physical transition' if finite_size else 'L-INDEPENDENT => physical'})")

    # (3) disordered control: no MOND enhancement
    print(f"[3] disordered control J={J_DISORDERED} (< J_c), L=16 ...")
    chiD, semD, mpD = chi_curve(16, J_DISORDERED, SEEDS[:8])
    pD, _, _ = fit_exponent(HS, chiD)
    flat_D = abs(pD) < 0.2
    print(f"    exponent p={pD:.3f}  ({'flat: no enhancement' if flat_D else 'rising'})")

    # ---- map to a_c2/a0 and verdict ----
    # h0 = field where chi leaves the flat plateau (the MOND knee, y=1).  Estimate as
    # the largest h whose chi is within 30% of the small-h plateau minimum.
    h0 = float(HS[np.argmin(chi16)])               # crude knee proxy (flat side)
    a_c2_over_a0 = hc16 / HS[0]                     # h_c in units of h(y=1)=HS max
    in_gap = GAP[0] <= a_c2_over_a0 <= GAP[1]

    if finite_size:
        verdict = "C1"
        why = ("the deep-MOND chi_par~h^{-p} divergence (p=%.2f, Goldstone origin) is "
               "cut off ONLY by finite size (h_c~L^-%.1f) -> sustained as L->inf -> no "
               "physical second transition from the bare ferromagnet -> the FM1 "
               "runaway persists.  A physical a_c2 needs an external correlation "
               "length (the Paper II vector mass m_A), not measured here." % (p16, q))
    elif in_gap:
        verdict = "A-candidate"
        why = ("L-independent second transition at a_c2/a0=%.3f, INSIDE the "
               "observational gap (0.005,0.016)." % a_c2_over_a0)
    else:
        verdict = "C4"
        why = ("L-independent second transition but a_c2/a0=%.3f is OUTSIDE the gap "
               "(0.005,0.016)." % a_c2_over_a0)

    print("-" * 72)
    print(f"  deep-MOND exponent p={p16:.3f} (microscopic origin of nu=1/sqrt(g/a0) "
          f"if p~0.5)")
    print(f"  second transition: {'finite-size (not physical)' if finite_size else 'physical'}; "
          f"a_c2/a0~{a_c2_over_a0:.3f}")
    print(f"  VERDICT FM2-1: {verdict} -- {why}")
    print("=" * 72)

    payload = {
        "verdict": verdict, "why": why,
        "deep_mond_exponent_p": p16, "p_ordered_L16": p16,
        "h_c_L16": hc16, "h_c_of_L": hc_of_L, "hc_L_exponent_q": q,
        "finite_size_cutoff": bool(finite_size),
        "a_c2_over_a0": a_c2_over_a0, "in_observational_gap": bool(in_gap),
        "gap": GAP,
        "hs": HS.tolist(),
        "chi_ordered_L16": chi16.tolist(), "sem_ordered_L16": sem16.tolist(),
        "m_par_ordered_L16": mp16.tolist(),
        "chi_disordered_L16": chiD.tolist(), "exponent_disordered": pD,
        "curves_L": curves_L,
        "config": {"J_ordered": J_ORDERED, "J_disordered": J_DISORDERED,
                   "L_scan": Lscan, "seeds": len(SEEDS), "n_burn": N_BURN,
                   "n_meas": N_MEAS},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "FM2_1_second_transition.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM2_1_second_transition.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(HS, chi16, sem16, curves_L, Lscan, chiD, p16)
    return payload


def make_figure(hs, chi16, sem16, curves_L, Lscan, chiD, p16):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    ax[0].errorbar(hs, chi16, yerr=sem16, marker="o", lw=1.5, label="J=1.0 ordered (L=16)")
    ax[0].errorbar(hs, chiD, marker="s", mfc="none", lw=1, label="J=0.55 disordered (L=16)")
    hh = np.logspace(np.log10(hs.min()), np.log10(hs.max()), 50)
    norm = chi16[np.argmax(chi16)] * np.sqrt(hs[np.argmax(chi16)])
    ax[0].plot(hh, norm / np.sqrt(hh), "k--", lw=1, label=r"$\propto h^{-1/2}$ (deep-MOND)")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel("external field h  (~ g)"); ax[0].set_ylabel(r"$\chi_\parallel$ (~ MOND $\nu$)")
    ax[0].set_title(f"MOND interpolation as Goldstone response (p={p16:.2f})")
    ax[0].legend(fontsize=8)
    for L in Lscan:
        c, e = curves_L[L]
        ax[1].plot(hs, c, "o-", ms=3, label=f"L={L}")
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("external field h"); ax[1].set_ylabel(r"$\chi_\parallel$")
    ax[1].set_title("finite-size scan: does the cutoff h_c survive L->inf?")
    ax[1].legend(fontsize=8)
    fig.suptitle("FM2-1: deep-MOND from the orientation ferromagnet + second-transition test",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM2_1_second_transition.png", dpi=130)
    print(f"saved {OUT/'FM2_1_second_transition.png'}")


if __name__ == "__main__":
    main()

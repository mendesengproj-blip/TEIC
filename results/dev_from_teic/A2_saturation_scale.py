"""A2_saturation_scale.py -- does the MOND scale a0 (X0=a0^2/2) have a GEOMETRIC origin
in the TEIC network: is the response saturation scale h_sat derivable from the
ferromagnet's internal quantities (spin stiffness rho_s, coupling J)?

Campaign DEV_FROM_TEIC, angle A2.  Charter: results/dev_from_teic/DEV_FROM_TEIC.md.

Background already MEASURED (build on it, do not repeat):
  * FM2-1: chi_par(h) = longitudinal susceptibility ~ the MOND interpolation nu(g/a0);
    it rises ~h^{-1/2} (deep-MOND) toward small h and its LOWER cutoff h_c is a
    FINITE-SIZE artifact (h_c ~ L^-2) -> no PHYSICAL second scale from the bare magnet.
  * C1: the deep-MOND coefficient rides on the stiffness rho_s(J) (external scale).

NEW test (never tried): the prompt's hypothesis  X0 = a0^2/2  ∝  rho_s * (J-J_c)/J_c.
We measure the UPPER crossover scale h_sat where the response leaves the deep-MOND
branch and becomes Newtonian:
    chi_par(h) -> C h^{-1/2}  (h << h_sat, deep-MOND / Goldstone anomaly)
    chi_par(h) -> chi_N       (h >> h_sat, Newtonian plateau)
    h_sat := field where chi_par(h) = THRESH * chi_N   (the MOND knee analog)
and ask whether h_sat(J) is DERIVABLE from rho_s(J) and (J-J_c): h_sat ∝ rho_s^a, etc.

Pre-registered reading:
  G0       reproduce FM2-1: chi_par rises toward small h in the ordered phase.
  A2-REL   if h_sat(J) tracks an internal combination of rho_s(J),(J-J_c) (good fit) =>
           the FORM of X0 emerges from the network -> [IDENTIFICADO].
  A2-SCALE the absolute a0 needs a lattice->SI unit map (the same external scale C1/D3D
           fixed) -> a0 stays [EXTERNO-B].  a0 is COMPARISON ONLY.

Anti-circularity: a0=1.2e-10 m/s^2 enters ONLY in the COMPARISON block at the end;
the engine uses only J, h, rho_s of the causal network.  Engine = fm2_core (E1).
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
J_SCAN = [0.75, 0.90, 1.10, 1.40, 1.80]          # ordered phase (J_c ~ 0.69 here)
HS = np.array([1.0, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01])
SEEDS = list(range(8))
N_BURN, N_MEAS = 400, 120
THRESH = 2.0                                       # knee: chi = THRESH * chi_Newtonian

# ---- COMPARISON ONLY (never used by the generator) ----
A0_SI = 1.2e-10            # m/s^2, SPARC (comparison point for the scale)


def chi_curve(L, J, seeds):
    """chi_par(h) = V*Var(m_par), seed-averaged (FM2-1 estimator)."""
    chi, sem = [], []
    for h in HS:
        vals = []
        for sd in seeds:
            s = fm2.sample_observables(L, J, h, seed=sd, n_burn=N_BURN, n_meas=N_MEAS)
            vals.append(L ** 3 * np.var(s["m_par"]))
        vals = np.array(vals)
        chi.append(float(vals.mean()))
        sem.append(float(vals.std() / np.sqrt(len(seeds))))
    return np.array(chi), np.array(sem)


def knee_hsat(hs, chi, thresh=THRESH):
    """h_sat = the field where chi(h), rising toward small h, first reaches thresh*chi_N.
    chi_N = Newtonian plateau = chi at the largest h.  Log-log linear interpolation
    between the bracketing points.  Returns (h_sat, chi_N)."""
    order = np.argsort(hs)[::-1]            # high h -> low h
    h = hs[order]; c = chi[order]
    chi_N = float(c[0])
    target = thresh * chi_N
    h_sat = float("nan")
    for i in range(1, len(h)):
        if c[i] >= target:                 # crossed the knee between h[i-1] and h[i]
            x0, x1 = np.log(h[i - 1]), np.log(h[i])
            y0, y1 = np.log(c[i - 1]), np.log(c[i])
            lt = np.log(target)
            if y1 != y0:
                h_sat = float(np.exp(x0 + (x1 - x0) * (lt - y0) / (y1 - y0)))
            else:
                h_sat = float(h[i])
            break
    return h_sat, chi_N


def main():
    t0 = time.time()
    print("=" * 78)
    print("A2 -- is the MOND saturation scale h_sat (X0) derivable from rho_s(J),(J-J_c)?")
    print("=" * 78)

    rows = {}
    for J in J_SCAN:
        chi, sem = chi_curve(L, J, SEEDS)
        h_sat, chi_N = knee_hsat(HS, chi)
        rho, mabs = fm2.helicity_modulus_series(L, J, seed=0, n_burn=N_BURN, n_meas=N_MEAS)
        rows[J] = {"chi": chi.tolist(), "sem": sem.tolist(), "chi_N": chi_N,
                   "h_sat": h_sat, "rho_s": float(rho), "m_abs": float(mabs)}
        print(f"  J={J:.2f}: rho_s={rho:.3f}  m_abs={mabs:.3f}  chi_N={chi_N:6.3f}  "
              f"h_sat={h_sat:.4f}  (chi rises {chi[-1]/chi[0]:.1f}x toward small h)")

    Js = np.array(J_SCAN, float)
    hsat = np.array([rows[J]["h_sat"] for J in J_SCAN])
    rhos = np.array([rows[J]["rho_s"] for J in J_SCAN])
    mabs = np.array([rows[J]["m_abs"] for J in J_SCAN])
    g0_pass = bool(np.all([rows[J]["chi"][-1] > rows[J]["chi"][0] for J in J_SCAN]))

    # ---- A2-REL: is h_sat derivable from the internal quantities rho_s, (J-J_c)? ----
    # J_c located where m_abs extrapolates to 0 (bare-magnet criticality); robust proxy:
    # the smallest-J point is near-critical.  Test candidate relations by their fit R^2
    # to log h_sat (so a pure proportional law gives slope ~ exponent, intercept = log k).
    valid = np.isfinite(hsat) & (hsat > 0) & (rhos > 0)
    candidates = {}
    if valid.sum() >= 3:
        lh = np.log(hsat[valid])
        # (i) h_sat ∝ rho_s^a
        a, b = np.polyfit(np.log(rhos[valid]), lh, 1)
        r2 = _r2(np.log(rhos[valid]), lh)
        candidates["h_sat ~ rho_s^a"] = {"exponent_a": float(a), "log_k": float(b), "R2": r2}
        # (ii) h_sat ∝ rho_s (proportional, exponent fixed 1): ratio CV
        ratio = hsat[valid] / rhos[valid]
        candidates["h_sat / rho_s (proportional)"] = {
            "mean_ratio": float(ratio.mean()), "CV": float(ratio.std() / ratio.mean())}
        # (iii) the prompt's X0 ∝ rho_s*(J-J_c)/J_c : use m_abs^2 as the (J-J_c)-proxy
        #       (m_abs^2 ∝ (J-J_c) near criticality, mean-field) -> X0 ∝ rho_s*m_abs^2
        proxy = rhos[valid] * mabs[valid] ** 2
        a3, b3 = np.polyfit(np.log(proxy), lh, 1)
        candidates["h_sat ~ [rho_s*(J-Jc)]^a  (J-Jc~m_abs^2)"] = {
            "exponent_a": float(a3), "log_k": float(b3), "R2": _r2(np.log(proxy), lh)}

    # best internal relation
    best = max((c for c in candidates if "R2" in candidates[c]),
               key=lambda c: candidates[c]["R2"], default=None)
    best_r2 = candidates[best]["R2"] if best else float("nan")
    rel_emerges = bool(best is not None and best_r2 > 0.9)

    # ---- A2-SCALE: COMPARISON ONLY -- map h_sat to a0, expose the unit gap ----
    # h_sat is O(0.01-0.1) in lattice (Zeeman) units; a0 is 1.2e-10 m/s^2.  The map
    # lattice->SI is exactly the external scale (G/hbar/f_pi) the program never derives.
    hsat_typ = float(np.nanmedian(hsat))
    comparison = {
        "h_sat_lattice_typical": hsat_typ,
        "a0_SI_comparison": A0_SI,
        "note": ("h_sat is a dimensionless lattice (Zeeman) field; a0 is a physical "
                 "acceleration.  Matching them requires the lattice->SI map (the same "
                 "external scale that fixes G_net, hbar, f_pi).  No internal derivation "
                 "of that map exists -> the ABSOLUTE a0 stays [EXTERNO-B]; only the "
                 "FORM/relation of h_sat to network quantities is testable here."),
    }

    if rel_emerges:
        status = "IDENTIFICADO"
        verdict = ("the saturation scale h_sat is DERIVABLE from internal network "
                   "quantities (best: %s, R^2=%.3f) -> the FORM of X0 emerges from the "
                   "ferromagnet.  But the ABSOLUTE a0 needs the external lattice->SI map "
                   "(A2-SCALE) -> a0 stays [EXTERNO-B].  'form derivable, scale external'."
                   % (best, best_r2))
    elif np.isfinite(best_r2):
        status = "INCONCLUSIVO"
        verdict = ("h_sat does NOT cleanly track a single internal combination of "
                   "rho_s,(J-J_c) (best R^2=%.3f < 0.9); and the absolute scale is "
                   "external.  a0 stays [EXTERNO-B]; the relation is at best suggestive."
                   % best_r2)
    else:
        status = "EXTERNO-B"
        verdict = ("h_sat could not be robustly extracted (knee not resolved in the "
                   "h-window) -> no internal derivation; a0 stays [EXTERNO-B].")

    print("-" * 78)
    print(f"  G0 (chi rises toward small h, deep-MOND): pass={g0_pass}")
    for c, d in candidates.items():
        print(f"  relation {c}: {d}")
    print(f"  best internal relation: {best}  (R^2={best_r2:.3f})")
    print(f"  A2-SCALE (COMPARISON ONLY): h_sat~{hsat_typ:.3f} lattice vs a0={A0_SI:.1e} SI "
          f"-> unit map external")
    print(f"  STATUS a0/X0: [{status}]")
    print(f"  VERDICT: {verdict}")
    print("=" * 78)

    _figure(rows, J_SCAN, hsat, rhos)
    payload = {
        "angle": "A2 -- geometric origin of a0 (saturation scale h_sat vs rho_s,J)",
        "engine": "fm2_core O(3) ferromagnet (E1)", "L": L, "J_scan": J_SCAN,
        "hs": HS.tolist(), "seeds": len(SEEDS), "thresh_knee": THRESH,
        "per_J": {str(J): rows[J] for J in J_SCAN},
        "h_sat": hsat.tolist(), "rho_s": rhos.tolist(), "m_abs": mabs.tolist(),
        "G0_chi_rises": g0_pass,
        "internal_relations": candidates, "best_relation": best, "best_R2": best_r2,
        "relation_emerges": rel_emerges,
        "comparison_only": comparison,
        "status_a0": status, "verdict": verdict,
        "anti_circularity": "a0 only in COMPARISON block; generator uses J,h,rho_s only",
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "A2_saturation_scale.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved A2_saturation_scale.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _r2(x, y):
    p = np.polyfit(x, y, 1)
    yhat = np.polyval(p, x)
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")


def _figure(rows, J_SCAN, hsat, rhos):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    for J in J_SCAN:
        ax[0].loglog(HS, rows[J]["chi"], "o-", ms=3, label=f"J={J} (rho_s={rows[J]['rho_s']:.2f})")
    ax[0].set_xlabel("external field h  (~ g)"); ax[0].set_ylabel(r"$\chi_\parallel$ (~ MOND $\nu$)")
    ax[0].set_title("response curves; knee h_sat = where chi = 2 chi_N")
    ax[0].legend(fontsize=7)
    good = np.isfinite(hsat) & (hsat > 0)
    ax[1].plot(rhos[good], hsat[good], "o", ms=8)
    if good.sum() >= 2:
        xx = np.linspace(rhos[good].min(), rhos[good].max(), 40)
        a, b = np.polyfit(np.log(rhos[good]), np.log(hsat[good]), 1)
        ax[1].plot(xx, np.exp(b) * xx ** a, "k--", lw=1, label=fr"$h_{{sat}}\propto\rho_s^{{{a:.2f}}}$")
        ax[1].legend(fontsize=9)
    ax[1].set_xlabel(r"spin stiffness $\rho_s(J)$"); ax[1].set_ylabel(r"$h_{sat}$ (X0 analog)")
    ax[1].set_title("is h_sat derivable from the internal stiffness?")
    ax[1].grid(alpha=0.2)
    fig.suptitle("A2: geometric origin of a0 -- saturation scale vs network stiffness", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "A2_saturation_scale.png", dpi=130)
    print("saved A2_saturation_scale.png")


if __name__ == "__main__":
    main()

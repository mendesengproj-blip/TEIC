"""VS5 -- do the four measured pure numbers of the network determine the
Standard Model coupling constants?

Charter: VACUUM_STRUCTURE.md (VS5).  Inputs are the four dimensionless numbers
already measured on the network (CR2 table + appendix):

    N1 = G_net rho^2 r_c^5      = 15/(8 pi^2)   (CR1/CR1b, measured to 2.5%)
    N2 = lambda_Sk^2 / <a^2>    = 1/120         (SC1-SC3, measured to 0.06%)
    N3 = X0 / (Dtheta_max^2 rho H^2) = pi/ln 2  (CR3, asymptotic closure 0.29%)
    N4 = m_iso^2 lambda_p       ~ 520           (CR4, CV 5.3% over rho x 4.7)

Targets (CODATA / PDG values, COMPARISON ONLY -- they are never inputs):

    alpha     = 1/137.035999   (fine structure)
    sin2_thW  = 0.23122        (weak mixing, MS-bar at m_Z)
    g_s       = 1.2            (strong coupling at ~1 GeV, charter's value)

Method (pre-registered in the charter):
  1. enumerate monomials  N1^a N2^b N3^c N4^d  with integer exponents in
     [-3, 3] (7^4 = 2401 combinations);
  2. for each target, record every combination within 10%, 5%, 1%;
  3. LOOK-ELSEWHERE CONTROL: the same search is run against random targets
     drawn log-uniformly over the decade window of each physical target.
     If the expected number of chance matches is >= 1 at a given tolerance,
     a match at that tolerance carries no evidential weight.

Honesty note (structural, independent of the numerics): alpha = e^2/(hbar c)
contains hbar.  The four network numbers are classical (the network's quantum
floor -- hbar, Born rule, quantisation -- is EXTERNAL, e11/T3C).  So a
derivation of alpha from {N1..N4} alone would actually CONTRADICT the
two-floor structure unless the hbar-dependence cancels in a ratio of
couplings.  The cleanest network-internal target is therefore a RATIO like
sin2_thW (dimensionless mixing of two couplings), not alpha itself.

Anti-circularity: no network generator is touched; this is pure arithmetic on
already-published measured constants.  Fixed seed for the Monte Carlo control.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- the inputs
PI = np.pi
N = {
    "N1": 15.0 / (8.0 * PI ** 2),     # 0.189982  (gravity)
    "N2": 1.0 / 120.0,                # 0.008333  (Skyrme length)
    "N3": PI / np.log(2.0),           # 4.532360  (DBI saturation / extremes)
    "N4": 520.0,                      # vector-mass invariant (CV 5.3%)
}
# relative 1-sigma uncertainties of the measured values (from their campaigns)
SIG = {"N1": 0.025, "N2": 0.0006, "N3": 0.0029, "N4": 0.053}

TARGETS = {
    "alpha":    1.0 / 137.035999,
    "sin2_thW": 0.23122,
    "g_s":      1.2,
}

EXP_RANGE = range(-3, 4)            # integer exponents -3..3
TOLS = (0.10, 0.05, 0.01)


def all_monomials():
    """Yield (exponents, value, sigma_rel) for every N1^a N2^b N3^c N4^d."""
    keys = list(N)
    for exps in itertools.product(EXP_RANGE, repeat=4):
        if all(e == 0 for e in exps):
            continue
        val = 1.0
        var = 0.0
        for k, e in zip(keys, exps):
            val *= N[k] ** e
            var += (e * SIG[k]) ** 2
        yield exps, val, np.sqrt(var)


def matches_for(target, combos, tol):
    out = []
    for exps, val, srel in combos:
        rel = abs(val - target) / target
        if rel <= tol:
            out.append({"exps": exps, "value": val, "rel_dev": rel,
                        "sigma_rel": srel})
    out.sort(key=lambda m: m["rel_dev"])
    return out


def chance_expectation(target, combos, tol, n_mc=2000, seed=42):
    """Expected number of matches if the target were a random number in the
    same decade: draw n_mc log-uniform fake targets in [target/sqrt(10),
    target*sqrt(10)] and average the match count at tolerance tol."""
    rng = np.random.default_rng(seed)
    vals = np.array([v for _, v, _ in combos])
    lo, hi = np.log(target / np.sqrt(10.0)), np.log(target * np.sqrt(10.0))
    fakes = np.exp(rng.uniform(lo, hi, n_mc))
    counts = [(np.abs(vals - f) / f <= tol).sum() for f in fakes]
    return float(np.mean(counts))


def fmt_exps(exps):
    keys = list(N)
    parts = [f"{k}^{e:+d}" for k, e in zip(keys, exps) if e != 0]
    return " ".join(parts)


def main():
    combos = list(all_monomials())
    print(f"enumerated {len(combos)} monomials, value range "
          f"[{min(v for _, v, _ in combos):.3e}, "
          f"{max(v for _, v, _ in combos):.3e}]")

    report = {"inputs": {k: N[k] for k in N}, "sigmas": SIG,
              "targets": TARGETS, "n_combos": len(combos), "results": {}}

    for tname, tval in TARGETS.items():
        entry = {"target": tval, "tols": {}}
        for tol in TOLS:
            mm = matches_for(tval, combos, tol)
            exp_chance = chance_expectation(tval, combos, tol)
            entry["tols"][f"{tol:.2f}"] = {
                "n_matches": len(mm),
                "expected_by_chance": exp_chance,
                "best": [{"combo": fmt_exps(m["exps"]),
                          "value": m["value"],
                          "rel_dev": m["rel_dev"],
                          "sigma_rel": m["sigma_rel"]} for m in mm[:5]],
            }
            print(f"{tname:9s} tol={tol:4.0%}: {len(mm):3d} matches "
                  f"(chance expectation {exp_chance:6.2f})"
                  + (f"  best: {fmt_exps(mm[0]['exps'])} = "
                     f"{mm[0]['value']:.6g} ({mm[0]['rel_dev']:.2%})"
                     if mm else ""))
        report["results"][tname] = entry

    # ------------------------------------------------- named simple ratios
    named = {
        "N2/N1": N["N2"] / N["N1"],
        "N1/N3": N["N1"] / N["N3"],
        "N1*N2": N["N1"] * N["N2"],
        "N3/N4": N["N3"] / N["N4"],
        "1/sqrt(N4)": N["N4"] ** -0.5,
        "N1^2": N["N1"] ** 2,
        "N3^-1": 1.0 / N["N3"],
    }
    print("\nnamed simple ratios:")
    for k, v in named.items():
        print(f"  {k:12s} = {v:.6g}")
    report["named_ratios"] = named

    # ------------------------------------------------- verdict bookkeeping
    # literal kill criterion: "no combination gives the constants at the
    # right order of magnitude".  Order of magnitude = factor 10 ~ tol large;
    # with 2401 monomials spanning ~20 decades this is trivially satisfiable,
    # so the literal kill CANNOT trigger; significance must come from the
    # chance control instead.
    significant = {}
    for tname, entry in report["results"].items():
        sig = []
        for tol_key, blk in entry["tols"].items():
            if blk["n_matches"] > 0 and blk["expected_by_chance"] < 0.5:
                sig.append(tol_key)
        significant[tname] = sig
    report["significant_tols"] = significant
    print("\nsignificance (matches where chance expectation < 0.5):",
          significant)

    (OUTDIR / "VS5_coupling_constants.json").write_text(
        json.dumps(report, indent=2, default=float))
    print("\nsaved VS5_coupling_constants.json")


if __name__ == "__main__":
    main()

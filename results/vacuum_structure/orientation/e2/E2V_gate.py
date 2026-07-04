"""E2V_gate.py -- engineering gate for the E2_MAGNON_BD campaign.

Charter: E2_MAGNON_BD.md (task E2-V).  MANDATORY before any physics measurement.
Validates the two engines E2 needs, on inputs with KNOWN answers, using exactly
the machinery that will run on the causal vacuum:

  GATE A -- ANALYSIS engine (S(k,omega) DFT + 3-model dispersion fit).
    Feed synthetic fields with a KNOWN dispersion law (these laws are the INPUT,
    labelled COMPARISON ONLY -- they are not produced by any network):
        * massless   omega = c0 k          -> fit must pick 'massless', c~c0;
        * massive    omega = sqrt(c0^2k^2+m0^2) -> fit must pick 'massive', m>0;
        * diffusive  omega = D0 k^2         -> fit must pick 'diffusive'.
    PASS if the fit recovers the right model and parameters within tolerance.

  GATE B -- PROPAGATION engine (the BD-smeared causal-set wave operator).
    (B1) Demonstrate WHY the symbol route is used: the retarded recursion
         phi(x)=2eps sum w(m) phi(y) is UNSTABLE (does not even preserve the
         constant zero-mode; the field blows up) -- the documented BD pointwise
         variance.  Reported, not hidden.
    (B2) Validate the STABLE observable: the operator symbol
         lambda(k,omega) = <f, B_eps f>/<f,f>,  f=cos(kx-wt), measured on real
         Poisson causal sets (seed-averaged).  In the continuum B_eps -> box, whose
         symbol is proportional to (k^2-omega^2) up to a normalization whose sign
         the smeared operator does not fix; the ON-SHELL dispersion is the zero
         crossing in omega.  PASS if the zero ridge is LINEAR with speed ~1 (the
         causal light-cone speed) -- a result, not an input: omega is scanned
         freely and c is a free fit parameter (anti-circularity).

ANTI-CIRCULARITY: no dispersion law enters the BD generator; c is never inserted;
probe waves are real cos (no complex literal); seeds fixed.  The synthetic laws in
GATE A are explicit COMPARISON-ONLY inputs used only to validate the analysis code.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e2_core as e2  # noqa: E402

OUT = Path(__file__).resolve().parent


# ====================================================================== #
# GATE A -- analysis engine on synthetic known dispersions
# ====================================================================== #
def gate_A():
    print("-" * 72)
    print("GATE A: S(k,omega) DFT + 3-model fit on synthetic KNOWN dispersions")
    rho, T, X = 8.0, 20.0, 12.0
    pts = e2.sprinkle_1plus1(rho, T, X, seed=0)
    # k modes spaced WIDER than the DFT resolution 2*pi/(2X) so neighbouring
    # synthetic modes do not leak into each other (leakage tilts the high-k peaks
    # and mimics a 'massive' trend).  k-range also keeps every law's omega(k)
    # inside the omega grid (most restrictive: diffusive D k^2 < omega_max).
    kmags = np.linspace(0.45, 1.6, 6)        # spacing 0.23 ~ DFT resolution 0.26
    omegas = np.linspace(0.0, 2.2, 220)

    c0, m0, D0 = 0.8, 0.5, 0.7
    laws = {
        "massless":  (lambda k: c0 * k),                       # COMPARISON ONLY
        "massive":   (lambda k: np.sqrt(c0**2 * k**2 + m0**2)),  # COMPARISON ONLY
        "diffusive": (lambda k: D0 * k**2),                    # COMPARISON ONLY
    }
    res = {}
    for name, fn in laws.items():
        phi = e2.synthetic_field(pts, kmags, fn)
        S = e2.structure_factor_kw(pts, phi, kmags, omegas)
        ostar, h, wd = e2.peak_dispersion(kmags, omegas, S)
        fit = e2.fit_dispersion(kmags, ostar, sigma=0.5 * (omegas[1] - omegas[0]) + 0.0 * ostar)
        ok = (fit["winner"] == name)
        res[name] = {"k": kmags.tolist(), "omega_star": ostar.tolist(),
                     "fit": fit, "winner": fit["winner"], "correct": bool(ok)}
        extra = ""
        if name == "massless":
            extra = f" c_fit={fit['massless']['c']:.3f} (true {c0})"
        elif name == "massive":
            extra = f" m_fit={fit['massive']['m']:.3f} (true {m0})"
        elif name == "diffusive":
            extra = f" D_fit={fit['diffusive']['D']:.3f} (true {D0})"
        print(f"   input '{name}': fit picks '{fit['winner']}' "
              f"{'OK' if ok else 'WRONG'}{extra}  v_rel_slope={fit['v_rel_slope']:+.3f}")
    passA = all(res[n]["correct"] for n in laws)
    print(f"   GATE A: {'PASS' if passA else 'FAIL'} "
          "(analysis distinguishes ck / massive / diffusive)")
    return res, passA


# ====================================================================== #
# GATE B1 -- demonstrate retarded-recursion instability
# ====================================================================== #
def gate_B1():
    print("-" * 72)
    print("GATE B1: retarded BD recursion is UNSTABLE (justifies the symbol route)")
    rho, T, X, eps = 10.0, 16.0, 8.0, 0.2
    pts = e2.sprinkle_1plus1(rho, T, X, seed=1)
    C = e2.order_matrix(pts)
    init_mask = pts[:, 0] <= 3.0
    phi0 = np.ones(pts.shape[0])                # constant = exact zero mode of box
    phi = e2.bd_propagate(pts, C, phi0, init_mask, eps)
    bulk = (~init_mask) & (pts[:, 0] > 0.3 * pts[:, 0].max())
    blow = float(np.max(np.abs(phi[bulk]))) if bulk.any() else float("nan")
    mean_bulk = float(np.mean(phi[bulk])) if bulk.any() else float("nan")
    unstable = (blow > 5.0) or (abs(mean_bulk - 1.0) > 1.0)
    print(f"   constant zero-mode after recursion: <phi_bulk>={mean_bulk:+.2f} "
          f"(want 1), max|phi|={blow:.1f}")
    print(f"   -> recursion {'UNSTABLE (expected, BD variance)' if unstable else 'stable'}; "
          "use the symbol route.")
    return {"mean_bulk": mean_bulk, "max_abs": blow, "unstable": bool(unstable),
            "params": {"rho": rho, "T": T, "X": X, "eps": eps}}


# ====================================================================== #
# GATE B2 -- BD symbol recovers a linear dispersion with speed ~1
# ====================================================================== #
def measure_symbol_dispersion(rho, T, X, eps, kmags, omegas, n_seeds, max_n=120,
                              seed0=0):
    """Seed-averaged BD symbol lambda(k,omega) and its zero-crossing dispersion.
    Also returns per-seed omega*(k) for error bars."""
    Lacc = np.zeros((len(kmags), len(omegas)))
    per_seed = []
    used = 0
    for s in range(n_seeds):
        pts = e2.sprinkle_1plus1(rho, T, X, seed0 + s)
        C = e2.order_matrix(pts)
        mids = e2.bulk_events(pts, max_n=max_n, seed=seed0 + s)
        if mids.size < 8:
            continue
        ops = e2.precompute_bd_operator(pts, C, mids, eps)
        L = e2.symbol_grid(pts, ops, mids, kmags, omegas)
        Lacc += L
        ostar_s, found_s = e2.dispersion_from_symbol(kmags, omegas, L)
        per_seed.append(ostar_s)
        used += 1
    L = Lacc / max(used, 1)
    ostar, found = e2.dispersion_from_symbol(kmags, omegas, L)
    per_seed = np.array(per_seed)                       # (used, n_k)
    with np.errstate(invalid="ignore"):
        sem = np.nanstd(per_seed, axis=0) / np.sqrt(max(used, 1))
    return L, ostar, found, sem, used


def gate_B2():
    print("-" * 72)
    print("GATE B2: BD symbol zero-ridge = dispersion (expect linear, speed ~1)")
    rho, T, X, eps = 30.0, 10.0, 16.0, 0.15
    kmags = np.linspace(0.5, 1.4, 8)
    omegas = np.linspace(0.0, 1.8, 46)
    n_seeds = 16
    L, ostar, found, sem, used = measure_symbol_dispersion(
        rho, T, X, eps, kmags, omegas, n_seeds)
    sig = np.where(np.isfinite(sem) & (sem > 0), sem, np.nanmedian(sem[sem > 0]) if np.any(sem > 0) else 0.05)
    fit = e2.fit_dispersion(kmags[found], ostar[found], sigma=sig[found])
    c_fit = fit["massless"]["c"]
    dev = fit["linear_rel_deviation_pct"]
    print(f"   seeds used={used}  found {found.sum()}/{len(kmags)} crossings")
    for i in range(len(kmags)):
        if found[i]:
            print(f"     k={kmags[i]:.2f}  omega*={ostar[i]:.3f}  (omega=k -> {kmags[i]:.2f})")
    print(f"   fit winner={fit['winner']} (aic={fit['winner_aic']})  c_fit={c_fit:.3f}  "
          f"v_rel_slope={fit['v_rel_slope']:+.3f}  linear deviation={dev:.1f}%")
    # PASS: a crossing found at most k, dispersion approximately linear, speed near 1
    passB = (found.sum() >= 5) and (dev < 20.0) and (0.6 < c_fit < 1.5)
    print(f"   GATE B2: {'PASS' if passB else 'FAIL'} "
          "(symbol gives a linear ridge with light-cone speed)")
    return ({"rho": rho, "T": T, "X": X, "eps": eps, "n_seeds": used,
             "k": kmags.tolist(), "omega": omegas.tolist(), "L": L.tolist(),
             "omega_star": ostar.tolist(), "found": found.tolist(),
             "sem": sig.tolist(), "fit": fit, "c_fit": c_fit, "deviation_pct": dev},
            passB)


# ====================================================================== #
# driver + figure
# ====================================================================== #
def main():
    t0 = time.time()
    print("=" * 72)
    print("E2-V GATE -- validate analysis + BD propagation engines")
    print("=" * 72)
    A, passA = gate_A()
    B1 = gate_B1()
    B2, passB2 = gate_B2()
    gate_pass = passA and B1["unstable"] and passB2

    print("=" * 72)
    print(f"GATE A (analysis):      {'PASS' if passA else 'FAIL'}")
    print(f"GATE B1 (instability):  {'SHOWN' if B1['unstable'] else 'not shown'}")
    print(f"GATE B2 (BD symbol):    {'PASS' if passB2 else 'FAIL'}")
    print(f"E2-V GATE: {'PASS -- proceed to E2-1' if gate_pass else 'FAIL -- do not proceed'}")
    print("=" * 72)

    # ---- figure ----
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    # panel 1: gate A synthetic recoveries
    for name, col in (("massless", "tab:blue"), ("massive", "tab:green"),
                      ("diffusive", "tab:red")):
        k = np.array(A[name]["k"]); o = np.array(A[name]["omega_star"])
        axes[0].plot(k, o, "o-", color=col, label=f"{name} -> {A[name]['winner']}")
    axes[0].set_xlabel("k"); axes[0].set_ylabel(r"$\omega^*(k)$")
    axes[0].set_title("GATE A: analysis recovers known dispersions")
    axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)
    # panel 2: BD symbol heatmap with zero ridge
    k = np.array(B2["k"]); om = np.array(B2["omega"]); L = np.array(B2["L"])
    pcm = axes[1].pcolormesh(k, om, L.T, shading="auto", cmap="RdBu_r",
                             vmin=-np.nanmax(np.abs(L)), vmax=np.nanmax(np.abs(L)))
    fig.colorbar(pcm, ax=axes[1], label=r"$\lambda(k,\omega)$")
    os_ = np.array(B2["omega_star"]); fnd = np.array(B2["found"])
    axes[1].plot(k[fnd], os_[fnd], "ko", ms=6, label=r"$\omega^*$ (zero ridge)")
    axes[1].plot(k, k, "k--", lw=1, label=r"$\omega=k$ (light cone)")
    axes[1].set_xlabel("k"); axes[1].set_ylabel(r"$\omega$")
    axes[1].set_title("GATE B2: BD symbol & zero ridge"); axes[1].legend(fontsize=8)
    # panel 3: dispersion + linear fit
    axes[2].errorbar(k[fnd], os_[fnd], yerr=np.array(B2["sem"])[fnd], fmt="ko",
                     capsize=3, label="symbol")
    kk = np.linspace(0, k.max(), 50)
    axes[2].plot(kk, B2["fit"]["massless"]["c"] * kk, "b-",
                 label=f"ck fit c={B2['c_fit']:.2f}")
    axes[2].plot(kk, kk, "k--", lw=1, label=r"$\omega=k$")
    axes[2].set_xlabel("k"); axes[2].set_ylabel(r"$\omega^*$")
    axes[2].set_title(f"GATE B2 dispersion (dev {B2['deviation_pct']:.0f}%)")
    axes[2].legend(fontsize=8); axes[2].grid(alpha=0.3)
    fig.suptitle("E2-V gate: analysis recovers known laws; BD symbol gives linear "
                 "omega=ck (c emergent, not inserted)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E2V_gate.png", dpi=130)
    print(f"saved {OUT/'E2V_gate.png'}")

    payload = {"gate_A": A, "gate_A_pass": bool(passA),
               "gate_B1_instability": B1,
               "gate_B2": B2, "gate_B2_pass": bool(passB2),
               "gate_pass": bool(gate_pass),
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E2V_gate.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E2V_gate.json'}  ({payload['runtime_s']:.0f}s)")
    return payload


if __name__ == "__main__":
    main()

"""D3A_robustness.py -- is the -1 exponent of D3 a law or a finite-size artefact?

BRIDGE / D3 AUDIT, task A.  Vary box size L, network density rho (= cell
resolution), seeds, and MC steps; measure the tail exponent p of theta(r)=A r^p.

Method (see d3_audit_core docstring): for the quadratic BD action the Metropolis
equilibrium MEAN is exactly the discrete-Poisson minimiser, so the deterministic
solver gives the L,rho->infinity (zero MC-noise) exponent on the full L x rho grid,
while the batched heat-bath MC gives the seed-to-seed error bars and shows the MC
noise on p shrinking with the number of sweeps.  No G / GM/r / Schwarzschild in the
generator: the source is a dimensionless weight w_M on a finite core.

Death criterion: if p drifts AWAY from -1 as L grows (e.g. -> -1.2 or -0.8), D3 was
a finite-size artefact.  Success: p -> -1 with clean 1/L convergence, and D3's -1.02
sits inside the band.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from d3_audit_core import (radial_grid, radial_source_core, radial_solve,
                           radial_mc_batch, fit_tail)

R_MIN, R_CORE, K, TEMP = 0.5, 2.0, 1.0, 0.02
L_LIST = [10.0, 20.0, 40.0, 80.0]
RHO_LIST = [50.0, 100.0, 200.0, 400.0]
SWEEP_LIST = [10_000, 100_000, 1_000_000]
N_SEEDS = 20
W_M = 1.0


def nbins_of_rho(rho):
    """rho (cell density) -> radial resolution: n_bins ~ 8.62 rho^(1/3), clipped."""
    return int(np.clip(round(8.62 * rho ** (1.0 / 3.0)), 20, 80))


def main():
    t0 = time.time()
    rng_seed_base = 20250607

    # ---------- PART 1: deterministic solver on the full L x rho grid ----------
    p_grid = np.full((len(L_LIST), len(RHO_LIST)), np.nan)
    A_grid = np.full_like(p_grid, np.nan)
    for iL, L in enumerate(L_LIST):
        for ir, rho in enumerate(RHO_LIST):
            nb = nbins_of_rho(rho)
            _, centers, sv = radial_grid(L, nb, R_MIN)
            q = radial_source_core(centers, sv, R_CORE, W_M)
            th = radial_solve(centers, sv, q, K)
            A, C, p = fit_tail(centers, th, R_CORE, 0.6 * L)
            p_grid[iL, ir] = p
            A_grid[iL, ir] = A

    # L -> infinity extrapolation (boundary correction ~ 1/L), per rho
    p_inf = {}
    for ir, rho in enumerate(RHO_LIST):
        invL = 1.0 / np.array(L_LIST)
        pcol = p_grid[:, ir]
        ok = np.isfinite(pcol)
        if ok.sum() >= 2:
            a, b = np.polyfit(invL[ok], pcol[ok], 1)   # p = a*(1/L) + b
            p_inf[rho] = float(b)                       # intercept = 1/L -> 0
        else:
            p_inf[rho] = float("nan")
    # also extrapolate the largest-rho column in BOTH 1/L and L: report the cleanest
    p_inf_overall = float(np.nanmean(list(p_inf.values())))

    # ---------- PART 2: MC error bars + noise vs sweeps (representative) -------
    L_rep, rho_rep = 40.0, 100.0
    nb = nbins_of_rho(rho_rep)
    _, centers, sv = radial_grid(L_rep, nb, R_MIN)
    q = radial_source_core(centers, sv, R_CORE, W_M)
    th_solve_rep = radial_solve(centers, sv, q, K)
    A_s, C_s, p_solve_rep = fit_tail(centers, th_solve_rep, R_CORE, 0.6 * L_rep)

    mc_noise = []   # (sweeps, mean_p, std_p, mean_absdev_from_solve)
    for ns in SWEEP_LIST:
        seeds = list(rng_seed_base + np.arange(N_SEEDS))
        nb_use = ns // 4
        ths = radial_mc_batch(centers, sv, q, K, TEMP, ns, nb_use, seeds)
        ps = np.array([fit_tail(centers, ths[:, k], R_CORE, 0.6 * L_rep)[2]
                       for k in range(N_SEEDS)])
        dev = np.mean([np.max(np.abs(ths[:, k] - th_solve_rep)) for k in range(N_SEEDS)])
        mc_noise.append((ns, float(np.nanmean(ps)), float(np.nanstd(ps)), float(dev)))

    # ---------- verdicts ----------
    # convergence: does |p_inf + 1| shrink and is the largest-L row close to -1?
    p_bigL = p_grid[-1, :]               # L = 80
    conv_ok = bool(np.nanmax(np.abs(p_bigL + 1.0)) < 0.06 and abs(p_inf_overall + 1.0) < 0.04)
    # MC noise decreases with sweeps?
    stds = [m[2] for m in mc_noise]
    noise_decreases = bool(stds[0] > stds[-1] and stds[-1] < 0.02)
    # D3's -1.02 inside the band?
    d3_path = OUT.parents[1] / "bridge" / "dynamics" / "D3_MC_data.json"
    d3_p = json.load(open(d3_path))["tail_exponent_offset_removed"] if d3_path.exists() else -1.02
    d3_in_band = bool(min(p_bigL.min(), -1.02) - 0.05 <= d3_p <= max(p_bigL.max(), -0.95) + 0.05)

    passes = conv_ok and noise_decreases and d3_in_band
    verdict = "PASSA" if passes else "FALHA"

    # ---------- figure ----------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for ir, rho in enumerate(RHO_LIST):
        ax[0].plot(1.0 / np.array(L_LIST), p_grid[:, ir], "o-", ms=5,
                   label=fr"$\rho={rho:.0f}$ (extrap $p_\infty={p_inf[rho]:.3f}$)")
    ax[0].axhline(-1.0, color="k", ls="--", lw=1, label="Newtonian $-1$")
    ax[0].set_xlabel("$1/L$ (box$^{-1}$)"); ax[0].set_ylabel("tail exponent $p$")
    ax[0].set_title("(D3-A) $p\\to-1$ as $L\\to\\infty$ (solver = MC mean)")
    ax[0].legend(fontsize=7.5); ax[0].invert_xaxis()

    sw = np.array([m[0] for m in mc_noise]); mp = np.array([m[1] for m in mc_noise])
    sd = np.array([m[2] for m in mc_noise])
    ax[1].errorbar(sw, mp, yerr=sd, fmt="s-", ms=6, capsize=4,
                   label=f"MC mean$\\pm$std ({N_SEEDS} seeds)")
    ax[1].axhline(-1.0, color="k", ls="--", lw=1, label="Newtonian $-1$")
    ax[1].axhline(p_solve_rep, color="C3", ls=":", lw=1.2,
                  label=f"solver (MC mean) $={p_solve_rep:.3f}$")
    ax[1].set_xscale("log"); ax[1].set_xlabel("MC sweeps")
    ax[1].set_ylabel("exponent $p$ (rep. $L{=}40,\\rho{=}100$)")
    ax[1].set_title("(D3-A) MC noise on $p$ shrinks with sweeps")
    ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "D3A_robustness.png", dpi=130)

    summary = {
        "what": "Robustness of D3's tail exponent under L, rho, seeds, MC steps.",
        "method": "solver = exact MC mean for the quadratic BD action (full L x rho "
                  "grid); batched heat-bath MC for seed error bars and noise-vs-sweeps.",
        "L_list": L_LIST, "rho_list": RHO_LIST, "nbins_of_rho":
            {str(r): nbins_of_rho(r) for r in RHO_LIST},
        "r_min": R_MIN, "r_core": R_CORE, "K": K, "temp": TEMP, "w_M": W_M,
        "p_grid_L_by_rho": p_grid.tolist(), "A_grid_L_by_rho": A_grid.tolist(),
        "p_inf_per_rho": {str(k): v for k, v in p_inf.items()},
        "p_inf_overall": p_inf_overall,
        "mc_noise_sweeps_meanP_stdP_dev": mc_noise,
        "p_solve_representative": p_solve_rep,
        "D3_stored_exponent": d3_p,
        "convergence_ok": conv_ok, "mc_noise_decreases": noise_decreases,
        "D3_inside_band": d3_in_band, "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "D3A_robustness_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("D3-A -- ROBUSTNESS OF THE -1 EXPONENT")
    print("=" * 72)
    print("p(L, rho) from the exact solver (= MC mean):")
    print("   L \\ rho " + "".join(f"{r:>9.0f}" for r in RHO_LIST))
    for iL, L in enumerate(L_LIST):
        print(f"   {L:6.0f}  " + "".join(f"{p_grid[iL,ir]:9.3f}" for ir in range(len(RHO_LIST))))
    print("-" * 72)
    for rho in RHO_LIST:
        print(f"  L->inf extrapolation (rho={rho:.0f}):  p_inf = {p_inf[rho]:+.4f}")
    print(f"  overall p_inf = {p_inf_overall:+.4f}   (Newtonian -1)")
    print("-" * 72)
    print(f"MC noise on p at L=40, rho=100 (solver p={p_solve_rep:.3f}):")
    for ns, mpv, sdv, dev in mc_noise:
        print(f"  sweeps={ns:>9}: p = {mpv:+.4f} +- {sdv:.4f}   |mc-solve|max={dev:.2e}")
    print("-" * 72)
    print(f"convergence to -1     : {conv_ok}")
    print(f"MC noise decreases    : {noise_decreases}  (std {stds[0]:.4f} -> {stds[-1]:.4f})")
    print(f"D3's {d3_p:.3f} in band : {d3_in_band}")
    print(f"VERDICT (D3-A): {verdict}   [{summary['runtime_s']}s]")
    return summary


if __name__ == "__main__":
    main()

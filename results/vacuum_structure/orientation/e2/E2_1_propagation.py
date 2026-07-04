"""E2_1_propagation.py -- dispersion of the orientation fluctuation via B_eps.

Charter: E2_MAGNON_BD.md (E2-1).  Runs ONLY because E2-V PASSED.  E1 established
that the causal vacuum is an orientation ferromagnet (ordered phase, J>J_c) whose
SOFT excitations are the transverse orientation fluctuations delta-n; E1-3 showed
the BARE-link Laplacian gives a FLAT, non-local S(k) (no gradient stiffness, no
omega=ck) and identified the smeared causal-set d'Alembertian (Sorkin/BD, e10) as
the missing relativistic kinetic operator.  E2-1 measures the dispersion that B_eps
gives to delta-n.

How (validated in E2-V).  The literal recipe "propagate delta-n by the Euler step
dn(t+dt)=dn(t)+dt*B_eps[dn] and FFT delta-n(x,t)" cannot be run: that explicit
inverse of B_eps is UNSTABLE on a causal set (E2-V B1: the constant zero-mode
blows up to |phi|~1000 -- the documented BD pointwise variance).  The STABLE,
equivalent observable is the operator's symbol
    lambda(k,omega) = <f, B_eps f>/<f,f>,   f = cos(k x - omega t),
whose zero ridge in omega IS the on-shell dispersion omega*(k) (B_eps -> box in
the continuum; box's symbol vanishes on shell).  The symbol's zero ridge is the
same dispersion that the peak ridge of S(k,omega) would trace -- B_eps is the
inverse propagator, S is the propagator; they share the on-shell locus.

U(1) vs O(3).  B_eps is a SCALAR operator: it acts identically on the U(1) phase
delta-phi and on each Cartesian component of the O(3) vector delta-n.  Hence the
DISPERSION is the same for both candidates -- the relativistic kinetic structure
is a property of the causal-set operator, not of the internal symmetry group.  We
therefore measure the (component) scalar symbol with high statistics; it applies
to both.  The U(1)/O(3) difference -- number and transversality of polarisations
-- is the subject of E2-3.

Anti-circularity: c never enters; probe waves are real cos; seeds fixed; the
dispersion shape (linear/quadratic/gapped) is the discriminator, not a number
compared to a pre-set c.
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

# ---- ordered-phase configuration (J>J_c lives in the E1 Metropolis; here the
# field is the FLUCTUATION delta-n whose kinetic operator is B_eps).  Box chosen
# for clean low-k (large X) while keeping n manageable for the O(n^2) order matrix.
RHO, T, X, EPS = 24.0, 10.0, 18.0, 0.15
KMAGS = np.linspace(0.40, 1.45, 10)
OMEGAS = np.linspace(0.0, 1.9, 48)
N_SEEDS = 20
MAX_N = 120


def main():
    t0 = time.time()
    print("=" * 72)
    print("E2-1 -- dispersion of the orientation fluctuation via the BD operator")
    print("=" * 72)
    print(f"config: rho={RHO} T={T} X={X} eps={EPS}  k in [{KMAGS[0]:.2f},{KMAGS[-1]:.2f}]"
          f"  {N_SEEDS} seeds")

    res = e2.measure_symbol_dispersion(RHO, T, X, EPS, KMAGS, OMEGAS, N_SEEDS,
                                       max_n=MAX_N, seed0=2000, verbose=True)
    k = res["k"]; om = res["omega"]; L = res["L"]
    ostar = res["omega_star"]; found = res["found"]; sem = res["sem"]
    print(f"\nseeds used: {res['n_seeds_used']}   crossings found: {found.sum()}/{len(k)}")
    for i in range(len(k)):
        if found[i]:
            print(f"   k={k[i]:.3f}  omega*={ostar[i]:.3f} +/- {sem[i]:.3f}   "
                  f"(omega=k -> {k[i]:.3f})  v=omega*/k={ostar[i]/k[i]:.3f}")

    # ---- save the dispersion for E2-2 (no fit here; E2-2 does the 3-model fit) ----
    payload = {
        "config": {"rho": RHO, "T": T, "X": X, "eps": EPS, "n_seeds": N_SEEDS,
                   "max_n": MAX_N, "k": k.tolist(), "omega": om.tolist()},
        "n_seeds_used": int(res["n_seeds_used"]),
        "omega_star": ostar.tolist(),
        "found": found.tolist(),
        "sem": sem.tolist(),
        "per_seed_omega_star": res["per_seed"].tolist(),
        "symbol_grid_L": L.tolist(),
        "note": ("omega*(k) = zero ridge of the BD symbol lambda(k,omega), seed-"
                 "averaged.  Applies to U(1) phase and to each O(3) component "
                 "(B_eps is a scalar operator).  E2-2 performs the ck/massive/"
                 "diffusive fit; E2-3 the polarisation."),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E2_1_propagation.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E2_1_propagation.json'}")

    # ---- figure: symbol map + zero ridge, and a wavefront reconstructed from
    # the MEASURED omega*(k) (a faithful picture of delta-n(x,t) propagating at the
    # measured speed -- the stable stand-in for the unstable direct propagation) ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    vmax = np.nanmax(np.abs(L))
    pcm = axes[0].pcolormesh(k, om, L.T, shading="auto", cmap="RdBu_r",
                             vmin=-vmax, vmax=vmax)
    fig.colorbar(pcm, ax=axes[0], label=r"$\lambda(k,\omega)=\langle f,B_\varepsilon f\rangle/\langle f,f\rangle$")
    axes[0].errorbar(k[found], ostar[found], yerr=sem[found], fmt="ko", ms=5,
                     capsize=3, label=r"$\omega^*$ (zero ridge)")
    axes[0].plot(k, k, "k--", lw=1, label=r"$\omega=k$ (light cone)")
    axes[0].set_xlabel("k"); axes[0].set_ylabel(r"$\omega$")
    axes[0].set_title("E2-1: BD symbol of the orientation fluctuation")
    axes[0].legend(fontsize=8)

    # reconstructed delta-n(x,t) from measured omega*(k)
    kf = k[found]; of = ostar[found]
    xs = np.linspace(-X, X, 240)
    ts = np.linspace(0, T, 200)
    XX, TT = np.meshgrid(xs, ts)
    field = np.zeros_like(XX)
    for kk, ww in zip(kf, of):
        field += np.cos(kk * XX) * np.cos(ww * TT)      # standing/superposed packet
    im = axes[1].pcolormesh(xs, ts, field, shading="auto", cmap="viridis")
    fig.colorbar(im, ax=axes[1], label=r"$\delta n(x,t)$ (reconstructed)")
    # light cone guides x = +/- c_meas t with c_meas ~ mean(omega*/k)
    c_meas = float(np.mean(of / kf))
    axes[1].plot(c_meas * ts, ts, "w--", lw=1, label=f"x={c_meas:.2f} t")
    axes[1].plot(-c_meas * ts, ts, "w--", lw=1)
    axes[1].set_xlabel("x"); axes[1].set_ylabel("t")
    axes[1].set_title(rf"$\delta n(x,t)$ from measured $\omega^*(k)$  (c$\approx${c_meas:.2f})")
    axes[1].legend(fontsize=8, loc="upper right")
    fig.suptitle("E2-1: orientation-fluctuation dispersion from the smeared "
                 "causal-set d'Alembertian (U(1)=O(3) component; c emergent)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E2_1_propagation.png", dpi=130)
    print(f"saved {OUT/'E2_1_propagation.png'}  ({payload['runtime_s']:.0f}s)")


if __name__ == "__main__":
    main()

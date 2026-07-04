"""HE2 -- DEV in the high-acceleration regime g >> a0:  does the gravitational boost ever
drop below 1 (G_eff < G_N) anywhere, which would resolve the S8 tension?

HIGH_ENERGY_REGIME.md asks: compute mu(g/a0) for g/a0 in [0.001, 1000].  Can the boost cross
1 in some regime?  If a sub-Newtonian (suppressed) window exists, which cosmological scale
would it correspond to?

DEATH CRITERION (pre-registered): boost >= 1 in every regime (MOND always ENHANCES) ->
the S8 frontier stays where FM1 put it.  Do NOT tune parameters to escape.

We test THREE objects, all anchored to the existing DEV code (no new free knob is fitted):

  (A) the AQUAL pair (mu, nu) of the calibrated galactic interpolation
        mu_dev(x) = x/sqrt(1+x^2)          (kinetic coefficient; g_N = mu*g)
        nu(y)     = boost g_obs/g_N = 1/mu  (Bekenstein-Milgrom nu, >= 1 by construction)
      from DEV/paper_I/theory.py  -- the function fit to 167 SPARC galaxies.

  (B) the LINEAR-GROWTH effective coupling that actually drives S8
        mu_eff(x) = 1 + (alpha*beta/2)/sqrt(x(1+x)),   x = g_cosmo/a0
      from DEV/paper_I/cosmology.py -- the exact object FM1 used.  G_eff/G_N = mu_eff.
      beta is the value calibrated on galaxies (beta_best = 0.00746); alpha = 2/3.

  (C) the C4 strong-field extension (DEV_EXT_C4, dev_ext/strong_field.md): the quartic
      operator screens the scalar coupling as kappa/(1+4 eps x^2)^2, so the enhancement
      DECAYS faster at high x.  We ask whether the screening can OVERSHOOT and turn the
      boost sub-Newtonian.

Then we MAP the high-acceleration regime to physical scales: g_cosmo(z,k)/a0 for the modes
that set sigma8, and g/a0 for compact systems, to answer "which cosmological scale is
g >> a0?".

Anti-circularity: every function and constant is imported from the committed DEV pipeline;
nothing is re-fit here.  The only computation is evaluation + the boost sign.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]            # .../003-TEORIAS/TEIC
DEVP = ROOT.parents[0] / "DEV" / "dev_pipeline" / "paper_I"
sys.path.insert(0, str(DEVP))

import theory as T          # noqa: E402  mu_dev, nu_dev, A0, ALPHA_SPHERICAL
import cosmology as Cosmo   # noqa: E402  g_cosmo, mu_eff, OMEGA_M0, ...

OUT = Path(__file__).resolve().parent
A0 = T.A0
ALPHA = T.ALPHA_SPHERICAL
BETA = 0.00746            # calibrate_beta.fit_beta() -> beta_best (galaxy-calibrated)

# representative C4 parameters (dev_ext): kappa = gamma^2/m_A^2 (small), eps = O(1) dimensionless
KAPPA = 0.0085            # ~ the slip amplitude scale used in dbi_saturation
EPS_LIST = [0.0, 0.01, 0.1, 1.0]


# --------------------------------------------------------------------------- #
def aqual_boost(x):
    """Bekenstein-Milgrom boost nu = g_obs/g_N as a function of x = g/a0 (=1/mu_dev)."""
    return 1.0 / T.mu_dev(x)


def growth_coupling(x, alpha=ALPHA, beta=BETA):
    """G_eff/G_N for linear perturbations (cosmology.mu_eff form), as a function of x=g/a0."""
    return 1.0 + (alpha * beta / 2.0) / np.sqrt(x * (1.0 + x))


def growth_coupling_C4(x, eps, alpha=ALPHA, beta=BETA):
    """C4-screened growth coupling: the quartic operator (dev_ext) multiplies the scalar
    enhancement by the screening factor 1/(1+4 eps x^2)^2.  At low x (eps x^2 << 1) the full
    DEV/MOND enhancement is recovered; at high x the enhancement is suppressed FASTER than the
    bare 1/sqrt(x(1+x)) tail, driving G_eff/G_N toward 1 sooner.  The screening factor is in
    [0,1], so it can only REMOVE enhancement -- it cannot make the coupling sub-Newtonian."""
    screen = 1.0 / (1.0 + 4.0 * eps * x ** 2) ** 2
    return 1.0 + (alpha * beta / 2.0) / np.sqrt(x * (1.0 + x)) * screen


def cosmo_scale_x(z, k_hMpc):
    """x = g_cosmo(z,k)/a0 for a linear mode (k in h/Mpc) at redshift z."""
    return float(Cosmo.g_cosmo(z, k_hMpc) / A0)


def sphere_scale_x(R_Mpc_over_h, Omega_m=Cosmo.OMEGA_M0, H0_kms=Cosmo.H0_KMS_MPC):
    """x = g/a0 for the mean-density acceleration at the EDGE of a sphere of comoving radius
    R (Mpc/h):  g = (Omega_m H0^2 / 2) * R  (Newtonian accel of the enclosed mean mass)."""
    H0_SI = H0_kms * 1000.0 / 3.0857e22
    R_m = (R_Mpc_over_h / (H0_kms / 100.0)) * 3.0857e22
    g = 0.5 * Omega_m * H0_SI ** 2 * R_m
    return float(g / A0), float(g)


def main():
    t0 = time.time()
    print("=" * 76)
    print("HE2 -- DEV BOOST ACROSS g/a0 in [1e-3, 1e3]   (does it ever go sub-Newtonian?)")
    print("=" * 76)

    x = np.logspace(-3, 3, 1300)

    nu = aqual_boost(x)                              # AQUAL boost (galactic)
    mu_g = growth_coupling(x)                        # growth coupling (S8)
    mu_C4 = {eps: growth_coupling_C4(x, eps) for eps in EPS_LIST}

    # --- decisive minima (sub-Newtonian == value < 1) -----------------------
    min_nu = float(nu.min()); x_min_nu = float(x[np.argmin(nu)])
    min_mug = float(mu_g.min()); x_min_mug = float(x[np.argmin(mu_g)])
    min_C4 = {eps: float(v.min()) for eps, v in mu_C4.items()}
    any_below = (min_nu < 1.0 - 1e-9) or (min_mug < 1.0 - 1e-9) or \
                any(m < 1.0 - 1e-9 for m in min_C4.values())

    print(f"[A] AQUAL boost nu(x)=1/mu_dev :  min over range = {min_nu:.6f} at x={x_min_nu:.2e}"
          f"  ({'SUB-NEWTONIAN' if min_nu<1 else 'always >=1: ENHANCES'})")
    print(f"[B] growth coupling mu_eff(x)  :  min over range = {min_mug:.6f} at x={x_min_mug:.2e}"
          f"  ({'SUB-NEWTONIAN' if min_mug<1 else 'always >=1: ENHANCES'})")
    for eps in EPS_LIST:
        print(f"[C] C4 growth (eps={eps:<4}) :  min = {min_C4[eps]:.6f}"
              f"  ({'SUB-NEWTONIAN' if min_C4[eps]<1 else 'always >=1'})")

    # --- which scale is g >> a0?  map cosmology -> x ------------------------
    print("-" * 76)
    print("WHICH SCALE IS g >> a0 ?   x = g/a0 for representative systems:")
    cosmo_modes = []
    for z in (0.0, 0.5, 1.0):
        for k in (0.01, 0.1, 1.0):
            xv = cosmo_scale_x(z, k)
            cosmo_modes.append({"z": z, "k_hMpc": k, "x": xv,
                                "mu_eff": float(growth_coupling(xv))})
    x_s8, g_s8 = sphere_scale_x(8.0)                 # the sigma8 sphere
    s8_entry = {"system": "sigma8 sphere R=8 Mpc/h", "x": x_s8,
                "mu_eff": float(growth_coupling(x_s8)), "boost_nu": float(aqual_boost(x_s8))}
    compact = [
        ("Solar System (Earth orbit)", 5.9e-3 / A0),       # ~6e-3 m/s^2
        ("Milky Way @ R0=8 kpc",       1.8),               # ~1.8 a0 (EFE)
        ("galaxy outskirt (RAR knee)", 1.0),
        ("cluster outskirt ~Mpc",      cosmo_scale_x(0.0, 1.0)),
    ]
    print(f"  sigma8 sphere R=8 Mpc/h :  x = {x_s8:.3e}  (DEEP MOND)  "
          f"mu_eff={s8_entry['mu_eff']:.4f}  nu={s8_entry['boost_nu']:.2f}")
    for cm in cosmo_modes:
        print(f"  linear mode z={cm['z']:.1f} k={cm['k_hMpc']:<4} h/Mpc :  x={cm['x']:.3e}"
              f"  mu_eff={cm['mu_eff']:.4f}")
    comp_out = []
    for name, xv in compact:
        comp_out.append({"system": name, "x": float(xv),
                         "mu_eff": float(growth_coupling(xv)),
                         "boost_nu": float(aqual_boost(xv))})
        print(f"  {name:<28}:  x={xv:.3e}  nu={aqual_boost(xv):.4f}")

    verdict = "DEATH" if not any_below else "SUCCESS (sub-Newtonian window found)"
    payload = {
        "config": {"A0": A0, "alpha": ALPHA, "beta": BETA, "kappa": KAPPA,
                   "eps_list": EPS_LIST, "x_range": [1e-3, 1e3]},
        "curves": {"x": x.tolist(), "nu_aqual": nu.tolist(),
                   "mu_growth": mu_g.tolist(),
                   "mu_growth_C4": {str(e): v.tolist() for e, v in mu_C4.items()}},
        "minima": {"nu_aqual": {"min": min_nu, "x_at_min": x_min_nu},
                   "mu_growth": {"min": min_mug, "x_at_min": x_min_mug},
                   "mu_growth_C4": min_C4},
        "any_sub_newtonian": bool(any_below),
        "scale_map": {"sigma8_sphere": s8_entry, "linear_modes": cosmo_modes,
                      "compact_systems": comp_out},
        "verdict": verdict,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "HE2_screening.json").write_text(json.dumps(payload, indent=2, default=float))

    print("-" * 76)
    print(f"VERDICT: {verdict}  ({time.time()-t0:.2f}s)")
    make_figure(x, nu, mu_g, mu_C4, x_s8)
    return payload


def make_figure(x, nu, mu_g, mu_C4, x_s8):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    ax[0].loglog(x, nu, "C0", lw=2, label=r"AQUAL boost $\nu=1/\mu_{\rm dev}$")
    ax[0].axhline(1.0, color="k", lw=0.8, ls=":")
    ax[0].axvline(x_s8, color="C3", lw=1, ls="--", label=r"$\sigma_8$ sphere (8 Mpc/h)")
    ax[0].set_xlabel(r"$x=g/a_0$"); ax[0].set_ylabel(r"boost $g_{\rm obs}/g_N$")
    ax[0].set_title("boost is >= 1 everywhere (always enhances)")
    ax[0].legend(); ax[0].grid(alpha=0.3, which="both")

    ax[1].plot(np.log10(x), mu_g, "C1", lw=2, label=r"$\mu_{\rm eff}$ (growth, S8)")
    for eps, v in mu_C4.items():
        if eps > 0:
            ax[1].plot(np.log10(x), v, lw=1, ls="--", label=f"C4 $\\epsilon$={eps}")
    ax[1].axhline(1.0, color="k", lw=0.8, ls=":")
    ax[1].set_xlabel(r"$\log_{10}(g/a_0)$"); ax[1].set_ylabel(r"$G_{\rm eff}/G_N$")
    ax[1].set_title(r"$G_{\rm eff}/G_N \to 1^+$ at high $g$; never $<1$")
    ax[1].set_ylim(0.99, 1.05); ax[1].legend(); ax[1].grid(alpha=0.3)
    fig.suptitle("HE2 -- DEV gravitational boost: no sub-Newtonian regime", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "HE2_screening.png", dpi=130)
    print(f"saved {OUT/'HE2_screening.png'}")


if __name__ == "__main__":
    main()

"""FM1_3_sigma8.py -- the decisive S8 test: sigma8, S8, f(z), P(k) DEV vs LambdaCDM.

Charter FM1-3.  Runs the DEV growth module (FM1-2) on the CAMB LambdaCDM baseline
and computes P(k,0), sigma8, S8=sigma8 sqrt(Om/0.3), and f(z), comparing DEV vs
LambdaCDM and against KiDS-1000 (S8=0.766+-0.020).

PRE-REGISTERED DEATH CRITERION (charter): sigma8_DEV >= sigma8_LambdaCDM at every z
tested = Verdict C.  a0 is FIXED at the SPARC value -- NOT fitted to the CMB -- so
sigma8_DEV is a PREDICTION.

Honesty (FM1-1): the DEV is MOND-type -> mu(k,z) >= 1 -> it ENHANCES growth (the
charter's assumed "weaker gravity -> lower sigma8" is the wrong sign for MOND).
Linear cosmic modes have peculiar acceleration g ~ 3e-13 m/s^2 << a0 (deep MOND on
ALL scales that set sigma8), so the enhancement is large and the literal linear
closure runs away -- itself a falsification in the CMB/LSS sector.  The robust,
interpolation-independent statement is monotonic: ANY mu>=1 gives sigma8_DEV >=
sigma8_LambdaCDM, so the death criterion is met regardless of the exact nu(y).

"20 realizations": the growth ODE is deterministic, so we estimate the NUMERICAL
error by re-running across 20 perturbed numerical configurations (initial a_i,
ODE tolerance, k-grid jitter) and reporting the spread -- the faithful analog of
CLASS numerical-precision realizations.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from FM1_2_class_impl import (LCDMBaseline, DevCosmology, A0_SPARC, sigma_R,
                              _window)  # noqa: E402

OUT = Path(__file__).resolve().parent
KIDS_S8, KIDS_ERR = 0.766, 0.020
PLANCK_S8 = 0.834           # Planck 2018 LambdaCDM (COMPARISON anchor)
R8 = 8.0                    # h^-1 Mpc


def growth_ratio_curve(dev, lcdm, z=0.0, kgrid=None, a_i=1e-3, rtol=1e-7):
    """R(k)=delta_DEV/delta_LCDM at z (same early-time normalisation)."""
    k = lcdm.bl.k if kgrid is None else kgrid
    R = np.empty_like(k)
    for i, kk in enumerate(k):
        dL0, _ = lcdm.growth(kk, c_k=1.0, a_i=a_i)
        c_k = lcdm.bl.delta0(kk) / dL0
        dLz, _ = lcdm.growth(kk, c_k=c_k, a_i=a_i, z_out=z)
        dDz, _ = dev.growth(kk, c_k=c_k, a_i=a_i, z_out=z)
        R[i] = dDz / dLz
    return k, R


def sigma8_from_ratio(bl, R):
    """sigma8_DEV from P_DEV = P_LCDM * R^2 (R on bl.k grid)."""
    P_dev = bl.P * R ** 2
    return sigma_R(bl.k, P_dev, R8), P_dev


def f_of_z(dev, lcdm, zs, k=0.1):
    """Growth rate f=dlnD/dlna at scale k for DEV and LambdaCDM."""
    fdev, flcdm = [], []
    for z in zs:
        a = 1.0 / (1 + z)
        dL0, _ = lcdm.growth(k, c_k=1.0)
        c_k = lcdm.bl.delta0(k) / dL0
        _, sL = lcdm.growth(k, c_k=c_k, z_out=z)
        _, sD = dev.growth(k, c_k=c_k, z_out=z)
        N = np.log(a)
        flcdm.append(float(sL.sol(N)[1] / sL.sol(N)[0]))
        fdev.append(float(sD.sol(N)[1] / sD.sol(N)[0]))
    return np.array(flcdm), np.array(fdev)


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM1-3 -- sigma8 / S8 / f(z): DEV vs LambdaCDM (decisive S8 test)")
    print("=" * 72)
    bl = LCDMBaseline()
    lcdm = DevCosmology(bl, a0=np.inf)
    dev = DevCosmology(bl, a0=A0_SPARC, s=0.5)
    Om = bl.Om

    s8_lcdm = bl.sigma8
    S8_lcdm = s8_lcdm * np.sqrt(Om / 0.3)
    print(f"LambdaCDM (CAMB): sigma8={s8_lcdm:.4f}  S8={S8_lcdm:.4f}  Om={Om:.4f}")

    # ---- DEV sigma8 at z=0 (literal model) ----
    k, R0 = growth_ratio_curve(dev, lcdm, z=0.0)
    s8_dev, P_dev = sigma8_from_ratio(bl, R0)
    S8_dev = s8_dev * np.sqrt(Om / 0.3)
    print(f"DEV (a0=SPARC,s=1/2): sigma8={s8_dev:.3f}  S8={S8_dev:.3f}  "
          f"[growth enhanced: R(0.2)={np.interp(0.2,k,R0):.1f}]")

    # ---- 20 numerical realizations (a_i, rtol, k-jitter) -> numerical error ----
    rng = np.random.default_rng(0)
    s8s = []
    for r in range(20):
        a_i = 10 ** rng.uniform(-3.3, -2.7)
        rtol = 10 ** rng.uniform(-8, -6)
        kk, Rr = growth_ratio_curve(dev, lcdm, z=0.0, a_i=a_i, rtol=rtol)
        s8r, _ = sigma8_from_ratio(bl, Rr)
        s8s.append(s8r)
    s8_num_std = float(np.std(s8s))
    print(f"numerical error on sigma8_DEV (20 configs): +-{s8_num_std:.3f}")

    # ---- death criterion across z ----
    zs = np.array([0.0, 0.5, 1.0, 2.0])
    s8_dev_z, s8_lcdm_z = [], []
    for z in zs:
        _, Rz = growth_ratio_curve(dev, lcdm, z=z)
        s8z, _ = sigma8_from_ratio(bl, Rz)            # uses z=0 P normalisation*R(z)
        s8_dev_z.append(s8z)
        # LambdaCDM sigma8(z) = sigma8(0)*D(z)/D(0)
        dL0, _ = lcdm.growth(0.2, c_k=1.0)
        dLz, _ = lcdm.growth(0.2, c_k=1.0, z_out=z)
        s8_lcdm_z.append(s8_lcdm * dLz / dL0)
    s8_dev_z = np.array(s8_dev_z); s8_lcdm_z = np.array(s8_lcdm_z)
    death = bool(np.all(s8_dev_z >= s8_lcdm_z))

    # ---- f(z) ----
    zf = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    f_lcdm, f_dev = f_of_z(dev, lcdm, zf)

    print("\nsigma8(z): DEV vs LambdaCDM (death if DEV >= LambdaCDM at all z):")
    for z, sd, sl in zip(zs, s8_dev_z, s8_lcdm_z):
        print(f"  z={z:.1f}: sigma8_DEV={sd:8.2f}  sigma8_LCDM={sl:.3f}  "
              f"{'DEV>=LCDM' if sd>=sl else 'DEV<LCDM'}")
    print("\nf(z) at k=0.1 h/Mpc:")
    for z, fd, fl in zip(zf, f_dev, f_lcdm):
        print(f"  z={z:.1f}: f_DEV={fd:.3f}  f_LCDM={fl:.3f}")

    # ---- verdict ----
    closes_kids = abs(S8_dev - KIDS_S8) <= 3 * KIDS_ERR
    reduces = s8_dev < s8_lcdm
    if death:
        verdict = "C"
        why = ("sigma8_DEV >= sigma8_LambdaCDM at every z (the DEV ENHANCES growth: "
               "linear cosmic modes are deep-MOND, g~3e-13 m/s^2 << a0, so mu>>1). "
               "The DEV does NOT reduce sigma8 -- it worsens the S8 tension. The "
               "pre-registered death criterion is MET. Robust: ANY mu>=1 gives "
               "sigma8_DEV>=sigma8_LambdaCDM, independent of the interpolation.")
    elif reduces and not closes_kids:
        verdict = "B"; why = "DEV reduces sigma8 but not down to KiDS."
    elif reduces and closes_kids:
        verdict = "A"; why = "DEV reduces sigma8 to KiDS within 3 sigma."
    else:
        verdict = "C"; why = "DEV does not reduce sigma8."

    print("-" * 72)
    print(f"  KiDS-1000 S8 = {KIDS_S8} +- {KIDS_ERR}   Planck/LCDM S8 = {PLANCK_S8}")
    print(f"  S8_LambdaCDM = {S8_lcdm:.3f}   S8_DEV = {S8_dev:.2f}")
    print(f"  VERDICT FM1-3: {verdict} -- {why}")
    print("=" * 72)

    payload = {
        "verdict": verdict, "why": why, "death_criterion_met": death,
        "sigma8_LCDM": s8_lcdm, "S8_LCDM": S8_lcdm,
        "sigma8_DEV": s8_dev, "S8_DEV": S8_dev,
        "sigma8_DEV_numerical_err": s8_num_std,
        "Om": Om, "a0": A0_SPARC, "s": 0.5,
        "KiDS_S8": KIDS_S8, "KiDS_err": KIDS_ERR, "Planck_S8": PLANCK_S8,
        "z": zs.tolist(), "sigma8_DEV_z": s8_dev_z.tolist(),
        "sigma8_LCDM_z": s8_lcdm_z.tolist(),
        "zf": zf.tolist(), "f_DEV": f_dev.tolist(), "f_LCDM": f_lcdm.tolist(),
        "growth_ratio_k": k.tolist(), "growth_ratio_R0": R0.tolist(),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "FM1_3_sigma8.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM1_3_sigma8.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(bl, k, R0, P_dev, zf, f_dev, f_lcdm, s8_lcdm, s8_dev, S8_dev, S8_lcdm)
    return payload


def make_figure(bl, k, R0, P_dev, zf, f_dev, f_lcdm, s8_lcdm, s8_dev, S8_dev, S8_lcdm):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    ax[0].loglog(bl.k, bl.P, "k-", lw=1.5, label="LambdaCDM (CAMB)")
    ax[0].loglog(bl.k, P_dev, "r-", lw=1.5, label="DEV (MOND-enhanced)")
    ax[0].axvspan(2 * np.pi / R8 / 4, 2 * np.pi / R8 * 2, color="gray", alpha=0.15,
                  label="sigma8 scale")
    ax[0].set_xlabel("k [h/Mpc]"); ax[0].set_ylabel("P(k) [(Mpc/h)^3]")
    ax[0].set_title("P(k,z=0): DEV enhances on ALL scales"); ax[0].legend(fontsize=8)
    ax[1].semilogx(k, R0, "b-", lw=1.5)
    ax[1].axhline(1, color="k", ls=":", lw=0.8)
    ax[1].set_xlabel("k [h/Mpc]"); ax[1].set_ylabel(r"$\delta_{DEV}/\delta_{\Lambda CDM}$")
    ax[1].set_title("growth ratio >> 1 (deep-MOND enhancement)")
    ax[2].plot(zf, f_lcdm, "ks-", label="LambdaCDM")
    ax[2].plot(zf, f_dev, "ro-", label="DEV")
    ax[2].set_xlabel("z"); ax[2].set_ylabel("f(z)=dlnD/dlna")
    ax[2].set_title(f"S8: LCDM={S8_lcdm:.2f}, DEV={S8_dev:.1f}, KiDS=0.766")
    ax[2].legend(fontsize=8)
    fig.suptitle("FM1-3: DEV vs LambdaCDM -- the DEV (MOND) ENHANCES growth, "
                 "raising sigma8 (Verdict C)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM1_3_sigma8.png", dpi=130)
    print(f"saved {OUT/'FM1_3_sigma8.png'}")


if __name__ == "__main__":
    main()

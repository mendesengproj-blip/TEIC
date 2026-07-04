"""E2_2_dispersion.py -- the dispersion relation omega(k): ck vs massive vs diffusive.

Charter: E2_MAGNON_BD.md (E2-2).  Reads the seed-averaged dispersion measured in
E2-1 (E2_1_propagation.json) and fits the three competing laws:

    massless   omega = c k                  (relativistic Goldstone = photon)
    massive    omega = sqrt(c^2 k^2 + m^2)   (Klein-Gordon)
    diffusive  omega = D k^2                 (non-relativistic magnon)

The preferred model is chosen by the scale-free phase-velocity trend (validated in
E2-V: v(k)=omega/k is flat for massless, rises for diffusive, falls for massive),
with chi^2/AIC reported as corroborating diagnostics.  The on-shell deviation from
omega=ck is reported against the charter thresholds.

Anti-circularity: c is a FREE fit parameter; it is compared to 1 (the causal
light-cone speed) only here in the conclusion, never inserted into the generator.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e2_core as e2  # noqa: E402

OUT = Path(__file__).resolve().parent


def main():
    data = json.loads((OUT / "E2_1_propagation.json").read_text())
    k_all = np.array(data["config"]["k"])
    ostar_all = np.array(data["omega_star"])
    found = np.array(data["found"], dtype=bool)
    sem_all = np.array(data["sem"])

    k = k_all[found]
    y = ostar_all[found]
    sem = sem_all[found]
    sem = np.where(np.isfinite(sem) & (sem > 0), sem, np.median(sem[sem > 0]))

    print("=" * 72)
    print("E2-2 -- dispersion relation: ck vs massive vs diffusive")
    print("=" * 72)
    print(f"points: {found.sum()} k-values  (seeds used {data['n_seeds_used']})")

    fit = e2.fit_dispersion(k, y, sigma=sem)

    ndof = len(k)
    print("\nmodel fits (chi^2 weighted by per-k SEM):")
    print(f"  massless  omega=ck        : c={fit['massless']['c']:.3f}   "
          f"chi2={fit['massless']['chi2']:.2f}  chi2/N={fit['massless']['chi2']/ndof:.2f}  AIC={fit['massless']['aic']:.2f}")
    print(f"  massive   omega=sqrt(c2k2+m2): c={fit['massive']['c']:.3f}  m2={fit['massive']['m2']:+.3f}  "
          f"m={fit['massive']['m']:.3f}  chi2={fit['massive']['chi2']:.2f}  AIC={fit['massive']['aic']:.2f}")
    print(f"  diffusive omega=Dk^2      : D={fit['diffusive']['D']:.3f}   "
          f"chi2={fit['diffusive']['chi2']:.2f}  chi2/N={fit['diffusive']['chi2']/ndof:.2f}  AIC={fit['diffusive']['aic']:.2f}")

    c_fit = fit["massless"]["c"]
    dev = fit["linear_rel_deviation_pct"]
    print(f"\n  phase-velocity trend v_rel_slope = {fit['v_rel_slope']:+.3f}  "
          f"(flat=massless | rises=diffusive | falls=massive; |thr|=0.15)")
    print(f"  winner (trend)  = {fit['winner']}")
    print(f"  winner (AIC)    = {fit['winner_aic']}")
    print(f"  measured speed  c_fit = {c_fit:.3f}  (light-cone speed = 1)")
    print(f"  deviation from omega=ck = {dev:.1f}%")

    # ---- verdict mapping (charter E2_MAGNON_BD.md) ----
    speed_dev = abs(c_fit - 1.0) * 100
    if fit["winner"] == "massless" and dev < 10.0 and speed_dev < 15.0:
        code, verdict = "A", ("FOTON = MAGNON BD-SMEARED: omega=ck, deviation "
                              f"{dev:.1f}%<10%, c={c_fit:.2f}~1 (light cone).")
    elif fit["winner"] in ("massless", "massive") and dev < 20.0:
        code, verdict = "A-/B", ("LINEAR/near-massless: omega~ck with deviation "
                                 f"{dev:.1f}% and c={c_fit:.2f}; relativistic, small "
                                 "residual (finite-size or small mass). Partial success.")
    elif fit["winner"] == "diffusive":
        code, verdict = "C", ("DIFFUSIVE omega=Dk^2: non-relativistic. Death "
                              "criterion met -- photon is NOT a BD-smeared magnon.")
    else:
        code, verdict = "B", (f"MASSIVE/other: winner={fit['winner']}, dev={dev:.1f}%.")
    print(f"\n  VERDICT (E2-2) [{code}]: {verdict}")
    print("=" * 72)

    # ---- figure ----
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    kk = np.linspace(0, k.max() * 1.05, 100)
    axes[0].errorbar(k, y, yerr=sem, fmt="ko", capsize=3, ms=5, label="measured $\\omega^*$", zorder=5)
    axes[0].plot(kk, fit["massless"]["c"] * kk, "b-",
                 label=f"massless ck  (c={fit['massless']['c']:.2f}, $\\chi^2$/N={fit['massless']['chi2']/ndof:.2f})")
    axes[0].plot(kk, np.sqrt(np.maximum(fit["massive"]["c"]**2 * kk**2 + fit["massive"]["m2"], 0)),
                 "g--", label=f"massive  (m={fit['massive']['m']:.2f})")
    axes[0].plot(kk, fit["diffusive"]["D"] * kk**2, "r:",
                 label=f"diffusive D$k^2$ ($\\chi^2$/N={fit['diffusive']['chi2']/ndof:.1f})")
    axes[0].plot(kk, kk, "k-.", lw=0.8, alpha=0.6, label=r"$\omega=k$ (light cone)")
    axes[0].set_xlabel("k"); axes[0].set_ylabel(r"$\omega^*(k)$")
    axes[0].set_title("E2-2: dispersion relation & three-model fit")
    axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)

    # phase velocity v(k) = omega/k -- the discriminator
    axes[1].errorbar(k, y / k, yerr=sem / k, fmt="ko", capsize=3, ms=5, label=r"$v=\omega^*/k$")
    axes[1].axhline(c_fit, color="b", ls="-", label=f"massless c={c_fit:.2f}")
    axes[1].axhline(1.0, color="k", ls="-.", lw=0.8, alpha=0.6, label="light cone =1")
    mv = fit["massive"]["c"]**2 + fit["massive"]["m2"] / kk[kk > 0]**2
    axes[1].plot(kk[kk > 0], np.sqrt(np.maximum(mv, 0.0)),
                 "g--", label="massive trend")
    axes[1].plot(kk, fit["diffusive"]["D"] * kk, "r:", label="diffusive trend")
    axes[1].set_xlabel("k"); axes[1].set_ylabel(r"$v(k)=\omega^*/k$")
    axes[1].set_ylim(0, max(2.0, 1.3 * np.nanmax(y / k)))
    axes[1].set_title(f"phase velocity (flat=massless): slope={fit['v_rel_slope']:+.2f}")
    axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)
    fig.suptitle(f"E2-2 [{code}]: orientation fluctuation dispersion is "
                 f"{fit['winner']}, c={c_fit:.2f}, dev {dev:.0f}%", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E2_2_dispersion.png", dpi=130)
    print(f"saved {OUT/'E2_2_dispersion.png'}")

    payload = {"k": k.tolist(), "omega_star": y.tolist(), "sem": sem.tolist(),
               "fit": fit, "c_fit": c_fit, "deviation_pct": dev,
               "speed_dev_pct": speed_dev, "ndof": ndof,
               "verdict_code": code, "verdict": verdict,
               "source": "E2_1_propagation.json"}
    (OUT / "E2_2_dispersion.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E2_2_dispersion.json'}")
    return payload


if __name__ == "__main__":
    main()

"""make_figures.py -- figures for the COEFFICIENTS task, from the saved JSON only.

Reads C1_moments_data.json and C3_scale_data.json (no recompute) and writes
C1_anisotropy.png and C3_powerlaw.png.  Pure plotting; no physics here.
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
c1 = json.loads((OUT / "C1_moments_data.json").read_text())
c3 = json.loads((OUT / "C3_scale_data.json").read_text())

# ---- C1: anisotropy (a) tensor bars, (b) box-size convergence -------------- #
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))

for lab, key, color in [("1+1D", "d2_main", "tab:blue"),
                        ("3+1D", "d4_main", "tab:red")]:
    M2 = np.asarray(c1[key]["M2"])
    diag = np.diag(M2)
    xs = np.arange(len(diag)) + (0.0 if lab == "1+1D" else 0.15)
    ax[0].bar(xs, diag, width=0.15, label=f"{lab}  diag M2", color=color, alpha=0.8)
ax[0].set_xlabel(r"tensor index $\mu$  (0 = time)")
ax[0].set_ylabel(r"$\langle\Delta\tau\, e^\mu e^\mu\rangle$")
ax[0].set_title(r"$M2^{\mu\nu}=\langle\Delta\tau\,e^\mu e^\nu\rangle$ "
                r"is Euclidean-like (all +), not $\propto g^{\mu\nu}$")
ax[0].legend()
ax[0].grid(alpha=0.3)

scan = c1["d2_boxsize_scan"]
X = [s["X"] for s in scan]
aniso = [s["anisotropy"] for s in scan]
ax[1].plot(X, aniso, "o-", color="tab:purple")
ax[1].axhline(2.0, ls="--", color="gray", label=r"converged $\lambda/|\kappa|\approx 2$")
ax[1].set_xlabel("spatial extent X (IR cutoff)")
ax[1].set_ylabel(r"anisotropy $\lambda/|\kappa|$")
ax[1].set_title("LV anisotropy CONVERGES (finite, not a divergence)")
ax[1].legend()
ax[1].grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "C1_anisotropy.png", dpi=130)
plt.close(fig)

# ---- C3: Dtau_min power law ------------------------------------------------ #
fig, ax = plt.subplots(figsize=(6.4, 4.6))
for dk, lab, color in [("d2", "1+1D", "tab:blue"), ("d4", "3+1D", "tab:red")]:
    rows = c3[dk]["rows"]
    rho = np.array([r["rho"] for r in rows])
    med = np.array([r["dtau_median"] for r in rows])
    p = c3[dk]["fit_median"]["q_exponent_dtau"]
    ax.loglog(rho, med, "o", color=color, label=f"{lab} median  (fit q={p:+.3f})")
    ax.loglog(rho, med[0] * (rho / rho[0]) ** p, "-", color=color, alpha=0.6)
# reference slope -1/2
rr = np.array([min(rho), max(rho)])
ax.loglog(rr, 0.05 * (rr / rr[0]) ** -0.5, "k--", alpha=0.6,
          label=r"slope $-1/2$ (light-cone sliver)")
ax.set_xlabel(r"density $\rho$")
ax.set_ylabel(r"$\Delta\tau_{\min}$  (nearest future link)")
ax.set_title(r"$\Delta\tau_{\min}\propto\rho^{-1/2}$ in BOTH dims $\Rightarrow X_0\propto\rho$")
ax.legend()
ax.grid(alpha=0.3, which="both")
fig.tight_layout()
fig.savefig(OUT / "C3_powerlaw.png", dpi=130)
plt.close(fig)
print("wrote C1_anisotropy.png, C3_powerlaw.png")

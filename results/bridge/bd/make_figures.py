"""make_figures.py -- BRIDGE/BD figures from saved JSON only (no recompute)."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
bd1 = json.loads((OUT / "BD1_diagnosis_data.json").read_text())
sa = json.loads((OUT / "bd_summed_action_data.json").read_text())

fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))

# (left) sharp (Euclidean, anisotropic) vs smeared (collapsed, ~0) second moment
sharp = bd1["sharp_second_moment"]
m = sa["main"]["second_moment_smeared"]
labels = ["a_t (sharp)", "a_x (sharp)", "a_t (BD)", "a_x (BD)"]
vals = [sharp["a_t"], sharp["a_x"], m["a_t"], m["a_x"]]
errs = [0, 0, m["a_t_sem"], m["a_x_sem"]]
colors = ["tab:red", "tab:orange", "tab:blue", "tab:cyan"]
ax[0].bar(range(4), vals, yerr=errs, color=colors, capsize=4)
ax[0].set_yscale("symlog")
ax[0].axhline(0, color="k", lw=0.8)
ax[0].set_xticks(range(4)); ax[0].set_xticklabels(labels, rotation=15)
ax[0].set_ylabel("second-moment component (symlog)")
ax[0].set_title("BD smearing collapses the O(1e4) sharp anisotropy\n"
                "(ratio 4) to O(0.1) consistent with 0 -- but not to g")
ax[0].grid(alpha=0.3, axis="y")

# (right) eps scan: lambda_space, lambda_time vs eps with error bars (Lorentz: s>0,t<0)
scan = sa["eps_scan"]
eps = [s["eps"] for s in scan]
ls = [s["lambda_space"] for s in scan]; lse = [s["lambda_space_sem"] for s in scan]
lt = [s["lambda_time"] for s in scan]; lte = [s["lambda_time_sem"] for s in scan]
ax[1].errorbar(eps, ls, yerr=lse, fmt="o-", capsize=4, label=r"$\lambda_{\rm space}$ (want >0)")
ax[1].errorbar(eps, lt, yerr=lte, fmt="s-", capsize=4, label=r"$\lambda_{\rm time}$ (want <0)")
ax[1].axhline(0, color="k", lw=0.8)
ax[1].set_xlabel(r"smearing retention $\epsilon$")
ax[1].set_ylabel(r"dispersion $\lambda$ (k=0.6)")
ax[1].set_title("No magic $\\epsilon_0$: signal ~ 0 at all $\\epsilon$,\n"
                "error grows with $\\epsilon$ (SNR ~ 1 throughout)")
ax[1].legend(); ax[1].grid(alpha=0.3)

fig.tight_layout()
fig.savefig(OUT / "BD_sharp_vs_smeared.png", dpi=130)
plt.close(fig)
print("wrote BD_sharp_vs_smeared.png")

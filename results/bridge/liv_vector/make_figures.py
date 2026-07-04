"""make_figures.py -- LIV_VECTOR campaign figure (2 panels).

Left:  cumulative E/B(eta_cut) for all box extents (LV3) -- curve collapse =
       one LI orbit, only the truncation endpoint moves.
Right: boost defect of the summed action vs field strength (LV4): measured
       R(beta) against the quadratic LV prediction; collapse to 1.
"""
from __future__ import annotations

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
lv3 = json.loads((OUT / "LV3_cutoff_data.json").read_text())
lv4 = json.loads((OUT / "LV4_global_action_data.json").read_text())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

# panel 1: cumulative E/B(eta_cut), rho=12 extents
for s in lv3["scans"]:
    if s["rho"] != 12.0:
        continue
    eta = np.array(s["curve_eta"])
    eb = np.array([np.nan if v is None else v for v in s["curve_EB"]], float)
    ax1.plot(eta, eb, "o-", ms=3, label=f"L={s['extent']:.0f}  (E/B={s['EB_total']:.2f})")
ax1.axhline(1.0, color="k", lw=0.8, ls="--")
ax1.axhline(3.0, color="gray", lw=0.8, ls=":")
ax1.text(0.12, 3.1, "W2 value", fontsize=8, color="gray")
ax1.set_yscale("log")
ax1.set_xlabel(r"rapidity cut $\eta_{\rm cut}$")
ax1.set_ylabel(r"cumulative  $E/B(\eta\leq\eta_{\rm cut})$")
ax1.set_title("one LI orbit, truncated by the box (LV3)")
ax1.legend(fontsize=8)

# panel 2: R(beta) vs E0 (LV4)
eb = lv4["config"]["EB_quadratic"]
betas = [x["beta"] for x in lv4["blocks"][0]["betas"]]
colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(lv4["blocks"])))
for b, c in zip(lv4["blocks"], colors):
    r = [x["R_mean"] for x in b["betas"]]
    e = [x["R_sem"] for x in b["betas"]]
    ax2.errorbar(betas, r, yerr=e, fmt="o-", ms=3, color=c,
                 label=rf"$E_0={b['E0_factor']}\,u_0$")
bq = np.linspace(0, 1.7, 100)
ax2.plot(bq, np.cosh(bq) ** 2 + np.sinh(bq) ** 2 / eb, "r--", lw=1.2,
         label=rf"quadratic LV ($E/B={eb:.1f}$)")
ax2.axhline(1.0, color="k", lw=0.8, ls="--")
ax2.set_yscale("log")
ax2.set_xlabel(r"probe-field boost rapidity $\beta$  (invariants fixed)")
ax2.set_ylabel(r"$R=\langle S(\beta)\rangle/\langle S(0)\rangle$")
ax2.set_title("summed action: LV resums away (LV4)")
ax2.legend(fontsize=7, ncol=2)

fig.suptitle("LIV_VECTOR: the E/B$\\approx$3 violation is the box-truncated "
             "quadratic expansion of an LI action", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(OUT / "LIV_restoration.png", dpi=150)
print("wrote", OUT / "LIV_restoration.png")

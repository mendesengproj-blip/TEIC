"""make_figures.py -- figures for BRIDGE/WILSON, from saved JSON only (no recompute)."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
w1 = json.loads((OUT / "W1_holonomy_data.json").read_text())
w3 = json.loads((OUT / "W3_strong_field_data.json").read_text())

# ---- W1: Stokes convergence + sprinkled scatter --------------------------- #
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
rows = w1["d2_varying_F"]["rows"]
h = np.array([r["h"] for r in rows]); err = np.array([r["rel_err_vs_F"] for r in rows])
ax[0].loglog(h, err, "o-", label="varying F (W/area)")
ax[0].loglog(h, err[0] * (h / h[0]) ** 2, "k--", alpha=0.6, label=r"slope 2 ($O(\mathrm{area})$)")
ax[0].set_xlabel("loop half-size h"); ax[0].set_ylabel(r"$|W/\mathrm{area}-F|/|F|$")
ax[0].set_title("W1: holonomy $\\to F$ (Stokes), $O(\\mathrm{area})$"); ax[0].legend(); ax[0].grid(alpha=0.3, which="both")

sd = w1["sprinkled_diamonds"]
Wd = np.array(sd["W"]); Wp = np.array(sd["Wpred"])
ax[1].plot(Wp, Wd, ".", alpha=0.3, ms=4)
lim = [min(Wp.min(), Wd.min()), max(Wp.max(), Wd.max())]
ax[1].plot(lim, lim, "k--", alpha=0.7, label="W = ½F:Ω")
ax[1].set_xlabel(r"$\frac{1}{2} F_{\mu\nu}\Omega^{\mu\nu}$ (Stokes)"); ax[1].set_ylabel("W (sum of link phases)")
ax[1].set_title(f"W1: real causal diamonds (const F)\ncorr={sd['corr_W_vs_stokes']:.4f}, slope={sd['slope_W_on_Wpred']:.3f}")
ax[1].legend(); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "W1_holonomy.png", dpi=130); plt.close(fig)

# ---- W3: DBI saturation + gauge hierarchy --------------------------------- #
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
sc = w3["scalar_channel"]["rows"]
amp = np.array([r["amp"] for r in sc])
ax[0].semilogx(amp, [r["S_over_quad"] for r in sc], "o-", label=r"$S_{\rm link}/S_{\rm quad}$ (DBI)")
ax[0].semilogx(amp, [r["saturation_frac"] for r in sc], "s-", label="saturation fraction")
ax[0].set_xlabel("scalar amplitude $\\Theta$"); ax[0].set_ylabel("ratio")
ax[0].set_title("W3 scalar channel: quartic $\\to$ DBI saturation"); ax[0].legend(); ax[0].grid(alpha=0.3)

g = w3["gauge_channel_lp1"]["rows"]
amp = np.array([r["amp"] for r in g])
ax[1].loglog(amp, [r["S_link_phi"] for r in g], "o-", label=r"$S_{\rm link}(\phi)$")
ax[1].loglog(amp, [r["S_plaq"] for r in g], "s-", label=r"$S_{\rm plaq}(W)\;(\lambda_p=1)$")
ax[1].loglog(amp, [r["S_plaq_quadratic"] for r in g], ":", label=r"$S_{\rm plaq}$ quad ($F^2$)")
ax[1].set_xlabel("gauge amplitude"); ax[1].set_ylabel("action")
ax[1].set_title("W3 gauge channel: both saturate, no explosion"); ax[1].legend(); ax[1].grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig(OUT / "W3_strong_field.png", dpi=130); plt.close(fig)
print("wrote W1_holonomy.png, W3_strong_field.png")

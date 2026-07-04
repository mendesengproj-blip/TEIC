"""Figure for CAMPANHA_SU3_ORDEM_TRANSICAO from OT_transition_order.json (saved data)."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / "OT_transition_order.json").read_text(encoding="utf-8"))
Js = np.array(d["Jgrid"])
Ls = sorted(int(k) for k in d["scans"])
cmap = plt.cm.viridis(np.linspace(0, 0.9, len(Ls)))

fig, ax = plt.subplots(2, 2, figsize=(12, 9))

# (a) chi_max vs L (log-log) + volume-law and 2nd-order references
cm = np.array([d["scans"][str(L)]["chi_max"] for L in Ls])
La = np.array(Ls, float)
x = float(np.polyfit(np.log(La), np.log(cm), 1)[0])
ax[0, 0].loglog(La, cm, "o-", color="crimson", label=f"data  (x≈{x:.2f})")
ax[0, 0].loglog(La, cm[0] * (La / La[0]) ** 3, "k--", lw=1, label="volume law L³ (1st order)")
ax[0, 0].loglog(La, cm[0] * (La / La[0]) ** 1.97, "b:", lw=1, label="γ/ν≈1.97 (2nd order)")
ax[0, 0].set_xlabel("L"); ax[0, 0].set_ylabel(r"$\chi_{max}$")
ax[0, 0].set_title("(a) χ_max scaling — super-volume (pre-asymptotic)")
ax[0, 0].legend(fontsize=8)

# (b) U4(J) curves
for c, L in zip(cmap, Ls):
    u = [d["scans"][str(L)]["perJ"][f"{J:.4f}"]["U4"] for J in Js]
    ax[0, 1].plot(Js, u, "o-", ms=3, color=c, label=f"L={L}")
ax[0, 1].axhline(2 / 3, color="grey", ls=":", lw=1, label="2/3 (ordered)")
ax[0, 1].set_xlabel("J"); ax[0, 1].set_ylabel(r"$U_4$")
ax[0, 1].set_title("(b) Binder cumulant — crossings wander, dip deepens")
ax[0, 1].legend(fontsize=8)

# (c) J_pk drift and U4@pk vs L
jp = [d["scans"][str(L)]["J_chi_max"] for L in Ls]
u4pk = [d["scans"][str(L)]["perJ"][f"{d['scans'][str(L)]['J_chi_max']:.4f}"]["U4"] for L in Ls]
axc = ax[1, 0]; axc2 = axc.twinx()
axc.plot(Ls, jp, "s-", color="darkgreen", label="J_pk (χ peak)")
axc2.plot(Ls, u4pk, "^-", color="purple", label="U4 at peak")
axc.set_xlabel("L"); axc.set_ylabel("J_pk", color="darkgreen")
axc2.set_ylabel("U4 at peak", color="purple")
axc.set_title("(c) J_pk converging (drift→0.01); U4 dip deepening")

# (d) latent-heat bimodality + hysteresis vs L
hl = sorted(d["histograms"], key=int)
bm = [d["histograms"][k]["bimodality_coeff"] for k in hl]
axd = ax[1, 1]
axd.plot([int(k) for k in hl], bm, "o-", color="teal", label="bimodality coeff")
axd.axhline(0.555, color="red", ls="--", lw=1, label="0.555 (bimodal threshold)")
hk = sorted(d.get("hysteresis", {}), key=int)
if hk:
    hy = [d["hysteresis"][k]["norm_hysteresis"] for k in hk]
    axd.plot([int(k) for k in hk], hy, "s-", color="orange", label="hysteresis (norm)")
    axd.axhline(0.15, color="orange", ls=":", lw=1, label="0.15 (1st-order)")
axd.set_xlabel("L"); axd.set_ylabel("value")
axd.set_title("(d) latent heat ABSENT (flat<0.555); hysteresis>0.15 (confounded)")
axd.legend(fontsize=8)

fig.suptitle("SU(3) colour-ferromagnet transition order (L=8–24): weak/pseudo-first-order",
             fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.97])
out = HERE / "OT_transition_order.png"
fig.savefig(out, dpi=110)
print("saved", out.name)

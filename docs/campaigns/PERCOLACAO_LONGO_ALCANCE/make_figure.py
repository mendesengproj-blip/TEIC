"""
make_figure.py -- dois graficos sobrepostos do gatilho: <z>(sigma) e C4(sigma),
no N comum a todos os sigma (N=1500), com barras de erro e referencias de Poisson
(extremo denso sigma->0) e do controle aleatorio / CSG nos extremos.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
meas = json.load(open(os.path.join(HERE, "longrange.json")))
ctrl = json.load(open(os.path.join(HERE, "control_c4.json")))

COMMON_N = 1500   # N medido para TODOS os sigma -> comparacao justa em sigma

# referencias das campanhas anteriores (mesmo estimador/linhagem)
CSG_C4 = 0.0190        # plato intermediate do CSG (RS-CLUSTERING)
POISSON_C4 = 0.0291    # controle mean-field de Poisson (RS-CLUSTERING)


def at_common_N(R):
    for r in R["rows"]:
        if r["N_target"] == COMMON_N:
            return r
    return R["rows"][-1]


sig = []
z, zerr, c4, c4err = [], [], [], []
for key, R in meas["by_sigma"].items():
    r = at_common_N(R)
    sig.append(R["sigma"])
    z.append(r["z_mean"]); zerr.append(r["z_sem"])
    c4.append(r["C4"]); c4err.append(r["C4_sem"])
sig = np.array(sig); order = np.argsort(sig)
sig = sig[order]
z = np.array(z)[order]; zerr = np.array(zerr)[order]
c4 = np.array(c4)[order]; c4err = np.array(c4err)[order]

# comparacao MESMO-N (familia vs controle medidos no MESMO top-N por sigma)
csig = np.array([r["sigma"] for r in ctrl["rows"]])
cc4 = np.array([r["C4_random_control"] for r in ctrl["rows"]])
cfam = np.array([r["C4_family"] for r in ctrl["rows"]])
co = np.argsort(csig); csig = csig[co]; cc4 = cc4[co]; cfam = cfam[co]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# ---- painel 1: <z>(sigma) ----
ax1.errorbar(sig, z, yerr=zerr, marker="o", color="C3", capsize=3, lw=1.8,
             label=fr"$\langle z\rangle(\sigma)$ familia, N={COMMON_N}")
ax1.axvline(meas["dim"], ls=":", color="gray",
            label=fr"$\sigma=d={meas['dim']}$ (transicao plana esperada)")
ax1.annotate("denso / Poisson-causal\n($\\sigma\\to0$: todos os pares)",
             xy=(sig[0], z[0]), xytext=(0.7, z.max() * 0.92),
             fontsize=8, color="C3")
ax1.annotate("esparso / CSG-like\n($\\sigma$ grande)", xy=(sig[-1], z[-1]),
             xytext=(5.0, z.min() * 1.4), fontsize=8, color="dimgray")
ax1.set_xlabel(r"$\sigma$ (expoente de decaimento de $p(\Delta\tau)$)")
ax1.set_ylabel(r"$\langle z\rangle$")
ax1.set_title(r"Coordenacao $\langle z\rangle(\sigma)$ — diverge com N em TODO $\sigma$"
              "\n(expoente local rel. >= 0.38, nunca satura)")
ax1.legend(fontsize=8, loc="upper right")
ax1.grid(alpha=0.3)

# ---- painel 2: C4(sigma) familia vs controle, MESMO N por sigma ----
ax2.plot(csig, cfam, marker="s", color="C0", lw=1.8,
         label=r"$C_4(\sigma)$ familia (top-N por $\sigma$)")
ax2.plot(csig, cc4, marker="x", ls="--", color="k",
         label=r"controle aleatorio, MESMO N (mesma densidade)")
ax2.axhline(POISSON_C4, ls=":", color="C2", label=r"Poisson MF $C_4\approx0.029$ (RS)")
ax2.axhline(CSG_C4, ls=":", color="C1", label=r"CSG intermediate $C_4\approx0.019$ (RS)")
ax2.axvline(meas["dim"], ls=":", color="gray")
ax2.set_xlabel(r"$\sigma$")
ax2.set_ylabel(r"$C_4$ (square clustering, normalizado)")
ax2.set_title(r"Clustering $C_4(\sigma)$ — ABAIXO do controle aleatorio em todo $\sigma$"
              "\n(familia suprime lacos; nao os cria)")
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(alpha=0.3)

fig.suptitle("Percolacao de longo alcance sobre a ordem causal — VEREDITO: SEM JANELA "
             "(z diverge sempre; C4 < controle sempre)", fontsize=11, y=1.02)
fig.tight_layout()
out = os.path.join(HERE, "longrange.png")
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"figura salva: {out}")

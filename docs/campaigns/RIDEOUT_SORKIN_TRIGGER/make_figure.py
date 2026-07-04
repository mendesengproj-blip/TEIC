"""Figura do gatilho: <z>(N) do CSG (>=3 regimes) sobreposto ao Poisson da ESCALA_XI.
Pergunta binaria e visual: o CSG satura enquanto o Poisson diverge?"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# Poisson baseline (3+1)D, lido de ESCALA_XI/campaign_full.json (mesmo estimador)
POISSON_N = [501.8, 1047.2, 1947.2, 3329.8]
POISSON_Z = [33.44, 52.13, 75.70, 103.02]

meas = json.load(open(os.path.join(HERE, "rs_trigger.json")))

fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

colors = {"sparse_fixed": "#1f77b4", "intermediate_fixed": "#2ca02c",
          "dense_fixed": "#d62728", "manifold_scaled": "#9467bd"}
labels = {"sparse_fixed": "CSG sparse (p=0.02)",
          "intermediate_fixed": "CSG intermediate (p=0.10)",
          "dense_fixed": "CSG dense (p=0.40)",
          "manifold_scaled": "CSG manifold-scaled (p=4/N)"}

for ax, logx in zip(axes, [False, True]):
    # Poisson
    ax.plot(POISSON_N, POISSON_Z, "o-", color="black", lw=2.4, ms=8,
            label="Poisson sprinkle 3+1D (ESCALA_XI)", zorder=5)
    for label, R in meas["regimes"].items():
        rows = R["rows"]
        N = [r["N"] for r in rows]
        z = [r["z_mean"] for r in rows]
        zerr = [r["z_sem"] for r in rows]
        ax.errorbar(N, z, yerr=zerr, fmt="s--", color=colors[label],
                    lw=1.8, ms=6, capsize=3, label=labels[label])
    ax.set_xlabel("N (número de eventos)")
    ax.set_ylabel(r"$\langle z \rangle$  =  coordenação média do grafo de Hasse")
    if logx:
        ax.set_xscale("log")
        ax.set_title("escala log-N (inclinação = " + r"$d\langle z\rangle/d\ln N$)")
    else:
        ax.set_title("escala linear")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")

fig.suptitle("GATILHO Rideout–Sorkin: CSG satura enquanto Poisson diverge  →  GATILHO ARMADO",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
out = os.path.join(HERE, "rs_trigger.png")
fig.savefig(out, dpi=130)
print("saved", out)

# tabela resumo
print("\nresumo z(N):")
print(f"{'regime':>20} | " + " | ".join(f"N={r['N']}" for r in meas["regimes"]["dense_fixed"]["rows"]))
for label, R in meas["regimes"].items():
    zs = " | ".join(f"{r['z_mean']:6.2f}" for r in R["rows"])
    print(f"{label:>20} | {zs}  | slope_top={R['local_exp_top']:+.2f}")
print(f"{'Poisson (XI)':>20} | " + " | ".join(f"{z:6.2f}" for z in POISSON_Z)
      + "  (+ N=3888 n/a) | slope~+37")

"""make_figure.py -- overlay CDT 3D vs Poisson (ESCALA_XI) vs CSG (kinematico).

Painel 1: chi_max(N) -- CDT (k0=1,3) vs Poisson baseline (plano = MF). Pergunta B.
Painel 2: U4(J) por tamanho (cruzamento = criticalidade) p/ CDT.
Painel 3: C4 (laços) cinematico -- CDT vs Poisson vs CSG vs rede 2D (a fila de substratos).
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
TEIC = HERE.parents[2]


def poisson_chimax():
    d = json.load(open(TEIC / "docs/campaigns/ESCALA_XI/campaign_full.json"))
    res = d["results"]["baseline_3p1"]
    Ns, cm = [], []
    for sz in res["sizes"]:
        chis = [row.get("chi", np.nan) for row in sz["rows"]]
        Ns.append(sz["N_mean"]); cm.append(np.nanmax(chis))
    return np.array(Ns), np.array(cm)


def main():
    out = json.load(open(HERE / "ferro_cdt.json"))
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))

    # ---- Painel 1: chi_max(N) ----
    for k0, col in (("1.0", "tab:blue"), ("3.0", "tab:red")):
        B = out["B"][k0]
        per = B["per_size"]
        Ns = np.array([per[v]["N0"] for v in per])
        cm = np.array([per[v]["chi_max"] for v in per])
        order = np.argsort(Ns)
        ax[0].plot(Ns[order], cm[order], "o-", color=col,
                   label=f"CDT 3D k0={k0} (N^{B['chi_max_exponent']:.2f})")
    pN, pcm = poisson_chimax()
    ax[0].plot(pN, pcm, "s--", color="gray", label="Poisson (ESCALA_XI, MF~plano)")
    # guia geometrico N^0.66
    xg = np.array([200, 2000.0])
    ax[0].plot(xg, 0.02 * xg ** 0.66, ":", color="green", label="guia N^0.66 (3D-geom)")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel("N (nos)"); ax[0].set_ylabel("chi_max")
    ax[0].set_title("B: chi_max(N) -- cresce (critico) vs plano (MF)")
    ax[0].legend(fontsize=7)

    # ---- Painel 2: U4(J) cruzamento (k0=1) ----
    for k0, axi in (("1.0", ax[1]), ("3.0", ax[2])):
        B = out["B"][k0]
        per = B["per_size"]
        Js = np.array(B["Js"])
        for v in sorted(per, key=lambda x: per[x]["N0"]):
            U4 = [row["U4"] for row in per[v]["scan"]]
            axi.plot(Js, U4, "o-", label=f"N~{per[v]['N0']:.0f}")
        axi.axhline(0.667, ls=":", color="gray", lw=0.8)
        axi.set_xlabel("J"); axi.set_ylabel("U4")
        axi.set_title(f"B: U4(J) cruzamento? k0={k0}")
        axi.legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(HERE / "ferro_cdt.png", dpi=130)
    print(f"-> {HERE/'ferro_cdt.png'}")


if __name__ == "__main__":
    main()

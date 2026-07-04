"""Figure for GATILHO 3: clustering C4 vs N -- tipo-CDT (stacked + flipped) overlaid
on the queue references (Poisson mean-field control; CSG tree-like; 2D-lattice target)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "cdt_kinematics.json")))

# reference curves from the queue (Gatilho 2 results)
CSG_INT = [(500, 0.0200), (1000, 0.0195), (2000, 0.0197), (3300, 0.0192), (3888, 0.0190)]
POISSON = [(500, 0.0545), (1000, 0.0401), (2000, 0.0291)]

fig, ax = plt.subplots(figsize=(7.8, 5.4))
colors = {"stacked": "#9467bd", "flipped": "#8c564b"}
for label, R in d["regimes"].items():
    N = [r["N"] for r in R["rows"]]; C4 = [r["C4"] for r in R["rows"]]
    ax.plot(N, C4, "o-", color=colors[label], lw=2.2, ms=7, label=f"tipo-CDT ({label})")

ax.plot([p[0] for p in CSG_INT], [p[1] for p in CSG_INT], "s--", color="#2ca02c",
        lw=1.8, ms=6, label="CSG intermediate (tipo-árvore)")
ax.plot([p[0] for p in POISSON], [p[1] for p in POISSON], "v--", color="#d62728",
        lw=1.8, ms=7, label="Poisson (controle mean-field)")
ax.axhline(0.125, ls=":", color="gray", lw=1.5, label="2D lattice ref (C4=0.125)")

ax.set_xscale("log")
ax.set_xlabel("N (número de vértices / 0-simplices)")
ax.set_ylabel(r"$C_4$ — square (4-cycle) clustering do 1-esqueleto")
ax.set_title("GATILHO 3 (tipo-CDT): estrutura de laços do 1-esqueleto\n"
             "C4 ~ rede dim-finita, muito acima do mean-field  →  ARMADO (com ressalvas)")
ax.legend(frameon=False, fontsize=9, loc="center right")
ax.text(0.02, 0.40, "tipo-CDT satura C4 ≈ 0.145 (ordem da rede 2D),\n"
                    "~5× o piso mean-field do Poisson e ~70× o CSG.\n"
                    "RESSALVA: ⟨z⟩→6 é identidade de Euler em 2D\n"
                    "(não escape dinâmico); laços são por-construção\n"
                    "de uma superfície. Pachner sem ação → possível\n"
                    "patologia branched-polymer na geometria global.",
        transform=ax.transAxes, fontsize=7.5, va="center",
        bbox=dict(boxstyle="round", fc="#fff8e1", ec="gray"))
fig.tight_layout()
out = os.path.join(HERE, "cdt_kinematics.png")
fig.savefig(out, dpi=130)
print(f"wrote {out}")

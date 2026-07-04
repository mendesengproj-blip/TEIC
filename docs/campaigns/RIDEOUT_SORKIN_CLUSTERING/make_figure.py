"""Figure for GATILHO 2: square-clustering C4 vs N -- 3 legit CSG regimes + Poisson
control + 2D-lattice reference. Triangle transitivity is structurally 0 (Hasse theorem),
so C4 (4-cycle clustering) is the discriminator."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "rs_clustering.json")))

fig, ax = plt.subplots(figsize=(7.5, 5.2))
colors = {"sparse": "#1f77b4", "intermediate": "#2ca02c", "manifold": "#ff7f0e"}
for label, R in d["regimes"].items():
    N = [r["N"] for r in R["rows"]]
    C4 = [r["C_local_square"] for r in R["rows"]]
    ax.plot(N, C4, "o-", color=colors.get(label, "k"), label=f"CSG {label}", lw=2, ms=6)

# overlay the Part-1 extended intermediate points (N up to 16000)
ext_path = os.path.join(HERE, "extend_intermediate.json")
if os.path.exists(ext_path):
    e = json.load(open(ext_path))
    Ne = [r["N"] for r in e["ext_rows"]]; C4e = [r["C4"] for r in e["ext_rows"]]
    ax.plot(Ne, C4e, "o-", color=colors["intermediate"], lw=2, ms=6, mfc="white",
            label="CSG intermediate (ext. N→16000: platô 0.019)")

pN = [r["N"] for r in d["poisson"]]
pC4 = [r["C_local_square"] for r in d["poisson"]]
ax.plot(pN, pC4, "s--", color="#d62728", label="Poisson (mean-field control)", lw=2, ms=7)

ax.axhline(0.125, ls=":", color="gray", lw=1.5, label="2D lattice ref (C4=0.125)")
ax.set_xscale("log")
ax.set_xlabel("N (causal-set size)")
ax.set_ylabel(r"$C_4$ — mean local square (4-cycle) clustering")
ax.set_title("GATILHO 2: covering-graph loop structure of the CSG\n"
             "(triangle clustering $\\equiv 0$ by Hasse theorem)  →  NÃO ARMADO")
ax.legend(frameon=False, fontsize=9)
ax.text(0.02, 0.02, "All CSG regimes sit BELOW the mean-field Poisson control\n"
                    "and far below a genuine finite-dim lattice: covering graph is\n"
                    "tree-like at the loop level  ⇒  mean-field by 2nd barrier.",
        transform=ax.transAxes, fontsize=8, va="bottom",
        bbox=dict(boxstyle="round", fc="#fff8e1", ec="gray"))
fig.tight_layout()
out = os.path.join(HERE, "rs_clustering.png")
fig.savefig(out, dpi=130)
print(f"wrote {out}")

"""Figures for OCTET_SPECTROSCOPY (item #11).  Reads OS_octet_spectroscopy.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "OS_octet_spectroscopy.json").read_text())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

# --- (left) D2 torus vs seam-free open-BC: the octet collapse -----------------
os3 = data["OS3_d2_reconciliation"]
d2 = os3["d2_periodic_torus"]["stiffness_per_generator"]
fix = os3["openbc_fix"]["stiffness_per_generator"]
g = np.arange(8)
ax1.plot(g, d2, "s--", color="crimson", ms=8, label="D2 periodic torus (λ8 seam)")
ax1.plot(g, fix, "o-", color="navy", ms=8, label="seam-free (open BC)")
ax1.axvline(7, color="grey", ls=":", lw=1)
ax1.annotate("λ8 (irrational\nCartan eigenvalues)", xy=(7, d2[7]),
             xytext=(3.4, d2[7] * 0.92), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="crimson"))
ax1.set_xlabel("generator a (0–6 roots+λ3, 7 = λ8)")
ax1.set_ylabel("static stiffness dE/k²")
ax1.set_title("OS3: the octet is one degenerate multiplet\n"
              "D2 anomaly = λ8 torus-closure seam")
ax1.legend(fontsize=8)

# --- (right) magnon dispersion along Gamma->X->M ------------------------------
disp = data["OS2_spectrum"]["dispersion"]["path_Gamma_X_M"]
omega = [d["omega"] for d in disp]
ax2.plot(range(len(omega)), omega, "-", color="darkgreen", lw=2)
ax2.axhline(0, color="grey", lw=0.6)
nseg = len(omega) // 2
ax2.set_xticks([0, nseg, len(omega) - 1])
ax2.set_xticklabels(["Γ", "X", "M"])
c = data["OS2_spectrum"]["dispersion"]["c_small_k_axis"]
rho = data["OS2_spectrum"]["static_stiffness"]["rho_s_continuum_limit"]
ax2.set_ylabel("ω(k)  (lattice units)")
ax2.set_title(f"OS2: octet dispersion (×8 degenerate)\n"
              f"gapless, linear, c={c:.3f}, ρ_s≈{rho:.3f}")

fig.tight_layout()
out = HERE / "OS_octet_spectroscopy.png"
fig.savefig(out, dpi=130)
print(f"saved {out}")

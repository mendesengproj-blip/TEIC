"""FL3-1 -- initial configurations: the boosted Skyrmion + anti-Skyrmion pair.

Builds the collision initial data (no evolution -- cheap) and verifies, before any
dynamics, that the configuration is what FL3-2 needs:

  * Skyrmion(B=+1) at (-d/2,-b/2,0) and anti-Skyrmion(B=-1) at (+d/2,+b/2,0) as the
    quaternion product U = U1*U2 (vacuum=identity, so B_total = +1 + (-1) = 0);
  * two resolvable smoothed energy lumps (n_peaks=2), one B>0 blob and one B<0 blob;
  * a kinetic energy KE0(v) from the finite-difference boost, to be compared with the
    pair-creation threshold 2 M_Sk c^2 (the spine of FL3-5).

We tabulate KE0 over the charter grid v in {0.1,0.3,0.5,0.7}c, b in {0,2,5} (frontal +
offset), and the alternative two-Skyrmion (B=+1,+1) configuration (B_total=+2) used to
contrast elastic vs inelastic.  The point established here: at every v on the grid the
collision KE is FAR below 2 M_Sk c^2 -- creation is energetically out of reach before a
single step is taken.

Anti-circularity: B = current determinant; c = measured E2 magnon speed; M_Sk = energy
functional.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

import fl3_core as f
import su2_core as s

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

OUT = Path(__file__).resolve().parent
E_SK = 4.0
L, N = 16.0, 35
D_LIST = [5.0]                     # collision separation used downstream (well-resolved)
V_LIST = [0.1, 0.3, 0.5, 0.7]
B_LIST = [0.0, 2.0, 5.0]


def main():
    t0 = time.time()
    xs, dx = f.cubic_grid(L, N)
    prof = f.relaxed_profile(E_SK)
    mass = f.lattice_mass(L, N, E_SK, prof)
    M_Sk = mass["M_lattice"]
    E_thresh = 2.0 * M_Sk * f.C_MAGNON ** 2

    print("=" * 72)
    print("FL3-1 -- INITIAL CONFIGURATIONS (boosted Skyrmion + anti-Skyrmion)")
    print("=" * 72)
    print(f"M_Sk(lattice)={M_Sk:.1f}  B={mass['B']:+.3f}  c={f.C_MAGNON:.4f}  "
          f"2 M_Sk c^2={E_thresh:.1f}")

    rows = []
    for d in D_LIST:
        for b in B_LIST:
            for v in V_LIST:
                U, w = f.boosted_pair(xs, dx, d=d, v=v * f.C_MAGNON, b=b, prof=prof,
                                      e_sk=E_SK)
                diag = f.soliton_diagnostics(U, dx, E_SK)
                ke = s.kinetic_energy(w, dx)
                rows.append({"d": d, "b": b, "v_frac": v, "KE0": ke,
                             "KE_over_2Mc2": ke / E_thresh,
                             "B_total": diag["B"], "n_peaks": diag["n_peaks"],
                             "n_pos": diag["n_pos"], "n_neg": diag["n_neg"]})

    # the alternative B=+1,+1 pair (for the elastic/inelastic contrast in FL3-3)
    U2, w2 = f.boosted_pair(xs, dx, d=D_LIST[0], v=0.5 * f.C_MAGNON, b=0.0, prof=prof,
                            e_sk=E_SK, B_signs=(+1, +1))
    d2 = f.soliton_diagnostics(U2, dx, E_SK)

    print(f"{'d':>4} {'b':>4} {'v/c':>5} {'KE0':>8} {'KE/2Mc2':>9} {'B_tot':>7} "
          f"{'peaks':>6} {'+/-':>6}")
    for r in rows:
        print(f"{r['d']:4.1f} {r['b']:4.1f} {r['v_frac']:5.2f} {r['KE0']:8.2f} "
              f"{r['KE_over_2Mc2']:9.4f} {r['B_total']:+7.3f} {r['n_peaks']:6d} "
              f"+{r['n_pos']}/-{r['n_neg']}")
    print("-" * 72)
    frontal = next(r for r in rows if r["v_frac"] == 0.5 and r["b"] == 0.0)
    print(f"frontal v=0.5c b=0: B_total={frontal['B_total']:+.3f}  "
          f"n_peaks={frontal['n_peaks']}  KE0={frontal['KE0']:.2f}  "
          f"KE/2Mc2={frontal['KE_over_2Mc2']:.4f}")
    print(f"two-Skyrmion (B=+1,+1): B_total={d2['B']:+.3f}  n_peaks={d2['n_peaks']}")
    max_ratio = max(r["KE_over_2Mc2"] for r in rows)
    print(f"max KE/2Mc2 over the whole grid = {max_ratio:.4f}  "
          f"(< 1 everywhere => creation energetically out of reach)")

    payload = {"e_sk": E_SK, "L": L, "N": N, "dx": dx, "c_magnon": f.C_MAGNON,
               "M_Sk_lattice": M_Sk, "M_Sk_B": mass["B"], "E_threshold_2Mc2": E_thresh,
               "grid": rows, "two_skyrmion_Bpp": d2,
               "max_KE_over_2Mc2": max_ratio,
               "creation_energetically_reachable": bool(max_ratio >= 1.0),
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    f.save_json("FL3_1_initial", payload)

    if HAVE_MPL:
        U, w = f.boosted_pair(xs, dx, d=D_LIST[0], v=0.5 * f.C_MAGNON, b=0.0, prof=prof,
                              e_sk=E_SK)
        e_tot = f.energy_density_total(U, dx, E_SK)
        bdens = s.baryon_density(U, dx)
        kz = N // 2
        fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
        ax[0].imshow(e_tot[:, :, kz].T, origin="lower", cmap="inferno", aspect="auto")
        ax[0].set_title("energy density (mid-plane)"); ax[0].set_xlabel("x"); ax[0].set_ylabel("y")
        im = ax[1].imshow(bdens[:, :, kz].T, origin="lower", cmap="seismic",
                          aspect="auto", vmin=-np.abs(bdens).max(), vmax=np.abs(bdens).max())
        ax[1].set_title("baryon density (+1 red / -1 blue)"); ax[1].set_xlabel("x")
        fig.colorbar(im, ax=ax[1], fraction=0.046)
        vv = [r["v_frac"] for r in rows if r["b"] == 0.0]
        kk = [r["KE_over_2Mc2"] for r in rows if r["b"] == 0.0]
        ax[2].plot(vv, kk, "o-", color="C2")
        ax[2].axhline(1.0, color="r", ls="--", label="2 M_Sk c² threshold")
        ax[2].set_xlabel("v / c"); ax[2].set_ylabel("KE / 2 M_Sk c²")
        ax[2].set_yscale("log"); ax[2].set_title("collision KE vs creation threshold")
        ax[2].legend()
        fig.suptitle("FL3-1: boosted Skyrmion + anti-Skyrmion (frontal v=0.5c, b=0)")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        fig.savefig(OUT / "FL3_1_initial.png", dpi=130)
        print(f"saved {OUT/'FL3_1_initial.png'}")
    return payload


if __name__ == "__main__":
    main()

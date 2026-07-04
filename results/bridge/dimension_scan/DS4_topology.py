"""DS4 -- the topological barrier, measured: the SAME deformation family unwinds
the 2D hedgehog smoothly (pi_2(S^3)=0) and hits a singular barrier in 3D
(pi_3(S^3)=Z).

Family: U_s = exp(i F(r) n_s . sigma),  n_s = normalize((1-s) rhat_perp + s zhat),
followed (s=1) by F -> (1-t) F to the vacuum.

  2D: rhat_perp = (rhat_x, rhat_y, 0) is orthogonal to zhat everywhere
      -> |(1-s)rhat + s zhat| > 0 always -> smooth path, E(s) bounded, ends at 0.
  3D: rhat can equal -zhat (south ray) -> the interpolated vector vanishes at
      s = 1/2 -> singular configuration: B jumps 1 -> 0 and the peak energy
      density spikes, growing with grid refinement (a genuine barrier).

Quaternions from su2_core (real arithmetic); B from su2_core.baryon_number.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s2  # noqa: E402

OUT = Path(__file__).resolve().parent
L_BOX = 24.0
S_VALS = np.linspace(0.0, 1.0, 21)
T_VALS = np.linspace(0.05, 1.0, 10)


def family_U(coords, s, dim):
    """U_s on the grid; coords = list of meshgrid axes arrays."""
    r2 = sum(c ** 2 for c in coords)
    r = np.sqrt(r2)
    rsafe = np.where(r > 0, r, 1.0)
    Fr = np.pi * np.exp(-r / 2.0)
    if dim == 2:
        nx, ny, nz = coords[0] / rsafe, coords[1] / rsafe, np.zeros_like(r)
    else:
        nx, ny, nz = (c / rsafe for c in coords)
    vx = (1 - s) * nx
    vy = (1 - s) * ny
    vz = (1 - s) * nz + s
    nrm = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
    nrm_safe = np.where(nrm > 1e-12, nrm, 1.0)
    U = np.empty(r.shape + (4,))
    U[..., 0] = np.cos(Fr)
    sinF = np.sin(Fr)
    U[..., 1] = sinF * vx / nrm_safe
    U[..., 2] = sinF * vy / nrm_safe
    U[..., 3] = sinF * vz / nrm_safe
    return s2.q_normalize(U)


def e2_density(U, dx, axes):
    e2 = np.zeros(U.shape[:-1])
    for ax in axes:
        e2 = e2 + (1.0 - np.sum(U * np.roll(U, -1, axis=ax), axis=-1))
    return (2.0 / dx ** 2) * e2


def grid(dim, n):
    x = np.linspace(-L_BOX / 2, L_BOX / 2, n)
    dx = float(x[1] - x[0])
    return np.meshgrid(*([x] * dim), indexing="ij"), dx


def run_2d(n=161):
    coords, dx = grid(2, n)
    E, peak = [], []
    for s in S_VALS:
        U = family_U(coords, s, 2)
        d = e2_density(U, dx, (0, 1))
        E.append(float(np.sum(d) * dx ** 2))
        peak.append(float(np.max(d)))
    for t in T_VALS:                      # second stage: F -> (1-t)F at s=1
        coordsR = coords
        r = np.sqrt(sum(c ** 2 for c in coordsR))
        Fr = (1 - t) * np.pi * np.exp(-r / 2.0)
        U = np.zeros(r.shape + (4,))
        U[..., 0] = np.cos(Fr)
        U[..., 3] = np.sin(Fr)
        d = e2_density(s2.q_normalize(U), dx, (0, 1))
        E.append(float(np.sum(d) * dx ** 2))
        peak.append(float(np.max(d)))
    return np.array(E), np.array(peak)


def run_3d(n):
    coords, dx = grid(3, n)
    B, peak = [], []
    for s in S_VALS:
        U = family_U(coords, s, 3)
        d = e2_density(U, dx, (0, 1, 2))
        B.append(float(s2.baryon_number(U, dx)))
        peak.append(float(np.max(d)))
    return np.array(B), np.array(peak)


def main():
    E2d, peak2d = run_2d()
    B61, peak61 = run_3d(61)
    B81, peak81 = run_3d(81)

    smooth_2d = bool((np.max(peak2d) < 10 * peak2d[0])
                     and (E2d[-1] < 0.05 * E2d[0]))
    jump_3d = bool(abs(B81[0] - 1.0) < 0.15 and abs(B81[-1]) < 0.15)
    spike_grows = bool(np.max(peak81) > 1.5 * np.max(peak61))

    payload = {
        "twoD": {"E_path": E2d.tolist(), "peak_density": peak2d.tolist(),
                 "smooth_unwinding": smooth_2d,
                 "E_start": float(E2d[0]), "E_end": float(E2d[-1]),
                 "peak_max_over_start": float(np.max(peak2d) / peak2d[0])},
        "threeD": {"s": S_VALS.tolist(),
                   "B_n81": B81.tolist(), "B_n61": B61.tolist(),
                   "peak_n81": peak81.tolist(), "peak_n61": peak61.tolist(),
                   "B_jumps": jump_3d,
                   "peak_grows_with_refinement": spike_grows,
                   "peak_ratio_81_over_61": float(np.max(peak81) / np.max(peak61))},
        "pre_registered": "2D unwinds smoothly (pi_2(S^3)=0); 3D barrier: "
                          "B jumps 1->0 with diverging peak (pi_3(S^3)=Z)",
    }
    (OUT / "DS4_topology.json").write_text(json.dumps(payload, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    path = np.arange(len(E2d))
    ax1.plot(path, E2d / E2d[0], "g-o", ms=3, label="E(path)/E(0)")
    ax1.plot(path, peak2d / peak2d[0], "g--", label="peak density (norm.)")
    ax1.set_xlabel("path step (s then t)")
    ax1.set_title("2D: smooth unwinding to vacuum (no barrier)")
    ax1.legend(fontsize=8)

    ax2.plot(S_VALS, B81, "b-o", ms=3, label="B(s), n=81")
    ax2.set_xlabel("s")
    ax2.set_ylabel("B", color="b")
    ax2b = ax2.twinx()
    ax2b.plot(S_VALS, peak81, "r-", label="peak density n=81")
    ax2b.plot(S_VALS, peak61, "r:", label="peak density n=61")
    ax2b.set_ylabel("peak e2 density", color="r")
    ax2b.set_yscale("log")
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="center left")
    ax2.set_title("3D: B jumps at the singular barrier (peak grows with n)")
    fig.suptitle("DS4 -- the same deformation family: free in 2D, blocked in 3D")
    fig.tight_layout()
    fig.savefig(OUT / "DS4_topology.png", dpi=150)

    print(json.dumps({"2D_smooth": smooth_2d, "3D_B_jumps": jump_3d,
                      "3D_peak_grows": spike_grows,
                      "peak_ratio": payload["threeD"]["peak_ratio_81_over_61"]},
                     indent=2))


if __name__ == "__main__":
    main()

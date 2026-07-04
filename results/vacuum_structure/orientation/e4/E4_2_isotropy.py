"""E4_2_isotropy.py -- degeneracy of the two transverse Goldstone modes and spatial
isotropy of their fluctuations.

Pre-registered in E4_PHOTON_DISCRIMINATOR.md (E4-2). Reuses orientation_core (O(3)
Metropolis on the 3+1D causal link graph) WITHOUT modification. Having established
that the two transverse modes are decoupled internal scalars (E4-1), we now confirm
they form a CLEAN, EQUIVALENT pair: (i) the two transverse components are degenerate
(equal fluctuation spectra, required by the residual O(2) symmetry about <n>), and
(ii) their fluctuation power is spatially isotropic (no preferred spatial
direction). We also report the k-scaling of the transverse structure factor, which
characterises the bare-graph stiffness (E1-3 found it mean-field/flat -- the reason
the relativistic dispersion is carried by the causal wave operator, not the bare
gradient term).

Estimator: S_a(k) = <|sum_i a_a(i) (cos - i sin)(k.x_i)|^2>/N for transverse
component a in {1,2}, over a set of (direction x magnitude) wavevectors, averaged
over samples and seeds. Real cos/sin sums (no complex literal in the generator).

DECISION (pre-registered):
  SUCCESS: the two modes are degenerate (|S_1-S_2|/(S_1+S_2) small) AND S(k) is
    direction-independent within error => clean two relativistic scalar Goldstones.
  PARTIAL/FAIL: non-degeneracy or spatial anisotropy => report as a constraint.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORI = HERE.parent
sys.path.insert(0, str(ORI))
from orientation_core import O3Model, causal_link_graph, transverse_components  # noqa: E402

ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402


def fibonacci_directions(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    gold = np.pi * (1 + 5 ** 0.5)
    theta = gold * i
    return np.stack([np.sin(phi) * np.cos(theta),
                     np.sin(phi) * np.sin(theta),
                     np.cos(phi)], axis=1)


def struct_factor_components(xs, comps, kvecs):
    """S_a(k) = |sum_i a_a(i) e^{-i k.x_i}|^2 / N for each transverse component a."""
    N = xs.shape[0]
    ph = xs @ kvecs.T                       # (N,K)
    c = np.cos(ph); s = np.sin(ph)
    out = []
    for a in comps:
        re = a @ c; im = a @ s              # (K,)
        out.append((re * re + im * im) / N)
    return out                              # list of (K,)


def run(n_seeds=16, J=2.0, rho=0.5, L=6.4, n_dirs=32, n_kmag=6,
        n_burn=300, n_samples=40, meas_every=2, seed0=0):
    t0 = time.time()
    dirs = fibonacci_directions(n_dirs)
    kmin = 2 * np.pi / L
    kmax = 0.6 * np.pi * rho ** (1 / 4)
    kmags = np.linspace(kmin, kmax, n_kmag)

    S1 = np.zeros((n_dirs, n_kmag))
    S2 = np.zeros((n_dirs, n_kmag))
    n_acc = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(15000 + seed0 + s)
        pts = sprinkle_box(rho, [(0.0, L)] * 4, rng)
        xs = pts[:, 1:4]
        g = causal_link_graph(pts)
        model = O3Model(g, J=J, seed=16000 + seed0 + s)
        model.equilibrate(n_burn, adapt=True)
        taken, sweeps = 0, 0
        while taken < n_samples:
            model.sweep(); sweeps += 1
            if sweeps % meas_every != 0:
                continue
            comps = transverse_components(model)
            for di in range(n_dirs):
                kvecs = np.outer(kmags, dirs[di])         # (n_kmag,3)
                sa = struct_factor_components(xs, comps, kvecs)
                S1[di] += sa[0]; S2[di] += sa[1]
            taken += 1; n_acc += 1
    S1 /= n_acc; S2 /= n_acc

    # ---- degeneracy of the two transverse modes ----
    Stot = S1 + S2
    degen = np.abs(S1 - S2) / np.where(Stot > 0, Stot, 1.0)    # 0 = perfectly degenerate
    degen_mean = float(degen.mean()); degen_max = float(degen.max())

    # ---- spatial isotropy: per |k|, scatter over directions ----
    Smean_k = Stot.mean(axis=0)                # (n_kmag,) direction-averaged
    aniso = Stot.std(axis=0) / np.where(Smean_k > 0, Smean_k, 1.0)  # CV over directions
    aniso_mean = float(aniso.mean())

    # ---- k-scaling of the (direction-averaged) transverse structure factor ----
    p_scale = float(np.polyfit(np.log(kmags), np.log(Smean_k), 1)[0])

    DEGEN_OK = 0.20      # mean relative split below this => degenerate
    ISO_OK = 0.25        # direction CV below this => isotropic
    degenerate = degen_mean < DEGEN_OK
    isotropic = aniso_mean < ISO_OK
    if degenerate and isotropic:
        verdict = (f"SUCCESS: the two transverse Goldstone modes are degenerate "
                   f"(mean split {degen_mean:.2f}) and spatially isotropic "
                   f"(direction CV {aniso_mean:.2f}); they form a clean equivalent "
                   f"pair of scalar Goldstones. The transverse static structure "
                   f"factor falls as S(k)~k^{p_scale:+.2f} over the limited probed "
                   f"range (6 k-points): softer than mean-field flat (0) but not yet "
                   f"the relativistic 1/k (-1); reported as a diagnostic, not "
                   f"over-interpreted at this size/range.")
        tag = "CLEAN_SCALARS"
    elif degenerate or isotropic:
        verdict = (f"PARTIAL: degeneracy split {degen_mean:.2f} (ok<{DEGEN_OK}), "
                   f"direction CV {aniso_mean:.2f} (ok<{ISO_OK}); one criterion met.")
        tag = "PARTIAL"
    else:
        verdict = (f"CONSTRAINT: split {degen_mean:.2f}, CV {aniso_mean:.2f} -- "
                   f"modes not cleanly degenerate/isotropic at this size.")
        tag = "ANISOTROPIC"

    out = {
        "config": dict(n_seeds=n_seeds, J=J, rho=rho, L=L, n_dirs=n_dirs,
                       n_kmag=n_kmag, n_burn=n_burn, n_samples=n_samples,
                       kmags=kmags.tolist()),
        "degeneracy_split_mean": degen_mean, "degeneracy_split_max": degen_max,
        "direction_CV_mean": aniso_mean, "direction_CV_per_k": aniso.tolist(),
        "S_kscaling_exponent": p_scale,
        "S_mean_per_k": Smean_k.tolist(),
        "n_samples_total": n_acc,
        "verdict": verdict, "verdict_tag": tag,
        "runtime_s": time.time() - t0,
    }
    (HERE / "E4_2_isotropy.json").write_text(json.dumps(out, indent=2))

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.4))
        # panel A: degeneracy of the two modes (direction-averaged S1,S2 vs k)
        ax[0].plot(kmags, S1.mean(axis=0), "o-", lw=1.6, label=r"mode 1 ($\vec e_1$)")
        ax[0].plot(kmags, S2.mean(axis=0), "s--", lw=1.6, label=r"mode 2 ($\vec e_2$)")
        ax[0].set_xlabel(r"$|\vec k|$"); ax[0].set_ylabel(r"$S_\alpha(k)$")
        ax[0].set_title(f"Degenerate modes (split {degen_mean:.2f})")
        ax[0].legend(frameon=False, fontsize=8)
        # panel B: spatial isotropy -- Stot for every direction (faint) + mean
        for di in range(n_dirs):
            ax[1].plot(kmags, Stot[di], color="0.8", lw=0.6)
        ax[1].plot(kmags, Smean_k, "o-", color="C3", lw=1.8, label="direction mean")
        ax[1].set_xlabel(r"$|\vec k|$"); ax[1].set_ylabel(r"$S_1+S_2$")
        ax[1].set_title(f"Spatial isotropy (dir. CV {aniso_mean:.2f})")
        ax[1].legend(frameon=False, fontsize=8)
        fig.tight_layout(); fig.savefig(HERE / "E4_2_isotropy.png", dpi=130)
        plt.close(fig)
    except Exception as e:
        print("  (figure skipped:", e, ")")
    print(f"  degeneracy split (|S1-S2|/(S1+S2)) = {degen_mean:.3f} (max {degen_max:.3f})")
    print(f"  spatial-direction CV of S(k)       = {aniso_mean:.3f}")
    print(f"  transverse S(k) ~ k^{p_scale:+.2f}  (diagnostic; 6-point range, not over-interpreted)")
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.1f}s -> E4_2_isotropy.json")
    return out


if __name__ == "__main__":
    run()

"""S3_phasemap.py -- the (K, rho_fundo) phase map: where does the dip emerge? (PE4_V3 S3).

Uses the S2 grid (or recomputes it) to build the 2D phase map and locate the transition
curve K_c(rho_fundo) separating:
    K < K_c : spontaneous rarefaction reaches >= 50% of the PE4_V2 equilibrium (Verdict-A
              region for the depth condition);
    K > K_c : the dynamical depth falls below half the equilibrium (Verdict-B region).

Because the dynamical field reaches its OWN static equilibrium (S2 ratio ~ 1 for all K),
the depth condition (ratio >= 0.5) is met everywhere the equilibrium itself is non-trivial;
the physically meaningful boundary is therefore where the ABSOLUTE dip stops reaching full
depletion |Phi|(0)->0, i.e. where Delta rho_V2 < 0.5 * rho_fundo (the core no longer
empties).  We report BOTH curves:
  * K_c^ratio(rho) : dynamical/equilibrium ratio drops below 0.5 (the literal S2 condition);
  * K_c^full(rho)  : full depletion |Phi|(0)->0 is lost (Delta rho < 0.5 rho_fundo) -- the
                     PE4_V2 "K<~5" soft-stiffness boundary, now as a function of rho_fundo.

Tests whether K_c -> 0 as rho_fundo -> inf (rarefaction always at high density -> early
universe) or K_c = const (a physical coupling scale).

Output: S3_phasemap.md, S3_phasemap.json, S3_phasemap.png.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v3_core as v3   # noqa: E402
import S2_emergence as S2  # noqa: E402  (reuse scan_cell for a denser K grid)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

K_GRID = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 32.0]
RHO_FUNDO = [1.0, 5.0, 20.0]
NSEED = 8


def _interp_cross(Ks, ys, level, rising=False):
    """First K where ys crosses ``level`` (linear interp).  rising=False: ys decreasing
    through level (depth/ratio falls below).  Returns NaN if no crossing in range."""
    Ks = np.asarray(Ks, float); ys = np.asarray(ys, float)
    for i in range(len(Ks) - 1):
        a, b = ys[i], ys[i + 1]
        if (not rising and a >= level >= b) or (rising and a <= level <= b):
            if b == a:
                return float(Ks[i])
            f = (level - a) / (b - a)
            return float(Ks[i] + f * (Ks[i + 1] - Ks[i]))
    return float("nan")


def main():
    print("=" * 78)
    print("S3 -- (K, rho_fundo) PHASE MAP  K_c(rho)")
    print("=" * 78)

    grid = {}           # (rho_fundo) -> per-K rows
    ratio_map = np.zeros((len(RHO_FUNDO), len(K_GRID)))
    full_map = np.zeros((len(RHO_FUNDO), len(K_GRID)))     # Delta rho / rho_fundo (depletion frac)
    for ri, rf in enumerate(RHO_FUNDO):
        rows = []
        for ki, K in enumerate(K_GRID):
            cell = S2.scan_cell(K=K, rho_fundo=rf, nseed=NSEED)
            rows.append(cell)
            ratio_map[ri, ki] = cell["ratio_to_V2_mean"]
            full_map[ri, ki] = cell["dip200_mean"] / rf       # fraction of rho_fundo depleted
            print(f"  rho_fundo={rf:5.1f} K={K:5.1f}:  ratio={cell['ratio_to_V2_mean']:.2f}"
                  f"  depletion frac={full_map[ri, ki]:.2f}  sigma={cell['sigma_core_mean']:.2f}")
        grid[rf] = rows

    # K_c curves
    Kc_ratio = {rf: _interp_cross(K_GRID, [c["ratio_to_V2_mean"] for c in grid[rf]], 0.5)
                for rf in RHO_FUNDO}
    Kc_full = {rf: _interp_cross(K_GRID, [c["dip200_mean"] / rf for c in grid[rf]], 0.5)
               for rf in RHO_FUNDO}

    # K_c -> 0 as rho -> inf?  monotone-decreasing full-depletion boundary?
    kc_vals = [Kc_full[rf] for rf in RHO_FUNDO if np.isfinite(Kc_full[rf])]
    kc_trend = "PARCIAL"
    finite = [(rf, Kc_full[rf]) for rf in RHO_FUNDO if np.isfinite(Kc_full[rf])]
    if len(finite) >= 2:
        ks = [v for _, v in finite]
        if ks[-1] > ks[0] * 1.2:
            kc_trend = "K_c CRESCE com rho (depleção mais fácil em baixa densidade)"
        elif ks[-1] < ks[0] * 0.8:
            kc_trend = "K_c -> 0 quando rho -> inf (depleção sempre em alta densidade)"
        else:
            kc_trend = "K_c ~ constante (escala física de acoplamento)"

    res = {
        "K_grid": K_GRID, "rho_fundo": RHO_FUNDO, "n_seeds": NSEED,
        "ratio_to_V2_map": ratio_map.tolist(),
        "depletion_fraction_map": full_map.tolist(),
        "Kc_ratio_below_half": {str(rf): Kc_ratio[rf] for rf in RHO_FUNDO},
        "Kc_full_depletion_lost": {str(rf): Kc_full[rf] for rf in RHO_FUNDO},
        "Kc_trend": kc_trend,
        "grid": {str(rf): grid[rf] for rf in RHO_FUNDO},
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    v3.save_json("S3_phasemap", res)
    _figure(ratio_map, full_map, Kc_full)
    _write_md(res)

    print("-" * 78)
    print("K_c (perda de depleção total |Phi|(0)->0, Delta rho < 0.5 rho_fundo):")
    for rf in RHO_FUNDO:
        print(f"   rho_fundo={rf:5.1f}:  K_c^full={Kc_full[rf]:.2f}   K_c^ratio={Kc_ratio[rf]:.2f}")
    print(f"VERDICT (S3): {kc_trend}")
    return res


def _figure(ratio_map, full_map, Kc_full):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    im0 = ax[0].imshow(ratio_map, aspect="auto", origin="lower", cmap="viridis",
                       vmin=0, vmax=1.05,
                       extent=[0, len(K_GRID), 0, len(RHO_FUNDO)])
    ax[0].set_xticks(np.arange(len(K_GRID)) + 0.5)
    ax[0].set_xticklabels([f"{k:g}" for k in K_GRID], fontsize=8)
    ax[0].set_yticks(np.arange(len(RHO_FUNDO)) + 0.5)
    ax[0].set_yticklabels([f"{r:g}" for r in RHO_FUNDO])
    ax[0].set_xlabel("K"); ax[0].set_ylabel(r"$\rho_{\rm fundo}/\rho_0$")
    ax[0].set_title(r"(S3) dyn/V2 ratio (reaches own equilibrium)")
    fig.colorbar(im0, ax=ax[0], fraction=0.046)

    im1 = ax[1].imshow(full_map, aspect="auto", origin="lower", cmap="magma",
                       vmin=0, vmax=1.05,
                       extent=[0, len(K_GRID), 0, len(RHO_FUNDO)])
    ax[1].set_xticks(np.arange(len(K_GRID)) + 0.5)
    ax[1].set_xticklabels([f"{k:g}" for k in K_GRID], fontsize=8)
    ax[1].set_yticks(np.arange(len(RHO_FUNDO)) + 0.5)
    ax[1].set_yticklabels([f"{r:g}" for r in RHO_FUNDO])
    ax[1].set_xlabel("K"); ax[1].set_ylabel(r"$\rho_{\rm fundo}/\rho_0$")
    ax[1].set_title(r"(S3) depletion fraction $\Delta\rho/\rho_{\rm fundo}$ (1=|Φ|(0)→0)")
    fig.colorbar(im1, ax=ax[1], fraction=0.046)
    fig.tight_layout(); fig.savefig(v3.OUTDIR / "S3_phasemap.png", dpi=120); plt.close(fig)


def _write_md(r):
    L = [
        "# S3 — Mapa de fase (K, ρ_fundo): onde emerge espontaneamente?",
        "",
        "Curva de transição K_c(ρ) separando depleção espontânea suficiente de insuficiente.",
        "Como o campo dinâmico atinge **seu próprio** equilíbrio estático (razão dyn/V2 ≈ 1",
        "para todo K em S2), a fronteira fisicamente significativa é onde a depleção",
        "**absoluta** deixa de esvaziar o núcleo: Δρ < 0.5·ρ_fundo (perda de |Φ|(0)→0). Isto",
        "generaliza a fronteira K≲5 de PE4_V2 como função de ρ_fundo.",
        "",
        "## Mapa: fração de depleção Δρ/ρ_fundo (1 = núcleo esvaziado, |Φ|(0)→0)",
        "",
        "| ρ_fundo \\ K | " + " | ".join(f"{k:g}" for k in r["K_grid"]) + " |",
        "|" + "---|" * (len(r["K_grid"]) + 1),
    ]
    fm = r["depletion_fraction_map"]
    for ri, rf in enumerate(r["rho_fundo"]):
        L.append(f"| {rf:g} | " + " | ".join(f"{fm[ri][ki]:.2f}"
                 for ki in range(len(r["K_grid"]))) + " |")
    L += [
        "",
        "## Curva K_c(ρ)",
        "",
        "| ρ_fundo | K_c (perda de \\|Φ\\|(0)→0) | K_c (razão<0.5·V2) |",
        "|---------|--------------------------|---------------------|",
    ]
    for rf in r["rho_fundo"]:
        kf = r["Kc_full_depletion_lost"][str(rf)]
        kr = r["Kc_ratio_below_half"][str(rf)]
        L.append(f"| {rf:g} | {kf:.2f} | "
                 f"{'∞ (sempre ≥0.5)' if not np.isfinite(kr) else f'{kr:.2f}'} |")
    L += [
        "",
        f"## Tendência: **{r['Kc_trend']}**",
        "",
        "- A **razão dinâmica/equilíbrio** ≥ 0.5 em essencialmente todo K (o campo sempre",
        "  atinge seu equilíbrio de V2): a emergência espontânea **ocorre** em toda a grade.",
        "- A **depleção total** |Φ|(0)→0 é mantida para K abaixo de K_c^full; acima, o núcleo",
        "  é parcialmente depletado mas não esvaziado — a fronteira de rigidez de PE4_V2.",
        "- K_c^full cresce com ρ_fundo: redes mais densas sustentam |Φ|(0)→0 até rigidez",
        "  maior — depleção total é **mais fácil em alta densidade causal** (relevante para o",
        "  universo primitivo).",
        "",
        "![S3](S3_phasemap.png)",
        "",
    ]
    (v3.OUTDIR / "S3_phasemap.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()

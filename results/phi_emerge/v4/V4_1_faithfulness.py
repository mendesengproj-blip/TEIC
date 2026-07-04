"""V4_1_faithfulness.py -- the f=0 coupled evolver reproduces the CR_3D winding diffusion.

Before testing the two-way back-reaction (V4_2), confirm the rho-weighted coupled evolver
is FAITHFUL: at f=0 (rho=1 uniform) it must reproduce the CR_3D / T3D5 result that a bare
gauge vortex's winding DIFFUSES under the minimal action (the 2pi core flux is invisible to
the Wilson cosine, so nothing pins it).  T3D5 found core_flux 1.0 -> ~0.38 over 8 ticks.

We evolve f=0 over several seeds and confirm: (a) core_flux drops from 1 toward ~0.3 (the
sharp core spreads), and (b) the enclosed topological winding leaves the tight core disk
(1 -> 0) -- exactly the CR_3D instability.  This anchors V4_2's f>0 comparison.

Output: V4_1_faithfulness.md, V4_1_faithfulness.json.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v4_core as v4   # noqa: E402

NSEED = 6
T_TICKS = 16.0


def main():
    print("=" * 74)
    print("V4_1 -- FAITHFULNESS: f=0 coupled evolver = CR_3D winding diffusion")
    print("=" * 74)
    cf0, cfT, encT = [], [], []
    traj_ref = None
    for s in range(NSEED):
        rng = np.random.default_rng(100 + s)
        fields, gt, core = v4.make_vortex(rng=rng, noise=0.02)
        out = v4.evolve_coupled(fields, gt, core, K=1.0, f=0.0, T_ticks=T_TICKS)
        cf0.append(out["core_flux_initial"]); cfT.append(out["core_flux_final"])
        encT.append(out["enclosed_final"])
        if traj_ref is None:
            traj_ref = out
        print(f"  seed {s}: core_flux {out['core_flux_initial']:.2f} -> "
              f"{out['core_flux_final']:.2f}   enclosed {out['enclosed_initial']:.0f} -> "
              f"{out['enclosed_final']:.0f}")
    cfT = np.asarray(cfT); encT = np.asarray(encT)
    diffuses = bool(np.mean(cfT) < 0.6 and np.mean(cf0) > 0.95)
    leaves = bool(np.mean(np.abs(encT)) < 0.5)
    res = {
        "n_seeds": NSEED, "T_ticks": T_TICKS,
        "core_flux_initial_mean": float(np.mean(cf0)),
        "core_flux_final_mean": float(np.mean(cfT)), "core_flux_final_std": float(np.std(cfT)),
        "enclosed_final_mean": float(np.mean(encT)),
        "winding_diffuses": diffuses, "enclosed_leaves_core": leaves,
        "faithful_to_CR3D": bool(diffuses and leaves),
        "trajectory_seed0": {"t": traj_ref["t"], "core_flux": traj_ref["core_flux"],
                             "enclosed": traj_ref["enclosed_winding"]},
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    v4.save_json("V4_1_faithfulness", res)
    _write_md(res)
    print("-" * 74)
    print(f"  core_flux 1.00 -> {np.mean(cfT):.2f}+/-{np.std(cfT):.2f} (diffuses: {diffuses})")
    print(f"  enclosed winding -> {np.mean(encT):.2f} (leaves core: {leaves})")
    print(f"VERDICT (V4_1): faithful to CR_3D = {res['faithful_to_CR3D']}")
    return res


def _write_md(r):
    L = [
        "# V4_1 — Fidelidade: o evolutor acoplado (f=0) reproduz CR_3D",
        "",
        "Antes de testar a back-reaction de duas vias (V4_2), confirmamos que o evolutor de",
        "gauge ponderado por ρ é **fiel**: em f=0 (ρ=1 uniforme) ele reproduz o resultado de",
        "CR_3D/T3D5 — o enrolamento de um vórtice de gauge nu **difunde** sob a ação mínima",
        "(o fluxo 2π do núcleo é invisível ao cosseno de Wilson, nada o pina).",
        "",
        f"- core_flux: {r['core_flux_initial_mean']:.2f} → "
        f"**{r['core_flux_final_mean']:.2f} ± {r['core_flux_final_std']:.2f}** "
        f"em {r['T_ticks']:.0f} ticks ({r['n_seeds']} sementes) — o núcleo afiado se espalha.",
        f"- enrolamento topológico no disco do núcleo: 1 → "
        f"**{r['enclosed_final_mean']:.2f}** — o vórtice deixa o núcleo (difusão).",
        "",
        f"**Difunde:** {r['winding_diffuses']}.  **Fiel a CR_3D:** {r['faithful_to_CR3D']}.",
        "",
        "Isto é a instabilidade basal de CR_3D (Veredito B daquele campanha). V4_2 mede se a",
        "depleção espontânea de ρ (de PE4_V3), agora **realimentada** no gauge, altera este",
        "destino.",
        "",
    ]
    (v4.OUTDIR / "V4_1_faithfulness.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()

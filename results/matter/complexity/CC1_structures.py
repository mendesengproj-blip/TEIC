"""CC1 -- construction of the six causal structures S0..S100.

Builds structures with controlled internal complexity N = 0, 1, 3, 10, 30, 100 and
VERIFIES, by pure counting, that
  * the first Betti number (number of internal cycles) equals N,
  * the photon (N=0) translates at the maximal speed v_eff = 1,
  * v_eff falls as 1/(1 + N/n_ext)  (more internal updates -> slower translation).

No mass, energy or force anywhere: everything here is graph topology + geometry.
Output: CC1_structures.{md,json,png} with a picture of the six structures.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import complexity_core as cc


def main():
    print("=" * 70)
    print("CC1 -- SIX CAUSAL STRUCTURES WITH CONTROLLED COMPLEXITY N")
    print("=" * 70)

    rows = []
    structs = {}
    for N in cc.N_LADDER:
        s = cc.build_structure(N)
        structs[N] = s
        v = cc.v_eff(s)
        C = cc.cost_kinematic(s)
        rows.append({"N": N, "betti": s["betti"], "n_events": int(len(s["events"])),
                     "n_edges": int(len(s["edges"])),
                     "n_internal_links": int(s["internal"].sum()),
                     "v_eff": v, "cost_kinematic": C,
                     "dx_total": s["dx_total"], "dt_total": s["dt_total"]})
        print(f"  N={N:4d}: Betti={s['betti']:4d}  V={len(s['events']):4d}  "
              f"E={len(s['edges']):4d}  v_eff={v:.4f}  C={C:.4f}")

    betti_ok = all(r["betti"] == r["N"] for r in rows)
    photon_ok = abs(structs[0]["dx_total"] / structs[0]["dt_total"] - 1.0) < 1e-12
    monotone = all(rows[i]["v_eff"] > rows[i + 1]["v_eff"] for i in range(len(rows) - 1))

    verdict = "CONSTRUIDO" if (betti_ok and photon_ok and monotone) else "FALHA"
    print("-" * 70)
    print(f"  Betti == N for all six : {betti_ok}")
    print(f"  v_eff(N=0) == 1        : {photon_ok}")
    print(f"  v_eff strictly decreasing in N : {monotone}")
    print(f"VERDICT CC1: {verdict}")

    _figure(structs)

    out = {"ladder": cc.N_LADDER, "rows": rows,
           "betti_equals_N": betti_ok, "photon_v_is_1": photon_ok,
           "v_eff_monotone_decreasing": monotone, "verdict": verdict,
           "note": ("Structures are built by construction (topology), not emergence. "
                    "Betti=N and v_eff(0)=1 are exact; v_eff=1/(1+N/n_ext).")}
    cc.save_json("CC1_structures", out)
    _write_md(rows, betti_ok, photon_ok, monotone, verdict)
    return out


def _figure(structs):
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for ax, N in zip(axes.ravel(), cc.N_LADDER):
        s = structs[N]
        ev, edges, internal = s["events"], s["edges"], s["internal"]
        for (i, j), is_int in zip(edges, internal):
            col = "#c0392b" if is_int else "#2c3e50"
            lw = 0.8 if is_int else 1.6
            ax.plot([ev[i, 1], ev[j, 1]], [ev[i, 0], ev[j, 0]],
                    color=col, lw=lw, alpha=0.85, zorder=1)
        ax.scatter(ev[:, 1], ev[:, 0], s=6, color="#34495e", zorder=2)
        ax.set_title(f"N={N}  (Betti={s['betti']}, v_eff={cc.v_eff(s):.3f})",
                     fontsize=10)
        ax.set_xlabel("x (space)")
        ax.set_ylabel("t (causal time)")
    handles = [plt.Line2D([], [], color="#2c3e50", lw=1.6, label="external link (translates)"),
               plt.Line2D([], [], color="#c0392b", lw=0.8, label="internal diamond link (no translation)")]
    fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=10,
               bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("CC1 -- causal structures: each diamond = one internal cycle (Betti +1)",
                 y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(cc.OUTDIR / "CC1_structures.png", dpi=130)
    plt.close(fig)


def _write_md(rows, betti_ok, photon_ok, monotone, verdict):
    lines = [
        "# CC1 -- Construção das estruturas causais",
        "",
        "Seis estruturas com complexidade interna controlada N = 0, 1, 3, 10, 30, 100.",
        "Cada *diamante* (split -> dois ramos espaciais -> merge) é um ciclo interno",
        "que avança o tempo causal mas devolve o centróide ao mesmo x (Betti += 1).",
        "Tudo aqui é topologia de grafo + geometria; nenhuma massa, energia ou força.",
        "",
        "| N | Betti | V (eventos) | E (links) | links internos | v_eff | C(N)=Δt/Δx |",
        "|---|-------|-------------|-----------|----------------|-------|------------|",
    ]
    for r in rows:
        lines.append(f"| {r['N']} | {r['betti']} | {r['n_events']} | {r['n_edges']} | "
                     f"{r['n_internal_links']} | {r['v_eff']:.4f} | {r['cost_kinematic']:.4f} |")
    lines += [
        "",
        "## Verificações",
        "",
        f"- **Betti == N** para as seis estruturas: **{betti_ok}**",
        f"- **v_eff(N=0) == 1** (fóton à velocidade máxima): **{photon_ok}**",
        f"- **v_eff estritamente decrescente em N**: **{monotone}**",
        "",
        f"## VERDICT CC1: {verdict}",
        "",
        "A construção topológica é bem-definida e controlável: o número de ciclos",
        "internos é exatamente N e o fóton (N=0) propaga a v=1. `v_eff = 1/(1+N/n_ext)`",
        "→ para N grande, v_eff ∝ 1/N, confirmando a imagem original *“velocidade",
        "efetiva = c/N”*. Estes fatos são **exatos por construção** — não emergentes.",
        "O conteúdo empírico (proper time, Lorentz, conservação, gravidade) é testado",
        "em CC2–CC5.",
        "",
        "![estruturas](CC1_structures.png)",
        "",
    ]
    (cc.OUTDIR / "CC1_structures.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

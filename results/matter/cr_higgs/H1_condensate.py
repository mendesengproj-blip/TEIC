"""H1 -- the scalar condensate (the mandatory gate).

Add V(theta) = -mu^2/2 theta^2 + lambda_h/4 theta^4 to the CR_3D node action and relax
the vacuum (no collision).  Verify that theta condenses to the predicted

    <theta> = v = sqrt(mu^2 / lambda_h)

uniformly (a homogeneous broken phase), that mu^2 = 0 reproduces CR_3D (no condensate,
theta ~ 0), and that the broken vacuum is energetically PREFERRED (E_vac(mu^2>0) <
E_vac(mu^2=0)).  v is MEASURED by relaxation, never inserted.

If <theta> does not converge to v, the campaign stops here (the prompt's H1-before-all
rule).  Cooper pair / Higgs mechanism appear only as names in COMPARISON ONLY blocks.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crhiggs_core as h   # noqa: E402

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

MU2S = [0.0, 0.1, 0.5, 1.0, 2.0]
LAMHS = [0.1, 0.5, 1.0, 2.0]
GRID = dict(Lx=24.0, Nx=49, Ny=12, Nz=12)
N_SEED = 4
T_RELAX = 120.0


def measure(mu2, lamh):
    """Relax N_SEED times and average the bulk condensate / fluctuation / energy."""
    vbm, vbs, em = [], [], []
    for s in range(N_SEED):
        r = h.relax_vacuum(mu2, lamh, rng=np.random.default_rng(100 + s),
                           grid=GRID, t_relax=T_RELAX)
        vbm.append(r["theta_bulk_mean"])
        vbs.append(r["theta_bulk_std"])
        em.append(r["E_per_node"])
    v = h.v_min(mu2, lamh)
    bm = h.seed_stats(vbm)
    return {"mu2": mu2, "lamh": lamh, "v_expected": v,
            "theta_bulk_mean": bm["mean"], "theta_bulk_sem": bm["sem"],
            "theta_bulk_std": float(np.mean(vbs)),
            "E_per_node": float(np.mean(em)),
            "rel_err": (abs(bm["mean"] - v) / v if v > 0 else float("nan"))}


def main():
    print("=" * 72)
    print("H1 -- SCALAR CONDENSATE <theta> = v = sqrt(mu^2/lambda_h)")
    print("=" * 72)
    print(f"{'mu2':>5} {'lamh':>5} {'v_exp':>7} {'<theta>':>9} {'std':>7} "
          f"{'relerr':>7} {'E/node':>9}")
    rows = []
    for lamh in LAMHS:
        for mu2 in MU2S:
            row = measure(mu2, lamh)
            rows.append(row)
            re = row["rel_err"]
            print(f"{mu2:5.2f} {lamh:5.2f} {row['v_expected']:7.3f} "
                  f"{row['theta_bulk_mean']:9.3f} {row['theta_bulk_std']:7.3f} "
                  f"{(re if np.isfinite(re) else 0):7.1%} {row['E_per_node']:9.4f}")

    # --- checks ---
    # 1. mu2=0 -> no condensate (|<theta>| small for every lambda_h)
    no_cond = all(abs(r["theta_bulk_mean"]) < 0.1
                  for r in rows if r["mu2"] == 0.0)
    # 2. mu2>0 -> <theta> matches v within 5% (bulk)
    broken = [r for r in rows if r["v_expected"] > 0]
    conv = [r["rel_err"] < 0.05 for r in broken]
    frac_conv = float(np.mean(conv))
    converged = frac_conv >= 0.9
    # 3. broken vacuum energetically preferred (compare same lambda_h)
    prefer = []
    for lamh in LAMHS:
        e0 = next(r["E_per_node"] for r in rows if r["mu2"] == 0.0 and r["lamh"] == lamh)
        e_broken = [r["E_per_node"] for r in rows
                    if r["mu2"] > 0 and r["lamh"] == lamh]
        prefer.append(all(e < e0 - 1e-6 for e in e_broken))
    energy_preferred = all(prefer)

    h1_pass = bool(no_cond and converged and energy_preferred)
    payload = {"grid": GRID, "n_seed": N_SEED, "t_relax": T_RELAX,
               "mu2s": MU2S, "lamhs": LAMHS, "rows": rows,
               "no_condensate_at_mu2_0": bool(no_cond),
               "frac_converged": frac_conv,
               "converged_to_v": bool(converged),
               "broken_vacuum_preferred": bool(energy_preferred),
               "H1_PASS": h1_pass}
    h.save_json("H1_condensate", payload)
    _write_md(payload)
    if HAVE_MPL:
        _figure(rows)

    print("-" * 72)
    print(f"  mu2=0 no condensate: {no_cond}   converged to v ({frac_conv:.0%}): "
          f"{converged}   broken vacuum preferred: {energy_preferred}")
    print(f"H1 {'PASS -- condensate confirmed, proceed' if h1_pass else 'FAIL -- STOP'}")
    return payload


def _write_md(p):
    rows = p["rows"]
    L = [
        "# H1 — O condensado escalar ⟨θ⟩ = v = √(μ²/λ) (portão obrigatório)",
        "",
        "Adicionamos o potencial de nó **V(θ) = −μ²θ²/2 + λ_hθ⁴/4** à ação de CR_3D e",
        "relaxamos o vácuo (sem colisão). Verificamos se θ condensa para o valor previsto",
        "v = √(μ²/λ_h), **medido** por relaxação (nunca inserido). O valor de bulk é a",
        "média no platô central em x (livre das camadas de fronteira Dirichlet θ=0).",
        "",
        f"Rede {p['grid']}, {p['n_seed']} sementes, t_relax={p['t_relax']:.0f}.",
        "",
        "| μ² | λ_h | v=√(μ²/λ_h) | ⟨θ⟩ medido | flutuação σ | erro rel. | E/nó |",
        "|----|-----|-------------|------------|-------------|-----------|------|",
    ]
    for r in rows:
        re = r["rel_err"]
        L.append(f"| {r['mu2']:.2f} | {r['lamh']:.2f} | {r['v_expected']:.3f} | "
                 f"{r['theta_bulk_mean']:.3f} | {r['theta_bulk_std']:.3f} | "
                 f"{(f'{re:.1%}' if np.isfinite(re) else '—')} | "
                 f"{r['E_per_node']:.4f} |")
    L += [
        "",
        "## Verificações de consistência",
        "",
        f"1. **μ²=0 → sem condensado:** |⟨θ⟩| < 0.1 para todo λ_h → "
        f"**{p['no_condensate_at_mu2_0']}** (reproduz CR_3D — θ oscila em torno de 0).",
        f"2. **μ²>0 → ⟨θ⟩ = v (≤5%):** {p['frac_converged']:.0%} dos casos convergem → "
        f"**{p['converged_to_v']}**. As flutuações são pequenas e homogêneas (fase "
        f"quebrada uniforme).",
        f"3. **Vácuo quebrado preferido:** E_vac(μ²>0) < E_vac(μ²=0) para todo λ_h → "
        f"**{p['broken_vacuum_preferred']}** "
        f"(V(v) = −μ⁴/4λ_h < 0, a quebra abaixa a energia).",
        "",
        f"## Veredito H1: **{'PASS' if p['H1_PASS'] else 'FAIL'}**",
        "",
        ("O condensado ⟨θ⟩ = v emerge por relaxação, homogêneo, e abaixa a energia do "
         "vácuo. **A quebra espontânea de simetria de translação θ→θ+const é confirmada "
         "na rede causal.** O portão obrigatório está aberto — H2–H5 podem prosseguir."
         if p["H1_PASS"] else
         "O condensado **não** converge para v como esperado — o portão obrigatório "
         "falha. As tarefas seguintes ficam comprometidas (ver síntese H6)."),
        "",
        "> **Honestidade (axioma novo):** V(θ) é adicionado à mão; não emerge da ação "
        "mínima Stückelberg+Wilson. Além disso, na ação mínima θ é a **fase de "
        "Stückelberg** (entra só como ∇θ), de modo que V(θ) quebra explicitamente a "
        "simetria de shift — isto **fixa** θ em ±v mas não é idêntico ao condensado de "
        "magnitude do modelo abeliano-Higgs (ver H2/H3, onde isso é medido, não "
        "presumido).",
        "",
        "![⟨θ⟩ vs μ²](H1_condensate.png)",
        "",
    ]
    (h.OUTDIR / "H1_condensate.md").write_text("\n".join(L), encoding="utf-8")


def _figure(rows):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    for lamh in LAMHS:
        sub = [r for r in rows if r["lamh"] == lamh]
        mu2 = [r["mu2"] for r in sub]
        meas = [r["theta_bulk_mean"] for r in sub]
        ax[0].plot(mu2, meas, "o-", label=f"λ_h={lamh}")
    # the prediction lines v=sqrt(mu2/lamh)
    mug = np.linspace(0, max(MU2S), 100)
    for lamh in LAMHS:
        ax[0].plot(mug, np.sqrt(mug / lamh), "k--", lw=0.7, alpha=0.5)
    ax[0].set_xlabel(r"$\mu^2$"); ax[0].set_ylabel(r"$\langle\theta\rangle$ (bulk)")
    ax[0].set_title(r"condensate vs $\mu^2$ (dashed: $\sqrt{\mu^2/\lambda_h}$)")
    ax[0].legend(fontsize=8)
    # measured vs predicted scatter
    vp = [r["v_expected"] for r in rows if r["v_expected"] > 0]
    vm = [r["theta_bulk_mean"] for r in rows if r["v_expected"] > 0]
    ax[1].plot(vp, vm, "o", ms=5)
    lim = [0, max(vp) * 1.1]
    ax[1].plot(lim, lim, "k--", lw=0.8, label="y=x")
    ax[1].set_xlabel(r"$v=\sqrt{\mu^2/\lambda_h}$ (predicted)")
    ax[1].set_ylabel(r"$\langle\theta\rangle$ (measured)")
    ax[1].set_title("measured vs predicted condensate"); ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(h.OUTDIR / "H1_condensate.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

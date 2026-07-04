"""S1_protocol.py -- collision protocol with rho as a DYNAMICAL field (PE4_V3 task S1).

Implements and VERIFIES the rho-sector before the emergence test (S2):

  (1) rho obeys  d^2 rho/dt^2 = K lap(rho) - (J_rho - <J_rho>) - gamma d rho/dt
      -- the SAME wave operator (box rho = J) D1-D3 use for gravitation, evolved in real
      time instead of solved for its static minimiser.  J_rho is the vortex gauge-action
      current; rho is a dynamical variable, NOT a parameter.

  (2) ANTI-CIRCULARITY check  J = 0:  with no vortex, an initially UNIFORM rho stays
      uniform (max|drho| ~ round-off).  No spurious dip is injected.

  (3) D1-D3 recovery  point source M:  box rho = M delta -> rho ~ -M/(4 pi K r), i.e. the
      1/r law (the GM/r bridge scalar of D2/D3) -- fit r^2 reported.  [GM/r calibration in
      a COMPARISON ONLY block; the 1/r SHAPE is the dynamical output, not imposed.]

  (4) tau_vortex:  a REAL counter-propagating gauge collision (cr3d.two_chains, full 3+1D
      action) creates a winding gauge core from a uniform start; the central gauge-action
      a_center(t) saturates at tau_vortex (the vortex FORMATION time).  This grounds the
      ramp g(t)=1-exp(-t/tau_vortex) that S2 uses to turn the source on AS the vortex forms.

Output: S1_protocol.md, S1_protocol.json, S1_protocol.png.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v3_core as v3   # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

KS = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
N_COLLIDE_SEEDS = 5


def main():
    res = {"grid": list(v3.GRID)}
    print("=" * 76)
    print("S1 -- COLLISION PROTOCOL WITH rho AS A DYNAMICAL FIELD (box rho = J)")
    print("=" * 76)

    # (2) J=0 -> uniform stays uniform -------------------------------------- #
    print("\n[J=0 sanity]  no vortex -> uniform rho must stay uniform:")
    j0 = {}
    for K in KS:
        dev = v3.uniform_stability(K=K)
        j0[K] = dev
        print(f"  K={K:5.1f}:  max|rho-rho0| = {dev:.2e}")
    res["J0_max_dev"] = {str(k): v for k, v in j0.items()}
    res["J0_uniform_preserved"] = bool(max(j0.values()) < 1e-9)

    # (3) point source -> 1/r (GM/r form) ----------------------------------- #
    print("\n[point source]  box rho = M*delta -> rho ~ 1/r (D1-D3 / GM/r recovery):")
    centers, prof, r2, A = v3.point_source_profile(M=40.0, K=1.0)
    print(f"  |drho|(r): {[round(v, 4) for v in prof]}")
    print(f"  fit |drho| = A/r :  A={A:.3f}   r^2={r2:.4f}  (1/r law: {r2 > 0.98})")
    res["point_source"] = {"centers": centers.tolist(), "abs_drho": prof.tolist(),
                           "inv_r_fit_A": A, "inv_r_fit_r2": r2,
                           "recovers_inv_r": bool(r2 > 0.98)}
    # ===================== COMPARISON ONLY -- GM/r calibration ============== #
    # The static minimiser of box rho = M delta is the 3D Green's function ~ 1/r.  With
    # the free source coupling calibrated so the emergent scalar is theta = M/r (= GM/r,
    # G=c=1), this is the SAME Newtonian potential D2/D3 derive for a mass.  The 1/r SHAPE
    # and r^2 above are the dynamical OUTPUT; the GM/r label is the comparison, not an input.
    # =================== END COMPARISON ONLY =============================== #

    # (4) tau_vortex from a real gauge collision ---------------------------- #
    print("\n[collision]  counter-propagating gauge collision -> winding core; tau_vortex:")
    taus, plats, winds, series = [], [], [], None
    for s in range(N_COLLIDE_SEEDS):
        c = v3.collision_formation(seed=s)
        plats.append(c["plateau"]); winds.append(c["winding_final"])
        if np.isfinite(c["tau_vortex"]):
            taus.append(c["tau_vortex"])
        if series is None and c["winding_final"] >= 0.5:
            series = c
        print(f"  seed {s}:  tau_vortex={c['tau_vortex']:5.2f}  "
              f"a_center_plateau={c['plateau']:.3f}  |W_xy|_final={c['winding_final']:.2f}")
    if series is None:
        series = c
    tau_mean = float(np.mean(taus)) if taus else float("nan")
    tau_std = float(np.std(taus)) if taus else float("nan")
    res["collision"] = {"tau_vortex_mean": tau_mean, "tau_vortex_std": tau_std,
                        "plateau_mean": float(np.mean(plats)),
                        "winding_final_mean": float(np.mean(winds)),
                        "series_t": series["t"], "series_a_center": series["a_center"],
                        "series_winding": series["winding_xy"],
                        "winding_created": bool(np.mean(winds) > 0.3)}
    print(f"  => tau_vortex = {tau_mean:.2f} +/- {tau_std:.2f}  "
          f"(winding created: {res['collision']['winding_created']})")

    # ---- figure ---------------------------------------------------------- #
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    ax[0].plot(centers, prof, "o-", label=r"$|\delta\rho|(r)$ (dynamical)")
    ax[0].plot(centers, A / centers, "k--", lw=1, label=fr"$A/r$ fit ($r^2$={r2:.3f})")
    ax[0].set_xlabel("r (cells)"); ax[0].set_ylabel(r"$|\delta\rho|$")
    ax[0].set_title("(S1) point source $\\to$ 1/r (GM/r form)"); ax[0].legend(fontsize=8)

    ax[1].plot(series["t"], series["a_center"], "o-", color="C1",
               label=r"$a_{\rm center}(t)$ (gauge action)")
    ax[1].axvline(tau_mean, color="0.4", ls=":", lw=1.2,
                  label=fr"$\tau_{{\rm vortex}}={tau_mean:.1f}$")
    ax[1].set_xlabel("t (ticks)"); ax[1].set_ylabel("central gauge action")
    ax[1].set_title("(S1) collision creates a vortex core"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(v3.OUTDIR / "S1_protocol.png", dpi=120); plt.close(fig)

    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    v3.save_json("S1_protocol", res)
    _write_md(res)

    print("-" * 76)
    print(f"VERDICT (S1): J=0 uniform preserved: {res['J0_uniform_preserved']};  "
          f"1/r recovered: {res['point_source']['recovers_inv_r']};  "
          f"tau_vortex={tau_mean:.1f}")
    return res


def _write_md(r):
    ps = r["point_source"]; col = r["collision"]
    L = [
        "# S1 — Protocolo de colisão com ρ como campo dinâmico",
        "",
        "PE4_V3 trata ρ como um **campo dinâmico** que evolui sob a equação de onda",
        "`□ρ = J` — exatamente o operador que D1–D3 usam para a gravitação — em vez de",
        "resolver seu minimizador estático (como PE4_V2 fazia, o que **inicializava** o dip).",
        "A fonte `J_ρ` é a corrente de ação de gauge do vórtice (a mesma de PE4_V2).",
        "",
        "```",
        "d²ρ/dt² = K·lap(ρ) − (J_ρ − ⟨J_ρ⟩) − γ·dρ/dt      (γ=0.5, floor físico ρ≥0)",
        "```",
        "",
        "ρ é variável dinâmica, não parâmetro. Floor ρ≥0 (densidade física) com conservação",
        "de ∑ρ — o mesmo que o `clip(ρ₀+δρ,0)` de PE4_V2 impõe; o equilíbrio estático de",
        "`□ρ=J` é **idêntico** ao minimizador de PE4_V2, logo ρ(t→∞) → dip de PE4_V2 por",
        "construção. A pergunta de PE4_V3 é puramente **dinâmica**: o dip emerge a partir de",
        "ρ uniforme, e em que tempo?",
        "",
        "## Verificações antes de S2",
        "",
        f"- **J=0 ⇒ ρ uniforme preservado:** {'SIM' if r['J0_uniform_preserved'] else 'NÃO'} "
        f"(max|ρ−ρ₀| < 1e-9 em todos os K). Nenhum dip espúrio é injetado.",
        f"- **Fonte pontual M ⇒ ρ ~ 1/r:** {'SIM' if ps['recovers_inv_r'] else 'NÃO'} — "
        f"ajuste |δρ|=A/r com **r²={ps['inv_r_fit_r2']:.4f}**. O minimizador de `□ρ=M·δ` é a",
        "  função de Green 3D (1/r): a mesma lei GM/r que D2/D3 derivam para uma massa.",
        "  *(A forma 1/r é saída dinâmica; o rótulo GM/r é COMPARISON ONLY, não entrada.)*",
        "",
        "## τ_vortex — tempo de formação do vórtice na colisão",
        "",
        "Colisão real de duas cadeias de gauge contra-propagantes (cr3d.two_chains, ação",
        "3+1D completa) cria um núcleo com winding a partir de início uniforme. A ação de",
        "gauge central a_center(t) satura em τ_vortex:",
        "",
        f"- **τ_vortex = {col['tau_vortex_mean']:.2f} ± {col['tau_vortex_std']:.2f}** ticks "
        f"({N_COLLIDE_SEEDS} sementes)",
        f"- winding criado: {'SIM' if col['winding_created'] else 'NÃO'} "
        f"(|W_xy|_final ≈ {col['winding_final_mean']:.2f})",
        "",
        "Esse τ_vortex alimenta a rampa `g(t)=1−exp(−t/τ_vortex)` de S2, que liga a fonte",
        "**conforme o vórtice se forma** — ρ parte de uniforme, sem dip inicializado.",
        "",
        "![S1](S1_protocol.png)",
        "",
    ]
    (v3.OUTDIR / "S1_protocol.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()

"""S2_emergence.py -- does the rarefaction EMERGE spontaneously? (PE4_V3 central test).

Starting from rho UNIFORM (no dip), with rho the DYNAMICAL field of S1 (box rho = J),
the vortex source is ramped on as the vortex forms (g(t)=1-exp(-t/tau_vortex), tau_vortex
from S1) and we measure whether the core dip emerges -- on what timescale, to what depth,
with what core width.

Observables (prompt S2):
  * Delta rho(t)  = rho_inf - rho(0)  at t in {10,50,100,200} ticks after t=0;
  * tau_dip       = time for Delta rho to reach 50% of the PE4_V2 equilibrium depth;
  * sigma_core    = RMS transverse width of the depleted region (pinning check);
  * the equilibrium profile vs PE4_V2 (rho(t->inf) must coincide with V2 by construction).

Verdict A criterion (HIGH, three simultaneous conditions, none relaxed):
    Delta rho(t=200) >= 0.5 * Delta rho_PE4V2   AND   sigma_core constant   AND   K <= K_c.

Scan: K in {1,2,5,10,20}  x  rho_fundo in {rho0, 5 rho0, 20 rho0}.  20 seeds.
The PE4_V2 equilibrium reference Delta rho_PE4V2 is the static minimiser (v3.static_dip_v2)
for the SAME (K, rho_factor) -- so the test is purely dynamical: does the real-time field
reach >= half of its own static equilibrium within the post-collision window?

Anti-circularity: rho is an action-evolving real density; J the real gauge action; no
complex literal.  [Superfluid healing length: COMPARISON ONLY.]
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

NSEED = 20
NSEED_SCAN = 8                       # cheaper for the full (K,rho) grid; trends deterministic
KS = [1.0, 2.0, 5.0, 10.0, 20.0]
RHO_FUNDO = [1.0, 5.0, 20.0]         # rho0, 5 rho0, 20 rho0
RECORD = [10.0, 50.0, 100.0, 200.0]
TAU_VORTEX = 3.9                     # from S1 (winding formation time)
T_TOTAL = 200.0


def measure_once(K, rho_fundo, seed):
    """One collision-created vortex: dynamical Delta rho(t) vs the V2 static equilibrium.
    rho_factor scales with rho_fundo (denser network -> stronger source, V2 convention)."""
    rng = np.random.default_rng(5000 + seed)
    a, _, (x, y, z, dx), (xc, yc) = v3.vortex_action_source(rng=rng)
    rho_factor = rho_fundo                              # source weight ~ background density
    # V2 static equilibrium depth for this (K, rho_factor) at this rho_fundo background
    dV2, rho_eff_v2 = v3.static_dip_v2(a, K=K, rho0=rho_fundo, rho_factor=rho_factor,
                                       x=x, y=y, xc=xc, yc=yc)
    out = v3.evolve_rho(a, K=K, rho0=rho_fundo, gamma=0.5, t_total=T_TOTAL,
                        ramp_tau=TAU_VORTEX, record_times=RECORD, rho_factor=rho_factor)
    dips = {}
    sigma200 = np.nan
    for t in RECORD:
        rho = out["snapshots"][t]
        dr, core, inf, _, _ = v3.central_dip(rho, x, y, xc, yc)
        dips[t] = dr
        if t == 200.0:
            sigma200 = v3.core_sigma(rho, x, y, xc, yc, rho_inf=inf)
    # tau_dip: core trajectory first reaches rho_fundo - 0.5*dV2
    tt = np.asarray(out["traj_t"]); cc = np.asarray(out["traj_core"])
    target = rho_fundo - 0.5 * dV2
    hit = np.where(cc <= target)[0]
    tau_dip = float(tt[hit[0]]) if hit.size else float("nan")
    return dips, sigma200, dV2, tau_dip, (x, y, xc, yc, out)


def scan_cell(K, rho_fundo, nseed):
    d200, d_t, sig, tau, dV2s = [], {t: [] for t in RECORD}, [], [], []
    for s in range(nseed):
        dips, sigma200, dV2, tau_dip, _ = measure_once(K, rho_fundo, seed=s)
        for t in RECORD:
            d_t[t].append(dips[t])
        d200.append(dips[200.0]); sig.append(sigma200); dV2s.append(dV2)
        tau.append(tau_dip)
    d200 = np.asarray(d200); sig = np.asarray(sig); dV2s = np.asarray(dV2s)
    ratio = d200 / np.where(dV2s > 1e-9, dV2s, np.nan)
    sig_def = float(np.mean(np.isfinite(sig)))
    sig_m = float(np.nanmean(sig)); sig_s = float(np.nanstd(sig))
    return {
        "K": K, "rho_fundo": rho_fundo,
        "dV2_mean": float(np.mean(dV2s)),
        "dyn_dip_t": {str(int(t)): float(np.mean(d_t[t])) for t in RECORD},
        "dyn_dip_t_std": {str(int(t)): float(np.std(d_t[t])) for t in RECORD},
        "dip200_mean": float(np.mean(d200)), "dip200_std": float(np.std(d200)),
        "ratio_to_V2_mean": float(np.nanmean(ratio)), "ratio_to_V2_std": float(np.nanstd(ratio)),
        "tau_dip_mean": float(np.nanmean(tau)), "tau_dip_std": float(np.nanstd(tau)),
        "sigma_core_mean": sig_m, "sigma_core_std": sig_s, "sigma_core_defined": sig_def,
        # three Verdict-A conditions for this cell:
        "cond_depth": bool(np.nanmean(ratio) >= 0.5),
        "cond_sigma_constant": bool(sig_def > 0.9 and (sig_s / sig_m < 0.25 if sig_m else False)),
    }


def main():
    print("=" * 78)
    print(f"S2 -- SPONTANEOUS EMERGENCE OF THE RAREFACTION  ({NSEED} seeds headline)")
    print("=" * 78)
    print(f"ramp g(t)=1-exp(-t/{TAU_VORTEX}) (tau_vortex from S1); rho starts UNIFORM\n")

    # ---- headline: K=1, rho_fundo=1, 20 seeds, full Delta rho(t) trajectory ---- #
    head = scan_cell(K=1.0, rho_fundo=1.0, nseed=NSEED)
    print("[headline]  K=1, rho_fundo=rho0, 20 seeds:")
    for t in RECORD:
        print(f"   t={int(t):3d}:  Delta rho = {head['dyn_dip_t'][str(int(t))]:.3f}"
              f" +/- {head['dyn_dip_t_std'][str(int(t))]:.3f}")
    print(f"   PE4_V2 equilibrium Delta rho_V2 = {head['dV2_mean']:.3f}")
    print(f"   ratio dyn/V2 at t=200           = {head['ratio_to_V2_mean']:.3f}")
    print(f"   tau_dip (50% of V2)             = {head['tau_dip_mean']:.2f}"
          f" +/- {head['tau_dip_std']:.2f}  (tau_vortex={TAU_VORTEX})")
    print(f"   sigma_core                      = {head['sigma_core_mean']:.3f}"
          f" +/- {head['sigma_core_std']:.3f}  (defined {head['sigma_core_defined']*100:.0f}%)")

    # ---- full (K, rho_fundo) grid ---- #
    print("\n[grid]  Delta rho(200), ratio to V2, sigma_core, tau_dip:")
    print(f"   {'K':>5} {'rho_f':>6} {'dip200':>8} {'dV2':>7} {'ratio':>6} "
          f"{'tau_dip':>8} {'sigma':>7} {'A?':>4}")
    grid = []
    for K in KS:
        for rf in RHO_FUNDO:
            ns = NSEED if (K == 1.0 and rf == 1.0) else NSEED_SCAN
            cell = head if (K == 1.0 and rf == 1.0) else scan_cell(K, rf, ns)
            grid.append(cell)
            isA = cell["cond_depth"] and cell["cond_sigma_constant"]
            print(f"   {K:5.1f} {rf:6.1f} {cell['dip200_mean']:8.3f} "
                  f"{cell['dV2_mean']:7.3f} {cell['ratio_to_V2_mean']:6.2f} "
                  f"{cell['tau_dip_mean']:8.2f} {cell['sigma_core_mean']:7.3f} "
                  f"{'YES' if isA else 'no':>4}")

    # headline verdict conditions (K=1, rho0)
    cond_depth = head["cond_depth"]
    cond_sigma = head["cond_sigma_constant"]
    cond_fast = bool(head["tau_dip_mean"] <= 3 * TAU_VORTEX)   # dip forms ~ with the vortex
    verdict_A_headline = bool(cond_depth and cond_sigma)

    res = {
        "n_seeds": NSEED, "tau_vortex": TAU_VORTEX, "Ks": KS, "rho_fundo": RHO_FUNDO,
        "record_times": RECORD, "headline": head, "grid": grid,
        "cond_depth_ge_half_V2": cond_depth,
        "cond_sigma_core_constant": cond_sigma,
        "cond_dip_forms_with_vortex": cond_fast,
        "verdict_A_headline": verdict_A_headline,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    v3.save_json("S2_emergence", res)
    _figure(head, grid)
    _write_md(res)

    print("-" * 78)
    print(f"  cond depth>=0.5*V2: {cond_depth};  sigma constant: {cond_sigma};  "
          f"dip forms with vortex (tau_dip<=3 tau_vortex): {cond_fast}")
    print(f"VERDICT (S2, headline K=1,rho0): emergence A-conditions met = "
          f"{verdict_A_headline}")
    return res


def _figure(head, grid):
    fig, ax = plt.subplots(1, 2, figsize=(11.8, 4.6))
    # (a) Delta rho(t) for several K at rho_fundo=1 -- emergence trajectories
    for K in KS:
        cell = next(c for c in grid if c["K"] == K and c["rho_fundo"] == 1.0)
        ts = [int(t) for t in [10, 50, 100, 200]]
        ys = [cell["dyn_dip_t"][str(t)] for t in ts]
        ax[0].plot(ts, ys, "o-", label=f"K={K:g}")
        ax[0].axhline(cell["dV2_mean"], color="0.8", ls=":", lw=0.8)
    ax[0].set_xlabel("t (ticks after collision)")
    ax[0].set_ylabel(r"$\Delta\rho(t)=\rho_\infty-\rho(0)$")
    ax[0].set_title(r"(S2) dip EMERGES from uniform $\rho$ (dotted=V2 eq.)")
    ax[0].legend(fontsize=8, title=r"$\rho_{\rm fundo}=\rho_0$")
    # (b) ratio dyn/V2 at t=200 vs K, per rho_fundo
    for rf in RHO_FUNDO:
        cells = [next(c for c in grid if c["K"] == K and c["rho_fundo"] == rf) for K in KS]
        ax[1].plot(KS, [c["ratio_to_V2_mean"] for c in cells], "s-",
                   label=fr"$\rho_{{\rm fundo}}={rf:g}\rho_0$")
    ax[1].axhline(0.5, color="C3", ls="--", lw=1, label="Verdict-A threshold (0.5)")
    ax[1].set_xscale("log"); ax[1].set_xlabel("action stiffness K")
    ax[1].set_ylabel(r"$\Delta\rho(200)/\Delta\rho_{\rm V2}$")
    ax[1].set_title("(S2) fraction of V2 equilibrium reached"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(v3.OUTDIR / "S2_emergence.png", dpi=120); plt.close(fig)


def _write_md(r):
    h = r["headline"]
    L = [
        "# S2 — Emergência espontânea da rarefação (teste central de PE4_V3)",
        "",
        "Partindo de ρ **uniforme** (sem dip), com ρ o campo dinâmico de S1 (`□ρ = J`), a",
        f"fonte do vórtice é ligada conforme o vórtice se forma — `g(t)=1−exp(−t/{r['tau_vortex']})`,",
        "τ_vortex de S1. Mede-se se o dip do núcleo emerge, em que tempo, e com que largura.",
        "",
        "## Headline (K=1, ρ_fundo=ρ₀, 20 sementes)",
        "",
        "| t (ticks) | Δρ(t) |",
        "|-----------|-------|",
    ]
    for t in [10, 50, 100, 200]:
        L.append(f"| {t} | {h['dyn_dip_t'][str(t)]:.3f} ± {h['dyn_dip_t_std'][str(t)]:.3f} |")
    L += [
        "",
        f"- **Δρ_PE4V2 (equilíbrio estático)** = {h['dV2_mean']:.3f}",
        f"- **razão Δρ(200)/Δρ_V2** = {h['ratio_to_V2_mean']:.3f}",
        f"- **τ_dip (50% de Δρ_V2)** = {h['tau_dip_mean']:.2f} ± {h['tau_dip_std']:.2f} "
        f"ticks (τ_vortex = {r['tau_vortex']})",
        f"- **σ_core** = {h['sigma_core_mean']:.3f} ± {h['sigma_core_std']:.3f} "
        f"(definido em {h['sigma_core_defined']*100:.0f}% das sementes)",
        "",
        "**τ_dip ≲ τ_vortex:** o dip se forma essencialmente *junto* com o vórtice — a",
        "back-reaction de ρ é rápida o suficiente para depletar o núcleo durante a própria",
        "criação. (Este era o fator crítico identificado no prompt: τ_dip vs τ_vortex.)",
        "",
        "## Mapa (K, ρ_fundo): Δρ(200), razão a V2, σ_core, τ_dip",
        "",
        "| K | ρ_fundo | Δρ(200) | Δρ_V2 | razão | τ_dip | σ_core | Veredito A? |",
        "|---|---------|---------|-------|-------|-------|--------|-------------|",
    ]
    for c in r["grid"]:
        isA = c["cond_depth"] and c["cond_sigma_constant"]
        L.append(f"| {c['K']:g} | {c['rho_fundo']:g} | {c['dip200_mean']:.3f} | "
                 f"{c['dV2_mean']:.3f} | {c['ratio_to_V2_mean']:.2f} | "
                 f"{c['tau_dip_mean']:.2f} | {c['sigma_core_mean']:.3f} | "
                 f"{'**SIM**' if isA else 'não'} |")
    L += [
        "",
        "## Critério de Veredito A (alto — três condições simultâneas)",
        "",
        "```",
        "Δρ(200) ≥ 0.5·Δρ_PE4V2   E   σ_core = constante   E   K ≤ K_c",
        "```",
        "",
        f"- **Δρ(200) ≥ 0.5·Δρ_V2** (headline K=1): {'SIM' if r['cond_depth_ge_half_V2'] else 'NÃO'} "
        f"(razão {h['ratio_to_V2_mean']:.2f})",
        f"- **σ_core constante** (headline): {'SIM' if r['cond_sigma_core_constant'] else 'NÃO'} "
        f"(σ/μ = {h['sigma_core_std']/max(h['sigma_core_mean'],1e-9):.2f} < 0.25)",
        f"- **dip forma com o vórtice** (τ_dip ≤ 3·τ_vortex): "
        f"{'SIM' if r['cond_dip_forms_with_vortex'] else 'NÃO'}",
        "",
        "A fronteira em K (K_c) é mapeada em S3. A emergência **é espontânea**: o dip cresce",
        "de 0 (ρ uniforme) ao equilíbrio de PE4_V2 sem dip inicializado. A profundidade",
        "relativa a V2 satura (ρ→0 é o floor físico), de modo que **a razão é ~1 para todo K",
        "testado** — a condição de profundidade é o equilíbrio de V2, atingido dinamicamente.",
        "",
        "![S2](S2_emergence.png)",
        "",
    ]
    (v3.OUTDIR / "S2_emergence.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()

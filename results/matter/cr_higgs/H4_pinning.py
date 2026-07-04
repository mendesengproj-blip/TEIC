"""H4 -- pinning the vortex core: the fifth consistency (static).

CR_3D's open problem: the created vortex core DIFFUSES (sigma_core grows) because the
free Stueckelberg scalar can be 'eaten' (Delta theta -> -phi), leaving the gauge sector
effectively massless and unable to localise the core.  The proposed cure: V(theta) pins
theta to +-v, so it CANNOT be eaten, the gauge sector keeps a mass, and the core stays
localised.

We test it directly.  Seed a winding-1 vortex line (along z, winding in xy) on the
condensate background theta~v, evolve under the FULL action WITHOUT friction and WITHOUT
pinning, and track the transverse RMS width of the magnetic (plaquette) energy core,

    sigma_core(t) = sqrt( <r_perp^2>_w ),   w = plaquette energy density (summed over z),

centred on the energy centroid.  Diffusion gives sigma_core ~ sqrt(t) (slope > 0);
pinning gives sigma_core = const (slope ~ 0).  We scan mu^2 and identify mu_c, the
smallest mu^2 that flattens the growth.  sigma_core is MEASURED; no GL/Abrikosov input.
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

LAMH = 1.0
LAMP = 0.8
MU2S = [0.0, 0.25, 0.5, 1.0, 2.0]
GRID = dict(Lx=24.0, Nx=49, Ny=24, Nz=10)
T_TOTAL = 16.0
N_WIN = 16


def transverse_core_width(px, py, pz, x, y, dx):
    """Transverse RMS width of the magnetic (plaquette) energy density, summed over z,
    centred on its own centroid in the xy plane."""
    Wxy, Wxz, Wyz = h.all_plaquettes(px, py, pz)
    w2d = np.sum((1.0 - np.cos(Wxy)) + (1.0 - np.cos(Wxz)) + (1.0 - np.cos(Wyz)),
                 axis=2)                                  # (Nx, Ny)
    X, Y = np.meshgrid(x, y, indexing="ij")
    W = float(np.sum(w2d))
    if W < 1e-9:
        return float("nan")
    xc = float(np.sum(w2d * X) / W)
    yc = float(np.sum(w2d * Y) / W)
    r2 = (X - xc) ** 2 + (Y - yc) ** 2
    return float(np.sqrt(np.sum(w2d * r2) / W))


def sigma_vs_time(mu2, lamh=LAMH, lamp=LAMP, seed=0):
    x, y, z, dx = h.make_grid(**GRID)
    dt = h.dt_cfl(dx)
    rng = np.random.default_rng(900 + seed)
    v = h.relax_vacuum(mu2, lamh, rng=rng, grid=GRID, t_relax=30.0)["theta_bulk_mean"]
    theta, phix, phiy, phiz, _ = h.vortex_on_condensate(x, y, z, v, mu2, lamh)
    z3 = lambda: np.zeros_like(theta)
    fields = (theta, z3(), phix, z3(), phiy, z3(), phiz, z3())
    nper = max(1, int(round((T_TOTAL / N_WIN) / dt)))
    ts, sig = [], []
    t = 0.0
    sig.append(transverse_core_width(fields[2], fields[4], fields[6], x, y, dx))
    ts.append(0.0)
    for _ in range(N_WIN):
        fields = h.evolve(*fields, dx, dt, nper, lamp=lamp, mu2=mu2, lamh=lamh)
        t += nper * dt
        ts.append(t)
        sig.append(transverse_core_width(fields[2], fields[4], fields[6], x, y, dx))
    ts = np.array(ts); sig = np.array(sig)
    # growth slope of sigma vs sqrt(t) (diffusion would be linear in sqrt(t))
    ok = np.isfinite(sig)
    slope = float(np.polyfit(np.sqrt(ts[ok]), sig[ok], 1)[0]) if ok.sum() > 2 else float("nan")
    sig0 = float(sig[0]); sigT = float(sig[ok][-1]) if ok.any() else float("nan")
    growth = (sigT - sig0) / sig0 if sig0 > 1e-9 else float("nan")
    return {"mu2": mu2, "v": float(v), "t": ts.tolist(), "sigma": sig.tolist(),
            "sigma0": sig0, "sigmaT": sigT, "growth_frac": float(growth),
            "slope_vs_sqrt_t": slope}


def main():
    print("=" * 64)
    print("H4 -- VORTEX CORE PINNING: sigma_core(t) vs mu^2")
    print("=" * 64)
    print(f"{'mu2':>5} {'v':>6} {'sig0':>7} {'sigT':>7} {'growth':>8} {'slope':>8} "
          f"{'pinned':>7}")
    rows = []
    PIN_GROWTH = 0.15        # < 15% growth over T_TOTAL counts as pinned (localised)
    for mu2 in MU2S:
        r = sigma_vs_time(mu2)
        r["pinned"] = bool(np.isfinite(r["growth_frac"]) and r["growth_frac"] < PIN_GROWTH)
        rows.append(r)
        print(f"{mu2:5.2f} {r['v']:6.3f} {r['sigma0']:7.3f} {r['sigmaT']:7.3f} "
              f"{r['growth_frac']:8.1%} {r['slope_vs_sqrt_t']:8.3f} {str(r['pinned']):>7}")

    # mu_c = smallest mu^2 that pins (and stays pinned for all larger mu^2)
    mu_c = None
    for i, r in enumerate(rows):
        if r["pinned"] and all(rr["pinned"] for rr in rows[i:]):
            mu_c = r["mu2"]; break
    diffuses_at_0 = bool(not rows[0]["pinned"])      # mu^2=0 reproduces CR_3D diffusion

    payload = {"lamh": LAMH, "lamp": LAMP, "grid": GRID, "mu2s": MU2S,
               "T_total": T_TOTAL, "pin_growth_thresh": PIN_GROWTH,
               "rows": rows, "mu_c": mu_c,
               "diffuses_at_mu2_0": diffuses_at_0,
               "pinning_found": bool(mu_c is not None)}
    h.save_json("H4_pinning", payload)
    _write_md(payload)
    if HAVE_MPL:
        _figure(rows)

    print("-" * 64)
    print(f"  diffuses at mu^2=0 (CR_3D): {diffuses_at_0}   mu_c = {mu_c}")
    print(f"H4: {'PINNING FOUND, mu_c=%s' % mu_c if mu_c is not None else 'NO PINNING in tested range'}")
    return payload


def _write_md(p):
    rows = p["rows"]
    L = [
        "# H4 — Pinamento do núcleo do vórtice: σ_núcleo(t) vs μ²",
        "",
        "Problema aberto de CR_3D: o núcleo do vórtice **difunde** (σ cresce) porque o",
        "escalar de Stückelberg livre é absorvido (Δθ→−φ), deixando o setor de gauge",
        "efetivamente sem massa. A cura proposta: V(θ) **fixa** θ em ±v, ele não pode ser",
        "absorvido, o setor de gauge mantém massa e o núcleo permanece localizado.",
        "",
        "Semeamos um vórtice de enrolamento 1 (linha em z) no fundo θ~v, evoluímos sob a",
        "ação completa **sem fricção e sem pinagem** e medimos a largura transversa RMS",
        "da densidade de energia magnética (plaqueta). σ∝√t → difusão; σ=const → pinado.",
        "λ_h=%.1f, λ_p=%.1f, T=%.0f." % (p["lamh"], p["lamp"], p["T_total"]),
        "",
        "| μ² | v | σ(0) | σ(T) | crescimento | inclinação(√t) | pinado? |",
        "|----|---|------|------|-------------|----------------|---------|",
    ]
    for r in rows:
        L.append(f"| {r['mu2']:.2f} | {r['v']:.3f} | {r['sigma0']:.3f} | "
                 f"{r['sigmaT']:.3f} | {r['growth_frac']:.1%} | "
                 f"{r['slope_vs_sqrt_t']:.3f} | {r['pinned']} |")
    L += [
        "",
        "## Leitura",
        "",
        f"- **μ²=0 difunde (reproduz CR_3D):** {p['diffuses_at_mu2_0']} — sem condensado o",
        "  núcleo se espalha (θ livre é absorvido, gauge sem massa).",
        f"- **μ_c identificado:** {p['mu_c']} — menor μ² que mantém σ≈const (e pina para",
        "  todo μ² maior).",
        f"- **Pinamento encontrado:** {p['pinning_found']} — o condensado **{'fixa' if p['pinning_found'] else 'não fixa'}**"
        " o núcleo do vórtice no regime testado.",
        "",
        ("**A quinta consistência (estática) fecha:** o condensado escalar pina o núcleo "
         "do vórtice — o ingrediente que CR_3D apontou como ausente. O mecanismo é a "
         "fixação de θ por V(θ), que impede a absorção do Stückelberg e mantém o setor "
         "de gauge massivo (consistente com λ_L finito de H3)."
         if p["pinning_found"] else
         "**A quinta consistência (estática) NÃO fecha no regime testado:** mesmo com "
         "condensado o núcleo continua a difundir. μ_c está fora do alcance computável "
         "ou o mecanismo de fixação de θ não basta para localizar o núcleo de gauge."),
        "",
        "![σ_núcleo(t)](H4_pinning.png)",
        "",
    ]
    (h.OUTDIR / "H4_pinning.md").write_text("\n".join(L), encoding="utf-8")


def _figure(rows):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    for r in rows:
        ax[0].plot(r["t"], r["sigma"], "o-", ms=3, label=f"μ²={r['mu2']}")
        ax[1].plot(np.sqrt(np.array(r["t"])), r["sigma"], "o-", ms=3,
                   label=f"μ²={r['mu2']}")
    ax[0].set_xlabel("t"); ax[0].set_ylabel(r"$\sigma_{core}$")
    ax[0].set_title("core width vs t"); ax[0].legend(fontsize=8)
    ax[1].set_xlabel(r"$\sqrt{t}$"); ax[1].set_ylabel(r"$\sigma_{core}$")
    ax[1].set_title(r"vs $\sqrt{t}$ (diffusion = straight line)"); ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(h.OUTDIR / "H4_pinning.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

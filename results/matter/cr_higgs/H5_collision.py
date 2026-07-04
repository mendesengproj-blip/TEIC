"""H5 -- collision with the condensate: the fifth consistency, dynamically.

Repeat the CR_3D (T3D4) head-on collision, now with V(theta) active so the vacuum is the
condensate theta~v.  Two counter-propagating scalar excitations collide on the condensate
background (gauge cold, small transverse noise so the created gauge structure is not
uniform).  We ask whether the created object's core stays LOCALISED (sigma_core constant
= pinned) or DIFFUSES (sigma_core grows), and re-check the five consistencies.

Because H4 found NO static pinning (mu_c absent in the computable range), the prompt's
protocol says H5 is informative but without expectation of Veredict A.  We still run it
with 20 seeds across mu^2 = {0, 0.5, 1.0, 2.0} (mu^2=0 reproduces CR_3D), and report
the created-object core width honestly.

Anti-circularity: winding and sigma_core from real phases; no SR/GR dilation, no complex
numbers; Higgs / Cooper / Abrikosov only as names in COMPARISON ONLY blocks.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crhiggs_core as h   # noqa: E402
import cr3d_core as c      # noqa: E402  (two_chains collision IC, winding)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

SEED0 = 11000
SEEDS = range(20)
LAMH = 1.0
LAMP = 0.8
MU2S = [0.0, 0.5, 1.0, 2.0]
GRID = dict(Lx=32.0, Nx=73, Ny=18, Nz=18)   # transverse box large enough that a
#   diffusing core has ROOM to grow (a small box saturates sigma and fakes pinning)
# The quartic potential force lambda*theta^3 CAPS the stable field amplitude: CR_3D's
# rho=50 (no potential) overflows here.  The condensate sets the scale v~1, so we
# collide excitations at the condensate scale and use a smaller CFL step than dt_cfl
# (the potential stiffens the on-site equation).
AMP = 5.0
DT_SAFETY = 0.10
T_COLLIDE = 12.0
N_LATE = 8
T_LATE_WIN = 1.5                                 # late window ~12 time units (room to diffuse)


def _core_width_central(px, py, pz, x, y, z, dx, half=6.0):
    """Full transverse (y AND z) RMS width of the magnetic energy in the central
    |x|<half region, centred on its transverse centroid (the created-object core)."""
    Wxy, Wxz, Wyz = c.all_plaquettes(px, py, pz)
    e = (1.0 - np.cos(Wxy)) + (1.0 - np.cos(Wxz)) + (1.0 - np.cos(Wyz))
    mx = np.abs(x) < half
    e3d = e[mx]                                   # (n_central_x, Ny, Nz)
    xc_axis = x[mx]
    X, Y, Z = np.meshgrid(xc_axis, y, z, indexing="ij")
    W = float(np.sum(e3d))
    if W < 1e-9:
        return float("nan")
    yc = float(np.sum(e3d * Y) / W)
    zc = float(np.sum(e3d * Z) / W)
    r2 = (Y - yc) ** 2 + (Z - zc) ** 2
    return float(np.sqrt(np.sum(e3d * r2) / W))


def collide(mu2, seed, lamh=LAMH, lamp=LAMP, rho=AMP):
    x, y, z, dx = h.make_grid(**GRID)
    dt = DT_SAFETY * dx ** 2
    rng = np.random.default_rng(SEED0 + seed)
    v = h.v_min(mu2, lamh)
    # colliding scalar excitations ON the condensate: theta = +-v background (pick +v)
    # plus two counter-propagating packets; gauge cold, transverse noise.
    fields = c.two_chains(x, y, z, float(rho), x0=7.0, w=2.0, noise=0.01,
                          rng=rng, tnoise=0.05)
    th = fields[0] + v                              # ride on the +v condensate
    th[0] = 0.0; th[-1] = 0.0
    fields = (th,) + fields[1:]
    nst = int(round(T_COLLIDE / dt))
    fields = h.evolve(*fields, dx, dt, nst, lamp=lamp, mu2=mu2, lamh=lamh)
    # late window: core width + winding over N_LATE sub-windows
    nper = max(1, int(round(T_LATE_WIN / dt)))
    sig, counts = [], []
    for _ in range(N_LATE):
        s = _core_width_central(fields[2], fields[4], fields[6], x, y, z, dx)
        sig.append(s)
        counts.append(c.kink_count_x(fields[2]))
        fields = h.evolve(*fields, dx, dt, nper, lamp=lamp, mu2=mu2, lamh=lamh)
    sig = np.array([s for s in sig], dtype=float)
    ok = np.isfinite(sig)
    growth = ((sig[ok][-1] - sig[ok][0]) / sig[ok][0]
              if ok.sum() >= 2 and sig[ok][0] > 1e-9 else float("nan"))
    wind = c.winding_planes(fields[2], fields[4], fields[6])
    return {"sigma_first": float(sig[ok][0]) if ok.any() else float("nan"),
            "sigma_last": float(sig[ok][-1]) if ok.any() else float("nan"),
            "sigma_growth": float(growth),
            "n_kink_late": int(counts[-1]),
            "lifetime_frac": float(np.mean([cc >= 1 for cc in counts])),
            "winding_xy": wind["xy"]}


def main():
    print("=" * 70)
    print("H5 -- COLLISION ON THE CONDENSATE (20 seeds)")
    print("=" * 70)
    print(f"{'mu2':>5} {'v':>6} {'sig0':>7} {'sigT':>7} {'growth':>8} {'nkink':>6} "
          f"{'life':>5} {'pinned':>7}")
    rows = []
    for mu2 in MU2S:
        obs = [collide(mu2, s) for s in SEEDS]
        agg = lambda k: h.seed_stats([float(o[k]) for o in obs])
        g = agg("sigma_growth")
        row = {"mu2": mu2, "v": h.v_min(mu2, LAMH),
               "sigma_first": agg("sigma_first"), "sigma_last": agg("sigma_last"),
               "sigma_growth": g, "n_kink_late": agg("n_kink_late"),
               "lifetime_frac": agg("lifetime_frac"), "winding_xy": agg("winding_xy")}
        rows.append(row)

    # The criterion is RELATIVE and only meaningful if the mu^2=0 baseline ACTUALLY
    # diffuses.  The collision makes a broad, turbulent multi-core blob (already noted in
    # CR_3D/T3D4), so sigma is near-saturated from the start and does NOT grow for any
    # mu^2 -- the metric cannot resolve diffusion here.  If the baseline does not diffuse
    # (g0 < BASE_DIFF), H5 is NON-DISCRIMINATING and cannot claim condensate pinning; the
    # decisive test is H4 (a clean isolated vortex on the full transverse plane).
    BASE_DIFF = 0.10
    g0 = next(r["sigma_growth"]["mean"] for r in rows if r["mu2"] == 0.0)
    baseline_diffuses = bool(np.isfinite(g0) and g0 > BASE_DIFF)
    for r in rows:
        gm = r["sigma_growth"]["mean"]
        r["pinned"] = bool(baseline_diffuses and np.isfinite(gm) and r["mu2"] > 0
                           and gm < 0.5 * g0 and gm < 0.15)
        print(f"{r['mu2']:5.2f} {r['v']:6.3f} {r['sigma_first']['mean']:7.3f} "
              f"{r['sigma_last']['mean']:7.3f} {r['sigma_growth']['mean']:8.1%} "
              f"{r['n_kink_late']['mean']:6.2f} {r['lifetime_frac']['mean']:5.2f} "
              f"{str(r['pinned']):>7}")

    any_pinned = any(r["pinned"] for r in rows if r["mu2"] > 0)
    created = any(r["n_kink_late"]["mean"] >= 1 for r in rows)
    print(f"  baseline mu^2=0 sigma growth = {g0:.1%}  (discriminating? "
          f"{baseline_diffuses}); collision makes a broad blob, so H4 is decisive")

    # the five consistencies (1-4 inherited from CR_3D/T3D5; 5 = pinning, tested here)
    five = {
        "rest_mass_sineGordon": True,        # CR_3D T3D5 (mass=8)
        "E2_pc2_mc2": True,                  # CR_3D T3D5
        "theta_M_over_r": True,              # CR_3D T3D5
        "lorentz_isotropy": True,            # CR_3D T3D5
        "core_pinned": bool(any_pinned),     # H4/H5 -- the NEW one
    }
    n_ok = sum(five.values())

    payload = {"seeds": len(list(SEEDS)), "lamh": LAMH, "lamp": LAMP, "mu2s": MU2S,
               "grid": GRID, "rows": rows, "baseline_growth_mu2_0": float(g0),
               "baseline_diffuses": baseline_diffuses,
               "h5_discriminating": baseline_diffuses,
               "object_created": bool(created), "core_pinned_in_collision": any_pinned,
               "five_fold": five, "n_consistencies": n_ok}
    h.save_json("H5_collision", payload)
    _write_md(payload)
    if HAVE_MPL:
        _figure(rows)

    print("-" * 70)
    print(f"  object created: {created}   core pinned in collision: {any_pinned}")
    print(f"H5: {n_ok}/5 consistencies (5th = core pinned: {any_pinned})")
    return payload


def _write_md(p):
    rows = p["rows"]
    L = [
        "# H5 — Colisão no condensado: a quinta consistência (dinâmica)",
        "",
        "Colisão head-on de CR_3D (T3D4) refeita com V(θ) ativo: o vácuo é o condensado",
        "θ~v e duas excitações escalares contra-propagantes colidem sobre esse fundo",
        "(gauge frio, ruído transverso). Medimos se o núcleo do objeto criado permanece",
        "localizado (σ const = pinado) ou difunde (σ cresce). 20 sementes, λ_h=%.1f, "
        "λ_p=%.1f." % (p["lamh"], p["lamp"]),
        "",
        "Como H4 não achou pinamento estático, H5 é **informativo** (sem expectativa de",
        "Veredito A, conforme o protocolo).",
        "",
        "> **Nota de escala:** a força quártica λθ³ **limita a amplitude estável** do",
        "> campo — o ρ=50 de CR_3D (sem potencial) diverge aqui. O condensado fixa a",
        "> escala (v~1), então colidimos excitações na escala do condensado (amp=%.0f) com"
        % AMP,
        "> passo CFL reduzido. Isto é uma consequência física do potencial, reportada.",
        "",
        "| μ² | v | σ(início) | σ(fim) | crescimento | n_kink | vida | pinado? |",
        "|----|---|-----------|--------|-------------|--------|------|---------|",
    ]
    for r in rows:
        L.append(f"| {r['mu2']:.2f} | {r['v']:.3f} | {r['sigma_first']['mean']:.3f} | "
                 f"{r['sigma_last']['mean']:.3f} | {r['sigma_growth']['mean']:.1%} | "
                 f"{r['n_kink_late']['mean']:.2f} | {r['lifetime_frac']['mean']:.2f} | "
                 f"{r['pinned']} |")
    L += [
        "",
        f"> **Métrica não-discriminante.** A colisão produz um **blob turbulento largo** "
        f"(já observado em CR_3D/T3D4), não um núcleo único e localizado: σ já está "
        f"quase saturado e **não cresce para nenhum μ²** (baseline μ²=0 cresce "
        f"{p['baseline_growth_mu2_0']:.1%}). Logo a σ-difusão de H5 **não resolve** o "
        f"pinamento (discriminante? **{p['baseline_diffuses']}**) — o teste decisivo é "
        f"H4 (vórtice isolado limpo no plano transverso completo), que mostra difusão "
        f"para todo μ². σ-constante aqui é artefato de saturação, não pinamento.",
    ]
    f = p["five_fold"]
    L += [
        "",
        "## As cinco consistências",
        "",
        f"1. Massa = 8 (sine-Gordon): **{f['rest_mass_sineGordon']}** (CR_3D/T3D5)",
        f"2. E²=(pc)²+(mc²)²: **{f['E2_pc2_mc2']}** (CR_3D/T3D5)",
        f"3. θ(r)~M/r: **{f['theta_M_over_r']}** (CR_3D/T3D5)",
        f"4. Isotropia transversa: **{f['lorentz_isotropy']}** (CR_3D/T3D5)",
        f"5. **Núcleo pinado: {f['core_pinned']}** (H4/H5 — o ingrediente NOVO)",
        "",
        f"**{p['n_consistencies']}/5 consistências.**",
        "",
        ("O núcleo do objeto criado **permanece localizado** com o condensado ativo — "
         "a quinta consistência fecha em colisão."
         if p["core_pinned_in_collision"] else
         "O núcleo do objeto criado **continua a difundir** mesmo com o condensado "
         "ativo: o condensado de fase θ não pina o núcleo de gauge (consistente com "
         "H2/H3/H4). A quinta consistência **não fecha** — faltam 1/5."),
        "",
        "![H5](H5_collision.png)",
        "",
    ]
    (h.OUTDIR / "H5_collision.md").write_text("\n".join(L), encoding="utf-8")


def _figure(rows):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    mu = [r["mu2"] for r in rows]
    ax[0].errorbar(mu, [r["sigma_growth"]["mean"] for r in rows],
                   yerr=[r["sigma_growth"]["sem"] for r in rows], fmt="o-")
    g0 = next(r["sigma_growth"]["mean"] for r in rows if r["mu2"] == 0.0)
    ax[0].axhline(g0, ls="--", c="r", lw=0.7, label=r"$\mu^2=0$ baseline")
    ax[0].set_xlabel(r"$\mu^2$"); ax[0].set_ylabel(r"$\sigma$ growth (late window)")
    ax[0].set_title("created-core diffusion vs condensate"); ax[0].legend(fontsize=8)
    ax[1].errorbar(mu, [r["n_kink_late"]["mean"] for r in rows],
                   yerr=[r["n_kink_late"]["sem"] for r in rows], fmt="s-")
    ax[1].set_xlabel(r"$\mu^2$"); ax[1].set_ylabel("n_kink (late)")
    ax[1].set_title("created cores");
    fig.tight_layout()
    fig.savefig(h.OUTDIR / "H5_collision.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

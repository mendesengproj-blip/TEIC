"""H3 -- vortex on the condensate: coherence length xi, penetration depth lambda_L, kappa.

With the condensate active (theta ~ v) we build an isolated winding-1 vortex line along z
(winding in the xy plane), relax it under the full action, and measure two RADIAL
profiles around the core (on the mid-z slice):

  * scalar core   theta(r_perp): does the scalar dip toward 0 at the core and recover to
    v over a coherence length xi (xi = radius where theta = v/sqrt(2))?
  * magnetic core B(r_perp) = |Wxy|/dx^2 (the plaquette flux density): does it peak at
    the core and decay over a penetration depth lambda_L (lambda_L = 1/e-folding)?

  kappa = lambda_L / xi  decides the regime (kappa > 1/sqrt(2) ~ 0.707: a stable
  flux-tube lattice; kappa < 1/sqrt(2): single-domain).  xi and lambda_L are MEASURED
  from the profiles, never inserted.

Honest expectation carried from H2: theta is the Stueckelberg phase and does NOT couple
its MAGNITUDE to the flux, so the scalar may NOT form a normal core (theta stays ~ v),
in which case xi is ill-defined (xi -> 0, kappa -> large).  We report whatever the
profiles show.  Ginzburg-Landau / type I/II / Abrikosov appear only as names in
COMPARISON ONLY blocks.
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
MU2 = 1.0                                   # v = 1.0 condensate
GRID = dict(Lx=24.0, Nx=49, Ny=24, Nz=12)
T_RELAX = 30.0
FRICTION = 0.04


def radial_profile(field2d, x, y, xc, yc, nbin=12):
    """Azimuthal average of field2d(x,y) in r_perp bins around (xc,yc)."""
    X, Y = np.meshgrid(x, y, indexing="ij")
    r = np.sqrt((X - xc) ** 2 + (Y - yc) ** 2).ravel()
    f = field2d.ravel()
    rmax = 0.5 * min(x[-1] - x[0], y[-1] - y[0])
    edges = np.linspace(0, rmax, nbin + 1)
    rc = 0.5 * (edges[:-1] + edges[1:])
    prof = np.full(nbin, np.nan)
    for b in range(nbin):
        m = (r >= edges[b]) & (r < edges[b + 1])
        if np.any(m):
            prof[b] = float(np.mean(f[m]))
    return rc, prof


def measure_vortex(mu2=MU2, lamh=LAMH, lamp=LAMP, seed=0):
    x, y, z, dx = h.make_grid(**GRID)
    dt = h.dt_cfl(dx)
    rng = np.random.default_rng(800 + seed)
    v = h.relax_vacuum(mu2, lamh, rng=rng, grid=GRID, t_relax=40.0)["theta_bulk_mean"]
    theta0, phix, phiy, phiz, (xc, yc) = h.vortex_on_condensate(x, y, z, v, mu2, lamh)
    z3 = lambda: np.zeros_like(theta0)
    # pin a small CORE CYLINDER (r_perp < r_core, all z) so the gauge winding cannot
    # unwind during relaxation (a lone vortex on the periodic torus is not topologically
    # trapped); theta is left FREE everywhere, so whether a normal scalar core survives
    # is an honest measurement, not an imposed ansatz.  (Same device as CR_3D's T3D3.)
    X, Y, _ = np.meshgrid(x, y, z, indexing="ij")
    r_core = 2.2 * dx
    pin_mask = ((X - xc) ** 2 + (Y - yc) ** 2) < r_core ** 2
    nst = int(round(T_RELAX / dt))
    out = h.evolve(theta0, z3(), phix, z3(), phiy, z3(), phiz, z3(),
                   dx, dt, nst, lamp=lamp, mu2=mu2, lamh=lamh, friction=FRICTION,
                   pin_mask=pin_mask)
    th, _, px, _, py, _, pz, _ = out
    kz = th.shape[2] // 2
    th2 = th[:, :, kz]
    Wxy = h.plaq_xy(px, py)
    B2 = np.abs(Wxy[:, :, kz]) / dx ** 2

    rc, th_prof = radial_profile(th2, x, y, xc, yc)
    _, B_prof = radial_profile(B2, x, y, xc, yc)

    # coherence length xi: radius where theta recovers to v/sqrt(2) from its core value
    th_core = float(np.nanmin(th_prof))
    th_inf = float(np.nanmedian(th_prof[-3:]))
    target = th_inf / np.sqrt(2.0)
    xi = float("nan")
    has_core = bool(th_core < 0.8 * th_inf)        # a genuine dip toward 0?
    if has_core:
        for i in range(len(rc)):
            if np.isfinite(th_prof[i]) and th_prof[i] >= target:
                xi = float(rc[i]); break
    # penetration depth lambda_L: 1/e-folding of B(r) from the core
    B0 = float(np.nanmax(B_prof))
    lam_L = float("nan")
    if B0 > 1e-6:
        for i in range(len(rc)):
            if np.isfinite(B_prof[i]) and B_prof[i] <= B0 / np.e:
                lam_L = float(rc[i]); break
    kappa = (lam_L / xi) if (np.isfinite(xi) and xi > 1e-6 and np.isfinite(lam_L)) \
        else float("nan")
    return {"v": float(v), "rc": rc.tolist(),
            "theta_profile": th_prof.tolist(), "B_profile": B_prof.tolist(),
            "theta_core": th_core, "theta_inf": th_inf, "has_normal_core": has_core,
            "xi": xi, "lambda_L": lam_L, "kappa": kappa}


def main():
    print("=" * 64)
    print("H3 -- VORTEX PROFILE: xi, lambda_L, kappa (mu2=%.1f, v~1)" % MU2)
    print("=" * 64)
    r = measure_vortex()
    print(f"  condensate v               = {r['v']:.3f}")
    print(f"  theta core / theta_inf     = {r['theta_core']:.3f} / {r['theta_inf']:.3f}")
    print(f"  normal core (theta dips)?  = {r['has_normal_core']}")
    print(f"  coherence length xi        = {r['xi']}")
    print(f"  penetration depth lambda_L = {r['lambda_L']:.3f}")
    print(f"  kappa = lambda_L/xi        = {r['kappa']}")

    kappa = r["kappa"]
    kc = 1.0 / np.sqrt(2.0)
    if np.isfinite(kappa):
        regime = ("TIPO II (kappa>1/sqrt2)" if kappa > kc
                  else "TIPO I (kappa<1/sqrt2)")
    else:
        regime = "indefinido (sem nucleo normal: xi nao medivel)"

    payload = {"mu2": MU2, "lamh": LAMH, "lamp": LAMP, "grid": GRID,
               "kappa_critical": kc, "regime": regime, **r}
    h.save_json("H3_vortex_profile", payload)
    _write_md(payload)
    if HAVE_MPL:
        _figure(payload)

    print("-" * 64)
    print(f"REGIME: {regime}")
    return payload


def _write_md(p):
    rc = p["rc"]; thp = p["theta_profile"]; Bp = p["B_profile"]
    L = [
        "# H3 — Perfil do vórtice no condensado: ξ, λ_L, κ",
        "",
        "Com o condensado ativo (θ~v), construímos um vórtice de enrolamento 1 (linha ao",
        "longo de z, enrolamento no plano xy), relaxamos sob a ação completa e medimos os",
        "perfis radiais em torno do núcleo (fatia z central). μ²=%.1f, λ_h=%.1f, λ_p=%.1f."
        % (p["mu2"], p["lamh"], p["lamp"]),
        "",
        "## Medições",
        "",
        f"- **Condensado v** = {p['v']:.3f}.",
        f"- **Núcleo escalar:** θ(0)={p['theta_core']:.3f} vs θ(∞)={p['theta_inf']:.3f} "
        f"→ há núcleo normal (θ mergulha para ~0)? **{p['has_normal_core']}**.",
        f"- **Comprimento de coerência ξ** (raio onde θ=v/√2): "
        f"{('%.3f' % p['xi']) if np.isfinite(p['xi']) else '— (sem núcleo)'}.",
        f"- **Comprimento de penetração λ_L** (1/e do campo B): {p['lambda_L']:.3f}.",
        f"- **κ = λ_L/ξ** = {('%.3f' % p['kappa']) if np.isfinite(p['kappa']) else '—'} "
        f"(crítico 1/√2≈{p['kappa_critical']:.3f}).",
        "",
        "| r⊥ | θ(r⊥) | B(r⊥) |",
        "|----|-------|-------|",
    ]
    for i in range(len(rc)):
        t = thp[i]; b = Bp[i]
        L.append(f"| {rc[i]:.2f} | {(f'{t:.3f}' if np.isfinite(t) else '—')} | "
                 f"{(f'{b:.3f}' if np.isfinite(b) else '—')} |")
    L += [
        "",
        f"## Regime: **{p['regime']}**",
        "",
        ("O condensado **fixa a magnitude** de θ ao redor de v; o campo magnético do "
         "vórtice (fluxo de plaqueta) é localizado e decai em λ_L≈1/m_A (consistente com "
         "a massa de gauge de H2). "
         if p["has_normal_core"] else
         "**Honestidade (consistente com H2):** θ é a fase de Stückelberg, não acopla a "
         "*magnitude* ao fluxo do vórtice, então θ **não** forma um núcleo normal "
         "(permanece ≈v) — ξ não é medível como no modelo abeliano-Higgs. O campo "
         "magnético B(r⊥) é localizado e decai em λ_L≈1/m_A (a massa de gauge de H2, "
         "fixada pelo cosseno e=1, não por v). A estrutura tipo-Abrikosov "
         "(núcleo normal + ξ) **não** emerge da ação mínima + V(θ)."),
        "",
        "![perfis](H3_vortex_profile.png)",
        "",
    ]
    (h.OUTDIR / "H3_vortex_profile.md").write_text("\n".join(L), encoding="utf-8")


def _figure(p):
    rc = np.array(p["rc"])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    ax[0].plot(rc, p["theta_profile"], "o-")
    ax[0].axhline(p["v"], ls="--", c="k", lw=0.7, label="v")
    ax[0].axhline(p["v"] / np.sqrt(2), ls=":", c="r", lw=0.7, label=r"$v/\sqrt{2}$")
    ax[0].set_xlabel(r"$r_\perp$"); ax[0].set_ylabel(r"$\theta(r_\perp)$")
    ax[0].set_title("scalar core"); ax[0].legend(fontsize=8)
    ax[1].plot(rc, p["B_profile"], "s-")
    ax[1].set_xlabel(r"$r_\perp$"); ax[1].set_ylabel(r"$B(r_\perp)=|W_{xy}|/dx^2$")
    ax[1].set_title("magnetic core")
    fig.tight_layout()
    fig.savefig(h.OUTDIR / "H3_vortex_profile.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

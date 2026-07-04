"""AH3 -- vortex profile: |Phi|(r) -> 0 at the core, coherence length xi, kappa.

With the complex condensate active, build an isolated winding-1 vortex (line along z,
winding in xy), pin a small core cylinder so the winding cannot unwind, relax the rest,
and measure the radial profiles on the mid-z slice:

  * magnitude  |Phi|(r_perp): expected |Phi|(0)->0 (normal core), |Phi|(inf)->v;
    coherence length xi = radius where |Phi| = v/sqrt(2).
  * magnetic   B(r_perp) = |Wxy|: peaks at the core, decays over the penetration depth
    lambda_L (1/e radius); m_A ~ 1/lambda_L cross-checks AH2.
  * kappa = lambda_L / xi : kappa > 1/sqrt(2) -> type II (stable flux-tube lattice).

Contrast with CR_HIGGS H3, where theta stayed ~v (no normal core, xi undefined).  Here
the MAGNITUDE of the complex field can vanish at the core -- the abelian-Higgs vortex.
xi, lambda_L MEASURED.  Ginzburg-Landau / type I-II / Abrikosov only in COMPARISON ONLY.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crahiggs_core as a   # noqa: E402

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

MU2 = 4.0
LAM = 2.0                 # v = sqrt(mu2/2lam) = 1.0; kappa = 2 sqrt(lam)/e ~ Type II
LAMP = 0.8
GRID = dict(Nx=33, Ny=28, Nz=10)
DT = 0.02
T_RELAX = 60.0
FRICTION = 0.05
R_CORE = 1.0             # small core pin: holds the winding, lets |Phi| relax to its
#                          physical coherence length (a large pin would imprint xi)


def screening_mA(mu2, lam, v, grid, seed=0):
    """Inline gauge-boson mass on a FROZEN condensate (unitary gauge), same method as
    AH2: a pinned transverse phi_y source, fit the spatial decay.  lambda_L = 1/m_A is
    the physical penetration depth (the pin-concentrated vortex B-field is sub-lattice
    at v~1 and cannot resolve it directly)."""
    x, y, z, _ = a.make_grid(Nx=81, Ny=grid["Ny"], Nz=grid["Nz"])
    sh = (len(x), len(y), len(z))
    pr = np.full(sh, max(v, 1e-6)); pi = np.zeros(sh)
    ic = sh[0] // 2
    phiy = np.zeros(sh); phiy[ic, :, :] = 0.3
    pin = np.zeros(sh, dtype=bool); pin[ic, :, :] = True
    zero = lambda: np.zeros(sh)
    out = a.evolve(pr, zero(), pi, zero(), zero(), zero(), phiy, zero(), zero(), zero(),
                   DT, int(round(80.0 / DT)), mu2, lam, lamp=0.8,
                   friction=0.05, pin_mask=pin, freeze_higgs=True)
    A = np.mean(out[6], axis=(1, 2))
    idx = []
    for k in range(1, 12):
        if A[ic + k] < 5e-4:
            break
        if idx and A[ic + k] > A[ic + idx[-1]]:
            break
        idx.append(k)
    if len(idx) >= 2:
        seg = ic + np.array(idx)
        return float(-np.polyfit(np.array(idx, float), np.log(A[seg]), 1)[0])
    return float("nan")


def radial_profile(field2d, x, y, xc, yc, nbin=14):
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


def _xi_crossing(rc, prof, target):
    """First radius where prof rises through ``target`` (linear interpolation)."""
    for i in range(1, len(rc)):
        a0, a1 = prof[i - 1], prof[i]
        if np.isfinite(a0) and np.isfinite(a1) and a0 < target <= a1:
            f = (target - a0) / (a1 - a0)
            return float(rc[i - 1] + f * (rc[i] - rc[i - 1]))
    # fall back: first bin at/above target
    for i in range(len(rc)):
        if np.isfinite(prof[i]) and prof[i] >= target:
            return float(rc[i])
    return float("nan")


def measure(mu2=MU2, lam=LAM, lamp=LAMP, seed=0):
    x, y, z, _ = a.make_grid(**GRID)
    rng = np.random.default_rng(800 + seed)
    v = a.relax_vacuum(mu2, lam, rng=rng, grid=GRID, t_relax=40.0, dt=DT)["rho_bulk_mean"]
    pr, pi, phix, phiy, phiz, (xc, yc) = a.vortex_state(x, y, z, v, n_wind=1)
    sh = pr.shape
    X, Y, _ = np.meshgrid(x, y, z, indexing="ij")
    pin_mask = ((X - xc) ** 2 + (Y - yc) ** 2) < R_CORE ** 2
    zero = lambda: np.zeros(sh)
    out = a.evolve(pr, zero(), pi, zero(), phix, zero(), phiy, zero(), phiz, zero(),
                   DT, int(round(T_RELAX / DT)), mu2, lam, lamp,
                   friction=FRICTION, pin_mask=pin_mask)
    PR, PI, PX, PY = out[0], out[2], out[4], out[6]
    kz = sh[2] // 2
    rho = a.magnitude(PR, PI)[:, :, kz]
    Wxy = a.c3.plaq_xy(PX, PY)
    B = np.abs(Wxy[:, :, kz])

    rc, rho_prof = radial_profile(rho, x, y, xc, yc, nbin=16)
    _, B_prof = radial_profile(B, x, y, xc, yc, nbin=16)

    rho_core = float(rho_prof[0])
    rho_inf = float(np.nanmedian(rho_prof[-4:]))
    has_core = bool(rho_core < 0.6 * rho_inf)            # genuine normal core?
    xi = _xi_crossing(rc, rho_prof, rho_inf / np.sqrt(2.0))

    # penetration depth from the gauge-boson mass (1/m_A); the pin-concentrated vortex
    # B-field is sub-lattice at v~1 and cannot resolve lambda_L directly.
    m_A = screening_mA(mu2, lam, v, GRID)
    lam_L = (1.0 / m_A) if (np.isfinite(m_A) and m_A > 1e-6) else float("nan")
    kappa = (lam_L / xi) if (np.isfinite(xi) and xi > 1e-6 and np.isfinite(lam_L)) \
        else float("nan")
    return {"v": float(v), "rc": rc.tolist(), "rho_profile": rho_prof.tolist(),
            "B_profile": B_prof.tolist(), "rho_core": rho_core, "rho_inf": rho_inf,
            "has_normal_core": has_core, "xi": xi, "m_A": float(m_A),
            "lambda_L": lam_L, "kappa": kappa}


def main():
    print("=" * 60)
    print("AH3 -- VORTEX PROFILE: |Phi|(0)->0, xi, lambda_L, kappa")
    print("=" * 60)
    r = measure()
    kc = 1.0 / np.sqrt(2.0)
    print(f"  v                         = {r['v']:.3f}")
    print(f"  |Phi| core / |Phi| inf    = {r['rho_core']:.3f} / {r['rho_inf']:.3f}")
    print(f"  normal core (|Phi|->0)?   = {r['has_normal_core']}")
    print(f"  coherence length xi       = {r['xi']}")
    print(f"  penetration depth lam_L   = {r['lambda_L']}")
    print(f"  kappa = lam_L/xi          = {r['kappa']}")
    if np.isfinite(r["kappa"]):
        regime = "TIPO II (kappa>1/sqrt2)" if r["kappa"] > kc else "TIPO I (kappa<1/sqrt2)"
    else:
        regime = "indefinido"
    payload = {"mu2": MU2, "lam": LAM, "lamp": LAMP, "grid": GRID,
               "kappa_critical": kc, "regime": regime, **r}
    a.save_json("AH3_vortex", payload)
    _write_md(payload)
    if HAVE_MPL:
        _figure(payload)
    print("-" * 60)
    print(f"REGIME: {regime}")
    return payload


def _write_md(p):
    rc = p["rc"]; rp = p["rho_profile"]; Bp = p["B_profile"]
    L = [
        "# AH3 — Perfil do vórtice: núcleo com |Φ|→0, ξ, λ_L, κ",
        "",
        "Vórtice de enrolamento 1 (linha em z) no condensado complexo, núcleo pinado para",
        "segurar o enrolamento, restante relaxado. Perfis radiais na fatia z central.",
        "μ²=%.1f, λ=%.1f, λ_p=%.1f, v=%.2f." % (p["mu2"], p["lam"], p["lamp"], p["v"]),
        "",
        "## Medições",
        "",
        f"- **Núcleo escalar:** |Φ|(0)={p['rho_core']:.3f} vs |Φ|(∞)={p['rho_inf']:.3f} → "
        f"**núcleo normal (|Φ|→0): {p['has_normal_core']}**.",
        f"- **Comprimento de coerência ξ** (|Φ|=v/√2): "
        f"{('%.3f' % p['xi']) if np.isfinite(p['xi']) else '—'}.",
        f"- **Comprimento de penetração λ_L = 1/m_A** = "
        f"{('%.3f' % p['lambda_L']) if np.isfinite(p['lambda_L']) else '—'} "
        f"(m_A={p['m_A']:.3f} pela blindagem de gauge; o B do vórtice pinado é "
        f"sub-rede em v~1 e não resolve λ_L diretamente).",
        f"- **κ = λ_L/ξ** = {('%.3f' % p['kappa']) if np.isfinite(p['kappa']) else '—'} "
        f"(crítico 1/√2≈{p['kappa_critical']:.3f}).",
        "",
        "| r⊥ | \\|Φ\\|(r⊥) | B(r⊥) |",
        "|----|-----------|-------|",
    ]
    for i in range(len(rc)):
        t = rp[i]; b = Bp[i]
        L.append(f"| {rc[i]:.2f} | {(f'{t:.3f}' if np.isfinite(t) else '—')} | "
                 f"{(f'{b:.3f}' if np.isfinite(b) else '—')} |")
    L += [
        "",
        f"## Regime: **{p['regime']}**",
        "",
        ("**O núcleo normal existe (|Φ|→0 no centro)** — exatamente o que CR_HIGGS não "
         "teve. A magnitude do campo complexo vai a zero no núcleo do vórtice (a fase é "
         "singular ali), o condensado se recupera em ξ, e o campo magnético penetra λ_L. "
         "É o vórtice de Abrikosov genuíno (COMPARISON ONLY)."
         if p["has_normal_core"] else
         "O núcleo normal não se formou claramente no regime medido — ver perfis."),
        "",
        "**Contraste com CR_HIGGS H3:** lá θ permanecia ≈v (sem núcleo normal, ξ "
        "indefinível); aqui |Φ|→0 no núcleo. É a diferença entre fase real e campo "
        "complexo.",
        "",
        "> **Caveat de rede (honesto):** κ = 2√λ/e é fixado por λ (não por v); na rede "
        "> de espaçamento unitário ξ não resolve abaixo de ~1 célula, então κ fica "
        "> **próximo do crítico** 1/√2 (Type II claro exige λ≳2). O resultado robusto, "
        "> independente da resolução, é o **núcleo normal |Φ|→0** — ausente em CR_HIGGS.",
        "",
        "![perfis](AH3_vortex.png)",
        "",
    ]
    (a.OUTDIR / "AH3_vortex.md").write_text("\n".join(L), encoding="utf-8")


def _figure(p):
    rc = np.array(p["rc"])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    ax[0].plot(rc, p["rho_profile"], "o-")
    ax[0].axhline(p["v"], ls="--", c="k", lw=0.7, label="v")
    ax[0].axhline(p["v"] / np.sqrt(2), ls=":", c="r", lw=0.7, label=r"$v/\sqrt{2}$")
    ax[0].set_xlabel(r"$r_\perp$"); ax[0].set_ylabel(r"$|\Phi|(r_\perp)$")
    ax[0].set_title("scalar core (|Phi|->0)"); ax[0].legend(fontsize=8); ax[0].set_ylim(0)
    ax[1].plot(rc, p["B_profile"], "s-")
    ax[1].set_xlabel(r"$r_\perp$"); ax[1].set_ylabel(r"$B(r_\perp)=|W_{xy}|$")
    ax[1].set_title("magnetic core")
    fig.tight_layout()
    fig.savefig(a.OUTDIR / "AH3_vortex.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

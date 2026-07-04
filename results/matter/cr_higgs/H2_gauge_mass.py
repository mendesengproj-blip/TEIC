"""H2 -- the gauge mass m_A: testing m_A = e v on the condensate.

With theta condensed at <theta>=v, does the gauge field phi acquire a mass that scales
as m_A = e v (the abelian-Higgs prediction)?  We measure m_A from the STATIC screening
of a gauge-field plane source: a thin x-slab carries a FIXED phi_x link perturbation
(phi_x is the component with an explicit x-laplacian, so it propagates in x; a phi_x(x)
profile is pure gauge -- removable by a theta shift -- UNLESS theta is held, so its
decay length is the gauge screening length).  On a frozen condensate background
theta=v=const (the unitary-gauge measurement of the propagating gauge boson) the
response decays as

    A(x) = <phi_x>_{y,z}(x)  ~  exp(-m_A |x - x_src|) ,

and a log-linear fit returns m_A.  m_A is FITTED, never inserted.

THE RESULT IS A CLARIFYING NEGATIVE (and it must be reported honestly).  In the minimal
TEIC action theta is the Stueckelberg PHASE: it enters cos(phi+Dtheta) only through its
GRADIENT, so a constant condensate theta=v (any magnitude) leaves the gauge mass term
-sin(phi) UNCHANGED.  The gauge mass is therefore set by the cosine coupling e=1, NOT by
v: m_A ~ 1 for every v, and m_A != 0 at v=0.  The abelian-Higgs relation m_A = e v
(which needs the field MAGNITUDE to multiply (d alpha - e A)^2) is NOT reproduced.  We
also record the FREE-theta response (theta allowed to relax against the source) for
completeness; it is contaminated by theta dynamics and is not the gauge-boson mass.

Stueckelberg mechanism / Higgs mass / abelian-Higgs appear only as names in COMPARISON
ONLY blocks.
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
MU2S = [0.0, 0.1, 0.5, 1.0, 2.0]
GRID = dict(Lx=40.0, Nx=81, Ny=10, Nz=10)
SRC_AMP = 0.3
T_RELAX = 80.0
FRICTION = 0.05


def _fit_decay(A, ic, dx, shape, floor=0.01, max_cells=12):
    """Fit log A vs x on the clean exponential region: contiguous cells from the source
    outward while A stays above the noise floor (and monotone), capped at max_cells."""
    xs = (np.arange(shape[0]) - ic) * dx
    idx = []
    for k in range(1, min(max_cells, shape[0] - ic - 1)):
        a = A[ic + k]
        if a < floor:
            break
        if idx and A[ic + k] > A[ic + idx[-1]]:   # stop if it stops decreasing
            break
        idx.append(k)
    if len(idx) >= 3:
        seg = ic + np.array(idx)
        p = np.polyfit(xs[seg], np.log(A[seg]), 1)
        return float(-p[0]), xs
    return float("nan"), xs


def screening_mass(mu2, lamh=LAMH, seed=0):
    """Relax theta to v, drive a fixed phi_x plane source at the centre, and fit m_A
    from the spatial decay of <phi_x>_{y,z}(x).

    Primary measurement: FROZEN condensate background theta=v=const (unitary gauge --
    the propagating gauge-boson mass).  Also returns the FREE-theta response (theta
    relaxes against the source) for completeness."""
    x, y, z, dx = h.make_grid(**GRID)
    dt = h.dt_cfl(dx)
    rng = np.random.default_rng(700 + seed)
    vac = h.relax_vacuum(mu2, lamh, rng=rng, grid=GRID, t_relax=T_RELAX)
    v_meas = vac["theta_bulk_mean"]
    theta = vac["field"].copy()
    shape = theta.shape
    z3 = lambda: np.zeros(shape)
    ic = shape[0] // 2
    pin_mask = np.zeros(shape, dtype=bool)
    pin_mask[ic, :, :] = True
    nst = int(round(T_RELAX / dt))

    def run(freeze):
        phix = z3(); phix[ic, :, :] = SRC_AMP
        out = h.evolve(theta.copy(), z3(), phix, z3(), z3(), z3(), z3(), z3(),
                       dx, dt, nst, lamp=0.0, mu2=mu2, lamh=lamh,
                       friction=FRICTION, pin_mask=pin_mask, freeze_theta=freeze)
        A = np.mean(out[2], axis=(1, 2))
        m_A, xs = _fit_decay(A, ic, dx, shape)
        return m_A, A, xs

    m_A, A, xs = run(freeze=True)          # PRIMARY: gauge-boson mass (unitary gauge)
    m_A_free, _, _ = run(freeze=False)     # contaminated by theta dynamics
    return {"mu2": mu2, "v_meas": float(v_meas), "m_A": m_A, "m_A_free": m_A_free,
            "profile_x": xs.tolist(), "profile_A": A.tolist(), "i_src": ic}


def main():
    print("=" * 64)
    print("H2 -- GAUGE MASS m_A FROM CONDENSATE SCREENING (lambda_h=%.1f)" % LAMH)
    print("=" * 64)
    print(f"{'mu2':>5} {'v':>7} {'m_A(froz)':>10} {'m_A(free)':>10} {'e*v':>7}")
    rows = []
    for mu2 in MU2S:
        r = screening_mass(mu2)
        rows.append(r)
        v = r["v_meas"]
        print(f"{mu2:5.2f} {v:7.3f} {r['m_A']:10.4f} {r['m_A_free']:10.4f} {v:7.3f}")

    # checks (the abelian-Higgs prediction is m_A = e v with e=1)
    vs = np.array([r["v_meas"] for r in rows])
    ms = np.array([r["m_A"] for r in rows])
    r0 = next(r for r in rows if r["mu2"] == 0.0)
    massless_at_v0 = bool(abs(r0["m_A"]) < 0.15)          # abelian-Higgs needs ~0
    # is m_A independent of v? (Stueckelberg/cosine mass, the actual finding)
    v_independent = bool(np.std(ms) / np.mean(ms) < 0.1)
    e_eff = float(np.mean(ms))                            # the cosine coupling ~1
    # does m_A = e v hold?  test slope of m_A vs v ~ 1 AND intercept ~ 0
    slope, intercept = np.polyfit(vs, ms, 1)
    m_eq_ev = bool(abs(slope - 1.0) < 0.3 and abs(intercept) < 0.2)

    h2 = {"lamh": LAMH, "mu2s": MU2S, "grid": GRID, "src_amp": SRC_AMP,
          "rows": rows,
          "massless_at_v0": massless_at_v0,
          "m_A_v_independent": v_independent,
          "e_eff_cosine_mass": e_eff,
          "m_A_vs_v_slope": float(slope),
          "m_A_vs_v_intercept": float(intercept),
          "m_A_equals_e_v": m_eq_ev,
          "H2_PASS": bool(m_eq_ev)}
    h.save_json("H2_gauge_mass", h2)
    _write_md(h2)
    if HAVE_MPL:
        _figure(rows)

    print("-" * 64)
    print(f"  m_A(v=0)~0: {massless_at_v0}   m_A v-independent: {v_independent}   "
          f"e_eff(cosine mass)={e_eff:.3f}")
    print(f"  m_A vs v: slope={slope:.3f} intercept={intercept:.3f} -> m_A=e*v? {m_eq_ev}")
    print(f"H2 {'PASS' if m_eq_ev else 'NAO -- m_A set by cosine coupling e, not by v'}")
    return h2


def _write_md(p):
    rows = p["rows"]
    L = [
        "# H2 — Massa de gauge m_A: o teste de m_A = e·v",
        "",
        "Com θ condensado em ⟨θ⟩=v, medimos a massa do campo de gauge φ pela **resposta",
        "estática** a uma fonte-plano: uma fatia fina em x carrega um φ_x fixo; o campo",
        "relaxa em volta e a resposta decai como A(x) ~ exp(−m_A|x−x_fonte|). A medição",
        "primária usa **fundo de condensado congelado θ=v=const (calibre unitário — a",
        "massa do bóson de gauge que propaga)**. m_A é **ajustada**, nunca inserida.",
        "λ_h = %.1f." % p["lamh"],
        "",
        "| μ² | v medido | m_A (θ congelado) | m_A (θ livre) | e·v (e=1) |",
        "|----|----------|-------------------|---------------|-----------|",
    ]
    for r in rows:
        v = r["v_meas"]
        L.append(f"| {r['mu2']:.2f} | {v:.3f} | {r['m_A']:.4f} | "
                 f"{r['m_A_free']:.4f} | {v:.3f} |")
    L += [
        "",
        "## Leitura — um negativo esclarecedor (reportado com honestidade)",
        "",
        f"- **m_A é independente de v:** {p['m_A_v_independent']} — a massa do bóson de "
        f"gauge é **≈ {p['e_eff_cosine_mass']:.2f} em toda a faixa de v** (inclui v≈1.4).",
        f"- **m_A(v=0) ≈ 0?** {p['massless_at_v0']} — m_A é **não-nula mesmo sem "
        f"condensado**. A predição abeliana-Higgs (m_A=0 em v=0) **falha**.",
        f"- **m_A = e·v?** inclinação(m_A vs v) = {p['m_A_vs_v_slope']:.2f}, intercepto "
        f"= {p['m_A_vs_v_intercept']:.2f} → **{p['m_A_equals_e_v']}**.",
        "",
        "**Por quê.** Na ação mínima θ é a **fase de Stückelberg**: entra em "
        "cos(φ+Δθ) só pelo *gradiente* Δθ. Um condensado **constante** θ=v (de qualquer "
        "magnitude) tem Δθ=0 e deixa o termo de massa −sin(φ) **inalterado** → a massa "
        "de gauge é fixada pelo **acoplamento do cosseno e=1**, não por v. A relação "
        "m_A=e·v exige que a *magnitude* do campo multiplique (∂α−eA)² (modelo "
        "abeliano-Higgs), o que esta ação **não** tem. A coluna “θ livre” mostra a "
        "resposta contaminada pela dinâmica de θ contra a fonte — não é a massa do bóson.",
        "",
        "## Conexão com a DEV (honesta)",
        "",
        "A DEV usa m_A como parâmetro livre. H2 mostra que a massa de gauge na TEIC é "
        "fixada pelo **acoplamento de Stückelberg e** (≈1 em unidades de rede, o teto do "
        "cosseno), **não** pelo condensado v. Portanto V(θ) **não deriva** m_A da DEV "
        "via m_A=e·v — esse mecanismo precisaria de θ como magnitude. O resultado "
        "honesto: o condensado existe (H1), mas **não** dá origem ao mecanismo de massa "
        "abeliano-Higgs (ver H6).",
        "",
        "![m_A vs v](H2_gauge_mass.png)",
        "",
    ]
    (h.OUTDIR / "H2_gauge_mass.md").write_text("\n".join(L), encoding="utf-8")


def _figure(rows):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    vs = [r["v_meas"] for r in rows]
    ms = [r["m_A"] for r in rows]
    ax[0].plot(vs, ms, "o-", label=r"$m_A$ measured")
    vg = np.linspace(0, max(vs), 100)
    ax[0].plot(vg, vg, "k--", lw=0.8, label=r"$m_A=e\,v$ (e=1)")
    ax[0].set_xlabel("v (measured condensate)"); ax[0].set_ylabel(r"$m_A$")
    ax[0].set_title("gauge mass vs condensate"); ax[0].legend(fontsize=8)
    for r in rows:
        xs = np.array(r["profile_x"]); A = np.array(r["profile_A"])
        ic = r["i_src"]
        m = np.arange(ic, len(xs))
        ax[1].semilogy(xs[m], np.clip(A[m], 1e-4, None), "-",
                       label=f"v={r['v_meas']:.2f}")
    ax[1].set_xlabel(r"$x-x_{src}$"); ax[1].set_ylabel(r"$\langle\phi_y\rangle$")
    ax[1].set_title("screening profiles"); ax[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(h.OUTDIR / "H2_gauge_mass.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

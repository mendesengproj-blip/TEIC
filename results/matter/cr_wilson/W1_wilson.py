"""W1 -- the full action (Stueckelberg + Wilson plaquette) and its MANDATORY gate.

Four checks before any string-tension / collision experiment (stop and report on
failure):

  (1) lambda_p = 0  ->  reproduces CR_GAUGE EXACTLY.  A y-uniform 2D config evolved with
      lambda_p=0 matches the 1D gauge_core evolution row-by-row to machine zero (forces
      already match to 0 in wilson_core's self-test).
  (2) theta = 0, lambda_p > 0  ->  PURE GAUGE / Maxwell static.  A pure-gauge config
      (W_p=0 everywhere) is a static solution (zero Wilson force); a config with W_p!=0
      carries magnetic energy lambda_p*sum(1-cos W) that RELAXES toward W_p=0 under
      damping (the lattice Maxwell magnetic term), and free evolution conserves energy.
  (3) ISOLATED kink with lambda_p > 0: rest mass still 8.  A y-uniform kink has W_p=0,
      so Wilson cannot change its self-energy -- mass and stability are untouched.
  (4) ENERGY CONSERVATION: E_total = E_links + E_plaquettes conserved < 1% on a generic
      free (frictionless) propagation with lambda_p > 0.

Output: W1_wilson.{md,json}.
"""

from __future__ import annotations

import numpy as np

import wilson_core as wc
import gauge_core as gc
import dbi_core as dbi


# (1) ------------------------------------------------------------------------ #
def reduces_to_cr_gauge():
    x, y, dx = wc.make_grid(Lx=40.0, Nx=201, Ny=6)
    dt = wc.dt_cfl(dx)
    rng = np.random.default_rng(11)
    th1d = rng.standard_normal(len(x)) * 0.4
    ph1d = rng.standard_normal(len(x)) * 0.4
    th1d[0] = th1d[-1] = 0.0; ph1d[0] = ph1d[-1] = 0.0
    theta = np.repeat(th1d[:, None], len(y), axis=1)
    phix = np.repeat(ph1d[:, None], len(y), axis=1)
    vth = np.zeros_like(theta); vphx = np.zeros_like(theta)
    phiy = np.zeros_like(theta); vphy = np.zeros_like(theta)
    th2, vth2, px2, vpx2, py2, vpy2 = wc.evolve(theta, vth, phix, vphx, phiy, vphy,
                                                dx, dt, 1500, lam=0.0)
    # 1D reference
    th1, vt1, ph1, vp1, _ = gc.evolve_coupled(th1d, np.zeros_like(x), ph1d,
                                              np.zeros_like(x), dx, dt, 1500)
    dth = float(np.max(np.abs(th2[:, 0] - th1)))
    dph = float(np.max(np.abs(px2[:, 0] - ph1)))
    yuniform = float(np.max(np.abs(th2 - th2[:, [0]])) + np.max(np.abs(py2)))
    return {"theta_diff": dth, "phix_diff": dph, "stays_y_uniform": yuniform,
            "ok": bool(dth < 1e-9 and dph < 1e-9 and yuniform < 1e-9)}


# (2) ------------------------------------------------------------------------ #
def pure_gauge_maxwell():
    x, y, dx = wc.make_grid(Lx=40.0, Nx=121, Ny=12)
    dt = wc.dt_cfl(dx)
    rng = np.random.default_rng(12)
    th0 = np.zeros((len(x), len(y)))
    vth0 = np.zeros_like(th0)
    # (a) pure-gauge config phi = grad(chi): W_p = 0 -> zero Wilson force, static
    chi = 0.3 * np.exp(-((x[:, None] - 0.0) ** 2) / 8.0) * np.cos(y[None, :])
    pgx = np.zeros_like(th0); pgx[:-1, :] = np.diff(chi, axis=0)
    pgy = wc._roll_up(chi) - chi
    flux_pure = wc.wilson_flux(pgx, pgy)
    fx = wc.force_phix(th0, pgx, pgy, dx, lam=0.7)
    fy = wc.force_phiy(th0, pgx, pgy, dx, lam=0.7)
    # subtract the lambda=0 part: the WILSON contribution to the force on a pure-gauge
    fx0 = wc.force_phix(th0, pgx, pgy, dx, lam=0.0)
    fy0 = wc.force_phiy(th0, pgx, pgy, dx, lam=0.0)
    wilson_force_pure = float(np.max(np.abs(fx - fx0)) + np.max(np.abs(fy - fy0)))
    # (b) a config WITH magnetic flux relaxes toward W=0 under damping (Maxwell)
    rpx = 0.4 * rng.standard_normal((len(x), len(y)))
    rpy = 0.4 * rng.standard_normal((len(x), len(y)))
    rpx[0, :] = rpx[-1, :] = 0.0; rpy[0, :] = rpy[-1, :] = 0.0
    flux0 = wc.wilson_flux(rpx, rpy)
    out = wc.evolve(th0, vth0, rpx, np.zeros_like(th0), rpy, np.zeros_like(th0),
                    dx, dt, 4000, lam=0.7, freeze_theta=True, friction=0.01)
    flux1 = wc.wilson_flux(out[2], out[4])
    return {"flux_pure_gauge": flux_pure, "wilson_force_on_pure_gauge": wilson_force_pure,
            "flux_before_relax": flux0, "flux_after_relax": flux1,
            "relaxes": bool(flux1 < 0.5 * flux0),
            "ok": bool(flux_pure < 1e-9 and wilson_force_pure < 1e-9 and flux1 < 0.5 * flux0)}


# (3) ------------------------------------------------------------------------ #
def kink_mass_unchanged():
    x, y, dx = wc.make_grid(Lx=80.0, Nx=801, Ny=6)
    dt = wc.dt_cfl(dx)
    k1d = 4.0 * np.arctan(np.exp(x / 1.0))
    phix = np.repeat(k1d[:, None], len(y), axis=1)
    th0 = np.zeros_like(phix); v0 = np.zeros_like(phix)
    phiy = np.zeros_like(phix)

    def mass(px):                                # DBI4 functional on a representative row
        return float(np.sum(dbi.energy_density_sg(px[:, 0], np.zeros(len(x)), dx)) * dx)

    m0 = mass(phix)
    out = wc.evolve(th0, v0, phix, v0.copy(), phiy, v0.copy(), dx, dt, 3000,
                    lam=0.7, freeze_theta=True)
    m1 = mass(out[2])
    flux = wc.wilson_flux(out[2], out[4])
    c_after = wc.kink_count_x(out[2])
    return {"mass_lam0_ref": 8.0, "kink_rest_mass": m0, "kink_mass_after": m1,
            "wilson_flux_on_kink": flux, "count_after": c_after,
            "ok": bool(abs(m0 - 8.0) < 0.1 and abs(m1 - m0) / m0 < 0.05
                       and flux < 1e-6 and c_after == 1)}


# (4) ------------------------------------------------------------------------ #
def energy_conservation():
    """Free (frictionless) propagation of a PHYSICAL collision config (smooth chains +
    small transverse noise that activates Wilson), lambda_p>0."""
    x, y, dx = wc.make_grid(Lx=60.0, Nx=301, Ny=12)
    dt = wc.dt_cfl(dx)
    rng = np.random.default_rng(14)
    th, vth, px, vpx, py, vpy = wc.two_chains(x, y, 10.0, x0=8.0, w=2.0,
                                              noise=0.01, rng=rng, ynoise=0.04)
    nst = int(round(18.0 / dt))
    e0 = wc.energy_components(th, vth, px, vpx, py, vpy, dx, 0.7)
    out = wc.evolve(th, vth, px, vpx, py, vpy, dx, dt, nst, lam=0.7)
    e1 = wc.energy_components(*out, dx, 0.7)
    drift = abs(e1["E_total"] - e0["E_total"]) / e0["E_total"]
    return {"E0": e0, "E1": e1, "drift": float(drift), "ok": bool(drift < 0.01)}


def main():
    print("=" * 70)
    print("W1 -- FULL ACTION (Stueckelberg + Wilson) + MANDATORY GATE")
    print("=" * 70)

    c1 = reduces_to_cr_gauge()
    print(f"  (1) lambda_p=0 -> CR_GAUGE: theta_diff={c1['theta_diff']:.1e}, "
          f"phix_diff={c1['phix_diff']:.1e}, y-uniform={c1['stays_y_uniform']:.1e} -> ok={c1['ok']}")
    c2 = pure_gauge_maxwell()
    print(f"  (2) pure gauge: W_p flux={c2['flux_pure_gauge']:.1e}, Wilson force on it="
          f"{c2['wilson_force_on_pure_gauge']:.1e}; magnetic flux relaxes "
          f"{c2['flux_before_relax']:.2f}->{c2['flux_after_relax']:.2f} -> ok={c2['ok']}")
    c3 = kink_mass_unchanged()
    print(f"  (3) kink + lambda_p>0: mass {c3['kink_rest_mass']:.3f}->{c3['kink_mass_after']:.3f} "
          f"(flux on kink={c3['wilson_flux_on_kink']:.1e}, count={c3['count_after']}) -> ok={c3['ok']}")
    c4 = energy_conservation()
    print(f"  (4) energy E_links+E_plaq: drift={c4['drift']:.2e} -> ok={c4['ok']}")

    passed = bool(c1["ok"] and c2["ok"] and c3["ok"] and c4["ok"])
    if passed:
        verdict = "VALIDADO"
        statement = (
            "The full action is consistent. (1) lambda_p=0 reproduces CR_GAUGE exactly "
            "(row diffs %.0e). (2) A pure-gauge config has W_p=0 and feels zero Wilson "
            "force; magnetic flux relaxes (%.2f->%.2f) -- the lattice Maxwell term. "
            "(3) A y-uniform kink has W_p=0, so Wilson leaves its rest mass 8 untouched "
            "(%.3f, stable). (4) E_links+E_plaquettes is conserved (drift %.0e < 1%%). "
            "W2-W6 may proceed." % (max(c1["theta_diff"], c1["phix_diff"]),
                                    c2["flux_before_relax"], c2["flux_after_relax"],
                                    c3["kink_mass_after"], c4["drift"]))
    else:
        verdict = "FALHOU (parar)"
        statement = ("Gate failed (1=%s 2=%s 3=%s 4=%s) -- per protocol, W2-W6 must NOT "
                     "proceed until fixed." % (c1["ok"], c2["ok"], c3["ok"], c4["ok"]))
    print("-" * 70)
    print(f"VERDICT W1: {verdict}")
    print(f"  {statement}")

    out = {"check1_cr_gauge": c1, "check2_pure_gauge": c2, "check3_kink_mass": c3,
           "check4_conservation": c4, "passed": passed, "verdict": verdict,
           "statement": statement}
    wc.save_json("W1_wilson", out)
    _write_md(out)
    return out


def _write_md(out):
    c1, c2, c3, c4 = (out["check1_cr_gauge"], out["check2_pure_gauge"],
                      out["check3_kink_mass"], out["check4_conservation"])
    lines = [
        "# W1 -- Ação completa (Stückelberg + Wilson) e validação obrigatória",
        "",
        "Ação `S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` numa rede espacial **2D** "
        "(x = eixo de colisão, extremos fixos; y = transverso, periódico). Quatro "
        "verificações antes de W2–W6 (parar se falhar):",
        "",
        f"## (1) λ_p=0 reproduz CR_GAUGE exatamente",
        f"Config y-uniforme, λ_p=0: diferença por linha vs motor 1D = "
        f"θ {c1['theta_diff']:.1e}, φx {c1['phix_diff']:.1e}; permanece y-uniforme "
        f"({c1['stays_y_uniform']:.1e}) → **ok = {c1['ok']}**.",
        "",
        f"## (2) θ=0, λ_p>0 → pure gauge (Maxwell estático)",
        f"Config pure-gauge (φ=∇χ): W_p = {c2['flux_pure_gauge']:.1e} e força de Wilson "
        f"sobre ela = {c2['wilson_force_on_pure_gauge']:.1e} (nula → estática). Fluxo "
        f"magnético relaxa {c2['flux_before_relax']:.2f}→{c2['flux_after_relax']:.2f} sob "
        f"amortecimento (termo magnético de Maxwell) → **ok = {c2['ok']}**.",
        "",
        f"## (3) Kink isolado com λ_p>0: massa ≈ 8",
        f"Kink y-uniforme tem W_p=0 → Wilson não altera a auto-energia: massa "
        f"{c3['kink_rest_mass']:.3f} → {c3['kink_mass_after']:.3f} (fluxo no kink "
        f"{c3['wilson_flux_on_kink']:.1e}, contagem {c3['count_after']}) → **ok = {c3['ok']}**.",
        "",
        f"## (4) Conservação de energia (E_links + E_plaquetas)",
        f"Deriva = {c4['drift']:.1e} (< 1%) → **ok = {c4['ok']}**.",
        "",
        f"## VERDICT W1: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (wc.OUTDIR / "W1_wilson.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

"""G1 -- the coupled theta+phi dynamics and its MANDATORY consistency gate.

The full minimal action S = sum_links Dtau[1 - cos(phi + Dtheta)] with BOTH fields
dynamical (gauge_core).  Before any transfer/collision experiment we VALIDATE the three
limits required by the protocol (stop and report on failure):

  (A) THETA-PURE (phi frozen 0): force_theta == DBI's force_cos exactly, and a scalar
      collision is a pass-through (psi_late ~ 0) -- reproduces DBI1/DBI3.
  (B) PHI-PURE  (theta frozen 0): force_phi == (1/dx^2) DBI's sine-Gordon force; an
      explicit compact kink is STABLE and has rest mass 8 (DBI4's functional).
  (C) CONSERVATION: the symplectic integrator conserves the coupled energy
      E_total = E_theta + E_phi + E_coupling to < 1% over a free coupled propagation.

Output: G1_coupled.{md,json}.
"""

from __future__ import annotations

import numpy as np

import gauge_core as gc
import dbi_core as dbi


# (A) ------------------------------------------------------------------------ #
def theta_pure_reproduces_dbi():
    """force_theta(.,phi=0) must equal force_cos; and a frozen-gauge scalar collision
    must pass through (psi_late = central cos energy minus the linear-BD prediction
    ~ 0), reproducing DBI3's scalar-sector null."""
    x, dx = gc.make_grid()
    rng = np.random.default_rng(1)
    th = rng.standard_normal(len(x)) * 0.5
    force_diff = float(np.max(np.abs(
        gc.force_theta(th, np.zeros_like(x), dx) - dbi.force_cos(th, dx))))

    dt = gc.dt_cfl(dx)
    th0, vth0, phi0, vph0 = gc.two_chains(x, amp=2.0)
    nst = int(round(16.0 / dt))                      # to t ~ 16 (collide at t ~ 8)
    thf, vthf, _, _, _ = gc.evolve_coupled(th0, vth0, phi0, vph0, dx, dt, nst,
                                           freeze_phi=True)
    # linear-BD reference on the same scalar data
    thl, vl, _ = dbi.evolve(th0, vth0, dbi.force_linear, dx, dt, nst)
    ec = dbi.central_energy(thf, vthf, x, dx, 4.0, "cos")
    el = dbi.central_energy(thl, vl, x, dx, 4.0, "quad")
    psi_late = float(ec - el)
    return {"force_diff_vs_force_cos": force_diff, "psi_late": psi_late,
            "passthrough": bool(abs(psi_late) < 0.5)}


# (B) ------------------------------------------------------------------------ #
def phi_pure_reproduces_dbi4():
    """force_phi(theta=0,.) must equal (1/dx^2) DBI sine-Gordon; an explicit kink must
    be STABLE with rest mass 8 under the coupled engine (theta frozen 0)."""
    x, dx = dbi.make_grid()                          # fine grid for a clean mass ~ 8
    force_diff = float(np.max(np.abs(
        (gc.force_phi(np.zeros_like(x), np.sin(x), dx)
         - dbi.force_sine_gordon_potential(np.sin(x), dx) / dx ** 2)[1:-1])))

    phi0 = 4.0 * np.arctan(np.exp(x / 1.0))          # charged kink, winding 1
    vph0 = np.zeros_like(x)
    th0 = np.zeros_like(x)
    vth0 = np.zeros_like(x)

    def mass(phi, vph):                              # DBI4's (unscaled) functional
        return float(np.sum(dbi.energy_density_sg(phi, vph, dx)) * dx)

    m_rest = mass(phi0, vph0)
    W0 = gc.winding_phi(phi0)
    c0 = gc.kink_count_phi(phi0)
    dt = gc.dt_cfl(dx)
    _, _, phif, vphf, _ = gc.evolve_coupled(th0, vth0, phi0, vph0, dx, dt, 4000,
                                            freeze_theta=True)
    m_after = mass(phif, vphf)
    c_after = gc.kink_count_phi(phif)
    stable = bool(c_after == 1 and abs(m_after - m_rest) / m_rest < 0.05)
    return {"force_diff_vs_sine_gordon": force_diff, "kink_rest_mass": m_rest,
            "kink_mass_after": m_after, "winding": W0,
            "count_initial": c0, "count_after": c_after, "stable": stable}


# (C) ------------------------------------------------------------------------ #
def energy_conservation():
    """Coupled energy drift over a long FREE propagation of a mixed config (both fields
    excited, no collision-induced runaway).  Reports the 3-way sector split too."""
    x, dx = gc.make_grid()
    dt = gc.dt_cfl(dx)
    rng = np.random.default_rng(2)
    th0, vth0 = dbi.packet(x, 0.6, -6.0, 3.0, +1)
    phi0 = 0.4 * np.exp(-((x + 4.0) ** 2) / 8.0)
    vph0 = np.zeros_like(x)
    s0 = gc.sector_energies(th0, vth0, phi0, vph0, dx)
    thf, vthf, phif, vphf, _ = gc.evolve_coupled(th0, vth0, phi0, vph0, dx, dt, 4000)
    s1 = gc.sector_energies(thf, vthf, phif, vphf, dx)
    drift = abs(s1["E_total"] - s0["E_total"]) / s0["E_total"]
    return {"E0": s0, "E1": s1, "drift": float(drift)}


def main():
    print("=" * 70)
    print("G1 -- COUPLED theta+phi DYNAMICS + MANDATORY GATE")
    print("=" * 70)

    a = theta_pure_reproduces_dbi()
    print(f"  (A) theta-pure: force_diff vs force_cos = {a['force_diff_vs_force_cos']:.2e}; "
          f"collision psi_late = {a['psi_late']:+.3f} -> passthrough={a['passthrough']}")

    b = phi_pure_reproduces_dbi4()
    # COMPARISON ONLY -- analytic sine-Gordon kink mass, not inserted into any generator
    sg_theory_mass = 8.0
    # END COMPARISON ONLY
    print(f"  (B) phi-pure : force_diff vs sine-Gordon = {b['force_diff_vs_sine_gordon']:.2e}; "
          f"kink mass = {b['kink_rest_mass']:.3f} (theory {sg_theory_mass:.0f}), "
          f"count {b['count_initial']}->{b['count_after']}, stable={b['stable']}")

    c = energy_conservation()
    print(f"  (C) conservation: E_total {c['E0']['E_total']:.3f} -> {c['E1']['E_total']:.3f}, "
          f"drift = {c['drift']:.2e}")

    a_ok = a["force_diff_vs_force_cos"] < 1e-9 and a["passthrough"]
    b_ok = b["force_diff_vs_sine_gordon"] < 1e-9 and b["stable"] \
        and abs(b["kink_rest_mass"] - sg_theory_mass) < 0.1
    c_ok = c["drift"] < 0.01
    passed = bool(a_ok and b_ok and c_ok)

    if passed:
        verdict = "VALIDADO"
        statement = (
            "The coupled engine is consistent. theta-pure limit IS DBI's force_cos "
            "(force diff %.0e) and a frozen-gauge collision passes through "
            "(psi_late %.2f ~ 0, DBI3). phi-pure limit IS DBI's sine-Gordon "
            "(force diff %.0e interior); an explicit compact kink is STABLE with rest "
            "mass %.3f (theory 8, DBI4). The symplectic integrator conserves the coupled "
            "energy E_theta+E_phi+E_coupling to %.1e (< 1%%). G2-G6 may proceed."
            % (a["force_diff_vs_force_cos"], a["psi_late"],
               b["force_diff_vs_sine_gordon"], b["kink_rest_mass"], c["drift"]))
    else:
        verdict = "FALHOU (parar)"
        statement = ("Gate failed (A=%s, B=%s, C=%s) -- per protocol the transfer and "
                     "collision experiments must NOT proceed until fixed."
                     % (a_ok, b_ok, c_ok))
    print("-" * 70)
    print(f"VERDICT G1: {verdict}")
    print(f"  {statement}")

    out = {"theta_pure": a, "phi_pure": {**b, "sine_gordon_theory_mass_comparison": sg_theory_mass},
           "conservation": c, "A_ok": bool(a_ok), "B_ok": bool(b_ok), "C_ok": bool(c_ok),
           "passed": passed, "verdict": verdict, "statement": statement}
    gc.save_json("G1_coupled", out)
    _write_md(out)
    return out


def _write_md(out):
    a, b, c = out["theta_pure"], out["phi_pure"], out["conservation"]
    lines = [
        "# G1 -- Dinâmica acoplada θ+φ e validação obrigatória",
        "",
        "A ação completa `S = Σ Δτ[1−cos(φ+Δθ)]` com **ambos** os campos dinâmicos",
        "(`gauge_core`). θ vive nos nós, φ (gauge, compacto) nos links; a combinação",
        "invariante de Stückelberg é `u_i = φ_i + (θ_{i+1}−θ_i)`. Três verificações",
        "obrigatórias antes de G2–G6 (parar se falhar):",
        "",
        "## (A) Limite θ-puro (φ=0) reproduz DBI1/DBI3",
        "",
        f"- `force_theta(·, φ=0)` − `force_cos`: máx |diff| = {a['force_diff_vs_force_cos']:.1e} "
        "(idêntico, propagação a velocidade unitária).",
        f"- Colisão escalar (gauge congelado): ψ_tardio = {a['psi_late']:+.3f} → "
        f"**pass-through = {a['passthrough']}** (o nulo escalar de DBI3).",
        "",
        "## (B) Limite φ-puro (θ=0) reproduz DBI4",
        "",
        f"- `force_phi(θ=0, ·)` − `(1/dx²)·sine-Gordon`: máx |diff| interior = "
        f"{b['force_diff_vs_sine_gordon']:.1e} (idêntico a menos do fator global de tempo).",
        f"- Kink compacto explícito (winding {b['winding']:.0f}): massa de repouso = "
        f"{b['kink_rest_mass']:.3f} (teoria sine-Gordon {b['sine_gordon_theory_mass_comparison']:.0f}); "
        f"após T: contagem {b['count_initial']}→{b['count_after']}, "
        f"**estável = {b['stable']}**.",
        "",
        "## (C) Conservação de energia (propagação livre acoplada)",
        "",
        f"E_total = E_θ + E_φ + E_acoplamento: {c['E0']['E_total']:.3f} → "
        f"{c['E1']['E_total']:.3f}, deriva = **{c['drift']:.1e}** (< 1%).",
        "",
        f"## VERDICT G1: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (gc.OUTDIR / "G1_coupled.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

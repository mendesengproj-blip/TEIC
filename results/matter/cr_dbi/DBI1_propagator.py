"""DBI1 -- the full cos propagator and its mandatory consistency validation.

The minimal action S = sum_links Dtau [1 - cos(phi + Dtheta)] has the lattice
sine-Gordon EOM; its force is force_cos = d/dx[sin(d theta)] (dbi_core).  Before any
collision we VALIDATE (protocol step 2 -- stop and report on failure):

  (A) WEAK FIELD reproduces BD: evolving the same initial data with the cos force and
      with the linear (BD) force gives the same trajectory as amplitude -> 0, with the
      difference scaling as amplitude^2 (the leading sin(u)-u correction is u^3/6).
  (B) STATIC reduces to D3: the weak-field static cos solve is the linear Poisson
      problem, whose radial solution is theta ~ 1/r (D3).  We confirm the 1/r tail.
  (C) CONSERVATION: the symplectic integrator conserves the cos energy on free
      propagation (no collision) to a small drift.

Output: DBI1_propagator.{md,json}.
"""

from __future__ import annotations

import numpy as np

import dbi_core as dbi


def weak_field_reproduces_bd():
    """Max |theta_cos - theta_linear| / |theta_linear| vs amplitude (must -> 0 ~ amp^2)."""
    x, dx = dbi.make_grid()
    dt = 0.2 * dx
    amps = [0.005, 0.01, 0.02, 0.04, 0.08]
    rels = []
    for amp in amps:
        th0, v0 = dbi.two_packets(x, amp)
        thc, _, _ = dbi.evolve(th0, v0, dbi.force_cos, dx, dt, 1500)
        thl, _, _ = dbi.evolve(th0, v0, dbi.force_linear, dx, dt, 1500)
        rels.append(float(np.max(np.abs(thc - thl)) / np.max(np.abs(thl))))
    # scaling exponent of rel-diff vs amp (leading correction u^3/6 -> rel ~ amp^2)
    p = float(np.polyfit(np.log(amps), np.log(rels), 1)[0])
    return amps, rels, p


def static_reduces_to_d3():
    """Weak-field static cos solve = linear Poisson -> theta ~ 1/r (tail exponent ~ -1)."""
    edges, centers, sv = dbi.cx.radial_grid(60.0, 40, r_min=1.0)
    q = dbi.cx.radial_source_core(centers, sv, r_core=4.0, w_source=1.0)
    theta = dbi.radial_static(centers, sv, q, K=1.0)
    A, C = dbi.cx.fit_amplitude(centers, theta, 4.0, 0.6 * 60.0)
    use = (centers >= 4.0) & (centers <= 0.6 * 60.0)
    resid = theta[use] - C
    ok = resid > 0
    p = float(np.polyfit(np.log(centers[use][ok]), np.log(resid[ok]), 1)[0])
    return A, C, p


def energy_conservation():
    """Cos energy drift over a long FREE propagation (single packet, no collision)."""
    x, dx = dbi.make_grid()
    dt = 0.2 * dx
    th0, v0 = dbi.packet(x, 0.5, 0.0, 3.0, +1)
    def E(th, v): return float(np.sum(dbi.energy_density(th, v, dx, "cos")) * dx)
    E0 = E(th0, v0)
    th, v, _ = dbi.evolve(th0, v0, dbi.force_cos, dx, dt, 2000)
    E1 = E(th, v)
    return E0, E1, abs(E1 - E0) / E0


def main():
    print("=" * 70)
    print("DBI1 -- FULL COS PROPAGATOR + MANDATORY VALIDATION")
    print("=" * 70)
    amps, rels, p = weak_field_reproduces_bd()
    print("  (A) weak-field cos vs BD (linear):")
    for a, r in zip(amps, rels):
        print(f"      amp={a:.3f}: max rel diff = {r:.2e}")
    print(f"      scaling rel ~ amp^{p:.2f} (expect ~2, leading u^3/6 correction)")

    A, C, p_tail = static_reduces_to_d3()
    print(f"  (B) static weak-field solve: 1/r amplitude A={A:.3f}, tail exponent={p_tail:.3f} (want -1)")

    E0, E1, drift = energy_conservation()
    print(f"  (C) cos energy: E0={E0:.4f} -> E1={E1:.4f}, drift={drift:.2e}")

    bd_ok = rels[0] < 1e-4 and 1.5 < p < 2.6
    d3_ok = abs(p_tail + 1.0) < 0.1
    cons_ok = drift < 1e-2
    passed = bd_ok and d3_ok and cons_ok

    if passed:
        verdict = "VALIDADO"
        statement = (
            "The cos propagator is consistent: it reproduces the linear BD evolution in "
            "weak field (rel diff %.0e at amp=%.3f, scaling ~ amp^%.1f), its static "
            "weak-field limit is D3's 1/r potential (tail exponent %.2f), and the "
            "symplectic integrator conserves the cos energy (drift %.0e). DBI3 may "
            "proceed." % (rels[0], amps[0], p, p_tail, drift))
    else:
        verdict = "FALHOU (parar)"
        statement = ("Validation failed (BD=%s, D3=%s, conservation=%s) -- per protocol "
                     "step 2, the collision experiments must NOT proceed until the "
                     "propagator is fixed." % (bd_ok, d3_ok, cons_ok))
    print("-" * 70)
    print(f"VERDICT DBI1: {verdict}")
    print(f"  {statement}")

    out = {"weak_field": {"amps": amps, "rel_diffs": rels, "scaling_exponent": p},
           "static_d3": {"A": A, "C": C, "tail_exponent": p_tail},
           "energy_conservation": {"E0": E0, "E1": E1, "drift": drift},
           "bd_ok": bool(bd_ok), "d3_ok": bool(d3_ok), "conservation_ok": bool(cons_ok),
           "passed": bool(passed), "verdict": verdict, "statement": statement}
    dbi.save_json("DBI1_propagator", out)
    _write_md(out)
    return out


def _write_md(out):
    w = out["weak_field"]
    lines = [
        "# DBI1 -- Propagador cos e validação obrigatória",
        "",
        "A ação mínima `S = Σ Δτ[1−cos(φ+Δθ)]` tem EOM sine-Gordon de rede; a força é",
        "`force_cos = d/dx[sin(Δθ)]`. Validação antes de qualquer colisão (parar se falhar):",
        "",
        "## (A) Campo fraco reproduz BD",
        "",
        "| amp | max rel diff (cos vs linear) |",
        "|-----|-------------------------------|",
    ]
    for a, r in zip(w["amps"], w["rel_diffs"]):
        lines.append(f"| {a:.3f} | {r:.2e} |")
    lines += [
        "",
        f"Escala como `rel ~ amp^{w['scaling_exponent']:.2f}` (esperado ~2; correção "
        "principal sin(u)−u = −u³/6).",
        "",
        "## (B) Estático reduz a D3",
        "",
        f"Solução estática de campo fraco: amplitude 1/r A = {out['static_d3']['A']:.3f}, "
        f"expoente da cauda = {out['static_d3']['tail_exponent']:.3f} (esperado −1) → θ ~ 1/r.",
        "",
        "## (C) Conservação de energia (propagação livre)",
        "",
        f"Energia cos: {out['energy_conservation']['E0']:.4f} → "
        f"{out['energy_conservation']['E1']:.4f}, deriva {out['energy_conservation']['drift']:.1e}.",
        "",
        f"## VERDICT DBI1: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (dbi.OUTDIR / "DBI1_propagator.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

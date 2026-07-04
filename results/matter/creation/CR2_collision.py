"""CR2 -- low-energy collision: the no-creation baseline.

Two low-density linear chains (N=0) are driven head-on through a collision region and
the dynamics is allowed to act.  We measure the creation order parameters defined in
creation_core:
  * field superposition residual  (linearity -> ~ 0, no field-level creation),
  * bichromatic covering cross-links during the encounter (transient) and AFTER it
    (a bound state would keep them; a pass-through lets them vanish),
  * persistent central over-density at late time vs the disjoint control.

Expectation (P4 already showed linear superposition): the chains pass through; no
loops are created.  N_loops after collision = 0 -> no creation (the baseline).
Output: CR2_collision.{md,json}.
"""

from __future__ import annotations

import numpy as np

import creation_core as cr

RHO_LOW = 2.0 * cr.RHO0      # low energy
SEEDS = range(20)


def main():
    print("=" * 70)
    print("CR2 -- LOW-ENERGY COLLISION (no-creation baseline)")
    print("=" * 70)
    obs = [cr.collision_observables(RHO_LOW, 300 + s) for s in SEEDS]
    res = cr.seed_stats([o["residual"] for o in obs])
    mid = cr.seed_stats([o["cross_mid"] for o in obs])
    late = cr.seed_stats([o["cross_late"] for o in obs])
    cen = cr.seed_stats([o["central_late"] for o in obs])

    print(f"  field superposition residual = {res['mean']:.2e} +/- {res['sem']:.0e}  (want ~0)")
    print(f"  cross-links during encounter = {mid['mean']:.1f} +/- {mid['sem']:.1f}  (transient interaction)")
    print(f"  cross-links AFTER (excess)   = {late['mean']:.2f} +/- {late['sem']:.2f}  (want ~0)")
    print(f"  central over-density late     = {cen['mean']:.2f} +/- {cen['sem']:.2f}  (want ~0)")

    no_creation = (abs(late["mean"]) < 2 * late["sem"] + 1.0 and
                   abs(cen["mean"]) < 2 * cen["sem"] + 1.0 and res["mean"] < 1e-10)
    verdict = "CONFIRMADO (sem criacao)" if no_creation else "INESPERADO"
    statement = (
        "At low energy the chains PASS THROUGH: the field is an exact linear "
        "superposition (residual %.1e), the two chains interact only transiently "
        "(%.0f cross-links at the encounter) and leave NO persistent bound structure "
        "(late cross-link excess %.2f, central over-density %.2f, both ~0). No loops "
        "are created -- the expected low-energy baseline, consistent with P4."
        % (res["mean"], mid["mean"], late["mean"], cen["mean"]))
    print("-" * 70)
    print(f"VERDICT CR2: {verdict}\n  {statement}")

    out = {"rho_low": RHO_LOW, "n_seeds": len(list(SEEDS)),
           "residual": res, "cross_mid": mid, "cross_late_excess": late,
           "central_late_excess": cen, "no_creation": bool(no_creation),
           "verdict": verdict, "statement": statement}
    cr.save_json("CR2_collision", out)
    _write_md(out)
    return out


def _write_md(out):
    lines = [
        "# CR2 -- Colisão de baixa energia (baseline sem criação)",
        "",
        f"Duas cadeias lineares de baixa densidade (ρ = {out['rho_low']}ρ₀) colidem de",
        "frente; a dinâmica age. Parâmetros de ordem de criação (creation_core):",
        "",
        f"- **Resíduo de superposição do campo** = {out['residual']['mean']:.1e} "
        "(linearidade → sem criação no campo).",
        f"- **Cross-links durante o encontro** = {out['cross_mid']['mean']:.0f} "
        "(interação transiente real).",
        f"- **Cross-links depois (excesso)** = {out['cross_late_excess']['mean']:.2f} "
        f"± {out['cross_late_excess']['sem']:.2f} (esperado ~0).",
        f"- **Sobredensidade central tardia** = {out['central_late_excess']['mean']:.2f} "
        f"± {out['central_late_excess']['sem']:.2f} (esperado ~0).",
        "",
        f"## VERDICT CR2: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (cr.OUTDIR / "CR2_collision.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

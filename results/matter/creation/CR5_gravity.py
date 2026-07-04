"""CR5 -- the gravitational field around the collision: is theta conserved?

D3: a causal-density source of weight w produces theta(r) ~ A/r with A proportional
to w (linear action).  The total causal energy is conserved across the collision
(CR4), so the total source weight is conserved.  Therefore the far field must satisfy

    theta_A(r) + theta_B(r)  ->  theta_C(r)      (A(w_A) + A(w_B) = A(w_A + w_B)),

i.e. the gravitational field is conserved through the collision -- trivially, because
the dynamics is linear and no new matter is created.  We MEASURE this additivity with
the D3 radial solver (complexity_core), depositing source weights equal to the chains'
causal energy (event rate), never a mass.

Output: CR5_gravity.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import creation_core as cr
import complexity_core as cx

L, N_BINS, R_CORE, K = 60.0, 40, 4.0, 1.0


def main():
    print("=" * 70)
    print("CR5 -- GRAVITATIONAL FIELD theta(r) AROUND THE COLLISION")
    print("=" * 70)
    edges, centers, sv = cx.radial_grid(L, N_BINS, r_min=1.0)

    # causal energies (event rates) of the two chains = source weights (no mass)
    rng = np.random.default_rng(0)
    evA = cr.sprinkle_tube(20.0, 0, cr.T_SPAN, 0.0, +cr.VEL, cr.WIDTH, rng)
    evB = cr.sprinkle_tube(20.0, 0, cr.T_SPAN, 0.0, -cr.VEL, cr.WIDTH, rng)
    wA = cr.e_causal(evA, 0, cr.T_SPAN)
    wB = cr.e_causal(evB, 0, cr.T_SPAN)
    print(f"  source weights (causal energy): wA={wA:.2f}  wB={wB:.2f}")

    def field(w):
        q = cx.radial_source_core(centers, sv, R_CORE, w_source=float(w))
        return cx.radial_solve(centers, sv, q, K)

    thA, thB = field(wA), field(wB)
    thC = field(wA + wB)                       # combined source (post-collision total)
    sum_field = thA + thB

    # additivity residual on the tail
    use = (centers >= R_CORE) & (centers <= 0.6 * L)
    resid = float(np.max(np.abs(thC[use] - sum_field[use])) /
                  np.max(np.abs(thC[use])))
    A_A, _ = cx.fit_amplitude(centers, thA, R_CORE, 0.6 * L)
    A_B, _ = cx.fit_amplitude(centers, thB, R_CORE, 0.6 * L)
    A_C, _ = cx.fit_amplitude(centers, thC, R_CORE, 0.6 * L)
    amp_resid = abs((A_A + A_B) - A_C) / abs(A_C)

    print(f"  1/r amplitudes: A_A={A_A:.3f}  A_B={A_B:.3f}  A_A+A_B={A_A+A_B:.3f}  A_C={A_C:.3f}")
    print(f"  field additivity residual (tail) = {resid:.2e}")
    print(f"  amplitude additivity residual    = {amp_resid:.2e}")

    conserved = resid < 1e-9 and amp_resid < 1e-6
    verdict = "SIM" if conserved else "NAO"
    statement = (
        "The gravitational field is CONSERVED through the collision: the combined "
        "source (the conserved total causal energy, CR4) produces exactly the sum of "
        "the individual 1/r fields (A_A+A_B=%.3f vs A_C=%.3f, residual %.0e). Because "
        "the D3 action is linear and no matter is created (CR3), theta_A+theta_B -> "
        "theta_C holds identically: the energy gravitates the same way before and "
        "after. This is a self-consistency closure (linearity), not a new mechanism; "
        "D3's caveat that the prefactor G is non-universal still applies."
        % (A_A + A_B, A_C, resid))
    print("-" * 70)
    print(f"VERDICT CR5: {verdict}\n  {statement}")

    _figure(centers, thA, thB, thC, sum_field)
    out = {"L": L, "n_bins": N_BINS, "r_core": R_CORE, "K": K,
           "wA": wA, "wB": wB, "A_A": A_A, "A_B": A_B, "A_C": A_C,
           "field_additivity_residual": resid, "amplitude_additivity_residual": amp_resid,
           "theta_conserved": bool(conserved), "verdict": verdict, "statement": statement}
    cr.save_json("CR5_gravity", out)
    _write_md(out)
    return out


def _figure(centers, thA, thB, thC, sum_field):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    m = (centers >= R_CORE) & (centers <= 0.6 * L)
    ax.plot(centers[m], thA[m], "-", color="#16a085", label="theta_A (chain A)")
    ax.plot(centers[m], thB[m], "-", color="#2980b9", label="theta_B (chain B)")
    ax.plot(centers[m], sum_field[m], "--", color="#7f8c8d", lw=2,
            label="theta_A + theta_B")
    ax.plot(centers[m], thC[m], ":", color="#c0392b", lw=2,
            label="theta_C (combined source, post-collision)")
    ax.set_xlabel("r (network units)")
    ax.set_ylabel("theta(r)")
    ax.set_title("CR5 -- gravitational field is conserved (linear): theta_A+theta_B = theta_C")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(cr.OUTDIR / "CR5_gravity.png", dpi=130)
    plt.close(fig)


def _write_md(out):
    lines = [
        "# CR5 -- O campo gravitacional da matéria (não) criada",
        "",
        "D3: uma fonte de densidade causal de peso w gera `θ(r) ~ A/r` com A ∝ w (ação",
        "linear). A energia causal total é conservada na colisão (CR4) → o peso total",
        "da fonte é conservado → o campo distante satisfaz `θ_A + θ_B → θ_C`.",
        "",
        f"- pesos da fonte (energia causal): wA = {out['wA']:.2f}, wB = {out['wB']:.2f}",
        f"- amplitudes 1/r: A_A = {out['A_A']:.3f}, A_B = {out['A_B']:.3f}, "
        f"A_A+A_B = {out['A_A']+out['A_B']:.3f}, A_C = {out['A_C']:.3f}",
        f"- resíduo de aditividade do campo (cauda): **{out['field_additivity_residual']:.1e}**",
        f"- resíduo de aditividade da amplitude: **{out['amplitude_additivity_residual']:.1e}**",
        "",
        f"## VERDICT CR5: {out['verdict']}",
        "",
        out["statement"],
        "",
        "![gravidade](CR5_gravity.png)",
        "",
    ]
    (cr.OUTDIR / "CR5_gravity.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

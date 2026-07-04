"""CC5 -- the gravity link: does the field theta(r) sourced by a structure scale with N?

D3 showed: a localized causal-density source produces an equilibrium field
theta(r) ~ 1/r (the Newtonian potential).  If mass = internal complexity, then a
structure of complexity N must deposit a causal-density source proportional to N
(its proper time tau(N) = a N, CC2), and therefore source a 1/r tail of amplitude

    theta(r) ~ A(N) / r ,     A(N)  proportional to  N ?

This closes the loop  complexity N -> cost C(N) -> rest mass tau(N) -> theta(r) -> gravity.

We deposit a source core of total weight  w = N  (equivalently proportional to the
measured tau = a N), solve the SAME quadratic gradient action / discrete Poisson
equation used by D3 (results/bridge/d3_audit), fit theta = A/r + C on the tail, and
test A(N) proportional to N.  NO G, NO mass, NO Schwarzschild: w is a dimensionless
deposited causal weight; A is read off the solved field.

HONESTY: D3's action is LINEAR, so A is proportional to the deposited weight by
construction.  The non-trivial physics is the IDENTIFICATION source-weight = N
(the hypothesis) and that the 1/r SHAPE survives for every N.  This is a
self-consistency closure, not an independent derivation; graded accordingly.
D3 itself found the prefactor G to be non-universal -- we inherit that caveat.

Output: CC5_gravity.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import complexity_core as cc

L, N_BINS, R_CORE, K = 60.0, 40, 4.0, 1.0
TAU_PER_LOOP = 10.366        # measured in CC2 (proper time per internal cycle)


def main():
    print("=" * 70)
    print("CC5 -- THETA(r) SOURCED BY A STRUCTURE vs COMPLEXITY N")
    print("=" * 70)
    edges, centers, sv = cc.radial_grid(L, N_BINS, r_min=1.0)

    Ns = [n for n in cc.N_LADDER if n > 0]      # N=0 sources nothing (flat theta=0)
    curves, amps, exps = {}, [], []
    for N in Ns:
        q = cc.radial_source_core(centers, sv, R_CORE, w_source=float(N))
        theta = cc.radial_solve(centers, sv, q, K)
        A, C = cc.fit_amplitude(centers, theta, R_CORE, 0.6 * L)
        # exponent of (theta - C) vs r on the tail (should be ~ -1 for 1/r)
        use = (centers >= R_CORE) & (centers <= 0.6 * L)
        resid = theta[use] - C
        ok = resid > 0
        p = (float(np.polyfit(np.log(centers[use][ok]), np.log(resid[ok]), 1)[0])
             if ok.sum() >= 4 else float("nan"))
        curves[N] = theta
        amps.append(A)
        exps.append(p)
        print(f"  N={N:4d}: A(1/r amplitude)={A:8.4f}  C(offset)={C:+.4f}  exponent={p:.3f}")

    Narr, Aarr = np.array(Ns, dtype=float), np.array(amps)
    # proportional fit A = k N
    k_prop = float(np.sum(Narr * Aarr) / np.sum(Narr ** 2))
    r2 = 1.0 - np.sum((Aarr - k_prop * Narr) ** 2) / np.sum((Aarr - Aarr.mean()) ** 2)
    # ratio A/N constancy
    ratio = Aarr / Narr
    ratio_cv = float(np.std(ratio) / np.mean(ratio))
    mean_exp = float(np.nanmean(exps))

    print("-" * 70)
    print(f"  A = k N  with k = {k_prop:.4f},  R^2 = {r2:.6f}")
    print(f"  A/N constancy: CV = {ratio_cv:.2e}")
    print(f"  mean tail exponent = {mean_exp:.3f}  (want -1 for 1/r)")

    shape_ok = abs(mean_exp + 1.0) < 0.12
    prop_ok = r2 > 0.999 and ratio_cv < 1e-6
    if prop_ok and shape_ok:
        verdict, grade = "CONFIRMADO", "B"
        statement = ("theta(r) keeps the 1/r Newtonian shape (mean tail exponent "
                     "%.3f) for every N, and its amplitude A(N) is STRICTLY "
                     "proportional to N (R^2=%.5f, A/N constant to %.0e). The loop "
                     "complexity -> cost tau -> sourced potential chain closes: a "
                     "structure of complexity N gravitates like a mass proportional to "
                     "N. REAL but INHERITED/definitional: D3's action is linear, so the "
                     "proportionality follows once source-weight = N is identified "
                     "(the hypothesis); the 1/r shape is D3's, and its prefactor G is "
                     "non-universal (D3 caveat)." % (mean_exp, r2, ratio_cv))
    else:
        verdict, grade = "PARCIAL", "C"
        statement = ("The amplitude tracks N but the 1/r shape or the proportionality "
                     "is not clean across the ladder at this grid size.")
    print(f"VERDICT CC5: {verdict}  (grade {grade})")
    print(f"  {statement}")

    _figure(centers, curves, Ns, Narr, Aarr, k_prop)
    out = {"L": L, "n_bins": N_BINS, "r_core": R_CORE, "K": K,
           "N": Ns, "amplitude_A": amps, "tail_exponent": exps,
           "A_eq_kN": k_prop, "r2_proportional": float(r2),
           "ratio_A_over_N_cv": ratio_cv, "mean_tail_exponent": mean_exp,
           "tau_per_loop_from_CC2": TAU_PER_LOOP,
           "verdict": verdict, "grade": grade, "statement": statement}
    cc.save_json("CC5_gravity", out)
    _write_md(centers, curves, Ns, amps, exps, out)
    return out


def _figure(centers, curves, Ns, Narr, Aarr, k_prop):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    for N in Ns:
        ax.plot(centers, curves[N], "-", label=f"N={N}")
    ax.set_xlabel("r (network units)")
    ax.set_ylabel("theta(r)")
    ax.set_title("CC5 -- field sourced by complexity N")
    ax.set_xlim(R_CORE, 0.6 * L)
    ax.legend(fontsize=8)

    ax2 = axes[1]
    ax2.plot(Narr, Aarr, "o", color="#c0392b", ms=8, label="fitted 1/r amplitude A(N)")
    xs = np.linspace(0, Narr.max(), 50)
    ax2.plot(xs, k_prop * xs, "-", color="#2c3e50", label=f"A = {k_prop:.3f} N")
    ax2.set_xlabel("internal complexity N")
    ax2.set_ylabel("1/r amplitude A")
    ax2.set_title("CC5 -- gravitational amplitude is proportional to N")
    ax2.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(cc.OUTDIR / "CC5_gravity.png", dpi=130)
    plt.close(fig)


def _write_md(centers, curves, Ns, amps, exps, out):
    lines = [
        "# CC5 -- O elo com a gravidade: θ(r) ∝ N",
        "",
        "D3: uma fonte de densidade causal localizada produz `θ(r) ~ 1/r` (potencial",
        "newtoniano). Se massa = complexidade interna, uma estrutura de complexidade N",
        "deposita uma fonte ∝ N (seu tempo próprio τ = a·N, CC2) e gera",
        "`θ(r) ~ A(N)/r` com **A(N) ∝ N**. Isto fecha o ciclo:",
        "",
        "`complexidade N → custo C(N) → massa τ(N) → θ(r) → gravidade`.",
        "",
        "| N | A (amplitude 1/r) | expoente da cauda |",
        "|---|-------------------|-------------------|",
    ]
    for N, A, p in zip(Ns, amps, exps):
        lines.append(f"| {N} | {A:.4f} | {p:.3f} |")
    lines += [
        "",
        f"- `A = k N` com k = {out['A_eq_kN']:.4f}, R² = {out['r2_proportional']:.6f}",
        f"- constância de A/N: CV = {out['ratio_A_over_N_cv']:.1e}",
        f"- expoente médio da cauda = {out['mean_tail_exponent']:.3f} (esperado −1)",
        "",
        f"## VERDICT CC5: {out['verdict']}  (grade {out['grade']})",
        "",
        out["statement"],
        "",
        "### Honestidade",
        "",
        "A ação de D3 é **linear**, logo A ∝ peso depositado é automático; o conteúdo",
        "não-trivial é a **identificação peso-da-fonte = N** (a própria hipótese) e que",
        "a forma 1/r sobrevive para todo N. É um fecho de auto-consistência, não uma",
        "derivação independente. Herdamos a ressalva de D3: o prefator G não é universal.",
        "",
        "![gravidade](CC5_gravity.png)",
        "",
    ]
    (cc.OUTDIR / "CC5_gravity.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

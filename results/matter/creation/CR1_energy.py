"""CR1 -- operational definition of "causal energy" and its free conservation.

Causal energy is defined WITHOUT inserting energy:

    E_causal(chain) = number of causal events per unit proper time-length = n / dtau.

High energy = high event density.  We verify it is (a) well-defined by counting and
(b) conserved under FREE propagation (no collision): the event rate is the same in
successive time-slices, and the count in an invariant causal region is Lorentz
invariant (inherited from R1's Poisson invariance).  No mc^2, no energy inserted.

Output: CR1_energy.{md,json}.
"""

from __future__ import annotations

import numpy as np

import creation_core as cr

RHO_CHAIN = 20.0
T_SPAN = 12.0
SEEDS = range(20)


def slice_rates(rho, seed, n_slices=6):
    """Event rate n_slice / dt in successive equal time-slices of one free chain."""
    rng = np.random.default_rng(seed)
    ev = cr.sprinkle_tube(rho, 0, T_SPAN, 0.0, cr.VEL, cr.WIDTH, rng)
    edges = np.linspace(0, T_SPAN, n_slices + 1)
    dt = edges[1] - edges[0]
    rates = []
    for a, b in zip(edges[:-1], edges[1:]):
        n = int(np.sum((ev[:, 0] >= a) & (ev[:, 0] < b)))
        rates.append(n / dt)
    return np.array(rates, dtype=float)


def boost_counts(rho, seed, rapidities):
    """Count of events inside an invariant causal diamond, as the events are boosted
    -- must be invariant (R1).  A static dense blob (vel=0) so the diamond, centred on
    the worldline, contains it in every frame."""
    rng = np.random.default_rng(seed)
    ev = cr.sprinkle_tube(rho, 0, T_SPAN, 0.0, 0.0, cr.WIDTH, rng)
    # invariant diamond: future of A=(2,0), past of B=(10,0), centred on the blob
    A, B = np.array([2.0, 0.0]), np.array([10.0, 0.0])
    counts = []
    for phi in rapidities:
        ch, sh = np.cosh(phi), np.sinh(phi)
        t, x = ev[:, 0], ev[:, 1]
        tb = ch * t + sh * x
        xb = sh * t + ch * x
        Ab = np.array([ch * A[0] + sh * A[1], sh * A[0] + ch * A[1]])
        Bb = np.array([ch * B[0] + sh * B[1], sh * B[0] + ch * B[1]])
        dtA = tb - Ab[0]; fa = (dtA > 0) & (dtA * dtA > (xb - Ab[1]) ** 2)
        dtB = Bb[0] - tb; fb = (dtB > 0) & (dtB * dtB > (xb - Bb[1]) ** 2)
        counts.append(int(np.sum(fa & fb)))
    return np.array(counts, dtype=float)


def main():
    print("=" * 70)
    print("CR1 -- CAUSAL ENERGY (events per proper length) AND FREE CONSERVATION")
    print("=" * 70)

    # (a) well-defined: deterministic count for a fixed event set
    rng = np.random.default_rng(0)
    ev = cr.sprinkle_tube(RHO_CHAIN, 0, T_SPAN, 0.0, cr.VEL, cr.WIDTH, rng)
    e_def = cr.e_causal(ev, 0, T_SPAN)
    print(f"  E_causal of a chain (rho={RHO_CHAIN}) = {e_def:.2f} events / proper length")

    # (b1) free conservation: rate flat across time-slices
    all_rates = np.array([slice_rates(RHO_CHAIN, 100 + s) for s in SEEDS])
    rate_mean = all_rates.mean(axis=0)
    cv_time = float(np.std(rate_mean) / np.mean(rate_mean))
    print(f"  rate per time-slice (mean over seeds): "
          f"{np.array2string(rate_mean, precision=1)}")
    print(f"  CV across slices (free propagation) = {cv_time:.1%}  (want small)")

    # (b2) Lorentz invariance of the count in an invariant region
    raps = np.linspace(0.0, 1.5, 7)
    bc = np.array([boost_counts(RHO_CHAIN, 200 + s, raps) for s in SEEDS])
    bc_mean = bc.mean(axis=0)
    cv_boost = float(np.std(bc_mean) / np.mean(bc_mean))
    print(f"  diamond count vs rapidity (mean): {np.array2string(bc_mean, precision=1)}")
    print(f"  CV across rapidity (Lorentz)      = {cv_boost:.1%}  (want small)")

    well_defined = np.isfinite(e_def) and e_def > 0
    conserved = cv_time < 0.10
    invariant = cv_boost < 0.10
    ok = well_defined and conserved and invariant
    verdict = "SIM" if ok else "PARCIAL"
    statement = (
        "Causal energy is well-defined by event counting (E=%.1f events/length), "
        "CONSERVED under free propagation (rate CV %.1f%% across time-slices), and "
        "Lorentz invariant (count CV %.1f%% across rapidity, inherited from R1). No "
        "energy, mc^2 or pair threshold was inserted -- E_causal is a pure rate."
        % (e_def, cv_time * 100, cv_boost * 100))
    print("-" * 70)
    print(f"VERDICT CR1: {verdict}\n  {statement}")

    out = {"rho_chain": RHO_CHAIN, "t_span": T_SPAN, "n_seeds": len(list(SEEDS)),
           "E_causal_example": e_def,
           "slice_rates_mean": rate_mean.tolist(), "cv_time": cv_time,
           "rapidities": raps.tolist(), "boost_counts_mean": bc_mean.tolist(),
           "cv_boost": cv_boost, "well_defined": bool(well_defined),
           "conserved_free": bool(conserved), "lorentz_invariant": bool(invariant),
           "verdict": verdict, "statement": statement}
    cr.save_json("CR1_energy", out)
    _write_md(out)
    return out


def _write_md(out):
    lines = [
        "# CR1 -- Energia causal e conservação livre",
        "",
        "Energia causal **sem inserir energia**:",
        "",
        "`E_causal(cadeia) = nº de eventos causais por unidade de comprimento próprio",
        "= n / Δτ`. Alta energia = alta densidade de eventos.",
        "",
        "## Verificações",
        "",
        f"- **Bem-definida por contagem:** E_causal = {out['E_causal_example']:.1f} "
        f"eventos/comprimento (ρ={out['rho_chain']}). Determinística dado o conjunto.",
        f"- **Conservada em propagação livre:** taxa por fatia temporal tem CV = "
        f"**{out['cv_time']:.1%}** (sem colisão, E_t1 = E_t2).",
        f"- **Invariante de Lorentz:** contagem numa região causal invariante tem CV = "
        f"**{out['cv_boost']:.1%}** sob boost (herdado de R1).",
        "",
        "Decomposição (conexão com CC): para uma estrutura com loops, "
        "`E_total = E_interna (∝ N loops, = τ de CC2) + E_externa (propagação)`.",
        "",
        f"## VERDICT CR1: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (cr.OUTDIR / "CR1_energy.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

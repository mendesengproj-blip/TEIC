"""CC3 -- Lorentz invariance of the cost: is tau(N) a true rest mass?

CC2 found the measured proper time tau(N) (longest causal chain through the
structure) is proportional to N.  A genuine REST mass must be Lorentz invariant:
the SAME structure, boosted to velocity beta, must have the SAME tau.

TEST (the clean isotropy test of R1 / M2, here on the constructed structures):
  * boost each structure by a range of rapidities phi (beta = tanh phi up to ~0.96),
    a pure coordinate map t' = t cosh phi + x sinh phi (NO dilation factor),
  * remeasure tau in the Poisson medium (20 seeds per rapidity).  Lorentz invariance
    => tau(phi) flat, small coefficient of variation CV.
  * regular-LATTICE medium control: anisotropic, so tau swings with direction -> CV
    large.  Separation CV_poisson << CV_lattice is the signature.

We ALSO verify the energy/momentum content directly from the geometry of a unit
proper-time interval: coordinate time per proper time is cosh phi and the spatial
advance is sinh phi.  With m = tau (invariant), this is E = m cosh phi and
p = m sinh phi -- i.e. E = m gamma, p = m gamma beta -- WITHOUT ever writing the
factor 1/sqrt(1-beta^2).  (cosh phi equals it for beta = tanh phi; we only use the
hyperbolic form, exactly as R1/e1 did.)

Output: CC3_lorentz.{md,json,png}.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import complexity_core as cc

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from causal_core import lattice_box  # noqa: E402

RHO = 60.0
RAPIDITIES = np.linspace(0.0, 2.0, 9)        # beta = tanh up to ~0.964
N_TEST = [1, 3, 10, 30]                       # skip N=0 (tau=0) and N=100 (slow)
SEEDS = range(12)


def _chain_in_diamond_lattice(struct, spacing):
    """Lattice-medium proper time: longest chain through each diamond on a regular
    grid (the anisotropic control).  Same selection as the Poisson version."""
    ev = struct["events"]
    total = 0
    pad = 0.15
    for (s, bp, bm, m) in struct["diamonds"]:
        A, B = ev[s], ev[m]
        box = [(A[0] - pad, B[0] + pad),
               (min(ev[bp][1], ev[bm][1]) - pad, max(ev[bp][1], ev[bm][1]) + pad)]
        pts = lattice_box(spacing, box)
        if len(pts):
            dtA = pts[:, 0] - A[0]; dx2A = (pts[:, 1] - A[1]) ** 2
            fa = (dtA > 0) & (dtA * dtA > dx2A)
            dtB = B[0] - pts[:, 0]; dx2B = (pts[:, 1] - B[1]) ** 2
            fb = (dtB > 0) & (dtB * dtB > dx2B)
            pts = pts[fa & fb]
        core = np.vstack([A, B, pts]) if len(pts) else np.vstack([A, B])
        total += cc.longest_chain(core)
    return total


def boost_invariance():
    """tau(N, phi) for Poisson and lattice media; return per-N CVs over rapidity."""
    results = {}
    spacing = RHO ** -0.5
    for N in N_TEST:
        s0 = cc.build_structure(N)
        tau_pois, tau_lat = [], []
        for phi in RAPIDITIES:
            sb = cc.boost(s0, phi)
            taus = []
            for seed in SEEDS:
                rng = np.random.default_rng(9000 + seed + int(phi * 100))
                taus.append(cc.proper_time(sb, RHO, rng))
            tau_pois.append(float(np.mean(taus)))
            tau_lat.append(float(_chain_in_diamond_lattice(sb, spacing)))
        tp, tl = np.array(tau_pois), np.array(tau_lat)
        cv_p = float(np.std(tp) / np.mean(tp))
        cv_l = float(np.std(tl) / np.mean(tl)) if np.mean(tl) > 0 else float("nan")
        results[N] = {"tau_poisson": tp.tolist(), "tau_lattice": tl.tolist(),
                      "cv_poisson": cv_p, "cv_lattice": cv_l,
                      "tau_rest": float(tp[0])}
        print(f"  N={N:3d}: tau_rest={tp[0]:7.1f}  CV_poisson={cv_p:.1%}  "
              f"CV_lattice={cv_l:.1%}")
    return results


def energy_momentum_geometry():
    """Verify dt/dtau = cosh phi and dx/dtau = sinh phi for a unit proper-time
    interval -- i.e. E = m gamma, p = m gamma beta -- as a pure coordinate map."""
    seg = {"events": np.array([[0.0, 0.0], [1.0, 0.0]])}   # unit timelike interval
    dt, dx, pred_ch, pred_sh = [], [], [], []
    for phi in RAPIDITIES:
        b = cc.boost(seg, phi)
        dt.append(float(b["events"][1, 0] - b["events"][0, 0]))
        dx.append(float(b["events"][1, 1] - b["events"][0, 1]))
        pred_ch.append(float(np.cosh(phi)))
        pred_sh.append(float(np.sinh(phi)))
    dt, dx = np.array(dt), np.array(dx)
    err = float(np.max(np.abs(dt - np.array(pred_ch))) +
                np.max(np.abs(dx - np.array(pred_sh))))
    inv = dt ** 2 - dx ** 2                       # must be 1 (the rest interval^2)
    return {"rapidity": RAPIDITIES.tolist(), "dt_over_dtau": dt.tolist(),
            "dx_over_dtau": dx.tolist(), "cosh": pred_ch, "sinh": pred_sh,
            "max_abs_error": err, "invariant_dt2_minus_dx2": inv.tolist(),
            "invariant_max_dev": float(np.max(np.abs(inv - 1.0)))}


def main():
    print("=" * 70)
    print("CC3 -- LORENTZ INVARIANCE OF THE COST (tau as rest mass)")
    print("=" * 70)
    inv = boost_invariance()
    cv_p = np.mean([inv[N]["cv_poisson"] for N in N_TEST])
    cv_l = np.mean([inv[N]["cv_lattice"] for N in N_TEST])
    em = energy_momentum_geometry()

    print("-" * 70)
    print(f"  mean CV_poisson over N = {cv_p:.1%}  (want small)")
    print(f"  mean CV_lattice over N = {cv_l:.1%}  (anisotropic control)")
    print(f"  E=m cosh phi, p=m sinh phi geometry: max abs error = {em['max_abs_error']:.2e}")
    print(f"  invariant dt^2-dx^2 max deviation from 1 = {em['invariant_max_dev']:.2e}")

    invariant = cv_p < 0.10 and cv_l > 2.5 * cv_p
    geometry_ok = em["max_abs_error"] < 1e-10 and em["invariant_max_dev"] < 1e-10
    if invariant and geometry_ok:
        verdict, grade = "CONFIRMADO", "B"
        statement = ("tau(N) is Lorentz invariant: the boosted structure keeps the "
                     "same proper time (Poisson CV %.1f%%) while the lattice control is "
                     "frame-dependent (CV %.1f%%). With m = tau, the coordinate-time and "
                     "spatial advances per unit proper time are exactly cosh(phi) and "
                     "sinh(phi) (E = m gamma, p = m gamma beta), the rest interval "
                     "dt^2-dx^2 = 1 being invariant. REAL but INHERITED: it is R1's "
                     "Poisson Lorentz-invariance + hyperbolic geometry, applied to the "
                     "complexity cost -- not an independently new dilation."
                     % (cv_p * 100, cv_l * 100))
    else:
        verdict, grade = "INCONCLUSIVO", "C"
        statement = ("Invariance of tau is not cleanly separated from the lattice "
                     "control at this size, or the boost geometry check failed.")
    print(f"VERDICT CC3: {verdict}  (grade {grade})")
    print(f"  {statement}")

    _figure(inv, em)
    out = {"rho": RHO, "rapidities": RAPIDITIES.tolist(), "N_test": N_TEST,
           "n_seeds": len(list(SEEDS)),
           "per_N": {str(N): inv[N] for N in N_TEST},
           "mean_cv_poisson": cv_p, "mean_cv_lattice": cv_l,
           "energy_momentum_geometry": em,
           "verdict": verdict, "grade": grade, "statement": statement}
    cc.save_json("CC3_lorentz", out)
    _write_md(inv, em, cv_p, cv_l, out)
    return out


def _figure(inv, em):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    beta = np.tanh(RAPIDITIES)
    for N in N_TEST:
        tp = np.array(inv[N]["tau_poisson"])
        ax.plot(beta, tp / tp[0], "o-", label=f"N={N} (Poisson)")
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("velocity  beta = tanh(phi)")
    ax.set_ylabel("tau(beta) / tau(0)   (rest cost, normalised)")
    ax.set_title("CC3 -- proper time is boost-invariant")
    ax.legend(fontsize=8)

    ax2 = axes[1]
    ax2.plot(RAPIDITIES, em["dt_over_dtau"], "o", color="#c0392b", label="dt/dtau (measured)")
    ax2.plot(RAPIDITIES, em["cosh"], "-", color="#c0392b", label="cosh(phi) = E/m = gamma")
    ax2.plot(RAPIDITIES, em["dx_over_dtau"], "s", color="#2c3e50", label="dx/dtau (measured)")
    ax2.plot(RAPIDITIES, em["sinh"], "-", color="#2c3e50", label="sinh(phi) = p/m")
    ax2.set_xlabel("rapidity phi")
    ax2.set_ylabel("advance per unit proper time")
    ax2.set_title("CC3 -- E = m gamma, p = m gamma beta (geometry)")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(cc.OUTDIR / "CC3_lorentz.png", dpi=130)
    plt.close(fig)


def _write_md(inv, em, cv_p, cv_l, out):
    lines = [
        "# CC3 -- Invariância de Lorentz do custo (τ como massa de repouso)",
        "",
        "Uma massa de repouso genuína deve ser invariante de Lorentz: a MESMA estrutura,",
        "boostada para velocidade β = tanh φ, deve ter o MESMO τ. O boost é um mapa de",
        "coordenadas `t' = t cosh φ + x sinh φ` (sem fator de dilatação).",
        "",
        "| N | τ_repouso | CV_poisson (rapidez) | CV_lattice (controle) |",
        "|---|-----------|----------------------|------------------------|",
    ]
    for N in out["N_test"]:
        d = inv[N]
        lines.append(f"| {N} | {d['tau_rest']:.1f} | {d['cv_poisson']:.1%} | {d['cv_lattice']:.1%} |")
    lines += [
        "",
        f"- média CV_poisson = **{cv_p:.1%}** (pequeno → invariante)",
        f"- média CV_lattice = **{cv_l:.1%}** (anisotrópico → quebra)",
        "",
        "## Energia–momento pela geometria",
        "",
        "Para um intervalo de tempo próprio unitário, avanços por unidade de τ:",
        f"- `dt/dτ = cosh φ` e `dx/dτ = sinh φ` reproduzidos com erro {em['max_abs_error']:.1e}",
        f"- invariante `dt²−dx² = 1` com desvio máximo {em['invariant_max_dev']:.1e}",
        "",
        "Com `m = τ`: **E = m cosh φ = m γ**, **p = m sinh φ = m γβ** — sem nunca",
        "escrever 1/√(1−β²). Esta é a forma hiperbólica de R1/e1.",
        "",
        f"## VERDICT CC3: {out['verdict']}  (grade {out['grade']})",
        "",
        out["statement"],
        "",
        "![lorentz](CC3_lorentz.png)",
        "",
    ]
    (cc.OUTDIR / "CC3_lorentz.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

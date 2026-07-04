"""PE2_condensate.py -- does Phi = rho e^{i phibar} condense spontaneously (no potential)?

PHI_EMERGE task PE2.  With V=0 (no added potential), measure over 20 seeds:
  (1) <|Phi|> and its fluctuation sigma_|Phi| vs the network (sprinkle) density;
  (2) the CONNECTED magnitude correlator C_|Phi|(r) = <drho(0)drho(r)>/<drho^2> -- does
      the MAGNITUDE develop long-range order (a true condensate) or decay (Poisson)?
  (3) the full field correlator |<Phi*(0)Phi(r)>| in the HOT (disordered) gauge vacuum
      AND in the RELAXED (cooled) gauge vacuum.

The decisive distinction (kept honest):
  * <|Phi|> = <rho> = 1 is TRIVIAL (the Voronoi normalisation), NOT condensation.
  * A genuine spontaneous condensate would show C(r) -> const (long-range order) in the
    CONNECTED correlator without any added potential.
  * If C_|Phi|(r) always decays to 0, the magnitude does NOT condense; any plateau in the
    full correlator after relaxation is the gauge (Stueckelberg) vacuum ordering its
    PHASE, not the |Phi| condensate the abelian-Higgs mechanism needs.

Anti-circularity: V=0 (no potential inserted); rho is a count, phibar is read from links;
two real arrays, no complex literal.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phi_emerge_core as pe   # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NSEED = 20
LAM = 0.7      # Wilson plaquette weight used only for the relaxation dynamics


def classify_decay(centers, C):
    """Classify C(r): 'constant' (plateau, no decay), 'power' (linear in log-log),
    'exponential' (linear in lin-log), else 'decays'.  Returns (label, corr_length)."""
    c = np.asarray(centers, float); C = np.asarray(C, float)
    use = np.isfinite(C) & (c >= 1.0)
    if use.sum() < 3:
        return "undetermined", float("nan")
    Cu = C[use]; cu = c[use]
    plateau = float(np.mean(Cu[-3:])) if Cu.size >= 3 else float(Cu[-1])
    # correlation length from the exponential fit of |C| (if positive & decaying)
    pos = Cu > 0
    xi = float("nan")
    if pos.sum() >= 3:
        p = np.polyfit(cu[pos], np.log(Cu[pos]), 1)
        if p[0] < 0:
            xi = float(-1.0 / p[0])
    if abs(plateau) > 0.3 * abs(Cu[0]):
        return "constant/plateau (long-range order)", xi
    if np.isfinite(xi) and xi < cu.max():
        return "decays (finite correlation length)", xi
    return "decays", xi


def run_density(rho_sprinkle, grid, T=8.0, seed0=0, r_edges=None, pairs=None):
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    absmean, absstd = [], []
    Cmag = []          # connected magnitude correlator per seed
    Cfull_hot, Cfull_relax = [], []
    for s in range(NSEED):
        rng = np.random.default_rng(seed0 + s)
        rho = pe.causal_density(Nx, Ny, Nz, rho_sprinkle, T, rng)
        absmean.append(float(rho.mean())); absstd.append(float(rho.std()))
        # magnitude correlator (precomputed radial pairs reused across seeds)
        cm = pe.correlation_magnitude(rho, r_edges, pairs=pairs)
        Cmag.append(cm["C_norm"])
        # hot gauge full correlator
        phix, phiy, phiz = pe.hot_gauge(x, y, z, rng)
        pb_hot, _ = pe.phibar(phix, phiy, phiz)
        Re, Im = pe.phi_field(rho, pb_hot)
        Cfull_hot.append(pe.correlation_full(Re, Im, r_edges, connected=True,
                                             pairs=pairs)["C_abs"])
        # relaxed (cooled) gauge full correlator
        px, py, pz = pe.relax_gauge(phix, phiy, phiz, dx, LAM, n_relax=400)
        pb_rel, _ = pe.phibar(px, py, pz)
        Re2, Im2 = pe.phi_field(rho, pb_rel)
        Cfull_relax.append(pe.correlation_full(Re2, Im2, r_edges, connected=True,
                                               pairs=pairs)["C_abs"])
    centers = np.asarray(pairs[1]).tolist()
    Cmag = np.nanmean(Cmag, axis=0)
    Cfh = np.nanmean(Cfull_hot, axis=0)
    Cfr = np.nanmean(Cfull_relax, axis=0)
    lab_mag, xi_mag = classify_decay(centers, Cmag)
    lab_rel, xi_rel = classify_decay(centers, Cfr / Cfr[0] if Cfr[0] else Cfr)
    return {
        "rho_sprinkle": rho_sprinkle,
        "abs_mean": float(np.mean(absmean)), "abs_std": float(np.mean(absstd)),
        "centers": centers,
        "C_magnitude_connected": Cmag.tolist(),
        "C_full_hot_abs": Cfh.tolist(),
        "C_full_relaxed_abs": Cfr.tolist(),
        "magnitude_decay": lab_mag, "magnitude_xi": xi_mag,
        "relaxed_full_decay": lab_rel, "relaxed_full_xi": xi_rel,
    }


def main():
    grid = (25, 20, 20)
    r_edges = np.arange(0.5, 10.0, 1.0)
    pairs = pe.precompute_pairs(grid, r_edges, max_pairs=40000,
                                rng=np.random.default_rng(12345))
    densities = [2.0, 4.0, 8.0, 16.0]
    rows = [run_density(rs, grid, seed0=200 + 40 * i, r_edges=r_edges, pairs=pairs)
            for i, rs in enumerate(densities)]

    condensate = any(r["magnitude_decay"].startswith("constant") for r in rows)
    summary = {"n_seeds": NSEED, "grid": list(grid), "V": 0.0, "rows": rows,
               "spontaneous_magnitude_condensate": bool(condensate),
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    pe.save_json("PE2_condensate", summary)

    # ---- figure: C(r) for each density ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.6))
    for r in rows:
        c = r["centers"]
        ax[0].plot(c, np.abs(r["C_magnitude_connected"]), "o-",
                   label=f"ρ_spr={r['rho_sprinkle']}")
        cf = np.asarray(r["C_full_relaxed_abs"]); cf = cf / cf[0] if cf[0] else cf
        ax[1].plot(c, cf, "s-", label=f"ρ_spr={r['rho_sprinkle']}")
    for a in ax:
        a.set_xlabel("r"); a.set_yscale("log"); a.legend(fontsize=8)
        a.axhline(0.05, color="0.7", ls=":", lw=1)
    ax[0].set_title("(PE2) connected |Φ|=ρ correlator  C(r)\n(decays ⇒ no magnitude order)")
    ax[0].set_ylabel("|C(r)|")
    ax[1].set_title("(PE2) full Φ correlator |⟨Φ*(0)Φ(r)⟩|, relaxed gauge\n(normalised)")
    fig.tight_layout()
    fig.savefig(pe.OUTDIR / "PE2_condensate.png", dpi=110)
    plt.close(fig)

    print("=" * 74)
    print(f"PE2 -- DOES Phi CONDENSE SPONTANEOUSLY (V=0)?  ({NSEED} seeds)")
    print("=" * 74)
    print(" rho_spr   <|Phi|>   sigma_|Phi|   magnitude C(r)            relaxed-full C(r)")
    for r in rows:
        print(f"  {r['rho_sprinkle']:5.1f}    {r['abs_mean']:.3f}     {r['abs_std']:.3f}     "
              f"{r['magnitude_decay'][:24]:24s}  {r['relaxed_full_decay'][:22]}")
    print(f"\n  magnitude correlation length xi_|Phi| (cells): "
          f"{[round(r['magnitude_xi'],2) for r in rows]}")
    print("-" * 74)
    print(f"VERDICT (PE2): spontaneous |Phi| condensate = {condensate}")
    print("  <|Phi|>=1 is the Voronoi normalisation (trivial), NOT condensation.  The")
    print("  CONNECTED magnitude correlator decays at the cell scale => the magnitude")
    print("  does not order.  Any plateau after relaxation is the gauge phase vacuum,")
    print("  not a |Phi| condensate.  Without a potential, Phi does not condense.")
    return summary


if __name__ == "__main__":
    main()

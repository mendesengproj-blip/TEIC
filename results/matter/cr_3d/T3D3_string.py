"""T3D3 -- string tension E(d) ~ d in 3D compact U(1): the Polyakov confinement test.

CR_WILSON's W2 relaxed a single classical vortex-antivortex pair and found only a
Coulomb/BKT (log, perimeter) interaction -- no linear string -- in 2D.  The reason
(T3D2): the linear Polyakov string is NOT a property of one classical configuration; it
is the free energy of the disordered MONOPOLE PLASMA.  So T3D3 measures the string
tension the correct way: the Wilson-loop AREA LAW over the gauge ENSEMBLE.

    <W(R,T)> = <cos(sum of enclosed plaquettes)>
    area law   <W> ~ exp(-sigma R T)  -> CONFINEMENT, V(R)=sigma R  (E(d) ~ d)
    perimeter  <W> ~ exp(-p (R+T))    -> Coulomb / free charges

The string tension is extracted by Creutz ratios, which cancel the perimeter and the
constant exactly:

    chi(R,T) = -ln[ W(R,T) W(R-1,T-1) / ( W(R-1,T) W(R,T-1) ) ]  ->  sigma .

We scan lambda_p across the T3D2 confinement<->Coulomb crossover and read off
sigma(lambda_p) and the threshold lambda_c (largest lambda_p with sigma>0).

Anti-circularity: the Wilson loop is the real cosine of a sum of REAL link phases over
the ensemble exp(-lambda_p sum[1-cos W_p]); no QCD input, no complex number, no dilation.
Reuses the T3D2 periodic Metropolis verbatim.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cr3d_core as c                      # noqa: E402
import T3D2_monopoles as mono              # noqa: E402  (metropolis + periodic plaqs)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

SEED = 16180
L = 12
LAMBDAS = [0.5, 0.8, 1.0, 1.5, 2.0, 3.0]
RMAX = 5
N_THERM = 240
N_MEAS = 40
MEAS_EVERY = 4


# --------------------------------------------------------------------------- #
def _box_sums(W, axA, axB, Rmax):
    """All R x T periodic box-sums of a plaquette field W over the (axA,axB) plane,
    R,T = 1..Rmax.  Returns dict[(R,T)] -> array (same shape) of the loop holonomy
    (sum of enclosed plaquettes = Wilson-loop phase, by lattice Stokes)."""
    rows = {1: W.copy()}
    for R in range(2, Rmax + 1):
        rows[R] = rows[R - 1] + np.roll(W, -(R - 1), axis=axA)
    out = {}
    for R in range(1, Rmax + 1):
        col = rows[R].copy()
        out[(R, 1)] = col.copy()
        for T in range(2, Rmax + 1):
            col = col + np.roll(rows[R], -(T - 1), axis=axB)
            out[(R, T)] = col.copy()
    return out


def wilson_loops(px, py, pz, Rmax):
    """Mean Wilson loops <cos(loop)> for R,T=1..Rmax, averaged over base sites and the
    three lattice planes (xy, xz, yz)."""
    Wxy, Wxz, Wyz = mono.plaqs_periodic(px, py, pz)
    acc = {(R, T): 0.0 for R in range(1, Rmax + 1) for T in range(1, Rmax + 1)}
    for W, axA, axB in ((Wxy, 0, 1), (Wxz, 0, 2), (Wyz, 1, 2)):
        boxes = _box_sums(W, axA, axB, Rmax)
        for key, loop in boxes.items():
            acc[key] += float(np.mean(np.cos(loop)))
    return {k: v / 3.0 for k, v in acc.items()}


def creutz(loops, R):
    """Creutz ratio chi(R,R) = -ln[ W(R,R)W(R-1,R-1)/(W(R-1,R)W(R,R-1)) ] -> sigma."""
    a = loops[(R, R)]; b = loops[(R - 1, R - 1)]
    cc = loops[(R - 1, R)]; d = loops[(R, R - 1)]
    if min(a, b, cc, d) <= 0:
        return float("nan")
    return float(-np.log((a * b) / (cc * d)))


def measure(lam, rng):
    shape = (L, L, L)
    px = rng.uniform(-np.pi, np.pi, shape)
    py = rng.uniform(-np.pi, np.pi, shape)
    pz = rng.uniform(-np.pi, np.pi, shape)
    for _ in range(N_THERM):
        mono.metropolis_sweep(px, py, pz, lam, rng)
    acc = {(R, T): [] for R in range(1, RMAX + 1) for T in range(1, RMAX + 1)}
    for _ in range(N_MEAS):
        for _ in range(MEAS_EVERY):
            mono.metropolis_sweep(px, py, pz, lam, rng)
        lp = wilson_loops(px, py, pz, RMAX)
        for k, v in lp.items():
            acc[k].append(v)
    loops = {k: float(np.mean(v)) for k, v in acc.items()}
    chis = {R: creutz(loops, R) for R in range(2, RMAX + 1)}
    # sigma estimate: prefer the mid-size loop chi(3,3) (area-law plateau, robust); in
    # the strongly-confined phase the large loops underflow to noise (W~exp(-sigma R^2)
    # -> 0 -> NaN), so fall back to the largest finite small-R Creutz, which is then a
    # lower bound on the (large) tension.  In the Coulomb phase chi(R,R) DECREASES with
    # R toward 0; we record that trend to discriminate area- from perimeter-law.
    sigma = chis.get(3, float("nan"))
    if not np.isfinite(sigma):
        finite = [chis[R] for R in sorted(chis) if np.isfinite(chis[R])]
        sigma = float(finite[-1]) if finite else float("nan")
    # area-law (confining) if chi does not collapse with R: chi(3,3) >= 0.4*chi(2,2)
    c22, c33 = chis.get(2, float("nan")), chis.get(3, float("nan"))
    plateau = (np.isfinite(c33) and np.isfinite(c22) and c33 >= 0.4 * c22) \
        or (not np.isfinite(c33) and np.isfinite(c22) and c22 > 0.4)
    # static potential V(R) = -ln W(R,Tref)/Tref at a fixed temporal extent
    Tref = RMAX
    Vr = {R: float(-np.log(loops[(R, Tref)]) / Tref) if loops[(R, Tref)] > 0
          else float("nan") for R in range(1, RMAX + 1)}
    # linear-vs-log discrimination on V(R): fit slope (linear) and check curvature
    Rs = np.array([R for R in Vr if np.isfinite(Vr[R])], float)
    Vs = np.array([Vr[R] for R in Vr if np.isfinite(Vr[R])], float)
    slope = float(np.polyfit(Rs, Vs, 1)[0]) if len(Rs) >= 2 else float("nan")
    return {"lambda": lam, "loops": {f"{R}x{T}": loops[(R, T)]
                                     for R in range(1, RMAX + 1)
                                     for T in range(1, RMAX + 1)},
            "creutz": {str(R): chis[R] for R in chis},
            "sigma": sigma, "area_law": bool(plateau),
            "V_of_R": {str(R): Vr[R] for R in Vr}, "V_slope": slope}


def main():
    rng = np.random.default_rng(SEED)
    results = [measure(lam, rng) for lam in LAMBDAS]

    # threshold lambda_c: largest lambda_p that still shows an AREA LAW (non-collapsing
    # Creutz plateau) with sizable tension -- the strong-confinement window edge.
    SIG_THR = 0.1
    confining = [r["lambda"] for r in results
                 if r["area_law"] and np.isfinite(r["sigma"]) and r["sigma"] > SIG_THR]
    lambda_c = max(confining) if confining else None
    linear = lambda_c is not None
    verdict = "SIM" if linear else "NAO"

    payload = {"seed": SEED, "L": L, "Rmax": RMAX, "sigma_threshold": SIG_THR,
               "results": results, "lambda_c": lambda_c,
               "confining_window": (f"lambda_p <= {lambda_c}" if lambda_c else "none"),
               "verdict": verdict}
    c.save_json("T3D3_string", payload)

    if HAVE_MPL:
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
        lams = [r["lambda"] for r in results]
        sigs = [r["sigma"] for r in results]
        ax[0].axhline(0, color="k", lw=0.6)
        ax[0].plot(lams, sigs, "o-")
        ax[0].set_xlabel(r"$\lambda_p$")
        ax[0].set_ylabel(r"string tension $\sigma$ (Creutz)")
        ax[0].set_title("E(d)~d when sigma>0 (confinement)")
        for r in results:
            Rs = [int(k) for k in r["V_of_R"]]
            Vs = [r["V_of_R"][str(R)] for R in Rs]
            ax[1].plot(Rs, Vs, "o-", label=f"λ={r['lambda']}")
        ax[1].set_xlabel("R (separation d)")
        ax[1].set_ylabel("V(R)  [static potential]")
        ax[1].set_title("static potential vs separation")
        ax[1].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(c.OUTDIR / "T3D3_string.png", dpi=130)

    print("=" * 70)
    print("T3D3 -- STRING TENSION (Wilson-loop area law, 3D compact U(1))")
    print("=" * 70)
    print(f"{'lambda_p':>9} {'sigma':>9} {'area':>5}  Creutz chi(R,R) R=2..%d  Vslope"
          % RMAX)
    for r in results:
        chis = " ".join(f"{r['creutz'][str(R)]:+.2f}" for R in range(2, RMAX + 1))
        print(f"{r['lambda']:9.2f} {r['sigma']:9.4f} {str(r['area_law']):>5}  "
              f"[{chis}]  {r['V_slope']:+.3f}")
    print("-" * 70)
    print(f"lambda_c (strong-confinement window edge) = {lambda_c}")
    print(f"VERDICT: linear confinement E(d)~d  {verdict}")
    return payload


if __name__ == "__main__":
    main()

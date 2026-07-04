"""T3D2 -- magnetic monopoles in the 3D compact-U(1) vacuum.

CR_WILSON's diagnosis: 2D has NO monopoles, so a 2pi flux is invisible to the cosine
and there is no linear (Polyakov) confinement.  In 3D, compact U(1) DOES admit magnetic
monopoles as point defects -- and the Polyakov mechanism is exactly their proliferation
into a plasma that Debye-screens the photon and confines electric charge.

This script measures, with NO collision, the vacuum monopole content of the magnetic
sector.  The plaquette term lambda_p*sum[1-cos W_p] is the ONLY part of the action that
sees the gauge field's curl (the theta-Stueckelberg term does not enter W_p), so the
magnetic vacuum is the pure-gauge ensemble exp(-lambda_p*sum[1-cos W_p]).  We sample it
by a vectorised checkerboard Metropolis on a fully periodic L^3 lattice (periodic so the
total magnetic charge is exactly conserved = 0), and measure:

  1. rho_M(lambda_p): fraction of unit cubes carrying |n|>=1 magnetic charge;
  2. the per-cube charge histogram (mostly 0, +-1, rare +-2) and net charge (~0);
  3. C(r) = <q_M(0) q_M(r)>: the monopole-antimonopole correlation (Debye screening:
     anticorrelated at short r -> a neutral plasma -> Polyakov-active).

Magnetic charge n is the DeGrand-Toussaint flux out of a cube (cr3d_core.monopole_*),
summed from the WRAPPED real plaquette; it is an integer by the discrete Bianchi
identity.  No QCD, no complex number, no dilation.

The decisive contrast with 2D: in 2D the analogous object does not exist at all.
Here rho_M>0 at every coupling (3D compact U(1) is permanently a monopole plasma) --
the mechanism CR_WILSON identified as missing is PRESENT.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cr3d_core as c   # noqa: E402

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

SEED = 27182
L = 12                                   # periodic L^3 lattice
LAMBDAS = [0.2, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]
N_THERM = 240
N_MEAS = 30
MEAS_EVERY = 4


# --------------------------------------------------------------------------- #
# Fully-periodic plaquettes and monopole charge (all three axes np.roll)
# --------------------------------------------------------------------------- #
def _r(a, ax, s):
    return np.roll(a, -s, axis=ax)


def plaqs_periodic(px, py, pz):
    Wxy = px + _r(py, 0, 1) - _r(px, 1, 1) - py
    Wxz = px + _r(pz, 0, 1) - _r(px, 2, 1) - pz
    Wyz = py + _r(pz, 1, 1) - _r(py, 2, 1) - pz
    return Wxy, Wxz, Wyz


def monopole_charge_periodic(px, py, pz):
    Wxy, Wxz, Wyz = plaqs_periodic(px, py, pz)
    w = lambda W: (W + np.pi) % (2 * np.pi) - np.pi
    n = ((_r(w(Wxy), 2, 1) - w(Wxy))
         - (_r(w(Wxz), 1, 1) - w(Wxz))
         + (_r(w(Wyz), 0, 1) - w(Wyz))) / (2 * np.pi)
    return n


# --------------------------------------------------------------------------- #
# Vectorised checkerboard Metropolis on S = lambda * sum[1 - cos W]
# --------------------------------------------------------------------------- #
def _parity_mask(shape, color):
    I, J, K = np.indices(shape)
    return ((I + J + K) % 2) == color


def metropolis_sweep(px, py, pz, lam, rng, step=1.0):
    """One sweep: for each direction and each parity colour, propose phi += delta on a
    non-interacting sublattice and accept by Metropolis.  Parallel same-colour links of
    one direction never share a plaquette, so the vectorised update is exact."""
    shape = px.shape
    for arr, dirn in ((px, 0), (py, 1), (pz, 2)):
        Wxy, Wxz, Wyz = plaqs_periodic(px, py, pz)
        for color in (0, 1):
            mask = _parity_mask(shape, color)
            delta = step * rng.uniform(-np.pi, np.pi, shape)
            # plaquettes a given link sits in, and the sign with which phi enters them
            if dirn == 0:      # x-link: +Wxy[here], -Wxy[j-1], +Wxz[here], -Wxz[k-1]
                terms = [(Wxy, +1, None), (_r(Wxy, 1, -1), -1, (1, +1)),
                         (Wxz, +1, None), (_r(Wxz, 2, -1), -1, (2, +1))]
            elif dirn == 1:    # y-link: -Wxy[here], +Wxy[i-1], +Wyz[here], -Wyz[k-1]
                terms = [(Wxy, -1, None), (_r(Wxy, 0, -1), +1, (0, +1)),
                         (Wyz, +1, None), (_r(Wyz, 2, -1), -1, (2, +1))]
            else:              # z-link: -Wxz[here], +Wxz[i-1], -Wyz[here], +Wyz[j-1]
                terms = [(Wxz, -1, None), (_r(Wxz, 0, -1), +1, (0, +1)),
                         (Wyz, -1, None), (_r(Wyz, 1, -1), +1, (1, +1))]
            dS = np.zeros(shape)
            for W, sgn, _shift in terms:
                dS += lam * (np.cos(W) - np.cos(W + sgn * delta))
            accept = mask & (rng.uniform(0, 1, shape) < np.exp(-dS))
            arr[accept] += delta[accept]
            # refresh the plaquettes touched by this colour for the next colour/dir
            Wxy, Wxz, Wyz = plaqs_periodic(px, py, pz)
    return px, py, pz


def sample(lam, rng):
    shape = (L, L, L)
    px = rng.uniform(-np.pi, np.pi, shape)
    py = rng.uniform(-np.pi, np.pi, shape)
    pz = rng.uniform(-np.pi, np.pi, shape)
    for _ in range(N_THERM):
        metropolis_sweep(px, py, pz, lam, rng)
    rhos, nets, hist, plaqavg = [], [], np.zeros(7), []
    corr_acc = None
    for m in range(N_MEAS):
        for _ in range(MEAS_EVERY):
            metropolis_sweep(px, py, pz, lam, rng)
        n = np.rint(monopole_charge_periodic(px, py, pz)).astype(int)
        rhos.append(float(np.mean(np.abs(n) >= 1)))
        nets.append(int(np.sum(n)))
        for q in range(-3, 4):
            hist[q + 3] += int(np.sum(n == q))
        Wxy, Wxz, Wyz = plaqs_periodic(px, py, pz)
        plaqavg.append(float(np.mean(np.cos(np.concatenate(
            [Wxy.ravel(), Wxz.ravel(), Wyz.ravel()])))))
        cr = charge_correlation(n)
        corr_acc = cr if corr_acc is None else corr_acc + cr
    return {"lambda": lam,
            "rho_M": float(np.mean(rhos)), "rho_M_std": float(np.std(rhos)),
            "net_charge_mean": float(np.mean(nets)),
            "plaq_cos_mean": float(np.mean(plaqavg)),
            "charge_hist": (hist / N_MEAS).tolist(),
            "correlation": (corr_acc / N_MEAS).tolist()}


def charge_correlation(n, rmax=6):
    """Radial monopole charge correlation C(r) = <q(0) q(r)> along the axes, averaged
    over the lattice and the three axes (periodic)."""
    out = np.zeros(rmax + 1)
    nf = n.astype(float)
    norm = nf.size
    for r in range(rmax + 1):
        acc = 0.0
        for ax in range(3):
            acc += float(np.sum(nf * np.roll(nf, -r, axis=ax)))
        out[r] = acc / (3 * norm)
    return out


def main():
    rng = np.random.default_rng(SEED)
    results = [sample(lam, rng) for lam in LAMBDAS]

    # Monopoles EXIST at every coupling (rho_M>0 always -- the dilute monopole gas of
    # 3D compact U(1), impossible in 2D).  They PROLIFERATE into a dense screening
    # plasma at strong coupling (small lambda_p); the confinement<->Coulomb crossover
    # is where rho_M falls through ~0.05.
    rho_min = min(r["rho_M"] for r in results)
    rho_max = max(r["rho_M"] for r in results)
    exists = rho_max > 0.05
    proliferates = rho_max > 0.10          # dense plasma in the strong-coupling window
    # screening: C(r) goes negative (anticorrelated) at short range for the densest pt
    dense = max(results, key=lambda r: r["rho_M"])
    cr = np.array(dense["correlation"])
    screened = bool(cr[0] > 0 and np.min(cr[1:3]) < 0)
    # crossover lambda_x: largest lambda with rho_M >= 0.05 (confining window edge)
    confining = [r["lambda"] for r in results if r["rho_M"] >= 0.05]
    lambda_x = max(confining) if confining else None

    verdict = ("SIM" if exists and proliferates and screened else
               ("PARCIAL" if exists else "NAO"))
    payload = {"seed": SEED, "L": L, "n_therm": N_THERM, "n_meas": N_MEAS,
               "results": results,
               "rho_M_range": [rho_min, rho_max],
               "exists": exists, "proliferates": proliferates,
               "screened": screened, "lambda_crossover": lambda_x,
               "confining_window": f"lambda_p <= {lambda_x}" if lambda_x else "none",
               "verdict": verdict}
    c.save_json("T3D2_monopoles", payload)

    if HAVE_MPL:
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
        lams = [r["lambda"] for r in results]
        rhos = [r["rho_M"] for r in results]
        errs = [r["rho_M_std"] for r in results]
        ax[0].errorbar(lams, rhos, yerr=errs, marker="o", capsize=3)
        ax[0].set_xlabel(r"$\lambda_p$ (= inverse coupling $\beta$)")
        ax[0].set_ylabel(r"monopole density $\rho_M$ (charged cubes / cube)")
        ax[0].set_title("3D compact U(1): permanent monopole plasma")
        ax[0].set_ylim(0, max(rhos) * 1.2)
        rr = np.arange(len(cr))
        ax[1].axhline(0, color="k", lw=0.6)
        ax[1].plot(rr, cr, "o-")
        ax[1].set_xlabel("r (lattice cubes)")
        ax[1].set_ylabel(r"$C(r)=\langle q_M(0)q_M(r)\rangle$")
        ax[1].set_title(f"charge correlation (lambda_p={dense['lambda']})")
        fig.tight_layout()
        fig.savefig(c.OUTDIR / "T3D2_monopoles.png", dpi=130)

    print("=" * 70)
    print("T3D2 -- MAGNETIC MONOPOLES IN THE 3D COMPACT-U(1) VACUUM")
    print("=" * 70)
    print(f"{'lambda_p':>9} {'rho_M':>8} {'+-std':>7} {'net Q':>7} {'<cosW>':>8}")
    for r in results:
        print(f"{r['lambda']:9.2f} {r['rho_M']:8.3f} {r['rho_M_std']:7.3f} "
              f"{r['net_charge_mean']:7.2f} {r['plaq_cos_mean']:8.3f}")
    print(f"rho_M range over couplings: [{rho_min:.3f}, {rho_max:.3f}]")
    print(f"C(r) (densest): {np.array(dense['correlation']).round(3).tolist()}")
    print("-" * 70)
    print(f"exists={exists}  proliferates(dense plasma)={proliferates}  "
          f"screened={screened}  confining window: lambda_p <= {lambda_x}")
    print(f"VERDICT: monopoles {verdict}")
    return payload


if __name__ == "__main__":
    main()

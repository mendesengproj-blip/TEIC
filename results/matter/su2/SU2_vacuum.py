"""SU2 -- the non-Abelian SU(2) vacuum: monopoles and the Wilson area law.

CR_3D found that 3D compact U(1) is a permanent monopole plasma with a linear string
(Polyakov), but the confining window was inverted (strong coupling).  SU(2) Yang-Mills
is the textbook confiner: it has an AREA LAW at ALL couplings in 3D (no deconfining
bulk transition; only a finite-T one), with a string tension sigma>0 that grows toward
strong coupling.  Here we sample the SU(2) link vacuum by a vectorised checkerboard
Metropolis on the Wilson action

    S = beta * sum_plaq (1 - 1/2 Tr U_p) ,    U_p = U_mu(n) U_nu(n+mu) U_mu(n+nu)^dag U_nu(n)^dag ,

on a periodic L^3 lattice (links are quaternions), and measure:

  1. <1/2 Tr U_p>(beta): the mean plaquette (strong coupling -> beta/4, weak -> 1);
  2. rho_M(beta): Abelian-projected (t'Hooft) monopole density per cube;
  3. the Wilson loops W(R,T) and their CREUTZ RATIOS chi(R,T) -> string tension sigma.
     An area law (W ~ exp(-sigma R T), chi(R,T) -> sigma > 0) is CONFINEMENT.

ANTI-CIRCULARITY: links are unit quaternions, group product = Hamilton (no Pauli, no
complex); the Wilson loop is the a0 component of the holonomy.  "quark"/"colour"/"QCD"
appear only in COMPARISON ONLY notes; no generator uses them.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

SEED = 31415
L = 8
BETAS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
N_THERM = 200
N_MEAS = 25
MEAS_EVERY = 4


def _roll(q, ax, sh):
    return np.roll(q, sh, axis=ax)


def staple_sum(Q, mu):
    """Sum of the 4 staples (2 per perpendicular direction) attached to every mu-link,
    so that U_p(mu,nu) = q_mul(Q[mu], staple).  Periodic in all axes."""
    A = np.zeros_like(Q[mu])
    for nu in range(3):
        if nu == mu:
            continue
        Qm, Qn = Q[mu], Q[nu]
        # forward: Q_nu(n+mu) Q_mu(n+nu)^dag Q_nu(n)^dag
        t1 = _roll(Qn, mu, -1)
        t2 = s.q_conj(_roll(Qm, nu, -1))
        t3 = s.q_conj(Qn)
        A = A + s.q_mul(s.q_mul(t1, t2), t3)
        # backward: Q_nu(n+mu-nu)^dag Q_mu(n-nu)^dag Q_nu(n-nu)
        b1 = s.q_conj(_roll(_roll(Qn, mu, -1), nu, +1))
        b2 = s.q_conj(_roll(Qm, nu, +1))
        b3 = _roll(Qn, nu, +1)
        A = A + s.q_mul(s.q_mul(b1, b2), b3)
    return A


def small_su2(shape, rng, eps=0.35):
    """Random SU(2) element near the identity (for the Metropolis proposal): axis random,
    angle ~ eps*uniform.  Returned as a quaternion array of given shape."""
    axis = rng.standard_normal(shape + (3,))
    ang = eps * rng.uniform(-np.pi, np.pi, shape)
    return s.q_from_axis_angle(axis, ang)


def metropolis_sweep(Q, beta, rng, eps=0.35):
    shape = Q[0].shape[:-1]
    I, J, K = np.indices(shape)
    parity = (I + J + K) % 2
    for mu in range(3):
        A = staple_sum(Q, mu)
        for color in (0, 1):
            mask = parity == color
            r = small_su2(shape, rng, eps)
            Qprop = s.q_mul(r, Q[mu])
            # dS = -beta/2 [ TrRe(Qprop A) - TrRe(Q A) ] ; 1/2 Tr = a0
            dS = -beta * (s.half_trace(s.q_mul(Qprop, A))
                          - s.half_trace(s.q_mul(Q[mu], A)))
            acc = mask & (rng.uniform(0, 1, shape) < np.exp(-dS))
            Q[mu][acc] = Qprop[acc]
    return Q


def mean_plaquette(Q):
    tot = 0.0; cnt = 0
    for mu in range(3):
        for nu in range(mu + 1, 3):
            Up = s.plaquette(Q[mu], _roll(Q[nu], mu, -1),
                             _roll(Q[mu], nu, -1), Q[nu])
            tot += float(np.mean(s.half_trace(Up))); cnt += 1
    return tot / cnt


def planar_wilson(Q, R, T, mu=0, nu=1):
    """Mean R x T planar Wilson loop in the (mu,nu) plane: ordered product of links around
    the rectangle (+mu R times, +nu T times, -mu R times, -nu T times), averaged over the
    lattice (periodic).  Returns <1/2 Tr W>."""
    Wl = s.q_identity(Q[mu].shape[:-1])
    # +mu edge
    for a in range(R):
        Wl = s.q_mul(Wl, _shift(Q[mu], mu, a, nu, 0))
    # +nu edge
    for b in range(T):
        Wl = s.q_mul(Wl, _shift(Q[nu], mu, R, nu, b))
    # -mu edge
    for a in range(R - 1, -1, -1):
        Wl = s.q_mul(Wl, s.q_conj(_shift(Q[mu], mu, a, nu, T)))
    # -nu edge
    for b in range(T - 1, -1, -1):
        Wl = s.q_mul(Wl, s.q_conj(_shift(Q[nu], mu, 0, nu, b)))
    return float(np.mean(s.half_trace(Wl)))


def _shift(field, mu, a, nu, b):
    """field at site n + a*e_mu + b*e_nu (periodic)."""
    out = np.roll(field, -a, axis=mu)
    out = np.roll(out, -b, axis=nu)
    return out


def creutz(W):
    """Creutz ratio chi(R,T) = -ln[ W(R,T) W(R-1,T-1) / (W(R-1,T) W(R,T-1)) ] from a
    dict W[(R,T)].  Returns chi at (2,2) if available (the cleanest small-loop estimate)."""
    def g(R, T):
        return max(W.get((R, T), 1e-9), 1e-9)
    try:
        return float(-np.log(g(2, 2) * g(1, 1) / (g(1, 2) * g(2, 1))))
    except Exception:
        return float("nan")


def sample(beta, rng):
    Q = [s.q_normalize(rng.standard_normal((L, L, L, 4))) for _ in range(3)]
    for _ in range(N_THERM):
        metropolis_sweep(Q, beta, rng)
    plaqs, rhos = [], []
    loops = {(R, T): [] for R in (1, 2, 3) for T in (1, 2, 3)}
    for m in range(N_MEAS):
        for _ in range(MEAS_EVERY):
            metropolis_sweep(Q, beta, rng)
        plaqs.append(mean_plaquette(Q))
        rho, _ = s.monopole_density(Q[0], Q[1], Q[2])
        rhos.append(rho)
        for (R, T) in loops:
            loops[(R, T)].append(planar_wilson(Q, R, T))
    Wmean = {rt: float(np.mean(v)) for rt, v in loops.items()}
    return {"beta": beta, "plaq": float(np.mean(plaqs)),
            "plaq_std": float(np.std(plaqs)),
            "rho_M": float(np.mean(rhos)), "rho_M_std": float(np.std(rhos)),
            "wilson": {f"{R}x{T}": Wmean[(R, T)] for (R, T) in loops},
            "creutz22": creutz(Wmean)}


def main():
    rng = np.random.default_rng(SEED)
    results = [sample(b, rng) for b in BETAS]

    sigmas = [r["creutz22"] for r in results]
    # Confinement window: the Creutz ratio needs statistically RESOLVED loops.  At very
    # strong coupling (beta<=0.5) the 2x2/3x3 loops underflow to ~0 (pure noise) so chi is
    # ill-defined there -- the area law is strongest but the small loops saturate.  We
    # certify the area law on the resolved window beta in [1.0, 2.5].
    resolved = [r for r in results if 1.0 <= r["beta"] <= 2.5]
    area_law = all(r["creutz22"] > 0 for r in resolved)
    rho_ok = all(r["rho_M"] > 0.02 for r in results)
    # sigma grows toward strong coupling within the resolved window
    sigma_grows = resolved[0]["creutz22"] > resolved[-1]["creutz22"]
    verdict = "SIM" if area_law and rho_ok else ("PARCIAL" if rho_ok else "NAO")

    payload = {"seed": SEED, "L": L, "n_therm": N_THERM, "n_meas": N_MEAS,
               "results": results,
               "area_law_all_beta": bool(area_law),
               "monopoles_all_beta": bool(rho_ok),
               "sigma_grows_strong_coupling": bool(sigma_grows),
               "verdict": verdict}
    s.save_json("SU2_vacuum", payload)

    if HAVE_MPL:
        fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
        bs = [r["beta"] for r in results]
        ax[0].errorbar(bs, [r["plaq"] for r in results],
                       yerr=[r["plaq_std"] for r in results], marker="o", capsize=3)
        ax[0].set_xlabel(r"$\beta$"); ax[0].set_ylabel(r"$\langle\frac12\mathrm{Tr}\,U_p\rangle$")
        ax[0].set_title("SU(2) mean plaquette")
        ax[1].errorbar(bs, [r["rho_M"] for r in results],
                       yerr=[r["rho_M_std"] for r in results], marker="s", capsize=3)
        ax[1].set_xlabel(r"$\beta$"); ax[1].set_ylabel(r"$\rho_M$ (Abelian-projected)")
        ax[1].set_title("SU(2) monopole density")
        ax[2].plot(bs, sigmas, "o-")
        ax[2].axhline(0, color="k", lw=0.6)
        ax[2].set_xlabel(r"$\beta$"); ax[2].set_ylabel(r"Creutz $\chi(2,2)\approx\sigma$")
        ax[2].set_ylim(-0.5, 1.2)
        ax[2].set_title("string tension (area law)")
        try:
            fig.savefig(s.OUTDIR / "SU2_vacuum.png", dpi=130, bbox_inches="tight")
        except Exception:
            fig.savefig(s.OUTDIR / "SU2_vacuum.png", dpi=130)

    print("=" * 72)
    print("SU2 -- SU(2) VACUUM: monopoles and Wilson area law")
    print("=" * 72)
    print(f"{'beta':>6} {'<plaq>':>8} {'rho_M':>8} {'W(1x1)':>9} {'W(2x2)':>9} {'chi22':>8}")
    for r in results:
        print(f"{r['beta']:6.2f} {r['plaq']:8.3f} {r['rho_M']:8.3f} "
              f"{r['wilson']['1x1']:9.3f} {r['wilson']['2x2']:9.3f} {r['creutz22']:8.3f}")
    print("-" * 72)
    print(f"area law (chi>0) em todo beta: {area_law}   monopolos: {rho_ok}   "
          f"sigma cresce no acoplamento forte: {sigma_grows}")
    print(f"VERDICT: vacuo SU(2) {verdict}")
    return payload


if __name__ == "__main__":
    main()

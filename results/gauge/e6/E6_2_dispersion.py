"""E6_2_dispersion.py -- gate H2: does the gauge field disperse as omega=ck?

Pre-registered in E6_BD_GAUGE.md (gate H2). The non-compact Maxwell action
S=(1/2) sum_P F_P^2 = (1/2) theta^T M theta (M=B^T B) is positive semi-definite, and
for an ON-SHELL electromagnetic plane wave F_{mu nu}F^{mu nu}=2(B^2-E^2)=0 (E=B for
radiation). So IF the causal diamonds sample bivector orientations isotropically (as
a Lorentz-invariant Poisson sprinkling should), the action symbol
lambda(k,omega)=<theta,M theta>/<theta,theta> on a transverse plane-wave 1-form
should be MINIMISED (-> 0) along the photon dispersion omega=|k|. We measure the
minimum locus omega*(k) and fit omega=ck.

Plane-wave 1-form on link l=(a,b): theta_l = (eps . dx_l) cos(k.xmid_space - omega*tmid),
eps a spatial polarisation transverse to k (eps.k=0), dx_l the 4-displacement (the
natural 1-form line integral A_mu dx^mu, no metric inserted). c is NOT inserted; it
is the fitted slope of omega*(k). This is the FLAT-SPACE validation of H2 -- it must
reproduce free Maxwell (omega=ck) or the construction does not represent a photon.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E5 = HERE.parent / "e5"
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
sys.path.insert(0, str(E5)); sys.path.insert(0, str(ORI))
from e5_core import causal_diamond_plaquettes   # noqa: E402
from orientation_core import causal_link_graph   # noqa: E402
ROOT = HERE.parents[2]; sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box             # noqa: E402


def build_M(g, pl, ps):
    L = g.edges.shape[0]; P = pl.shape[0]
    B = np.zeros((P, L))
    for p in range(P):
        for j in range(4):
            B[p, pl[p, j]] += ps[p, j]
    return B.T @ B


def transverse_pols(kvec):
    """Two spatial unit vectors orthogonal to the spatial kvec."""
    k = kvec / (np.linalg.norm(kvec) + 1e-12)
    a = np.array([1.0, 0, 0]) if abs(k[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = a - k * (a @ k); e1 /= np.linalg.norm(e1) + 1e-12
    e2 = np.cross(k, e1)
    return e1, e2


def plane_wave_theta(g, pts, kvec, omega, eps_spatial):
    """theta_l = (eps . dx_space) cos(k.xmid_space - omega tmid). eps is spatial."""
    edges = g.edges
    a = edges[:, 0]; b = edges[:, 1]
    dx = pts[b, 1:] - pts[a, 1:]               # spatial 3-displacement
    xmid = 0.5 * (pts[a, 1:] + pts[b, 1:])
    tmid = 0.5 * (pts[a, 0] + pts[b, 0])
    amp = dx @ eps_spatial                      # eps . dx (spatial 1-form pairing)
    phase = xmid @ kvec - omega * tmid
    return amp * np.cos(phase)


def symbol(M, theta):
    d = float(theta @ theta)
    return float(theta @ (M @ theta) / d) if d > 0 else np.nan


def main():
    t0 = time.time()
    rho, L_box = 0.5, 4.6
    rng = np.random.default_rng(1)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    Lk, pl, ps = causal_diamond_plaquettes(g, max_per_pair=3, seed=1)
    M = build_M(g, pl, ps)
    N = g.n; L = g.edges.shape[0]

    # k magnitudes (box fundamental upward) and directions
    kmin = 2 * np.pi / L_box
    kmags = np.linspace(kmin, 3.0 * kmin, 6)
    dirs = [np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]),
            np.array([1, 1, 0]) / np.sqrt(2), np.array([1, 1, 1]) / np.sqrt(3)]
    omegas = np.linspace(0.0, 3.5 * kmags[-1], 60)

    ostar = []
    for km in kmags:
        # average the symbol over directions and the 2 transverse polarisations
        o_dir = []
        for d in dirs:
            kvec = km * d
            e1, e2 = transverse_pols(d)
            lam = np.zeros(len(omegas))
            for iw, w in enumerate(omegas):
                s1 = symbol(M, plane_wave_theta(g, pts, kvec, w, e1))
                s2 = symbol(M, plane_wave_theta(g, pts, kvec, w, e2))
                lam[iw] = 0.5 * (s1 + s2)
            # on-shell = omega that MINIMISES the symbol (F^2 -> 0 for radiation)
            o_dir.append(omegas[int(np.argmin(lam))])
        ostar.append(np.mean(o_dir))
    ostar = np.array(ostar)

    # fit omega* = c k through the origin
    c_fit = float(np.sum(kmags * ostar) / np.sum(kmags ** 2))
    resid = ostar - c_fit * kmags
    rel_dev = float(np.sqrt(np.mean(resid ** 2)) / (np.sqrt(np.mean(ostar ** 2)) + 1e-12))
    # also: is the minimum at omega~0 (no propagation) instead of omega~k?
    near_zero = bool(np.mean(ostar) < 0.3 * np.mean(kmags))

    if near_zero:
        verdict = (f"H2 FAIL (no propagation): the symbol minimum sits near omega=0, "
                   f"not on a light cone -- the naive Euclidean action does not yield a "
                   f"propagating photon. The Lorentzian electric/magnetic (BD-type) "
                   f"construction is required.")
        tag = "H2_FAIL_NOPROP"
    elif rel_dev < 0.20 and 0.7 < c_fit < 1.4:
        verdict = (f"H2 PASS (photon dispersion): omega*(k) = ck with c={c_fit:.2f} "
                   f"(dev {100*rel_dev:.0f}%), the light-cone speed recovered WITHOUT "
                   f"insertion. The physical modes disperse relativistically -- a "
                   f"photon. Next: polarisation count (2 transverse) + Coulomb (H3).")
        tag = "H2_PHOTON"
    else:
        verdict = (f"H2 INCONCLUSIVE: omega*(k) rises (c={c_fit:.2f}) but not a clean "
                   f"ck (dev {100*rel_dev:.0f}%); nonlocality (large diamonds) likely "
                   f"distorts the dispersion -- a BD-smeared / refined complex is "
                   f"needed. Not a clean photon, not a clean failure.")
        tag = "H2_INCONCLUSIVE"

    out = {"config": {"rho": rho, "L_box": L_box}, "N": N, "L": L,
           "kmags": kmags.tolist(), "omega_star": ostar.tolist(),
           "c_fit": c_fit, "rel_deviation": rel_dev, "min_near_zero": near_zero,
           "verdict": verdict, "verdict_tag": tag, "runtime_s": time.time() - t0}
    (HERE / "E6_2_dispersion.json").write_text(json.dumps(out, indent=2))
    print(f"N={N} L={L}")
    for km, os_ in zip(kmags, ostar):
        print(f"  k={km:.3f}  omega*={os_:.3f}  (omega*/k={os_/km:.2f})")
    print(f"fit: omega = {c_fit:.3f} k  (rel dev {100*rel_dev:.0f}%)")
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.0f}s -> E6_2_dispersion.json")


if __name__ == "__main__":
    main()

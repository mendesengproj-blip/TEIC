"""fm3_core.py -- primordial-texture engine for FM3_PRIMORDIAL_TEXTURE.

DATA GENERATOR for the FM3 campaign (the "relic orientation texture" hypothesis,
TEIC_DEV_VISION.md sec.6).  Contains NO cosmology interpretation: "dark matter" /
"resolve S8" live only in the synthesis (COMPARISON ONLY).  Tests whether the
early-universe ORDERING transition of the orientation ferromagnet (E1) leaves a
relic defect/texture network (Kibble-Zurek), and characterises it (defect density
vs quench rate, coarsening, effective equation of state).

Reuses (additively, no prior code modified):
  * fm2_core.O3Lattice  -- periodic O(3) Heisenberg Metropolis (E1 vacuum engine);
  * e3_core             -- cubic solid-angle topological charge field (defect count),
                           gradient energy, and trilinear dilation (for w_eff).

The quench: start DISORDERED (random n, J<J_c), ramp J(t) up through J_c to the
ordered phase over tau_Q sweeps.  Causally disconnected regions order in different
directions -> domains -> defects at the boundaries (Kibble mechanism).  Slower
quench (larger tau_Q) -> larger domains -> fewer defects (Zurek scaling
xi_dom ~ tau_Q^sigma).  Defects are counted AFTER a fixed short cooling (standard
lattice protocol: cooling removes thermal UV wrinkles whose spurious fractional
solid angle would otherwise swamp the genuine integer defects).

Anti-circularity: J_c, the defect density and the equation of state are MEASURED on
the lattice; no sigma8/Planck/Turok value is inserted.  The O(3) energy and the
solid-angle charge follow orientation_core / e3_core conventions.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                       # .../TEIC
sys.path.insert(0, str(ROOT / "results" / "cmb" / "fm2"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation" / "e3"))

import fm2_core as fm2   # noqa: E402  (periodic O(3) lattice MC)
import e3_core as e3     # noqa: E402  (cubic solid-angle charge, gradient E, dilation)

JC_O3 = 0.693            # E1 / literature 3D O(3) ordering coupling (COMPARISON)
COOL_STEPS = 30          # fixed cooling before counting defects (remove UV wrinkles)


# ====================================================================== #
# Quench through the ordering transition (Kibble-Zurek)
# ====================================================================== #
def quench(L, tau_Q, J_lo=0.30, J_hi=1.20, seed=0, hold=0):
    """Cool the O(3) ferromagnet from disordered (J_lo) to ordered (J_hi) over
    tau_Q sweeps, starting from a RANDOM (hot) configuration.  Returns the final
    (L,L,L,3) field.  tau_Q is the quench timescale: large tau_Q = slow quench."""
    lat = fm2.O3Lattice(L, J_lo, h=0.0, seed=seed)
    # disordered (hot) start
    rng = np.random.default_rng(seed + 12345)
    v = rng.standard_normal((L, L, L, 3))
    lat.n = v / np.linalg.norm(v, axis=-1, keepdims=True)
    n_steps = max(int(tau_Q), 1)
    for t in range(n_steps):
        frac = (t + 1) / n_steps
        lat.J = J_lo + (J_hi - J_lo) * frac           # linear ramp through J_c
        lat.sweep()
    lat.J = J_hi
    for _ in range(hold):
        lat.sweep()
    return lat.n


# ====================================================================== #
# Defect counting (cooled solid-angle charge)
# ====================================================================== #
def cool(n, steps=COOL_STEPS, dt=0.1):
    """Zero-T gradient-flow cooling (remove thermal UV wrinkles; keep integer
    winding).  Returns the cooled field."""
    if steps <= 0:
        return n
    _, nc = e3.relax_gradient(n, n_steps=steps, dt=dt, record_every=steps)
    return nc


def defect_count(n, cool_steps=COOL_STEPS, thr=0.5):
    """Number of topological defects = cubes whose cooled solid-angle charge has
    |q|>thr.  Returns (n_defects, density = n_def/V, cooled gradient energy)."""
    nc = cool(n, cool_steps)
    q = e3.charge_field(nc)
    ndef = int((np.abs(q) > thr).sum())
    V = n.shape[0] ** 3
    return ndef, ndef / V, e3.gradient_energy(nc)


def coherence_length(density):
    """Mean defect separation xi_dom ~ density^{-1/3} (3D)."""
    return float(density ** (-1.0 / 3.0)) if density > 0 else float("inf")


# ====================================================================== #
# Coarsening: defect density vs continued (flat-space) evolution time
# ====================================================================== #
def coarsening(n, times, dt=0.1):
    """Continued zero-T relaxation AFTER the quench: defects annihilate (the
    network coarsens).  Returns (times, n_def(t)) -- the flat-space, ACAUSAL fate
    (defects disappear).  Contrast with the E3b causal-cone result, where a frozen
    causal boundary PRESERVES the winding (super-horizon freezing)."""
    ndefs = []
    cur = n.copy()
    prev = 0
    for t in times:
        if t > prev:
            _, cur = e3.relax_gradient(cur, n_steps=t - prev, dt=dt, record_every=t - prev)
            prev = t
        q = e3.charge_field(cur)
        ndefs.append(int((np.abs(q) > 0.5).sum()))
    return np.asarray(times), np.asarray(ndefs)


# ====================================================================== #
# Effective equation of state: gradient-energy scaling under expansion
# ====================================================================== #
def w_effective(n, lambdas=None, center=None):
    """Effective equation of state of the frozen texture from how its gradient
    energy density scales under an expansion (dilation) of the pattern.

    A field FROZEN in comoving coordinates and stretched by a factor lambda has
    gradient energy density rho ~ |grad n|^2 ~ lambda^{-2} * (comoving grad)^2; for
    a power law rho(lambda) ~ lambda^{-p}, the FRW scaling rho ~ a^{-3(1+w)} with
    a~lambda gives  w = p/3 - 1.   p=2 (frozen texture) -> w=-1/3 (NOT cold);
    p=3 -> w=0 (cold, like CDM); p=0 (scaling, const) -> w=-1.

    Returns (lambdas, rho_grad(lambda), p, w_eff).  rho = E_grad / volume(lambda)."""
    L = n.shape[0]
    if lambdas is None:
        lambdas = np.array([1.0, 1.3, 1.7, 2.2, 3.0])
    rho = []
    for lam in lambdas:
        nl = e3.dilate(n, lam, center)               # stretch the pattern
        E = e3.gradient_energy(nl)
        rho.append(E / (L ** 3))                      # energy density (fixed comoving box)
    rho = np.asarray(rho)
    # fit rho ~ lambda^{-p}
    good = rho > 0
    p = -np.polyfit(np.log(lambdas[good]), np.log(rho[good]), 1)[0]
    w = p / 3.0 - 1.0
    return np.asarray(lambdas), rho, float(p), float(w)


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("fm3_core self-test")
    # quench: faster quench (small tau_Q) leaves MORE defects than slow quench
    for tau in (5, 40):
        nd = []
        for sd in range(3):
            n = quench(16, tau_Q=tau, seed=sd)
            ndef, dens, _ = defect_count(n)
            nd.append(ndef)
        print(f"  tau_Q={tau:3d}: <n_def>={np.mean(nd):.1f}  (fast quench -> more defects)")
    # equation of state of a single hedgehog texture
    nh = e3.hedgehog(16, +1)
    lam, rho, p, w = w_effective(nh)
    print(f"  hedgehog texture: rho~lambda^-{p:.2f}  =>  w_eff={w:+.2f}  "
          f"(frozen texture p~2 => w~-1/3)")
    print("self-test OK")

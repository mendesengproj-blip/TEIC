"""SU1 -- the SU(2) engine gate: four mandatory checks before any physics.

The whole campaign rests on the quaternion SU(2) engine in su2_core.  Before measuring
a single vacuum or soliton we certify, with no free parameters, that the engine is a
faithful, gauge-invariant, energy-conserving non-Abelian generalisation of CR_3D:

  1. U(1) LIMIT.  Restricting every link/field to the sigma_3 subgroup exp(i phi s3)
     must reproduce the Abelian engine EXACTLY:
       (a) group product = angle addition  (q_mul(u1,u1) <-> phi1+phi2);
       (b) 1/2 Tr U = cos(phi);
       (c) the SU(2) Wilson action on sigma_3 links == cr3d_core's U(1) Wilson energy;
       (d) the SU(2) Abelian-projected monopole charge == cr3d_core.monopole_charge.
  2. GROUP IDENTITY.  U U^{-1} = 1, associativity, |U V| = 1 (closure) to ~1e-15.
  3. GAUGE INVARIANCE.  S_Wilson[U] = S_Wilson[g U g^{-1}] for a random site gauge
     field g in SU(2): the action is invariant under local gauge transforms.
  4. ENERGY CONSERVATION.  Free projected-Verlet propagation of a smooth chiral field
     conserves E_kin+E2+E4 (drift < 1e-3).

If any check fails the campaign stops.  ANTI-CIRCULARITY: quaternions only (4 reals),
no Pauli matrices, no complex literal, no SR/GR dilation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_3d"))
import cr3d_core as c3  # noqa: E402

SEED = 20242


def check_u1_limit(rng):
    """Gate 1: the sigma_3 subgroup reproduces CR_3D exactly."""
    # (a),(b) group product / trace already at machine precision; re-measure here.
    a = rng.uniform(-3, 3, 50); b = rng.uniform(-3, 3, 50)
    prod = s.q_mul(s.u1_embed(a), s.u1_embed(b))
    wrap = lambda t: (t + np.pi) % s.TWO_PI - np.pi
    err_add = float(np.max(np.abs(wrap(s.u1_angle(prod)) - wrap(a + b))))
    err_tr = float(np.max(np.abs(s.half_trace(s.u1_embed(a)) - np.cos(a))))

    # (c) SU(2) Wilson action on sigma_3 links == U(1) lam*sum(1-cos W).
    x, y, z, dx = c3.make_grid(Lx=20.0, Nx=33, Ny=8, Nz=8)
    shape = (len(x), len(y), len(z))
    phix = rng.uniform(-1, 1, shape); phix[0] = phix[-1] = 0.0
    phiy = rng.uniform(-1, 1, shape)
    phiz = rng.uniform(-1, 1, shape)
    qx, qy, qz = s.u1_embed(phix), s.u1_embed(phiy), s.u1_embed(phiz)
    lam = 0.7
    S_su2 = s.wilson_action(qx, qy, qz, lam, interior_x=True)
    # U(1) reference: lam * sum (1 - cos W_p) over the three planes, interior x.
    Wxy, Wxz, Wyz = c3.all_plaquettes(phix, phiy, phiz)
    S_u1 = lam * (float(np.sum(1.0 - np.cos(Wxy[:-1])))
                  + float(np.sum(1.0 - np.cos(Wxz[:-1])))
                  + float(np.sum(1.0 - np.cos(Wyz))))
    err_action = abs(S_su2 - S_u1) / max(abs(S_u1), 1e-12)

    # (d) Abelian-projected monopole charge == cr3d_core.monopole_charge.
    n_su2 = s.su2_monopole_charge(qx, qy, qz)
    n_u1 = c3.monopole_charge(phix, phiy, phiz)
    err_mono = float(np.max(np.abs(n_su2 - n_u1)))

    ok = (err_add < 1e-12 and err_tr < 1e-12 and err_action < 1e-10
          and err_mono < 1e-10)
    return {"err_angle_addition": err_add, "err_half_trace": err_tr,
            "err_wilson_action": err_action, "err_monopole_charge": err_mono,
            "pass": bool(ok)}


def check_group_identity(rng):
    """Gate 2: U U^{-1}=1, associativity, closure |U V|=1."""
    p = s.q_normalize(rng.standard_normal((200, 4)))
    q = s.q_normalize(rng.standard_normal((200, 4)))
    r = s.q_normalize(rng.standard_normal((200, 4)))
    err_inv = float(np.max(np.abs(s.q_mul(p, s.q_conj(p)) - s.q_identity((200,)))))
    err_assoc = float(np.max(np.abs(s.q_mul(s.q_mul(p, q), r)
                                    - s.q_mul(p, s.q_mul(q, r)))))
    err_close = float(np.max(np.abs(s.q_norm(s.q_mul(p, q)) - 1.0)))
    ok = err_inv < 1e-12 and err_assoc < 1e-12 and err_close < 1e-12
    return {"err_inverse": err_inv, "err_associativity": err_assoc,
            "err_closure": err_close, "pass": bool(ok)}


def check_gauge_invariance(rng):
    """Gate 3: S_Wilson[U] = S_Wilson[g U g^{-1}] for random site gauge g in SU(2)."""
    x, y, z, dx = c3.make_grid(Lx=16.0, Nx=21, Ny=8, Nz=8)
    shape = (len(x), len(y), len(z))
    qx = s.q_normalize(rng.standard_normal(shape + (4,)))
    qy = s.q_normalize(rng.standard_normal(shape + (4,)))
    qz = s.q_normalize(rng.standard_normal(shape + (4,)))
    lam = 0.9
    S0 = s.wilson_action(qx, qy, qz, lam, interior_x=False)
    g = s.q_normalize(rng.standard_normal(shape + (4,)))
    qxg, qyg, qzg = s.gauge_transform_links(qx, qy, qz, g)
    S1 = s.wilson_action(qxg, qyg, qzg, lam, interior_x=False)
    err = abs(S1 - S0) / max(abs(S0), 1e-12)
    return {"S_before": S0, "S_after": S1, "rel_err": err, "pass": bool(err < 1e-10)}


def check_energy_conservation(rng):
    """Gate 4: free projected-Verlet propagation conserves E_kin+E2+E4 (drift<1e-3)."""
    L = 8.0; N = 21
    xs = np.linspace(-L / 2, L / 2, N); dx = float(xs[1] - xs[0])
    # smooth small-amplitude chiral wave around the vacuum
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    amp = 0.25
    ax = amp * np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / 6.0)
    U = s.q_from_axis_angle(np.stack([np.ones_like(X), 0.5 * Y, 0.3 * Z], -1), ax)
    # body angular velocity (3-vector per site), localised pulse
    g = 0.15 * np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / 6.0)
    w = np.stack([g, 0.5 * g, np.zeros_like(g)], axis=-1)
    e_sk = 0.5
    nsteps = 150
    dt = 0.1 * dx
    E0 = s.chiral_energy(U, dx, e_sk)[2] + s.kinetic_energy(w, dx)
    # no boundary clamp: the localised pulse stays interior over this window, so the
    # geodesic-leapfrog invariant is a clean test of the symplectic integrator.
    Uf, wf, hist = s.chiral_evolve(U, w, dx, dt, nsteps, e_sk, clamp_boundary=False)
    Ef = hist[-1][0]
    drift = abs(Ef - E0) / max(abs(E0), 1e-12)
    return {"E0": E0, "E_final": Ef, "drift": drift, "nsteps": nsteps,
            "pass": bool(drift < 1e-3)}


def main():
    rng = np.random.default_rng(SEED)
    g1 = check_u1_limit(rng)
    g2 = check_group_identity(rng)
    g3 = check_gauge_invariance(rng)
    g4 = check_energy_conservation(rng)
    all_pass = g1["pass"] and g2["pass"] and g3["pass"] and g4["pass"]
    payload = {"seed": SEED,
               "gate1_u1_limit": g1, "gate2_group_identity": g2,
               "gate3_gauge_invariance": g3, "gate4_energy_conservation": g4,
               "all_pass": bool(all_pass),
               "verdict": "SIM" if all_pass else "NAO"}
    s.save_json("SU1_motor", payload)

    print("=" * 70)
    print("SU1 -- SU(2) ENGINE GATE (four checks)")
    print("=" * 70)
    print(f"1 U(1) limit       : angle+={g1['err_angle_addition']:.1e} "
          f"trace={g1['err_half_trace']:.1e} action={g1['err_wilson_action']:.1e} "
          f"mono={g1['err_monopole_charge']:.1e}  -> {'PASS' if g1['pass'] else 'FAIL'}")
    print(f"2 group identity   : inv={g2['err_inverse']:.1e} "
          f"assoc={g2['err_associativity']:.1e} close={g2['err_closure']:.1e}  "
          f"-> {'PASS' if g2['pass'] else 'FAIL'}")
    print(f"3 gauge invariance : rel_err={g3['rel_err']:.1e}  "
          f"-> {'PASS' if g3['pass'] else 'FAIL'}")
    print(f"4 energy conserv.  : drift={g4['drift']:.1e} over {g4['nsteps']} steps  "
          f"-> {'PASS' if g4['pass'] else 'FAIL'}")
    print("-" * 70)
    print(f"VERDICT: motor {'VALIDADO (SIM)' if all_pass else 'FALHOU (NAO)'}")
    return payload


if __name__ == "__main__":
    main()

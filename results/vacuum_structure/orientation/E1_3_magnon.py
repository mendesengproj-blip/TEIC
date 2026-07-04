"""E1_3_magnon.py -- the orientation wave of the causal vacuum: gapless Goldstone?

Charter: E1_ORIENTATION.md (E1-3).  Runs ONLY because E1-1 confirmed an ordered
phase (J > J_c).  The charter asks whether the orientation wave is a PHOTON
(omega = c k, relativistic Goldstone) or a MAGNON (omega = D k^2) or MASSIVE
(omega^2 = c^2 k^2 + m^2).

What is honestly measurable here, and what is not
-------------------------------------------------
The Metropolis update is RELAXATIONAL (model-A) dynamics: it samples the
equilibrium ensemble but does NOT carry the Lorentzian time-structure of the
physical theory.  The equal-time transverse structure factor

    S(k) = < | sum_i s_perp,i e^{-i k.x_i} |^2 > / N

is the same for omega=ck and for omega=Dk^2 (both have spatial stiffness ~ k^2,
hence S ~ 1/k^2): the time-derivative structure that separates them is NOT in the
equilibrium fluctuations.  So this probe can decide:

    * GAPLESS vs MASSIVE   -- S(k->0) diverges (Goldstone) or saturates (gap);
    * the spatial exponent alpha in S(k) ~ 1/k^alpha (alpha=2 = ordinary
      gradient stiffness, the relativistic SPATIAL term).

It CANNOT by itself decide omega=ck vs omega=Dk^2 -- that needs propagating
(Lorentzian) dynamics (the causal-set d'Alembertian, e10_sorkin_dalembertian /
NIVEL4 E2).  Under the relativistic assumption (2nd-order time derivative, which
the causal/Lorentzian structure supplies) omega^2 = v^2 k^alpha, so alpha=2 gives
omega ~ k (linear, photon-like).  This conditional is reported, not claimed.

Step A validates the S(k) estimator on the 3D cubic lattice (must give alpha~2).
Step B measures S(k) for the causal vacuum.  Anti-circularity: 'photon'/'magnon'
do not steer the generator; real cos/sin sums; fixed seeds.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import orientation_core as oc  # noqa: E402

OUT = Path(__file__).resolve().parent


def collect_samples(model, n_burn, n_meas, meas_every=2):
    model.equilibrate(n_burn, adapt=True)
    samples = []
    s, taken = 0, 0
    while taken < n_meas:
        model.sweep()
        s += 1
        if s % meas_every == 0:
            samples.append([c.copy() for c in oc.transverse_components(model)])
            taken += 1
    return samples


def fit_power(k, S, kmax_frac=1.0):
    """Fit log S = const - alpha log k over the cleanest range; return alpha, R^2."""
    sel = (k > 0) & (S > 0) & np.isfinite(S)
    if kmax_frac < 1.0:
        sel &= k <= kmax_frac * k.max()
    lk, lS = np.log(k[sel]), np.log(S[sel])
    a = np.polyfit(lk, lS, 1)
    alpha = -a[0]
    R2 = oc._r2(lS, a[1] + a[0] * lk)
    return float(alpha), float(R2)


# ----------------------------------------------------------------------- #
# Step A -- validate S(k) ~ 1/k^2 on the 3D cubic lattice (ordered phase)
# ----------------------------------------------------------------------- #
def step_A():
    print("-" * 72)
    print("E1-3 step A: validate S(k) estimator on 3D cubic XY/O(3) (expect alpha~2)")
    L = 24
    g = oc.lattice_periodic((L, L, L))
    coords = np.stack(np.unravel_index(np.arange(g.n), (L, L, L)), axis=1).astype(float)
    kmags = 2 * np.pi / L * np.arange(1, 9)        # commensurate spatial modes
    res = {}
    for model_name, J in (("U(1)", 1.0), ("O(3)", 1.5)):
        m = oc.MODELS[model_name](g, J=J, seed=3)
        samples = collect_samples(m, n_burn=1500, n_meas=120, meas_every=2)
        S = oc.structure_factor(samples, coords, kmags, n_dirs=3)
        alpha, R2 = fit_power(kmags, S)
        res[model_name] = {"k": kmags.tolist(), "S": S.tolist(),
                           "alpha": alpha, "R2": R2}
        print(f"   {model_name}: alpha={alpha:.2f}  R2={R2:.3f}  "
              f"(gapless: S rises as k->0 = {S[0] > S[-1]})")
    ok = all(abs(res[m]["alpha"] - 2.0) < 0.4 for m in res)
    print(f"   step-A validation: {'PASS' if ok else 'FAIL'} "
          "(estimator reproduces gradient stiffness alpha~2)")
    return res, ok


# ----------------------------------------------------------------------- #
# Step B -- S(k) of the causal vacuum in the ordered phase
# ----------------------------------------------------------------------- #
RHO = 0.5
BOX = [(0.0, 10.0)] * 4          # isotropic 4D box for clean spatial S(k)
J_ORD = 2.0                      # deep in the ordered phase (J >> J_c ~ 0.1)
N_SEEDS = 6
N_K = 16


def step_B():
    print("-" * 72)
    print(f"E1-3 step B: causal-vacuum S(k)  rho={RHO} box={BOX[0]}^4 J={J_ORD}")
    res = {m: {"S_acc": None, "k": None} for m in ("U(1)", "O(3)")}
    gstats = []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(9000 + seed)
        pts = oc.sprinkle_box(RHO, BOX, rng)
        g = oc.causal_link_graph(pts)
        xs = pts[:, 1:]                                   # spatial coords (3D)
        spacing = RHO ** (-0.25)
        kmin = 2 * np.pi / (BOX[1][1] - BOX[1][0])
        kmax = np.pi / spacing                            # ~ Nyquist of the sprinkle
        kmags = np.geomspace(kmin, kmax, N_K)
        gstats.append({"n": g.n, "links": g.n_links, "avgdeg": 2 * g.n_links / g.n})
        for model_name in ("U(1)", "O(3)"):
            m = oc.MODELS[model_name](g, J=J_ORD, seed=100 * seed + 5)
            samples = collect_samples(m, n_burn=1000, n_meas=80, meas_every=2)
            S = oc.structure_factor(samples, xs, kmags, n_dirs=3)
            if res[model_name]["S_acc"] is None:
                res[model_name]["S_acc"] = np.zeros_like(S)
                res[model_name]["k"] = kmags
            res[model_name]["S_acc"] += S
        print(f"   seed {seed}: n={g.n} avgdeg={2*g.n_links/g.n:.0f}")
    out = {}
    for model_name in ("U(1)", "O(3)"):
        k = res[model_name]["k"]
        S = res[model_name]["S_acc"] / N_SEEDS
        # fit over the trustworthy window (drop the highest k near Nyquist)
        alpha, R2 = fit_power(k, S, kmax_frac=0.7)
        ratio = float(S[0] / S[-1])
        # classify the spatial stiffness:
        #   'goldstone' : S ~ 1/k^2, strong small-k rise (local gradient stiffness);
        #   'flat'      : S ~ const, alpha~0, ratio~1 (NON-LOCAL / mean-field, the
        #                 causal-set non-locality -- no gradient term);
        #   'massive'   : S saturates to a small-k plateau then falls (mass gap).
        if alpha >= 1.4 and ratio > 4.0:
            shape = "goldstone"
        elif alpha < 0.6 and ratio < 2.0:
            shape = "flat_nonlocal"
        else:
            shape = "massive_or_mixed"
        out[model_name] = {"k": k.tolist(), "S": S.tolist(), "alpha": alpha,
                           "R2": R2, "ratio_kmin_kmax": ratio, "shape": shape}
        print(f"   {model_name}: alpha={alpha:.2f}  R2={R2:.3f}  "
              f"S(kmin)/S(kmax)={ratio:.1f}  shape={shape}")
    out["graph_stats"] = {kk: float(np.mean([s[kk] for s in gstats]))
                          for kk in ("n", "links", "avgdeg")}
    return out


def main():
    t0 = time.time()
    print("=" * 72)
    print("E1-3 -- orientation wave of the causal vacuum (Goldstone structure)")
    print("=" * 72)
    A, A_ok = step_A()
    B = step_B()

    # ---- verdict --------------------------------------------------------
    shapes = {m: B[m]["shape"] for m in ("U(1)", "O(3)")}
    if not A_ok:
        code, verdict = "INVALID", "estimator failed step-A validation"
    elif all(s == "goldstone" for s in shapes.values()):
        code = "A"
        verdict = ("GAPLESS GOLDSTONE, S~1/k^2 (local gradient stiffness) -> under "
                   "relativistic 2nd-order dynamics omega~k, PHOTON-like.  ck-vs-Dk^2 "
                   "not separable by an equilibrium probe -- PARTIAL on magnon.")
    elif all(s == "flat_nonlocal" for s in shapes.values()):
        code = "C"
        verdict = ("FLAT S(k) (alpha~0): the link-coupled orientation field is "
                   "NON-LOCAL / mean-field (avgdeg~130, causal-set non-locality) -- "
                   "it has NO gradient (k^2) stiffness, so the naive links do NOT "
                   "support a relativistic Goldstone/photon.  'photon=magnon' NOT "
                   "established by the bare link action; recovering omega=ck needs the "
                   "smeared causal-set d'Alembertian (Sorkin/BD, e10).")
    else:
        code = "B"
        verdict = (f"MIXED/MASSIVE: shapes={shapes} -- gapped or intermediate "
                   "stiffness; relativistic Goldstone not cleanly supported.")

    print("-" * 72)
    print(f"step A (estimator valid): {'PASS' if A_ok else 'FAIL'}")
    print(f"causal vacuum S(k) shapes: {shapes}")
    print(f"VERDICT (E1-3) [{code}]: {verdict}")
    print("=" * 72)

    # ---- figure --------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for model_name, col in (("U(1)", "tab:blue"), ("O(3)", "tab:red")):
        kL = np.array(A[model_name]["k"]); SL = np.array(A[model_name]["S"])
        axes[0].loglog(kL, SL, "o", color=col, label=f"{model_name} (lattice)")
        kC = np.array(B[model_name]["k"]); SC = np.array(B[model_name]["S"])
        axes[1].loglog(kC, SC, "o-", color=col,
                       label=f"{model_name} alpha={B[model_name]['alpha']:.2f}")
    for ax in axes:
        kk = np.array(A["U(1)"]["k"])
        ax.loglog(kk, kk.astype(float) ** -2.0 * (A["U(1)"]["S"][0] * kk[0] ** 2),
                  "k--", lw=1, label=r"$1/k^2$ (gapless Goldstone)")
        ax.set_xlabel("k"); ax.set_ylabel("S(k)"); ax.legend(fontsize=8)
        ax.grid(alpha=0.2, which="both")
    axes[0].set_title("step A: 3D lattice (validation, expect 1/k^2)")
    axes[1].set_title("step B: causal vacuum transverse S(k)")
    fig.suptitle("E1-3: transverse structure factor -- gapless Goldstone test\n"
                 "S(k)~1/k^2 = massless mode; saturation at small k = mass gap",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E1_3_magnon.png", dpi=130)
    print(f"saved {OUT/'E1_3_magnon.png'}")

    payload = {"step_A": A, "step_A_pass": bool(A_ok), "step_B": B,
               "config_B": {"rho": RHO, "box": BOX, "J": J_ORD, "n_seeds": N_SEEDS,
                            "n_k": N_K},
               "shapes": shapes, "verdict_code": code, "verdict": verdict,
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E1_3_magnon.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E1_3_magnon.json'}  ({payload['runtime_s']:.0f}s)")


if __name__ == "__main__":
    main()

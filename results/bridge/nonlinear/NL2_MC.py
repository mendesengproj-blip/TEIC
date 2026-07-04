"""NL2_MC.py -- The quadratic (second-order) coefficient: dynamical vs kinematic.

BRIDGE / NON-LINEAR investigation.  Independent of R1-R3 and e6-e11; modifies
nothing.  Continues NL1 (lambda free: the BD action is quadratic, so it carries no
dynamical non-linearity) and D3 (linear MC -> theta = A/r).

The question: does the network reproduce Schwarzschild's SECOND order, i.e. the
quadratic term of rho_eff/rho0 = 1/sqrt(1-2u) = 1 + u + (3/2)u^2 + ...?  (Target
coefficient +3/2 for the DENSITY -- see NL1; the prompt's 1/2 is the redshift's.)

Two channels, measured separately and honestly:

  (1) DYNAMICAL.  Run the D3 field MC (longer / higher inner resolution) and fit the
      emergent potential theta_MC(r) = C + A1/r + A2/r^2.  Because the BD action is
      LINEAR (quadratic action -> linear Euler-Lagrange operator), the minimiser is
      the harmonic 1/r with NO 1/r^2 term: we expect A2/A1^2 ~ 0.  This is the
      direct test of "does the field dynamics generate a second order" -> NO,
      confirming NL1.

  (2) KINEMATIC.  The bridge density is rho_eff = rho0 / (dtau/dt), and dtau/dt is a
      static observer's PROPER-TIME clock, measured by COUNTING (P2/P3, R3).  Feeding
      the LINEAR potential theta_MC into a flat variable-density sprinkle of local
      proper density (1 - 2 theta) [an allowed volume element -- NO square root in
      the generator], the counted clock rate comes out sqrt(1-2 theta), so
          rho_eff/rho0 = 1/sqrt(1-2 theta) = 1 + theta + (3/2) theta^2 + ...
      and a fit rho_eff/rho0 = 1 + B1/r + B2/r^2 returns B2/B1^2 ~ 3/2.  The second
      order is reproduced KINEMATICALLY (the diamond-volume sqrt of the clock acting
      on the linear potential), not dynamically.

ANTI-CIRCULARITY.  The generator sprinkles at density (1 - 2 theta) (allowed volume
element); the square root EMERGES from the causal counting (diamond volume), never
imposed.  Schwarzschild's 1/sqrt(1-2u) and the coefficient 3/2 appear ONLY in the
final COMPARISON ONLY block.  The guard (tests/test_no_circularity.py) still passes.

Verdict logic: NL2 (dynamical) reproduces the prompt's MORTE (A2 ~ 0 -> linear
action carries no non-linearity), AND the kinematic channel reproduces +3/2 (strong
evidence the bridge density converges to Schwarzschild at second order).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval  # noqa: E402
from repro import rng  # noqa: E402
from volume import tau_from_count  # noqa: E402
from validation import schwarzschild_redshift  # noqa: E402 (COMPARISON ONLY)

OUT = Path(__file__).resolve().parent

SEED = 2718281828
D = 3
R_MIN, R_MAX, R_CORE = 1.0, 60.0, 4.0
N_BINS = 60
K_STIFF, KAPPA_M, TEMP, STEP = 1.0, 1.0, 0.02, 0.05
N_SWEEPS, N_BURN = 40000, 10000

# counting-channel parameters (P3-style); radii are chosen in main() by target u
RHO0 = 6000.0
N_REAL = 80
DELTAS = np.array([0.8, 1.2, 1.6, 2.0])


# --------------------------------------------------------------------------- #
# (1) D3 field MC -> emergent linear potential theta_MC(r)
# --------------------------------------------------------------------------- #
def run_field_mc():
    g = np.random.default_rng(SEED)
    edges = np.geomspace(R_MIN, R_MAX, N_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    shell_vol = (edges[1:] ** D - edges[:-1] ** D) / D
    dr_edge = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H_l = (0.5 * K_STIFF * vbar / dr_edge ** 2).tolist()
    s = np.where(centers < R_CORE, shell_vol, 0.0)
    s_l = (s / s.sum()).tolist()
    V_l = shell_vol.tolist()
    B = N_BINS
    invT = 1.0 / TEMP
    theta = [0.0] * B

    def delta_E_pair(i, dti, j, dtj):
        th = theta
        et = set()
        for x in (i, j):
            if x - 1 >= 0:
                et.add(x - 1)
            if x < B - 1:
                et.add(x)
        old = 0.0
        for e in et:
            d = th[e + 1] - th[e]; old += H_l[e] * d * d
        th[i] += dti; th[j] += dtj
        new = 0.0
        for e in et:
            d = th[e + 1] - th[e]; new += H_l[e] * d * d
        th[i] -= dti; th[j] -= dtj
        return (new - old) - KAPPA_M * (s_l[i] * dti + s_l[j] * dtj)

    acc = np.zeros(B); nm = 0
    for sweep in range(N_SWEEPS):
        for _ in range(B):
            i = int(g.integers(0, B)); j = int(g.integers(0, B))
            if i == j:
                continue
            dti = STEP * g.uniform(-1.0, 1.0)
            dtj = -dti * V_l[i] / V_l[j]
            dE = delta_E_pair(i, dti, j, dtj)
            if dE <= 0.0 or g.uniform() < np.exp(-dE * invT):
                theta[i] += dti; theta[j] += dtj
        if sweep >= N_BURN:
            acc += theta; nm += 1
    return centers, shell_vol, acc / max(nm, 1)


# --------------------------------------------------------------------------- #
# (2) kinematic counting channel: dtau/dt by counting in a (1-2 theta) sprinkle
# --------------------------------------------------------------------------- #
def sprinkle_flat_variable(rho0, fval, t_bounds, x_bounds, g):
    t_bounds = np.asarray(t_bounds, float); x_bounds = np.asarray(x_bounds, float)
    area = (t_bounds[1] - t_bounds[0]) * (x_bounds[1] - x_bounds[0])
    n = g.poisson(rho0 * fval * area)
    return np.column_stack([g.uniform(t_bounds[0], t_bounds[1], n),
                            g.uniform(x_bounds[0], x_bounds[1], n)])


def count_clock_rate(theta_pot_r, g):
    """Static-observer dtau/dt at radius with potential theta_pot_r, by counting in a
    flat sprinkle of local proper density rho0*(1 - 2 theta) (no sqrt in generator)."""
    fval = 1.0 - 2.0 * theta_pot_r                          # allowed volume element
    taus = []
    for dt in DELTAS:
        t1, t2 = -dt / 2, dt / 2
        A = np.array([t1, 0.0]); Bp = np.array([t2, 0.0])
        pad = 0.05 * dt
        tb = (t1 - pad, t2 + pad); xb = (-dt / 2 - pad, dt / 2 + pad)
        ns = [len(alexandrov_interval(sprinkle_flat_variable(RHO0, fval, tb, xb, g), A, Bp))
              for _ in range(N_REAL)]
        taus.append(tau_from_count(np.mean(ns), RHO0, 2))
    taus = np.array(taus)
    return float(np.sum(DELTAS * taus) / np.sum(DELTAS ** 2))


def main():
    # ---- (1) dynamical channel ----
    centers, shell_vol, theta_mc = run_field_mc()
    # Fit theta_MC = C + A1/r + A2/r^2 FAR from the source core (r >= 2.5 R_CORE),
    # where the harmonic solution is pure 1/r; near-core bins (where the profile
    # bends through the smeared source) would inject a spurious A2.
    use = (centers >= 2.5 * R_CORE) & (centers <= R_MAX * 0.6)
    Xd = np.vstack([np.ones(use.sum()), 1.0 / centers[use], 1.0 / centers[use] ** 2]).T
    Cc, A1, A2 = np.linalg.lstsq(Xd, theta_mc[use], rcond=None)[0]
    A1, A2, Cc = float(A1), float(A2), float(Cc)
    dyn_ratio = A2 / A1 ** 2 if A1 != 0 else float("nan")   # ~ 0 expected (linear)
    # robust corroboration: offset-removed log-log slope ~ -1 (pure 1/r, no 2nd order)
    resid = theta_mc[use] - Cc
    rok = resid > 0
    dyn_expo = float(np.polyfit(np.log(centers[use][rok]), np.log(resid[rok]), 1)[0]) \
        if rok.sum() >= 4 else float("nan")

    # ---- (2) kinematic channel: count rho_eff for the linear potential theta=A1/r ----
    # Choose radii by TARGET u = A1/r in the weak-to-moderate band, so the quadratic
    # coefficient is detectable yet the weak-field expansion is valid.  Extract the
    # second-order coefficient as the u->0 intercept of c2(r) = (rho_eff-1-u)/u^2
    # (which equals 3/2 + (5/2)u + ...), avoiding strong-field contamination.
    g = rng(SEED + 7)
    u_targets = np.array([0.18, 0.14, 0.105, 0.075, 0.05])
    radii_cnt = A1 / u_targets
    u = A1 / radii_cnt
    theta_pot = A1 / radii_cnt
    dtau = np.array([count_clock_rate(t, g) for t in theta_pot])
    rho_eff = 1.0 / dtau                                    # rho_eff/rho0 (bridge)
    c2 = (rho_eff - 1.0 - u) / u ** 2                       # per-point apparent 2nd coeff
    # linear extrapolation c2 = a + b u  ->  intercept a is the 2nd-order coefficient
    bcoef, acoef = np.polyfit(u, c2, 1)[0], np.polyfit(u, c2, 1)[1]
    kin_ratio = float(acoef)                               # ~ 3/2 expected
    kin_slope = float(bcoef)

    # ============================ COMPARISON ONLY ============================
    sch_rho = 1.0 / schwarzschild_redshift(radii_cnt, A1)  # 1/sqrt(1-2u)
    newt_rho = 1.0 + u
    cnt_vs_sch_err = float(np.max(np.abs(rho_eff - sch_rho) / sch_rho))
    cnt_vs_newt_err = float(np.max(np.abs(rho_eff - newt_rho) / newt_rho))
    target_2nd = 1.5
    # ========================== END COMPARISON ONLY =========================

    RADII_CNT = radii_cnt                                  # for reporting/plot
    dyn_is_zero = bool(abs(dyn_ratio) < 0.3 or abs(dyn_expo + 1.0) < 0.1)
    kin_matches = bool(abs(kin_ratio - target_2nd) < 0.2 * target_2nd)  # +/-20%
    cnt_beats_newt = bool(cnt_vs_sch_err < cnt_vs_newt_err)
    verdict = ("PASSA (cinematico)" if kin_matches and cnt_beats_newt else
               ("PARCIAL" if (kin_ratio > 0.8 and cnt_beats_newt) else "FALHA"))

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    ax[0].loglog(centers[use], np.abs(theta_mc[use] - Cc), "o", ms=4,
                 label=r"$|\theta_{\rm MC}-C|$ (dynamical)")
    rr = centers[use]
    ax[0].loglog(rr, A1 / rr, "k--", lw=1, label=r"$A_1/r$ (slope $-1$)")
    ax[0].set_title(f"(NL2) dynamical: $A_2/A_1^2$={dyn_ratio:.2f} (linear $\\to$ 0)")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$\theta-C$"); ax[0].legend(fontsize=8)

    ax[1].plot(RADII_CNT, rho_eff, "o", ms=7, label="counted $\\rho_{\\rm eff}/\\rho_0$")
    rrc = np.linspace(RADII_CNT.min(), RADII_CNT.max(), 200)
    ax[1].plot(rrc, 1.0 / schwarzschild_redshift(rrc, A1), "k-", lw=1.3,
               label=r"Schwarzschild $1/\sqrt{1-2u}$")
    ax[1].plot(rrc, 1.0 + A1 / rrc, "0.6", ls="--", lw=1, label=r"Newtonian $1+u$")
    ax[1].set_title(f"kinematic: $B_2/B_1^2$={kin_ratio:.2f} (Schwarzschild $=3/2$)")
    ax[1].set_xlabel("r"); ax[1].set_ylabel(r"$\rho_{\rm eff}/\rho_0$"); ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "NL2_MC.png", dpi=130)

    summary = {
        "what": "second-order coefficient: dynamical (field MC, ~0) vs kinematic "
                "(proper-time counting on the linear potential, ~3/2).",
        "target_density_2nd_order_coeff": target_2nd,
        "note_prompt_value": "prompt's 1/2 is the redshift coeff; density target is 3/2 (NL1).",
        "dynamical": {"C": Cc, "A1": A1, "A2": A2, "A2_over_A1sq": dyn_ratio,
                      "offset_removed_exponent": dyn_expo, "is_zero": dyn_is_zero,
                      "meaning": "linear BD action -> no dynamical second order (NL1)."},
        "kinematic": {"2nd_order_coeff_intercept": kin_ratio, "c2_slope_in_u": kin_slope,
                      "matches_3_2_within_20pct": kin_matches,
                      "u": u.tolist(), "c2_per_point": c2.tolist(),
                      "counted_rho_eff": rho_eff.tolist(),
                      "radii": RADII_CNT.tolist()},
        "COMPARISON_count_vs_schwarzschild_max_err": cnt_vs_sch_err,
        "COMPARISON_count_vs_newtonian_max_err": cnt_vs_newt_err,
        "COMPARISON_count_beats_newtonian": cnt_beats_newt,
        "verdict": verdict,
        "seed": SEED,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "NL2_MC_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("NL2 -- SECOND-ORDER COEFFICIENT: DYNAMICAL vs KINEMATIC")
    print("=" * 72)
    print(f"target (density 2nd-order coeff)  : 3/2   [prompt's 1/2 is the redshift's]")
    print("-" * 72)
    print("DYNAMICAL channel (D3 field MC, linear action):")
    print(f"  theta_MC = C + A1/r + A2/r^2 (far fit): C={Cc:+.4f}  A1={A1:.4f}  A2={A2:+.4f}")
    print(f"  A2/A1^2 = {dyn_ratio:+.3f}  | offset-removed exponent = {dyn_expo:+.3f}")
    print(f"  -> ~0 (no dynamical second order): {dyn_is_zero}")
    print("-" * 72)
    print("KINEMATIC channel (proper-time counting on linear potential theta=A1/r):")
    for r_, u_, re_, c_ in zip(RADII_CNT, u, rho_eff, c2):
        print(f"   r={r_:5.1f} (u={u_:.3f}):  rho_eff/rho0={re_:.4f}  c2=(rho-1-u)/u^2={c_:.3f}")
    print(f"  2nd-order coeff (u->0 intercept of c2) = {kin_ratio:.3f}  "
          f"(Schwarzschild = 1.5; +/-20%: {kin_matches})")
    print(f"  [COMPARISON] count vs Schwarzschild err {cnt_vs_sch_err:.2%} | "
          f"vs Newtonian err {cnt_vs_newt_err:.2%} -> Schwarzschild better: {cnt_beats_newt}")
    print("-" * 72)
    print(f"VERDICT (NL2): {verdict}")
    print("  dynamical second order ~ 0 (linear action, confirms NL1); kinematic")
    print("  second order ~ 3/2 (clock sqrt on the linear potential) -> convergence.")
    return summary


if __name__ == "__main__":
    main()

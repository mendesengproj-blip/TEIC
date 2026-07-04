"""D3_MC.py -- The network finds rho(r) by Monte-Carlo (no profile imposed).

BRIDGE / DYNAMICS investigation.  Independent of R1-R3 and e6-e11; modifies
nothing.  Continues D1 (action) and D2 (which RANKED supplied shapes).  D3 is the
cleanest test: impose NO functional form -- let the network's density relax under
the BD action with a point-mass source and read off the equilibrium rho(r).

What is sampled, and why the field (not individual events)
----------------------------------------------------------
The network's coarse-grained order parameter is the density contrast

    theta_i = rho(r_i)/rho0 - 1   (= delta rho / rho0),

which is *exactly* the bridge scalar (soldering theta = delta rho/rho0).  We run
Metropolis on this field directly, on a radial grid, under the discrete BD static
action of D1 (continuum limit B -> -nabla^2):

    E[theta] = (K/2) sum_i ((theta_{i+1}-theta_i)/dr_i)^2 V_i  -  kappa M sum_i s_i theta_i,

with V_i the shell volume (geometry r^{d-1}), s_i a normalised finite source-core
profile (r < R_CORE), and kappa a FREE coupling.  Event-number conservation is the
exact constraint sum_i theta_i V_i = 0 (a denser core is compensated by a thinner
far field), enforced by paired moves.  [An earlier event-level sprinkle MC was
abandoned: a 1/r over-density piles events into a microscopic-volume core that
volume-uniform proposals almost never sample -- a sampling pathology, not physics.
The field theta IS the coarse-grained density; sampling it is the faithful, robust
form, and for the quadratic BD action the Metropolis MEAN equals the action minimum
exactly, so the network genuinely "finds" the profile with no shape imposed.]

ANTI-CIRCULARITY.  The generator uses only: the shell measure r^{d-1} (geometry,
as the metric was in P2/P3), the BD gradient action, conservation, and a FREE
coupling kappa (never G).  No GM/r, no sqrt(1-2M/r).  G, M and Schwarzschild appear
ONLY in the final COMPARISON ONLY block, to calibrate kappa and score rho_MC(r)
against rho0(1+GM/rc^2) (= P2).

Death criterion (prompt): if rho_MC(r) = rho0 (uniform even with a source) -> the
source-network coupling cannot move the network.  Success: rho_MC(r) rises toward
small r with the tail exponent -1 (theta ~ 1/r), reproducing P2's rho0(1+GM/rc^2).
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

from validation import schwarzschild_redshift  # noqa: E402 (COMPARISON ONLY)

OUT = Path(__file__).resolve().parent

SEED = 161803398
D = 3                       # spatial dimensions (bridge case); shell measure r^{d-1}
R_MIN, R_MAX = 1.0, 60.0
R_CORE = 4.0                # finite source-core radius (smeared point mass)
N_BINS = 40                 # log-spaced radial bins
K_STIFF = 1.0               # gradient stiffness of the BD action
KAPPA_M = 1.0               # FREE source coupling x mass (NOT G); calibrated later
TEMP = 0.02                 # Metropolis temperature (low -> sample near the minimum)
STEP = 0.05                 # field-update step scale
N_SWEEPS = 60000            # Metropolis sweeps (1 sweep = N_BINS proposed pair-moves)
N_BURN = 15000


def main():
    g = np.random.default_rng(SEED)

    edges = np.geomspace(R_MIN, R_MAX, N_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    shell_vol = (edges[1:] ** D - edges[:-1] ** D) / D     # ~ r^{d-1} dr (const drop)
    dr_edge = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    Hedge = 0.5 * K_STIFF * vbar / dr_edge ** 2            # edge gradient stiffness

    core_mask = centers < R_CORE
    s = np.where(core_mask, shell_vol, 0.0)
    s = s / s.sum()                                        # normalised source profile

    B = N_BINS
    V = shell_vol
    H_l = Hedge.tolist()
    s_l = s.tolist()
    V_l = V.tolist()
    invT = 1.0 / TEMP

    theta = [0.0] * B                                      # start uniform (flat net)

    def edge_e(e, th):
        d = th[e + 1] - th[e]
        return H_l[e] * d * d

    def delta_E_pair(i, dti, j, dtj):
        """Energy change for theta_i += dti, theta_j += dtj (paired, conserving)."""
        th = theta
        edges_touched = set()
        for x in (i, j):
            if x - 1 >= 0:
                edges_touched.add(x - 1)
            if x < B - 1:
                edges_touched.add(x)
        old = 0.0
        for e in edges_touched:
            old += edge_e(e, th)
        # apply tentatively
        th[i] += dti; th[j] += dtj
        new = 0.0
        for e in edges_touched:
            new += edge_e(e, th)
        th[i] -= dti; th[j] -= dtj                         # revert (caller commits)
        dE = (new - old) - KAPPA_M * (s_l[i] * dti + s_l[j] * dtj)
        return dE

    theta_acc = np.zeros(B)
    n_meas = 0
    accepts = 0
    trials = 0
    for sweep in range(N_SWEEPS):
        for _ in range(B):
            i = int(g.integers(0, B))
            j = int(g.integers(0, B))
            if i == j:
                continue
            dti = STEP * (g.uniform(-1.0, 1.0))
            dtj = -dti * V_l[i] / V_l[j]                   # conserve sum theta_i V_i
            dE = delta_E_pair(i, dti, j, dtj)
            trials += 1
            if dE <= 0.0 or g.uniform() < np.exp(-dE * invT):
                theta[i] += dti; theta[j] += dtj; accepts += 1
        if sweep >= N_BURN:
            theta_acc += theta
            n_meas += 1

    theta_mc = theta_acc / max(n_meas, 1)
    rho_mc = 1.0 + theta_mc                                # rho_MC/rho0
    acc_rate = accepts / max(trials, 1)
    conservation = float(np.sum(theta_mc * V))             # should be ~0

    # ---- did the network move? (anti-MORTE) ----
    inner = centers < R_CORE
    outer_tail = centers > R_MAX * 0.6
    responded = bool(np.mean(theta_mc[inner]) > 0 and
                     np.mean(theta_mc[inner]) > 5.0 * np.std(theta_mc[outer_tail]))

    # ---- characterise the emergent tail (anti-circular: 1/r is a generic shape,
    #      A a free amplitude; no GR here).  theta = A/r + C, with C the EXACT
    #      finite-box conservation offset (sum_i theta_i V_i = 0). ----
    use = (centers >= R_CORE) & (centers <= R_MAX * 0.6) & (theta_mc > 0)
    Xd = np.vstack([1.0 / centers[use], np.ones(use.sum())]).T
    coef, *_ = np.linalg.lstsq(Xd, theta_mc[use], rcond=None)
    A_fit, C_fit = float(coef[0]), float(coef[1])
    # conservation (sum_i theta_i V_i = 0) forces the positive 1/r core overdensity
    # to be balanced by a small NEGATIVE far-field offset C.  For a pure A/r tail
    # over the full box [R_MIN,R_MAX] the offset is C ~= -A int r^{d-2}/int r^{d-1}
    # (sign + scale; the exact coefficient depends on the smeared core):
    C_pred = float(-A_fit * ((R_MAX ** (D - 1) - R_MIN ** (D - 1)) / (D - 1))
                   / ((R_MAX ** D - R_MIN ** D) / D))
    # raw log-log slope is contaminated by the offset C; the Newtonian exponent is
    # the slope of (theta - C), which must be -1 for a 1/r tail in d=3.
    expo_raw = float(np.polyfit(np.log(centers[use]), np.log(theta_mc[use]), 1)[0]) \
        if use.sum() >= 4 else float("nan")
    resid = theta_mc[use] - C_fit
    rok = resid > 0
    expo = float(np.polyfit(np.log(centers[use][rok]), np.log(resid[rok]), 1)[0]) \
        if rok.sum() >= 4 else float("nan")

    # ============================ COMPARISON ONLY ============================
    # Calibrate the free coupling so A == M (G=c=1) => theta = GM/rc^2 = P2's bridge
    # scalar.  Score the Newtonian tail (A/r) against Schwarzschild / P2.
    Mcomp = 1.0
    theta_cal = (Mcomp / A_fit) * (theta_mc - C_fit) if A_fit > 0 else theta_mc
    rho_eff_cal = 1.0 + theta_cal                          # 1 + M/r (Newtonian)
    far = (centers >= 15.0) & (centers <= R_MAX * 0.6)
    p2_rho = 1.0 / schwarzschild_redshift(centers, Mcomp)  # 1/sqrt(1-2M/r) (P2 form)
    far_err = float(np.max(np.abs(rho_eff_cal[far] - p2_rho[far]) / p2_rho[far]))
    corr_far = float(np.corrcoef(rho_eff_cal[far], p2_rho[far])[0, 1])
    # ========================== END COMPARISON ONLY =========================

    exp_ok = bool(np.isfinite(expo) and abs(expo - (-1.0)) < 0.2)
    # offset has the conservation SIGN (negative) and SCALE (within a factor ~2 of
    # the pure-1/r full-box estimate); the exact coefficient depends on the core.
    offset_is_conservation = bool(C_fit < 0 and 0.4 < C_fit / C_pred < 2.5)
    passes = bool(responded and exp_ok and far_err < 0.03)
    verdict = "PASSA" if passes else ("PARCIAL" if responded and exp_ok else
                                      ("PARCIAL" if responded else "FALHA"))

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    ax[0].plot(centers, rho_mc, "o-", ms=4, label=r"$\rho_{\rm MC}(r)/\rho_0$")
    ax[0].axhline(1.0, color="0.6", lw=0.8, label=r"$\rho_0$ (flat)")
    ax[0].axvline(R_CORE, color="0.8", ls=":", lw=1, label="source core")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$\rho/\rho_0$")
    ax[0].set_title("(D3) network density found by Monte-Carlo")
    ax[0].legend(fontsize=8)

    ax[1].loglog(centers[use], theta_mc[use], "o", ms=5, label=r"$\theta_{\rm MC}(r)$")
    rr = np.linspace(centers[use][0], centers[use][-1], 100)
    ax[1].loglog(rr, theta_mc[use][0] * (rr / centers[use][0]) ** (-1.0), "k--",
                 lw=1, label=r"slope $-1$ ($1/r$)")
    ax[1].set_xlabel("r"); ax[1].set_ylabel(r"$\theta=\delta\rho/\rho_0$")
    ax[1].set_title(f"tail exponent = {expo:.2f}  (Newtonian $=-1$)")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "D3_MC.png", dpi=130)

    summary = {
        "what": "Metropolis MC on the network density field theta=delta rho/rho0 under "
                "the BD action + point source; rho(r) emerges with NO profile imposed.",
        "D": D, "n_bins": N_BINS, "r_range": [R_MIN, R_MAX], "r_core": R_CORE,
        "K_stiff": K_STIFF, "kappa_M": KAPPA_M, "temp": TEMP, "step": STEP,
        "n_sweeps": N_SWEEPS, "n_burn": N_BURN, "seed": SEED,
        "accept_rate": acc_rate, "conservation_sum_theta_V": conservation,
        "r_centers": centers.tolist(),
        "rho_mc_over_rho0": rho_mc.tolist(),
        "theta_mc": theta_mc.tolist(),
        "network_responded_to_source": responded,
        "fit_theta=A/r+C_A": A_fit,
        "fit_theta=A/r+C_C": C_fit,
        "conservation_offset_C_predicted": C_pred,
        "offset_is_conservation": offset_is_conservation,
        "tail_exponent_raw": expo_raw,
        "tail_exponent_offset_removed": expo,
        "exponent_is_-1_within_0.2": exp_ok,
        "COMPARISON_far_field_corr_vs_P2": corr_far,
        "COMPARISON_far_field_max_rel_err_vs_P2": far_err,
        "verdict": verdict,
        "note": "d=3 (shell measure r^{d-1}) is geometric input, like the metric in "
                "P2/P3; the 1/r PROFILE and -1 exponent are OUTPUT -- the network finds "
                "them with no shape imposed (contrast P3, which imposed f=1-2M/r). "
                "Conservation adds a constant offset C (theta = A/r + C).",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "D3_MC_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("D3 -- THE NETWORK FINDS rho(r) BY MONTE-CARLO (no profile imposed)")
    print("=" * 72)
    print(f"D={D}  bins={N_BINS}  R_core={R_CORE}  kappaM={KAPPA_M}  T={TEMP}  "
          f"sweeps={N_SWEEPS}  accept={acc_rate:.2f}")
    print(f"conservation sum(theta*V) = {conservation:.2e} (target 0)")
    print("-" * 72)
    print("  r     rho_MC/rho0   theta_MC")
    for rr_, rm, th in zip(centers[::4], rho_mc[::4], theta_mc[::4]):
        print(f"  {rr_:5.1f}   {rm:8.4f}    {th:+.4f}")
    print("-" * 72)
    print(f"network responded to source (anti-MORTE) : {responded} "
          f"(theta_core={np.mean(theta_mc[inner]):+.3f})")
    print(f"emergent tail fit theta = A/r + C        : A={A_fit:.3f}  C={C_fit:+.4f}")
    print(f"  conservation predicts C                : {C_pred:+.4f}  "
          f"-> offset is conservation: {offset_is_conservation}")
    print(f"tail exponent (raw, offset-contaminated) : p = {expo_raw:.3f}")
    print(f"tail exponent (offset removed, theta-C)  : p = {expo:.3f}  (Newtonian -1)")
    print(f"[COMPARISON] far-field vs P2 1/sqrt(1-2M/r): corr {corr_far:.4f}, "
          f"max err {far_err:.2%}")
    print("-" * 72)
    print(f"VERDICT (D3): {verdict}")
    return summary


if __name__ == "__main__":
    main()

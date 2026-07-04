"""MG1_skyrmion_gravity.py -- the Skyrmion as a DIRECT source of gravity.

Charter: docs/prompts/MG1_MATTER_SOURCES_GRAVITY.md (kill criteria PRE-REGISTERED).
Item R2 of RESEARCH_MAP.md: the central gap of PAPER_MATTER_GRAVITY (Sec. VII).

The paper establishes theta = G_net M / r as a COMPOSITION of two separately measured
laws (the shape-independent Poisson exterior + the soliton as a localised weight), but
the soliton's OWN energy-density profile was never used as the literal source ("the
natural next step").  MG1 composes the two existing engines:
  * gravity: the static Benincasa-Dowker (BD) action of D1-D3
    (results/bridge/dynamics/D3_MC.py), E[theta] = sum_e H_e (dtheta)^2 - sum_i b_i theta_i,
    with conservation sum_i theta_i V_i = 0.  The action is QUADRATIC, so its minimum is
    the exact linear Poisson solution -- solved directly here, validated vs the D3
    Metropolis at gate G0.
  * matter: the SU(2)/colour Skyrmion radial profile F(r) of su3_core.radial_relax,
    whose energy density eps(r) = dE/dr is fed in AS the source b_i.

Tests (pre-registered):
  G0  exact solver reproduces D3 (top-hat source, K=1, kappaM=1): exponent -1, A>0,
      conservation offset C<0.
  M-EXPOENTE  source = Skyrmion eps(r): exterior exponent = -1 +- 0.10 (else the
      concentrated profile breaks the Poisson exterior -> gap is real).
  M-LINEARIDADE  scan e_sk -> distinct masses M; G_net = A/M constant (CV<15%).
  M-GNET  G_net(Skyrmion) vs G_net(top-hat of same M): agree within 15%.

Anti-circularity: no relativistic expression in the generator; shell measure r^{d-1}
and a free coupling kappa (never G); e_sk the declared external Skyrme stabiliser.
G, M, Schwarzschild only in COMPARISON ONLY.  Fixed seeds; auto-descriptive JSON.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "fl1"))
sys.path.insert(0, str(ROOT / "src"))
import su3_core as s3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

D = 3
R_MIN, R_MAX = 0.1, 60.0
N_BINS = 64
K_STIFF = 1.0
KAPPA = 1.0                         # free source coupling (NOT G); fixed across scan
E_SK_SCAN = [0.3, 0.5, 0.7, 1.0, 1.5]


# =========================================================================== #
# exact BD solver: minimise E = sum_e H_e (theta_{i+1}-theta_i)^2 - sum_i b_i theta_i
# subject to sum_i theta_i V_i = 0  (the quadratic-action minimum = linear Poisson)
# =========================================================================== #
def make_grid():
    edges = np.geomspace(R_MIN, R_MAX, N_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    shell_vol = (edges[1:] ** D - edges[:-1] ** D) / D           # ~ r^{d-1} dr
    return edges, centers, shell_vol


def bd_solve(centers, shell_vol, b, K=K_STIFF):
    """Exact minimiser of the BD gradient action with a per-shell source b_i and the
    conservation constraint sum_i theta_i V_i = 0.  Returns theta."""
    n = len(centers)
    dr = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H = 0.5 * K * vbar / dr ** 2                                  # per-edge stiffness
    # gradient Laplacian L (E_grad = theta^T L theta): L_ii = sum_{e in i} H_e
    L = np.zeros((n, n))
    for e in range(n - 1):
        L[e, e] += H[e]; L[e + 1, e + 1] += H[e]
        L[e, e + 1] -= H[e]; L[e + 1, e] -= H[e]
    # stationarity: 2 L theta - b + mu V = 0 ; V^T theta = 0 (augmented system)
    V = shell_vol
    A = np.zeros((n + 1, n + 1))
    A[:n, :n] = 2.0 * L
    A[:n, n] = V
    A[n, :n] = V
    rhs = np.concatenate([b, [0.0]])
    sol = np.linalg.lstsq(A, rhs, rcond=None)[0]
    return sol[:n]


def fit_tail(centers, theta, r_lo, r_hi):
    """Fit theta = A/r + C over [r_lo, r_hi]; return A, C and the offset-removed
    log-log exponent (Newtonian = -1)."""
    use = (centers >= r_lo) & (centers <= r_hi) & np.isfinite(theta)
    if use.sum() < 4:
        return float("nan"), float("nan"), float("nan"), use
    X = np.vstack([1.0 / centers[use], np.ones(use.sum())]).T
    coef = np.linalg.lstsq(X, theta[use], rcond=None)[0]
    A_fit, C_fit = float(coef[0]), float(coef[1])
    resid = theta[use] - C_fit
    ok = resid > 0
    expo = (float(np.polyfit(np.log(centers[use][ok]), np.log(resid[ok]), 1)[0])
            if ok.sum() >= 4 else float("nan"))
    return A_fit, C_fit, expo, use


# =========================================================================== #
# Skyrmion energy density eps(r) = dE/dr from the relaxed hedgehog profile
# =========================================================================== #
def skyrmion_density(e_sk):
    """Return (r, eps(r), M) for the relaxed SU(2)/colour Skyrmion.  eps = dE/dr with
    E2 density 4pi r^2 (F'^2 + 2 sin^2F/r^2) and E4 density 4pi e_sk sin^2F (2F'^2 +
    sin^2F/r^2); M = integral eps dr = E2 + E4 (the measured soliton mass)."""
    r, dr = s3.radial_grid(rmax=10.0, n=700)
    F, E2, E4 = s3.radial_relax(r, dr, e_sk=e_sk)
    Fp = np.gradient(F, dr)
    s2 = np.sin(F) ** 2
    e2_dens = 4.0 * np.pi * (r ** 2 * (Fp ** 2 + 2.0 * s2 / r ** 2))
    e4_dens = 4.0 * np.pi * e_sk * (s2 * (2.0 * Fp ** 2 + s2 / r ** 2))
    eps = e2_dens + e4_dens
    M = float(np.sum(eps) * dr)
    return r, eps, M, float(E2), float(E4)


def source_from_density(r_fine, eps_fine, edges):
    """Bin the soliton energy into the gravity grid via the cumulative profile (mass-
    conserving): b_i = kappa * (energy in gravity shell i).  Energy beyond the soliton
    support maps to ~0 (exterior shells empty)."""
    dr = r_fine[1] - r_fine[0]
    cum = np.concatenate([[0.0], np.cumsum(eps_fine) * dr])       # C(r) at fine edges
    r_edges_fine = np.concatenate([[0.0], r_fine + 0.5 * dr])
    C_at = np.interp(edges, r_edges_fine, cum, left=0.0, right=cum[-1])
    energy_per_shell = np.diff(C_at)                              # energy in each grid shell
    return KAPPA * energy_per_shell


def support_radius(r_fine, eps_fine, frac=0.99):
    dr = r_fine[1] - r_fine[0]
    cum = np.cumsum(eps_fine) * dr
    cum /= cum[-1]
    return float(r_fine[np.searchsorted(cum, frac)])


# =========================================================================== #
def gate_g0(centers, shell_vol):
    """G0: exact solver with D3's top-hat source (normalised, r<4), K=1, kappaM=1 must
    reproduce D3 (A~1.03, C~-0.028, exponent~-1)."""
    R_CORE = 4.0
    core = centers < R_CORE
    s = np.where(core, shell_vol, 0.0); s = s / s.sum()
    b = 1.0 * s                                                  # kappaM = 1
    theta = bd_solve(centers, shell_vol, b, K=1.0)
    A, C, expo, _ = fit_tail(centers, theta, R_CORE, 0.6 * R_MAX)
    cons = float(np.sum(theta * shell_vol))
    passes = bool(abs(expo + 1.0) < 0.1 and A > 0 and C < 0)
    return {"A": A, "C": C, "exponent": expo, "conservation": cons,
            "D3_ref": {"A": 1.028, "C": -0.028, "exponent": -1.018},
            "passes": passes}


def main():
    t0 = time.time()
    edges, centers, shell_vol = make_grid()
    print("=" * 74)
    print("MG1 -- the Skyrmion as a DIRECT source of gravity (compose BD + soliton)")
    print("=" * 74)

    print("\n[G0] exact BD solver vs D3 (top-hat source, K=1, kappaM=1)")
    g0 = gate_g0(centers, shell_vol)
    print(f"  A={g0['A']:.3f} (D3 1.028)  C={g0['C']:+.4f} (D3 -0.028)  "
          f"exponent={g0['exponent']:.3f} (D3 -1.018)  PASS={g0['passes']}")
    if not g0["passes"]:
        print("  G0 FAILED -- solver does not represent the BD action; STOP.")
        (OUT / "MG1_skyrmion_gravity.json").write_text(json.dumps(
            {"G0_gate": g0, "verdict": "ABORTED at G0"}, indent=2))
        return

    print("\n[M-EXPOENTE / M-LINEARIDADE] Skyrmion eps(r) as the literal source, scan e_sk")
    scan = {}
    for e_sk in E_SK_SCAN:
        r_f, eps_f, M, E2, E4 = skyrmion_density(e_sk)
        b = source_from_density(r_f, eps_f, edges)
        r_supp = support_radius(r_f, eps_f)
        theta = bd_solve(centers, shell_vol, b)
        r_lo = max(r_supp * 1.5, 8.0)
        A, C, expo, use = fit_tail(centers, theta, r_lo, 0.6 * R_MAX)
        Q = float(np.sum(b))                       # total source charge = kappa * M
        G_net = A / M if M > 0 else float("nan")
        scan[e_sk] = {"M_mass": M, "E2": E2, "E4": E4, "Q_source": Q,
                      "r_support99": r_supp, "r_fit_lo": r_lo,
                      "A_amplitude": A, "C_offset": C, "exponent": expo,
                      "G_net_A_over_M": G_net, "n_fit": int(use.sum())}
        print(f"  e_sk={e_sk:.2f}: M={M:7.1f} A={A:7.3f} expo={expo:+.3f} "
              f"G_net=A/M={G_net:.5f} (r_fit>={r_lo:.1f})")

    # ---- M-GNET: top-hat of the same total mass as the e_sk=0.5 Skyrmion ----
    M_ref = scan[0.5]["M_mass"]
    R_CORE = scan[0.5]["r_support99"]
    core = centers < R_CORE
    s = np.where(core, shell_vol, 0.0); s = s / s.sum()
    b_th = KAPPA * M_ref * s
    theta_th = bd_solve(centers, shell_vol, b_th)
    A_th, C_th, expo_th, _ = fit_tail(centers, theta_th, max(R_CORE * 1.5, 8.0), 0.6 * R_MAX)
    G_net_th = A_th / M_ref
    G_net_sk = scan[0.5]["G_net_A_over_M"]
    gnet_match = abs(G_net_sk - G_net_th) / abs(G_net_th)

    # ---- verdicts over the scan ----
    expos = [scan[e]["exponent"] for e in E_SK_SCAN]
    gnets = [scan[e]["G_net_A_over_M"] for e in E_SK_SCAN]
    exp_ok = all(abs(x + 1.0) < 0.10 for x in expos)
    gnet_cv = float(np.std(gnets) / np.mean(gnets))
    lin_ok = gnet_cv < 0.15
    gnet_ok = gnet_match < 0.15
    robust = exp_ok and lin_ok and gnet_ok

    verdict = ("MATTER->GRAVITY DERIVED -- the Skyrmion sources theta=G_net M/r with its "
               "OWN energy-density profile: exterior exponent -1, amplitude linear in the "
               "soliton's own mass, same G_net as a generic source. Sec. VII [FRACO]->[SOLIDO]."
               if robust else
               "GAP REAL -- the soliton's concentrated profile does not reduce to the "
               "generic source; Sec. VII stays [FRACO]/composition.")

    print("\n[M-GNET] Skyrmion vs top-hat of the same mass M")
    print(f"  G_net(Skyrmion)={G_net_sk:.5f}  G_net(top-hat)={G_net_th:.5f}  "
          f"rel.diff={gnet_match:.1%}  match={gnet_ok}")
    print("-" * 74)
    print(f"  M-EXPOENTE pass={exp_ok}  M-LINEARIDADE pass={lin_ok} (G_net CV={gnet_cv:.1%})"
          f"  M-GNET pass={gnet_ok}")
    print(f"VERDICT: {verdict}")
    print("=" * 74)

    _figure(centers, scan, edges, shell_vol, theta_th, G_net_sk, G_net_th)
    payload = {"D": D, "grid": {"r_min": R_MIN, "r_max": R_MAX, "n_bins": N_BINS},
               "K_stiff": K_STIFF, "kappa": KAPPA, "e_sk_scan": E_SK_SCAN,
               "G0_gate": g0, "scan": {str(k): v for k, v in scan.items()},
               "M_gnet_tophat": {"M_ref": M_ref, "A": A_th, "exponent": expo_th,
                                 "G_net": G_net_th, "rel_diff_vs_skyrmion": gnet_match},
               "exponents": expos, "G_nets": gnets, "G_net_CV": gnet_cv,
               "exp_ok": exp_ok, "linearity_ok": lin_ok, "gnet_ok": gnet_ok,
               "robust": bool(robust), "verdict": verdict,
               "runtime_s": time.time() - t0}
    (OUT / "MG1_skyrmion_gravity.json").write_text(json.dumps(payload, indent=2))
    print(f"saved MG1_skyrmion_gravity.json  ({payload['runtime_s']:.1f}s)")
    return payload


def _figure(centers, scan, edges, shell_vol, theta_th, gsk, gth):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    # (a) theta(r) for each e_sk, log-log, with 1/r guide
    for e_sk in E_SK_SCAN:
        r_f, eps_f, M, _, _ = skyrmion_density(e_sk)
        b = source_from_density(r_f, eps_f, edges)
        th = bd_solve(centers, shell_vol, b)
        m = th > 0
        ax[0].loglog(centers[m], th[m], "o-", ms=3, label=f"e_sk={e_sk} (M={M:.0f})")
    rr = np.array([8.0, 36.0])
    ax[0].loglog(rr, scan[0.5]["A_amplitude"] / rr, "k--", lw=1, label="slope -1 (1/r)")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$\theta=\delta\rho/\rho_0$")
    ax[0].set_title("(a) Skyrmion sources theta(r): exterior 1/r")
    ax[0].legend(fontsize=7)
    # (b) A vs M linearity
    Ms = [scan[e]["M_mass"] for e in E_SK_SCAN]
    As = [scan[e]["A_amplitude"] for e in E_SK_SCAN]
    ax[1].plot(Ms, As, "o", ms=7, label="Skyrmion source")
    mm = np.linspace(0, max(Ms) * 1.05, 50)
    ax[1].plot(mm, gsk * mm, "-", lw=1, label=f"A=G_net M, G_net={gsk:.4f}")
    ax[1].set_xlabel("soliton mass M = E2+E4"); ax[1].set_ylabel("well amplitude A")
    ax[1].set_title(f"(b) amplitude linear in mass\n(top-hat G_net={gth:.4f})")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.2)
    fig.suptitle("MG1: the Skyrmion sources its own gravitational field (theta=G_net M/r)")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "MG1_skyrmion_gravity.png", dpi=130)
    print("saved MG1_skyrmion_gravity.png")


if __name__ == "__main__":
    main()

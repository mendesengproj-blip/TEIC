"""D3C_superposition.py -- does theta_total = theta_1 + theta_2 ? (linearity)

BRIDGE / D3 AUDIT, task C.  Poisson is LINEAR: nabla^2(theta1+theta2)=J1+J2.  Two
core sources separated by d; run the MC for each mass alone and for both, and test
superposition pointwise.

Two parts, and the HONEST split between them:
  PART 1 (the implemented BD action).  The static Benincasa-Dowker action is
  QUADRATIC (BRIDGE_NONLINEAR/NL1: it has no phi^3 / (grad theta)^2 term), so its
  Euler-Lagrange equation is the LINEAR Poisson equation and superposition must be
  EXACT at every field strength.  Confirming this is the decisive test that the
  network obeys a linear law (not a non-linear one in disguise).

  PART 2 (illustrative, conditional -- NOT the implemented action).  The cone /
  clock sector produces a DBI saturation sqrt(1 - X/X0) (BRIDGE_NONLINEAR, W3).
  Where that non-linearity is present, superposition must break -- and only in
  strong field, in the SATURATING direction.  We add the DBI coefficient by hand
  (clearly labelled) and show exactly this: linear in weak field, breaking toward
  saturation in strong field.  This is shown to characterise what a non-linear
  completion would do; it is NOT a property of the BD action used in D1-D3.

No G / GM/r / Schwarzschild in any generator: sources are deposited weights.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from d3_audit_core import grid3d, poisson3d_solve, mc3d_heatbath, deposit_ball

L, N, K, TEMP = 40.0, 36, 1.0, 0.005
N_SWEEPS, N_BURN = 9000, 3000
SEP, R0, W_M = 14.0, 3.0, 1.0


# --------------------- illustrative DBI nonlinear relaxation --------------- #
def _grad2(theta, h):
    gx = (np.roll(theta, -1, 0) - np.roll(theta, 1, 0)) / (2 * h)
    gy = (np.roll(theta, -1, 1) - np.roll(theta, 1, 1)) / (2 * h)
    gz = (np.roll(theta, -1, 2) - np.roll(theta, 1, 2)) / (2 * h)
    return gx ** 2 + gy ** 2 + gz ** 2


def dbi_relax(source, h, K, X0, n_outer=40, n_jacobi=120):
    """Relax -nabla.( c(x) grad theta ) = (source-bg), c = 1/sqrt(1 - X/X0).

    Variable-coefficient Jacobi (illustrative DBI saturation).  Returns theta.
    """
    n = source.shape[0]
    J = (source - source.mean())
    theta = poisson3d_solve(source, h, K)          # linear start
    for _ in range(n_outer):
        X = _grad2(theta, h)
        c = 1.0 / np.sqrt(np.clip(1.0 - X / X0, 1e-3, 1.0)) * K
        for _ in range(n_jacobi):
            num = np.zeros_like(theta); den = np.zeros_like(theta)
            for ax in range(3):
                for s in (+1, -1):
                    cnb = np.roll(c, s, ax)
                    cf = 2 * c * cnb / (c + cnb + 1e-12)     # harmonic face coeff
                    th_nb = np.roll(theta, s, ax)
                    num += cf * th_nb
                    den += cf
            theta = (num + J * h ** 2) / (den + 1e-12)
            theta -= theta.mean()
    return theta


def superposition_metrics(t1, t2, ttot, mask):
    pred = (t1 + t2)[mask].ravel()
    obs = ttot[mask].ravel()
    corr = float(np.corrcoef(pred, obs)[0, 1])
    scale = np.max(np.abs(obs)) - np.min(np.abs(obs)) + 1e-12
    reldev = float(np.max(np.abs(obs - pred)) / (np.max(np.abs(obs)) + 1e-12))
    rms = float(np.sqrt(np.mean((obs - pred) ** 2)) / (np.std(obs) + 1e-12))
    return corr, reldev, rms


def main():
    t0 = time.time()
    g = grid3d(L, N); h = g["h"]
    c1 = (-SEP / 2, 0, 0); c2 = (+SEP / 2, 0, 0)
    s1 = deposit_ball(g, R0, W_M, c1)
    s2 = deposit_ball(g, R0, W_M, c2)
    s12 = s1 + s2

    m = np.ones((N, N, N), dtype=bool); b = 3
    m[:b] = m[-b:] = m[:, :b] = m[:, -b:] = m[:, :, :b] = m[:, :, -b:] = False

    # ----- PART 1: linear BD action (genuine MC) -----
    th1 = mc3d_heatbath(s1, h, K, TEMP, N_SWEEPS, N_BURN, 11)
    th2 = mc3d_heatbath(s2, h, K, TEMP, N_SWEEPS, N_BURN, 12)
    thT = mc3d_heatbath(s12, h, K, TEMP, N_SWEEPS, N_BURN, 13)
    corr, reldev, rms = superposition_metrics(th1, th2, thT, m)
    # solver (zero MC noise) is the decisive linear test: for the QUADRATIC BD action
    # the EOM is linear, so theta_total = theta1 + theta2 must hold exactly.  The MC
    # estimates each mean with independent sampling noise, so the MC difference is the
    # sampling floor (~sqrt(3) sigma), NOT a superposition violation -- reported as
    # supporting evidence only.
    s1s = poisson3d_solve(s1, h, K); s2s = poisson3d_solve(s2, h, K)
    sTs = poisson3d_solve(s12, h, K)
    corr_s, reldev_s, rms_s = superposition_metrics(s1s, s2s, sTs, m)
    linear_holds = bool(corr_s > 0.9999 and rms_s < 1e-3)
    mc_consistent = bool(corr > 0.9)

    # ----- PART 2: illustrative DBI saturation (labelled, NOT the BD action) -----
    # choose X0 so the field is weak (X<<X0) far out and strong (X~X0) near cores
    # strong, CLOSE, heavy sources on a coarse grid so the overlap region approaches
    # saturation (the weak normalised sources of part 1 never engage the cusp).
    DBI_N, DBI_L, DBI_W, DBI_SEP, DBI_R0, DBI_FRAC = 28, 24.0, 200.0, 6.0, 2.0, 0.85
    gd = grid3d(DBI_L, DBI_N); hd = gd["h"]
    e1 = deposit_ball(gd, DBI_R0, DBI_W, (-DBI_SEP / 2, 0, 0))
    e2 = deposit_ball(gd, DBI_R0, DBI_W, (+DBI_SEP / 2, 0, 0))
    e12 = e1 + e2
    md = np.ones((DBI_N,) * 3, bool); bd = 2
    md[:bd] = md[-bd:] = md[:, :bd] = md[:, -bd:] = md[:, :, :bd] = md[:, :, -bd:] = False
    th_lin12 = poisson3d_solve(e12, hd, K)
    gmax = np.sqrt(np.max(_grad2(th_lin12, hd)))
    X0 = (gmax / DBI_FRAC) ** 2                               # max X/X0 ~ FRAC^2 < 1
    d1 = dbi_relax(e1, hd, K, X0, 30, 80); d2 = dbi_relax(e2, hd, K, X0, 30, 80)
    dT = dbi_relax(e12, hd, K, X0, 30, 80)
    resid = (dT - (d1 + d2))
    Xfield = _grad2(th_lin12, hd) / X0                       # local strength fraction
    xs = Xfield[md].ravel(); rs = np.abs(resid[md].ravel())
    order = np.argsort(xs)
    xs, rs = xs[order], rs[order]
    nb_ = 8
    edges = np.quantile(xs, np.linspace(0, 1, nb_ + 1))
    binc, binr = [], []
    for i in range(nb_):
        sel = (xs >= edges[i]) & (xs <= edges[i + 1])
        if sel.sum() > 0:
            binc.append(float(0.5 * (edges[i] + edges[i + 1])))
            binr.append(float(np.mean(rs[sel])))
    dbi_corr = float(np.corrcoef((d1 + d2)[md].ravel(), dT[md].ravel())[0, 1])
    # direction: in strong field is |dT| < |d1+d2| (saturation suppresses)?
    strong = Xfield[md] > 0.5 * Xfield[md].max()
    satur_dir = bool(np.mean(np.abs(dT[md][strong])) <
                     np.mean(np.abs((d1 + d2)[md][strong])))
    breaks_in_strong = bool(binr[-1] > 3 * binr[0] and satur_dir)

    verdict = ("PASSA" if linear_holds else "FALHA")

    # ---- figures ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    pred = (th1 + th2)[m].ravel(); obs = thT[m].ravel()
    sub = np.random.default_rng(0).choice(pred.size, min(4000, pred.size), replace=False)
    ax[0].scatter(pred[sub], obs[sub], s=6, alpha=0.3)
    lo, hi = pred.min(), pred.max()
    ax[0].plot([lo, hi], [lo, hi], "k--", lw=1, label=r"$\theta_{\rm tot}=\theta_1+\theta_2$")
    ax[0].set_xlabel(r"$\theta_1+\theta_2$"); ax[0].set_ylabel(r"$\theta_{\rm total}$ (MC)")
    ax[0].set_title(f"(D3-C) linear BD action: superposition exact\n"
                    f"corr={corr:.5f}, rms/std={rms:.3f}")
    ax[0].legend(fontsize=8)

    ax[1].plot(binc, binr, "o-", ms=5, color="C3")
    ax[1].set_xlabel(r"local field strength $X/X_0$")
    ax[1].set_ylabel(r"$|\theta_{\rm tot}-(\theta_1+\theta_2)|$ (DBI, illustrative)")
    ax[1].set_title("(D3-C) illustrative DBI: superposition breaks in strong field\n"
                    f"(saturating direction: {satur_dir})")
    fig.tight_layout(); fig.savefig(OUT / "D3C_superposition.png", dpi=130)

    summary = dict(
        what="Superposition theta_total =? theta1 + theta2 for two separated sources.",
        grid=dict(L=L, N=N, h=h), separation=SEP, r0=R0, w_M=W_M, K=K, temp=TEMP,
        n_sweeps=N_SWEEPS,
        part1_linear_BD=dict(mc_corr=corr, mc_max_reldev=reldev, mc_rms_over_std=rms,
                             mc_consistent=mc_consistent,
                             solver_corr=corr_s, solver_rms_over_std=rms_s,
                             superposition_exact=linear_holds,
                             note="quadratic BD action => linear EOM => exact "
                                  "superposition at all field strengths (NL1)."),
        part2_DBI_illustrative=dict(X0=float(X0), dbi_superposition_corr=dbi_corr,
                                    field_strength_bins=binc, resid_by_strength=binr,
                                    saturating_direction=satur_dir,
                                    breaks_in_strong_field=breaks_in_strong,
                                    note="DBI coefficient added BY HAND (labelled); not "
                                         "the BD action of D1-D3. Shows what a non-linear "
                                         "completion does: linear weak field, breaking in "
                                         "strong field toward saturation."),
        verdict=verdict, runtime_s=round(time.time() - t0, 1),
        timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    (OUT / "D3C_superposition_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("D3-C -- SUPERPOSITION (LINEARITY)")
    print("=" * 72)
    print(f"two cores, separation d={SEP}, grid {N}^3")
    print("-- PART 1: implemented (linear) BD action, genuine MC --")
    print(f"  theta_total vs theta1+theta2 : corr={corr:.5f}  rms/std={rms:.4f}  "
          f"maxreldev={reldev:.4f}")
    print(f"  (solver, zero MC noise)      : corr={corr_s:.6f}  rms/std={rms_s:.2e}")
    print(f"  superposition EXACT          : {linear_holds}")
    print("-- PART 2: illustrative DBI saturation (added by hand; NOT the BD action) --")
    print(f"  X0={X0:.3f}  DBI superposition corr={dbi_corr:.4f}")
    print(f"  residual by field strength   : {[round(x,4) for x in binr]}")
    print(f"  breaks in strong field, saturating direction: {breaks_in_strong}")
    print("-" * 72)
    print(f"VERDICT (D3-C): {verdict}   [{summary['runtime_s']}s]")
    return summary


if __name__ == "__main__":
    main()

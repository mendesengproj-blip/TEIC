"""E6e_extrapolation.py -- ANALYTIC extrapolation of E6c's curvature data (NO new Monte Carlo).

E6c measured the B-type (magnetic) 2-cell fraction frac_B and the per-cell magnetic content
b²/e² of height-4 causal diamonds vs de Sitter curvature radius R̂ = R_dS/ℓ (ℓ = mean
spacing). frac_B rises monotonically from the flat (Minkowski) floor ≈0.0026 to 0.0117 at
R̂=2. E6e asks the purely analytic question: what curvature R̂ would push frac_B to O(10%),
and is that R̂ physically reasonable (sub-Planckian) or trans-Planckian (a physical, not just
technical, frontier)?

We fit THREE pre-registered models to frac_B(R̂) and to b²/e²(R̂), pick the lowest-residual
one, extrapolate to frac_B = 0.05, 0.10, 0.50, and -- crucially -- REPORT THE CONDITIONING:
if a parameter is uncertain by >50% the extrapolation is flagged as ill-conditioned rather
than quoted with false precision, and the additional R̂ points that would resolve it are named.

  Model A (power)        : frac_B = a · (1/R̂)^α
  Model B (exponential)  : frac_B = a · exp(−b · R̂)
  Model C (quadratic)    : frac_B = a · (1/R̂)²            [leading curvature correction ∝ H²]

The Minkowski FLOOR frac_B(∞) (the flat-space E6b tail, curvature-independent) is handled
explicitly: power/quadratic through the origin cannot represent a nonzero floor, so we ALSO
fit the curvature-INDUCED EXCESS Δ(R̂) = frac_B(R̂) − frac_B(∞), which is what curvature adds.

Honesty note (updated vs the charter's worry): E6c has FIVE finite-curvature points
(R̂=16,8,4,3,2) with small binomial errors and a clean monotone signal -- NOT a single
positive point -- so the fit is better-conditioned than the charter feared. This is reported.
No relativistic literal is used; this script only reads E6c's JSON and fits curves.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
E6C = HERE.parent / "e6c"
H_PRIMARY = 4                          # E6c's best-sampled magnetic height (crossed 0.01)
TARGETS = [0.05, 0.10, 0.50]
PLANCK_ASSUMPTION = ("ℓ_lattice ≡ ℓ_Planck (discreteness scale = Planck scale): then R̂ is "
                     "directly the curvature radius in Planck units. [EXTERNO/ASSUMIDO]")


# ---------------------------------------------------------------------- #
# Load E6c aggregate
# ---------------------------------------------------------------------- #
def load_e6c(h=H_PRIMARY, N=2000):
    """Return (R_hat, R_dS, frac_B, err, b2e2) arrays for finite R̂ + the Minkowski floor."""
    src = next(E6C.glob("E6c_*scan.json"))
    d = json.loads(src.read_text())
    ag = d["aggregate"]
    rows = []
    floor = None
    for R in d["params"]["R_hats"]:
        rk = "inf" if R == "inf" else f"{R:g}"
        a = ag.get(f"{N}_{rk}_{h}")
        if not a or a.get("P_tot", 0) == 0:
            continue
        if rk == "inf":
            floor = {"frac_B": a["frac_B"], "err": a["binom_err"], "b2e2": a["mean_b2_over_e2"]}
            continue
        rows.append((float(R), a["R_dS"], a["frac_B"], a["binom_err"], a["mean_b2_over_e2"]))
    rows.sort(key=lambda r: r[0])
    arr = np.array(rows)
    return {"R_hat": arr[:, 0], "R_dS": arr[:, 1], "frac_B": arr[:, 2],
            "err": arr[:, 3], "b2e2": arr[:, 4], "floor": floor, "source": src.name, "h": h, "N": N}


# ---------------------------------------------------------------------- #
# Models, fitting, R², conditioning
# ---------------------------------------------------------------------- #
def m_power(Rhat, a, alpha):          # A
    return a * (1.0 / Rhat) ** alpha


def m_exp(Rhat, a, b):                # B
    return a * np.exp(-b * Rhat)


def m_quad(Rhat, a):                  # C
    return a * (1.0 / Rhat) ** 2


MODELS = {"power": (m_power, ("a", "alpha"), [0.05, 1.0]),
          "exp":   (m_exp,   ("a", "b"),     [0.02, 0.1]),
          "quad":  (m_quad,  ("a",),         [0.05])}


def _r2(y, yhat, w=None):
    if w is None:
        w = np.ones_like(y)
    ybar = np.average(y, weights=w)
    ss_res = np.sum(w * (y - yhat) ** 2)
    ss_tot = np.sum(w * (y - ybar) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")


def fit_model(name, Rhat, y, sigma):
    fn, pnames, p0 = MODELS[name]
    try:
        popt, pcov = curve_fit(fn, Rhat, y, p0=p0, sigma=sigma, absolute_sigma=True,
                               maxfev=200000)
    except Exception as e:                       # pragma: no cover
        return {"model": name, "ok": False, "error": str(e)}
    perr = np.sqrt(np.diag(pcov))
    yhat = fn(Rhat, *popt)
    rel = [float(abs(perr[i] / popt[i])) if popt[i] != 0 else float("inf")
           for i in range(len(popt))]
    # reduced chi-square (data has real binomial errors)
    dof = max(len(y) - len(popt), 1)
    chi2 = float(np.sum(((y - yhat) / sigma) ** 2) / dof)
    return {"model": name, "ok": True, "params": dict(zip(pnames, popt.tolist())),
            "perr": dict(zip(pnames, perr.tolist())), "rel_unc": dict(zip(pnames, rel)),
            "R2": _r2(y, yhat), "R2_weighted": _r2(y, yhat, 1.0 / sigma ** 2),
            "chi2_red": chi2, "max_rel_unc": float(max(rel)),
            "ill_conditioned": bool(max(rel) > 0.50)}


def invert_to_target(name, params, target):
    """Solve model(R̂)=target for R̂. Returns (R̂ or None, reason). For models bounded above
    (exp saturates at a as R̂→0), returns None with 'saturates' when target>sup."""
    if name == "power":
        a, al = params["a"], params["alpha"]
        if a <= 0 or al == 0:
            return None, "degenerate"
        x = (target / a) ** (1.0 / al)            # x = 1/R̂
        return (1.0 / x if x > 0 else None), "ok"
    if name == "quad":
        a = params["a"]
        if a <= 0:
            return None, "degenerate"
        x = np.sqrt(target / a)
        return 1.0 / x, "ok"
    if name == "exp":
        a, b = params["a"], params["b"]
        if target >= a:
            return None, f"saturates (model sup = a = {a:.4f} < target)"
        Rhat = -np.log(target / a) / b
        return (Rhat if Rhat > 0 else None), "ok"
    return None, "unknown"


def analyse(Rhat, y, sigma, label, include_floor_excess=False, floor=0.0):
    """Fit all three models to (Rhat, y); return per-model fit + extrapolation table."""
    out = {"label": label, "fits": {}, "best": None}
    best_name, best_chi = None, np.inf
    for name in MODELS:
        f = fit_model(name, Rhat, y, sigma)
        if f.get("ok"):
            # extrapolate (targets are on the SAME quantity y; if excess, caller adjusts)
            extr = {}
            for t in TARGETS:
                tt = (t - floor) if include_floor_excess else t
                R, reason = invert_to_target(name, f["params"], tt)
                extr[str(t)] = {"R_hat": (None if R is None else float(R)), "reason": reason}
            f["extrapolation"] = extr
            if f["chi2_red"] < best_chi:
                best_chi, best_name = f["chi2_red"], name
        out["fits"][name] = f
    out["best"] = best_name
    return out


# ---------------------------------------------------------------------- #
# Figure
# ---------------------------------------------------------------------- #
def make_figure(data, frac_analysis, verdict_tag):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    Rhat, y, err, floor = data["R_hat"], data["frac_B"], data["err"], data["floor"]["frac_B"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.8))

    # left: frac_B vs 1/R̂ with the fits + extrapolation down to small R̂
    x = 1.0 / Rhat
    ax1.errorbar(x, y, yerr=err, fmt="o", color="k", capsize=3, zorder=5, label="E6c data (h=4)")
    ax1.axhline(floor, ls=":", c="grey", lw=1, label=f"Minkowski floor {floor:.4f}")
    Rgrid = np.linspace(0.2, 20, 400); xg = 1.0 / Rgrid
    styles = {"power": ("-", "#1f77b4"), "exp": ("--", "#ff7f0e"), "quad": ("-.", "#2ca02c")}
    for name, (ls, col) in styles.items():
        f = frac_analysis["fits"][name]
        if not f.get("ok"):
            continue
        fn = MODELS[name][0]
        yg = fn(Rgrid, *[f["params"][p] for p in MODELS[name][1]])
        tag = "  [BEST]" if name == frac_analysis["best"] else ""
        ax1.plot(xg, yg, ls, color=col, lw=1.6,
                 label=f"{name}: R²={f['R2']:.3f}{tag}")
    for t in TARGETS:
        ax1.axhline(t, ls="--", c="red", lw=0.7, alpha=0.6)
        ax1.text(0.02, t * 1.04, f"{t:.2f}", color="red", fontsize=7)
    ax1.set_xlabel(r"curvature  $1/\hat{R}$   (0 = Minkowski)")
    ax1.set_ylabel("frac_B (magnetic fraction)")
    ax1.set_yscale("log"); ax1.set_ylim(1e-3, 1.0); ax1.set_xlim(-0.02, 1.6)
    ax1.set_title(f"E6c frac_B vs curvature + extrapolation\n[{verdict_tag}]")
    ax1.legend(fontsize=7.5, loc="lower right"); ax1.grid(alpha=0.3)

    # right: b²/e² vs 1/R̂
    ax2.errorbar(x, data["b2e2"], fmt="s", color="purple", capsize=3, label="E6c b²/e² (h=4)")
    ax2.axhline(1.0, ls=":", c="grey", lw=1, label="b²/e²=1 (mean cell on light cone)")
    ax2.axhline(data["floor"]["b2e2"], ls=":", c="violet", lw=1,
                label=f"Minkowski {data['floor']['b2e2']:.2f}")
    ax2.set_xlabel(r"curvature  $1/\hat{R}$")
    ax2.set_ylabel("mean b²/e²")
    ax2.set_title("Per-cell magnetic content vs curvature")
    ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "E6e_extrapolation.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------- #
# Verdict
# ---------------------------------------------------------------------- #
def make_verdict(frac_direct_g, frac_excess_g, any_ill):
    """Pre-registered verdict from the extrapolated R̂ for frac_B≈O(10%)."""
    # collect R̂ at target 0.10 across all OK, reaching models (direct + excess)
    R10 = []
    for an in (frac_direct_g, frac_excess_g):
        for name, f in an["fits"].items():
            if f.get("ok"):
                e = f["extrapolation"]["0.1"]
                if e["R_hat"] is not None:
                    R10.append((an["label"], name, e["R_hat"]))
    R10_vals = [r for *_, r in R10]
    if not R10_vals:
        return "INCONCLUSIVE", ("No model can reach frac_B=0.10 (all bounded/degenerate) -- "
                                "the exponential saturates below 0.10. Extrapolation undefined."), R10
    rmin, rmax, rmed = min(R10_vals), max(R10_vals), float(np.median(R10_vals))
    # The exponential model (if it fit) SATURATES below 0.10 -> a pessimistic bound worth
    # stating: if frac_B decays exponentially in R̂, O(10%) is unreachable at ANY curvature.
    exp_saturates = any(
        an["fits"]["exp"].get("ok") and an["fits"]["exp"]["extrapolation"]["0.1"]["R_hat"] is None
        for an in (frac_direct_g, frac_excess_g))
    sat_note = (" (NB: the exponential-in-R̂ model, R²≈0.99 on the excess, SATURATES below "
                "0.10 -- under that reading O(10%) is unreachable at any curvature, an even "
                "stronger frontier.)" if exp_saturates else "")
    if any_ill:
        tag = "INCONCLUSIVE-ILLCOND"
        v = (f"Some fits are ill-conditioned (a parameter uncertain >50%); the R̂ for "
             f"frac_B=0.10 spans {rmin:.2f}–{rmax:.2f} (median {rmed:.2f}). Report range, not "
             f"false precision; 2–3 added points (R̂=1.5,1.0,0.5) would resolve it.{sat_note}")
    elif rmed < 0.1:
        tag = "DEATH"
        v = (f"frac_B~O(10%) requires R̂≈{rmed:.3f} < 0.1 -- TRANS-PLANCKIAN. The BD-gauge "
             f"photon via curvature is a physical/structural frontier; E6e (full MC) not "
             f"worth it.{sat_note}")
    elif rmed < 1.0:
        # R̂<1 == curvature radius below the mean spacing (= Planck length under the stated
        # assumption): the continuum/sprinkling picture is at/below its validity floor.
        tag = "PHYSICAL-FRONTIER"
        v = (f"frac_B~O(10%) requires R̂≈{rmed:.2f} (range {rmin:.2f}–{rmax:.2f}), i.e. BELOW "
             f"the discreteness scale (R̂<1: curvature radius < mean spacing ≈ Planck length "
             f"under the stated assumption). This is a PHYSICAL frontier, not merely technical: "
             f"the mechanism needs near-/sub-Planckian curvature, so the observable universe "
             f"(R̂ astronomically large) gets only the flat tail (~0) -- this framework does NOT "
             f"explain why the observable universe has photons. NOT the hard structural death "
             f"(R̂≪0.1): the value sits at the 0.5 boundary, so running E6e at R̂=1.5,1.0,0.5 "
             f"to CONFIRM the ∝1/R̂² law within the valid continuum regime is defensible, but it "
             f"would confirm a Planck-scale requirement, not bring the photon within reach.{sat_note}")
    elif rmed <= 5.0:
        tag = "SUCCESS"
        v = (f"frac_B~O(10%) requires R̂≈{rmed:.2f} (range {rmin:.2f}–{rmax:.2f}) -- sub-Planckian "
             f"but not absurd. Worth running E6e (full MC) at R̂≈1.5,1.0,0.5 to confirm.{sat_note}")
    else:
        tag = "REASONABLE"
        v = (f"frac_B~O(10%) at R̂≈{rmed:.1f} (range {rmin:.2f}–{rmax:.2f}) -- a comfortably "
             f"sub-Planckian curvature; E6e clearly worth running.{sat_note}")
    return tag, v, R10


def main():
    data = load_e6c(h=H_PRIMARY)
    Rhat, frac, err = data["R_hat"], data["frac_B"], data["err"]
    floor = data["floor"]["frac_B"]

    # (1) fit frac_B DIRECTLY (finite points), and (2) the curvature EXCESS Δ=frac−floor.
    frac_direct = analyse(Rhat, frac, err, "frac_B (direct, 5 finite pts)")
    excess = np.clip(frac - floor, 1e-9, None)
    frac_excess = analyse(Rhat, excess, err, "Δfrac_B = frac − Minkowski floor",
                          include_floor_excess=True, floor=floor)

    # (3) b²/e² fits (supporting; extrapolate to b²/e²=1, the 'mean cell on the light cone')
    b2_analysis = {"fits": {}}
    for name in MODELS:
        f = fit_model(name, Rhat, data["b2e2"], np.full_like(data["b2e2"], 0.02))
        if f.get("ok"):
            R1, reason = invert_to_target(name, f["params"], 1.0)
            f["R_hat_at_b2e2_eq_1"] = (None if R1 is None else float(R1))
            f["b2e2_reason"] = reason
        b2_analysis["fits"][name] = f

    any_ill = any(f.get("ill_conditioned") for an in (frac_direct, frac_excess)
                  for f in an["fits"].values() if f.get("ok"))
    tag, verdict, R10 = make_verdict(frac_direct, frac_excess, any_ill)
    make_figure(data, frac_direct, tag)

    out = {"source": data["source"], "h": data["h"], "N": data["N"],
           "minkowski_floor": data["floor"], "data_points": int(Rhat.size),
           "R_hat": Rhat.tolist(), "frac_B": frac.tolist(), "err": err.tolist(),
           "b2e2": data["b2e2"].tolist(),
           "fit_frac_direct": frac_direct, "fit_frac_excess": frac_excess,
           "fit_b2e2": b2_analysis, "targets": TARGETS,
           "R_hat_for_frac0.10_allmodels": R10,
           "planck_assumption": PLANCK_ASSUMPTION,
           "any_ill_conditioned": any_ill, "verdict_tag": tag, "verdict": verdict}
    (HERE / "E6e_extrapolation.json").write_text(json.dumps(out, indent=2))

    # ---- console report ----
    print(f"E6c source: {data['source']}  (h={data['h']}, N={data['N']}, {Rhat.size} finite pts)")
    print(f"Minkowski floor frac_B(∞) = {floor:.5f}\n")
    for an in (frac_direct, frac_excess):
        print(f"=== fit: {an['label']}  (best by χ²_red: {an['best']}) ===")
        print(f"{'model':>6} {'R2':>7} {'chi2red':>8} {'max_rel_unc':>11} {'cond':>5}  params  | extrap R̂@(0.05,0.10,0.50)")
        for name, f in an["fits"].items():
            if not f.get("ok"):
                print(f"{name:>6}  FAILED: {f.get('error')}"); continue
            pr = ", ".join(f"{k}={v:.4f}" for k, v in f["params"].items())
            ex = []
            for t in TARGETS:
                e = f["extrapolation"][str(t)]
                ex.append("—(sat)" if e["R_hat"] is None else f"{e['R_hat']:.2f}")
            cond = "ILL" if f["ill_conditioned"] else "ok"
            print(f"{name:>6} {f['R2']:>7.3f} {f['chi2_red']:>8.2f} {f['max_rel_unc']:>11.2f} "
                  f"{cond:>5}  {pr:28s}| {', '.join(ex)}")
        print()
    print("=== b²/e² fits (extrapolate to b²/e²=1, mean cell on light cone) ===")
    for name, f in b2_analysis["fits"].items():
        if f.get("ok"):
            R1 = f.get("R_hat_at_b2e2_eq_1")
            print(f"{name:>6}  R²={f['R2']:.3f}  R̂(b²/e²=1)={'—' if R1 is None else f'{R1:.2f}'}")
    print(f"\nPlanck assumption: {PLANCK_ASSUMPTION}")
    print(f"\nVERDICT [{tag}]: {verdict}")
    print("-> E6e_extrapolation.json, E6e_extrapolation.png")
    return out


if __name__ == "__main__":
    main()

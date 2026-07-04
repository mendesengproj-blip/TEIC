"""E1V_gate.py -- MANDATORY engineering gate for E1_ORIENTATION.

Validate the spin-model Monte-Carlo engine (orientation_core) on the REGULAR
d=1,2,3 lattices where the literature anchors live, using exactly the machinery
that will later run on the causal network.  The gate must reproduce:

  1D  XY & O(3)  : NO long-range order at any J>0 (Mermin-Wagner).  C(r) decays
                   exponentially.  XY is checked QUANTITATIVELY against the exact
                   transfer-matrix result  C(r) = (I1(J)/I0(J))**r.
  2D  XY         : Kosterlitz-Thouless.  C(r) crosses from exponential (small J,
                   hot) to power-law r^{-eta} (large J, cold) near J_KT ~ 1.12.
      O(3)       : NO long-range order (Mermin-Wagner); C(r) stays exponential.
  3D  XY & O(3)  : long-range order for J > J_c (XY J_c~0.454, O(3) J_c~0.693).
                   C(r) -> C0 > 0 (fit winner = const) and the order parameter m
                   lifts off the disordered ~1/sqrt(N) baseline.

If the engine fails these, the gate FAILS and the physical measurement (E1-1)
does not proceed.  Anti-circularity: no critical temperature is inserted into the
generator; the literature J_c values appear only in this COMPARISON-ONLY scoring.
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
SEEDS = (0, 1, 2)

# ----- literature anchors (COMPARISON ONLY) -------------------------------- #
J_KT_2D = 1.12       # 2D XY Kosterlitz-Thouless coupling (T_KT ~ 0.893)
JC_3D = {"U(1)": 0.454, "O(3)": 0.693}   # 3D ordering couplings

# ----- run sizes ----------------------------------------------------------- #
CFG = {
    "1D": dict(builder=lambda: oc.ring_1d(4000), r_max=24,
               n_burn=1200, n_meas=250, n_sources=60,
               Js=[0.5, 1.0, 2.0, 4.0]),
    "2D": dict(builder=lambda: oc.lattice_periodic((64, 64)), r_max=20,
               n_burn=2000, n_meas=300, n_sources=48,
               Js=[0.6, 0.9, 1.1, 1.4, 2.0]),
    "3D": dict(builder=lambda: oc.lattice_periodic((16, 16, 16)), r_max=10,
               n_burn=2000, n_meas=300, n_sources=48,
               Js_by_model={"U(1)": [0.3, 0.4, 0.454, 0.55, 0.7, 1.0],
                            "O(3)": [0.45, 0.6, 0.693, 0.85, 1.1, 1.5]}),
}


def run_case(dim, model_name):
    cfg = CFG[dim]
    Js = cfg.get("Js_by_model", {}).get(model_name, cfg.get("Js"))
    Model = oc.MODELS[model_name]
    rows = []
    curves = {}
    for J in Js:
        Cs, ms, steps = [], [], []
        for seed in SEEDS:
            g = cfg["builder"]()
            m = Model(g, J=J, seed=100 * seed + 7)
            r, C, w, m_series = oc.measure_correlation(
                m, n_burn=cfg["n_burn"], n_meas=cfg["n_meas"],
                n_sources=cfg["n_sources"], r_max=cfg["r_max"])
            Cs.append(C)
            ms.append(float(np.mean(m_series)))
            steps.append(m.step)
        Cs = np.array(Cs)
        Cmean = Cs.mean(axis=0)
        Cstd = Cs.std(axis=0)
        fit = oc.fit_forms(r, Cmean, sigma=Cstd, r_lo=2)
        m_mean, m_err = float(np.mean(ms)), float(np.std(ms))
        rows.append({"J": J, "r": r.tolist(), "C": Cmean.tolist(),
                     "C_err": Cstd.tolist(), "fit": fit,
                     "m": m_mean, "m_err": m_err, "step": float(np.mean(steps))})
        curves[J] = (r, Cmean, Cstd)
        win = fit.get("winner", "?")
        extra = ""
        if win == "exp":
            extra = f"xi={fit['exp']['xi']:.2f}"
        elif win == "power":
            extra = f"eta={fit['power']['eta']:.2f}"
        elif win == "const":
            extra = f"C0={fit['const']['C0']:.3f}"
        print(f"  {dim} {model_name} J={J:5.3f}  m={m_mean:.3f}+-{m_err:.3f}  "
              f"C(r): {win:5s} {extra}  step={np.mean(steps):.2f}")
    return rows, curves, Js


def verdict_1d(results):
    """1D: NO long-range order at any J (Mermin-Wagner) -- no 'const' plateau and
    m stays at the disordered ~1/sqrt(N) baseline; XY xi matches transfer matrix."""
    ok = True
    notes = []
    for model in ("U(1)", "O(3)"):
        for row in results[("1D", model)][0]:
            w = row["fit"].get("winner")
            if w == "const":
                ok = False
                notes.append(f"1D {model} J={row['J']}: LRO plateau (must be none)")
            if row["m"] > 0.12:           # disordered ~ 1/sqrt(N) ~ 0.016
                ok = False
                notes.append(f"1D {model} J={row['J']}: m={row['m']:.2f} too large")
    # quantitative XY vs exact transfer-matrix xi (only where xi_exact resolvable)
    from scipy.special import i0, i1
    qnotes = []
    for row in results[("1D", "U(1)")][0]:
        J = row["J"]
        xi_mc = row["fit"]["exp"]["xi"]
        xi_exact = -1.0 / np.log(i1(J) / i0(J))
        rel = abs(xi_mc - xi_exact) / xi_exact if np.isfinite(xi_mc) else np.nan
        resolvable = xi_exact >= 1.0
        qnotes.append((J, xi_mc, xi_exact, rel, resolvable))
        if resolvable and (not np.isfinite(rel) or rel > 0.20):
            ok = False
            notes.append(f"1D XY J={J}: xi_mc={xi_mc:.2f} vs exact {xi_exact:.2f} "
                         f"({rel:.0%})")
    return ok, notes, qnotes


def verdict_2d(results):
    """2D XY: KT -- exp correlation length GROWS as cooled, then a scale-free
    power-law (critical) regime appears near J_KT.  2D O(3): no true LRO (the
    plateau must not equal m^2 -- Mermin-Wagner)."""
    ok = True
    notes = []
    xy = sorted(results[("2D", "U(1)")][0], key=lambda r: r["J"])
    # correlation length grows on the disordered (hot) side
    hot = [r for r in xy if r["J"] <= J_KT_2D and r["fit"]["winner"] == "exp"]
    grew = len(hot) >= 2 and hot[-1]["fit"]["exp"]["xi"] > hot[0]["fit"]["exp"]["xi"]
    if not grew:
        ok = False
        notes.append("2D XY: correlation length does not grow toward J_KT")
    # a power-law (critical/KT) regime exists with eta of order the KT value
    crit = [r for r in xy if r["fit"]["winner"] == "power"
            and 0.1 <= r["fit"]["power"]["eta"] <= 0.7]
    if not crit:
        ok = False
        notes.append("2D XY: no scale-free power-law (KT) regime found")
    # 2D O(3): no genuine LRO -- plateau (if any) must NOT match m^2
    for r in results[("2D", "O(3)")][0]:
        if r["fit"]["winner"] == "const":
            cl, m2 = r["fit"]["C_long"], r["m"] ** 2
            if m2 > 0 and abs(cl - m2) / m2 < 0.25:
                ok = False
                notes.append(f"2D O(3) J={r['J']}: genuine LRO (C_long=m^2) "
                             "violates Mermin-Wagner")
    return ok, notes


def verdict_3d(results):
    """3D XY & O(3): genuine LRO for J>J_c -- a flat 'const' plateau with
    C_long = m^2 (Mermin clustering) and m well above the disordered baseline;
    disordered below J_c; a power-law critical point near J_c."""
    ok = True
    notes = []
    m2_checks = []
    for model in ("U(1)", "O(3)"):
        rows = sorted(results[("3D", model)][0], key=lambda r: r["J"])
        jc = JC_3D[model]
        above = [r for r in rows if r["J"] > jc * 1.1]
        below = [r for r in rows if r["J"] < jc * 0.9]
        lro = [r for r in above if r["fit"]["winner"] == "const"]
        if not lro:
            ok = False
            notes.append(f"3D {model}: no LRO plateau above J_c")
        # plateau equals m^2 (internal consistency of true LRO)
        for r in lro:
            cl, m2 = r["fit"]["C_long"], r["m"] ** 2
            rel = abs(cl - m2) / m2 if m2 > 0 else np.nan
            m2_checks.append((model, r["J"], cl, m2, rel))
            if not (rel < 0.20):
                ok = False
                notes.append(f"3D {model} J={r['J']}: C_long={cl:.3f} != m^2={m2:.3f}")
        m_hi = max((r["m"] for r in above), default=0.0)
        if m_hi < 0.5:
            ok = False
            notes.append(f"3D {model}: order parameter stays low (max m={m_hi:.2f})")
        m_lo = min((r["m"] for r in below), default=1.0)
        if m_lo > 0.12:
            notes.append(f"3D {model}: NB m below J_c = {m_lo:.2f} (finite-size)")
        # critical power-law point near J_c
        if not any(r["fit"]["winner"] == "power" for r in rows
                   if jc * 0.9 <= r["J"] <= jc * 1.1):
            notes.append(f"3D {model}: NB no clean power-law point sampled at J_c")
    return ok, notes, m2_checks


def make_figure(results):
    fig, axes = plt.subplots(3, 2, figsize=(11, 12))
    dims = ["1D", "2D", "3D"]
    models = ["U(1)", "O(3)"]
    for i, dim in enumerate(dims):
        for j, model in enumerate(models):
            ax = axes[i, j]
            rows, curves, Js = results[(dim, model)]
            for J in Js:
                r, C, Cstd = curves[J]
                sel = (r >= 1) & (C > 0)
                ax.plot(r[sel], C[sel], "o-", ms=3, lw=1, label=f"J={J:g}")
            ax.set_yscale("log")
            ax.set_xlabel("r (graph hops)")
            ax.set_ylabel("C(r)")
            ax.set_title(f"{dim} {model}")
            ax.legend(fontsize=7, ncol=2)
            ax.grid(alpha=0.2)
    fig.suptitle("E1-V gate: orientation correlation C(r) on regular lattices "
                 "(log scale)\nexp=straight line, power=curved, LRO=flattening",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUT / "E1V_gate.png", dpi=130)
    print(f"saved {OUT/'E1V_gate.png'}")


def main():
    t0 = time.time()
    results = {}
    print("=" * 72)
    print("E1-V GATE -- engine validation on regular lattices")
    print("=" * 72)
    for dim in ("1D", "2D", "3D"):
        for model in ("U(1)", "O(3)"):
            rows, curves, Js = run_case(dim, model)
            results[(dim, model)] = (rows, curves, Js)

    ok1, n1, q1 = verdict_1d(results)
    ok2, n2 = verdict_2d(results)
    ok3, n3, m2chk = verdict_3d(results)
    gate_pass = ok1 and ok2 and ok3

    print("-" * 72)
    print("1D XY transfer-matrix check  C(r)=(I1(J)/I0(J))^r,  xi_mc vs exact:")
    for J, xm, xe, rel, res in q1:
        tag = "" if res else "  (xi<1, unresolvable -- excluded)"
        rels = f"{rel:5.1%}" if np.isfinite(rel) else "  n/a"
        print(f"   J={J:4.1f}  xi_mc={xm:6.2f}  xi_exact={xe:6.2f}  rel={rels}{tag}")
    print("3D Mermin clustering check  C(infinity) == m^2 (genuine LRO):")
    for model, J, cl, m2, rel in m2chk:
        print(f"   {model} J={J:5.3f}  C_long={cl:.3f}  m^2={m2:.3f}  rel={rel:5.1%}")
    print("-" * 72)
    print(f"1D verdict (no LRO, exp, quantitative XY): {'PASS' if ok1 else 'FAIL'}")
    for x in n1:
        print("   -", x)
    print(f"2D verdict (XY KT crossover, O(3) no LRO):  {'PASS' if ok2 else 'FAIL'}")
    for x in n2:
        print("   -", x)
    print(f"3D verdict (XY & O(3) LRO above J_c):       {'PASS' if ok3 else 'FAIL'}")
    for x in n3:
        print("   -", x)
    print("=" * 72)
    print(f"GATE: {'PASS -- engine validated, E1-1 may proceed' if gate_pass else 'FAIL'}")
    print("=" * 72)

    # serialise
    payload = {
        "gate_pass": bool(gate_pass),
        "verdicts": {"1D": bool(ok1), "2D": bool(ok2), "3D": bool(ok3)},
        "notes": {"1D": n1, "2D": n2, "3D": n3},
        "xy_1d_xi_check": [{"J": J, "xi_mc": xm, "xi_exact": xe, "rel_err": rel,
                            "resolvable": bool(res)} for J, xm, xe, rel, res in q1],
        "mermin_clustering_3d": [{"model": mdl, "J": J, "C_long": cl, "m2": m2,
                                  "rel_err": rel} for mdl, J, cl, m2, rel in m2chk],
        "literature_anchors": {"J_KT_2D": J_KT_2D, "J_c_3D": JC_3D},
        "seeds": list(SEEDS),
        "config": {d: {k: v for k, v in CFG[d].items() if k != "builder"}
                   for d in CFG},
        "cases": {f"{dim}/{model}": results[(dim, model)][0]
                  for dim in ("1D", "2D", "3D") for model in ("U(1)", "O(3)")},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E1V_gate.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E1V_gate.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(results)
    return gate_pass


if __name__ == "__main__":
    main()

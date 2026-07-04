"""BD1_diagnosis.py -- isolate the source of the order-1 Lorentz violation.

BRIDGE/BD task BD1.  W2 found the emergent F^2 has E/B ~ 3 (not 1); C1 found the link
second moment has a_t/a_x ~ 3.4.  BD1 traces both to a single, exact structural fact:
the sharp action S=sum_links Dtau[1-cos] is a sum of POSITIVE terms, so its coarse-
grained second moment M2 = <Dtau e^mu e^nu> is POSITIVE-DEFINITE, hence cannot be
proportional to the indefinite metric g^{mu nu}.  We demonstrate the positive-
definiteness numerically and connect it to the temporal asymmetry of the causal cone.

No Lorentz/SR formula in the generator; the DEV/W2/C1 numbers are read for context only.
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402
from bd_core import causal_past_idx  # noqa: E402

OUT = Path(__file__).resolve().parent


def sharp_past_second_moment(rho, T, X, n_real, cap, seed0=0):
    """Sharp Dtau-weighted second moment over the causal past of bulk events.
    Positive weights (Dtau>=0) -> positive-definite by construction; we verify."""
    M = np.zeros((2, 2)); used = 0
    eigs_all = []
    for s in range(n_real):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, [[0, T], [0, X]], rng)
        t, x = pts[:, 0], pts[:, 1]
        base = np.nonzero((t > T * 0.4) & (t < T * 0.65) & (x > X * 0.3) & (x < X * 0.7))[0]
        if len(base) > cap:
            base = rng.choice(base, cap, replace=False)
        Mr = np.zeros((2, 2)); ur = 0
        for xi in base:
            P = causal_past_idx(pts, xi)
            if P.size < 4:
                continue
            e = pts[xi] - pts[P]
            dtau = np.sqrt(np.maximum(e[:, 0] ** 2 - e[:, 1] ** 2, 0.0))
            Mr += np.tensordot(dtau, e[:, :, None] * e[:, None, :], axes=(0, 0))
            ur += 1
        if ur:
            M += Mr; used += ur
            eigs_all.append(np.linalg.eigvalsh(Mr / ur))
    M /= used
    eigs = np.linalg.eigvalsh(M)
    return M, eigs, used


def main():
    res = {}
    M, eigs, used = sharp_past_second_moment(40.0, 8.0, 16.0, n_real=8, cap=120)
    a_t, a_x = float(M[0, 0]), float(M[1, 1])
    res["sharp_second_moment"] = {
        "M2": M.tolist(), "a_t": a_t, "a_x": a_x, "ratio_a_t_over_a_x": a_t / a_x,
        "eigenvalues": eigs.tolist(),
        "positive_definite": bool(np.all(eigs > 0)),
        "can_equal_g_munu": False,
        "note": ("M2 is a sum of Dtau(>=0) * (e outer e)(PSD) => positive-definite. "
                 "g^{mu nu}=diag(+,-) is indefinite, so M2 can NEVER be ~ g. The "
                 "'anisotropy' (a_t/a_x and E/B) is this Euclidean-vs-Lorentzian "
                 "mismatch, sourced by (i) the temporal elongation of causal links "
                 "(a_t = <Dtau Dt^2> dominates) and (ii) the all-positive weighting."),
    }

    # context (read only): C1 link anisotropy and W2 E/B
    ctx = {}
    try:
        c1 = json.loads((ROOT / "results" / "bridge" / "coefficients" /
                         "C1_moments_data.json").read_text())
        ctx["C1_d4_a_t_over_a_x"] = c1["d4_main"]["decomposition"]["a_t_over_a_x"]
    except Exception:
        ctx["C1_d4_a_t_over_a_x"] = None
    try:
        w2 = json.loads((ROOT / "results" / "bridge" / "wilson" /
                         "W2_coarse_graining_data.json").read_text())
        ctx["W2_d4_EB"] = w2["d4"]["EB_anisotropy_ratio"]
    except Exception:
        ctx["W2_d4_EB"] = None
    res["context_existing"] = ctx

    res["cure_identified"] = (
        "An INDEFINITE form needs a SIGN-ALTERNATING weight. The Benincasa-Dowker "
        "smeared weight w(m) (e10) alternates sign by construction -> the only network "
        "operator that can give a Lorentzian (indefinite) second moment. BD2 implements it.")
    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "BD1_diagnosis_data.json").write_text(json.dumps(res, indent=2))

    print("=" * 72)
    print("BD1 -- DIAGNOSIS: why the sharp action is Lorentz-violating")
    print("=" * 72)
    print(f"sharp M2 = <Dtau e e> over causal past (positive weights):")
    print(f"   a_t=<Dtau Dt^2> = {a_t:+.1f}")
    print(f"   a_x=<Dtau Dx^2> = {a_x:+.1f}")
    print(f"   ratio a_t/a_x   = {a_t / a_x:.2f}   (temporal elongation of the cone)")
    print(f"   eigenvalues     = {eigs}  -> positive-definite: {bool(np.all(eigs > 0))}")
    print(f"   => M2 is PSD (sum of Dtau>=0 times e(x)e); g=diag(+,-) is indefinite,")
    print(f"      so M2 can NEVER equal g. THIS is the order-1 'anisotropy'.")
    print(f"\ncontext: C1 a_t/a_x(3+1D)={ctx['C1_d4_a_t_over_a_x']}, W2 E/B={ctx['W2_d4_EB']}")
    print(f"\ncure: {res['cure_identified']}")
    return res


if __name__ == "__main__":
    main()

"""A4 / C4 -- stable Goldstone propagation from the BD-smeared operator.

Campaign PROPAGACAO_A4 (Fase 2, Frente A).  Closes the E2 [FRACO] gap: E2 got
omega=ck from the operator SYMBOL because the literal retarded BD march
(e2_core.bd_propagate, one-sided/non-normal) is UNSTABLE.  A4 asks whether a STABLE
time-evolution of a localized packet, built from the smeared operator, propagates
ballistically with omega=ck MEASURED FROM THE EVOLUTION (not the symbol).

Stages:
  1. machinery gate -- regular 1D lattice, SHARP Laplacian: leapfrog d_t^2 phi=-L phi;
     a launched packet must move ballistically at v_g~1 (omega=ck), stable.  Textbook.
  2. SMEARED symmetric operator on the regular lattice: same test.  Does the smeared
     (longer-range, sign-alternating BD) coupling stay PSD and give stable omega=ck?
  3. causal set -- the symmetric smeared BD operator (c5 construction): is its spectrum
     PSD (stable) or indefinite (the [FRACO] instability root)?  Plus a quantitative
     blow-up demo of the retarded march (e2_core.bd_propagate).

Anti-circularity (CRITICAL): omega is measured from the evolution; c is fitted, never
inserted; the initial packet is real (gaussian*cos), no e^{ikL} injected; smeared
weights and the causal graph are under the A1 guard.

Run:  python docs/campaigns/PROPAGACAO_A4/a4_bd_propagation.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "results" / "foundations" / "c5"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation" / "e2"))
sys.path.insert(0, str(ROOT / "src"))
import c5_core as c5                                  # noqa: E402  smeared BD weights + ancestor
import e2_core as e2                                  # noqa: E402  retarded bd_propagate
from causal_core import sprinkle_box                  # noqa: E402

EPS = c5.EPS_DEFAULT


# ======================================================================== #
# leapfrog evolution of  d_t^2 phi = -L phi  and packet diagnostics
# ======================================================================== #
def leapfrog(L_apply, phi0, pi0, dt, nsteps):
    """Symplectic leapfrog. L_apply(phi) returns L@phi. Returns the field history
    (nsteps+1, N) and the max|phi| over time (stability monitor)."""
    phi = phi0.copy()
    pi = pi0.copy()
    hist = [phi.copy()]
    maxabs = [float(np.max(np.abs(phi)))]
    pi = pi - 0.5 * dt * L_apply(phi)                 # half kick
    for _ in range(nsteps):
        phi = phi + dt * pi
        pi = pi - dt * L_apply(phi)
        hist.append(phi.copy())
        maxabs.append(float(np.max(np.abs(phi))))
    return np.array(hist), np.array(maxabs)


def launch_packet(x, x0, width, k0):
    """Real right-moving wave packet: phi = exp(-(x-x0)^2/2w^2) cos(k0 x)."""
    env = np.exp(-((x - x0) ** 2) / (2 * width ** 2))
    return env * np.cos(k0 * x)


def centroid(x, phi):
    w = phi ** 2
    s = w.sum()
    return float((x * w).sum() / s) if s > 0 else float("nan")


def group_velocity(x, hist, dt, period_box):
    """Track the packet centroid (unwrapped on a periodic box) and fit v_g = slope."""
    cs = np.array([centroid(x, h) for h in hist])
    # unwrap centroid across periodic boundary
    cs_un = cs.copy()
    for i in range(1, len(cs)):
        d = cs_un[i] - cs_un[i - 1]
        if d > period_box / 2:
            cs_un[i:] -= period_box
        elif d < -period_box / 2:
            cs_un[i:] += period_box
    t = np.arange(len(cs)) * dt
    # fit over the first portion (before the packet disperses / wraps a lot)
    nfit = max(5, len(t) // 2)
    v = float(np.polyfit(t[:nfit], cs_un[:nfit], 1)[0])
    return v, cs_un


# ======================================================================== #
# regular-lattice operators (circulant)
# ======================================================================== #
def sharp_laplacian_apply(N):
    def ap(phi):
        return 2 * phi - np.roll(phi, 1) - np.roll(phi, -1)
    return ap, "sharp nearest-neighbour"


def smeared_operator_apply(N, eps=EPS, dmax=8):
    """Symmetric circulant Laplacian with BD-smeared couplings g(d)=2 eps w(d) over
    distance d=1..dmax: L phi = sum_d g(d) (2 phi - roll(phi,d) - roll(phi,-d)).
    Returns the apply fn, a label, and the small-k stiffness c^2 = sum_d g(d) d^2."""
    ds = np.arange(1, dmax + 1)
    g = 2.0 * eps * c5.smeared_weight(ds.astype(float), eps)
    c2 = float(np.sum(g * ds ** 2))                   # small-k: omega^2 ~ c2 k^2

    def ap(phi):
        out = np.zeros_like(phi)
        for d, gd in zip(ds, g):
            out += gd * (2 * phi - np.roll(phi, int(d)) - np.roll(phi, -int(d)))
        return out
    return ap, f"smeared BD (dmax={dmax})", c2, g.tolist()


def mode_frequency(apply_fn, x, k, dt, nsteps):
    """Evolve the single Fourier mode phi=cos(kx), pi=0, and read omega from the
    realised oscillation (FROM EVOLUTION): project onto cos(kx), FFT the time series,
    peak frequency = omega.  Also returns whether the mode stayed BOUNDED (stable)."""
    N = len(x)
    basis = np.cos(k * x)
    phi0 = basis.copy()
    hist, maxabs = leapfrog(apply_fn, phi0, np.zeros(N), dt, nsteps)
    a = hist @ basis / (basis @ basis)                # modal amplitude a(t)
    stable = bool(np.isfinite(maxabs[-1]) and maxabs[-1] < 20 * maxabs[0])
    if not stable:
        return float("nan"), False
    a = a - a.mean()
    freqs = np.fft.rfftfreq(len(a), d=dt) * 2 * np.pi  # angular frequency
    spec = np.abs(np.fft.rfft(a))
    spec[0] = 0.0
    omega = float(freqs[np.argmax(spec)])
    return omega, True


def lattice_stage(apply_fn, label, N=256, ks=(0.10, 0.20, 0.30, 0.40, 0.50), n_periods=12):
    """Measure omega(k) from single-mode evolution; fit omega=ck and stability."""
    x = np.arange(N).astype(float)
    v = np.random.default_rng(0).standard_normal(N)
    for _ in range(60):
        v = apply_fn(v); nv = np.linalg.norm(v); v = v / (nv + 1e-30)
    lam_max = float(v @ apply_fn(v) / (v @ v))
    dt = 0.4 / np.sqrt(abs(lam_max) + 1e-12)
    rows, stable_all = [], True
    for k in ks:
        # enough steps to resolve several periods even for the slowest mode
        nsteps = int(n_periods * 2 * np.pi / (max(k, 0.05) * dt))
        nsteps = int(np.clip(nsteps, 200, 6000))
        omega, stable = mode_frequency(apply_fn, x, k, dt, nsteps)
        stable_all = stable_all and stable
        rows.append({"k": k, "omega": omega, "c_phase": (omega / k if stable else float("nan")),
                     "stable": stable})
    ok = [r for r in rows if r["stable"] and np.isfinite(r["omega"])]
    if len(ok) >= 2:
        kk = np.array([r["k"] for r in ok]); ww = np.array([r["omega"] for r in ok])
        c_fit = float(np.polyfit(kk, ww, 1)[0])        # omega = c k slope
        # linearity: R^2 of omega vs k through origin region
        cph = ww / kk
        c_spread = float(np.std(cph) / (abs(np.mean(cph)) + 1e-12))
        c_mean = float(np.mean(cph))
        linear = bool(c_spread < 0.15 and c_fit > 0)
    else:
        c_fit = c_mean = float("nan"); c_spread = float("nan"); linear = False
    return {"label": label, "lam_max": lam_max, "dt": dt, "rows": rows,
            "c_fit_slope": c_fit, "c_mean_phase": c_mean, "c_spread": c_spread,
            "stable": bool(stable_all), "dispersion_linear_omega_ck": linear}


# ======================================================================== #
# causal-set symmetric smeared BD operator (c5 construction) + spectrum sign
# ======================================================================== #
def bd_operator_matrix(A, eps=EPS):
    """The symmetric Euclideanised smeared BD operator M (c5_core construction),
    returned as a matrix (not just eigenvalues)."""
    Af = A.astype(np.float32)
    inter = (Af @ Af).astype(np.float64)
    m = inter + inter.T
    R = A | A.T
    W = c5.smeared_weight(m, eps)
    M = np.where(R, W, 0.0)
    np.fill_diagonal(M, 0.0)
    np.fill_diagonal(M, -M.sum(axis=1))
    return M


def causet_spectrum_stage(dim=2, Ns=(250, 400), eps=EPS):
    """Build the symmetric smeared BD operator on causal sprinkles; report whether
    its RAW spectrum is PSD (stable evolution possible) or INDEFINITE (the [FRACO]
    instability root: above-light-cone modes have lambda<0 -> exp growth)."""
    rows = []
    for N in Ns:
        rng = np.random.default_rng(N)
        # size the box to hit ~N events at rho=1: N = rho * T * (2X)^(dim-1), T=2X
        X = 0.5 * (N) ** (1.0 / dim)
        bounds = [(0.0, 2 * X)] + [(-X, X)] * (dim - 1)
        pts = sprinkle_box(1.0, bounds, rng)
        A = c5.ancestor_matrix(pts)
        M = bd_operator_matrix(A, eps)
        ev = np.linalg.eigvalsh(M)
        neg_frac = float(np.mean(ev < -1e-9))
        # leapfrog stability of d_s^2 phi = -M phi from a localized packet:
        N_ev = M.shape[0]
        lam_max = float(np.max(np.abs(ev)))
        dt = 0.5 / np.sqrt(lam_max + 1e-12)
        phi0 = np.exp(-((pts[:, 1]) ** 2) / (2 * 0.3 ** 2))   # spatial gaussian
        _, maxabs = leapfrog(lambda p: M @ p, phi0, np.zeros(N_ev), dt, 400)
        blow = float(maxabs[-1] / (maxabs[0] + 1e-30))
        rows.append({"N": int(N_ev), "neg_eig_frac": neg_frac,
                     "lambda_min": float(ev.min()), "lambda_max": float(ev.max()),
                     "leapfrog_maxabs_ratio": blow,
                     "indefinite": bool(neg_frac > 0.02),
                     "evolution_blows_up": bool(blow > 100 or not np.isfinite(blow))})
        print(f"  causet d={dim} N={N_ev}: neg-eig frac={neg_frac:.2f} "
              f"lambda in [{ev.min():.2f},{ev.max():.2f}]  leapfrog max|phi| x{blow:.1e} "
              f"({'INDEFINITE->unstable' if neg_frac>0.02 else 'PSD'})", flush=True)
    return rows


def retarded_march_demo(dim=2, N_target=400, eps=EPS):
    """Quantify the instability of the literal retarded BD march (e2_core.bd_propagate)
    -- the [FRACO] root: max|phi| after marching from a localized initial slab."""
    pts = e2.sprinkle_1plus1(1.0, 3.0, 1.5, seed=7) if dim == 2 else None
    C = e2.order_matrix(pts)
    t = pts[:, 0]
    init_mask = t < 0.2 * t.max()
    phi0 = np.zeros(pts.shape[0])
    phi0[init_mask] = np.cos(3.0 * pts[init_mask, 1])     # real initial data, no phase
    phi = e2.bd_propagate(pts, C, phi0, init_mask, eps)
    prop = phi[~init_mask]
    ratio = float(np.max(np.abs(prop)) / (np.max(np.abs(phi0)) + 1e-30)) if prop.size else 0.0
    # the retarded march fails EITHER way: ratio>>1 (blow-up) or ~0 (signal lost/damped);
    # a faithful propagator would keep O(1) amplitude.
    fails = bool(ratio > 10 or ratio < 0.1)
    mode = "BLOWS UP" if ratio > 10 else ("SIGNAL LOST/damped" if ratio < 0.1 else "O(1)")
    print(f"  retarded march (bd_propagate): propagated max|phi|/init = {ratio:.2e} "
          f"({mode}) -- not a faithful propagator either way", flush=True)
    return {"n_events": int(pts.shape[0]), "maxabs_ratio": ratio,
            "fails_to_propagate": fails, "mode": mode}


# ======================================================================== #
def main():
    t0 = time.time()
    print("=" * 80)
    print("A4 / C4 -- stable BD-smeared Goldstone propagation (omega=ck from evolution)")
    print("=" * 80)

    print("\n[STAGE 1] machinery gate: regular lattice, SHARP Laplacian")
    ap, lab = sharp_laplacian_apply(256)
    s1 = lattice_stage(ap, lab)
    print(f"  {lab}: c(slope)={s1['c_fit_slope']:.3f} c(phase)={s1['c_mean_phase']:.3f} "
          f"(spread {s1['c_spread']:.1%}), stable={s1['stable']}, "
          f"omega=ck linear={s1['dispersion_linear_omega_ck']}")

    print("\n[STAGE 2] SMEARED symmetric operator on the regular lattice")
    ap2, lab2, c2, gd = smeared_operator_apply(256)
    s2 = lattice_stage(ap2, lab2)
    s2["small_k_stiffness_c2"] = c2
    s2["predicted_c"] = float(np.sqrt(c2)) if c2 > 0 else float("nan")
    print(f"  {lab2}: small-k c^2=sum g(d)d^2={c2:.3f} -> predicted c={s2['predicted_c']}")
    print(f"  measured: c(slope)={s2['c_fit_slope']:.3f} (spread {s2['c_spread']:.1%}), "
          f"stable={s2['stable']}, omega=ck linear={s2['dispersion_linear_omega_ck']}")

    print("\n[STAGE 3] causal set: symmetric smeared BD operator spectrum + retarded march")
    s3_spec = causet_spectrum_stage(dim=2)
    s3_march = retarded_march_demo(dim=2)

    # ---- verdict (PRE_REGISTRO sec.2/3) ------------------------------------- #
    gate_ok = s1["stable"] and s1["dispersion_linear_omega_ck"] and abs(s1["c_mean_phase"] - 1) < 0.15
    smeared_stable_ck = (s2["stable"] and s2["dispersion_linear_omega_ck"]
                         and s2["small_k_stiffness_c2"] > 0)
    causet_psd = all(not r["indefinite"] for r in s3_spec)
    causet_unstable = any(r["evolution_blows_up"] for r in s3_spec) or s3_march["fails_to_propagate"]

    if not gate_ok:
        tag = "INCONCLUSIVE"
        verdict = "INCONCLUSIVE: the machinery gate (sharp lattice) did not validate."
    elif smeared_stable_ck and causet_psd:
        tag = "SUCCESS_E2_SOLIDO"
        verdict = (
            f"SUCCESS: the SMEARED symmetric operator supports STABLE ballistic "
            f"propagation with omega=ck MEASURED FROM EVOLUTION (lattice: c={s2['c_mean_phase']:.2f}, "
            f"spread {s2['c_spread']:.0%}, stable), and the causal-set smeared BD "
            f"operator spectrum is effectively PSD -> a stable propagating realization "
            f"EXISTS. E2 [FRACO]->[SOLIDO]; the Paper Goldstone ressalva can be REMOVED.")
    elif smeared_stable_ck and not causet_psd:
        tag = "MORTE_PARCIAL_RESSALVA_CARACTERIZADA"
        verdict = (
            f"MORTE PARCIAL (ressalva caracterizada, mantida): the smeared operator gives "
            f"stable omega=ck on the regular lattice (c={s2['c_mean_phase']:.2f}, stable) -- so the "
            f"SYMBOL result is dynamically realizable in principle -- BUT the causal-set "
            f"symmetric smeared BD operator is INDEFINITE (neg-eig frac "
            f"{max(r['neg_eig_frac'] for r in s3_spec):.0%}: above-light-cone Lorentzian modes "
            f"have lambda<0), so direct evolution on the real causal set BLOWS UP, and the "
            f"retarded march fails too ({s3_march['mode']}). The instability is "
            f"IRREDUCIBLE and now PRECISELY characterized (operator indefiniteness, not a "
            f"coding artifact). E2 stays [FRACO]; the Paper Goldstone ressalva STANDS but is "
            f"documented with its exact mechanism -- submit with it explicit.")
    else:
        tag = "MORTE"
        verdict = (
            f"MORTE: even the smeared operator fails to give stable omega=ck "
            f"(lattice stable={s2['stable']}, linear={s2['dispersion_linear_omega_ck']}, "
            f"c^2={s2['small_k_stiffness_c2']:.2f}). The propagating Goldstone stays SYMBOLIC; "
            f"E2 [FRACO] permanent, ressalva STANDS (submit with it explicit).")

    out = {"campaign": "PROPAGACAO_A4", "eps": EPS,
           "stage1_gate_sharp": s1, "stage2_smeared_lattice": s2,
           "stage3_causet_spectrum": s3_spec, "stage3_retarded_march": s3_march,
           "verdict": verdict, "verdict_tag": tag, "runtime_s": time.time() - t0}
    (HERE / "a4_bd_propagation.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 80)
    print(f"VERDICT [{tag}]:\n{verdict}")
    print(f"[{out['runtime_s']:.0f}s] -> a4_bd_propagation.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

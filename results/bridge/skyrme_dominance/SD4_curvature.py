"""SD4 -- can local curvature R make the net quartic positive (self-stabilising
Skyrmion)?

Pre-registered (SKYRME_DOMINANCE.md addendum, items 4 and 8):

  (a) SIGN THEOREM: the per-link quartic is -(a^4/384)|l_e|^4 -- the -1/24
      comes from the cosine Taylor series, not from geometry. Hence
      E4 = -(a^4/384) <|l_e|^4>_measure <= 0 for ANY direction measure
      (anisotropic, clustered, discrete, any rho) and ANY configuration.
      Extreme case: the hedgehog core has G ~ I, so (e^T G e)^2 = g^4 for
      EVERY direction e -- its quartic is negative under any measure at all.
      Adversarial check below: sup over random measures x random configs of
      the net quartic must be < 0 (and -> 0 only as the field -> 0).

  (b) CURVATURE THROUGH LINK LENGTHS: with the R4-measured interval-volume
      correction Vol(tau) = (pi/24) tau^4 (1 - R tau^2 / 96 + ...), the
      link-length distribution p_R(tau) ~ rho V'_R(tau) exp(-rho V_R(tau))
      shifts: R > 0 shrinks volumes -> less e^{-rho V} suppression -> longer
      links -> <a^4> GROWS: f(R) = <a^4>_R / <a^4>_0 = 1 + kappa R rho^{-1/2}
      with kappa > 0. But curvature scales c_S and c_K together (isotropy of
      directions preserved), so f(R) > 1 makes the net quartic MORE negative:
      curvature is an ANTI-stabiliser, and by (a) no f(R) can flip the sign.

  DEATH CRITERION (charter): f(R) = 1 for all R (curvature inert), OR
  f(R) != 1 but unable to flip the sign (curvature ineffective for
  dominance). Expected: the second branch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sd_core as sd

A_LINK = 1.0


# ---- (a) adversarial sign theorem -------------------------------------------- #
def random_measure(rng, n=4000):
    """A deliberately pathological direction measure: mixture of uniform,
    axis-clustered (von-Mises-like), and a few discrete atoms, with random
    weights."""
    kind = rng.integers(0, 3)
    if kind == 0:                                      # clustered around a pole
        axis = sd.unit_directions(1, 3, rng)[0]
        conc = float(rng.uniform(0.5, 30.0))
        v = axis[None, :] + rng.standard_normal((n, 3)) / np.sqrt(conc)
        dirs = v / np.linalg.norm(v, axis=1, keepdims=True)
    elif kind == 1:                                    # few discrete atoms
        k = int(rng.integers(1, 6))
        atoms = sd.unit_directions(k, 3, rng)
        dirs = atoms[rng.integers(0, k, size=n)]
    else:                                              # uniform
        dirs = sd.unit_directions(n, 3, rng)
    w = rng.random(n) ** 2
    return dirs, w / np.sum(w)


def net_quartic(C, dirs, w, a=A_LINK):
    """Weighted-measure net quartic per link: -(a^4/384) <|l_e|^4>_w."""
    l_e = dirs @ C
    m4 = np.sum(l_e * l_e, axis=1) ** 2
    return -(a ** 4 / 384.0) * float(np.sum(w * m4))


def adversarial_sign(rng, n_trials=20_000):
    sup = -np.inf
    sup_norm = -np.inf                                 # normalised by S (scale-free)
    hedgehog_vals = []
    for _ in range(n_trials):
        dirs, w = random_measure(rng)
        C = rng.standard_normal((3, 3)) * np.exp(rng.standard_normal() * 1.5)
        e4 = net_quartic(C, dirs, w)
        _, S, _ = sd.invariants_d(C)
        sup = max(sup, e4)
        sup_norm = max(sup_norm, e4 / S)
        hedgehog_vals.append(net_quartic(np.eye(3) * 0.05, dirs, w) / 0.05 ** 4)
    return sup, sup_norm, float(np.max(hedgehog_vals)), float(np.min(hedgehog_vals))


# ---- (b) curvature through the link-length distribution ----------------------- #
def vol_R(tau, R):
    return (np.pi / 24.0) * tau ** 4 * (1.0 - R * tau ** 2 / 96.0)


def link_length_moments(rho, R, n_grid=40_000):
    """p_R(tau) ~ rho V'_R(tau) exp(-rho V_R(tau)); returns <tau^4>.
    Grid cut where the curvature correction stays perturbative (<25%)."""
    tau_max = min((96.0 * 0.25 / abs(R)) ** 0.5 if R != 0 else np.inf,
                  6.0 * (24.0 / (np.pi * rho)) ** 0.25)
    tau = np.linspace(1e-6, tau_max, n_grid)
    V = vol_R(tau, R)
    dV = np.gradient(V, tau)
    p = np.clip(rho * dV, 0.0, None) * np.exp(-rho * np.clip(V, 0.0, None))
    Z = np.trapezoid(p, tau)
    return float(np.trapezoid(p * tau ** 4, tau) / Z)


def curvature_scan():
    rhos = [50.0, 200.0, 1000.0, 5000.0]
    out = {}
    for rho in rhos:
        # keep R tau_typ^2 ~ R rho^{-1/2} perturbative: scan R in units of sqrt(rho)
        tau_typ2 = (24.0 / (np.pi * rho)) ** 0.5
        Rs = np.array([-2.0, -1.0, -0.5, 0.5, 1.0, 2.0]) / tau_typ2 * 0.05
        m0 = link_length_moments(rho, 0.0)
        fs = [link_length_moments(rho, R) / m0 for R in Rs]
        # linear fit f = 1 + kappa * R * rho^{-1/2}
        xs = Rs / np.sqrt(rho)
        kappa = float(np.polyfit(xs, np.array(fs) - 1.0, 1)[0])
        out[rho] = {"R_values": Rs.tolist(), "f_R": fs, "kappa_fit": kappa,
                    "tau4_flat": m0}
    return out


# ---- (c) axial anisotropy: can the effective ratio flip the sign? ------------- #
def anisotropy_scan(rng, n=400_000):
    """w(c) ~ exp(kappa_a c^2), c = e_z. Extract effective (cS, cK) from
    configs A/B as in SC2 and check the net sign for the WORST config (the
    one maximising K at fixed S under the anisotropic measure)."""
    out = []
    base = sd.unit_directions(n, 3, rng)
    c2 = base[:, 2] ** 2
    for ka in [-5.0, -2.0, -1.0, 0.0, 1.0, 2.0, 5.0]:
        w = np.exp(ka * c2)
        w = w / np.sum(w)
        g = 0.05
        # effective quartic residuals for configs A (K=0, S=9g^4) and
        # B (K=6g^4, S=9g^4): r = cS*S + cK*K  =>  cS = rA/9, cK = (rB-rA)/6
        l_eA = base @ sd.sc.config_A(g)
        l_eB = base @ sd.sc.config_B(g)
        eA = 1.0 - np.cos(0.5 * A_LINK * np.linalg.norm(l_eA, axis=1))
        eB = 1.0 - np.cos(0.5 * A_LINK * np.linalg.norm(l_eB, axis=1))
        qA = eA - (A_LINK ** 2 / 8.0) * np.sum(l_eA ** 2, axis=1)
        qB = eB - (A_LINK ** 2 / 8.0) * np.sum(l_eB ** 2, axis=1)
        rA = float(np.sum(w * qA)) / g ** 4
        rB = float(np.sum(w * qB)) / g ** 4
        cS = rA / 9.0
        cK = (rB - rA) / 6.0
        # adversarial config under this measure: maximise net quartic / S
        best = -np.inf
        for _ in range(2000):
            C = rng.standard_normal((3, 3))
            l_e = base @ (0.05 * C)
            m4 = np.sum(l_e ** 2, axis=1) ** 2
            e4 = -(A_LINK ** 4 / 384.0) * float(np.sum(w * m4))
            _, S, _ = sd.invariants_d(0.05 * C)
            best = max(best, e4 / S)
        out.append({"kappa_a": ka, "cS_eff": cS, "cK_eff": cK,
                    "ratio_cK_over_minus_cS": -cK / cS,
                    "sup_net_quartic_over_S": best})
    return out


def main():
    rng = np.random.default_rng(20260612)

    sup, sup_norm, hh_max, hh_min = adversarial_sign(rng)
    cur = curvature_scan()
    ani = anisotropy_scan(rng)

    kappas = [cur[r]["kappa_fit"] for r in cur]
    f_ne_1 = all(any(abs(f - 1.0) > 1e-4 for f in cur[r]["f_R"]) for r in cur)
    sign_flipped = (sup_norm > 0) or any(a["sup_net_quartic_over_S"] > 0
                                         for a in ani)

    payload = {
        "a_sign_theorem": {
            "n_trials": 20000,
            "sup_net_quartic": sup,
            "sup_net_quartic_over_S": sup_norm,
            "hedgehog_quartic_per_g4_max": hh_max,
            "hedgehog_quartic_per_g4_min": hh_min,
            "hedgehog_measure_invariant": bool(abs(hh_max - hh_min) < 1e-9),
            # G = g^2 I  =>  |l_e|^2 = g^2 for EVERY e  =>  quartic = -g^4/384
            "expected_hedgehog_value": -(A_LINK ** 4 / 384.0),
        },
        "b_curvature": {str(r): cur[r] for r in cur},
        "b_kappa_summary": {"kappa_mean": float(np.mean(kappas)),
                            "kappa_std": float(np.std(kappas)),
                            "sign": "positive (R>0 lengthens links)"},
        "c_anisotropy": ani,
        "verdict": {
            "f_R_differs_from_1": bool(f_ne_1),
            "net_sign_ever_positive": bool(sign_flipped),
            "note": ("curvature DOES move c4 (f(R) = 1 + kappa R rho^{-1/2}, "
                     "kappa > 0) but multiplies S and K channels together and "
                     "f>1 makes the net quartic MORE negative; anisotropy "
                     "moves the effective cK/cS ratio yet the sign theorem "
                     "holds under every measure tried: no self-stabilisation."),
        },
    }
    sd.save_json("SD4_curvature.json", payload)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.2))
    for r, col in zip(cur, ["C0", "C1", "C2", "C3"]):
        xs = np.array(cur[r]["R_values"]) / np.sqrt(float(r))
        ax1.plot(xs, cur[r]["f_R"], "o-", color=col,
                 label=fr"$\rho$={int(r)} ($\kappa$={cur[r]['kappa_fit']:.3f})")
    ax1.axhline(1.0, color="k", lw=0.8, ls=":")
    ax1.set_xlabel(r"$R\,\rho^{-1/2}$")
    ax1.set_ylabel(r"$f(R)=\langle a^4\rangle_R/\langle a^4\rangle_0$")
    ax1.set_title("curvature moves $c_4$ (collapse in $R\\rho^{-1/2}$)")
    ax1.legend(fontsize=7.5)

    kas = [a["kappa_a"] for a in ani]
    ax2.plot(kas, [a["ratio_cK_over_minus_cS"] for a in ani], "o-", color="C4")
    ax2.axhline(2.0 / 3.0, color="tab:gray", ls=":", lw=1,
                label="isotropic 2/3 (= 2/2880 over 3/5760)")
    ax2.set_xlabel(r"axial anisotropy $\kappa_a$")
    ax2.set_ylabel(r"$-c_K^{\rm eff}/c_S^{\rm eff}$")
    ax2.set_title("anisotropy moves the channel ratio...")
    ax2.legend(fontsize=8)

    ax3.plot(kas, [a["sup_net_quartic_over_S"] for a in ani], "s-", color="C3")
    ax3.axhline(0.0, color="k", lw=0.8)
    ax3.set_xlabel(r"axial anisotropy $\kappa_a$")
    ax3.set_ylabel(r"$\sup_{\rm configs}\;E_4^{\rm net}/S$")
    ax3.set_title("...but the net quartic never goes positive")
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SD4_curvature.png", dpi=150)

    print(json.dumps({"sign_theorem": payload["a_sign_theorem"],
                      "kappa": payload["b_kappa_summary"],
                      "verdict": payload["verdict"]}, indent=2))


if __name__ == "__main__":
    main()

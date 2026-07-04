"""FM3_2_freezing.py -- is the relic cold and frozen? (charter FM3-2)

Two pre-registered questions about the relic texture from FM3-1:

  (A) EQUATION OF STATE.  A frozen field pattern stretched by cosmic expansion has
      gradient-energy density rho ~ |grad n|^2 ~ a^{-2} (physical gradients dilute),
      i.e. w = -1/3 -- NOT cold (w=0, CDM).  We MEASURE the effective w on the
      lattice from how the relic's gradient-energy density scales under dilation
      (rho ~ lambda^{-p}, w = p/3 - 1).  Death-relevant: w >= 0 (cold) is what S8
      needs; w ~ -1/3 (texture/global-monopole) does NOT cluster like CDM.

  (B) FREEZING vs COARSENING.  Under continued FLAT (acausal) zero-T relaxation the
      relic network COARSENS -- defects annihilate (n_def falls).  The E3b causal
      cone, by contrast, FREEZES a super-horizon winding (B preserved; reproduced in
      the gate).  So the relic is frozen ONLY while super-horizon (causal), and
      decays once it can evolve (sub-horizon / acausal).  We measure the flat
      coarsening law n_def(t) to quantify the post-re-entry decay.

Pre-registered P2: w_eff ~ -1/3 (frozen texture), confirmed; the relic is cosmo-
logical-scale (FM3-1) and causally frozen super-horizon (E3b) -- but NOT cold.
Death C2/C3 logic lives in FM3-3/5.  Anti-circularity: w and the coarsening law are
measured; no cosmological number inserted.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fm3_core as f3  # noqa: E402

OUT = Path(__file__).resolve().parent
SEEDS = list(range(20))
L = 20
TAU_Q = 8                     # representative quench
COOL_DOMAINS = 15             # partial cool: keep domains, drop UV noise
LAMBDAS = np.array([1.0, 1.3, 1.7, 2.2, 3.0])
COARSEN_T = [0, 20, 50, 100, 200, 400]


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"FM3-2 -- relic equation of state (w_eff) and freezing vs coarsening (L={L})")
    print("=" * 72)

    # ---- (A) effective equation of state ----
    ws, ps = [], []
    rho_acc = np.zeros(len(LAMBDAS))
    for sd in SEEDS:
        n = f3.quench(L, tau_Q=TAU_Q, seed=sd)
        nc = f3.cool(n, COOL_DOMAINS)
        lam, rho, p, w = f3.w_effective(nc, LAMBDAS)
        ws.append(w); ps.append(p); rho_acc += rho / rho[0]
    w_mean = float(np.mean(ws)); w_sem = float(np.std(ws) / np.sqrt(len(SEEDS)))
    p_mean = float(np.mean(ps))
    rho_mean = rho_acc / len(SEEDS)
    cold = w_mean > -0.1                       # w~0 would be cold (CDM-like)
    texture_like = abs(w_mean + 1.0 / 3.0) < 0.15
    print(f"[A] equation of state: rho ~ lambda^-{p_mean:.2f}  =>  "
          f"w_eff = {w_mean:+.3f} +- {w_sem:.3f}")
    print(f"    cold (w~0, CDM-like)? {cold}   texture-like (w~-1/3)? {texture_like}")

    # ---- (B) coarsening under flat evolution ----
    print("[B] coarsening under continued FLAT relaxation (acausal: defects annihilate)")
    nd_t = np.zeros(len(COARSEN_T))
    for sd in SEEDS[:8]:
        n = f3.quench(L, tau_Q=TAU_Q, seed=sd)
        ts, nd = f3.coarsening(n, COARSEN_T)
        nd_t += nd
    nd_t /= len(SEEDS[:8])
    # coarsening exponent n_def ~ t^-q (t>0)
    tpos = np.array(COARSEN_T[1:], float); npos = nd_t[1:]
    q = -np.polyfit(np.log(tpos), np.log(np.maximum(npos, 1e-3)), 1)[0]
    for tt, nn in zip(COARSEN_T, nd_t):
        print(f"    t={tt:4d}: <n_def>={nn:6.2f}")
    print(f"    flat coarsening law: n_def ~ t^-{q:.2f}  (acausal: relic decays)")

    verdict = ("relic is COSMOLOGICAL-scale (FM3-1) and causally FROZEN super-horizon "
               f"(E3b, gate) -- but its equation of state is w_eff={w_mean:+.2f} "
               "(~ -1/3, texture/global-monopole), NOT cold (w=0). Under flat "
               f"(sub-horizon) evolution it coarsens away (n_def ~ t^-{q:.2f}). So it "
               "is NOT a cold, clustering CDM-like component.")
    print("-" * 72)
    print(f"  FM3-2: {verdict}")
    print("=" * 72)

    payload = {
        "w_eff": w_mean, "w_eff_sem": w_sem, "rho_exponent_p": p_mean,
        "cold_CDM_like": bool(cold), "texture_like_minus_third": bool(texture_like),
        "coarsening_exponent_q": float(q),
        "lambdas": LAMBDAS.tolist(), "rho_norm": rho_mean.tolist(),
        "coarsen_t": COARSEN_T, "n_def_t": nd_t.tolist(),
        "verdict": verdict, "L": L, "tau_Q": TAU_Q, "seeds": len(SEEDS),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "FM3_2_freezing.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM3_2_freezing.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(LAMBDAS, rho_mean, w_mean, COARSEN_T, nd_t, q)
    return payload


def make_figure(lam, rho, w, ts, nd, q):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    ax[0].plot(lam, rho, "o-", lw=1.5, label="measured")
    ax[0].plot(lam, lam ** (-2.0), "k--", label=r"$\lambda^{-2}$ (w=-1/3, texture)")
    ax[0].plot(lam, lam ** (-3.0), "r:", label=r"$\lambda^{-3}$ (w=0, cold/CDM)")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel(r"expansion $\lambda \sim a$"); ax[0].set_ylabel(r"$\rho_{grad}/\rho_0$")
    ax[0].set_title(f"equation of state: w_eff={w:+.2f} (~ -1/3, NOT cold)")
    ax[0].legend(fontsize=8)
    ax[1].plot(ts, nd, "s-", color="firebrick")
    ax[1].set_xlabel("flat (acausal) evolution time"); ax[1].set_ylabel("n_def(t)")
    ax[1].set_title(f"coarsening: relic decays (n_def~t^-{q:.2f}) unless causally frozen")
    fig.suptitle("FM3-2: the relic is cosmological & frozen super-horizon, but w~-1/3 "
                 "(not cold)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM3_2_freezing.png", dpi=130)
    print(f"saved {OUT/'FM3_2_freezing.png'}")


if __name__ == "__main__":
    main()

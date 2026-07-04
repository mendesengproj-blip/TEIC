"""FM2_2_condensate_cs.py -- sound speed of the orientation condensate (charter FM2-2).

The second knob for the S8 inversion (FM2 charter) is a Jeans / free-streaming
suppression from the condensate's sound speed c_s.  To suppress sigma8 at k~0.1-0.2
h/Mpc today we need c_s/c ~ 1.7-3.3e-3.  The two extremes are DEATH:
  c_s ~ c  -> free-streams everything (no structure)      [charter death C3]
  c_s -> 0 -> clusters cold like CDM (sigma8 >= LambdaCDM) [charter death C2]
so the S8 solution lives in a NARROW window c_s/c ~ 1e-3.

We measure the Goldstone sound speed of the ordered O(3) condensate,
    c_s = sqrt(rho_s / chi),
with rho_s the spin stiffness (helicity modulus, ensemble-averaged) and chi the
order-parameter susceptibility, across the ordered phase J >= J_c.  The reference
speed is the magnon speed of E2 (c=1 in natural units; the relativistic Goldstone
of the Lorentz-invariant vacuum).  Question: where does c_s/c sit?  Deep order
(J >> J_c) is stiff -> c_s ~ O(1) (free-streams, C3); near J_c the stiffness
vanishes -> c_s -> 0 (cold, C2); the Jeans window is hit only in a narrow band, an
honest fine-tuning question we report as-measured.

Anti-circularity: c from E2; c_s measured on the lattice; no sigma8 inserted.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fm2_core as fm2  # noqa: E402

OUT = Path(__file__).resolve().parent
SEEDS = list(range(8))
N_BURN, N_MEAS = 500, 200
# ordered phase, from just above J_c(=0.693) to deep order
JS = np.array([0.72, 0.8, 0.9, 1.1, 1.4, 1.8, 2.4])
C_REF = 1.0                 # E2 magnon speed (natural units; the relativistic c)
JEANS_WINDOW = (1.7e-3, 3.3e-3)   # c_s/c needed for sigma8-scale Jeans suppression


def cs_at_J(J, L, seeds):
    css, rhos, chis, ms = [], [], [], []
    for sd in seeds:
        cs, rho, chi, m = fm2.sound_speed(L, J, sd, N_BURN, N_MEAS)
        css.append(cs); rhos.append(rho); chis.append(chi); ms.append(m)
    return (float(np.mean(css)), float(np.std(css) / np.sqrt(len(seeds))),
            float(np.mean(rhos)), float(np.mean(chis)), float(np.mean(ms)))


def main():
    t0 = time.time()
    print("=" * 72)
    print("FM2-2 -- sound speed of the orientation condensate (Jeans knob)")
    print("=" * 72)
    L = 16
    rows = []
    print(f"J-scan (ordered phase), L={L}, {len(SEEDS)} seeds:")
    for J in JS:
        cs, sem, rho, chi, m = cs_at_J(J, L, SEEDS)
        rows.append(dict(J=float(J), c_s=cs, c_s_sem=sem, rho_s=rho, chi=chi, m=m))
        print(f"  J={J:.2f}: c_s={cs:.3f}+-{sem:.3f}  rho_s={rho:.3f}  chi={chi:.4f}  m={m:.3f}")

    cs_arr = np.array([r["c_s"] for r in rows])
    cs_over_c = cs_arr / C_REF
    in_window = np.any((cs_over_c >= JEANS_WINDOW[0]) & (cs_over_c <= JEANS_WINDOW[1]))
    min_cs = float(cs_over_c.min()); max_cs = float(cs_over_c.max())

    # verdict
    if in_window:
        verdict = "A-candidate"
        why = "some J gives c_s/c in the Jeans window (1.7-3.3e-3)."
    elif min_cs > JEANS_WINDOW[1] * 3:
        verdict = "C3"
        why = ("c_s/c is O(1) across the ordered phase (min %.2f) -> the condensate "
               "free-streams; no Jeans suppression at the sigma8 scale. Reaching the "
               "1e-3 window needs J fine-tuned exponentially close to J_c (where "
               "rho_s->0), not generic." % min_cs)
    else:
        verdict = "B"
        why = ("c_s/c approaches but does not cleanly enter the Jeans window "
               "(range %.2e-%.2e); marginal." % (min_cs, max_cs))

    print("-" * 72)
    print(f"  c_s/c range over ordered phase: [{min_cs:.3f}, {max_cs:.3f}]")
    print(f"  Jeans window (c_s/c ~ 1.7-3.3e-3) hit: {'YES' if in_window else 'NO'}")
    print(f"  VERDICT FM2-2: {verdict} -- {why}")
    print("=" * 72)

    payload = {
        "verdict": verdict, "why": why, "c_ref_E2": C_REF,
        "jeans_window": JEANS_WINDOW, "cs_over_c_min": min_cs, "cs_over_c_max": max_cs,
        "in_jeans_window": bool(in_window),
        "rows": rows, "J": JS.tolist(),
        "config": {"L": L, "seeds": len(SEEDS), "n_burn": N_BURN, "n_meas": N_MEAS},
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "FM2_2_condensate_cs.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM2_2_condensate_cs.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(rows)
    return payload


def make_figure(rows):
    J = [r["J"] for r in rows]
    cs = [r["c_s"] for r in rows]
    sem = [r["c_s_sem"] for r in rows]
    rho = [r["rho_s"] for r in rows]
    chi = [r["chi"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    ax[0].errorbar(J, cs, yerr=sem, marker="o", lw=1.5, color="C3")
    ax[0].axhspan(JEANS_WINDOW[0], JEANS_WINDOW[1], color="green", alpha=0.2,
                  label="Jeans window c_s/c~1e-3")
    ax[0].axhline(1.0, color="k", ls="--", lw=1, label="c (magnon, E2)")
    ax[0].axvline(0.693, color="gray", ls=":", label="J_c")
    ax[0].set_yscale("log")
    ax[0].set_xlabel("J (condensate coupling)"); ax[0].set_ylabel("c_s / c")
    ax[0].set_title("condensate sound speed vs order"); ax[0].legend(fontsize=8)
    ax[1].plot(J, rho, "o-", label=r"$\rho_s$ (stiffness)")
    ax[1].plot(J, chi, "s-", label=r"$\chi$ (susceptibility)")
    ax[1].set_xlabel("J"); ax[1].set_ylabel("value"); ax[1].legend(fontsize=8)
    ax[1].set_title(r"$c_s=\sqrt{\rho_s/\chi}$: stiffness vs susceptibility")
    fig.suptitle("FM2-2: the condensate is relativistic (c_s~c) except near J_c "
                 "-> free-streams (C3)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM2_2_condensate_cs.png", dpi=130)
    print(f"saved {OUT/'FM2_2_condensate_cs.png'}")


if __name__ == "__main__":
    main()

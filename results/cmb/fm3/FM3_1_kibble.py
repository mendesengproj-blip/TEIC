"""FM3_1_kibble.py -- does the early-universe ordering transition leave a relic?
(charter FM3-1, Kibble-Zurek)

Quench the O(3) orientation ferromagnet (the E1 vacuum) from disordered (hot) to
ordered (cold) through J_c at varying quench timescales tau_Q, and measure the relic
defect density n_def and the domain coherence length xi_dom.  Kibble: causally
disconnected regions order in different directions -> domains -> defects.  Zurek:
slower quench -> larger domains -> fewer defects, with xi_dom ~ tau_Q^sigma.

Pre-registered P1: a relic DOES form (n_def > 0 for plausible quench), following a
Zurek power law (not n_def -> 0).  Death C1: n_def -> 0 (no relic).

Anti-circularity: defect density measured by the cooled solid-angle charge; no
cosmological number inserted.  20 seeds.
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
TAUS = np.array([2, 4, 8, 16, 32, 64])


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"FM3-1 -- Kibble-Zurek relic of the ordering transition (L={L}, "
          f"{len(SEEDS)} seeds)")
    print("=" * 72)
    rows = []
    for tau in TAUS:
        nd, dens, xi = [], [], []
        for sd in SEEDS:
            n = f3.quench(L, tau_Q=int(tau), seed=sd)
            ndef, density, _ = f3.defect_count(n)
            nd.append(ndef); dens.append(density)
            xi.append(f3.coherence_length(density) if density > 0 else np.nan)
        row = dict(tau_Q=int(tau), n_def=float(np.mean(nd)),
                   n_def_sem=float(np.std(nd) / np.sqrt(len(SEEDS))),
                   density=float(np.mean(dens)),
                   xi_dom=float(np.nanmean(xi)))
        rows.append(row)
        print(f"  tau_Q={tau:3d}: <n_def>={row['n_def']:5.1f}+-{row['n_def_sem']:.1f}  "
              f"xi_dom={row['xi_dom']:.2f}")

    tau = np.array([r["tau_Q"] for r in rows], float)
    ndef = np.array([r["n_def"] for r in rows])
    xi = np.array([r["xi_dom"] for r in rows])
    # Zurek fits: n_def ~ tau^-mu  and  xi_dom ~ tau^sigma
    mu = -np.polyfit(np.log(tau), np.log(ndef), 1)[0]
    sigma = np.polyfit(np.log(tau), np.log(xi), 1)[0]
    relic_forms = bool(ndef.min() > 1.0)           # defects survive even slow quench
    # O(3) model-A expectation sigma = nu/(1+nu z), nu~0.71, z~2 -> ~0.29 (COMPARISON)
    sigma_O3 = 0.29

    if not relic_forms:
        verdict = "C1"; why = "n_def -> 0: no relic forms (death)."
    else:
        verdict = "P1-confirmed"
        why = (f"a relic network forms with Zurek scaling: n_def ~ tau^-{mu:.2f}, "
               f"xi_dom ~ tau^{sigma:.2f} (O(3) model-A expectation ~{sigma_O3}). "
               "The early-universe ordering transition leaves a defect/texture relic.")

    print("-" * 72)
    print(f"  Zurek: n_def ~ tau^-{mu:.2f}   xi_dom ~ tau^{sigma:.2f}  "
          f"(O(3) expect sigma~{sigma_O3})")
    print(f"  relic forms (n_def>1 at slowest quench): {relic_forms}")
    print(f"  FM3-1: {verdict} -- {why}")
    print("=" * 72)

    payload = {
        "verdict": verdict, "why": why, "relic_forms": relic_forms,
        "zurek_mu_ndef": float(mu), "zurek_sigma_xi": float(sigma),
        "sigma_O3_expectation": sigma_O3,
        "rows": rows, "L": L, "seeds": len(SEEDS),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "FM3_1_kibble.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM3_1_kibble.json'}  ({payload['runtime_s']:.0f}s)")
    make_figure(tau, ndef, xi, rows, mu, sigma)
    return payload


def make_figure(tau, ndef, xi, rows, mu, sigma):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    sem = [r["n_def_sem"] for r in rows]
    ax[0].errorbar(tau, ndef, yerr=sem, marker="o", lw=1.5)
    ax[0].plot(tau, ndef[0] * (tau / tau[0]) ** (-mu), "k--",
               label=fr"$n_{{def}}\propto\tau^{{-{mu:.2f}}}$")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel(r"quench time $\tau_Q$"); ax[0].set_ylabel("defects (relic density)")
    ax[0].set_title("Kibble-Zurek: relic defect count"); ax[0].legend(fontsize=8)
    ax[1].plot(tau, xi, "s-", color="teal",
               label=fr"$\xi_{{dom}}\propto\tau^{{{sigma:.2f}}}$")
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel(r"quench time $\tau_Q$"); ax[1].set_ylabel(r"$\xi_{dom}$ (domain size)")
    ax[1].set_title("Zurek scaling of the domain size"); ax[1].legend(fontsize=8)
    fig.suptitle("FM3-1: the ordering transition leaves a relic texture (Kibble-Zurek)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FM3_1_kibble.png", dpi=130)
    print(f"saved {OUT/'FM3_1_kibble.png'}")


if __name__ == "__main__":
    main()

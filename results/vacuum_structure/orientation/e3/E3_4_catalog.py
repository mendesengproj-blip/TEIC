"""E3_4_catalog.py -- catalogue of other n-textures.

Charter E3-4.  Beyond the B=+1 hedgehog, measure charge, energy and fate of:

  anti-hedgehog  n(r) = -r_hat            (expect B = -1: the 'anti-matter' sign)
  dipole         hedgehog + anti-hedgehog (expect net B = 0; does it annihilate
                                           to the vacuum under relaxation?)
  toroidal       a vortex-ring winding    (charge measured, not assumed)

For each: B, gradient energy, B and r_eff after gradient-flow relaxation, and --
for the dipole -- whether the energy decays toward 0 (pair annihilation into the
uniform vacuum).  Anti-circularity: charges are solid-angle counts; 'matter' /
'anti-matter' are COMPARISON-ONLY words.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e3_core as e3  # noqa: E402

OUT = Path(__file__).resolve().parent
L = 24
STEPS = 3000


def relax_track(n, label):
    c = e3.default_center(L)
    rec = list(range(0, STEPS + 1, 300))
    traj = []
    cur = n.copy()
    prev = 0
    for tt in rec:
        if tt > prev:
            _, cur = e3.relax_gradient(cur, n_steps=tt - prev, dt=0.1,
                                       record_every=tt - prev, center=c)
            prev = tt
        traj.append({"t": tt, "B": e3.topological_charge(cur),
                     "E": e3.gradient_energy(cur), "r_eff": e3.r_eff(cur, c)})
    print(f"  {label:14s}: B {traj[0]['B']:+.3f}->{traj[-1]['B']:+.3f}  "
          f"E {traj[0]['E']:.1f}->{traj[-1]['E']:.1f}  "
          f"r_eff {traj[0]['r_eff']:.2f}->{traj[-1]['r_eff']:.2f}")
    return traj


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3-4 -- catalogue of n-textures (charge, energy, fate)")
    print("=" * 72)
    entries = {
        "hedgehog": e3.hedgehog(L, +1),
        "anti_hedgehog": e3.hedgehog(L, -1),
        "dipole": e3.dipole(L),
        "toroidal": e3.toroidal(L),
    }
    cat = {}
    for name, n in entries.items():
        traj = relax_track(n, name)
        B0, Bf = traj[0]["B"], traj[-1]["B"]
        E0, Ef = traj[0]["E"], traj[-1]["E"]
        # annihilation = energy decays to a small fraction of its start AND |B|~0
        annihilates = (abs(Bf) < 0.5) and (Ef < 0.25 * E0)
        cat[name] = {"B0": B0, "Bf": Bf, "E0": E0, "Ef": Ef,
                     "rf": traj[-1]["r_eff"], "annihilates": bool(annihilates),
                     "traj": traj}

    print("-" * 72)
    print("  summary:")
    print(f"    hedgehog       B={cat['hedgehog']['B0']:+.2f} -> {cat['hedgehog']['Bf']:+.2f}  (matter, COMPARISON ONLY)")
    print(f"    anti-hedgehog  B={cat['anti_hedgehog']['B0']:+.2f} -> {cat['anti_hedgehog']['Bf']:+.2f}  (anti, COMPARISON ONLY)")
    print(f"    dipole net     B={cat['dipole']['B0']:+.2f} -> {cat['dipole']['Bf']:+.2f}  "
          f"E {cat['dipole']['E0']:.0f}->{cat['dipole']['Ef']:.0f}  "
          f"annihilates={cat['dipole']['annihilates']}")
    print(f"    toroidal       B={cat['toroidal']['B0']:+.2f} -> {cat['toroidal']['Bf']:+.2f}  "
          f"E {cat['toroidal']['E0']:.0f}->{cat['toroidal']['Ef']:.0f}")
    anti_exists = abs(cat["anti_hedgehog"]["Bf"] + 1) < 0.1
    print("-" * 72)
    print(f"  anti-hedgehog B=-1 exists & survives: {anti_exists}")
    print(f"  pair (B=+1,-1) annihilates to vacuum: {cat['dipole']['annihilates']}")
    print("=" * 72)

    payload = {"L": L, "steps": STEPS, "catalog": cat,
               "anti_hedgehog_exists": bool(anti_exists),
               "pair_annihilates": bool(cat["dipole"]["annihilates"]),
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E3_4_catalog.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3_4_catalog.json'}  ({payload['runtime_s']:.0f}s)")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    ax = axes[0]
    for name in entries:
        tr = cat[name]["traj"]
        ax.plot([s["t"] for s in tr], [s["B"] for s in tr], "o-", ms=3, label=name)
    ax.axhline(0, color="k", ls=":", lw=0.6); ax.axhline(1, color="k", ls=":", lw=0.6)
    ax.axhline(-1, color="k", ls=":", lw=0.6)
    ax.set_xlabel("gradient-flow time"); ax.set_ylabel("B(t)")
    ax.set_title("topological charge under relaxation"); ax.legend(fontsize=8); ax.grid(alpha=0.25)
    ax = axes[1]
    for name in entries:
        tr = cat[name]["traj"]
        ax.plot([s["t"] for s in tr], [s["E"] for s in tr], "o-", ms=3, label=name)
    ax.set_xlabel("gradient-flow time"); ax.set_ylabel("E(t)")
    ax.set_title("energy under relaxation (dipole -> annihilation?)")
    ax.legend(fontsize=8); ax.grid(alpha=0.25)
    fig.suptitle("E3-4: catalogue of orientation defects", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3_4_catalog.png", dpi=130)
    print(f"saved {OUT/'E3_4_catalog.png'}")


if __name__ == "__main__":
    main()

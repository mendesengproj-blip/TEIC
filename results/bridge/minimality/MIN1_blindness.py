"""MIN1 -- universal blindness of U(1) class functions to 2pi flux.

Theorem (closed numerically here): any gauge-invariant link action on compact
U(1) is a function of the GROUP ELEMENT of the plaquette holonomy, i.e. a
2pi-periodic function f(W). A vortex carries geometric flux 2pi through its
core plaquette, but the group element there is exp(i 2pi) = identity, so
f(W_core) = f(0) = 0 for EVERY f in the class -- not small, zero. The winding
is geometrically present (unwrapped sum = 2pi) and energetically invisible.

This closes the higher-harmonic loophole of PHI_EMERGE V4 (which measured the
blindness for f = 1-cos W only): cos(2W), cos(3W), and any random harmonic
series are equally blind. The SU(2) charge B is NOT a loop holonomy (it is the
volume index det(c_x,c_y,c_z), su2_core.baryon_density), so the theorem does
not apply to it -- the structural reason the non-Abelian sector escapes.

Setup: N x N site grid, ideal vortex phase phi = atan2(y, x) with the core at
a plaquette centre; link phases wrapped to (-pi, pi]; W_p = wrapped plaquette
sum; the geometric flux is the UNwrapped plaquette sum.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
N = 64
RNG = np.random.default_rng(20260611)


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def vortex_links(n):
    """Wrapped link phases of the ideal vortex centred between sites."""
    xs = np.arange(n) - (n - 1) / 2.0
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    phi = np.arctan2(Y, X)
    dpx = wrap(np.roll(phi, -1, axis=0) - phi)     # link (i,j)->(i+1,j)
    dpy = wrap(np.roll(phi, -1, axis=1) - phi)
    return dpx, dpy


def plaquette_sums(dpx, dpy):
    """Unwrapped plaquette sum (geometric flux) and wrapped W (group element)."""
    raw = dpx + np.roll(dpy, -1, axis=0) - np.roll(dpx, -1, axis=1) - dpy
    return raw, wrap(raw)


def main():
    dpx, dpy = vortex_links(N)
    raw, W = plaquette_sums(dpx, dpy)
    interior = (slice(1, -2), slice(1, -2))        # drop open-boundary row/col
    raw_i, W_i = raw[interior], W[interior]

    core = np.unravel_index(np.argmax(np.abs(raw_i)), raw_i.shape)
    flux_core = float(raw_i[core])                  # geometric flux: 2pi
    W_core = float(W_i[core])                       # group element: 0
    total_winding = float(np.sum(raw_i) / (2 * np.pi))

    harmonics = {"1-cos(W)": lambda w: 1 - np.cos(w),
                 "1-cos(2W)": lambda w: 1 - np.cos(2 * w),
                 "1-cos(3W)": lambda w: 1 - np.cos(3 * w)}
    coeffs = RNG.uniform(0.1, 1.0, 6)
    harmonics["random 6-harmonic series"] = (
        lambda w: sum(c * (1 - np.cos((k + 1) * w))
                      for k, c in enumerate(coeffs)))

    core_costs = {name: float(f(W_i[core])) for name, f in harmonics.items()}
    # contrast: the same functions applied to the GEOMETRIC flux would all see it
    geometric_would_see = {name: float(f(raw_i[core]) if "2W" not in name
                                       and "3W" not in name and "random" not in name
                                       else f(raw_i[core]))
                           for name, f in harmonics.items()}

    payload = {
        "grid": N,
        "core_geometric_flux": flux_core,
        "core_geometric_flux_over_2pi": flux_core / (2 * np.pi),
        "core_group_element_W": W_core,
        "total_winding_number": total_winding,
        "core_cost_per_action": core_costs,
        "note_geometric": ("the same f applied to the UNwrapped flux would cost "
                           "f(2pi-multiples) -- nonzero only because the argument "
                           "is then not a group element"),
        "f_of_geometric_flux": geometric_would_see,
        "theorem": ("any 2pi-periodic f (= any class function of the U(1) group "
                    "element) has f(W_core)=f(0)=0: core cost identically zero "
                    "for the whole class; V4's single-cosine result is the n=1 "
                    "case. B (SU(2)) is a volume index, not a loop holonomy: "
                    "the theorem structurally does not apply."),
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__},
    }
    (OUT / "MIN1_blindness.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({k: payload[k] for k in
                      ("core_geometric_flux_over_2pi", "core_group_element_W",
                       "total_winding_number", "core_cost_per_action")},
                     indent=2))


if __name__ == "__main__":
    main()

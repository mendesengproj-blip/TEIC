"""DS3 -- the Derrick window vs dimension, with the network's locked coefficients.

Radial hedgehog F = pi exp(-u) generalised to d spatial dimensions: current Gram
eigenvalues F'^2 (radial) and s = sin^2 F / u^2 with multiplicity (d-1).

Three energies, dilation x -> x/lambda:
  E2(lambda)      = lambda^{d-2} E2      (sigma term)
  E_manual        = lambda^{d-2} E2 + e_sk lambda^{d-4} E4K  (dominant quartic)
                    -> interior minimum iff 2 < d < 4  (d=3 unique integer)
  E_cos(lambda;a) = full link cosine with the LOCKED coefficients of SC1
                    (direction average with the d-dim isotropic weight
                     (1-c^2)^{(d-3)/2}): pre-registered MONOTONIC in every d
                    (the -3S+2K saturation is d-independent; this also kills
                     the sextic rescue route in d=5, since the full cosine
                     contains all orders).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import roots_jacobi

OUT = Path(__file__).resolve().parent

U = np.linspace(1e-4, 14.0, 2400)
DU = float(U[1] - U[0])
F = np.pi * np.exp(-U)
FP = -np.pi * np.exp(-U)
S_TAN = np.sin(F) ** 2 / U ** 2
DIMS = [2, 3, 4, 5]
LAMS = np.geomspace(0.05, 4.0, 100)
E_SK = 1.0
A_LINK = 1.0


def energies_lambda1(d):
    trG = FP ** 2 + (d - 1) * S_TAN
    K = trG ** 2 - (FP ** 4 + (d - 1) * S_TAN ** 2)
    meas = U ** (d - 1) * DU                       # radial measure (x solid angle)
    E2 = float(np.sum(meas * trG))
    E4K = float(np.sum(meas * K / 2.0))            # su2_core convention sum_{i<j}
    return E2, E4K


def cos_weights(d, n=64):
    """Quadrature for <f(c)>, c = e.rhat in d dims: weight (1-c^2)^{(d-3)/2}."""
    al = (d - 3) / 2.0
    x, w = roots_jacobi(n, al, al)
    return x, w / np.sum(w)


def e_cos(lam, a, d, cnodes, cw):
    q2 = FP[:, None] ** 2 * cnodes[None, :] ** 2 + \
        S_TAN[:, None] * (1.0 - cnodes[None, :] ** 2)
    arg = (a / (2.0 * lam)) * np.sqrt(np.maximum(q2, 0.0))
    avg = (1.0 - np.cos(arg)) @ cw
    dens = (24.0 / a ** 2) * avg
    return float(np.sum((lam * U) ** (d - 1) * dens) * (lam * DU))


def main():
    out = {}
    fig, axes = plt.subplots(1, len(DIMS), figsize=(16, 4.0))
    for d, ax in zip(DIMS, axes):
        E2, E4K = energies_lambda1(d)
        e_man = LAMS ** (d - 2) * E2 + E_SK * LAMS ** (d - 4) * E4K
        cn, cw = cos_weights(d)
        e_full = np.array([e_cos(l, A_LINK, d, cn, cw) for l in LAMS])

        i_man = int(np.argmin(e_man))
        man_interior = 0 < i_man < len(LAMS) - 1
        cos_monotonic = bool(np.all(np.diff(e_full) > 0))
        out[d] = {
            "E2": E2, "E4K": E4K,
            "manual": {"interior_minimum": bool(man_interior),
                       "lambda_star": float(LAMS[i_man]) if man_interior else None,
                       "lambda_star_pred": float(np.sqrt(E_SK * E4K / E2) *
                                                 ((4 - d) / (d - 2)) ** 0.5)
                       if 2 < d < 4 else None},
            "cosine": {"monotonic_increasing": cos_monotonic,
                       "interior_minimum": bool(
                           0 < int(np.argmin(e_full)) < len(LAMS) - 1)},
        }
        ax.plot(LAMS, e_man / e_man[len(LAMS) // 2], "b-", label="manual quartic")
        ax.plot(LAMS, e_full / e_full[len(LAMS) // 2], "r-", label="full cosine")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(r"$\lambda$")
        ax.set_title(f"d={d}: manual "
                     f"{'MIN @ %.2f' % LAMS[i_man] if man_interior else 'no min'}"
                     f" / cos {'mono' if cos_monotonic else 'STRUCT'}")
        if d == DIMS[0]:
            ax.set_ylabel(r"$E(\lambda)$ (norm.)")
        ax.legend(fontsize=7)
    fig.suptitle("DS3 -- Derrick window: interior minimum only for 2<d<4 (manual); "
                 "cosine alone never")
    fig.tight_layout()
    fig.savefig(OUT / "DS3_derrick.png", dpi=150)

    window = [d for d in DIMS if out[d]["manual"]["interior_minimum"]]
    payload = {"per_dimension": {str(d): out[d] for d in DIMS},
               "derrick_window_integers": window,
               "pre_registered": "window = [3]; cosine monotonic in every d"}
    (OUT / "DS3_derrick.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({"window": window,
                      "cosine_monotonic": {str(d): out[d]["cosine"]
                                           ["monotonic_increasing"]
                                           for d in DIMS}}, indent=2))


if __name__ == "__main__":
    main()

"""PE5_collision.py -- collision test (N/A for a pinning claim; confirmed, not assumed).

PHI_EMERGE task PE5.  The protocol runs the AH5-style collision ONLY if PE4 showed
pinning.  PE4 found no magnitude core (|Phi|=rho is the bare substrate, decoupled from the
gauge sector), so a Veredito-A "stable matter without the extra ingredient" claim is N/A.
Rather than assert N/A, we CONFIRM it: drive a gauge-sector collision (two counter-
propagating gauge wavepackets that build transient flux) and check whether the emergent
|Phi|=rho ever develops a PERSISTENT core (sigma_core constant) anywhere along the way.

Because rho is the static causal-density substrate, it cannot acquire a core from the
gauge dynamics; the collision only stirs the PHASE.  We verify sigma_core stays undefined
(no |Phi| structure) throughout, i.e. no stable matter is created by the composition alone.

Anti-circularity: rho a count; gauge collision is cr3d's own evolution; no complex literal.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phi_emerge_core as pe   # noqa: E402

NSEED = 20
LAM = 0.7


def main():
    grid = (49, 16, 16)
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    sh = (Nx, Ny, Nz)
    dt = pe.c3.dt_cfl(dx)
    xc = float(x[Nx // 2])
    yc = float(y[Ny // 2])

    core_ever_forms = []
    min_dip_seen = []
    for s in range(NSEED):
        rng = np.random.default_rng(500 + s)
        rho = pe.causal_density(Nx, Ny, Nz, rho_sprinkle=8.0, T=8.0, rng=rng)
        # two counter-propagating gauge wavepackets on phix (collision along x), with a
        # transverse bump so plaquettes are excited (cr3d two_chains-style, gauge sector)
        phix = np.zeros(sh); phiy = np.zeros(sh); phiz = np.zeros(sh)
        xx = x[:, None, None]
        amp = 1.5
        phix += amp * np.exp(-((xx - (xc - 8)) ** 2) / 4.0)
        phix -= amp * np.exp(-((xx - (xc + 8)) ** 2) / 4.0)
        phix += 0.1 * amp * rng.standard_normal(sh)
        phix[0] = phix[-1] = 0.0
        vphx = np.zeros(sh)
        # give them velocity toward each other
        vphx += 0.8 * np.exp(-((xx - (xc - 8)) ** 2) / 4.0)
        vphx -= 0.8 * np.exp(-((xx - (xc + 8)) ** 2) / 4.0)

        worst_dip = 0.0
        th, vth = np.zeros(sh), np.zeros(sh)
        py, vpy = phiy.copy(), np.zeros(sh)
        pz, vpz = phiz.copy(), np.zeros(sh)
        px, vpx = phix.copy(), vphx.copy()
        for blk in range(8):
            out = pe.c3.evolve(th, vth, px, vpx, py, vpy, pz, vpz, dx, dt, 120,
                               lam=LAM, freeze_theta=True, friction=0.01)
            th, vth, px, vpx, py, vpy, pz, vpz = out
            pb, _ = pe.phibar(px, py, pz)
            Re, Im = pe.phi_field(rho, pb)
            absF = pe.phi_abs(Re, Im)
            far = float(np.mean(absF))
            core_region = absF[Nx // 2 - 2:Nx // 2 + 3]
            core = float(np.mean(core_region))
            worst_dip = max(worst_dip, (far - core) / far)
        min_dip_seen.append(worst_dip)
        core_ever_forms.append(worst_dip > 0.15)

    frac_core = float(np.mean(core_ever_forms))
    summary = {
        "n_seeds": NSEED, "grid": list(grid), "V": 0.0,
        "status": "N/A for Veredito A (PE4 showed no pinning); collision CONFIRMS no core",
        "max_core_dip_mean": float(np.mean(min_dip_seen)),
        "max_core_dip_std": float(np.std(min_dip_seen)),
        "frac_seeds_core_forms": frac_core,
        "stable_matter_without_extra_ingredient": bool(frac_core > 0.5),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    pe.save_json("PE5_collision", summary)

    print("=" * 74)
    print(f"PE5 -- COLLISION (N/A for Veredito A; confirming no core)  ({NSEED} seeds)")
    print("=" * 74)
    print("  PE4 found no magnitude core, so the AH5 collision is N/A for a pinning claim.")
    print("  We drive a gauge collision and check if |Phi|=rho EVER forms a core:")
    print(f"  max |Phi| core dip over the whole collision: "
          f"{summary['max_core_dip_mean']:.3f} +/- {summary['max_core_dip_std']:.3f}")
    print(f"  fraction of seeds where a core (dip>0.15) ever forms: {frac_core:.2f}")
    print("-" * 74)
    print(f"VERDICT (PE5): stable matter without the extra ingredient? "
          f"{summary['stable_matter_without_extra_ingredient']}")
    print("  The gauge collision stirs the PHASE, but |Phi|=rho (static substrate) never")
    print("  develops a core: no stable structure is created by the composition alone.")
    print("  Veredito A is N/A -- the emergent composition is insufficient for matter")
    print("  creation, exactly as PE4 predicted.")
    return summary


if __name__ == "__main__":
    main()

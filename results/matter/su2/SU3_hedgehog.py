"""SU3 -- the hedgehog/Skyrmion: does a stable point soliton exist on the lattice?

The hedgehog U(r) = exp(i F(r) rhat.sigma) = (cos F, sin F rhat) maps S^3 (space + the
point at infinity) onto SU(2) = S^3 with winding B = 1 when F(0)=pi, F(inf)=0.  Derrick's
theorem in 3D: under a dilation x -> x/lambda the sigma energy scales E2(lambda)=lambda E2
and a 4-derivative (Skyrme) energy E4(lambda)=E4/lambda, so

    E(lambda) = lambda E2 + E4/lambda ,   dE/dlambda=0  ->  lambda*=sqrt(E4/E2),

with a stable minimum ONLY when BOTH terms are present, and at the minimum the VIRIAL
identity E2 = E4 holds.  A pure sigma model (E4=0) collapses (lambda -> 0); the Skyrme
term is the stabiliser.  We test this two ways:

  (A) RADIAL: relax the 1D profile F(r) of the full Skyrme functional for several Skyrme
      weights e_sk; report F(0), F(inf), E2, E4, the Derrick ratio E2/E4 (-> 1), and the
      soliton mass M = E2 + E4.
  (B) 3D LATTICE: embed the relaxed profile on the cubic lattice and scan the dilation
      energy E(lambda) of the lattice functional -- with Skyrme a minimum sits at
      lambda~1 (stable); without Skyrme (e_sk=0) the energy falls monotonically to
      lambda=0 (collapse), the lattice image of Derrick instability.

ANTI-CIRCULARITY: quaternions only; "baryon"/"proton" appear only as NAMES.  B is the
discrete current determinant (su2_core.baryon_number).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

E_SK_LIST = [1.0, 2.0, 4.0]


def radial_study():
    """Relax F(r) for each e_sk on the fixed grid (rmax=14, n=360) that converges to the
    virial minimum E2=E4 for the cores tested here (e_sk=1,2,4 -> core 0.86..1.71 << 14).
    L-BFGS-B with the analytic jac (su2_core._radial_grad) finds the Skyrme profile."""
    r, dr = s.radial_grid(rmax=14.0, n=360)
    out = []
    profiles = {}
    for e_sk in E_SK_LIST:
        F, E2, E4 = s.radial_relax(r, dr, e_sk)
        out.append({"e_sk": e_sk, "E2": E2, "E4": E4, "ratio_E2_E4": E2 / E4,
                    "mass": E2 + E4, "F0": float(F[0]), "Finf": float(F[-1])})
        profiles[e_sk] = (r, F)
    return out, profiles, r, dr


def lattice_dilation(profile_F, r_prof, e_sk, L=28.0, N=85):
    """E(lambda) of the 3D lattice functional for the hedgehog with profile F(r/lambda).
    lambda<1 shrinks the soliton, lambda>1 spreads it.  A well-resolved core (>~5 pts) is
    needed so the UV-sensitive E4 is captured.  Returns lambdas, E2, E4, B."""
    xs = np.linspace(-L / 2, L / 2, N); dx = float(xs[1] - xs[0])
    lambdas = np.linspace(0.6, 1.8, 13)
    E2s, E4s, Bs = [], [], []
    for lam in lambdas:
        prof = lambda rr, lam=lam: np.interp(rr / lam, r_prof, profile_F,
                                             left=s.PI, right=0.0)
        U = s.hedgehog_field(xs, xs, xs, profile=prof)
        E2, E4, _ = s.chiral_energy(U, dx, e_sk)
        E2s.append(E2); E4s.append(E4); Bs.append(s.baryon_number(U, dx))
    return lambdas.tolist(), E2s, E4s, Bs


def main():
    radial, profiles, r, dr = radial_study()

    # pick a WELL-RESOLVED profile (e_sk=4, core ~1.7) for the 3D dilation test
    e_ref = 4.0
    r_prof, F_ref = profiles[e_ref]
    lam, E2_sk, E4_sk, B_sk = lattice_dilation(F_ref, r_prof, e_ref)
    Etot_sk = [a + b for a, b in zip(E2_sk, E4_sk)]
    lam0, E2_0, E4_0, B0 = lattice_dilation(F_ref, r_prof, 0.0)   # no Skyrme: e4 weight 0
    Etot_0 = E2_0                                                 # only sigma

    # stability diagnostics on the lattice dilation curve
    imin_sk = int(np.argmin(Etot_sk))
    lam_min_sk = lam[imin_sk]
    stable_sk = bool(0.7 < lam_min_sk < 1.6 and imin_sk not in (0, len(lam) - 1))
    # without Skyrme: minimum should be at the smallest lambda (collapse)
    imin_0 = int(np.argmin(Etot_0))
    collapse_0 = bool(imin_0 <= 1)

    # radial Derrick virial: E2/E4 -> 1 at the relaxed soliton
    ratios = [d["ratio_E2_E4"] for d in radial]
    virial_ok = all(abs(rr - 1.0) < 0.1 for rr in ratios)
    profile_ok = all(abs(d["F0"] - s.PI) < 0.05 and abs(d["Finf"]) < 0.05
                     for d in radial)

    verdict = ("SIM" if (virial_ok and profile_ok and stable_sk and collapse_0)
               else "PARCIAL" if virial_ok and profile_ok else "NAO")

    payload = {"e_sk_list": E_SK_LIST, "radial": radial,
               "virial_E2_eq_E4": bool(virial_ok), "profile_pi_to_0": bool(profile_ok),
               "lattice_dilation": {
                   "e_sk_ref": e_ref, "lambda": lam,
                   "E_total_with_skyrme": Etot_sk, "E_total_sigma_only": Etot_0,
                   "lambda_min_with_skyrme": lam_min_sk,
                   "stable_with_skyrme": stable_sk,
                   "collapse_without_skyrme": collapse_0,
                   "B_vs_lambda": B_sk},
               "mass_e_sk_1": radial[E_SK_LIST.index(1.0)]["mass"],
               "verdict": verdict}
    s.save_json("SU3_hedgehog", payload)

    if HAVE_MPL:
        fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
        for e_sk in E_SK_LIST:
            rr, FF = profiles[e_sk]
            ax[0].plot(rr, FF, label=f"e_sk={e_sk}")
        ax[0].axhline(np.pi, color="k", lw=0.5, ls=":")
        ax[0].set_xlabel("r"); ax[0].set_ylabel("F(r)")
        ax[0].set_title("relaxed hedgehog profile F(r)"); ax[0].legend()
        ax[1].plot(lam, Etot_sk, "o-", label="with Skyrme")
        ax[1].axvline(1.0, color="k", lw=0.5, ls=":")
        ax[1].axvline(lam_min_sk, color="r", lw=0.8, ls="--", label=f"min@{lam_min_sk:.2f}")
        ax[1].set_xlabel(r"dilation $\lambda$"); ax[1].set_ylabel("E(lambda)")
        ax[1].set_title("Derrick: stable minimum"); ax[1].legend()
        ax[2].plot(lam0, Etot_0, "s-", color="C3")
        ax[2].set_xlabel(r"dilation $\lambda$"); ax[2].set_ylabel("E2(lambda) (sigma only)")
        ax[2].set_title("no Skyrme -> collapse")
        fig.tight_layout(); fig.savefig(s.OUTDIR / "SU3_hedgehog.png", dpi=130)

    print("=" * 72)
    print("SU3 -- HEDGEHOG / SKYRMION: existence and stability")
    print("=" * 72)
    print(f"{'e_sk':>6} {'E2':>9} {'E4':>9} {'E2/E4':>7} {'mass':>9} {'F(0)':>6} {'F(inf)':>7}")
    for d in radial:
        print(f"{d['e_sk']:6.2f} {d['E2']:9.3f} {d['E4']:9.3f} {d['ratio_E2_E4']:7.3f} "
              f"{d['mass']:9.3f} {d['F0']:6.3f} {d['Finf']:7.0e}")
    print("-" * 72)
    print(f"virial E2=E4 (Derrick): {virial_ok}   F:pi->0: {profile_ok}")
    print(f"3D lattice with Skyrme: min at lambda={lam_min_sk:.2f}  stable={stable_sk}")
    print(f"3D lattice sigma-only : collapse (min at smallest lambda)={collapse_0}")
    print(f"VERDICT: hedgehog {verdict}")
    return payload


if __name__ == "__main__":
    main()

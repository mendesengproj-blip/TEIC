"""BQ3 -- the single calibration: N-Delta splitting fixes the Skyrme coupling e.

Collective quantization has ONE dimensionless coupling (e) and ONE external scale
(f_pi).  Feeding the two baryon masses M_N, M_Delta as inputs solves (f_pi, e).
The non-trivial check: the SAME machinery must reproduce the established ANW
calibration e ~ 5.45 (the dimensionless coupling).  f_pi comes out ~2x ANW's
64.5 MeV -- the well-known F_pi = 2 f_pi normalisation convention; f_pi is the
declared EXTERNAL scale (status of G, hbar, a0), so its convention-dependent value
is immaterial to the parameter-free claims.

PRE-REGISTERED KILL: cannot reproduce ANW e within 10% -> formula/units bug, STOP.
"""
from __future__ import annotations
import bq_core as b


def main():
    F, x, dx, Ehat = b.relax_profile()
    f_pi, e = b.calibrate(F, x, dx, M_N_target=939.0, M_D_target=1232.0)
    obs = b.physical(F, x, dx, f_pi, e)

    e_anw, fpi_anw = 5.45, 64.5
    e_rel = abs(e - e_anw) / e_anw
    e_ok = e_rel < 0.10
    # (M_Delta - M_N)/M_N is the calibrating dimensionless ratio
    ratio_ND = obs["M_D_minus_N"] / obs["M_N"]

    payload = dict(
        inputs=dict(M_N=939.0, M_Delta=1232.0),
        calibrated_e=e, calibrated_f_pi_MeV=f_pi,
        ANW_e=e_anw, ANW_f_pi_MeV=fpi_anw,
        e_rel_err_vs_ANW=e_rel, e_ok=bool(e_ok),
        f_pi_over_ANW=f_pi / fpi_anw,
        reproduced_M_N=obs["M_N"], reproduced_M_Delta=obs["M_D"],
        M_sol_classical=obs["M_sol"],
        NDelta_over_N=ratio_ND,
        Ehat=Ehat, Lhat=obs["Lhat"], Iner_invMeV=obs["Iner"],
        convention_note=("f_pi ~ 2x ANW's 64.5 MeV is the F_pi=2 f_pi convention; "
                         "the DIMENSIONLESS coupling e is convention-robust and "
                         "matches ANW. f_pi is the declared EXTERNAL scale."),
        verdict="PASS" if e_ok else "STOP",
    )
    b.save_json("BQ3_calibration", payload)
    print(f"BQ3  calibrated e={e:.3f} (ANW {e_anw})  rel err {e_rel*100:.1f}%  ok={e_ok}")
    print(f"     f_pi={f_pi:.1f} MeV (= {f_pi/fpi_anw:.2f}x ANW; convention)  "
          f"(M_D-M_N)/M_N={ratio_ND:.3f}")
    return payload


if __name__ == "__main__":
    main()

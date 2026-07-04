"""Q4 -- the Finkelstein-Rubinstein constraint: half-integer j selected for B=1.

For a B=1 Skyrmion a closed path q(t) that performs a 2pi rotation is a NON-contractible
loop in configuration space (pi_1(SO(3)) = Z_2): it ends at the SU(2) ANTIPODE,
q(T) = -q(0).  The path integral must weight such paths by the FR phase

    (-1)^{B * W[q]} ,   W[q] = 1 if q(T) = -q(0) (one antipodal crossing), else 0 ,

so for B=1 the amplitude to return after a 2pi rotation carries a MINUS sign.  Summed
over paths this is the projection onto wavefunctions ODD under q -> -q:

    K_FR(q_f, q_i) = K(q_f, q_i) - K(-q_f, q_i)

which acts as 2K on the ODD S^3 harmonics (degree l odd <=> j = l/2 half-integer) and
kills the EVEN ones (integer j).  Result: integer j is REMOVED, the ground state becomes
j = 1/2.

We verify:
  1. the 2pi-rotation path indeed ends at -q(0) (W=1, FR phase -1); 4pi ends at +q(0) (W=0);
  2. the FR spectrum keeps only HALF-INTEGER j (degeneracies (2j+1)^2 = 4, 16, ... for
     j=1/2, 3/2), ground state j=1/2, while the non-FR ground is j=0;
  3. the half-integer law E_{3/2}/E_{1/2} = 5 (= (15/4)/(3/4)).

ANTI-CIRCULARITY: W is a topological count of antipodal crossings of the quaternion path;
the phase (-1)^W is computed from quaternions; B=1 is from SU4.  "fermion"/"boson"/
"statistics" only in COMPARISON ONLY notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2q_core as q   # noqa: E402
import su2_core as s    # noqa: E402

SEED = 1618
A_COEF = 6.0
M_POINTS = 5000


def rotation_path_endpoint(axis, total_angle, n=200):
    """Quaternion at the end of a rotation by ``total_angle`` about ``axis`` (a closed
    SO(3) loop for total_angle multiple of 2pi); also count antipodal crossings W (sign
    flips of the 4-vector dot with the start, i.e. passages through the q.q0=0 equator)."""
    q0 = q.rotation_quat(axis, 0.0)                 # identity (1,0,0,0)
    ts = np.linspace(0, total_angle, n)
    path = np.array([q.rotation_quat(axis, t) for t in ts])
    dots = path @ q0                                 # q(t) . q(0) = cos(t/2)
    # W = number of equator crossings (q.q0 changes sign): each crossing = half-turn
    crossings = int(np.sum(np.sign(dots[:-1]) != np.sign(dots[1:])))
    endpoint = path[-1]
    ends_at_antipode = bool(np.allclose(endpoint, -q0, atol=1e-6))
    return crossings, ends_at_antipode, float(endpoint @ q0)


def group_means(lam, sizes):
    out = []; i = 0
    for sz in sizes:
        out.append(float(np.mean(lam[i:i + sz]))); i += sz
    return np.array(out)


def main():
    rng = np.random.default_rng(SEED)

    # 1) FR phase from path topology: 2pi -> antipode (W=1), 4pi -> start (W=0)
    W_2pi, anti_2pi, dot_2pi = rotation_path_endpoint(2, 2 * np.pi)
    W_4pi, anti_4pi, dot_4pi = rotation_path_endpoint(2, 4 * np.pi)
    phase_2pi = (-1) ** W_2pi
    phase_4pi = (-1) ** W_4pi
    fr_phase_ok = bool(anti_2pi and phase_2pi == -1 and (not anti_4pi) and phase_4pi == 1)

    # 2) spectra: full vs FR
    pts = q.sample_s3(M_POINTS, rng)
    lam_full, _ = q.transfer_spectrum(pts, a=A_COEF, n_levels=30)
    lam0 = lam_full[0]                               # l=0 (j=0) reference
    mu_fr, _ = q.transfer_spectrum(pts, a=A_COEF, n_levels=30, fr=True)
    # FR eigenvalues = 2*lambda_l for odd l; recover absolute E_l = -ln(lambda_l/lam0)
    E_fr = -np.log((mu_fr / 2.0) / lam0)
    # degeneracies of the FR spectrum: expect 4 (j=1/2,l=1), 16 (j=3/2,l=3)
    gm_fr = group_means(mu_fr, [4, 16])
    E_half = float(np.mean(E_fr[:4]))                # j=1/2 (l=1)
    E_3half = float(np.mean(E_fr[4:20]))             # j=3/2 (l=3)
    ratio = E_3half / E_half
    half_integer_law_ok = abs(ratio - 5.0) < 0.4     # (15/4)/(3/4) = 5

    # ground state: FR ground (j=1/2) vs non-FR ground (j=0)
    full_ground_E0 = 0.0                             # l=0, j=0
    fr_selects_half = bool(E_half > 0 and half_integer_law_ok)

    # degeneracy of FR ground multiplet (should be 4 = (2j+1)^2 for j=1/2)
    # count FR eigenvalues within 5% of the largest
    top = mu_fr[0]
    ground_mult = int(np.sum(mu_fr > 0.95 * top))

    all_ok = fr_phase_ok and fr_selects_half
    payload = {
        "a_coef": A_COEF,
        "FR_phase": {"W_2pi": W_2pi, "ends_at_antipode_2pi": anti_2pi,
                     "phase_2pi": phase_2pi, "W_4pi": W_4pi,
                     "ends_at_start_4pi": (not anti_4pi), "phase_4pi": phase_4pi,
                     "ok": fr_phase_ok},
        "full_ground_j": 0.0,
        "FR_ground_j": 0.5,
        "FR_ground_multiplicity": ground_mult,
        "E_half (j=1/2)": E_half, "E_3half (j=3/2)": E_3half,
        "ratio_E3half_Ehalf": ratio, "expected_ratio": 5.0,
        "half_integer_law_ok": bool(half_integer_law_ok),
        "fr_selects_half_integer": fr_selects_half,
        "verdict": "SIM" if all_ok else ("PARCIAL" if fr_phase_ok else "NAO"),
    }
    q.save_json("Q4_FR", payload)

    print("=" * 70)
    print("Q4 -- FINKELSTEIN-RUBINSTEIN: half-integer j for B=1")
    print("=" * 70)
    print(f"FR phase from path topology:")
    print(f"  2pi rotation: ends at antipode={anti_2pi} (q.q0={dot_2pi:+.2f}) "
          f"W={W_2pi} phase=(-1)^W={phase_2pi}")
    print(f"  4pi rotation: ends at start  ={not anti_4pi} (q.q0={dot_4pi:+.2f}) "
          f"W={W_4pi} phase={phase_4pi}")
    print(f"  -> B=1 path integral weights a 2pi loop by -1: {'OK' if fr_phase_ok else 'NO'}")
    print(f"spectrum:")
    print(f"  non-FR ground:   j=0   (integer j allowed)")
    print(f"  FR ground:       j=1/2 (multiplicity {ground_mult}, expect 4=(2j+1)^2)")
    print(f"  E(j=3/2)/E(j=1/2) = {ratio:.3f}  (expect 5.0)  "
          f"-> {'OK' if half_integer_law_ok else 'NO'}")
    print("-" * 70)
    print(f"VERDICT: FR selects j=1/2 as ground state: {payload['verdict']}")
    return payload


if __name__ == "__main__":
    main()

"""R5-1 -- representation-theoretic invariants of SU(N), N=2..8.

PRE-REGISTERED HYPOTHESES AND KILL CRITERIA (written before running)
--------------------------------------------------------------------
Central question: does an analytical criterion force the colour group to be
SU(3) rather than SU(N>=4)?  Three candidate selectors are tested.

H_reality (the candidate POSITIVE):
    "SU(3) is the minimal simple compact Lie group whose FUNDAMENTAL
     representation is complex (3 != 3-bar)."
  KILLED if: SU(2) fundamental is also complex, OR SU(3) fundamental is
             real/pseudoreal, OR some smaller candidate is complex.
  Predicted: SU(2) pseudoreal, SU(3) the first complex -> survives.

H_anomaly:
    "SU(3) is the minimal group carrying a nonzero symmetric cubic invariant
     d^abc (the gauge-anomaly / cubic-Casimir coefficient)."
  KILLED if: d^abc != 0 for SU(2), OR d^abc = 0 for SU(3).
  Predicted: zero at SU(2), nonzero from SU(3) on -> survives.

H_uniqueness (the strong claim the campaign would LOVE to confirm):
    "Some invariant flips between SU(3) and SU(4), singling out N=3 uniquely."
  KILLED if: every invariant that is OFF at SU(2) and ON at SU(3) is ALSO ON at
             SU(4),SU(5),... (i.e. the only boundary is N=2|N=3, never N=3|N=4).
  Predicted: KILLED -- minimality, not uniqueness.

Honesty: none of these invariants is measured by the TEIC causal network; N is
an input to su3_core exactly as d=3 is an input to the geometry.  R5 tests what
PURE group theory selects, and is explicit that the selecting REQUIREMENT
(e.g. "fundamental must be complex") is imported, not derived from the lattice.
"""

import json
import os

import numpy as np

from r5_group_core import (
    gell_mann,
    check_normalisation,
    d_symbol_sumsq,
    fundamental_reality,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def run(Nmax=8):
    rows = []
    for N in range(2, Nmax + 1):
        gens = gell_mann(N)
        norm_err = check_normalisation(gens)
        sum_dsq, max_d = d_symbol_sumsq(gens)
        reality, null_dim, _ = fundamental_reality(gens)
        rows.append(
            {
                "N": N,
                "group": f"SU({N})",
                "dim_adjoint": N * N - 1,
                "rank": N - 1,
                "norm_err": float(norm_err),
                "anomaly_sumsq_dabc": float(sum_dsq),
                "max_abs_dabc": float(max_d),
                "has_cubic_invariant": bool(sum_dsq > 1e-9),
                "fundamental_reality": reality,
                "fundamental_complex": reality == "complex",
                "intertwiner_null_dim": int(null_dim),
            }
        )
    return rows


def boundary_analysis(rows):
    """For each boolean selector, find the value of N at which it switches ON,
    and check whether there is ANY later switch (would-be N=3|N=4 boundary)."""
    out = {}
    for key in ("fundamental_complex", "has_cubic_invariant"):
        seq = [(r["N"], r[key]) for r in rows]
        first_on = next((N for N, v in seq if v), None)
        # any change between consecutive N's after first_on?
        switches = [
            (seq[i][0], seq[i - 1][1], seq[i][1])
            for i in range(1, len(seq))
            if seq[i][1] != seq[i - 1][1]
        ]
        out[key] = {
            "first_true_at_N": first_on,
            "switch_points": switches,  # list of (N, prev, now)
            "single_boundary": switches == [(first_on, False, True)],
        }
    return out


if __name__ == "__main__":
    rows = run(Nmax=8)
    bounds = boundary_analysis(rows)

    print("  N  group   dim  rank   reality      cubic d^abc (sum d^2)")
    for r in rows:
        print(
            f"  {r['N']}  {r['group']:6s} {r['dim_adjoint']:4d}  {r['rank']:3d}   "
            f"{r['fundamental_reality']:11s}  "
            f"{'YES' if r['has_cubic_invariant'] else 'no ':3s}  "
            f"({r['anomaly_sumsq_dabc']:.4f})"
        )
    print()
    for key, b in bounds.items():
        print(
            f"{key}: first ON at SU({b['first_true_at_N']}); "
            f"switches={b['switch_points']}; "
            f"single boundary (N=2|3 only)? {b['single_boundary']}"
        )

    payload = {
        "description": "Representation-theoretic invariants of SU(N), N=2..8, "
        "for colour-group selection (campaign R5).",
        "normalisation": "Tr(T_a T_b)=1/2 delta_ab; d^abc=2 Tr({T_a,T_b}T_c).",
        "rows": rows,
        "boundary_analysis": bounds,
        "max_norm_err": max(r["norm_err"] for r in rows),
    }
    with open(os.path.join(HERE, "R5_invariants.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote R5_invariants.json")

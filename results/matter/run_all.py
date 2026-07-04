"""run_all.py -- run the matter campaign in order M1 -> M2 -> E1 -> E2 -> P1 ->
P2 -> P3 -> P4 and print the verdict table.  S1_synthesis.md is hand-authored from
these results.  Run from anywhere: `python results/matter/run_all.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import M1_inertia, M2_lorentz_mass            # noqa: E402
import E1_energy, E2_conservation             # noqa: E402
import P1_localstate, P2_dispersion, P3_spin, P4_interference  # noqa: E402

STEPS = [("M1", M1_inertia), ("M2", M2_lorentz_mass),
         ("E1", E1_energy), ("E2", E2_conservation),
         ("P1", P1_localstate), ("P2", P2_dispersion),
         ("P3", P3_spin), ("P4", P4_interference)]


def main():
    grades = {}
    for name, mod in STEPS:
        print("\n" + "#" * 72 + f"\n# {name}\n" + "#" * 72)
        grades[name] = mod.main()["verdict"]
    print("\n" + "=" * 72)
    print("MATTER CAMPAIGN VERDICTS")
    print("=" * 72)
    for name, _ in STEPS:
        print(f"  {name}: {grades[name]}")
    print("\nSee results/matter/S1_synthesis.md for the synthesis and honest claim.")


if __name__ == "__main__":
    main()

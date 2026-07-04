"""run_all.py -- reproduce the FL3_SKYRMION_COLLISION campaign end to end.

Order: validation gate -> initial configs -> collision dynamics -> analysis.
FL3-4/FL3-5 are conditional docs (no creation observed); FL3-6 is the synthesis.
"""

from __future__ import annotations

import importlib
import time


STEPS = ["FL3V_gate", "FL3_1_initial", "FL3_2_dynamics", "FL3_3_analysis"]


def main():
    t0 = time.time()
    for name in STEPS:
        print("\n" + "#" * 72)
        print(f"# {name}")
        print("#" * 72)
        mod = importlib.import_module(name)
        mod.main()
    print(f"\nFL3 campaign complete in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

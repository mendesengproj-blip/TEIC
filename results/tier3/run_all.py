"""run_all.py -- reproduce the whole TIER3 campaign in pre-registered order.

Order matters only for the gate: T3V validates the MCMC growth sampler against
e7's exact enumeration; T3A and T3B refuse to run if the gate has not passed.
T3C is independent of the growth sampler (it reuses CC2/e11 machinery).

    python results/tier3/run_all.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    HERE / "T3V_validation.py",
    HERE / "T3A_dynamic_poisson" / "T3A_growth.py",
    HERE / "T3B_dimension_attractor" / "T3B_attractor.py",
    HERE / "T3C_hbar_granularity" / "T3C_phase.py",
]


def main():
    for script in STEPS:
        print(f"\n>>> {script.relative_to(HERE.parents[1])}")
        rc = subprocess.call([sys.executable, "-u", str(script)])
        if rc != 0:
            print(f"ABORT: {script.name} exited with {rc} "
                  "(gate failure or error); stopping the campaign.")
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())

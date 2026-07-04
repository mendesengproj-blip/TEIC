"""run_all.py -- run the full MATTER_SU2_QUANT campaign (Q1..Q7) in order.

  python results/matter/su2_quant/run_all.py          # all
  python results/matter/su2_quant/run_all.py Q1 Q3    # selected

Q1 is the mandatory gate (zero modes); Q3 (path integral) must precede Q4 (FR).
Costs: Q3/Q4/Q5 diagonalise a ~5000x5000 kernel (seconds) + a Monte-Carlo path integral.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["su2q_core", "Q1_zeromodes", "Q2_inertia", "Q3_pathintegral", "Q4_FR",
          "Q5_observables", "Q6_gravity", "Q7_synthesis"]


def main(argv):
    want = argv or STAGES
    for name in STAGES:
        if name not in want and name.split("_")[0] not in want:
            continue
        print("\n" + "#" * 74 + f"\n# {name}\n" + "#" * 74)
        t = time.time()
        mod = importlib.import_module(name)
        if hasattr(mod, "main"):
            mod.main()
        print(f"[{name} done in {time.time() - t:.1f}s]")


if __name__ == "__main__":
    main(sys.argv[1:])

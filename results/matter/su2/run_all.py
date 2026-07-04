"""run_all.py -- run the full MATTER_SU2 campaign (SU1..SU9) in order.

  python results/matter/su2/run_all.py            # all
  python results/matter/su2/run_all.py SU1 SU3    # selected

Cost note: SU2 (SU(2) Metropolis) and SU6 (20-seed collision) are the slow ones
(minutes); SU4/SU7/SU8 carry FD-Skyrme evaluations.  SU1 is the mandatory gate -- if it
fails, stop.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["su2_core", "SU1_motor", "SU2_vacuum", "SU3_hedgehog", "SU4_baryon",
          "SU5_skyrme", "SU6_collision", "SU7_spin", "SU8_consistency",
          "SU9_synthesis"]


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

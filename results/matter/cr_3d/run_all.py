"""run_all.py -- run the full CR_3D campaign (T3D1..T3D6) in order.

  python results/matter/cr_3d/run_all.py            # all
  python results/matter/cr_3d/run_all.py T3D1 T3D2  # selected

T3D4 (the 20-seed 3+1D collision) is the costly one; the others are minutes or less.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["cr3d_core", "T3D1_network", "T3D2_monopoles", "T3D3_string",
          "T3D4_collision", "T3D5_soliton", "T3D6_synthesis"]


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

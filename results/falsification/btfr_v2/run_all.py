"""run_all.py -- run FALSIFICATION_BTFR_V2 (B1 prediction -> B2 data -> B3 comparison).

  python results/falsification/btfr_v2/run_all.py
Requires astropy. B4 is a literature markdown (no script). See FALSIFICATION_BTFR_V2.md.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["B1_prediction", "B2_data", "B3_comparison"]


def main(argv):
    want = argv or STAGES
    for name in STAGES:
        if name not in want:
            continue
        print("\n" + "#" * 74 + f"\n# {name}\n" + "#" * 74)
        t = time.time()
        mod = importlib.import_module(name)
        if hasattr(mod, "main"):
            mod.main()
        print(f"[{name} done in {time.time() - t:.2f}s]")


if __name__ == "__main__":
    main(sys.argv[1:])

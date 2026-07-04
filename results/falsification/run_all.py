"""run_all.py -- run the full FALSIFICATION campaign (F_EHT, F_JWST, F_CMB, F_LENSING, synthesis).

  python results/falsification/run_all.py
All tests are analytic + comparison to cited published data (seconds).
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["F_EHT", "F_JWST", "F_CMB", "F_LENSING", "F_synthesis"]


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

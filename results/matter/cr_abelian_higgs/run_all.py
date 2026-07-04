"""run_all.py -- run the full CR_ABELIAN_HIGGS campaign (AH1..AH7) in order.

  python results/matter/cr_abelian_higgs/run_all.py            # all
  python results/matter/cr_abelian_higgs/run_all.py AH1 AH2    # selected

AH1 is the MANDATORY GATE (five checks before everything); AH2/AH3 precede AH4 (correct
condensate before dynamic pinning); AH4 precedes AH5.  AH5 (20-seed collision) is the
costly one.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["crahiggs_core", "AH1_setup", "AH2_mass", "AH3_vortex",
          "AH4_pinning", "AH5_collision", "AH6_annihilation", "AH7_synthesis"]


def main(argv):
    want = argv or STAGES
    for name in STAGES:
        if name not in want and name.split("_")[0] not in want:
            continue
        print("\n" + "#" * 74 + f"\n# {name}\n" + "#" * 74)
        t = time.time()
        mod = importlib.import_module(name)
        if name == "AH1_setup" and hasattr(mod, "main"):
            res = mod.main()
            if not res.get("AH1_PASS", False):
                print("\nAH1 FAILED -- gate not passed; stopping.")
                return
        elif hasattr(mod, "main"):
            mod.main()
        print(f"[{name} done in {time.time() - t:.1f}s]")


if __name__ == "__main__":
    main(sys.argv[1:])

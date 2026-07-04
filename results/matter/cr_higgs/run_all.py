"""run_all.py -- run the full CR_HIGGS campaign (H1..H6) in order.

  python results/matter/cr_higgs/run_all.py            # all
  python results/matter/cr_higgs/run_all.py H1 H2      # selected

H1 is the MANDATORY GATE (the prompt's H1-before-all rule); H4 must precede H5
(static pinning before dynamic).  H5 (the 20-seed collision on the condensate) is the
costly one; the others are minutes or less.
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = ["crhiggs_core", "H1_condensate", "H2_gauge_mass", "H3_vortex_profile",
          "H4_pinning", "H5_collision", "H6_synthesis"]


def main(argv):
    want = argv or STAGES
    for name in STAGES:
        if name not in want and name.split("_")[0] not in want:
            continue
        print("\n" + "#" * 74 + f"\n# {name}\n" + "#" * 74)
        t = time.time()
        mod = importlib.import_module(name)
        # H1 is the gate: stop the campaign if the condensate does not form
        if name == "H1_condensate" and hasattr(mod, "main"):
            res = mod.main()
            if not res.get("H1_PASS", False):
                print("\nH1 FAILED -- condensate did not converge; stopping (gate rule).")
                return
        elif hasattr(mod, "main"):
            mod.main()
        print(f"[{name} done in {time.time() - t:.1f}s]")


if __name__ == "__main__":
    main(sys.argv[1:])

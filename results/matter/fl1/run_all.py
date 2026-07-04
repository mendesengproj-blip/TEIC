"""run_all.py -- reproduce the whole FL1_SU3_FOUNDATION campaign (Phases A-D).

Usage:  python run_all.py [quick|full]
  quick : fast presets (~minutes) for a smoke reproduction
  full  : production presets (Phase B ~2h, Phase C ~8min) -- the reported numbers

Each phase is gated: it only matters because the previous one passed.  All phases
PASSED (A+B+C+D), so the campaign is the SUCCESS branch.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCALE = sys.argv[1] if len(sys.argv) > 1 else "full"


def run(script, *args):
    print(f"\n{'#' * 74}\n# {script} {' '.join(args)}\n{'#' * 74}")
    subprocess.run([sys.executable, str(HERE / script), *args], check=True)


if __name__ == "__main__":
    run("su3_core.py")                       # engine smoke tests
    run("FLA_definition.py")                 # Phase A (no scale arg)
    run("FLB_ordering.py", SCALE)            # Phase B
    run("FLC_confinement.py", SCALE)         # Phase C
    run("FLD_synthesis.py")                  # Phase D (synthesis)
    print("\nFL1_SU3_FOUNDATION complete -- see FL*.md for verdicts.")

"""Run the whole MATTER_CR_GAUGE campaign G1 -> G6 in order.

G1 is the mandatory validation gate (protocol step 2); G3 is the heaviest (coupled
field evolution over the density ladder x 20 seeds plus the secondary sweeps).  The
full run takes a few minutes.  After G6, run tests/test_no_circularity.py.
"""

from __future__ import annotations

import G1_coupled
import G2_transfer
import G3_collision
import G4_stability
import G5_charge
import G6_synthesis

if __name__ == "__main__":
    gate = G1_coupled.main()
    if not gate["passed"]:
        raise SystemExit("G1 validation failed -- stopping (protocol step 2).")
    print()
    for mod in (G2_transfer, G3_collision, G4_stability, G5_charge, G6_synthesis):
        mod.main()
        print()

"""Run the whole MATTER_CR_DBI campaign DBI1 -> DBI6 in order.

DBI1 is the mandatory validation gate; DBI2/DBI3 are the heaviest (field evolution
over the density ladder x 20 seeds).  The full run takes a few minutes.
"""

from __future__ import annotations

import DBI1_propagator
import DBI2_phase_map
import DBI3_collision
import DBI4_stability
import DBI5_a0
import DBI6_synthesis

if __name__ == "__main__":
    gate = DBI1_propagator.main()
    if not gate["passed"]:
        raise SystemExit("DBI1 validation failed -- stopping (protocol step 2).")
    print()
    for mod in (DBI2_phase_map, DBI3_collision, DBI4_stability,
                DBI5_a0, DBI6_synthesis):
        mod.main()
        print()

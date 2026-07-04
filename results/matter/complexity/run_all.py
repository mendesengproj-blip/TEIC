"""Run the whole MATTER_COMPLEXITY campaign CC1 -> CC6 in order."""

from __future__ import annotations

import CC1_structures
import CC2_cost
import CC3_lorentz
import CC4_conservation
import CC5_gravity
import CC6_synthesis

if __name__ == "__main__":
    for mod in (CC1_structures, CC2_cost, CC3_lorentz,
                CC4_conservation, CC5_gravity, CC6_synthesis):
        mod.main()
        print()

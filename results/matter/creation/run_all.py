"""Run the whole MATTER_CREATION campaign CR1 -> CR6 in order.

CR3 is the heavy step (O(n^3) covering at rho=100); the full run takes a few minutes.
"""

from __future__ import annotations

import CR1_energy
import CR2_collision
import CR3_high_energy
import CR4_conservation
import CR5_gravity
import CR6_synthesis

if __name__ == "__main__":
    for mod in (CR1_energy, CR2_collision, CR3_high_energy,
                CR4_conservation, CR5_gravity, CR6_synthesis):
        mod.main()
        print()

"""Run the whole MATTER_CR_WILSON campaign W1 -> W6 in order.

W1 is the mandatory gate; W2 fixes lambda_c before W3; W3 and W5 are the heaviest (2D
field evolution over the (lambda_p, rho) ladders x seeds).  The full run takes several
minutes.  After W6, run tests/test_no_circularity.py.
"""

from __future__ import annotations

import W1_wilson
import W2_string
import W3_collision
import W4_mass
import W5_phasediagram
import W6_synthesis

if __name__ == "__main__":
    gate = W1_wilson.main()
    if not gate["passed"]:
        raise SystemExit("W1 validation failed -- stopping (protocol step 2).")
    print()
    for mod in (W2_string, W3_collision, W4_mass, W5_phasediagram, W6_synthesis):
        mod.main()
        print()

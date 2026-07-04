"""run_all.py -- run the full C3_REGGE_SKYRMIONS campaign in order.

Gate C3-V first (mandatory); stop if it fails.  Then C3-1, C3-2, C3-3.  C3-4 is
a static qualitative note (C3_4_polaris.md), C3-5 the synthesis (C3_5_synthesis.md).
"""

from __future__ import annotations

import C3V_gate
import C3_1_spectrum
import C3_2_regge
import C3_3_multiskyrmion


def main():
    print("\n########## C3-V GATE ##########")
    gate = C3V_gate.main()
    if not gate["gate_pass"]:
        print("GATE FAILED -- campaign halted.")
        return
    print("\n########## C3-1 SPECTRUM ##########")
    C3_1_spectrum.main()
    print("\n########## C3-2 REGGE TENSION ##########")
    C3_2_regge.main()
    print("\n########## C3-3 MULTI-SKYRMION ##########")
    C3_3_multiskyrmion.main()
    print("\nDone.  See C3_4_polaris.md (qualitative) and C3_5_synthesis.md.")


if __name__ == "__main__":
    main()

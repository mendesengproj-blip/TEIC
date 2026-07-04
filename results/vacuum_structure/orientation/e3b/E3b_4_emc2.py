"""E3b_4_emc2.py -- emergent E^2 = (mc^2)^2 + (pc)^2  (RUNS ONLY UNDER VERDICT A).

Charter E3b-4 + protocol 3: "E3b-4 APENAS se Veredito A em E3b-1".  The mass/energy
relation is computed ONLY if the hedgehog is shown to be INTRINSICALLY stable on
the causal network -- which, per the pre-registered Verdict A, requires BOTH:

    (i)  B=1 preserved under causal evolution  (E3b-1), AND
    (ii) the causal Derrick energy has an INTERIOR minimum  (E3b-3)

so that E_defect is the energy of a self-supporting soliton, not a
boundary-pinned configuration.  This guard reads the two verdicts and refuses to
proceed unless both hold -- exactly the anti-circularity discipline that kept
spin-1/2 honest (no "mass", no "E=mc^2" is asserted for a configuration that is not
a genuine energy minimum).  If it ever runs, c is the MEASURED 0.98 of E2 (never a
constant inserted here) and the relativistic relation is checked for >=5 momenta
with a triple verification.

Current inputs: E3b-1 = B preserved (death criterion not triggered) but E3b-3 =
NO interior Derrick minimum -> Verdict is NOT A -> E=mc^2 is NOT computed.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
C_FROM_E2 = 0.98          # measured magnon speed (E2); used ONLY if Verdict A


def _load(name):
    p = OUT / name
    return json.loads(p.read_text()) if p.exists() else None


def verdict_is_A():
    """Verdict A requires B preserved (E3b-1) AND an interior Derrick minimum
    (E3b-3).  Returns (is_A, reasons)."""
    e1 = _load("E3b_1_hedgehog.json")
    e3 = _load("E3b_3_derrick_causal.json")
    reasons = []
    if e1 is None or e3 is None:
        return False, ["E3b-1 and/or E3b-3 results not found -- run them first."]
    b_ok = e1.get("verdict") == "B=1-preserved" and e1.get("global_survival", 0) >= 0.9
    derrick_ok = bool(e3.get("all_interior_min", False))
    reasons.append(f"E3b-1 B preserved under causal evolution: {b_ok} "
                   f"(global survival {e1.get('global_survival', 0):.0%})")
    reasons.append(f"E3b-3 causal Derrick has interior minimum at all scales: "
                   f"{derrick_ok}")
    return (b_ok and derrick_ok), reasons


def main():
    print("=" * 72)
    print("E3b-4 -- E=mc^2 guard (runs only under Verdict A)")
    print("=" * 72)
    is_A, reasons = verdict_is_A()
    for r in reasons:
        print("  -", r)
    if not is_A:
        msg = ("Verdict is NOT A: the hedgehog has no INTERIOR Derrick minimum "
               "(E3b-3), so its preserved charge (E3b-1/E3b-2) is protected by the "
               "frozen boundary slab propagated through the causal links, not by a "
               "self-supporting energy minimum. E_defect is therefore not a rest "
               "mass and E=mc^2 is NOT computed -- doing so would be the exact "
               "circularity the charter forbids (protocol 3 + anti-circularity 2).")
        print("-" * 72)
        print("  DECISION: SKIP E=mc^2.  " + msg)
        print("=" * 72)
        payload = {"ran": False, "verdict_A": False, "reasons": reasons,
                   "decision": "skip", "explanation": msg,
                   "c_from_E2_would_be": C_FROM_E2}
        (OUT / "E3b_4_emc2.json").write_text(json.dumps(payload, indent=2, default=float))
        print(f"saved {OUT/'E3b_4_emc2.json'}")
        return payload

    # ---- (only reached under Verdict A) -------------------------------------
    # Boosted-hedgehog dispersion E^2=(mc^2)^2+(pc)^2 with c=C_FROM_E2, >=5 momenta,
    # triple verification.  Intentionally left as the explicit next step: it must
    # not be implemented speculatively while the verdict is B, to avoid asserting a
    # mass for a non-minimum.  See E3b_5_synthesis.md.
    raise NotImplementedError(
        "Verdict A reached: implement the boosted-hedgehog E^2=(mc^2)^2+(pc)^2 "
        "measurement (c=0.98 from E2, >=5 momenta, triple verification V1/V2/V3).")


if __name__ == "__main__":
    main()

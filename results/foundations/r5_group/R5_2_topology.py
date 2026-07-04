"""R5-2 -- homotopy / Bott analysis: does TOPOLOGY select SU(3)?

The TEIC programme would most like the colour group to be fixed by TOPOLOGY,
because the matter sector's charges ARE topological (B = pi_3 index, measured in
MATTER_SU2; spin-1/2 from pi_4=Z_2).  This task tabulates the low homotopy groups
of SU(N) (standard results; Bott periodicity for the stable range) and applies a
mechanical "does it distinguish N=3 from N=4?" test to each.

PRE-REGISTERED KILL CRITERION (for H_topology):
    H_topology = "a homotopy group pi_k(SU(N)) that carries physical meaning in
                  3+1D (k <= 5: instanton/Skyrmion charge k=3, spin-statistics
                  k=4, WZW/baryon term k=5) takes a DIFFERENT value at SU(3) than
                  at SU(4)."
    KILLED if every physically-relevant pi_k (k<=5) is equal for SU(3) and SU(4).
    Predicted: KILLED.  pi_3=Z for all N (Bott); pi_4,pi_5 separate SU(2) from
    N>=3 but NOT 3 from 4.

These are reference constants (homotopy groups are not numerically computable
here); the script's job is to apply the distinguish-test reproducibly and record
the verdict, not to recompute topology.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Standard low homotopy groups of SU(N).  "Z"=integers, "0"=trivial, "Zn"=cyclic.
# Sources: Bott (1956) stable range; Mimura-Toda tables for unstable entries.
# physical_role flags the dimensions with a known 3+1D interpretation.
HOMOTOPY = {
    "pi_3": {
        "physical_role": "instanton / Skyrmion (baryon) winding number",
        "values": {2: "Z", 3: "Z", 4: "Z", 5: "Z", 6: "Z"},
        "note": "Bott: pi_3(G)=Z for every simple compact Lie group.",
    },
    "pi_4": {
        "physical_role": "spin-statistics enabler; Witten SU(2) global anomaly",
        "values": {2: "Z2", 3: "0", 4: "0", 5: "0", 6: "0"},
        "note": "pi_4(SU(2))=Z2 (used for spin-1/2, FQ2); 0 for N>=3.",
    },
    "pi_5": {
        "physical_role": "Wess-Zumino-Witten term / baryon-number current",
        "values": {2: "Z2", 3: "Z", 4: "Z", 5: "Z", 6: "Z"},
        "note": "SU(3) is the first with pi_5=Z (nontrivial WZW); but SU(N>=3) all Z.",
    },
    "pi_6": {
        "physical_role": "none known in 3+1D (maps S^6 -> G)",
        "values": {2: "Z12", 3: "Z6", 4: "0", 5: "0", 6: "0"},
        "note": "UNSTABLE: pi_6(SU(3))=Z6 differs from pi_6(SU(4))=0 -- a genuine "
        "3-vs-4 distinction, but with no physical role.",
    },
}


def distinguishes(values, a, b):
    return values.get(a) != values.get(b)


def run():
    table = []
    for pik, info in HOMOTOPY.items():
        v = info["values"]
        table.append(
            {
                "homotopy": pik,
                "physical_role": info["physical_role"],
                "SU2": v[2],
                "SU3": v[3],
                "SU4": v[4],
                "distinguishes_2_from_3": distinguishes(v, 2, 3),
                "distinguishes_3_from_4": distinguishes(v, 3, 4),
                "note": info["note"],
            }
        )
    # Verdict on H_topology: any PHYSICAL pi_k (k<=5) that separates 3 from 4?
    physical = [
        row
        for row in table
        if row["homotopy"] in ("pi_3", "pi_4", "pi_5")
    ]
    physical_separates_3_4 = any(row["distinguishes_3_from_4"] for row in physical)
    any_separates_3_4 = any(row["distinguishes_3_from_4"] for row in table)
    return table, physical_separates_3_4, any_separates_3_4


if __name__ == "__main__":
    table, phys34, any34 = run()
    print(f"{'pi_k':6s} {'SU2':5s} {'SU3':5s} {'SU4':5s}  2|3?  3|4?  role")
    for row in table:
        print(
            f"{row['homotopy']:6s} {row['SU2']:5s} {row['SU3']:5s} {row['SU4']:5s}  "
            f"{str(row['distinguishes_2_from_3'])[0]:4s}  "
            f"{str(row['distinguishes_3_from_4'])[0]:4s}  {row['physical_role']}"
        )
    print()
    print(f"H_topology KILLED (no PHYSICAL pi_k separates SU3 from SU4)? "
          f"{not phys34}")
    print(f"  (any pi_k at all separates 3 from 4? {any34} -- pi_6, physically inert)")

    payload = {
        "description": "Low homotopy of SU(N) and the colour-selection test (R5).",
        "table": table,
        "H_topology_killed_physical": not phys34,
        "any_homotopy_separates_3_from_4": any34,
        "verdict": (
            "Topology (physically-relevant pi_3,pi_4,pi_5) does NOT distinguish "
            "SU(3) from SU(4). pi_4/pi_5 separate SU(2) from N>=3 only. The single "
            "homotopy group that separates 3 from 4 (pi_6) has no 3+1D role."
        ),
    }
    with open(os.path.join(HERE, "R5_topology.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote R5_topology.json")

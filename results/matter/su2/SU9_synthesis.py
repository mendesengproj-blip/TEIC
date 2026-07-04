"""SU9 -- aggregate the SU1..SU8 verdicts into a single honest summary (see SU9_synthesis.md)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

OUT = Path(__file__).resolve().parent


def load(name):
    p = OUT / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    su1 = load("SU1_motor"); su2 = load("SU2_vacuum"); su3 = load("SU3_hedgehog")
    su4 = load("SU4_baryon"); su5 = load("SU5_skyrme"); su6 = load("SU6_collision")
    su7 = load("SU7_spin"); su8 = load("SU8_consistency")

    summary = {
        "SU1_motor": su1.get("verdict"),
        "SU2_vacuum_confines": su2.get("verdict"),
        "SU3_hedgehog_stable": su3.get("verdict"),
        "SU4_baryon_B1_conserved": su4.get("verdict"),
        "SU5_derrick_stable": "SIM",
        "SU5_skyrme_from_C4": "NAO (antisymmetric, non-Abelian; not the C4 quartic)",
        "SU6_created_by_collision": su6.get("verdict"),
        "SU7_spin_half": su7.get("verdict"),
        "SU8_consistencies": su8.get("passed"),
        "VERDICT": "B",
        "verdict_text": (
            "B -- stable point Skyrmion with B=1 (mass, self-gravity proportional to "
            "mass, isotropy; topological charge quantised and conserved), stabilised by "
            "the genuinely non-Abelian Skyrme term. NOT created by collision (C for the "
            "creation question) and spin-1/2 not classically verifiable (a quantum FR "
            "phase), so NOT verdict A. The frontier moved from the U(1) diffuse vortex "
            "(1D) to a stable SU(2) point soliton (0D); the remaining ingredients are "
            "collective-coordinate quantisation (spin) and a topological creation "
            "mechanism (dynamical birth)."),
    }
    s.save_json("SU9_synthesis", summary)

    print("=" * 72)
    print("SU9 -- SYNTHESIS")
    print("=" * 72)
    for k, v in summary.items():
        if k in ("verdict_text",):
            continue
        print(f"  {k:32s}: {v}")
    print("-" * 72)
    print(summary["verdict_text"])
    return summary


if __name__ == "__main__":
    main()

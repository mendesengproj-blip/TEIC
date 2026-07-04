"""Run the full BARYON_QUANTITATIVE campaign (BQ1-BQ5) in order."""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for mod in ["BQ1_tower", "BQ2_inertia", "BQ3_calibration", "BQ4_moments",
            "BQ5_synthesis"]:
    print(f"\n===== {mod} =====")
    runpy.run_path(str(HERE / f"{mod}.py"), run_name="__main__")

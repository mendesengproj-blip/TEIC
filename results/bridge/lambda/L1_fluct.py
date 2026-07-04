"""L1 -- Poisson density fluctuations in nested volumes: the 1/sqrt(rho V) law.

Total point count drawn ~ Poisson(lambda) (true Poisson process, so the
regional count N(v) is exactly Poisson and rms(dN/N) = 1/sqrt(rho v) with
coefficient exactly 1 -- the pre-registered baseline). 20 seeds; nested balls.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
LAM = 100_000              # expected total points in the unit ball
RADII = [0.2, 0.3, 0.4, 0.5]
N_SEEDS = 200
V_BALL = 4.0 * np.pi / 3.0


def sprinkle(rng):
    n = rng.poisson(LAM)
    v = rng.standard_normal((n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    r = rng.uniform(0.0, 1.0, n) ** (1.0 / 3.0)
    return v * r[:, None]


def main():
    rho = LAM / V_BALL
    counts = {r: [] for r in RADII}
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(8000 + seed)
        pts = sprinkle(rng)
        rr = np.linalg.norm(pts, axis=1)
        for r in RADII:
            counts[r].append(int(np.sum(rr < r)))

    rows = []
    for r in RADII:
        c = np.array(counts[r], dtype=float)
        v = V_BALL * r ** 3                      # = (4pi/3) r^3
        mean, std = float(np.mean(c)), float(np.std(c, ddof=1))
        coeff = (std / mean) * np.sqrt(rho * v)
        rows.append({"radius": r, "volume": v, "mean_N": mean,
                     "rms_dN_over_N": std / mean,
                     "predicted_rms": 1.0 / np.sqrt(rho * v),
                     "coefficient": float(coeff)})

    coeffs = [row["coefficient"] for row in rows]
    payload = {"lambda_total": LAM, "rho": rho, "n_seeds": N_SEEDS,
               "rows": rows,
               "coefficient_mean": float(np.mean(coeffs)),
               "pre_registered": "1.00 +- 0.05 (sampling error of an rms with "
                                 "n seeds ~ 1/sqrt(2n): 0.16 at n=20, 0.05 at "
                                 "n=200; first 20-seed run gave 0.88 -- within "
                                 "1 sigma -- and was tightened to 200 seeds)",
               "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                         "numpy": np.__version__}}
    (OUT / "L1_fluct.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({"coefficients": coeffs,
                      "mean": payload["coefficient_mean"]}, indent=2))


if __name__ == "__main__":
    main()

"""repro.py -- Reproducibility helpers: fixed seeds + metadata stamped to outputs."""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"
FIGS = ROOT / "results" / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)


def rng(seed):
    """Single source of randomness for an experiment."""
    return np.random.default_rng(seed)


def env_metadata(seed, params):
    """Dict describing the run, written next to every data product."""
    import scipy
    import sympy
    return {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed": seed,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "libs": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sympy.__version__,
        },
        "params": params,
    }


def save_run(name, seed, params, arrays=None, summary=None):
    """Persist metadata (+ optional arrays/summary) under results/data/<name>."""
    meta = env_metadata(seed, params)
    if summary is not None:
        meta["summary"] = summary
    (DATA / f"{name}.meta.json").write_text(json.dumps(meta, indent=2))
    if arrays:
        np.savez(DATA / f"{name}.npz", **arrays)
    return meta

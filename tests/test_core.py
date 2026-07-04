"""Unit tests for the causal-network core (run with: python tests/test_core.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causal_core import (alexandrov_interval, precedes, sprinkle_box)  # noqa: E402
from chain import longest_chain_2d, longest_chain_dag  # noqa: E402
from volume import diamond_volume, tau_from_count  # noqa: E402


def approx(a, b, tol):
    return abs(a - b) <= tol


def test_precedes():
    assert precedes([0, 0], [1, 0])          # straight up: timelike
    assert precedes([0, 0], [2, 1])          # inside cone
    assert not precedes([0, 0], [1, 2])      # spacelike
    assert not precedes([1, 0], [0, 0])      # past, not future
    assert precedes([0, 0, 0, 0], [3, 1, 1, 1])      # 1+3D timelike (9>3)
    assert not precedes([0, 0, 0, 0], [1, 1, 1, 1])  # 1+3D spacelike (1<3)
    print("  precedes: ok")


def test_chain_agreement():
    rng = np.random.default_rng(0)
    pts = sprinkle_box(40.0, [(0, 4), (-2, 2)], rng)
    A, B = np.array([0.0, 0.0]), np.array([4.0, 0.0])
    idx = alexandrov_interval(pts, A, B)
    sub = np.vstack([A, pts[idx], B])
    l2 = longest_chain_2d(sub)
    ldag = longest_chain_dag(sub)
    assert l2 == ldag, (l2, ldag)
    print(f"  longest chain 2d==dag: ok (length {l2})")


def test_volume_roundtrip():
    # tau -> expected count -> tau, for both dimensions
    for d in (2, 4):
        tau, rho = 5.0, 100.0
        N = rho * diamond_volume(tau, d)
        assert approx(tau_from_count(N, rho, d), tau, 1e-9), d
    print("  volume tau<->count roundtrip: ok")


def test_interval_count_scaling():
    # mean count in a 2D diamond should be rho * (1/2) tau^2
    rng = np.random.default_rng(1)
    rho, tau = 200.0, 3.0
    counts = []
    for _ in range(30):
        pts = sprinkle_box(rho, [(0, tau), (-tau / 2, tau / 2)], rng)
        idx = alexandrov_interval(pts, [0.0, 0.0], [tau, 0.0])
        counts.append(len(idx))
    mean = np.mean(counts)
    expected = rho * diamond_volume(tau, 2)
    rel = abs(mean - expected) / expected
    assert rel < 0.06, (mean, expected, rel)
    print(f"  diamond count scaling: ok (mean {mean:.1f} vs {expected:.1f}, {rel:.1%})")


if __name__ == "__main__":
    print("test_core:")
    test_precedes()
    test_chain_agreement()
    test_volume_roundtrip()
    test_interval_count_scaling()
    print("ALL CORE TESTS PASSED")

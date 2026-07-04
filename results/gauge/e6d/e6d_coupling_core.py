"""e6d_coupling_core.py -- ferromagnet<->gauge coupling on E6c's CURVED substrate.

E6c found the first positive signal in the photon sector: de Sitter curvature (R̂=2)
furnishes a magnetic (B-type) 2-cell fraction of ~1.17% in height-4 causal diamonds --
above the 1% threshold but far from the O(1) a real emergent photon needs. E6d (Direction
B) asks whether COUPLING the ordered orientation ferromagnet (E1, an O(3)/Heisenberg field
n⃗∈S² on the events) to the U(1) gauge sector AMPLIFIES that 1.17% toward O(1).

SUBSTRATE = E6c's curved geometry (R̂≈2, h=4), NOT flat Minkowski. The orientation field
lives on the SAME causal link graph used for the diamonds (as in E1/E2).

THE COUPLING (prompt). Φ_{ij} = A_{ij} + λ (n⃗_i × n⃗_j)·ê_z, with ê_z = ⟨n⃗⟩ the order
direction. We realise this EXACTLY inside E6's geometric E/B classifier, so that λ=0 returns
E6c bit-for-bit. Key identity: for transverse components (u,v)=(n·e1, n·e2) in any
orthonormal basis {e1,e2,ê_z},

        (n_i × n_j)·ê_z = u_i v_j − v_i u_j ,

so appending the internal coordinates λ(u_c, v_c) to each event's 5D de Sitter embedding
X_c and taking the area bivector of the AUGMENTED 7D embedding gives an internal–internal
bivector component

        Ã^{(5)(6)}_P = ½ λ² Σ_c (u_c v_{c+1} − v_c u_{c+1}) = ½ λ² Σ_c (n_c × n_{c+1})·ê_z
                     = ½ λ² Φ^orient_P  (the prompt's coupling, summed around the plaquette).

The internal axes carry NO time component, so they are spacelike -> they feed ONLY the
magnetic content b² (and the time–internal cross terms feed e², the space–internal feed b²).
Thus the orientation field couples into the gauge bivector exactly as a spacelike (magnetic)
channel of strength λ, and:

  * λ=0  -> Ã reduces to the 5D de Sitter bivector -> E6c EXACTLY  (gate G0/G1, bit-for-bit).
  * the coupling uses ONLY the transverse magnon components (n ⊥ ê_z), i.e. it vanishes when
    the field is aligned and is sourced by the texture relative to the order direction --
    so an ORDERED ferromagnet (smooth, small coherent texture) and a DISORDERED one
    (random texture) give DIFFERENT contributions, which is exactly the G2 discriminator.

The E/B physics (`polygon_bivectors`, B-type iff b²>e²) and the 2h-gon diamonds
(`height_h_plaquettes`) are REUSED VERBATIM from e6b/e6_bd_core (polygon_bivectors already
works in ANY dimension D; here D=7). The de Sitter geometry is REUSED VERBATIM from e6c.
Only the augmentation (the coupling) is new. No relativistic literal inserted.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E6 = HERE.parent / "e6"
E6B = HERE.parent / "e6b"
E6C = HERE.parent / "e6c"
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
ROOT = HERE.parents[2]
for p in (str(HERE), str(E6), str(E6B), str(E6C), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from e6b_diamond_height_core import polygon_bivectors, height_h_plaquettes   # noqa: E402 REUSE
from e6c_curved_core import desitter_sprinkle, RHO                            # noqa: E402 REUSE
from orientation_core import O3Model, causal_link_graph                      # noqa: E402 REUSE

R_HAT_SUBSTRATE = 2.0     # E6c's curved substrate (R_dS ≈ 1.68 ℓ) -- where frac_B≈0.0117
H_DIAMOND = 4            # E6c's best-sampled magnetic height


# ====================================================================== #
# Orientation ferromagnet on the causal link graph (E1 / O(3))
# ====================================================================== #
def equilibrate_orientation(g, J, seed, n_burn=400):
    """Equilibrate the O(3) Heisenberg ferromagnet (E1) on causal graph g at coupling J.
    Returns (n, M, ez): unit-vector field (n_events,3), order parameter |⟨n⟩|, and the
    order direction ê_z=⟨n⟩/|⟨n⟩| (a fixed reference axis if disordered)."""
    m = O3Model(g, J, seed=seed)
    m.equilibrate(n_burn)
    n = m.n.copy()
    mean = n.mean(axis=0)
    M = float(np.linalg.norm(mean))
    ez = mean / (M + 1e-12) if M > 1e-6 else np.array([0.0, 0.0, 1.0])
    return n, M, ez


def transverse_basis(ez):
    """Orthonormal {e1,e2} spanning the plane ⊥ ê_z (the magnon plane)."""
    ez = np.asarray(ez, float); ez = ez / (np.linalg.norm(ez) + 1e-12)
    a = np.array([1.0, 0, 0]) if abs(ez[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = a - ez * (a @ ez); e1 /= np.linalg.norm(e1) + 1e-12
    e2 = np.cross(ez, e1)
    return e1, e2


def augmented_embedding(pts_embed5, n, ez, lam):
    """7D augmented embedding X̃ = [ X(5D de Sitter) , λ(n·e1) , λ(n·e2) ].
    The two internal axes realise the coupling λ(n_i×n_j)·ê_z as a SPACELIKE bivector
    channel (see module docstring). λ=0 -> exactly the 5D E6c embedding."""
    if lam == 0.0:
        return np.asarray(pts_embed5, float)
    e1, e2 = transverse_basis(ez)
    u = (n @ e1)[:, None]
    v = (n @ e2)[:, None]
    return np.concatenate([np.asarray(pts_embed5, float), lam * u, lam * v], axis=1)


def measure_coupled_fraction(pts_embed5, n, ez, lam, V):
    """B-type fraction of the given diamonds V under coupling λ, on the curved substrate.
    Reuses polygon_bivectors VERBATIM on the augmented embedding. Returns
    (P, n_B, frac_B, mean_e2, mean_b2)."""
    P = int(V.shape[0])
    if P == 0:
        return 0, 0, float("nan"), float("nan"), float("nan")
    Xt = augmented_embedding(pts_embed5, n, ez, lam)
    _, e2, b2 = polygon_bivectors(Xt, V)
    n_B = int(np.sum(b2 > e2))
    return P, n_B, n_B / P, float(np.mean(e2)), float(np.mean(b2))


def build_substrate(N, seed, R_hat=R_HAT_SUBSTRATE, h=H_DIAMOND,
                    max_plaqs=10000, paths_per_source=100, max_pairs=4):
    """E6c curved sprinkle + height-h diamonds (shared across the λ,J sweep for one seed).
    Returns (pts_conf, pts_embed5, g, V, info)."""
    pc, pe, info = desitter_sprinkle(N, R_hat, seed, rho=RHO)
    g = causal_link_graph(pc)
    V = height_h_plaquettes(g, h, max_plaqs=max_plaqs, max_sources=g.n,
                            paths_per_source=paths_per_source,
                            max_pairs_per_pair=max_pairs, seed=seed)
    return pc, pe, g, V, info


# ====================================================================== #
# Self-test: gate G0 (λ=0 == E6c) bit-for-bit; coupling identity; phase probe
# ====================================================================== #
if __name__ == "__main__":
    N, seed = 1500, 1
    pc, pe, g, V, info = build_substrate(N, seed)
    print(f"substrate: N={g.n}  R_dS={info['R_dS']:.3f}  h={H_DIAMOND}  P={V.shape[0]}")

    # (1) GATE G0: λ=0 reproduces the E6c geometric fraction BIT-FOR-BIT (any n, any ez).
    rng = np.random.default_rng(0)
    n_rand = rng.standard_normal((g.n, 3)); n_rand /= np.linalg.norm(n_rand, axis=1, keepdims=True)
    _, e2c, b2c = polygon_bivectors(pe, V)                       # pure E6c (5D)
    frac_e6c = float(np.mean(b2c > e2c))
    P, nB, frac0, _, _ = measure_coupled_fraction(pe, n_rand, np.array([0, 0, 1.0]), 0.0, V)
    assert abs(frac0 - frac_e6c) < 1e-15, (frac0, frac_e6c)
    print(f"OK  G0: λ=0 reproduces E6c bit-for-bit (frac_B={frac0:.5f} == {frac_e6c:.5f})")

    # (2) coupling identity: internal-internal bivector component == ½λ² Σ(n_c×n_{c+1})·ê_z.
    ez = np.array([0.0, 0.0, 1.0]); lam = 1.3
    Xt = augmented_embedding(pe, n_rand, ez, lam)
    A, _, _ = polygon_bivectors(Xt, V[:200])
    A56 = A[:, 5, 6]
    Xv = n_rand[V[:200]]                                          # (200, 2h, 3)
    twist = np.zeros(A56.shape[0])
    m = V.shape[1]
    for c in range(m):
        ni, nj = Xv[:, c, :], Xv[:, (c + 1) % m, :]
        twist += np.cross(ni, nj) @ ez
    twist *= 0.5 * lam * lam
    assert np.allclose(A56, twist, atol=1e-10), np.max(np.abs(A56 - twist))
    print(f"OK  coupling identity: Ã^(5)(6) == ½λ²Σ(n×n')·ê_z (max dev {np.max(np.abs(A56-twist)):.1e})")

    # (3) phase probe: locate the ferromagnet's ordering on THIS curved causal graph.
    print("\nphase probe  M(J) on the R̂=2 causal graph (locate J_c):")
    for J in (0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2):
        _, M, _ = equilibrate_orientation(g, J, seed=seed, n_burn=300)
        print(f"   J={J:4.2f}  |M|={M:.3f}  {'ordered' if M>0.5 else ('critical' if M>0.2 else 'disordered')}")
    print("self-test OK")

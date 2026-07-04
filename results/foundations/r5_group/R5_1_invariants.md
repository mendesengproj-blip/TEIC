# R5-1 -- Representation-theoretic invariants of SU(N)

Numerical (exact, machine-precision) properties of the abstract algebra su(N),
N = 2..8. No TEIC lattice result enters; N is the free input.

| N | group | dim (adj) | rank | fundamental | cubic d^abc (sum d^2) |
|---|-------|-----------|------|-------------|-----------------------|
| 2 | SU(2) | 3  | 1 | **pseudoreal** | **0** (no cubic invariant) |
| 3 | SU(3) | 8  | 2 | **complex** | 13.333 |
| 4 | SU(4) | 15 | 3 | complex | 45.000 |
| 5 | SU(5) | 24 | 4 | complex | 100.800 |
| 6 | SU(6) | 35 | 5 | complex | 186.667 |
| 7 | SU(7) | 48 | 6 | complex | 308.571 |
| 8 | SU(8) | 63 | 7 | complex | 472.500 |

(Generator normalisation Tr(T_a T_b)=½δ_ab verified to <2e-16;
d^abc = 2 Tr({T_a,T_b}T_c), computed by structural null-space / trace, not by
Haar integration.)

## Pre-registered hypotheses -- outcome

- **H_reality** ("SU(3) = minimal simple compact group with a complex fundamental
  rep"): **SURVIVES.** SU(2) is pseudoreal (intertwiner null-dim 1, antisymmetric
  S = iσ₂), SU(3) is the first complex one (null-dim 0).
- **H_anomaly** ("SU(3) = minimal group with nonzero symmetric cubic invariant
  d^abc"): **SURVIVES.** d^abc ≡ 0 at SU(2), nonzero from SU(3) on.
- **H_uniqueness** ("some invariant flips between SU(3) and SU(4)"): **KILLED here.**
  Both selectors flip ON at exactly N=3 with a *single* boundary (N=2|3); neither
  switches again at N=3|4. SU(3) and SU(4) sit on the same side of both.

**The two selectors coincide.** "Complex fundamental" and "nonzero d^abc" turn on
at the *same* place (N=3) -- they are two faces of one fact: su(2) is the unique
simple algebra whose adjoint action admits no symmetric cubic invariant and whose
fundamental is self-conjugate.

Data: `R5_invariants.json`. Reproduce: `python R5_1_invariants.py`.

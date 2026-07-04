# FL3-1 — Initial Configurations

The boosted Skyrmion + anti-Skyrmion pair is built as the quaternion product
`U = U1·U2` of a hedgehog (B=+1) at (−d/2, −b/2, 0) and an anti-hedgehog (B=−1) at
(+d/2, +b/2, 0), each given a translation velocity by the finite-difference body angular
velocity (validated in FL3-V, early-time speed ≈ v). The static lattice mass is
**M_Sk = 285.5** (B = +0.92), so the pair-creation threshold is **2 M_Sk c² = 548.1**
(c = 0.9797 from E2).

## Configuration is correct (no evolution yet)
Every configuration on the charter grid has **B_total ≈ 0** (the +1 and −1 cancel;
residual ≈0.02 is lattice discretisation), **two** resolvable smoothed energy lumps, and
exactly one B>0 blob + one B<0 blob.

## The collision energy is far below threshold — *before a single step*

| v/c | KE₀ (b=0) | KE₀ / 2M_Sk c² |
|---|---|---|
| 0.10 | 0.40 | 0.0007 |
| 0.30 | 3.64 | 0.0066 |
| 0.50 | **10.11** | **0.0184** |
| 0.70 | 19.81 | 0.0361 |

Offsetting the impact parameter (b = 2, 5) barely changes KE₀ (0.0205 at b=5, v=0.5c).
**Across the entire grid the maximum is KE/2M_Sk c² = 0.040 ≪ 1.**

The alternative two-Skyrmion configuration (B=+1,+1) gives B_total ≈ +1.82 (≈ +2), n_peaks
= 2 — the elastic/inelastic contrast for FL3-3.

## Reading
Pair creation requires injecting **two new rest masses** (2 M_Sk c²) of topological
energy. The frontal v=0.5c collision carries **1.8%** of that; even an ultra-relativistic
v=0.7c carries **4%**. This is the E=mc² condition of FL3-5 evaluated up front: it is
**not met by any configuration on the charter grid**. The dynamics (FL3-2) can therefore
only realise annihilation or elastic scattering — never creation — and they do so for the
energetic reason, not a contingent one.

(Note: the boosted lattice profile is not an exact discrete eigenstate, so it radiates part
of its momentum during flight; the *effective* collision energy is even lower than KE₀,
which only widens the gap to threshold.)

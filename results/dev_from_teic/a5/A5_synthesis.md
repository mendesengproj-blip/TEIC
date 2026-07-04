# A5 — Anderson–Higgs on the causal network: synthesis

> Charter: `results/dev_from_teic/A5_ANDERSON_HIGGS.md` (kill criteria pre-registered).
> Direct extension of DEV_FROM_TEIC angle A1. Reuses E1/FM2 (orientation ferromagnet)
> and E5/E7 (causal-set U(1) gauge). Code/data: this folder. Run jun/2026.
> Anti-circularity guard extended to scan `results/dev_from_teic/a5/` and PASSES;
> m_A_DEV appears only in the COMPARISON block below, never in any generator.

## Verdict: **MORTE por NÃO-LOCALIDADE** — the mechanism is real but the causal set
## obstructs it, for a precise structural reason

The DEV vector field A_μ does **not** emerge via Anderson–Higgs on the causal network.
But this is not a null "it failed": A5 *isolates the obstruction*. The Anderson–Higgs
mechanism works perfectly on a regular cubic lattice (G1 PASS); it is the **non-locality
of the causal set** (the same one that obstructed E5's Wilson loops and E7's Coulomb
phase) that specifically prevents the gauge field from eating a Goldstone. This **sharpens
A1** (which found no spontaneous Proca mass in the bare ferromagnet) and **reinforces
Scenario B** (DEV_FROM_TEIC): A_μ mass stays **[EXTERNO-B]**, now with a *mechanism-level*
reason, not just a search failure.

## What was built (and why it is trustworthy)

An **exactly gauge-invariant** abelian-Higgs model: the O(3) orientation ferromagnet of
E1/FM2 with its gauged U(1)_z subgroup (rotations about ê_z) coupled to a U(1) link
field via the **covariant hopping** −J·Re[conj(φ_i) e^{iλθ_ij} φ_j], φ = n⁰+in¹, plus
non-compact Maxwell (1/2g²)Σθ_P². The prompt's linear coupling −λA·(n×n)·ê_z is exactly
the O(λ) term of this (since (n_i×n_j)·ê_z = Im conj(φ_i)φ_j); the exponential form is
invariant for **any** real λ. Gauge invariance verified to machine precision (|ΔS| ≤
7×10⁻¹² cubic, **0.0** causal) **before** any physical measurement, as the charter demands.

## Phase A — G1 gate on a 4D cubic lattice: **PASS** (the mechanism is correctly implemented)

| Test | Result | Meaning |
|---|---|---|
| GAUGE-INV | max\|ΔS\| = 7×10⁻¹² | coupling exactly gauge invariant |
| m_A vs λ (J=2J_c) | 0.0 → 0.30 → 0.47 → **0.63** (λ:0→1) | **massless → massive**: Goldstone eaten |
| m_A vs J (λ=1) | J_c **−0.08** → 2J_c 0.63 → 3J_c **1.07** | mass ∝ condensate; **zero without order** |
| m_A vs g | g=0.5→0.94, g=1→0.63 | stiffer gauge → heavier (as expected) |
| phase boundary | λ≥2 or g≥2: bond 0.69→0.06 | large charge / soft gauge **melt** the condensate (real boundary) |

The gauge-invariant vector correlator C(t)=⟨W_k(t)W_k(0)⟩ is massless at λ=0 and develops
e^{−m_A t} with m_A>0 in the Higgs branch, m_A growing with λ (ordered branch) and
vanishing at J_c. Standard Anderson–Higgs, reproduced. **Gate cleared → causal set.**

## Phase B — the causal set: **MORTE-NONLOCALITY**

Same construction on the Hasse graph of a 3+1D Poisson sprinkling (ρ=4, N=331, reusing
`e5_core.causal_diamond_plaquettes`). The decisive observable is the **orientation** of
the order parameter, split into the **charged** (gauged, in-plane) bond and the
**neutral** (ungauged, n_z) bond:

| λ | charged bond (gauged) | neutral bond (ungauged) | state |
|---|---|---|---|
| 0.0 | **0.91** | 0.00 | in-plane — U(1) **broken** (Higgs would work) |
| 0.1 | 0.005 | **0.91** | neutral-axis escape — U(1) **unbroken** |
| 0.5 | 0.005 | 0.91 | neutral-axis escape |
| 1.0 | 0.004 | 0.91 | neutral-axis escape |

**The mechanism and its obstruction, precisely:**
1. The pure ferromagnet **orders fine** on the causal set (charged bond 0.91 at λ=0) —
   so the failure is *not* a lack of order.
2. The moment λ>0, each event's **~25 charged bonds** (mean Hasse degree 24.7, vs 8 for
   a local 4D lattice, and **growing with N**: 13.3→24.7 from N=137→331) carry
   **incoherent gauge phases** e^{iλθ}. The in-plane condensate cannot form against that
   frustration.
3. So the O(3) ferromagnet **escapes to the ungauged neutral z-axis** (neutral bond
   0.00→0.91). The gauged U(1)_z **stays unbroken → no Goldstone is eaten → the photon
   stays massless → m_A = 0**.
4. **Not a tunable artifact:** a stiffer gauge (g=0.2, β_g=25, near-flat field) does
   **not** rescue the charged condensate (bond ≤0.005). Longer burn-in (2000 sweeps)
   does not change it. The escape is structural.

This is the **same non-locality** that obstructed **E5** (Wilson-loop confinement test)
and **E7** (Coulomb-phase discriminator): the causal future cone has infinite volume, the
Hasse degree grows with N, and there is no Lorentz-invariant local neighbourhood. A5
shows this non-locality **specifically kills the Anderson–Higgs mechanism** by frustrating
the charged condensate — a new, concrete face of the E5/E7 frontier.

## Pre-registered death criterion — which fired

The charter's **MORTE**: "the U(1) field stays massless even coupled to the ordered
ferromagnet — the Goldstone is not eaten — A_μ does not emerge via Anderson–Higgs →
Scenario B reinforced." This fired, **and** the charter's diagnostic clause ("if the
E5/E7 non-locality reappears, document specifically how it obstructs the Higgs mechanism")
is answered: the obstruction is the incoherent-phase frustration of the charged condensate
from the growing causal degree, with the neutral-axis escape as the smoking gun.

## COMPARISON ONLY — the DEV scale (never an input)

The DEV (Paper II/V) needs A_μ massive with m_A ∈ [3.7×10⁻²⁵, 1.2×10⁻²²] eV/c² (a
Proca/Stückelberg vector). A5 asked whether that mass could *emerge* from the causal
network by Anderson–Higgs. It cannot on this substrate (m_A = 0, the U(1) is not broken),
so the DEV's m_A remains **calibrated/external**, consistent with A1 and with the whole
DEV_FROM_TEIC verdict (Scenario B). No DEV number entered any generator; this paragraph is
the only place m_A_DEV appears.

## RESEARCH_MAP update
- New row **A5** (campaign #14). A1's [EXTERNO-B] for A_μ is **strengthened to a
  mechanism-level statement**: not only is there no bare Proca mode (A1), the natural
  field-theoretic route to generate one (Anderson–Higgs) is **obstructed by the causal
  non-locality** (G1 proves the mechanism; Phase B proves the substrate blocks it).
- Adds to the E5/E7 non-locality dossier a **third, independent** manifestation (after
  Wilson loops and the Coulomb discriminator): the Higgs condensate.

## Anti-circularity
No DEV/relativistic number in any generator (`a5_higgs_core`, `a5_causal_core`,
`A5_G1_cubic_gate`, `A5_B_causal`). m_A_DEV only in the COMPARISON block above. Gauge
invariance gated before physics. Fixed seeds; auto-descriptive JSON. Guard
`tests/test_no_circularity.py` scans `results/dev_from_teic/a5/` and PASSES.

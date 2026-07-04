# R5-3 -- Honest synthesis: why SU(3) as the colour group?

```
QUESTION (roadmap R5 / Section 6 #5):
  Is there an analytical criterion -- extending Bott/Cartan + what MIN1-3
  measured for SU(2) -- that FORCES the colour group to be SU(3) rather
  than SU(N>=4)?

R5-1 (representation invariants):
  fundamental rep complex from N=3 on?           YES (SU(2) pseudoreal)
  symmetric cubic invariant d^abc nonzero N>=3?  YES (=0 at SU(2))
  any invariant flips at N=3 | N=4?              NO (single boundary N=2|3)
R5-2 (topology):
  pi_3 (Skyrmion charge) distinguishes 3 from 4? NO (=Z all N, Bott)
  pi_4, pi_5 distinguish 3 from 4?               NO (only 2 from N>=3)
  any PHYSICAL pi_k (k<=5) separates 3 from 4?   NO
  (the lone separator pi_6 = Z6 vs 0 has no 3+1D role)

VERDICT:

[ ] A -- UNIQUE selection: a physical invariant forces N=3 over all N>=4
[X] B -- MINIMAL selection: SU(3) is the SMALLEST group with a complex
         fundamental / nonzero cubic invariant; the selecting REQUIREMENT is
         imported, not derived; topology does not distinguish 3 from 4
[ ] C -- DEATH: no analytical criterion at all; pure phenomenological input
```

## Verdict B, with precision

**The positive (a real minimality theorem).** SU(3) is the **minimal simple
compact Lie group whose fundamental representation is complex** (3 ≠ 3̄) -- or
equivalently, the minimal one carrying a nonzero symmetric cubic invariant
d^abc. The two statements coincide at the same boundary: su(2) is the unique
simple algebra with a self-conjugate fundamental and no cubic invariant; every
algebra from su(3) up has both. Measured exactly (R5-1).

This is the **colour-space analogue of the MIN3 chain**. MIN3 selected SU(2) as
the minimal group supporting *point matter with a conserved charge* (π₃ index +
spin-½). R5 selects SU(3) as the minimal group supporting *a colour charge that
distinguishes matter from antimatter at the constituent level* (complex 3̄ ≠ 3,
so a "quark" is genuinely different from an "antiquark", unlike the real/pseudo-
real SU(2) doublet). Both are **"minimal consistent", not "dynamically derived".**

**The negative (and the honest cost).** Three things must be said straight:

1. **Topology -- the thing TEIC could hope to derive from Bott -- does NOT
   distinguish SU(3) from SU(4)** (R5-2). π₃=ℤ for all N; π₄,π₅ only separate
   SU(2) from the rest. The only homotopy group that separates 3 from 4 (π₆) is
   physically inert. So the selection is *not* topological.

2. **Minimality is not uniqueness.** Nothing makes SU(4),SU(5),... inconsistent
   -- they too are complex, anomalous, confining. SU(3) wins only by being the
   *smallest* group past the N=2|3 boundary. "Smallest with property P" is a
   selection principle, not a no-go theorem.

3. **The requirement P is imported.** "The fundamental must be complex" (matter ≠
   antimatter at the constituent level) is a **phenomenological / structural
   input**, exactly as d=3 is. The TEIC causal network does **not** measure or
   force it: N is hard-wired into `su3_core` just as d=3 is hard-wired into the
   shell measure rⁿ⁻¹. FL1 *assumed* N=3 and then measured confinement, the
   octet, and a colour Skyrmion -- it never selected N=3.

   (Caveat noted for honesty: the SU(2) matter sector already distinguishes B
   from −B by the *sign* of the oriented volume index, so "baryon ≠ antibaryon"
   alone does not force complex reps. The complex-rep requirement is specifically
   about the **constituent colour charge** being non-self-conjugate -- the thing
   that makes a colour-singlet baryon εⁱʲᵏ q_i q_j q_k of N=3 quarks distinct
   from its conjugate. That is a richer input than the SU(2) sign.)

## Relation to the rest of the map

- This is the **group-space twin of DS1-3** (d=3 "by structural exclusion"). Both
  give the observed value as the minimal consistent point of a choice space, and
  both are explicit that this is *selection*, not dynamical *emergence* (T3A/T3B
  killed dynamical emergence of d; no "group attractor" is even formulated, just
  as MIN3 stated).
- It **does not** upgrade FL1's [SÓLIDO] status (FL1 stands on its own measured
  confinement/octet); it closes the *logical hole* the roadmap flagged: "the
  programme proves SU(2) minimal but does not distinguish SU(3) from SU(N≥4)."
  Answer: representation theory distinguishes SU(3) as the **minimal complex /
  anomalous** group; topology does not distinguish at all; the distinguishing
  requirement is imported.

## What would move B → A

A genuine A would need a *physical* invariant (one with a 3+1D role) that is ON
for SU(3) and OFF for SU(4) -- e.g. a consistency/anomaly-cancellation argument
internal to the network that fails for N≥4. None exists here: the cubic anomaly
d^abc grows with N (it does not switch off), and the only homotopy that flips at
3|4 is π₆ (inert). Absent such an argument, the colour group is **SU(3) by
minimality given an imported complex-charge requirement** -- the honest ceiling
of this campaign.

# E6b — Literature scan: causal diamonds of height > 2 in CST

> Pre-measurement step required by the E6b_DIAMOND_HEIGHT prompt ("verificar na
> literatura se existe análise de diamantes causais de altura > 2 em CST —
> Benincasa–Dowker usam altura 2 por padrão — por quê?"). Run jun/2026 via
> WebSearch. Complements `../e6/E6_literature.md` (BD operator line is scalar-only;
> no BD gauge operator exists) and `../e7/E7_literature.md` (gauge-action line).
> Sources at the bottom. The short answer: **the question, posed about the gauge
> 2-cell, has no literature — because the BD line is scalar and uses a different
> object ("order-interval layers") than the gauge plaquette's "height", and the
> minimal gauge plaquette is height-2 by graph-theoretic necessity, not convention.**

## 1. What "height" means here vs. what Benincasa–Dowker actually use

There are two different notions, and conflating them is the trap this note removes:

- **BD "layers" `L_k(x)`** (Benincasa–Dowker 2010; Dowker–Glaser 2013). The discrete
  scalar d'Alembertian `(Bφ)(x) = (4/√6 ℓ²)[−½φ(x) + Σ_k c_k Σ_{y∈L_k} φ(y)]` sums
  over **inclusive-order-interval layers**: `L_k(x)` = events `y ≺ x` whose order
  interval `|{z : y ≺ z ≺ x}|` has **cardinality exactly k−1** (k nested pasts by
  element COUNT). 4D uses the **first four layers** with alternating coefficients
  `(1, −9, 16, −8)`; Dowker–Glaser tabulate the layer count and `a_i^{(d)}` for
  d = 2..7. The "depth" here is a **cardinality** of an interval, not a chain length,
  and it acts on a **scalar** `φ(y)` (one number per event).
- **E6 "height-h diamond"** is a *gauge plaquette*: a closed 4-link loop
  `i→a→k→b→i` built from **two ascending Hasse (covering-relation) paths** of link
  length 2 between a tip pair `i ≺ k`. "Height" here = **longest chain length**
  between the two tips. This is the object whose **area bivector** carries the
  E/B (timelike/spacelike) split — there is no scalar analogue of it.

**Why BD "use height 2".** They do *not*, in the plaquette sense — the question as
posed mixes the two notions. BD use the first **few interval-cardinality layers**
(four in 4D), chosen so the Poisson mean of the alternating sum cancels the divergent
mean-field and converges to `□φ`. The number of layers is fixed by the
*dimension-dependent continuum-limit theorem*, not by any "diamond height". The E6
gauge operator's "height 2" is a separate fact (next section).

## 2. Why the minimal gauge plaquette is height-2 — a graph fact, not a choice

For the **gauge** 2-cell the relevant constraint is purely combinatorial:

> **Every 4-cycle in a Hasse diagram has min→max longest-chain length ≤ 2.**

Proof sketch: a 4-cycle has 4 vertices and 4 covering edges. If its minimum `m` and
maximum `M` were joined by a chain `m⋖p⋖q⋖M` of length 3, then `m,p,q,M` are the four
vertices and `m–p, p–q, q–M` are three edges; the fourth edge must be `M–m`, i.e.
`m⋖M` a **covering** relation — contradicting that `p,q` lie strictly between `m` and
`M`. Hence a 4-link plaquette can only be a **height-2 diamond** (1 min, 2 mids,
1 max — the E6 object) or a **height-1 box** `K_{2,2}` (2 mins, 2 maxs). E6 measured
only the diamond. So "height 2" for the **smallest** plaquette is forced by the cycle
length, not adopted by convention.

**Consequence for E6b.** To probe height `h ≥ 3` one cannot stay at 4-gons; one must
use **larger plaquettes** — here a `2h`-gon formed by two vertex-disjoint ascending
Hasse paths of length `h` between the tips (h=2 reproduces the E6 4-gon). This is the
construction E6b measures. It is the natural generalisation of E5/E6's "two length-2
paths between a tip pair" to "two length-h paths."

## 3. Is there any CST analysis of height > 2 diamonds / larger plaquettes?

**Nothing found that bears on the gauge 2-cell's E/B signature.** What the literature
does have, none of it the E6b object:

- **Order-interval / abundance distributions** (Glaser–Surya "interval abundances",
  Bombelli–Meyer chain counting; "Combinatorial interpretation of the coefficients of
  the causal set d'Alembertian", 2024). These count *k-element order intervals* and
  *m-chains* (paths of length m) as **scalar combinatorial invariants** used to
  estimate dimension, curvature and the BD coefficients. They never assign a
  **spacetime area bivector** to a cell or classify it timelike/spacelike — there is no
  E/B split anywhere in this line, because it is all scalar.
- **k-chains / longest chains** (Myrheim–Meyer dimension; Brightwell–Gregory geodesic).
  Long ascending paths are studied as *length* estimators (proper time), not as the
  boundary of a 2-cell whose enclosed area could be spacelike.
- **The gauge line** (Sverdlov 2008; Sverdlov–Bombelli 2009) builds holonomies around
  **causal diamonds** but, as `../e6/E6_literature.md` and `../e7/E7_literature.md`
  established, only writes an **action**, only on the minimal diamond, never analyses
  taller diamonds, never a smeared operator, never a dispersion/signature question.

So the specific question — *do taller causal diamonds furnish spacelike (B-type)
gauge 2-cells?* — is, as far as this scan reaches, **unasked in the CST literature**.
That is itself informative: it is downstream of the (also absent) BD gauge operator.
The honest prior: there is **no theorem** that a `2h`-gon's area bivector becomes
spacelike at large `h`. Both outcomes (it does / it never does) are original CST
information, exactly as the E6b kill criterion pre-registers.

## 4. Does the BD scalar operator change from height 2 to height 3?

For the **scalar** BD operator the relevant knob is the **number of interval-cardinality
layers**, and yes — it changes with dimension and with the smearing scale (Dowker–Glaser
fix more/different layers per `d`; the smeared `B_ε` mixes layers over a mesoscale `ε`).
But this is orthogonal to the gauge "height": adding layers to the scalar operator does
not create a spacelike 2-cell, because the scalar operator has **no 2-cell at all** — it
sums field *values*, not oriented areas. There is no published "height-3 BD scalar
operator" in the plaquette sense; the closest analogue (more layers) is a different
mechanism (mean-field cancellation), not a magnetic-sector construction. Hence E6b's
height ladder is genuinely new territory for the gauge object and has no scalar
precedent to inherit.

## Sources

- [Benincasa & Dowker, *The Scalar Curvature of a Causal Set*, PRL 104, 181301 (2010) (arXiv:1001.2725)](https://arxiv.org/abs/1001.2725)
- [Dowker & Glaser, *Causal set d'Alembertians for various dimensions* (arXiv:1305.2588, 2013)](https://arxiv.org/abs/1305.2588)
- [Belenchia, Benincasa, Dowker, *The continuum limit of a 4-dimensional causal set scalar d'Alembertian* (arXiv:1510.04656)](https://arxiv.org/pdf/1510.04656)
- [*Combinatorial interpretation of the coefficients of the causal set d'Alembertian* (arXiv:2412.14036, 2024)](https://arxiv.org/pdf/2412.14036)
- [Sverdlov, *Gauge Fields in Causal Set Theory* (arXiv:0807.2066, 2008)](https://arxiv.org/pdf/0807.2066)
- [Sverdlov & Bombelli, *Dynamics for causal sets with matter fields* (arXiv:0905.1506, 2009)](https://arxiv.org/pdf/0905.1506)
</content>
</invoke>

# E6b — Diamond height scan: do taller causal diamonds furnish spacelike 2-cells?

> Direct extension of E6_BD_GAUGE_LORENTZIAN (E6-3/E6-3b). Code: `e6b_diamond_height_core.py`
> (2h-gon construction, reuses `../e6/e6_bd_core.py` for the E/B physics verbatim),
> `E6b_1_height_scan.py` (scan + figure). Data: `E6b_1_height_scan.json`. Figure:
> `E6b_1_height_scan.png`. Literature first: `E6b_literature.md`. Run jun/2026.
> **Pre-registered kill criterion** (from the prompt) checked against the measured data.

## The question, and why it is well-posed

E6-3b nailed the H2 failure to a precise structural fact: **every height-2 causal
diamond is electric**. A diamond `i→a→k→b→i` (two ascending Hasse paths of link length 2
between a tip pair `i≺k`) always contains the timelike past-tip→future-tip extent, so its
area bivector is `A^{0i}`-dominant (`b²<e²`) and the B-type (spacelike/magnetic) fraction
is **0.0000 exactly** across 9 sprinklings. The indefinite `E²−B²` operator has no
magnetic sector to balance the electric one → no `ω=ck` light cone.

E6b asks the natural follow-up: is the exact zero **specific to height 2**, or a property
of **every scale** of the Poisson causal order? A 4-link plaquette can only ever be
height-2 (graph fact: every 4-cycle in a Hasse diagram has min→max chain length ≤2 — see
`E6b_literature.md`). So to probe height `h≥3` we generalise the plaquette:

> **height-h diamond plaquette = a 2h-gon**, the loop closed by two vertex-disjoint
> ascending Hasse paths of link length `h` between a tip pair `i≺k`. h=2 reproduces the
> E6 4-gon exactly.

The E/B classification is **reused unchanged** from `e6_bd_core` (area bivector
`A^{μν}=½Σ_c x_c∧x_{c+1}`, `e²=Σ(A^{0i})²`, `b²=Σ(A^{ij})²`, B-type iff `b²>e²`); the only
generalisation is the cyclic area sum over `2h` vertices instead of 4. A self-test asserts
`polygon_bivectors` reproduces `e6_bd_core.plaquette_bivectors` byte-for-byte on 4-gons,
so no E/B physics is reimplemented. h=2 reproduces E6's **exact 0.0000** (validation
anchor passed).

## Results (heights h=2..6, N≈200/500/1000/2000, 3 seeds, ρ=2)

Pooled over seeds; `wilsonHi` = 95% upper bound (so a "death" claim is bounded); `b2/e2`
= mean per-cell magnetic content. **Best-sampled cells (largest N) are the decisive ones.**

```
   N  h   P_tot    nB   frac_B   ±binom  wilsonHi   b2/e2
 2000  2   30000     0  0.00000  0.00000   0.00013   0.222     <- E6 exact zero reproduced
 2000  3   30000    73  0.00243  0.00028   0.00306   0.142
 2000  4   27502    70  0.00255  0.00030   0.00321   0.112
 2000  5   15407    24  0.00156  0.00032   0.00232   0.088
 2000  6    8312     8  0.00096  0.00034   0.00190   0.079     <- back at the death floor
 1000  3   28486    68  0.00239  0.00029   0.00302   0.128
 1000  6     381     4  0.01050  0.00522   0.02668   0.071     <- 4 cells, P=381: a fluctuation
  500  3   11659    16  0.00137  0.00034   0.00223   0.132
```

Best-sampled (N≈2000) B-type fractions by height:
`h2=0.0000, h3=0.0024, h4=0.0025, h5=0.0016, h6=0.0010`.

Three facts, all decisive:

1. **The height-2 exact zero is BROKEN at h≥3.** Spacelike B-type 2-cells genuinely exist
   in taller diamonds — `frac_B` rises from a literal 0 (h=2) to ≈0.0024 (h=3). This is an
   honest correction to the *literal* E6-3b statement "no spacelike 2-cells exist": they
   exist, but as a rare tail.
2. **The fraction does NOT grow with height — it peaks ~h=3–4 and DECLINES.** At the
   trustworthy N≈2000 cells it goes `0.0024 → 0.0025 → 0.0016 → 0.0010`, sliding back to
   the death floor by h=6. Taller diamonds do **not** become more magnetic; the opposite.
3. **Per-cell magnetic content `b²/e²` shrinks monotonically with h** (0.22→0.08, collapsing
   across all N — right panel of the figure). Even the B-type cells that do appear carry
   *less* relative spacelike area as the diamond gets taller, because a 2h-gon between two
   tips `i≺k` is still bounded by the timelike `i→k` extent, which grows with h.

The single point above 0.01 — `N=1000, h=6, frac_B=0.0105` — is **4 B-cells out of
P=381** (binomial ±0.005, Wilson interval [0.004, 0.027]); the **22× better-sampled**
`N=2000, h=6` cell gives **0.00096**. It is a low-statistics fluctuation, not an
exceedance. No cell with adequate statistics (P≥2000) has a Wilson **lower** bound
anywhere near 0.01.

**N-trend** (the prompt's mandated decisive test, on best-sampled cells): `d(frac_B)/
d(log10 N) ≈ +0.0017` (h=3), `+0.0023` (h=4) — driven mostly by the under-sampled N≈500
point; between the two best-sampled sizes (N≈1000→2000) the fraction is **flat**
(0.00239→0.00243 at h=3). The tail **saturates around 0.002–0.0025**, it does not climb
toward 0.01.

## Verdict (against the pre-registered criterion)

```
PRE-REGISTERED:
  SUCCESS      frac_B > 0.01 at some h            -> report minimal h as "gauge radius"
  DEATH        frac_B < 0.001 at ALL h, even N↑   -> [FRONTEIRA-ESTRUTURAL]
  INCONCLUSIVE small, non-zero, doesn't clear 0.001 robustly -> report values honestly

MEASURED  ->  INCONCLUSIVE (leans structural).
  - NOT success: no statistically significant cell reaches 0.01 (the lone 0.0105 is a
    4-event P=381 fluctuation; best-sampled h=6 = 0.00096). Wilson lower bounds never >0.01.
  - NOT a clean death either: the best-sampled mid-heights (h=3,4) sit at ≈0.0024–0.0025,
    a factor ~2.5 ABOVE the 0.001 floor — the exact-zero of height 2 does not persist.
  - The tail neither grows with height (peaks h=3–4, declines to the floor by h=6) nor
    with N (saturates ~0.0025). Per-cell b²/e² shrinks with h. There is NO usable magnetic
    sector at any tested height.
```

**Physical reading.** E6b *sharpens and partially corrects* E6-3b. The literal claim
"the magnetic sector is exactly empty / structurally absent" was a **height-2 artefact**:
spacelike 2-cells do exist at h≥3. But the corrected statement is, if anything, stronger
for the photon question: the spacelike cells form a **non-growing ~0.25% tail** whose
relative magnetic content *decreases* with diamond size, so a BD-gauge `E²−B²` operator
built on any height-h diamond complex still gets a magnetic term ~400× weaker than its
electric term — far too weak to open a `k²−ω²` zero locus. **There is no "gauge radius" h
that rescues the operator.** The obstruction is not literally "zero spacelike cells" but
"the spacelike cells are a parametrically negligible, non-growing tail" — a *measure-zero*
rather than *empty* magnetic sector. The photon via this specific BD-gauge mechanism
remains blocked on the bare Poisson substrate, now demonstrated across scale (N) and
diamond height, not just at the minimal cell.

## What this changes for E6 / RESEARCH_MAP

- E6 stays **[FRONTEIRA TÉCNICA]** — the kill criterion did **not** strictly fire (DEATH
  required `frac_B<0.001` at all h; the measured h=3,4 sit ≈0.0025). Per protocol an
  INCONCLUSIVE outcome does not flip the tag to [FRONTEIRA-ESTRUTURAL].
- But the diagnosis is **refined**: the E6-3b "exact 0.0000, structural" must be read as
  "exact only at height 2; a non-growing ≈0.25% tail at h≥3 with shrinking per-cell b²/e²".
  The conclusion (no usable B² sector → no light cone) is unchanged and now scale- and
  height-tested. The missing piece remains a **spacelike 2-cell construction that yields an
  O(1) magnetic fraction** — which the natural "taller diamond" generalisation does NOT.

## Anti-circularity

No relativistic literal inserted: the E/B split uses only the embedding time column (the
sprinkling's own causal/time direction), identical to E6; `c` is never used here (this
campaign measures only the bivector signature fraction, as E6-3b did). h=2 reproduces E6's
exact 0.0000 as a validation anchor. The verdict is the pre-registered INCONCLUSIVE branch,
reached by measurement and reported with the small measured values and their statistics,
not adjusted to claim a cleaner death or a success. The lone supra-threshold point is
explicitly identified as a low-statistics fluctuation rather than suppressed. E6/E7 code
untouched; `e6_bd_core` reused, not modified.
</content>

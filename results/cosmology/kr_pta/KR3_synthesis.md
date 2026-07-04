# KR-PTA -- Honest synthesis: direct search for the m_A line in PTA data

```
QUESTION (RESEARCH_MAP Section 6 #10):
  HQ3 showed only THEORETICAL consistency (the m_A KR line lands in the PTA
  band, amplitude "grazes the threshold").  Has the line m_A would produce
  already been SEARCHED FOR and EXCLUDED by the PTAs' published direct searches?

KR1 (signal model, KR 2014):
  f_KR(m) in the PTA band over the window?          YES (m ~ 6e-24..1.2e-22 eV)
  h_c(f=1) at m=1e-23 eV                            2.7e-15  (KR Eq 21)
  timing residual dt(f=1) at m=1e-23 eV            ~25 ns
KR2 (confront published direct searches):
  PPTA-2018 gravitational limit reaches f_max=1 at  m ~ 2.6e-24 eV
                                                    (BELOW the window low edge)
  100%-ULDM excluded anywhere in the window?        NO (f_max = 2.5 .. 2160)
  Lyman-a forces m_A subdominant in the band?       YES (needs m>~1e-21 for 100%)

KILL CRITERION (pre-registered): fires only if the published gravitational
search excludes f=1 across the WHOLE window AND m_A must be ~100% DM there.

VERDICT:

[ ] DEATH      -- PTA direct search rules out the m_A=CDM line in the band
[X] CONSISTENT -- no current PTA constraint bites; line below threshold;
                  PTA is a FUTURE probe (with PARTIAL flavour, see below)
[ ] (PARTIAL)  -- PTA excludes part of the window
```

## Verdict: CONSISTENT (not excluded), with the honest detail

**The direct searches have looked and found nothing that touches m_A.** The
cleanest published gravitational (Khmelnitsky-Rubakov) direct search, PPTA-2018
(Porayko et al., arXiv:1810.03227), limits the local ULDM density to
ρ < 6 GeV/cm³ (95%) at m ≤ 1e-23 eV. Translated to a fraction f = ρ/ρ_local
(ρ_local = 0.4 GeV/cm³), that is **f_max ≈ 15 at m = 1e-23 eV** -- i.e. it does
**not even exclude 100 % local-DM ULDM** there, let alone a subdominant m_A. The
limit tightens toward lower mass (KR strain ∝ ρ/m²) and reaches f_max = 1 only
near **m ~ 2.6e-24 eV, just BELOW the HQ3 overlap window** (≥ 4.1e-24 eV). So
across the entire window the published direct search allows even the maximal
line. The pre-registered kill criterion does **not** fire. NANOGrav-15yr
(arXiv:2306.16219) ran the same gravitational metric-fluctuation search and also
found no signal, improving the reach modestly but not into the f ≪ 1 regime
relevant here.

**Independently, m_A is already required to be subdominant in this band.**
Fuzzy-DM structure bounds (Lyman-α / high-z) need m ≳ 1e-21 eV for ULDM to be
~100 % of dark matter -- two orders of magnitude above the PTA band. So in the
PTA band m_A can only be a small fraction of DM (consistent with FM4's "Lyman →
subdominante"), and the KR line it produces is correspondingly **far below
current PTA sensitivity**. There is no tension and no detection: the
non-detection is exactly what the m_A picture predicts.

**What this changes vs HQ3.** HQ3 was theoretical consistency ("the line lands in
the band; amplitude grazes the threshold"). KR-PTA confronts the **actual
published direct searches** and finds: the threshold the line "grazes" in HQ3 is
*not* reached by the real searches in the overlap window -- the line sits below
it. The upgrade is from "consistent in principle" to **"confronted with the
direct searches: not excluded, below threshold, a future probe."**

## Honesty / declared limits

1. **We did not re-run a PTA pipeline on raw residuals.** A bespoke matched-filter
   line search at the m_A frequencies would need the public timing data and is a
   larger campaign; it is unnecessary for the falsification question, which the
   published exclusion curves already answer. (This is the one residual: a
   *dedicated* line search could in principle reach slightly deeper than the
   collaborations' generic ULDM bound.)
2. **The PPTA limit was extrapolated by a single white-noise scaling**
   (ρ_lim ∝ m², anchored at the quoted 6 GeV/cm³). At the low-mass edge
   (f < 1/T_span, < 1 cycle in the span) the true sensitivity is *worse* than
   this scaling -- so the extrapolation is, if anything, optimistic about
   exclusion; the CONSISTENT verdict is robust (real limits are weaker, not
   stronger).
3. **ρ_local = 0.4 GeV/cm³** assumed; KR Eq (21) is normalised to 0.3, carried
   explicitly. m_A window and SPARC bound are from Paper II/FM4, **not** tuned to
   PTA.

## Bottom line for the map

The m_A dark-matter line is **not excluded** by existing PTA direct searches and
is **predicted to be undetectable now** (subdominant in the band by Lyman-α). PTA
remains a genuine **future** discovery channel for the high-mass tail of the m_A
window as sensitivity improves. HQ3's [FRACO]/[IDENTIFICADO] status is unchanged
in kind but sharpened: the "direct search never done" residual is now closed at
the level the public data allow.

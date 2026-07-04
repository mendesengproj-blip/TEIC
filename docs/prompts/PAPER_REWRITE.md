# PAPER_REWRITE — reframing `paper/main.tex`

> Record of the reframing of the TEIC paper from a *reproduction study* to a
> *theory with an independent route and an observational bridge*. **No numerical
> result changed** — R1–R3, e6–e11, and D1–D3 are byte-for-byte the same values.
> Only the framing (the paper's voice) and one new results section changed. The
> paper compiled clean before and compiles clean after.

---

## What changed (W1–W7)

| Task | Change | Location in `main.tex` |
|---|---|---|
| **W6** | New title: "Emergent Lorentzian geometry, matter dynamics, and a modified gravity connection…" — dropped "a reproduction study". | `\title` |
| **W1** | New abstract: opens "We derive…" (was "We test a model…"). Adds the D1–D3 matter-dynamics result and the modified-gravity bridge. **~216 words (< 250).** | `abstract` |
| **W2** | New introduction: three affirmative paragraphs — (1) the expansion-centres picture, (2) "we derive… we identify… we establish…", (3) honest coincidence with CST + the one result the route makes natural. | `\section{Introduction}` |
| **W3** | **New section** `Matter dynamics and the modified gravity bridge` (`\label{sec:matter}`), inserted between curvature and discussion, with three subsections (BD action + source → Poisson; unconstrained Monte Carlo → ρ(r); the weld relation) and the D3 figure. | after the curvature verdict |
| **W4** | Discussion rewritten as three points: *what is new* / *what coincides with CST (a fact, not the verdict)* / *the conceptual route*. | `\section{Discussion}` |
| **W5** | Limitations: corrected the now-false "there is no matter dynamics"; **added items (6)** (weak-field only; full √(1−2M/r) kinematic; horizon open) **and (7)** (weld relation linear-regime, nonlinear/vector sector open). | `\section{Honest limitations}` (`\label{sec:limitations}`) |
| **W7** | Added `Metropolis1953` and `Regge1961` to `refs.bib`; both cited (MC paragraph; limitation (6)). | `refs.bib`, `main.tex` |

The D3 figure was copied to `paper/figures/D3_MC.png`.

## What did NOT change (by rule)

- **Every number:** correlations `0.9998 / 1.0000 / 0.9991`, errors `0.21% / 0.62% /
  0.06%`, dimensions `2.006 / 4.004`, curvature `−1/96` at `23.5σ`, exponent `−1.02`.
  Verified present and unchanged after the rewrite.
- R1–R4, e6–e11 (interference, growth dynamics, Sorkin operator, two-floor
  structure, vector fields, the negative Wilson/`f(θ)F²` bridge) — text and verdicts
  intact.
- The CST-equivalence statement (kept — as a stated fact, not the conclusion) and the
  anti-circularity protocol.
- The honest limitations of section 10 (expanded, not removed).

## Framing rules honoured

- The modified gravity theory is **not named** (under review): "a class of
  scalar–vector–tensor modified gravity theories" / "galactic rotation curves" (no
  specific dataset size asserted in-paper).
- **No inflation:** D1–D3 are presented with explicit limits — weak field, `d=3` as
  geometric input, only the leading Newtonian term dynamical, the full Schwarzschild
  profile *kinematic*, the horizon left open.
- The paper is **stronger, not longer**: the abstract and introduction are the same
  size; W3 adds ~2 pages; the voice moves from defensive to affirmative.

---

## Verification (W8)

```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

| check | result |
|---|---|
| compiles (all passes exit 0) | ✅ |
| undefined references / citations | ✅ none |
| critical warnings | ✅ none (only a pre-existing empty-journal note for `Meyer1988`; one 11.6 pt overfull hbox in a pre-existing paragraph) |
| abstract word count | ✅ ~216 (< 250) |
| new section figure with label | ✅ `figures/D3_MC.png` renders |
| `tests/test_no_circularity.py` | ✅ PASSED |
| R1–R3 and all numbers unchanged | ✅ verified by grep |

The resulting paper opens with *"We derive…"*, carries the matter-dynamics result as
its own section, documents the modified-gravity bridge with its boundary of validity
stated precisely, keeps every honesty caveat, and reflects what was actually built:
not a shadow of causal set theory, but a theory that reached the same place by its own
route — and went further.

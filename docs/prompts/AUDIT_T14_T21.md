# AUDIT_T14_T21 — matter as causal connectivity (TEIC-GE)

> **Audit, not a new result.** Validates/refutes the T14–T21BIS experiments in
> `../TEIC-GE/results/teic_st/T14/`, whose synthesis claims: *"particles, mass, energy,
> time, gravity and motion are macroscopic descriptions of the same microscopic causal
> network."* Does **not** modify TEIC R1–R3 or e6–e11. Artefacts in
> [`results/audit/t14_t21/`](results/audit/t14_t21/). Golden rule obeyed: **every
> load-bearing experiment was re-implemented and re-run** (with the missing seeds and
> error bars) before judging.

## The claim, and the standard
The claim is extraordinary, so it needs extraordinary evidence. The audit keeps one
distinction throughout: **"the network produces X" ≠ "X is the network."** Newton did
not show gravity explains the tides by elegance; he computed the force and the numbers
matched. The question is whether T14–T21 *computed* its six identities or *interpreted*
them.

## What was found

**The tooling is GE's fork of TEIC's core** (`causal_core.py`), and all of T14–T21 lives
in the **`teic_st` scalar-tensor phase** that `AUDIT_GEMINI.md` already flagged as the
lighter, partly-circular one. Every generator is 32–118 lines, one numpy pass, $n=30$–
$1000$, **single-seed (42) or unseeded, no error bars, no anti-circularity guard**.

**Reproduction (`INV2_reproduce.py`, 20 seeds) verdicts:**

| theme | claim | reproduced result | status |
|---|---|---|---|
| **relativity** (T18/T19) | time dilation $1/\gamma$, $E\propto\gamma$ emerge | the "measurement" is a hand-translated Gaussian blob; it fits $e^{-0.52v^2}$ at RMSE **0.003** vs **0.20** for $1/\gamma$, and the fit **depends on the arbitrary blob width**; $v$ is imposed by hand | **not a derivation** (not circular: γ only in comparison) |
| **mass** (T14–16) | $m=\langle k\rangle$, universal | cost/⟨k⟩ = **0.245–0.418** (GE: 0.24–0.29 from single shots); cost and ⟨k⟩ **both count links/event** | **near-tautological correlation** |
| **gravity** (T17) | Schwarzschild $1/r$ from connectivity | the Poisson operator is **hard-coded**; $|\text{corr}|\approx1$ with $1/r$ for *any* central source | **circular**; a less-rigorous rediscovery of TEIC **D1–D3** (corr 0.9991) |
| **particles** (T20/21BIS) | spin-1/2, Pauli, Standard Model | hand-drawn helices; "exclusion" = link saturation (~15) of two fixed curves; no spin/statistics test | **interpretation of imposed structures** |

**The six claims, graded** (A=calc+verified, B=calc not verified, C=argument, D=reinterpretation):

| time | gravity | mass | particles | energy | motion |
|---|---|---|---|---|---|
| **D** (=R1–R3) | **D** (=D1–D3) | **B** | **B→C** | **C** | **C** |

**No claim reaches A.** Two are TEIC's own already-established results re-dressed (time,
gravity); two are calculated-but-unverified (mass, localized structures); two are
arguments (energy, motion).

## The honest bottom line

> **The direction is right; the tense is wrong.** The TEIC-GE T14–T21 work shows that
> **causal connectivity ⟨k⟩ is a natural microscopic correlate of inertia** and that an
> **excess of connectivity sources a $1/r$ potential under the (assumed) Poisson law** —
> reproducing, in connectivity language, TEIC's own proper-time (R1–R3) and Newtonian-
> profile (D1–D3) results. Hand-built helical/braided structures form separable
> topological classes. These are **suggestive framings**, not demonstrations. The work
> does **not** derive particles, Lorentz-invariant mass, energy conservation, spin, or
> the Standard Model. The maximal claim that these six things **are** causal
> connectivity is an **interpretive synthesis in the correct direction but well beyond
> what the calculations establish** — single-shot, error-bar-free measurements of
> imposed structures, with the decisive tests (Lorentz invariance, dynamical stability,
> Noether conservation, spin-statistics, geodesics) absent.

This is the **`AUDIT_GEMINI.md` pattern repeating**: sound fundamentals and a correct
direction, **oversold in the `RESUMO_FINAL` summaries** ("CONFIRMADA", "validado
empiricamente", "unificação completa"). Recommendation: **use the framings** (⟨k⟩ as an
inertia correlate; connectivity as a Poisson source), **reject the "is/confirmed/
unified" language**, and note that the strongest two themes (time, gravity) are already
TEIC's own R1–R3 / D1–D3 — done there with far more rigor.

## What would move the claims toward A
Stable localized states with a conserved charge and a derived Dirac/Klein–Gordon
equation; a mass definition independent of "links/event" shown Lorentz-invariant with
$E^2=m^2c^4+p^2c^2$; Noether energy conservation; a real $2\pi$-vs-$4\pi$ spin test; the
$1/r$ **without** hard-coded Poisson (TEIC D3 already does this); and a derived
geodesic/F=ma. Until then the minimal honest statement in `INV6_synthesis.md` (d) stands.

## Documents
| file | content |
|---|---|
| [`INV1_inventory.md`](results/audit/t14_t21/INV1_inventory.md) | full census + calculation→conclusion map per T |
| [`INV2_reproduction.md`](results/audit/t14_t21/INV2_reproduction.md) · `INV2_reproduce.py` | 20-seed reproduction of the four critical themes |
| [`INV3_claims.md`](results/audit/t14_t21/INV3_claims.md) | A/B/C/D grade for each of the six claims |
| [`INV4_circularity.md`](results/audit/t14_t21/INV4_circularity.md) | anti-circularity checklist; the T17 coded-Poisson case |
| [`INV5_novelty.md`](results/audit/t14_t21/INV5_novelty.md) | new vs reinterpretation vs extrapolation |
| [`INV6_synthesis.md`](results/audit/t14_t21/INV6_synthesis.md) | honest answers to (a)–(d) |

Reproduce: `python results/audit/t14_t21/INV2_reproduce.py` (~6 s; writes
`INV2_reproduce_data.json`). TEIC's own guard is unaffected: `python
tests/test_no_circularity.py` still passes (this audit adds only files under
`results/`).

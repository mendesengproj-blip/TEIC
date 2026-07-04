# C1 — TEIC ≡ Khoury? synthesis: the equivalence is a deep-MOND *limit*, not a phonon identity

> Charter: `docs/prompts/C1_KHOURY_EQUIVALENCE.md` (kill criteria pre-registered).
> Item R3 of `RESEARCH_MAP.md` / Path C1 of `CONVERGENCE_PATHS.md` (rank 2).
> Data/code: `C1_khoury_equivalence.py`, `.json`, `.png`. Run jun/2026.

## Verdict: **LIMIT EQUIVALENCE (partial)** — sharpens Fase 2, kills a loose claim

The TEIC↔Khoury equivalence lives in the **longitudinal response sector** (the
deep-MOND anomaly χ∥~h^{−1/2}), **NOT** in the tree-level transverse phonon action.
The O(3) magnon — the ω=ck mode of E2 — is a **quadratic** Goldstone (∝X), **not**
Khoury's postulated X^{3/2}. So the often-stated "the TEIC magnon *is* Khoury's
phonon" is **false**; what is true (and rigorous) is that all three frameworks share
the **deep-MOND limit** by the Milgrom/AQUAL theorem (Fase 2).

## K1 — analytic (the conceptual core)

1. **O(3) around ⟨n⃗⟩:** 2 transverse Goldstones + 1 longitudinal mode. The transverse
   kinetic term is **quadratic** (L = ½ρ_s(∂π)²), giving ω=ck — exactly E2's measured
   massless magnon (c=0.98). Quadratic ⇒ action ∝ X (n=1), **Newtonian/linear response**.
2. **Khoury's phonon is X^{3/2}** (n=3/2) — a **fractional, non-analytic** power put in
   by hand via the superfluid equation of state P∝ρ³. A *free/interacting Goldstone
   kinetic term is not fractional*; integrating out the massive longitudinal mode
   generates only **analytic** corrections (X², higher derivatives), never X^{3/2}.
3. **Where the deep-MOND non-analyticity lives:** in the O(3) model it is the
   **longitudinal coexistence anomaly** χ∥~h^{−1/2} (Brezin–Wallace) — an **emergent
   IR/loop effect** (the transverse Goldstone fluctuations dress the longitudinal
   susceptibility), not a tree-level kinetic term.
4. **Milgrom theorem (Fase 2):** deep-MOND scale-invariance (g→√(g_N a₀)) forces the
   unique form L∝|∇Φ|³ ≡ X^{3/2}; DEV (DBI), Khoury (superfluid EoS) and TEIC (χ∥
   anomaly) all share it **in the limit**, by different routes.

**Conclusion of K1:** the charter's first death criterion — "if the transverse action
is NOT ∝X^{3/2} → equivalence fails in the phonon sector" — **fires informatively**:
the transverse phonon is ∝X (quadratic). The equivalence is therefore a **deep-MOND
limit** statement in the **longitudinal response**, which Khoury postulates in his
phonon EoS and TEIC realises as an emergent IR anomaly.

## K2 — numerical discriminator (O(3) ferromagnet, fm2_core, L=16, 16 seeds)

Measured on the SAME ordered lattice, both susceptibilities vs the external field h
(↔ gravitational gradient g):

| Sector | Estimator | Exponent | Meaning |
|---|---|---|---|
| **Longitudinal χ∥** | V·Var(m_par) | **h^{−0.37}** | deep-MOND anomaly (FM2-1: −0.4±0.1; ideal −0.5) |
| **Transverse χ⊥** | Ward: ⟨m_par⟩/h | **h^{−0.98}** | Goldstone/magnon (∝X), ≈ h^{−1} |

**Distinct exponents (−0.37 vs −0.98)** → the deep-MOND non-analyticity is in the
**longitudinal** sector, not the transverse phonon. Gate G0 passes (χ∥ reproduces
FM2-1). 

**K2-ESCALA:** the candidate "Λ" (Khoury's decay constant) is the spin stiffness ρ_s;
measured ρ_s(J) spans 0.25→1.16 over J=0.9→2.2 — it **rides on the coupling/action
normalisation** (external). So even the response-sector equivalence is **"form
equivalent, scale external"**: a₀ absolute stays external (as VS5/C3/CR3 already fixed).

## Honest correction logged (transparency, project discipline)

A first pass used the **fluctuation** estimator χ⊥ = V·Var(M_x), which **saturates** at
small h (4.2→5.96, exponent only −0.26) because the transverse correlation length
ξ⊥~1/√h **exceeds the box** L=16 — a finite-size artefact, not the physics. The
**Ward identity** χ⊥ = ⟨m_par⟩/h (the rigorous transverse susceptibility in the broken
phase, Goldstone theorem) is not finite-size-limited and gives a clean h^{−0.98}. The
verdict uses the Ward estimator; the fluctuation one is reported with its saturation
for transparency. (Same finite-size lesson as the FLR confinement indicator — fix to
the physically correct estimator, document, do not adjust to force an outcome.)

## What this resolves (RESEARCH_MAP update)

- **R3 / C1 closed (partial positive).** Seção 4.2 (a₀ / Khoury) and Seção 5 of the
  convergence: the equivalence is a **deep-MOND limit in the longitudinal sector**,
  confirmed and sharpened; the magnon≠Khoury-phonon distinction is now measured.
- **a₀ remains [EXTERNO-B]** — strengthened, not weakened: the deep-MOND coefficient
  rides on ρ_s(J,K). The implication flagged in the map holds: since DEV≡Khoury in the
  deep-MOND limit, Khoury's a₀ is external by the same Milgrom-theorem structure.
- **Did NOT establish** a tree-level phonon identity (it does not exist) nor any
  derivation of an absolute scale. K3 (vortices→physical circulation) is therefore
  **deferred to C6**, per the charter (it was gated on a tree-level closure that did
  not occur).

## Anti-circularity
No MOND/SI number in the generator (a₀ COMPARISON ONLY); engine is the E1 O(3)
ferromagnet (fm2_core); fixed seeds; G0 reproduces FM2-1 before any claim; guard
`test_no_circularity.py` passes. `C1_khoury_equivalence.json` keeps both χ⊥ estimators.

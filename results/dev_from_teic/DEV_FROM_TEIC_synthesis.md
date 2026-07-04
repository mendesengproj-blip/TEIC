# DEV_FROM_TEIC — synthesis: does the DEV *derive* from the TEIC? (Scenario A vs B)

> Charter: `results/dev_from_teic/DEV_FROM_TEIC.md`. Four NEVER-TRIED angles, run in
> order A1→A2→A3→A4, each built on already-measured campaigns (FM2-1, C1, D3/R3/MG1),
> not repeating dead ends (a0 via D3D, ℏ via C5). Code/data in this folder. Run jun/2026.
> Anti-circularity guard `tests/test_no_circularity.py` extended to cover this campaign
> and PASSES; a0, β, η-window appear only in COMPARISON/verdict sections, never in any
> data generator.
>
> **Follow-up A5 (Anderson–Higgs, `a5/A5_synthesis.md`):** tested the one mechanism that
> all four dead-ends point to in common — does the link-U(1) acquire a mass by eating a
> ferromagnet Goldstone (→ A_μ)? The mechanism is correct (G1 cubic-lattice gate PASS),
> but it is **obstructed by the causal-set non-locality** (MORTE): the charged condensate
> cannot form against ~25 incoherent gauge phases per event, so the order escapes to the
> ungauged axis and the U(1) stays unbroken (m_A=0). This strengthens A1's [EXTERNO-B]
> for A_μ to a *mechanism-level* statement and reinforces Scenario B.

## Verdict: **CENÁRIO B** (two compatible but independent theories), with one partial
## form-correlate (A2)

The DEV's **numerical parameters** — the vector mass m_A, the scale a0, the coupling
β, the slip value η — are **NOT derived** from the TEIC causal network. What recurs in
every angle is the same pattern the program already knew from C1: a **network correlate
of the FORM exists, but the absolute SCALE/VALUE is external**. So the DEV remains the
**effective theory of the same causal ferromagnet** in *form*, but a0/β/m_A/η are
**calibrated, not emergent**. This confirms and sharpens — does not overturn — the prior
state (C1 "form equivalent, scale external"; a0 [EXTERNO-B]; E4 orientation-photon morto).

| Angle | Question | Result | Status |
|---|---|---|---|
| **A1** | does the vector A_μ emerge? | longitudinal gap **closes** ∝h^0.31 (= Brezin–Wallace, the deep-MOND anomaly); no spontaneous Proca mass | **[EXTERNO-B]** |
| **A2** | does a0~cH0 have geometric origin? | h_sat **does** track stiffness (h_sat∝ρ_s^−0.48, R²=0.90) but **opposite sign** to the hypothesis X0∝+ρ_s(J−J_c); absolute a0 external | **[INCONCLUSIVO]** (weak form-correlate) |
| **A3** | does β come from the ferromagnet? | ρ_s/K=0.34 at the operating point J0=1 — **48×** β; reaches β only at J_c (near-critical fine-tuning) | **[EXTERNO-B]** |
| **A4** | does the slip η have a derivable form? | Skyrmion anisotropic-stress slip is **O(1)** (interior 31%, exterior plateau 61%) — a genuine slip in FORM, ~15× the DEV window; needs the absent A_μ | **[EXTERNO-B]/[INCONCLUSIVO]** |

## A1 — A_μ as the massive longitudinal mode (NEGATIVE)

Measured the static mass gap m² from the equal-time structure factor 1/S(k)=k²/A+m²/A
(the rigorous equilibrium-MC observable: gap = inverse correlation length = ω(k→0)),
separately in the longitudinal (n·M̂, the A_μ candidate) and transverse (2 Goldstone)
channels of the E1 O(3) ferromagnet, L=16, 12 seeds, h∈{0.3,0.1,0.03,0.01}.

- **G0 PASS**: transverse is gapless — m²_⊥∝h^0.76 → 0 (the E2 magnon, field-gapped).
- **The longitudinal gap also CLOSES**: m²_∥∝h^**0.31** → 0. The exponent ≈ C1/FM2-1's
  χ∥~h^{−0.37}: m²_∥=A/χ∥, so the closing longitudinal gap is the flip side of the
  diverging deep-MOND susceptibility — the **same Brezin–Wallace coexistence anomaly**.
- Honest nuance: the longitudinal mode stays parametrically ~36× heavier than the
  transverse (ratio rises 6.6→36 as h→0), a clear scale separation — but **not** a
  surviving gap. The would-be A_μ mass is **field-induced (∝h^0.15), not intrinsic**.

A_μ is not the bare amplitude mode of the TEIC ferromagnet → **[EXTERNO-B]**, with a
precise structural reason consistent with E4 (orientation photon morto).

## A2 — geometric origin of a0 (PARTIAL form-correlate, scale external)

Extended FM2-1's χ∥(h) to a J-scan (J∈[0.75,1.8]); h_sat = the response knee (χ∥=2χ_N).

- **G0 PASS** (χ∥ rises toward small h, deep-MOND reproduced).
- h_sat **is a genuine internal network scale**: it tracks the spin stiffness with
  best fit **h_sat∝ρ_s^−0.48, R²=0.90** — so a0's FORM is not an arbitrary external
  number, it has a network correlate.
- **But** (honesty): the relation has the **opposite sign** to the prompt's hypothesis
  X0∝+ρ_s(J−J_c) (h_sat *decreases* with stiffness), so the specific hypothesized law is
  **not** supported; R²=0.90 over 5 points is marginal; and the absolute a0 still needs
  the lattice→SI unit map (the external scale C1/D3D already declared external).

Net: weak positive on the form, negative on the specific law and on the absolute scale
→ **a0 stays [EXTERNO-B]**; angle status **[INCONCLUSIVO]**.

## A3 — β from the ferromagnet stiffness (NEGATIVE)

Measured ρ_s(J)/K over a fine grid (K=1, the MG1/D3D gravity-sector normalisation,
declared **[ASSUMIDO]**; β=0.0070 COMPARISON only).

- At the **physical operating point J0=1.0** (the vacuum used throughout E1→MG1):
  **ρ_s/K=0.336 = 48× β**.
- ρ_s/K equals β only at **J0=0.657 ≈ J_c=0.650** (tuning 0.02 — essentially *at*
  criticality, ρ_s→0): unnatural fine-tuning.

No reasonable operating point gives β; with the unit map also assumed → **β stays
[EXTERNO-B]**. Consistent with C1's K2-ESCALA (the deep-MOND coefficient rides on ρ_s/K).

## A4 — gravitational slip η=Ψ/Φ (NEGATIVE)

The hedgehog orientation field ⟨n⃗(r)⟩=(sinF·r̂,cosF) carries anisotropic stress
Π(r)=p_t−p_r (sigma-sector, rigorous, exterior-dominant; E4 stress a declared
subleading omission). Fed Φ (source ε) and Φ−Ψ (source Π) through MG1's BD relaxer
(same κ ⇒ η convention-free); e_sk=0.5 Skyrmion, **G0 PASS** (Φ exterior ∝1/r).

- The slip is **O(1)**: interior |η−1|≈31%, exterior a **constant plateau ≈61%**
  (∫Π/∫ε=−0.61, the anisotropic stress has a non-zero monopole). A genuine slip in
  **FORM** (constant exterior plateau, like the DEV η=const), but ~**15×** the DEV
  window [2.2%,4.1%].
- The orientation tilt 1−cosF(r)~r^−5.1 and Φ(r)~r^−0.9 have **different falloffs**, so
  ⟨n⃗⟩/θ is not the constant ratio of a DEV slip.

The Skyrmion's intrinsic slip is a **relativistic-soliton / local-baryon** effect, not
the weak-field galactic slip the DEV predicts — and the DEV's galactic η is a
**vector-sector (A_μ) effect, which A1 showed does not emerge** → η stays
**[EXTERNO-B]/[INCONCLUSIVO]**. (Caveat: the local baryon slip is conceptually related
but not identical to the DEV's effective galactic slip.)

## What this means for the program (RESEARCH_MAP update)

- **Scenario A (one unified theory deriving a0/β/m_A/η) is DISFAVOURED.** The four
  never-tried angles do not deliver the DEV's numbers from the network. The unification
  paper TEIC→DEV can be written, but with the **central honest caveat**: the deep-MOND
  *form* (C1) and the matter→gravity *form* (MG1) emerge; **a0, β, m_A and η are
  external/calibrated**, by precisely characterised structural reasons (not mere
  search failure):
  - **A1/A_μ**: the d=3 Goldstone dressing makes the amplitude mode gapless (the same
    anomaly that *gives* deep-MOND) — no spontaneous Proca mass.
  - **A2/a0**: the saturation scale is a real network quantity (∝ρ_s^−0.5) but the
    absolute value needs the lattice→SI map; the proposed X0∝ρ_s(J−J_c) law is wrong-signed.
  - **A3/β**: at the physical vacuum ρ_s/K is ~50× β; β requires near-critical tuning.
  - **A4/η**: a slip plateau exists but is O(1) (a baryon, not a galaxy) and the DEV's
    galactic η needs the absent A_μ.
- This is **Scenario B confirmed** at the level of derived parameters, with **one
  partial form-correlate (A2)** worth a footnote. It coheres with the whole map: C1
  (form equivalent, scale external), a0/f_A/m_A [EXTERNO-B], E4 photon morto, T3C ℏ
  proportion-only. The TEIC and DEV are **two compatible but independent theories**;
  their shared content is the *form* of the deep-MOND/matter-gravity sector, not the
  *scales*.

## Anti-circularity
No DEV parameter enters any data generator. The generators (`structure_factors`,
`chi_curve`/`knee_hsat`, `rho_of_J`, `skyrmion_stress`+`bd_solve`) use only J, h, ρ_s,
K and the Skyrmion profile F(r) of the causal network. a0=1.2e-10, β=0.0070, η∈[2.2%,
4.1%] appear ONLY in COMPARISON/verdict blocks. The guard `test_no_circularity.py` was
extended to scan `results/dev_from_teic/` and PASSES (no dilation formula, no complex
literal in generator code). Fixed seeds; auto-descriptive JSON per angle.

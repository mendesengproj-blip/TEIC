# AB5 — The weakest bridge result (ranked by the numbers)

**Task.** Identify, honestly, the bridge result most vulnerable to a referee — not the one
that *looks* weak, but the one the *numbers* expose. `AB5_weakest.py` loads the 20-seed
audit data (AB1/AB2/AB3) and scores each candidate by how close it sits to "a referee could
reject this."

## Table: RESULTADO | CRÍTICA MAIS FORTE | RESPOSTA

| Vuln. | Result | Strongest critique | Response |
|---|---|---|---|
| **0.85** | **BD5: Lorentz restoration (SNR≈1)** | "You claim BD smearing *restores* Lorentz invariance, but show only numbers **consistent with zero** at SNR<2 — and with the **wrong sign**. A non-detection is equally consistent with *no* restoration: a null result dressed as success." | **Fully conceded — and this is how BD5 already reports it.** The signature is *not* positively resolved (SNR<2, mis-signed, no ε helps). The honest claim is narrower: smearing *removes* the gross Euclidean anisotropy (AB3 BD3: a_t/a_x 4→O(0.1)) and the obstruction is the **physical** □/(2ερ) variance wall. Closure is computational, flagged as the **risk outcome**. |
| 0.55 | E/B≈3 (raw-operator Lorentz violation) | "The theory *confidently* predicts an order-1 Lorentz violation (E/B = 3.25 ± 0.10, ~22σ from 1) — ruled out experimentally to ~10⁻²⁰. Dead on arrival." | This is the **raw unsmeared** operator (positive-definite second moment, AB1). The cure — the sign-alternating BD operator — is identified and *does* collapse the anisotropy (AB3). E/B≈3 is a property of the bare operator, not the physical prediction; what's unshown is the positive restoration (→ BD5). |
| 0.40 | "All DEV operators emerge" (form-completeness) | "Completeness is *structural*: F² only appears once you *add* a plaquette term whose weight λ_p is **free** — like the DEV's free K. You matched the *form*, not the coefficients." | Correct and stated (W4): the bridge is **form-complete, not calibration-complete**. Every DEV operator appears with the right structure, the Stückelberg ratios are **locked** (1,2), there are genuine extra quartics (AB1: C_q at 9–17σ) and **no forbidden** higher-derivative term (AB2 W4). The free λ_p is the one honest gap, identical to the DEV's K. |
| 0.35 | C₂/C₁=1, C₃/C₁=2 | "Not a derivation: 1 and 2 are forced by a *single* cosine (a perfect Stückelberg square). Any single-cosine model gives them; the geometry isn't tested." | Conceded and stated (C2/AB1): the ratios are **algebraic** (zero seed variance); the geometry enters only as the scale κ (which *does* vary seed-to-seed) and the anisotropy λ. The claim is "the minimal action = the gauge-invariant Stückelberg/Proca *special case* of the DEV," not "the geometry derives 1 and 2." |

## Weakest result (AB5)

> **BD5 — the Lorentz-restoration claim (SNR≈1).** It is the result a referee can most
> credibly reject, because it is a **non-detection underpinning the central "Lorentz
> restoration" narrative**: the smeared dispersion is consistent with zero at SNR<2 and
> mis-signed at every ε. The audit's recommendation matches the original BD5 framing —
> **state it as the risk outcome**: smearing demonstrably *removes* the Euclidean anisotropy
> (BD3) and the obstruction is identified as a *physical* computational wall, but positive
> Lorentz restoration is **not** demonstrated and must not be claimed.

The good news from the audit: the *other* three candidates all survive with their honest
framings intact, and the two strongest single numbers — the locked ratios (zero variance,
AB1) and E/B≈3 (AB2) — are exactly as reported. The bridge's vulnerability is concentrated
in the one place the original synthesis already flagged.

## Output
`AB5_weakest.py`, `AB5_weakest_data.json`.

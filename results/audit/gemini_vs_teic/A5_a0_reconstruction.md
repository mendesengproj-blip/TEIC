# A5 — Reconstruction of Gemini's a₀ "derivation"

The most consequential claim in the user's summary is "a₀ foi derivado." Reconstructing
it from the files shows it is **not a derivation**. Gemini has **two contradictory
statements** about a₀, in two phases.

## Gemini phase 1 (fundamental, T2) — a₀ NOT derived

Algorithm (reproduced): sprinkle a growing network; measure the only intrinsic scales.
- The single intrinsic length is the discreteness scale $\rho^{-1/d}$; $X_0\propto\rho$
  (UV).
- The boundary ("now"-front) bias $\langle B\cdot1\rangle$ does **not** scale as $1/T$
  (reproduced: $B_{\rm end}\cdot T$ = 3.6, 7.4, 55, 46 — not constant).
- Conclusion: **"C) Nenhuma escala IR emerge naturalmente."** $H\sim1/T$ gives the right
  *order of magnitude* "by definition of $H$" but **"sem acoplamento dinâmico derivado."**

This is **identical to TEIC's C3**: $X_0\propto\rho^{1}$ (UV), $a_0\sim cH$ **not
supported** by the network — a coincidence of magnitudes, not a derivation.

## Gemini phase 2 (scalar-tensor, ST3/T11/T14) — a₀ ~ c/T POSTULATED

Algorithm:
1. `ST3_cosmology.py`: writes $H=\dfrac1V\dfrac{dV}{dT}=\dfrac{d}{T}$ for a Minkowski
   diamond ($V\propto T^d$) — pure analysis; then the line *"For a0 ~ cH link: a* =
   4c/T"* simply **asserts** the MOND coincidence. (The script's
   `analyze_boundary_curvature` is a `pass` **stub**; it computes nothing.)
2. `T11_scale_emergence.py`: fits $\langle B\cdot1\rangle_{\rm boundary}=A/T+C$ and
   prints *"Characteristic Acceleration Scale A* … (units of network-c/T)"* — i.e.
   **measures A\* already in units of c/T**, assuming the scale it claims to find. (Its
   `test_phase_a_dynamic` is also a `pass` **stub**.) And from T2 the $1/T$ fit is poor.
3. `T14A`: *"A escala $a_0$ é **vinculada** ao horizonte IR"* — explicitly an
   **identification**, then computes the *evolution* $a_0(z)\propto(1+z)^{1/4}$ assuming
   $a_0\propto1/T$.

So phase 2 **assumes $a_0=cH$** (Milgrom's coincidence, externally motivated) and
explores its consequences. **It does not derive $a_0$ from the network** — and ST3 even
admits "a expansão acelerada **não emerge** naturalmente."

## TEIC's a₀ algorithm (for comparison)

C3: measure the smallest causal-link proper time vs density. Result
$\Delta\tau_{\min}\propto\rho^{-1/2}$ (light-cone sliver, dimension-independent) ⇒
$X_0\propto\rho^{+1}$ (UV). Conclusion: the saturation scale is **UV/granularity**; the
IR scale $a_0\sim cH$ is **not** produced — a separate, undischarged coincidence.

## Where they diverge, and who is right

| | a₀ origin | status |
|---|---|---|
| TEIC C3 | $\propto\rho$ (UV); $cH$ not derived | derived scaling, honest negative on $a_0$ |
| Gemini T2 (fundamental) | UV only; no IR scale emerges | **same as TEIC** |
| Gemini ST3/T11/T14 (scalar-tensor) | $a_0\sim c/T$ **postulated** | identification, not derivation; stubbed code |

**There is no contradiction with TEIC on the physics:** both fundamental analyses say
a₀ is **not derived**. Gemini's own two phases are **mutually inconsistent**, and the
"derived a₀" the user reported is the *postulated* c/T of the lighter phase, not a result.

**Audit conclusion (A5):** a₀ was **NOT derived** by Gemini. Its fundamental phase
agrees with TEIC that only UV scales emerge; its scalar-tensor phase *assumes* $a_0=cH$
(partly via stub code) and studies the consequences. No observational data was fit to
*obtain* a₀ (so not circular in that narrow sense), but $a_0=cH$ is **imported by
dimensional/symmetry analogy**, i.e. verifiable as an assumption, not a derivation.

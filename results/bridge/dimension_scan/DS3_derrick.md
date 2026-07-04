# DS3 — The Derrick window vs dimension

> Task DS3 of `DIMENSION_SCAN.md`. Radial quadrature of the generalised hedgehog
> in d spatial dimensions (current eigenvalues F′² radial + (d−1)·sin²F/r²
> tangential); dilation scan with (a) the dominant manual quartic and (b) the
> full link cosine with SC1's locked coefficients and the d-dimensional
> isotropic direction weight (Jacobi quadrature).
> Data: `DS3_derrick.json`; figure: `DS3_derrick.png`.

## Verdict: **the Derrick window contains exactly one integer dimension: d=3** — and the cosine alone is monotonic in every d (no sextic rescue)

```
d   E(λ) = λ^{d−2}E₂ + λ^{d−4}E₄   interior minimum?    full cosine
2   λ⁰E₂ + λ⁻²E₄ (E₂ scale-inv.)   ✗ (marginal)         monotonic
3   λE₂ + λ⁻¹E₄                    ✓ λ* interior        monotonic
4   λ²E₂ + λ⁰E₄ (E₄ scale-inv.)    ✗ (collapse)         monotonic
5   λ³E₂ + λ⁻¹E₄ → both shrink     ✗                    monotonic
```

## What this establishes

1. **The stabilisation window 2<d<4 is measured on the network's own
   functional** (the same E₂, E₄ = K/2 that SC1–SC4 derived), not quoted from
   the continuum literature: with a dominant quartic, only d=3 gives an
   interior minimum — in d=2 the sigma term is scale-invariant (marginal), in
   d=4 the quartic is (collapse), in d=5 both terms shrink with λ.
2. **The sextic route in d=5 is dead**: the full cosine contains *all* orders
   of the expansion, and it is monotonic in every dimension tested — the
   higher-order terms inherit the same net-saturating sign (3S−2K>0) that SC4
   measured in d=3. A "λ⁻¹ from the sextic" rescue does not materialise.
3. Consistency: the d=3 manual row reproduces SC4's control (λ* interior,
   matching the Derrick prediction).

## Honest limitations

- The cosine's monotonicity means the *minimal action* stabilises nowhere —
  the Derrick window statement is about the theory **with** the core-cost
  ingredient (the Paper II Skyrmion). The dimensional selection is therefore:
  *given* the one extra matter ingredient, topological matter is possible only
  in d=3. The d-scan does not remove that ingredient (SC4's boundary).
- Single profile family (F=πe⁻ᵘ); the window boundaries are exponent
  identities in λ, independent of the profile — only the λ* value moves.

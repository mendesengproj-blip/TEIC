# W2 -- Tensão de corda: λ_p confina a carga?

Vórtice (winding +1) e antivórtice (−1) separados por d, núcleos fixados, campo
de gauge relaxado ao mínimo de energia. Confinamento ⟺ E(d) **linear** (corda de
tensão σ); desconfinamento ⟺ E(d) satura/log (Coulomb). Ajustamos ambas as formas.

| λ_p | σ (total, fit lin) | R²_lin | R²_log | E_wilson (núcleo) | σ_wilson |
|-----|--------------------|--------|--------|-------------------|----------|
| 0.01 | +0.349 | 0.79 | 0.58 | 0.1 | +0.0001 |
| 0.1 | +0.349 | 0.79 | 0.58 | 1.1 | +0.0007 |
| 0.5 | +0.352 | 0.80 | 0.59 | 5.5 | +0.0029 |
| 1.0 | +0.355 | 0.81 | 0.60 | 10.6 | +0.0052 |
| 5.0 | +0.368 | 0.84 | 0.64 | 44.2 | +0.0115 |

## VERDICT W2: NAO (sem corda linear controlada por lambda_p neste regime estatico)

No lambda-controlled linear string. The vortex-antivortex interaction is dominated by the inherited gauge STIFFNESS (the spin-wave / Coulomb energy, slope ~0.35, essentially lambda-INDEPENDENT), while the genuine Wilson contribution E_wilson(d) is core SELF-energy: it grows with lambda_p (0.1 -> 44.2 over the range) but is ~d-INDEPENDENT (slope ~0.004), i.e. NOT a flux string. This is the honest 2D physics: static compact-U(1) winding-+/-1 charges are COULOMB (BKT) bound, not linearly confined -- a full 2pi flux quantum is nearly invisible to the compact cos term (cos 2pi=1), and linear confinement (Polyakov) is a DYNAMICAL monopole effect not seen in a static relaxation. No sharp lambda_c exists in {0.01, 0.1, 0.5, 1.0, 5.0}; for W3 we use the operational scale lambda~1.0 where the Wilson energy first reaches the kink mass 8 (so Wilson could plausibly act dynamically).

![string](W2_string.png)

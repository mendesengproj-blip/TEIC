# C3-3 -- Universalidade entre numeros barionicos (B = 1, 2, 3)

Campos axiais de grau n (mapa angular `axial_bn`) com o perfil radial **relaxado
de B=1** (`su2_core.radial_relax`).

| n | B (rede) | E_class | I | alpha_C | R^2(m^2 vs J) | R^2(m^2 vs J(J+1)) |
|---|---|---|---|---|---|---|
| 1 | 0.939 | 297.17 | 312.74 | 0.9502 | 0.9626 | 1.000000 |
| 2 | 1.771 | 606.35 | 312.74 | 1.9389 | 0.9626 | 1.000000 |
| 3 | 2.430 | 1060.09 | 312.74 | 3.3897 | 0.9626 | 1.000000 |

## Universalidade ESTRUTURAL (a afirmacao firme)

Para **todo** B em {1,2,3}: m^2 e linear em J(J+1) (R^2 ~ 1) e **nao** em J
(R^2 < 0.99).  O criterio de morte de C3-1 dispara **identicamente** em cada B.
=> A conclusao (Casimir, nao Regge) e **universal**: True.

## Universalidade NUMERICA de alpha_C (a afirmacao que NAO posso fazer)

Os ansaetze axiais aqui **nao** sao multi-Skyrmions relaxados (o cooling 3D com
o stencil e4 da rede e numericamente instavel neste regime) e reutilizam o
**mesmo** perfil radial, logo I ~ 313 fica quase
independente de B.  Como alpha_C ~ E_class/I, alpha_C entao apenas **acompanha a
massa** (alpha_C(B=2)/alpha_C(B=1) ~ 2.04,
alpha_C(B=3)/alpha_C(B=1) ~ 3.57).  Isto e um
**artefato** do ansatz nao-relaxado, nao fisica.  Um teste limpo da
universalidade de alpha_C exige solitons B>=2 relaxados (com seus proprios I).

> **Veredito da universalidade numerica de alpha_C: INDETERMINADO.**

## Conclusao C3-3

A **forma** do espectro (Casimir, morte de Regge) e universal em B -- a mesma
fisica do rotor rigido para 1, 2 e 3 barions.  A **igualdade numerica** de
alpha_C entre B (a universalidade de Regge de QCD) fica indeterminada com a
ferramenta disponivel.

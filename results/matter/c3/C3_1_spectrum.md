# C3-1 -- Espectro rotacional e o teste de linearidade de Regge

Skyrmion B=1: **E_class = 297.1681**, **I = 312.7366**
(unidades da rede, c = 1).  Espectro de rotor rigido
E_J = E_class + J(J+1)/(2I), massa m_J = E_J.

| J | J(J+1) | E_J | m^2 = E_J^2 |
|---|---|---|---|
| 0.0 | 0.0 | 297.16809 | 88308.8739 |
| 0.5 | 0.75 | 297.16929 | 88309.5866 |
| 1.0 | 2.0 | 297.17129 | 88310.7744 |
| 1.5 | 3.75 | 297.17409 | 88312.4373 |
| 2.0 | 6.0 | 297.17768 | 88314.5753 |

## O teste pre-registrado: m^2(J) e linear em J?

| ajuste | R^2 | residuos |
|---|---|---|
| m^2 vs **J** (hipotese de Regge) | 0.96257 | [0.475, -0.238, -0.475, -0.238, 0.475] |
| m^2 vs **J(J+1)** (rotor rigido) | 1.0000000 | [1e-05, 0.0, -1e-05, -1e-05, 1e-05] |

Os residuos do ajuste vs J formam um padrao em **U** (sinais + - - - +): a
assinatura inequivoca de uma curva **quadratica** forcada num ajuste linear.
m^2 vs J(J+1), em contraste, e linear a ~1e-5 (R^2 ~ 1.0000000), com inclinacao
**alpha_C = 0.95023** (unidades da rede).

Isto e exatamente esperado: o rotor rigido da E_J proporcional ao Casimir
J(J+1), logo m = E_J e m^2 = E_J^2 sao **lineares em J(J+1)** e **quadraticos em
J** -- nunca lineares em J.  A lei de Regge m^2 = alpha' J exige que o soliton
se DEFORME (se estique numa corda rotativa relativistica) a J alto; a
quantizacao coletiva de corpo rigido nao captura essa deformacao.

## Robustez (10 sementes, flutuacao de vacuo eps = 0.02)

| quantidade | media +/- desvio |
|---|---|
| E_class | 304.839 +/- 0.156 |
| I | 314.323 +/- 0.738 |
| R^2 (m^2 vs J) | 0.9626 +/- 0.0000 |
| R^2 (m^2 vs J(J+1)) | 1.000000 +/- 0.000000 |
| alpha_C = inclinacao(m^2 vs J(J+1)) | 0.9698 +/- 0.0024 |

Em **todas** as 10 sementes m^2 e linear em J(J+1) (R^2 ~ 1) e NAO
em J (R^2 ~ 0.963 < 0.99).  A flutuacao de vacuo move E_class e I
mas nao altera a estrutura.

## Veredito C3-1: **C**

m^2(J) **nao** segue a lei linear em J (R^2 = 0.9626 < 0.99, com
residuos quadraticos sistematicos).  O criterio de morte pre-registrado e
**acionado**: a trajetoria de Regge NAO emerge do rotor rigido do Skyrmion.
O espectro e a lei de Casimir do rotor rigido (m^2 propto J(J+1)), nao a lei de
corda de Regge (m^2 propto J).

Figura: `C3_1_spectrum.png`.

# C5-1 -- Heat kernel na rede causal de Poisson

Operador de difusao = d'Alembertiano causal suavizado de Sorkin/BD
(c5_core.bd_operator_eigs, reaproveitando e10). Probabilidade de retorno
media K(sigma) = (1/N) sum_i exp(-sigma|lambda_i|); dimensao espectral
D_s(sigma) = -2 d log K / d log sigma. A escala de difusao e adimensional
(s = sigma * lambda_escala) para comparar densidades diferentes -- D_s e
invariante a esse reescalonamento.

## D_s(s) para multiplos N (2D, diamante unitario; N varia = densidade varia)

| N | s=0.10 | s=0.49 | s=1.00 | s=3.00 | s=8.16 | s=20.10 |
|---|---|---|---|---|---|---|
| 1000 | 0.23 | 0.85 | 1.28 | 1.78 | 1.93 | 1.92 |
| 2000 | 0.23 | 0.86 | 1.29 | 1.81 | 1.96 | 1.96 |
| 4000 | 0.23 | 0.86 | 1.29 | 1.81 | 1.96 | 1.97 |

Convergencia em N: as curvas D_s(s) para N = 1000, 2000, 4000 sao praticamente IDENTICAS na variavel adimensional s (ver figura,
painel a, e C5-2). O heat kernel esta bem definido e converge.

## Decaimento do heat kernel

No plateau, K(s) ~ s^(-MM/2) (painel b da figura) -- a assinatura de
uma variedade de dimensao MM. Para s pequeno K -> 1 (gerador toca todos
os modos igualmente: regime de discretude) e para s grande K -> 1/N
(modo zero/constante sobrevive: saturacao por tamanho finito).

![C5 heat kernel](C5_heatkernel.png)

Multiplos N (minimo 3) cumpridos: 2D {1000,2000,4000}, 4D {1500,3000,5000}.
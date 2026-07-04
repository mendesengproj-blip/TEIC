# FR2 — Troca = meia-volta espacial rígida ∘ isospin global: identidade EXATA

> Task FR2 of `MATTER_FR_EXCHANGE.md`. Avaliação analítica, d=8.
> Data: `FR2_rigid.json`.

## Verdict: **erro 0.0 (zero de máquina)** — o endpoint da troca e o da meia-volta rígida diferem por exatamente UMA conjugação de isospin global D(π)

```
||U_rigid − D·U_exch·D⁻¹||  =  0.0   (max e mean, exatos)
controle sem conjugação:       max 2.00 (anticorrelados — a conjugação é real)
D = lift de R_z(π) = quaternion (0,0,0,1)
```

(As duas direções de conjugação coincidem porque D⁻¹=−D e conjugação é cega ao
sinal global — consistente, não ambíguo.)

## O que fica estabelecido

A troca de dois Skyrmions **é** uma rotação espacial rígida de π, a menos de um
único elemento de isospin global — identidade de campo exata, válida ponto a
ponto na rede, não assintótica. Isso reduz o problema da classe de homotopia do
loop de troca ao problema do loop de rotação — exatamente a redução que o
teorema FR usa, agora **medida** no campo (o passo "spin from isospin" dos
hedgehogs). Com FR3 (a rotação age pelo duplo recobrimento), as duas premissas
mecânicas do teorema estão verificadas no substrato.

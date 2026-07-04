# SU6 — Criação por colisão: o Skyrmion emerge? (20 sementes)

## Veredito: **NÃO — colisão não cria Skyrmion (B nunca quantiza em ±1)**

```
20 sementes, rede 25³, cadeias quirais com inclinação transversa (não-Abeliana).
|B| máximo na janela tardia, todas as sementes:   ≤ 0.41
|B| máximo em TODA a trajetória, todas:           ≤ 0.413
sementes com |B|>0.5 (transiente ou tardio):      0 / 20
```

## O que acontece

Repetindo T3D4 (colisão de CR_3D) com o campo quiral SU(2): duas cadeias escalares
contrapropagantes, embebidas em SU(2) com uma **inclinação transversa dependente da
semente** (para quebrar o plano σ₃ Abeliano — SU5 mostrou que `B≡0` para configurações
Abelianas/colineares) — dando ao enrolamento π₃ uma chance justa.

Em **nenhuma das 20 sementes** o número topológico `B` se aproxima de ±1. Ele flutua
até `|B|≈0.4` (um enrolamento *parcial*, não-inteiro, durante a sobreposição), mas
nunca quantiza num Skyrmion. A energia cresce (colapso do setor sigma sem fixação),
mas o enrolamento topológico **não é gerado**.

## Nota de método (honesta)

A força de Skyrme (E₄) é por diferença finita e cara demais para 150 passos × 20
sementes. Como SU5 mostrou que o termo de Skyrme apenas **estabiliza** um `B` já formado
(não pode *criar* enrolamento que a colisão não produz), a colisão foi evoluída com a
força sigma **analítica** (rápida). O resultado é decisivo: se `B` não emerge na
colisão sigma, nenhum Skyrmion é criado — e ele de fato não emerge.

## Por que (a física)

Gerar `B=±1` a partir de dados iniciais suaves exige uma **flutuação topológica
grande**: o campo teria que varrer toda a esfera-alvo S³, passando por configurações
quase-singulares. Uma colisão suave de duas cadeias não fornece isso — exatamente como
em U(1) (T3D4/G3) o enrolamento de vórtice não era criado espontaneamente de forma
robusta. A topologia que torna o Skyrmion **estável** (SU3) é a mesma que o torna
**difícil de criar** dinamicamente: setores topológicos não se conectam suavemente.

## Conclusão

O hedgehog/Skyrmion é um sóliton **estático estável** com `B=1` (SU3, SU4), mas **não é
criado por esta colisão** — o setor topológico `B=1` não é alcançado a partir do vácuo
por evolução suave. Isto coloca a fronteira no **Veredito C** para a questão da
*criação* (hedgehog estático existe, criação por colisão não ocorre), enquanto a
existência/estabilidade do objeto permanece firme (B, ver SU9).

## Anti-circularidade

Quaternions; `B` = determinante das correntes; "próton"/"bárion" só como nomes.
`results/matter/su2/SU6_collision.json` + `SU6_collision.py`.

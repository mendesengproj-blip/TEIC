# FR1 — O loop de troca existe na rede

> Task FR1 of `MATTER_FR_EXCHANGE.md`. Par de hedgehogs B=1 (ansatz produto),
> caminho de troca = meia-volta das posições com orientações fixas; avaliação
> analítica (sem interpolação). Data: `FR1_loop.json`; figura: `FR1_loop.png`.

## Verdict: **o loop fecha assintoticamente com a taxa prevista e⁻ᵈ/² — carga e energia conservadas ao longo do caminho**

```
d     B_total   drift de B    E max/min    erro de fechamento
6     1.813     0.0036        1.0006       0.490
8     1.817     0.0013        1.0018       0.177
10    1.818     0.0005        1.0055       0.063
razões de decaimento por Δd=+2:  2.78, 2.81   (pré-registrado ≥2; e¹=2.72)
```

## O que fica estabelecido

1. **O loop é bem-definido no regime de moduli** (separação grande): o erro de
   fechamento — o comutador dos dois fatores do produto, a única obstrução —
   decai exatamente como e^{−d/2} (razões 2.78/2.81 vs e¹=2.72). No regime em
   que a quantização FR de coordenadas coletivas se aplica, a troca é um loop
   fechado genuíno do espaço de configurações da rede.
2. **B é conservado ao longo do caminho** (drift ≤ 0.004 — duas ordens abaixo
   do valor) e **a energia é limitada e quase constante** (variação ≤ 0.5%):
   nenhuma barreira, nenhuma singularidade — a troca é um caminho físico.

## Nota de honestidade (banda pré-registrada vs medido)

O valor absoluto B=1.813 ficou **fora da banda pré-registrada 2±0.15** por
0.04. Causa verificada: discretização do hedgehog único nesta grade
(dx=0.4): B_único = 0.9096, e 2×0.9096 = 1.819 — o par reproduz **2× a linha
de base da mesma grade a 0.3%**. O conteúdo físico pré-registrado
(carga aditiva e conservada) confirma; a banda absoluta foi mal calibrada
para dx=0.4 (MIN2 com dx=0.27 dava 0.958/hedgehog). Registrado como está.

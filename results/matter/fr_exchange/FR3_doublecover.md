# FR3 — Rotações espaciais agem no Skyrmion pelo duplo recobrimento (medido)

> Task FR3 of `MATTER_FR_EXCHANGE.md`. 17 ângulos amostrados em [0, 2π];
> lift contínuo rastreado. Data: `FR3_doublecover.json`.

## Verdict: **identidade a 7×10⁻¹⁶ em todo θ; o lift contínuo termina em −𝟙; W = 1 cruzamento antipodal**

```
U₀(R(θ)x) = D(θ)·U₀(x)·D(θ)†   pior erro: 7.2e-16 (máquina)
q(2π) = (−1, 0, 0, 0)           exato
cruzamentos antipodais (equador a₀=0): W = 1
```

## O conteúdo medido (dito com cuidado)

Em cada θ isolado, a conjugação é cega ao sinal de D — o que fixa o sinal é a
**continuidade do caminho** em SU(2). O caminho contínuo que realiza a rotação
espacial completa do Skyrmion termina no antípoda −𝟙, cruzando o equador de S³
exatamente uma vez: **W = 1 — o mesmo invariante que a maquinaria FR de
MATTER_SU2_QUANT conta** para selecionar j=½. Ou seja: girar o Skyrmion da
rede de 2π arrasta a coordenada coletiva pelo caminho não-contrátil que o
setor de quantização já usa. A peça que liga "rotação espacial física" ao
"caminho q(t) em S³" deixa de ser suposição: é identidade de campo medida.

## Honestidade

O −1 mora no lift, e o lift é matemática de SU(2); o que o teste verifica é
que **este** lift (e não uma ação que fatore trivialmente) é o que age sobre o
campo da rede com continuidade — a premissa mecânica do FR. A projeção sobre
funções ímpares (o passo quântico que converte W=1 em fase −1 física) continua
sendo a quantização por integral de caminho de MATTER_SU2_QUANT.

# MATTER_FR_EXCHANGE: a estrutura spin-estatística vive na rede?

## ✅ VEREDITO: **as três premissas mecânicas do FR estão MEDIDAS; resta só o passo de homotopia** (mortes NÃO ativadas)

```
FR1  o loop de troca fecha como e^{−d/2} (razões 2.78/2.81 por Δd=+2 vs e¹=2.72);
     B conservado (drift ≤0.004); E limitada (≤0.5%). Nota honesta: B=1.813 ficou
     fora da banda 2±0.15 — verificado: = 2×B_único(0.910) da mesma grade a 0.3%
     (discretização dx=0.4, não física).
FR2  troca = meia-volta espacial rígida ∘ isospin global D(π): erro 0.0 EXATO.
FR3  U₀(R(θ)x) = D(θ)U₀(x)D(θ)† a 7e-16; lift contínuo termina em −𝟙; W=1 —
     o invariante que MATTER_SU2_QUANT converte em j=½.
FR4  importado restante: troca ≅ rotação-2π em π₁(config B=2) (FR 1968;
     Williams 1970) + a quantização coletiva. Fronteira ESTREITADA a esse passo.
```
Síntese: [`results/matter/fr_exchange/FR4_synthesis.md`](results/matter/fr_exchange/FR4_synthesis.md).

> Ataque 7 do `ROADMAP_REVOLUCAO.md` — o degrau honesto rumo ao "Nível 4" do
> revisor. O teorema FR diz: trocar dois Skyrmions idênticos ≃ rodar um deles de
> 2π. Esta campanha MEDE as peças dessa identidade no campo da rede (motor
> `su2_core`, quaternions reais) e nomeia com precisão o que permanece teorema
> importado. Resultados em `results/matter/fr_exchange/`. NÃO modifica campanhas
> anteriores.
>
> **Declaração de fronteira (antes de rodar):** o FR completo exige π₁ do espaço
> de configurações B=2 — a identificação final troca≅rotação-2π permanece
> teorema (Finkelstein–Rubinstein 1968; Williams 1970; Giulini). Prior art a
> citar: Friedman–Sorkin 1980 (geons com spin-½ de pura topologia). O objetivo é
> ESTREITAR a fronteira: medir que (i) o loop de troca existe e fecha na rede,
> (ii) troca = meia-volta espacial rígida ∘ isospin global (identidade exata),
> (iii) rotações espaciais arrastam a coordenada coletiva pelo DUPLO
> RECOBRIMENTO (o caminho que a maquinaria FR de MATTER_SU2_QUANT conta como
> W=1). Não cruzar; estreitar.

## PREVISÕES PRÉ-REGISTRADAS

```
FR1 (o loop de troca existe):
  config produto de dois hedgehogs B=1 separados por d: B_total = 2 (±0.15);
  o loop de troca (posições em meia-volta, orientações fixas) fecha
  ASSINTOTICAMENTE: erro de fechamento ~ comutador dos fatores ~ e^{-d/2}
  → cai por fator ≳2 a cada Δd=+2 (d = 6, 8, 10);
  B(s) = 2 conservado ao longo do caminho; E(s) limitada (max/min < 1.5).

FR2 (troca = rotação rígida, exatamente):
  para hedgehogs, o endpoint da troca e o endpoint da meia-volta espacial
  rígida diferem por UMA conjugação de isospin global D(π) — identidade
  EXATA (< 1e-12), não assintótica.

FR3 (o duplo recobrimento age):
  U₀(R(θ)x) = D(θ) U₀(x) D(θ)† pontualmente (< 1e-12) para todo θ amostrado,
  com D(θ) o lift contínuo; o caminho do lift termina em D(2π) = −𝟙
  (cruzamento antipodal W = 1 — o invariante de MATTER_SU2_QUANT).
```

## CRITÉRIO DE MORTE (pré-registrado)

```
FR1 morre se o erro de fechamento NÃO decair com a separação (loop mal-definido).
FR2/FR3 morrem se as identidades exatas falharem acima de erro de máquina
(i.e., se a ação das rotações espaciais sobre o Skyrmion da rede NÃO se der
pelo lift SU(2) — nesse caso a rota FR inteira está errada para esta rede).
```

## Tarefas

```
FR1: loop de troca — fechamento vs d, B(s), E(s)    → FR1_loop.{py,md,json,png}
FR2: troca ↔ meia-volta rígida (identidade exata)    → FR2_rigid.{py,md,json}
FR3: duplo recobrimento medido + W=1                 → FR3_doublecover.{py,md,json}
FR4: síntese — o que está medido, o que segue teorema → FR4_synthesis.md
```

## O que isto compraria (se tudo bater)

O Paper II §VII hoje diz "FR aplicado como teorema". Depois: *"as três premissas
mecânicas do teorema — o loop de troca bem-definido, a identidade
troca=rotação-rígida, e a ação por duplo recobrimento — são MEDIDAS no campo da
rede; o que se importa é apenas o passo final de homotopia (π₁ do espaço de
configurações)."* Fronteira estreitada com precisão; não cruzada.

# SÍNTESE — B6 · η em d=4 causal: derivação em cadeia via Molloy–Reed

> Campanha ESCALAS_B6 (Fase 2, Frente B). Pré-registro: usuário (jun/2026).
> Driver: `b6_eta_chain.py` → `b6_eta_chain.json`. Stages 0–4.
> **Veredito: MORTE PARCIAL (bem-entendida). O MECANISMO de η(4) é identificado e
> funciona (Molloy–Reed + clustering via 1/(1−C), ambos invariantes d-only,
> reproduzem k_c a 7%), mas o VALOR PRECISO de η fica [EXTERNO-B]: amplificação
> quadrática + não-convergência finite-size de k_c dão ~24–30% de incerteza. E B6
> REFINA B5: a "size-stability" de k_c era um platô de N≤1600.**

---

## 1. Pergunta e disciplina

B5 mostrou k_c(d) = z_c_MR(d) + Δ_clustering(d) (calculável). B6 pergunta: os
invariantes que fixam k_c(4) — CV (heterogeneidade de grau) e C (clustering) — são
**d-only** (independentes de ρ, V, K), de modo que η=(k_c−1)² desce de d=4 sem outro
input? **Armadilha de circularidade declarada antes de rodar:** se Δ_clustering for
*definido como o gap residual* k_c−z_c_MR, então η_pred=(z_c_MR+Δ−1)²=η trivialmente.
Por isso: (a) z_c_MR é **predição forward** da CV medida; (b) C é medido
**independentemente** (triângulos/triplas); (c) Δ é diagnóstico, e testa-se uma
**fórmula independente** de C. Grafo = relação causal simetrizada, **idêntico a B5**.

## 2. Stage 0 — gate (PASSOU, bloqueante)

- ER(N=800,p=0.05): ⟨k⟩=39.96 (exato), C=0.0498 (=p) → estimadores validados.
- d=2 diamante: percolação k_c=1.084 (B5 1.01 ✓), z_c_MR=0.899 (B5 0.90 ✓).
- **Correção da redação do pré-reg:** o Stage 0 pedia "z_c_MR reproduz k_c(2)=1.01",
  mas z_c_MR(2)=0.90 ≠ 1.01 — **o gap É o clustering**. O gate valida cada estimador
  contra o seu valor de B5 (percolação→k_c, MR→z_c).

## 3. Stage 1 — ρ-invariância (VERDE, mas trivial)

CV, z_c_MR, C **exatamente invariantes** (spread 0.0%) sob ρ∈{0.25,0.5,1,2} a N=979
fixo (caixa, L ajustado). **Razão:** a causalidade de Minkowski é **scale-invariante**
(x≺y preservado sob x→λx), então a ρ fixo-N o grafo causal é estatisticamente
idêntico. Real, mas trivial: CV, C, z_c dependem só de (N, d), nunca de ρ ou V isolados.
(Nota: a CV da caixa=0.557 difere da CV do diamante=1.00 — geometria de bordo importa;
a cadeia principal usa o diamante, B5-consistente.)

## 4. Stage 2 — FSS de k_c(4) (o ponto crítico)

| N | k_c | CV | z_c_MR | C | η=(k_c−1)² |
|---|---|---|---|---|---|
| 200 | 0.740 | 1.01 | 0.509 | 0.148 | 0.067 |
| 500 | 0.665 | 1.00 | 0.508 | 0.143 | 0.112 |
| 1000 | 0.683 | 1.00 | 0.502 | 0.139 | 0.101 |
| 1800 | 0.626 | 1.00 | 0.501 | 0.143 | 0.140 |
| 2600 | 0.585 | 1.00 | 0.500 | 0.142 | 0.173 |
| 3600 | 0.613 | 1.00 | 0.503 | 0.143 | 0.150 |

- **z_c_MR e CV rock-stable** (CV→1.00, z_c_MR→0.50 em todo N): o termo de Molloy–Reed
  é o invariante d-only sólido.
- **k_c NÃO é precisamente pinado:** banda large-N (N≥1000) = **0.627 ± banda 0.10**,
  com drift suave **abaixo** do platô de N≤1600. É **não-genérico** (8σ abaixo do valor
  ER=1) e dimension-dependent — mas o valor exato não converge a N≤3600.
- **REFINA B5:** a "size-stability" (tail-spread 0.008) de B5 era um **platô de
  N≤1600**; estendendo a N=3600, k_c deriva suavemente (~0.69→~0.61). O **núcleo de
  B5 (k_c dimension-dependent, não-genérico, liderado por MR) PERMANECE**; só a precisão
  ("size-stable", valor 0.67) é suavizada.

## 5. Stage 3+4 — decomposição e veredito

- **z_c_MR(4)=0.502** (forward da CV, d-only) → **η_MR=(z_c_MR−1)²=0.248** (termo
  líder, derivado em cadeia de d=4).
- **C(4)=0.142** (medido, d-only, ρ-invariante).
- gap **Δ=k_c−z_c_MR=+0.125 (+20%)**, positivo (clustering eleva k_c), <40% (Stage 3 ✓).
- **Fórmula independente (não-circular):** `z_c_MR/(1−C) = 0.585` reproduz k_c=0.627 a
  **7%**; `z_c_MR·(1+C)=0.573` a 9%. → **o mecanismo de fecho funciona no nível de k_c**
  a partir de dois invariantes d-only (CV via z_c_MR, e C).
- **MAS no nível de η:** η=(k_c−1)² é quadrático; 7% em k_c → ~24% em η
  (η=0.139 vs η_pred=0.172). Falha o critério estrito de 10%.

**Veredito: MORTE_B6_PARCIAL.** O *mecanismo* de η(4) está identificado e é
quantitativamente correto (MR + clustering 1/(1−C), invariantes d-only, k_c a 7%) — η
NÃO é o parâmetro livre da SR; é **d-determinado em ordem líder** (η~0.14, não-genérico
a 8σ). Mas o **valor preciso** de η fica **[EXTERNO-B]** por dois motivos identificados
(resultado de 1ª classe): (1) amplificação quadrática (k_c→η) e (2) não-convergência
finite-size de k_c (banda 0.10 a N≤3600). O input que falta é a **correção
clustering+finite-size** — uma propriedade de grafo sem forma fechada exata —, **não**
uma escala em SI.

## 6. Conexão com o programa

Padrão recorrente, agora confirmado para η: **mecanismo/forma emerge do substrato; o
número absoluto preciso herda um input** (aqui, a correção de clustering finite-size,
geométrica mas sem forma fechada). B1 (rescala global não fixa hierarquia) + B5 (k_c =
limiar de grafo forçado, dimension-dependent) + B6 (mecanismo MR+clustering de η
identificado, valor preciso externo) **fecham a tese de escalas com mecanismo e três
portas bem-entendidas**. O elo R1(seleção d=4)→colapso(η) é **parcial**: o termo líder
η_MR=0.25 desce de d=4; o valor refinado ~0.14 precisa da correção de clustering.

## 7. Limitação honesta

N≤3600 (drift residual de k_c não resolvido; o asymptote pode ser ~0.60 ou continuar
para z_c_MR=0.50 — não decidível aqui). A fórmula 1/(1−C) é uma forma-padrão de
percolação-com-clustering (aresta redundante), **testada** a 7%, não **derivada** do
DAG causal — fica [IDENTIFICADO]. Geometria diamante vs caixa muda CV (1.00 vs 0.56):
a cadeia usa o diamante (B5-consistente); a dependência de forma-de-bordo é um
sistemático registrado, não controlado.

## 8. Anti-circularidade

Gate A1 verde sobre `b6_eta_chain.py` (dilatação + literais de escala) antes de rodar
(bloqueante). C medido (triângulos/triplas), não inserido. η de k_c medido, nunca input.
Δ tratado como diagnóstico; o veredito repousa em k_c medido e numa fórmula
**independente** de C, **não** em Δ:=residual (a armadilha circular foi evitada).
Valores SR (0.1, 0.99) só em pós-dição.

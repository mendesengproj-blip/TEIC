# SÍNTESE — B3b · Gauge-invariância e fechamento do 2-complexo de cones futuros

> Campanha FOTON_B3b (Fase 3, Frente do Fóton). Follow-up de B3 (candidato).
> Driver: `b3b_closure.py`. Resultado: `b3b_closure.json`. jun/2026.
> **Decisão do usuário: rodar SÓ os gates bloqueantes — Stage 0 (reconstrução validada)
> + Stage 1 (gauge). Parar no primeiro veredito.**
>
> **Veredito: MORTE_B3b_NOGAUGE.** O 2-complexo de cones futuros de B3 *fecha*
> (∂∂=0) e a ação é gauge-invariante a nível de máquina (ΔS/S≈10⁻¹⁵) — **mas isso é
> automático para qualquer conjunto de quadriláteros fechados**: o null cinemático de
> B3 (ápices aleatórios) reproduz o mesmo zero de máquina. O "pass" não carrega
> informação. Decisivamente, as células **não vivem no setor de links de Hasse** (a
> substrato de gauge que E6_1 validou): só ~31% dos lados são links, e a fração **cai**
> com N. As células de cones futuros são um **complexo de relações**, não um complexo
> de gauge. O frac_B=0.84 era estrutura spacelike, não um fóton. **Stages 2 e 3
> (polarização, dispersão) NÃO rodaram — bloqueados pelo gate, como pré-registrado.**
> Canal "cones futuros" → **[FRONTEIRA]**; nenhum charter de paper congelado.

---

## 1. O que B3b testou (e por que o gate mudou de forma antes de rodar)

B3 deixou três lacunas; a primeira (gauge) é o gate que invalida tudo a jusante. A
leitura do código existente (`E6_1_gauge_structure.py`, `e5_core.py`,
`orientation_core.py`) **antes** de rodar mostrou que a forma literal do gate do
pré-registro estava mal-posta:

- O complexo de gauge que E5/E6 validaram é construído **inteiramente a partir de
  links de Hasse** (relações de cobertura; `causal_diamond_plaquettes`,
  `height_h_plaquettes`). É o *setor de links* cujo campo de gauge E6_1 confirmou.
- A célula de B3 é o quad ordenado (i,k,j,l): i,j spacelike-incomparáveis, k,l no
  futuro comum. Seus quatro lados são **relações causais** i<k, j<k, i<l, j<l — que em
  geral **não são links de Hasse**. B3 só mediu áreas de bivetores geometricamente;
  **nunca construiu uma incidência no grafo de links.**
- **Consequência (avisada ao usuário antes de rodar):** para uma ação S=½ΣF², F=dθ, a
  invariância de gauge θ→θ+dχ é **automática** sempre que o complexo fecha (∂∂=0). E
  ∂∂=0 é automático para um 4-loop i→k→j→l→i (telescopa a zero por construção). Logo
  `|ΔS/S|<10⁻¹²` **não é o gate** — passa trivialmente. O gate real é (a) o complexo
  vive no substrato de links de Hasse? e (b) o null cinemático reproduz o "pass"?

Por isso B3b mediu **as duas coisas que discriminam**, com o null de B3 passando pela
**mesma** maquinaria — exatamente a disciplina que salvou B3/B4 dos falsos-positivos.

## 2. Stage 0 — reconstrução validada (gate bloqueante): PASSA

| controle | ∂∂ (max\|BG\|) | ΔS/S (máx) | modos de gauge | físicos | veredito |
|---|---|---|---|---|---|
| **lattice 4D (4⁴) = Maxwell** | **0.00** | **3.3×10⁻¹⁶** | **255 (= N−1 ✓)** | 765 | **PASS** |
| null cinemático (ápices aleatórios) | 0.00 | ~7×10⁻¹⁶ | (ver §3) | (ver §3) | (controle) |

A mesma maquinaria de incidência/cobordo reproduz o complexo de plaquetas de Maxwell
a ~10⁻¹⁶, com a contagem de modos de gauge exata (N_sites−1 num lattice conexo). A
reconstrução é confiável — qualquer claim a jusante é válido.

## 3. Stage 1 — a tríade (só gauge mediu; lock e dispersão bloqueados)

| métrica | SINAL N=400 | SINAL N=800 | NULL N=400 | NULL N=800 |
|---|---|---|---|---|
| **∂∂  (max\|BG\|)** | 0.00 | 0.00 | 0.00 | 0.00 |
| **ΔS/S (1000 χ)** | 9.9×10⁻¹⁶ | 9.4×10⁻¹⁶ | 6.6×10⁻¹⁶ | 9.1×10⁻¹⁶ |
| **frac. lados = link Hasse** | 0.452 | **0.308 ↓** | — | — |
| **frac. células 100% link** | 0.059 | **0.015 ↓** | — | — |
| frac. modos de gauge (rank G/L) | 0.192 | 0.298 | 0.082 | 0.165 |
| frac. modos físicos (rank B/L) | 0.639 | 0.604 | 0.303 | 0.298 |
| — correlação-k̂ (Stage 2) | NÃO RODOU | NÃO RODOU | — | — |
| — ω=ck (Stage 3) | NÃO RODOU | NÃO RODOU | — | — |

**Leitura:**

1. **∂∂=0 e ΔS/S≈10⁻¹⁵ — em SINAL E NULL.** O complexo fecha e a ação é
   gauge-invariante a nível de máquina. Pelo critério **literal** do pré-registro
   (`|ΔS/S|<10⁻¹² → GATE VERDE`), isto seria um **FALSO VERDE**. O null com ápices
   **aleatórios** dá o **mesmo** zero de máquina ⇒ o "pass" é **não-discriminante**:
   é automático para qualquer conjunto de quads fechados. (Lição B3/B4, um nível mais
   fundo: um pass que o null reproduz não é evidência.)

2. **Fora do substrato de gauge (decisivo).** Só **30.8%** dos lados das células são
   links de Hasse a N=800 (e **apenas 1.5%** das células têm os quatro lados como
   links). Pior: a fração **cai** de 0.452 (N=400) para 0.308 (N=800) — o oposto de
   N-estável. À medida que N cresce, os ápices do futuro comum ficam mais "fundos"
   (mais relações intermediárias), então **menos** lados são relações de cobertura. As
   células migram para **fora** do setor de links — o substrato cujo campo de gauge
   E6_1 validou. São um **complexo de relações**, não o complexo de gauge.

3. **A única nuance a favor (registrada honestamente):** o setor físico do SINAL é
   mais rico que o do NULL (frac. modos físicos 0.60 vs 0.30; gap 0.31). Isto ecoa o
   `null_gap=0.22` de B3 — a estrutura causal do futuro comum **cria conectividade mais
   organizada** que quads aleatórios. **Mas isto é conectividade, não caráter de
   gauge.** Não estabelece uma redundância de gauge genuína no substrato; a
   invariância de gauge em si é a trivial (compartilhada com o null), e o complexo está
   fora dos links. Pela regra de ouro (dúvida → ramo conservador), não basta para VERDE.

## 4. Veredito

**MORTE_B3b_NOGAUGE.** O elemento da tríade que falhou: **gauge**. Não por ∂∂≠0 (o
complexo fecha), mas porque (i) a invariância de gauge é **automática e reproduzida
pelo null** — não-informativa; e (ii) as células estão **fora do substrato de links de
Hasse** e o abandonam à medida que N cresce. O canal "cones futuros" não produz o
fóton. Retorna a **[FRONTEIRA]**. Como pré-registrado, **Stages 2 (polarização) e 3
(dispersão) não rodaram** — o gate é bloqueante.

## 5. O ponto metodológico (o resultado de 1ª classe)

O critério **literal** do pré-registro (`|ΔS/S|<10⁻¹²`) teria dado **VERDE** e mandado
"prosseguir para Stage 2". Foi exatamente o risco sinalizado ao usuário **antes** de
rodar: para F=dθ, a invariância de gauge é automática dado o fechamento, e o fechamento
é automático para 4-loops. O gate genuíno não é ΔS/S — é **(a) pertencimento ao
substrato de links** e **(b) o null cinemático**. Sem esses dois controles, B3b teria
"confirmado um fóton emergente" sobre um pass vazio. **Os controles são a ciência; o
ΔS/S cru era a armadilha** — a mesma estrutura de B3 (null de ápices) e B4 (plano
não-esticado), agora aplicada à invariância de gauge.

## 6. O que B3b NÃO afirma

- Não afirma que o setor de links de Hasse (E6) deixa de ser gauge — esse continua
  sendo o complexo de plaquetas fiel (elétrico, E6/E6b/E6c). B3b usa células
  **diferentes** (cones futuros), e a morte é dessas células, não dos diamantes BD.
- Não afirma impossibilidade absoluta: o gap de setor físico (§3.3) mostra que o
  complexo de **relações** carrega *alguma* estrutura acima do ruído aleatório. Definir
  uma conexão no complexo de relações e mostrar uma redundância não-trivial **não
  reproduzida pelo aleatório** seria uma campanha nova — não é este canal, e não é
  fóton. Fica como fronteira, não como porta aberta.

## 7. Consequência para o programa

| | |
|---|---|
| Fóton magnético via cones futuros | **[FRONTEIRA]** (gauge não-genuíno) |
| Diamantes BD (E6) | inalterados: gauge fiel, elétrico |
| Próxima porta do fóton | **B4 Bianchi-I genuíno** (anisotropia na *ordem causal*, não no embedding) = a última alavanca a baixa curvatura |
| Paper Photon-Arc | ganha um ponto no mapa: cones futuros **fecham mas não são gauge do setor de links** |

## 8. Anti-circularidade

Guarda A1 **verde** (`pytest tests/ -q` = 2 passed; `SCAN_DIRS` cobre
`docs/campaigns/**`, então varreu `b3b_closure.py` — sem dilatação, sem literal de
escala). Nenhum c/ω inserido (Stage 3 nem rodou). Controle positivo (lattice 4D) +
null cinemático (ápices aleatórios) em todo número reportado. Bivetores e ordem causal
são geometria do sprinkle. O veredito conservador foi escolhido na presença de uma
nuance ambígua (§3.3), como manda a regra de ouro.

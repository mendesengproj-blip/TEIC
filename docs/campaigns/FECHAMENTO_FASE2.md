# FECHAMENTO — Campanha de Organização TEIC (Fase 2)

> Relatório de fechamento. jun/2026. Cobre A1, A2, A3, A4, A5 (Frente A / Tier 1)
> e B1, B5, B6 (Frente B / escalas). Guarda anti-circularidade verde em CI sobre
> os 396 geradores ao longo de toda a campanha. Nenhum paper submetido sem revisão
> do usuário. Pausa de consolidação executada antes de B3/B4.

---

## (a) Status epistêmico: antes vs depois da Fase 2

| Claim do programa | Antes da Fase 2 | Depois da Fase 2 | Item |
|---|---|---|---|
| **Guarda anti-circularidade** | protocolo declarado, varria ~6 dirs | **teste em CI sobre 396 geradores** (dilatação + literais de escala); R-0 não disparado | A1 |
| **Confinamento SU(3)** | "no cúbico 8⁴" (paper) + dúvida sobre o causet | **[SÓLIDO] cúbico, [FRONTEIRA] causet** (operador não-local; ~80–100% autovalores wrong-sign); escopo do paper **confirmado** | A2 |
| **LRO do ferromagneto de orientação** | medido a N≤1462 | **genuíno a N=3888** (m→0.995, U4=2/3, trend +0.011) — não é artefato de tamanho | A3 |
| **S(k) do setor de orientação** | α≈0.28 (plano) a N≈1462, "talvez tamanho" | **α≈0.06 plano robusto a N=3888** — campo médio não-local confirmado | A3 |
| **ω=ck do Goldstone (E2)** | [FRACO]: "do símbolo; propagação direta instável (sharp)" | **[FRACO] caracterizado**: instabilidade = indefinição Lorentziana do operador (de princípio, não artefato); símbolo é a extração estável correta | A4 |
| **ε(2)=1 / spin-estatística do bárion** | medido em 1 calibrador, uniformidade assumida | **ε=1 em 3 campos winding-2 distintos** → uniforme na classe swap → **fechado** | A5 |
| **θ=G_net·M/r (MG1)** | medido no solver radial | **confirmado em malha 3D Cartesiana** (expo −0.991, G_net∝M CV 0%) — não é artefato radial | A5 |
| **Hierarquia M_próton/M_Planck** | [EXTERNO-B] (busca falhou) | **[EXTERNO-B] com mecanismo**: rescala global S→K·S não fixa razão (∝√K escala) | B1 |
| **η (limiar de colapso) / "não pina"** | FD1: morte, k_c≈1 genérico (N=300) | **Verdito B**: k_c dimension-dependent, não-genérico (d4: 8–30σ), forçado por Molloy–Reed+clustering | B5 |
| **η(4) derivado em cadeia de d=4?** | nunca tentado | **MORTE PARCIAL**: mecanismo MR+clustering identificado (k_c a 7%), valor preciso **[EXTERNO-B-geométrico]** | B6 |
| **Tese de escalas (global)** | dispersa, sem gradação | **B1+B5+B6 unificados**: "mecanismo emerge, número preciso herda input geométrico"; nova tag **[EXTERNO-B-geométrico]** ≠ [EXTERNO] SI | B1+B5+B6 |

**Padrão da campanha:** nenhum claim publicado foi rebaixado. A2/A3/A5 **confirmaram**
que a redação dos papers já era honesta; A4 transformou uma ressalva numérica aberta
em limitação de princípio caracterizada. Todo negativo veio com o *porquê* (1ª classe).

## (b) Estado exato de cada paper

| Paper | Alvo | Status | Mudança nesta Fase | PDF |
|---|---|---|---|---|
| **Goldstone** | PRD | **em prep** (submission prep: e-mail/figuras vetoriais pendentes) | A3 (FSS→N=3888, Tabela+abstract) + A4 (ressalva afiada: operador não-positivo/Lorentziano) | ✅ compila (789 KB) |
| **Matter+Gravity** | PRD | **em prep** (cover letter pendente) | A5 (ε(2) multi-campo na §spin-estatística; 3D-Cartesiano na ressalva de gravidade) | ✅ compila (389 KB) |
| **Síntese (TEIC_MASTER)** | Zenodo (não-journal) | arquivo guarda-chuva | nova tag [External^geo] + parágrafo B1+B5+B6 + 3 linhas na Tabela I (hierarquia, η-mecanismo, η-valor) | ✅ compila (600 KB) |
| **SU(3)** | PRD | em prep | A2 confirmou escopo cúbico (sem edição necessária — já correto) | ✅ |
| **BTFR** | MNRAS | submission prep (a₀∝H(z) confirmado, ~19σ) | não tocado nesta fase | ✅ |
| **Ferromagneto** | PRL | em prep | não tocado | ✅ |
| **Photon-Arc** | CQG | em prep | **aguarda B3/B4** (fóton magnético no causet) | ✅ |

> **Nenhum paper submetido.** Todos os 6 compilam. As edições desta Fase aguardam a
> revisão final do usuário antes de qualquer upload.

## (c) O que B3/B4 encontrará quando começar

B3/B4 são o **caminho crítico do fóton** (Paper Photon-Arc), independentes da frente
de escalas (já fechada). Atacam a **única lacuna** localizada do setor de gauge: a
2-célula magnética spacelike a **baixa curvatura** (R̂≫1, universo observável), que
altura (E6b), curvatura isotrópica (E6c/e) e acoplamento (E6d) **não** deram (só
marginal no regime Planckiano).

- **B3 (Direção B):** classificador **novo** do bivetor de área das **intersecções de
  cones de luz futuros** (não diamantes height-2). Sucesso pré-registrado **verbatim**:
  fB > 0.01 a baixa curvatura, N-estável, gauge-invariante. Código novo; ~3–7 CPU-dias.
- **B4 (Direção A):** sprinkle de Sitter **flat slicing com anisotropia controlada**;
  fB cruza 0.01 a baixa curvatura com direção preferencial? Adapta o sprinkler de E6c;
  ~3–6 CPU-dias. **Roda em paralelo a B3.**

**Predição honesta (não pré-julgamento):** o padrão de A2/A4 — o operador causal
não-local é Lorentziano-indefinido e resiste a estruturas spacelike limpas — **sugere**
que B3/B4 podem encontrar a mesma fronteira (fB marginal fora do regime Planckiano).
Mas isso é **exatamente o que o experimento testa**; o classificador de cone-futuro de
B3 é uma construção genuinamente nova nunca tentada, e a anisotropia de B4 é uma
alavanca não testada. Se **qualquer** das duas der fB>0.01 a baixa curvatura, é "o
resultado mais publicável do programa" (fóton emergente real) → congela charter de
paper novo. Se ambas morrerem, a Direção B junta-se às alavancas esgotadas e o
Photon-Arc fica [FRONTEIRA] limpo. **Anti-circ.:** sob a guarda A1 (gauge varrido);
o bivetor não pode injetar fase.

## (d) Questões abertas que a Fase 2 NÃO tocou

1. **Forte-vs-fraca da transição SU(3)** (Tier 0): requer L≳48 multicanônico/cluster —
   fora do desktop; isolado, não afeta os outros claims. **Não iniciado** (por desenho).
2. **B2** (ξ_grav/ξ_cor entre domínios): **não promovido** — dependia de um B1 positivo.
   A 2ª razão de comprimento entre domínios fica não testada.
3. **Aspersão causal irregular genuína** para Wilson (A2) e gravidade (A5): bate na
   fronteira de não-localidade; só o cúbico/Cartesiano regular foi feito. A construção
   de um operador de coarse-graining que preserve ordenação não-abeliana **não existe**
   (mesmo obstáculo E5/E7/A2/A4) — lacuna estrutural conhecida.
4. **Valor preciso de η(4)** ([EXTERNO-B-geométrico]): a correção clustering+finite-size
   não tem forma fechada testada; k_c não converge a N≤3600. Forma fechada via C fica
   aberta (B6 §7).
5. **Elo η→ℏ:** B6 deriva η(4) em ordem líder, mas a conexão η→ℏ (a granularidade
   absoluta) requereria um mecanismo adicional **não testado** — ℏ permanece [EXTERNO].
6. **Conexão R1(seleção d=4)→colapso(η):** estabelecida só **parcialmente** (termo
   líder η_MR=0.25 desce de d=4; valor refinado herda input geométrico).
7. **A propagação hiperbólica IVP** (separar t e ∇² na rede causal): A4 testou só
   evolução elíptica + marcha retardada; um esquema hiperbólico que contorne a
   indefinição Lorentziana não foi construído (esperado falhar pela não-localidade,
   não provado).

---

## Resumo de uma linha

A Fase 2 transformou **protocolo declarado em teste de CI** (A1), **endureceu** dois
papers em prep (A3→Goldstone, A5→MG), **caracterizou** uma ressalva de princípio
(A4→Goldstone), **confirmou** o escopo honesto de um terceiro (A2→SU(3)), e **fechou
a frente de escalas com mecanismo e uma gradação epistêmica nova** ([External^geo],
B1+B5+B6) — sem rebaixar nenhum claim publicado. Resta o fóton (B3/B4), o único item
substantivo aberto.

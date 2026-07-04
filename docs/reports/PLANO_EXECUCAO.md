# PLANO DE EXECUÇÃO — campanha de organização TEIC (Fase 2)

> Fontes: `INVENTARIO_PIPELINE.md` (Fase 0) e `HIERARQUIA_EXPERIMENTOS.md` (Fase 1).
> As duas frentes — **CONSOLIDAR** (Tier 1, A) e **ESCALAS** (Tier 2, B) — rodam em
> paralelo onde recursos permitem. **Nada novo é executado antes da revisão do usuário**
> (esta tarefa é preparação).

---

## 1. Hierarquia final ordenada

```
TIER 0  (intocável — em execução / sucessor exigido)
  T0   L≳48 multicanônico/Wang-Landau (cluster) ......... NÃO iniciar/interromper

TIER 1 — CONSOLIDAR (Frente A)            TIER 2 — ESCALAS (Frente B)
  A1 = C1  Auditoria+extensão da guarda      B1  Razões internas K-indep (hierarquia)
  A2 = C3  Wilson loops no causet            B2  ξ_grav/ξ_cor entre domínios
  A3 = C2  Goldstone N maior + S(k)~k^α      B3  2-célula spacelike (cones futuros)
  A4 = C4  Propagação BD smeared (E2)        B4  Geometria anisotrópica (Direção A)
  A5 = C5  Resíduos baratos (ε(2), MG1-3D)   B5  Por que η/ℏ não pinam
```

**Sequência recomendada (com paralelismo):**

```
SEMANA 0  ── T0 segue sozinho no cluster (não tocar) ────────────────────────────►

GATE DE ENTRADA (serial, bloqueante):
  A1 (guarda) ───────────────►  PASSA?  ──► libera todo o resto
        │                          │
        │ (se achar problema)      └─► não: re-auditar resultado afetado primeiro
        ▼
PARALELO (após A1 verde):
  Frente A:  A3 (Goldstone N/S(k)) ──► A2 (Wilson causet) ──► A4 (prop BD) ──► A5
  Frente B:  B1 (razões K-indep) ────────────────────────►  B3 ∥ B4 (fóton)
                                    └─► B2 (depende de A3+B1) ──► B5
```

Justificativa da serialização do **A1 primeiro**: é barato, e seu resultado pode
**invalidar a confiança** em qualquer medição a jusante (critério 4, obsolescência).
Rodar escalas (B1) sobre um pipeline cuja guarda tem buraco seria construir sobre
fundação não-verificada. A1 é o único gate verdadeiramente bloqueante.

Tudo o mais é paralelizável por frente: a frente B (escalas) **não depende** da frente A
exceto B2 (precisa de A3/C2 para definir ξ_grav) — então B1, B3, B4 podem arrancar
assim que A1 passar, em paralelo com A2/A3/A4.

---

## 2. Caminho crítico até uma DECISÃO sobre escalas

A pergunta-mãe da frente nova é: **o substrato fixa razões adimensionais entre
domínios?** A sequência mínima que leva mais rápido a um sim/não decisivo:

```
A1 (guarda verde)  →  B1 (razões M_Sk, σ, G_net independentes de K?)
```

**Só dois experimentos.** Ambos com **código existente** (A1 estende a guarda; B1
orquestra medidas já implementadas de M_Sk, σ, G_net). Custo combinado ~3–5 CPU-dias.

- Se **B1 = positivo** (uma combinação é número puro K-invariante): o programa tem sua
  **primeira razão de escala derivada** — decisão positiva sobre escalas. Próximo passo
  imediato: B2 (2ª razão, comprimento) para ver se é um padrão ou um acidente.
- Se **B1 = morte** (nenhuma combinação invariante / só trivialidades geométricas): a
  hierarquia permanece [EXTERNO-B], **decisão negativa bem-entendida** — e B5 (por que
  η/ℏ não pinam) passa a ser a peça que explica *por quê*, fechando a tese "forma deriva,
  escala não" com um mecanismo, não só com falhas de busca.

Em ambos os ramos, **uma decisão de primeira classe sai em ~1 semana de CPU** após o
gate A1. As direções do fóton (B3/B4) são valiosas mas **não** estão no caminho crítico
de *escalas* — pertencem ao caminho crítico do *fóton* (Paper Photon-Arc), que corre em
paralelo.

Caminho crítico secundário (fóton, paralelo): `A1 → (B3 ∥ B4)` — uma decisão sobre se a
2-célula spacelike O(1) existe em baixa curvatura sai quando a primeira das duas direções
fechar (sucesso fB>0.01 ou morte em ambas).

---

## 3. Pontos de reavaliação (quando revisar a hierarquia)

| # | Gatilho | O que reavaliar |
|---|---|---|
| **R-0** | **A1 termina** | Se a guarda achar dilatação/literal de escala num gerador publicado: **PARAR a frente B**, re-auditar o resultado afetado e propagar a correção ao paper antes de qualquer escala. Se verde: liberar todo o paralelismo. |
| **R-1** | **B1 termina** | Decisão sobre escalas (§2). Positivo → promover B2 e redigir nota de síntese; negativo → promover B5 ao topo da frente B e registrar porta fechada no RESEARCH_MAP. |
| **R-2** | **T0 (multicanônico) termina** | Incorporar forte-vs-fraca ao Paper SU3; reavaliar se a seção de transição muda alguma dependência (não deve — é isolada). Atualizar RESEARCH_MAP linha OT-L48. |
| **R-3** | **A2 (Wilson causet) termina** | Se σ_causet não distinguível de 0: rebaixar o claim de confinamento "no causet" no Paper SU3 para "no controle cúbico" — **reavaliar a redação do paper antes de submeter**. |
| **R-4** | **A3 (Goldstone N/S(k)) termina** | Se m(N) decai em N grande: rebaixar LRO no Paper Goldstone (PRD) **antes da submissão** já em prep. α de S(k) define como B2 mede ξ_grav → destrava/ajusta B2. |
| **R-5** | **primeira de B3/B4 dá fB>0.01 a baixa curvatura** | Escalar imediatamente (é "o mais publicável"): congelar charter de paper do fóton emergente; reavaliar prioridade de tudo o mais para baixo. |
| **R-6** | **C4 (propagação BD) termina** | Se passar: promover E2 [FRACO]→[SÓLIDO], atualizar Paper Photon-Arc. Se instável: manter ressalva, não insistir sem entender a instabilidade. |

**Regra de parada por frente (conduta da campanha):** um negativo só encerra uma linha
quando se entende *por quê*. Negativo informativo (B1 morte, A2 fronteira, B5 teorema) =
resultado de 1ª classe → RESEARCH_MAP. Negativo ambíguo (artefato de tamanho/método) →
investigar a causa antes de declarar morte (ex.: A3 m(N), B5 k_c com N maior).

---

## 4. Ordem de submissão / RESEARCH_MAP primeiro

Todo resultado novo passa pelo **RESEARCH_MAP.md** antes de virar/alterar paper (prática
vigente). Sequência de incorporação:

1. A1 verde → nota no RESEARCH_MAP + teste em CI (`test_no_scale_literal.py`).
2. B1 → nova linha "B1 razões internas" (positivo: tag [DERIVADO] para a razão;
   negativo: [EXTERNO-B] com mecanismo) → Paper Síntese.
3. A2/A3/A4 → atualizam linhas FL1/E1/E2; alimentam Papers SU3, Goldstone, Photon-Arc
   **antes** da submissão (BTFR e Goldstone estão em prep — ver STATUS.md).
4. T0 → linha OT-L48; Paper SU3 seção de transição.
5. B3/B4 → se positivo, charter de paper novo (fóton emergente).

---

## 5. Tabela de prontidão (o que falta para cada um poder rodar)

| Exp | Pré-registro | Código | Pronto para rodar após |
|---|---|---|---|
| A1 | escrever critério de literais | estender SCAN_DIRS + novo teste | **já — é o gate** |
| B1 | escrever ficha de invariância de K | escrever varredor (orquestra existentes) | A1 |
| A3 | escrever critério S(k) α | adaptar medida S(k) (FFT de C(r)) | A1 |
| A2 | escrever critério σ_causet | adaptar Wilson causet | A1 |
| A4 | escrever critério estabilidade | escrever driver de evolução BD | A1 |
| B3 | ficha fB>0.01 (já verbatim) | **classificador de cones futuros (novo)** | A1 |
| B4 | ficha anisotropia | adaptar sprinkler de Sitter | A1 |
| B2 | **definir observável ξ_grav** (não-trivial) | adaptar ξ dois setores | A3 + B1 |
| B5 | ficha k_c estável | adaptar FD1 (sr_teic_core entra na guarda) | A1 |
| A5 | — (resíduos já desenhados) | existe | A1 |

> Itens que exigem **escrever código novo** antes de rodar: B3 (classificador de cones),
> A4 (driver de evolução), o varredor de B1, o detector de literais de A1. Todos os
> demais são adaptações de geradores existentes. Nenhum roda antes da revisão da
> hierarquia pelo usuário.

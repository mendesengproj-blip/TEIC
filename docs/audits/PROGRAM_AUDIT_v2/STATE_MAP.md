# STATE_MAP — PROGRAM_AUDIT_v2 (jun/2026)

> **Natureza.** Análise documental pura. Zero simulação, zero alteração de parâmetro
> ou código. Apenas leitura e diagnóstico. Produzido por varredura completa de
> `RESEARCH_MAP.md`, `PROGRAM_AUDIT.md`, `docs/campaigns/`, `paper/submission/`,
> `paper/umbrella/` e do log git (todos os branches).

- **Audit anterior:** ENCONTRADO em `PROGRAM_AUDIT.md` (raiz do repo TEIC), produzido
  jun/2026 — "espelho honesto do estado do programa". Cobre os 4 papers de submissão,
  o ferromagneto (3 colunas DERIVADO/IDENTIFICADO/EXTERNO), as lacunas por paper e as
  conexões naturais. **Usado como baseline.**
- **Esta rodada:** **DELTA** desde o baseline. O baseline NÃO cobre três resultados
  posteriores ao seu fechamento, que são o foco desta rodada:
  1. **SU3_ORDEM_TRANSICAO** (branch `su3-ordem-transicao`, commit `551be10`) — ordem
     da transição de cor resolvida a "1ª ordem fraca provável".
  2. **COLAPSO_SR_TEIC** (branch `colapso-sr-teic`, commits `cb99f15`, `f2256b2`,
     `da9e114`) — EXP1-2, ramos FD1-2, alavancas FS1-2.
  3. **FRONTEIRA_SETA_COSMOLOGICA** (commit `41dcf4c`) — Desfecho B, fronteira fechada.
- **Nota de cobertura:** o `RESEARCH_MAP.md` da raiz **já foi atualizado** com os três
  resultados novos (itens OT #15, seção "Camada de colapso e seta do tempo"). O
  `PROGRAM_AUDIT.md` (baseline) **não**. Esta auditoria reconcilia os dois e estende o
  diagnóstico de paper para o estado pós-delta.

---

## 1. INVENTÁRIO DE CAMPANHAS (delta + estado consolidado)

### 1A — Campanhas NOVAS desde o baseline (foco desta rodada)

#### SU3_ORDEM_TRANSICAO (#15 / "OT") — branch `su3-ordem-transicao` — **COMPLETA**
- **Veredito:** **1ª ORDEM FRACA é a leitura mais provável** em L≤24; H0 (2ª ordem,
  como SU(2)) **DESFAVORECIDA**; contínua-com-forte-finite-size **não estritamente
  excluída** (calor latente abaixo da resolução até L=24).
- **Kill-criteria:** a nula pré-registrada ("2ª ordem para todo L") foi **rejeitada**
  (χ_max lei-de-volume x_eff≈3.6 > qualquer γ/ν de 2ª ordem; dip de Binder aprofunda
  0.62→0.485 sem saturar). Critério de 1ª ordem forte (bimodalidade de E) **não
  disparou** (plano 0.385→0.412, dip 0.00).
- **Status do resultado:** **[MEDIDO]** — leitura "1ª ordem fraca" é inferência de
  peso de evidência, com dois confounds declarados (x_eff>d impossível assintótico ⇒
  pré-assintótico; histerese por sweep rápido). NÃO é [DERIVADO] limpo: é uma
  caracterização honesta com resíduo nomeado (L≳32 multicanônico).
- **Reversão registrada:** **reverte parcialmente FLB2** ("1ª ordem desfavorecida" →
  "1ª ordem fraca favorecida"). Mesmo fato (sem calor latente) + melhor medição de
  χ/Binder (grade fina ΔJ=0.01 rastreia o pico que deriva 2.65→2.74). Transparência
  exemplar: o documento explicita que é mudança interpretativa, não de dado.
- **Conexão com papers:** alimenta o **PAPER_SU3 (inexistente)** — entrega exatamente
  a "seção de ordem" que o portão Desfecho B exigia. **NÃO afeta** Goldstone PRD,
  Matter-Gravity, Photon-Arc, BTFR (ver Consistência §3).
- **Resultado sem paper:** SIM — não há veículo SU(3).

#### COLAPSO_SR_TEIC — branch `colapso-sr-teic` — **COMPLETA (ponte morta, cirúrgica)**
- **Veredito principal:** **PONTE MORTA em EXP2**, mas cirúrgica: a *saturação* de
  χ_eff de SR emerge da rede causal de TEIC; a *seta do tempo* não.
- Sub-resultados com status:
  | Sub | Pergunta | Veredito | Status |
  |---|---|---|---|
  | **EXP1** | χ_eff satura espontâneo? | **SOBREVIVE** | [DERIVADO em forma] — χ_A=λ_max(A)/N satura ~0.55 (d2)/~0.17 (d4), N-estável; reproduz a dicotomia 2-setores de SR (adjacência satura, Laplaciano/BD decaem) |
  | **EXP2 (eixo)** | ordem causal antissimétrica? | **SOBREVIVE** | [DERIVADO/estrutural] — DAG estrito perfeito, acíclico=1.000 |
  | **EXP2 (seta)** | irreversibilidade emerge? | **MORTE** | [EXTERNO] — forward/backward indistinguíveis (D_TR<3); seta só sob contorno baixa-entropia imposto (cone D_TR~55) |
  | **FD1 (η)** | η emerge ou é calibrado? | **MORTE** | [EXTERNO-B] — k_c≈1 = limiar ER genérico, não robusto (d4 desvia 33%); η não pinado |
  | **FD2 (assinatura)** | classe de colapso? | **Classe A (SR σ⁻²)** | [IDENTIFICADO] — afastado de CSL (σ⁻³)/DP (flat), mas por razão genérica-Laplaciano |
  | **FS1 (Lindblad)** | gerador CP + decoerência ∝Δx²? | **SOBREVIVE em forma** | [DERIVADO em forma] — CP via continuação Euclidiana; q mediana=2.14 (Δx²); 2 ressalvas (continuação é escolha; prefator não-universal) |
  | **FS2 (Dyson/RMT)** | espectro = DBM? | **SOBREVIVE** | [DERIVADO/estrutural] — ⟨r⟩→0.53 GOE em 3 operadores × 2 dims (positivo estrutural) |
- **Kill-criteria:** EXP2 (seta) é morte **pré-registrada e definitiva** — não reaberta.
  FD1 (η) morte pré-registrada (pico≥2× E robusto<±20%; robustez falhou). EXP3/EXP4
  originais não rodam (gated por EXP2).
- **Conexão com papers:** **NENHUM paper** (decisão explícita do autor, registrada).
- **Resultado sem paper:** SIM — candidato C3 (ver NEXT_PAPER_CANDIDATES).

#### FRONTEIRA_SETA_COSMOLOGICA — commit `41dcf4c` — **COMPLETA (fronteira fechada)**
- **Veredito:** **DESFECHO B — FRONTEIRA FECHADA.** Nenhuma estrutura de TEIC/DEV/SR
  DERIVA o contorno de baixa entropia que EXP2 mostrou necessário. Todos os 5 contatos
  examinados (C1 FRW-DEV / C2 1º evento / C3 Λ-dinâmica / C4 Big Idle-SR / C5 textura)
  são **transporte** (importam a assimetria) ou **ausentes**.
- **Kill-criteria:** todos os 5 falsificadores dispararam. Argumento-mãe: o gerador
  `sprinkle_box` é **uniforme por construção** ⇒ arrow-free; medido em EXP2 (D_TR~0).
- **Status:** **[FRONTEIRA FECHADA — universal]**. A Past Hypothesis é externa a
  TEIC, DEV e SR igualmente (status idêntico a CST/Modelo Padrão). Única fresta
  não-circular (ponto de Janus / crescimento de complexidade) é **programa externo**,
  registrada com trava em `PRE_REGISTRO_FUTURO.md`, **não** reivindicada.
- **DEV:** lida, não alterada (zero parâmetro tocado). Confirmado no documento.
- **Conexão com papers:** NENHUM paper. Resultado fica como fronteira documentada.

### 1B — Campanhas do baseline (estado consolidado, sem mudança material)

Confirmadas inalteradas desde o baseline (resumo; detalhe em `RESEARCH_MAP.md` FASE 1):

- **Geometria/gravidade:** R1–R4, D1–D3, NL1–3 [SÓLIDO forma / =CST]; MG1 [SÓLIDO forma]
  (perfil próprio do sóliton sourceia θ=G_net·M/r); E1 [SÓLIDO]; E2 [FRACO] (símbolo BD).
- **Fóton (arco E4→E6e):** E4 [MORTO], E5/E7 [FRONTEIRA não-localidade], E6/E6-3
  [FRONTEIRA TÉCNICA], E6b (altura não ajuda), E6c (curvatura cruza 0.01, marginal/
  Planckiano), E6d [MORTO] (ferromagneto não amplifica), E6e [FRONTEIRA FÍSICA]
  (frac_B∝H², O(1) só Planckiano). **A5 Anderson-Higgs [MORTO por não-localidade]** —
  3ª face da mesma não-localidade de E5/E7.
- **Matéria SU(2):** SU1–9, Q/PI/FR [SÓLIDO]; BQ [SÓLIDO adimensional, Veredito A];
  Skyrme-dominância [EXTERNO-T]; Regge-bárion [MORTO] (rotor de Casimir).
- **Matéria SU(3):** FL1 (A–D) [SÓLIDO]; FLR robustez ±10% [SÓLIDO]; OS octeto
  degenerado [SÓLIDO]; FLB/FLB2 + **OT (delta acima)**.
- **Cosmologia/fenomenologia:** LD Λ-dinâmica [CONSISTENTE]; FM2-1 ν_MOND [FRACO];
  C1 Khoury equivalência-de-limite [SÓLIDO parcial]; FM1–4 (S8) [MORTO]; FM4 m_A=CDM
  [FRACO]; HQ3/KR-PTA [IDENTIFICADO/CONSISTENTE]; R5 seleção SU(3) [SÓLIDO, Veredito B].
- **DEV←TEIC:** A1–A4 [CENÁRIO B] (parâmetros calibrados, não derivados); A5 [MORTO].

---

## 2. MAPA DE FRONTEIRAS (atualizado)

| Fronteira | Status no baseline | Mudança no delta | Status atual |
|---|---|---|---|
| **Fóton** (2-célula spacelike) | [FRONTEIRA] não-localidade | nenhuma campanha nova tocou; A5 confirma 3ª face | **[FRONTEIRA]** — inalterada; razão unificada (não-localidade ~25 vizinhos) |
| **Escalas absolutas** (G, ℏ, a₀, β, f_π, m_A) | [EXTERNO-B/T] | nenhuma campanha nova derivou escala; SR↔TEIC **reconfirma** o padrão (forma emerge, escala/mecanismo não) | **[EXTERNO]** — inalterada, reforçada |
| **3 gerações / léptons** | [FRONTEIRA] bacia única | nenhuma | **[FRONTEIRA]** — inalterada |
| **Seta do tempo (local)** | implícita | EXP2: eixo emerge, seta é input | **[EXTERNO]** — agora medido e localizado |
| **Seta do tempo (cosmológica)** | não mapeada | FRONTEIRA_SETA_COSMOLÓGICA: Desfecho B | **[FRONTEIRA FECHADA — universal]** — não dívida de TEIC |
| **SR↔TEIC camada de colapso** | inexistente no baseline | EXP1-2 + FD1-2 + FS1-2 mapeada por completo | **MAPEADA** — saturação/eixo/GOE/CP/Δx² emergem (forma); seta/η/ℏ externos. Junta cirúrgica identificada |
| **Ordem da transição SU(3)** | aberta (FLB2, 1ª ordem desfavorecida) | OT: reverte para 1ª ordem fraca | **[MEDIDO — 1ª ordem fraca]**, resíduo L≳32 |

**Leitura das fronteiras:** o delta **não move nenhuma das fronteiras "grandes"** (fóton,
escalas absolutas, gerações). Ele (a) **fecha** uma fronteira nova e a declara universal
(seta cosmológica), (b) **mapeia** uma camada nova (colapso) que confirma o padrão
forma/escala do programa inteiro, e (c) **refina** uma caracterização interna (ordem da
transição SU(3)). É um delta de consolidação e cobertura, não de avanço de fronteira.

---

## 3. CONSISTÊNCIA INTERNA

Verificação de contradições entre resultados de campanhas distintas:

1. **Algum resultado novo contradiz um [DERIVADO]/[SÓLIDO] anterior?** **Não.**
   - OT reverte FLB2, mas FLB2 nunca foi [SÓLIDO]: era [MEDIDO — 1ª ordem desfavorecida].
     A reversão é interpretativa sobre um item já marcado provisório; **não toca** o
     [SÓLIDO] de FL1 (confinamento + octeto são **independentes da ordem da transição** —
     verificado: o `RESEARCH_MAP` §2.1 e a SYNTHESIS de OT o declaram explicitamente).
   - SR↔TEIC EXP1 (saturação emerge) é coerente com o padrão forma/escala; não conflita
     com nada. EXP2 (seta externa) é coerente com Λ-dinâmica e com a fronteira cosmológica.

2. **Algum kill-criterion morreu mas o resultado foi reusado em paper?** **Não há risco
   ativo:** os três resultados novos NÃO entram em nenhum paper de submissão (decisão
   registrada). A única reutilização cross-campanha — EXP2 (seta externa) sustentando a
   FRONTEIRA_SETA_COSMOLÓGICA — é consistente (ambas concluem "seta = input").

3. **Alguma fronteira declarada fechada sem evidência suficiente?** **A seta cosmológica
   (Desfecho B) é o ponto a vigiar.** O documento fecha a fronteira com 4 argumentos
   estruturais (gerador uniforme; teorema de fundo simétrico; DEV sem setor; SR postula)
   e 0 contatos sobreviventes. A auto-checagem anti-viés está no próprio documento. **A
   honestidade do fechamento é defensável** porque cada anti-argumento é uma propriedade
   verificável, não uma narrativa. Ressalva registrada: a fresta de Janus é uma porta
   *externa* deixada explicitamente aberta — o "fechado" é "fechado para as estruturas
   atuais de TEIC/DEV/SR", não "fechado em absoluto". Isso está corretamente declarado.

4. **Reconciliação baseline ↔ delta:** o `PROGRAM_AUDIT.md` (baseline) **não menciona**
   a camada de colapso nem a seta cosmológica (são posteriores). O `RESEARCH_MAP.md` já
   as incorpora. **Não é contradição** — é defasagem temporal do baseline. Recomendação:
   quando o baseline for revisado, anexar a seção "camada de colapso" (já redigida no
   RESEARCH_MAP, linhas 818–836).

**Nenhuma contradição material encontrada.**

---

## 4. STATUS DO GUARD ANTI-CIRCULARIDADE

- `tests/test_no_circularity.py` **existe**; CI configurado em `.github/workflows/ci.yml`.
- **Não executado** nesta auditoria (restrição do charter: verificar status, não rodar).
- Evidência documental de verde nos branches do delta:
  - OT SYNTHESIS §"Anti-circularidade": "Guard `tests/test_no_circularity.py` passa
    (análise puramente real; o complexo de SU(3) fica dentro de `su3_core`)".
  - COLAPSO usa engines validados (`tier3_core`, `c5_core`, `causal_core`) sem dinâmica
    causal nova; camada nova é só parâmetros de ordem espectrais.
  - DEV_FROM_TEIC e A5 declaram guard estendido e PASSA (`RESEARCH_MAP` FASE 1).
- **Status reportado (não verificado por execução):** verde nos branches do delta,
  conforme as sínteses de campanha. Verificação por execução fica fora do escopo.

---

## 5. SÍNTESE DO ESTADO (uma frase)

Desde o baseline, o programa **não avançou nenhuma fronteira grande** mas **consolidou
três frentes**: caracterizou a ordem da transição SU(3) (1ª ordem fraca, com resíduo
honesto), mapeou cirurgicamente a camada de colapso contra a Stochastic Rupture
(saturação/eixo/GOE/CP/Δx² emergem; seta/η/ℏ externos — o mesmo padrão forma/escala do
programa inteiro) e fechou a fronteira da seta do tempo cosmológica como problema
*universal*, não dívida de TEIC — restando, do lado de publicação, **um veículo para o
SU(3)** (inexistente) e **uma face faltante (A5) no arco do fóton**.

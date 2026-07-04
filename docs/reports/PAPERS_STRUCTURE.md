# PAPERS_STRUCTURE — estrutura dos quatro papers (Fase 2 do TEIC_REWRITE)

> Âncora de coerência produzida ANTES de qualquer LaTeX. Baseada em
> `REWRITE_MAP.md` (Fase 1). Cada resultado citado abaixo existe no mapa de
> quatro colunas. Marcação [D]/[I]/[N]/[A] = Derivado / Identificado / Negativo /
> Aberto. Regra de voz: "we derive/establish/show" só para [D]; "we assume/add/
> extend" para [I]; o [N] é reportado como resultado; o kill criterion em destaque.
>
> **Mudança de enquadramento (por que reescrever):** os papers antigos
> apresentavam a TEIC como "redescoberta da CST + 3 resultados". Hoje a TEIC parte
> do mesmo substrato causal e deriva fóton, MOND microscópico, matéria escura fria,
> matéria bariônica com spin-½, e tem confirmação observacional inicial + 2 kill
> criteria. O nome permanece **TEIC**. A DEV nunca é nomeada nos papers (é a EFT
> efetiva interna; ver `TEIC_DEV_CORRESPONDENCE.md`).

---

## Visão geral dos quatro papers

| # | Título curto | Venue | Eixo |
|---|---|---|---|
| I | A rede causal: geometria, gravitação, gravidade modificada | CQG / PRD | o substrato e sua EFT |
| II | O vácuo, o fóton, a matéria | PRD | o ferromagneto e seus modos/defeitos |
| III | A estrutura inevitável | PRL (carta) | seleção por necessidade estrutural |
| IV | Confirmação observacional | ApJL | o teste e o kill criterion |

Fio condutor entre os quatro: **um único substrato causal de Poisson** gera, em
camadas, geometria (I) → vácuo ferromagnético e seus modos/defeitos (II) → a
demonstração de que a estrutura é forçada (III) → o confronto com o céu (IV).

---

## PAPER I — A Teoria da Rede Causal

- **Título proposto:** *Emergent spacetime, Newtonian gravitation, and the operator
  structure of a tested modified-gravity theory from a discrete causal network.*
- **Venue:** Classical and Quantum Gravity (ou Physical Review D).
- **Argumento central (uma frase):** A rede causal de Poisson gera relatividade,
  gravitação newtoniana e a estrutura completa de operadores de uma EFT escalar-
  vetor-tensor testada em 167 galáxias, seleciona d=3 e SU(2) por exclusão
  estrutural, fixa quatro números puros sem parâmetros livres, e morre se a evolução
  da BTFR a alto-z for plana.

- **Resultados que entram (do mapa):**
  - Geometria [D]: R1 (SR), R2 (dimensão), R3 (Schwarzschild), R4 (curvatura), NL1–3.
  - Gravitação [D]: D1–D3 (Newton de MC livre); G∝1/K.
  - Ação mínima → 5 operadores [D]; razões algébricas (dito).
  - Operadores proibidos = GW170817 + Fermi-LAT [D]; LIV resolvida [D] (resíduo 12% [A]).
  - d=3 por exclusão [D]; atrator dinâmico [N] (T3A/B, dito como morte).
  - **SU(2) por cadeia de eliminação (MIN1–3) [D]** — ponteiro para Paper II.
  - 4 números puros [D]: 15/8π², 3/320π², πρH²/ln2, ≈520 (herança √ρ morta [N]).
  - k∝N (T3C) [D]: ℏ como granularidade causal; escala absoluta externa.
  - Λ flutuante [D] (coef. medidos; magnitude herdada CST).
  - BTFR: previsão [I] + forecast + Ciocan+2026 (0.5–0.9σ; ΛCDM ~19σ) — kill z≥2 [A].

- **Seção obrigatória:** *"What is new relative to causal set theory"* — lista
  numerada explícita: (1) dinâmica de matéria; (2) ação mínima de uma linha e seus
  5 operadores; (3) origem microscópica de uma gravidade modificada testada;
  (4) d=3 por exclusão; (5) cadeia SU(2); (6) os 4 números puros sem parâmetros;
  (7) o vácuo ferromagnético e o fóton-magnon (apontando ao Paper II).

- **Tabela obrigatória:** derivado/assumido (forma derivada / escala externa /
  número puro calculável — o padrão universal).
- **Kill criterion em destaque:** §previsões — BTFR z≥2 (não em nota de rodapé).

- **O que NÃO entra (e por quê):**
  - Ferromagneto causal E1/E2, fóton-magnon detalhado → Paper II (só citado em (7)).
  - Matéria escura m_A / FM4 → Paper II.
  - Skyrmion, spin-½, FR → Paper II (Paper I só estabelece a cadeia até SU(2)).
  - Detalhe observacional BTFR (forecast, regime KMOS, Ciocan R1–R4) → Paper IV.

- **Base:** o `paper_I.tex` atual já cobre ~80%; a reescrita (a) adiciona a cadeia
  SU(2) explícita, (b) cria a seção numerada "what is new vs CST", (c) adiciona o
  item (7) ferromagneto/fóton apontando ao Paper II, (d) promove o kill criterion.

---

## PAPER II — O Vácuo, o Fóton, a Matéria

- **Título proposto:** *The causal vacuum is an orientation ferromagnet: photons as
  Goldstone magnons and matter as topological defects.*
- **Venue:** Physical Review D.
- **Argumento central (uma frase):** O vácuo da rede causal é um ferromagneto de
  orientação cujos modos de Goldstone são fótons (derivado, sem ingrediente externo)
  e cujos defeitos topológicos são matéria — bariônica via um setor SU(2)+Skyrme
  adicionado mínimo (com spin-½ derivado) e escura via o setor massivo m_A frio.

- **Narrativa canônica (abertura):** "O vácuo não é um fluido de densidade — é um
  ferromagneto. O fóton não é uma perturbação de θ — é a oscilação coletiva de n⃗. A
  matéria não é uma partícula adicionada — é um defeito topológico do ferromagneto."

- **Resultados que entram (do mapa):**
  - VS1 [D/N]: densidade ρ NÃO é o parâmetro de ordem (resposta escravizada ao drive).
  - **E1 [D, Veredito A]:** ferromagneto de orientação confirmado (ordem de longo alcance).
  - **E2 [D, Veredito A]:** fóton = magnon BD-smeared (ω=ck, 2 polarizações).
  - **FM2-1 [D, positivo]:** ν_MOND emerge da susceptibilidade de Goldstone (χ∥~h^−1/2).
  - **FM4 [D para DM]:** m_A frio (w≈0, ρ∝a⁻³) — matéria escura de onda; FN3 [I]:
    Ω_{m_A}≈0.12 com f_A livre (escala GUT); S8 não resolvida [N] (Lyman-α).
  - E3+E3b [D, Veredito B]: matéria estável exige SU(2)+Skyrme (ferromagneto nu só
    metaestável; cone = pinçamento de contorno; sem Derrick).
  - SU1–SU9 [D]: Skyrmion B=1 estável, M≈146–207, gravita ∝ massa; Skyrme emerge
    (SC), dominância não (SD, teorema); cadeia SU(2) (MIN, ecoada do Paper I).
  - Q1–Q7 [D]: **spin-½ derivado** (verificação tripla); FR = teorema aplicado [I].
  - PI0–PI5 [D]: π₁=ℤ₂ medido; lei ε(n)=(n−1) mod 2.
  - FL3 [D, Veredito B]: aniquilação→radiação; E=mc² (c de E2, M_Sk de SU3) proíbe
    criação sub-relativística. Confirma a lei de conservação na rede.

- **Tabela obrigatória (seção central):**

  | Derivado da rede | Assumido/adicionado |
  |---|---|
  | Ferromagneto causal (E1) | SU(2) (único por eliminação, MIN1–3) |
  | Fóton = magnon BD (E2) | Skyrme (único estabilizador; dominância é teorema SD) |
  | ν_MOND da susceptibilidade de Goldstone (FM2-1) | Quantização coletiva (regra ANW) |
  | m_A frio w≈0 (FM4) | f_A (parâmetro livre, FN3) |
  | Skyrmion B=1, gravita; spin-½ (Q); FR π₁=ℤ₂ (PI) | fase FR (teorema topológico aplicado) |

- **Kill / honestidade:** seção dedicada — o que morreu (S8 nos 4 setores; criação por
  colisão; condensado espontâneo) reportado como resultado. m_A é DM mas não resolve S8.

- **O que NÃO entra:** geometria/gravitação R1–R4 (Paper I); o teste observacional da
  BTFR/RAR (Paper IV); a síntese "estrutura inevitável" (Paper III).

- **Base:** o `paper_II.tex` atual cobre U(1)/SU(2)/Skyrmion/spin/FR (~50%); a
  reescrita **reordena em torno do ferromagneto** (E1→E2→FM2-1 primeiro, depois
  defeitos), e **adiciona** E1, E2, FM2-1, FM4/FN3, FL3 — ausentes hoje.

---

## PAPER III — A Estrutura Inevitável

- **Título proposto:** *The structure a causal network cannot avoid.*
- **Venue:** Physical Review Letters (carta, 4–6 páginas).
- **Argumento central (uma frase):** A rede causal seleciona, por necessidade
  estrutural verificada, exatamente o conteúdo de operadores, a dimensão e o grupo de
  gauge que a astronomia de ondas gravitacionais, a astronomia de raios-γ e a
  existência de matéria estável em 3D selecionaram observacionalmente.

- **Frase central:** "The causal network selects, by structural necessity, precisely
  the operator content and gauge group that gravitational-wave astronomy and particle
  physics selected observationally."

- **Resultados (compacto, todos [D]):**
  - Operadores proibidos = GW170817 (Horndeski G₄ₓ/G₅) — OP1.
  - Fermi-LAT: Poisson é a única discretização LI (contraste R1 17% vs 0.8%).
  - d=3: única dimensão com gravidade de longo alcance + matéria estável — DS1–3.
  - Skyrme: emerge do coarse-graining da isotropia (SC1–3); dominância é teorema (SD).
  - 4 números puros: G (15/8π²), λ_Sk, X₀ (π/ln2), m_A — sem parâmetros.

- **O que NÃO entra:** derivações longas (ficam em I e II — esta é a síntese);
  cosmologia/BTFR (Paper IV); spin-½/quantização (Paper II).

- **Base:** `paper_III.tex` atual; revisar para incluir Skyrme-emerge + 4 números na
  forma de carta, e alinhar a frase central.

---

## PAPER IV — Confirmação Observacional

- **Título proposto:** *A rising critical acceleration at z~1: the first test of a
  causal-network modified-gravity prediction.*
- **Venue:** Astrophysical Journal Letters.
- **Argumento central (uma frase):** A previsão Δlog v=¼log[H(z)/H₀] da TEIC passou seu
  primeiro teste no regime correto (Ciocan+2026, 0.5–0.9σ) enquanto ΛCDM está a ~19σ no
  mesmo regime, com o kill criterion armado para z≥2 e uma segunda previsão falsificável
  (binárias largas newtonianas abaixo de 17 pc).

- **Resultados que entram:**
  - A previsão a₀∝H(z) [I] derivada da camada efetiva (não da geometria — dito).
  - Por que KMOS³D estava no regime errado (alta aceleração).
  - Forecast F1: gargalo sistemático; z≥2, σ_sys≤0.03, ~9–25 rotadores decidem a 3–5σ.
  - Ciocan+2026: a₀ crescendo com z (~15σ); R1–R4 com vereditos honestos; Jeanneau+26
    (eixo-massa) sem evolução — indecidível na forma, decidível no sinal.
  - **2ª previsão [I, FN4 Veredito C]:** blindagem MOND <λ_A=17.3 pc → binárias largas
    sub-pc newtonianas; debate Chae vs Banik (Gaia DR4) testa AGORA.
  - m_A como DM em aglomerados (fração; conexão FM4/FN3) — resíduo.

- **Seção obrigatória:** *"The riskiest prediction"* — kill criterion em destaque, com
  ambos os lados (BTFR z≥2 e binárias <17 pc), não enterrado nas conclusões.

- **O que NÃO entra:** a derivação da rede (Papers I/II); a microfísica do m_A (Paper II,
  só citada).

- **Base:** `paper_IV.tex` atual cobre previsão/forecast/KMOS/Ciocan (~85%); a reescrita
  **adiciona a 2ª previsão (FN4)** e a conexão m_A-DM, e consolida o kill duplo.

---

## Verificações finais (checklist por paper, da Fase 3)
1. Abstract: verbo ativo, ≤250 palavras.
2. Cada número quantitativo referenciado ao experimento (R/E/FM/FN/SU/Q/PI/FL).
3. "derives" só para [D]; "assume/add" para [I]; [N] como resultado.
4. Tabela derivado/assumido presente (Papers I e II).
5. Kill criterion nas conclusões (Papers I e IV) — em destaque.
6. "What is new vs CST" articulado (Paper I, lista numerada).
7. Ferromagneto causal com lugar central (Paper II, abertura).
8. Guard anti-circularidade `python tests/test_no_circularity.py` → exit 0.
9. Compila: pdflatex×2 + bibtex para cada paper.

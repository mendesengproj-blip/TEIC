# TEIC ↔ DEV — A Correspondência Canônica

> **O que este documento é.** A resposta consolidada à pergunta: *o que é o
> vácuo da DEV na linguagem microscópica da TEIC?* Cada correspondência já
> foi derivada ou localizada em alguma campanha; o trabalho aqui é
> consolidação, não descoberta. Charter: `VACUUM_STRUCTURE.md`.
>
> **Regra de honestidade** (a mesma de todo o projeto), aplicada linha a
> linha:
> - **[DERIVADO]** — demonstrado por experimento com número verificável
>   (a fonte está citada; o código e o JSON existem em `results/`).
> - **[IDENTIFICADO]** — proposto como hipótese consistente com os dados,
>   mas não derivado (tipicamente: a *forma* emerge, a calibração é externa).
> - **[EM ABERTO]** — não investigado ou investigado sem fechamento.
>
> Convenção de nomes: "DEV" aqui designa a teoria efetiva escalar-vetor
> (a EFT de gravitação modificada cuja estrutura de operadores a ponte
> reproduziu — `results/bridge/`, W4). Nos papers ela nunca é nomeada;
> este é um documento interno.

---

## 1. A tabela de correspondência

```
TEIC (microscópico)          →  DEV (efetivo)              →  Física observada
```

| TEIC (microscópico) | DEV (efetivo) | Física observada | Status | Fonte |
|---|---|---|---|---|
| **Evento causal** (centro de expansão; Poisson sprinkling) | ponto do espaço-tempo contínuo | tempo próprio = contagem em cadeia; dilatação √(1−β²) | **[DERIVADO]** | R1 (corr 0.9998–1.0000) |
| **Link causal** (relação elementar A→B, com fase de Stückelberg u = A·e + Δθ) | setor Proca/Stückelberg: A², A·∂θ com razões **travadas** 1:2 | massa vetorial; acoplamento escalar-vetor | **[DERIVADO]** (razões C₂/C₁=1, C₃/C₁=2 algébricas) | C1–C2, W4 |
| **Densidade ρ** (eventos por volume; contagem de Voronoi) | campo de fundo que fixa todas as escalas UV (X₀ ∝ ρ; granularidade) | G_net calculável: G·ρ²·r_c⁵ = 15/8π² (2.5%) | **[DERIVADO]** (o número puro); a escala SI é externa | CR1/CR1b, D3D |
| **Fase de gauge φ** (por link; holonomia por plaqueta) | F_μν e o termo de Maxwell −¼F² (de plaquetas, não de links) | eletromagnetismo de Maxwell; corr(holonomia/área, F) = 1.0000 | **[DERIVADO]** (forma); peso λ_p livre (como K da DEV) | W1–W2, C4→W4 |
| **Campo θ = δρ/ρ₀** (perturbação de densidade) | o escalar da DEV; □θ = J no regime fraco | potencial de Newton 1/r espontâneo; Schwarzschild 0.21% | **[DERIVADO]** | D1–D3, R3, S1(V3) |
| **Isotropia de Poisson** (única discretização sem direção preferida) | invariância de Lorentz do setor efetivo; seleção dos operadores LI | CV 0.8% vs 17% (grade); dispersão de fótons exatamente nula | **[DERIVADO]** (rede); LV residual E/B≈3 do operador cru morta como artefato (LV1–LV4b); restauração positiva numérica além do alcance computacional | R1, LIV_VECTOR, BD5 |
| **Saturação DBI** (cosseno do link satura; X → X₀) | K(X) tipo DBI: √(1−X/X₀) | regime não-linear de campo forte; fase crítica ρ_π = 18ρ₀ | **[DERIVADO]** (forma e constante pura X₀: π/ln2 a 0.29%); a escala física de X₀ é UV (∝ρ), **não** a₀ — identificação X₀↔a₀ **morta** | W3, CR3, DBI5, C3 |
| **Defeito topológico U(1)** (vórtice de winding W=1) | vórtice do setor de gauge abeliano | objeto 1D semi-estável; núcleo difunde (cos 2π = 1 — teorema de cegueira) | **[DERIVADO]** (existência e a razão da não-estabilidade) | CR_3D, CR_WILSON, PE4_V4 |
| **Defeito topológico SU(2)** (Skyrmion, hedgehog B=1) | — (a DEV não tem setor de matéria; aqui a TEIC excede a DEV) | sóliton pontual estável, massa M≈146–207, gravita ∝ massa; números quânticos de um bárion; premissas FR de spin-½ medidas (π₁=ℤ₂) | **[DERIVADO]** (existência, estabilidade com Skyrme, B=1, FR); **[IDENTIFICADO]**: "isto é um bárion" | SU1–SU9, SC1–SC3, PI0–PI4 |
| **Condensado ρ_dinâmico** (ρ promovido a campo, □ρ = J) | o que na DEV seria o setor de Higgs/magnitude | depleção total no núcleo do vórtice (espontânea DADO o vórtice, τ_dip<τ_vortex); **não** condensa sem vórtice; **não** pina o enrolamento | **[DERIVADO]** (os três fatos); a magnitude de Higgs como ingrediente irredutível é **teorema da campanha**, não lacuna | PE1–PE6, V2/V3/V4, **VS1** |

### Leituras transversais da tabela

1. **O padrão universal**: em todos os setores, *a forma é derivada, a
   escala absoluta é externa, e o número puro adimensional é calculável*.
   (G, ℏ, a₀, massas em unidades SI: externos. 15/8π², 1/120, π/ln2, ≈520,
   3/320π²: calculados.) Isso é tratado como traço estrutural da teoria.
2. **Onde a TEIC excede a DEV**: setor de matéria SU(2) completo; quartos
   gauge-invariantes (A+∂θ)⁴ com coeficiente fixado relativo (predição,
   ausente da DEV); saturação "magnética" de plaqueta; relações cruzadas
   sem parâmetro livre (a DEV tem K livre — a rede não tem nada livre no
   quociente gravitação↔matéria).
3. **Onde a DEV excede a TEIC**: calibração (a DEV é ajustada a rotação
   galáctica; a rede não entrega a₀ em unidades físicas — C3 mostrou que
   X₀∝ρ é UV) e a invariância de Lorentz manifesta (na rede ela é
   estatística, com a restauração numérica do operador local bloqueada
   pela parede de variância ρ^(3/4) — BD5).

---

## 2. Os campos hidrodinâmicos da rede

Os "campos de ordem" do vácuo — todos definidos por contagem, sem fórmula
relativística no gerador (guard ativo):

$$\rho(x) = \text{densidade local de eventos causais (contagem de Voronoi, normalizada)}$$

**[DERIVADO]** como campo: flutuação de Poisson 1/√(ρV) medida (L1–L3,
0.971±0.05); como campo *dinâmico* □ρ=J é a extensão legítima da ponte
(D1–D3) — validada em V3 (fonte pontual → 1/r, r²=0.9992).

$$J^\mu(x) = \text{fluxo causal (corrente de ação de gauge nos links incidentes)}$$

**[DERIVADO]** no setor de gauge: a corrente circulante do vórtice (V2:
circulação 0.57) é a fonte que depleta ρ_din. Como 4-corrente
hidrodinâmica geral da rede: **[IDENTIFICADO]** — usada onde precisou,
nunca formalizada como campo conservado próprio.

$$Q(x) = \text{conectividade média (links por evento)}$$

**[EM ABERTO]** como campo independente. Os momentos de link
⟨Δτ·e…e⟩ (C1) e o grau de Voronoi (PE1) cumpriram o papel até aqui;
nenhuma campanha precisou de Q(x) como grau de liberdade separado.
Candidato natural a campo de dilaton da rede — não investigado.

$$\Phi(x) = \rho_{\rm din}(x)\,e^{i\bar\phi(x)} \quad \text{(campo complexo emergente, PHI\_EMERGE)}$$

**[DERIVADO]** como composição bem-definida sem parâmetro novo (PE1) e
como mecanismo *parcial*: o setor de fase funciona (m_A do propagador;
em rede 3D proxy ~√ρ — corrigido em CR4: no substrato causal o invariante
é m²·λ_p ≈ 520, a herança √ρ morreu a 9.5σ); o setor de magnitude só
funciona com ρ dinâmico E um vórtice presente (V3), e **não** fecha a
estabilização (V4). ⟨Φ⟩ como condensado espontâneo: **morto** (PE2 + VS1).

---

## 3. As três fases do vácuo

### Fase normal (ρ = ρ₀ uniforme, sem defeitos)

- Fótons = perturbações propagantes da holonomia de fase (□θ = 0 no setor
  escalar; onda de plaqueta no setor de gauge) — **[DERIVADO]** (W1–W2).
- Gravidade = deformação lenta e estática de θ/ρ ao redor de matéria
  (□θ = J → 1/r) — **[DERIVADO]** (D1–D3).
- DEV no regime fraco — **[DERIVADO]** (é exatamente o setor quadrático
  C1–C2).
- **Estabilidade da própria fase** — **[DERIVADO em VS1, com condição]**:
  o vácuo uniforme é estável para K > K_c ≈ 8.5 e instável à depleção
  local sob ruído arbitrariamente pequeno para K < K_c. A rigidez da
  geometria é condição de existência da fase normal — um critério físico
  novo para fixar K (subproduto de VS1).

### Fase condensada (⟨|Φ|⟩ = v ≠ 0)

**Status global: [IDENTIFICADO como estrutura efetiva; NÃO emerge do
substrato — três mortes independentes].**

- m_A = e·v com v∝√ρ: reproduzido pelo Φ composto **em rede 3D proxy**
  (PE3) mas **morto no substrato causal** (CR4, 9.5σ); o invariante real é
  m²·λ_p ≈ 520. A *estrutura* abelian-Higgs (AH1–AH3: condensado, Meissner,
  vórtice pinado) funciona quando o campo complexo é **adicionado** —
  CR_ABELIAN_HIGGS, e a campanha PHI_EMERGE provou que essa adição é
  genuína (o quarto ingrediente é irredutível: PE6, V4, VS1).
- Vórtices estáveis existem **nesta fase efetiva** — [DERIVADO dado o
  ingrediente] (AH); não existem na ação mínima pura (CR_3D núcleo difunde).
- Matéria = defeitos topológicos estáveis: realizada **não** pela fase
  condensada U(1), mas pelo setor SU(2) (Skyrmion) — a rota que a
  investigação efetivamente fechou.
- Transição para esta fase: **não existe no probe dinâmico** — VS2 mediu
  crossover suave (todos os parâmetros de ordem; só um onset gradual de
  monopólos congelados em s≈1.0). O vácuo da rede não tem estrutura
  termodinâmica de fases acessível pela dinâmica da ação mínima.

### Fase saturada (local, |θ| > θ_c)

- Regime DBI não-linear — **[DERIVADO]** (W3: saturação do link; DBI2:
  fase crítica π atingida em ρ_π = 18ρ₀).
- Criação de defeitos topológicos possível — **[DERIVADO com fronteira
  precisa]**: o setor escalar **não** cria (pass-through subcrítico;
  acima de ρ_π a ação perde hiperbolicidade — fronteira de validade,
  DBI3/Cenário 4); o setor **compacto** nuclea pares kink-antikink
  **transientes** que aniquilam (análogo de pares virtuais, DBI4);
  criação **estável** exige o setor de gauge A_μ (Cenário 3) — e mesmo
  lá, colisões suaves não alcançam B≠0 (SU6: |B|≤0.41).
- Análogo do plasma de QED em campo forte — **[IDENTIFICADO]** (a
  correspondência pares-virtuais↔kink-antikink é qualitativa; CC2 só
  qualitativo).
- Experimento de Oxford (vacuum four-wave mixing) — **[EM ABERTO]**:
  nenhuma campanha conectou o regime saturado da rede a esse observável.
  Registrado como possível teste futuro do setor DBI; nenhuma previsão
  quantitativa existe hoje.

---

## 4. A hierarquia completa (6 níveis)

```
Nível 0: Rede causal (eventos + links)
Nível 1: Hidrodinâmica causal (ρ, J^μ, Q)
Nível 2: DEV — teoria efetiva (θ, A_μ, DBI)
Nível 3: Defeitos topológicos (vórtice, Skyrmion)
Nível 4: Modelo Padrão
Nível 5: Cosmologia
```

**Nível 0 — Rede causal.**
DERIVADO: tempo próprio, dimensão, curvatura, Schwarzschild (R1–R4;
coincide com CST, dito sempre); isotropia de Poisson como única
discretização viável (interno + Fermi-LAT).
IDENTIFICADO: a leitura "eventos = centros de expansão" (rota conceitual
própria; testavelmente equivalente à ordem parcial da CST).
EM ABERTO: a dinâmica de crescimento (e7/T3A/T3B: duas mortes pagas —
a rede é ansatz cinemático validado, não processo derivado).

**Nível 1 — Hidrodinâmica causal.**
DERIVADO: ρ como campo (flutuações, resposta, □ρ=J validado); J no setor
de gauge.
IDENTIFICADO: J^μ como 4-corrente geral.
EM ABERTO: Q(x); a termodinâmica do vácuo (VS2: sem transição no probe
dinâmico; ensemble térmico de Metropolis não testado).

**Nível 2 — DEV (teoria efetiva).**
DERIVADO: os 5 operadores {X, DBI, A·∂θ, A², F²} com razões Stückelberg
travadas (1,2) — links + plaquetas (C1–C4, W1–W4); quartos extras
preditos; X₀ e sua constante pura (CR3).
IDENTIFICADO: a soldagem θ = (M/α)·δρ/ρ₀ (a relação de escala da ponte ao
setor galáctico); a₀(z) ∝ H(z) (testada observacionalmente — BTFR_V3 mede
a direção certa; kill armado para z≥2).
EM ABERTO: restauração numérica positiva de Lorentz do operador local
(BD5: parede de variância); o peso de gauge λ_p (livre dos dois lados).

**Nível 3 — Defeitos topológicos.**
DERIVADO: cadeia de eliminação até SU(2) (MIN1–MIN3); Skyrmion B=1
estável com operador de Skyrme emergente da isotropia (SC1–SC3,
λ_Sk = a/√120 a 0.06%); FR medido (π₁=ℤ₂, PI0–PI4, com calibrador
declarado); relação cruzada 3/320π²; **não-dominância** como teorema
(SD1–SD4: o custo de núcleo é o único ingrediente importado, nomeado).
IDENTIFICADO: Skyrmion ↔ bárion (números quânticos batem; nenhum espectro).
EM ABERTO: criação dinâmica de B≠0 (SU6 negativo; FL3); quantização
coletiva (spin-½ como espectro — regra de quantização importada).
FECHADOS NEGATIVOS por esta campanha: **VS4** — o setor B=1 tem UMA bacia
(10 perfis → mesma massa a 0.02%; sem degenerescência de gerações; o
candidato remanescente é o espectro da quantização coletiva); **VS3** —
sem neutrino neutro: a marca ℤ₂ de spin-½ (π₁ de SO(3)) sem carga
topológica B (π₃) desenrola como perturbação trivial; spin-½ estável
exige B≠0, que carrega número bariônico (`VS3_neutrino.md`).

**Nível 4 — Modelo Padrão.**
EM ABERTO, com fronteiras medidas: não há espectro de massas, carga
elétrica como quantum, sabor, nem três gerações derivadas. VS5 (esta
campanha) **fechou negativo** o atalho aritmético: as constantes de
acoplamento (α, sin²θ_W, g_s) **não** emergem de combinações dos quatro
números puros acima do nível do acaso — e α conteria ℏ, que é do andar
de cima (contradição estrutural com dois andares). O caminho declarado:
SU(3) (FL1), SU(2)×U(1) (FL2) — novos motores, anos.

**Nível 5 — Cosmologia.**
DERIVADO: Λ flutuante com coeficientes medidos (L1–L3; magnitude 10⁻¹²²
herdada da CST, citada); redshift causal como aplicação de R2 (e8,
isolado).
IDENTIFICADO: a₀(z)∝H(z) e a previsão BTFR Δlog v = ¼log[H(z)/H₀]
(kill pré-registrado FO1 — o setor falsificável da teoria).
EM ABERTO: Λ dinâmica (FM4); CMB S8/ISW/lensing (FM1–FM3); a forma exata
da evolução de a₀ (BTFR_V3: indecidível com âncora atual).

---

## 5. O que é o vácuo DEV na linguagem da TEIC (a resposta em um parágrafo)

O vácuo da DEV é **a fase normal da rede causal**: um ensemble de Poisson
de eventos causais com densidade uniforme ρ₀, links portando fases sem
holonomia líquida, e flutuação irredutível 1/√(ρV). Sobre esse estado,
θ = δρ/ρ₀ é o escalar da DEV (sua onda é o setor □θ=0; sua deformação
estática é a gravitação 1/r), a holonomia de plaqueta é o F_μν de Maxwell,
e a saturação do cosseno do link é o K(X) tipo DBI — com as razões de
Stückelberg travadas em (1,2), que a DEV trata como livres. O que o vácuo
da rede **não é**: um condensado. Três campanhas independentes (PE2, V4,
VS1) estabeleceram que nenhum ⟨Φ⟩ ≠ 0 espontâneo existe no substrato — a
magnitude tipo Higgs é um ingrediente genuíno do andar de cima, e o vácuo
não tem transição de fase termodinâmica acessível à dinâmica da ação
mínima (VS2). A estrutura é estratificada como a tabela do §1: forma
derivada, escala externa, números puros calculáveis — e os pontos onde
isso pode morrer estão pré-registrados (`PREDICTIONS.md`, FO1–FO4).

---

## 6. Registro de manutenção

- Criado em jun/2026 pela campanha VACUUM_STRUCTURE (VS1–VS5 em
  `results/vacuum_structure/`).
- Atualizar quando: (i) qualquer linha da tabela do §1 mudar de status;
  (ii) VS3/VS4 fecharem; (iii) a vigília BTFR (FO1) disparar em qualquer
  direção; (iv) FL1/FL2 abrirem o Nível 4.
- Este documento não substitui `TEIC.md` (resumo vivo) nem
  `TEIC_NARRATIVE.md` (narrativa física); ele é a **ponte formal** entre
  os dois e os papers.

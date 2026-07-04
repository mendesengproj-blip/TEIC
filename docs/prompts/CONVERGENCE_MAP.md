# CONVERGENCE_MAP — TEIC ↔ DEV ↔ Khoury (Fase 2)

> **O que este documento é.** A síntese de convergência entre três teorias:
> a TEIC (rede causal microscópica), a DEV (EFT escalar-vetor-tensor de
> dinâmica galáctica) e o Superfluid Dark Matter de Khoury (2015,
> arXiv:1507.04730 / Berezhiani–Khoury 1506.07399). Produzido pela campanha
> `CONVERGENCE_INVESTIGATION`, Fase 2. Nenhuma campanha anterior é
> modificada; este documento **consolida e cruza**, não descobre setores
> novos.
>
> **Regra de honestidade (linha a linha):**
> - **[DERIVADO]** — verificado por experimento da TEIC com número (fonte
>   citada; código/JSON em `results/`), OU teorema-padrão de MOND que a DEV
>   demonstrável­mente herda.
> - **[POSTULADO]** — axioma da DEV (ou de Khoury) sem derivação na TEIC.
> - **[ESPECULATIVO]** — hipótese consistente, não testada.
> - **[MORTO]** — testado e refutado (com referência ao experimento).
>
> **Fontes lidas (Fase 1):** `TEIC.md`, `REWRITE_MAP.md`,
> `TEIC_DEV_CORRESPONDENCE.md`, `NIVEL4_ORIENTATION.md`,
> `results/HIGH_ENERGY_REGIME_SYNTHESIS.md`, `results/cosmology/hq2,hq3`,
> `results/cmb/fm1,fm2`, `results/matter/fl3`,
> `results/vacuum_structure/orientation/{E1,e2,e3,e3b}`,
> `results/bridge/d3_audit/D3D`, `docs/prompts/CROSS_RELATIONS_II.md`;
> DEV `paper_master/dev_master.tex` (Lagrangeano completo, Eqs.
> eq:LDEV/eq:DBI/eq:mu), `DEV/README.md`, `DEV/CLAUDE.md`.

---

## 0. CORREÇÃO DE PREMISSA DO PROMPT (obrigatória, antes de tudo)

O prompt enuncia a função DBI da DEV como
`F(X) = X₀[√(1+X/X₀) − 1]`. **Essa não é a forma canônica da DEV.**
O `dev_master.tex` (Eq. `eq:DBI`, linha 269) traz a forma com **argumento
ao quadrado**:

```
F(X) = X₀[√(1+(X/X₀)²) − 1]            (DEV canônico)
F_X  = (X/X₀)/√(1+(X/X₀)²)
```

com `X ≡ −½∇_μθ∇^μθ`, `X₀ ≡ a₀²/2` (axioma de saturação, Sec. dbi). A forma
do prompt corresponde, no máximo, à parametrização-X′ alternativa do rodapé
(`F(X′)=X₀[√(1+2X′/X₀)−1]`, `X′≡½(∇θ)²`), que difere só na convenção de sinal
de X e é idêntica ao nível de `F_X`.

**Consequência direta para a análise de Khoury (2B):** a análise assintótica
do prompt (`X≫X₀ → X^{1/2}`) está baseada na forma errada. Com a forma
canônica, os limites são:
- `X ≫ X₀` (g ≫ a₀, **Newtoniano**): `F_X → 1` (cinética canônica).
- `X ≪ X₀` (g ≪ a₀, **deep-MOND**): aqui aparece o X^{3/2} de Khoury — ver §2B.

Isto é registrado no mesmo espírito da correção do Ω_GW em HQ3 (o prompt
trazia uma fórmula errada; corrigimos sem maquiar).

---

## 2A. CORRESPONDÊNCIA PRECISA ENTRE OS CAMPOS (TEIC ↔ DEV)

Classificação: **IDÊNTICO** (mesma matemática) · **ANÁLOGO** (mesma função,
forma diferente) · **INCOMPATÍVEL** (contradição a resolver) · **SEM PAR**
(objeto sem correspondente).

| # | TEIC (microscópico) | DEV (efetivo) | Relação | Status | Fonte |
|---|---|---|---|---|---|
| 1 | Evento causal (centro de expansão; Poisson) | ponto do espaço-tempo contínuo | **IDÊNTICO** (tempo próprio = contagem em cadeia; √(1−β²)) | **[DERIVADO]** | R1 (corr 0.9998–1.0000) |
| 2 | Campo θ = δρ/ρ₀ (perturbação de densidade) | escalar θ da DEV (□θ=J no regime fraco) | **IDÊNTICO** (Newton 1/r espontâneo; Schwarzschild 0.21%) | **[DERIVADO]** | D1–D3, R3 |
| 3 | Fase de gauge φ por link (Stückelberg u=A·e+Δθ) | setor Proca/Stückelberg A², A·∂θ | **IDÊNTICO em forma** (razões C₂/C₁=1, C₃/C₁=2 **algébricas** e travadas; a DEV trata como livres) | **[DERIVADO]** (forma+razões) | C1–C2, W4 |
| 4 | Holonomia de plaqueta (winding por face) | F_μν, termo −¼KF² de Maxwell | **IDÊNTICO em forma** (corr holonomia/área = 1.0000; peso λ_p=K **livre** dos dois lados) | **[DERIVADO]** (forma); peso **[POSTULADO]** | W1–W2 |
| 5 | Saturação do cosseno do link (cúspide do cone) | K(X) tipo DBI √(1+(X/X₀)²) | **IDÊNTICO em forma**; constante pura X₀·Δθ⁻²/(ρH²)=π/ln2 (0.29%). A **escala** de X₀ é UV (∝ρ), **não** a₀ | **[DERIVADO]** (forma+nº puro); identificação X₀↔a₀ **[MORTO]** (C3) | W3, CR3 |
| 6 | Densidade ρ (contagem de Voronoi) | campo de fundo que fixa todas as escalas UV | **ANÁLOGO** (G_net·ρ²·r_c⁵=15/8π² calculável; escala SI externa) | **[DERIVADO]** (nº puro) | CR1, D3D |
| 7 | Isotropia de Poisson | invariância de Lorentz do setor efetivo | **IDÊNTICO funcionalmente** (CV 0.8% vs 17%; dispersão de fóton nula na média) | **[DERIVADO]** (rede; restauração local do operador cru bloqueada por BD5) | R1, BD5 |
| 8 | **Vácuo = ferromagneto de orientação** n⃗∈S², ⟨n⃗⟩≠0 | **fundo do condensado** (a DEV expande em torno de θ=0; a TEIC diz: expandir em torno de ⟨n⃗⟩≠0) | **ANÁLOGO → refina a DEV** (E1: transição 2ª ordem J_c(O(3))≈0.08; C(∞)=m²) | **[DERIVADO]** | E1-1/E1-2 |
| 9 | **Magnon BD** δn⃗, ω=ck, 2 polarizações | — (a DEV postula o fóton; não o deriva) | **SEM PAR na DEV** (a TEIC excede: fóton=Goldstone) | **[DERIVADO]** (ω=ck, c=0.98, m²<0) | E2-2/E2-3 |
| 10 | Defeito U(1) (vórtice winding W=1) | vórtice do setor de gauge abeliano | **ANÁLOGO**; semi-estável (núcleo difunde; cos2π=1) | **[DERIVADO]** (existência + razão da não-estabilidade) | CR_3D, PE4 |
| 11 | Defeito SU(2) (Skyrmion hedgehog B=1) | — (a DEV não tem setor de matéria) | **SEM PAR na DEV** (a TEIC excede) | **[DERIVADO]** (estável c/ Skyrme, B=1, FR π₁=ℤ₂); "é bárion" **[IDENTIFICADO]** | SU1–SU9, PI0–PI4 |
| 12 | m_A (massa do link/vetor) | m_A (massa vetorial Proca) | **ANÁLOGO em forma; INCOMPATÍVEL no mecanismo herdado** | herança m_A∝√ρ **[MORTO]** (9.5σ); nº puro m²·λ_p≈520 escala-invariante **[DERIVADO]** | CR4 |
| 13 | Condensado ρ_din (□ρ=J) | setor de magnitude/Higgs da DEV | **ANÁLOGO**; depleta no núcleo do vórtice, **não condensa sozinho** | **[DERIVADO]** (3 fatos); ⟨Φ⟩≠0 espontâneo **[MORTO]** (PE2+V4+VS1) | PE1–PE6, VS1 |

**Leitura transversal (o padrão universal):** em todo setor *a forma é
derivada, a escala absoluta é externa, o número puro adimensional é
calculável*. Os dois valores de m_A (TEIC vs DEV) **não** coincidem em
unidades físicas (ambos externos); coincidem na *estrutura* Proca/Stückelberg
com razões travadas. O único conflito real resolvido foi a herança m_A∝√ρ,
que **morreu** no substrato causal (CR4) e foi corrigida para um invariante
escala-invariante.

---

## 2B. A CONEXÃO COM SUPERFLUID DARK MATTER (Khoury 2015) — a investigação central

### Verificação 1 — A DEV reduz ao X^{3/2} de Khoury?

**Khoury usa:** `P(X) = X^{3/2}/Λ³` no regime de baixa aceleração; os fônons
do condensado mediam MOND. (A potência 3/2 é o que dá P_X ∝ √X ∝ |∇φ|, isto
é, a lei deep-MOND μ→x.)

**Resultado analítico (verificado simbolicamente):** o X^{3/2} aparece no
**limite deep-MOND da DEV (X ≪ X₀, isto é g ≪ a₀)** — *não* em X≫X₀ como o
prompt supunha (premissa baseada na forma errada de F, ver §0). A cadeia é um
teorema-padrão de MOND (Bekenstein–Milgrom AQUAL):

```
EOM da DEV (Eq. eq:MONDeq):   ∇·[ μ(|∇Φ|/a₀) ∇Φ ] = 4πG ρ_b,
                              μ(x) = x/√(1+x²)         (Eq. eq:mu, DBI-fixada)

Lagrangeano AQUAL equivalente: L = −(a₀²/8πG) F((∇Φ/a₀)²),  dF/dy = μ(√y)
Deep-MOND (x→0): μ(√y) → √y  ⇒  F = (2/3) y^{3/2}
   ⇒  L ∝ y^{3/2} = (|∇Φ|/a₀)³ = |∇Φ|³/a₀³ ∝ X^{3/2}     (X = ½|∇Φ|²)
```

Logo **L_deep-MOND(DEV) ∝ X^{3/2} ≡ P(X)_Khoury**. As duas teorias têm
**a mesma forma funcional no regime deep-MOND** — não por coincidência, mas
porque ambas reproduzem μ→x (a invariância de escala de Milgrom força L∝|∇Φ|³).

- **Onde diferem:** Khoury usa X^{3/2} **puro**, sem limite Newtoniano (precisa
  do condensado quebrar / dois-campos no regime denso). A DEV tem a **completação
  saturante**: X≫X₀ → F_X→1 (Newton), embutida no DBI. **A DBI da DEV é a UV/Newton
  completion que o X^{3/2} de Khoury não tem.**
- **Status:** **[DERIVADO]** — o limite compartilhado é teorema de MOND; a DEV o
  herda demonstravelmente (Eq. eq:mu derivada do DBI, não escolhida).
- **Correção ao prompt:** não é preciso X₀=X₀(ρ) com expoente n para "fazer
  aparecer" X^{3/2}. O X^{3/2} já está lá, no limite X≪X₀. A sugestão de tunar
  X₀∝ρ^n é desnecessária (e partia da forma errada de F).

### Verificação 2 — O ferromagneto causal da TEIC é o condensado de Khoury?

| Khoury (superfluido de partículas) | TEIC (ferromagneto do vácuo) |
|---|---|
| Condensado complexo Ψ=√ρ·e^{iφ}, grupo **U(1)** | Orientação n⃗∈S², grupo **O(3)**, ⟨n⃗⟩≠0 |
| Parâmetro de ordem ⟨Ψ⟩=√ρ₀ e^{iφ} | Parâmetro de ordem M⃗=M₀n⃗ (C(∞)=m², E1) |
| Flutuações = **fônons** (Goldstone) | Flutuações = **magnons** (Goldstone, E2: ω=ck) |
| Fônon media MOND via P(X)∝X^{3/2} | **χ∥ ~ h^{−1/2} do Goldstone dá deep-MOND** (FM2-1) |

**O achado decisivo (FM2-1):** a função de interpolação deep-MOND **emerge** da
susceptibilidade longitudinal do ferromagneto O(3): `χ∥ ~ h^{−1/2}` (anomalia de
coexistência de Goldstone, Brezin–Wallace; medido `χ∥~h^{−0.4±0.1}`). Isto é
*exatamente a estrutura de Khoury* — um modo mole (Goldstone/fônon) de um
condensado gerando a lei MOND — só que a TEIC o realiza no **vácuo sem
partículas** (orientação dos nós) em vez de num **superfluido de partículas**.

- **Status:** **ANÁLOGO [IDENTIFICADO no mecanismo]** — mesma física (Goldstone de
  condensado → deep-MOND), grupos diferentes (U(1) superfluido vs O(3)
  ferromagneto). É precisamente a dualidade "vácuo sem partículas ↔ superfluido de
  partículas" que a nota do prompt propõe — e a TEIC **deriva microscopicamente**
  (FM2-1) o que Khoury **postula** fenomenologicamente.
- **A TEIC herda ℏ de Khoury?** **[ESPECULATIVO — provavelmente NÃO].** O
  ferromagneto da TEIC é um sigma model O(3) **clássico** na rede causal; ω=ck é
  dispersão de onda clássica, sem ℏ no gerador. A quantização (e portanto ℏ) entra
  só pela coordenada coletiva (T3C: ℏ=k/N estrutural, **escala absoluta externa**) —
  e VS5 fechou que α conteria ℏ, contradição de "dois andares". Khoury oferece a
  **relação de escala de de Broglie**, não o **valor** de ℏ. O valor absoluto
  permanece externo (inalterado desde e11/T3C). Caminho C1 (Fase 3) testa se a
  identificação formal fixa ao menos a *relação* ℏ↔condensado.

### Verificação 3 — Vórtices quantizados?

- TEIC **tem** vórtices U(1) com π₁(S¹)=ℤ ⇒ topologicamente `∮∇φ·dl = 2πn`
  (winding inteiro) — **[DERIVADO]** (CR_3D, CR_WILSON). A quantização *topológica*
  da circulação de fase existe.
- Khoury prevê `∮v·dl = nℏ/m` ⇒ vórtices de escala λ_dB=h/(m_A v) ~ kpc para
  m_A~10⁻²⁴ eV, v~200 km/s.
- **A ponte falha em dois pontos:** (1) os vórtices nus da TEIC são **semi-estáveis**
  — o núcleo difunde (teorema de cegueira cos2π=1, CR_3D); só estabilizam com o
  campo complexo **adicionado** (AH, ingrediente irredutível VS1). (2) Converter
  `∮∇φ·dl=2πn` em `∮v·dl=nℏ/m` exige a **escala ℏ/m absoluta**, que é externa.
- **Status:** quantização topológica `∮∇φ·dl=2πn` **[DERIVADO]**; circulação física
  `nℏ/m` e a previsão **kpc nos halos [ESPECULATIVO]** — depende de o vácuo ser um
  superfluido-ℏ genuíno, que a TEIC nua **não** é. Caminho C6 (Fase 3) quantifica.

**Verificação numérica da escala (registrada honestamente):** com m_A>3.7×10⁻²⁵ eV
(Paper II), ξ_A=ℏ/(m_A c)=**17.3 pc** — sub-galáctico, ~7×10⁵× menor que σ8 (FM2-5).
Os vórtices da TEIC, se físicos, seriam de escala de aglomerado globular/binária larga
(a 2ª previsão FN4: λ_A=17.3 pc), **não** kpc — a menos que m_A esteja no topo da
janela (~10⁻²² eV → ~λ_dB de kpc). A previsão de "estrutura kpc" só vive no topo da
janela de massa.

---

## 2C. AS RELAÇÕES CRUZADAS COMO PONTE PARA CONSTANTES FUNDAMENTAIS

As quatro relações cruzadas (CROSS_RELATIONS_II) são **números puros
adimensionais** medidos na mesma rede:

| Setor | Número puro | Valor | Status |
|---|---|---|---|
| Gravitação | G_net·ρ²·r_c⁵ | 15/8π² (2.5%) | **[DERIVADO]** (nº puro) |
| Matéria topológica | λ²_Sk/⟨a²⟩ | 1/120 (0.06%) | **[DERIVADO]** |
| Saturação DBI | X₀·Δθ⁻²/(ρH²) | π/ln2 (0.29%) | **[DERIVADO]** |
| Massa vetorial | m²_iso·λ_p | ≈520, escala-inv. (CV 5.3%) | **[DERIVADO]** |

### Teste do prompt: G·ρ²·r_c⁵=15/8π² com r_c=r_próton e ρ=ρ_Planck reproduz G?

**Resultado: NÃO — falha por ~108 ordens de grandeza, e é dimensionalmente
inconsistente.** Cálculo (script verificado):

```
ρ_Planck (massa) = m_Pl/l_Pl³ = 5.15×10⁹⁶ kg/m³
r_c = r_próton    = 0.841 fm
G_pred = (15/8π²)/(ρ_Planck²·r_próton⁵) = 1.70×10⁻¹¹⁹  (vs G=6.674×10⁻¹¹)
   → razão 2.5×10⁻¹⁰⁹ ; ~108.6 ordens curto.

Dimensão de G·ρ²·r_c⁵ com densidade de MASSA:
   [m³kg⁻¹s⁻²]·[kg²m⁻⁶]·[m⁵] = kg·m²·s⁻² = JOULE  (NÃO adimensional)
```

**Interpretação honesta:** a relação `G_net·ρ²·r_c⁵=15/8π²` é adimensional
**apenas em unidades naturais da rede** (ρ = densidade de *contagem*, r_c e G_net em
unidades de rede). Para "reproduzir G em SI" seria preciso fixar o mapa rede→SI (o
espaçamento de rede / escala de Planck) — exatamente o que **D3D matou**: G_net é
constante em (w_M, ρ, L) mas **cavalga na rigidez K** (G_net∝1/K, expoente −1.0000), e
K é a normalização da ação, um **input externo**. Cravar simultaneamente r_c=r_próton
(escala nuclear) e ρ=ρ_Planck (escala de Planck) impõe **duas escalas físicas
independentes** que a teoria não vincula — daí o absurdo de 108 ordens.

- **Status:** identificação r_c↔r_próton para derivar G em SI = **[ESPECULATIVO →
  falha numérica]**. **Fortalece**, não enfraquece, o veredito existente: a relação é
  **[DERIVADO] como número puro**, com escala absoluta **externa** (D3D). G **não** é
  derivado; nenhuma teoria puramente geométrica o derivou e a TEIC não é exceção.
- O que *sobrevive* e é genuíno: a relação vincula G_net, ρ e r_c **entre si** sem
  parâmetro livre (o quociente gravitação↔granularidade), e isso é a ponte real — não
  o valor SI de G.

---

## 2D. A CORRIDA DIMENSIONAL E ℏ (registro de fronteira)

- T3C mediu k ∝ N^{1.008} (R²=0.99997) ⇒ ℏ = k/N **estrutural**, escala absoluta
  externa. **[DERIVADO]** (a proporcionalidade); **[POSTULADO/externo]** (o valor).
- A sugestão do prompt — medir a **dimensão espectral D_s(σ)** da rede causal de
  Poisson via heat kernel e ver se corre de d=4 (IR) a d=2 (UV) como em CDT — **não
  foi executada** na TEIC. É um observável novo e legítimo (caminho **C5** da Fase 3).
- Conexão com Khoury: se D_s→2 em pequena escala marca a escala onde a rede muda de
  regime, essa escala é candidata natural ao corte ℏ do condensado. **[ESPECULATIVO]**
  — nenhuma medição existe hoje.

---

## 3. RESUMO — ONDE AS TRÊS TEORIAS SE ENCONTRAM

```
                 TEIC (micro)         DEV (efetivo)        Khoury (superfluido)
                 ────────────         ─────────────        ────────────────────
vácuo            ferromagneto O(3)    fundo do condensado  superfluido U(1) BEC
                 ⟨n⃗⟩≠0 (E1)          (expandir em ⟨n⃗⟩)    Ψ=√ρ e^{iφ}
fóton/fônon      magnon ω=ck (E2)     postulado            fônon (Goldstone)
MOND deep        χ∥~h^{−1/2} (FM2-1)  μ=x/√(1+x²) (DBI)     P(X)∝X^{3/2}
   ⇒ MESMA forma deep-MOND  L ∝ X^{3/2} ≡ |∇Φ|³  (teorema de Milgrom/AQUAL)
matéria          Skyrmion SU(2)       —                    vórtices/halo
vórtice          π₁=ℤ, ∮∇φ·dl=2πn     —                    ∮v·dl=nℏ/m (kpc)
escala absoluta  EXTERNA (D3D,T3C)    calibrada (a₀,G,β)   ℏ do BEC (postulado)
```

**A frase de convergência:** A DEV é a EFT efetiva; a TEIC é seu substrato
microscópico (ferromagneto causal); Khoury é a mesma física da DEV numa
linguagem de superfluido de partículas. O ponto de encontro **rigoroso e
derivado** é o **limite deep-MOND L∝X^{3/2}**, que as três compartilham — e a
TEIC dá a ele uma **origem microscópica** (susceptibilidade de Goldstone do
ferromagneto, FM2-1) que tanto a DEV quanto Khoury apenas **postulam**. O ponto
de encontro **que NÃO se realiza** é a escala absoluta (G, ℏ, a₀): externa em
toda parte; o teste G·ρ²·r_c⁵ com escalas físicas falha por 108 ordens.

---

## 4. FRONTEIRAS QUE CADA CAMINHO PODERIA CRUZAR (prévia para a Fase 3)

| Caminho | Cruza a fronteira? | Probabilidade a priori |
|---|---|---|
| C1 — TEIC ≡ Khoury (equivalência formal) | ℏ como *relação* (não valor) | Média — mecanismo já meio-derivado (FM2-1) |
| C2 — G de G·ρ²·r_c⁵=15/8π² | **Não** (108 ordens; D3D) | **Baixa — quase morta** |
| C3 — Trajetórias de Regge dos Skyrmions | tensão de corda hadrônica | Média-alta (motor SU2 existe) |
| C4 — SU(2)×U(1) e 3 gerações | espectro do Modelo Padrão | Baixa (anos; VS4/VS5 negativos) |
| C5 — Dimensão espectral D_s(σ) e ℏ | TEIC↔CDT, escala de ℏ | Média (observável novo, limpo) |
| C6 — Vórtices quantizados (kpc) | estrutura nos halos | Média (analítico; depende da janela m_A) |

> Detalhamento, ranqueamento e prompts concretos: **Fase 3 →
> `CONVERGENCE_PATHS.md`** (a produzir após revisão desta Fase 2).
```

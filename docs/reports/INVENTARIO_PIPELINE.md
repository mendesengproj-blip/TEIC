# INVENTÁRIO DO PIPELINE TEIC — estado factual (Fase 0)

> Produzido por varredura direta do repositório (jun/2026), na branch de trunk de
> fato `su3-ordem-transicao` (memória do projeto: master está 121 commits atrás).
> Postura: relatar o que existe, não o que se gostaria que existisse. Fontes
> primárias lidas: `RESEARCH_MAP.md` (mestre), `STATUS.md`, `FUTURE_EXPERIMENTS.md`,
> `tests/test_no_circularity.py` (guarda), os `SYNTHESIS.md`/`PRE_REGISTRO.md` das
> campanhas em `docs/campaigns/`, e a árvore `results/`.
>
> **Este documento NÃO executa nada.** É a base factual para `HIERARQUIA_EXPERIMENTOS.md`
> e `PLANO_EXECUCAO.md`.

---

## 0. Reconciliação da campanha "em execução" (Tier 0)

O prompt instrui a não interromper uma execução de **L=32 SU(3) multicanônico**. O
estado factual encontrado:

- A campanha `docs/campaigns/SU3_ORDEM_L32/` (parallel tempering, NÃO multicanônico)
  **está CONCLUÍDA**: `L32_verdict.json` (23/jun 11:04), `SYNTHESIS.md` (11:06),
  `L32_histogram.png` (11:04). Veredito **B+D (1ª ordem reforçada; forte-vs-fraca não
  resolvida; FRONTEIRA TÉCNICA)**. Já incorporada ao `RESEARCH_MAP.md` (linha OT-L32).
- **Nenhum processo Python ativo** foi observado no host no momento da varredura.
- O sucessor exigido pelo próprio veredito de L32 é exatamente **L≳48 multicanônico /
  Wang-Landau em cluster** — que é o que o prompt chama de "L=32 multicanônico em
  execução agora".

**Decisão de conduta (sem ultrapassar):** trato qualquer job multicanônico em
andamento como **Tier 0 intocável**. Não inicio, não interrompo, não inspeciono seu
processo. O PT-L32 é tratado como concluído e já incorporado. Caso exista um job
multicanônico rodando que eu não enxergo, ele permanece off-limits; este inventário e
a hierarquia foram construídos para serem válidos independentemente do resultado dele
(a ordem da transição não afeta confinamento/octeto/Skyrmion — ver §1, FL1).

---

## 1. Mapa de campanhas (estado × paper que alimenta)

Estado: ✅ completa · ◐ parcial/fronteira · ☠ morta (negativo pré-registrado) ·
▶ em execução/sucessora imediata. "Paper": qual dos 6 papers a campanha alimenta
(G=Goldstone PRD, MG=Matter+Gravity, PH=Photon-Arc, SU3=Paper V cor, BTFR=MNRAS,
SÍNT=síntese "forma deriva, escala não").

### Geometria / substrato (coincide com CST — o chão sólido)
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| R1 (SR emerge) | ✅ | corr 0.9998–1.0; grade falha | SÍNT/G |
| R2 (dimensão) | ✅ | d=2.006, 4.004 | SÍNT |
| R3 (Schwarzschild) | ✅ | corr 1.0, err 0.21% | SÍNT |
| R4 (curvatura=Ricci) | ✅ | 23.5σ, coef −1/96 | SÍNT |
| D1–D3 / NL (1/r, não-linear) | ✅/◐ | expoente −1.02; 2ª ordem só cinemática | MG |
| C5 (dimensão espectral) | ☠ | plateau único Myrheim-Meyer; sem corrida CDT | — |

### Operadores / matéria / cor
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| C1–C4 / W1–W4 (ação mínima→5 operadores) | ✅ | {X,DBI,A·∂θ,F²,A²}, razões (1,2) | MG/SÍNT |
| SC1–3 (Skyrme emerge) | ✅ | razão 5/9 a 0.06%, λ_Sk=a/√120 | MG |
| SD1–4 (Skyrme domina?) | ☠/EXT-T | K≤⅔S identidade pontual (teorema) | MG |
| MIN1–3 (SU(2) mínimo) | ✅ | cadeia escalar→U(1)→SU(2), Bott | MG |
| SU1–9 / MATTER_SU2 (Skyrmion B=1) | ✅ | estável M≈146–207, gravita | MG |
| Q/PI0–4/FR + BQ (spin-½, FR, bárion quant.) | ✅ | E_J∝J(J+1); 2π→−1; μ_p/μ_n=−1.515 | MG |
| FQ2/PI5 (2º calibrador π₁) | ✅ | ε(n)=(n−1)mod2 | MG |
| PHI_EMERGE V1–V4 | ◐/EXT-T | magnitude emerge; enrolamento irredutível | MG |
| FL1 SU(3) A–D (cor/confinamento/octeto) | ✅ | ferromagneto cor, V~σr, octeto | SU3 |
| FLR (robustez ±10% FL1) | ✅ | σ>0, 8/8 octeto, Derrick estável | SU3 |
| R5 (por que SU(3)) | ✅ | menor grupo c/ fundamental complexa | SU3 |
| OS (espectroscopia octeto) | ✅ | octeto exatamente degenerado | SU3 |
| MG1 (matéria→gravidade) | ✅ | expo −0.992, G_net cte | MG |
| C3 (Regge bárion) | ☠ | Casimir m²∝J(J+1), não linear | — |
| FL3/HE/SU6 (criação de matéria) | ☠ | E=mc² proíbe; aniquila | — |

### Vácuo / orientação / fóton
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| E1 (vácuo ordena, ferromagneto) | ✅ | transição 2ª ordem J_c≈0.08, C(∞)=m² | G/PH |
| E2 (magnon=fóton ω=ck) | ◐ FRACO | ω=ck do SÍMBOLO BD; **campo não propaga estável** | PH |
| E4 (fóton=Goldstone) | ☠ | escalares internos, p=0.23, sem k-locking | G |
| E5 (fóton no link U(1) Wilson) | ◐ FRONTEIRA | motor ok; confinamento inconclusivo (não-localidade grau∝L^2.9) | PH |
| E6 / E6b–e (operador BD-gauge) | ◐ FRONTEIRA(téc+fís) | E²−B² gauge-inv; H2 falha no causet; curvatura ajuda mas só Planck (frac_B∝H²) | PH |
| E7 (U(1) Coulomb vs confina) | ◐ FRONTEIRA | crossover β≈1; Coulomb não certificado (sem Creutz no causet) | PH |

### Cosmologia / DEV / ponte
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| CR1–4 (relações cruzadas) | ✅ | 15/8π², 1/120, ≈520 (nº puros) | SÍNT |
| DS1–3 (d=3 por exclusão) | ✅ | única c/ gravidade+escape+sóliton | MG |
| L1–L3 + LD (Λ everpresent + dinâmica) | ✅ | δρ/ρ=0.971; Λ_rms∝ρ_crit^1.107 consistente | — |
| CONVERGENCE / C1 (TEIC≡Khoury) | ✅/◐ | deep-MOND L∝X^{3/2}; equiv. de limite longitudinal | SÍNT |
| FM2-1 (ν_MOND da susceptibilidade) | ◐ FRACO | χ∥~h^(−0.4±0.1) | BTFR/SÍNT |
| FM4 (m_A=CDM de onda) | ◐ CDM / ☠ S8 | w≈0 frio SIM; S8 não (Lyman-α) | SÍNT |
| FM1/FM2/FM3/HQ2 (S8) | ☠ | S8 não resolvido em 5 ataques (1 razão estrutural) | — |
| FN3/FN3b (relíquia m_A, f~GUT) | ◐ B | Ω_{m_A}h²≈0.12 alcançável; f_A livre | — |
| HQ3 + KR-PTA (m_A vs NANOGrav) | ◐ B/consist. | linha KR roça limiar; SGWB 21 ordens abaixo | — |
| C6 (vórtices quantizados) | ◐ B | circulação física no setor m_A (Madelung) | — |
| BTFR_V3 (a0∝H(z)) | ✅ | confirmado em sinal por Ciocan 2026 (~19σ) | BTFR |
| DEV_FROM_TEIC A1–A4 + A5 (DEV deriva?) | ☠/EXT-B | Cenário B: formas emergem, escalas externas; A5 morre por não-localidade | SÍNT |

### Crescimento / dinâmica
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| T3A/T3B (d=3+1 da regra e7) | ☠ | não-manifold d*=1.43 | — |
| T3C (ℏ estrutural k∝N) | ✅/EXT-B | α=1.008, R²=0.99997; valor externo | SÍNT |
| FM5 (regras alternativas a e7) | ☠ | toda forma graduada → d≈1.3–1.4 | — |

### Colapso / SR
| Campanha | Estado | Resultado central | Paper |
|---|---|---|---|
| COLAPSO EXP1 (saturação) | ✅ | reproduz dicotomia 2-setores da SR | — |
| COLAPSO EXP2 (seta do tempo) | ☠ | eixo emerge; seta é input | — |
| FRONTEIRA_SETA_COSMOLÓGICA | ◐ FECHADA | Past Hypothesis externa a TEIC/DEV/SR | — |
| FD1 (η emerge?) | ☠ | k_c≈1 = limiar ER genérico; η não pina | — |
| FD2 (assinatura colapso) | ✅ classe A | Γ∝σ_x⁻² (SR-like) | — |
| FS1 (ponte Lindblad) | ◐ sobrevive | gerador CP via continuação Euclidiana; Δx² | — |
| FS2 (Dyson/RMT) | ◐ sobrevive | espectro causal = GOE/DBM, ⟨r⟩→0.53 | — |

### Ordem da transição SU(3) (linha viva)
| Campanha | Estado | Resultado | Paper |
|---|---|---|---|
| FLB2 (L≤16) | ✅ | 1ª ordem desfavorecida (revertido depois) | SU3 |
| OT (L≤24, Binder-crossing) | ✅ | **1ª ordem fraca provável**; χ lei-de-volume x≈3.6 | SU3 |
| **OT-L32 (parallel tempering, L=32)** | ✅ (verdict B+D) | **1ª ordem reforçada**; forte-vs-fraca NÃO resolvida; PT não cruza a barreira (0 round-trips, swap 0.118 no gargalo) | SU3 |
| **▶ L≳48 multicanônico/Wang-Landau** | ▶ Tier 0 / sucessor exigido | resolver forte-vs-fraca-vs-contínua | SU3 |

**Papers (6, status conhecido):** Goldstone (PRD, submissão prep), Matter+Gravity,
Photon-Arc (com correção E4 + addendum A5/Anderson-Higgs), SU3 (Paper V draft), BTFR
(MNRAS, submissão prep), Síntese "forma deriva, escala não". A ordem da transição **só
muda a força da evidência da seção de transição do Paper SU3** — não toca confinamento,
octeto, Skyrmion.

---

## 2. Resultados pendentes / não-incorporados (débito técnico)

O `RESEARCH_MAP.md` está **notavelmente atualizado** — incorpora tudo até OT-L32 e A5
inclusive. O débito real é pequeno e é majoritariamente **documental**, não de medição:

1. **`FUTURE_EXPERIMENTS.md` está parcialmente obsoleto** (débito documental, médio).
   Lista como "futuro" coisas já feitas/revisadas pelo programa:
   - FN1–FN4 ("Nível 4 — orientação") aparecem como campanha futura, mas a campanha de
     orientação/fóton (E1/E2/E4) **já foi executada** e o veredito-chave (fóton=Goldstone)
     **morreu** (E4). A tabela de prioridades de `FUTURE_EXPERIMENTS.md` ainda lista
     FN1/FN2 como "ALTA — primeira nova campanha após papers".
   - FL1 (SU(3)) listado como "BAIXA prioridade, longo prazo, novo motor" — **já é
     [SÓLIDO]** (FL1 A–D + FLR + R5 + OS).
   - FM1–FM4 listados como "ALTA/MÉDIA prazo" — **todos ☠ para S8** (RESEARCH_MAP).
   → **Ação:** marcar/arquivar entradas superadas, redirecionando para o RESEARCH_MAP
     como fonte de verdade. Não é perda de resultado; é risco de alguém reabrir linha
     morta por ler o doc errado.

2. **Resíduos medidos-mas-não-fechados (débito de medição, baixo):**
   - **PI1_B2 / FR:** ε(2) entre dois campos winding-2 **distintos** nunca foi
     re-medido (FQ2/PI5 usou um calibrador winding-3 classe-1). Resíduo menor explícito.
   - **MG1:** versão Skyrmion-3D-na-sprinkling-causal → relaxador BD 3D não rodada
     (a redução radial é exata para o hedgehog, mas a versão 3D é o teste mais forte).
   - **LD (Λ dinâmica):** sem solve estocástico autoconsistente; fundo ΛCDM importado;
     assinatura testável w_eff(envelope)≈−0.66 registrada mas não confrontada.
   - **FM5:** família CSG completa (t_n) não varrida (só formas graduadas).

3. **Não há resultado de simulação "órfão"** (medido e jogado fora) detectado: cada
   `*.json`/`*_synthesis.md` em `results/` tem entrada correspondente no RESEARCH_MAP.
   A corrida `prod_l32_miscentered.json` foi preservada e explicitamente descartada do
   veredito por transparência (não é débito — é boa prática registrada).

---

## 3. Experimentos desenhados (critério de morte) mas NÃO executados

Fontes: Seção 6 e 7 do `RESEARCH_MAP.md` ("o que nunca foi tentado"), os charters em
`docs/prompts/`, e os `PRE_REGISTRO_FUTURO.md`.

| ID | Pergunta | Critério de morte (resumido) | Código | Urgência (RM) |
|---|---|---|---|---|
| **4b-2cell** | Existe 2-célula spacelike Lorentz-inv. no causet → fóton magnético? | frac_B fica <0.01 em BAIXA curvatura em toda geometria testada | adaptar `results/gauge/e6*` | ALTA / dif. ALTA |
| **E2-prop** | O campo de orientação propaga ω=ck por **propagação direta** (não só pelo símbolo BD)? | dispersão não-linear ou instável sob operador BD *smeared* | adaptar (E2 + BD smeared de e10) | (Tier 1, base) |
| **E7-Coulomb** | O setor U(1) certifica fase de Coulomb? | sem discriminador área-vs-perímetro construível | fronteira (causet não-local) | MÉDIA |
| **DEV←TEIC #6** | a₀, β, A_μ, η em unidades físicas? | escala não deriva (4 falhas já) | parcial existente | ALTA / dif. ALTA |
| **#13 inércia** | Inércia como princípio isolado | observável não-definível de forma não-trivial | novo | BAIXA |
| **#16 léptons** | Léptons como objetos próprios | sem ponto de entrada / sem modo zero | novo motor | BAIXA / MUITO ALTA |
| **#17 SU(2)×U(1)** | Eletrofraco + 3 gerações | sem breaking ou massas erradas (VS4/VS5 negativos) | novo motor | BAIXA / MUITO ALTA |
| **FC1 fermions** | Férmions = defeitos/modos de borda? | nenhum modo spin-½ genuíno acoplado à cor | novo motor de índice | ALTA-import/BAIXA-exec |
| **CSG-family** | Família completa de regras de crescimento → d=4? | toda regra → d≠4 ou não-manifold | motor Tier-3 (existe) | BAIXA-MÉDIA |

**Experimentos NOVOS propostos pelo prompt (não desenhados ainda no repo)** — entram em
`HIERARQUIA_EXPERIMENTOS.md` com pré-registro a escrever:
- **Razões internas independentes de K** (M_Sk, σ, G_net) — problema de hierarquia.
- **Razões de comprimento de correlação entre domínios** (ξ_grav/ξ_cor; transmutação dimensional).
- **2-célula spacelike por classificação de bivetor de cones futuros** (Direção B genuína).
- **Geometria anisotrópica** (de Sitter flat slicing com anisotropia) (Direção A).
- **Por que η e ℏ não pinam** (teorema vs artefato de tamanho).
- **S(k)~k^α do setor Goldstone** com N maior e range de k amplo.
- **Auditoria formal da guarda** (literais numéricos em todos os geradores).

---

## 4. Cobertura da guarda anti-circularidade (lacuna real e concreta)

`tests/test_no_circularity.py` roda **VERDE** (confirmado). O que ela faz: proíbe
fórmulas de dilatação SR/GR em **qualquer** código gerador, e proíbe números complexos
exceto em blocos rotulados `COMPARISON ONLY` (fase QM postulada) ou `SU(3) GROUP-DEF
COMPLEX` (definição de Gell-Mann). É uma guarda **sintática por diretório**.

**O ponto crítico — a guarda só varre 6 diretórios** (`SCAN_DIRS`):
`src`, `experiments`, `results/matter`, `results/bridge`, `results/tier3`,
`results/dev_from_teic`.

| Diretório | .py (excl. pycache) | Na guarda? | Conteúdo |
|---|---|---|---|
| src | (motor) | ✅ | núcleo causal |
| experiments | (e1–e11) | ✅ | geometria/CST |
| results/matter | 140 | ✅ | SU2/SU3/baryon/skyrme/**su3_core.py** |
| results/bridge | 58 | ✅ | operadores, cross-relations, wilson, BD |
| results/dev_from_teic | 8 | ✅ | A1–A5 |
| results/tier3 | 7 | ✅ | crescimento |
| **results/vacuum_structure** | **34** | ❌ | **E1–E4 orientação/fóton** |
| **results/cosmology** | **33** | ❌ | fn3, fn4, hq2, hq3, lambda_dyn, kr_pta, c6, he2 |
| **results/phi_emerge** | **23** | ❌ | V1–V4 |
| **results/gauge** | **23** | ❌ | **E5, E6 (operador BD-gauge)** |
| **results/cmb** | **12** | ❌ | fm1–fm4 |
| **results/falsification** | **11** | ❌ | testes de falsificação |
| **results/foundations** | **7** | ❌ | **C5, R5** |
| **results/audit** | **7** | ❌ | auditorias (bridge_recheck, gemini) |
| **results/convergence** | **1** | ❌ | C1 |
| **results/predictions** | **1** | ❌ | — |
| **docs/campaigns/COLAPSO_SR_TEIC** | **10** | ❌ | tem **`sr_teic_core.py` próprio** |
| **docs/campaigns/SU3_ORDEM_L32** | **2** | ❌ | importa su3_core (scanned) |
| **docs/campaigns/SU3_ORDEM_TRANSICAO** | **2** | ❌ | importa su3_core (scanned) |

**Total de código gerador/análise FORA da varredura automática: ≈166 arquivos `.py`.**

Status de cada um:
- A maioria das campanhas fora-da-guarda **alega "guard verde"** nas suas sínteses
  porque (a) reutiliza um core já varrido (`su3_core` está em `results/matter` ✅) e
  (b) sua camada de análise é "puramente real". Isso é **plausível mas não verificado
  pela própria guarda** — é uma afirmação humana, não um teste que roda.
- Exceção que merece atenção: `docs/campaigns/COLAPSO_SR_TEIC/sr_teic_core.py` é um
  **gerador próprio** (não importa core varrido) e está **fora** da guarda.
- `results/gauge/e6*` (operador BD-gauge) manipula **bivetores/assinatura indefinida** e
  está fora da varredura — é exatamente onde "injetar uma fase" seria mais sutil.

→ **Esta é a lacuna #1 da frente de consolidação** (Tier 1): a guarda declara um
protocolo, mas ~166 arquivos geradores nunca passam por ela. A auditoria formal pedida
pelo prompt (listar literais numéricos, checar coincidência com c/G/ℏ a <1%) **também
não existe** — a guarda atual é só anti-dilatação/anti-complexo, não anti-literal-de-escala.

---

## 5. Tamanhos atuais (N/L) por campanha de finite-size scaling

| Campanha | Tamanhos usados | Limite de convergência | Alvo de "N maior" |
|---|---|---|---|
| **Goldstone / E4** (orientação) | **N = 175 … 1462** eventos | U4=2/3 em todo N; m(N) monotônico | prompt pede **N~5–10k** (≈3–7× acima do atual) |
| **E1 ferromagneto** (FSS E4-0) | reforço de FSS feito | LRO confirmada | idem Goldstone (mesma rede) |
| **SU(3) ordem (FLB2)** | L ≤ 16 | unimodal | superado |
| **SU(3) ordem (OT)** | **L = 8,12,16,20,24** (ΔJ=0.01, grade fina) | χ lei-de-volume; calor latente não resolvido | superado por L32 |
| **SU(3) ordem (OT-L32, PT)** | **L = 32** (gate L=16) | **barreira NÃO cruzada** (0 round-trips, swap 0.118) | **L≳48 multicanônico** (Tier 0) |
| **E6 / E6b–e (fóton link)** | N ≤ 626 (E6-3); N ≤ 2000 (E6b); 28k plaquetas (E6c) | frac_B satura ~3% (∝H²), Planckiano | 2-célula spacelike / anisotropia |
| **A5 Anderson-Higgs (causet)** | N = 331 (grau Hasse 25) | morre por não-localidade | — |
| **S(k) structure factor** | **não há campanha S(k) dedicada** detectável | — | proposta nova (Tier 1) |
| **Tier-3 crescimento** | N ≈ 2000 (~80s/run) | d*≈1.3–1.4 | (motor disponível) |

Observações de convergência relevantes para a hierarquia:
- O setor **Goldstone é o de maior alavanca de "N maior" barata**: N_max atual 1462 vs
  alvo 5–10k, mesma física, motor existente.
- O setor **SU(3) ordem está no teto do que desktop/PT alcança** (L=32). O próximo
  passo é qualitativamente diferente (multicanônico + cluster) — Tier 0, não Tier 1.
- Não existe medida de **S(k)** do setor Goldstone no repo: o expoente α (campo médio
  α=0 vs relativístico α=−1) **nunca foi medido** — é experimento novo, não "N maior".

---

## 6. Síntese factual para a hierarquia

1. **A base está madura e bem-documentada.** RESEARCH_MAP é fonte de verdade confiável;
   débito de medição é pequeno e localizado (§2). Isso favorece gastar esforço de Tier 1
   onde há **lacuna estrutural** (guarda §4) e não em re-documentação.
2. **A guarda tem uma lacuna real e mensurável** (~166 arquivos fora da varredura;
   sem auditoria de literais de escala). É a consolidação de maior retorno: transforma
   "protocolo declarado" em "evidência verificável" e cobre o ponto mais sutil (e6 gauge,
   sr_teic_core). **Custo baixo, decisividade alta, destrava confiança em TODO o resto.**
3. **A frente de escalas tem um alvo executável com código existente:** razões internas
   independentes de K (M_Sk, σ, G_net). Todos os três já foram medidos isoladamente
   (FL1, MG1) — falta só testar se uma combinação é número puro. **É o único ataque ao
   problema de hierarquia que não exige fixar unidade SI.**
4. **A fronteira do fóton (E6) está precisamente localizada:** falta 2-célula spacelike
   O(1) em baixa curvatura. Altura (E6b), curvatura isotrópica (E6c/e) e acoplamento
   ferromagneto (E6d) estão **esgotados**. Restam exatamente as duas direções do prompt:
   **anisotropia (A)** e **2-célula genuinamente nova / bivetor de cones futuros (B)**.
5. **Goldstone N maior + S(k)** é a consolidação mais barata e decisiva do setor que já
   gerou um paper (PRD): decide campo-médio vs relativístico para o setor de orientação.
6. **Tier 0 (multicanônico L≳48) é independente do resto:** seu resultado só afeta a
   força da evidência da seção de transição do Paper SU3; confinamento/octeto/Skyrmion
   não dependem dele. A hierarquia abaixo é válida rode ele o que render.

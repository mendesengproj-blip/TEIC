# RESEARCH_MAP — Mapa Completo de Pesquisa TEIC + DEV

> **Archive note (EN).** The complete research map — what is solid, what is weak,
> what was postulated by hand, what was never tried — kept in Portuguese as the
> working language of the research record. It is included here as evidence of
> method (pre-registered kill criteria, negatives reported as negatives). File
> references to `docs/…` and `results/…` point into the full research archive,
> available from the author on request.

> **O que este documento é.** Um mapa honesto e completo de todo o programa
> TEIC+DEV: o que está sólido, o que é fraco, o que foi postulado à mão, o que
> foi inferido em vez de medido, e o que nunca foi tentado. É um documento de
> **diagnóstico e roteiro**, não de execução nem de criação de papers. Produzido
> jun/2026 por varredura completa do repositório (FASE 1).
>
> **Postura.** A mesma do protocolo anti-circularidade: não inflar o que temos,
> não esconder o que falta. Papers são SAÍDA do programa, não GUIA. Ver
> "Protocolo de pesquisa" ao final.
>
> **Documentos-fonte primários:** `TEIC.md`, `STATUS.md`,
> `docs/reports/RELATORIO_TEIC.md`, `TEIC_DEV_CORRESPONDENCE.md`,
> `CONVERGENCE_MAP/PATHS/GAPS.md`, `FL1_SU3_FOUNDATION.md`,
> `paper/PAPER_MATTER_GRAVITY.tex`, `FM4_WAVE_CONDENSATE.md`,
> `E6_BD_GAUGE.md`, `HQ3_NANOGRAV.md`, `FUTURE_EXPERIMENTS.md`.

---

## Sistema de tags (aplicado a cada item)

```
[SÓLIDO]        — medido, protocolo verificado, critério de morte não disparado
[FRACO]         — plausível mas com brecha técnica real (inferido vs medido,
                  ou dependente de escolha não justificada)
[POSTULADO]     — ingrediente inserido à mão, declarado externo, NECESSIDADE
                  não provada por teorema
[EXTERNO]       — declarado externo COM prova de necessidade (teorema ou 4+ falhas)
[MORTO]         — testado com critério pré-registrado, falsificado
[NUNCA TENTADO] — lacuna conhecida, nunca atacada
[FRONTEIRA]     — atacado mas obstruído por razão de princípio
[IDENTIFICADO]  — forma/números batem com objeto conhecido, mas escala não derivada
```

Distinção crítica entre os dois "externos":
- **[EXTERNO-T]** (por teorema): necessidade provada (ex.: dominância de Skyrme, K≤⅔S).
- **[EXTERNO-B]** (por falha de busca): não encontrado em 4+ tentativas (ex.: G, ℏ, a₀ em SI).
- **[EXTERNO-B-geométrico]** (gradação introduzida por B1+B5+B6, jun/2026): o input que
  falta para fixar o **valor preciso** é uma propriedade **geométrica e calculável em
  princípio** do substrato (dimensão, clustering do grafo causal, forma-de-bordo) — **não**
  uma constante arbitrária do mundo real. A *forma* e o *mecanismo* são [DERIVADO]; só o
  número exato herda a correção geométrica. **Distinto de [EXTERNO-B] simples** (G, f_π em
  SI: escalas dimensionais sem rota de cálculo). No Paper Síntese deve aparecer como uma
  **gradação**, não na mesma categoria de G ou f_π.

---

# FASE 1 — Varredura completa do repositório

Cada campanha executada, sua pergunta, resultado, status da afirmação central e a
brecha mais concreta.

| Campanha | Pergunta atacada | Resultado | Status central | Brecha mais concreta |
|---|---|---|---|---|
| **R1** | SR emerge da rede Poisson? | corr 0.9998–1.0000; grade falha (CV 17%) | [SÓLIDO] (=CST) | A ação ser quadrática é input, não derivada |
| **R2** | dimensão por contagem? | d=2.006, 4.004 | [SÓLIDO] (=CST) | — |
| **R3** | Schwarzschild não-circular? | corr 1.0000, err 0.21% | [SÓLIDO] (=CST) | regime r→2M em aberto |
| **R4** | curvatura = Ricci? | 23.5σ; coef −1/96 | [SÓLIDO] (=CST) | — |
| **D1–D3** | 1/r emerge da ação BD? | expoente −1.02, sem ansatz | [SÓLIDO] (forma) | d=3 é input; ação linear (sem back-reação) |
| **NL1–NL3** | 2ª ordem de Schwarzschild? | converge 0.06% cinematicamente | [FRONTEIRA] | não-linearidade genuína (λ livre); só cinemático |
| **C1–C4/W1–W4** | ação mínima → operadores? | 5 operadores {X,DBI,A·∂θ,F²,A²}, razões (1,2) | [SÓLIDO] (forma+razões) | pesos K, λ_p livres (externos) |
| **BRIDGE_RHO** | ρ(r) derivável? | P1 circular; P2 passa cinemático; P3 impõe perfil | [FRACO] | P3 impõe o perfil que deveria emergir |
| **E1** | vácuo ordena? | transição 2ª ordem J_c≈0.08, C(∞)=m² | [SÓLIDO] | — |
| **E2** | magnon = fóton (ω=ck)? | ω=ck, c=0.98, 2 polarizações | [FRACO] | é do OPERADOR BD (símbolo); campo não propaga estável |
| **E4** | fóton = Goldstone de orientação? | escalares internos, p=0.23, sem k-locking | [MORTO] | — (medição clara) |
| **E5** | fóton no link U(1) Wilson? | motor validado; confinamento INCONCLUSIVO | [FRONTEIRA] | não-localidade do causal set (grau∝L^2.9) |
| **E6** | Maxwell no link propaga? + operador BD-Lorentziano dá fóton? | H1 estrutura PASS; H2 Euclidiano FALHA; **E6-3 (jun/2026): operador BD-gauge indefinido E²−B² construído (split E/B por bivetor de área), gauge-inv 5.7e-16, validado em rede 4D (zero crossing segue ω=ck, c=1.05), mas H2 FALHA no causet**; **E6b (jun/2026): varredura de ALTURA do diamante (2h-gon, h=2..6, N≤2000) — zero EXATO só de height-2; B-type aparece em h≥3 mas como cauda ~0.25% NÃO-crescente, b²/e²↓ com h → INCONCLUSIVO (pende estrutural)**; **E6c (jun/2026): varredura de CURVATURA (de Sitter, R̂=∞→2, ordem conforme-plana = ensemble E6b idêntico, split E/B no embedding 5D do hiperbolóide) — GATE PASS (R_dS=∞ reproduz E6b exato), frac_B SOBE monotonicamente com curvatura, b²/e² por célula 0.11→0.97 (8.6×); em R̂=2 (R_dS≈1.68ℓ, trans-Planckiano) h=4 CRUZA 0.01 (frac_B=0.0117, Wilson-lo 0.0105, N-estável, 28k plaquetas) → SUCESSO (marginal, curvatura-extrema); h=2 fica 0.0000 em TODA curvatura (imune)**; **E6d (jun/2026): acoplamento ferromagneto↔gauge Φ=A+λ(n×n)·ê_z no substrato CURVO de E6c (R̂=2,h=4); coupling realizado no embedding aumentado 7D (componente interno-interno = ½λ²Σ(n×n)·ê_z exato) → G0/G1 PASS bit-for-bit, mas G2 FALHA: frac_B sobe com λ (até 0.27 em λ=2) MAS pela DESORDEM, não pela ordem — λ=2: desordenado 0.272 > J_c 0.205 > 2J_c 0.099 (mais ordem = MENOS magnético); ordem até SUPRIME em λ pequeno → HIPÓTESE DE AMPLIFICAÇÃO FALSIFICADA [MORTO]**; **E6e (jun/2026, ANALÍTICO, sem MC novo): extrapolação dos 5 pontos de E6c (bem condicionada, σ_rel≤17% — não 1 ponto como temido) — o EXCESSO de curvatura Δfrac_B ∝ (1/R̂)^1.73 ≈ H² (R²=0.997); O(10%) exige R̂≈0.5–0.6, O(50%) R̂≈0.2–0.3, O(5%) R̂≈0.8–0.9 — TODOS R̂<1 (raio de curvatura < espaçamento ℓ ≡ ℓ_Planck [ASSUMIDO]); modelo exponencial (R²≈0.99) SATURA em ~3% (O(10%) inalcançável em qualquer R̂) → [FRONTEIRA FÍSICA]: setor magnético O(1) só em curvatura Planckiana; universo observável (R̂ enorme) tem frac_B≈0 → mecanismo NÃO explica os fótons observados** | [FRONTEIRA TÉCNICA + FRONTEIRA FÍSICA] (refinado por E6b; revisado UPWARD por E6c; E6d fecha acoplamento; **E6e quantifica: curvatura funciona mas só na escala de Planck**) | **diamantes height-2 são 100% elétricos em flat E sob curvatura (imune); E6b: height NÃO ajuda; E6c: a CURVATURA ajuda (frac_B∝H²) e cruza 0.01; E6d: ferromagneto NÃO amplifica (ruído da desordem, ordem suprime); E6e: O(10%) exige R̂≈0.5–0.6 sub-Planckiano.** Falta: fração magnética O(1) em BAIXA curvatura — todas as alavancas testadas (altura/curvatura-isotrópica/acoplamento) ou mortas ou Planckianas; resta geometria anisotrópica/inomogênea ou 2-célula genuinamente diferente |
| **E7** | setor U(1) está em fase de Coulomb ou confinante? | crossover confina→Coulomb perto de β≈1 (espelha rede 4D); Coulomb não certificado; "confina em todo β" DESFAVORECIDO | [FRONTEIRA] (inconclusivo, lean) | discriminador limpo (Creutz em retângulos R×T) inconstruível no causet não-local; surrogate de patch falha o controle Stage-A |
| **MIN1–3** | SU(2) é mínimo? | cadeia escalar→U(1)→SU(2) medida; Bott | [SÓLIDO] (contido) | minimalidade entre candidatos, não unicidade |
| **SC1–3** | Skyrme emerge? | razão 5/9 a 0.06%; λ_Sk=a/√120 | [SÓLIDO] (forma) | só a forma; dominância não (SD) |
| **SD1–4** | Skyrme domina sozinho? | K≤⅔S identidade pontual (Cauchy–Schwarz) | [MORTO] / [EXTERNO-T] | — (teorema de impossibilidade) |
| **MATTER M1–P4** | escalar livre = partícula? | campo clássico sem massa | [MORTO] (matéria do escalar) | — |
| **MATTER_COMPLEXITY** | massa = custo causal? | E²=(pc)²+(mc²)² fecha, mas definicional | [FRACO] | núcleo construído, não emergente; sem escala |
| **MATTER_CREATION/CR_*** | colisão cria matéria? | ação BD linear: atravessa; só AH estabiliza | [MORTO] (criação escalar) | exige campo complexo adicionado |
| **PHI_EMERGE V1–V4** | 4º ingrediente eliminável? | magnitude emerge; enrolamento NÃO (Derrick) | [FRACO]→[EXTERNO-T] | cos2π=1 cega ρ; custo de núcleo irredutível |
| **SU1–9 (MATTER_SU2)** | Skyrmion B=1 estável? | estável, M≈146–207, gravita | [SÓLIDO] (c/ Skyrme externo) | Skyrme externo (SD); massa em unid. de rede |
| **Q1–7 / PI0–4 / FR** | spin-½ + estatística FR? | E_J∝J(J+1); 2π→−1; troca=rot2π∈ℤ₂ | [SÓLIDO] | ε(2) entre winding-2 distintos não re-medido; **inércia de Q2 era só-σ → corrigida em BQ (#12)** |
| **BQ (bárion quantitativo #12)** | a quantização coletiva dá os números bariônicos? | torre FR `(2j+1)²=[4,16,36]` (N,Δ,j=5/2), spin=isospin, razão `8/3` (1%); inércia completa σ+Skyrme (Skyrme=43%, 𝓘=1.76× Q2); 1 calibração (N–Δ) → e=5.39 (ANW 5.45, 1%); μ_p/μ_n=−1.515 (ANW −1.43, exp −1.46), raio 0.65 fm, g_A=0.56 — parameter-free | [SÓLIDO] (estrutura adimensional do bárion) — Veredito A | f_π escala [EXTERNO-B] (conv. F_π=2f_π); correntes EM importadas (como a fase FR de Q4); g_A herda ~10-30% do Skyrme mínimo |
| **FQ2/PI5** | 2º calibrador π₁? | classe 1 = previsão; ε(n)=(n−1)mod2 | [SÓLIDO] | residual ε(2) menor |
| **CR1–4** | relações cruzadas sem param.? | 15/8π², 1/120, π/ln2, ≈520 | [SÓLIDO] (nº puro) | m_A herança √ρ MORTA (9.5σ) |
| **DS1–3** | d=3 por exclusão? | única c/ gravidade+escape+sóliton; Derrick={3} | [SÓLIDO] (estrutural) | — |
| **L1–L3 (LAMBDA)** | Λ flutuante? | δρ/ρ=1/√(ρV) (0.971); de Sitter R²=0.9999 | [SÓLIDO] (estática) | ~~dinâmica temporal NUNCA TENTADA~~ → **LD (jun/2026): feita; rastreia ρ_crit, dissolve coincidência, CONSISTENTE** |
| **LD (Λ dinâmica #7)** | Λ(t) everpresent evolui consistente? | Λ_rms∝ρ_crit^1.107 (R²=0.996); finita z=0; Ω_Λ~O(1) por 6.9 e-folds (vs 1.0 ΛCDM) | [CONSISTENTE] (diagnóstico; modelo importado) | w_eff envelope≈−0.66 (borda alta DE); sem solve estocástico autoconsistente; fundo ΛCDM importado |
| **LV1–4b (LIV)** | LIV E/B≈3 real? | artefato de regulador; teorema e²>b² | [MORTO] (ameaça) | restauração positiva além do alcance numérico |
| **T3A/T3B** | d=3+1 emerge da regra e7? | não-manifold, d*=1.43; seeds não fluem | [MORTO] (p/ e7) | vale p/ e7, não p/ família RS geral (FM5) |
| **T3C** | ℏ estrutural k∝N? | α=1.008, R²=0.99997 | [SÓLIDO] (proporção); [EXTERNO-B] (valor) | escala absoluta externa |
| **FL1 (SU3) A–D** | SU(3), cor, confinamento? | ferromagneto cor + Skyrmion + V~σr + octeto | [SÓLIDO] | **robustez FECHADA (FLR, jun/2026):** confinamento+octeto+Skyrmion sobrevivem ±10%; ordem de transição ainda inconclusiva L≤12 |
| **FLR (robustez FL1)** | SU(3) sobrevive a ±10% na ação? | σ(2,2)>0, 8/8 octeto, Derrick estável p/ todo ε | [SÓLIDO] | resolve R1 do roteiro; σ-drift reflete coupling efetivo, não perda de confinamento |
| **MG1 (matéria→gravidade)** | Skyrmion sourceia M/r com perfil próprio? | expo −0.992; A∝M (G_net cte 5 díg.); = top-hat | [SÓLIDO] (forma) | resolve R2; G_net absoluto continua [EXTERNO]; resíduo: versão 3D-sprinkling |
| **C1 (TEIC ≡ Khoury)** | equivalência é identidade de fônon ou só limite? | χ⊥~h^{−0.98} (magnon ∝X) vs χ∥~h^{−0.37} (deep-MOND); ρ_s cavalga em J | [SÓLIDO] (limite parcial) | resolve R3; equivalência no setor longitudinal, não no fônon; a₀ externo reforçado |
| **FM5 (formas de regra)** | morte do e7 generaliza a outras formas? | toda forma graduada → d_int≈1.3–1.4, não-manifold; nenhuma →4 | [MORTO] (generaliza) | reforça T3A/T3B; regra que premia componentes dá d MENOR (surpresa) |
| **FLB2 (ordem da transição SU3)** | transição de cor é 1ª ordem ou contínua? | histograma de E unimodal em L=12/14/16; dip de Binder encolhe; χ_max ruidoso | [MEDIDO] — 1ª ordem DESFAVORECIDA | resolve resíduo de FLB; previsão N≥3 não suportada; resíduo: 1ª-ordem-fraca em L=24–32 |
| **OT (ordem da transição SU3 #15, L≤24)** | reabre FLB2 com Binder-CROSSING + L=20,24 | χ_max 2.45→125.6 (x_eff≈3.6 super-volume), U4 no pico aprofunda 0.62→0.485, cruzamentos não convergem ao pico, histerese 0.17→0.20; **MAS bimodalidade de E plana/ausente até L=24** | [MEDIDO] — **1ª ORDEM FRACA (leitura provável); H0 2ª-ordem DESFAVORECIDA; contínua-forte-finite-size não excluída** | **REVERTE parcialmente FLB2**: grade fina (ΔJ=0.01) rastreia o pico que deriva (2.65→2.74) → χ lei-de-volume que FLB2 perdia; concorda c/ FLB2 que calor latente é não-resolvido. V1 ok (J_c(L8)=2.65). Pré-registro+kill-criteria congelados; L=24 condicional (regra disparou). Resíduo: forte-vs-fraca-vs-contínua exige L≳32 multicanônico/cluster |
| **OT-L32 (ordem da transição SU3, parallel tempering, L=32)** | resolve forte-vs-fraca-vs-contínua em L=32 via PT (alt. ao multicanônico) | gate L=16 PASSA-parcial (U4=0.563≈OT 0.565; χ ~25% menor = des-inflação do sub-equilíbrio de OT). L=32: **P(b) bimodal numa banda contígua de 5 slots centrais (dip≤0.60)**, **degrau abrupto de χ** (8→185 em ΔJ=0.004), **gargalo de troca de PT localizado EM J_c** (swap 0.118 vs 0.4–0.5 nos bulks = diagnóstico de 1ª ordem), aprisionamento metaestável abaixo de J_c; x(16→32)=3.67≈volume | [MEDIDO] — **1ª ORDEM REFORÇADA (qualitativa); 2ª-ordem E contínua-finite-size AMBAS mais improváveis; forte-vs-fraca NÃO resolvida (FRONTEIRA)** | **AVANÇA OT, não reverte.** PT **não cruza a barreira** (up_crossings=0, swap 0.118 no gargalo) ⇒ ΔF/calor latente não-quantificados — §6.1 fronteira disparada. Gargalo+metaestabilidade são intrínsecos à 1ª ordem (não erro de ladder; corrida centrada confirmou). L=40 não-viável E não-informativo (barreira piora c/ L). Requisito atualizado: **L≳48 multicanônico/Wang-Landau em cluster**. Guard verde. `docs/campaigns/SU3_ORDEM_L32/SYNTHESIS.md` |
| **OS (espectroscopia octeto #11)** | o octeto de Goldstone é um multipleto degenerado? espectro quantitativo? | octeto **exatamente degenerado** (spread 4e-8 cubic+causal; desacoplamento harmônico (J/3)·Laplaciano); ρ_s≈1/3, c=√(2/3); D2 ~10% = costura de toro do λ8 (Cartan irracional), removida → 9e-6 | [SÓLIDO] (degenerescência + reconciliação) | escala lattice→GeV externa (usual); sem split de massa de quark (limite quiral exato); dispersão causal herda E2 |
| **R5 (seleção do grupo de cor)** | por que SU(3), não SU(N≥4)? | SU(3)=menor grupo simples c/ fundamental complexa / d^abc≠0 (fronteira N=2\|3, exato N=2..8); topologia (π₃ Bott) não distingue 3 de 4 | [SÓLIDO] (seleção estrutural) — Veredito B | minimalidade ≠ unicidade; requisito "complexa" importado (como d=3); rede nunca mede N |
| **FL3 / HE1 / HE3 / SU6** | criação de matéria (B≠0)? | aniquila; sinal fixo; 0 pares | [MORTO] | E=mc² proíbe por construção |
| **FM1** | MOND realça → S8? | σ8 piora (μ≥1 sempre realça) | [MORTO] | — |
| **FM2** | DM = fase do campo MOND? | obstrução estrutural (ordem vs ponto crítico) | [MORTO] (S8) | — |
| **FM2-1** | ν_MOND da susceptibilidade? | χ∥~h^(−0.4±0.1) vs −0.5 teórico | [FRACO] | tamanho finito empurra p/ 0; identificação |
| **FM3** | textura primordial fria? | w≈−1/3, não fria | [MORTO] | — |
| **FM4** | m_A = matéria escura de onda? | w≈0 frio SIM; S8 não (Lyman-α) | [FRACO] (CDM) / [MORTO] (S8) | misalignment importado da cosmologia FRW |
| **HQ2** | ferromagneto crítico → S8? | morte (parte das 4 portas S8) | [MORTO] | — |
| **HQ3** | m_A vs NANOGrav? | linha KR roça limiar; SGWB 21 ordens abaixo | [FRACO] / [IDENTIFICADO] | ~~busca direta nos dados PTA NUNCA feita~~ → **KR-PTA (jun/2026): feita; linha NÃO excluída, abaixo do limiar, CONSISTENT** |
| **KR-PTA (busca direta #10)** | linha KR do m_A já foi buscada/excluída nos PTAs? | PPTA-2018/NANOGrav-15yr não excluem nem 100% DM na janela (f_max=2.5→2160); f_max=1 só em ~2.6e-24 eV (abaixo da janela); Lyman-α força subdominante | [CONSISTENTE] (não excluído) | sem matched-filter dedicado em resíduos crus (usa curvas publicadas); limite PPTA extrapolado por escala white-noise |
| **VS1** | condensado espontâneo? | resposta linear escravizada; K_c≈8.5 | [MORTO] (condensado) | subproduto: K_c critério físico |
| **VS2** | transição de fase do vácuo? | crossover suave, sem salto | [MORTO] | ensemble térmico Metropolis não testado |
| **VS3** | neutrino neutro de vida longa? | marca ℤ₂ sem B desenrola trivial | [MORTO] | — |
| **VS4** | gerações no B=1? | bacia única, 10 perfis → 0.02% | [MORTO] | candidato restante: espectro de quantização coletiva |
| **VS5** | constantes via aritmética dos 4 nº? | matches = acaso; α conteria ℏ | [MORTO] | — |
| **C3 (Regge)** | bárion tem trajetória de Regge? | Casimir m²∝J(J+1), não linear | [MORTO] (Regge bárion) | (resolvido: bárion=rotor, tubo=corda) |
| **C5 (dim. espectral)** | D_s corre 4→2 como CDT? | **JÁ EXECUTADO** (jun/2026): D_s = plateau único = Myrheim-Meyer; queda sub-d é corte de discretude (invariante por refinamento), sem corrida CDT | [MORTO] (operador viável) + [FRONTEIRA] (operador BD afiado inacessível, ρ^{3/4}) | ℏ permanece externo; `results/foundations/c5/` |
| **C6 (vórtices quant.)** | circulação física ∮v·dl=nℏ/m? | **JÁ EXECUTADO** (jun/2026, veredito B): circulação real via condensado m_A (Madelung, FM4); ferromagneto rejeitado (sem ℏ) | [DERIVADO em forma] (setor m_A) / [IDENTIFICADO] | previsão kpc condicional ao topo da janela m_A; ℏ externo; `results/cosmology/c6/` |
| **CONVERGENCE (Fase 1–3)** | TEIC≡DEV≡Khoury? | deep-MOND L∝X^{3/2} compartilhado | [SÓLIDO] (limite) / [NUNCA TENTADO] (C1 lattice) | Λ_Khoury da rede não derivado |
| **DEV_FROM_TEIC (A1–A4 #13)** | a DEV *deriva* da TEIC (Cenário A) ou é teoria efetiva compatível mas independente (Cenário B)? 4 ângulos nunca tentados | **JÁ EXECUTADO (jun/2026): CENÁRIO B.** A1 (A_μ = modo longitudinal massivo?) **[EXTERNO-B]**: gap longitudinal FECHA ∝h^0.31 (= anomalia Brezin–Wallace = deep-MOND), sem massa Proca espontânea; transverso Goldstone (G0 pass), longitudinal ~36× mais pesado mas ambos→0. A2 (a0~cH0 geométrico?) **[INCONCLUSIVO]**: h_sat É escala interna (∝ρ_s^−0.48, R²=0.90) mas sinal OPOSTO à hipótese X0∝+ρ_s(J−J_c); a0 absoluto externo. A3 (β=ρ_s(J0)/K?) **[EXTERNO-B]**: ρ_s/K=0.34 em J0=1 (**48× β**); bate β só em J_c≈0.65 (fine-tuning crítico). A4 (slip η geométrico?) **[EXTERNO-B]**: slip do Skyrmion O(1) (interior 31%, platô exterior 61%) — FORMA de slip genuína mas ~15× a janela DEV [2.2%,4.1%]; precisa do A_μ ausente (A1) | [CENÁRIO B] — parâmetros DEV (a0,β,m_A,η) **calibrados, não derivados**; só FORMAS emergem (1 correlato parcial: A2) | padrão recorrente "forma com correlato de rede, escala/valor externo" (coerente c/ C1, a0/f_A [EXTERNO-B], E4 photon morto); guard estendido p/ `results/dev_from_teic/` e PASSA |
| **A5 ANDERSON–HIGGS (#14)** | A_μ massivo da DEV emerge se o U(1) do link "engole" um Goldstone do ferromagneto (Anderson–Higgs)? extensão direta de A1 | **JÁ EXECUTADO (jun/2026): MORTE por NÃO-LOCALIDADE.** Construção abelian-Higgs exatamente gauge-invariante (O(3) gaugeado⊗U(1) não-compacto, hopping covariante real cos/sin, |ΔS|≤7e-12). **G1 (lattice cúbica 4D): PASS** — m_A: 0→0.63 com λ (massless→massivo), m_A: −0.08(J_c)→0.63(2J_c)→1.07(3J_c) (massa ∝ condensado, zero sem ordem); λ≥2/g≥2 derretem o condensado (fronteira real). **Fase B (causal set, N=331, grau Hasse 25 vs 8 local, cresce c/ N): MORTE** — ferromagneto ordena puro (charged bond 0.91 em λ=0), MAS com λ>0 a ordem FOGE p/ o eixo neutro não-gaugeado (charged 0.91→0.00, neutral 0.00→0.91 já em λ=0.1): as ~25 fases de gauge incoerentes por evento frustram o condensado in-plane → U(1)_z fica NÃO-quebrado → nenhum Goldstone comido → fóton massless, m_A=0; gauge mais rígido (g=0.2) NÃO resgata | [EXTERNO-B mecanismo-nível] — A_μ não emerge via Higgs; o mecanismo é correto (G1) mas a não-localidade causal o obstrui especificamente | 3ª face independente da não-localidade E5/E7 (após Wilson loops e discriminador de Coulomb): agora o condensado de Higgs; reforça A1 e Cenário B; `results/dev_from_teic/a5/`, guard PASSA |

---

# FASE 2 — O Mapa

## Seção 1 — Substrato e Geometria

O **chão sólido**, e a contribuição mais honesta do programa. **Mas: tudo aqui
coincide com a Causal Set Theory (CST).** O distintivo é a rota conceitual
(expansões locais superpostas vs ordem parcial abstrata), não o conteúdo testável.

### 1.1 Relatividade especial (R1) — [SÓLIDO]
(a) **[SÓLIDO]**: corr 0.9998 (cadeia) / 1.0000 (volume); a grade regular falha
(CV 17% vs 0.8%). O contraste é o ponto: Lorentz exige aleatoriedade de Poisson.
(b) **Brecha:** nenhuma técnica no resultado em si; a brecha é de **originalidade**
— é redescoberta fiel da CST (Bombelli–Hensonm–Sorkin 2009).
(c) Fechar: nada a fechar internamente; só posicionamento honesto (já feito).
(d) Tentado, sólido.

### 1.2 Dimensão, Schwarzschild, curvatura (R2–R4) — [SÓLIDO]
(a) **[SÓLIDO]** os três (d=2.006/4.004; corr 1.0000 / 0.21%; −1/96 a 23.5σ).
(b) **Brecha:** = CST; Schwarzschild forte (r→2M) explicitamente em aberto.
(c) Fechar r→2M exigiria a completação não-linear (mesma brecha da gravidade).
(d) Tentado, sólido; horizonte [FRONTEIRA].

### 1.3 Gravidade newtoniana 1/r (D1–D3) — [SÓLIDO] na forma, com brechas nomeadas
(a) **[SÓLIDO]** para a FORMA: expoente −1.02 sem ansatz, Poisson para 4 fontes
estendidas (corr 0.9998), superposição exata (resíduo 1.8e-9).
(b) **A brecha mais concreta (a que o prompt antecipou):** a equação de Poisson em
3D produz 1/r **trivialmente, DADO que a ação é quadrática**. O resultado
interessante seria mostrar **por que** a ação da rede é quadrática — e isso **não é
derivado**: a ação BD é o operador CST padrão, escolhido, e a não-linearidade
genuína (back-reação −½Rφ, setor Einstein/Regge) **não está** na ação como usada
(NL1: λ livre). A dimensão d=3 é **input geométrico** (o 1+1D literal prefere perfil
blindado). O valor de G_net cavalga em K (G_net∝1/K, expoente −1.0000, D3D) —
**[EXTERNO-B]**.
(c) Fechar exigiria: (i) derivar a quadraticidade da ação da estatística de Poisson
(não feito); (ii) a completação não-linear (Regge/Einstein) — campanha de fronteira.
(d) Forma tentada e sólida; quadraticidade e não-linearidade **[NUNCA TENTADO]** /
**[FRONTEIRA]**.

> **Resumo Seção 1:** o núcleo geométrico é o resultado mais sólido do programa,
> mas é CST. A única afirmação "além de CST" aqui — que a forma quadrática + 1/r
> emergem de uma rota conceitual nova — não tem teorema que force a quadraticidade.

---

## Seção 2 — Vácuo e Campo

### 2.1 Ordenamento espontâneo (E1) — [SÓLIDO]
(a) **[SÓLIDO]**, reforçado por E4-0 (FSS: m(N) sobe 0.961→0.991, U4=2/3, 13–38× acima
do piso N⁻½ → ordem de longo alcance **genuína**, não artefato de tamanho finito).
**Ressalva (atualizada jun/2026):** ordem da transição medida limpa em O(3) (J_c≈0.08);
no setor SU(3) ficou inconclusiva em L≤12 (FLB). FLB2 (L≤16) desfavoreceu 1ª ordem com
χ_max ruidoso (grade grossa errava o pico). A campanha **OT (L≤24, Binder-crossing,
ΔJ=0.01)** corrige o rastreamento do pico (deriva 2.65→2.74) e **REVERTE
parcialmente**: χ_max cresce lei-de-volume (x_eff≈3.6, super-volume), dip de Binder
aprofunda (0.62→0.485), histerese 0.17→0.20 → **1ª ordem FRACA é a leitura mais
provável; H0 (2ª ordem, como SU(2)) desfavorecida**. Porém o calor latente
(bimodalidade de E) segue **ausente e plano até L=24** ⇒ 1ª ordem só *fraca*
(coexistência abaixo da resolução), e contínua-com-forte-finite-size não estritamente
excluída. Detalhe: `docs/campaigns/SU3_ORDEM_TRANSICAO/SYNTHESIS.md`.
A campanha seguinte **OT-L32 (L=32, parallel tempering)** chega a L=32 e **AVANÇA** (não
reverte): aparece **P(b) bimodal numa banda contígua de slots centrais**, um **degrau
abrupto de χ** em J≈2.703, um **gargalo de troca de PT localizado exatamente em J_c**
(diagnóstico de 1ª ordem — gap de energia entre as fases) e **aprisionamento metaestável**
abaixo de J_c. Estas assinaturas, ausentes/mais fracas em L≤24, **reforçam a 1ª ordem** e
tornam tanto a 2ª-ordem quanto a contínua-com-finite-size **menos prováveis**. **Mas o PT
não tuneliza através da barreira** (up_crossings=0; swap 0.118 no gargalo) ⇒ ΔF e o calor
latente **não são quantificados** e **forte-vs-fraca segue em aberto**. O gargalo é
intrínseco à 1ª ordem (a barreira cresce com L; PT canônico cruza em tempo exponencial —
por isso o multicanônico existe), confirmado pela corrida centrada; L=40 é não-viável e
não-informativo. **Requisito atualizado de L≳32 para L≳48 com multicanônico/Wang-Landau
em cluster.** Detalhe: `docs/campaigns/SU3_ORDEM_L32/SYNTHESIS.md`.

### 2.2 Dispersão relativística via operador BD (E2/E4) — [FRACO]
**A brecha exata (como o prompt formulou):** ω=ck é propriedade do **operador BD**
(o símbolo do d'Alembertiano de Sorkin–Benincasa–Dowker), **não do campo de
orientação em si**. No setor de matéria (P2) o sinal de dispersão ω²=k²+m² ficou
**soterrado sob a variância do BD** — o campo não propaga de forma estável; a
dispersão é do **símbolo**, não de uma dinâmica de campo estável e medível. É um
**[FRACO]** real: a forma relativística existe no operador padrão, mas não como
propriedade dinâmica robusta do campo da rede.

### 2.3 O Fóton — arco completo E4→E6
- **E4** — orientação: os 2 modos transversais são **escalares internos**
  (corr autovetor↔k̂ = 0.10, permutação p=0.23), **não** vetor de gauge → **[MORTO]**.
- **E5** — link U(1) Wilson: motor validado (G1 gauge-inv. 1.8e-15; G2 transição 4D;
  G3 resolvido), plaquetas-diamante gauge-invariantes, MAS o teste de fóton está
  **[FRONTEIRA]**: a U(1) nua herda a **não-localidade mean-field** do substrato
  (grau médio cresce 34→133; região {futuro, τ≤τ_max} tem volume infinito em
  Minkowski — não existe vizinhança local de volume finito Lorentz-invariante).
- **E6** — Maxwell não-compacta no link: **H1 PASS** (estrutura de gauge real,
  redundância = N−1, 1184 modos físicos transversos — a estrutura que E4 não tinha),
  **H2 FALHA**: a ação ½ΣF_P² é **positiva-definida (Euclidiana)**, mínimo em ω≈0,
  não dá ω=ck. **[FRONTEIRA]**.
- **E6-3 (jun/2026)** — o **operador BD-gauge LORENTZIANO** (assinatura indefinida
  E²−B²) FOI construído e medido (`results/gauge/e6/E6_3_bd_lorentzian.*`,
  `E6_literature.md`). Cada plaqueta-diamante é classificada E-type (bivetor de área
  timelike, A^{0i}) vs B-type (spacelike, A^{ij}) e entram com sinais opostos,
  `w=(b²−e²)/(b²+e²)`. **H1 PASS por construção** (gauge-inv 5.7e-16 — a assinatura
  indefinida NÃO quebra invariância: F=dθ, BG=0=d²); **validação STAGE-0 PASS** (em
  rede 4D regular o zero crossing do símbolo segue ω=ck, c=1.05, dev 3%). **Mas H2
  FALHA no causet, com razão agora PRECISA:** os diamantes causais height-2 são
  **100% elétricos** (fração B-type = **0.0000 exata** em 9 sprinklings, N≤626) — todo
  diamante contém a extensão timelike ponta-passada→ponta-futura, então `b²<e²` sempre.
  O **setor magnético é VAZIO**, o símbolo fica `λ∝−E²∝−ω²` (sempre negativo) e nunca
  cruza zero. Não é a falha Euclidiana de E6-2 (positiva-def., min em ω=0); é a falha
  oposta de um operador corretamente indefinido **sem termo B² para balancear**.
  **[FRONTEIRA TÉCNICA]** — assinatura resolvida, falta uma **2-célula spacelike** na
  ordem causal (não um peso diferente). Refina o "non-locality" de E5/E6-1 para uma
  afirmação concreta: o 2-complexo de diamantes causais carrega só células timelike.
- **E6b (jun/2026)** — varredura de **ALTURA** do diamante (`results/gauge/e6b/`,
  `E6b_synthesis.md`). Generaliza a plaqueta height-2 para um **2h-gon** (duas cadeias
  ascendentes de comprimento h entre as pontas; h=2 reproduz o 4-gon de E6 com B-type
  **0.0000 exato** — âncora de validação). Mede a fração B-type para h=2..6, N≤2000, 3
  seeds (E/B reusa `e6_bd_core` verbatim). **Resultado: o zero EXATO é específico de
  height-2.** Células spacelike B-type **aparecem** em h≥3 — mas como uma **cauda ~0.25%
  que NÃO cresce** (best-sampled N≈2000: h3=0.0024, h4=0.0025, h5=0.0016, h6=0.0010,
  declinando) e cujo **b²/e² por célula DECRESCE com h** (0.22→0.08). Nenhuma célula bem
  amostrada chega ao limiar 0.01 (o único 0.0105 é flutuação de 4 células em P=381,
  contradito pelo N=2000,h=6=0.00096). **Veredito INCONCLUSIVO (pende estrutural)** — o
  critério de morte (`<0.001` em todo h) não disparou estritamente, então E6 **mantém**
  [FRONTEIRA TÉCNICA], mas a afirmação "setor magnético VAZIO/estrutural" de E6-3 é
  **corrigida** para "vazio só em height-2; cauda de medida-zero (~0.25%, não-crescente)
  em h≥3" → setor magnético ~400× mais fraco que o elétrico, **sem cone de luz em nenhuma
  altura**. A rota "diamante mais alto" para a 2-célula spacelike está **descartada**.
- **E6c (jun/2026)** — varredura de **CURVATURA** (`results/gauge/e6c/`,
  `E6c_synthesis.md`). Rota ortogonal à de E6b: em vez de diamantes mais altos, **curvatura
  espacial** (fundo de Sitter dS₄, fatiamento plano). de Sitter é **conforme-plano**, então
  a **ordem causal** nas coords conformes `(η,x)` é a MESMA de Minkowski/E6b — sprinkla-se
  uma **caixa conforme cúbica**, dando o **ensemble de causet idêntico ao de E6b em toda
  curvatura** (sem colapso de estatística; a curvatura é a única variável). O split E/B é
  lido do **embedding 5D do hiperbolóide** `−X0²+ΣXi²=R²` (curvatura entra SÓ no bivetor;
  `e6_bd_core` reusado verbatim, D=5). **GATE obrigatório PASS:** R_dS=∞ reproduz E6b
  bit-a-bit (h2=0.0000, h3=0.0024). **Resultado: curvatura FURNECE setor magnético,
  monotonicamente** — oposto da altura. frac_B sobe a cada passo de curvatura; o `b²/e²` por
  célula sobe **8.6×** (h=4: 0.11→0.97). Em **R̂=2** (R_dS≈1.68ℓ, ~escala de Planck; E6e fixa
  o sub-Planckiano em R̂<1), h=4:
  **frac_B=0.0117, Wilson-lo 0.0105 > 0.01**, N-estável, **28k plaquetas** (não flutuação) →
  **critério SUCESSO pré-registrado DISPARA**. Calibração honesta: o cruzamento é
  **marginal (1.17%) e só em curvatura extrema**; o diamante médio segue elétrico
  (`b²/e²=0.97<1`) — setor magnético é cauda ~1.2% na **borda do cone (E²≈B²)**, não O(1).
  **h=2 fica 0.0000 em TODA curvatura** (imune: contém sempre a extensão timelike
  ponta-a-ponta). **DEATH NÃO disparou** (frac_B ≫ 0.001 em toda parte) → E6 **mantém**
  [FRONTEIRA TÉCNICA] mas **revisado upward**: a obstrução "setor magnético inutilizável" é
  **flat-específica e curvatura-removível**; a 2-célula spacelike **existe e cresce com
  curvatura**. Falta: tornar a fração magnética **O(1)** (b²/e²>1 típico), não cauda.
- **E6d (jun/2026)** — acoplamento **ferromagneto↔gauge** no substrato CURVO de E6c
  (`results/gauge/e6d/`, `E6d_synthesis.md`). Direção B: testa se o ferromagneto ordenado de
  E1 (campo O(3) n⃗∈S²) acoplado ao gauge via `Φ=A+λ(n⃗_i×n⃗_j)·ê_z` **amplifica** o sinal de
  1.17% de E6c em R̂=2, h=4. O acoplamento é realizado **exato** dentro do classificador E/B
  geométrico: o embedding 5D de E6c é aumentado com eixos internos `λ(n·e1,n·e2)`, cujo
  componente interno-interno do bivetor é `½λ²Σ(n×n)·ê_z` (a fórmula do prompt, verificado a
  1e-11) e que, sendo spacelike, alimenta o canal magnético; **λ=0 ⇒ E6c bit-a-bit**.
  **G0/G1 PASS** (λ=0 reproduz E6c, 0.01169, por-run <1e-12). **G2 FALHA decisivamente:**
  frac_B sobe com λ (até **0.27 em λ=2**) MAS pela **DESORDEM**, não pela ordem — em λ=2 o
  **desordenado (0.272) > J_c (0.205) > 2J_c (0.099)**: mais ordem = MENOS magnético; em λ
  pequeno (0.5) a ordem até SUPRIME abaixo da baseline (0.0088<0.0117). O `b²/e²` médio fica
  **<1** em todo λ/fase (≤0.986) — o diamante típico segue elétrico. **Veredito: [MORTO] —
  hipótese de amplificação FALSIFICADA.** Embora frac_B exceda 0.05, é **ruído spacelike** da
  textura incoerente (qualquer campo interno aleatório infla b²=Σ(Ã^{ij})²), que a ordenação
  REMOVE — o análogo Meissner (condensado coerente amplifica) NÃO se realiza. O ferromagneto
  **não adiciona** ao setor magnético; a **curvatura (E6c) é a única rota viva** para O(1).
  E6 mantém [FRONTEIRA TÉCNICA].
- **E6e (jun/2026)** — extrapolação **analítica** dos dados de E6c (`results/gauge/e6e/`,
  `E6e_synthesis.md`; sem Monte Carlo novo). Ajusta 3 modelos (potência, exponencial,
  quadrático em 1/R̂²) aos **5 pontos finitos** de E6c (h=4, N=2000). **Bem condicionado**
  (σ_rel ≤ 17%, longe do flag de 50%) — a preocupação do charter ("só 1 ponto positivo") era
  desatualizada. **Melhor ajuste: o EXCESSO de curvatura Δfrac_B = frac_B − piso ∝ (1/R̂)^1.73,
  R²=0.997** ≈ **H²** (a quadrática pura dá R²=0.984) — a fração magnética que a curvatura
  ADICIONA escala como a curvatura ao quadrado. **Extrapolação:** O(10%) exige **R̂≈0.5–0.6**
  (faixa 0.13–0.75), O(50%) R̂≈0.2–0.3, O(5%) R̂≈0.8–0.9 — **todos R̂<1**, raio de curvatura
  abaixo do espaçamento ℓ (≡ ℓ_Planck, **[EXTERNO/ASSUMIDO]**). O modelo **exponencial**
  (R²≈0.99) **SATURA em ~3%** → sob essa leitura O(10%) é inalcançável em QUALQUER curvatura
  (fronteira ainda mais forte). O b²/e² médio chega a 1 (célula média no cone) em R̂≈1.9–2.2
  (≈ o R̂=2 já medido), mas frac_B lá é só ~1.2% (distribuição estreita). **Veredito: [FRONTEIRA
  FÍSICA]** — não a morte dura (R̂≪0.1), mas o setor magnético O(1) via este mecanismo exige
  **curvatura Planckiana**; o universo observável (R̂ astronômico) tem frac_B≈0 (só o piso
  flat), logo **o mecanismo BD-gauge de curvatura NÃO explica os fótons do universo observável,
  de baixa curvatura**. **Recomendação honesta:** E6e completo (MC com R̂<2) **não vale a pena**
  como busca de fóton (a extrapolação já responde: Planckiano); um run confirmatório pequeno em
  R̂=1.5,1.0 só verificaria a lei ∝1/R̂² dentro do contínuo válido, não traria o fóton para
  perto. O problema vivo volta a ser: **2-célula spacelike com fração O(1) em BAIXA curvatura**
  — altura (E6b), curvatura isotrópica (E6c→Planck, E6e), e acoplamento (E6d) esgotados; resta
  geometria anisotrópica/inomogênea ou uma 2-célula genuinamente diferente.
- **E7** — fase de Coulomb vs confinamento no setor U(1) (pré-requisito de E6):
  **[FRONTEIRA] / INCONCLUSIVO (com lean)**. Reusou o motor de E5 (gates G1/G2
  re-passados: gauge-inv 3.3e-15 nos diamantes, β_c=1.00). A medição de Wilson loops
  acha um **crossover confina→Coulomb perto de β≈1** que **espelha a rede 4D** (o
  log-slope de loops grandes cruza da banda confinante para a de Coulomb em β≈0.85,
  rastreando os âncoras de rede em β casado) → **"confinamento em todo β" é
  DESFAVORECIDO**. Mas o **Coulomb não é certificado**: o discriminador limpo (razão de
  Creutz em retângulos R×T) **é inconstruível no causet não-local** (sem estrutura
  retangular de loop), e o surrogate de patch **falha o próprio controle Stage-A**
  (rotula o ponto de rede sabidamente-confinante como "perímetro"). σ_area nunca → 0
  (mín 0.056 em β=2.0). É a **mesma não-localidade de E5-1b (grau∝L^2.9) reaparecendo no
  observável de Wilson loop**. `results/gauge/e7/` (E7_synthesis.md).

**O que cruzaria a fronteira (ATUALIZADO por E6-3, jun/2026):** o **operador de gauge
BD-Lorentziano com assinatura indefinida** (split E²−B²) FOI construído e medido — e o
resultado **re-localiza a fronteira**. A assinatura indefinida NÃO era o obstáculo final:
o operador é gauge-invariante por construção, reproduz ω=ck numa rede 4D, mas falha no
causet porque **os diamantes causais height-2 só fornecem 2-células ELÉTRICAS (timelike);
não há nenhuma célula MAGNÉTICA (spacelike) para o termo B²**. A peça que falta agora não
é a assinatura nem um peso BD diferente (norm/sharp/raw falham idênticos), mas uma
**construção de 2-célula spacelike Lorentz-invariante** no causet — definir uma plaqueta
cujo bivetor de área seja tipo-espaço sem um referencial preferido para chamar eventos de
"simultâneos". Esse é o novo problema em aberto preciso. (E7 já dizia que o setor U(1) não
está permanentemente confinado e espelha a rede 4D — consistente com "a física do fóton
existe, falta a estrutura geométrica certa"; E6-3 nomeia qual estrutura.)

**Precedente na literatura de CST:** **busca FEITA (E6-3, jun/2026, `E6_literature.md`).**
Confirmado: **todos** os operadores BD / Dowker–Glaser (Benincasa–Dowker 2010;
Dowker–Glaser 2013, arXiv:1305.2588, que generaliza para d=2..7) são **só escalares** —
nenhum operador BD para campo vetorial / 1-forma / gauge existe. Sverdlov (0807.2066) e
Sverdlov–Bombelli (0905.1506) constroem a **ação** de gauge via holonomias em diamantes,
mas não um operador suavizado nem dispersão Lorentziana. Logo o operador BD-gauge indefinido
de E6-3 É novidade research-grade, sem precedente nem teorema — sua correção foi gateada
contra Maxwell livre numa rede 4D (STAGE-0 PASS) antes de qualquer leitura no causet.

**Dificuldade estimada:** **ALTA** — pesquisa de fronteira genuína. **Resultado de E6-3
(jun/2026): parcial, como previsto** (H1 factível, H2 difícil) — e mais informativo que
um simples "H2 falha": isolou que o obstáculo não é a assinatura (resolvida) mas a
**ausência de 2-células spacelike** nos diamantes causais. Próxima fronteira nomeada.

---

## Seção 3 — Matéria Topológica

### 3.1 SU(2) Skyrmion
| Item | Status | Nota |
|---|---|---|
| B=1, estável, gravita | **[SÓLIDO]** | com Skyrme externo declarado |
| spin-½, estatística fermiônica | **[SÓLIDO]** | E_J∝J(J+1); 2π→−1 (5e-16); troca=rot2π∈ℤ₂; ε(n)=(n−1)mod2 (n=1,2,3) |
| Skyrmion ↔ bárion | **[IDENTIFICADO]→[DERIVADO] (estrutura adimensional, BQ #12)** | quantização coletiva quantitativa reproduz ANW: multipletos `[4,16,36]`, μ_p/μ_n=−1.515 (exp −1.46), e=5.39 (1% de ANW) parameter-free; só a escala GeV (f_π) fica EXTERNA |
| Skyrme domina sozinho | **[MORTO]/[EXTERNO-T]** | K≤⅔S identidade pontual; 10⁶ config. adversariais |
| Regge do bárion | **[MORTO]** | rotor de Casimir m²∝J(J+1), R²=1.0 |

**Promover [IDENTIFICADO]→[DERIVADO] — FEITO para a estrutura adimensional (BQ #12,
jun/2026).** A quantização coletiva *quantitativa* (não só a lei j(j+1) de Q1–7) reproduz
a fenomenologia bariônica de Adkins–Nappi–Witten: a torre FR dá os multipletos
`(2j+1)²=[4,16,36]` (N, Δ, j=5/2) com spin=isospin e a razão pura `8/3` (1%); a **inércia
completa σ+Skyrme** (Q2 usava só-σ; o termo de Skyrme é 43%, 𝓘_full=1.76× Q2); **uma**
calibração (o split N–Δ) fixa o acoplamento `e=5.39` (1% de ANW 5.45) e então `μ_p/μ_n=
−1.515` (ANW −1.43, exp −1.46), raio isoscalar 0.65 fm e `g_A=0.56` são **previsões
parameter-free**. O que continua **[EXTERNO-B]** é apenas a **escala física GeV** (`f_π`,
mesma razão de G/ℏ; a rede→SI não é vinculada) e as **correntes EM** são importadas
(status da fase FR de Q4). Charter+dados: `BARYON_QUANTITATIVE.md`;
`results/matter/baryon_quant/` (`BQ5_synthesis.json`).

**Por que Casimir e não Regge — resolvido, não é fronteira:** o bárion é um **rotor
rígido** (quantização coletiva de Adkins–Nappi–Witten → Casimir m²∝J(J+1)); a
**trajetória de Regge linear** pertence ao **tubo de fluxo confinante** (corda,
α'=1/(2πσ)), que **existe** no setor SU(3) (FL1-D3). Logo são **duas torres
distintas**, ambas presentes: é uma propriedade estrutural da topologia do Skyrmion
(rotor), não uma limitação. O charter C3 (que pré-registrava Regge para o bárion)
foi respondido com o negativo correto.

### 3.2 SU(3) — forte vs fraco (FL1)
| Item | Status | Nota |
|---|---|---|
| Ferromagneto de cor + ordem espontânea | **[SÓLIDO]** | J_c≈0.3 (causal); C_long=m² |
| Confinamento V(r)~σr | **[SÓLIDO] mas medido uma vez** | σ>0, σ(β) decrescente (liberdade assintótica) |
| Octeto de mésons (8 Goldstones gapless) | **[SÓLIDO]** | 8/8 modos robustos a ±10% (FLR); fecha lacuna do píon |
| Regge do tubo de fluxo | **[FRACO]** | α'=1/(2πσ): forma robusta, valor cavalga no coupling efetivo (FLR) |
| **Teste de robustez (variar ação ~10%)** | **[SÓLIDO] — EXECUTADO (FLR)** | confinamento+octeto+Skyrmion sobrevivem |

> **Brecha mais urgente do programa de matéria — FECHADA (FLR, jun/2026).** A campanha
> de robustez (charter `FLR_SU3_ROBUSTNESS.md`, dados `FLR_robustness.json`) deformou a
> ação mínima em ±10% (`g_ε(p)=(1−p)+ε(1−p)²`) e mediu: confinamento (Creutz σ(2,2)>0
> em todo ε, 0.94–1.65), octeto (8/8 modos gapless em todo ε), Skyrmion (mínimo de
> Derrick interior em todo ε; tamanho λ* invariante). **Veredito: SU(3) ROBUSTO** — os
> resultados qualitativos não são artefato da forma exata da ação. Nota de honestidade:
> um 1º passo deu FRÁGIL por **bug de operacionalização** (flag "V(r) cresce" falha
> quando o confinamento é mais FORTE, esgotando os loops resolvíveis); corrigido para o
> estimador de Creutz (o que a própria FLC designou robusto), documentado em
> `FLR_synthesis.md`. **Resíduos não fechados:** ordem de transição (L≤12) e o valor de
> α' (cavalga no coupling — caveat de escala externa usual).

### 3.3 Ligação matéria→gravidade (Seção VII) — [SÓLIDO] (forma), FECHADA (MG1)
A inferência "o Skyrmion tem massa M → gera M/r" era **[FRACO]** (composição de duas
leis medidas; o perfil próprio nunca usado como fonte literal). **FECHADA em MG1
(jun/2026):** o perfil de densidade de energia REAL do sóliton ε(r) foi usado como
fonte literal no relaxador BD (charter `MG1_MATTER_SOURCES_GRAVITY.md`, dados
`results/matter/mg/`). Resultado: expoente exterior **−0.992** (1/r limpo, não
corrompido pela concentração do perfil), amplitude **linear na massa própria**
(G_net=A/M=0.9307 constante a 5 dígitos sobre M=175→218), e **mesmo G_net** de uma
fonte top-hat de igual massa (0.0% diff). Gate G0: o solver exato reproduz D3.
**Status: [SÓLIDO] para a forma** (θ=G_net·M/r, amplitude=massa própria); G_net
**absoluto permanece [EXTERNO]** (∝1/K). Caveat honesto (em `MG1_synthesis.md`): a
exatidão de A∝M é em parte lei de Gauss (exterior depende só da carga total) — MG1
confirma que isso vale também para o sóliton E que o expoente não corrompe; um teste
independente maior (Skyrmion 3D na sprinkling causal → relaxador BD 3D) fica como
passo opcional, a redução radial é exata para o hedgehog embutido.

---

## Seção 4 — Fenomenologia MOND e DEV

### 4.1 ν_MOND via susceptibilidade de Goldstone (FM2-1) — [FRACO]
(a) Expoente medido **−0.4±0.1** vs teórico **−0.5** (anomalia de coexistência de
Goldstone, Brezin–Wallace χ∥~h^(−1/2)). Efeitos de tamanho finito empurram o expoente
**para zero** — ressalva real. **[FRACO]**.
(b) O argumento "χ∥~h^(−1/2) dá ν_MOND" é mais **identificação** que derivação: a
forma da função de interpolação ν emerge da susceptibilidade longitudinal, mas a
**identificação χ∥ ↔ ν** é feita no nível da função de interpolação, não derivada
elemento a elemento. Honestamente: forma derivada, calibração e amplitude externas.
É, ainda assim, o positivo que **liga Paper I (MOND) a E1 (ferromagneto)** e é a
ponte microscópica com Khoury.

### 4.2 a₀ externo — [EXTERNO-B], com um teste de Khoury ainda em aberto
(a) 4+ tentativas falhadas (C3: X₀∝ρ é UV, não a₀; CR3: π/ln2 é nº puro, escala
externa) → **[EXTERNO-B] confirmado**.
(b) **O caminho de Khoury (C1) FOI testado (R3/C1, jun/2026).** Veredito: **EQUIVALÊNCIA
DE LIMITE (parcial).** A equivalência TEIC↔Khoury vive no **setor de resposta
LONGITUDINAL** (anomalia χ∥~h^{−0.37}, deep-MOND), **NÃO** na ação de árvore do fônon
transverso — o magnon (E2, ω=ck) é **quadrático (∝X)**, não o X^{3/2} de Khoury (medido:
χ⊥~h^{−0.98} via Ward vs χ∥~h^{−0.37}, expoentes distintos). Mata a afirmação solta
"magnon = fônon de Khoury"; confirma e SHARPENA a Fase 2. Charter `C1_KHOURY_EQUIVALENCE.md`;
dados `results/convergence/c1/`.
(c) **Implicação confirmada:** o coeficiente deep-MOND (rigidez ρ_s) cavalga em J/K
(ρ_s: 0.25→1.16) → "forma equivalente, escala externa". Como DEV≡Khoury no deep-MOND, o
**a₀ de Khoury é externo pela mesma estrutura de Milgrom** — [EXTERNO-B] reforçado, não
enfraquecido.

### 4.3 Matéria escura fria (FM4) — [FRACO]
(a) **Mecanismo de misalignment: [FRACO].** O resultado "m_A é CDM (w≈0, ρ∝a⁻³)" tem
três camadas de status distintas:
  - A **dispersão massiva** ω²=c²k²+m_A² foi **medida na rede** (FM4-V, gate PASS) —
    **[SÓLIDO]**.
  - A **equação de campo** φ̈+3Hφ̇+m_A²φ=0 **NÃO foi derivada da rede**: é a
    Klein–Gordon/Proca padrão em fundo FRW, **[POSTULADO]** (cosmologia importada,
    consistente com a rede, não emergente dela). O "freeze (H>m_A) → oscila → w=0" é
    física de áxion/ULDM padrão aplicada a um campo cuja massa é externa.
  - A massa m_A e a constante de decaimento f_A são **[EXTERNO-B]**.
(b) **f_A externo, quão externo:** f_A é a escala de decaimento tipo-GUT da janela
ULDM; **não há argumento na teoria de onde ela vem** — é coincidência com a janela
fenomenológica, não derivação. **[EXTERNO-B]**.
(c) **S8: [MORTO]** (4ª porta) — a fração que ajudaria σ8 super-suprime o Lyman-α.
Não há janela. A *peça fria* (m_A=CDM) vive; *resolver S8* morre.

> **Resumo Seção 4:** a fenomenologia MOND/DEV deriva **formas** (deep-MOND, ν,
> dispersão massiva) e tem matéria escura fria genuína (m_A), mas: o expoente ν está
> 1σ do teórico e ameaçado por tamanho finito; o misalignment é cosmologia importada;
> a₀ e f_A são externos; e S8 está morto em 4 portas. O elo C1 com Khoury, que daria
> origem microscópica ao a₀, nunca foi fechado.

---

## Seção 5 — O Fóton: mapa completo da fronteira

(a) **O que foi tentado:** E4 (orientação → escalares, MORTO), E5 (gauge U(1) Wilson
nu → obstruído por não-localidade), E6 (Maxwell não-compacta → estrutura SIM,
propagação NÃO), **E7 (fase de Coulomb vs confinamento → INCONCLUSIVO com lean: crossover
tipo-rede perto de β≈1, "confina sempre" desfavorecido, Coulomb não certificado porque o
discriminador limpo é inconstruível no causet não-local)**, **E6-3 (operador
BD-Lorentziano → CONSTRUÍDO e medido: gauge-inv por construção, validado em rede 4D,
mas H2 falha no causet porque os diamantes são 100% elétricos)**, **E6b (varredura de
ALTURA → a height não ajuda, cauda ~0.25% decrescente)**, **E6c (varredura de CURVATURA →
a curvatura AJUDA monotonicamente; frac_B cruza 0.01 em curvatura trans-Planckiana; SUCESSO
marginal — a 2-célula spacelike existe e cresce com curvatura)**, **E6d (acoplamento
ferromagneto↔gauge no substrato curvo → MORTO: não amplifica; a subida de frac_B é ruído
spacelike da desordem (G2 falha) e a ordem SUPRIME — análogo Meissner não se realiza)**. O
operador BD-Lorentziano deixou de ser hipótese — é resultado; a fronteira do fóton está agora
**em movimento, não parada** (a curvatura é o primeiro ingrediente que eleva o setor
magnético; o acoplamento de ordem foi testado e descartado), **E6e (extrapolação analítica
→ frac_B∝H²; O(10%) exige R̂≈0.5–0.6 sub-Planckiano → [FRONTEIRA FÍSICA]: curvatura funciona
só na escala de Planck, não explica os fótons do universo observável)**.

(b) **A obstrução de princípio:** a ação ½ΣF_P² no link é **Euclidiana
(positiva-definida)**, com mínimo em ω≈0 — ela mede uma "energia" não-negativa, não
uma propagação. O fóton Lorentziano precisa de uma ação de **assinatura indefinida**
(E²−B²), onde os modos elétrico e magnético entram com sinais opostos, dando o cone de
luz ω=ck. A ação nua não tem essa estrutura.

(c) **O que seria necessário — REVISADO por E6-3 (jun/2026):** o operador de gauge BD com
assinatura indefinida foi construído (split E²−B² por bivetor de área das plaquetas) e
**(i) é gauge-invariante** (5.7e-16 — a assinatura indefinida não quebra isso, pois
F=dθ ⇒ BG=0=d²) **e (ii) converge para Maxwell numa rede 4D** (zero crossing em ω=ck,
c=1.05). O que **falta** não é mais a assinatura: é o **análogo causal do Hodge star / da
2-célula MAGNÉTICA**. Os diamantes height-2 fornecem só 2-células elétricas (timelike);
o termo B² (spacelike) está estruturalmente ausente (fração B-type=0.0000). A construção
em aberto agora é precisa: **uma 2-célula spacelike Lorentz-invariante no causet**.
**Refinado por E6b (jun/2026, `results/gauge/e6b/`):** a varredura de altura (2h-gons,
h=2..6, N≤2000) mostra que o zero exato é **só de height-2**; em h≥3 surge uma **cauda
~0.25% não-crescente** de células B-type (b²/e² por célula caindo com h), nunca chegando
ao limiar 0.01 → setor magnético de **medida-zero**, não O(1). A rota "diamante mais alto"
para a 2-célula spacelike está **descartada**; a construção viável precisa de fração
magnética O(1), que um diamante maior não entrega.
**Avançado por E6c (jun/2026, `results/gauge/e6c/`):** a varredura de **curvatura** (de
Sitter, R̂=∞→2; ordem conforme-plana = ensemble E6b idêntico em toda curvatura; split E/B no
embedding 5D do hiperbolóide) mostra que a **curvatura SIM entrega** o setor magnético, ao
contrário da altura: frac_B sobe **monotonicamente** e o b²/e² por célula sobe **8.6×**
(0.11→0.97), **cruzando 0.01** em R̂=2 (R_dS≈1.68ℓ, trans-Planckiano; h=4, frac_B=0.0117,
Wilson-lo 0.0105, 28k plaquetas, N-estável) → **SUCESSO pré-registrado (marginal,
curvatura-extrema)**. A 2-célula spacelike **existe e cresce com curvatura** — não é de
medida-zero sob curvatura. O que falta é uma fração magnética **O(1)** (b²/e²>1 típico): sob
curvatura extrema o diamante médio fica na **borda do cone** (E²≈B², b²/e²=0.97<1), com só
~1.2% das células tombando para spacelike. **h=2 é imune** (0.0000 em toda curvatura). DEATH
não disparou; E6 mantém [FRONTEIRA TÉCNICA], revisado **upward** (obstrução curvatura-removível).
**Rota de acoplamento FECHADA por E6d (jun/2026, `results/gauge/e6d/`):** acoplar o
ferromagneto ordenado (E1) ao gauge via `Φ=A+λ(n×n)·ê_z` no substrato curvo de E6c **NÃO
amplifica** o sinal. G0/G1 PASS (λ=0 ⇒ E6c bit-a-bit), mas **G2 FALHA**: frac_B sobe com λ
(até 0.27) pela **DESORDEM** da textura (ruído spacelike infla b²), não pela ordem — e a
**ordem SUPRIME** (λ=2: desord. 0.272 > J_c 0.205 > 2J_c 0.099). Análogo Meissner não se
realiza → **[MORTO]** (hipótese de amplificação falsificada). Logo a fração magnética **O(1)**
só pode vir da **curvatura** (E6c), não do acoplamento de ordem; o próximo passo viável fica
no lado geométrico (curvatura mais forte/anisotrópica), não no ferromagneto.
**Quantificado por E6e (jun/2026, `results/gauge/e6e/`, analítico):** ajustando os 5 pontos de
E6c (bem condicionado), o excesso Δfrac_B ∝ (1/R̂)^1.73 ≈ **H²** (R²=0.997). Extrapolando:
O(10%) exige **R̂≈0.5–0.6**, O(50%) R̂≈0.2–0.3 — **todos R̂<1** (raio de curvatura < ℓ ≡
ℓ_Planck, **[ASSUMIDO]**); o modelo exponencial sequer alcança O(10%) (satura ~3%). Logo o
setor magnético O(1) via curvatura existe mas **só na escala de Planck** → **[FRONTEIRA
FÍSICA]**: o universo observável (R̂ enorme) tem frac_B≈0, e este mecanismo **não explica os
fótons observados**. A rota "curvatura isotrópica mais forte" está assim **fechada como
explicação física** (funciona, mas Planckiana); o que resta verdadeiramente aberto é uma
2-célula spacelike com fração O(1) em **baixa** curvatura — geometria anisotrópica/inomogênea
ou uma definição de 2-célula genuinamente nova (nenhuma testada ainda).

(d) **Precedente em CST:** **busca FEITA em E7 (jun/2026, `E7_literature.md`).**
Sverdlov "Gauge Fields in Causal Set Theory" (0807.2066, 2008) e Sverdlov–Bombelli
"Dynamics for causal sets with matter fields" (0905.1506, 2009) constroem campos de
gauge U(1)/Yang–Mills em causets via **holonomias em diamantes causais** — uma
construção de **ação/Lagrangeana**, o ancestral conceitual exato do que E5/E7 mediram.
Mas **a medição Monte-Carlo da fase confinamento/Coulomb dessa ação num causet
esparramado NÃO está na literatura** → a medição de E7 é ela própria um pequeno passo
original. Confirma o charter: não há operador de gauge BD padrão.

(d') **E7 (jun/2026) — a fase, parcialmente:** mediu Wilson loops no setor U(1) e achou
um **crossover confina→Coulomb perto de β≈1 espelhando a rede 4D** (desfavorece
"confinamento permanente"), mas **não certifica a fase de Coulomb**: a razão de Creutz
(único discriminador limpo, validado na rede com separação 8×) **não pode ser construída
no causet não-local** (sem retângulos R×T controlados), e o surrogate de patch falha o
controle Stage-A. **[FRONTEIRA] / inconclusivo-estrutural.** Não promove a
[FRONTEIRA-ESTRUTURAL] (confinamento não demonstrado — de fato desfavorecido) nem a
[SÓLIDO-PARCIAL] (Coulomb não certificado). Implicação: E6 **mantém** motivação (lean
favorável, não contradito), e o próximo passo para fechar a fase É o operador BD-suavizado
de E6, não um E7 maior.

(e) **Dificuldade estimada:** **ALTA / problema em aberto** — research-grade. **E6-3
(jun/2026) avançou a fronteira sem cruzá-la:** o operador BD-Lorentziano existe, é
gauge-invariante e funciona numa rede 4D; o obstáculo restante foi re-localizado de
"assinatura Euclidiana" (E6-2) para "ausência de 2-célula magnética/spacelike na ordem
causal" — uma afirmação concreta e original (a literatura CST não tem operador BD de gauge
nem mediu isto). É o **resultado potencialmente mais publicável** do programa se a 2-célula
spacelike for construível. Melhor afirmação publicável **hoje** permanece E4 (ordem
orientacional + Goldstone escalar relativístico; fóton localizado estruturalmente,
não-propagante).

---

## Seção 6 — O que nunca foi tentado (lista completa)

Ordenada com urgência e dificuldade re-avaliadas nesta varredura.

| # | Lacuna | Urgência | Dificuldade | Pré-requisitos |
|---|---|---|---|---|
| 1 | ~~**Robustez de FL1** (variar ação ~10%)~~ ✅ **EXECUTADO** (FLR) — SU(3) robusto | — | — | resolvido jun/2026 |
| 2 | ~~**Skyrmion como fonte direta de gravidade**~~ ✅ **EXECUTADO** (MG1) — forma [SÓLIDO] | — | — | resolvido jun/2026 |
| 3 | ~~**C1 — Khoury formal**~~ ✅ **EXECUTADO** (C1) — equivalência de limite (setor longitudinal) | — | — | resolvido jun/2026 |
| 4 | ~~**Operador BD-gauge Lorentziano** (o fóton real)~~ ✅ **EXECUTADO (E6-3, jun/2026)**: operador indefinido E²−B² construído, gauge-inv 5.7e-16, validado em rede 4D (ω=ck). H2 FALHA no causet — diamantes 100% elétricos (B-type=0.0000), setor magnético vazio. **[FRONTEIRA TÉCNICA]**, fronteira re-localizada → **falta 2-célula spacelike** | — | — | `results/gauge/e6/E6_3_*` |
| 4b | **2-célula spacelike Lorentz-invariante no causet** (o que falta para o fóton, isolado por E6-3) — **rota "diamante mais alto" descartada (E6b)**; **rota "curvatura" PARCIALMENTE BEM-SUCEDIDA (E6c)**: curvatura de Sitter eleva frac_B monotonicamente (b²/e²/célula 0.11→0.97), CRUZA 0.01 em R̂=2 (Wilson-lo 0.0105) — 2-célula spacelike **existe e cresce**, mas marginal/extrema, ainda não O(1); **rota "acoplamento ferromagneto" MORTA (E6d, jun/2026)**: λ(n×n)·ê_z no substrato curvo NÃO amplifica (G2 falha — subida é ruído spacelike da desordem; ordem SUPRIME); **rota "curvatura mais forte" quantificada e [FRONTEIRA FÍSICA] (E6e, jun/2026)**: frac_B∝H², O(10%) exige R̂≈0.5–0.6 sub-Planckiano (R̂<1) → funciona só na escala de Planck, não no universo observável | ALTA | ALTA | obter fração magnética **O(1)** em **BAIXA** curvatura — geometria **anisotrópica/inomogênea** ou 2-célula genuinamente nova (altura, curvatura isotrópica e acoplamento todos esgotados); `results/gauge/e6c/`, `results/gauge/e6e/` |
| 5 | ~~**Seleção de grupo via teorema** (por que SU(3), não SU(4))~~ ✅ **EXECUTADO (R5, jun/2026)**: SU(3)=menor grupo simples com fundamental COMPLEXA / d^abc≠0 (seleção por minimalidade); topologia (π₃ Bott) NÃO distingue 3 de 4; requisito "complexa" importado (como d=3). Veredito B. | — | — | `results/foundations/r5_group/` |
| 6 | **DEV←TEIC completo** (a₀, β, A_μ, slip η em unidades físicas) | ALTA | ALTA | 4 tentativas já falharam p/ a₀/G/ℏ |
| 7 | ~~**Λ dinâmica** (evolução temporal; elo aberto de LAMBDA_EVERPRESENT)~~ ✅ **EXECUTADO (LD, jun/2026)**: Λ_rms~1/√V₄ (coef. L1 medido) rastreia ρ_crit (p=1.107, R²=0.996); finita em z=0; Ω_Λ~O(1) por ~7 e-folds (vs ~1 no ΛCDM) → coincidência dissolvida; caveat: w_eff(envelope)≈−0.66 (assinatura testável). Veredito CONSISTENTE. | — | — | `results/cosmology/lambda_dyn/` |
| 8 | ~~**C5 — dimensão espectral D_s(σ)**~~ ✅ **JÁ EXECUTADO** (morte: sem corrida; D_s=MM) — **erro do mapa, corrigido** | — | — | `results/foundations/c5/` |
| 9 | ~~**C6 — vórtices quantizados**~~ ✅ **JÁ EXECUTADO** (veredito B; circulação física no setor m_A) — **erro do mapa, corrigido** | — | — | `results/cosmology/c6/` |
| 10 | ~~**Busca direta da linha KR nos dados PTA** (NANOGrav existentes)~~ ✅ **EXECUTADO (KR-PTA, jun/2026)**: confronto com buscas diretas publicadas (PPTA-2018 ρ<6 GeV/cm³ ⇒ f_max≈15 em 1e-23 eV; NANOGrav-15yr) — linha m_A **NÃO excluída** em parte alguma da janela (f_max=2.5→2160); abaixo do limiar; Lyman-α força m_A subdominante na banda. Veredito CONSISTENT. | — | — | `results/cosmology/kr_pta/` |
| 11 | ~~**Espectroscopia quantitativa do octeto** (FL1-D)~~ ✅ **EXECUTADO (OS, jun/2026)**: octeto **exatamente degenerado** (spread 4e-8 cubic/causal — os 8 geradores desacoplam em formas Laplacianas idênticas (J/3)); ρ_s(por link)≈1/3, c=√(2/3)=0.8165, dispersão linear isotrópica gapless; **spread ~10% da D2 = costura de toro do λ8** (autovalores Cartan irracionais, \|exp−I\|=1.94; fix BC-aberta colapsa p/ 9e-6). | — | — | `OCTET_SPECTROSCOPY.md`; `results/matter/fl1/OS_*` |
| 12 | ~~**Quantização de coordenadas coletivas do bárion** (quantitativa)~~ ✅ **EXECUTADO (BQ, jun/2026)**: torre FR dá multipletos `(2j+1)²=[4,16,36]` (N,Δ,j=5/2), spin=isospin, razão pura `8/3` a 1%; **inércia completa σ+Skyrme** (Q2 era só-σ; Skyrme = 43%, 𝓘_full=1.76× Q2); **1 calibração** (split N–Δ) → `e=5.39` (ANW 5.45, 1%); previsões parameter-free `μ_p/μ_n=−1.515` (exp −1.46), raio isoscalar 0.65 fm, `g_A=0.56`. Veredito A. | — | — | `BARYON_QUANTITATIVE.md`; `results/matter/baryon_quant/` |
| 13 | **Inércia como princípio isolado** — **PENDENTE, NUNCA TENTADA** (auditoria jun/2026). Três coisas distintas têm "inertia" no nome e **não devem ser confundidas**: (a) `results/matter/M1_inertia` + `M2_lorentz_mass` — inércia operacional `m=F/a` do **escalar livre sem massa**, **[MORTO]** (Verdict C); (b) `su2_quant/Q2_inertia` + `baryon_quant/BQ2_inertia` — **momento de inércia do Skyrmion** para quantização coletiva, **EXECUTADAS** (Verdict A); (c) **este item 13** — inércia como **princípio isolado** (o lado inercial da dinâmica modificada, massa inercial vs gravitacional), **nunca tentada**. O bloqueio **não é prioridade**, é **falta de observável**: não há formulação não-trivial de "o lado inercial" isolado da modificação de dinâmica. **Antes de qualquer código, o passo necessário é uma sessão de DEFINIÇÃO do observável** — é uma pendência conceitual, não uma execução pendente. | BAIXA | MÉDIA | **definir o observável (não-trivial) — pré-requisito conceitual, não código** |
| 14 | ~~**FM5 — regras de crescimento alternativas a e7**~~ ✅ **EXECUTADO** (jun/2026): morte do e7 generaliza à FORMA da regra (graduada por componentes); nenhuma dá d→4 manifold-like. Acoplamento já fora varrido em T3A-3 | — | — | resíduo: família CSG completa (t_n) — **gatilho RS coberto, ver abaixo** |
| 14b | ~~**Gatilho Rideout–Sorkin: a coordenação do CSG diverge (como Poisson) ou satura?**~~ ✅ **EXECUTADO — CAMPANHA COMPLETA (RS-TRIGGER, `docs/campaigns/RIDEOUT_SORKIN_TRIGGER/`, jun/2026): GATILHO ARMADO.** ⟨z⟩(N) do grafo de Hasse do crescimento sequencial clássico (percolação transitiva, subfamília t_n=t^n) **satura** em O(1)–O(10) nos 4 regimes, enquanto o Poisson **diverge**. Estimador idêntico ao da XI (cross-check numérico diff 0). **Tabela ⟨z⟩(N)** (N=500→3888): Poisson 33.4→52.1→75.7→103.0 (×3.1, expoente +25→+51 **acelera**); sparse p=0.02 6.5→8.6 (×1.33); intermediate p=0.10 5.7→6.0 (×1.05); dense p=0.40 3.56→3.57 (×1.00, plano); manifold p=4/N 3.84→4.01 (×1.04). Todos os CSG têm expoente local `d⟨z⟩/dlnN`≤+0.26 e plano/decrescente. **Mecanismo:** *"o CSG não tem boosts; a não-localidade Lorentz-protegida que a ESCALA_XI isolou como motor da divergência de coordenação é uma propriedade do sprinkling sobre um background de Minkowski, não dos causal sets em geral."* **Reabre a "Saída 2" da XI** (o fechamento de §10 era prematuro). ARMADO ⇒ a campanha completa (ferromagneto+ξ sobre CSG) **se justifica** — decisão separada, **bloqueada por 2 pré-condições** (ver Gatilho 2). | — | — | **fechada**; sucessor pré-registrado: `docs/campaigns/RIDEOUT_SORKIN_CLUSTERING/` |
| 14c | ~~**Gatilho 2 (Rideout–Sorkin clustering): o grafo de cobertura do CSG é tipo-árvore ou tem laços?**~~ ✅ **EXECUTADO (2026-06-27, `docs/campaigns/RIDEOUT_SORKIN_CLUSTERING/`): GATILHO 2 NÃO ARMADO.** Gate de validação VERDE (ER≈p, K_n=1, árvore=0, toro 2D C4=0.125). **Achado primário = TEOREMA:** a transitividade (3-ciclos) do grafo de cobertura é **≡0 por construção** — o diagrama de Hasse de qualquer poset é **livre de triângulos** (3 nós mutuamente cobertos formariam cadeia a≺b≺c, mas então a≺c tem intermediário ⇒ não-cobertura). **Discriminador real = square-clustering C4 (4-ciclos, Lind, normalizado):** sparse 0.0056→0.0043, intermediate platô ~0.019, manifold 0.0029→0.0003. **Decisivo (controle):** o Poisson — provado mean-field na XI — tem C4 **MAIOR** (0.029–0.054, decaindo) que TODOS os regimes do CSG, e a rede dim-finita (toro) tem C4=0.125 (~6–30× acima do CSG). ⇒ grafo de cobertura do CSG é **mais tipo-árvore que o Poisson mean-field**. Pré-condições herdadas respeitadas (`dense` excluído; satura-vs-decai resolvido pelo controle). **Coordenação finita ≠ suficiente: a 2ª barreira fica de pé.** **Fronteira (Parte 1, ext. N→16000):** o intermediate é **platô genuíno C4≈0.019** (expoente local→0, não decaimento) ⇒ veredito qualificado = **morte 2/3 (sparse, manifold) + FRONTEIRA 1/3 (intermediate)**, análogo ao k-NN da XI; mas o platô é **sub-MF** (abaixo do Poisson 0.029), então **"CSG ENCERRADA" se mantém** (campanha completa de ξ não roda), citado com a ressalva-fronteira. | — | — | **fechada** (fronteira 1/3); sucessor EXECUTADO: `docs/campaigns/CDT_VIABILIDADE/` (Gatilho 3, 14d) |
| 14d | ~~**Gatilho 3 (viabilidade tipo-CDT): aresta fixa + colagem livre Pachner escapa das 2 barreiras?**~~ ✅ **EXECUTADO (2026-06-27, `docs/campaigns/CDT_VIABILIDADE/`): GATILHO 3 ARMADO (com ressalvas).** Gate VERDE (seed=K4 z=3/C_tri=1/C4=1; manifold V−E+F=2; rede triangular transitividade=0.400). 1-esqueleto de triangulação 2D evoluída por Pachner ((1,3)+(2,2) flips), **sem ação**. Regime flipped/DT: ⟨z⟩→6, **transitividade≈0.30 e C4≈0.145 saturantes** (~5× piso MF Poisson, ordem rede 2D) ⇒ **primeiro substrato da fila a passar a barreira de laços**. **Ressalvas (limitam o peso):** (1) ⟨z⟩→6 é **identidade de Euler** em 2D (bate 6−12/V à 4ª casa) — barreira de coordenação **trivial, passada por construção, não conquistada**; (2) Pachner sem peso de ação ⇒ possível patologia **branched-polymer** na geometria global (teste mede laços **locais**, sadios; não dimensão de Hausdorff). ⇒ ARMADO cinemático **necessário, não suficiente**. Anti-circ respeitado (aresta `[External]`, nada "escala emergiu"). | — | — | **fechada (cinemática)**; sucessor PENDENTE não-iniciado: CDT-COMPLETA (tipo-CDT + ação Regge + Wick + ξ) |
| 15 | ~~**SU(3) ordem de transição em L>12**~~ ✅ **EXECUTADO 2×**: FLB2 (L≤16, 1ª ordem desfavorecida) **+ OT (L≤24, jun/2026)** que REVERTE parcialmente → **1ª ordem FRACA provável** (χ_max lei-de-volume x≈3.6, Binder dip aprofunda, histerese; calor latente ainda não-resolvido). H0 2ª-ordem desfavorecida. Resíduo: L≳32 multicanônico p/ forte-vs-fraca-vs-contínua | — | — | `docs/campaigns/SU3_ORDEM_TRANSICAO/`, `FLB2_transition_order.*` |
| 16 | **Léptons como objetos próprios** | BAIXA | MUITO ALTA | sem ponto de entrada claro |
| 17 | **C4 — SU(2)×U(1) e 3 gerações** | BAIXA | MUITO ALTA (anos) | motor novo; VS4/VS5 negativos |

---

## Seção 7 — Postulado vs genuinamente derivado (a tabela mais importante)

Versão expandida e honesta da Tabela Canônica de Status, incluindo o que é
**postulado disfarçado de derivado**.

| Ingrediente | Status real | Se POSTULADO: o que derivaria? / Se EXTERNO: T ou B? |
|---|---|---|
| **Tempo próprio = contagem (γ, Schwarzschild)** | **DERIVADO** | — (medido, R1/R3; = CST) |
| **Ação O(3)/sigma da Eq.(1)** (`Σ Δτ[1−cos∠]`) | **POSTULADO** (mínimo-justificado) | É o modelo sigma **mínimo** invariante por rotação — argumentado como mínimo, **não derivado unicamente**. Derivá-lo exigiria mostrar que a coarse-graining de Poisson **força** essa forma e nenhuma outra. NUNCA provado. |
| **Δτ_ij como peso do link** | **DERIVADO** | é o tempo próprio do link, peso natural da estrutura causal (não inserido à mão) |
| **Ação BD para propagação** | **EXTERNO-escolhido** (=CST padrão) | é o d'Alembertiano de Sorkin–BD, **escolhido** porque reproduz o contínuo conhecido (e10); **não derivado de forma única** da rede. Reproduz resultado conhecido. |
| **Quadraticidade da ação gravitacional** | **POSTULADO** | dá 1/r trivialmente; derivar a quadraticidade da estatística de Poisson é a brecha aberta de §1.3 |
| **Operador de Skyrme (forma λ_Sk=a/√120)** | **DERIVADO** (forma) | medido 5/9 a 0.06%, grade cega — emerge da isotropia de Poisson |
| **Dominância de Skyrme (estabilização)** | **EXTERNO-T** | provado necessário: K≤⅔S (Cauchy–Schwarz, 10⁶ config.) — não é busca falhada |
| **Razões de Stückelberg (1,2)** | **DERIVADO** | algébricas e travadas (C1–C2, W4); a DEV as trata como livres |
| **Pesos K (rigidez), λ_p (gauge)** | **EXTERNO-B** | normalizações da ação; G_net∝1/K (D3D) |
| **G, ℏ, a₀, massas em SI** | **EXTERNO-B** | forma derivada, valor não (D3D, T3C/e11, C3, CR4); VS5 fechou o atalho aritmético |
| **Campo complexo Φ / magnitude de Higgs** | **EXTERNO-T** (parcial) | magnitude |Φ|=ρ **emerge** (PE3); enrolamento **irredutível** por teorema de Derrick (cos2π=1 cega ρ) |
| **Mecanismo de misalignment (m_A=CDM)** | **POSTULADO** | a dispersão massiva é medida (FM4-V); a evolução FRW φ̈+3Hφ̇+m²φ=0 é cosmologia importada, **consistente** com a rede, não **derivada** dela |
| **f_A (constante de decaimento)** | **EXTERNO-B** | escala tipo-GUT; sem argumento de origem |
| **d=3 (dimensão espacial)** | **POSTULADO/input** | input geométrico no shell measure r^(d-1); DS1–3 dá d=3 "por exclusão estrutural" mas como seleção, não emergência dinâmica (T3A/B mataram a emergência via e7) |
| **a₀(z)∝H(z)** | **IDENTIFICADO** | a relação de escala da ponte; testada (BTFR_V3 mede a direção certa) — o setor falsificável |

> **A leitura transversal (o padrão universal, e a verdade mais importante do
> programa):** *em todo setor, a forma é derivada, a escala absoluta é externa, o
> número puro adimensional é calculável.* Os itens **POSTULADO** acima são os que mais
> facilmente passam por "derivados" no discurso: a forma da ação O(3), a
> quadraticidade gravitacional, o misalignment, e d=3. Nenhum tem teorema de
> necessidade; todos são escolhas mínimas/padrão justificadas por economia, não por
> prova.

---

# FASE 3 — Roteiro de Pesquisa

Ordenado por: **(1) urgência para integridade** → **(2) razão impacto/esforço** →
**(3) sequência lógica** (não atacar fronteira avançada sem consolidar a base).

### R1 — Robustez de FL1 (variar ação ~10%) ✅ **EXECUTADO (FLR, jun/2026)**
- **Pergunta:** o confinamento V~σr, o octeto de mésons e o Skyrmion de SU(3)
  sobrevivem a uma perturbação de ~10% na ação?
- **Veredito: SU(3) ROBUSTO.** Deformação `g_ε(p)=(1−p)+ε(1−p)²`, ε∈[−0.2,+0.2]:
  confinamento (Creutz σ(2,2)>0 em todo ε), octeto (8/8 gapless em todo ε), Skyrmion
  (mínimo de Derrick interior em todo ε; λ* invariante). Gate G0 (ε=0 = motor
  original) PASS. Charter `FLR_SU3_ROBUSTNESS.md`; síntese `FLR_synthesis.md`; dados
  `FLR_robustness.json`. Correção de honestidade: 1º passo FRÁGIL por bug de
  operacionalização (V(r) não-resolvível ≠ deconfinamento), corrigido para o
  estimador de Creutz e documentado.
- **Resíduos abertos:** ordem de transição (L≤12); valor de α' (cavalga no coupling).
- **Dependências cumpridas.** Próximo do roteiro: **R2**.

### R2 — Skyrmion como fonte direta de gravidade ✅ **EXECUTADO (MG1, jun/2026)**
- **Veredito: MATÉRIA→GRAVIDADE DERIVADA (forma).** O perfil ε(r) real do sóliton,
  fonte literal no relaxador BD: expoente exterior −0.992, A linear na massa própria
  (G_net=0.9307 cte a 5 dígitos), = G_net top-hat (0.0% diff). Gate G0 reproduz D3.
  Sec. VII: [FRACO]/composição → **[SÓLIDO] (forma)**; G_net absoluto [EXTERNO].
  Charter `MG1_MATTER_SOURCES_GRAVITY.md`; síntese `results/matter/mg/MG1_synthesis.md`.
- **Resíduo (opcional):** versão Skyrmion-3D-na-sprinkling-causal → relaxador BD 3D
  (campanha maior; a redução radial usada é exata para o hedgehog embutido).
- **Próximo do roteiro: R3 (C1 — equivalência formal TEIC ≡ Khoury).**

### R3 — C1: equivalência formal TEIC ≡ Khoury ✅ **EXECUTADO (C1, jun/2026)**
- **Veredito: EQUIVALÊNCIA DE LIMITE (parcial).** A equivalência vive no setor de
  **resposta longitudinal** (anomalia deep-MOND χ∥~h^{−0.37}), **não** na ação de
  árvore do fônon transverso: o magnon (E2) é quadrático **∝X** (medido χ⊥~h^{−0.98}
  via Ward), não o X^{3/2} de Khoury. Expoentes distintos → setores distintos.
  **Mata** a afirmação solta "magnon = fônon de Khoury"; **confirma e sharpena** a
  Fase 2 (Milgrom). ρ_s cavalga em J (0.25→1.16) → "forma equivalente, escala externa";
  a₀ externo reforçado. Charter `C1_KHOURY_EQUIVALENCE.md`; síntese
  `results/convergence/c1/C1_synthesis.md`. Correção honesta: estimador χ⊥ de flutuação
  satura por tamanho finito; usado o de Ward (correto), documentado.
- **K3 (vórtices→circulação física) adiado para C6** (estava condicionado a um
  fechamento de árvore que não ocorreu).
- **Próximo do roteiro:** R4 (operador BD-gauge Lorentziano, o fóton) — fronteira ALTA
  dificuldade; ou itens baratos da Seção 6 (C5 dim. espectral, C6 vórtices, busca KR).

### R4 — Operador BD-gauge Lorentziano (o fóton) ✅ **EXECUTADO (E6-3, jun/2026)**
- **Pergunta:** uma ação de gauge SBD-suavizada com assinatura indefinida produz um
  fóton emergente (ω=ck, 2 polarizações transversas, fase de Coulomb)?
- **Veredito: FRONTEIRA TÉCNICA — H1 PASS, H2 FALHA, razão PRECISA.** O operador
  indefinido E²−B² (split E/B por bivetor de área das plaquetas-diamante) é
  **gauge-invariante por construção** (5.7e-16; a assinatura indefinida não quebra
  invariância pois F=dθ ⇒ d²=0) e **validado em rede 4D** (STAGE-0: zero crossing do
  símbolo segue ω=ck, c=1.05, dev 3%). **Mas H2 falha no causet:** os diamantes causais
  height-2 são **100% elétricos** (fração B-type = 0.0000 em 9 sprinklings, N≤626) —
  todo diamante carrega a extensão timelike ponta-passada→ponta-futura, `b²<e²` sempre.
  O **setor magnético é vazio**, λ∝−ω² nunca cruza zero. H3 NÃO alcançado (gateado atrás
  de H2, como pré-registrado). **A fronteira foi re-localizada**, não cruzada: o
  obstáculo não é a assinatura (resolvida) nem o peso BD (norm/sharp/raw idênticos), mas a
  **ausência de 2-células spacelike** na ordem causal (novo item 4b). Charter
  `E6_BD_GAUGE.md`; literatura `E6_literature.md`; dados/figura `results/gauge/e6/E6_3_*`.
- **Dificuldade:** ALTA (foi campanha dedicada; resultado parcial como previsto).
- **Dependências CUMPRIDAS (E7, jun/2026):** (i) **busca de literatura CST de gauge
  FEITA** (`E7_literature.md`: Sverdlov 0807.2066, Sverdlov–Bombelli 0905.1506 — ação
  existe, fase nunca medida); (ii) **pré-requisito de fase de E7 RESOLVIDO no que pôde
  ser:** o setor U(1) não está permanentemente confinado (crossover tipo-rede 4D perto de
  β≈1) → E6 **não é bloqueado por confinamento estrutural**, mantém motivação. Resíduo que
  E7 NÃO pôde fechar (área-vs-perímetro limpo) **é exatamente o que E6 resolve** (operador
  BD-suavizado dá os retângulos/observável que o causet nu não tem). Idealmente após R1–R3
  (base consolidada — todas cumpridas).
- **Resultado E6-3 (jun/2026):** executado; FRONTEIRA TÉCNICA. O obstáculo de E7
  (área-vs-perímetro) e o de E6-3 (sem termo B²) convergem na MESMA raiz geométrica: o
  2-complexo de diamantes causais não tem células spacelike. O próximo passo concreto
  para o fóton é o **item 4b** (construir essa célula), não um operador BD diferente.

### R5 — Seleção de grupo via teorema (por que SU(3), não SU(4)) ✅ **EXECUTADO (R5, jun/2026)**
- **Pergunta:** existe um critério (analítico, extrapolando Bott/Cartan + o que MIN1–3
  mediram) que force SU(3) como o grupo de cor, em vez de SU(N≥4)?
- **Veredito B — SELEÇÃO POR MINIMALIDADE (não unicidade; requisito importado).**
  SU(3) é o **menor grupo de Lie simples compacto com representação fundamental
  COMPLEXA** (3≠3̄) ≡ menor com invariante cúbico simétrico d^abc≠0 (os dois ligam na
  MESMA fronteira N=2|3; medido exato N=2..8 em R5-1). **Topologia NÃO seleciona:**
  π₃=ℤ p/ todo grupo simples (Bott); π₄,π₅ só separam SU(2) de N≥3, nunca 3 de 4; o
  único π_k que separa 3 de 4 (π₆=ℤ₆ vs 0) é fisicamente inerte em 3+1D (R5-2).
  Minimalidade ≠ unicidade (SU(4+) também complexos/anômalos); o requisito "fundamental
  complexa" é **importado** (fenomenológico), como d=3 — a rede causal nunca mede N
  (input do `su3_core`, como d=3 é input de rⁿ⁻¹). Análogo de espaço-de-grupos do DS1–3.
- **Status:** [NUNCA TENTADO] → **[SÓLIDO] (seleção estrutural, com import declarado)**.
  Fecha o buraco lógico ("prova SU(2) mínimo mas não distingue SU(3) de SU(N≥4)");
  NÃO altera o [SÓLIDO] de FL1 (que se sustenta no confinamento/octeto medidos).
- Charter+dados: `R5_GROUP_SELECTION.md`; `results/foundations/r5_group/`
  (`R5_3_synthesis.md`). **Dependências CUMPRIDAS** (FL1/R1 consolidado; MIN3).

> **Itens de prioridade menor** (DEV←TEIC completo a₀/β/η; Λ dinâmica; C5 dimensão
> espectral; C6 vórtices; busca KR em PTA; FM5; léptons; SU(2)×U(1)) seguem na
> Seção 6 com urgência/dificuldade; entram no roteiro após os 5 acima, ou em paralelo
> quando baratos e independentes (ex.: FM5, busca KR em dados públicos).

---

# Protocolo de pesquisa

```
1. Resultado encontrado → registrar AQUI (atualizar o status do item
   correspondente nas Seções 1–7) → NÃO criar paper imediatamente.

2. Continuar a rota planejada — não desviar para empacotar um resultado antes de
   explorar todos os caminhos do mesmo cluster.

3. Um cluster está "maduro para paper" quando:
   (a) todas as brechas identificadas no mapa foram atacadas (ou declaradas
       fronteira com razão documentada);
   (b) o resultado sobreviveu ao teste de robustez;
   (c) a ligação com o resultado vizinho mais próximo foi verificada
       (ex.: matéria→gravidade direta, R2).

4. Papers são SAÍDA do programa, não GUIA — a rota não muda porque um paper foi
   submetido ou rejeitado.

5. Honestidade obrigatória: se um [SÓLIDO] mostrar brecha nova, atualizar o status
   IMEDIATAMENTE — nunca manter status inflado porque o paper já foi submetido.
```

> **A1 / C1 — Auditoria formal da guarda anti-circularidade ✅ EXECUTADO (jun/2026).**
> Gate de entrada da campanha de organização (Fase 2). (i) `SCAN_DIRS` da guarda
> (`tests/test_no_circularity.py`) estendido do subconjunto antigo para **TODO o
> tree gerador** (`src`, `experiments`, `results/**`, `docs/campaigns/**` incl.
> `sr_teic_core.py`) = **396 arquivos**; guarda **VERDE** (zero fórmula de dilatação,
> zero complexo não-rotulado; `r5_group_core.py` recebeu marcador `SU(3) GROUP-DEF
> COMPLEX`, mesma exceção principiada de `su3_core.py`). (ii) Novo detector
> `tests/test_no_scale_literal.py` (critério pré-registrado: `|literal/X−1|<1%` para
> X∈{c,G,ℏ,a₀,m_e,M_Pl,+potências/combos}; 48 alvos) → **21 candidatos, TODOS
> classificados** como constante externa em camada de comparação/conversão/falsificação
> (nenhum alimenta gerador da rede causal). **Critério de morte R-0 NÃO disparado** —
> a tese "forma emerge, escala é externa" sobrevive à auditoria formal: escala entra
> só na fronteira de comparação, declarada externa. (iv) Ambas as guardas agora
> **descobríveis por pytest** e no CI. Relatório verbatim:
> `docs/campaigns/GUARDA_A1/SCALE_LITERAL_REPORT.md`; síntese: `.../SYNTHESIS.md`.
> **R-0 verde ⇒ libera o paralelismo da campanha (B1, A2–A5, B3/B4).**

> **B1 — Razões internas independentes de K (hierarquia) ☠ MORTE bem-entendida
> (jun/2026).** Prioridade da Frente B (escalas). Pergunta: existe combinação
> adimensional de M_Sk, σ, G_net invariante sob a normalização da ação E que
> carregue hierarquia? Decisão de desenho: **K = rescala global S→K·S** (todos os
> setores herdam um K). Varredor `docs/campaigns/ESCALAS_B1/B1_kscan.py` (K∈[0.3,10],
> 33×, expoentes **ajustados** do scan): **M_Sk∝K^+1.00** (saddle clássico),
> **G_net∝K^−1.00** (Poisson re-medido, reproduz D3D), **σ corre** (β→Kβ, lib.
> assintótica). Resultado: a única combinação plana a <5% é **M_Sk·G_net**, mas é
> **definicional** (G_net≡A/M ⇒ =amplitude A, sem hierarquia, morte-b); a combinação
> que carregaria a hierarquia **M_Sk·√G_net = M_Sk/M_Pl ∝ K^+½ ESCALA** (CV 56%,
> morte-a); todo combo com σ varia (×6.2, ×3.1). **Razão estrutural:** rescala global
> da ação é só escolha de unidade — não fixa número grande adimensional entre
> domínios. ⇒ **hierarquia M_próton/M_Planck permanece [EXTERNO-B]**; porta fechada
> bem-entendida (negativo de 1ª classe). **Plano R-1:** promove **B5** (por que η/ℏ
> não pinam) ao topo da Frente B como mecanismo desta porta; B2 NÃO promovido
> (dependia de B1 positivo). Síntese: `docs/campaigns/ESCALAS_B1/SYNTHESIS.md`.

> **B5 — Por que η e ℏ "não pinam" ⟲ REVISA FD1 (MORTE → Verdito B) (jun/2026).**
> Promovido ao topo da Frente B pelo R-1. Pergunta: o k_c≈1 de FD1 (η não pina) é
> artefato de tamanho ou fundamental? FSS `docs/campaigns/ESCALAS_B5/B5_fss.py`
> (N=200..1600, d∈{2,4}, bootstrap): **k_c é SIZE-STABLE** (tail-spread d4=0.008; a
> não-robustez de FD1 era efeito de N=300 ⇒ **teorema, não artefato**) e
> **dimension-dependent**: d2 k_c→1.01 (≈ER-genérico, 1σ) vs **d4 k_c→0.67 (30σ ≠1,
> NÃO-genérico)**. k_c segue o **Molloy–Reed** z_c=⟨k⟩²/(⟨k²⟩−⟨k⟩) (CV de grau
> geométrico N-estável: 0.33 em d2, 1.0 em d4) + correção de clustering — propriedade
> de grafo calculável. ⇒ η=(k_c−1)² é **FORÇADO** (≈0 em d2, ≈0.11 em d4), NÃO o
> parâmetro livre da SR, **mas dimension-dependent ⇒ sem η universal** (herda o input
> de dimensão, como d=3 [EXTERNO] em DS1–3). "Não pina" = não há valor
> independente-de-dimensão a pinar; o limiar é geométrico. **Revisa o FD1 MORTE** (era
> parcial — vale d2, falha d4 — e contaminado por tamanho). **Elo com B1:** B1 (escala
> global não fixa hierarquia) + B5 (limiares absolutos = propriedades de grafo
> calculáveis mas dependentes de input) fecham a tese "forma deriva, escala não" **com
> mecanismo**. Síntese: `docs/campaigns/ESCALAS_B5/SYNTHESIS.md`.
> **[REFINADO por B6 (jun/2026)]:** a "size-stability" de k_c(4) (tail-spread 0.008) era
> um **platô de N≤1600**; estendendo a N=3600, k_c deriva suavemente (~0.69→~0.61, banda
> 0.10). O **núcleo permanece** (k_c dimension-dependent, não-genérico a 8σ, liderado por
> Molloy–Reed); só a precisão do valor (0.67) e a palavra "size-stable" são suavizadas.

> **B6 — η em d=4 via Molloy–Reed: derivação em cadeia ◐ MORTE PARCIAL bem-entendida
> (jun/2026).** Pergunta: os invariantes que fixam k_c(4) (CV, clustering C) são d-only,
> tornando η=(k_c−1)² derivado de d=4? Driver `docs/campaigns/ESCALAS_B6/b6_eta_chain.py`
> (gate Stage 0 ✓; grafo idêntico a B5). **Stage 1** ρ-invariância VERDE mas **trivial**
> (causalidade de Minkowski é scale-invariante → CV/C/z_c dependem só de N,d). **Stage 2:**
> z_c_MR=0.50 e CV=1.00 **rock-stable** (líder d-only), mas **k_c não precisamente pinado**
> (banda large-N 0.627±0.10, drift residual → refina B5). **Stage 3+4:** a forma
> **independente** (não-circular) `z_c_MR/(1−C)=0.585` reproduz k_c a **7%** a partir de
> dois invariantes d-only (CV, C) → **mecanismo de η identificado e correto no nível de
> k_c**; MAS η=(k_c−1)² é **quadrático** (7% em k_c → 24% em η) e k_c não converge a
> N≤3600 → **valor preciso de η fica [EXTERNO-B]**. **Resultado:** η NÃO é parâmetro livre
> da SR (d-determinado em ordem líder, η_MR=0.25, não-genérico a 8σ), mas o valor refinado
> (~0.14) precisa da **correção clustering+finite-size** (geométrica, sem forma fechada) —
> não uma escala SI. Padrão "mecanismo emerge, número preciso herda input". Elo
> R1(d=4)→colapso(η) **parcial**. Síntese: `docs/campaigns/ESCALAS_B6/SYNTHESIS_B6.md`.

> ## ⊕ B1+B5+B6 — TESE DE ESCALAS COMPLETA COM MECANISMO (jun/2026)
>
> A Frente B (escalas) fecha como um todo coerente, com mecanismo e gradação de status:
>
> 1. **[B1]** A **normalização global da ação (K)** não fixa razões de massa entre
>    domínios: sob S→K·S, M_Sk∝K e G_net∝1/K, então a hierarquia M_Sk·√G_net = M_próton/M_Pl
>    **escala ∝√K** — uma rescala global é só escolha de unidade.
> 2. **[B5]** Os **limiares absolutos** que o substrato produz (η, e por analogia ℏ) são
>    **propriedades de grafo (Molloy–Reed + clustering)**, **dimension-dependent**, sem
>    valor universal a pinar.
> 3. **[B6]** **η(4) é d-determinado em ordem líder** (Molloy–Reed z_c_MR=0.50, não-genérico
>    a 8σ; mecanismo `z_c_MR/(1−C)` reproduz k_c a 7%), mas o **valor preciso** herda uma
>    **correção geométrica (clustering+finite-size) sem forma fechada exata**.
>
> **Padrão unificado:** *mecanismo/forma emerge do substrato; o número preciso herda um
> input **geométrico** (dimensão, clustering) — não uma escala SI.*
>
> **Status gradado:**
> - **[DERIVADO]** para a **forma e o mecanismo** (rescala-de-unidade, limiar de percolação,
>   Molloy–Reed + clustering).
> - **[EXTERNO-B-geométrico]** para o **valor preciso** — input geométrico calculável em
>   princípio (dimensão, clustering do grafo causal), **distinto de [EXTERNO-B] simples**
>   (G, f_π em SI). No **Paper Síntese**: apresentar como **gradação**, não como a mesma
>   categoria de G ou f_π.
>
> Sínteses: `docs/campaigns/{ESCALAS_B1,ESCALAS_B5,ESCALAS_B6}/SYNTHESIS*.md`.

> **A4 — Propagação BD smeared estável (ω=ck da evolução) ☠ MORTE CARACTERIZADA;
> ressalva do Goldstone PRD mantida-com-mecanismo (jun/2026).** Frente A, **timing:
> antes da submissão do Paper Goldstone**. Fecha (ou não) a brecha [FRACO] de E2
> ("ω=ck é do símbolo; propagação direta instável"). Driver `docs/campaigns/
> PROPAGACAO_A4/a4_bd_propagation.py`. **Stage 1 gate** (lattice sharp): ω=ck c=1.000
> spread 0.0% estável — máquina validada. **Stage 2** (smeared como Laplaciano espacial):
> rigidez pequeno-k c²=Σg(d)d²=**−20 (tachiônico)** — pesos BD alternam sinal, não são
> Laplaciano PSD. **Stage 3** (operador BD simétrico no causet, N=235/381): **~80%
> autovalores NEGATIVOS** (indefinido = Lorentziano □), leapfrog blow-up ×10⁸³; marcha
> retardada falha (sinal amortecido/não-normal). **Veredito:** a hipótese C4 (smearing
> estabiliza) é **falsificada** — o problema NÃO é sharp-vs-smeared (smearing corrige
> LOCALIDADE, problema de C5); a instabilidade da propagação é a **indefinição
> Lorentziana** do d'Alembertiano, intrínseca a qualquer aproximante de □. **ω=ck é REAL
> on-shell** (símbolo, E2 correto); propagação direta estável **não existe** (modos
> off-shell λ<0 crescem). **E2 fica [FRACO]**, ressalva = limitação **de princípio
> caracterizada** (não artefato numérico). **Paper Goldstone:** submeter com a ressalva
> explícita e seu mecanismo — **resolvida (caracterizada), não pendente**. Timing
> cumprido. Síntese: `docs/campaigns/PROPAGACAO_A4/SYNTHESIS.md`.

> **A5 — Resíduos baratos (ε(2) + MG1-3D) ✅ SUCCESS, fecha últimas ressalvas do Paper MG
> (jun/2026).** Frente A, prioridade mais baixa. Driver `docs/campaigns/RESIDUOS_A5/
> a5_residuos.py`. **(1) ε(2):** ε=1 em **3 calibradores winding-2 swap DISTINTOS** (PI0b
> base + perfis width=1.5/2.5, todos comps=1 swap, estáveis, classe=1) → anomalia de
> framed-transfer **uniforme** na classe swap → **spin-estatística do bárion fechada**
> (a correção ε(2)=1 do PI3 não é mais campo-único; com PI5 ε(3)=0, ε é paridade de
> winding medida em n=1,2,3 robusta a campo). Controle: rotação sobre eixo isospin
> distinto dá comps=2 (não-swap), corretamente excluído. **(2) MG1-3D:** na malha **3D
> Cartesiana** completa (poisson3d_solve, sem 1/r), expoente exterior **−0.991≈−1** e
> **G_net=A/M constante (CV 0.0%)** ao varrer e_sk (M 175→218) → θ=G_net·M/r **não é
> artefato de simetria radial**. Aspersão irregular genuína = mesma fronteira de
> não-localidade de A2/A4 (registrada, não tentada). Síntese:
> `docs/campaigns/RESIDUOS_A5/SYNTHESIS.md`.

> **B3 ∥ B4 — O fóton: 2-célula magnética a baixa curvatura ⚑ B3 candidato / B4 morte
> (artefato); [FRONTEIRA] permanece (jun/2026).** Caminho crítico do fóton (Photon-Arc).
> Lacuna: E6c abre o setor magnético só no Planckiano (frac_B cruza 0.01 só a R̂=2;
> <0.01 a R̂≥8). **B3** (`docs/campaigns/FOTON_B3B4/b3_future_cone.py`): células de
> intersecção de cones futuros (par spacelike + futuro comum) dão **frac_B=0.84** a
> baixa curvatura (gate timelike=0.000 ✓), MAS o **controle de tautologia** (ápices
> aleatórios) dá **0.61** → ~61% é piso cinemático da base spacelike, só ~22pp são
> causais → **SUCCESS_B3_CANDIDATE** (gauge-invariância + 2-complexo NÃO testados; não
> são os diamantes do operador BD → novo complexo proposto). **B4**
> (`b4_anisotropic.py`): de Sitter anisotrópico dá frac_B 0.003→0.58, MAS o **controle
> de artefato** mostra os planos esticados (12,13) explodindo ×6e4 e o não-esticado (23)
> fixo ×1.00 → **DEATH_B4_COORD_ARTIFACT** (stretch de coordenada no embedding, não
> física; B4 fiel = anisotropia na ordem causal Bianchi-I, campanha maior). **Veredito
> conjunto:** fóton magnético **[FRONTEIRA]**; nenhum charter de paper congelado; ambas
> as direções têm follow-up bem-definido (não esgotadas). **Ponto alto:** dois resultados
> crus espetaculares (0.84, 0.58) eram falsos — controles pré-pensados expuseram a
> contaminação; sem eles, um paper teria sido congelado sobre um artefato. Síntese:
> `docs/campaigns/FOTON_B3B4/SYNTHESIS.md`.

> **A3 — Goldstone FSS (N maior) + S(k)~1/k^α ✅ CONSOLIDA (jun/2026).** Frente A.
> Driver `docs/campaigns/GOLDSTONE_A3/A3_fss_sk.py` (motor `orientation_core` sem
> modificação; estimador S(k) validado na rede 3D ordenada: α=1.76≈2). **(a) LRO:**
> m(N) **cresce** monotônico (0.961→0.995, trend d ln m/d ln N=+0.011 ≫ piso −0.5),
> U4=0.667=2/3 exato, m/piso 12–62×, estendido de N=1462 → **N=3888 (2.7×)** →
> **SUCCESS_LRO; a ordem do ferromagneto de orientação NÃO é artefato de tamanho** →
> nenhum rebaixamento do Paper Goldstone PRD (R-4 positivo). **(b) S(k):** α=**0.06±0.01
> PLANO** e **independente de N** (812→3888; tendência −0.00) → links causais **nus =
> campo médio NÃO-LOCAL**, exclui rigidez k² (α=2) a ~190σ → **endurece E1-3 Verdito C**:
> o magnon relativístico (E2, ω=ck) exige o operador BD/Sorkin (e10), não os links nus.
> Teto N=3888 (alvo 5–10k não atingido, build O(N³)), mas m(N) e α(N) planos no range ⇒
> extrapolação não muda veredito. Síntese: `docs/campaigns/GOLDSTONE_A3/SYNTHESIS.md`.

> **A2 — Loops de Wilson SU(3) no causet ⚑ FRONTEIRA, confirma escopo cúbico do
> Paper SU3 (jun/2026).** Frente A, **maior risco de obsolescência** (poderia
> rebaixar o confinamento do Paper SU3). Driver `docs/campaigns/CONFINAMENTO_A2/
> a2_su3_causet.py`. **Risco mitigado a priori:** o paper já escopa confinamento ao
> **lattice cúbico 8⁴** ("Wilson loops on an $8^4$ lattice"); só ferromagnetismo é
> reivindicado nos dois. **Stage A** (validação): MC gauge SU(3), Creutz χ(2,2)=
> 1.39/0.96/0.38 em β=4/5/6 **reproduz FLC** (1.35/0.96/0.33), σ>0 decrescente =
> liberdade assintótica → MC validado. **Stage B** (causet): gauge SU(3) termaliza
> nas plaquetas de diamante (⟨W₁⟩ sobe 0.31→0.46 com β) MAS **todas as plaquetas são
> diamantes área-1**, **zero retângulos R×T controlados**, e a holonomia não-abeliana
> de patch não fecha palavra-de-bordo limpa (surrogate abeliano de E7 **não se estende**
> a SU(3)) ⇒ **string tension sem estimador controlado no causet** (death-trigger 2).
> Confinamento = **[SÓLIDO] no cúbico, [FRONTEIRA] no causet** (obstrução E5/E7, pior
> no não-abeliano). **Paper SU3 cúbico-só CORRETO, permanece — SEM rebaixamento**;
> fronteira documentada. Síntese: `docs/campaigns/CONFINAMENTO_A2/SYNTHESIS.md`.

---

# Verificação final

> **Correção registrada (jun/2026).** A varredura da FASE 1 confiou em
> `CONVERGENCE_PATHS.md` (que lista C1–C6 como caminhos *futuros*) sem abrir os
> diretórios `results/foundations/c5/` e `results/cosmology/c6/`, que **já estavam
> preenchidos**: C5 (dimensão espectral) foi executado com veredito C (morte, sem
> corrida CDT) e C6 (vórtices quantizados) com veredito B. Ambos foram listados
> indevidamente como [NUNCA TENTADO] e estão **corrigidos** acima. Re-varredura dos
> demais itens "nunca tentados" (FM5, Λ-dinâmica, léptons, inércia, seleção-de-grupo,
> espectroscopia-octeto, busca-KR-em-dados) confirmou que **não têm diretório de
> resultados** → genuinamente não tentados. Lição: abrir todo diretório de `results/`,
> não confiar só nos índices.

**1. Todas as campanhas varridas?** Sim (com a correção acima) — geometria (R1–R4, D1–D3, NL), vácuo
(E1–E6, VS1–VS5), matéria (M/P, CR_*, PHI, SU2, SU2_QUANT, FR, PI, FL1, FL3),
fenomenologia (FM1–FM4, FN, HQ2/HQ3, BTFR, LIV), estrutura (DS, MIN, CR, T3A–C,
LAMBDA), convergência (Fases 1–3). Ver tabela da FASE 1.

**2. [SÓLIDO] com brecha não declarada?** Auditados e re-tagueados nesta varredura:
- E2 ("dispersão relativística") foi rebaixado de [SÓLIDO] implícito para **[FRACO]**
  (é do operador BD, não do campo).
- FL1/SU(3) ("SUCESSO TOTAL") permanece [SÓLIDO] **com ressalva explícita**: robustez
  não testada, Regge do tubo medido uma vez (R1, R5 do roteiro fecham).
- A ligação matéria→gravidade está corretamente como **[FRACO]/composição** (R2 fecha).
- m_A=CDM rebaixado para **[FRACO]** (misalignment importado).

**3. Lista de [NUNCA TENTADO] completa?** Após a correção de C5/C6 (ver caixa acima) e
o fechamento de R1–R3, restam **12** itens genuinamente não tentados na Seção 6,
incluindo os pequenos (busca KR em PTA, ordem de transição SU(3) em L>12, espectroscopia
do octeto, quantização coletiva quantitativa) e os grandes (fóton BD-gauge, DEV completo).
A re-varredura dos diretórios de `results/` confirmou que esses 12 não têm dados.

**4. Roteiro ordenado por critérios explícitos?** Sim — urgência de integridade →
impacto/esforço → sequência lógica, declarados em cada item.

## Contagem por categoria de status

| Categoria | Itens |
|---|---|
| **[SÓLIDO]** | ~17 (R1–R4, D1–D3-forma, C1–C4, E1, MIN, SC-forma, SU2 B=1/spin½, CR1–4, DS, L1–L3, T3C-proporção, FL1-com-ressalva, FQ2) |
| **[FRACO]** | 6 (E2/dispersão, BRIDGE_RHO P3, MATTER_COMPLEXITY, FM2-1 ν, FM4 m_A=CDM, FL1 Regge-tubo) |
| **[POSTULADO]** | 4 (ação O(3), quadraticidade gravitacional, misalignment, d=3) |
| **[EXTERNO-T]** (por teorema) | 3 (dominância Skyrme, enrolamento Higgs, Derrick) |
| **[EXTERNO-B]** (por falha) | 6 (G, ℏ, a₀, m_A/massas, f_A, pesos K/λ_p) |
| **[IDENTIFICADO]** | 3 (Skyrmion↔bárion, a₀(z)∝H(z), Khoury-mecanismo) |
| **[MORTO]** | ~15 (E4 fóton, S8 ×4, Skyrme-dominância, criação ×4, VS1–VS5, Regge-bárion, LIV, T3A/B, condensado) |
| **[FRONTEIRA]** | 5 (Schwarzschild forte/horizonte, NL não-linear, E5, E6, E7 — E7 inconclusivo-estrutural, lean anti-confinamento) |
| **[NUNCA TENTADO]** | 10 (Seção 6; fechados jun/2026: 1/robustez FL1, 2/Skyrmion→gravidade, 3/C1-Khoury, 14/FM5, 15/ordem-transição-SU3; **corrigidos: 8/C5 e 9/C6 JÁ estavam executados — erro de varredura da FASE 1**) |

## Os 5 itens de maior prioridade no roteiro

1. ~~**Robustez de FL1 (variar ação ~10%)**~~ ✅ **EXECUTADO (FLR, jun/2026) — SU(3)
   ROBUSTO.** Confinamento, octeto (8/8) e Skyrmion sobrevivem ±10% na ação. Era a
   posição 1 por integridade pura (SU(3) sustenta o PAPER_MATTER_GRAVITY companion); a
   ressalva "robustez não testada" do mapa está fechada. **Próximo do roteiro: R2.**

2. ~~**Skyrmion como fonte direta de gravidade**~~ ✅ **EXECUTADO (MG1, jun/2026) —
   forma [SÓLIDO].** O perfil ε(r) real do sóliton sourceia θ=G_net·M/r (expoente
   −0.992, A∝massa própria, = G_net top-hat). Fecha a brecha central do paper mais
   forte (o "natural next step" que ele nomeia). G_net absoluto continua [EXTERNO].

3. ~~**C1 — equivalência formal TEIC ≡ Khoury**~~ ✅ **EXECUTADO (C1, jun/2026) —
   EQUIVALÊNCIA DE LIMITE (parcial).** A equivalência vive no setor longitudinal
   (χ∥~h^{−0.37}, deep-MOND), não no fônon transverso (magnon ∝X, χ⊥~h^{−0.98}). Mata
   "magnon = fônon de Khoury"; sharpena a Fase 2; a₀ externo reforçado (ρ_s cavalga em
   J). Positivo parcial, como previsto. Consolida FM2-1.

4. ~~**Operador BD-gauge Lorentziano (o fóton)**~~ ✅ **EXECUTADO (E6-3, jun/2026) —
   FRONTEIRA TÉCNICA.** Construído o operador indefinido E²−B²: gauge-invariante por
   construção (5.7e-16), validado em rede 4D (ω=ck, c=1.05), mas **H2 falha no causet
   porque os diamantes são 100% elétricos** (B-type=0.0000) — setor magnético vazio, sem
   cone de luz. Resultado parcial como previsto (H1 sim, H2 não), mas com diagnóstico
   afiado: a fronteira é a **ausência de 2-célula spacelike** (novo item 4b), não a
   assinatura. Sem precedente na literatura CST (busca feita, `E6_literature.md`).

5. ~~**Seleção de grupo via teorema (por que SU(3), não SU(4))**~~ ✅ **EXECUTADO (R5,
   jun/2026) — VEREDITO B (seleção por minimalidade).** SU(3)=menor grupo simples com
   fundamental complexa / d^abc≠0 (mesma fronteira N=2|3, medido exato N=2..8). A
   topologia (π₃=ℤ, Bott) NÃO distingue 3 de 4 — confirmou a metade negativa antecipada;
   o requisito "complexa" é importado (fenomenológico), como d=3. Análogo de DS1–3 no
   espaço de grupos. Fecha o buraco lógico sem inflar FL1.
```

---

## Camada de colapso e seta do tempo (campanhas COLAPSO_SR_TEIC + FRONTEIRA_SETA_COSMOLÓGICA)

- **COLAPSO_SR_TEIC** (`docs/campaigns/COLAPSO_SR_TEIC/`): a rede causal de TEIC GERA
  espontaneamente a SATURAÇÃO de χ_eff de SR (χ_A=λ_max(A)/N satura ~0.55 d=2 / ~0.17
  d=4, N-estável; reproduz a dicotomia de 2 setores de SR — adjacência satura,
  Laplaciano/BD decaem). **[EXP1 SOBREVIVE]** Mas NÃO gera a SETA do tempo: forward vs
  backward indistinguíveis (D_TR<3), ordem causal = DAG perfeito (eixo emerge, seta não).
  **[EXP2 MORTO]** A seta só surge sob contorno de baixa entropia imposto (cone D_TR~55).

- **Seta do tempo cosmológica:** **[FRONTEIRA FECHADA — universal, não dívida de TEIC]**
  (`docs/campaigns/FRONTEIRA_SETA_COSMOLOGICA/`). A Past Hypothesis é externa a TEIC, DEV
  e SR igualmente. Λ-dinâmica = transporte (V₄_past finito + E(z) ΛCDM importado); DEV
  não tem setor cosmológico derivado (vácuo DBI = equilíbrio de referência, lida não
  alterada); SR postula a poda irreversível. Gerador de TEIC (`sprinkle_box`) é UNIFORME
  → arrow-free por construção. TEIC sai à frente: entrega o EIXO (DAG) que SR engendra via
  d_s:3→4. Única fresta não-circular (ponto de Janus/complexidade) é programa EXTERNO,
  registrada com trava em `PRE_REGISTRO_FUTURO.md` (não reivindicada). Status idêntico a
  CST/Modelo Padrão.

---

## Meta-análise: mapa de invariantes TEIC × DEV × SR (jun/2026)

- **MAPA_CONVERGENCIA** (`../NOVA TEORIA/INVENTARIO_CONVERGENCIA.md`,
  `MAPA_CONVERGENCIA.md`): **primeira campanha que cruza as três teorias num mapa de
  invariantes**, com gate anti-convergência-espúria (mesmo objeto matemático, não só a
  mesma palavra; arquivo:linha obrigatório). Pré-requisito de uma eventual "teoria
  invertida" por engenharia reversa dos invariantes compartilhados.
- **Achado:** o núcleo invariante é **bipartido** (eixo TEIC≡SR medido em
  `COLAPSO_SR_TEIC`/FS: saturação λ_max/N, dicotomia 2 setores, GOE ⟨r⟩→0.53, Δx², σ⁻²,
  Lindblad CP; eixo TEIC≡DEV por teorema: deep-MOND X^{3/2}). **Nenhum invariante
  triádico.** Todas as formas sobreviventes são **genéricas-por-teorema** (Milgrom, RMT,
  Laplaciano de ordem-líder, Poisson).
- **Veredito de restrição: [CLASSE GRANDE]** — o núcleo NÃO seleciona uma estrutura;
  isoespectralismo (B8) confirmado a **nível de teoria**. A teoria invertida seria mais
  um membro da classe de equivalência, não única. **Recomendação registrada: não
  construir a teoria invertida como teoria nova/única** (o mapa não deu [FORÇA ESTRUTURA]).
- **Divergências que excluem identidade:** setor vetorial (DEV exige Proca m_A>0; TEIC
  força m_A=0 — identidade DEV↔TEIC FALSIFICADA, `DEV/auditoria_fundacao/`); magnon ∝X vs
  fônon X^{3/2} (C1); d_s plateau (TEIC) vs corrida 2→4 (SR, [EXTERNO NÃO-AUDITADO]).
- **Parede comum confirmada e herdada:** seta do tempo (Past Hypothesis, uma só); escala
  absoluta (três paredes coincidentes, mecanismos distintos); η (só TEIC≡SR). Nenhum
  caminho para a escala no núcleo (B1, B7, FD1, DEV-fundo todos fecham).
- **Cross-check (re-run independente da Fase 0, `../NOVA TEORIA/AUDITORIA_RERUN_FASE0.md`):**
  passada independente das fontes primárias reproduz o inventário **16/16 itens, gate
  idêntico** → **sem ancoragem detectável** (3 sinais de não-viés: auto-caveats genérico-
  Laplaciano, [VERBAL] na palavra-armadilha "saturação", candidatos omitidos reforçam).
  Achou 2 candidatos omitidos (Λ_eff=3γ₀²/4 vs a₀~cH₀ = [VERBAL]; slip DEV↔TEIC 15× off =
  [PARCIAL]) — ambos **falham o gate**, não entram no núcleo, não mudam [CLASSE GRANDE].
- **FX1 (teste de novidade §C, executado jun/2026, `COLAPSO_SR_TEIC/FX1_VERDICT.md`):** o único
  candidato a previsão fora do núcleo — razão adimensional R_FX1=Γ_dec/Var_bulk(λ) do mesmo
  operador (colapso FS1 ÷ gás espectral FS2) — foi pré-registrado e morto: **H_NULO**, R_FX1
  cavalga em σ_x (fator ~6) e dim (~2×); Stage 0 passa (scale-free 7e-16, controle GOE=1.74).
  **[CLASSE GRANDE] agora SELADO empiricamente** — não há razão forçada que ancore teoria
  invertida única. Recomendação reforçada: não construir; publicar o mapa como resultado.

## Campanha XI — Um comprimento de correlação pode divergir? (jun/2026) — [FALSIFICADA]

`docs/campaigns/ESCALA_XI/` (PRE_REGISTRO + SYNTHESIS + xi_suite/run_campaign/analyse/
validate_positive/focused_knn). Engine `orientation_core` reutilizado SEM modificação;
guard VERDE. **Pergunta:** o caráter mean-field do ferromagneto O(3) sobre o sprinkling
causal (sem ξ divergente) é consequência da alta coordenação não-local do Hasse cru?
Reduzindo a coordenação, emerge uma 2ª ordem genuína com ξ_2nd divergente?

- **Controle positivo (rede 3D periódica, idêntico pipeline):** criticidade CERTIFICADA
  — U₄ cruza em J_c≈0.69, χ_max ∝ N^0.667 (=γ/ν/d Heisenberg-3D). Prova que a suíte
  enxerga criticidade. (ξ_2nd transverso é Goldstone-singular na fase ordenada → veredito
  repousa no tripé z(N)/drift-J_c/χ_max, não em ξ/L sozinho.)
- **Achado 1 — não-localidade é Lorentz-protegida:** Alavanca B (janela de tempo-próprio
  ℓ_k) e C (dimensão (2+1)D) **FALHAM em reduzir coordenação** — z DIVERGE com N (×2.3 a
  ×2.8, como o baseline ×3.1). Corte por τ não localiza (slab hiperbólico cresce com a
  caixa); reduzir dimensão não cura (Hasse 2+1D ainda z→∞). **Só um cap de CONTAGEM
  (k-NN) reduz coordenação** sem injetar referencial.
- **Achado 2 — sem cap, NÃO há ponto fixo:** baseline/C/B têm **J_c→0** conforme z→∞
  (0.10→0.03; como grafo completo J_c∼1/z). Um ξ divergente não tem onde morar.
- **Achado 3 — com cap (k-NN, z→2k fixo, J_c fixo):** transição contínua REAL (U₄ cruza
  em J≈0.6), MAS ξ_2nd/L **métrico** é um **platô LRO ~0.1** (mesmo valor em J_c e fundo
  na fase ordenada — não tem PICO em J_c), e χ_max ∝ N^≲0.5 (FSS mean-field, não o
  geométrico N^0.67 do controle). Grafo causal esparso = **small-world/Bethe-like** →
  Heisenberg mean-field por teorema; correlação de grafo diverge, métrica não.
- **Circularidade:** o sinal ingênuo ξ/ℓ→∞ aparece em A mas é a armadilha LRO
  (necessário-não-suficiente; qualquer LRO dá ξ∼L); o suficiente (pico de ξ/L em J_c)
  FALHA. k, ℓ_k marcados `[External]`, nunca usados na conclusão (só adimensionais).
- **VEREDITO: HIPÓTESE FALSIFICADA — mean-field ESTRUTURAL** a esta classe de
  substratos, por barreira DUPLA (Lorentz proíbe corte métrico de coordenação +
  topologia small-world/Bethe). Reforça nota-de-rodapé-1 do paper do fóton e
  B7-MEANFIELD/B9 com mecanismo. **Transmutação dimensional sem âncora — frente fechada.**
  §10 do charter (crescimento Rideout–Sorkin) NÃO se justifica (gatilho era ≥1 alavanca
  com sinal não-circular; nenhuma deu). A (k-NN) é FRONTEIRA, não morte-limpa (tem
  U₄-crossing); morte vem do platô-ξ/L + χ_max-MF + argumento Bethe.

> **Atualização posterior (jun/2026, via `docs/campaigns/RIDEOUT_SORKIN_TRIGGER/`) —
> refinação de precisão, NÃO reversão.** O veredito da XI **permanece correto** para o
> **sprinkling de Poisson sobre um background Lorentziano de fundo** (e as variações
> testadas: coordenação geométrica, não-localidade intermediária ℓ_k, dimensão (2+1)D).
> A campanha RIDEOUT_SORKIN_TRIGGER mostrou que esta propriedade **não se generaliza** a
> causal sets gerados por **crescimento sequencial (CSG)**, cuja coordenação ⟨z⟩(N)
> **satura** (finita) em todos os regimes testados, em vez de divergir. A frase correta,
> revisada, é: **"o mean-field é estrutural ao sprinkling Lorentziano de Poisson, não aos
> causal sets como classe."** O mecanismo é o mesmo Achado 1 da XI lido ao contrário: a
> divergência de coordenação vem da não-localidade **Lorentz-protegida** (boosts), que o
> CSG não tem. ⇒ A afirmação "§10 RS NÃO se justifica" acima fica **superada quanto à
> pergunta de coordenação**: a frente RS sai de dormente para **GATILHO ARMADO** (a
> campanha completa dependia do **Gatilho 2 / clustering**, agora **EXECUTADO (2026-06-27)
> = NÃO ARMADO** — `docs/campaigns/RIDEOUT_SORKIN_CLUSTERING/`: grafo de cobertura do CSG é
> tipo-árvore, square-clustering C4 sub-mean-field ⇒ a campanha completa de ξ sobre CSG
> **não roda**, linha CSG encerrada). Os Achados 2 e 3 e o veredito de falsificação para o
> sprinkling permanecem intactos.

---

## FILA DE SUBSTRATOS — STATUS (2026-06-27)

A pergunta-mãe da frente da escala: existe **algum** substrato discreto cuja cinemática
escape das DUAS barreiras baratas de mean-field — (1) coordenação ⟨z⟩ divergente (Bethe) e
(2) topologia tipo-árvore (clustering sub-mean-field) — antes de qualquer construção de ação?
Quatro famílias, testadas por gatilhos cinemáticos baratos:

| # | Via | Barreira 1 (⟨z⟩ finito?) | Barreira 2 (laços dim-finita?) | Status | Próxima ação |
|---|---|---|---|---|---|
| 1 | **Poisson** (sprinkling Minkowski) | **FALHA** (⟨z⟩ diverge, Lorentz-protegida) | — (já morta na 1ª) | **MORTA** (`ESCALA_XI/`) | nenhuma nesta linha |
| 2 | **CSG** (crescimento sequencial) | **PASSA** (⟨z⟩ satura O(1)–O(10), Gatilho 1 ARMADO) | **FALHA** (Gatilho 2 NÃO ARMADO: cobertura tipo-árvore, C4 sub-MF; **fronteira em 1/3** — intermediate platô 0.019, ainda sub-MF) | **ENCERRADA** (com ressalva fronteira-intermediate) (`RIDEOUT_SORKIN_*/`) | campanha completa de ξ **não roda**; linha fechada |
| 3 | **Não-localidade intermediária** (B_k) | não testada como família própria | não testada | **NUNCA TESTADA** (só alavanca na XI) | sem prioridade definida nesta tarefa |
| 4 | **Tipo-CDT** (aresta fixa + colagem livre Pachner) | passa **trivialmente** (⟨z⟩→6 por Euler em 2D, não conquistada) | **PASSA** (C4≈0.145 saturante ~ rede 2D, ~5× piso MF) | **ARMADO (com ressalvas)** (Gatilho 3, `CDT_VIABILIDADE/`) | ✅ **executada → linha 4b** |
| 4b | **CDT 3D COMPLETO** (ação Regge+Wick, F1b validado; ferromagneto O(3) por cima) | z~13–15 (alta, fixa) | **PASSA** (C4≠0, herda laços 3D) | **A=REPRODUZ / B=NÃO RESOLVIDO** (`CDT_TEIC_FERRO/`, 2026-06-28) | B com muitos seeds (resolver χ_max noise) |
| 5 | **Percolação de longo alcance** (sobre Poisson; conecta par causal i≺j com p=min(1,(Δτ/Δτ₀)^−σ), Δτ₀=ρ^(−1/d) [External]) | **FALHA (diverge em TODO σ)** — exp. local rel. +0.68→+0.39, nunca <0.05 | **FALHA (C4 < controle aleatório em 0/11 σ)** — suprime laços, não cria | **SEM JANELA** (`PERCOLACAO_LONGO_ALCANCE/`, 2026-06-29) — **death DUPLA**, gate Lorentz VERDE (arestas bit-idênticas sob boost η=0.8) | linha **fechada** (funil: sem ferromagneto/ξ) |

### Argumento de impossibilidade parcial — ✅ FORMALIZADO (2026-06-29, `IMPOSSIBILIDADE_PARCIAL/`)
Após a 6ª morte, formalizou-se o mecanismo comum das seis (`IMPOSSIBILIDADE_PARCIAL/RESULTADO.md`).
**Veredito da análise: PROPOSIÇÃO SUPORTADA**, com a metade de *coordenação* elevada a **teorema parcial**
(não só conjectura). **Resultado rigoroso (Campbell–Mecke + não-compacidade de Lorentz):** para QUALQUER
regra de conexão Poincaré-invariante sobre o *sprinkling* de Poisson em M^d, a valência esperada é
`⟨z⟩ = ρ·Vol(H^{d−1})·∫ Δτ^{d−1} q(Δτ) dΔτ`, com `Vol(H^{d−1})=∞` (a órbita de boost a Δτ fixo é o
hiperbolóide não-compacto) ⇒ **⟨z⟩=∞ a menos que q≡0** (trivialmente esparso). Vale inclusive para a
**relação de cobertura** (q=e^{−ρc_dΔτ^d}>0) — recupera o fato conhecido de CST (valência de *link*
infinita = não-localidade). Numa caixa finita, Vol(H) é regularizado mas **cresce com N** ⇒ MF.
**Crucial — fecha (parcialmente) a porta não-pairwise:** pela média de Palm, regras de k pontos sobre o
*sprinkling* invariante ainda dão h=h(Δτ) ⇒ mesma divergência. **N(i,j) era o candidato mais próximo de
exceção e cai provadamente:** E[N|Δτ]=ρc_dΔτ^d é bijeção monotônica (verificado: N∝Δτ³) ⇒ N é "Δτ
disfarçado". **Aberturas honestas que NÃO fecha:** (1) regras de configuração sobre medidas NÃO-Poisson/
dinâmicas (CSG é o representante testado, cai na barreira-2; espaço não-varrido); (2) fora-do-equilíbrio
genuíno para a geometria (≠ NESS já testado). **Leitura unificada:** as 2 barreiras são faces de 1 tensão
— invariante-de-Lorentz ⇒ valência ∞ (barreira 1: Poisson, longo-alcance); abandonar a medida invariante
p/ valência finita ⇒ laços tipo-árvore/trivial (barreira 2: CSG, CDT). **Conexão DEV (sugestiva, NÃO
lógica):** dá razão estrutural retrospectiva p/ a importação de a₀ externo ser possivelmente forçada, não
provisória — explicitamente NÃO "DEV certo porque alternativas falharam" (inversão inválida).

**Mecanismos (por que cada veredito):**
- **Poisson MORTA:** ⟨z⟩ diverge (×3.1) pela não-localidade Lorentz-protegida (boosts); J_c→0, ξ sem onde morar (XI). **Agora explicado por teorema (IMPOSSIBILIDADE_PARCIAL): a órbita de boost a Δτ fixo é o hiperbolóide não-compacto.**
- **CSG ENCERRADA:** passa a barreira 1 (sem boosts ⇒ ⟨z⟩ finito) mas falha a 2 — o grafo de
  cobertura (Hasse) é **livre de triângulos por teorema** e a square-clustering C4 (≤0.019) é
  **abaixo do controle de Poisson mean-field** (C4≈0.03–0.05) e ~6–30× abaixo de uma rede
  dim-finita (toro C4=0.125). Coordenação finita ≠ suficiente; topologia tipo-árvore ⇒ mean-field
  por 2ª via independente. **Fronteira (Parte 1, ext. N→16000):** o regime intermediate é platô
  genuíno C4≈0.019 (não decaimento), logo **morte 2/3 + fronteira 1/3** — mas ainda sub-MF, então
  "encerrada" se mantém. **Achado próprio:** o CSG é **mais livre de laços que o próprio Poisson MF**.
- **Tipo-CDT ARMADO (com ressalvas):** o 1-esqueleto da triangulação 2D (regime flipped/DT) tem
  C4≈0.145 e transitividade≈0.30 saturantes — laços de dimensão finita, o que falta ao CSG.
  **Único da fila a passar as duas barreiras.** MAS: (1) ⟨z⟩→6 é **identidade de Euler** em 2D
  (barreira de coordenação trivial, passada por construção, não conquistada — bate 6−12/V à 4ª
  casa); (2) Pachner sem peso de ação ⇒ possível patologia branched-polymer na geometria **global**
  (o teste mede laços **locais**, sadios; não a dimensão de Hausdorff). ⇒ ARMADO cinemático é
  **necessário, não suficiente**; decisão real fica para a dinâmica completa (ação + Wick).
- **CDT 3D COMPLETO (linha 4b, `CDT_TEIC_FERRO/`, 2026-06-28) — A=REPRODUZ, B=NÃO RESOLVIDO:** com
  o motor F1b (ação de Regge + Wick, E0-3D verde, d_H→~3) rodou-se o ferromagneto O(3) da TEIC
  **verbatim** sobre o 1-esqueleto da geometria CDT 3D (fase estendida k₀=1,3, **sem semente**).
  **Pergunta A (reprodução): REPRODUZ** — LRO genuíno por FSS (m/floor 15→29, U₄=2/3, C(r)
  plateau), a ordem da TEIC sobrevive sobre **geometria dinâmica** (não só Poisson estático).
  **Pergunta B (universalidade): NÃO RESOLVIDO** — χ_max∝N^x é **noise-dominated** (4 seeds sobre
  desordem quenched; k₀=1→0.24, k₀=3→0.88 por spike, bracketam MF/geom sem resolver); o sinal
  **limpo (k₀=1) lean mean-field** junto do Poisson (χ_max~Poisson, J_c deriva ↓). z~13–15 alto
  domina apesar de C4≠0. **Geometria dinâmica reproduz a ordem mas NÃO demonstra escapar do
  mean-field** com este orçamento; resolver B exige média de desordem (muitos seeds).

- **Longo alcance SEM JANELA (linha 5, `PERCOLACAO_LONGO_ALCANCE/`, 2026-06-29) — death DUPLA:**
  varreu-se σ ∈ {0.5…8} (11 valores) na regra de conexão Lorentz-invariante p=min(1,(Δτ/Δτ₀)^−σ)
  sobre o sprinkling de Poisson, procurando a janela não-mean-field de Fisher–Ma–Nickel/Sak. **⟨z⟩
  diverge em TODO σ** (expoente local rel. +0.68→+0.39, nunca satura) e **C4 fica ABAIXO do controle
  aleatório de mesma densidade em 0/11 σ** (a estrutura de decaimento por Δτ **suprime** laços; C4 da
  família entre CSG 0.019 e Poisson MF 0.029). **Sem ponto de sobreposição:** {σ:⟨z⟩ satura}=∅ e
  {σ:C4>controle}=∅. **Mecanismo:** a regra decai na variável **errada** — Δτ é invariante, logo o
  limiar **não corta os atalhos de boost** (par de grande separação espacial mas Δτ pequeno tem p
  alto e conecta); suprimi-los exigiria limiar dependente de referencial, que a XI já provou violar
  Lorentz. **Gate de Lorentz VERDE explicitamente** (arestas bit-idênticas sob boost η=0.8) ⇒ a opção
  "TROCA COM LORENTZ" do pré-registro **não se realiza**: a janela não existe nem às custas da
  invariância. Confirma, agora **contínuo em σ** e com a invariância verificada, que o mean-field é
  **estrutural ao sprinkling Lorentziano de Poisson** — nenhuma regra de conexão Lorentz-invariante
  sobre ele escapa. Única família a falhar as DUAS barreiras simultaneamente em todo o parâmetro.

**Lição metodológica transversal (da Parte 1):** no grafo de Hasse a transitividade (3-ciclos)
é **0 por teorema** — o discriminador é o C4 (4-ciclos) normalizado, comparado ao **controle de
Poisson** (piso mean-field) e à **referência de rede dim-finita**. Um platô fraco isolado engana;
só o controle resolve. Esta disciplina está fixada no pré-registro do Gatilho 3.

**Estado da frente (2026-06-29):** **5 famílias** cinemáticas testadas por gatilho barato. Poisson
e CSG fechadas; **tipo-CDT (2D) é a única que arma**, mas as duas barreiras nela são passadas em
grande parte **por construção** (Euler fixa ⟨z⟩=6; superfície triangulada tem laços), então o
ARMADO é fraco. **Percolação de longo alcance (linha 5, 2026-06-29) = SEM JANELA, death DUPLA**:
varredura de σ (regra Lorentz-invariante p∝Δτ^−σ sobre Poisson) — ⟨z⟩ diverge em todo σ E C4 fica
abaixo do controle aleatório em todo σ, sem sobreposição; gate de Lorentz verde explicitamente
(arestas bit-idênticas sob boost) ⇒ a janela **não existe nem às custas da invariância**. Reforça
o teorema operacional: **o mean-field é estrutural ao sprinkling Lorentziano de Poisson; nenhuma
regra de conexão Lorentz-invariante sobre ele escapa** (decair em Δτ não corta os atalhos de boost).
**Linhas não-fechadas restantes** (sem recomendação, só registro): (a) campanha completa do tipo-CDT
**com ação real** (Regge + Wick) — a única que decide a geometria global (resolve a ressalva
branched-polymer) e a criticalidade não-trivial; (b) tipo-CDT em **dim 3** (onde ⟨z⟩ não é
Euler-fixado, barreira 1 volta a ser informativa) — parcialmente coberto pela linha 4b (CDT 3D
completo, B não-resolvido); (c) Via 3 (não-localidade intermediária B_k) nunca testada como família
própria. Nenhuma é gatilho barato — todas exigem construção maior.

**Síntese teórica (2026-06-29, `IMPOSSIBILIDADE_PARCIAL/`):** após a 6ª morte, o mecanismo comum foi
**formalizado** — a metade de coordenação da tensão é um **teorema parcial** (não-compacidade de Lorentz
⇒ valência ∞ para toda regra invariante de par/vizinhança sobre o *sprinkling*), que **inclusive estreita
a porta não-pairwise** (via média de Palm) e mata o candidato N(i,j) (=Δτ disfarçado). As 6 famílias são
6 faces de 1 tensão. As únicas portas honestas que sobram exigem **medidas não-Poisson/dinâmicas** ou
**fora-do-equilíbrio genuíno da geometria** — ambas fora da classe coberta pelo teorema. **Estado do
programa de escala: a frente de gatilhos baratos está esgotada e explicada; reabri-la exige sair da
ordem causal pura de pares num sprinkling de equilíbrio.**

### Campanha CDT-COMPLETA — ✅ EXECUTADA (2026-06-28, `CDT_TEIC_FERRO/`)
- **CDT-COMPLETA (tipo-CDT + ação + ferromagneto):** ERA registrada como PENDENTE; foi **executada**
  via TEORIA_CDT/F1b (motor CDT 3D com ação de Regge + Wick, E0-3D verde) + ferromagneto O(3) da
  TEIC por cima. A ressalva-2 do Gatilho 3 (geometria global sadia, não branched-polymer) está
  **resolvida por F1b** (d_H→~3, fase estendida não-degenerada). **Resultado: A=REPRODUZ
  (ordem genuína), B=NÃO RESOLVIDO (mean-field não-excluído, sinal limpo lean MF).** A
  criticalidade não-trivial (escape do mean-field) **não foi demonstrada** com 4 seeds — o
  discriminante χ_max é noise-limited; **follow-up: muitos seeds (média de desordem)**. A semente
  ("informação SOURCE o crescimento") foi testada **separadamente** e **morreu** (TEORIA_CDT/FS-3D,
  D2/memória) — esta campanha é CDT PURO + ferromagneto, sem semente.

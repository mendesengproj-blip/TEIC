# INVENTÁRIO B9 — varredura dos pipelines TEIC e DEV (Fase 0)

> **O que este documento é.** A varredura factual (código + linha, não memória) que
> precede qualquer desenho de experimento do B9. Pergunta-mãe: *o acoplamento da TEIC
> ao vácuo-DEV restaura a estrutura que a alta conectividade do causal set aniquila —
> fornecendo a escala (que B7 negou) e/ou o índice spacelike do fóton (que a Frente do
> Fóton negou)?*
>
> **Achado central, antecipado:** o B9 **não é território virgem**. Existe uma campanha
> ancestral direta — `results/dev_from_teic/` (A1–A5, jun/2026) — e o **gate do expoente
> já está medido em C1** (`results/convergence/c1/`). A varredura abaixo localiza cada
> número no código; o mapa (Fase 1) compõe o veredito.
>
> Marcadores de honestidade: **[DERIVADO]** (número verificável + JSON), **[IDENTIFICADO]**
> (forma emerge, calibração externa), **[EXTERNO]** (postulado/calibrado), **[EM ABERTO]**.

---

## 0. As duas árvores (o que existe de fato)

| | TEIC | DEV |
|---|---|---|
| Núcleo gerador | `src/causal_core.py`, `results/cmb/fm2/fm2_core.py` (ferromagneto O(3)) | EFT SVT, sem substrato; geradores são ajustes a SPARC/cosmologia |
| Acoplamento já tentado | `results/dev_from_teic/` (A1–A5), `results/convergence/c1/` | `results/bridge/` (V1–V5: DEV reconstruída a partir da rede) |
| Repositório | git trunk `su3-ordem-transicao` | git próprio em `DEV/dev_pipeline/.git` (separado) |

**Nota estrutural:** os dois lados já se encontraram duas vezes. `results/bridge/`
(lado DEV) reconstruiu os operadores DEV a partir da rede; `results/dev_from_teic/`
(lado TEIC) testou se os *números* da DEV emergem da rede. O B9 herda ambos.

---

## 1. Mapa de objetos compartilhados

| Objeto | Na TEIC | Na DEV | Status TEIC | Status DEV | Fonte (arquivo:linha) |
|---|---|---|---|---|---|
| **a₀** (escala MOND) | não embutido; correlato de grafo `h_sat ∝ ρ_s^−0.48` (R²=0.90, **sinal oposto** à hipótese) | embutido: `a₀=3703 (km/s)²/kpc`, calibrado a SPARC | **[EXTERNO-B]** | **[EXTERNO]** (calibrado) | `dev_from_teic/DEV_FROM_TEIC_synthesis.md:32`; `DEV/paper_IV/propagator_analysis.py:18` |
| **X₀ = a₀²/2** (escala de saturação) | saturação DBI do cosseno do link; constante pura π/ln2 (0.29%); escala física **∝ ρ** (UV), **não** a₀ | axioma: `X₀=a₀²/2`, fixa todas as escalas UV | **[DERIVADO]** (forma+const pura); escala **[EXTERNO]** | **[EXTERNO]** (axioma) | `TEIC_DEV_CORRESPONDENCE.md:37`; `DEV/paper_IV/propagator_analysis.py:19` |
| **β = γ²/(m_A²a₀)** | razão de grafo `ρ_s/K = 0.336` no ponto de operação J₀=1 → **48× β**; só atinge β em J_c (tuning crítico) | parâmetro único, `β≈0.0070 [0.0055,0.0085]`, calibrado | **[EXTERNO-B]** | **[EXTERNO]** (1 parâmetro livre) | `dev_from_teic/DEV_FROM_TEIC_synthesis.md:33,70-81`; `DEV/CLAUDE.md` |
| **Expoente de dispersão (kin. term)** | magnon transverso **quadrático ∝X**, ω=ck (c≈0.98); Goldstone | phonon superfluido/deep-MOND **X^(3/2)** (axioma DBI/EoS P∝ρ³) | **[DERIVADO]** (∝X) | **[EXTERNO]** (postulado) | **§3 abaixo** |
| **Resposta longitudinal χ∥ ↔ μ(x)** | anomalia de coexistência Brezin–Wallace `χ∥ ~ h^−0.37` (FM2-1) | interpolação `μ(x)=x/√(1+x²)` derivada do DBI | **[DERIVADO]** (forma deep-MOND emergente) | **[DERIVADO]** (do axioma DBI) | `C1_synthesis.md:46`; `DEV/dev_master.tex:481` |
| **Setor vetorial A_μ** (Proca massivo) | **não emerge**: gap longitudinal fecha ∝h^0.31 (A1); Anderson–Higgs obstruído por não-localidade (A5, m_A=0) | Proca/Stückelberg, 3 GdL, `m_A∈[3.7e-25,1.2e-22] eV` | **[EXTERNO-B]** (mecanismo) | **[EXTERNO]** (postulado) | `dev_from_teic/A1_longitudinal_mode.py`; `a5/A5_synthesis.md:9-19` |
| **Comprimento de coerência / L_A** | comprimento de correlação ξ⊥~1/√h (Goldstone); ξ **não diverge** (B7: campo-médio) | `L = √K/m_A < 17 pc` (escala vetorial) | **[DERIVADO]** (forma); escala **[EXTERNO]** | **[EXTERNO]** | `B7` (memória); `DEV/CLAUDE.md` |
| **Slip η = Ψ/Φ** | slip do Skyrmion **O(1)** (platô exterior 61%) — bárion local, ~15× a janela DEV; precisa do A_μ ausente | `η−1 ∈ [2.2%,4.1%]` pontual, do setor vetorial | **[EXTERNO-B]/[INCONCLUSIVO]** | **[DERIVADO]** (do A_μ) | `dev_from_teic/DEV_FROM_TEIC_synthesis.md:34,83-101` |
| **Razões de Stückelberg (C₂/C₁=1, C₃/C₁=2)** | **travadas algebricamente** (links+plaquetas) | trata **K como livre** | **[DERIVADO]** | **[EXTERNO]** (livre) | `TEIC_DEV_CORRESPONDENCE.md:32` |
| **ρ_vac ~ ρ_Λ** (coincidência) | Λ flutuante 10^−122 herdado da CST | `ρ_vac=a₀²/16πG ≈ ρ_Λ` (fator 1.5) | **[IDENTIFICADO]/[SUGESTIVO]** | **[SUGESTIVO]** (a própria DEV marca assim) | `TEIC_DEV_CORRESPONDENCE.md:46` |

**Leitura transversal (já conhecida do programa):** em todo objeto compartilhado a
**forma é derivada de um lado, a escala absoluta é externa dos dois**. Nenhum objeto é
[DERIVADO] em escala nos dois lados ao mesmo tempo.

---

## 2. Pontos de contato candidatos (mesmo objeto físico, lados diferentes)

Ordenados por prioridade do prompt:

### PC1 — Resposta longitudinal: χ∥^TEIC ↔ μ(x)^DEV  ★ (o ponto de contato central)
- **Estado:** já fechado em **C1** como **EQUIVALÊNCIA DE LIMITE (parcial)**.
- As duas descrevem o **mesmo setor de resposta deep-MOND**, mas por rotas distintas:
  a DEV via axioma DBI (`μ` derivada do DBI), a TEIC via **anomalia IR longitudinal
  emergente** `χ∥~h^−0.37` (Brezin–Wallace). Pelo **teorema de Milgrom** (Fase 2 da
  TEIC) ambas — mais Khoury — compartilham a forma `L∝|∇Φ|³ ≡ X^(3/2)` **no limite**.
- **Honestidade (C1):** a frase "o magnon da TEIC *é* o phonon de Khoury" é **falsa**;
  o que é rigoroso é o compartilhamento do **limite deep-MOND**, com escala externa.
- Fonte: `results/convergence/c1/C1_synthesis.md:9-37,44-57`.

### PC2 — Setor vetorial: análogo TEIC do A_μ coerente da DEV?
- **Estado:** fechado **NEGATIVO por três rotas independentes** (ver §3 do MAPA).
  A1 (sem modo Proca espontâneo), A5 (Anderson–Higgs obstruído pela não-localidade,
  m_A=0), V2 (o A_μ–θ da DEV é Stückelberg/corrente, F_μν=0 no regime galáctico).
- Consequência direta para o B9: **não há candidato genuíno** na TEIC ao A_μ coerente
  que forneceria o índice spacelike do fóton → a opção **B9-irmãos perde seu pilar**.
- Fonte: `dev_from_teic/A1_longitudinal_mode.py`; `a5/A5_synthesis.md`; `DEV/results/bridge/V2_coupling.md`.

### PC3 — X₀ = a₀²/2 (DEV) ↔ limiar/escala de grafo (TEIC)
- **Estado:** correlato **fraco e de sinal errado** (A2). `h_sat ∝ ρ_s^−0.48` (R²=0.90)
  — `h_sat` *decresce* com a rigidez, ao passo que a hipótese pedia `X₀∝+ρ_s(J−J_c)`.
  A constante pura de saturação X₀ é [DERIVADO] (π/ln2, 0.29%) mas a **escala física
  é UV (∝ρ), explicitamente não-a₀** (C3/CR3, identificação X₀↔a₀ **morta**).
- Fonte: `dev_from_teic/DEV_FROM_TEIC_synthesis.md:32,54-68`; `TEIC_DEV_CORRESPONDENCE.md:37`.

### PC4 — β (DEV) ↔ razão adimensional de grafo (TEIC, como η veio de Molloy–Reed)
- **Estado:** **48× fora** no ponto de operação físico; só casa em J_c (tuning crítico).
  Não há ponto de operação natural que entregue β.
- Fonte: `dev_from_teic/DEV_FROM_TEIC_synthesis.md:33,70-81`.

---

## 3. A discrepância do expoente, quantificada (o GATE do B9) — arquivo e linha

Este é o gate bloqueante. **Já está medido.** Os dois lados, exatos:

### Lado TEIC — magnon transverso é **quadrático ∝X** (ω=ck)
1. **Analítico** (C1, K1.1): em torno de ⟨n⃗⟩ o O(3) dá 2 Goldstones transversos com
   termo cinético **quadrático** `L = ½ρ_s(∂π)²` → ω=ck → ação ∝ X (n=1).
   `results/convergence/c1/C1_synthesis.md:21-22`.
2. **Numérico — dispersão:** o ajuste `ω* = ck` (c≈0.98) está em
   `results/gauge/e6/E6_2_dispersion.py:106-120` (gate H2 do fóton/E2).
3. **Numérico — susceptibilidade transversa (Ward):** `χ⊥ = ⟨m_par⟩/h ~ h^−0.98 ≈ h^−1`
   — o expoente do Goldstone (∝X). `C1_synthesis.md:46-48` (tabela K2).

### Lado DEV — phonon superfluido/deep-MOND é **X^(3/2)**
1. **Coeficiente DBI:** `F_XX = (1/X₀)/(1+(X/X₀)²)^(3/2)` —
   `DEV/paper_II/stability.py:76`; `DEV/paper_master/dev_master.tex:481`;
   `DEV/paper_IV/propagator_analysis.py:37-39`.
2. **Lei deep-MOND / Milgrom:** invariância de escala `g→√(g_N a₀)` força a forma única
   `L∝|∇Φ|³ ≡ X^(3/2)` (n=3/2), **fracionária, não-analítica**, posta por axioma
   (EoS superfluida P∝ρ³ em Khoury; DBI na DEV). `C1_synthesis.md:23-24,30-31`.
3. **Green deep-MOND:** `G(r)~r^−3/2` (e `G̃(p)~p^−3/2`) é a assinatura dessa não-analiticidade.
   `DEV/paper_IV/propagator_analysis.py:6,95`; `DEV/paper_master/dev_master.tex:633`.

### O que C1 já estabeleceu sobre a **transmutação** quadrático→X^(3/2)
- Integrar o modo longitudinal massivo gera **apenas correções analíticas** (X², derivadas
  superiores), **nunca X^(3/2)**. Um termo cinético de Goldstone livre/interagente **não é
  fracionário**. `C1_synthesis.md:23-24`.
- A não-analiticidade deep-MOND da TEIC **não está no termo cinético transverso** — está
  na **anomalia IR longitudinal** `χ∥~h^−0.37` (Brezin–Wallace), um **efeito de loop
  emergente**, não de árvore. `C1_synthesis.md:25-28,44-49`.

> **Implicação para o gate (desenvolvida na Fase 1):** o gate, como posto no prompt
> (magnon-quadrático → phonon-X^(3/2)), compara **setores diferentes**. O X^(3/2) já
> existe na TEIC — no setor **longitudinal**, internamente, sem meio. O magnon
> **transverso** é quadrático **por proteção de Goldstone** (propriedade fixa). O meio-DEV
> não tem onde inserir o expoente que falta, porque ele não falta.

---

## 4. O que a DEV TEM que a TEIC não tem (candidatos a "o que o meio fornece")

| Estrutura DEV | TEIC tem análogo? | Veredito |
|---|---|---|
| **Vácuo saturado** (axioma X₀ = a₀²/2) | saturação DBI existe, mas escala ∝ρ (UV), não a₀ | meio poderia fornecer a **escala a₀** — mas A2 mostra correlato de sinal errado |
| **a₀ embutido** (calibrado a SPARC) | não; correlato de grafo fraco | candidato #1 a "o que o meio fornece"; **escala externa dos dois lados** |
| **A_μ Proca massivo coerente** (m_A) | **não emerge** (A1+A5+V2) | candidato a fornecer índice spacelike do fóton — **morto como análogo** |
| **β** (parâmetro único calibrado) | razão ρ_s/K existe, 48× off | meio fornece β por calibração, não por derivação |
| **Axioma DBI** (forma fracionária X^(3/2) posta à mão) | a TEIC **deriva** a forma deep-MOND (não precisa do axioma) | aqui a TEIC **excede** a DEV — o meio não acrescenta |

**Conclusão da §4:** a única coisa genuína que o meio-DEV teria a fornecer é a **escala
absoluta** (a₀, β). Não fornece um expoente novo (a TEIC já tem a forma), nem um setor
vetorial (não há análogo). E a escala, B7 (campo-médio) + A2/A3 dizem ser inacessível
internamente e de correlato errado.

## 5. O que a TEIC TEM que a DEV não tem (candidatos a "o que o piano fornece")

| Estrutura TEIC | DEV tem? | Veredito |
|---|---|---|
| **Substrato microscópico** (causal set Poisson) | não (EFT contínua) | o piano fornece o "de onde vem" da EFT |
| **Forma da interpolação μ(x) derivada** | postula via axioma DBI | a TEIC fornece a **forma**; convergem no limite (C1) |
| **Razões de Stückelberg travadas (1,2)** | trata K como livre | predição da TEIC ausente na DEV |
| **Setor de matéria SU(2)/SU(3)** (Skyrmion=bárion, octeto de mésons) | a DEV não tem matéria | a TEIC excede largamente |
| **Números puros calculáveis** (15/8π², π/ln2, 3/320π²) | calibração externa | o piano fornece os adimensionais |
| **A anomalia χ∥ emergente** (deep-MOND como efeito IR, não axioma) | posto por axioma | a TEIC **deriva** o que a DEV postula |

---

## 6. Guarda anti-circularidade — cobertura sobre código que cruza TEIC↔DEV

- **O que a guarda cobre hoje** (`tests/test_no_circularity.py:54-55`): `SCAN_DIRS =
  {src, experiments, results, docs/campaigns}` — **toda a árvore TEIC**, incluindo
  `results/dev_from_teic/` e `results/bridge/` (lado TEIC). A1/A5 confirmam que a guarda
  foi estendida e **PASSA** sobre essas campanhas.
- **Lacuna identificada:** a guarda **não varre `DEV/`** (repositório separado,
  `DEV/dev_pipeline/.git`). Se um gerador do B9 viver sob `DEV/` ou **importar** um módulo
  gerador da DEV, a guarda TEIC **não o vê**. Os docs `DEV/results/bridge/V*.md` que li
  são markdown (não geradores), então a lacuna é potencial, não atual.
- **Recomendação (vinculante para qualquer ficha B9):** manter **todo gerador B9 sob
  `TEIC/results/b9/`** (já varrido) e usar números DEV (a₀, β, m_A, X₀) **somente em blocos
  `# COMPARISON ONLY`** — exatamente o padrão de A1–A5. Se algum gerador precisar importar
  um módulo DEV, estender `SCAN_DIRS` para incluir `DEV/` **antes** de rodar. Sem a₀/G/ℏ em
  nenhum gerador.

---

## 7. Síntese da Fase 0 (entrada para o MAPA)

1. O **gate do expoente já está medido** (C1): magnon transverso ∝X (Goldstone),
   phonon DEV X^(3/2) (axioma), forma deep-MOND compartilhada **no limite** via Milgrom,
   localizada na TEIC na **anomalia longitudinal χ∥**, não no termo de árvore.
2. O **setor vetorial** (pilar da opção irmãos) está **triplamente morto** (A1+A5+V2).
3. Os candidatos a **escala** (a₀, β) são **externos dos dois lados**, com correlato de
   grafo **fraco/sinal-errado** (A2) ou **48× off** (A3); B7 diz que o substrato é
   campo-médio (sem transmutação).
4. A guarda cobre o lado TEIC; o lado DEV exige a disciplina COMPARISON-ONLY.

→ Tudo aponta para o veredito do mapa **antes** de qualquer CPU. Ver `MAPA_ACOPLAMENTO_B9.md`.

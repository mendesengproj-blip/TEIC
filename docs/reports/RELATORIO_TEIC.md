# RELATÓRIO COMPLETO — TEIC (Teoria da Expansão Informacional Causal)
### Do início ao fim: o que foi testado, o que ficou provado, e onde a teoria para

> Síntese de toda a investigação: fundação geométrica, fronteira quântica, ponte
> gravitacional e as três camadas de matéria. Cada veredito abaixo é o *medido*,
> incluindo os critérios de morte. Disciplina anti-circularidade
> (`tests/test_no_circularity.py`) passa em todas as campanhas.

---

## 0. O que é a TEIC

A realidade fundamental é uma **rede discreta de eventos ligados por causalidade**. Não há
espaço-tempo de fundo: espaço, tempo, dilatação e gravitação **emergem** da estrutura
causal. Cada evento é um centro local de expansão; não há centro privilegiado.

O objeto central é o **tempo próprio entre dois eventos A→B**, definido de duas formas que
a teoria compara:

- **Cadeia** (clássica): comprimento da maior cadeia causal de A a B.
- **Volume** (do autor): τ = (k_d · N / ρ)^(1/d), com N = nº de eventos no intervalo de
  Alexandrov (futuro de A ∩ passado de B).

**Contexto honesto, declarado desde o charter:** nos regimes testados a TEIC coincide com a
**Causal Set Theory** (Bombelli–Lee–Meyer–Sorkin 1987; Myrheim; Meyer; Sorkin). Muito
provavelmente é uma redescoberta independente. O projeto **testa** a teoria — não a confirma.

---

## 1. A regra que define o projeto: anti-circularidade

O erro original da investigação foi **inserir o fator de Lorentz `γ` no código que gera os
dados e depois "observá-lo"** — circularidade pura. Toda a metodologia foi reconstruída em
torno de uma regra inegociável:

> Nenhuma fórmula relativística (γ, √(1−β²), √(1−2M/r)), nenhum número complexo, nenhum
> `mc²`, `E=ma`, Klein–Gordon, Dirac pode aparecer no **gerador** de dados. Esses conceitos
> só vivem em blocos rotulados `COMPARISON ONLY` ou em `validation.py`.

Isto é imposto mecanicamente por `tests/test_no_circularity.py`, que tokeniza cada gerador e
falha se uma fórmula proibida aparecer em código executável. **A dilatação tem de *emergir*
da contagem.** Esse guard passou em **todas** as campanhas, do início ao fim.

Esquema de vereditos usado em todo o projeto: **PROVADO** / **A** (derivado e verificado) /
**B** (real mas herdado/parcial) / **C** (argumento ou medido-negativo) / **D** (refutação /
reinterpretação). *O critério de morte vale tanto quanto o de sucesso.*

---

## 2. CAMADA 1 — Geometria: espaço-tempo, relatividade e gravitação **(o núcleo PROVADO)**

| Resultado | O quê | Veredito |
|---|---|---|
| **R1** | Dilatação SR `√(1−β²)` de uma rede Poisson aleatória | **PROVADO** — corr 0.9998 (cadeia)/1.0000 (volume); a grade regular **falha** (CV 17% vs 0.8%) — o contraste é o ponto: Lorentz exige aleatoriedade Poisson |
| **R2** | Lei de volume causal + dimensão | **PROVADO** — Vol₂=½τ², Vol₄=πτ⁴/24; dimensão medida d=2.006 e 4.004 |
| **R3** | Schwarzschild `√(1−2M/r)` por contagem **não-circular** | **PROVADO** — corr 1.0000, erro máx 0.21% |
| **Tarefa A** | Expansão analítica de curvatura | Vol=½τ²[1−Rτ²/48+…] — o **escalar de Ricci** |
| **Tarefa B** | Cadeia vs volume em dS/AdS (numérico) | **PROVADO (divergência)** — separação de **23.5σ** |

**A pergunta que decide (§4 do charter):** as duas formulações de tempo próprio divergem em
espaço-tempo curvo? **Sim** — divergem na ordem `Rτ²`: o estimador de **volume** codifica a
curvatura de bulk (coef −1/96), o de **cadeia** segue a geodésica (coef ≈ 0). Essa
divergência é o mecanismo pelo qual um conjunto causal codifica o escalar de Ricci.

**Significado honesto:** a divergência é real e reprodutível, mas **não é nova** — é uma
redescoberta fiel da Causal Set Theory (Benincasa–Dowker; Roy–Sinha–Surya). No estado atual,
o conteúdo *testável* da TEIC coincide com CST; o que é, no máximo, distintivo é a **rota
conceitual** (expansões locais superpostas vs. ordem parcial abstrata).

---

## 3. CAMADA 2 — A fronteira com a Mecânica Quântica (e6–e11): mapeada, não cruzada

Uma sonda isolada (não alimenta nada acima) sobre se a **interferência quântica** emerge da
contagem causal:

- **e6** — contagem real pura **não** cancela (sem franjas escuras), mas a geometria da
  dupla-fenda `ΔL(x)` está **correta** (inclinação 0.634 vs 0.629 geométrico). Faltam
  exatamente **dois** ingredientes: um sinal oscilante (análogo do `i`/cos) e uma escala `k`
  (passos→ângulo).
- **e10** — o **d'Alembertiano causal de Sorkin** (Benincasa–Dowker) **deriva** o ingrediente
  (i): um peso que **alterna de sinal** por construção. Reproduz resultado conhecido, não
  descoberta.
- **e11** — a escala `k` **não emerge** da geometria: é **externa** (`k = m/ℏ`, propriedade da
  matéria que propaga, não da rede).

**Resultado: a fronteira TEIC↔QM está completamente mapeada — *forma derivada, escala
externa*.** Isso motiva a figura de **dois andares**: a geometria embaixo; `ℏ, m, e` acima.
A TEIC não deriva a Mecânica Quântica; deriva a moldura geométrica sobre a qual ela age.

*(Sondas exploratórias relacionadas, isoladas: e7 dinâmica de crescimento — família
Rideout–Sorkin re-coordenatizada; e8 redshift causal — aplicação da escala de R2.)*

---

## 4. A PONTE — TEIC ↔ gravitação (do cinemático ao dinâmico)

Investigação independente (fora do paper), perguntando se a densidade causal ρ(r) ao redor
de uma massa pode ser *derivada*.

| Campanha | O quê | Veredito |
|---|---|---|
| **BRIDGE_RHO** (P1–P3) | ρ(r) ao redor de massa | P1 **CIRCULAR**; P2 **PASSA** (cinemático): ρ_eff=ρ₀/√(1−2M/r), corr 1.00000; P3 confirma mas **impõe** o perfil |
| **BRIDGE_DYNAMICS** (D1–D3) | a ação de Benincasa–Dowker com fonte | **PASSA** — `Bθ=J → □θ=4πG T/c⁴`; massa pontual → `θ=GM/rc²`; o perfil **1/r emerge** do Monte-Carlo sem ansatz (expoente −1.02) |
| **BRIDGE_NONLINEAR** (NL1–3) | a segunda ordem de Schwarzschild | NL1 **λ LIVRE** (a ação BD é quadrática); NL2/NL3 **PASSA cinematicamente**: a densidade converge para `ρ₀/√(1−2u)` a **0.06%** — mas pelo *relógio* de tempo próprio, não por uma ação não-linear derivada |

**O que a ponte estabelece:** o escalar da gravitação modificada **é** o contraste
fracionário de densidade causal `θ = δρ_eff/ρ₀ = GM/rc²` — agora **derivado dinamicamente em
primeira ordem** da ação BD, e **cinematicamente convergente a todas as ordens** de
Schwarzschild (regime sub-horizonte).

**Fronteira honesta, localizada:** (1) a dimensão `d=3` é *entrada* geométrica (o 1+1D
literal prefere um perfil blindado, não 1/r); (2) a não-linearidade genuína (a back-reação
`−½Rφ`, o setor Einstein/Regge) **não** está na ação como usada; (3) o horizonte (`r→2M`)
fica explicitamente em aberto. O **vetor**-bridge para uma teoria escalar-vetor-tensor
específica deu **resultado negativo** (acoplamento Stückelberg, não dilatônico) — registrado
honestamente.

---

## 5. CAMADA 3 — Matéria: mais que geometria, muito menos que o Modelo Padrão

A matéria estava originalmente *fora de escopo*. Uma auditoria (INV1–INV6) mostrou que os
experimentos de matéria herdados (T14–T21) eram **tautológicos/circulares**, e tudo foi
**refeito do zero** com a disciplina anti-circularidade. Esta camada é a maior, e o resultado
é uma **fronteira nítida**.

### 5a. A geometria da matéria (M1–P4): o escalar livre é um campo clássico sem massa

| Afirmação | Grade | Evidência |
|---|:--:|---|
| Massa inercial emerge | **C** | M1: `m=F/a` não recuperável — não há partícula para acelerar |
| Proxy de massa é Lorentz-invariante | **B** | M2: invariante (CV 1.5% Poisson) — mas herdado de R1 |
| Energia emerge | **D** | E1: `E=mγ` a 0.4% — mas γ *é* a contagem de R1 (reinterpretação) |
| Estado localizado estável | **C** | P1: um lump deslocaliza (σ~t^0.76) — sem repouso estável |
| Dispersão ω²=k²+m² | **C** | P2: sinal soterrado sob variância BD |
| **Spin-½** | **C** | P3: rotação 2π → +estado (sem dupla-cobertura espinorial) |
| Interferência quântica | **C** | P4: superposição linear (resíduo 1e-15); sem `|ψ|²` |

> **Nenhuma afirmação de matéria atinge A.** O setor escalar livre comporta-se como um
> **campo real clássico sem massa**: deslocaliza balisticamente, superpõe linearmente,
> carrega só estrutura angular inteira. Massa inercial, espectro de partículas, spin-½ e
> amplitudes quânticas exigem estrutura **ausente** do escalar θ sobre um conjunto causal.

### 5b. Massa como complexidade & criação por colisão

- **MATTER_COMPLEXITY (CC1–6):** construindo objetos com complexidade topológica controlada
  (Betti=N), o custo de deslocamento `τ(N)∝N` é Lorentz-invariante e fecha até
  `E²=(pc)²+(mc²)²` **(B)** — mas o núcleo é **definitional** (a relação é construída, não
  emergente); falta uma escala de massa física.
- **MATTER_CREATION (CR1–6):** duas cadeias de alta densidade colidem — criam loops? **Não há
  limiar ρ\* (D)**. A ação BD é **linear** (`□θ=J`): o resíduo de superposição é ~0 em toda
  densidade; as cadeias **atravessam-se**. *Conservação e ausência-de-criação são o mesmo
  fato (linearidade).* **Localização:** criar matéria exige **não-linearidade** além de
  `□θ=J` — o setor interagente da QFT.

### 5c. A escada da teoria de campo: rumo a uma partícula estável

Aqui a ação mínima ganha o setor de gauge compacto e o termo de Wilson:
`S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]`. Cada campanha localiza o gargalo seguinte:

```
CR_DBI         → EOM do cosseno = sine-Gordon; θ não tem winding;
                 o setor de GAUGE tem kink estável (massa = 8)
CR_GAUGE       → Stückelberg transfere até 57% θ→φ; kink isolado estável,
                 par transiente (virtual); colisão NÃO cria estável (cenário 2+3)
CR_WILSON (2D) → [D] suporta matéria (m=8, 5 consistências) mas não cria/confina:
                 U(1) 2D não tem monopólos; fluxo 2π invisível ao cos de Wilson
CR_3D (3+1D)   → [B] monopólos + plasma + corda E(d)∝d PRESENTES; a colisão CRIA
                 estrutura semi-estável; objeto suportado = VÓRTICE (S¹),
                 relativístico, gravita (4/5 consistências); núcleo DIFUNDE
CR_HIGGS       → [C] o escalar θ condensa (⟨θ⟩=v ✓) mas é uma FASE, não magnitude;
                 não pina o núcleo. Falta |Φ|²|D_μΦ|²
CR_ABELIAN_HIGGS → [A] o campo complexo Φ pina o núcleo: 5/5 consistências fecham —
                 MAS Φ é um QUARTO INGREDIENTE adicionado à ação (A honesto)
```

As **cinco consistências** da matéria (massa=8, E²=(pc)²+(mc²)², θ~M/r, isotropia, núcleo
pinado) fecham **com o campo complexo adicionado**. O setor que é *derivado* — geometria, SR,
Schwarzschild, gravitação newtoniana — é sólido; **matéria estável exige o campo complexo
como ingrediente extra**, reportado com honestidade.

### 5d. PHI_EMERGE (V1–V4): o quarto ingrediente é eliminável?

A pergunta mais aguda: o campo complexo `Φ = ρ·e^{iφ̄}` era física nova, ou uma **composição**
de campos que a rede já tem (`|Φ|=ρ` densidade causal, `arg Φ=φ̄` fase de gauge)?

```
PHI_EMERGE    [C] — a composição reproduz a FASE (massa de gauge m_A∝√ρ) mas
                    NÃO a MAGNITUDE: |Φ|=ρ_Poisson é substrato estático, não dipa no núcleo
PHI_EMERGE_V2 [B] — com ρ DINÂMICO (o ρ de D1–D3) inicializado, a magnitude FECHA:
                    |Φ|(0)→0, núcleo pinado σ_core=3.73 — condicionado a ρ dinâmico + K suave
PHI_EMERGE_V3 [B] — com ρ dinâmico ESPONTÂNEO (de ρ uniforme, □ρ=J): o dip EMERGE rápido
                    (τ_dip≈2.3 < τ_vortex≈3.9), atinge o equilíbrio de V2, 5/5 consistências;
                    K_c≈8.5 mapeado (indep. de ρ). Resíduo: o enrolamento de gauge
PHI_EMERGE_V4 [B] — com ρ de DUAS VIAS (ρ realimenta a ação de gauge): a depleção NÃO pina
                    o enrolamento. Mecanismo MEDIDO: ρ acopla só por cossenos [1−cos],
                    cegos ao fluxo 2π (cos 2π=1) — ponderar um termo cego o mantém cego.
                    Resíduo IRREDUTÍVEL; o quarto ingrediente (magnitude/não-Abeliano) é necessário
```

**O que PHI_EMERGE concluiu:** a **magnitude** de Higgs `|Φ|=ρ` **emerge** da densidade causal
dinâmica (a mesma de D1–D3), sem axioma extra — fechando a metade da composição que faltava.
Mas a **estabilização topológica do enrolamento** exige um custo de núcleo não-cosseno que a
ação mínima não tem e que ρ **não pode** suprir. O quarto ingrediente é **reduzido** (a
magnitude emergiu), **não eliminado** (o enrolamento permanece).

---

## 6. A FIGURA GERAL — o que a TEIC deriva, e onde para

```
┌────────────────────────────────────────────────────────────────────┐
│ DERIVADO E VERIFICADO (PROVADO / A)                                 │
│  • Espaço-tempo, relatividade especial √(1−β²)         [R1]          │
│  • Lei de volume causal + dimensão                     [R2]          │
│  • Schwarzschild √(1−2M/r) não-circular                [R3]          │
│  • Curvatura = escalar de Ricci (cadeia vs volume)     [§4, 23.5σ]   │
│  • Gravitação newtoniana GM/r da ação BD (1ª ordem)    [D1–D3]       │
│  • Convergência cinemática a Schwarzschild (todas ord.)[NL2–3]       │
├────────────────────────────────────────────────────────────────────┤
│ FRONTEIRA MAPEADA (a "moldura" emerge, o conteúdo é externo)         │
│  • Interferência: FORMA derivada, ESCALA k externa     [e6–e11]      │
│    → dois andares: geometria abaixo; ℏ, m, e acima                   │
├────────────────────────────────────────────────────────────────────┤
│ MATÉRIA — mais que geometria, muito menos que o Modelo Padrão        │
│  • Escalar livre = campo clássico SEM massa            [M1–P4: C/D]  │
│  • Criação por colisão: nenhuma (ação BD linear)       [CR: D]       │
│  • Defeito topológico (vórtice S¹) relativístico,                    │
│    gravitante, com MAGNITUDE de Higgs emergente        [3D, PHI V2–3]│
│  • Estabilização do enrolamento: IRREDUTÍVEL por ρ     [PHI V4: B]   │
│    → exige magnitude complexa (|Φ|→0) ou não-Abeliano                │
└────────────────────────────────────────────────────────────────────┘
```

**A estrutura recorrente — e a descoberta mais profunda:** toda fronteira de matéria
localiza-se no **mesmo lugar**. A criação precisa do setor **não-linear/interagente**; a
estabilização do núcleo precisa da **magnitude/Higgs**; o próton e o spin-½ precisam de
**conteúdo não-Abeliano**. E V4 mostrou *por que* — pelo teorema de **Derrick**: defeitos
topológicos precisam de uma **escala que fixe seu tamanho**, e ρ (que só reescala termos de
cosseno) não pode fornecê-la.

> **A TEIC mínima é uma teoria de espaço-tempo e gravitação *emergentes*, completa nesse
> setor. A matéria não é de graça: ela entra por um único ingrediente bem-caracterizado (um
> custo de núcleo não-cosseno).** A teoria não substitui o Modelo Padrão — ela **aponta para**
> a estrutura dele (Higgs, grupo não-Abeliano), localizando com precisão cirúrgica onde a
> geometria pura termina.

---

## 7. Sobre partículas, antipartículas e spin (interpretação)

Os **vórtices/anti-vórtices** que aparecem nas colisões são uma realização estrutural
legítima — porém **bosônica e abeliana** — da relação partícula/antipartícula: carga
topológica conservada (winding ∈ ℤ = π₁(U(1))), oposta para o anti-vórtice, e **aniquilação
de pares com radiação** (vista em CR_ABELIAN_HIGGS/AH6). É análogo a um bóson carregado e sua
antipartícula (quantum de fluxo), **não** a um elétron; e em 3+1D o objeto é uma **linha de
fluxo** (corda), não um ponto.

**Spin-½ não** vem do vórtice abeliano (é bóson: 2π → +1). Férmions exigiriam ou um
**Skyrmion + termo de Wess–Zumino** (a rota do próton, não-Abeliano, π₃) ou um composto
**carga–monopolo** (Jackiw–Rebbi). A campanha já localizou (T3D5/6) que o hedgehog/Skyrmion
está **fora do alcance da ação abeliana** — exige conteúdo não-Abeliano. Logo **matéria
estável e spin-½ apontam para o mesmo ingrediente ausente.**

---

## 8. Status e próximos passos

**Status atual:** paper fundacional completo e reprodutível (R1–R3 + §4 + Open Questions com
e6–e11 e a ponte). As extensões (ponte dinâmica, matéria, PHI_EMERGE) são investigações
independentes, todas commitadas, todas passando no guard, nenhuma modificando as anteriores.

**A rota natural seguinte:** estender a rede para um campo de gauge **não-Abeliano (SU(2))** e
testar, com a mesma disciplina, se aparecem (a) o hedgehog/Skyrmion (S²/π₃), (b) sua
estabilidade tipo-Derrick (o custo de núcleo que falta), e (c) a quantização como **spin-½**
via termo de Wess–Zumino. Matéria estável e spin-½ apontam para o **mesmo** ingrediente
ausente — seria o teste decisivo de ambos.

**O caráter da investigação inteira:** disciplina anti-circularidade absoluta; resultado
negativo reportado como negativo; cada fronteira *localizada*, não escondida. O que é derivado
é sólido e publicável; o que não é, está mapeado com a precisão máxima.

---

## Apêndice — Índice de campanhas e documentos

| Camada | Documento raiz | Resultados |
|---|---|---|
| Fundação | `README.md`, `paper/main.tex` | R1–R3, §4, e6–e11 |
| Ponte (densidade) | `BRIDGE_RHO.md` | `results/bridge/rho/` (P1–P3) |
| Ponte (dinâmica) | `BRIDGE_DYNAMICS.md` | `results/bridge/dynamics/` (D1–D3) |
| Ponte (não-linear) | `BRIDGE_NONLINEAR.md` | `results/bridge/nonlinear/` (NL1–3) |
| Ponte (sub-peças) | `BRIDGE_COEFFICIENTS.md`, `BRIDGE_WILSON.md`, `BRIDGE_BD.md`, `BRIDGE_D3_AUDIT.md` | `results/bridge/` |
| Matéria (geometria) | `MATTER_EXPERIMENTS.md` | `results/matter/` (M1–P4, S1) |
| Matéria (complexidade) | `MATTER_COMPLEXITY.md` | `results/matter/complexity/` (CC1–6) |
| Matéria (criação) | `MATTER_CREATION.md` | `results/matter/creation/` (CR1–6) |
| Matéria (campo) | `MATTER_CR_DBI.md`, `MATTER_CR_GAUGE.md`, `MATTER_CR_WILSON.md`, `MATTER_CR_3D.md`, `MATTER_CR_HIGGS.md`, `MATTER_CR_ABELIAN_HIGGS.md` | `results/matter/cr_*/` |
| Higgs emergente | `PHI_EMERGE.md`, `PHI_EMERGE_V2.md`, `PHI_EMERGE_V3.md`, `PHI_EMERGE_V4.md` | `results/phi_emerge/` (PE, v2, v3, v4) |
| Auditorias | `AUDIT_T14_T21.md`, `AUDIT_BRIDGE.md`, `AUDIT_GEMINI.md` | — |

Reprodução: cada experimento fixa semente e escreve JSON/`.meta.json` auto-descritivo.
`python tests/test_no_circularity.py` deve sair 0 (guard limpo).

# PAPER_FERROMAGNETO_GAPS — por que a Fase 1 parou antes de escrever

> Resultado da Fase 1 do charter PAPER_FERROMAGNETO. A avaliação foi feita **antes** de
> escrever qualquer linha do paper, lendo RESEARCH_MAP.md, as sínteses dos quatro domínios
> (D3/R3/MG1; MATTER_SU2/BQ/FL1/OS; FM2-1/C1/FM4/LD; COLAPSO_SR_TEIC/FS1/FS2),
> DEV_FROM_TEIC/A1–A5 e PAPER_DIAGNOSTICO.md.
>
> **Veredito: SUPORTA PARCIALMENTE, com exceções ESTRUTURAIS → paper NÃO escrito.**
> O padrão empírico (forma deriva, escala fica externa) é real e forte nos 4 domínios.
> Mas a **afirmação central como escrita** contém uma razão causal falsa, um objeto
> unificador que não cobre 1 dos 4 domínios, e um elo [FRACO] — então o problema é de
> **afirmação (precisa reformular)**, não (principalmente) de dados. Charter manda parar.

---

## 1. O que EXATAMENTE não suporta a afirmação central

A afirmação tem quatro componentes. Avaliação de cada uma contra os dados:

| Componente da afirmação | Status | Evidência |
|---|---|---|
| (a) "forma/razão adimensional deriva" | **SUPORTA** (cosmologia parcial) | geometria −0.992; matéria c=√(2/3), [4,16,36]; cosmologia ν=−0.37 [FRACO]; colapso GOE/Δx² |
| (b) "escala absoluta dimensional fica de fora" | **SUPORTA** | G∝1/K; f_π externo; a₀ [EXTERNO-B]; η MORTE |
| (c) "tudo emerge **desse ferromagneto**" | **NÃO SUPORTA** (1/4 domínios) | colapso emerge da **rede causal nua**, sem ferromagneto |
| (d) "razão: substrato adimensional **não pode** gerar escala" | **NÃO SUPORTA** | h_sat É escala interna; QCD transmuta ΛQCD |

As componentes (a) e (b) — o **padrão empírico** — passam. As componentes (c) e (d) — o
**objeto unificador** e a **razão causal** — falham. Como (c) e (d) são o coração da tese
(o título proposto é "...absolute scales do not", e §4 do charter quer asseverar (d)
explicitamente), a falha é estrutural.

### Exceção estrutural 1 — a razão causal está errada (a mais grave)

A afirmação: *"um substrato adimensional NÃO PODE gerar escalas dimensionais absolutas."*

Os dados contradizem em dois pontos independentes:

- **O substrato GERA escalas internas.** `DEV_FROM_TEIC` A2: o joelho de resposta
  h_sat *"is a genuine internal network scale"*, com `h_sat∝ρ_s^{−0.48}` (R²=0.90). A
  rigidez ρ_s varia 0.25→1.16; σ (tensão de corda) 1.35→0.33; M_Skyrmion≈146–207;
  λ_Sk=a/√120 — **todas dimensionais em unidades de rede**. O substrato não é incapaz de
  escala; ele produz escalas medidas em unidades de rede. O que está ausente é a **única
  conversão rede→SI** (o "lattice→GeV unit map", declarado externo em C1/D3D).
- **O contraexemplo é a própria analogia do charter.** O §4 proposto cita ΛQCD como
  "precedente" de "formas derivadas, escala precisa de renormalização." Mas ΛQCD **emerge
  por transmutação dimensional** de um acoplamento adimensional — é exatamente um caso em
  que *"um substrato adimensional GERA uma escala."* A analogia **refuta** a razão (d) em
  vez de sustentá-la. (O que QCD ainda precisa de fora é **um** input experimental que fixa
  a unidade física — que é a posição honesta da TEIC também.)

→ A razão honesta não é "não pode gerar escala", e sim: *"a rede gera estrutura
adimensional e escalas internas em unidades de rede, mas não exibe um mecanismo que fixe a
conversão rede→física; logo toda escala física absoluta precisa de exatamente uma
calibração externa."* Isto é uma afirmação **diferente** — mais fraca e mais precisa.

### Exceção estrutural 2 — "ferromagneto" não cobre o domínio de colapso

A afirmação diz que *toda* a estrutura emerge *"desse ferromagneto"*. Mas a campanha
COLAPSO_SR_TEIC opera sobre a **rede causal de Poisson nua** e seus operadores espectrais
(adjacência, Laplaciano, d'Alembertiano BD via `tier3_core`/`c5_core`), com **zero
dinâmica de ferromagneto** — o próprio RESEARCH_MAP da campanha: *"nenhuma dinâmica causal
nova; zero η, zero poda"*, camada nova = só parâmetros de ordem espectrais. χ_eff, GOE e
Δx² são propriedades do **espectro do conjunto causal**, não do vácuo orientacional
ordenado. → "ferromagneto" é o substantivo errado para unificar os 4 domínios; o objeto
comum é o **substrato causal de Poisson**, do qual o ferromagneto é *uma* estrutura (vácuo/
matéria/cosmologia) e o colapso usa *outra* (o espectro nu).

### Exceção estrutural 3 — o padrão é em parte artefato do guard

O guard anti-circularidade **proíbe** inserir qualquer escala (γ, c, G, dilatação) no
gerador. Logo, por construção, **só estrutura adimensional PODE emergir**. "As escalas
ficam externas" é então em parte uma consequência do **método**, não só do substrato. Isto
não torna o padrão falso (ele é verificável em cada domínio), mas impede afirmar a razão
(d) como uma *lei da natureza descoberta* — ela é, em parte, a *sombra da disciplina
metodológica*. (Já registrado em PAPER_DIAGNOSTICO.md, Q2/Q3.)

### Exceção (de dados, não estrutural) 4 — a cosmologia é o elo [FRACO]

O único elo *físico* vácuo→galáxias (FM2-1/C1) mede ν_MOND `χ∥~h^{−0.37}` (FM2-1:
−0.4±0.1; ideal −0.5), com finite-size *"pushing the exponent toward 0"* e R²/amostragem
"marginal"; e o magnon é ∝X **não** X^{3/2} (a afirmação solta "magnon = fônon de Khoury"
foi **morta** por C1). A equivalência deep-MOND é "no limite" (teorema de Milgrom), não na
forma medida diretamente. → o domínio cosmológico **suporta (b)** (a₀ externo) mas a forma
de **(a)** é [FRACO], não [SÓLIDO]. Esta é a única exceção que é *de dados*.

---

## 2. O que seria necessário para suportar (a afirmação ORIGINAL)

Sem sugerir campanhas — apenas identificando o que mudaria o veredito:

1. **Para a razão (d) ser verdadeira:** seria preciso mostrar que a rede *não pode nem
   mesmo internamente* gerar uma escala — o que é **falso** (h_sat). A razão original é
   irrecuperável; ela tem de ser **substituída** (ver §4), não preenchida com mais dados.
2. **Para (c) ser verdadeira:** seria preciso que o domínio de colapso emergisse do
   ferromagneto ordenado, e não do espectro nu — o que **não é o que a campanha fez**.
   Irrecuperável sem refazer a campanha sobre o vácuo ordenado (e não há razão física para
   esperar que mude o resultado). A reformulação ("substrato causal", não "ferromagneto")
   resolve sem dado novo.
3. **Para (a) ser [SÓLIDO] na cosmologia:** o expoente ν precisaria ser pinado em −0.5 com
   tamanho finito controlado — hoje é [FRACO]. Esta é a única lacuna genuinamente de dados.

---

## 3. O problema é de DADOS ou de AFIRMAÇÃO?

**Predominantemente de AFIRMAÇÃO (precisa reformular).** Três das quatro exceções (1, 2, 3)
são sobre o que a afirmação *diz* — a razão causal, o objeto unificador, e o status
metodológico — e nenhuma se resolve com mais simulação; resolvem-se **enunciando uma
afirmação diferente e mais precisa**. Apenas a exceção 4 (cosmologia [FRACO]) é de dados, e
ela sozinha não bloquearia um paper (seria uma ressalva declarada). O bloqueio vem de 1+2+3.

Pela regra do charter: *"Se o problema é de afirmação (a afirmação precisa ser reformulada)
→ produzir GAPS, não escrever o paper."* → é exatamente este caso.

---

## 4. A afirmação REFORMULADA que os dados suportariam (caminho construtivo)

Os dados **suportam** um paper mais modesto e mais preciso — se a tese for reescrita assim:

> *"Sob uma disciplina anti-circularidade que proíbe inserir escalas no gerador, um único
> **substrato causal de Poisson** produz, em quatro domínios independentes (geometria,
> matéria, cosmologia, e — não-planejadamente — colapso quântico), a **estrutura
> adimensional** da física (formas funcionais, razões, expoentes, fatos topológicos),
> enquanto **toda escala física absoluta requer exatamente uma calibração externa** (o mapa
> rede→SI nunca é fixado). O padrão não é que o substrato 'não possa gerar escala' — ele
> gera escalas internas em unidades de rede (ρ_s, σ, h_sat, M_Skyrmion) — mas que nenhum
> mecanismo de transmutação dimensional foi exibido para convertê-las em unidades físicas,
> a mesma posição em que a QCD de rede se encontra antes de um input experimental."*

O que esse paper reformulado **poderia** afirmar honestamente (e só isso):
- O padrão empírico forma-deriva / escala-externa, com a evidência numérica de cada domínio.
- "Substrato causal" (não "ferromagneto") como objeto unificador; o ferromagneto como *uma*
  das estruturas (3 dos 4 domínios), o colapso como o espectro nu.
- O colapso como **convergência não-planejada** (padrão SR↔TEIC), explicitamente **não**
  como derivação (formas emergem por razão genérica-Laplaciana; η morre; CP exige
  continuação Euclidiana = escolha).
- A QCD como **precedente correto**: estrutura adimensional derivada, uma unidade física
  externa — **incluindo** o reconhecimento de que QCD *transmuta* uma escala, que a TEIC
  ainda **não** faz (a diferença honesta, não varrida para baixo do tapete).
- A fronteira declarada com o mesmo destaque que os positivos: o elo cosmológico é [FRACO];
  o padrão é em parte sombra do guard; as escalas externas são **separadamente** externas
  (a tentativa de uni-las morreu — CONVERGENCE, G-de-r_proton 108 ordens).

E o que esse paper **continuaria sem poder** afirmar: que os domínios estão *fisicamente
unificados* além de partilharem substrato e método (não há lei cross-setor derivada; as
escalas são separadamente externas).

---

## 5. Recomendação

**Não escrever o PAPER_FERROMAGNETO como afirmado.** A afirmação central, na forma do
charter, asseveraria (c) e (d), que os dados contradizem. Há dois caminhos honestos, à
escolha do autor:

- **(i) Reformular** a tese para a versão de §4 acima (substrato causal, não ferromagneto;
  "uma calibração externa", não "não pode gerar escala"; colapso = convergência) e então a
  Fase 2 seria viável — mas seria um paper **diferente** do charter, e em grande medida já é
  o conteúdo do umbrella `TEIC_MASTER` (e PAPER_DIAGNOSTICO já registrou que o enquadramento
  abrangente foi *removido* das submissões por risco de desk-reject, `PUBLICATION_REVIEW.md`).
- **(ii) Não escrever** e manter o padrão forma/escala como o que ele é: a leitura
  transversal honesta do programa (RESEARCH_MAP §7, PROGRAM_AUDIT §2), já documentada, sem
  um veículo de submissão próprio que precise asseverar uma razão estrutural que não se
  sustenta.

Aguardo decisão do autor. Não escrevi o paper e não alterei nenhum resultado.

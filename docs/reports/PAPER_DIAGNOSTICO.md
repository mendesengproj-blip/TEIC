# PAPER_DIAGNOSTICO — avaliação independente do que temos

> Tarefa de leitura e avaliação, não de escrita. Li os cinco papers de submissão
> completos (`paper/submission/{goldstone_prd, matter_gravity_prd, photon_arc_cqg,
> su3_prd, btfr_mnras}`), o `RESEARCH_MAP.md`, o `PROGRAM_AUDIT.md` e as sínteses de
> campanha (E1/E2/E4, FL1/FLR/OS/BQ, FM2-1/C1, D3/R3/MG1, FM4/LD, DEV_FROM_TEIC/A1–A5,
> COLAPSO_SR_TEIC/FS1/FS2, FRONTEIRA_SETA_COSMOLÓGICA). Abaixo respondo as três
> perguntas com a evidência específica de onde, nos dados, cada afirmação se apoia.
> **Não escrevo nenhum paper e não sugiro campanhas.** Onde não há conexão, digo que
> não há.

Os cinco papers, em uma linha cada (do que cada um LITERALMENTE estabelece):

| Paper | Venue | Estabelece | Escopo declarado |
|---|---|---|---|
| **Goldstone** | PRD | ferromagneto de orientação O(3) ordena (FSS genuíno); operador causal dá ω=ck; os 2 Goldstones transversos são **escalares internos, não fóton** (p=0.23, retratação) | vácuo + modos de Goldstone |
| **Matter-Gravity** | PRD | Newton 1/r (Poisson, Schwarzschild 0.2%); SU(2) forçado por topologia; Skyrme externo por teorema; Skyrmion B=1 spin-½ = bárion (adimensional, e=5.39); **o sóliton sourceia seu próprio campo** θ=G_net M/r | SU(2) matéria + gravidade |
| **Photon-Arc** | CQG | mapa negativo: o fóton não emerge — E4 (escalar), E5/E7+A5 (não-localidade), operador E²−B² (diamantes 100% elétricos), curvatura só Planckiana | a fronteira do fóton |
| **SU3** | PRD | ferromagneto de cor; confinamento V~σr; octeto de 8 Goldstones degenerado; ordem da transição (1ª fraca) | setor de cor SU(3) |
| **BTFR** | MNRAS | teste **framework-independente** de a₀∝H(z); MUSE-DARK III; a₀ sobe ≥15σ | uma predição observacional |

---

# O que os papers não cobrem

Resultados que estão **[SÓLIDO]/[DERIVADO] ou medidos no RESEARCH_MAP** mas que **não
aparecem em nenhum dos cinco papers**. (Sem julgamento de importância — só a lista.)

1. **A origem microscópica do MOND (FM2-1) e a equivalência TEIC≡Khoury (C1).** O deep-MOND
   `L∝X^{3/2}` é a anomalia de susceptibilidade longitudinal do ferromagneto
   (`χ∥~h^{−0.37}`, Brézin–Wallace), e C1 mostrou que TEIC e Khoury coincidem **no setor
   longitudinal**. Isto é literalmente a ponte entre o ferromagneto (Goldstone, paper 1) e
   a dinâmica galáctica (BTFR, paper 5) — e **não está em paper nenhum**. O BTFR a evita
   deliberadamente ("the reader may regard Eq. as a parameter-free phenomenological ansatz",
   §I); o Matter-Gravity aponta o BTFR como "the empirical content of the gravitational
   sector" (§III.F) mas **não deriva ν_MOND**. → maior lacuna de cobertura.

2. **A conexão A1↔FM2-1 (a "mais bonita" do programa).** O gap longitudinal fecha
   `∝h^{0.31}` = a mesma anomalia deep-MOND (`m²_∥=A/χ∥`); é por isso que o A_μ não tem
   massa Proca espontânea. Em nenhum paper.

3. **O setor de matéria escura (FM4).** `m_A` é CDM fria medida (`w≈0`, dispersão massiva
   na rede). O Matter-Gravity **explicitamente exclui**: "dark matter are out of scope"
   (§I, §claim). Em nenhum paper.

4. **Λ dinâmica (LD).** `Λ_rms∝ρ_crit^{1.107}` (R²=0.996), dissolve a coincidência, com
   assinatura testável `w_eff≈−0.66`. Em nenhum paper.

5. **A relação DEV↔TEIC (A1–A4, Cenário B).** A EFT escalar-vetor-tensor (DEV) é
   **calibrada, não derivada** da rede; os papers nunca nomeiam a DEV (decisão de projeto,
   `TEIC_DEV_CORRESPONDENCE.md`). A própria relação de Cenário B não está em paper.

6. **A camada de colapso / decoerência (COLAPSO_SR_TEIC, FS1, FS2, FD1, FD2).** Saturação
   de χ_eff emerge, espectro = GOE/Dyson, gerador CP + decoerência ∝Δx² emergem; seta/η/ℏ
   externos. Em nenhum paper (decisão explícita: "Nenhum paper").

7. **A fronteira da seta do tempo (FRONTEIRA_SETA_COSMOLÓGICA).** Past Hypothesis externa a
   TEIC/DEV/SR igualmente — fronteira universal. Em nenhum paper.

8. **Resultados de fundação/estrutura do umbrella, ausentes das submissões:** os 5
   operadores de Stückelberg e suas razões (C1–C4/W); os 4 números puros adimensionais
   (CR1–4); `k∝N` (ℏ como granularidade, T3C); `d=3` por exclusão (DS1–3); R5 (por que
   SU(3) e não SU(4): fundamental complexa / `d^{abc}≠0`) — o SU3 paper assume SU(3), não o
   seleciona. Estes vivem em `TEICDoc1`/`TEIC_MASTER`, não nas 5 submissões.

9. **Resultados de nicho medidos:** C5 (dimensão espectral, morte), C6 (vórtices, m_A),
   HQ3/KR-PTA (linha NANOGrav). Em nenhum paper.

**Padrão da lacuna:** os cinco papers cobrem cinco *blocos isolados* (vácuo+Goldstone,
SU(2)+gravidade, fronteira-fóton, cor SU(3), uma predição galáctica). O que falta é
exatamente o **tecido conectivo** entre eles: MOND-microscópico (1↔5), matéria escura,
Λ, DEV, colapso, e a estrutura de fundação (operadores/números/seleções). Quase tudo que
falta é *ponte ou fundação*, não *novo bloco*.

---

# Conexão natural — existe ou não?

**Existem dois fios condutores presentes nos dados. Um é físico e fraco; o outro é
epistêmico e forte. Nenhum dos dois é nomeado como tese unificadora em nenhum paper.**

### Fio 1 (físico) — um único vácuo ferromagnético causal, vários setores. PRESENTE, parcialmente declarado.

Os cinco papers usam **o mesmo substrato e a mesma família de ação**. Evidência direta, nos
próprios textos:
- Goldstone Eq.(1): `S=J Σ Δτ_ij[1−n_i·n_j]` (O(3)).
- Matter-Gravity Eq.(2): `S=Σ Δτ_ij[1−cos∠(n_i,n_j)]` (a **mesma** ação O(3)).
- SU3 Eq.(1): `E=−J Σ ⅓Re Tr(U_iU_j†)`, declarada "the direct SU(3) analogue of the O(3)
  tension of the orientation sector" e identificada como um O(18) restrito.
- Photon-Arc §3 reusa o ferromagneto de orientação de Goldstone verbatim (cita `GoldstonePRD`).
- BTFR é a consequência observacional do setor gravitacional/MOND do **mesmo** vácuo
  (cita `TEICDoc1` como proveniência).

→ É a mesma física (um vácuo que ordena, em O(3)/SU(2)/SU(3)) lida em setores diferentes.
**Mas isto já é parcialmente declarado** via cross-citações (`GoldstonePRD`, `TEICDoc1`,
`BTFRMNRAS`, `PaperII`) — cada paper sabe que tem irmãos. O que nenhum paper faz é
**montar** o vácuo único como afirmação central. É um fio real, mas é "substrato
compartilhado", não uma unificação física nova (ver Q3 — não há lei cross-setor derivada).

### Fio 2 (epistêmico) — a fronteira FORMA/ESCALA. PRESENTE, FORTE, não nomeada como tese.

Este é o fio mais nítido e o mais verificável nos dados: **em todo paper, o que é derivado é
FORMA (uma lei funcional, uma razão adimensional, um fato topológico/estrutural); todo valor
DIMENSIONAL absoluto é externo.** A regularidade vale através de físicas completamente
distintas, e três dos cinco papers a declaram explicitamente — nas suas próprias palavras:

- **Matter-Gravity** (a mais explícita): "The form is derived; the absolute coupling
  `G_net∝1/K` and the GeV scale are external" (abstract); tabela de tags `[Derived]`/
  `[Identified]`/`[External]` onde **todo item [External] é uma escala** (G, f_π) e todo
  derivado é forma ou razão adimensional (`μ_p/μ_n=−1.51`, `[4,16,36]`).
- **SU3**: "All dimensionful scales remain external: the substrate fixes forms and
  dimensionless ratios, not the lattice-to-GeV scale" (abstract); σ, α', m_π externos;
  `ρ_s≈⅓`, `c=√(2/3)`, degenerescência `4×10⁻⁸` derivados.
- **Goldstone**: `c` "recovered without inserting it" mas declarado "a property of the
  operator"; o expoente de S(k) "a size-limited diagnostic, not a precision result"
  (§claim) — forma sim, escala não.
- **Photon-Arc**: a obstrução é estrutural (diamantes elétricos, não-localidade); onde a
  curvatura funciona, exige escala **Planckiana** (§frontier) — i.e. a única alavanca
  positiva é barrada por uma *escala*.
- **BTFR** (o caso aparentemente contrário, e por isso o mais informativo): é um paper
  *sobre uma escala* (a₀). Mas ele **não deriva o valor de a₀** — testa a **forma da sua
  evolução**, `a₀(z)/a₀(0)=H(z)/H₀`, e "`H₀` cancels from the observable" (§I). Mesmo o
  paper-da-escala testa uma razão adimensional e deixa a escala absoluta externa. **O fio
  vale até onde parecia quebrar.**

**Como sei que está nos dados e não na minha interpretação:** não é uma leitura minha — é o
conteúdo literal de `RESEARCH_MAP.md` Seção 7 ("*em todo setor, a forma é derivada, a escala
absoluta é externa, o número puro adimensional é calculável*") e de `PROGRAM_AUDIT.md` §2
("*a fronteira derivado/externo do programa coincide exatamente com a fronteira
forma/escala*"). A campanha COLAPSO_SR_TEIC, num domínio totalmente novo (colapso objetivo),
**reproduziu o mesmo padrão de forma independente**: "o que é forma emerge; o que é
escala/mecanismo absoluto não" (RESEARCH_MAP, §camada de colapso). Um padrão que se repete
num domínio que não estava na amostra original é evidência, não viés.

**Honestidade sobre o que o Fio 2 é e não é:** é uma regularidade **epistêmica/metodológica**,
não um mecanismo físico. Ela é em parte *consequência do guard anti-circularidade*: o guard
proíbe inserir escalas (γ, c, G, dilatação) no gerador, então **só coisas adimensionais
PODEM emergir**. Logo "as escalas são externas" é em parte *construído pelo método*, não uma
lei da natureza descoberta. Isto não a torna falsa — ela é verificável em cada paper — mas
delimita o que ela pode afirmar (ver Q3).

---

# Um paper abrangente seria honesto?

**PARCIALMENTE.** Com uma distinção que os próprios documentos do repositório já fizeram.

### O que seria honesto afirmar

Um paper abrangente do tipo **síntese/umbrella** — "um substrato causal, vários setores,
unidos pela assinatura forma/escala" — é honesto, porque cada peça tem evidência direta:
- *coletar* os positivos dos cinco papers (Newton 1/r; Goldstone escalar relativístico;
  bárion SU(2) adimensional; confinamento+octeto SU(3); predição a₀∝H(z)) é honesto — cada
  um é medido sob guard;
- *nomear* a fronteira forma/escala como a assinatura comum é honesto — está declarada em
  3 dos 5 papers e é verificável nos outros 2.

Este paper **já existe**: é o `TEIC_MASTER`/`TEICDoc1` (o umbrella no Zenodo), citado por
todos os cinco como proveniência.

### O que NÃO seria honesto afirmar (fabricaria pontes)

1. **Unificação física cross-setor.** Não há nenhuma lei derivada ligando as escalas de
   setores diferentes. G, f_π e a₀ são **cada um independentemente externo** — o programa
   **tentou** ligá-los e **morreu**: `G-from-r_proton` falhou por 108 ordens
   (CONVERGENCE), `m_A` por herança √ρ morreu a 9.5σ. Um paper que afirmasse "as escalas
   são uma só" estaria contra os dados.

2. **A fronteira forma/escala como teorema da natureza.** Como dito em Q2, ela é em parte
   um artefato do guard. Honesto: "esta é a assinatura que a disciplina anti-circularidade
   produz; se as escalas da natureza são deriváveis fica em aberto (as tentativas
   morreram)" — não "a natureza separa forma de escala".

3. **A ponte física que faria os cinco UM só está fraca.** O único elo físico que ligaria o
   setor de vácuo (papers 1–2) à predição galáctica (paper 5) é o MOND-microscópico
   (FM2-1/C1), e ele é **[FRACO]**: o expoente ν medido é `−0.4±0.1` vs `−0.5` teórico, e
   "efeitos de tamanho finito empurram o expoente para zero" (RESEARCH_MAP §4.1). Um paper
   abrangente que afirmasse "o substrato prevê a dinâmica galáctica" estaria apoiado no elo
   **mais fraco** do programa, não num [SÓLIDO]. O BTFR foi deliberadamente escrito
   *framework-independente* exatamente para **não** depender desse elo.

### A evidência do próprio repositório contra um abrangente *de submissão*

Há um registro direto e relevante: `docs/reports/PUBLICATION_REVIEW.md` (2026-06-17) avaliou
e **removeu** uma "Section 0" de programa (tese central + tabela do programa inteiro) dos
papers de submissão, concluindo que ela "*dispara o heurístico 'theory of everything' antes
do resultado específico*" e "*amplifica o desk-reject*". Ou seja: o programa **já decidiu**,
por razão estratégica, que o enquadramento abrangente prejudica a publicação e deve ficar
**só no umbrella Zenodo**, não numa submissão. Isto é independente de a conexão ser real — e
ela é (Fio 2) — mas responde à pergunta "seria um bom paper *para submeter*": a evidência
interna diz que não, e diz por quê.

**Veredito de Q3:** um paper abrangente é **honesto como umbrella/síntese (e já existe)**;
**não é honesto como afirmação de unificação física nova** (as escalas são separadamente
externas, a tentativa de uni-las morreu, e o único elo físico 1↔5 é fraco); e **não é
estrategicamente recomendável como submissão** (decisão já registrada e fundamentada no
próprio repo).

---

# Se parcialmente: o que ele poderia afirmar

Estritamente o que os dados suportam, sem ponte fabricada:

- **Afirmação central honesta:** "Um único substrato causal de Poisson com um campo interno
  que ordena ferromagneticamente produz, em setores de simetria interna distintos, as
  **formas** de gravidade Newtoniana, modos de Goldstone relativísticos escalares, um bárion
  SU(2) (fenomenologia adimensional), confinamento e octeto de mésons SU(3), além de uma
  predição galáctica falsificável — e em **todos** os setores o conteúdo derivado é forma e
  razão adimensional, com toda escala dimensional absoluta declarada externa."
- **Pode afirmar** a assinatura forma/escala como regularidade medida e verificável (3 papers
  a declaram, 2 a exibem; reproduzida independentemente no setor de colapso).
- **Pode afirmar** o substrato único e a disciplina anti-circularidade comum como o método
  que gera essa regularidade.
- **Deve afirmar, no mesmo fôlego**, que (i) as escalas são *separadamente* externas e a
  tentativa de ligá-las morreu; (ii) a regularidade é em parte consequência do guard; (iii)
  o elo físico vácuo↔galáxias (MOND-microscópico) é fraco; (iv) a matéria escura, a Λ
  dinâmica, a DEV e a camada de colapso são compatíveis com o mesmo vácuo mas **não** entram
  como derivações fortes.

Em suma: um paper de **síntese honesta com assinatura epistêmica declarada** — não um paper
de **unificação física**.

---

# O que faltaria para ele ser mais forte

(Identificação de lacunas; **sem sugerir campanhas**.)

1. **O elo MOND-microscópico (FM2-1/C1) teria de ser [SÓLIDO], não [FRACO].** Enquanto o
   expoente ν for `−0.4±0.1` e ameaçado por tamanho finito, o único elo *físico* entre o
   vácuo (papers 1–2) e a predição galáctica (paper 5) não sustenta uma afirmação de
   unificação — só de compatibilidade.

2. **Faltaria uma relação derivada ENTRE as escalas externas.** Hoje G, f_π, a₀, ℏ são cada
   um externo por razão própria; não há nenhuma medida que derive uma da outra. Sem isso, a
   "unificação" é de *forma e método*, não de *conteúdo dimensional*. (As tentativas
   conhecidas — CONVERGENCE, herança √ρ — estão [MORTO].)

3. **A fronteira forma/escala precisaria de um argumento de por que a natureza seria assim,
   além do guard.** Como está, ela é uma assinatura do método tanto quanto do substrato; um
   abrangente forte teria de separar "a rede não deriva escalas" de "o guard proíbe inseri-
   las" — distinção que os dados atuais não fazem.

4. **Os blocos compatíveis-mas-não-derivados (DM/FM4, Λ/LD, DEV, colapso/SR) ficariam como
   *contexto*, não como pilares** — porque cada um é [FRACO], [CONSISTENTE-importado] ou
   [fronteira], não [SÓLIDO]. Um abrangente honesto os listaria como "compatíveis com o mesmo
   vácuo", e essa é a afirmação máxima que os dados permitem para eles.

> **Conclusão de uma linha.** Os cinco papers não são cinco resultados sem fio condutor —
> partilham um substrato (fio físico, já citado entre eles) e exibem uma fronteira
> forma/escala comum (fio epistêmico forte, não nomeado como tese). Um paper abrangente é
> honesto como **síntese dessa assinatura** (e já existe como umbrella), mas **não** como
> unificação física: as escalas são separadamente externas, a tentativa de uni-las morreu, o
> único elo físico vácuo↔galáxias é fraco, e o próprio repositório já registrou que o
> enquadramento abrangente prejudica a submissão. O que os dados mostram é convergência de
> **forma e método**, não de **conteúdo dimensional**.

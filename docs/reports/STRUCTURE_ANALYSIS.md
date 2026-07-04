# STRUCTURE_ANALYSIS.md

**Diagnóstico e recomendação de arquitetura da série de papers TEIC**
Análise pura — nenhum paper foi escrito ou modificado nesta tarefa.
Data: 2026-06-17.

---

## EXECUTIVE SUMMARY (leia primeiro — uma página)

A série TEIC hoje são **5 companions** (I=13pp em revisão na CQG; II=6pp em
revisão na PRD; III=3pp; IV=7pp; V=5pp não submetido) **+ 1 TEIC\_MASTER (20pp)**.
O `TEIC_MASTER.tex` atual **não** é um esboço de 13 páginas raso: é um documento
de 20 páginas com prosa integrada, uma Tabela de Status Canônica e uma hierarquia
Núcleo→Aplicações. Ele está *bem escrito*. Mesmo assim ele continua sendo, por
**construção**, um índice — e por uma razão que a polidez de prosa nunca resolve:
toda seção sua diz *"full treatment in Paper X; we summarise here"* e ele carrega
um **disclaimer explícito de não-submissão dupla** ("does not constitute dual
submission of any companion's original research content"). Ou seja, as derivações
**moram nos companions**; o Master apenas **aponta** para elas. Um documento cujo
trabalho é apontar É um índice, por melhor que seja a prosa.

Por que o DEV Master não tem esse problema e o TEIC Master tem? Porque são papéis
**opostos**. O DEV Master é o artefato **primário**: as derivações moram *nele*, e
os companions DEV eram apenas depósitos de prioridade no Zenodo. O DEV pôde
consolidar tudo num manuscrito único porque **nada estava em revisão ativa**. O
TEIC **não pode** fazer isso: **Paper I está em revisão na CQG e Paper II na PRD**.
Não dá para absorver, fundir ou substituir manuscritos que estão sob avaliação
independente sem criar risco real de submissão dupla e sem abandonar dois
processos de revisão ativos. Essa é a restrição dura que mata as opções de
consolidação.

O insight do autor está **correto**: um Master separado não resolve o "fatia
isolada", porque quem recebe só o Paper II continua vendo uma fatia. Mas a
conclusão que o autor tirou (consolidar em menos documentos maiores) colide
frontalmente com a restrição I→CQG / II→PRD. A solução que honra o insight **sem**
colidir com a revisão ativa é mover o resumo-do-todo de **dentro de um documento
separado** para **dentro de cada companion**.

> ### RECOMENDAÇÃO ÚNICA: Opção C — "Section 0 / Theory Overview" embutida em cada paper
>
> Extrair o que o `TEIC_MASTER.tex` já tem de melhor — o **box da tese central
> (Nível 0)**, a **figura da hierarquia Núcleo→Aplicações** e a **Tabela de Status
> Canônica** — para um único arquivo reutilizável (`theory_overview.tex`, ~1,5–2pp)
> e inseri-lo como **Seção 0 ("The TEIC programme at a glance")** logo após o
> abstract de **cada um dos cinco papers**. Assim qualquer leitor que abra
> *qualquer* peça vê o programa inteiro e o mapa derivado/externo antes do
> resultado específico daquela peça. O `TEIC_MASTER` separado é **aposentado** como
> manuscrito (ou rebaixado a um depósito-guarda-chuva só no Zenodo, claramente
> rotulado como não-primário), porque a Seção 0 passa a fazer o seu trabalho
> dentro de cada paper.
>
> **Por que C e não A/B/D:** A, B e D **todas** exigem fundir ou substituir o
> conteúdo de Paper I e/ou Paper II num documento maior — exatamente os dois que
> estão em revisão e não podem ser mexidos. C é a única que (a) resolve o insight
> do autor (nenhuma fatia desconectada), (b) resolve a crítica do revisor de
> comunidade (hierarquia clara + consistência derivado/externo, agora **forçada por
> uma única fonte da verdade** replicada em todos os papers) e (c) respeita I→CQG /
> II→PRD (a Seção 0 é **aditiva** — entra como esclarecimento na rodada de revisão
> de I/II, não altera o conteúdo científico em avaliação).
>
> **Esforço:** ~3,5–4,5 sessões. **Dependência dura:** o teste de robustez de FL1
> controla a linha SU(3) da Tabela de Status; como a tabela é um arquivo
> compartilhado, um resultado negativo de FL1 é **uma** edição que se propaga para
> os cinco papers — isso é uma força, não um custo.

O resto deste documento é a justificativa detalhada.

---

## FASE 1 — INVENTÁRIO COMPLETO

### 1.1 Os cinco companions TEIC (estado atual)

| Paper | Arquivo | Págs | Escopo declarado | Status (registro estabelecido) |
|---|---|---|---|---|
| I | `TEIC/paper/paper_I/paper_I.tex` | **13** | Espaço-tempo emergente, gravitação, conteúdo de operadores, números puros, predição BTFR | Zenodo + **em revisão na CQG** |
| II | `TEIC/paper/paper_II/paper_II.tex` | **6** | Vácuo ferromagneto, fóton-magnon, Skyrmion SU(2), spin-½, m_A matéria escura | Zenodo + **em revisão na PRD** + Research Square |
| III | `TEIC/paper/paper_III/paper_III.tex` | **3** | "A estrutura inevitável": seleção medida de operadores, dimensão, grupo de gauge, estabilizador (Letter, alvo PRL) | **Research Square apenas** |
| IV | `TEIC/paper/paper_IV/paper_IV.tex` | **7** | Confirmação observacional: aceleração crítica subindo com z, critérios de morte | **Research Square (rejeitado 2×)** |
| V | `TEIC/paper/paper_V/paper_V.tex` | **5** | SU(3): confinamento de cor e octeto de mésons pseudoescalares | **Escrito, não submetido** (pendente teste de robustez de FL1) |

Total: **~34 páginas**, fragmentadas em 5 peças. Três delas (III=3pp, V=5pp,
II=6pp) são **finas**. É exatamente o sintoma que o insight do autor descreve:
*cada peça parece pequena e desancorada*. Um Letter de 3 páginas (Paper III) lido
isolado parece um fragmento; o Paper V de 5 páginas sobre SU(3) lido isolado
parece uma curiosidade desconectada do programa.

Observação importante de qualidade: os companions **não estão mal escritos**.
Paper II já abre referenciando Paper I e dá uma narrativa autocontida do setor de
vácuo com uma "mandatory derived/assumed table"; Paper III já comprime as seis
seleções no abstract. Eles **já se cruzam**. O que lhes falta não é prosa — é o
**mapa do todo na frente de cada um**.

### 1.2 O DEV Paper Master — o padrão a imitar

`DEV/paper_master/dev_master.tex` (2159 linhas, **20pp**, formato PRD duas colunas).
Lido por inteiro, o que importa é **como** ele integra:

- **É o artefato primário.** As derivações moram *nele*: o axioma DBI, o limite
  quase-estático que recupera μ(x), o tensor de stress vetorial que dá α=2/3, a
  estabilidade (c_s²∈[1/3,1)), o operador não-local e o teorema γ_G=1−s, o fit
  SPARC de 167 galáxias, fσ₈, UDGs, restrições de massa, a predição BTFR(z) — tudo
  com equações completas, não resumos.
- **Os companions são secundários.** A introdução do Master diz literalmente que
  "as cinco componentes técnicas foram **depositadas independentemente como
  preprints companions no Zenodo, estabelecendo prioridade**". Os companions são
  registros de prioridade, não manuscritos rivais em revisão.
- **Proporção resultado-central vs. contexto/conexão.** Estimativa: ~70–75% do
  documento é resultado central (equações, derivações, tabelas de fit) e ~25–30% é
  contexto e conexão entre partes (intro de 90 linhas que costura a narrativa de
  Newton→MOND→slip→cosmologia; seção de limitações; discussão; posicionamento na
  literatura não-local). É um fluxo único: cada seção *usa* o resultado da anterior
  (o background deep-MOND da §6 vem do μ(x) derivado na §4), não seções isoladas
  empilhadas.

**Essa é a chave do diagnóstico:** o DEV Master integra porque ele é onde a física
acontece. A integração não veio de prosa de costura — veio de ser **primário**.

### 1.3 O TEIC\_MASTER atual — a "tentativa anterior"

`TEIC/paper/TEIC_MASTER.tex` (971 linhas, **20pp**, formato article uma coluna).
A premissa do prompt ("13 páginas, tipo índice") está **desatualizada**: o
documento foi expandido para 20 páginas e tem prosa real, não bullets. Ele tem
dois ativos genuinamente bons:

1. A **Tabela de Status Canônica** (Sec. 2) — uma `longtable` que dá a *um* status
   (`[Derived]`/`[Identified]`/`[External]`/`[Dead]`) para cada ingrediente da
   teoria inteira, com macros que tornam a deriva de linguagem mecanicamente
   impossível. Esta é a resposta direta à objeção do revisor sobre consistência
   derivado/externo.
2. A **hierarquia Núcleo→Aplicações** (Fig. 1, Sec. 1.3) — Nível 0 tese / Nível 1
   núcleo / Nível 2 provas de rigor / Nível 3 aplicações / Nível 4 mortes.

Mas o documento permanece um índice por três traços estruturais, não de prosa:

- **Toda seção de conteúdo difere ao companion.** §3: "complete derivations in
  Paper I; we summarise". §4: "Full treatment in Paper II". §5, §6, §7, §8, §9:
  idem. As derivações não estão aqui — estão lá.
- **Disclaimer de não-submissão dupla** (Sec. 11): "This Master document is a
  synthesis/overview and **does not constitute dual submission** of any companion's
  original research content." O documento se **declara** secundário.
- **Postura defensiva forçada.** O cabeçalho diz "Companions I–V are NOT modified"
  e "Depth/length calibrated against the DEV Master (20 pp)". Ele foi escrito para
  não pisar nos companions — e companions em revisão (I, II) tornam essa cautela
  obrigatória.

### 1.4 O conteúdo científico por peso (Hierarquia Núcleo→Aplicações)

Usando a hierarquia já estabelecida no próprio Master:

- **Nível 0 — Tese central:** rede causal de Poisson + ordenamento espontâneo de
  orientação ⇒ luz (magnon) E matéria (Skyrmion) juntas. (<1pp)
- **Nível 1 — Núcleo:** (1) espaço-tempo + gravitação [≈ Paper I, 13pp]; (2) vácuo
  = ferromagneto de orientação [Paper II]; (3) fóton = magnon BD ω=ck [Paper II];
  (4) matéria = defeito topológico SU(2) [Paper II].
- **Nível 2 — Provas de rigor:** eliminação de grupo de gauge; teorema K≤⅔S (SU2)
  e K≤6·TrM² (SU3) — os ingredientes externos são **necessários**. (~2–3pp)
- **Nível 3 — Aplicações:** SU(3) confinamento + octeto [Paper V, 5pp]; MOND
  microscópica/identificação Khoury; m_A matéria escura fria; BTFR predição +
  confirmação [Paper IV, 7pp]; binárias largas <17pc.
- **Nível 4 — Mortes pré-registradas:** S₈ (5 mortes, uma razão estrutural);
  criação colisional; 3 gerações; Higgs espontâneo; running de dimensão espectral;
  Regge do bárion. (~2–3pp)

---

## FASE 2 — DIAGNÓSTICO

### 2.1 Por que a tentativa de Master ficou "tipo índice"?

A resposta do prompt oferecia (a) falta de profundidade técnica, (b) falta de
conexão entre seções, (c) compressão excessiva, ou (d) outra razão. A resposta
honesta, depois de ler o `TEIC_MASTER.tex` inteiro, é **(d), e ela é estrutural,
não de redação**:

> O TEIC Master ficou índice porque foi concebido num **papel oposto** ao do DEV
> Master. O DEV Master é **primário** — as derivações moram nele. O TEIC Master é
> **secundário** — as derivações moram nos companions e ele aponta para elas. Um
> documento cujo trabalho declarado é apontar para onde a física está É um índice,
> não importa quão boa seja a prosa de ligação.

Evidência textual concreta:

- Não é (a): a prosa de §3–§9 é densa e correta; o teorema K≤⅔S, por exemplo, é
  *resumido com a derivação em três linhas* (Cauchy-Schwarz → bound pontual), não
  só citado. Há profundidade.
- Não é (b): a conexão entre seções existe e é explícita (§6 "building on the
  ferromagnetic-vacuum mechanism of §4"; §7 idem). A costura está lá.
- Não é (c): 20 páginas não são compressão excessiva; é o mesmo orçamento do DEV
  Master.
- **É (d):** cada seção termina entregando a derivação ao companion ("Full
  treatment in Paper II"), e o documento se autodeclara não-primário (Sec. 11). O
  leitor sente um índice porque é literalmente um guia-de-leitura para outros
  cinco documentos.

E a causa-raiz dessa escolha de papel é a **restrição dura**: Paper I (CQG) e
Paper II (PRD) estão em revisão. Se o TEIC Master tentasse ser primário —
reproduzir as derivações de I e II — ele seria submissão dupla do material que
está sob avaliação. O DEV não tinha essa amarra (companions só no Zenodo), então
o DEV Master pôde ser primário. **O TEIC Master ficou índice porque a única coisa
que ele tinha permissão de ser, com I e II em revisão, era um índice.**

Corolário: **nenhum retrabalho de prosa do Master separado vai consertar isso.**
Enquanto for um documento à parte com I/II em revisão, ele é estruturalmente
condenado a ser índice. Isso, por si só, valida o insight do autor de que "um
resumo separado NÃO resolve" — e empurra a solução para *dentro* dos papers.

### 2.2 Quantos documentos finais fariam sentido? (as 4 opções)

**OPÇÃO A — Um único documento (Master único substituindo todos os companions).**
- Resolve o insight do autor? Sim, *se* for a única coisa enviada.
- Resolve a crítica do revisor? Sim (uma fonte da verdade).
- Compatível com I→CQG / II→PRD? **NÃO.** Exige descontinuar os companions; I e II
  estão em revisão ativa e não podem ser "des-enviados". Um documento de 40–60pp
  também não cabe em CQG/PRD/PRL/ApJL (escopos focados). **Morta pela restrição
  dura.**
- Retrabalho: máximo (escrever as derivações de I+II+V de novo num só lugar).

**OPÇÃO B — Dois documentos por natureza ("Foundations & Matter" / "Phenomenology
& Tests").**
- Resolve o insight? Parcialmente — dois documentos grandes, mas cada um ainda é
  uma "fatia" do outro a menos que cada um ganhe um overview (i.e., precisa de C de
  qualquer jeito).
- Resolve o revisor? Sim.
- Compatível com I/II? **NÃO.** O conteúdo de Paper I cairia em "TEIC I" e o de
  Paper II ficaria partido entre os dois — exatamente os dois manuscritos em
  revisão. Cria o mesmo emaranhado de submissão dupla de A. 
- Retrabalho: alto (fusão e reescrita genuínas).

**OPÇÃO C — Manter 5 documentos, cada um ganha uma Seção 0 / Theory Overview.**
- Resolve o insight? **Sim, diretamente.** Quem abrir *qualquer* uma das 5 peças vê
  a Tabela de Status completa e a hierarquia Núcleo→Aplicações antes do resultado
  específico. Nenhuma fatia chega desancorada.
- Resolve o revisor? **Sim, e melhor que o Master separado**: a consistência
  derivado/externo passa a ser forçada por *uma fonte da verdade replicada em todos
  os papers* (não um documento que ninguém que recebe o Paper II isolado vê).
- Compatível com I/II? **SIM.** A Seção 0 é aditiva e não muda o conteúdo
  científico em avaliação; entra como esclarecimento na rodada de revisão de I/II
  (ou em prova), e as versões Zenodo podem ser atualizadas já. Baixo risco.
- Retrabalho: **moderado e em grande parte reaproveitamento** — o overview já
  existe pronto dentro do `TEIC_MASTER.tex` (tabela + hierarquia + box da tese);
  só precisa ser extraído para um arquivo e incluído nos 5 papers.

**OPÇÃO D — Híbrido: 2–3 docs por natureza, o mais amplo faz o papel de Master.**
- Resolve o insight? Como B.
- Resolve o revisor? Sim.
- Compatível com I/II? **NÃO** pela mesma razão de B/A: o documento amplo absorve
  I e/ou II.
- Retrabalho: alto.

**Veredito da Fase 2.2:** A restrição dura I→CQG / II→PRD elimina A, B e D — todas
exigem fundir ou substituir manuscritos em revisão ativa. **C é a única
sobrevivente** que satisfaz as três pressões simultaneamente.

### 2.3 O que fazer com Paper I e Paper II já enviados?

Esta é a restrição que decide tudo. Tratamento explícito:

- **A consolidação (A/B/D) é inviável para I e II.** Você não pode pegar um
  manuscrito sob avaliação na CQG e embuti-lo num documento maior submetido a outro
  lugar — isso é submissão dupla e, na prática, abandono do processo de revisão. O
  DEV pôde consolidar porque seus companions eram só Zenodo (prioridade), não
  revisões de periódico ativas. **TEIC já passou desse ponto para I e II.**
- **A consolidação só é livre para o material NÃO travado:** conteúdo de Paper III
  (Research Square apenas), Paper IV (Research Square, rejeitado 2×), Paper V (não
  submetido), e os resultados de C1–C6/FL1 ainda não publicados em periódico. Esses
  *poderiam* ser reorganizados/fundidos sem colidir com revisão alguma. Mas isso é
  uma jogada **secundária e opcional**, não o eixo da recomendação.
- **Como apresentar um documento amplo sem prejudicar I/II:** a Opção C resolve
  isso sem documento amplo. Se mesmo assim se quiser um guarda-chuva citável, ele
  vai **só para o Zenodo**, claramente rotulado "overview/synthesis, não constitui
  pesquisa original nem submissão dupla" — que é, aliás, exatamente o que o
  `TEIC_MASTER.tex` já é. Mas o autor já julgou (corretamente) que esse
  guarda-chuva separado não resolve o "fatia isolada". Logo: **a Seção 0 embutida
  substitui o guarda-chuva; o guarda-chuva separado é redundante.**
- **Para I e II especificamente:** NÃO tocar nas versões em revisão. Preparar o
  bloco Seção 0 como uma revisão **em espera**, a ser incorporada quando vier o
  relatório do referee (adicionar uma seção de orientação/estrutura que situa o
  paper na série é aditivo, bem-visto, e responde diretamente à objeção do revisor
  de comunidade "qual é a apresentação autossuficiente?"). As versões Zenodo
  (prioridade) podem ganhar a Seção 0 já, numa nova versão.

### 2.4 Qual é o peso real de cada resultado? (orçamento de páginas na densidade DEV)

Se *hipoteticamente* tudo fosse consolidado como primário na densidade do DEV
Master:

| Nível | Conteúdo | Páginas (densidade DEV) |
|---|---|---|
| 0 | Tese central | <1 |
| 1 | Núcleo: geometria+gravitação (≈Paper I) | ~13 |
| 1 | Núcleo: vácuo+fóton+SU(2) (≈Paper II core) | ~6 |
| 2 | Provas de rigor (eliminação gauge, K≤⅔S, K≤6TrM²) | ~2–3 |
| 3 | SU(3) + MOND/Khoury + m_A DM + BTFR + binárias | ~12–15 |
| 4 | Mortes catalogadas | ~2–3 |
| | **Total consolidado** | **~35–40pp** |

Leitura desse orçamento:

- **35–40pp confirma que A (um doc gigante) é impraticável** para qualquer
  periódico, e que B (dois docs extensos) seria a forma "realista" de consolidar
  *se a consolidação fosse permitida* — mas não é, para I e II.
- Para o material **livre** (III + V + provas de rigor + overview) o orçamento é
  ~10–13pp — i.e., naturalmente **um paper médio**. Isso é o que sustenta a jogada
  *opcional secundária*: depois de C, III e V poderiam um dia fundir-se num único
  "TEIC: structure, colour and confinement" sem tocar em I/II. Mas é opcional.

---

## FASE 3 — RECOMENDAÇÃO FINAL

### 3.1 Recomendação única e clara

**Adotar a Opção C: embutir uma Seção 0 ("The TEIC programme at a glance",
~1,5–2pp) idêntica em cada um dos cinco companions, extraída dos ativos que o
`TEIC_MASTER.tex` já contém; aposentar o TEIC\_MASTER como manuscrito separado
(ou rebaixá-lo a depósito-guarda-chuva só-Zenodo, não-primário).**

A Seção 0 contém exatamente três coisas, num único arquivo `\input`-ável:

1. O **box da tese central** (Nível 0).
2. A **figura da hierarquia Núcleo→Aplicações** (Níveis 1–4).
3. A **Tabela de Status Canônica** condensada (derivado/identificado/externo/morto
   para os ingredientes principais), com a nota de que ela é a fonte da verdade
   para a série inteira.

Por que essa, e por que ela resolve as três pressões **ao mesmo tempo**:

- **Insight do autor (nenhuma fatia desconectada):** resolvido na raiz — o resumo
  do todo agora viaja *dentro* de cada peça. Quem receber só o Paper II (em revisão
  na PRD) vê o programa inteiro e o mapa derivado/externo antes do resultado de
  vácuo. É literalmente o que o autor pediu: "cada paper deve CONTER um resumo da
  teoria como um todo".
- **Crítica do revisor de comunidade (hierarquia clara + consistência
  derivado/externo):** resolvido melhor do que pelo Master separado. A mesma Tabela
  de Status, em todos os papers, vinda de um arquivo único, torna a deriva de
  status mecanicamente impossível através da série inteira — não só dentro de um
  documento que o leitor de uma fatia talvez nunca veja.
- **Realidade I→CQG / II→PRD:** respeitada. C é aditiva, não funde nem substitui
  nada; a Seção 0 entra em I/II na rodada de revisão sem alterar a ciência em
  avaliação.

### 3.2 Plano de transição concreto (em ordem)

1. **Extrair o overview compartilhado.** Criar `TEIC/paper/theory_overview.tex`
   (~1,5–2pp) com: box da tese, figura da hierarquia, Tabela de Status condensada e
   as quatro macros de status. Fonte: copiar de `TEIC_MASTER.tex` (Secs. 1.2–1.3 e
   2). *Não escrever nada novo de física.*
2. **Inserir nos papers livres primeiro (III, IV, V).** `\input{../theory_overview}`
   como "Section 0" logo após o abstract. Compilar cada um, conferir que renderiza e
   que a paginação não explode (cuidar do formato: III é `prl reprint` duas colunas;
   a tabela pode precisar de uma versão `\small`/landscape ou condensada).
3. **Preparar a Seção 0 em espera para I e II.** Gerar a versão da Seção 0 para o
   formato de cada um (I=article/CQG, II=`prd reprint`), **sem** tocar nas versões
   em revisão. Atualizar **já** os depósitos Zenodo de I e II para uma nova versão
   contendo a Seção 0 (prioridade + coerência pública imediata).
4. **Aposentar o `TEIC_MASTER.tex`.** Ou retirá-lo de circulação, ou mantê-lo
   apenas como depósito Zenodo "overview", removendo a moldura defensiva (o
   disclaimer de submissão dupla deixa de ser necessário porque o overview agora
   mora em cada paper). Decidir: recomendo **manter só no Zenodo como guarda-chuva
   citável**, porque ele já existe e é bom — mas parar de tratá-lo como "a
   apresentação autossuficiente"; esse papel passou para a Seção 0 × 5.
5. **Gate de FL1 sobre a linha SU(3).** Antes de finalizar, confirmar o teste de
   robustez de FL1. Como a linha SU(3) da Tabela de Status mora no
   `theory_overview.tex` compartilhado, qualquer downgrade (de `[Derived]` para
   `[Identified]`/`[Dead]`) é **uma edição única** que se propaga aos cinco papers
   e ao Paper V (cujo conteúdo é o SU(3)).

### 3.3 Estimativa de esforço

| Etapa | Sessões |
|---|---|
| 1. Extrair `theory_overview.tex` | 0,5–1 |
| 2. Inserir + compilar em III, IV, V | 1 |
| 3. Preparar Seção 0 para I e II + atualizar Zenodo | 1 |
| 4. Aposentar/rebaixar o Master | 0,5 |
| 5. Gate FL1 (verificação + propagação se negativo) | 0,5–1 |
| **Total** | **~3,5–4,5 sessões** |

Compare com A/B/D: reescrita genuína de 35–40pp de derivações primárias = ordens
de grandeza mais trabalho, **e** colisão com I/II. C é mais barata *e* mais segura.

### 3.4 Riscos explícitos

**O que pode dar errado:**
- *Editor de I/II vê a Seção 0 como alteração do manuscrito.* Mitigação: NÃO empurrar
  durante a revisão; segurar para a rodada de resposta ao referee (ou prova). A
  versão Zenodo absorve a mudança imediatamente sem risco.
- *Repetição entre os 5 papers.* A mesma Seção 0 em todos cria autossobreposição.
  Periódicos raramente objetam a *enquadramento* repetido (não são resultados
  duplicados), mas manter ≤1,5–2pp e rotular claramente como "orientation". Em
  Letters (Paper III, PRL) o espaço é apertado — pode ser preciso uma Tabela de
  Status ainda mais condensada ou movida para material suplementar.
- *Propagação de erro.* Fonte única significa que um erro no overview aparece em
  cinco lugares. É o reverso da moeda da consistência.

**O que fica mais frágil:**
- A série **perde** o apelo de "um grande manuscrito unificado" que o DEV tem. TEIC
  permanece distribuído. Isso é **inevitável** dado que I e II já foram comprometidos
  com periódicos separados. A Seção 0 embutida é o melhor substituto disponível para
  a coesão de manuscrito único do DEV — não é tão forte quanto um Master primário,
  mas é a única coisa compatível com a restrição dura.

**O que fica mais forte:**
- Cada fatia passa a se autoancorar (insight do autor: resolvido).
- A consistência derivado/externo é forçada na série inteira por uma única tabela
  (crítica do revisor: resolvida, e de forma mais robusta que o Master separado).
- Zero colisão com as revisões ativas de I/II (restrição dura: respeitada).
- A dependência de FL1 vira um ponto único de edição em vez de uma caça por cinco
  documentos.

### 3.5 Dependência de FL1 (declarada na recomendação)

O teste de robustez de FL1 está pendente e **alimenta diretamente** o conteúdo do
Paper V e a linha SU(3) da Tabela de Status compartilhada. Se FL1 sair **negativo**:
o Paper V (SU(3) confinamento + octeto) precisa de revisão de escopo antes de
qualquer submissão, e a linha "SU(3) colour ferromagnet / confinamento / octeto"
deve ser rebaixada de `[Derived]` no `theory_overview.tex`. Por causa da Opção C,
essa correção é **uma** edição que se propaga corretamente para os cinco papers —
e este é precisamente um dos motivos pelos quais a fonte-única da Seção 0 é
preferível a manter o resumo do todo só num Master separado que o leitor de uma
fatia nunca vê.

---

*Fim da análise. Nenhum paper foi escrito ou modificado.*

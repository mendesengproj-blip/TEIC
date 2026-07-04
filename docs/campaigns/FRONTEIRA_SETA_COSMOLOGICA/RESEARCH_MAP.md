# RESEARCH_MAP — FRONTEIRA_SETA_COSMOLOGICA

> **Origem.** A campanha `COLAPSO_SR_TEIC` matou EXP 2 cirurgicamente: a rede causal
> de TEIC entrega o EIXO de tempo (DAG estrito, aciclicidade 1.000) e a SATURAÇÃO de
> χ_eff, mas NÃO a SETA (irreversibilidade). A assimetria só apareceu sob um contorno
> de baixa entropia imposto (cone "começo" D_TR~50–60 vs diamante simétrico ~0) = a
> Past Hypothesis.
>
> **Tarefa.** Mapear ESTRUTURALMENTE (sem simular) se a Past Hypothesis tem contato
> GENUÍNO — derivação, não transporte — com o setor cosmológico de TEIC/DEV.
> Capaz de concluir "fronteira fechada" com a mesma naturalidade que "ponte candidata".
>
> **Status:** ZERO simulação. DEV: **lida, não alterada** (confirmado abaixo).
> Análise documental sobre fontes já no pipeline.

---

## VEREDITO (resultado primeiro)

**[X] DESFECHO B — FRONTEIRA FECHADA.**

Nenhuma estrutura cosmológica concreta de TEIC, DEV ou SR DERIVA o contorno de baixa
entropia que EXP 2 mostrou ser necessário. Todos os contatos examinados são de tipo
**TRANSPORTE** (importam a assimetria de uma condição inicial/background escolhido) ou
**AUSENTES** (a estrutura simplesmente não existe na teoria). A Past Hypothesis
permanece **externa a TEIC, DEV e SR igualmente** — exatamente o status do problema em
toda a física (CST, Modelo Padrão inclusos). **TEIC não é deficiente; está em boa
companhia.** Isto encerra a questão honestamente; não reabrir sem física nova.

| contato | tipo | derivação ou transporte? | falsificador disparou? |
|---|---|---|---|
| C1 expansão FRW de DEV → seta | **ausente** | — (DEV não tem setor FRW derivado) | SIM |
| C2 primeiro evento do sprinkling | **estrutural sólido (contra)** | nenhum (gerador é uniforme) | SIM — é o nó que mata |
| C3 Λ dinâmica ∝ ρ_crit (everpresent) | analógico | **TRANSPORTE** (precisa de V₄_past finito = começo) | SIM (circularidade) |
| C4 Big Idle / ciclo termo de SR | analógico | **TRANSPORTE** (poda irreversível postulada) | SIM (= morte de EXP 2) |
| C5 textura primordial (FM3) / BTFR(z) | analógico | **TRANSPORTE** (pressupõe H(z) hot→cold) | SIM (já [MORTO]) |

Há **uma única rota logicamente não-circular conhecida** (ponto de Janus / seta por
crescimento de complexidade), mas ela **NÃO é uma estrutura atual de TEIC/DEV** — é um
programa externo (Barbour/Carroll). Registrada em `PRE_REGISTRO_FUTURO.md` como opção
externa opcional sob ceticismo máximo, **não** como ponte encontrada.

---

## FASE 1 — LEITURA (o que cada fonte LITERALMENTE diz sobre condição inicial)

### FONTE A — `COLAPSO_SR_TEIC` (EXP 2)
- **Medido:** trajetória de χ_A forward (passado→futuro) vs backward; D_TR < 3 em todos
  os n no diamante simétrico → χ_eff é **reversível**. Ordem causal = DAG estrito
  perfeito (acíclico=1.000): o EIXO existe, a SETA não.
- **Contorno que produziu D_TR~50–60** (`exp2_confirm.py`): `sprinkle_future_cone` —
  t~U(0,1), x uniforme na bola de raio t. Geometria: **um único ápice no passado**
  (origem, t=0) e um futuro que se alarga. Isto é uma condição de contorno de
  **volume/entropia mínimos no início** (um "começo"), vs o diamante que tem ápices
  simétricos no passado E no futuro.
- **Forma EXATA da Past Hypothesis nos dados:** uma fronteira temporal de baixa
  cardinalidade (um começo de poucos eventos) imposta à MÃO via escolha da região de
  sprinkling. Não emergiu de dinâmica — foi a forma da região.

### FONTE B — Setor cosmológico de TEIC (`LAMBDA_DYNAMICS.md`, `RESEARCH_MAP.md`)
- **Λ dinâmica (LD):** Λ_rms ~ 1/√(V₄_**past**) (everpresent de Sorkin). Resultado:
  Λ_rms ∝ ρ_crit^1.107, Ω_Λ O(1) por ~7 e-folds. **Background flat-ΛCDM E(z) é
  IMPORTADO e citado** (Zwane–Afshordi–Sorkin); só o coeficiente de amplitude (L1=0.971)
  e os números derivados são de TEIC. "Diagnóstico de consistência, não um solve
  estocástico auto-consistente."
- **Sprinkling de Poisson (`causal_core.sprinkle_box`):** "Poisson sprinkle events
  **uniformly** in a box": n=Poisson(ρ·vol), pts=uniform(bounds). **Densidade uniforme,
  sem gradiente de entropia.** Não há "primeira fatia" privilegiada por construção.
- **BTFR (Paper V):** Δlog v = ¼ log[H(z)/H₀] — depende de H(z) **importado**.
- **Condição inicial de baixa entropia em TEIC?** A única linha adjacente no
  RESEARCH_MAP é **FM3 (textura primordial) = [MORTO]**. A rede causal é **agnóstica
  quanto ao início**: o gerador é homogêneo.

### FONTE C — Setor cosmológico de DEV (LIDO, NÃO ALTERADO)
- `paper_master/dev_master.tex` é uma **EFT GALÁCTICA** (saturação do vácuo
  gravitacional abaixo de a₀ = matéria escura aparente; SPARC 167 galáxias). Busca por
  "initial condition / entropy / arrow / big bang / primordial" → **NADA**.
- **Vácuo DBI:** estado de referência **saturado/inerte** (acima de a₀ inerte; abaixo
  efervesce). É um **equilíbrio de referência**, NÃO um contorno cosmológico de baixa
  entropia. Não há evolução cosmológica de baixa→alta entropia em DEV.
- **FRW/expansão em DEV?** Ausente do master. As incursões cosmológicas (S8/fσ8) são
  Verdict C [MORTAS] e usaram **background importado** (CAMB). DEV **não tem seta
  cosmológica embutida** própria; a₀(z)∝H(z) **transporta** H(z) importado.

### FONTE D (contexto) — SR
- **Ciclo termodinâmico** (poda→Unruh→gravidade→restauração): a direção vem da
  **irreversibilidade da poda — POSTULADA** ("3→4 step", §2.1, declarado problema
  aberto pelo próprio autor). **Confirmado: input, não output** (= morte de EXP 2).
- **Big Idle** (Γ→0, predição 12): estado FINAL onde a poda cessa por diluição da
  expansão — um fim de **alta entropia** (heat-death-like). O início (alta conectividade)
  seria a baixa entropia, mas a seta entre eles é a poda postulada. Não ajuda TEIC.

---

## FASE 2 — MAPA DE CONTATO (com falsificadores obrigatórios)

### [CONTATO POTENCIAL C1] — Expansão FRW de DEV fornece a seta
- **Afirmação:** a expansão a→∞ de DEV definiria a direção termodinâmica que a rede
  local de TEIC não gera.
- **Tipo:** *coincidência superficial* (a premissa nem existe).
- **Sustenta:** universos em expansão têm seta termodinâmica padrão.
- **FALSIFICA:** "se DEV não tiver um setor FRW DERIVADO, a ponte morre." →
  **DISPAROU.** DEV-master não tem FRW; a₀(z)∝H(z) usa H(z) importado. O vácuo DBI é
  equilíbrio de referência (não baixa entropia). **Morto na fonte.**
- **Custo / pré-condição:** n/a (falsificado documentalmente).

### [CONTATO POTENCIAL C2] — O "primeiro evento" do sprinkling de Poisson
- **Afirmação:** a geração da rede causal teria um gradiente de entropia embutido.
- **Tipo:** **estrutural sólido — mas CONTRA a ponte (é o falsificador-mãe).**
- **Sustenta (contra):** `sprinkle_box` é **uniforme** por definição → homogeneidade
  estatística → simetria temporal dentro de qualquer região simétrica (EXP 2 mediu
  D_TR~0). Um processo uniforme **não contém Past Hypothesis por construção**.
- **FALSIFICA a ponte:** "se a rede é gerada por processo uniforme, nenhuma cosmologia
  local a salva." → **DISPAROU.** Não é uma lacuna a preencher; é uma propriedade: o
  gerador é livre de seta.
- **Custo:** zero (é definição do gerador).

### [CONTATO POTENCIAL C3] — Λ dinâmica rastreando ρ_crit
- **Afirmação:** Λ_rms ∝ ρ_crit^1.107 decai monotonicamente → uma seta.
- **Tipo:** *analógico frouxo*.
- **Sustenta:** decaimento monótono de ρ_crit com a expansão é direcional.
- **FALSIFICA:** "circularidade — se Λ(ρ_crit) só funciona ASSUMINDO expansão dirigida,
  transporta, não deriva." → **DISPAROU** (ver Fase 3). Λ_rms~1/√(V₄_**past**) exige (i)
  a distinção passado/futuro e (ii) **V₄_past FINITO** = um começo que limita o volume
  4D — isto É a Past Hypothesis, e o background E(z) é importado.
- **Custo:** o solve auto-consistente (ADGS estocástico) seria médio/alto; mas ver
  Fase 3 — predito como transporte de qualquer modo.

### [CONTATO POTENCIAL C4] — Big Idle / ciclo termodinâmico de SR
- **Afirmação:** SR teria começo (alta conectividade) → fim (Big Idle) = seta.
- **Tipo:** *analógico*.
- **FALSIFICA:** "confirmar que a seta de SR é input." → **DISPAROU.** A direção vem da
  poda irreversível **postulada** (mesma morte de EXP 2). SR não deriva; não ajuda TEIC.

### [CONTATO POTENCIAL C5] — Textura primordial (FM3) / BTFR(z)
- **Afirmação:** relíquias primordiais (Kibble–Zurek) ou a₀(z)∝H(z) carregam a seta.
- **Tipo:** *analógico*.
- **FALSIFICA:** "pressupõe uma evolução cosmológica hot→cold (uma seta) já dada." →
  **DISPAROU.** FM3 já é **[MORTO]**; BTFR usa H(z) importado. Transporte.

---

## FASE 3 — O TESTE DE CIRCULARIDADE (o coração)

> Para cada contato: a estrutura DERIVA o contorno de baixa entropia (de premissas SEM
> assimetria temporal), ou PRESSUPÕE algo equivalente a ele?

- **C1:** n/a — estrutura ausente.
- **C2:** não há o que derivar — o gerador é uniforme (arrow-free). Veredito: a rede
  **não contém** a baixa entropia; ponto final.
- **C3 (o mais tentador):** **PRESSUPÕE.** "V₄_past" embute a direção passado/futuro; a
  **finitude** de V₄_past embute um começo (sem começo, V₄_past diverge — o próprio LD1
  só converge porque o background importado tem big bang). O exponente p=1.107 é um
  diagnóstico de consistência SOBRE um background com seta já dentro. **Transporte, não
  derivação.** NÃO é vitória.
- **C4:** **PRESSUPÕE** (poda irreversível postulada). Transporte.
- **C5:** **PRESSUPÕE** (hot→cold dado). Transporte.

**Resultado, como previsto honestamente de antemão:** **todos os contatos são
transporte, circulares ou ausentes.** A cosmologia de TEIC/DEV pode TRANSPORTAR a seta
de uma condição inicial importada, mas **nenhuma das três teorias a DERIVA** —
consistente com o status do problema em toda a física.

---

## POR QUE A PONTE PROVAVELMENTE NÃO FUNCIONA (seção obrigatória, peso igual)

Quatro argumentos estruturais, cada um suficiente sozinho:

1. **O gerador é uniforme (o argumento decisivo).** `sprinkle_box` produz densidade de
   Poisson **homogênea**. Homogeneidade estatística ⟹ invariância sob reversão temporal
   dentro de qualquer região temporalmente simétrica. EXP 2 mediu isto diretamente
   (D_TR~0, mean(in−out)=0). Nenhuma estrutura cosmológica LOCAL pode injetar
   retroativamente um gradiente de entropia num processo que é uniforme **por
   definição**. Isto não é uma lacuna que pesquisa futura preenche; é uma propriedade do
   objeto. Para ter Past Hypothesis, TEIC teria de **trocar o gerador** por um não-uniforme
   com um começo — que é precisamente IMPOR a condição inicial. Mesma morte de EXP 2.

2. **Toda "derivação" da seta via expansão/estado-especial é circular (teorema de
   fundo).** As equações de fundo (Friedmann, ou a dinâmica de rede) são **simétricas
   sob reversão temporal**. Solução simétrica + dinâmica simétrica não geram solução
   assimétrica sem uma **condição inicial assimétrica**. Isto é Penrose/Price/Wald, não
   uma fraqueza de TEIC. C3 cai exatamente aqui: importa a assimetria do E(z) de ΛCDM.

3. **DEV simplesmente não tem o setor.** O master é uma EFT galáctica; suas incursões
   cosmológicas estão MORTAS e usaram backgrounds importados. Pedir a DEV a Past
   Hypothesis é pedir a uma teoria de rotação de galáxias que explique o big bang — fora
   de escopo por construção. O vácuo DBI é um **equilíbrio de referência**, o estado de
   MENOR atividade local, não um estado cosmológico de baixa entropia global.

4. **SR está no mesmo buraco.** SR POSTULA a irreversibilidade da poda (seu autor o
   declara aberto). Logo SR não pode emprestar a TEIC uma seta que ela própria não tem.
   As três teorias compartilham exatamente a mesma dívida.

**Auto-checagem anti-viés:** esta seção tem 4 argumentos estruturais sólidos; a seção
pró-contato (Fase 2) tem 0 contatos que sobrevivem (todos os falsificadores dispararam).
O peso pende DECISIVAMENTE para "não há ponte" — e isso é evidência, não viés, porque
cada anti-argumento é uma propriedade verificável (uniformidade do gerador; importação do
E(z); ausência do setor em DEV; postulação em SR), não uma narrativa.

---

## POR QUE PODERIA, MESMO ASSIM, HAVER ALGO (a única fresta honesta)

Há **uma** rota que NÃO é trivialmente circular, e a honestidade exige registrá-la:
**quebra ESPONTÂNEA da simetria de reversão temporal** (não imposição). Dinâmica
simétrica PODE gerar soluções assimétricas por quebra espontânea — como uma bola no topo
de um morro escolhe um lado. Os cenários de **ponto de Janus** (Barbour et al.) e
**two-headed time** (Carroll–Chen) derivam uma seta em CADA ramo a partir de dados
centrais simétricos, via crescimento de **COMPLEXIDADE** (não de entropia imposta num
contorno). O ensemble permanece simétrico; cada realização tem seta.

- **Por que é uma fresta real:** escapa do teorema de fundo (Fase 3 #2) porque não impõe
  contorno assimétrico — a assimetria é emergente/espontânea.
- **Por que NÃO é uma ponte de TEIC/DEV hoje:** ponto de Janus **não é uma estrutura de
  TEIC nem de DEV**. É um programa externo. Importá-lo seria trazer física nova, não
  achar contato. Por isso o veredito permanece **fronteira fechada**; a fresta vai para
  `PRE_REGISTRO_FUTURO.md` como **opção externa opcional**, sob ceticismo máximo e com
  kill-criterion de circularidade — explicitamente **não** reivindicada como descoberta.

---

## FASE 5 — REGISTRO

- **Veredito:** DESFECHO B (fronteira fechada). A Past Hypothesis é externa a TEIC, DEV
  e SR igualmente — fronteira UNIVERSAL da seta do tempo, **não dívida específica de
  TEIC**. TEIC inclusive sai na frente: entrega o EIXO (DAG perfeito) que SR precisa
  engendrar via d_s:3→4.
- **DEV:** lida, não alterada. Zero parâmetro tocado (a₀, β, η canônicos intactos), zero
  fit novo, zero desenvolvimento. Confirmado.
- **Pré-registro futuro:** escrito SÓ para a fresta de Janus/complexidade (externa,
  opcional, ceticismo máximo) — ver `PRE_REGISTRO_FUTURO.md`. NÃO é um contato de TEIC/DEV.
- **Nenhum paper.** Resultado fica aqui, aguarda física nova.
- **Não reabrir** sem um gerador não-uniforme motivado por física, OU adoção explícita do
  programa de Janus pelo autor.

### Para o RESEARCH_MAP de TEIC (linha a acrescentar)
> **Seta do tempo cosmológica:** fronteira UNIVERSAL (Past Hypothesis), não dívida de
> TEIC. EXP 2 mostrou que a seta exige contorno de baixa entropia externo; FRONTEIRA_SETA
> _COSMOLÓGICA mostrou que nem Λ-dinâmica (transporte: V₄_past finito + E(z) importado),
> nem DEV (sem setor; vácuo DBI = equilíbrio), nem SR (poda postulada) a DERIVAM. Status
> idêntico a CST/SM. [FRONTEIRA FECHADA]

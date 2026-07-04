# Escala emergente em substratos causais: seis mortes, um mecanismo

**Data:** 2026-06-29 · `docs/campaigns/IMPOSSIBILIDADE_PARCIAL/`
**Natureza:** documento analítico (conjectura motivada por seis experimentos + meio-teorema). Não há experimento novo nesta tarefa.

> **Aviso de linguagem.** Este documento contém **um resultado rigoroso parcial** (a divergência da coordenação, §3.1) e **uma conjectura mais ampla** que ele apoia mas não fecha (§3.2–§3.4). A palavra "prova" é usada **apenas** para a parte rigorosa, sempre qualificada. A tese geral é uma **conjectura**, não um teorema.

---

## 1. Tese central

Toda regra de conexão definida exclusivamente em termos de quantidades **invariantes de Lorentz** entre eventos de um *sprinkling* de Poisson causal está sujeita a uma tensão fundamental:

- **ou** a regra carece de informação espacial fina suficiente para cortar os "atalhos de boost" — e então **herda a coordenação divergente do Poisson** (campo-médio tipo-Bethe, valência infinita);
- **ou** introduz dependência de referencial — e então **viola o princípio** (a invariância estatística do *sprinkling*) que é a única razão pela qual *causal sets* são um substrato relativístico legítimo.

As **seis mortes** documentadas no programa são instâncias desta tensão, cada uma atacando um eixo diferente. O ponto não-óbvio, estabelecido aqui, é que a parte de *coordenação* desta tensão é **um teorema** (§3.1), não um acidente empírico: ela decorre da **não-compacidade do grupo de Lorentz**.

---

## 2. As seis instâncias

| # | Família | O que foi modificado | Por que falhou (mecanismo) | O que revelou sobre a tensão |
|---|---|---|---|---|
| 1 | **Poisson** (`ESCALA_XI`) | nada — substrato base (links de cobertura do *sprinkling*) | ⟨z⟩ **diverge** com N; J_c→0, ξ sem onde morar | A divergência é a **não-localidade Lorentz-protegida**: a órbita de boost a Δτ fixo é não-compacta |
| 2 | **CSG** (`RIDEOUT_SORKIN_*`) | abandona o *sprinkling*; cresce por percolação transitiva (sem *embedding*) | passa a barreira-1 (⟨z⟩ finito) mas o grafo de cobertura é **tipo-árvore** (C4 sub-MF, livre de triângulos por teorema) | abandonar a medida invariante **compra** ⟨z⟩ finito mas **perde os laços** (cai do outro lado da tensão) |
| 3 | **CDT-equilíbrio** (`CDT_TEIC_FERRO`) | geometria dinâmica (Regge+Wick) + ferromagneto O(3) | reproduz a ordem (A), mas χ_max **lean mean-field** (B não-resolvido); z~13–15 alto | dinâmica de geometria reproduz ordem, **não baixa a valência efetiva** abaixo do MF |
| 4 | **CDT-NESS** (`NESS_GEOMETRIA`) | geometria **fora-do-equilíbrio** (drive paramétrico k₀(τ)) | escala aparente χ~N^0.53 era **ruído** (varredura de amplitude irreprodutível) → MF | um *drive* fora-do-equilíbrio **sobre a geometria** não altera a classe |
| 5 | **CDT-4D cinemático** (`CDT_4D_VIABILIDADE`) | gatilho cinemático em 4D (ensemble *stacked*) | *clustering* **decai para MF** (C4~N^−0.33); z satura finito mas rumo-árvore | subir para 4D **não arma** o gatilho |
| 6 | **Percolação de longo alcance** (`PERCOLACAO_LONGO_ALCANCE`) | regra de par **Lorentz-invariante** p(Δτ)=min(1,(Δτ/Δτ₀)^−σ) | ⟨z⟩ **diverge em TODO σ** E C4 < controle aleatório em 0/11 σ; gate de Lorentz verde | decair em Δτ **não corta os atalhos de boost** (Δτ é o invariante errado) |

**Leitura da tabela.** As linhas **1 e 6** são o lado "invariante-de-Lorentz ⟹ valência infinita" da tensão. As linhas **2–5** são o lado "abandonar a medida invariante ⟹ laços tipo-árvore / trivialmente Euler / MF mesmo assim". Nenhuma das seis fica do lado bom das **duas** barreiras ao mesmo tempo de forma conquistada.

---

## 3. A tensão formalizada

### 3.1 A parte rigorosa: coordenação invariante ⟹ valência infinita

**Afirmação (rigorosa, sob as hipóteses (i)–(iii) abaixo).** Seja Φ um *sprinkling* de Poisson de densidade ρ em M^d (Minkowski), e seja uma regra de conexão que liga dois eventos causalmente relacionados i≺j com probabilidade que é um funcional **Poincaré-invariante** de Φ. Então a valência esperada de um evento típico é

> ⟨z⟩ = ρ · Vol(H^{d−1}) · ∫₀^∞ Δτ^{d−1} q(Δτ) dΔτ ,

onde q(Δτ) é a probabilidade de conexão **marginalizada** sobre o resto do processo (uma função só de Δτ, por invariância) e H^{d−1} é o hiperbolóide unitário (a órbita de Lorentz a Δτ fixo). Como **Vol(H^{d−1}) = ∞** (o grupo de Lorentz é não-compacto), ⟨z⟩ = ∞ a menos que q ≡ 0 quase-sempre (regime trivialmente esparso, sem conexões).

**Esboço de prova.** Pela fórmula de Campbell–Mecke (Palm) do processo de Poisson, ⟨z⟩ = ρ ∫_{cone futuro} h(i,x_j) d^d x_j, com h(i,x_j) = E_Φ[1(i,x_j conectados)]. Tanto a lei do *sprinkling* quanto a regra são Poincaré-invariantes, logo h(g·i, g·x_j) = h(i,x_j) para todo g no grupo ⟹ **h depende apenas do invariante Δτ_ij** — inclusive para regras que dependem de toda a configuração de vizinhança (a dependência em k pontos é absorvida na média h). Decompondo a medida no cone futuro, d^d x = Δτ^{d−1} dΔτ dμ_{H^{d−1}}, e como h não depende da posição no hiperbolóide (seria dependência de referencial), a integral **fatoriza**: o fator hiperbólico Vol(H^{d−1}) sai como prefator infinito. ∎(esboço)

**Consequências.** (a) Mesmo a **relação de cobertura** (a própria fundação do *causal set*: q_cover(Δτ)=e^{−ρ c_d Δτ^d} > 0) tem valência infinita em M^d infinito — fato conhecido em CST como a origem da não-localidade dos *links*. (b) Numa caixa finita, Vol(H^{d−1}) é regularizado mas **cresce com o tamanho do sistema** (a faixa de rapidez acessível cresce), logo ⟨z⟩ **diverge com N** — campo-médio. Esta é exatamente a fenomenologia das linhas 1 e 6.

**O candidato mais próximo de exceção — N(i,j) — e por que também falha.** O número de eventos no intervalo de Alexandrov [i,j] parecia carregar informação espacial que Δτ não tinha. Não carrega: o volume do intervalo é fixado pelo próprio Δτ, V(i,j)=c_d Δτ^d, logo N(i,j) ~ Poisson(ρ c_d Δτ^d) e **E[N | Δτ] = ρ c_d Δτ^d é uma bijeção monotônica**. N(i,j) é um "termômetro ruidoso" de Δτ — a mesma variável disfarçada (verificado numericamente: E[N] cresce estritamente com Δτ, ∝ Δτ³ em 2+1D). Toda quantidade combinatória de par (comprimento da cadeia mais longa ≈ ρ^{1/d}Δτ, contagens de vizinhos comuns) é igualmente função de V ∝ Δτ^d. Todas caem em q(Δτ) e morrem pela mesma não-compacidade.

### 3.2 Hipóteses explícitas (o que falta para ser teorema da tese **inteira**)

A afirmação de §3.1 é rigorosa sob:
- **(i)** O substrato é um *sprinkling* de Poisson em M^d (ou sua medida é a invariante de Bombelli–Henson–Sorkin), com a correspondência discreto-contínuo **independente de referencial**.
- **(ii)** A regra de conexão é um funcional mensurável de Φ que usa **apenas** a ordem causal e contagens invariantemente definidas (sem coordenadas de *embedding*).
- **(iii)** "Campo-médio" é identificado com **valência esperada divergente** (Bethe).

Sob (i)–(iii), "⟨z⟩ divergente" é teorema. A **tese geral** ("nenhum substrato de ordem causal tem escala emergente") permanece **conjectura**, porque:
1. A regularização de caixa finita troca "∞" por "cresce com N" — operacionalmente MF, mas não literalmente ∞.
2. A hipótese (i) exclui medidas **não-Poisson / dinâmicas** (CSG, CDT), que de fato escapam da barreira-1 — ao custo da barreira-2.
3. §3.1 fecha a barreira de **coordenação**; a barreira de **clustering** (laços de dimensão finita) é argumentada separadamente, não pelo mesmo teorema.

### 3.3 O contraexemplo mínimo que falsificaria a tese

Uma regra de conexão sobre o *sprinkling* de Poisson em M^d que seja **Poincaré-invariante**, tenha **⟨z⟩ finito** no limite N→∞, conexões **não-triviais**, **e** *clustering* C4 de dimensão finita (acima do controle aleatório). §3.1 prova que tal contraexemplo **não pode existir na classe par/vizinhança-invariante** (exigiria h dependente da posição no hiperbolóide = quebra de invariância). Logo um contraexemplo só pode vir de **fora** de (i)–(ii): uma medida genuinamente não-invariante-mas-"covariante-em-sentido-fraco" (rótulo-invariante, como o CSG) ou uma dinâmica fora-do-equilíbrio que produza uma medida não-Poisson. Ambas as portas estão parcialmente exploradas (linhas 2–5) e caíram na barreira-2 ou em MF.

### 3.4 Duas aberturas honestas que este resultado **não** fecha

1. **Regras não-*pairwise* sobre medidas não-Poisson.** O argumento de Palm (§3.1) **estreita muito** esta porta — ele fecha a barreira de coordenação mesmo para regras de k pontos, *desde que a medida seja o sprinkling invariante*. O que sobra é: regras de configuração sobre uma medida que **não** seja o *sprinkling* de Poisson invariante (p.ex. construída autoconsistentemente por uma dinâmica). O CSG é o representante já testado dessa classe — e ele cai na barreira-2. Mas o espaço de tais construções **não** foi varrido exaustivamente; pode haver uma medida dinâmica cujo grafo de cobertura tenha laços de dimensão finita. Esta é a abertura mais concreta.
2. **Dinâmica genuinamente fora-do-equilíbrio para a geometria.** O NESS (linha 4) testou um *drive* paramétrico e morreu, e a semente de memória de matéria em equilíbrio morreu (FS-3D). Mas "fora-do-equilíbrio para a **geometria** em si", num sentido diferente do NESS aqui tentado (p.ex. um regime de relaxação transiente que nunca atinge estacionariedade, registrado como direção em [[teoria-cdt-nova]]), não foi testado.

Em ambas as aberturas, o ingrediente que falta é **explicitamente "além da ordem causal pura de pares num sprinkling de equilíbrio"** — exatamente o que §3.1 isola como insuficiente.

---

## 4. O que isto significa para programas de substrato causal

Não é que *causal sets* "não funcionem". É que a questão específica de **escala emergente** — fazer um comprimento de correlação divergir, uma classe de universalidade não-trivial emergir da contagem — pode exigir **um ingrediente além da ordem causal pura de pares**. O teorema parcial de §3.1 dá a esse "pode exigir" uma razão estrutural: a não-compacidade do grupo de Lorentz força valência infinita para qualquer regra invariante de par/vizinhança sobre o *sprinkling*. As construções que escapam (CSG, CDT) o fazem **abandonando** a medida invariante, e então encontram a barreira dos laços. As seis mortes não são seis acidentes independentes; são seis faces de uma única tensão entre **invariância manifesta** e **localidade efetiva finita**.

Isto é consistente com — e dá uma leitura microscópica a — práticas conhecidas em CST: os d'Alembertianos **não-locais** (suavização B_k) existem precisamente porque a valência de *link* é infinita; eles **importam** uma escala de suavização externa para recuperar localidade. O presente resultado sugere que essa importação não é um truque técnico, mas reflexo da mesma tensão.

---

## 5. Conexão com o DEV

O único resultado **positivo** robusto desta longa investigação é o **DEV** (a teoria escalar-vetorial-tensorial): ele funciona, faz fenomenologia de galáxias (MOND, BTFR), porque **não tenta derivar a escala do substrato** — importa a₀ como **parâmetro externo** (condição de contorno IR, a₀~cH₀) e faz física com ela.

A conexão com o resultado aqui é **sugestiva, não lógica**, e é importante ser preciso sobre isso. **Não** se afirma "o DEV está certo *porque* tentamos alternativas e falhamos" — isso seria uma inversão causal inválida (a falha de N tentativas não prova a correção da N+1-ésima). O que se afirma é mais fraco e mais honesto: a tensão identificada em §3.1 — que regras invariantes de par sobre o *sprinkling* não geram escala sem importá-la — fornece, **retrospectivamente**, uma *razão estrutural* para suspeitar que importar a₀ como ingrediente externo pode ser **a opção honesta**, e não apenas uma limitação provisória a ser removida por mais engenhosidade. É uma mudança de status da escala externa: de "buraco a ser tapado" para "possivelmente forçada pelo que sabemos sobre substratos causais". Continua sendo uma **suspeita motivada**, sujeita às aberturas de §3.4, não uma dedução.

---

## Apêndice — verificações

- **E[N(i,j)] monotônico em Δτ (∝ Δτ³ em 2+1D):** confirmado em `PERCOLACAO_LONGO_ALCANCE` (bins de Δτ, N=2000) — N cresce 0.04→41.6 estritamente; razão N/Δτ³ → ρc_d. Estabelece que N(i,j) é Δτ disfarçado.
- **⟨z⟩ diverge para todo q(Δτ) > 0:** confirmado empiricamente em `PERCOLACAO_LONGO_ALCANCE` (⟨z⟩ cresce com N em todos os 11 valores de σ, expoente local +0.39→+0.68, nunca satura) — a fenomenologia da fórmula de §3.1 com regularização de caixa.
- **Gate de Lorentz:** a mesma campanha verificou que regras em Δτ são bit-idênticas sob boost (η=0.8), confirmando a premissa de invariância de §3.1.

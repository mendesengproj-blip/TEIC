# TEIC — A Narrativa Canônica

> Este documento é a descrição física da teoria: o que acontece, em sequência,
> visto de dentro. Não há matemática pesada aqui — as equações, os números e os
> erros estão em `TEIC.md`, em `TEIC_DEV_CORRESPONDENCE.md` (a correspondência
> formal com a teoria efetiva), nos charters (`docs/prompts/`,
> `VACUUM_STRUCTURE.md`) e nos papers (`paper/`). Há, porém, uma regra de
> honestidade que vale em cada parágrafo: quando algo foi **derivado** (saiu da
> rede, medido, com guard anti-circularidade), dizemos derivado. Quando foi
> **identificado** (a rede produz a estrutura, mas a calibração ou a escala vem
> de fora), dizemos identificado. Quando foi **importado** (adicionado como
> hipótese), dizemos importado. A teoria tem um critério de morte ativo, e ele
> está na última seção.
>
> Estrutura: as dez perguntas do charter VACUUM_STRUCTURE, na ordem.
> Atualizado em jun/2026 (pós-campanha VS1–VS5).

---

## 1. O que é a rede causal? De que é feita?

De nada. Essa é a resposta honesta e é o ponto de partida.

Um **evento** é um centro de expansão causal: um "aqui-agora" do qual influência
pode se espalhar. Não há palco — não existe um espaço previamente dado onde os
eventos estão. Existe apenas a relação entre eles: o evento A pode ter
alcançado o evento B, ou não. Essa relação de alcance — quem está no futuro
causal de quem — é toda a estrutura. A rede não é feita *de* alguma coisa;
as coisas é que são feitas *da* rede.

Nenhum evento é privilegiado. Cada um é um centro de expansão; o universo é a
sobreposição de todos esses centros. Dessa imagem segue uma exigência técnica
que se revelou a decisão mais importante da teoria: os eventos têm de estar
distribuídos **ao acaso** (estatística de Poisson), não numa grade. Uma grade
tem direções preferidas; medimos que ela quebra a isotropia relativística em
17%, enquanto a distribuição de Poisson a preserva a 0.8%. E a contraparte
observacional existe: uma discretização regular do espaço-tempo produziria
dispersão de luz dependente de energia, que o Fermi-LAT já excluiu além da
escala de Planck. **Poisson não é uma conveniência de simulação; é a única
discretização que sobrevive, ao mesmo tempo, ao teste interno e ao limite
observacional.** (Derivado/medido; coincide com o teorema central da Causal
Set Theory, e dizemos isso sempre.)

Do contar de eventos emergem, sem que nenhuma fórmula relativística entre nos
geradores (um teste automático garante isso):

- **o tempo próprio** — o relógio de uma trajetória é quantos eventos ela
  atravessa em cadeia; a dilatação de Lorentz √(1−β²) emerge da contagem;
- **a dimensão** — quantos eventos cabem num diamante causal cresce com uma
  potência do tempo próprio, e o expoente *é* a dimensão (medimos 2.006 e
  4.004 onde devia dar 2 e 4);
- **a curvatura** — dois jeitos de medir o mesmo tempo próprio (cadeia mais
  longa vs volume do diamante) concordam no plano e divergem no curvo, e a
  divergência é exatamente o escalar de Ricci (coeficiente −1/96, 23.5σ).

Uma ressalva de honestidade estrutural: a *dinâmica* que faria a rede crescer
sozinha e escolher sua dimensão **não foi encontrada**. Testamos a regra de
crescimento natural da teoria até N=2000: os causets crescidos não são
variedades e a dimensão não converge para 3+1 (duas mortes pré-registradas,
pagas e reportadas). A rede, tal como a usamos, é um *ansatz* cinemático
validado — não um processo dinâmico derivado.

## 2. O que é o vácuo?

O vácuo é **a fase normal da rede**: eventos de Poisson em densidade uniforme
ρ₀, links portando fases sem holonomia líquida — e nada mais. Não é um meio,
não é um éter, e — isto agora está medido por três caminhos independentes —
**não é um condensado**.

A campanha da estrutura do vácuo (VS1, jun/2026) fez a pergunta diretamente:
sem nenhum vórtice inicializado, em alta densidade, a densidade causal
dinâmica escolhe espontaneamente um valor diferente do fundo? Resposta: não.
A estrutura de ρ é resposta linear pura à inomogeneidade que se impõe a ela
(ganho constante sobre 65× de amplitude de drive; correlação espacial fixa com
a fonte), e desaparece quando a fonte desaparece. Junto com PE2 (o campo
composto Φ não condensa) e PE4_V4 (a depleção de ρ não estabiliza vórtice
algum), isso fecha: **o análogo do Higgs não é uma propriedade espontânea do
vácuo da rede** — é um ingrediente genuíno do andar de cima.

O vácuo também não tem termodinâmica de fases acessível à dinâmica da teoria:
varremos a desordem do quench de ponta a ponta (VS2) e todos os parâmetros de
ordem variam suavemente — um crossover, nunca um salto. O que existe de
estrutura é mais interessante que uma transição: (i) abaixo de uma rigidez
crítica da geometria (K_c ≈ 8.5), o vácuo uniforme é *instável* — ruído
arbitrariamente pequeno cava depleções totais; a fase normal só existe em
geometria suficientemente rígida, um critério físico novo para um parâmetro
que era livre; (ii) esfriado de desordem forte, o vácuo congela num **plasma
de monopólos** — um estado vítreo com defeitos topológicos presos que não
relaxam. E há a assinatura de Poisson: qualquer região finita carrega
flutuação irredutível de densidade 1/√(ρV) — um Λ flutuante, de magnitude
10⁻¹²² em unidades de Planck no volume de Hubble (magnitude e sinal flutuante
herdados da CST/Sorkin, citados como tal; os coeficientes da resposta são
nossos, medidos).

E a gravidade vive aqui: quando uma fonte desequilibra a densidade, a rede
relaxa espontaneamente para o perfil 1/r — o potencial de Newton, sem nenhum
"1/r" em lugar algum do gerador (auditado: expoente estável, equação linear,
fontes estendidas dão Poisson genérico). A mesma contagem reproduz a dilatação
de Schwarzschild a 0.21%. O que não entrega: o valor de G em unidades físicas
(cavalga na granularidade, externa). O que entrega: o prefator adimensional
puro, G_net·ρ²·r_c⁵ → 15/8π², medido a 2.5%. Esse padrão — *forma derivada,
escala externa, número puro calculável* — repete-se em todos os setores, e
tratamo-lo como traço estrutural, não defeito a esconder.

## 3. O que é um fóton?

Primeiro, o que é a luz: a luz é a **borda da causalidade**. "Velocidade da
luz" não é uma propriedade de uma partícula que por acaso viaja rápido; é o
próprio limite do que pode alcançar o quê. Por isso c é exata e
universal — ela define a rede, não corre nela.

Sobre essa borda vive um grau de liberdade mínimo: cada **link** causal (a
relação elementar entre dois eventos) carrega uma fase. O conteúdo invariante
dessas fases é a holonomia — o quanto a fase falha em fechar quando se
percorre um circuito mínimo de links. Quando se faz a média dessa estrutura
sobre a rede de Poisson, o que emerge é exatamente o eletromagnetismo de
Maxwell: verificamos que a holonomia por unidade de área reproduz o campo
F_μν com correlação 1.0000. Um fóton, na linguagem da TEIC, é **uma onda de
holonomia de fase propagando na borda do cone causal**.

Dois adendos honestos. Primeiro: o *fóton quantizado* — o pacote com energia
ℏω — não é da rede; o ℏ pertence ao andar de cima (seção 10). O que a rede
deriva é o setor de Maxwell clássico e uma previsão rígida: como a rede de
Poisson é Lorentz-invariante em distribuição, **a dispersão de fótons no vácuo
é exatamente nula na média** — sem botão para acomodar um desvio. Qualquer
dispersão sistemática confirmada (CTA, LHAASO) mata a discretização de Poisson
e, com ela, o primeiro resultado da teoria. Segundo: a ameaça interna a esse
quadro (uma violação de Lorentz aparente de ordem 1 no setor vetorial,
E/B≈3) foi investigada até o fim e **morreu como artefato de regulador**:
toda plaqueta causal é um plano tipo-tempo (teorema exato), o ensemble é
covariante sob boost (medido), e a ação global ressoma a violação (defeito de
boost 0.98→0.003). Resta um resíduo de ~12% entendido e documentado, com kill
próprio registrado.

## 4. O que é a energia de um fóton?

A resposta honesta tem duas metades, e a fronteira entre elas é o resultado.

A metade da rede: energia é **taxa de contagem causal**. O relógio de um
objeto em movimento atravessa menos rede por tempo de coordenada; o fator
γ = 1/√(1−β²) emerge da contagem (R1), e E = m·γ é recuperado a <0.5% — mas
dizemos com a nota que o próprio experimento (E1) se deu: isso é uma
*releitura* de R1 multiplicada por uma escala de repouso m, não uma derivação
independente de energia. A aditividade (E_tot = E₁+E₂ para relógios que não
interagem) vale por construção — contagem de união disjunta é soma.

A metade que falta: **E = ℏω não é da rede.** A relação entre energia e
frequência exige a escala quântica, e medimos onde exatamente ela entra: a
fase por passo causal (e11 — a escala k = m/ℏ não pode vir da geometria; teria
de absorver uma dependência de densidade que a física não tem). O que a rede
*sustenta* é a leitura estrutural "ℏ = ação por evento causal": a fase de uma
estrutura de complexidade N escala como N (k ∝ N^1.008, R²=0.99997, T3C) —
consistência interna, não derivação. A energia do fóton, em uma linha: **a
forma relativística é contagem; o quantum é importado.**

## 5. O que acontece na colisão?

Depende do setor — e a sequência de respostas negativas e positivas é o mapa
mais informativo que a investigação produziu.

**Setor escalar, baixa energia:** nada. As duas cadeias se atravessam em
superposição linear exata (resíduo 0.0; cross-links só transientes). Sem
criação — o baseline limpo.

**Setor escalar, alta energia (regime DBI):** abaixo da fase crítica
(ρ_π = 18ρ₀) ainda pass-through; acima, a própria ação perde hiperbolicidade —
encontramos a fronteira de validade da descrição escalar, não criação. E o
winding é estruturalmente zero num campo de densidade (valor único, nada para
enrolar).

**Setor compacto:** a mesma dinâmica num campo de fase (S¹) nuclea **pares
kink-antikink que aniquilam** — o análogo de rede dos pares virtuais da QED.
Um kink carregado isolado não nasce do vácuo: winding se conserva. Regra de
seleção topológica, medida.

**Setor de gauge U(1):** a colisão **cria um vórtice** (W=1, em ~4 ticks) — e,
se a densidade causal é dinâmica, o núcleo do vórtice cava sua depleção
*espontaneamente, junto com o vórtice* (τ_dip < τ_vortex, medido em toda a
grade — PE4_V3). É o evento de "quase-matéria" da rede: estrutura topológica
nasce da colisão. Quase: o enrolamento difunde depois, porque nenhum termo de
cosseno vê um fluxo de 2π (seção 6).

**Setor SU(2):** colisões suaves **nunca alcançam B≠0** (|B| ≤ 0.41 em 20
sementes). A mesma topologia que torna o Skyrmion estável o torna difícil de
criar — setores topológicos não se conectam por evolução suave. A criação
dinâmica de matéria verdadeira é a fronteira aberta (FL3), e a colisão é
exatamente onde ela está.

## 6. O que é matéria?

Matéria é **um nó que a rede não consegue desatar**.

A história tem três atos, e os dois primeiros são negativos — o que é
informação, não fracasso. Primeiro ato: o campo escalar livre sobre a rede
(a "vibração" mais simples) **não forma matéria**: qualquer pacote se espalha
e se dissolve; medimos a dissolução. Segundo ato: com fases de link U(1)
(eletromagnetismo), a rede em 3+1D forma um vácuo rico — um plasma de
monopólos, confinamento com tensão de corda linear — e colisões criam
**vórtices topológicos** que quase persistem. Quase: o núcleo do vórtice
difunde, porque um fluxo de 2π é invisível para qualquer medida de fase
compacta (cos 2π = 1 — provamos que *toda* função de classe de U(1) é cega ao
núcleo). U(1) tem topologia, mas não tem como *pagar* o custo do núcleo que a
estabilizaria.

Terceiro ato: o grupo mínimo seguinte, SU(2). Aqui não foi escolha — foi
**cadeia de eliminação medida**: o escalar não tem nada para enrolar; os
grupos discretos colapsam a carga em paredes de domínio divergentes (medido);
U(1) é cega ao núcleo (teorema + medida); SU(2) suporta um sóliton pontual
com carga inteira protegida; e acima de SU(2) nada novo é necessário (todo
grupo maior contém um SU(2) e a mesma topologia). Com SU(2), a rede sustenta
um **Skyrmion**: uma textura em que o campo "enrola" o espaço inteiro uma vez
(carga topológica B=1, conservada porque desenrolar exigiria passar por uma
barreira que medimos crescer sem limite sob refinamento — em d=3; em d=2 o
mesmo objeto desenrola suavemente). Esse objeto tem massa finita, gravita com
o 1/r do setor gravitacional, e é o candidato da teoria a "partícula de
matéria": os números quânticos de um bárion.

A surpresa genuína da campanha: o **operador de Skyrme** — o termo que a
literatura de redes regulares sempre precisou adicionar à mão para estabilizar
o sóliton — **emerge sozinho** do coarse-graining da ação mínima sobre a rede
de Poisson, com coeficiente travado e comprimento fixado pela granularidade.
E emerge *pela mesma razão* que a relatividade especial emerge: a isotropia de
Poisson. Uma grade cúbica é exatamente cega a ele (medimos: razão 1.0 a
precisão de máquina). O mesmo ingrediente que dá Lorentz dá o estabilizador
de matéria.

A fronteira honesta: o operador emerge, **a dominância não**. A própria
isotropia trava a razão entre o termo estabilizador e o termo saturante de
modo que o quártico líquido nunca estabiliza sozinho; falta um custo de núcleo
que a ação de cossenos não contém. Duas campanhas independentes (uma pela
topologia, outra pela energética) localizaram **a mesma fronteira**: o único
ingrediente de matéria genuinamente importado da teoria é esse custo de
núcleo. Não três ingredientes, não nenhum: **um**, nomeado, com critério de
morte registrado. E a campanha do vácuo acrescentou a contraprova de cima:
nem em alta densidade, nem em regime mole, o substrato fabrica esse
ingrediente sozinho (VS1 — três vias independentes fechadas).

Sobre as **três gerações** (a pergunta VS4): testamos se o setor B=1 esconde
múltiplos mínimos de energia — três maneiras de enrolar o mesmo nó, com massas
diferentes. Não esconde: dez perfis iniciais radicalmente distintos (energias
iniciais cobrindo duas ordens de magnitude, excursões não-monotônicas
incluídas) relaxam todos para **a mesma massa, a 0.02%**. Uma bacia só.
Se múon e tau existem na linguagem da rede, não são bacias topológicas — o
candidato honesto que resta é o espectro da quantização coletiva (excitações
do *mesmo* objeto, a rota que a literatura de Skyrme usa para N e Δ), que é
camada quântica, ainda não testada.

## 7. O que é a massa?

Três camadas, com status diferentes — e a distinção entre elas é o resultado.

**Inércia do campo livre: não existe.** Medimos m = F/a para o pacote escalar
livre e a aceleração mal responde à força, dominada por artefato (M1, morte
paga). O campo livre da rede não tem nada que acelere como partícula — por
isso matéria precisou de topologia (seção 6).

**Massa como custo causal: derivada.** Uma região com estrutura interna
consome mais eventos — relógios ali atravessam mais rede. É *isso* que
gravita: colocada a fonte, a rede se adensa em 1/r (seção 2). A massa
gravitacional é o custo causal da estrutura, e o experimento de complexidade
(CC1–CC6) mediu o custo crescer com a estrutura e gravitar
proporcionalmente.

**Massa de repouso de uma partícula: a energia do nó.** O Skyrmion tem massa
finita M ≈ 146–207 (unidades de rede), que é literalmente a energia E2+E4 da
textura — e gravita proporcionalmente a ela (Q6). O virial de Derrick
(E2=E4, medido a 1%) é o que a sustenta. E há uma única massa por setor
topológico (VS4) — sem espectro de gerações na camada clássica.

O que nenhuma camada entrega: **o valor das massas em quilogramas** — escala
absoluta, externa, como sempre. E o espectro das partículas reais (por que o
elétron pesa o que pesa) está dois andares acima: exige a quantização
coletiva e o Modelo Padrão na rede (Nível 4, aberto).

## 8. O que é a carga elétrica?

O que a rede tem de carga é **topologia de enrolamento**: o winding da fase
de gauge ao redor de um defeito (W do vórtice, a carga magnética dos
monopólos no vácuo confinante, o B do Skyrmion). Essas cargas são inteiras e
conservadas *por construção topológica* — a quantização da carga, na rede, é
um teorema, não um mistério. [DERIVADO nesse sentido preciso.]

O que a rede **não** tem: a carga *elétrica* como número de acoplamento — o
"e" que mede quão forte o defeito puxa o campo de Maxwell. O peso do setor de
gauge (λ_p) é livre na rede exatamente como K é livre na teoria efetiva (W4);
e α = e²/ℏc contém ℏ, que é do andar de cima. A campanha VS5 fechou a porta
do atalho: as constantes de acoplamento (α, sin²θ_W, g_s) **não** emergem de
combinações dos quatro números puros da rede acima do nível do acaso — 2400
combinações testadas contra controle de look-elsewhere; os "acertos" de 0.14%
são exatamente o que o acaso produz nessa densidade de busca. A identificação
"carga elétrica = winding de gauge do defeito" fica como [IDENTIFICADO];
o valor de e fica [EM ABERTO], no Nível 4 com o resto do Modelo Padrão.

E o neutrino (a pergunta VS3): a rede suporta um objeto com a marca de
spin-½ mas *sem* carga de gauge? Testamos a "bola de torção π" — uma
configuração que carrega a estrutura de cobertura dupla (o caminho 1→−1,
o gerador de spin-½) mas com winding topológico zero e carga zero. Ela
**desenrola para o vácuo exatamente como uma perturbação trivial** (descida
monótona de energia, sem plateau), enquanto o Skyrmion protegido (B=1)
segura seu marcador por toda a relaxação. A lição: a marca de spin-½ vive
num grupo (π₁ de SO(3)) que *não* protege; quem protege é a carga
topológica B (π₃), e ela só vem do nó completo — que carrega os números
de um bárion. Spin-½ estável e carga estão amarrados na rede; um neutrino
neutro de vida longa não emerge deste setor (kill disparado).

## 9. De onde vem o spin-½?

Do fato de que **trocar dois nós de lugar e girar um nó por uma volta completa
são o mesmo laço** — e a rede sabe disso.

O Skyrmion clássico tem massa e carga, mas spin-½ é uma propriedade de fase:
um objeto que só volta a si mesmo após *duas* voltas. O caminho clássico para
isso é o argumento de Finkelstein–Rubinstein: se o laço de "girar 2π" é
topologicamente não-trivial no espaço de configurações, a quantização pode
atribuir-lhe fase −1, e o sóliton quantiza como férmion. A pergunta da TEIC
foi: quanto disso a rede *mede*, em vez de assumir?

A resposta, hoje: quase tudo que é físico. Medimos na rede que o laço de troca
de dois Skyrmions fecha; que a troca é exatamente uma meia-volta rígida (a
identidade vale ponto a ponto, a erro de máquina); que girar 2π arrasta a
coordenada coletiva ao seu antípoda — o invariante que vira a fase −1. E na
campanha final, computamos as classes de homotopia diretamente na rede:
**[troca] = [rotação-2π] = 1 no grupo π₁ = ℤ₂**, com a 2-torção (4π = nada,
troca² = nada) e o caso bosônico (girar o *par* = nada) também medidos. A
identificação de Finkelstein–Rubinstein deixou de ser teorema citado e virou
igualdade entre dois números medidos — com uma condição declarada: a leitura
da classe de troca exigiu um calibrador de topologia (ε_swap), validado num
caso de classe conhecida; um segundo calibrador independente está registrado
como experimento futuro e removeria essa ressalva.

O que segue importado, dito sem disfarce: a topologia algébrica de livro-texto
(π₄(S³)=ℤ₂) e **a própria regra de quantização** — o passo "laço não-trivial ⇒
fase −1 ⇒ espectro de rotor com j=½" é o procedimento padrão de quantização
coletiva, aplicado de fora. A rede fornece todas as premissas mecânicas;
não fornece a mecânica quântica.

## 10. O que está além da rede?

A fronteira foi mapeada com precisão, e tem nome: **a escala quântica**.

A rede deriva a *forma* da interferência — a geometria da diferença de
caminhos num experimento de duas fendas sai da contagem causal a 0.8% — e até
o ingrediente "algo que oscila com sinal" (os pesos alternantes do operador
causal). O que ela não fornece é o *mapa* entre diferença de passos causais e
ângulo de fase: a escala k = m/ℏ. Medimos que essa escala não pode vir da
geometria (ela teria de absorver uma dependência de densidade que a física não
tem). E fechamos um refinamento tardio: a fase de uma estrutura de
complexidade N escala como N (k ∝ N, medido com R²=0.99997) — o que sustenta a
*leitura* "ℏ = ação por evento causal" como consistência interna, mas a escala
absoluta de ℏ segue externa, e dizemos por quê: é o mesmo padrão de todos os
setores (forma derivada, escala externa).

Há, portanto, **dois andares**. O andar de baixo é a rede: geometria,
gravitação, o setor de Maxwell, a topologia da matéria, as premissas do
spin-estatística — tudo clássico, real, contável. O andar de cima é quântico:
ℏ, a regra de Born, a quantização como procedimento, a magnitude de Higgs
(VS1 provou que o substrato não a fabrica), as constantes de acoplamento
(VS5 provou que não são aritmética dos números puros). A teoria não finge
derivar o andar de cima; ela localiza a escada. Também ficam de fora, por
ora: o valor físico de G, de a₀ e das massas (só os números puros
adimensionais são calculáveis); a dinâmica de crescimento da rede (as duas
mortes do Tier 3); o Modelo Padrão (não há espectro de massas, carga elétrica
como acoplamento, sabor — há um objeto com os números quânticos de *um*
bárion, uma bacia só no seu setor topológico).

## Onde a teoria pode morrer

Este é o traço que mais prezamos, então fecha a narrativa.

A camada efetiva da teoria — a que conecta a rede à dinâmica galáctica — faz
uma previsão que nenhuma teoria padrão faz: **a massa bariônica fixa, galáxias
giram mais rápido no passado**, com Δlog v = ¼·log[H(z)/H₀]. ΛCDM prevê
exatamente zero. O critério de morte está pré-registrado, com números: uma
amostra de ≥25 rotadores ricos em gás a z≥2, no regime de baixa aceleração,
com sistemáticos ≤0.03 dex, medindo Δlog v ≤ 0, **mata o setor galáctico sem
apelação** — o critério já inclui os sistemáticos.

Estado em junho de 2026: o primeiro dado no regime certo (MUSE-DARK III, 79
galáxias, z até 1.44) mede a₀ **crescendo** com z — a direção que a previsão
exige — com amplitude consistente com ¼log[H/H₀] dentro do sistemático de
âncora (0.5–0.9σ na âncora SPARC). Quem está a ~19σ desse dado é a evolução
nula. Não chamamos isso de confirmação: o regime decisivo (z≥2) ainda não foi
medido, a forma exata da evolução está indecidida, e uma leitura rival pelo
eixo de massa (Jeanneau+2026) ainda discorda. A vigília está declarada.

As outras duas formas de morte são herdadas da estrutura e não têm botão de
ajuste: qualquer desvio confirmado da velocidade das ondas gravitacionais
(c_T ≠ c) mata a seleção de operadores inteira; qualquer dispersão
sistemática de fótons no vácuo mata a discretização de Poisson. E há a morte
interna: qualquer rede futura que meça o acoplamento gravitacional e o
comprimento de Skyrme na mesma configuração e não encontre o número puro
3/320π² derruba a relação cruzada que amarra gravitação e matéria.

---

## O parágrafo final (a tese, do tamanho certo)

Uma rede de eventos causais distribuídos ao acaso — e nada mais — gera a
relatividade especial, a dimensão, a gravitação de Schwarzschild e a curvatura
(coincidindo, em todo o setor geométrico, com a Causal Set Theory, por uma
rota conceitual independente). Além desse chão, e além do que a CST possui, a
mesma rede seleciona a estrutura de operadores de uma teoria efetiva de
gravitação testada em rotação galáctica, proíbe exatamente as classes de
operadores que GW170817 e Fermi-LAT executaram, seleciona d=3 por exclusão
estrutural medida, seleciona SU(2) por cadeia de eliminação medida, gera o
operador de Skyrme pela mesma isotropia que gera Lorentz, e mede as premissas
do spin-estatística do seu sóliton — restando, nomeados e contados, um
ingrediente de matéria (o custo de núcleo, que o vácuo comprovadamente não
fabrica sozinho), uma regra de quantização e as escalas absolutas. Nada foi
forçado; cada negativo está reportado; e a teoria mantém, ativo e
pré-registrado, o critério da própria morte.

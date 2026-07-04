# C3-4 -- Comparacao qualitativa com o experimento do Polaris (Ding et al. 2025)

> Analise **qualitativa**, sem codigo novo (protocolo C3-4).

## O que o Polaris mediu

O experimento (Polaris + lattice QCD, Ding et al. 2025) mapeou as Generalized
Parton Distributions (GPDs) do **pion** em 3D. Uma descoberta central: o
**tamanho transversal** do pion **decresce com o momento** -- ao ser "chutado",
a distribuicao de partons se estreita na direcao transversal ao boost.

## O analogo na TEIC

Na TEIC o pion nao existe diretamente (SU(3) nao derivado -- ver FL1). O objeto
candidato a barion e o **Skyrmion B=1**. A pergunta C3-4: ao dar um boost ao
Skyrmion, o seu tamanho transversal decresce com o momento, como no Polaris?

Tres ingredientes ja estabelecidos no programa respondem **qualitativamente
SIM**, por um mecanismo puramente cinematico:

1. **Estrutura causal => contracao de Lorentz.** A relatividade especial da
   TEIC nao e postulada: emerge da rede causal (Papers I-III; FN3b mostrou que a
   rigidez vem do "boundary-pinning" do cone causal, e que E = mc^2 vale). Um
   Skyrmion em movimento com velocidade v ao longo de x sofre contracao
   **longitudinal** por 1/gamma = sqrt(1 - v^2/c^2): a sua extensao **ao longo do
   boost** encolhe. A extensao transversal (perpendicular ao boost) e
   invariante de Lorentz.

2. **Tamanho proprio finito (E3b).** E3b mediu o raio efetivo do defeito como
   **r_eff ~ 0.32 L** (tamanho finito, nao colapsa nem dispersa -- o Skyrmion e
   um PONTO estavel com nucleo de tamanho proprio bem definido). E o "tamanho de
   repouso" que o boost depois contrai.

3. **GPDs sao distribuicoes no plano transverso vs. o momento longitudinal.**
   A observavel do Polaris (largura transversal vs momento) mistura o eixo do
   boost com o plano transverso. Sob boost, a densidade de carga barionica
   `baryon_density(U)` -- que e exatamente o que a TEIC computa -- e a densidade
   de winding de pi_3; ela se reorganiza no referencial boostado pela mesma
   contracao de Lorentz longitudinal. O perfil **projetado** no plano de impacto
   (impact parameter) estreita com o momento, reproduzindo qualitativamente a
   tendencia do Polaris.

## Onde a analogia e solida e onde nao e

**Solida (cinematica):** a contracao do Skyrmion boostado segue a contracao de
Lorentz que a TEIC ja deriva (M2_lorentz_mass, FN3b). A direcao da tendencia --
estreitamento com o momento -- e a mesma do Polaris, e e geometria, nao um
parametro ajustado.

**Nao solida (dinamica de partons):** o Polaris mede uma distribuicao de
**partons** (quarks/gluons, setor SU(3) com graus de liberdade de cor). A TEIC
descreve a mesma regiao do espaco como um **soliton topologico** de um unico
campo SU(2), sem partons. As duas linguagens descrevem o mesmo objeto (o
barion/pion de menor massa) mas a estrutura interna **detalhada** -- a forma
funcional exata da GPD, a dependencia em x de Bjorken -- pertence ao setor SU(3)
nao derivado. A TEIC reproduz a **tendencia geometrica**, nao o **conteudo
partonico**.

## Relacao com o veredito C3 (Regge)

C3-1/C3-2 mostraram que o espectro **rotacional** do Skyrmion e a lei de Casimir
do rotor rigido, nao a lei de Regge de corda. Coerentemente, a estrutura
**espacial** sob boost aqui (C3-4) e a de um corpo rigido contraido por Lorentz,
nao a de uma corda relativistica que se estica. As duas observacoes apontam para
a mesma fisica: **o Skyrmion da TEIC e um corpo rigido topologico**, nao uma
corda hadronica. Reproduz a topologia e a cinematica do barion; o espectro de
corda (Regge) e o conteudo partonico (Polaris detalhado) ficam no setor SU(3).

## Conclusao C3-4

Qualitativamente **SIM**: o Skyrmion boostado estreita transversalmente com o
momento, pelo mesmo mecanismo de contracao de Lorentz que a TEIC deriva da rede
causal, partindo do tamanho proprio finito de E3b (r_eff ~ 0.32 L). A analogia
com o Polaris e **cinematica e direcional**, nao partonica. Nenhuma simulacao
nova foi rodada (protocolo).

# C3-5 -- Sintese honesta: Trajetorias de Regge dos Skyrmions

Campanha `C3_REGGE_SKYRMIONS.md`. Motor reutilizado **sem modificacao**:
`su2q_core.py` / `su2_core.py` (SU2_QUANT + MATTER_SU2), `pi1_core.py` (B>=2).
Resultados em `results/matter/c3/`. Nenhuma campanha anterior foi tocada.

## Quadro de resultados

```
C3-V (gate):
  Momento de inercia I bem definido?         SIM  I = 312.74 (rede)
  I finito, positivo, esferico?              SIM  (spread 0, offdiag ~1e-18)
  Cross-check FR (2pi -> -psi, SU2_QUANT)?   SIM  (residuo 5.1e-16)

C3-1 (espectro, 10 sementes):
  m^2(J) linear em J?                        NAO  R^2 = 0.9626 (< 0.99)
                                                  residuos quadraticos + - - - +
  m^2(J) linear em J(J+1)?                   SIM  R^2 = 1.0000000
  Inclinacao de Casimir alpha_C:             0.95023 +/- 0.00235 (rede)

C3-2 (tensao de Regge):
  alpha' de Regge VERDADEIRA:                INDEFINIDA (lei nao e linear em J)
  alpha_C (Casimir, rede):                   0.95023  (= E_class/I)
  alpha_C em GeV^-2:                          NAO CONVERTIVEL (escala nao derivada)
  Comparavel a alpha'_QCD = 0.9 GeV^-2?      INDETERMINADO (lei diferente)

C3-3 (multi-Skyrmion B=1,2,3):
  Forma universal (Casimir, nao Regge)?      SIM  (R^2 identico em todo B)
  Universalidade NUMERICA de alpha_C?        INDETERMINADO (ansatz nao relaxado)
```

## VEREDITO: **C -- MORTE: m^2(J) NAO E LINEAR EM J**

O criterio de morte pre-registrado foi **acionado**. O espectro rotacional do
Skyrmion da TEIC e a **lei de Casimir do rotor rigido**

> E_J = E_class + J(J+1)/(2I),  m^2 = E_J^2  propto  J(J+1),

e **nao** a lei de corda de Regge m^2 = alpha' J. O ajuste linear em J tem
R^2 = 0.9626 (abaixo do limiar de sucesso 0.99) com residuos sistematicamente
quadraticos (sinais + - - - +); o ajuste em J(J+1) e perfeito (R^2 ~ 1.0000000).

A identificacao **[IDENTIFICADO] Skyrmion <-> barion permanece** -- nao passa a
[DERIVADO] pela via do espectro de Regge.

## Por que isto era esperado (e e fisica correta, nao um bug)

A quantizacao **coletiva de corpo rigido** trata o Skyrmion como um rotor
indeformavel: a energia rotacional e o Casimir J(J+1)/(2I). Como a massa de
repouso m = E_J, m^2 e necessariamente **quadratico em J** -- nunca linear. A
lei de Regge linear (m^2 propto J) surge num regime **diferente**: quando o
soliton **se deforma** e se estica numa corda rotativa relativistica a J alto
(a velocidade da borda -> c), regime que a aproximacao de corpo rigido **omite
por construcao**. Este e um resultado conhecido do modelo de Skyrme; a TEIC o
reproduz fielmente.

C3-4 (qualitativo) e coerente: sob boost o Skyrmion se contrai como um **corpo
rigido** de Lorentz (a partir do tamanho proprio r_eff ~ 0.32 L de E3b), nao
como uma corda que se estica. Espectro **e** estrutura espacial apontam para a
mesma conclusao: **o Skyrmion da TEIC e um corpo rigido topologico**, nao uma
corda hadronica.

## O que morreu e o que sobrevive

**Morreu:** a esperanca de derivar a trajetoria de Regge (e portanto a tensao de
corda alpha' ~ 0.9 GeV^-2 e o contato direto com o experimento do Polaris) a
partir do **rotor rigido** do Skyrmion da TEIC. O espectro de hadroes, no nivel
de corda/Regge, requer o setor SU(3) + QCD (FL1) ou um Skyrmion **deformavel**.

**Sobrevive (e fica mais preciso):**
- A identificacao topologica Skyrmion <-> barion (B=1, spin-1/2 via FR) intacta.
- O espectro rotacional **correto** de baixo J (a lei de Casimir e a fisica
  certa do rotor rigido; e o que o modelo de Skyrme preve).
- Uma caracterizacao nova e honesta: o Skyrmion da TEIC e **pesado e rigido**
  (a banda rotacional inteira fica a (E_(1/2)-E_class)/E_class ~ 4e-6 da massa),
  o regime **oposto** ao das cordas hadronicas leves de QCD.

## Caminho a frente (se alguem quiser ressuscitar Regge)

A unica rota fisica para m^2 propto J e abandonar o corpo rigido: quantizar um
Skyrmion **deformavel / cranked** que se alonga com J ate o regime de corda
rotativa. Exige (i) cooling 3D estavel para B>=2 (o stencil e4 atual e instavel),
(ii) um termo estabilizador de tamanho transversal sob rotacao. E uma campanha
distinta (matter, proxima FN4 -- o termo de Skyrme como estabilizador faltante),
nao um conserto desta. Registrado e reportado.

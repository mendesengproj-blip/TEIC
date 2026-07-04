# HQ3-5 — Síntese honesta: o m_A da DEV vs NANOGrav 2023

> Campanha HQ3_NANOGRAV. O campo vetorial massivo m_A — a matéria escura fria da
> TEIC+DEV (FM4, FN3) — é consistente com o sinal de ondas gravitacionais detectado
> pelo NANOGrav em 2023? Teste, não ajuste: m_A vem do Paper II (galáxias), não do PTA.

## Quadro de resultados

```
HQ3-1 (frequência):
  m_A com f_GW na banda PTA existe?        SIM
  Range compatível:                        4.1×10⁻²⁴ a 1.2×10⁻²² eV (overlap c/ Paper II)

HQ3-2 (amplitude):
  Linha KR (100% DM local) compatível?     ROÇA o limiar só em m_A≈4–10×10⁻²⁴ eV (Ψ_c/h_c~0.1–1)
  Linha KR (subdominante, Lyman-α)?        ABAIXO do limiar
  SGWB que se propaga (Ω_GW)?              ~21 ordens ABAIXO de 8×10⁻⁹  →  NÃO é o fundo NANOGrav
  Valor calculado (teto Ω_GW):             1.4×10⁻²⁹
  Valor observado (Ω_GW NANOGrav):         8.1×10⁻⁹

HQ3-3 (forma espectral):
  Espectro do m_A compatível com SGWB?     NÃO (linha monocromática vs lei de potência)
  Índice do m_A:                           γ→∞ (linha, Δf/f~10⁻⁶)
  Índice do NANOGrav:                      γ≈13/3=4.33

HQ3-4 (limites):
  BBN OK?                                  SIM (ΔN_eff~10⁻²⁴)
  CMB OK?                                  SIM (Ω_GW h²~10⁻³⁰)
  Sólitons (1.3e-21–1.4e-20 eV)?           não afeta (banda abaixo)
  Lyman-α?                                 força m_A subdominante na banda (rebaixa amplitude)
```

## VEREDITO: **B — PARCIALMENTE CONSISTENTE**

```
[ ] A — CONSISTENTE COM NANOGRAV (fundo SGWB)
        Exigiria f_GW na banda + Ω_GW compatível + forma γ=13/3 + limites OK,
        simultaneamente. FALHA em DOIS: (i) o m_A é uma LINHA, não o contínuo que o
        NANOGrav detectou; (ii) o SGWB que ele irradia está ~21 ordens abaixo. Um
        condensado homogêneo não irradia gráviton on-shell — não pode ser o fundo.

[X] B — PARCIALMENTE CONSISTENTE
        A FREQUÊNCIA bate: 4.1×10⁻²⁴–1.2×10⁻²² eV do Paper II produzem f_GW na banda
        do PTA (~2/3 da janela, em log). E o MESMO m_A produz uma oscilação métrica
        monocromática (Khmelnitsky–Rubakov) cuja amplitude ROÇA a sensibilidade atual
        do PTA na ponta de massa baixa (Ψ_c/h_c ~ 0.1–1 se 100% da DM local). Mas:
        amplitude e forma NÃO batem com o SGWB detectado — é um sinal DIFERENTE
        (raia, não fundo), e Lyman-α empurra o m_A para subdominante, rebaixando a
        amplitude abaixo do limiar. "Frequência certa, amplitude/forma do SGWB não."

[ ] C — INCOMPATÍVEL
        Não no sentido forte: a frequência cai na banda e nenhum limite duro é
        violado. O m_A simplesmente não EXPLICA o sinal NANOGrav 2023 — mas isso já
        era esperado (o SGWB tem explicação dominante por SMBH).
```

## Leitura honesta do veredito

**O que é verdade e robusto.** A frequência. Ela depende só de m_A (galáxias, Paper
II) e de h — zero ajuste. E é notável: a janela de massa que a DEV fixou por dinâmica
estelar **coincide** com a banda em que os PTAs operam. Massas de 4×10⁻²⁴ a 10⁻²² eV
caem direto em [2×10⁻⁹, 10⁻⁷] Hz. Isso não é coincidência forçada — é a mesma física
ultraleve que faz a DM "fuzzy" ser procurada por PTAs (Khmelnitsky–Rubakov 2014; caso
vetorial arXiv:2412.12975).

**Por que B e não A — a separação de dois sinais.** O prompt mistura dois observáveis
que a física separa:
- A **linha KR** (oscilação local da métrica, Ψ_c = πGρ/ω²) é o observável **real** de
  PTA para DM ultraleve. Frequência na banda; amplitude ~10⁻¹⁴–10⁻¹⁵ que **roça** o
  limiar do NANOGrav só no melhor caso (100% da DM local, massa baixa).
- O **SGWB que se propaga** — o que o NANOGrav de fato detectou (Hellings–Downs,
  γ=13/3) — **não** vem do m_A: um condensado homogêneo não irradia gráviton on-shell,
  e o fundo das suas flutuações está ~21 ordens abaixo. A fórmula "Ω_GW h² ~ 10⁻⁶" do
  prompt pertence a um mecanismo **diferente** (produção taquiônica/paramétrica de
  fóton escuro), **não** ao misalignment do m_A (FM4/FN3); usá-la aqui seria
  superestimar por ~25 ordens. Reportamos honestamente o teto correto.

**Por que não C.** Nada é falsificado: a frequência está na banda, BBN/CMB/sólitons
OK. O m_A não explica o SGWB do NANOGrav, mas o SGWB tem explicação dominante (SMBH) —
não se esperava que o m_A fosse essa fonte. O que sobra é positivo: uma **segunda
janela observacional** (raia de PTA) onde a DEV faz uma previsão distinta e testável.

**A previsão viva que HQ3 deixa.** Se o m_A for uma fração não-desprezível da DM local
numa massa de 4–10×10⁻²⁴ eV, os PTAs verão (ou limitarão) uma **linha monocromática**
em f_GW = 2m_A c²/h ≈ 2–5 nHz — distinta, em forma e correlação, do fundo de SMBH. As
buscas de DM ultraleve do NANOGrav/EPTA já operam exatamente nessa banda; HQ3 mapeia
onde a DEV cai dentro delas.

## Posição no programa

| Componente | Origem | Status |
|---|---|---|
| Fóton | E2 (mágnon BD, ω=ck) | derivado |
| MOND / galáxias | Paper I–IV + ν de FM2-1 | ajustado a SPARC |
| Matéria escura fria | FM4-1 (m_A, w=0) | existe (w=0 confirmado) |
| Abundância da DM (Ω~0.12) | FN3 (misalignment) | alcançável c/ f_A~10¹⁷ GeV (B) |
| **Sinal de PTA (linha KR)** | **HQ3 (oscilação métrica do m_A)** | **frequência na banda (B); não é o SGWB do NANOGrav** |

**Avanço de HQ3:** transforma o m_A — já estabelecido como DM fria (FM4) com
abundância plausível (FN3) — numa **previsão de PTA**. Não é uma terceira confirmação
livre-de-ajuste (seria preciso o Veredito A, e o SGWB detectado não é do m_A), mas
abre uma **segunda frente observacional** (depois da BTFR em galáxias): uma raia de
nanohertz cuja frequência a DEV fixa sem ajuste.

## Anti-circularidade e disciplina

m_A da janela do Paper II (galáxias + GW170817); a frequência e a amplitude vêm da
dinâmica do campo; a banda do PTA, A_yr=2.4×10⁻¹⁵, γ=13/3 e ρ_DM local são
**COMPARISON ONLY** — nada inserido para mover m_A. Critério de morte pré-registrado:
"Ω_GW << observado OU frequência fora da banda OU forma incompatível". A interpretação
**SGWB** aciona DUAS dessas (Ω_GW 21 ordens abaixo + forma de linha vs contínuo) — e
isso foi reportado, não escondido. O que salva o veredito de C é o observável
**correto** (a linha KR), cuja frequência está na banda e cuja amplitude roça o limiar:
"amplitude ou frequência compatível, mas não os dois simultaneamente" → **B**, como
pré-registrado. A fórmula Ω_GW~10⁻⁶ do prompt (mecanismo errado) foi corrigida, não
usada para inflar o resultado.

## Limitações declaradas

- Ψ_c de Khmelnitsky–Rubakov com coeficiente O(1) ambíguo (πGρ/ω² 1ºpr vs ~2×10⁻¹⁵
  da literatura, fator ~4): potencial vs strain vs resíduo, o fator 2 do 2ω. A
  conclusão (roça o limiar só na ponta de massa baixa) é robusta a esse fator.
- ρ_DM local = 0.4 GeV/cm³ (valor padrão do halo); a fração subdominante imposta por
  Lyman-α (FM4/FN3) é o que de fato rebaixa a amplitude — declarada, não absorvida.
- Teto do SGWB (~Ψ_c²) é deliberadamente generoso; o valor real é muito menor. A
  direção (m_A não é o fundo NANOGrav) é robusta por ~20 ordens de margem.
- Caráter vetorial (3 polarizações) tratado como modulação O(1) de stress anisotrópico
  sobre a linha; um cálculo completo de polarização mudaria coeficientes, não a forma
  (linha) nem a banda (frequência).

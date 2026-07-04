# FN3-5 — Síntese honesta: a densidade relíquia do m_A

> Campanha FN3_RELIC_DENSITY. Quanto m_A existe hoje? Ω_{m_A} h² ≈ 0.12 usando os
> parâmetros do Paper II (galáxias), sem ajuste ao CMB?

## Quadro de resultados

```
FN3-1 (analítico):
  Ω_{m_A} h² ≈ 0.12 possível na janela do Paper II?    SIM
  Para quais (m_A, f_A)?    f_A = (1–4)×10¹⁷ GeV (escala GUT), toda a janela de massa

FN3-2 (numérico):
  Concorda com o analítico?    SIM, dentro de fator ~2 (onset O(1))
  Ω_{m_A} h² medido numericamente:    0.067 no f_A da linha de 0.12 (w_cauda≈0, frio)

FN3-3 (f_A da DEV):
  f_A determinável sem parâmetro livre?    NÃO
  f_A estimado:    ~10¹⁷ GeV REQUERIDO (livre); Stückelberg m_A/e ~10⁻³¹ GeV (47–50
                   ordens curto → relíquia ~0); escala da rede ~M_Pl mas não-derivada

FN3-4 (limites):
  Compatível com Lyman-α?         como 100% DM só no topo (~10⁻²² eV); subdominante: SIM
  Compatível com CMB primordial?  SIM (frio antes de z_eq em toda a janela)
  Compatível com estrutura z~0?   SIM (m_A≥10⁻²³ eV ou subdominante); tensão Jeans abaixo
```

## VEREDITO: **B — Ω_{m_A} ≈ 0.12 alcançável, mas COM f_A livre**

```
[ ] A — Ω_{m_A} ≈ 0.12 SEM AJUSTE
        Exigiria f_A derivado dos parâmetros do Paper II. Falha: a massa m_A vem das
        galáxias, mas f_A não — o f_A de Stückelberg (m_A/e) está 47–50 ordens errado,
        e a escala da rede que funciona (~10¹⁷ GeV) é não-derivada (declarada em D3D).

[X] B — Ω_{m_A} ≈ 0.12 COM AJUSTE DE f_A
        m_A do Paper II é plenamente compatível com Ω=0.12; basta f_A ~ (1–4)×10¹⁷ GeV
        (escala GUT, natural mas escolhida). DM consistente, não derivada de um único
        conjunto de dados. A massa é prevista; a abundância exige uma escala alta extra.

[ ] C — Ω_{m_A} INCONSISTENTE
        Não: 0.12 é confortavelmente alcançável e não há sobreprodução inevitável. O
        critério de morte pré-registrado (>2 ordens de 0.12 para TODA a janela) NÃO foi
        acionado.
```

## Leitura honesta do veredito

**O positivo.** A TEIC+DEV não só tem um candidato a matéria escura fria (FM4-1, w=0)
— FN3 mostra que esse candidato pode ter **a abundância certa** (Ω~0.12) com uma
constante de decaimento na **escala GUT**, que é precisamente o que a literatura de
ULDM/axiverso espera de um campo ultraleve de origem UV-Planckiana. A massa m_A vem
das galáxias (Paper II); a relíquia 0.12 cai naturalmente na banda f_A~10¹⁷ GeV. Não
é coincidência forçada — é a "coincidência do axiverso" aparecendo na DEV.

**O custo (por que B e não A).** f_A **não** é fixado pelos dados de galáxias. A
leitura de Stückelberg (f_A=m_A/e) dá ~10⁻³¹ GeV — 47–50 ordens curto, relíquia
desprezível. A leitura correta (f_A = escala de quebra espontânea = corte UV da rede)
dá a ordem certa (Planckiana), mas a escala física absoluta é **declarada
não-derivada desde D3D** (mesmo status de X₀ e m_A em GeV). A relação pura da rede
(m²_iso·λ_p≈520, CR4) fixa a **razão** m_A/√K=√520, não a escala em GeV. Logo a
abundância é **alcançável, não prevista sem escolher f_A**.

**O muro de Lyman-α (herança de FM4).** Mesmo aceitando f_A~10¹⁷ GeV, m_A como
**100% da DM** só sobrevive ao Lyman-α no **topo** da janela (m_A~10⁻²² eV, P=0.963);
para massas ≤10⁻²³ eV, 100% DM é excluído e m_A só pode ser **subdominante**. Isto é
consistente com a 4ª morte de FM4: a janela de massa leve útil para estrutura é
fechada pelo Lyman-α.

## Posição no programa

| Componente | Origem | Status |
|---|---|---|
| Fóton | E2 (mágnon BD, ω=ck) | derivado |
| MOND / matéria (galáxias) | Paper I–IV + ν de FM2-1 | ajustado a SPARC |
| **Matéria escura fria** | **FM4-1 (m_A, w=0)** | **existe (w=0 confirmado)** |
| **Abundância da DM (Ω~0.12)** | **FN3 (misalignment)** | **alcançável com f_A~10¹⁷ GeV livre (B)** |

**Avanço de FN3 sobre FM4:** FM4 respondeu "*o que* é a DM?" (o m_A frio). FN3
responde "*quanto*?" — e a resposta é que **Ω~0.12 é compatível e natural na escala
GUT**, mas **não derivado** sem fixar f_A. A previsão observacional viva da DEV
continua sendo a BTFR (galáxias); FN3 não adiciona uma 2ª confirmação livre-de-ajuste
(seria preciso o Veredito A), mas **remove uma possível morte**: a abundância de DM
**não** é inconsistente com a TEIC+DEV.

## Anti-circularidade e disciplina

m_A da janela do Paper II (galáxias + GW170817); a relíquia da dinâmica do campo
(misalignment, integrado em FRW); Ω_DM h²=0.12, o limite de Lyman-α e z_eq são
**COMPARISON ONLY** — nenhum inserido no cálculo. Critério de morte fixado no charter
ANTES de rodar: "Ω >2 ordens de 0.12 para TODA a janela" → **não acionado** (0.12 é
alcançável). Veredito pré-registrado B (compatível com ajuste de f_A) confirmado,
pontuado como escrito. A leitura de Stückelberg que mataria a rota foi reportada
honestamente (47–50 ordens), não escondida; a dispersão de fator ~8 entre
canônico/numérico/entrópico é a ambiguidade O(1) de onset/g_* declarada.

## Limitações declaradas

- Fórmula de misalignment com θ_i~O(1); anarmonicidade (θ_i→π) e correções de onset
  precisas mudam o coeficiente por O(1) — declarado, absorvido no fator R≈0.40.
- Transfer de Lyman-α de Hu+2000 (analítica, herdada de FM4); números finais com
  perturbações ULDM completas pediriam CLASS+axionCAMB. A direção (100%-DM leve
  excluído, topo da janela marginal) é robusta.
- f_A em GeV permanece não-derivado (D3D/e11); só a razão m_A/√K=√520 é pura. Esta é
  a fronteira que mantém o veredito em B e não A.

# FL1_SU3_FOUNDATION — Fase D: Síntese e Conexão com o Programa

> Roda porque **A+B+C todas passaram**. Conecta a fundação SU(3) ao resto do
> programa. **Única fase** em que números reais de QCD aparecem — e apenas em
> blocos `COMPARISON ONLY`, para comparação qualitativa, nunca como input.
> Driver: `FLD_synthesis.py`. Saídas: `FLD_synthesis.{json,png}`.

## ✅ VEREDITO: **FASE D COMPLETA — A+B+C+D: fundação SU(3) estabelecida**

```
O Skyrmion de cor (bárion) é degenerado com o Skyrmion SU(2); o vácuo SU(3)
ordenado tem 8 modos de Goldstone = o octeto pseudoescalar de mésons (fecha a
lacuna deixada por C3-4); o bárion é um rotor de Casimir (m²∝J(J+1)) e o tubo de
fluxo confinante é a corda de Regge (α'=1/2πσ). Dois setores — bárion-rotor e
méson/corda — emergem do mesmo vácuo SU(3).
```

---

## [D1] Massa: Skyrmion de cor vs Skyrmion SU(2)

O Skyrmion de cor B=1 **é** o hedgehog SU(2) embutido num subgrupo SU(2) de SU(3)
(o bloco inferior-direito = 1 não contribui corrente), então o funcional de energia
é **idêntico** → as massas são **degeneradas por construção**.

| | E2 | E4 | M_virial = 2√(E2·E4) |
|---|---|---|---|
| radial e_sk=0.5 | 200.1 | 14.9 | 109.2 |
| radial e_sk=1.0 | 200.2 | 29.8 | **154.5** |

A massa virial (Derrick-ótima) `M≈154` (e_sk=1) bate com o Skyrmion SU(2) de
MATTER_SU2 (`M≈146–207`, unidades da rede) — confirmação nativa de que o objeto SU(3)
realiza a mesma massa. B=+0.95 no campo SU(3) 3D (a carga inteira do bárion).

> **Espécies de bárion.** A degenerescência clássica significa que próton e nêutron
> (e o octeto/decupleto) **não** se separam no nível clássico — a separação vem da
> **quantização das coordenadas coletivas** (rotações de sabor SU(3)), que é mais
> rica que em SU(2). Isso é consistência, não derivação das massas individuais.
>
> *(COMPARISON ONLY — núcleons quase degenerados: próton 938.3, nêutron 939.6 MeV,
> diferença 0.1% de origem EM+massa de quark, fora deste modelo clássico.)*

---

## [D2] O píon / octeto de mésons: 8 Goldstones do vácuo SU(3)

O vácuo ordenado da Fase B quebra `SU(3)_L × SU(3)_R → SU(3)_diag`, deixando
`dim = 16 − 8 = 8` bósons de Goldstone. Medição (torção helicoidal
`U_i = exp(i k x_i T_a) U_0` em torno de cada gerador `T_a`, custo estático `ΔE(k)`):

```
8/8 modos GAPLESS encontrados (um por gerador quebrado)
  geradores 0–6 (off-diagonais): dE/k² ≈ 3545–3849 (constante => dE ~ k²)
  gerador 7 (λ8, diagonal):      dE/k² ≈ 4000 (gapless, stiffness distinta)
```

`ΔE → 0` quando `k → 0` com `ΔE ~ ρ_s k²` → dispersão **linear `ω ~ k`** (sem massa
no limite quiral). Os 8 modos macios são o **octeto pseudoescalar de mésons** — o
**análogo do píon**.

> **Isto fecha a lacuna de C3-4.** A campanha C3 (Regge) teve de anotar: *"na TEIC o
> pion não existe diretamente (SU(3) não derivado — ver FL1)"*. Com a Fase B (vácuo
> SU(3) ordenado) o píon **agora existe**: é o setor de Goldstone do vácuo SU(3).
>
> *(COMPARISON ONLY — o octeto pseudoescalar de QCD: π⁰, π±, K⁰, K̄⁰, K±, η = 8
> estados leves; massas pequenas porque são pseudo-Goldstones da quebra quiral.)*

---

## [D3] Regge vs Casimir — duas torres distintas

Há **dois** objetos excitáveis no programa SU(3), com leis espectrais diferentes:

**Bárion (Skyrmion de cor) = rotor rígido → Casimir.**
Da campanha C3 (rotor rígido do Skyrmion SU(2), herdado exatamente pelo Skyrmion de
cor embutido): `m² ∝ J(J+1)`, **R² = 1.0000000**, vs `m² ∝ J` (Regge) com R²=0.963.
Inclinação de Casimir `α_C = 0.950` (rede). O bárion **não** é uma corda.

**Tubo de fluxo confinante (Fase C) = corda de Regge.**
A corda confinante medida na Fase C (`V(r)=σr`) **é** o objeto tipo-corda. Sua
inclinação de Regge sai da **tensão de corda medida**, `α' = 1/(2πσ)`:

| β | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 |
|---|---|---|---|---|---|
| σ (Creutz, medido) | 1.35 | 1.10 | 0.96 | 0.67 | 0.33 |
| α' = 1/(2πσ) | 0.118 | 0.145 | 0.165 | 0.237 | 0.488 |

(Unidades de rede, não conversíveis para GeV⁻² — escala não derivada, mesma ressalva
de C3-2.) **O ponto é estrutural:** bárion = rotor de Casimir; méson/tubo-de-fluxo =
corda de Regge. A Regge linear que o Skyrmion sozinho não dá (C3) **vive no setor de
confinamento**, não no rotor topológico.

---

## [D4] Conexão com o Polaris (qualitativa)

C3-4 comparou com o Polaris (Ding et al. 2025: tamanho transversal do píon decresce
com o momento) usando o Skyrmion boostado (contração de Lorentz), mas teve de notar
que **o píon não existia** no modelo. A Fase D completa o quadro:

- **O píon agora é realizado** (D2: o octeto de Goldstone). Seu "tamanho" é dado pelo
  comprimento de correlação `ξ` do vácuo SU(3) ordenado, que **encolhe mais fundo na
  fase ordenada** (J maior → ξ menor) — o análogo qualitativo do estreitamento
  transversal com o momento.
- O mecanismo cinemático de C3-4 (contração de Lorentz da densidade de winding
  bariônica sob boost, herdada da estrutura causal) permanece válido para o bárion.

*(COMPARISON ONLY, qualitativo — sem ajuste a dados do Polaris; apenas a direção do
efeito. O modelo não pretende reproduzir as GPDs quantitativamente.)*

---

## SÍNTESE HONESTA FINAL — FL1_SU3_FOUNDATION

```
FASE A (definição):
  Ação SU(3) positiva semi-definida?        SIM (Wilson + sigma PSD)
  Localidade causal preservada?              SIM (100% causal + gauge-covariante)

FASE B (ordenamento):
  Transição de fase encontrada?              SIM
  J_c(SU(3)):                                ≈2.65 (cúbico), ≈0.3 (causal)
  Ordem da transição:                        contínua/1ª-fraca (não resolvida L≤12)
  Ordem de longo alcance (causal)?           SIM (C_long = m², ferromagneto de cor)

FASE C (defeitos / confinamento):
  Defeito topológico estável existe?         SIM (Skyrmion de cor, π₃(SU(3))=ℤ, B=+1;
                                             Derrick-estável com Skyrme externo;
                                             B robusto a ruído térmico)
  Sinal de confinamento (E(r)~σr)?           SIM (V(r) linear; σ>0; σ(β) decresce)

FASE D (síntese):
  Massa SU(3) vs SU(2)?                       DEGENERADA (M≈154; bárion = SU(2) embutido)
  Análogo do píon?                            SIM (8 Goldstones = octeto de mésons)
  Regge vs Casimir?                           bárion = Casimir; tubo-de-fluxo = Regge

[X] SUCESSO TOTAL (A+B+C+D) — fundação para quarks estabelecida.
```

### Veredito geral
A rede causal de Poisson da TEIC **não** se limita a estruturas tipo-SU(2): ela
hospeda SU(3) (A), faz SU(3) ordenar num **ferromagneto de cor** (B), suporta um
**Skyrmion de cor estável** e **confinamento** com tensão de corda medida (C), e
desse vácuo emergem um **bárion** (degenerado com o Skyrmion SU(2)), um **octeto de
mésons** (8 Goldstones) e **duas torres espectrais** — Casimir (bárion-rotor) e Regge
(tubo de fluxo) (D). É o análogo SU(3) completo de E1–E3, **mais** o fenômeno
genuinamente novo do confinamento.

### Ingredientes externos (declarados, não escondidos)
1. **Termo de Skyrme** (`e_sk`): a Fase A provou (`K ≤ 6·TrM²` + teorema do sinal)
   que a dominância de Skyrme não emerge do cosseno — em SU(3) **nem mais nem menos**
   que em SU(2). O estabilizador é o mesmo "último ingrediente externo" do setor de
   matéria, herdado, não uma penalidade nova de SU(3).
2. **Escala da rede**: não derivada (D3D), igual a todo o programa — por isso `σ`,
   `α_C`, `α'`, massas ficam em unidades de rede, não conversíveis para GeV.

### Anti-circularidade
Nenhum número de QCD entrou em A–C. Em D, valores reais (massas de núcleon, octeto,
GPDs do Polaris) aparecem **somente** em blocos `COMPARISON ONLY`, qualitativos. O
guard de anti-circularidade e o `pytest` permanecem verdes; a exceção complexa de
SU(3) é rotulada e restrita (dilatação proibida em todo lugar).

### O que avança no programa
- **Setor de matéria** ([[teic-project-state]]): além do Skyrmion SU(2) (bárion),
  agora há um caminho SU(3) completo com cor, confinamento e octeto de mésons.
- **Fecha a lacuna de [[c3]]** (C3-4): o píon existe como octeto de Goldstone.
- **Regge encontrado** onde C3 não achou: no tubo de fluxo confinante, não no rotor.

---

*Reprodução:* `python FLD_synthesis.py` (≈12 s) → `FLD_synthesis.{json,png}`.
Lê `FLC_confinement.json` para σ. Determinístico. numpy 2.4.4, scipy 1.17.1.

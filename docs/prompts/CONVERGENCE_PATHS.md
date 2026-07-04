# CONVERGENCE_PATHS — os caminhos vivos, ranqueados (Fase 3)

> Campanha `CONVERGENCE_INVESTIGATION`, Fase 3. Pré-requisito: `CONVERGENCE_MAP.md`
> (Fase 2, reportada e aprovada). Ranqueamento por **probabilidade × impacto
> (honesto)** — a chance real de resultado positivo dado o que já morreu, vezes a
> fronteira cruzada se der certo. **C2 (derivar G de r_próton) foi movido para
> `CONVERGENCE_GAPS.md` como [MORTO]** (falha de 108 ordens, ver Fase 2 §2C).
>
> Restam **5 caminhos vivos**. Cada um traz: probabilidade estimada, o que
> precisaria ser derivado, a fronteira (S8/ℏ/gerações/outra), o custo, e um
> **prompt concreto** pronto para virar charter — com critério de morte
> pré-registrado, na disciplina do projeto.

---

## Quadro de ranqueamento (probabilidade × impacto)

| Rank | Caminho | Prob. de positivo | Impacto (fronteira) | Prontidão | Score |
|---|---|---|---|---|---|
| **1** | **C3 — Trajetórias de Regge dos Skyrmions** | Alta (~0.7) | Tensão de corda hadrônica (setor de matéria) | Motor existe (`su2q_core.py`) | **alto** |
| **2** | **C1 — TEIC ≡ Khoury (equivalência formal)** | Média (~0.5) | Unifica TEIC+DEV+Khoury; ℏ como *relação* | Analítico; mecanismo meio-feito (FM2-1) | **alto** |
| **3** | **C6 — Vórtices quantizados** | Média (~0.5) | Previsão falsificável (estrutura kpc / sub-pc) | Analítico; liga a FN4 (Gaia DR4) | **médio** |
| **4** | **C5 — Dimensão espectral D_s(σ)** | Média (~0.45) | TEIC↔CDT; escala de ℏ | Observável novo, limpo | **médio** |
| **5** | **C4 — SU(2)×U(1) e 3 gerações** | Baixa (~0.1) | Espectro do Modelo Padrão | Motor novo, anos; VS4/VS5 negativos | **baixo** |

> **Nota de honestidade sobre o ranqueamento.** C2 saiu (morto na Fase 2). C4
> permanece na lista por ser um caminho legítimo, mas é rebaixado: VS4 (bacia
> única, sem degenerescência de gerações no B=1) e VS5 (constantes de
> acoplamento não saem da aritmética dos 4 números) já fecharam *negativos* os
> atalhos para gerações — C4 teria de produzir o que esses experimentos não
> encontraram, num motor que ainda não existe.

---

## C3 — Trajetórias de Regge dos Skyrmions  ★ rank 1

**Hipótese.** O Skyrmion quantizado coletivamente (já com spin-½ derivado,
Q1–Q7) gera um espectro rotacional `E_J` que, plotado contra J, traça uma
**trajetória de Regge** linear `J ≈ α' E² + α₀` — a assinatura de que a TEIC
deriva a **tensão de corda** dos hádrons a partir da granularidade causal.

**O que precisaria ser derivado.** O momento de inércia coletivo I do hedgehog
B=1, rodando o motor `su2q_core.py` (que já dá `E_J ∝ J(J+1)`) para J=0,1,2,…;
extrair `α'` (inclinação de Regge) e testar se o número puro `α'·Λ²` (Λ = escala
de rede) é constante na varredura de ρ — mais uma relação cruzada sem parâmetro
livre, agora no setor rotacional.

**Fronteira.** Setor de matéria / espectro hadrônico. **Não** toca S8 nem ℏ
absoluto. Cruzaria a fronteira "a TEIC só tem a *massa* do bárion, não o
*espectro*" (atualmente [IDENTIFICADO]: Skyrmion↔bárion sem espectro).

**Probabilidade ~0.7.** O motor existe e já dá `E_J∝J(J+1)`; uma trajetória
linear `J vs E²` é o resultado-padrão de Skyrmions quantizados (Adkins–Nappi–Witten).
A probabilidade de *algum* positivo é alta; o risco é o número puro `α'·Λ²` não
ser constante (como m_A não foi, CR4) — nesse caso o resultado é "espectro existe,
mas a tensão de corda cavalga em escala externa", ainda informativo.

**Custo.** Motor existente, ~1 semana.

**Prompt concreto:**
```
CHARTER: REGGE_SKYRMION (entrada FQ/FL no FUTURE_EXPERIMENTS)
Pré-registro de morte ANTES de qualquer código.

Objetivo: medir a trajetória de Regge do Skyrmion B=1 da TEIC e testar se a
tensão de corda α' é um número puro escala-invariante (5ª relação cruzada).

Infra: results/matter/su2_quant/su2q_core.py (já dá E_J ∝ J(J+1), spin-½, Q1–Q7).

Tarefas:
  RG1: rodar quantização coletiva para J=0,1,2,3; extrair E_J e o momento de
       inércia I(ρ). Plotar J vs E_J² ; ajustar α' (inclinação) e α₀ (intercepto).
  RG2: varrer ρ (≥4 densidades, mesmas sprinklings de SC/CR); testar se α'·λ_Sk²
       (ou α'·⟨a²⟩) é constante (CV<20%) → número puro; senão reportar o expoente
       medido (status de m_A em CR4).
  RG3: cruzar com a massa M_Sk de SU3 e a 1ª relação cruzada (3/320π²) — verificar
       consistência interna (mesma rede, mesmos defeitos).

Critério de morte (pré-registrado):
  - Se J vs E² não for linear (R²<0.9) → não há trajetória de Regge: reportar
    negativo (o espectro rotacional não organiza como corda).
  - Se α'·(escala)² tiver CV>20% na varredura → tensão de corda NÃO é número puro;
    reportar como "espectro existe, escala externa" (não maquiar).
Honestidade: λ_Sk de SC1–SC3 (não reajustado); spin-½ de Q1–Q7 (importado, citado);
nenhum valor hadrônico (m_π, f_π SI) inserido — só números puros da rede.
```

---

## C1 — TEIC ≡ Superfluid DM (Khoury): a equivalência formal  ★ rank 2

**Hipótese.** O ferromagneto O(3) do vácuo da TEIC (E1) e o condensado U(1) BEC
de Khoury são **a mesma EFT de baixa energia** — vácuo sem partículas vs
superfluido de partículas, como propõe a nota do prompt. A Fase 2 já mostrou o
elo derivado (deep-MOND `L∝X^{3/2}` compartilhado; `χ∥~h^{−1/2}` de FM2-1). C1
**fecha a equivalência formal**: provar que a expansão de Goldstone do
ferromagneto O(3) em torno de ⟨n⃗⟩≠0 produz, ao integrar dois dos três modos, a
**ação de fônon único** `P(X)=X^{3/2}/Λ³` de Khoury — com o coeficiente Λ
expresso na granularidade da rede.

**O que precisaria ser derivado.** O mapa O(3)→U(1)-efetivo: na fase ordenada, 2
Goldstones transversais (E2: as 2 polarizações do fóton) + 1 modo longitudinal
massivo (a magnitude). Integrar o longitudinal e mostrar que a dinâmica
transversal mole reproduz a ação de Khoury. Se `Λ_Khoury` sair em função de
`J_c`, `K`, `ρ` da rede → a TEIC **deriva microscopicamente** o parâmetro que
Khoury postula.

**Fronteira.** ℏ **como relação** (não valor — o valor permanece externo,
T3C/VS5). Unifica as três teorias num único arcabouço. É o coração conceitual de
toda a investigação CONVERGENCE.

**Probabilidade ~0.5.** O mecanismo está meio-derivado (FM2-1 deu o expoente). O
risco: a equivalência pode exigir um regime denso (superfluido de *partículas*)
que o vácuo nu da TEIC não tem — a Fase 2 marcou a herança de condensado como
[MORTO] (⟨Φ⟩≠0 espontâneo não existe; PE2/V4/VS1). Então C1 pode entregar
"equivalência no setor de fônon/Goldstone, mas não no setor de magnitude" —
um positivo parcial, ainda valioso.

**Custo.** Análise analítica + ~1 semana de código (varrer Λ_efetivo vs J_c, K, ρ).

**Prompt concreto:**
```
CHARTER: KHOURY_EQUIVALENCE (entrada FN no FUTURE_EXPERIMENTS)
Pré-registro de morte ANTES de qualquer código.

Objetivo: provar (ou refutar) que a EFT de Goldstone do ferromagneto O(3) da
TEIC (E1/E2) reduz à ação de fônon P(X)=X^{3/2}/Λ³ de Khoury (1507.04730), e
expressar Λ na granularidade da rede.

Base: E1 (⟨n⃗⟩≠0, J_c(O(3))≈0.08), E2 (magnon ω=ck, 2 Goldstones), FM2-1
(χ∥~h^{−1/2} = deep-MOND), DEV deep-MOND L∝X^{3/2} (CONVERGENCE_MAP §2B).

Tarefas:
  K1 (analítico): expandir o sigma model O(3) em torno de ⟨n⃗⟩; separar 2 modos
     transversais (Goldstone) + 1 longitudinal (massa). Integrar o longitudinal;
     mostrar a ação efetiva dos transversais no regime mole.
  K2 (numérico): medir na rede o coeficiente da ação efetiva (a "constante de
     decaimento" do Goldstone) vs J, K, ρ; testar se reproduz a estrutura
     Λ=Λ(J_c,K,ρ) sem parâmetro livre.
  K3: testar a verificação-3 do prompt (vórtices ∮∇φ·dl=2πn → circulação física)
     SÓ se K1/K2 fecharem — senão fica para C6.

Critério de morte (pré-registrado):
  - Se a ação efetiva dos transversais NÃO for ∝ X^{3/2} no limite mole →
    a equivalência com Khoury falha no setor de fônon: reportar negativo.
  - Se Λ_efetivo depender de uma escala externa não-vinculada (como m_A em CR4) →
    "forma equivalente, escala externa" (não é derivação de ℏ).
Honestidade declarada de saída: ℏ ABSOLUTO continua externo (VS5: α conteria ℏ,
contradição dois-andares). O alvo é a RELAÇÃO ℏ↔condensado, não o valor.
```

---

## C6 — Vórtices quantizados: a previsão de estrutura nos halos  ★ rank 3

**Hipótese.** Os vórtices U(1) da TEIC (π₁=ℤ, `∮∇φ·dl=2πn`, [DERIVADO]) — quando
o campo complexo está presente (fase AH) — têm circulação física quantizada
`∮v·dl=nℏ/m_A`, gerando uma **escala de de Broglie** `λ_dB=h/(m_A v)` observável
nos halos. Para m_A no topo da janela (~10⁻²² eV), λ_dB ~ kpc; para m_A baixo,
liga-se à 2ª previsão FN4 (binárias largas sub-pc, λ_A=17.3 pc).

**O que precisaria ser derivado.** Calcular a circulação física do vórtice da
DEV/TEIC: `∮A_μ dx^μ` para o setor de gauge, converter via ℏ/m_A, e mapear
λ_dB(m_A, v) sobre a janela de massa do Paper II. Comparar com dados de
sub-estrutura de halos (vórtices em ULDM dão interferência granular).

**Fronteira.** Previsão observacional falsificável — a mesma classe da BTFR e das
binárias largas. **Não** resolve S8 nem ℏ absoluto, mas adiciona um 3º front
observacional ao lado de BTFR e FN4.

**Probabilidade ~0.5.** O cálculo analítico é direto; o risco é que a Fase 2 já
mostrou que (i) os vórtices nus são semi-estáveis (núcleo difunde, CR_3D) e
(ii) λ_dB é kpc **só** no topo da janela, sub-galáctico no resto. Então o
positivo provável é "previsão de granularidade sub-pc (binárias/aglomerados
globulares)", reforçando FN4 — não a estrutura kpc grandiosa.

**Custo.** Cálculo analítico + comparação com dados, ~1 semana.

**Prompt concreto:**
```
CHARTER: HALO_VORTEX (entrada FN/FO no FUTURE_EXPERIMENTS)
Pré-registro de morte ANTES de qualquer código.

Objetivo: derivar a circulação física quantizada do vórtice da TEIC/DEV e mapear
λ_dB(m_A,v) sobre a janela de massa do Paper II; testar se prevê estrutura
observável (kpc ou sub-pc) nos halos.

Base: vórtices π₁=ℤ ∮∇φ·dl=2πn (CR_3D, CR_WILSON, [DERIVADO]); janela m_A
[3.76e-25, 1.2e-22] eV (Paper II); ξ_A=17.3 pc; FN4 (binárias largas, Gaia DR4).

Tarefas:
  HV1: calcular ∮A_μ dx^μ do vórtice no setor de gauge; converter para ∮v·dl=nℏ/m_A.
  HV2: mapear λ_dB=h/(m_A v) com v~200 km/s sobre toda a janela m_A; identificar
       onde λ_dB ∈ {sub-pc, pc, kpc}.
  HV3: confrontar com a previsão FN4 (binárias <17 pc newtonianas) — são o mesmo
       fenômeno em m_A diferente? Conectar ao debate Chae(γ=1.43) vs Banik(γ≈1).

Critério de morte (pré-registrado):
  - Se a circulação física exigir ℏ/m_A absolutos não-vinculados → previsão é
    qualitativa, não quantitativa (registrar como tal).
  - Se λ_dB for kpc SÓ num ponto isolado da janela já excluído por Lyman-α →
    reportar que a "estrutura kpc" não sobrevive, restando só a previsão sub-pc (FN4).
Honestidade: os vórtices nus são SEMI-estáveis (CR_3D); a previsão vale na fase AH
(ingrediente complexo adicionado, VS1) — declarar a condição, não esconder.
```

---

## C5 — Dimensão espectral D_s(σ) e a escala de ℏ  ★ rank 4

**Hipótese.** A rede causal de Poisson, como a CDT, tem uma **dimensão espectral
que corre** de D_s=4 (IR, grande escala) a D_s=2 (UV, pequena escala). A escala σ*
onde D_s muda de regime é candidata natural à escala onde ℏ "liga" — conectando a
TEIC à CDT e dando um significado geométrico ao ℏ=k/N de T3C.

**O que precisaria ser derivado.** O heat kernel de retorno `K(σ)=∫dV ρ(x,x',σ)`
na rede causal, e `D_s(σ)=−2 d log K/d log σ`. Medir se D_s→2 no UV. Se sim, σ* é
um observável novo e a escala de ℏ ganha conteúdo estrutural.

**Fronteira.** ℏ (relação à escala σ*) + conexão TEIC↔CDT. Conceitualmente alta,
mas o payoff é especulativo: mesmo medindo σ*, o **valor** de ℏ continua externo
(VS5). O ganho é interpretativo, não um número novo derivado.

**Probabilidade ~0.45.** Causal sets têm não-localidade conhecida (E1-3: S(k)
plano, ⟨grau⟩≈130) — o heat kernel pode não dar uma corrida limpa 4→2 sem o
suavizador BD (e10). Risco real de "D_s não corre como CDT" (negativo honesto,
ainda informativo: distingue a rede de Poisson da CDT).

**Custo.** Observável novo, ~1–2 semanas.

**Prompt concreto:**
```
CHARTER: SPECTRAL_DIMENSION (entrada FN no FUTURE_EXPERIMENTS)
Pré-registro de morte ANTES de qualquer código.

Objetivo: medir a dimensão espectral D_s(σ) da rede causal de Poisson via heat
kernel; testar se corre de 4 (IR) a 2 (UV) como em CDT, e se a escala de transição
σ* tem relação com ℏ=k/N (T3C).

Base: T3C (ℏ=k/N, k∝N^1.008); e10 (operador BD suavizado, localidade); E1-3
(links nus são não-locais, ⟨grau⟩≈130) — usar o operador BD, não o Laplaciano nu.

Tarefas:
  SD1: construir o heat kernel de retorno K(σ) com o d'Alembertiano BD (e10);
       medir D_s(σ)=−2 d log K/d log σ em ≥2 décadas de σ.
  SD2: identificar σ* (transição 4→2) se existir; testar estabilidade em ρ e N.
  SD3: cruzar σ* com a escala de ℏ de T3C — é a mesma escala de granularidade?

Critério de morte (pré-registrado):
  - Se D_s não correr (fica em 4, ou em 2, ou plana) → a rede de Poisson NÃO é
    CDT-like: reportar negativo (distingue Poisson de CDT — resultado válido).
  - Se σ* existir mas não tiver relação com k/N → "corrida existe, ℏ não conectado".
Honestidade: o VALOR de ℏ continua externo (VS5/e11); o alvo é σ* como escala
estrutural, não o valor de ℏ.
```

---

## C4 — SU(2)×U(1) e 3 gerações  ★ rank 5 (mantido, rebaixado)

**Hipótese.** Estender o motor de matéria SU(2) ao grupo eletrofraco SU(2)×U(1) e
verificar se as 3 gerações de férmions aparecem como mínimos de energia distintos.

**O que precisaria ser derivado.** Um motor novo (gauge eletrofraco na rede
causal) e um espectro de defeitos com 3 bacias degeneradas.

**Fronteira.** Espectro do Modelo Padrão (gerações, sabor) — a maior fronteira
aberta. Impacto enorme se positivo.

**Probabilidade ~0.1 (baixa, honesta).** Dois experimentos já fecharam negativos os
atalhos: **VS4** (o setor B=1 tem **uma** bacia única, 10 perfis → mesma massa a
0.02%, *sem* degenerescência de gerações) e **VS5** (constantes de acoplamento
não emergem da aritmética dos 4 números puros; α conteria ℏ, contradição
dois-andares). C4 teria de encontrar gerações que VS4 não encontrou, num grupo
maior, com motor que não existe. É um caminho de **anos**, listado por completude.

**Custo.** Motor novo, 2–3 semanas só para o esqueleto; resolução real = anos.

**Prompt concreto (esqueleto, não recomendado como próximo passo):**
```
CHARTER: ELECTROWEAK_SU2U1 (entrada FL no FUTURE_EXPERIMENTS) — longo prazo
Pré-registro de morte ANTES de qualquer código.

Objetivo: estender su2_core/su2q_core ao grupo SU(2)×U(1); buscar se há ≥3 bacias
de energia degeneradas (candidatas a gerações).

Tarefas:
  EW1: motor de gauge SU(2)×U(1) na rede causal (quaternions + fase U(1)).
  EW2: catálogo de defeitos; contar bacias de energia distintas; medir
       degenerescência.
  EW3: se ≥3 bacias → testar razões de massa (números puros) vs gerações.

Critério de morte (pré-registrado):
  - Se houver UMA bacia (como VS4 no B=1) → sem gerações: confirma VS4 no grupo
    maior, reportar negativo.
  - Se as razões de massa exigirem α/ℏ (dois-andares) → confirma VS5, reportar.
Honestidade: VS4 e VS5 já apontam negativo; este caminho testa se o grupo maior
muda o veredito. Probabilidade a priori baixa, declarada.
```

---

## Recomendação de sequência (probabilidade × impacto)

1. **C3 (Regge)** — primeiro: pronto, provável positivo, fecha um [IDENTIFICADO]
   aberto (Skyrmion↔bárion ganha espectro) sem motor novo.
2. **C1 (Khoury)** — segundo: o coração conceitual da investigação; consolida o
   que a Fase 2 já meio-derivou, com risco controlado de positivo parcial.
3. **C6 (vórtices)** — terceiro: adiciona um front observacional (liga a FN4/Gaia).
4. **C5 (dim. espectral)** — quarto: observável novo, payoff interpretativo de ℏ.
5. **C4 (eletrofraco)** — por último: alto impacto, baixa probabilidade, anos;
   só após os de cima, e ciente de VS4/VS5.

> Lacunas e impossibilidades (incluindo **C2, morto**): `CONVERGENCE_GAPS.md`.
```

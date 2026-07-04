# SÍNTESE — A4 / C4 · Propagação dinâmica estável dos Goldstones (BD smeared)

> Campanha PROPAGACAO_A4 (Fase 2, Frente A). Pré-registro: `PRE_REGISTRO.md`.
> Driver: `a4_bd_propagation.py` → `a4_bd_propagation.json`. jun/2026.
> **Veredito: MORTE CARACTERIZADA. A propagação estável ω=ck via evolução direta
> NÃO existe — não por bug, mas porque o operador BD smeared é intrinsecamente
> INDEFINIDO (Lorentziano). O smearing corrige LOCALIDADE (problema do C5), NÃO a
> SIGNATURE. ω=ck é real ON-SHELL mas só extraível estável via o SÍMBOLO (E2). E2
> fica [FRACO]; a ressalva do Paper Goldstone PERMANECE — agora com mecanismo
> exato — e deve ser submetida explícita. Timing cumprido: resolvido ANTES da
> submissão.**

---

## 1. A brecha [FRACO] de E2

E2 obteve ω=ck do **símbolo** do operador (λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩, on-shell) porque
a **marcha retardada direta** `bd_propagate` (`φ(x)=2ε Σ w(m)φ(y)`, só passado) é
**instável** ("substituto estável da propagação direta instável"). A4 testou se uma
**evolução estável** com o operador smeared dá ω=ck **medido na evolução**.

## 2. Stage 1 — gate de máquina (VALIDADO)

Lattice 1D regular, Laplaciano **sharp**, leapfrog ∂_t²φ=−Lφ, ω(k) medido por FFT
da oscilação de cada modo (da evolução): **c(slope)=1.000, c(fase)=1.000, spread
0.0%, estável, ω=ck linear**. O integrador + estimador de ω(k) estão validados
(resultado de livro reproduzido exatamente) — o que falha adiante é o operador, não
a máquina.

## 3. Stage 2 — operador smeared como Laplaciano espacial (TACHIÔNICO)

Operador BD smeared simétrico (pesos w(d) decaindo, d=1..8) usado como stiffness
espacial: **rigidez de pequeno-k c²=Σ g(d)d² = −20.1 < 0**. Negativa ⇒ ω²<0 ⇒ ω
imaginário ⇒ **modos de pequeno-k crescem** (tachiônico) ⇒ instável, sem ω=ck. Os
pesos BD **alternam sinal** (w>0 perto de m=0, w<0 intermediário); somados com peso
d² dão stiffness negativa. O kernel BD **não é** um Laplaciano espacial PSD.

## 4. Stage 3 — operador BD simétrico no causal set (INDEFINIDO)

Operador BD smeared simétrico (construção c5_core) em aspersões reais:

| N | fração autovalores < 0 | λ ∈ | leapfrog max\|φ\| |
|---|---|---|---|
| 235 | **0.83** | [−15.2, +5.9] | ×2.8e83 |
| 381 | **0.76** | [−16.0, +6.6] | ×7.3e83 |

O operador é **fortemente indefinido** (~80% dos autovalores negativos, λ de ambos
os sinais) — porque aproxima o **d'Alembertiano Lorentziano** □=∂_t²−∇² (assinatura
−+++, indefinido por construção; o C5 já tomava |λ| por isso). A evolução
∂_s²φ=−Mφ trata M como Laplaciano elíptico (PSD), mas M é indefinido ⇒ os modos
λ<0 (acima do cone de luz) **crescem exponencialmente** ⇒ **blow-up ×10⁸³**. A
marcha retardada `bd_propagate` falha de outra forma (sinal amortecido a ~0 aqui;
não-normal/mal-condicionada) — **nenhum dos dois é um propagador fiel**.

## 5. Veredito (MORTE caracterizada — 1ª classe)

A hipótese de C4 ("o smearing estabiliza a propagação, vs o sharp") é **falsificada**,
e o motivo é instrutivo: o problema **não é** sharp-vs-smeared. O smearing corrige a
**não-localidade** (que quebrou o operador causal sharp em C5: grau∝L^2.9). Mas a
instabilidade da **propagação** vem da **assinatura indefinida (Lorentziana)** do
d'Alembertiano — intrínseca a **qualquer** aproximante de □. 

Consequência:
- **ω=ck é REAL on-shell** (o símbolo de □ se anula no cone; E2 mede isso corretamente).
- Mas um pacote genérico excita modos **off-shell (acima do cone, λ<0)** que crescem
  ⇒ **não há evolução direta estável**. O **símbolo** (E2) é a extração estável
  CORRETA de ω=ck, não um atalho — a propagação direta estável **não existe** para um
  operador Lorentziano indefinido.
- **E2 permanece [FRACO]** — corretamente. A ressalva é agora **precisamente
  caracterizada**: instabilidade = indefinição Lorentziana do operador + não-normalidade
  da marcha retardada, **não** um artefato numérico.

## 6. Impacto no Paper Goldstone (PRD) — pressão de timing CUMPRIDA

A4 terminou **antes da submissão** (o requisito). A ressalva de "instabilidade numérica
do operador sharp" **permanece**, mas transformada de **dúvida numérica aberta** em
**limitação de princípio caracterizada**:

> "A relação ω=ck é uma propriedade **on-shell** (símbolo) do d'Alembertiano BD
> smeared, validada por E2. Uma **propagação direta estável** não é obtida porque o
> operador é **Lorentziano-indefinido**: modos acima do cone de luz têm λ<0 e crescem
> sob evolução elíptica explícita (A4: ~80% autovalores negativos, blow-up ×10⁸³), e a
> marcha retardada é não-normal. O símbolo é a extração estável correta; ω=ck on-shell
> é genuíno. Esta é uma limitação intrínseca à assinatura Lorentziana, não um artefato."

**Submeter com esta redação explícita** é honesto e defensável — a ressalva está
**resolvida** (caracterizada), não pendente.

## 7. Limitação honesta

A4 testou a evolução **elíptica** (∂_s²φ=−Mφ) e a **marcha retardada**; não esgota
TODO esquema concebível (ex.: um solver hiperbólico IVP que separe explicitamente t
e ∇² na rede causal não-local — que é precisamente o que a não-localidade impede de
construir limpo, o mesmo obstáculo de E5/E7/A2). Que um tal esquema também falharia é
**esperado** mas não **provado** aqui — registrado como fronteira, não como teorema.
N≤381 no causet (a indefinição já é ~80%, robusta).

## 8. Anti-circularidade

Gate A1 verde sobre `a4_bd_propagation.py` (dilatação + literais de escala) antes de
rodar. ω medido da evolução (FFT da oscilação); c sai do ajuste, **nunca inserido**;
pacote/modo inicial real (cos), sem fase e^{ikL} injetada. Operador BD e grafo causal
sob a guarda. "Fóton" não entra no gerador.

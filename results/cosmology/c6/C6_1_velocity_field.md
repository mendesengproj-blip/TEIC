# C6-1 — Existe um campo de velocidade efetivo v_TEIC = κ∇φ? (teste decisivo)

> Resultado: **SIM — via Candidato 1 (m_A), NÃO via Candidato 2 (ferromagneto).**
> A relação `v_TEIC = (ℏ/m_A)∇θ` é identificável na estrutura JÁ existente do
> condensado massivo m_A de FM4 (descrição de Madelung do campo coerente que FM4
> já usou para a escala de de Broglie/Jeans). O ferromagneto causal dá uma
> velocidade de spin-superfluido `v ∝ ∇φ` formal, mas com κ **clássico** (sem ℏ).

---

## Os dois candidatos, lidos do código existente

### Candidato 2 — corrente do ferromagneto causal (E1/HQ2, `fm2_core.py`) — **REJEITADO**

`fm2_core.py` implementa o sigma model O(3) clássico: `E = −J Σ n_i·n_j − h Σ n_i·ẑ`,
Metropolis a β=1. A corrente de Noether das rotações O(3) é a **corrente de spin**,
calculada explicitamente em `_helicity_pieces`:

```
current  =  J Σ_{<ij>‖μ}  a·(n_i × n_j)            (corrente de spin, gerador â)
curvature = J Σ_{<ij>‖μ}  (n_i·n_j − (a·n_i)(a·n_j))
ρ_s (rigidez) = (⟨curvature⟩ − ⟨current²⟩)/V         (módulo de helicidade)
```

Definindo `v ≡ j/ρ` e reduzindo ao plano fácil (ângulo azimutal φ de n⃗ em torno do
eixo h), a hidrodinâmica de magnon dá de fato uma **velocidade de spin-superfluido**

```
v_spin = (ρ_s / M) ∇φ        ⇒   v ∝ ∇φ   (forma correta)
```

**Mas o coeficiente κ = ρ_s/M é uma rigidez de spin em UNIDADES DE REDE — clássico,
SEM ℏ.** Isto não é uma falha de medição: é estrutural. O CONVERGENCE_MAP §2D e E2 já
fixaram que *"o ferromagneto da TEIC é um sigma model O(3) **clássico** na rede causal;
ω=ck é dispersão de onda clássica, **sem ℏ no gerador**"*. Logo:

- A circulação que este candidato quantiza é a **topológica** `∮∇φ·dl = 2πn`
  (π₁(S¹)=ℤ) — que **já é [DERIVADO]** (CR_3D, CR_WILSON). Nada novo.
- A circulação **física** `∮v·dl = κ·2πn` tem `κ = ρ_s/M` clássico → unidades de
  rede, **não identificável com ℏ/m_A**. É "forma sem ℏ".

→ **Candidato 2 não carrega a ponte física.** Coerente com a Fase 2 (a quantização
física `nℏ/m` exige uma escala ℏ/m que o vácuo nu clássico não tem).

### Candidato 1 — corrente do campo m_A (FM4/FN3, `fm4_core.py`) — **ACEITO**

`fm4_core.py` evolui o campo massivo coerente pela equação de misalignment

```
φ'' + 3 H φ' + m_A² φ = 0          (Klein-Gordon/Proca em fundo FRW)
ρ = ½φ̇² + ½m_A²φ²,   p = ½φ̇² − ½m_A²φ²,   ⟨w⟩ → 0  (FM4-1: m_A É CDM frio)
```

Um campo massivo **coerente** no regime não-relativístico (H ≪ m_A, que é
precisamente o regime oscilante de FM4-1) admite a decomposição de Madelung padrão.
Escrevendo o campo como uma onda lenta modulando a oscilação rápida e^{−im_A t}:

```
φ(x,t) = Re[ √(2/m_A) · Ψ(x,t) · e^{−i m_A t/ℏ} ]
```

a redução não-relativística leva Ψ a obedecer a equação de Schrödinger/Gross-Pitaevskii,
e com `Ψ = √n · e^{iθ}` a **corrente de número de partículas** (a U(1) **emergente** da
conservação de número de quanta do campo oscilante — esta é a "corrente de Noether do
campo m_A" do enunciado) é

```
j = (ℏ/m_A) · n · ∇θ        ⇒   v_TEIC ≡ j/n = (ℏ/m_A) ∇θ
```

**Esta é exatamente a relação procurada, com θ = fase do condensado de onda.**

#### Por que isto NÃO é inventar um campo novo

A fase θ e a velocidade de Madelung **já estão dentro de FM4**, não são acrescentadas
aqui. `fm4_core.py` usa:

- `k_half_mode` / `jeans_scale_z` / `fuzzy_transfer`: a **escala de Jeans quântica** e a
  transfer function de **fuzzy DM** (Hu-Barkana-Gruzinov). Essa pressão quântica é o
  termo `(ℏ²/2m_A²)·∇²√n/√n` da hidrodinâmica de Madelung — **só existe se** o campo é
  descrito por Ψ=√n e^{iθ} com v=(ℏ/m_A)∇θ.

Ou seja: **ao escrever k_J, FM4 já se comprometeu com v=(ℏ/m_A)∇θ.** C6-1 apenas torna
explícito o campo de velocidade que FM4 usou implicitamente. Não há terceiro candidato
artificial; o candidato 1 é o setor massivo que FM4/FN3 já estabeleceram.

#### A condição de estabilidade do vórtice é satisfeita aqui (não no candidato 2)

A Fase 2 (CONVERGENCE_MAP §2B Ver. 3) registrou que os vórtices **nus** da
orientação são *semi-estáveis* (núcleo difunde, cegueira cos2π=1) e que a
quantização física exige o **campo complexo adicionado** (ingrediente irredutível
VS1, fase Abelian-Higgs). **O condensado de m_A É esse campo complexo:** Ψ=√n e^{iθ} é
genuinamente complexo, e o núcleo do vórtice é regularizado pela **pressão quântica**
(comprimento de healing ξ=ℏ/m_A v) — não difunde. Portanto a condição que o candidato
2 não cumpre, o candidato 1 cumpre por construção.

---

## Veredito C6-1

| | v ∝ ∇φ? | κ identificável | quantização física? |
|---|---|---|---|
| **Cand. 2 (ferromagneto)** | SIM (spin-superfluido) | κ=ρ_s/M **clássico, sem ℏ** | só topológica 2πn (já [DERIVADO]) |
| **Cand. 1 (m_A condensado)** | **SIM** (Madelung) | **κ = ℏ/m_A** (C6-2) | **SIM**: ∮v·dl = n·h/m_A |

**C6-1 = SUCESSO.** O campo de velocidade efetivo existe e é
`v_TEIC = (ℏ/m_A)∇θ`, identificado na descrição de onda (Madelung) do condensado
massivo m_A que FM4 já estabeleceu — não um campo novo. A ponte é carregada pelo
**setor massivo** (matéria de onda), não pelo vácuo clássico de orientação, o que é
fisicamente correto: circulação física quantizada precisa de uma matéria-onda com ℏ.

→ Prosseguir para **C6-2** (extrair κ e comparar com ℏ/m_A).

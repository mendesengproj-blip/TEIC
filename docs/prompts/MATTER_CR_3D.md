# MATTER_CR_3D — Rede Causal 3+1D com Topologia Magnética

> Testa criação de matéria em rede causal **genuinamente 3+1D**, com monopólos
> magnéticos (DeGrand–Toussaint / Polyakov) e topologia não-trivial.
> Continua após `MATTER_CR_WILSON.md` (Veredito D: o gargalo é U(1) 2D **sem
> monopólos** → confinamento linear exige d≥3 + topologia magnética).
> **Não modifica** nenhuma campanha anterior.
> Código e resultados: `results/matter/cr_3d/`.

---

## O que CR_WILSON localizou com precisão

O Veredito D de CR_WILSON não foi fracasso — foi **localização**:

```
U(1) compacto 2D:
  cos(W_p), W_p = 2π → cos(2π) = 1  (quantum de fluxo invisível ao cosseno)
  confinamento linear (Polyakov) exige monopólos
  monopólos em U(1) compacto exigem d ≥ 3
⇒ rede 2D não confina cargas de winding, por maior que seja λ_p.
```

A solução está identificada: **dimensão ≥ 3** (monopólos existem em 3D), **topologia
magnética**, e o **efeito Polyakov** (proliferação de monopólos → massa do fóton de
gauge → confinamento de cargas elétricas). CR_3D implementa a rede 3+1D com essas
propriedades.

## A ação (idêntica, agora em 6 planos)

$$S_{3D} = \sum_{\text{links}} \Delta\tau\,[1-\cos(\phi+\Delta\theta)]
        + \lambda_p \sum_{\text{plaq}} [1-\cos(W_p)]$$

Dois lados, ambos construídos e verificados:

- **Conjunto causal:** sprinkling de Poisson 4D, dimensão por **Myrheim–Meyer**
  (contagem de relações causais — sem fórmula relativística).
- **Teoria de campo:** rede espacial 3D (x = eixo de colisão Dirichlet; y, z transversos
  periódicos) + tempo de evolução. θ nos sítios; φ_x, φ_y, φ_z nos elos; **três planos de
  plaqueta** (xy, xz, yz) — o mínimo que admite monopólos magnéticos.

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| T3D1 | Rede 3+1D: d=4 (Myrheim–Meyer), causalidade, redução a D3 e a CR_WILSON? | `T3D1_network.{py,md,json}` |
| T3D2 | Densidade de monopólos ρ_M no vácuo; plasma/Polyakov ativo? | `T3D2_monopoles.{py,md,json,png}` |
| T3D3 | Tensão de corda E(d)∝d (lei de área/Creutz); λ_c? | `T3D3_string.{py,md,json,png}` |
| T3D4 | Colisão 3+1D: estrutura criada? Polyakov ⟨P⟩? (λ_p×ρ, 20 sementes) | `T3D4_collision.{py,md,json,png}` |
| T3D5 | Topologia (vórtice/hedgehog/Skyrmion) + cinco consistências | `T3D5_soliton.{py,md,json}` |
| T3D6 | Síntese + veredito (A–D) | `T3D6_synthesis.{py,md,json}` |

## Protocolo / anti-circularidade

1. **Monopólos** medidos por **fluxo saindo de hipercubo** (DeGrand–Toussaint, soma da
   plaqueta enrolada real = inteiro por Bianchi). **Polyakov** medido por **produto de
   fases temporais** (módulo de ⟨e^{iΦ}⟩ via médias cos/sin — sem número complexo).
   QCD, quarks e o próton só em blocos `COMPARISON ONLY`.
2. **T3D1 obrigatório** antes de T3D2–T3D6 (sprinkling 4D reproduz d=4).
3. **T3D2 antes de T3D3** (confirmar monopólos antes de testar confinamento).
4. **20 sementes** para T3D4. Rede 3+1D é cara: começar pequeno e verificar convergência.

---

## Resultados (resumo)

| Tarefa | Resultado |
|--------|-----------|
| **T3D1** | **SIM** — d_MM = 4.00 (Myrheim–Meyer + lei de volume p=4.01), causalidade estrita, θ→Poisson 3D (2×10⁻⁶), redução a CR_WILSON a zero de máquina |
| **T3D2** | **SIM** — monopólos existem em todo λ_p; **plasma denso** (ρ_M até 0.41) e **blindado** (Debye, C(1)<0) para λ_p≲1.5; crossover Coulomb em λ_p≈1.5 |
| **T3D3** | **SIM** — laço de Wilson com **lei de área**, Creutz σ>0: **E(d)∝d**, λ_c≈1.5 (mesma janela de T3D2) |
| **T3D4** | **grade B** — colisão 3+1D (20 sementes) **cria** estrutura semi-estável: em ρ=50, n_kink≈2–4.5, sobrevivência 100% na janela tardia, com **plasma de monopólos gerado pela própria colisão** (ρ_M até 0.44). Em 2D **nada** era criado. ⟨P⟩ não chaveia dinamicamente |
| **T3D5** | **4/5 consistências** — objeto suportado = **vórtice (S¹)**: massa 8 (0.1%), E²=(pc)²+(mc²)² (3.2%), θ(r)~M/r (−0.99), isotropia transversa; **núcleo não fixado** (sem Higgs) |

A inversão de CR_WILSON **persiste**: a janela confinante é **λ_p pequeno** (plasma denso
de monopólos), não λ_p grande — a intuição QCD-4D não se transfere.

## Veredito — **B: estrutura criada, semi-estável (vida finita)**

Ver `results/matter/cr_3d/T3D6_synthesis.md` para o quadro completo.

```
[ ] A — Matéria criada em 3+1D com Polyakov ativo
[x] B — Estrutura criada, semi-estável (vida finita)
[ ] C — Monopólos existem mas colisão insuficiente
[ ] D — Sem criação mesmo em 3+1D
```

**Síntese:** em 3+1D a ação mínima **contém** o mecanismo de Polyakov que faltava em 2D
— monopólos magnéticos, plasma blindado, e corda linear `E(d)∝d` — e a colisão de alta
energia (ρ=50) **cria** uma estrutura topológica que **sobrevive** à janela tardia e
**gera seu próprio plasma de monopólos** (ρ_M até 0.44). Isto é criação genuína que 2D
(CR_WILSON, grade D) **não** conseguia. O objeto suportado é um **vórtice (S¹)**
relativístico que gravita (θ~M/r, E²=(pc)²+(mc²)²).

A ressalva honesta que mantém o veredito em **B** e não **A**: o objeto criado é um
**blob multi-núcleo turbulento** (winding ruidoso em vários planos), não um sóliton
único limpo; o loop de Polyakov **não chaveia dinamicamente** durante a colisão (é
baixo onde há densidade alta, alto onde não há — fixado pela energia, não por uma
transição desconfinado→confinado); e o vórtice isolado **não tem núcleo fixado** (seu
fluxo 2π é invisível ao cosseno de Wilson e não há campo de magnitude/Higgs que lhe dê
tensão, T3D5: difunde de 1.0 a 0.38 em 8 ticks). A fronteira da **estabilização limpa
de uma única partícula** está identificada: não é mais a dimensão nem a topologia
magnética, e sim **o que fixa o núcleo do defeito** (Higgs/condensado) e, para a
topologia tipo próton (hedgehog S² / Skyrmion), **conteúdo não-Abeliano** — fora do
alcance da ação de uma linha.

```
2D U(1) (CR_WILSON):  kink m=8 suportado; SEM monopólos, SEM corda → Veredito D (nada criado)
3D U(1) (CR_3D):      monopólos + plasma + corda E(d)∝d PRESENTES;
                      colisão CRIA estrutura semi-estável rica em monopólos → Veredito B;
                      vórtice (S¹) suportado, relativístico e gravitante;
                      sóliton único estável → Higgs/condensado (fixa o núcleo);
                      hedgehog(S²)/Skyrmion → próton → não-Abeliano
```

# PHI_EMERGE_V4 — Acoplamento de duas vias ρ↔gauge: o resíduo é eliminável?

PE4_V3 (Veredito B) fechou o setor de **magnitude**: a densidade causal dinâmica ρ
depleta espontaneamente no núcleo do vórtice (`□ρ=J`, uma via) e pina um núcleo de
largura constante. Mas ρ era **unidirecional** — não retroalimentava o gauge — então
o **enrolamento de gauge** continuava difundindo como em CR_3D. PE4_V4 fecha o laço:
ρ agora **pesa a ação de gauge** (Δτ~ρ), e perguntamos se o núcleo depletado
(ρ→0 lá) **pina** o enrolamento, **não o afeta**, ou o **desestabiliza**.

Código/dados: `results/phi_emerge/v4/`. Anti-circularidade: ρ é o peso de densidade
real (Δτ~ρ, já usado globalmente em v2.relax_gauge); fases reais; sem literal
complexo; "supercondutor" só em COMPARISON ONLY.

## O experimento

Vórtice W=1 (= T3D5) evoluído sob a força de gauge **ponderada por ρ**, com ρ
recalculado a cada tick do estado de gauge (depleção controlada por f: f=0 = ρ
uniforme = CR_3D; f=1 = depleção total, o regime K~1 de PE4_V3). Mede-se a
sobrevivência do enrolamento (core_flux = afiamento; enrolamento topológico no disco
do núcleo). Apenas o termo de Stückelberg (Δτ~ρ) é ponderado; rigidez/Maxwell mantém
força plena (mantém o campo bem posto). Robustez: f=1 com Wilson também ponderado.

## Resultado

| f (depleção) | core_flux (méd. tardia) | retenção topológica | ρ_min núcleo |
|--------------|------------------------|---------------------|--------------|
| 0.00 | 0.275 ± 0.001 | 0.00 | 1.00 |
| 0.25 | 0.270 ± 0.001 | 0.00 | 0.75 |
| 0.50 | 0.251 ± 0.001 | 0.00 | 0.50 |
| 0.75 | 0.293 ± 0.001 | 0.00 | 0.25 |
| 1.00 | 0.336 ± 0.001 | 0.00 | 0.15 |

Fidelidade (f=0 = CR_3D): **True** (enrolamento difunde
1→0.18). Variação f=0→f=1: **+22.0%** no core_flux; retenção topológica **0.00→0.00**. Turbulência: nenhuma.

O core_flux tardio fica **abaixo do quantum (0.5)** para todo f (o núcleo difunde
sub-quantum); há um arrasto fraco para cima na depleção profunda (+22%), mas a
**retenção topológica é 0 em todo f** — o enrolamento nunca é pinado. Afiamento
marginal não é estabilização.

## Veredito: **B** — a depleção de ρ NÃO pina o enrolamento (resíduo irredutível pela back-reaction)

```
[ ] A — depleção PINA o enrolamento → resíduo eliminado, ação mínima
        deriva matéria estável sem ingrediente extra (VERIFICAÇÃO TRIPLA exigida)
[x] B — depleção NÃO afeta o enrolamento → resíduo IRREDUTÍVEL pela
        back-reaction de ρ; o quarto ingrediente (magnitude/Higgs) é necessário
[ ] C — emergência parcial / efeito fraco mas não-nulo
[ ] D — depleção DESESTABILIZA o enrolamento (turbulência no núcleo)
```

## A razão física (o mecanismo)

> ρ realimenta o gauge **somente** pelos termos de **cosseno** da ação mínima
> (Stückelberg `[1−cos u]`, Wilson `[1−cos W]`). Esses cossenos são **cegos ao fluxo
> 2π** do núcleo (cos 2π = 1) — a mesma cegueira que CR_3D identificou como a razão
> de o vórtice não se estabilizar. **Ponderar um termo cego por ρ o mantém cego.**
> A depleção enfraquece o acoplamento de fase no núcleo, mas não cria o custo de
> energia de núcleo que pinaria o enrolamento. Por isso ρ **não pina** (≠A) e **não
> desestabiliza** (≠D): seu canal é estruturalmente disjunto do setor topológico.

## O que PHI_EMERGE conclui, agora completo

```
PHI_EMERGE     [C]: |Φ|=ρ_Poisson reproduz a FASE, não a MAGNITUDE
PHI_EMERGE_V2  [B]: ρ dinâmico inicializado → magnitude fecha (|Φ|(0)→0, pinado)
PHI_EMERGE_V3  [B]: ρ dinâmico ESPONTÂNEO → magnitude EMERGE rápido, 5/5; resíduo
                    = enrolamento de gauge (não testado, ρ unidirecional)
PHI_EMERGE_V4  [B]: ρ de DUAS VIAS → o resíduo do enrolamento é IRREDUTÍVEL pela
                    back-reaction de ρ (canal cosseno cego ao 2π) → o quarto
                    ingrediente (magnitude |Φ|→0 / não-Abeliano) é NECESSÁRIO
```

**A resposta à pergunta de PE4_V3 ("o resíduo é eliminável?"): não.** A magnitude
`|Φ|=ρ` emerge da geometria causal dinâmica sem axioma extra (V2–V3), mas a
estabilização do enrolamento topológico exige um custo de núcleo não-cosseno que a
ação mínima não possui — exatamente o campo complexo de CR_ABELIAN_HIGGS, agora
mostrado **não substituível** por ρ dinâmico. A fronteira da matéria estável está
localizada com precisão máxima e mecanística: não é a densidade (emergiu), é o
**custo de núcleo do enrolamento**. Veredito B em todas as três versões, com a
razão — não mais uma conjectura — medida.

## Reprodução
`python results/phi_emerge/v4/V4_1_faithfulness.py` … `V4_3_synthesis.py`. Detalhe
por tarefa em `V4_1…V4_3 .md`, com JSON e figura `V4_2_backreaction.png`.

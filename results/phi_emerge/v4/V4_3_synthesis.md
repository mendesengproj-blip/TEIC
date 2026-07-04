# V4_3 — Síntese e veredito de PHI_EMERGE_V4

## Quadro
```
V4_1 — f=0 reproduz CR_3D (difusão do enrolamento):  True
V4_2 — core_flux f=0 → f=1:                          0.275 → 0.336 (+22.0%)
V4_2 — retenção topológica f=0 → f=1:                0.00 → 0.00
V4_2 — turbulência (blow-up):                        nenhuma
```

## Veredito: **B** — depleção não pina o enrolamento
```
[ ] A — depleção PINA o enrolamento → resíduo eliminado, ação mínima
        deriva matéria estável sem ingrediente extra (VERIFICAÇÃO TRIPLA exigida)
[x] B — depleção NÃO afeta o enrolamento → resíduo IRREDUTÍVEL pela
        back-reaction de ρ; o quarto ingrediente (magnitude/Higgs) é necessário
[ ] C — emergência parcial / efeito fraco mas não-nulo
[ ] D — depleção DESESTABILIZA o enrolamento (turbulência no núcleo)
```

### A razão (mecanismo, não apenas observação)

ρ realimenta o setor de gauge **somente** pelos termos de cosseno da ação mínima —
Stückelberg `[1−cos(u)]` (peso Δτ~ρ) e Wilson `[1−cos(W_p)]`. **Ambos são cegos ao
fluxo 2π** do núcleo do vórtice (cos 2π = 1). Ponderar um termo cego por ρ não o faz
enxergar: a depleção enfraquece o acoplamento de fase local, mas não introduz o
**custo de energia de núcleo** que pinaria o enrolamento. Logo a back-reaction de ρ
**não pode**, por construção da ação mínima, estabilizar o enrolamento — e também
não o desestabiliza (o termo de rigidez/Maxwell, não-ponderado, mantém o campo bem
posto). O resíduo é **irredutível** pela densidade causal dinâmica.

## O que isto fecha em PHI_EMERGE

PE4_V3 deixou uma pergunta exata: o resíduo do enrolamento é eliminável tornando ρ
de duas vias? **Resposta: não.** O canal de ρ (cossenos) é estruturalmente disjunto
do que controla a topologia do enrolamento. O quarto ingrediente de CR_AH —
magnitude `|Φ|→0` no núcleo — não é substituível por ρ dinâmico; ele é o custo de
núcleo não-cosseno que a ação mínima não tem. PE4_V4 converte a calibração honesta
de PE4_V3 ("não testado") em um resultado **medido e mecanístico**.

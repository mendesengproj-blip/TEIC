# G6 -- Síntese: o setor de gauge acoplado cria matéria?

## Quadro de resultados

```
G1 — Dinâmica acoplada consistente:     SIM (θ-puro=force_cos, φ-puro=sine-Gordon massa 8, energia conservada)
G2 — Transferência θ → φ:               SIM (até 57% da energia ao setor de gauge; taxa cresce com ρ)
G3 — Kink criado por colisão (W_φ≠0):   MARGINAL (par só em ρ≥50, no regime mal-posto)
G3 — Limiar ρ_gauge:                     NÃO no regime controlado (peak_φ<π até ρ_π=18)
G4 — Kink isolado estável:               SIM (massa 8.0 ≈ 8)
G4 — Par virtual (transiente):          SIM (nuclea e aniquila)
G4 — Consistência com CC:                qualitativa (winding=N_interno; τ(N) não-numérica)
G5 — Carga topológica conservada:       SIM (Q=0 sempre; criação em pares ±)
```

## Cenário

```
[ ] 1 — Kinks estáveis criados na colisão acoplada → matéria da TEIC
[x] 2 — Pares transientes (setor de gauge compacto: par kink-antikink nuclea e aniquila) → pares virtuais QFT
[x] 3 — Sem criação ESTÁVEL no regime controlado (só marginal/mal-posto) → fronteira mais profunda (precisa de dinâmica de plaquetas/Wilson ou campo externo)
[ ] 4 — Sem transferência θ→φ → Stückelberg ineficaz (EXCLUÍDO: G2 mostrou transferência efetiva)
```

## A resposta honesta

A ação de uma linha `S = Σ Δτ[1−cos(φ+Δθ)]`, com θ (nós) e φ (gauge, links)
**acoplados** dentro do cosseno, foi testada pela primeira vez no regime de
colisão. O resultado tem três camadas:

1. **A transferência Stückelberg é real (Cenário 4 EXCLUÍDO).** Partindo de toda a
   energia nas cadeias escalares e o gauge frio, até 57% flui para o setor de gauge; a taxa cresce com a inclinação das cadeias (mesma
   não-linearidade de fase→π de DBI2). Os setores **falam** dinamicamente.
2. **O setor de gauge hospeda matéria topológica (Cenário 2).** Um kink carregado
   isolado é **estável** (massa 8.0 ≈ sóliton sine-Gordon 8); uma colisão
   de gauge nuclea um **par kink-antikink transiente** que aniquila (pares
   virtuais). A carga topológica Q=∮dφ/2π é **conservada** (G5): criação só em
   pares ±, nunca uma carga isolada do vácuo.
3. **Mas a colisão acoplada NÃO cria matéria estável no regime controlado
   (Cenário 3).** A energia transferida termina como **radiação de gauge**; a fase
   φ só atinge π (limiar de nucleação) em ρ≳50 — exatamente onde o setor escalar
   já é **mal-posto** (runaway, `cos''<0` acima de ρ_π=18). Lá nuclea um par em
   ~15% das sementes, mas no regime descontrolado — não é criação limpa.

**Conclusão:** a ação mínima acoplada contém **a transferência** (Stückelberg
efetivo) **e o objeto** (kink de gauge estável, pares virtuais, carga conservada),
mas **não** converte uma colisão escalar em matéria **estável** no regime
controlado. A fronteira é mais profunda do que o acoplamento Stückelberg: criar um
kink estável a partir de cadeias exige estrutura adicional — dinâmica própria de
A_μ (Wilson loops + plaquetas, BRIDGE_WILSON) ou um campo/assimetria externa que
separe a carga antes da aniquilação. É o mesmo veredito de DBI (Cenário 3),
agora **refinado**: o gargalo não é a transferência (que funciona), mas a
**estabilização** da carga criada.

## Mapa de camadas (fechado)

```
BD linear     → sem criação              (CR3)
DBI escalar   → sem winding              (DBI3: campo não-compacto)
DBI compacto  → kink estável / par virtual (DBI4: setor isolado)
DBI acoplado  → transferência SIM, par virtual SIM, matéria estável NÃO  (CR_GAUGE)
  estável exige → dinâmica de gauge própria (plaquetas) ou campo externo
```

## Conexão Oxford/Lisboa

Oxford: três campos EM polarizam o vácuo (via pares virtuais e⁻e⁺ da QED) e geram
um quarto campo. TEIC: duas cadeias escalares transferem energia ao setor de gauge
via Stückelberg (G2) e nucleiam pares kink-antikink **transientes** (G4) — o
intermediário de pares virtuais está **na topologia do campo de gauge**, sem
precisar de pares e⁻e⁺ como entidade separada. Mas, como em Oxford, o quarto campo
é transiente: estabilizá-lo exige mais que a colisão.

![G2](G2_transfer.png)
![G3](G3_collision.png)

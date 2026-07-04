# DBI6 -- Síntese: o setor não-linear (DBI) cria matéria?

## Quadro de resultados

```
DBI1 — propagador cos validado (BD fraco + D3):  SIM
DBI2 — fase crítica π atingida em ρ_π:           SIM, ρ_π = 18.0 ρ₀
DBI3 — loops criados (setor escalar, ψ>0):       NÃO (pass-through subcrítico)
DBI3 — winding ≠ 0 (setor escalar):              NÃO (∮Δθ=0, campo não-compacto)
DBI4 — kink isolado estável (campo compacto):    SIM (massa 8.0 ~ 8)
DBI4 — par kink-antikink:                        TRANSIENTE (aniquila → pares virtuais)
DBI4 — τ(N_criado) bate com CC2:                 N/A (só correspondência qualitativa)
DBI5 — ρ_DBI ≈ ρ(a₀):                            NÃO (ρ_DBI é UV, a₀ é IR)
```

## Cenário

```
[ ] 1 — ρ* existe, loops estáveis → DBI cria matéria
[x] 2 — ρ* existe, loops instáveis → pares virtuais (setor COMPACTO: par kink-antikink transiente, aniquila)
[x] 3 — criação estável exige além do setor escalar → o setor de gauge A_μ (winding vive na fase compacta, não no campo de densidade)
[x] 4 — regime ultra-forte (ρ > ρ_π): perda de hiperbolicidade, fuga não-convergente — fronteira de validade da ação escalar
```

## A resposta honesta

O setor **escalar** (campo de densidade) da ação mínima cos **não cria matéria**:

- Abaixo de ρ_π ≈ 18ρ₀ a colisão é **pass-through** (ψ_tardio ~ 0,
  W = 0): a não-linearidade do gradiente só amolece a sobreposição — estende o
  nulo de CR3 ao regime não-linear-mas-subcrítico.
- Acima de ρ_π (`cos'' < 0`) a evolução **perde hiperbolicidade** e foge de forma
  não-convergente (mal-posta) — **Cenário 4**, uma quebra da ação, não criação.
- O **winding é estruturalmente zero** porque o campo de densidade é não-compacto
  (valor único). A MESMA dinâmica num campo **compacto** (S¹) sustenta um kink
  isolado **estável** (massa 8.0, = sóliton sine-Gordon) e
  nuclea um **par kink-antikink transiente** que **aniquila** (análogo a pares
  virtuais, **Cenário 2**). Um kink carregado isolado **não** pode nascer do vácuo
  (winding conservado) — regra de seleção topológica.

**Conclusão:** a criação de matéria **estável** exige o setor de gauge **A_μ**
(onde a fase é genuinamente compacta), não o setor escalar θ — **Cenário 3**. E a
escala de criticalidade ρ_DBI é **UV (granularidade, X₀∝ρ)**, não a escala IR
cosmológica a₀ (DBI5) — reproduzindo C3/W4 pelo lado da criação.

## O que isto diz à física (mapa de camadas)

```
BD linear      → não cria             (CR3: D)
DBI escalar    → não cria estável     (este trabalho: pass-through / mal-posto)
DBI compacto   → pares virtuais       (transientes, aniquilam — Cenário 2)
  estável exige → setor de gauge A_μ  (Cenário 3, próxima camada)
  escala        → UV, não a₀ (IR)     (DBI5)
```

A ação de uma linha `S = Σ Δτ[1−cos(φ+Δθ)]` contém a estrutura para pares
virtuais (no setor compacto) mas **não** produz matéria estável a partir do
campo escalar sozinho. A fronteira TEIC↔QFT está agora mapeada por quatro
caminhos independentes: e11 (escala), M1-S1 (dispersão), CR3 (criação linear),
DBI (criação não-linear → precisa de A_μ).

![DBI2](DBI2_phase_map.png)
![DBI3](DBI3_collision.png)
![DBI5](DBI5_a0.png)

# VS1 — O Higgs como condensado causal espontâneo?

> Charter: `VACUUM_STRUCTURE.md` (VS1). Pergunta: ⟨ρ_dinâmico⟩ ≠ ρ₀
> espontaneamente, sem vórtice inicializado, em regime de alta densidade?
> Código: `VS1_higgs_condensate.py`; dados: `VS1_higgs_condensate.json`.
> Infraestrutura: v2_core (solver estático conservante), phi_emerge_core,
> cr3d_core, v3_core (GRID) — nenhuma modificada.

## Protocolo (4 medidas, 3 sementes cada)

(a) **Controle cinemático** — contagem de Poisson pura em densidade
crescente. (b) **Vácuo dinâmico** — campo de gauge inicializado em
desordem s ∈ {0.3, 1.0, π}, esfriado pela ação mínima (sem vórtice em
lugar algum); sua ação residual J_vac alimenta o setor de ρ dinâmico
(equilíbrio estático `relax_density`, o minimizador de V2 que V3 provou
ser o limite t→∞ do campo real). (c) **Varredura de drive**
rho_factor ∈ {1..64} (rede mais densa = drive mais forte). (e) **Regime
linear** K=10 > K_c ≈ 8.5: o ganho dev_std/J_std deve ser constante se a
estrutura de ρ é resposta, e destacar-se se há instabilidade espontânea.

## Resultados

**(a) Cinemático:** std(ρ) cai 0.250 → 0.031 conforme ρ_sprinkle 2 → 128
(∝ 1/√ρ exato), média ≡ 1. Sem canal de condensação na contagem — alta
densidade *aproxima* o vácuo de ρ₀ uniforme, não o afasta.

**(e) Regime rígido K=10 > K_c (o discriminador central):** sobre 65× de
amplitude de drive (J_std 0.017 → 1.11), o ganho é constante:

```
ganho dev_std/J_std = 0.43 ± 0.01 nas 9 células (3 sementes × 3 desordens)
corr(δρ, J−⟨J⟩)     = −0.51 em todas as células
frac no piso ρ=0    = 0.000 (exceto 3% em s=π)
⟨ρ⟩                 = 1.0000 exato
```

Resposta **linear pura**: a estrutura de ρ é proporcional ao drive e
espacialmente escravizada a ele (correlação fixa). Quando J → 0, δρ → 0
(dev_std = 0.007 no vácuo mais ordenado). Não há quebra espontânea: o
campo não escolhe um valor ⟨ρ⟩ ≠ ρ₀ próprio; ele segue a inomogeneidade
que lhe é imposta, e some com ela.

**(b)(c) Regime mole K=1 < K_c — o achado lateral:** a amplitude de
equilíbrio da resposta (∝ rf·J/K, amplificada pelos modos longos da
caixa) **excede a profundidade de depleção total** mesmo para o ruído
residual minúsculo do vácuo quase-ordenado: 24% do volume no piso ρ=0 a
s=0.3, 43% a s=π (rf=16), com a massa conservada empilhada nas regiões de
baixa ação. O vácuo uniforme **não é uma configuração estável do regime
mole sob inomogeneidade arbitrariamente pequena** — mas a estrutura
continua determinística e correlacionada ao drive (corr ≈ −0.25 sob
saturação; idêntica sob esfriamento 4× mais longo). É instabilidade
*dirigida*, não condensação espontânea: nada aqui escolhe um ⟨ρ⟩ ≠ ρ₀
por conta própria.

**(d) Estado vítreo (s=π):** o vácuo quente esfriado congela num plasma
de monopólos (ρ_M ≈ 0.024, windings grandes presos); J_vac **não decai**
com esfriamento 4× mais longo (J_decay = 1.000). A estrutura persistente
de ρ nesse estado é **pinada por defeitos topológicos congelados**
(desordem quenched), não espontânea.

## Veredito

```
[x] CRITÉRIO DE MORTE DISPARA: ⟨ρ_local⟩ = ρ₀ em todos os regimes, no
    sentido preciso — o desvio local é resposta escravizada ao drive
    (ganho constante 0.43 e corr −0.51 no regime rígido; estrutura
    drive-determinística no regime mole), desaparece com o drive, e
    nenhuma média espontânea ⟨ρ⟩ ≠ ρ₀ aparece em regime algum.
[ ] Condensado espontâneo — NÃO observado.
```

**O Higgs NÃO é uma propriedade espontânea do vácuo da rede.** Isto fecha
por terceira via independente o que PE2 (sem condensação do Φ composto) e
PE4_V4 (custo de núcleo irredutível pela back-reaction de ρ) já haviam
localizado: a magnitude de Higgs é um ingrediente genuíno do andar de
cima, não um produto do substrato. A cadeia completa:

```
PE2:    Φ = ρ·e^{iφ̄} não condensa (sem potencial, sem ordem de magnitude)
PE4_V3: ρ dinâmico depleta no núcleo SE um vórtice existe (espontâneo dado o vórtice)
PE4_V4: a depleção não pina o enrolamento (cossenos cegos a 2π)
VS1:    sem vórtice, nada condensa — nem em alta densidade, nem no regime
        mole (onde há instabilidade, ela é dirigida e drive-correlacionada)
```

## Subprodutos registrados

1. **Instabilidade do regime mole**: para K < K_c, o vácuo uniforme é
   destruído por ruído arbitrariamente pequeno (depleção total em fração
   finita do volume) — candidato a critério físico para fixar K na ponte:
   a geometria precisa ser rígida o bastante (K > K_c) para o vácuo
   uniforme ser estável. Conecta-se à fronteira K_c ≈ 8.5 de PE4_V3 por
   um caminho independente.
2. **O vácuo vítreo**: esfriamento de desordem forte congela um plasma de
   monopólos com ação residual que não decai — o análogo de rede de um
   vácuo com desordem topológica quenched (defeitos primordiais).
3. **Artefato numérico documentado (relevante para reuso de v3_core):**
   `evolve_rho` com fonte que preenche a caixa inteira (i) vaza massa
   total pela borda espelhada do Laplaciano (deriva uniforme medida até
   40× em K=10, s=π) e (ii) a redistribuição do piso pode empurrar
   células para ρ<0. Irrelevante para o uso original de V3 (vórtice
   central localizado; observáveis relativos ao far-field), fatal para
   fonte de vácuo global. Por isso VS1 usa o minimizador estático
   conservante (`relax_density`), cujo equilíbrio é o limite t→∞ provado
   de V3. As medidas de flutuação (dev_std, corr) coincidem entre os dois
   solvers (0.477 vs 0.483 em K=10, s=π) — a conclusão não depende da
   escolha.

## Honestidade

- ρ global é conservado pelo solver (projeção a cada iteração); o clip
  final em ρ≥0 é só o piso físico, reportado via frac_floor.
- O experimento detecta condensação *local/estrutural*; a média global é
  conservada por construção — e é disso que a pergunta do charter trata.
- O "regime de alta densidade" entra por dois caminhos independentes
  (ρ_sprinkle na contagem; rho_factor no drive) — ambos negativos.
- Anti-circularidade: nenhum número complexo, nenhum parâmetro de
  condensado inserido; "Higgs" aparece apenas como nome. Sementes fixas.

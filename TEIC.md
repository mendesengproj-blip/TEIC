# TEIC — o resumo vivo da teoria

> **Language note (EN).** This is the programme's living summary, kept in Portuguese
> as the working language of the research record. The campaign documents it cites
> (`docs/…`, `results/…`) ship in this repository. The English front door is
> `README.md`.

> **Este arquivo é o abstract permanente do projeto.** Atualizar ao fim de cada
> campanha: o que mudou de status entra aqui; o detalhe fica nos documentos de
> campanha. Última atualização: **jun/2026, pós-E4/E5 + pivô editorial.**
>
> **Pivô editorial (jun/2026, após desk-reject da CQG ao Paper I).** Diagnóstico:
> o desk-reject foi por ESCOPO (lê como "teoria de tudo") + venue errado (CQG p/
> conteúdo que reproduz CST) + novidade mal posicionada — NÃO por falta de
> matemática. Correção: estreitar e separar venues. Dois "papers-bala" focados,
> framework mínimo, compilados e prontos:
> `paper/PAPER_BTFR_MNRAS_submit.tex` (7 pp, classe mnras: predição a₀∝H(z) +
> teste Ciocan 2026; com seção de robustez/sistemáticos e ΛCDM-Ludlow 2017) e
> `paper/PAPER_GOLDSTONE_PRD.tex` (5 pp, revtex/PRD: ordem orientacional + setor
> de Goldstone escalar, com as 3 figuras E4). Cover letters: `COVER_*.md`.
> Documentos densos `TEIC_DOC1_FOUNDATIONS.tex` (15 pp) + `TEIC_DOC2_*` ficam
> como guarda-chuva Zenodo. `PAPER_PHOTON_PRD.tex` SUPERADO (ver E4).
>
> Antes disso: VACUUM_STRUCTURE (VS1–VS5); TEIC_MASTER; os 5 papers I–V.

---

## A tese em um parágrafo

Uma rede causal discreta com sprinkling de Poisson — eventos como centros de
expansão causal — analisada com protocolo estritamente anti-circular, gera
espontaneamente: relatividade especial, dimensão, gravitação de Schwarzschild,
curvatura (tudo coincidindo com a Causal Set Theory), **e além da CST**: a
estrutura completa de operadores de uma EFT escalar-vetor-tensor de gravitação
modificada testada contra rotação galáctica, um setor de matéria topológica
SU(2) com estabilizador de Skyrme emergente, relações cruzadas sem parâmetros
livres entre gravitação e matéria, e uma Λ flutuante com coeficientes medidos.
Nada é forçado; negativo é reportado como negativo; kill criteria são
pré-registrados.

## O que está medido (e onde)

### Geometria — coincide com CST (o chão sólido)
| Resultado | Medida | Fonte |
|---|---|---|
| RE emerge; grade regular falha LI | corr 0.9998–1.0000; CV 0.8% vs 17% | R1 |
| Volume/dimensão | d = 2.006, 4.004 | R2 |
| Schwarzschild não-circular | corr 1.0000, err máx 0.21% | R3 |
| Curvatura: volume≠cadeia | 23.5σ; coef −1/96 (Ricci) | R4 / Tasks A–B |
| Regime não-linear | +3/2 correto; 0.06% até r=2.5GM/c² | NL1–NL3 |

### Além da CST (a contribuição própria)
| Resultado | Medida | Fonte |
|---|---|---|
| Ação mínima: 5 operadores forçados {X, DBI, A·∂θ, F², A²} | razões (1,2) algébricas — dito explicitamente | C1–C4, W1–W3 |
| Operadores proibidos = exclusões observacionais | Horndeski G₄ₓ/G₅ ⟷ GW170817; frame n^μ ⟷ Fermi-LAT | §9.5, OP1 |
| LIV E/B≈3 morta: artefato de regulador | teorema e²>b² exato; defeito de boost 0.98→0.003 (40–54σ) | LV1–LV4b |
| Operador de Skyrme emerge da isotropia de Poisson | 5/9 a 0.06%; grade cúbica cega; λ_Sk=a/√120 | SC1–SC3 |
| Dominância de Skyrme: impossível (teorema) | K≤⅔S identidade pontual; sinal ≤0 em qualquer medida; 5/9 em links reais | SD1–SD4 (MORTE forte) |
| SU(2) é o grupo mínimo consistente | cadeia escalar→discretos→U(1)→SU(2) medida; Bott fecha acima | MIN1–MIN3 |
| Premissas mecânicas de FR (spin-estatística) | loop de troca fecha; 2π arrasta ao antípoda (7e-16) | MATTER_FR_EXCHANGE |
| **FR medido**: [troca]=[rot-2π]=1 ∈ π₁=ℤ₂ | Pontryagin–Thom na rede; 2-torção e par bosônico medidos; ε-calibrado (condição declarada) | PI0–PI4 |
| 1ª relação cruzada sem parâmetros | G_net·ρ²·r_c⁵ → 15/8π² (2.5%); G_net·ρ²·r_c³·λ²_Sk = 3/320π² | CR1–CR2 |
| Constante pura de X₀ (estatística de extremos) | X₀·Δθ_max⁻² = πρH²/ln2; Exp(1) exato; fechamento 0.29% | CR3 |
| Massa vetorial: número puro escala-invariante | m²_iso·λ_p ≈ 520 (CV 5.3%, ρ×4.7); herança PE3 √ρ MORTA (9.5σ) | CR4 |
| Λ flutuante: coeficientes medidos | δρ/ρ=1/√(ρV) (0.971±0.05); de Sitter R²=0.9999; 10⁻¹²² herdado CST | L1–L3 |
| d=3 por exclusão estrutural | única com gravidade ligada+escape E sóliton estável; Derrick={3} | DS1–DS3 |
| d=3+1 NÃO emerge da dinâmica (e7) | causets não-manifold, d*=1.43; seeds não fluem | T3A–T3B (MORTE) |
| ℏ estrutural: k ∝ N | α=1.008, R²=0.99997; franjas ∝ 1/N; escala absoluta segue externa | T3C |

### Negativos fechados (pagos — não reabrir sem porta nova)
ℏ absoluto da geometria (e11) · a₀∼cH (C3: X₀∝ρ é UV) · regra de Born (dois
andares) · ponte vetorial dilatônica · dimensão emergente da regra e7 (T3A/T3B)
· dominância de Skyrme pela ação mínima (SD1–SD4: teorema de impossibilidade)
· condensado espontâneo do vácuo (VS1: resposta linear escravizada ao drive,
3ª via depois de PE2/V4) · transição de fase do vácuo no probe dinâmico (VS2:
crossover suave; onset de monopólos s≈1 sem salto) · degenerescência de
gerações no setor B=1 (VS4: bacia única, 10 perfis → mesma massa a 0.02%)
· neutrino neutro de vida longa (VS3: marca ℤ₂ de spin-½ sem carga B
desenrola como perturbação trivial; spin-½ estável exige B≠0 bariônico)
· constantes de acoplamento por aritmética dos 4 números puros (VS5: matches
= expectativa de acaso; α conteria ℏ — contradição com dois andares).

### Fóton: campanha E4 (jun/2026) — identificação ingênua FALSIFICADA por medição
O "fóton = magnon de Goldstone do ferromagneto de orientação" (alegado em Paper II)
foi testado e **morreu**. Charter `E4_PHOTON_DISCRIMINATOR.md`; dados em
`results/vacuum_structure/orientation/e4/`.
| Teste | Medida | Veredito |
|---|---|---|
| E4-0 FSS | m(N) sobe 0.961→0.991 (N:175→1462), U4=2/3, 13–38× acima do piso N⁻½ | ordem de longo alcance **GENUÍNA** (reforça E1) |
| E4-1 locking | corr autovetor↔k̂ = 0.10, teste de permutação p=0.23 | **escalares, NÃO vetor de gauge** → fóton excluído |
| E4-2 iso/deg | split 0.037, CV direcional 0.042; S(k)~k⁻⁰·⁵⁸ (diagnóstico) | par escalar limpo, degenerado, isotrópico |
Conclusão: os Goldstones de orientação carregam índice **interno** desacoplado do
espaço-tempo → são 2 escalares (pião-like; consistente com o octeto SU(3)), não um
fóton. O fóton, se emergente, mora no **setor de conexão de link** (E5), não aqui.
A conjectura foi retratada no paper; o resto da teoria (gravidade, matéria, MOND,
DM) NÃO dependia do fóton e segue de pé.

### Fóton: campanha E5 (jun/2026) — setor de link U(1); motor validado, E5-1 INCONCLUSIVO
Charter `E5_PHOTON_LINK_SECTOR.md`; `results/gauge/e5/`. Motor U(1) Wilson no grafo
causal. **Motor PLENAMENTE VALIDADO:** G1 invariância de gauge (1.8e-15, exato); G2
transição 4D U(1) (pico β=1.00≈β_c≈1.01); **G3 RESOLVIDO** com motor vetorizado
(`e5_fast.py`, validado vs lento): 4D C/N_plaq cresce com volume (slope +0.44 =
transição), 3D plano (+0.01 = crossover). **E5-1 (primeiro scan no causal set):**
plaquetas-diamante são gauge-invariantes (1.8e-15, positivo limpo) — U(1) é
bem-definida no grafo causal. MAS o scan de confinamento deu **INCONCLUSIVO**: peguei
meu próprio over-call ("deconfinement-like") — C/N_plaq cresceu ×3.32 entre 2
tamanhos, mas a geometria de diamantes explodiu sem controle (plaquetas ×8.9 vs
eventos ×2.2); expoente normalizado 0.55 (entre crossover 0 e 1ª ordem 1). Não
decide deconfinamento vs confinamento. NENHUMA alegação de fóton. Falta: geometria
de plaqueta controlada + ≥3-4 tamanhos + estimador Wilson-loop lei-de-área.
**E5-1b (tentativa de geometria controlada): OBSTRUÍDA por princípio.** O fix
(corte de tempo próprio τ_max, Lorentz-invariante) FALHOU: grau médio ainda cresce
34→133. Razão: a região {futuro, τ≤τ_max} tem volume INFINITO em Minkowski (boosts
estendem a hiperboloide ao infinito espacial) — nenhuma vizinhança local de volume
finito Lorentz-invariante existe (a tensão LI/discretude/localidade dos causal sets,
a mesma que força o operador BD não-local). Conclusão honesta: a U(1) de Wilson nos
diamantes NUS herda a não-localidade mean-field do substrato; um teste de fóton no
link exige uma construção de gauge BD-suavizada (análogo ao que E2 fez no setor
escalar), não Wilson nu. Motor U(1) segue validado (G1+G2+G3) e gauge-invariante nos
diamantes — esses positivos ficam. Sem alegação de fóton. Fronteira honesta: a
mesma não-localidade que o BD domou no escalar reaparece como obstrução no gauge.

### Fóton: campanha E6 (jun/2026) — gauge no link: estrutura SIM, propagação NÃO
`results/gauge/e6/`. **H1 (E6-1) PASS:** Maxwell não-compacta (1-cochain nos links,
F_P=dθ nos diamantes) é gauge-invariante exata; modos gauge = N−1 (redundância
COMPLETA), 698 harmônicos, 1184 físicos transversos. O setor de link TEM a estrutura
de gauge que o E4 (escalares internos) NÃO tinha — positivo estrutural real. **H2
(E6-2) FALHA:** a ação ½ΣF_P² é positiva-definida (Euclidiana, mínimo em ω≈0), não dá
ω=ck; o fóton Lorentziano exige ação de assinatura indefinida (split E/B = operador
de gauge BD-Lorentziano), não construído (research-grade, não fabricado).
**CONCLUSÃO E4→E6: nenhum fóton emergente estabelecido em nenhum setor; mapeado
exatamente onde/por quê é difícil.** Estrutura de gauge disponível no link, mas a
propagação relativística exige domar a não-localidade do causal set para um 1-form
(como o BD fez no escalar). Melhor afirmação publicável = E4 (ordem orientacional +
Goldstone escalar relativístico; fóton localizado estruturalmente, não-propagante).

### Subprodutos da campanha do vácuo (VS, jun/2026)
K > K_c ≈ 8.5 como condição de estabilidade do vácuo uniforme (critério
físico p/ fixar K da ponte — VS1) · vácuo vítreo: quench forte congela
plasma de monopólos que não relaxa (VS2/VS1) · instabilidades numéricas
documentadas: `chiral_cool` rate≤0.002 em dx=0.5/e_sk=4; vazamento de B em
dx≥0.5; `evolve_rho` vaza massa com fonte global (VS3/VS4/VS1 notas).

## O que a teoria representa

A TEIC começou como redescoberta da CST por outra rota conceitual (expansões
locais sobrepostas vs ordem parcial abstrata) — e isso segue verdade para a
geometria. A fronteira atual: **a CST não tem setor de matéria, não tem ação
mínima e não prevê dinâmica galáctica; a TEIC tem os três, com coeficientes
amarrados à mesma granularidade e com pontos vulneráveis nomeados.** O valor de
G, ℏ e a₀ em unidades físicas segue externo (exige escala absoluta); o que é
calculável — e calculado — são **relações** entre setores na mesma rede, sem
nada ajustável.

## Onde a teoria pode morrer (previsões falsificáveis)

1. **BTFR em alto-z**: `Δlog v_flat = ¼ log[H(z)/H₀]`. Decisão exige z≳2 e
   σ_sys≲0.03 dex (~10–25 rotadores ricos em gás). Se a evolução for plana, a
   teoria morre. **Estado jun/2026 (`FALSIFICATION_BTFR_V3`):** MUSE-DARK III
   (79 SFGs, 0.33<z<1.44, regime de baixa aceleração) mede a₀ CRESCENDO com z
   (15σ); amplitude bate ¼log[H/H₀] a 0.5–0.9σ na âncora SPARC; forma linear
   1.2–1.7× mais rápida que H (2–3σ, âncora-dependente, indecidível). Kill não
   disparado; ΛCDM-sem-evolução é quem está a ~19σ. Vigília: SKA deep HI;
   Jeanneau+26 vs Ciocan+26 (massa-eixo vs aceleração-eixo).
2. **Dispersão de fótons exatamente nula na média** (herança da LI de Poisson)
   — distingue de LQG/Hořava.
3. **R(β)=S(β)/S(0)** a invariantes fixos — o observável de discriminação da
   campanha LIV.
4. **Falsificação interna**: qualquer rede futura que meça G_net e λ_Sk na
   mesma configuração e não encontre 3/320π² derruba a relação cruzada.

## Caminhos abertos (ordem de retorno/realismo)

1. **Programa de constantes** ← ✅ **EXECUTADO** (`CROSS_RELATIONS_II.md`):
   o quadro de quatro setores FECHOU — gravitação 15/8π² (2.5%), matéria 1/120
   (0.06%), saturação DBI π/ln2 (0.29%), massa vetorial ≈520 escala-invariante
   (CV 5.3%). Correção honesta: a herança PE3 (m_A∝√ρ) morreu no substrato
   causal (9.5σ); tabela CR2 corrigida em apêndice datado.
2. **π₁(config B=2) na rede** ← ✅ **EXECUTADO** (`MATTER_PI1_B2.md`): a
   identificação FR troca≅rotação-2π é igualdade de números MEDIDOS (classe 1,
   estável; 2-torção 0; par bosônico 0). Importado residual: π₄(S³)=ℤ₂ +
   quantização coletiva. Residual aberto: 2º calibrador swap de classe 1.
3. **Dominância de Skyrme** ← ✅ **EXECUTADO** (`SKYRME_DOMINANCE.md`):
   MORTE TOTAL na forma forte — K ≤ ⅔S é identidade PONTUAL (Cauchy–Schwarz,
   hedgehog satura); teorema do sinal: quártico ≤ 0 sob QUALQUER medida;
   sêxtico = artefato de truncamento (u(λ*)=8); curvatura move c₄
   (f=1+0.038Rρ^(−1/2)) mas anti-estabiliza. A fronteira virou teorema de
   impossibilidade; Paper II enuncia o custo de núcleo como necessário.
4. **Λ dinâmica** ← na fila (evolução temporal — o elo aberto de
   `LAMBDA_EVERPRESENT`); depois: 2º calibrador swap (PI1_B2) e vigília BTFR.
5. **Regras de crescimento alternativas** no motor N~2000 do Tier 3 (a morte do
   e7 vale para o e7, não para a família Rideout–Sorkin geral).
6. **Observacional**: acompanhar rotadores JWST a z≳2 (item 1 de morte).

Registro completo de experimentos futuros — fila imediata (FQ1 Skyrme, FQ2
2º calibrador), médio prazo incluindo CMB (FM1 S8, FM2 ISW, FM3 lensing),
longo prazo (FL) e observacional (FO) — com kill criteria pré-registrados:
`FUTURE_EXPERIMENTS.md`.

## Regras do projeto (invariantes)

Kill criteria pré-registrados antes de rodar · negativo reportado como negativo
· guard anti-circularidade em todo gerador · a teoria DEV nunca é nomeada no
paper · convenções de campanha em `docs/reports/ROADMAP_REVOLUCAO.md` e memória do projeto.

## Layout do repositório (reorganizado jun/2026)

```
TEIC.md; docs/reports/TEIC_NARRATIVE.md ← resumo vivo + narrativa canônica
docs/reports/ROADMAP_REVOLUCAO.md ← os 8 ataques e vereditos
PREDICTIONS.md, FUTURE_EXPERIMENTS.md ← setor falsificável + fila futura
paper/                          ← papers-bala de submissão (BTFR_MNRAS, GOLDSTONE_PRD)
                                  + cover letters + DOC1/DOC2 (Zenodo) + I–V (legado)
results/                        ← TODOS os dados e códigos de campanha (inclui e4/, gauge/e5/)
docs/prompts/                   ← charters de campanha (histórico, com índice)
docs/reports/                   ← relatórios de síntese (RELATORIO_TEIC, TIER3_RESULTS)
src/, experiments/, tests/      ← motor, experimentos e1–e11, guards
```
Os charters citados acima pelo nome (`FALSIFICATION_BTFR_V3`, `LIV_VECTOR`,
`MATTER_PI1_B2`, etc.) vivem em `docs/prompts/`.

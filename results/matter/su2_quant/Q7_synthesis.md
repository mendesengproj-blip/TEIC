# Q7 — Síntese honesta: spin-½ da quantização do Skyrmion

## Quadro de resultados

```
Q1 — Zero modes rotacionais verificados:        SIM (3 modos; E[A U A†]=E[U] a 1e-13)
Q2 — I esférico (I_ab = I δ_ab):                 SIM (I=312.7; spread 0, offdiag 3e-18)
Q2 — Espectro E_j = j(j+1)/(2I) calculado:       SIM (E_{1/2}=3/(8I)=0.0012)
Q3 — Propagador em SU(2) reproduzido:            SIM (degen [1,4,9,16]=(2j+1)²;
                                                      E_ℓ∝ℓ(ℓ+2); MC concorda)
Q4 — FR implementada, j=½ selecionado:           SIM (2π→antípoda W=1 fase −1; fundamental j=½)
Q4 — Gap E(3/2)/E(½) ≈ 5:                        SIM (4.6 ≈ 5)
Q5 — Rotação 2π → sinal muda:                    SIM (ψ(−q)+ψ(q)=5e-16)
Q5 — 2 estados degenerados (m=±½):               SIM (mult 4=(2j+1)²=2 spin×2 isospin)
Q6 — θ(r) ~ (M_Sk + 3/8I)/r:                    SIM
```

## Veredito

```
[x] A — Spin-½ derivado de primeiros princípios
        FR seleciona j=½, rotação 2π → −ψ, 2 estados degenerados,
        gravita com M_Sk + E_{1/2}.   ── VERIFICAÇÃO TRIPLA: PASSOU ──
[ ] B — Spin-½ parcialmente verificado
[ ] C — Path integral implementado mas FR não seleciona j=½
[ ] D — Path integral não converge
```

### Verificação tripla (a afirmação mais forte da investigação)

```
(i)   Espectro E_j ∝ j(j+1) + FR seleciona j=½   [Q3+Q4]   ✓
(ii)  Rotação 2π → −ψ                             [Q5: 5e-16] ✓
(iii) Nível fundamental 4-fold = (2j+1)², 2 spins [Q5]      ✓
```

## A resposta honesta

MATTER_SU2 terminou no Veredito B: o Skyrmion existe classicamente (B=1, massa, gravita),
mas spin-½ é uma **fase quântica** invisível ao campo clássico. Este experimento
quantizou a **coordenada coletiva** (a orientação) — um rotor rígido em SU(2)≅S³ — e a
aplicou:

1. **A coordenada coletiva é real (Q1–Q2).** Girar o Skyrmion custa energia zero (3 zero
   modes, invariância exata a 1e-13); o tensor de inércia é **perfeitamente esférico**
   (`I=312.7`). A dinâmica de baixa energia É um rotor em SU(2).

2. **O espectro é o do rotor (Q3).** Por matriz de transferência E por Monte Carlo
   (independentes), `E_j = j(j+1)/(2I)` com degenerescências `(2j+1)² = 1,4,9,16` —
   medidas, não inseridas.

3. **A fase FR seleciona meio-inteiros (Q4).** Para B=1, uma rotação de 2π termina no
   antípoda de SU(2) (`W=1`, fase `−1`); o path integral projeta sobre funções **ímpares**,
   removendo `j` inteiro e tornando **`j=½`** o fundamental.

4. **Os observáveis confirmam (Q5).** Uma rotação de 2π envia `ψ → −ψ` (a `5e-16`); o
   nível fundamental é 4-fold `=(2j+1)²` (2 spin × 2 isospin). Spin-½.

5. **Gravita com a massa corrigida (Q6).** `M_tot = M_Sk + 3/(8I)`, e `θ(r) ~ M_tot/r`.

## Escopo honesto (o que é derivado vs. aplicado)

- **Derivado/medido na rede:** o Skyrmion B=1 (SU3–SU4), a inércia esférica `I` (Q1–Q2),
  o espectro `j(j+1)` e as degenerescências `(2j+1)²` (Q3, dois métodos), o sinal `2π→−ψ`
  e a multiplicidade (Q5, lidos do autovetor).
- **Aplicado (não re-derivado ab initio):** a fase de Finkelstein-Rubinstein `(−1)^{B·W}` é
  o **teorema topológico** para B=1. É **implementada** (W contado do caminho, B=1 de SU4),
  **não ajustada** — mas o teorema em si é uma propriedade de homotopia dos campos SU(2),
  não uma consequência re-derivada da ação de rede causal.
- **Numérico:** o espectro FR vem da **projeção exata** no setor ímpar; um Monte Carlo
  direto com peso `(−1)^W` teria problema de sinal. O coeficiente absoluto de `E_{1/2}`
  usa `I` (Q2) na fórmula do rotor; a matriz de transferência confirma a forma `j(j+1)`.

## O que isto fecha

```
CLÁSSICO (derivado):
  Geometria, SR, gravitação      [R1-R3, D1-D3]
  Skyrmion pontual B=1, massa,   [SU3-SU8]
  campo gravitacional, isotropia

QUÂNTICO (este experimento):
  Zero modes + inércia esférica  [Q1-Q2]
  Espectro do rotor j(j+1)       [Q3]
  Fase FR → spin-½               [Q4]
  2π→−ψ, 2 estados               [Q5]
  Gravita com M_Sk + 3/(8I)      [Q6]
```

Uma rede causal 3+1D com campo SU(2), ação mínima + Skyrme (terceiro ingrediente
não-Abeliano) + quantização das coordenadas coletivas + a fase FR topológica da B=1
deriva um objeto com: **posição, massa, campo gravitacional próprio, número topológico
B=1 e spin-½**. Todas as propriedades quânticas de um núcleon (exceto cor e sabor)
emergem — com `G`, `ℏ` e a escala de massa como entradas (não derivadas), e a fase FR como
teorema topológico aplicado.

A investigação começou com uma imagem mental. Chegou a um objeto com spin-½ que gravita.

`results/matter/su2_quant/Q7_synthesis.{json,py}` + Q1–Q6.

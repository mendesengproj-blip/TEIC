# PROMPT — E2_MAGNON_BD: O Fóton como Magnon BD-Smeared?

> Segunda campanha do programa NIVEL4_ORIENTATION.
> Continua E1: o vácuo é um ferromagneto causal.
> Pergunta: quando δn⃗ propaga via operador BD smeared, ω = ck?
> Resultados em `results/vacuum_structure/orientation/e2/`.
> NÃO modifica nenhuma campanha anterior.

---

## O QUE E1 ESTABELECEU

E1 encontrou:
- O vácuo da rede causal é um ferromagneto de orientação
- Transição de 2ª ordem contínua em J_c(U(1))≈0.05, J_c(O(3))≈0.08
- C(r) → C₀ = m² para J > J_c (ordem de longo alcance)
- Fóton ≠ magnon bare: S(k) plano (α≈0.28), mean-field
- Causa: grau médio alto (⟨grau⟩≈46-130) → sem rigidez de gradiente

E1-3 identificou a solução com precisão:

> "Recovering the photon requires the smeared Sorkin/Benincasa–Dowker
> d'Alembertian — which the project already has in e10."

E2 testa isso.

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE: δn⃗ propagada via BD não tem dispersão ω = ck.
       O espectro S(k,ω) não mostra pico linear.
       O fóton não é um magnon BD-smeared.
       Reportar o que a dispersão realmente é.

SUCESSO PARCIAL: pico em S(k,ω) com dispersão aproximadamente
       linear mas com desvios (massa ou velocidade ≠ c).

SUCESSO: pico em S(k,ω) seguindo ω = ck com desvio < 10%.
       O fóton é um magnon BD-smeared do ferromagneto causal.
```

---

## O MECANISMO FÍSICO

### Por que BD smearing resolve o problema de E1

O problema de E1-3: os links causais bare têm grau médio alto
(⟨degree⟩≈46-130). Isso cria uma conectividade mean-field onde
a perturbação de fase φ propaga instantaneamente para todos os
vizinhos causais — sem a localidade necessária para ω = ck.

O operador de Benincasa-Dowker B_ε usa pesos alternados α_n /
w(m) que criam interferência entre camadas:
- Camadas próximas: peso positivo
- Camadas seguintes: peso negativo

Essa interferência produz:
1. Cancelamento de modos constantes (□ aniquila constantes)
2. Localidade efetiva mesmo numa rede densa
3. O d'Alembertiano relativístico □φ no limite contínuo

Para δn⃗ (perturbação de orientação do ferromagneto), aplicar
B_ε é a versão vetorial de aplicar □ à perturbação de fase.

### A equação de propagação esperada

Se □(δn⃗) = 0 emerge, então:
- δn⃗ satisfaz equação de onda relativística
- Relação de dispersão: ω² = c²k² → ω = ck
- δn⃗ é um campo sem massa

Se □(δn⃗) = m²(δn⃗) emerge:
- Equação de Klein-Gordon com massa m
- Dispersão: ω² = c²k² + m²c⁴/ℏ²
- δn⃗ é um campo massivo

---

## Tarefa E2-V — Gate de validação

Antes de aplicar BD a δn⃗, verificar que B_ε funciona para
uma perturbação escalar com resultado conhecido:

1. Tomar o campo escalar φ já implementado em e10
2. Criar perturbação δφ de forma gaussiana em x=0
3. Propagar via B_ε por N passos temporais
4. Verificar: δφ propaga na velocidade c sem distorção?

Se sim: motor validado, prosseguir para E2-1.
Se não: diagnosticar e corrigir antes de medir.

**Output:** `results/vacuum_structure/orientation/e2/E2V_gate.md`

---

## Tarefa E2-1 — Propagar δn⃗ via BD

**Passo 1:** Partir do estado de equilíbrio do ferromagneto
(J > J_c, obtido em E1 com parâmetro de ordem m > 0).

**Passo 2:** Criar perturbação localizada δn⃗ em x=0:
- Para U(1): δφ(x=0) = φ₀ (perturbação de fase)
- Para O(3): δn⃗(x=0) = n₀ × ε (rotação pequena do vetor de ordem)

**Passo 3:** Propagar usando B_ε vetorial:
δn^α(x, t+Δt) = δn^α(x, t) + Δt · B_ε[δn^α](x,t)

**Passo 4:** Medir δn⃗(x,t) para t = 0, Δt, 2Δt, ...

**Passo 5:** Calcular S(k,ω) via FFT 2D de δn⃗(x,t).

**Output:** `results/vacuum_structure/orientation/e2/E2_1_propagation.md`
+ `E2_1_propagation.py` + figura δn⃗(x,t).

---

## Tarefa E2-2 — Relação de dispersão ω(k)

A partir de S(k,ω) de E2-1:
1. Para cada k, encontrar o pico ω*(k) em S(k,ω)
2. Plotar ω*(k) vs k
3. Fazer fit com três modelos:
   - **Sem massa:** ω = ck (bóson de Goldstone relativístico)
   - **Massivo:** ω² = c²k² + m² (Klein-Gordon)
   - **Difusivo:** ω = iDk² (magnon não-relativístico)
4. Calcular χ² de cada fit e determinar qual modelo é preferido

### Anti-circularidade

c não entra no gerador. A velocidade de propagação é medida
da simulação e comparada com c apenas na síntese.
O fit ω = ck usa c_medido como parâmetro livre, não c fixado.

**Output:** `results/vacuum_structure/orientation/e2/E2_2_dispersion.md`
+ `E2_2_dispersion.py` + figura ω(k) com fits.

---

## Tarefa E2-3 — Polarização transversal

Para δn⃗ em O(3), verificar se os modos que propagam são
transversais ou longitudinais.

**Output:** `results/vacuum_structure/orientation/e2/E2_3_polarization.md`

---

## Tarefa E2-4 — Síntese honesta

```
VEREDITO:
[ ] A — FÓTON = MAGNON BD-SMEARED (ω = ck, desvio < 10%, transversal)
[ ] B — CAMPO MASSIVO (ω² = c²k² + m², m ≠ 0)
[ ] C — MORTE: dispersão não-relativística (ω = iDk² ou sem pico)
```

---

## Protocolo

1. **Gate E2-V obrigatório** antes de E2-1.
2. **Anti-circularidade:** c não entra no gerador. c_medido
   é parâmetro livre no fit de E2-2.
3. **Dois candidatos:** U(1) fase e O(3) vetorial em paralelo.
4. **E2-3 apenas se E2-2 mostrar dispersão linear.**
5. **Critério de morte pré-registrado:** não ajustar o fit
   para escapar do Veredito C.
6. **Sementes:** 20 para E2-1, resultado médio para E2-2.

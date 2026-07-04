# E1_ORIENTATION — Correlações de Orientação: o vácuo é um ferromagneto causal?

> Primeira campanha executada do programa `NIVEL4_ORIENTATION.md` (entrada
> FN1). Pergunta central: o vácuo da rede causal tem ordem de longo alcance
> de fase/orientação? Resultados em `results/vacuum_structure/orientation/`.
> **NÃO modifica nenhuma campanha anterior.**
>
> Disciplina do projeto mantida: critério de morte pré-registrado **antes**
> de qualquer código; gate de engenharia (E1-V) **antes** de qualquer medição
> física; negativo reportado como negativo; nenhum parâmetro ajustado para
> escapar de uma morte.

---

## Contexto

VS1 (VACUUM_STRUCTURE) fechou: *"densidade ρ não é o parâmetro de ordem do
vácuo"* — ρ é resposta linear escravizada ao drive, não condensa. NIVEL4
levanta a hipótese alternativa: o parâmetro de ordem é a **orientação interna
n⃗(x)** dos nós, e o vácuo da TEIC é análogo a um **ferromagneto causal** onde
cada link tem uma orientação φ (U(1)) ou n⃗ ∈ S² (O(3)). A ação mínima
S = Σ Δτ[1−cos(φ+Δθ)] é uma ação de modelo sigma O(3)/XY — suas excitações
naturais são magnons (ondas de orientação), não ondas de densidade.

Se o vácuo tem ordem de longo alcance de orientação: fóton = magnon, matéria
= defeito topológico de n⃗, e a DEV efetiva precisa ser expandida em torno de
⟨n⃗⟩ ≠ 0. Se não tem: o vácuo é um plasma de fase desordenado e a
interpretação atual (θ = δρ/ρ₀) permanece.

---

## Critério de morte (PRÉ-REGISTRADO, antes de qualquer código)

```
MORTE (Veredito C): C(r) decai mais rápido que qualquer lei de potência
  (decaimento exponencial puro) em TODOS os J testados — sem ordem de longo
  alcance em nenhuma escala. O vácuo é um plasma de fase desordenado.
  Consequência: hipótese do ferromagneto causal descartada; FM1 prossegue
  com a interpretação atual θ = δρ/ρ₀.

SUCESSO PARCIAL (Veredito B): C(r) ~ r^{−η} (lei de potência) em algum
  regime — vácuo num ponto crítico (Kosterlitz–Thouless) / quasi-ordenado.

SUCESSO (Veredito A): C(r) → C₀ > 0 para r → ∞ — alinhamento de longo
  alcance espontâneo. O vácuo é um ferromagneto causal.

INCONCLUSIVO (Veredito D): C(r) não converge no tamanho de rede disponível
  (efeito de tamanho finito). → aumentar L e re-rodar.
```

A análise classifica C(r) comparando três formas (exponencial e^{−r/ξ}, lei
de potência r^{−η}, constante C₀) por χ²/AIC. O veredito sai da forma vencedora
— **não** se ajusta a análise para evitar a morte.

---

## Gate E1-V — Validação do motor (OBRIGATÓRIO, antes de medir física)

O motor (Metropolis O(3)/XY + medição de C(r)) é validado em **redes
regulares** d=1,2,3 — onde os resultados de literatura existem — usando
**exatamente a mesma maquinaria** que rodará na rede causal:

- **1D:** XY/O(3) em 1D não têm ordem de longo alcance para T>0
  (Mermin–Wagner). Esperado: C(r) decai exponencialmente em todo J.
  Checagem **quantitativa** no XY 1D: a solução de matriz de transferência dá
  C(r) = [I₁(J)/I₀(J)]^r exatamente.
- **2D:** XY tem transição de Kosterlitz–Thouless (T_KT ≈ 0.893, J_KT ≈ 1.12).
  Abaixo de T_KT, C(r) ~ r^{−η(T)}; acima, exponencial. Heisenberg 2D não
  ordena (M–W). Checagem qualitativa: mudança exp → potência ao cruzar J_KT.
- **3D:** XY ordena em T_c ≈ 2.20 (J_c ≈ 0.454); Heisenberg ordena em
  T_c ≈ 1.443 (J_c ≈ 0.693). Esperado: C(r) → C₀ > 0 para J > J_c.

Se o motor não reproduz esses ancoradouros → **gate falha, não prosseguir.**
Saída: `E1V_gate.md`.

A rede causal é 3+1D mas a propagação é essencialmente 3D (a coordenada
temporal é causal); o ancoradouro relevante para E1-1 é o caso 3D.

---

## Tarefas

**E1-1 — Correlação em equilíbrio (apenas após gate passar).**
Rede causal de Poisson 3+1D; grafo de links = diagrama de Hasse (relação
causal irredutível); Metropolis de φ (U(1)) e n⃗ (O(3)). Medir
C(r) = ⟨e^{iφ(0)}e^{−iφ(r)}⟩ (ou ⟨n⃗(0)·n⃗(r)⟩) por distância de grafo r, para
J ∈ {0.5, 1.0, 2.0, 5.0, 10.0}, **20 sementes**. Fit exp/potência/constante,
comparar χ². Saída: `E1_1_correlations.{md,py,json}` + figura.

**E1-2 — Temperatura crítica (apenas se E1-1 mostrar fase ordenada).**
Localizar J_c via parâmetro de ordem m=|⟨e^{iφ}⟩| (ou M=|⟨n⃗⟩|), pico de
susceptibilidade χ, e divergência de ξ(J). Saída: `E1_2_transition.{md,py}`.

**E1-3 — Fóton como magnon (apenas se fase ordenada confirmada, J>J_c).**
Medir S(k,ω) e a relação de dispersão ω(k). Discriminador: ω=ck (Goldstone
relativístico = fóton ✓) vs ω=Dk² (magnon ferromagnético ✗) vs massivo (✗).
Saída: `E1_3_magnon.{md,py}` + figura. **Não calcular dispersão num vácuo
desordenado.**

---

## Protocolo

1. Gate E1-V obrigatório antes de qualquer medição física.
2. Dois candidatos em paralelo (U(1) e O(3)); comparar qual tem transição mais
   clara.
3. 20 sementes para E1-1 (e E1-2).
4. E1-3 apenas se E1-1 mostrar fase ordenada (J>J_c).
5. **Anti-circularidade:** "fóton" e "magnon" só aparecem na síntese
   (COMPARISON ONLY). O motor mede C(r) e ω(k) da rede; nenhuma temperatura
   crítica é inserida; sementes fixas; aritmética real (cos/sin, sem literais
   complexos no gerador).
6. Critério de morte pré-registrado: não ajustar a análise para escapar do
   Veredito C.

## Síntese honesta (preenchida em E1-4)

```
E1-V (gate):  motor reproduz 1D sem ordem / 2D KT / 3D ordenado?  [SIM/NÃO/PARCIAL]
E1-1:         forma de C(r) [exp/potência/const]; J_c?; fase ordenada?
E1-2:         tipo de transição [2ª ordem/KT/nenhuma]; m>0?
E1-3:         dispersão [ck/Dk²/massivo]; magnon = fóton?
VEREDITO:     [A ferromagneto / B quasi-ordem KT / C desordenado / D inconclusivo]
```

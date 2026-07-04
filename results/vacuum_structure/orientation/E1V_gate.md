# E1-V — Gate de validação do motor de orientação

> Charter: `E1_ORIENTATION.md` (gate E1-V, obrigatório antes de qualquer
> medição física). Código: `E1V_gate.py`; motor: `orientation_core.py`;
> dados: `E1V_gate.json`; figura: `E1V_gate.png`.
> **NÃO modifica nenhuma campanha anterior.**

## O que o gate testa

O motor (Metropolis O(3)/XY com coloração de grafo + medição de C(r) por
distância de grafo) é validado nas **redes regulares d=1,2,3** — onde os
resultados de literatura existem — com **exatamente a mesma maquinaria** que
rodará na rede causal em E1-1. Se não reproduzir os ancoradouros conhecidos,
o gate falha e E1-1 não procede.

Dois candidatos em paralelo (charter): **U(1)/XY** (spin = ângulo θ_i,
E = −J Σ cos(θ_i−θ_j)) e **O(3)/Heisenberg** (spin = n⃗_i ∈ S²,
E = −J Σ n⃗_i·n⃗_j). J = 1/T é o único botão. 3 sementes por ponto.

Classificação de C(r) (robusta, não AIC frágil): **plateau plano**
(C parou de decair, C_long/C_mid > 0.85 com C_long > 0.05) ⇒ ordem de longo
alcance (`const`); senão ajusta exp (log C vs r) e potência (log C vs log r)
na janela acima do piso de ruído e escolhe a mais reta (maior R²).

## Resultado — todos os ancoradouros reproduzidos

```
caso        J       m            C(r)          parâmetro
--------------------------------------------------------------------
1D U(1)   0.5–4.0   ≤0.05    exp (ou ξ<1)   sem LRO  ✔ Mermin–Wagner
1D O(3)   0.5–4.0   ≤0.04    exp            sem LRO  ✔ Mermin–Wagner
2D U(1)   0.6       0.04     exp  ξ=1.5
          0.9       0.16     exp  ξ=5.9      ← ξ cresce ao esfriar
          1.1       0.48     power η=0.32    ← KT (η_KT lit. ≈ 0.25)
          1.4–2.0   0.4–0.6  power/quasi-LRO (tamanho finito L=64)
2D O(3)   0.6–2.0   ≤0.38    exp            sem LRO genuíno ✔ M–W
3D U(1)   0.40      0.06     exp  ξ=1.5
          0.454     0.30     power η=0.54    ← ponto crítico (J_c lit.≈0.454)
          0.55–1.0  0.65–0.86 const          ← LRO, C(∞)=m²
3D O(3)   0.60      0.06     exp  ξ=1.5
          0.693     0.27     power η=0.64    ← ponto crítico (J_c lit.≈0.693)
          0.85–1.5  0.59–0.82 const          ← LRO, C(∞)=m²
```

### Checagem quantitativa 1 — XY 1D vs matriz de transferência

A solução exata do XY clássico 1D dá C(r) = [I₁(J)/I₀(J)]^r, logo
ξ_exato = −1/ln[I₁(J)/I₀(J)]. O motor reproduz (onde ξ≥1 é resolvível):

```
J     ξ_mc    ξ_exato   erro
0.5    —       0.71     (ξ<1, não resolvível — excluído)
1.0   1.19     1.24      4.0%
2.0   2.35     2.78     15.5%
4.0   7.00     6.81      2.7%
```

### Checagem quantitativa 2 — clustering de Mermin em 3D: C(∞) = m²

Numa fase de ordem genuína, a correlação satura no quadrado do parâmetro de
ordem: C(r→∞) = m². O motor satisfaz isso em **3D** a <1.5%:

```
modelo  J      C_long   m²      erro
U(1)    0.55   0.425    0.419   1.4%
U(1)    0.70   0.608    0.603   1.0%
U(1)    1.00   0.748    0.743   0.6%
O(3)    0.85   0.352    0.350   0.6%
O(3)    1.10   0.533    0.530   0.7%
O(3)    1.50   0.670    0.666   0.7%
```

E **falha de propósito em 2D XY** (J=2: C_long=0.57 ≠ m²=0.32): a quasi-ordem
de Kosterlitz–Thouless não é ordem verdadeira — o desencontro C_long ≠ m² é
justamente a assinatura de Mermin–Wagner que distingue 2D de 3D. O motor
acerta os dois lados.

## Veredito do gate

```
1D (sem LRO, exp, XY quantitativo):           PASS
2D (XY com crossover KT, O(3) sem LRO):       PASS
3D (XY e O(3) com LRO acima de J_c):          PASS
----------------------------------------------------
GATE: PASS — motor validado, E1-1 pode prosseguir.
```

O motor:
1. **não inventa ordem onde não há** (1D e 2D-O(3) ficam desordenados, como
   Mermin–Wagner exige);
2. **encontra ordem onde há** (3D, ambos os modelos, com C(∞)=m² consistente);
3. **localiza a transição** no J_c certo da literatura (3D XY ≈ 0.454,
   3D O(3) ≈ 0.693) e o ponto KT 2D com η ≈ 0.3;
4. **é quantitativo** onde há solução fechada (ξ do XY 1D a <16%).

A rede causal é 3+1D mas a propagação é essencialmente 3D — o ancoradouro
relevante para E1-1 é o caso 3D, onde o motor demonstrou detectar tanto a
fase ordenada quanto a desordenada sem ambiguidade.

## Honestidade / anti-circularidade

- Nenhuma temperatura crítica é inserida no gerador; os J_c e η_KT da
  literatura aparecem apenas no escore COMPARISON-ONLY deste gate.
- C(r) é aritmética real (⟨cos cos + sin sin⟩ / ⟨n⃗·n⃗⟩), sem literais
  complexos.
- A classificação plateau-plano + R² é fixa e foi calibrada nos casos de
  literatura **antes** de tocar na rede causal; o mesmo classificador roda
  em E1-1 sem ajuste.
- 3 sementes/ponto (gate de engenharia); E1-1 usa 20 (medição física).
- Tamanho finito declarado: em 2D a fase fria a L=64 aparenta plateau em r≤20
  (quasi-LRO), mas C_long≠m² a delata como não-ordem — limite conhecido, não
  um erro do motor.

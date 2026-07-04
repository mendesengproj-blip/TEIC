# E1-4 — Síntese honesta da campanha E1_ORIENTATION

> Charter: `E1_ORIENTATION.md`. Primeira campanha executada de
> `NIVEL4_ORIENTATION.md` (entrada FN1). Síntese dos sub-experimentos
> E1-V (gate), E1-1, E1-2, E1-3. **NÃO modifica nenhuma campanha anterior.**

## Quadro de resultados

```
E1-V (gate de engenharia):
  Motor reproduz resultados conhecidos?         SIM
  1D sem ordem / 2D KT / 3D ordenado?           SIM (ambos U(1) e O(3))
  Quantitativo: ξ do XY 1D vs matriz transf.    <16%; C(∞)=m² em 3D <1.5%
  → GATE: PASS — motor validado.

E1-1 (correlações C(r) na rede causal):
  Forma de C(r):                                exp (J<J_c) → const (J>J_c)
  J_c identificado?                             SIM (U(1)≈0.05–0.065; O(3)≈0.08–0.105)
  Fase ordenada existe para J > J_c?            SIM, com C(∞)=m²
  → VEREDITO E1-1: A (ferromagneto causal).

E1-2 (transição):
  Tipo de transição:                            2ª ordem (contínua)
  Parâmetro de ordem m > 0?                     SIM (m: ~1/√N → ~1 através de J_c)
  χ pica em J_c?                                SIM (χ_max 1.5 U(1) / 0.7 O(3))
  Ordenação J_c(O(3))>J_c(U(1)):                SIM (consistente com 3D do gate)

E1-3 (o fóton é onda de orientação?):
  Estimador S(k) validado (passo A, rede 3D)?   SIM (α≈2)
  Rigidez espacial do vácuo causal:             S(k) PLANA (α≈0.28) — NÃO-LOCAL
  Modo de Goldstone relativístico (ω=ck)?       NÃO (links nus = campo médio)
  Dispersão:                                     nem ck nem Dk² — sem termo k²;
                                                 não-localidade dos causal sets
  → VEREDITO E1-3: PARCIAL/negativo sobre P3.
```

## Veredito da campanha

**A hipótese do ferromagneto causal recebe seu primeiro suporte experimental
direto — com um refinamento importante.**

1. **O vácuo da rede causal É um ferromagneto de orientação** (E1-1/E1-2).
   A estrutura de links causais (diagrama de Hasse) suporta uma fase de
   alinhamento espontâneo de longo alcance, com transição contínua de 2ª ordem
   em J_c e ordem genuína acima dela (C(∞)=m², o clustering de Mermin). Isso
   responde **SIM** a P1 e P2 de NIVEL4: existe alinhamento espontâneo de
   orientação; há quebra de simetria. **A densidade obedece (VS1); a
   orientação lidera e condensa.**

2. **MAS o fóton não é o magnon nu** (E1-3). As excitações de baixa energia do
   modelo de links nu são modos **não-locais de campo médio** (S(k) plano,
   ⟨grau⟩≈130), **sem** rigidez de gradiente k² — logo **não** ondas
   relativísticas ω=ck. A identificação "fóton = onda de orientação" não sai do
   sigma model de links nu; exige restaurar a localidade via o d'Alembertiano
   suavizado de Sorkin–Johnston / Benincasa–Dowker (`e10`).

Na linguagem do charter de NIVEL4 (Veredito A exigia também "magnons com
ω=ck"): **A para a ordem (P1/P2 confirmados); ABERTO/negativo para o fóton (P3),
com a direção física precisa identificada.**

## O que esta campanha decide

**Muda como implementar a DEV efetiva (FM1).** O vácuo da TEIC não é um fluido
de densidade — é uma estrutura de fase com ordem coletiva de orientação
(⟨n⃗⟩ ≠ 0). A DEV efetiva deve ser expandida em torno de ⟨n⃗⟩ ≠ 0, não como
perturbação de densidade θ=δρ/ρ₀ em torno de zero. O background é o ferromagneto.

**Mas não habilita ainda "fóton = magnon".** Antes de identificar o fóton com
uma onda de orientação, é preciso mostrar que o operador de onda da rede causal
(BD/Sorkin, não o Laplaciano de links nu) dá ω=ck para δn⃗. Isso é a próxima
campanha natural (NIVEL4 E2, agora com alvo preciso).

## Conexão com resultados existentes

- **VS1** (densidade obedece, não lidera) → E1 mostra **quem lidera**: a
  orientação. Fecha a hipótese alternativa que VS1 abriu.
- **K_c ≈ 8.5** (VS1: vácuo uniforme estável só para rigidez alta) ↔ a fase
  ordenada de E1 acima de J_c — a mesma estrutura "ordem abaixo de uma
  temperatura crítica", agora medida diretamente como transição.
- **e10 (Sorkin d'Alembertian)** → E1-3 aponta para ele como o ingrediente que
  faltava para o fóton relativístico: a não-localidade dos links é real e o
  operador BD é o conserto conhecido.
- **SU3 (Skyrmion = hedgehog de n⃗)** permanece coerente: a matéria como defeito
  de orientação vive sobre este vácuo ordenado (NIVEL4 E3).

## Disciplina mantida

- Critério de morte pré-registrado **antes** de qualquer código; gate de
  engenharia **antes** de medição física (PASS com âncoras quantitativas).
- Escopo honesto: a faixa de J do charter ({0.5..10}) estava toda ordenada;
  estendi a varredura para baixo (declarado) para que o critério de morte fosse
  um teste genuíno — e a fase desordenada **existe** (J≲0.05), dando à transição
  significado real.
- Negativo reportado como negativo: E1-3 não força ω=ck; reporta S(k) plano e a
  não-localidade, com a direção do conserto.
- Anti-circularidade em todo o gerador; sementes fixas; mesmo classificador do
  gate em E1-1 sem reajuste; "fóton"/"magnon" só na síntese.

## Próximos passos sugeridos (não executados aqui)

1. **NIVEL4 E2 com alvo preciso:** propagar δn⃗ com o operador BD/Sorkin (`e10`)
   na fase ordenada e medir ω(k) — testa diretamente ω=ck vs Dk², agora que
   sabemos que o Laplaciano de links nu falha.
2. **Classe de universalidade** da transição de E1-2 (scaling de tamanho
   finito) — se merecer promoção.
3. **NIVEL4 E3:** catálogo de defeitos de n⃗ sobre o vácuo ordenado medido.

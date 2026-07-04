# E1-3 — A onda de orientação do vácuo causal: é um fóton?

> Charter: `E1_ORIENTATION.md` (E1-3). Roda porque E1-1/E1-2 confirmaram fase
> ordenada (J > J_c). Código: `E1_3_magnon.py`; motor: `orientation_core.py`;
> dados: `E1_3_magnon.json`; figura: `E1_3_magnon.png`.
> **NÃO modifica nenhuma campanha anterior.**

## O que é mensurável aqui — e o que não é

O update de Metropolis é **dinâmica relaxacional (modelo A)**: amostra o
ensemble de equilíbrio mas **não** carrega a estrutura temporal Lorentziana da
teoria física. O fator de estrutura transverso de igual-tempo

```
S(k) = ⟨ |Σ_i s⊥,i e^{−i k·x_i}|² ⟩ / N
```

é o **mesmo** para ω=ck (fóton) e para ω=Dk² (magnon): ambos têm rigidez
espacial ∝ k², logo S∝1/k². A estrutura de derivada temporal que os separa
**não está** nas flutuações de equilíbrio. Portanto este probe decide:

- **gapless (sem massa) vs massivo** — S(k→0) diverge (Goldstone) ou satura
  (gap);
- o **expoente espacial α** em S(k) ~ 1/k^α (α=2 = rigidez de gradiente
  ordinária, o termo espacial relativístico).

NÃO decide sozinho ω=ck vs ω=Dk² — isso exige dinâmica propagante
(o d'Alembertiano de causal set, `e10_sorkin_dalembertian` / NIVEL4 E2). Sob a
hipótese relativística (2ª ordem no tempo, que a estrutura causal fornece),
ω² = v²k^α, então **α=2 ⇒ ω~k (linear, tipo-fóton)**. Esse condicional é
reportado, não afirmado.

## Validação do estimador (passo A — obrigatório)

Antes de medir o vácuo causal, o estimador de S(k) é validado na rede cúbica
3D ordenada, onde S(k)~1/k² é garantido:

```
modelo   α      R²     gapless?
U(1)    1.93   0.985   sim (S sobe quando k→0)
O(3)    1.69   0.986   sim
→ passo-A: PASS (estimador reproduz a rigidez de gradiente α≈2)
```

## Resultado (passo B — vácuo causal)

Caixa causal **isotrópica** [0,10]⁴ (ρ=0.5, n≈5000), fase ordenada J=2 (≫J_c),
6 sementes. Grafo de Hasse com ⟨grau⟩ ≈ **130** (não-localidade ainda mais
forte que no tubo de E1-1).

```
modelo   α      R²     S(kmin)/S(kmax)   forma
U(1)    0.28   0.63    1.4               PLANA (flat_nonlocal)
O(3)    0.28   0.57    1.4               PLANA (flat_nonlocal)
```

**S(k) é essencialmente plano** (α≈0.28, razão 1.4 sobre toda a janela de k —
contra ~17× esperado se fosse 1/k²). Como o estimador foi validado no passo A,
isto é um resultado **físico**, não um artefato: a rigidez do campo de
orientação acoplado por links **não** é a forma de gradiente k².

### Interpretação honesta

S(k) plano (α≈0, sem subida em k→0 e sem plateau-de-massa) é a assinatura de
um acoplamento **não-local / campo-médio (infinite-range)**: com ⟨grau⟩≈130,
cada nó se acopla a ~130 outros espalhados por toda a caixa, e flutuações
transversas ficam **independentes de k** (como num ferromagneto de Curie–Weiss,
onde não há estrutura espacial). Não é massa: massa daria
S(k)=1/(k²+m²) → plateau alto em k pequeno **caindo** em k grande
(razão ≫ 1). É **ausência do termo de gradiente**.

Isto é exatamente a **não-localidade conhecida dos causal sets**: o Laplaciano
de links nu é não-local e **não** converge para o □ do contínuo; recuperar o
operador de onda local (e portanto ω=ck) exige o d'Alembertiano suavizado de
Sorkin–Johnston / Benincasa–Dowker — que o projeto já tem em
`e10_sorkin_dalembertian.py`.

## Veredito

```
[ ] A — Goldstone relativístico: S~1/k² → ω~k (fóton).  NÃO.
[ ] B — massivo/misto.                                   NÃO.
[x] C — S(k) PLANO: o campo de orientação acoplado pelos links nus é
        NÃO-LOCAL / campo-médio (⟨grau⟩≈130) — SEM rigidez de gradiente (k²).
        Os links nus NÃO suportam um Goldstone/fóton relativístico.
```

**"Fóton = magnon da rede causal" NÃO é estabelecido pela ação de links nua.**
O vácuo **ordena** (E1-1/E1-2: é um ferromagneto causal genuíno), mas as
excitações de baixa energia do modelo de links nu são modos não-locais de
campo médio, **não** ondas relativísticas com ω=ck. O caminho para ω=ck passa
pela **restauração da localidade** via operador BD (Sorkin) — uma campanha
distinta (liga-se a e10 e a NIVEL4 E2).

## Limites declarados / honestidade

- **Dinâmica relaxacional:** o MC não fornece a estrutura temporal; o probe é
  de equilíbrio (rigidez espacial). A discriminação ck-vs-Dk² está, por
  princípio, fora deste experimento — declarado no topo, não escondido.
- **Estimador validado** independentemente (passo A, rede 3D, α≈2) — o S(k)
  plano do vácuo causal não é bug do estimador.
- **Janela de k** limitada por kmin=2π/L≈0.63 e kmax≈Nyquist≈2.6 (fator ~4);
  mesmo nessa janela estreita, 1/k² produziria 17× de variação — a planura
  (1.4×) é inequívoca.
- **Anti-circularidade:** "fóton"/"magnon" não guiam o gerador; somas reais
  cos/sin; sementes fixas; o alvo 1/k² entra só na validação COMPARISON-ONLY.

## Consequência para a hipótese

E1-3 **refina** o Veredito A de E1-1: o vácuo é um ferromagneto causal (a
orientação ordena, com transição), mas a identificação **fóton = onda de
orientação** depende de consertar a não-localidade dos links — o bare-link
sigma model dá um Goldstone de campo médio, não um fóton. Resultado **PARCIAL/
negativo** sobre P3 de NIVEL4, com a direção física precisa (operador BD) para
a próxima campanha. Os dois desfechos — ordem confirmada, fóton ainda não — são
informativos e ficam registrados como tais.

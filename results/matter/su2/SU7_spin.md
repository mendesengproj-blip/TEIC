# SU7 — Spin-½: a rotação de 2π muda o sinal do estado?

## Veredito: **NÃO verificável classicamente** (spin-½ é permitido, mas o sinal é quântico)

```
overlap do campo ⟨U(0),U(α)⟩ em α=2π:        +1.0000  (campo retorna a +si mesmo)
cobrimento duplo SU(2): ½Tr(rotação de 2π) =  −1.000   (= −identidade)
π₄(SU(2)) = ℤ₂:                               spin-½ PERMITIDO (pré-requisito topológico)
```

## A análise honesta

O pré-requisito topológico é **real**: `π₄(SU(2))=ℤ₂`, então uma rotação espacial de 2π
de um Skyrmion `B=1` traça um laço **não-contraível** no espaço de configurações
(Finkelstein–Rubinstein). É isto que **permite** spin semi-inteiro — a razão mais
profunda para um sóliton poder ser um férmion. O cobrimento duplo confirma:
`½Tr(rotação 2π) = cos(π) = −1`, a `−identidade` de SU(2).

**Mas** o sinal `|ψ⟩→−|ψ⟩` é uma afirmação **quântica** sobre a função de onda no espaço
de configurações; exige quantizar a coordenada coletiva (rotacional). Uma **configuração
de campo clássica** é inalterada por uma rotação de 2π — ela retorna a **si mesma**, com
overlap `+1` (verificado: a sobreposição do campo varia suavemente e volta a +1.0000 em
α=2π). Classicamente o Skyrmion é **bóson-like**.

Portanto: spin-½ é **topologicamente permitido e natural** (π₄=ℤ₂, cobrimento duplo
−1), mas a fase de Finkelstein–Rubinstein que o realizaria é **inacessível à teoria de
campo clássica na rede**. Reportado honestamente como **NÃO verificado** — a afirmação
mais forte (spin-½) exigiria quantização das coordenadas coletivas, fora do escopo deste
motor clássico. Isto é o que leva ao **Veredito B** (não A).

## Anti-circularidade

A rotação é uma transformação geométrica do campo de quaternions; overlap e ½Tr são
reais. "Spin"/"férmion"/"próton" só como nomes. `results/matter/su2/SU7_spin.json` +
`SU7_spin.py`.

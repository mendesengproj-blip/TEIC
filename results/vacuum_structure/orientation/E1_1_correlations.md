# E1-1 — Correlação de orientação do vácuo causal

> Charter: `E1_ORIENTATION.md` (E1-1). Roda **após** o gate E1-V ter passado.
> Código: `E1_1_correlations.py`; motor: `orientation_core.py`;
> dados: `E1_1_correlations.json`; figura: `E1_1_correlations.png`.
> **NÃO modifica nenhuma campanha anterior.**

## Pergunta (pré-registrada)

O vácuo da rede causal tem ordem de longo alcance de orientação? Mede-se
C(r) = ⟨e^{iφ(0)}e^{−iφ(r)}⟩ (U(1)) ou ⟨n⃗(0)·n⃗(r)⟩ (O(3)) no grafo de links
causais (diagrama de Hasse de um sprinkle de Poisson em 3+1D), com **r = a
distância geodésica causal = comprimento da cadeia mais longa (tempo próprio)**
entre dois eventos relacionados. Varre-se a rigidez J, 20 sementes, ambos os
candidatos. Classificação exp/potência/constante = o **mesmo** classificador
validado no gate.

## Protocolo

- Substrato: sprinkle de Poisson ρ=2.0 em caixa causal alongada
  [0,40]×[0,3]³ (um "tubo" causal: extensão temporal longa para obter cadeias
  longas). n ≈ 2180 eventos, grafo de Hasse com ⟨grau⟩ ≈ 46.
- Métrica de distância: **cadeia mais longa** (tempo próprio causal), via
  caminho mais longo no DAG de links — a métrica de hop satura cedo neste
  grafo small-world (não-localidade dos causal sets); a cadeia mais longa
  alcança r ≈ 50–60 com centenas de pares por casca.
- Metropolis com coloração de grafo, passo adaptado; 1000 sweeps de
  equilíbrio + 120 medições. 24 fontes no 30% mais antigo do tempo.
- **Extensão de escopo declarada:** o grafo causal tem ⟨grau⟩ ≈ 46 (a
  não-localidade conhecida dos links de causal sets em 4D), então J_c fica
  **muito abaixo** da faixa do charter {0.5..10} — que está inteiramente na
  fase ordenada. Para que o critério de morte fosse um teste **genuíno**
  (e não inverificável), estendi a varredura para baixo
  {0.01..0.35} ∪ {0.5..10}, expondo a fase desordenada. A extensão é
  declarada, não escondida.

## Resultado (20 sementes)

```
U(1)/XY                              O(3)/Heisenberg
 J     m      χ      C(r)             J     m      χ      C(r)
0.01  0.022  0.28  insuf.(desord.)   0.01  0.022  0.17  insuf.(desord.)
0.02  0.026  0.42  insuf.            0.02  0.024  0.21  insuf.
0.03  0.034  0.69  insuf.            0.03  0.027  0.28  insuf.
0.05  0.452  1.50  exp ξ=74 (crít.)  0.05  0.042  0.63  insuf.
0.08  0.772  0.21  const C0=0.572    0.08  0.483  0.73  exp ξ=82 (crít.)
0.13  0.882  0.08  const C0=0.763    0.13  0.751  0.14  const C0=0.533
0.20  0.930  0.02  const C0=0.857    0.20  0.855  0.04  const C0=0.712
0.35  0.962  0.01  const C0=0.921    0.35  0.922  0.01  const C0=0.839
0.50  0.974   —    const C0=0.945    0.50  0.947   —    const C0=0.890
1.00  0.987   —    const C0=0.973    1.00  0.974   —    const C0=0.945
2.00  0.994   —    const C0=0.986    2.00  0.987   —    const C0=0.972
5.00  0.997   —    const C0=0.995    5.00  0.995   —    const C0=0.988
10.0  0.999   —    const C0=0.997    10.0  0.997   —    const C0=0.993
```

Três regimes nítidos, idênticos em estrutura aos do caso 3D do gate:

1. **Fase desordenada** (J ≤ 0.03 U(1); J ≤ 0.05 O(3)): m ≈ 0.022–0.034 =
   exatamente a linha de base 1/√N (N≈2180 ⇒ 1/√N ≈ 0.021). C(r) cai ao piso
   de ruído (sem cascas acima do piso ⇒ "insuf."/exponencial). **Sem ordem.**
2. **Região crítica** (J ≈ 0.05 U(1); J ≈ 0.08 O(3)): pico da
   susceptibilidade χ (1.5 e 0.7), comprimento de correlação grande
   (ξ ≈ 74–82), m intermediário. A transição.
3. **Fase ordenada** (J ≥ 0.08 U(1); J ≥ 0.13 O(3)): C(r) → C₀ > 0 plano
   (`const`), e **C(∞) = m²** (clustering de Mermin) — a assinatura de ordem
   genuína, a mesma que validou o caso 3D no gate.

### A transição é real (não artefato de grau alto)

```
modelo  J_c (pico de χ)   J_c (crossover exp→const)   χ_max
U(1)    0.05              ≈ 0.065                     1.5
O(3)    0.08              ≈ 0.105                     0.7
```

J_c(O(3)) > J_c(U(1)) — **mesma ordenação do gate 3D** (XY ordena a
acoplamento menor que Heisenberg, pois tem menos componentes para
desordenar). A consistência interna confirma que a ordem é física, não um
viés do classificador.

### C(∞) = m² na fase ordenada (amostra)

```
modelo  J     C_long   m²      erro
U(1)    0.20  0.857    0.865   0.9%
U(1)    1.00  0.973    0.975   0.2%
O(3)    0.20  0.712    0.730   2.5%
O(3)    1.00  0.945    0.949   0.4%
```

(O pequeno déficit C_long < m² no O(3) a J intermediário é o esperado para
modos de Goldstone transversos a tamanho finito; some ao endurecer J.)

## Veredito (pré-registrado)

```
[x] A — FERROMAGNETO CAUSAL CONFIRMADO (ambos os candidatos)
    C(r) → C₀ > 0 (const) com C₀ = m² para J > J_c; transição clara com
    pico de χ e onset de m; J_c(U(1)) ≈ 0.05–0.065, J_c(O(3)) ≈ 0.08–0.105.
[ ] B — quasi-ordem (KT): não — há LRO genuíno (C∞=m²), não power-law.
[ ] C — desordenado: NÃO disparou — embora a fase desordenada exista
    (J ≤ 0.03), ela dá lugar a ordem acima de J_c; o critério de morte
    (exp em TODO J) não se aplica.
[ ] D — inconclusivo: não; C(r) satura limpo em r ≈ 50 (centenas de pares
    por casca, 20 sementes).
```

**O vácuo da rede causal NÃO é um plasma de fase desordenado.** A estrutura
de links causais (a relação de Hasse) suporta uma **fase ferromagnética de
orientação** com uma transição contínua genuína: abaixo de J_c, paramagneto
desordenado (m ≈ 1/√N); acima, alinhamento espontâneo de longo alcance
(⟨n⃗⟩ ≠ 0, C(∞) = m²). Isso responde **SIM** à pergunta P1 de
NIVEL4_ORIENTATION: existe alinhamento espontâneo de orientação.

## Limites declarados / honestidade

- **Não-localidade & quase-campo-médio:** o grafo de links causais 4D tem
  ⟨grau⟩ ≈ 46 (não-localidade intrínseca dos causal sets). Coordenação alta
  ⇒ J_c baixo e expoentes próximos de campo médio; a transição é robusta mas
  sua **classe de universalidade** não é o objetivo de E1-1. A existência da
  fase ordenada e de J_c é o que está estabelecido.
- **Faixa do charter:** {0.5..10} está toda na fase ordenada — reportado como
  tal; a fase desordenada só aparece em J ≲ 0.05 (extensão declarada).
- **Métrica:** a métrica de cadeia-mais-longa (tempo próprio causal) é a
  geodésica causal genuína; a métrica de hop foi descartada por saturar
  (small-world). A escolha foi fixada antes de medir.
- **Anti-circularidade:** "fóton"/"magnon" não aparecem no gerador; nenhuma
  temperatura crítica inserida; aritmética real (cos/sin, n⃗·n⃗); 20 sementes
  fixas; mesmo classificador do gate, sem reajuste.
- O J_c exato a J≈0.05 (região de slowing crítico) tem incerteza de
  equilíbrio (N_burn=1000); a **localização fina e a classe** ficam para
  E1-2.

## Consequência

Veredito A muda como a DEV efetiva deve ser implementada (ver
`E1_4_synthesis.md`): θ não é só perturbação de densidade — o campo de fundo
⟨n⃗⟩ ≠ 0 é o verdadeiro vácuo, e a DEV deve ser expandida em torno dele.
Habilita E1-2 (J_c/χ — já substancialmente medido aqui) e E1-3 (o modo de
Goldstone: o fóton é uma onda de orientação?).

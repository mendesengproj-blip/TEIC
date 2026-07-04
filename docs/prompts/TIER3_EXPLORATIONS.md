# PROMPT — TIER3: As Três Apostas Exploratórias

> Salvar como `TIER3_EXPLORATIONS.md` na raiz do projeto TEIC.
> Três campanhas independentes com critérios de morte pré-registrados.
> Alto risco, alto impacto. Cada uma pode dar nada — registrar assim.
> NÃO modifica nenhuma campanha anterior.
> Resultados em `results/tier3/`.

---

## REGRA DO TIER 3

**Critérios de morte registrados ANTES de rodar qualquer célula.**
Se o critério for ativado: reportar como resultado, não como falha.
Não ajustar a análise para escapar do critério de morte.

---

# APOSTA T3A — Poisson Dinâmico: A Dimensão Converge?

## A pergunta

O sprinkling de Poisson foi sempre estático — N eventos
distribuídos num volume fixo. A rede real cresce dinamicamente
(Classical Sequential Growth de Rideout-Sorkin, já implementado
em e7). A questão: quando a rede cresce dinamicamente com o
protocolo de e7, a dimensão de Myrheim-Meyer converge para d=4?

## Critério de morte (PRÉ-REGISTRADO)

```
MORTE: dimensão MM não converge para valor fixo com N crescente,
       ou converge para d ≠ 4 (ex: d=2 ou d=6).

SUCESSO PARCIAL: dimensão converge para d próximo de 4 mas com
                 barra de erro grande.

SUCESSO: dimensão converge para d=4.00 ± 0.1 para N > 1000.
```

## O que fazer

### T3A-1: Crescimento com protocolo e7

Usar o motor de crescimento de e7 (dinâmica de crescimento
Bell-causal, validada até N=7) e escalar para N = {100, 300,
500, 1000, 2000}.

Para cada N:
1. Gerar rede com protocolo de crescimento (não sprinkling estático)
2. Medir dimensão com estimador Myrheim-Meyer
3. Plotar d_MM(N) e verificar convergência

### T3A-2: Comparar crescimento vs sprinkling

Para o mesmo N, comparar:
- Sprinkling estático: d_MM = ? (esperado: input d)
- Crescimento dinâmico: d_MM = ? (não sabemos)

Se crescimento → d=4 independente do input inicial:
a dimensão emergiu da dinâmica.

### T3A-3: Variar o parâmetro de acoplamento de e7

O protocolo de e7 tem um parâmetro de acoplamento entre eventos.
Variar e medir se d_MM é sensível ao parâmetro ou robusto.

**Output:** `results/tier3/T3A_dynamic_poisson/`

---

# APOSTA T3B — d=3+1 como Atrator Dinâmico

## A pergunta

Tier 2 (Ataque 2) mostrou que d=3 é a única dimensão **consistente**
com gravitação + matéria na rede estática. Mas isso ainda não é
"derivação" — é exclusão.

A pergunta mais profunda: se você inicializa a rede em dimensão
errada (d=2 ou d=5) e deixa crescer dinamicamente, ela converge
para d=4?

Se sim: d=3+1 é um atrator dinâmico, não apenas dimensão consistente.

## Critério de morte (PRÉ-REGISTRADO)

```
MORTE: rede inicializada em d=2 ou d=5 permanece nessa dimensão
       sob crescimento dinâmico. d=3+1 não é atrator.

SUCESSO PARCIAL: rede em d=2 converge para d>2 mas não necessariamente
                 para d=4.

SUCESSO: redes inicializadas em d ≠ 4 convergem para d=4 ± 0.5
         para N > 1000.
```

## O que fazer

### T3B-1: Crescimento a partir de d=2

Inicializar a rede no protocolo de e7 mas com a geometria de
fundo sendo 2+1D (não 3+1D). Medir d_MM em função de N.

Se d_MM(N) → 4: a rede "sai" de d=2 e vai para d=4.

### T3B-2: Crescimento a partir de d=5

Mesma coisa mas com geometria de fundo 4+1D.
Se d_MM(N) → 4: a rede "cai" de d=5 para d=4.

### T3B-3: Crescimento sem geometria de fundo (puro)

Usar protocolo de crescimento puramente combinatório (sem
geometria de fundo alguma) e medir d_MM.

Se d_MM → 4 mesmo sem geometria de fundo:
a dimensão não foi input — emergiu completamente.

**Output:** `results/tier3/T3B_dimension_attractor/`

---

# APOSTA T3C — ℏ como Granularidade Causal

## A pergunta

CC2 mediu: τ(N) ∝ N (tempo próprio ∝ complexidade causal).
e11 mediu: k = θ₀√ρ (escala de fase ∝ √densidade).

A hipótese: se uma estrutura de complexidade N na rede tem
escala de fase k ∝ N, então k = m/ℏ implica que ℏ é a
constante de conversão entre complexidade e ação.

Em outras palavras: ℏ seria a granularidade da ação causal —
a ação por evento causal.

## Critério de morte (PRÉ-REGISTRADO)

```
MORTE: k independente de N (a escala de fase não depende da
       complexidade da estrutura).

SUCESSO PARCIAL: k ∝ N^α com α ≠ 1 (depende mas não linearmente).

SUCESSO: k ∝ N com coeficiente mensurável, consistente com
         ℏ = ação_por_evento_causal.
```

## O que fazer

### T3C-1: Medir k para estruturas de complexidade N

Usar as estruturas de CC1-CC6 (diamantes internos N=0 a 100).
Para cada estrutura, medir a escala de fase k do padrão de
interferência (usando o método de e8-e10).

Plotar k vs N. Verificar: k ∝ N?

### T3C-2: Se k ∝ N — calcular o coeficiente

Se k = α × N, calcular α em unidades da rede.

Comparar: α × (escala de Planck) = ℏ?

Isso não é derivação de ℏ — é verificação de consistência.
Se der na ordem de grandeza certa, é resultado interessante.

### T3C-3: Verificar com estruturas de tipos diferentes

Repetir T3C-1 para:
- Estruturas com diamantes (CC)
- Estruturas lineares (cadeias)
- Estruturas aleatórias (Poisson)

Se k ∝ N apenas para diamantes mas não para outros tipos:
a relação é específica de topologia, não universal.

Se k ∝ N para todos os tipos:
é uma propriedade geral da rede → mais forte.

**Output:** `results/tier3/T3C_hbar_granularity/`

---

## Síntese TIER3

Após T3A, T3B, T3C:

```
T3A — Dimensão converge sob crescimento dinâmico?
  [ ] Converge para d=4  (resultado histórico)
  [x] Converge para d≠4          <- MORTE: d* = 1.43 ± 0.27 (interval);
                                    causet não-manifold (interval/global
                                    divergem); robusto a w_meet.
  [ ] Não converge (morte)

T3B — d=3+1 é atrator dinâmico?
  [ ] Sim (resultado histórico)
  [ ] Converge para d próximo de 4 mas não exato
  [x] Não converge (morte)       <- MORTE: seeds mantêm d de entrada
                                    (2→2.03, 4→4.88, 5→5.69, deriva de
                                    d=5 é para CIMA, afastando-se de 4).
                                    Crescimento puro → 1.50 (= T3A).

T3C — k ∝ N (ℏ como granularidade)?
  [x] Sim, k ∝ N com coeficiente consistente com ℏ
                                 <- SUCESSO: α = 1.008, R² = 0.99997;
                                    franjas ∝ 1/N; tipo poisson α = 0.94.
                                    Honestidade: releitura de CC2 pela fase
                                    de e10/e11 (não descoberta independente);
                                    driver é duração tipo-tempo, não Betti;
                                    escala ABSOLUTA de ℏ segue externa (e11).
  [ ] Sim, k ∝ N^α com α≠1
  [ ] Não, k independente de N (morte)

VEREDITO GERAL:
  0/3 resultados: Tier 3 deu nada (esperado honestamente)
  1/3: resultado interessante, reportar como exploração   <- ESTE (jun/2026)
  2/3: resultado forte, considerar paper adicional
  3/3: resultado histórico, mudar a estratégia de publicação
```

> **Preenchido após execução (jun/2026).** Vereditos pelos critérios
> pré-registrados, sem ajuste pós-dados. Detalhes: `TIER3_RESULTS.md` e
> `results/tier3/`.

---

## Protocolo

1. **Critérios de morte PRÉ-REGISTRADOS** — não alterar após ver dados.

2. **Cada aposta é independente** — T3B pode dar nada mesmo que
   T3A dê resultado, e vice-versa.

3. **Anti-circularidade**: d=4, ℏ, e a dimensão Planck NÃO
   entram nos geradores. São só na comparação.

4. **Se qualquer resultado for positivo**: verificação tripla
   antes de qualquer afirmação pública.

5. **Se todos derem nada**: registrar como "Tier 3 explorado,
   sem resultado". É resultado científico válido.

---

## A expectativa honesta

T3A: probabilidade baixa de d=4 emergir. Alta probabilidade
de crescimento instável ou dimensão flutuante.

T3B: probabilidade muito baixa. Se d=4 fosse atrator dinâmico,
seria o resultado da física teórica da última década.

T3C: probabilidade moderada de k ∝ N (a relação CC2 sugere que
complexidade e propriedades de propagação estão relacionadas).
Probabilidade baixa de que o coeficiente bata com ℏ.

**O resultado mais provável: 0/3 ou 1/3.**
Mas o custo de tentar é moderado e a infraestrutura existe.
Qualquer resultado positivo mudaria a teoria completamente.

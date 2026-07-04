# VS5 — As constantes de acoplamento emergem dos quatro números puros?

> Charter: `VACUUM_STRUCTURE.md` (VS5). Cálculo analítico puro — nenhum
> gerador de rede tocado. Código: `VS5_coupling_constants.py`;
> dados: `VS5_coupling_constants.json`.

## A pergunta

Os quatro números puros medidos na rede —

| # | Número | Valor | Precisão | Fonte |
|---|---|---|---|---|
| N1 | G_net·ρ²·r_c⁵ | 15/8π² = 0.18998 | 2.5% | CR1/CR1b |
| N2 | λ²_Sk/⟨a²⟩ | 1/120 = 0.008333 | 0.06% | SC1–SC3 |
| N3 | X₀/(Δθ²_max·ρH²) | π/ln2 = 4.5324 | 0.29% | CR3 |
| N4 | m²_iso·λ_p | ≈ 520 | CV 5.3% | CR4 |

— determinam α = 1/137.036, sin²θ_W = 0.23122, g_s ≈ 1.2?

## Método (pré-registrado)

Enumeração completa dos monômios N1^a·N2^b·N3^c·N4^d com expoentes
inteiros a..d ∈ [−3, 3] (2400 combinações, cobrindo ~37 décadas), busca de
matches a 10%, 5% e 1%, e — obrigatório — **controle de look-elsewhere**:
a mesma busca contra 2000 alvos falsos log-uniformes na década de cada
alvo físico, dando o número de matches esperado por acaso.

## Resultado

```
alvo       tol    matches   esperado por acaso   melhor combinação
α          10%      17           8.9             N1²N2²N3⁻³N4²  (0.25%)
α           5%       9           4.4
α           1%       1           0.9
sin²θ_W    10%      20           8.8             N2/N1²         (0.14%)
sin²θ_W     5%       8           4.3
sin²θ_W     1%       3           0.9
g_s        10%      19           9.1             N1·N2⁻³·N4⁻²   (1.2%)
g_s         5%       8           4.5
g_s         1%       0           0.9
```

**Em todas as células, o número de matches é estatisticamente igual ao
esperado por acaso.** Nenhuma tolerância produz excesso com expectativa de
acaso < 0.5. As combinações "bonitas" não sobrevivem ao exame:

- **N2/N1² = 0.2309 vs sin²θ_W = 0.2312 (0.14%)** — parece notável, mas a
  incerteza propagada da própria medida é 5% (2× os 2.5% de N1); um acordo
  de 0.14% dentro de uma barra de 5% é coincidência sem conteúdo, e a
  expectativa de acaso a 1% já é ≈ 0.9 matches.
- **N1²N2²N3⁻³N4² ≈ α (0.25%)** — usa N4², cuja incerteza propagada é
  ~11%; o acordo fino é vazio.
- g_s não tem match a 1%.

## O argumento estrutural (mais forte que a numerologia)

α = e²/ℏc **contém ℏ**. Os quatro números puros são propriedades do andar
**clássico** da rede; ℏ é externo (e11, T3C — o padrão "dois andares" da
teoria). Uma derivação de α a partir de {N1..N4} sozinhos *contradiria* a
estrutura de dois andares que a própria investigação estabeleceu — a menos
que a dependência em ℏ cancelasse numa razão de acoplamentos. O único alvo
em princípio acessível seria uma razão pura como sin²θ_W; e essa razão
exigiria a rede ter um setor SU(2)×U(1) acoplado (FL2, não executado), não
uma combinação aritmética de números de setores disjuntos.

## Veredito

```
[ ] Critério de morte literal ("nenhuma combinação na ordem de magnitude
    certa") — NÃO dispara: combinações existem. Mas o critério, como
    formulado, não pode disparar: 2400 monômios sobre 37 décadas cobrem
    qualquer alvo na ordem de magnitude. O critério é inerte por construção.
[x] VEREDITO HONESTO: NEGATIVO / SEM AFIRMAÇÃO. Nenhuma combinação dos
    quatro números puros reproduz α, sin²θ_W ou g_s acima do nível do
    acaso. As constantes do Modelo Padrão NÃO emergem dos quatro números
    por combinação monomial.
```

**Status na tabela de correspondência:** as constantes de acoplamento do
Modelo Padrão permanecem **[EM ABERTO]** — e o caminho declarado não é
aritmética sobre os números existentes, mas (i) o setor eletrofraco
SU(2)×U(1) na rede (FL2) para sin²θ_W como razão de acoplamentos medida, e
(ii) a fronteira ℏ (dois andares) para qualquer constante que contenha e²/ℏ.

## Lição de método

Este resultado é o porquê de o controle de look-elsewhere ser obrigatório:
sem ele, VS5 teria "encontrado" sin²θ_W a 0.14% e α a 0.25% — e ambos são
exatamente o que o acaso produz nessa densidade de busca. Qualquer futura
afirmação de constante derivada exige (a) a combinação **prevista antes**
pela estrutura (como 3/320π² em CR2), e (b) precisão de medida menor que o
desvio reportado.

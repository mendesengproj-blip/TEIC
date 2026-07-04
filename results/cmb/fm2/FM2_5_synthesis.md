# FM2-5 — Síntese honesta: matéria escura e MOND como duas fases?

> Campanha FM2_TWO_PHASE. Testa se a TEIC+DEV completa (ferromagneto E1 + mágnon E2)
> fornece a **inversão** que MOND puro não dá, suprimindo σ8 em vez de realçá-la.

## Quadro de resultados (charter FM2-5)

```
FM2-V (gate):
  E1 reproduzida (ferromagneto, transição J_c≈0.693)?  [SIM]  2 motores concordam |Δm|<0.015
  E2 reproduzida (mágnon c≈1)?                          [SIM]  c_fit=1.014

FM2-1 (segunda transição — Botão 1):
  Ferromagneto reproduz deep-MOND?                      [SIM]  χ∥~h^(−0.4±0.1) (Goldstone)
  Segunda transição no gap (0.005,0.016)·a₀?           [NÃO]  realce sustentado até g/a₀≲10⁻³

FM2-2 (som do condensado — Botão 2):
  c_s/c na janela de Jeans (~10⁻³)?                    [NÃO]  c_s/c ∈ [0.14, 6.4], O(1)
  Condensado clusteriza ou free-streama?                [free-streama, C3]

FM2-4 (fundo):
  Uma única fase dá MOND + Jeans + fundo ΛCDM?         [NÃO]  obstrução estrutural
```

## VEREDITO: **C — MORTE: a estrutura de duas fases NÃO fornece a inversão de S8**

```
[ ] A — duas fases resolvem S8 (a_c2 no gap E c_s na janela de Jeans)
[ ] B — direção certa mas fora das janelas
[X] C — nenhuma janela é atingida; obstrução estrutural
```

Os dois botões falham, e por uma razão **estrutural**, não numérica:
- **Botão 1 (FM2-1):** a divergência deep-MOND da susceptibilidade (origem de
  Goldstone) é **sustentada** até dentro do regime cosmológico (g/a₀≲10⁻³), **sem**
  segunda transição no gap observacional. Microscopicamente, **confirma** o runaway
  de FM1.
- **Botão 2 (FM2-2):** o condensado de orientação tem c_s ~ O(c) (relativístico,
  travado pela Lorentz de R1 + mágnon de E2) → **free-streama** (C3); a janela de
  Jeans só existiria com fine-tuning crítico.
- **Obstrução (FM2-1+FM2-2):** MOND quer a fase **ordenada** (Goldstone divergente);
  Jeans quer o **ponto crítico** (c_s→0). São fases **opostas**. Nenhum J único dá
  os dois — nem preserva o fundo como poeira (FM2-4).

## O resultado POSITIVO que sobrevive (registrado honestamente)

Apesar da morte cosmológica, FM2-1 entrega um resultado de valor próprio:

> **A função de interpolação MOND da DEV tem origem microscópica na TEIC.** A
> susceptibilidade longitudinal do ferromagneto de orientação O(3) (o vácuo de E1)
> reproduz o expoente deep-MOND χ∥ ~ h^(−1/2) — a anomalia de coexistência de
> Goldstone (Brezin–Wallace). A fenomenologia ν=1/√(g/a₀) da DEV (Paper I), antes
> postulada, **emerge** da estrutura de Goldstone do vácuo orientacional.

Isto **fortalece** o setor de galáxias da DEV (liga Paper I a E1), mesmo enquanto o
setor cosmológico morre.

## Consequência

```
Tensão S8: NÃO resolvida pela estrutura de duas fases da TEIC+DEV.
  A inversão (σ8 menor) exigiria acertar DUAS janelas estreitas a partir da rede;
  a rede mostra que elas pedem fases OPOSTAS do ferromagneto → impossível
  simultaneamente sem ingrediente externo.
  → matéria escura como "fase do campo MOND" NÃO é realizada pelo ferromagneto nu.
  → a previsão observacional válida da DEV permanece BTFR (galáxias), reforçada
    agora pela origem microscópica do ν MOND (FM2-1).
  → fronteira confirmada: TEIC+DEV funciona onde foi calibrada; o setor de
    perturbações cosmológicas exige física que o ferromagneto nu não tem.
```

## O que faltaria para reabrir — e por que o m_A NÃO basta (cálculo honesto)

Um **comprimento de correlação externo** daria o corte físico L-independente que
FM2-1 mostrou faltar. O candidato natural é a massa do vetor m_A do Paper II, que dá
um comprimento de Compton ξ_A = ℏ/(m_A c). O **mecanismo** funciona (massa → gap dos
Goldstones → χ∥ para de divergir → segunda escala). Mas a **escala está errada por
~6 ordens de grandeza:**

| Escala | Valor |
|---|---|
| ξ_A = ℏ/(m_A c), com m_A > 3.7×10⁻²⁵ eV (Paper II) | **17.3 pc** (= "L<17 pc" do Paper II) |
| Escala de σ8 (R₈ = 8 Mpc/h) | 11.9 Mpc |
| ξ_A / R₈ | **1.5×10⁻⁶** |

ξ_A é **sub-galáctico** (~17 pc), ~7×10⁵ vezes menor que a escala de σ8. Em escalas
cosmológicas o campo com essa massa é efetivamente blindado/pontual — **não altera o
crescimento na escala de σ8**, então o **Veredito C permanece**. Pior: o corte do
m_A atua em **alta** aceleração (escalas pequenas, lado newtoniano), o **extremo
oposto** ao gap de baixa aceleração (g/a₀ ∈ 0.005–0.016) que precisaríamos preencher.

Para um corte na escala cosmológica (ξ ~ Mpc) seria preciso m ~ 5×10⁻³¹ eV/c² — ~7×10⁵
vezes **mais leve** que o vetor, massa que o **próprio Paper II exclui**. Logo a
reabertura exigiria uma **segunda escala nova** (muito mais leve), não o m_A.

> O m_A **prevê** algo real porém **sub-galáctico**: blindagem da MOND abaixo de
> ~17 pc (aglomerados globulares, binárias largas) — o oposto do que S8 precisa.

O Botão 2 (separar c_s do mágnon do vácuo via equação de estado do condensado a
densidade finita) também exige a ação relativística completa da DEV + CLASS, fora do
escopo da rede E1/E2. Sem uma escala nova ≪ m_A, **Veredito C** fica.

## Anti-circularidade e disciplina

a₀ de SPARC; a_c2 e c_s **medidos na rede**; nenhum valor de σ8/KiDS inserido. As
duas janelas (gap a_c2, Jeans c_s) foram fixadas no charter ANTES de medir; a rede
não as atingiu e nenhum parâmetro foi ajustado para escapar. As mortes C1/C3/C4
foram pontuadas como escritas. O desfecho mais provável pré-registrado (B/C) se
confirmou: **C**.

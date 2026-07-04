# PRÉ-REGISTRO — CAMPANHA XI: Um comprimento de correlação pode divergir?

> Congelado **antes** de qualquer simulação registrada. Charter: prompt do usuário
> "Campanha XI — teste de emergência de escala". Predecessores diretos:
> E1/E4 (ferromagneto de orientação O(3) sobre Hasse 3+1D, veredito mean-field) e a
> nota de rodapé 1 do paper do fóton ("sem comprimento de correlação divergente").
> Engine reutilizado SEM MODIFICAÇÃO: `results/vacuum_structure/orientation/orientation_core.py`.

**Data de congelamento:** 2026-06-24

---

## HIPÓTESE SOB TESTE

O caráter **mean-field** do ferromagneto de orientação sobre o sprinkling de Poisson
(3+1)D — correlação conectada por link ~1/z sem cauda, U₄=2/3 em todo tamanho, z
crescendo com N, **nenhum ξ divergente** — é consequência da **alta coordenação
não-local** do grafo de Hasse cru. Reduzindo a não-localidade efetiva do substrato,
uma transição genuinamente de 2ª ordem **com ξ divergente** pode emergir.

**Null:** nenhuma modificação que reduza a coordenação efetiva produz ξ divergente;
o caráter mean-field é estrutural para esta classe de substratos.

---

## ALERTA ANTI-CIRCULARIDADE (congelado)

Alavancas A e B inserem uma escala de corte (ℓ ou ℓ_k ou cap k). **Essa escala é
inserida à mão e é `[External]`.**

- Um ξ finito da ordem do corte inserido **NÃO conta como sucesso** (é circular).
- O ÚNICO sinal legítimo de emergência: ξ_2nd/ℓ → ∞ com L em J_c (ξ rastreia o
  TAMANHO L, não o corte ℓ). Equivalentemente ξ_2nd/L cresce ou cruza.
- A Alavanca C (dimensão menor) **não insere escala** → se ξ divergir lá, é limpo.
- Toda escala inserida é registrada e marcada `[External]` no JSON de saída e na
  síntese.

---

## OBSERVÁVEIS (definições congeladas)

Substrato base: Poisson (3+1)D (e (2+1)D na Alavanca C), grafo de Hasse
(`causal_link_graph`), modelo O(3) (`O3Model`), J = acoplamento = 1/T.

- **Parâmetro de ordem:** `m = model.order_parameter()` = |⟨n⃗⟩| (≥0).
- **Binder cumulant:** `U4 = 1 − ⟨m⁴⟩/(3⟨m²⟩²)`.
- **Susceptibilidade:** `χ = N·(⟨m²⟩ − ⟨m⟩²) = N·Var(m)`.
- **Coordenação:** z = ⟨degree⟩ do grafo de links (mean-field se z↑ com N).
- **Comprimento de correlação de 2º momento** (estimador FSS-friendly), do fator
  de estrutura transverso `structure_factor` (real, cos/sin — sem complexo):
  ```
  xi_2nd = (1/k_min) * sqrt( S(k_min)/S(k_2) - 1 )      # forma de 2 modos
  ```
  com k_min = 2π/L_s o menor modo da caixa espacial e k_2 = 2·k_min. (Uso a forma
  de dois modos k_min,2·k_min em vez de S(0)/S(k) porque a caixa NÃO é periódica e
  S(0) do componente transverso mean-subtraído é mal-condicionado; ambas medem a
  curvatura de S(k) perto de k=0. A quantidade decisiva é a razão adimensional
  **ξ_2nd/L_s**, congelada AGORA.)
- **C(r) real-space:** `fit_forms` na cauda (já existe; reporta winner exp/power/const).
  Declaro honestamente que a distância de grafo satura rápido (small-world) — esse
  alcance limitado É parte do fenômeno, reportado não escondido.

---

## LOCALIZAÇÃO DE J_c (congelada antes de medir ξ)

J_c é localizado **pela varredura** (pico de χ), por substrato/tamanho, SEM importar
nenhum valor externo. Âncora de plausibilidade (não usada na decisão): E1/E4 mediram
χ-peak em J≈0.05–0.08 para O(3)/U(1) no Hasse 3+1D. Toda medição de ξ decisiva é
feita **em J_c localizado**, nunca fundo numa fase.

---

## PARÂMETROS CONGELADOS (não ajustar após ver resultados)

| Parâmetro | Valor frozen |
|---|---|
| Engine | `orientation_core` (O3Model, causal_link_graph, structure_factor), SEM modificação |
| Modelo | O(3) (mais barato; mesmo do veredito mean-field) |
| Caixas (3+1)D | cúbicas L⁴, L ∈ {3.0, 3.6, 4.2, 4.8} a ρ=2.0 → ladder de ≥4 tamanhos |
| Caixas (2+1)D | cúbicas L³, L ∈ {3.6, 4.6, 5.6, 6.6} a ρ=2.0 (ajustado p/ N comparável) |
| Densidade ρ | 2.0 (fixa em todas as alavancas) |
| Grade J | varredura grossa [0.02…0.40] (8–10 pts) p/ localizar J_c; refino ΔJ fino em torno do pico |
| Sementes | ≥6 por (L,J); seeds determinísticas `1000+s` |
| Termalização | 300 sweeps (passo adaptativo, target 0.4) |
| Medição | 60 amostras, meas_every=2 (config E4_0 validada) |
| k da ξ_2nd | k_min=2π/L_s, k_2=2·k_min (congelado acima) |

---

## ALAVANCAS E CRITÉRIOS (congelados ANTES de rodar)

### Alavanca C — Dimensão efetiva menor (2+1)D — PRIORIDADE 1 (não insere escala)
Sprinkling (2+1)D em vez de (3+1)D. Grafo de Hasse menos conectado.
- **SUCESSO `[Derived]`:** ξ_2nd/L cresce/cruza em (2+1)D **sem corte inserido** —
  emergência limpa não-circular.
- **MORTE:** mean-field persiste em (2+1)D (ξ_2nd/L não-crescente, U₄ sem cruzamento).

### Alavanca A — Coordenação efetiva finita (cap rígido k-NN) — PRIORIDADE 2
Substitui os links de Hasse pelos **k vizinhos causais mais próximos** (por
tempo-próprio do link), levando z de O(10–100) para O(1–10). Cap k é `[External]`.
O Metropolis roda VERBATIM sobre o grafo podado (só o conjunto de arestas muda).
- **SUCESSO `[Derived]`:** num k, a suíte vira 2ª-ordem genuína **E** ξ_2nd/ℓ → ∞ com
  L em J_c (diverge em unidades do corte; ℓ≡escala do cap).
- **CIRCULAR (não é sucesso):** ξ ~ k (só rastreia o corte).
- **MORTE:** para todo k testado que mantenha ordem, ξ_2nd/L não-crescente e U₄ sem
  cruzamento.
- **Confound vigiado:** cap pequeno demais FRAGMENTA (sem ordem por desconexão, não
  por criticidade). Meço `connected_fraction` e mantenho LRO antes de aceitar; ξ
  medido EM J_c, não fundo numa fase.

### Alavanca B — Não-localidade intermediária (mesoescala ℓ_k) — PRIORIDADE 3
Grafo de vizinhança de mesoescala: conecta i–j causalmente relacionados dentro de
uma janela de tempo-próprio ℓ_k ≫ escala de discretude (proxy de família B_k de
Aslanbeigi–Saravani–Sorkin no nível do grafo de acoplamento; declarado como proxy).
ℓ_k é `[External]`. Mesmos critérios de A com ξ_2nd/ℓ_k.

---

## CRITÉRIO DE MORTE GLOBAL (verbatim, pré-registrado)

Se em TODAS as alavancas A, B, C que levam a coordenação efetiva ao regime O(1)–O(10)
mantendo ordem de longo alcance, ξ_2nd(L) medido em J_c **não diverge** — isto é,
ξ_2nd/L é **não-crescente** com L, U₄ **não** exibe cruzamento invariante de escala, e
χ_max permanece em **lei de volume / mean-field** — então a hipótese de que reduzir a
não-localidade permite ξ divergente está **FALSIFICADA** para esta classe de
substratos, e o caráter mean-field (e a consequente ausência de escala emergente por
transmutação) é confirmado como **ESTRUTURAL**. Nenhum apelo a tamanho maior é
admissível se ξ/L já decresce monotonicamente nos tamanhos medidos.

Falsificação aqui é resultado **publicável e forte**. "Não" não é fracasso.

---

## PROTOCOLO ANTI-CIRCULARIDADE
- ξ e a suíte usam só o grafo + energia cos/dot + S(k) real (cos/sin). Sem complexo,
  sem fórmula de dilatação. Guard `tests/test_no_circularity.py` deve passar.
- J_c localizado pela varredura, sem importar valor externo.
- Toda escala inserida (k, ℓ_k) marcada `[External]`; conclusão de emergência só usa
  adimensionais (ξ/L, ξ/ℓ, expoentes).
- Sementes congeladas acima. NÃO reajustar grade J nem thresholds após ver dados.

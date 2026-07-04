# PRÉ-REGISTRO — CAMPANHA_SU3_ORDEM_TRANSICAO

> Congelado **antes** de qualquer simulação nova. Charter: prompt do usuário
> (CAMPANHA_SU3_ORDEM_TRANSICAO). Predecessor direto: FLB2 (`results/matter/fl1/
> FLB2_transition_order.py`, L≤16, "1ª ordem desfavorecida, statistics-limited").

**Data de congelamento:** 2026-06-22

### Emendas pré-resultado (registradas antes de QUALQUER run registrado)
Duas emendas feitas após o smoke-test (`quick`, parâmetros NÃO-registrados) e a
decisão de escopo do autor, **antes** de qualquer simulação com os parâmetros
congelados produzir resultado:
1. **Grade J alargada** de [2.60,2.72] (13 pts) para **[2.60,2.76] (17 pts)**. Razão:
   FLB2 documentou que uma grade que perde o pico que deriva com L é erro de
   operacionalização (não de física); o pico deriva 2.65→2.70 até L=16 e pode subir
   mais em L=20/24. Alargar só ajuda a localizar o pico, não enviesa a ordem.
2. **L=24 tornado condicional** (escopo "Opção 3" do autor): rodar L≤20 primeiro;
   só gastar as ~3h de L=24 se o veredito em L≤20 NÃO for concordante. O critério de
   disparo (abaixo) é congelado AGORA, antes de ver L=20, para que "borderline" não
   possa ser redefinido com os dados de L=20 à mão.

---

## RECONCILIAÇÃO DE UNIDADES (registrada antes de rodar — não é ajuste pós-hoc)

O charter cita "J_c≈0.3" e "engine de sprinkling SU(3)". Esses são números de
**substratos diferentes**:

- **J_c≈0.3** é do ferromagneto de cor no **substrato causal de Poisson** (memória
  FL1 Fase B — rede causal esparsa).
- **J_c≈2.65** é do mesmo ferromagneto no **engine de rede cúbica periódica**
  (`su3_core.SU3ChiralModel` + `lattice_periodic`), que é o engine que FLB/FLB2
  usaram para caracterizar a transição e medir Binder/χ. Verificado por benchmark
  nesta sessão: o pico de χ está em J≈2.65–2.70.

Esta campanha é a **continuação direta de FLB2** e portanto usa o **engine de rede
cúbica** (`su3_core`, importado SEM MODIFICAÇÃO). A varredura é em torno de
**J≈2.65**, não 0.3 — varrer em 0.3 cairia fundo na fase desordenada e não veria
transição alguma. A comparação com o J_c de FL1/FLB (2.65) só é feita em V1, DEPOIS
de medir (protocolo anti-circularidade abaixo).

---

## HIPÓTESES

**H0 (nula):** A transição SU(3) é de **SEGUNDA ORDEM** para todos os L testados
(sem descontinuidade em E, sem pico de χ crescente como volume, sem histerese). O
ferromagneto de cor se comporta como o SU(2).

**H1 (alternativa):** A transição é de **PRIMEIRA ORDEM** em L suficientemente grande
(descontinuidade em E, pico de χ ∝ L^d, histerese detectável).

---

## OBSERVÁVEIS (definições congeladas)

- Parâmetro de ordem: `m = model.order_parameter()` (= |⟨v_i⟩|, sempre ≥ 0).
- **Binder cumulant:** `U4 = 1 − ⟨m⁴⟩ / (3⟨m²⟩²)`.
- **Susceptibilidade:** `χ = N·(⟨m²⟩ − ⟨m⟩²) = N·Var(m)` (como m≥0, ⟨|m|⟩=⟨m⟩).
- Energia intensiva: `model.energy_per_link()/J` (para histograma de calor latente).

---

## PARÂMETROS CONGELADOS (não ajustar após ver resultados)

| Parâmetro | Valor frozen |
|---|---|
| Engine | `su3_core.SU3ChiralModel` em `lattice_periodic((L,L,L))`, SEM modificação |
| L primário | **8, 12, 16, 20** (ordem crescente; checkpoint por L) |
| L=24 | **CONDICIONAL** — só roda se o critério abaixo disparar (decidido ANTES de ver L=20) |
| Grade J | `np.arange(2.60, 2.761, 0.01)` → 2.60…2.76, **ΔJ=0.01, 17 pontos** |
| Range J | **[2.60, 2.76] fixado agora** (bracketa a deriva documentada de FLB2 J_c(L): 2.65→2.70; +0.06 de folga no topo). NÃO reajustar. |
| Sementes | **5 por (L,J)**: `seed = 1000*s + 7`, s∈{0,1,2,3,4} → {7,1007,2007,3007,4007} |
| Termalização | **500 sweeps** (passo adaptativo, target acc 0.4) |
| Medição | **2000 sweeps**, meas_every=1 (5×2000 = 10000 amostras de m por (L,J)) |
| Histograma E em J_c | 1500 burn + 4000 meas, 3 sementes {2000,2031,2062} (só p/ D-latente em L≥16) |

---

## KILL-CRITERIA NUMÉRICOS (pré-registrados)

### OT1 — Binder cumulant U4(L)
- **MORTE de 1ª ordem (⇒ 2ª ordem):** cruzamentos U4*(L) das curvas convergem para
  um J_c estável com **|J_c(L=24) − J_c(L=12)| < 0.01**, e U4 não exibe dip abaixo
  do platô gaussiano.
- **MORTE de 2ª ordem (⇒ 1ª ordem):** cruzamentos se afastam com L, **OU** U4 mínimo
  cai **abaixo de (valor-de-platô − 0.05)** com dip que se aprofunda com L.

### OT2 — Susceptibilidade χ_max(L)
Ajuste χ_max ∝ L^x (equivalentemente ∝ N^{x/3}); reportamos o expoente em L.
- **2ª ordem:** **x ≈ γ/ν < 2** (sub-volume).
- **1ª ordem:** **x ≈ d = 3** em L (= ∝ volume N¹; rede 3D cúbica).
- **Inconclusivo:** x ∈ (2, 3) → registrar como inconclusivo.

> Nota dimensional: a rede é **3D cúbica** (N=L³). Lei de volume de 1ª ordem é
> χ_max ∝ N = L³, i.e. **x=3 em L**. (O charter escreveu "d=4"; isso valeria para
> rede 4D. O engine de FLB/FLB2 é 3D — congelo x_volume = 3.)

### OT3 — Histerese (só roda se OT1 e OT2 derem vereditos OPOSTOS)
Ciclo J: 2.60→2.72→2.60, medindo ⟨m⟩ nas duas direções, L=16 e 20.
- **1ª ordem:** área normalizada do ciclo **> 15%** em L=20.
- **2ª ordem:** área normalizada **< 5%** em L=20.
- **Inconclusivo:** entre 5% e 15%.
Se OT1 e OT2 concordarem, OT3 é desnecessário — registrar isso, não rodar.

### CRITÉRIO DE DISPARO DE L=24 (congelado ANTES de ver L=20)
Decidir rodar L=24 com base SÓ nos indicadores de L≤20, segundo esta regra fixa:

**RODAR L=24 se QUALQUER uma:**
- U4 ainda não convergiu: **|J_c(L=20) − J_c(L=16)| > 0.01** (J_c(L)=pico de χ), OU
- expoente de χ_max em zona inconclusiva: **x ∈ (2.0, 3.5)**, OU
- histerese em L=20 entre **5% e 15%** (zona inconclusiva).

**NÃO RODAR L=24 se** os três indicadores derem veredito **concordante** em L≤20
(todos 2ª ordem OU todos 1ª ordem). Nesse caso L=24 só confirmaria o já confirmado —
gasto de ~3h sem ganho científico; declarar L=24 como confirmação dispensável.

> Nota sobre histerese aqui: OT3 normalmente só roda se OT1 e OT2 discordam. Para
> alimentar este critério, OT3 (L=16,20) roda SEMPRE que OT1 e OT2 NÃO forem ambos
> concordantes-2ª-ordem em L≤20 (i.e. quando há qualquer dúvida); se OT1 e OT2 já
> concordam limpo, a histerese é dispensável e o terceiro voto é considerado
> concordante por construção.

### INCONCLUSIVO (declarar como tal, não forçar)
- Indicadores contraditórios entre OT1/OT2/OT3, OU
- L_max atingido (CPU esgotada) antes de convergência clara, OU
- Resultado muda sob o teste de robustez V3 (±10% na ação).

---

## VERIFICAÇÕES DE CONSISTÊNCIA

- **V1 (consistência com FL1):** J_c medido deve cair em **±0.02 de 2.65** (J_c de
  FLB). Se divergir mais: PARAR e investigar antes de interpretar a ordem.
- **V2 (consistência interna):** OT1+OT2 (+OT3 se rodar) devem concordar. Se 2
  concordam e 1 discorda, registrar qual e por quê — não forçar consenso.
- **V3 (robustez):** repetir L=16 com J reescalado por ±10% (mesmo teste de FLR). O
  veredito sobre a ordem não pode mudar. Se mudar → INCONCLUSIVO.

---

## PROTOCOLO ANTI-CIRCULARIDADE
- A varredura J localiza o pico de χ / cruzamento de U4 **sem usar** o valor 2.65;
  comparação com FLB só em V1, depois de medir.
- Sementes fixas e registradas acima, antes de rodar.
- NÃO ajustar o range de J depois de ver os primeiros resultados.
- Guard `tests/test_no_circularity.py` deve passar (script de análise é puramente
  real; o complexo SU(3) fica dentro de `su3_core`, nos blocos SU(3) GROUP-DEF).

---

## DESFECHOS (registrar resultado primeiro, narrativa depois)
- **A — SEGUNDA ORDEM confirmada:** U4 converge, χ_max sub-volume, sem histerese.
  → Ressalva FL1 fechada; portão do PAPER_SU3 desbloqueado.
- **B — PRIMEIRA ORDEM detectada:** U4 com dip que aprofunda, χ_max ∝ L³, histerese.
  → Adendo honesto a FL1 + seção dedicada no paper. NÃO mata SU(3) (confinamento +
  octeto permanecem); só muda a descrição da transição.
- **C — INCONCLUSIVO:** indicadores contraditórios ou L_max insuficiente.
  → PAPER_SU3 declara a limitação; campanha maior (L>24, cluster) fica como futuro.

Em todos: não reabrir kill-criterion após ver resultado; resultado vai para
RESEARCH_MAP antes de qualquer paper; commit na branch `su3-ordem-transicao`.

# PRE-REGISTRO — B1 · Razões internas independentes de K (hierarquia)

> Campanha de organização TEIC (Fase 2), Frente B (ESCALAS), item B1 — prioridade
> da frente. Gate A1 já VERDE (libera a frente B). Fontes: `HIERARQUIA_EXPERIMENTOS.md`
> §B1, `PLANO_EXECUCAO.md` §2, `INVENTARIO_PIPELINE.md` §6. Pré-registro escrito
> ANTES do varredor (disciplina do programa).

---

## 1. Pergunta

Existe uma combinação adimensional de **M_Sk** (massa do Skyrmion), **σ** (string
tension) e **G_net** (resposta gravitacional) que seja **independente da
normalização K da ação**? Se for um número puro **não-trivial**, ataca o problema
de hierarquia (M_próton/M_Planck ~ 10⁻¹⁹) — o único tipo de escala (razão entre
domínios) que a teoria pode prever sem fixar unidade SI.

## 2. Definição de K (decisão registrada)

**K = rescala global da ação fundamental, S → K·S** (escolha do autor, jun/2026).
A ação fundamental única recebe um prefator global K; os três setores o herdam.
Consequências analíticas (a serem CONFIRMADAS pelo varredor, não assumidas):

| quantidade | setor | resposta a S→K·S | expoente em K |
|---|---|---|---|
| **M_Sk** | quiral+Skyrme (clássico, `E2+e_sk·E4`) | saddle minimiza K·E ⇒ **perfil invariante**, energia ×K | **+1** |
| **G_net** | gravidade (Poisson `−K_stiff·∇²θ=fonte`) | K_stiff→K·K_stiff ⇒ θ→θ/K | **−1** |
| **σ** | gauge (Wilson `S_W=β·Σ(…)`) | S→K·S ≡ **β→K·β** ⇒ σ corre (liberdade assintótica) | **não-potência** |

A assimetria é o cerne de B1: σ **corre** com β (curva medida FLC:
σ=[1.35,1.10,0.96,0.67,0.33] em β=[4,4.5,5,5.5,6]), não escala como potência de K.
Logo nenhuma combinação **com σ** pode ser invariante de potência.

## 3. Combinações candidatas e predição

Sejam M_Sk∝Kᵃ, G_net∝K^c (a=+1, c=−1 previstos); σ corre.

| combinação | expoente líquido | predição |
|---|---|---|
| **M_Sk·G_net** | a+c = 0 | invariante — MAS = A (amplitude de Poisson), pois G_net≡A/M ⇒ **trivial/definicional** |
| **M_Sk·√G_net** (= M_Sk/M_Pl, a HIERARQUIA) | a+c/2 = +½ | **escala ∝√K** — hierarquia NÃO fixada |
| **M_Sk²·G_net** | 2a+c = +1 | escala |
| **σ·G_net** | corre + (−1) | escala (σ corre) |
| **M_Sk/√σ** | corre | escala |

## 4. Critério de sucesso

Uma combinação adimensional é **constante a <5%** ao varrer K em **≥1 década**,
**enquanto M_Sk, σ, G_net individualmente escalam com K** (controle), **E** o seu
valor é um **número puro não-trivial** (não O(1) geométrico, não definicional).

## 5. Critério de morte

(a) Toda combinação não-trivial ainda **escala com K** (não invariante); OU
(b) a única combinação invariante é **trivial** — 1/constante-geométrica conhecida,
definicional (ex.: M_Sk·G_net≡A), ou O(1) sem hierarquia.
→ o substrato **não fixa razão de massa entre domínios** via a normalização da
ação; a hierarquia permanece **[EXTERNO-B]**, reportada como **porta fechada
bem-entendida** (negativo de 1ª classe), e **alimenta B5** (por que η/ℏ não pinam).

## 6. Anti-circularidade (atenção máxima)

Nenhum K-independente pode vir de um literal de escala (guarda A1 cobre o varredor).
A invariância tem de **emergir do varredor**: M_Sk e G_net re-medidos/re-escalados
sob a ação×K via código existente (`su3_core.radial_relax`, `d3_audit_core`
Poisson); σ(K) da curva MC medida (β=K·β₀), com a limitação de range honestamente
reportada. Os expoentes (a, c) são **ajustados do scan**, não impostos.

## 7. Entregáveis

1. `B1_kscan.py` — varredor (orquestra medidas existentes sob S→K·S).
2. `B1_kscan.json` + `SCAN_REPORT.md` — expoentes ajustados, combos, valores.
3. `SYNTHESIS.md` — veredito + atualização do RESEARCH_MAP.

# SÍNTESE — B1 · Razões internas independentes de K

> Campanha ESCALAS_B1 (Fase 2, Frente B), prioridade da frente. Pré-registro:
> `PRE_REGISTRO.md`. Varredor: `B1_kscan.py` → `B1_kscan.json`. Data: jun/2026.
> **Veredito: MORTE bem-entendida — o substrato NÃO fixa razão de massa entre
> domínios via a normalização da ação. Hierarquia permanece [EXTERNO-B].**

---

## 1. Decisão de desenho

K = **rescala global da ação, S → K·S** (escolha do autor). Os três setores
herdam um único K com respostas **distintas**, confirmadas pelo varredor:

| quantidade | expoente ajustado em K | origem |
|---|---|---|
| **M_Sk** | **K^+1.000** | saddle clássico de E2+e_sk·E4 (perfil K-invariante, energia ×K) |
| **G_net** | **K^−1.000** | Poisson `−K·∇²θ=fonte` re-medido (reproduz D3D "G_net~1/K") |
| **σ** | **corre (K^−3.2 na janela)** | Wilson β→Kβ; liberdade assintótica (curva FLC medida) |

Controle satisfeito: M_Sk, σ, G_net **individualmente escalam/correm com K**.

## 2. Teste de invariância (emergente do scan, K ∈ [0.3, 10] = 33×)

| combinação | expoente em K | CV | invariante <5%? | leitura |
|---|---|---|---|---|
| **M_Sk·G_net** | 0.00 | 0.000 | **SIM** | mas = amplitude A (G_net≡A/M) → **definicional/trivial** |
| **M_Sk·√G_net** (= M_Sk/M_Pl, a HIERARQUIA) | **+0.50** | 0.56 | não | **escala ∝√K** |
| **M_Sk²·G_net** | +1.00 | 1.03 | não | escala |
| **σ·G_net** (janela β∈[4,6]) | corre | 0.51 (×6.2) | não | σ corre |
| **M_Sk/√σ** (janela) | corre | 0.42 (×3.1) | não | σ corre |

## 3. Veredito (R-1 negativo)

**MORTE, critério (a)+(b):**

- **(b)** A única combinação plana a <5% é **M_Sk·G_net**, que é **definicional**:
  G_net é *medido* como A/M (amplitude de Poisson sobre massa-fonte), logo
  M_Sk·G_net = A trivialmente. Não é uma razão entre domínios prevista — é a
  própria definição de G_net. Não carrega hierarquia.
- **(a)** A combinação que **carregaria** a hierarquia — M_Sk·√G_net = M_Sk/M_Pl
  (pois M_Pl ~ 1/√G_net) — **escala como K^+½** (CV 56%). O substrato **não fixa**
  a razão de massa: ela flutua com a normalização global da ação.
- σ **corre** (não é potência de K) → entra em **nenhuma** invariante de potência;
  toda combinação com σ varia (×6.2, ×3.1 na janela medida).

**Razão estrutural limpa:** sob S→K·S, M_Sk∝K¹ e G_net∝K⁻¹; a hierarquia
M_Sk·√G_net tem expoente líquido +½ ≠ 0. Uma rescala global da ação é apenas uma
escolha de unidade — não pode fixar um número grande adimensional entre domínios.
Este é o conteúdo de "forma emerge, escala não": o único invariante é o
definicional; o fisicamente significativo (hierarquia) não é invariante.

## 4. Consequência (plano R-1)

Decisão de escalas **negativa, bem-entendida** (negativo de 1ª classe, não falha
de busca):

- A hierarquia M_próton/M_Planck permanece **[EXTERNO-B]**.
- **Promover B5** ("por que η e ℏ não pinam") ao topo da Frente B: B5 passa a ser
  a peça que **explica o mecanismo** desta porta fechada (rescala global = unidade;
  não há número grande invariante), fechando a tese "forma deriva, escala não" com
  um teorema/mecanismo, não só com a falha de B1.
- B2 (ξ_grav/ξ_cor) **não** é promovido (dependia de um B1 positivo para uma 2ª razão).
- Porta registrada no `RESEARCH_MAP.md`.

## 5. Anti-circularidade

Varredor sob guarda A1 (guarda de dilatação + literais de escala VERDE sobre
`B1_kscan.py`). A invariância **emergiu do scan** (expoentes ajustados, não
impostos): M_Sk^+1.000 e G_net^−1.000 ajustados; nenhum número-puro veio de
literal. Os σ usados são razões de Creutz adimensionais medidas (FLC_confinement.json),
não escalas físicas.

## 6. Limitação honesta

σ(K) sobre uma década completa exigiria Wilson MC fresco em β∈[1.5,50] (regime de
medição degradado nas pontas). Como σ **não** participa de nenhuma invariante (corre),
a morte é determinada pelos combos sem-σ sobre a década inteira; os combos-com-σ
são demonstrados não-invariantes na janela β∈[4,6] medida (×6.2, ×3.1). O veredito
é robusto à extensão de σ.

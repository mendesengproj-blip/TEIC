# CROSS_RELATIONS_II: as constantes puras de X₀ e m_A na mesma rede

> Continuação do Ataque 6 (`CROSS_RELATIONS.md`), executando o "próximo elo"
> declarado em `results/bridge/cross_relations/CR2_table.md`: m_A∝√ρ (PE3) e
> X₀∝ρ (C3) entraram na tabela só como **expoentes herdados**; aqui medem-se as
> suas **constantes puras na mesma rede** — fechando o quadro de quatro setores
> (gravitação, matéria topológica, massa vetorial, saturação DBI) sobre uma
> única granularidade. Resultados em `results/bridge/cross_relations/`.
> NÃO modifica campanhas anteriores (consome os protocolos C1, C3, W2).
>
> **Condição "mesma rede", declarada com honestidade:** G_net e λ_Sk vivem no
> RGG espacial d=3 (CR1/SC — inalterados); X₀ e m_A vivem no sprinkling causal
> 3+1D. CR3 e CR4 usam **as mesmas sprinklings** (mesmas sementes, mesmas
> caixas): dentro do setor causal a condição é literal.

## ✅ VEREDITO (preenchido após as corridas; nenhum critério alterado)

```
CR3  SUCESSO — colapso Exp(1) confirmado (KS ≤ 0.025 nos dois ρ mais altos;
     check exato de mediana ρV(τ_med,H)/ln2 ∈ [0.98, 1.04] em todos os ρ);
     expoente q = −0.534 ± 0.017 (2.0σ de −½, dentro do limite 3σ — desvio
     consistente com a correção sublíder t⁴ln(H/t) do volume exato).
     Constante pura: X₀·Δθ_max⁻² = πρH²/ln2, fechamento assintótico a 0.29%
     (π̂ = 2.795→3.151 = π·1.0029 em ρ=75 — padrão CR1b). O expoente é UV
     (∝ρ, C3 inalterado); a constante carrega o regulador IR H² declarado.
CR4  VEREDITO B — a herança PE3 (s=+1/2) MORRE no substrato causal:
     s_m = 0.068 ± 0.045 (9.5σ de +0.5; consistente com ZERO a 1.5σ).
     Reportada como morte da entrada herdada (sliver não-local domina os
     momentos de link — premissa "escala única ρ^¼" falha, cf. C1).
     O que sobrevive: m²_iso·λ_p = 4(C2_t+3C2_x)/(Π_E+Π_B) é número puro
     ESCALA-INVARIANTE ≈ 520 (CV 5.3% sobre ρ×4.7; caixa +8.7% — não
     IR-regulado). Split E/B 4.11→3.47 decrescendo rumo ao 2.97 de W2
     (artefato de regulador, cf. LIV_VECTOR) — reportado por canal.
```

Relatórios: [`CR3_x0_constant.md`](results/bridge/cross_relations/CR3_x0_constant.md) ·
[`CR4_ma_constant.md`](results/bridge/cross_relations/CR4_ma_constant.md).
**O quadro de quatro setores fecha** — com a correção honesta de que a entrada
m_A da tabela CR2 muda de natureza (não ∝√ρ; é escala-invariante):

| Setor | Número puro | Valor | Status |
|---|---|---|---|
| Gravitação | G_net·ρ²·r_c⁵ | 15/8π² (2.5%) | CR1/CR1b |
| Matéria topológica | λ²_Sk/⟨a²⟩ | 1/120 (0.06%) | SC1–SC3 |
| Saturação DBI | X₀·Δθ_max⁻²/(ρH²) | **π/ln2 (0.29%)** | **CR3 (novo)** |
| Massa vetorial | m²_iso·λ_p | **≈520, escala-invariante (CV 5.3%)** | **CR4 (novo)** |

---

## CR3 — a constante pura de X₀ (previsão exata, derivada antes de medir)

**Setup.** X₀ = (Δθ_max/Δτ_min)² (C3). Δτ_min por evento de bulk = menor tempo
próprio entre os vizinhos causais futuros com Δt < H (cap declarado, cone
inteiro dentro da caixa). Para um sprinkling de Poisson de densidade ρ, o
número de eventos no sliver {0 < τ < t, 0 < Δt < H} é Poisson com média ρ·V(t,H),
onde (cálculo exato, 3+1D):

```
V(t,H) = (π/3)H⁴ − (4π/3)·[ H(2H²−5t²)√(H²−t²)/8 + (3t⁴/8)·ln((H+√(H²−t²))/t) ]
       = π t² H² · [1 + O((t/H)² ln(H/t))]        (forma líder)
```

**Previsão exata (sem parâmetros):** a variável reescalada **u ≡ ρ·V(Δτ_min, H)
é Exponencial(1)** para todo evento de bulk — colapso distribucional completo,
qualquer ρ. Em particular median(u) = ln 2, e na forma líder

```
X₀·Δθ_max⁻² = 1/Δτ²_med = π ρ H² / ln 2          (constante pura: π/ln2 ≈ 4.532)
```

**O conteúdo físico pré-declarado:** o expoente de X₀ é UV (∝ρ¹, C3 inalterado),
mas a **constante carrega o regulador IR H²** — o link mínimo é estatística de
extremos do sliver que abraça o cone (não-compacto; truncado pelo cap H, mesmo
status do regulador de caixa em LV3). Honestidade: Δτ é invariante; H é
frame-dependente e declarado.

**Critérios de morte (pré-registrados):**
```
CR3 morre se: distância KS entre u empírico e Exp(1) > 0.05 nos DOIS ρ mais
              altos; OU median(u)/ln2 fora de [0.85, 1.15] nos dois ρ mais
              altos; OU expoente q de Δτ_med ∝ ρ^q com |q+1/2| > 3σ.
Caveats declarados: u_i de eventos próximos são fracamente correlacionados
(cones futuros sobrepostos) → usa-se a DISTÂNCIA KS, não p-valor; truncagem
(eventos sem vizinho no cap) exige ρ(π/3)H⁴ ≥ 5 (fração < 1%, contada).
```

## CR4 — a constante pura de m_A (teste da herança PE3 no substrato causal)

**Setup.** A massa do vetor exige o setor de plaquetas (C4/W1: só com links A é
auxiliar). Na mesma sprinkling: links = relações de cobertura (protocolo C1),
plaquetas = diamantes causais mínimos (protocolo W2), ambos filtrados ao bulk.

```
C2^{μν} = (1/2V_in) Σ_links Δτ e^μ e^ν      (canais C2_t = C2^{00}, C2_x = média C2^{ii})
Π_E     = (1/V_in) Σ_plaq Σ_i (Ω^{0i})²  ;  Π_B = (1/V_in) Σ_plaq Σ_{i<j} (Ω^{ij})²
m²_E ≡ 4 C2_x/(λ_p Π_E/3) ;  m²_B ≡ 4 C2_x/(λ_p Π_B/3) ;
m²_iso ≡ 4 (C2_t+3C2_x)/(λ_p (Π_E+Π_B))
```

Fatores O(1) de convenção (contagem de planos) **declarados** acima; o conteúdo
registrado são (a) os expoentes, (b) a constância do número puro na varredura,
(c) o split E/B reportado e cruzado com LIV_VECTOR (artefato de regulador).
λ_p é livre (= K da DEV, W4); todo número puro é **condicionado a λ_p declarado
= 1** — calculável, não ajustável.

**Hipótese herdada (pré-registrada):** PE3 (proxy de rede 3D, w=ρ) deu
m_A ∝ √ρ. A tradução dimensionalmente honesta para unidades causais naturais
(única escala: ρ^{1/4}) é **s_m = +1/2** em m²_iso·λ_p ∝ ρ^{s_m}. O número puro
candidato: P ≡ m²_iso·λ_p·ρ^{−1/2} (e P_E, P_B por canal) — primeira medição,
sem valor previsto (reportado como o b≈0.85 de CR1b).

**Critérios de morte (pré-registrados):**
```
CR4 (herança) morre se: |s_m − 0.5| > 3σ do ajuste → o proxy PE3 não sobrevive
              no substrato causal; reportar como morte da entrada herdada e
              registrar o expoente medido + constante pura correspondente.
CR4 (tabela) só fecha se: alguma combinação m²·λ_p·ρ^{−s} (s medido) for
              constante na varredura com CV < 20%; senão "não constante" é o
              veredito.
Verificação de regulador: uma densidade re-medida em caixa menor (E=2.56);
dependência forte de caixa nos números puros → reportar como IR-regulado
(mesmo status do H² de CR3), não esconder.
```

## Parâmetros (fixados antes de rodar)

```
Caixa 3+1D: extent E=3.2 (todas as coords), margem de bulk 0.8 (frac 0.25),
cap H=0.75 (< margem → cone inteiro na caixa). ρ ∈ {16, 27, 45, 75}
(ρ(π/3)H⁴ = 5.3 … 24.9 ✓), 8 sementes/ρ, mesmas sprinklings para CR3 e CR4.
Caixa de verificação: E=2.56, margem 0.64, H=0.60, ρ=45, 8 sementes.
```

## Tarefas

```
CR3: u-colapso Exp(1) + mediana + expoente + constante pura → CR3_x0_constant.{py,md,json,png}
CR4: momentos C2/Π na mesma sprinkling, expoentes, números puros, split E/B,
     verificação de caixa → CR4_ma_constant.{py,md,json,png}
```

## Honestidade pré-declarada

- X₀ e m_A em unidades FÍSICAS seguem não derivados (inalterado desde D3D/e11);
  o que se deriva/mede são constantes do substrato condicionadas a reguladores
  declarados (H, λ_p) — calculáveis, não ajustáveis.
- O split E/B do setor de plaquetas cru é o conhecido artefato de
  regulador/expansão (LIV_VECTOR); reportado por canal, não escondido.
- Se a herança PE3 morrer, a tabela CR2 será corrigida (não maquiada): a
  entrada "m_A∝√ρ" passa a "expoente causal medido = s_m".

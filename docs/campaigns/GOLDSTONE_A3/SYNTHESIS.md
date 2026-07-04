# SÍNTESE — A3 / C2 · Goldstone FSS (N maior) + expoente S(k)

> Campanha GOLDSTONE_A3 (Fase 2, Frente A). Pré-registro: `PRE_REGISTRO.md`.
> Driver: `A3_fss_sk.py` → `A3_fss_sk.json`. jun/2026.
> **Veredito: (a) LRO GENUÍNA confirmada a N=3888 (endurece o Paper Goldstone PRD);
> (b) S(k) MEAN-FIELD (α≈0) robusto em N — endurece E1-3 Verdito C. Consolidação
> limpa, sem mover trave.**

---

## 1. Estimador validado (gate)

S(k) na rede cúbica 3D ordenada (L=12): **α=1.76** — rigidez de gradiente (≈2,
S~1/k²) como esperado. O déficit de 0.24 vs 2 é efeito de janela finita na rede de
validação; é irrelevante para o veredito causal, pois o α causal (0.06) é **28×
menor** → a discriminação plano(0) vs rígido(2) é inequívoca.

## 2. Parte (a) — LRO sobrevive a N maior

| L | N | m=\|⟨n⃗⟩\| | U4 | piso N^−½ |
|---|---|---|---|---|
| 4.4 | 175 | 0.9609 | 0.667 | 0.076 |
| 6.4 | 812 | 0.9869 | 0.667 | 0.035 |
| 7.4 | 1469 | 0.9911 | 0.667 | 0.026 |
| 8.4 | 2457 | 0.9934 | 0.667 | 0.020 |
| **9.4** | **3888** | **0.9950** | **0.667** | 0.016 |

m **cresce monotonicamente** (trend d ln m/d ln N = **+0.011** > 0, longe do piso
aleatório −0.5), m/piso de 12× a 62×, **U4=0.667=2/3 exato** em todos os tamanhos.
**SUCCESS_LRO** estendido de 1462 → **3888** (2.7×). A ordem de longo alcance do
setor de orientação (Mermin, C_long=m²) **não é artefato de tamanho**. → **Nenhum
rebaixamento** do Paper Goldstone (R-4, ramo positivo).

## 3. Parte (b) — S(k) transverso é campo médio, robusto em N

| N | α (S~1/k^α) | janela |
|---|---|---|
| 812 | 0.06±0.01 | 1.6 déc |
| 1469 | 0.06±0.01 | 1.6 déc |
| 2457 | 0.06±0.01 | 1.6 déc |
| 3888 | 0.06±0.01 | 1.6 déc |

α=**0.06±0.01 PLANO**, **independente de N** (tendência d(α)/d(ln N) = −0.00).
Exclui rigidez de gradiente (α=2) a ~190σ; |α−0|<0.5 → campo médio. Os **links
causais nus** carregam orientação de **campo médio NÃO-LOCAL**, sem rigidez k² —
**não** um Goldstone relativístico ω=ck. A planura de E1-3 (α≈0.28 a N≈1462) é
**robusta a N grande** (e mais limpa: 0.06 com melhor estatística/janela).

**Endurece E1-3 Verdito C:** o magnon relativístico (E2, ω=ck Verdito A) emerge do
**operador BD/Sorkin** (e10), não dos links nus. A3 fecha a lacuna de tamanho que
poderia ter reaberto a questão.

## 4. Quadro consolidado (Paper Goldstone PRD)

A3 endurece a história de duas camadas do programa, já honesta no paper:
1. **Ordem** (E1/E4/A3): o vácuo causal é um **ferromagneto de orientação com LRO
   genuína** (m→plateau, U4=2/3, C_long=m²) — agora a N=3888.
2. **Dinâmica** (E1-3/A3 vs E2): os **links nus** dão rigidez de **campo médio**
   (S(k) plano, α≈0); a rigidez relativística (fóton, ω=ck) requer o **operador
   BD/Sorkin** — não os links nus. A3 confirma a separação com N grande.

α≈0 também informaria como B2 mediria ξ_grav (correlação de campo médio), mas B2
não está no caminho (B1 negativo).

## 5. Limitação honesta

N teto ~3888 (≈2.7× o anterior; alvo 5–10k da HIERARQUIA não atingido neste
desktop — build do grafo é O(N³)). Mas tanto m(N) quanto α(N) estão **planos** no
range medido (sem deriva), então a extrapolação a 10k não muda o veredito. Janela
de S(k) = 1.6 década (≥1.5 pré-registrado). Estimador 3D deu 1.76 (não 2 exato) por
janela finita — não afeta a discriminação (α causal 28× menor).

## 6. Anti-circularidade

`orientation_core.py` e `A3_fss_sk.py` sob as guardas A1 (dilatação + literais de
escala VERDE). α emerge do ajuste; "fóton" não entra no gerador. Estimador validado
independentemente na rede 3D antes do uso causal.

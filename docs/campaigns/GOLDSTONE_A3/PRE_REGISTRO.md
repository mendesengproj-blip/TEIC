# PRE-REGISTRO — A3 / C2 · Goldstone FSS (N maior) + expoente S(k)~1/k^α

> Campanha de organização TEIC (Fase 2), Frente A (CONSOLIDAR), item A3 = C2.
> Gate A1 já VERDE (orientation_core sob a guarda). Fontes:
> `HIERARQUIA_EXPERIMENTOS.md` §C2, E1-3 (`.../orientation/E1_3_magnon.md`), E4-0
> (`.../e4/E4_0_fss.py`). Pré-registro antes de rodar.

---

## 1. Pergunta

(a) Os achados do setor de orientação (LRO, U4=2/3, m(N) não-decai) sobrevivem a
N maior (alvo 5–10k; teto prático ~4–5k neste desktop)?
(b) O **structure factor transverso S(k) ~ 1/k^α** dos *links causais nus*
seleciona **campo médio** (α≈0, plano, não-local — sem rigidez de gradiente) ou
**rigidez de gradiente / tipo-relativístico** (α≈2 ⇒ S~1/k² ⇒ ω~k)?

Contexto: E1-3 mediu S(k) PLANO (α≈0.28) a N≈1462 → campo médio (Verdito C). A3
testa se essa planura é **robusta a N** (endurece o Paper Goldstone PRD) ou era
artefato de tamanho.

## 2. Convenção e âncora (E1-3, validada)

S(k) = ⟨|Σ_i s⊥,i e^{−i k·x_i}|²⟩ / N, transverso = direções de Goldstone. Ajuste
**S(k) ~ A/k^α** em log-log. **Estimador VALIDADO** na rede cúbica 3D ordenada,
onde a rigidez de gradiente garante **α≈2** (S~1/k²) — gate obrigatório antes de
medir o vácuo causal. (NB: a redação "α=−1" da HIERARQUIA é frouxa; a âncora física
medida e validada é α≈2 para rigidez relativística, α≈0 para campo médio.)

## 3. Critério de sucesso / morte

**Parte (a) — LRO:**
- SUCESSO: m(N) permanece ≫ piso aleatório (N^{−1/2}), d ln m/d ln N > −0.15, e
  U4 ≳ 0.6 (→2/3) até o maior N. (Já SUCCESS_LRO até 1462; A3 estende.)
- MORTE: m(N) passa a rastrear o piso (d ln m/d ln N < −0.35) e U4→0 → LRO era
  artefato → **rebaixar LRO no Paper Goldstone** (R-4).

**Parte (b) — S(k) α (janela de k ≥ 1.5 década):**
- α robusto e **≈0** (barra exclui rigidez, |α−0|<3σ e claramente <1): **campo
  médio confirmado** a N grande → endurece o escopo honesto do Paper (links nus =
  campo médio; rigidez relativística exige operador BD/Sorkin, E2/e10). Verdito C
  hardened.
- α **sobe com N rumo a ≈2** (|α−2|<3σ no maior N): rigidez de gradiente emerge →
  reabre a possibilidade de magnon relativístico nos links nus (improvável dado E1-3).
- INDECIDÍVEL: α fica preso entre 0 e 2 sem barra que exclua, mesmo com janela
  ampla → fronteira de método (reportar como tal; não mover trave).

α de S(k) também define como B2 mediria ξ_grav (R-4) — registrado, mas B2 não está
no caminho (B1 negativo).

## 4. Protocolo

1. **Gate do estimador**: S(k) na rede cúbica 3D ordenada (J grande) → confirmar
   α≈2 antes de tudo.
2. **FSS LRO**: O(3) Metropolis nos links causais (motor E4-0 sem modificação),
   J=2.0, ρ=0.5, L crescente até N~4–5k; m(N), U4(N), piso; menos seeds no topo.
3. **S(k) α por N**: medir S(k) transverso em ≥2 tamanhos (incl. o maior), janela
   de k ≥1.5 década, ajuste α com bootstrap sobre seeds; reportar α(N) e tendência.
4. Veredito por §3. Só grafo + energia cos/dot; nenhuma fórmula relativística.

## 5. Anti-circularidade

`orientation_core.py` (gerador) **sob a guarda A1** (`results/vacuum_structure/**`
varrido; verificado). Sem T_c, sem dispersão, sem literal de escala; α emerge do
ajuste. Palavra "fóton" não entra no gerador (só na síntese, COMPARISON ONLY).

## 6. Entregáveis

`A3_fss_sk.py`, `A3_fss_sk.json`, `SYNTHESIS.md`; atualização do RESEARCH_MAP
(linha Goldstone/E1-3) e nota de impacto no Paper Goldstone PRD.

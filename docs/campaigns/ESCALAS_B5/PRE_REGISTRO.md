# PRE-REGISTRO — B5 · Por que η e ℏ "não pinam" (teorema vs artefato de tamanho)

> Campanha de organização TEIC (Fase 2), Frente B (ESCALAS), item B5 —
> **promovido ao topo da Frente B** pelo R-1 (B1 deu morte negativa). Fontes:
> `HIERARQUIA_EXPERIMENTOS.md` §B5, FD1 (`docs/campaigns/COLAPSO_SR_TEIC/`).
> Pré-registro antes de qualquer nova corrida de FD1 (disciplina).

---

## 1. Pergunta

A morte de η no valor genérico (FD1: k_c≈1, limiar de percolação) e a não-fixação
de ℏ são **fundamentais** (teorema a provar) ou **artefato de tamanho** (recalcular
com N maior)? FD1 mediu (N=300): k_c=1.2 (d=2), 0.6 (d=4); η=(k_c−1)²≈0.04, 0.16;
veredito MORTE — disparado pela **não-robustez** (k_c move >20% sob ±10% densidade),
não por k_c≡1.

Relação SR (pós-dição): `p_c·N = 1+√η` ⇒ **k_c = 1+√η** ⇒ **η = (k_c−1)²**.

## 2. Handle analítico (Molloy–Reed)

Para percolação de ligação num grafo com distribuição de grau {p_k}, o **grau médio
retido crítico** é
    z_c = ⟨k⟩² / (⟨k²⟩ − ⟨k⟩) = 1 / ((1+CV²) − 1/⟨k⟩)   →  1/(1+CV²)   (⟨k⟩→∞),
onde CV = desvio/média do grau. **z_c=1 sse Poisson/árvore (CV→0)**. O grafo causal
é denso (⟨k_full⟩~N/2) com **CV de grau geométrico** (nº de ancestrais depende da
posição no diamante) — medido **estável ~0.33** em N=300..1000, NÃO desaparece.
Logo z_c→1/(1+0.33²)≈0.90 (estimativa árvore); o **clustering/transitividade** do
DAG causal eleva o limiar real acima disso. A invariância/limite tem de **emergir
do scan** (anti-circ): CV e z_c medidos por N, não impostos.

## 3. Critério de sucesso / morte (FSS, congelado)

- **(a) η PINA (reabre FD1):** k_c(N) converge para um valor **estável E
  significativamente ≠1** (barra de bootstrap exclui 1) E **universal** (mesmo em
  d=2 e d=4) → há um η_emergente robusto.
- **(b) MORTE FUNDAMENTAL (porta fechada, teorema/mecanismo):** k_c é **forçado
  pela estatística de grau** do grafo causal — z_c (Molloy–Reed) + correção de
  clustering prevê k_c medido, e o limite é um **O(1) calculável** (não um número
  universal pinável). Em particular, k_c **depende da dimensão** (d=2≠d=4) ⇒ não há
  η universal a pinar; reproduz a relação de consistência da SR sem derivar um η.
- **(c) INDETERMINADO:** k_c≈1 sem se provar que é forçado E sem estabilizar ≠1 →
  reportar como tal; **não declarar teorema sem prova**.

## 4. Protocolo

1. FSS de k_c(N): N ∈ {200, 350, 600, 1000, 1600} (estendido se o tempo permitir),
   d ∈ {2,4}, grade k fina perto de 1, ≥16 seeds (menos no topo), k_c = pico de
   susceptibilidade com **interpolação parabólica** sub-grade + **bootstrap** sobre
   seeds. Ajuste k_c(N)=k_c(∞)+a·N^{−ω}.
2. Analítico por N: ⟨k⟩, ⟨k²⟩, CV do grafo causal cheio → z_c Molloy–Reed; comparar
   com k_c medido (gap = efeito de clustering).
3. Veredito por §3. Só medida sobre o grafo causal validado; nenhuma dinâmica nova.

## 5. Anti-circularidade

`sr_teic_core.py` é gerador próprio — **já sob a guarda A1** (extensão de SCAN_DIRS
cobre `docs/campaigns/**`; verificado). Sem literal de escala; k_c e η emergem do
scan.

## 6. Entregáveis

`B5_fss.py`, `B5_fss.json`, `SYNTHESIS.md`; atualização do RESEARCH_MAP (porta η).

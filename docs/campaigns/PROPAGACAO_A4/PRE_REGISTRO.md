# PRE-REGISTRO — A4 / C4 · Propagação dinâmica estável dos Goldstones (BD smeared)

> Campanha de organização TEIC (Fase 2), Frente A (CONSOLIDAR), item A4 = C4.
> **Pressão de timing:** o Paper Goldstone (PRD) está em preparação **com a ressalva
> de instabilidade numérica do operador sharp**. A4 tem de **terminar antes da
> submissão**: se passar, a ressalva some; se falhar, a ressalva permanece mas
> documentada com honestidade e o paper é submetido com ela explícita.
> Gate A1 já VERDE. Fontes: §C4, E2 (`results/vacuum_structure/orientation/e2/`),
> c5_core (operador BD smeared simétrico), e2_core (`bd_propagate` retardado).

---

## 1. Pergunta

A relação ω=ck do setor de orientação aparece por **propagação direta** de um
pacote — medida **na evolução**, não no **símbolo** do operador — usando o operador
BD smeared? Fecha a brecha **[FRACO]** de E2: "ω=ck é do símbolo; a propagação
direta (`bd_propagate`) é instável".

**Diagnóstico herdado:** a marcha retardada `bd_propagate` (`φ(x)=2ε Σ w(m) φ(y)`,
só passado) é **não-normal/unilateral** → instável; por isso E2 recuou ao símbolo
λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩ (estável, mas simbólico). O candidato a evolução **estável**
é o operador BD smeared **simétrico** (c5_core: M = w(m) sobre R=A|Aᵀ, auto-adjunto,
espectro real), não a marcha retardada.

## 2. Critério de sucesso (congelado)

Um pacote inicial localizado propaga com:
- **dispersão linear ω=ck medida na EVOLUÇÃO** (oscilação/propagação dos modos no
  tempo, não o símbolo), com **c dentro de ~5% de 1** (unidades de rede);
- **estável** (sem blow-up; max|φ| limitado) por **≥ várias travessias** do domínio;
- em **≥2 tamanhos**;
- usando o operador **smeared** (não o sharp).
→ E2 promovido **[FRACO]→[SÓLIDO]**; ressalva removida do Paper Goldstone/Photon-Arc.

## 3. Critério de morte (congelado)

A evolução é **instável** (cresce sem limite) **OU** difusiva (ω∝k², pacote espalha
∝√t) mesmo com smearing → o "Goldstone/fóton propagante" permanece **só simbólico**;
**E2 fica [FRACO] permanente** e o Paper mantém a ressalva (submetido com ela
explícita). Caracterizar **por quê** (operador indefinido/não-normal; modos
acima-do-cone crescem) — isso é o resultado de 1ª classe.

## 4. Protocolo

1. **Gate de máquina (lattice regular):** leapfrog ∂_t²φ=−Lφ com Laplaciano **sharp**
   na cadeia 1D periódica → ω=ck, c=1, estável (resultado de livro). Valida o
   integrador + o estimador de ω(k) **antes** de tocar no smeared/causet.
2. **Smeared simétrico (lattice):** mesmo leapfrog com o operador **smeared**
   (pesos BD decaindo, simétrico) → espectro (PSD?), estabilidade, ω(k) da evolução.
   Testa se o smearing **preserva** ω=ck estável.
3. **Causal set:** operador BD smeared **simétrico** (c5) numa aspersão real:
   (a) espectro — **PSD** (estável) ou **indefinido** (instável, raiz do [FRACO])?
   (b) evolução de um pacote — balístico (largura∝t, ω=ck) vs difusivo (∝√t) vs
   blow-up; medir c, estabilidade, ≥2 tamanhos.
   (c) demonstrar a instabilidade da marcha retardada `bd_propagate` (quantitativa).
4. Veredito por §2/§3. Só grafo + operador BD; **nenhum ω=ck inserido** (ω medido da
   evolução; c nunca input).

## 5. Anti-circularidade (CRÍTICO)

Propagação direta é **onde "injetar e^{ikL}" seria a recaída clássica**. Sob a guarda
A1: nenhum literal imaginário cru no gerador; se comparar com QM/símbolo, usar bloco
`COMPARISON ONLY` rotulado. ω emerge da evolução medida; c sai do ajuste, nunca
inserido. Pacote inicial é real (cos/gaussiana), sem fase complexa injetada.

## 6. Entregáveis

`a4_bd_propagation.py`, `a4_bd_propagation.json`, `SYNTHESIS.md`; atualização do
RESEARCH_MAP (linha E2) e **nota de impacto no Paper Goldstone PRD** (ressalva
removida ou mantida-documentada) — **antes da submissão**.

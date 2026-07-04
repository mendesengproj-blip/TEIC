# SÍNTESE — Percolação de longo alcance sobre a ordem causal (3ª família)

**Data:** 2026-06-29 · **Diretório:** `docs/campaigns/PERCOLACAO_LONGO_ALCANCE/`
**Natureza:** gatilho cinemático barato (⟨z⟩ + C4), sem ferromagneto, sem ξ.
**VEREDITO: `SEM_JANELA`** (death limpa, em ambas as barreiras simultaneamente).

---

## 1. O que foi testado

Sobre o **mesmo sprinkling de Poisson** (Lorentz preservado por construção; `causal_core.sprinkle_box`/`causal_matrix` VERBATIM), substituiu-se a regra "todo par causal conecta" por **percolação de longo alcance** sobre a ordem causal:

```
p(Δτ_ij) = min(1, (Δτ_ij / Δτ₀)^(−σ)) ,   Δτ₀ = ρ^(−1/d)  [External]
```

`Δτ_ij` = tempo-próprio invariante; `σ` = único parâmetro novo, adimensional, varrido em **11 valores** {0.5 … 8.0}; ladder N {500…3000} (2+1D, caixa larga-baixa T=1, L=3, geometria `[External]`). Estimadores ⟨z⟩ e C4 = `rs_clustering.clustering_metrics` **importado VERBATIM** do Gatilho 2.

**Motivação (literatura plana):** o critério Fisher–Ma–Nickel/Sak prevê uma janela intermediária de σ (≈ d) com classe de universalidade própria não-mean-field. A pergunta foi se essa janela sobrevive na versão causal/Lorentziana.

---

## 2. Gate de validação — VERDE (6/6)

| Item | Resultado |
|---|---|
| σ=6 esparso z claramente < σ=0.5 denso | z 11.1 vs 28.4 (ratio 0.39) ✓ |
| σ=0.5 conecta a maioria dos pares causais | frac 0.80 ✓ |
| cross-check ⟨z⟩ = 2·E/N (estimador VERBATIM) | bit-idêntico (1e-9) ✓ |
| C4 não-trivial (difere do controle aleatório) | C4_fam 0.062 ≠ C4_rnd 0.088 ✓ |
| **Invariância de Lorentz: arestas BIT-idênticas sob boost η=0.8** | simdif=0, ⟨z⟩/C4 idênticos a 1e-9 ✓ |

A invariância (Seção 2 do charter) passa **por construção e verificada**: a regra depende só de `Δτ` (invariante) e de um sorteio por par chaveado pela **identidade dos nós** (preservada sob boost). Re-derivar o grafo de coordenadas *boosted* dá o **mesmo grafo**. ⇒ a opção "TROCA COM LORENTZ" do pré-registro **não se realiza**: não há regularização dependente de referencial; a janela não existe nem mesmo às custas da invariância.

---

## 3. Resultado central (`longrange.json`, `verdict_final.json`, `control_c4.json`)

**Barreira 1 — coordenação ⟨z⟩(N,σ): NUNCA satura.** Em TODOS os 11 valores de σ, ⟨z⟩ cresce com N; o expoente local relativo `(d⟨z⟩/dlnN)/z_top` vai de **+0.68** (σ=0.5) a **+0.39** (σ=8) — sempre ≫ o limiar de saturação 0.05. A divergência de coordenação **Lorentz-protegida** (motor isolado na ESCALA_XI) **sobrevive intacta** à modificação de longo alcance.

**Barreira 2 — clustering C4(σ): ABAIXO do controle aleatório em 0/11 σ.** O controle de triviality (mesmo pool de pares causais, mesma contagem de arestas, sorteio uniforme) tem C4 **MAIOR** que a família em todos os σ (razão 0.70→0.93, subindo rumo a 1 conforme σ→esparso). Ou seja, a estrutura de decaimento por Δτ **suprime** os laços em vez de criá-los; o C4 da família fica entre o CSG (0.019) e o Poisson MF (0.029) no extremo esparso, e **nunca** acima da rede dim-finita.

**Sem ponto de sobreposição (o trade-off de sempre, agora contínuo):** o conjunto {σ : ⟨z⟩ satura} = ∅; o conjunto {σ : C4 não-trivial (>controle)} = ∅. A região de C4 mais alto (σ pequeno) é exatamente onde ⟨z⟩ diverge mais forte; a região de menor ⟨z⟩ (σ grande) é onde C4 colapsa ao controle. **JANELA = ∅.**

| σ | ⟨z⟩ (rel. slope) | C4 (razão/controle) |
|----|---|---|
| 0.5 | 53.5 (+0.68 **div**) | 0.138 (0.82 <ctrl) |
| 2.0 | 34.9 (+0.54 **div**) | 0.048 (0.71 <ctrl) |
| 3.0 | 30.2 (+0.45 **div**) | 0.033 (0.77 <ctrl) |
| 6.0 | 21.0 (+0.39 **div**) | 0.027 (0.90 <ctrl) |
| 8.0 | 19.2 (+0.39 **div**) | 0.025 (0.93 <ctrl) |

---

## 4. Mecanismo (por que morre, e por que era previsível)

A regra de longo alcance é, ela própria, **Lorentz-invariante** (limiar sobre o invariante Δτ). Por isso **não consegue cortar os atalhos de boost** que são a causa-raiz do mean-field do sprinkling de Poisson: um par com grande separação de coordenadas mas pequeno Δτ (gerado por boost) tem **alto** `p` e conecta — exatamente o "atalho" que se queria suprimir. Suprimir esses atalhos exigiria limiar sobre uma quantidade **dependente de referencial** (coordenada espacial, coordenação k-NN) — o que a ESCALA_XI já provou que **viola Lorentz** (barreira dupla: [[escala-xi-correlation-divergence]]). 

⇒ A 3ª família ataca o decaimento *na variável errada*: decair em Δτ preserva a não-localidade que se queria matar. O resultado confirma, agora de forma **contínua em σ** e **com a invariância explicitamente verificada**, o teorema operacional das campanhas anteriores: **o mean-field é estrutural ao sprinkling Lorentziano de Poisson; nenhuma regra de conexão Lorentz-invariante sobre ele escapa das duas barreiras.**

---

## 5. Ressalvas honestas

- **Faixa dinâmica modesta:** numa caixa, `Δτ_max/Δτ₀ ~ T·ρ^(1/d)` é pequena (~5–10), então o limite esparso é **suave** (σ=8 ainda retém ~13% dos pares causais e ⟨z⟩ ainda cresce com N). Estendeu-se o scan até σ=8 para ancorá-lo; o expoente local **decresce** monotonicamente com σ (de +0.68 a +0.39), confirmando a direção, mas **não chega a 0** no orçamento. Isto **não muda o veredito**: mesmo no σ mais esparso medido, ⟨z⟩ diverge e C4 está abaixo do controle. Uma faixa dinâmica maior exigiria N ≫ 10⁴ (custo do square-clustering pure-Python ~N·z²) sem nenhuma indicação de cruzamento.
- **Caps de N por σ** (denso capado a N≤1500) são de **custo**, não de física: cada σ mantém ≥3 pontos de ladder para o expoente local, e a faixa decisiva (σ≥2.5) roda o ladder completo até N=3000.
- **C4 < controle é robusto:** medido no MESMO N (família e controle no mesmo top-N por σ), 0/11 acima.

---

## 6. Posição na fila de substratos

5ª via testada por gatilho cinemático barato. Resultado consolida o padrão:

| Família | Barreira 1 (⟨z⟩) | Barreira 2 (C4) | Status |
|---|---|---|---|
| Poisson | FALHA (diverge) | — | MORTA |
| CSG | PASSA | FALHA (sub-MF, árvore) | ENCERRADA |
| Tipo-CDT 2D | passa (trivial, Euler) | PASSA (rede 2D) | ARMADO fraco |
| CDT 3D completo | z alto | passa | A=reproduz / B=não-resolvido |
| **Longo alcance** | **FALHA (diverge ∀σ)** | **FALHA (<controle ∀σ)** | **SEM JANELA (death dupla)** |

**Única família a falhar as DUAS barreiras simultaneamente em todo o parâmetro** — e a única em que a invariância de Lorentz foi **verificada explicitamente** como a causa da falha (não removível por regularização sem violar Lorentz).

---

## 7. Funil (o que NÃO foi feito, por disciplina)

Não se rodou ferromagneto nem ξ — gatilho cinemático puro. Como o veredito é SEM JANELA, **nenhuma campanha completa sobre esta família se justifica** (mesma trava de funil dos Gatilhos 1–3). Linha **fechada**.

## Arquivos
`PRE_REGISTRO.md` (critérios travados antes de rodar) · `longrange_percolation.py` (gerador+gate+scan+verdito) · `focused_control.py` (controle de triviality, criterio 5) · `finalize.py` (veredito final completo) · `validation_gate.json` · `longrange.json` · `control_c4.json` · `verdict_final.json` · `longrange.png` (⟨z⟩(σ) e C4(σ)).

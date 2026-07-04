# results/vacuum_structure/orientation/e3b — campanha E3b_CAUSAL_DEFECT (jun/2026)

> Charter: `E3b_CAUSAL_DEFECT.md` (raiz). Testa o **mecanismo 3** deixado em aberto
> por E3: a rigidez topológica do **cone causal 3+1D**. Pergunta: o hedgehog de n⃗
> é estável na rede causal real (não na rede cúbica espacial de E3)?
> **NÃO modifica nenhuma campanha anterior.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **E3b-V** | substrato reproduz SR? B em Poisson? mais local que E1? | **PASS** — cadeia corr 0.9991 com √(1−β²); Delaunay B=+1/−1/0; ⟨grau⟩=23 < 46; 0 violações causais | `E3bV_gate.{py,md,json,png}` |
| **E3b-1** | B=1 sobrevive à evolução causal (Protocolo A)? | **SIM** — 100% (20 sementes, todas as folhas); r_eff≈2.7 estável; morte não acionada | `E3b_1_hedgehog.{py,md,json,png}` |
| **E3b-2** | causal preserva B melhor que MC acausal? | **SIM mas** — causal 100% vs acausal 0% (vida >1000 vs 200 sw); **controle fatia FUTURA também 100%** ⇒ pinçamento de contorno, não seta do tempo | `E3b_2_evolution.{py,md,json,png}` |
| **E3b-3** | Derrick causal tem mínimo interior? | **NÃO** — λ*=0.40 (encolhe), 3 escalas; E_temporal <1% de E_total, não compensa | `E3b_3_derrick_causal.{py,md,json,png}` |
| **E3b-4** | E²=(mc²)²+(pc)²? | **NÃO RODADO** — só sob Veredito A (guard verifica E3b-1 ∧ E3b-3) | `E3b_4_emc2.{py,json}` |
| **E3b-5** | síntese | **B — SUCESSO PARCIAL** | `E3b_5_synthesis.md` |

Motor: `e3b_core.py` (sprinkling de Poisson 3+1D; substrato de **links causais** /
Hasse `L = C & ~(C@C)`, ⟨grau⟩≈23; hedgehog dos eventos pelas coordenadas
espaciais; carga B = grau de ângulo sólido de Berg–Lüscher adaptado a **tetraedros
de Delaunay** — faces internas cancelam, sobra o grau da fronteira; evolução causal
determinística Protocolo A; Metropolis colorido vetorizado com máscara congelada
Protocolo B; Derrick causal com split espacial/temporal). Self-test: `python e3b_core.py`.

## Resultado de uma linha

**A rigidez do cone causal existe mas é insuficiente para matéria estável.** O
hedgehog B=1 é preservado pela evolução causal (E3b-1) e o Monte Carlo causal com
o passado congelado supera a relaxação livre por >5× (E3b-2) — mas o controle de
fatia **futura** preserva igual, então é **pinçamento de contorno propagado pelos
links**, não a seta do tempo; e **não há mínimo de Derrick causal** (E3b-3,
E_temporal <1%). Logo E=mc² não roda (E3b-4). **Matéria estável ainda exige
SU(2)+Skyrme — Paper II permanece.** Refina E3: o cone causal prolonga a vida do
defeito mas não o estabiliza intrinsecamente. Mecanismo 3 testado e descartado.

## Notas numéricas para reuso

- **B em Poisson via Delaunay:** cada tetraedro é uma S² (4 triângulos orientados
  para FORA do apex); faces compartilhadas por tetraedros adjacentes cancelam
  (orientação oposta), restando o grau na fronteira do convex hull. Retorna
  +1/−1/0 exato. Sem orientar as faces para fora, o sinal embaralha.
- **⟨grau⟩ do grafo de Hasse depende da GEOMETRIA da caixa** (diverge log com a
  extensão temporal). ρ=1.5, T=3.0, L=4.0 → ⟨grau⟩≈23 (metade de E1); T grande
  sobe o grau (T=6→⟨grau⟩≈90). Escolher caixa quase-cúbica para ficar local.
- **Cooling antes de medir B sob MC:** igual a E3 — alinhar a TODOS os vizinhos
  (~10–12 passes Jacobi) remove rugas UV térmicas sem mover o winding inteiro.
- **MC vetorizado por cor:** reusa a coloração de `orientation_core.Graph`; nós
  congelados nunca são propostos mas alimentam o campo de vizinhos (Dirichlet).
  ~100× mais rápido que o loop por evento.
- **Controle decisivo (anti-auto-engano):** congelar fatia passada *e* futura.
  Ambas preservam B ⇒ a proteção é contorno, não causalidade temporal. Sem esse
  controle, seria fácil (e errado) declarar Veredito A.
- **Derrick causal:** um r̂ puro é invariante de escala; usar **core finito**
  (=1.5) para ter alavanca de dilatação. E_temporal (links com dx≈0) é ~const(λ)
  porque eventos co-localizados no espaço têm o mesmo n⃗ de hedgehog.

## Regras (as de sempre)

Kill criterion pré-registrado ("B(t)→0 sob Protocolo A = Veredito C", pontuado
como escrito — B não colapsa ⇒ não é C; mas sem mínimo de Derrick ⇒ não é A ⇒
Veredito B); gate de engenharia (E3b-V) antes de qualquer medida de defeito;
negativos/limitações reportados (a preservação de B é contorno, não seta do tempo;
sem contra-termo temporal); anti-circularidade (B = ângulo sólido de Delaunay; E =
funcional de ligações; c nunca no gerador — seria o 0.98 de E2, só sob Veredito A;
"massa"/"matéria"/"E=mc²" só em COMPARISON; 20 sementes fixas). Verificação tripla
exigida para Veredito A — não atingida, portanto não afirmada.

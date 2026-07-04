# results/vacuum_structure/orientation — campanha E1_ORIENTATION (jun/2026)

> Charter: `E1_ORIENTATION.md` (raiz). Primeira campanha executada de
> `NIVEL4_ORIENTATION.md` (entrada FN1). Pergunta central: o vácuo da rede
> causal tem ordem de longo alcance de orientação — é um ferromagneto causal?
> **NÃO modifica nenhuma campanha anterior.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **E1-V** | o motor O(3)/XY reproduz 1D/2D/3D conhecidos? | **PASS** — sem ordem 1D, KT 2D (η≈0.32), LRO 3D com C(∞)=m² (<1.5%); ξ do XY 1D vs matriz de transferência <16% | `E1V_gate.{py,md,json,png}` |
| **E1-1** | C(r) tem ordem de longo alcance na rede causal? | **A — FERROMAGNETO** — exp (J<J_c) → const com C(∞)=m² (J>J_c); J_c(U(1))≈0.05, J_c(O(3))≈0.08 | `E1_1_correlations.{py,md,json,png}` |
| **E1-2** | tipo de transição e J_c? | **2ª ORDEM** — m sobe de ~1/√N, χ pica em J_c; J_c(O(3))>J_c(U(1)) | `E1_2_transition.{py,md,json,png}` |
| **E1-3** | o fóton é uma onda de orientação (ω=ck)? | **PARCIAL/NEGATIVO** — S(k) PLANA (α≈0.28): links nus = campo médio não-local, sem rigidez k²; precisa do operador BD/Sorkin (e10) | `E1_3_magnon.{py,md,json,png}` |
| **E1-4** | síntese | **A para a ordem; aberto para o fóton** | `E1_4_synthesis.md` |

Motor: `orientation_core.py` (grafos 1D/2D/3D + grafo de links causais de
Hasse; Metropolis XY/U(1) e O(3)/Heisenberg com coloração de grafo; C(r) por
distância geodésica causal = cadeia mais longa; fator de estrutura S(k);
classificador exp/potência/constante). Self-test: `python orientation_core.py`.

## Resultado de uma linha

**O vácuo da rede causal É um ferromagneto de orientação** (ordena com
transição contínua, C(∞)=m²) — a orientação lidera onde VS1 mostrou que a
densidade só obedece. **MAS** o modo de Goldstone dos links nus é não-local
(campo médio, S(k) plano), **não** um fóton relativístico ω=ck: a identificação
fóton=magnon exige restaurar a localidade via o d'Alembertiano de Sorkin/BD.

## Notas numéricas para reuso

- **Não-localidade dos causal sets:** o grafo de Hasse 4D tem ⟨grau⟩ alto
  (≈46 em tubo [0,40]×[0,3]³; ≈130 em cubo [0,10]⁴) — empurra J_c para baixo
  (J_c≪0.5, fora da faixa ingênua tipo-rede-cúbica) e torna a rigidez espacial
  campo-médio (S(k) plano). É feature física, não bug.
- **Métrica de distância:** hop satura (small-world); usar **cadeia mais longa**
  (tempo próprio causal, `longest_chain_from`) para C(r) — alcança r≈50–60.
- **Classificador C(r):** plateau-plano (C_long/C_mid>0.85, C_long>0.05) ⇒ LRO;
  senão exp vs potência por R². `C(∞)=m²` é o teste de ordem genuína
  (vale em 3D/causal; falha de propósito em 2D-XY = assinatura de Mermin–Wagner).
- **Estimador S(k):** validar sempre em rede 3D (α≈2) antes de aplicar no
  causal set; dinâmica de Metropolis é relaxacional (modelo A) e **não** decide
  ω=ck vs ω=Dk² — só a rigidez espacial.

## Regras (as de sempre)

Kill criteria pré-registrados no charter antes de rodar; gate de engenharia
antes de medição física; negativos reportados como vereditos válidos;
anti-circularidade (sem números complexos nos geradores, sem constantes-alvo
inseridas); sementes fixas.

# results/vacuum_structure/orientation/e2 — campanha E2_MAGNON_BD (jun/2026)

> Charter: `E2_MAGNON_BD.md` (raiz). Segunda campanha executada de
> `NIVEL4_ORIENTATION.md` (entrada FN2). Continua E1. Pergunta central: quando a
> flutuação de orientação δn⃗ propaga via o d'Alembertiano BD-suavizado, ω=ck?
> **NÃO modifica nenhuma campanha anterior.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **E2-V** | motor de análise + propagação BD validados? | **PASS** — GATE A recupera ck/massive/diffusive; B1 mostra recursão instável (\|φ\|→1068); B2 símbolo BD dá crista linear c≈1 | `E2V_gate.{py,md,json,png}` |
| **E2-1** | δn⃗ propaga via BD com frente ≈c? | **SIM** — via o símbolo λ(k,ω); v=ω*/k≈1 sem tendência (20 sementes, 10/10 k) | `E2_1_propagation.{py,md,json,png}` |
| **E2-2** | dispersão é ck, massiva ou difusiva? | **ck (massless)** — c=0.98, desvio 4.5%, χ²/N=0.46; difusivo rejeitado (χ²/N=11.9); m²<0 (sem massa) | `E2_2_dispersion.{py,md,json,png}` |
| **E2-3** | modos transversais dominam? | **SIM** — transversal/longitudinal=183:1; 2 Goldstones=2 polarizações (caveat: transversalidade interna, não de gauge a k⃗) | `E2_3_polarization.{py,md,json,png}` |
| **E2-4** | síntese | **A — FÓTON = MAGNON BD-SMEARED** | `E2_4_synthesis.md` |

Motor: `e2_core.py` (sprinkling 1+1D + ordem causal de `src/causal_core.py`;
peso suave de Sorkin/BD reusado de `experiments/e10_sorkin_dalembertian.py`;
recursão retardada — instável, só para demonstração; **símbolo** λ(k,ω) do
operador via regressão de Rayleigh sobre ondas de prova cos reais; cruzamento de
zero = dispersão; ajuste de 3 modelos por tendência de v(k) + χ²/AIC). Self-test:
`python e2_core.py`.

## Resultado de uma linha

**O fóton é um magnon BD-smeared do ferromagneto causal.** A flutuação de
orientação δn⃗ do vácuo ordenado de E1, propagada pelo d'Alembertiano suavizado
de Sorkin/Benincasa–Dowker (o conserto que E1-3 indicou), tem dispersão **ω=ck**
(c=0.98≈cone de luz, emergente; sem massa; difusivo rejeitado), e os modos suaves
são os **2 Goldstones transversais** (= 2 polarizações). E1 deu A para a ordem e
deixou o fóton aberto; **E2 fecha o fóton na dispersão.**

## Notas numéricas para reuso

- **Recursão BD direta = MORTA** (como a regra síncrona de e10): o inverso
  explícito de B_ε amplifica a variância pontual de BD; o modo-zero constante
  explode (\|φ\|~1000). Usar sempre o **símbolo** λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩ (estável).
- **Sinal do símbolo:** medido B_ε ≈ −K·(k²−ω²) (oposto às âncoras assumidas em
  e10, que só fixou *ordenamento*). A dispersão = cruzamento de zero **independe**
  dessa normalização; `dispersion_from_symbol` detecta o sinal espacial e cruza.
- **Discriminador de modelo robusto:** a corrida AIC/χ² é frágil (depende do σ);
  usar a **tendência de v(k)=ω/k** (plana=ck / sobe=Dk² / desce=massiva, limiar
  ±0.15) — independente de escala e de ruído. Calibrado em E2-V GATE A.
- **Resolução de DFT:** modos sintéticos têm de ser espaçados ≥ 2π/(2X) senão
  vazam e inclinam picos de alto-k (fazem massless parecer massivo). Bug do teste
  encontrado e corrigido em E2-V.
- **Tamanho-finito:** caixa pequena (X=16) eleva o ponto de menor k; caixa maior
  (X=18) limpa. Memória de causal_matrix ~ n²·8 bytes; manter n≲9000 (rho·T·2X).

## Regras (as de sempre)

Kill criteria pré-registrados no charter antes de rodar (difusivo = Veredito C,
testado de verdade e rejeitado); gate de engenharia antes de medição física;
negativos/limitações reportados (recursão instável, caveat de polarização, m²<0);
anti-circularidade (c nunca inserido; ondas de prova cos reais; sem literais
complexos nos geradores; sementes fixas); "fóton"/"magnon" só na síntese.

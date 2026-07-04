# FX1 — PRÉ-REGISTRO (congelado ANTES de qualquer código)

> **Origem.** Único candidato a previsão de novidade que sobreviveu ao teste §(C) do
> `MAPA_CONVERGENCIA.md`: o núcleo invariante liga, no MESMO operador causal, a **taxa de
> colapso** Γ_dec (decoerência de Lindblad, FS1) e a **escala do gás espectral** de Dyson
> Brownian Motion (FS2). Se uma estrutura mínima força as duas a compartilhar a **mesma
> escala** (uma razão adimensional fixa), isso é uma previsão **fora** do conjunto que
> TEIC/DEV/SR enunciam — o único caminho que poderia mover o veredito de **[CLASSE GRANDE]**.
>
> **Disciplina (padrão TEIC).** Predições + critérios de morte congelados aqui, ANTES de
> escrever `fx1_ratio.py`. Resultado-primeiro-narrativa-depois. Morte pré-registrada é
> definitiva. Engenharia (Stage 0) ANTES de medição. Nenhum parâmetro novo, nenhuma escala
> injetada (regra inviolável de `sr_teic_core.py`).
> **Congelado em:** 2026-06-27. Reusa engines validados (`sr_teic_core`, `fs_core`, `c5_core`)
> SEM modificação.

---

## 1. A pergunta cirúrgica

A taxa de decoerência de FS1 (Γ_dec, quadrática no operador M) e a variância espectral de
bulk de FS2 (Var(λ), a "temperatura" do gás de Coulomb de Dyson) são **ambas** funções do
MESMO operador causal M. Ambas escalam como λ² ⇒ a razão

  **R_FX1 ≡ Γ_dec(σ_x) / Var_bulk(λ_M)**

é **adimensional** e **invariante sob M→cM** (rescala global cancela: anti-circularidade
embutida; a escala externa ℏ/Γ que é a parede NÃO entra).

**A pergunta:** R_FX1 é um **número fixo universal** (independente de σ_x, dimensão e N) —
o que significaria que a geometria causal **trava** a taxa de colapso à escala espectral por
uma constante que nenhuma das três teorias deriva — ou R_FX1 **cavalga** (depende de σ_x /
dim / N), caso em que não há relação forçada?

---

## 2. Observável (definição exata, congelada)

Por realização (dim, N, seed):
1. Substrato: `pts = core.sprinkle(N, dim, rng)`; `A = core.ancestor_matrix(pts)`.
2. Operador **PRIMÁRIO**: `M = fs_core.bd_matrix(A)` (Sorkin/BD com sinal, real simétrico —
   o operador que FS2 achou GOE e FS1 usou). **SECUNDÁRIO**: `S = fs_core.sym_adjacency(A)`.
3. **Escala do gás espectral:** `Var_bulk(λ)` = variância dos autovalores de M no **bulk**
   (descarta 10% de cada borda, `edge_frac=0.10`, idêntico a `fs_core.gap_ratios`).
4. **Taxa de colapso:** para cada σ_x e separação Δx, dois modos gaussianos espaciais
   `ψ1,ψ2 = fs_core.spatial_mode(pts, σ_x, centro∓Δx/2)`; `Γ_dec = fs_core.decoherence_rate(M,ψ1,ψ2)`.
   Usa-se **Δx grande** (modos bem separados, termo cruzado→0): Δx = 60% da extensão espacial.
5. **R_FX1(σ_x, dim, N) = Γ_dec / Var_bulk(λ)**.

Varredura congelada: **dim ∈ {2, 4}**, **N ∈ {100, 200, 400}**, **σ_x ∈ {0.10, 0.18, 0.30}**
(da extensão espacial; mesmas 3 larguras de FD2/FS1), **8 seeds**. Mediana sobre seeds.

---

## 3. Stage 0 — Gate de engenharia (ANTES de qualquer medição de física)

Bloqueante. Se qualquer um falhar, a medição não roda (resultado seria artefato):
- **G0-a (invariância de escala, sanidade):** R_FX1 inalterado (|Δ|<1e-6) sob M→7·M.
  Garante que a parede de escala não está sendo medida por acidente. (Analiticamente trivial;
  asseverado numericamente.)
- **G0-b (termo cruzado controlado):** ⟨ψ|M|ψ⟩ pequeno vs √Var na config. Δx grande, de modo
  que Γ_dec ≈ ½(⟨M²⟩₁+⟨M²⟩₂) (regime de modos separados, onde a comparação com Var é limpa).
  Registrar a fração cruzado/total; se >20%, aumentar Δx.
- **G0-c (controle positivo / referência sem estrutura):** o MESMO R_FX1 numa **matriz GOE
  aleatória** de mesmo N com modos espaciais aleatorizados (sem geometria causal). Dá o valor
  de referência "espectro genérico, modo genérico". Se TEIC produzir o MESMO R do GOE-aleatório
  → R é genérico-RMT (não-novidade); se TEIC produzir um R **distinto e fixo** → candidato real.

---

## 4. Predições (congeladas — três desfechos possíveis)

- **H_novidade [moveria o veredito]:** R_FX1 é um número **fixo, não-trivial e universal**
  (estável <±20% através de σ_x a (dim,N) fixos; sem deriva sistemática em dim/N; **distinto**
  do controle GOE-aleatório de G0-c; **não** reduzível à identidade definicional de Lindblad).
  ⇒ a geometria causal força uma relação colapso↔espectro que TEIC/DEV/SR não enunciam.
  ⇒ candidato a **[FORÇA ESTRUTURA]** (fraco, 1 razão adimensional).

- **H_trivial [sela CLASSE GRANDE]:** R_FX1 ≈ constante, mas **igual** ao controle GOE-aleatório
  OU igual à identidade de Lindblad Γ_dec=½Var(M) (i.e. o modo gaussiano espacial amostra o
  espectro como a medida uniforme). ⇒ a "relação" é uma **identidade definicional**, não uma
  previsão física nova. Núcleo continua genérico.

- **H_nulo [sela CLASSE GRANDE]:** R_FX1 **cavalga** em σ_x (e/ou dim, N) — não há razão fixa.
  ⇒ taxa de colapso e escala espectral **não** estão travadas. (É o meu prior: FS1 já achou o
  PREFATOR do Δx² não-universal, rel_var 0.05–3.26, `RESEARCH_MAP.md:274-276`.)

---

## 5. Critério de morte (pré-registrado, definitivo)

**NOVIDADE MORRE** se QUALQUER:
1. R_FX1 varia >±20% através das 3 larguras σ_x a (dim,N) fixos (= H_nulo), OU
2. R_FX1 deriva sistematicamente com dim ou N (não-universal), OU
3. R_FX1 coincide (dentro de ±15%) com o controle GOE-aleatório de G0-c (= genérico-RMT), OU
4. R_FX1 coincide com a identidade de Lindblad ½ (= definicional, H_trivial).

Se NENHUM dos quatro dispara → **NOVIDADE SOBREVIVE** (candidato a previsão fora do núcleo;
abre uma campanha de construção, NÃO fecha aqui).

**Honestidade obrigatória de prior:** eu espero **H_nulo ou H_trivial** (morte). O valor do
pré-registro é justamente deixar o dado derrubar o prior se R_FX1 for fixo e não-trivial. Não
favorecer H_novidade por ser o desfecho empolgante (mesma regra do `MAPA_CONVERGENCIA.md`).

---

## 6. O que cada desfecho significa para a teoria invertida

| Desfecho | Veredito do mapa | Próximo passo |
|---|---|---|
| H_novidade | [CLASSE GRANDE] **trincado** num ponto — há 1 previsão forçada | campanha de construção mínima focada nessa razão |
| H_trivial | **[CLASSE GRANDE] selado** — a relação é identidade, não física | publicar o mapa como resultado |
| H_nulo | **[CLASSE GRANDE] selado** — nem identidade há | publicar o mapa como resultado |

Arquivos: `fx1_ratio.py` (código), `fx1_ratio.json` (dados), veredito em `FX1_VERDICT.md`
(separado deste pré-registro, que não se edita após ver os números).

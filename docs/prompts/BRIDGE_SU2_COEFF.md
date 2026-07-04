# BRIDGE_SU2_COEFF: Coarse-graining SU(2) — Skyrme emerge?

> Testa se o termo de Skyrme emerge do coarse-graining da ação SU(2) na rede causal,
> como F² emergiu do coarse-graining U(1) em W1–W2 (`BRIDGE_WILSON.md`).
> Resultados em `results/bridge/su2_coeff/`. Ataque 1 do `ROADMAP_REVOLUCAO.md`.
> NÃO modifica `su2_core.py` nem nenhuma campanha anterior (importa, não altera).

## ✅ VEREDITO: **B — o OPERADOR de Skyrme emerge; a DOMINÂNCIA não** (como pré-registrado no adendo)

```
SC1  expansão: E⁽⁴⁾ = −(3a⁴/5760)S + (a⁴/2880)K — Skyrme presente, sinal estabilizador
SC2  razão Poisson B/A = 0.55522±0.00030 (pred 5/9); cúbica = 1.0 exata (grade CEGA);
     c_K = +3.477e-4±4e-7 (pred +a⁴/2880 = 3.472e-4) — morte NÃO ativada
SC3  c_K ∝ a⁴ (expoente 4.000); λ_Sk = a/√120 (expoente 2.000) — escala = granularidade
SC4  cosseno sozinho: E(λ) monotônica, SEM mínimo interior (K ≤ ⅔S trava o sinal);
     controle Skyrme manual: λ* = 1.20 (pred 1.20) ✓
```
**Descoberta central:** o operador de Skyrme é gerado pela **isotropia de Poisson** —
a grade cúbica é exatamente cega a ele (por isso a literatura de rede o adiciona à
mão). O mesmo ingrediente de R1 (Poisson ⇒ Lorentz) gera o estabilizador da matéria
(Q1→Q6). O limite U(1) (K=0) reproduz o quártico DBI negativo de W2. O que permanece
importado: a dominância (custo de núcleo não-cosseno) — a mesma fronteira de
PHI_EMERGE V4, agora pela energética. Paper II: ingredientes 3 → 2.
Síntese: [`results/bridge/su2_coeff/SC5_synthesis.md`](results/bridge/su2_coeff/SC5_synthesis.md).

---

## CRITÉRIO DE MORTE (pré-registrado, antes de qualquer resultado)

O experimento falha (Skyrme permanece axioma) se:

```
O operador de quarta ordem emergente do coarse-graining SU(2)
é APENAS o SIMÉTRICO (Tr F²)² / (TrG)², SEM componente do
ANTISSIMÉTRICO Tr([U⁻¹∂_μU, U⁻¹∂_νU])²  (= Σ|c_μ×c_ν|²).
```

A distinção é precisa:
- Simétrico: existe em U(1) também — não é específico de SU(2).
- Antissimétrico (Skyrme): zero em U(1), não-zero em SU(2).

Se o quártico emergente for só simétrico: reportar como resultado honesto.
Não ajustar a análise para encontrar o Skyrme.

**Vereditos possíveis (pré-nomeados):** A (Skyrme emerge com dominância
estabilizadora) · **B/PARCIAL** (o operador de Skyrme emerge com coeficiente
travado, mas sem dominância — ver adendo) · C (só simétrico — morte) ·
D (ruído soterra — inconclusivo).

---

## ADENDO TÉCNICO PRÉ-REGISTRADO (análise feita ANTES de rodar)

A inspeção de `su2_core.py` (campanha MATTER_SU2) e a expansão analítica do cosseno
de link motivam **previsões numéricas exatas, registradas aqui antes de qualquer
execução**, que SC1–SC2 devem confirmar ou refutar:

**Dois canais distintos (ambos testados):**
- **Canal quiral (link de sítio, onde o Skyrmion vive):** o termo de link
  `Δτ[1−½Tr(U_i†U_j)]` em uma direção e tem expansão exata
  `1−cos(a|ℓ_e|/2)`, com `ℓ_e^a = ℓ_μ^a e^μ` (correntes `c_μ`). O quártico de UM link
  vê só `|ℓ_e|⁴` — **uma grade cúbica (links só nos 3 eixos) soma apenas Σ_i|ℓ_i|⁴,
  diagonal: estruturalmente CEGA ao comutador**. A média isotrópica de Poisson gera os
  momentos cruzados `⟨e^μe^νe^ρe^σ⟩ = (δδ+δδ+δδ)/15` e produz
  `⟨|ℓ_e|⁴⟩ = [(TrG)² + 2Tr(G²)]/15 = [3S − 2K]/15`,
  onde `G_μν = c_μ·c_ν`, `S=(TrG)²` (simétrico) e `K=(TrG)²−Tr(G²) = Σ_{μν}|c_μ×c_ν|²`
  (**o operador de Skyrme**). Ou seja: **o operador de Skyrme emerge da isotropia de
  Poisson — o mesmo ingrediente de R1 — e a grade cúbica o perde** (é por isso que
  MATTER_SU2 precisou adicioná-lo à mão na grade).
- **Canal de gauge (plaqueta):** o quártico do cos da plaqueta é o simétrico `(|F|²)²`;
  o comutador entra DENTRO de `|F|²` (segunda ordem, sinal +), mas no setor do sóliton
  Stückelberg blinda F→0. Previsão: este canal NÃO fornece o Skyrme do sóliton.

**Previsões numéricas exatas (falsificáveis) para SC2, campo constante:**
- Config A (abeliana, K=0, S casado): `c_x=c_y=c_z=g(1,0,0)` → 3S−2K = 27g⁴.
- Config B (tipo-hedgehog): `c_x=g(1,0,0), c_y=g(0,1,0), c_z=g(0,0,1)` → 3S−2K = 15g⁴.
- **Razão Poisson r₄(B)/r₄(A) = 15/27 = 5/9 ≈ 0.5556** (≠1 ⇒ comutador presente).
- **Razão cúbica = 1.0000 exatamente** (cegueira da grade — o controle).
- Coeficiente de K por link: **+a⁴/2880** (sinal positivo = estabilizador), do
  termo −x⁴/24 do cosseno: `−(a⁴/384)·(3S−2K)/15`.

**Risco pré-declarado (o que pode forçar veredito B em vez de A):** como
`Tr(G²) ≥ (TrG)²/3` ⇒ `K ≤ ⅔S` ⇒ `3S−2K ≥ (5/3)S > 0` — o quártico LÍQUIDO do
cosseno é sempre negativo (saturação DBI, consistente com W2 em U(1), que é o corte
K=0 desta fórmula). Então a previsão honesta é: **o operador de Skyrme emerge com
coeficiente positivo e travado em K:S = +2:−3, mas a parte simétrica domina o sinal
líquido** — a estabilização de Derrick pelo cosseno puro deve falhar no truncamento
e SC4 mede se o cosseno completo (limitado) pina o sóliton na escala de granularidade.
Se SC4 não encontrar mínimo interior: **veredito B**, reportado como tal — o Skyrme
move de "axioma" para "operador derivado com razão fixa, dominância não derivada".

---

## Por que este experimento importa

W1–W2 fizeram para U(1): `Wilson U(1) coarse-grained → F²` (erro 1e-12 em campo
constante). A pergunta análoga para SU(2): o quártico do coarse-graining é o Skyrme
ou outro? Se o Skyrme emerge: o Paper II passa de "3 ingredientes importados" para
"1 ingrediente" (o grupo SU(2) — ele próprio forçado por minimalidade, Ataque 5).
E o coeficiente emergente é fixado pela granularidade — a relação cruzada com
G∝1/K do Ataque 6.

## Infraestrutura

- `results/matter/su2/su2_core.py` — quaternions, Hamilton, 4 portões validados.
- `results/bridge/wilson/` — protocolo de coarse-graining U(1) (referência).
- Guard: `tests/test_no_circularity.py` escaneia `results/bridge/` — sem complexos,
  sem fórmulas de dilatação nos geradores (quaternions reais, cos/sin).

---

## Tarefas

### SC1 — Expansão analítica até quarta ordem
Derivar e VERIFICAR (sympy + quaternions numéricos) as identidades do adendo:
(i) `1−½Tr(exp(aL_e)) = 1−cos(a|ℓ_e|/2)`; (ii) momento isotrópico
`⟨(e·u)²(e·v)²⟩ = [u²v²+2(u·v)²]/15`; (iii) `⟨|ℓ_e|⁴⟩ = (3S−2K)/15`;
(iv) `K = Σ|c_μ×c_ν|² ↔ −2Tr([L_μ,L_ν]²)`-tipo (a identidade su(2) do produto
vetorial); (v) o quártico da plaqueta de gauge é simétrico em F.
Output: `SC1_expansion.md` + `SC1_expansion.tex` + `SC1_expansion.json`.

### SC2 — Teste numérico decisivo em campo constante
Configs A/B do adendo; 20 sementes de direções; medir resíduo quártico por link
(energia exata do quaternion − termo quadrático exato), medidas Poisson E cúbica.
```
SKYRME PRESENTE:  razão B/A = 5/9 (Poisson), 1.0 (cúbica), coef K = +a⁴/2880
SÓ SIMÉTRICO:     razão B/A = 1.0 em ambas  → CRITÉRIO DE MORTE ATIVADO
```
Output: `SC2_constant_field.{py,md,json}` + figura.

### SC3 — Coeficiente: constância e escala
c₄ constante em g (platô g→0)? Escala com a granularidade: λ²_Sk = (E₄/K)/(E₂/TrG)
∝ a² (expoente 2 em log-log)? Relação cruzada: o mesmo a (=1/K-rigidez) que fixa
G∝1/K fixa o comprimento de Skyrme — registrar para o Ataque 6.
Output: `SC3_coefficient.{py,md,json}` + figura.

### SC4 — Derrick com o quártico emergente
Hedgehog radial; E(λ) sob dilatação com (a) truncamento quártico emergente e
(b) cosseno completo via MC de links Poisson (limitado ⇒ sem explosão).
Pergunta: mínimo interior em λ ~ granularidade (pinning) ou colapso?
Controle: E(λ) com Skyrme manual (+e_sk·K) reproduz o mínimo do Paper II.
Output: `SC4_derrick.{py,md,json}` + figura.

### SC5 — Síntese honesta
Veredito A/B/C/D contra o pré-registro acima; tabela "previsto vs medido";
o que muda no Paper II em cada caso.

## Protocolo

1. Anti-circularidade: Skyrme NUNCA inserido como alvo de fit; SC2 mede o resíduo
   e DEPOIS compara com a previsão pré-registrada.
2. Campo constante antes de variável (SC2 antes de SC3/SC4), como W1→W2.
3. O teste do comutador (SC2, razão A vs B) é o decisivo.
4. 20 sementes para SC2–SC3; sementes fixas; JSON auto-descritivo.
5. Critério de morte ativado em SC2 ⇒ reportar imediatamente como C.

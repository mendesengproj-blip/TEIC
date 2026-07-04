# SKYRME_DOMINANCE: O Último Asterisco Interno

> Investiga se a dominância do operador de Skyrme pode emergir da ação mínima
> em algum regime da rede. Fecha a fronteira deixada por `BRIDGE_SU2_COEFF`
> (veredito B: o operador emerge, a dominância não).
> Resultados em `results/bridge/skyrme_dominance/`.
> NÃO modifica nenhuma campanha anterior (importa `sc_core.py`, não altera).

## ✅ VEREDITO: **MORTE TOTAL — na forma forte** (como pré-registrado no adendo)

```
SD1  K ≤ (1−1/d)·S é identidade PONTUAL (Cauchy–Schwarz no Gram PSD), saturada
     pelo hedgehog; em d=3 NÃO EXISTE configuração com K/S > 2/3; razão −3:+2
     d-independente ⇒ 3S−2K ≥ (1+2/d)S > 0 em toda dimensão; adversarial 10⁶: ✓
SD2  c₆ > 0 (exato) mas mínimo truncado em u(λ*)=8.0 ≫ 1 (óctico/sêxtico 0.55,
     erro 42%); cosseno completo monotônico — artefato de truncamento
SD3  κ₃ = 2/5 constante em ρ=10..1000 (isotropia exata); 5/9 verificado em links
     causais REAIS; causal ≡ tipo-espaço; κ cresce com d mas gap nunca fecha
SD4  TEOREMA DO SINAL: E₄ = −(a⁴/384)⟨|ℓ|⁴⟩ ≤ 0 sob QUALQUER medida (sup −2e−13
     em 20k medidas patológicas; hedgehog invariante de medida); f(R)=1+0.038·Rρ^(−1/2)
     ≠ 1 mas ANTI-estabilizador; isotropia já é o ótimo do canal K
```
**Descoberta central:** a fronteira virou teorema. A dominância não é "não
encontrada" — é estruturalmente inalcançável no canal cosseno: identidade
pontual + sinal herdado da série de Taylor (não da geometria). O custo de
núcleo não-cosseno permanece o último ingrediente externo do setor de matéria,
agora localizado por argumento de impossibilidade. Paper II: a linha Skyrme
ganha o enunciado forte. Síntese:
[`results/bridge/skyrme_dominance/SD5_synthesis.md`](../../results/bridge/skyrme_dominance/SD5_synthesis.md).

---

---

## O problema preciso

BRIDGE_SU2_COEFF (Ataque 1) derivou:

$$E^{(4)} = -\frac{3a^4}{5760} S + \frac{a^4}{2880} K$$

onde S é o operador simétrico e K é o operador de Skyrme.

O resultado: K emerge com sinal estabilizador (+), mas a restrição K ≤ ⅔S
mantém o quártico líquido sempre negativo. O cosseno sozinho é monotônico —
sem mínimo interior.

**A questão:** existe algum regime da rede onde K > ⅔S?
Ou a desigualdade K ≤ ⅔S é estrutural e inviolável?

---

## CRITÉRIO DE MORTE (pré-registrado)

```
MORTE TOTAL: K ≤ ⅔S em todos os regimes testados,
             demonstrável analiticamente como identidade.
             Dominância não emerge.
             A afirmação honesta permanece:
             "o operador emerge, a dominância não."

MORTE PARCIAL: K < ⅔S sempre mas a razão K/S cresce com
               algum parâmetro — identificar o parâmetro
               e o limite assintótico.

SUCESSO PARCIAL: existe regime (alta ρ, ou campos específicos,
                 ou termos de ordem maior) onde K/S > 2/3.

SUCESSO COMPLETO: K/S > 1 em algum regime →
                  quártico líquido torna-se positivo →
                  mínimo interior existe sem Skyrme adicionado.
```

---

## ADENDO TÉCNICO PRÉ-REGISTRADO (análise feita ANTES de rodar)

A inspeção das identidades de `sc_core.py`/SC1 motiva previsões exatas,
registradas aqui antes de qualquer execução, que SD1–SD4 devem confirmar
ou refutar:

1. **K ≤ S é identidade exata e inviolável.** Com G = C·Cᵀ (Gram das
   correntes, semidefinido positivo): K = S − Tr(G²) e Tr(G²) ≥ 0.
   Igualdade só em G = 0. Nenhuma configuração tem K > S.

2. **A restrição é mais forte e é PONTUAL, não média.** Cauchy–Schwarz nos
   autovalores λᵢ ≥ 0 do Gram d×d: d·Σλᵢ² − (Σλᵢ)² = Σᵢ<ⱼ(λᵢ−λⱼ)² ≥ 0, logo
   **K ≤ (1 − 1/d)·S pontualmente**, saturada exatamente quando G ∝ I — o
   hedgehog. Em d = 3: **K ≤ ⅔S é identidade pontual link a link**, não um
   resultado da média isotrópica; o hedgehog já a satura (K/S = 2/3). Não
   existe configuração em d = 3 com K/S > 2/3. SUCESSO PARCIAL e COMPLETO
   são portanto previstos como matematicamente impossíveis no canal quártico.

3. **A razão de coeficientes −3:+2 é independente de d.** O momento
   isotrópico em d dimensões, ⟨(e·u)²(e·v)²⟩ = [u²v² + 2(u·v)²]/(d(d+2)),
   dá ⟨|ℓ_e|⁴⟩ = (3S − 2K)/(d(d+2)): só o prefator muda com d, a combinação
   3S − 2K não. Com (2): 3S − 2K = S + 2Tr(G²) ≥ (1 + 2/d)·S > 0 em TODA
   dimensão e TODA configuração — nem d → ∞ fecha o gap (limite: 3S−2K ≥ S).

4. **Teorema do sinal (o mais forte).** O quártico do cosseno por link é
   −(a⁴/384)·|ℓ_e|⁴, com o −1/24 vindo da série de Taylor do cosseno, não da
   geometria. Logo E⁽⁴⁾ = −(a⁴/384)·⟨|ℓ_e|⁴⟩_medida ≤ 0 para **qualquer**
   medida de direções de link (anisotrópica, curva, discreta, qualquer ρ) e
   qualquer configuração. Caso extremo: para o hedgehog (G ∝ I), (eᵀGe)² = g⁴
   independente de e — o quártico do núcleo é negativo sob QUALQUER medida.
   Curvatura, densidade e anisotropia podem mudar a MAGNITUDE de c₄, nunca o
   sinal líquido.

5. **Fração de canal cruzado por link** (a quantidade K/S(d) do enunciado:
   S(e) = (Σ(e^μ)²)² = 1, K(e) = 1 − Σ(e^μ)⁴; é a fração do peso quártico do
   link em canais μ≠ν — NÃO confundir com K/S dos invariantes do campo):
   ⟨K/S⟩(d) = 1 − 3/(d+2). Valores: d=1 → 0 (uma direção só — sem canal de
   comutador; é o "K=0" do enunciado, que o atribui a d=2: lapso de rótulo,
   d ali é o ESPAÇO-TEMPO 1+1), d=2 → 1/4, d=3 → 2/5, d=4 → 1/2,
   d=5 → 4/7 (o enunciado lista 3/7: lapso aritmético, 1−3/7 = 4/7),
   d→∞ → 1. Cresce com d mas o item (3) mostra que isso nunca fecha o gap.

6. **Os três números não são o mesmo número.** 5/9 (SC2) é
   (3S−2K)_B/(3S−2K)_A = 15/27, razão de resíduos quárticos entre configs;
   2/3 é o K/S pontual do hedgehog (saturação); 2/5 é a fração média de canal
   cruzado por link em d=3; 1/2 é a mesma fração em 4 componentes. A pergunta
   do enunciado "5/9 bate com 1/2?" compara quantidades distintas — SD1
   esclarece as quatro.

7. **Sêxtico:** o termo +u⁶/720 do cosseno dá +(a⁶/46080)·|ℓ_e|⁶ por link,
   média isotrópica d=3: ⟨|ℓ|⁶⟩ = [(TrG)³ + 6TrG·TrG² + 8TrG³]/105 ≥ 0 →
   **c₆ > 0 garantido** (estabilizador). O Derrick truncado
   E(λ) = λE₂ − |E₄|/λ + E₆/λ³ tem SEMPRE mínimo interior formal (diverge nos
   dois extremos). A questão honesta é a validade: previsão pré-registrada —
   a fase de link no mínimo, u(λ*) = (a/2λ*)·max|ℓ| ≫ 1, fora do raio de
   convergência útil; a oitava ordem (−u⁸/40320, sinal de novo negativo) é
   comparável ao sêxtico em λ*; o cosseno completo (que ressoma a série e é
   limitado) já foi medido monotônico em SC4/DS3. **Critério: o resgate
   sêxtico só é real se u(λ*) < 1 E o cosseno completo tiver mínimo interior.**

8. **Curvatura:** com Vol(τ) = (π/24)τ⁴[1 − Rτ²/96 + …] (coeficiente −1/96
   medido em R4/Tasks A–B), R > 0 reduz volumes de intervalo → menos supressão
   e^{−ρV} → links mais longos → ⟨a⁴⟩ cresce: **f(R) ≠ 1 esperado**
   (f = 1 + κ·R·ρ^{−1/2}, κ > 0). Mas curvatura isotrópica preserva a
   isotropia das direções → multiplica c_S e c_K igualmente → razão −3:+2
   intacta → **f(R) > 1 torna o quártico líquido MAIS negativo** (anti-
   estabilizador). Pelo item (4), nenhum f(R) flipa o sinal.

9. **Densidade:** a isotropia de Poisson é exata em todo ρ (a distribuição de
   direções espaciais de links é uniforme em S² por simetria, independente de
   ρ). Previsão: K/S(ρ) constante; flutuações ∝ N_links^{−1/2}.

**Veredito previsto: MORTE TOTAL**, na forma forte — não "em todos os regimes
testados" mas demonstrável como identidade para qualquer medida de links.
Se algum teste numérico violar (1)–(4), o erro está na análise e o resultado
numérico manda.

---

## Tarefa SD1 — Análise analítica da desigualdade K ≤ ⅔S

Demonstrar (sympy + verificação numérica adversarial): K = S − Tr(G²) ≤ S
exata; K ≤ (1−1/d)·S pontual com saturação no hedgehog; razão −3:+2
independente de d; 3S−2K ≥ (1+2/d)·S > 0. Esclarecer os quatro números do
item (6). Busca adversarial: max K/S sobre 10⁶ configurações aleatórias em
d = 2..6 → deve aproximar 1−1/d, nunca exceder.
**Output:** `results/bridge/skyrme_dominance/SD1_analysis.md` + json.

## Tarefa SD2 — Termos de ordem superior

Calcular c₆ exato (momento sêxtico isotrópico, verificação simbólica por
pareamentos + MC); Derrick truncado E₂+E₄+E₆ para o hedgehog: localizar λ*,
medir u(λ*), comparar truncamentos (4ª, 6ª, 8ª ordem) com o cosseno completo
na mesma grade; aplicar o critério do item (7).
**Output:** `SD2_higher_order.md` + json + figura.

## Tarefa SD3 — Varredura K/S em função de parâmetros

(a) fração de canal cruzado vs d (MC, d=1..8) contra 1−3/(d+2);
(b) max K/S do campo vs d contra 1−1/d; gap líquido (1+2/d) vs d;
(c) sprinklings reais em diamante causal M^{3+1}, ρ ∈ {10, 50, 200, 1000},
20 sementes: direções espaciais de links (cobertura da relação causal),
fração 3d (pred 2/5) e 4d (pred 1/2 para isotrópico — links causais devem
desviar), razão SC2-style r₄(B)/r₄(A) com direções medidas (pred 5/9),
links causais vs pares espaciais separadamente.
**Output:** `SD3_ratio_scan.md` + json + figura.

## Tarefa SD4 — Curvatura como estabilizador

(a) Teorema do sinal: verificação adversarial — medidas de direção aleatórias
(uniformes, clusterizadas, discretas, pesos aleatórios) × configurações
aleatórias: sup do quártico líquido = 0⁻ (nunca positivo); núcleo hedgehog
invariante de medida. (b) f(R) = ⟨a⁴⟩_R/⟨a⁴⟩_0 da distribuição de comprimentos
de link p_R(τ) ∝ V'_R(τ)·e^{−ρV_R(τ)} com V_R = (π/24)τ⁴(1−Rτ²/96); extrair
κ em f = 1 + κ·R·ρ^{−1/2}; sinal do efeito sobre o quártico líquido.
(c) Anisotropia axial w(c) ∝ exp(κ_a c²), κ_a ∈ [−5,5]: razão efetiva
c_K:c_S muda? Sinal líquido alguma vez flipa? (Pelo item 4: não pode.)
**Critério de morte:** f(R) = 1 para todo R (curvatura não afeta c₄) — OU
f(R) ≠ 1 mas incapaz de flipar o sinal (curvatura ineficaz para dominância).
**Output:** `SD4_curvature.md` + json + figura.

## Tarefa SD5 — Síntese honesta

Quadro de vereditos contra este pré-registro; o que muda no Paper II.

---

## Protocolo

1. Anti-circularidade: aritmética real (quaternions de `su2_core` via
   `sc_core`); sem complexos; Skyrme nunca inserido como alvo de fit;
   guard `tests/test_no_circularity.py` cobre `results/bridge/`.
2. Kill criteria no docstring de cada gerador ANTES de rodar.
3. Sementes fixas; 20 sementes onde há MC; JSON auto-descritivo com `_meta`.
4. Qualquer conflito numérico com o adendo → o número manda, reportar.

## O que este resultado significa para os papers

**Se MORTE TOTAL** — Paper II, Seção "derivado vs assumido", linha Skyrme:
o operador emerge (SC1–SC3) mas a dominância é estruturalmente inalcançável
pela ação mínima: identidade pontual K ≤ ⅔S + teorema do sinal. A afirmação
honesta ganha força: não é "não encontramos o regime", é "o regime não existe
no canal quártico do cosseno". O custo de núcleo não-cosseno permanece o
último ingrediente externo do setor de matéria — agora com a fronteira
demonstrada, não apenas medida.

**Se SUCESSO (sêxtico ou curvatura):** verificação tripla obrigatória antes
de tocar nos papers.

## Prioridade

**ALTA** — último asterisco interno antes da submissão.

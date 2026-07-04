# SD4 — Curvatura local modifica c₄? (autoestabilização)

> Gerador: `SD4_curvature.py` → `SD4_curvature.json` + `.png`.
> Pré-registro: adendo itens 4 e 8. Usa o coeficiente de volume −1/96 medido
> em R4/Tasks A–B; nenhum input novo.

## (a) O teorema do sinal — o resultado mais forte da campanha

O −1/24 do quártico vem da série de Taylor do cosseno, não da geometria:
o quártico por link é −(a⁴/384)|ℓ_e|⁴ ≤ 0 **termo a termo**. Logo

$$E^{(4)} = -\frac{a^4}{384}\,\big\langle |\ell_e|^4 \big\rangle_{\rm medida} \le 0$$

para **qualquer** medida de direções (anisotrópica, clusterizada, atômica,
qualquer ρ, qualquer curvatura) e **qualquer** configuração. Verificação
adversarial: 20 000 medidas patológicas (mistura de uniformes, von-Mises
concentradas, 1–5 átomos discretos, pesos aleatórios) × configurações com
escalas heavy-tail:

- sup E₄ = −1.7·10⁻¹³ (nunca positivo; → 0 só com o campo → 0);
- sup E₄/S = −1.6·10⁻⁸ (escala-livre: nunca positivo);
- **núcleo hedgehog (G ∝ I): E₄/g⁴ = −1/384 = −0.0026042 sob TODAS as
  medidas** (max−min = 3·10⁻¹⁵) — pois |ℓ_e|² = g² independe de e. O núcleo
  do Skyrmion tem quártico negativo invariante de medida: nenhuma deformação
  geométrica da rede o salva.

## (b) f(R): a curvatura MOVE c₄ — na direção errada

Distribuição de comprimentos de link p_R(τ) ∝ ρV′_R(τ)e^{−ρV_R(τ)} com
V_R = (π/24)τ⁴(1 − Rτ²/96):

$$f(R) = \frac{\langle a^4\rangle_R}{\langle a^4\rangle_0} = 1 + \kappa\,R\,\rho^{-1/2},
\qquad \kappa = 0.03827 \pm 10^{-15}\ \text{(colapso exato em }R\rho^{-1/2},\ \rho\ 50\to5000).$$

O critério de morte "f(R) = 1" **não** ativa: curvatura positiva reduz
volumes de intervalo → menos supressão e^{−ρV} → links mais longos → ⟨a⁴⟩
cresce. Mas a curvatura isotrópica preserva a isotropia das direções,
multiplica c_S e c_K pelo MESMO f, e f > 1 só faz o quártico líquido **mais
negativo**. A curvatura que o Skyrmion cria (R > 0) é **anti-estabilizadora**;
e pelo teorema (a), nenhum f conseguiria flipar o sinal de qualquer forma.

## (c) Anisotropia: a isotropia já é ótima para K

Medida axial w(c) ∝ exp(κ_a c²), razão efetiva −c_K/c_S extraída via configs
A/B (método SC2):

| κ_a | −5 | −2 | −1 | 0 | +1 | +2 | +5 |
|---|---|---|---|---|---|---|---|
| −c_K/c_S | 0.619 | 0.656 | 0.667 | **0.671** | 0.667 | 0.650 | 0.550 |
| sup E₄/S (2000 configs) | −7.6e−5 | −2.2e−4 | −2.7e−4 | −3.0e−4 | −2.7e−4 | −2.2e−4 | −7.5e−5 |

A razão é **máxima exatamente na isotropia** (0.671 ≈ 2/3, o resíduo é g⁶) e
cai para os dois lados — deformar a medida só piora o canal de Skyrme. E o
sup do quártico líquido permanece negativo em toda a varredura, como o
teorema exige.

## Veredito SD4: **curvatura eficaz sobre a magnitude, ineficaz para dominância**

f(R) ≠ 1 (κ = 0.038 > 0, lei f = 1 + κRρ^{−1/2} limpa) — mas o efeito tem o
sinal anti-estabilizador, e o teorema do sinal fecha a porta por completo:
nenhuma geometria de medida torna o quártico do cosseno positivo. A
autoestabilização por curvatura não existe neste canal.

Reprodução: `python SD4_curvature.py` (~2 min).

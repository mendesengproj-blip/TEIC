# FM1-1 — Equações de perturbação DEV: derivação de μ(k,z)

> Charter FM1-1. Deriva analiticamente o fator de gravidade efetiva μ(k,z) da DEV,
> com a₀(z)∝H(z)ˢ e o sinal correto de B_ε (descoberta de E2). O analítico guia o
> numérico (FM1-2/3). **COMPARISON ONLY** para "tensão S8"; a derivação é da ação.

## 1. Ponto de partida: Poisson modificada deep-MOND

A DEV é uma teoria SVT que reproduz a fenomenologia MOND no regime de baixa
aceleração (Paper I; a₀ calibrado em 167 galáxias SPARC, χ²ν≈1.3). No limite
quase-estático, sub-horizonte, a equação de Poisson para o potencial que governa a
matéria Ψ é a forma AQUAL/QUMOND:

$$\nabla\cdot\!\big[\,\mu_{\rm MOND}(|\nabla\Psi|/a_0)\,\nabla\Psi\,\big] = 4\pi G\,\rho_m,$$

com a função de interpolação μ_MOND(x)→x no regime profundo (x≪1) e →1 no
newtoniano (x≫1). Para uma perturbação linear de número de onda comóvel k e
contraste δ, |∇Ψ|≡g é a aceleração gravitacional da própria perturbação. A
gravidade efetiva sentida pela matéria é **realçada** por ν≡1/μ_MOND:

$$G_{\rm eff}/G_N \equiv \mu(k,z) = \nu\!\left(\frac{g(k,z)}{a_0(z)}\right),\qquad
\nu(y)\xrightarrow{y\ll1}\frac{1}{\sqrt{y}}\;(>1),\quad \nu(y)\xrightarrow{y\gg1}1.$$

> ⚠️ **Direção física (honestidade obrigatória).** MOND **realça** a gravidade no
> regime de baixa aceleração (é assim que explica curvas de rotação planas sem
> matéria escura): μ>1. A narrativa do charter ("gravidade mais fraca → cresce
> mais devagar → σ8 menor") está **invertida** para uma teoria tipo-MOND. A
> derivação honesta dá μ≥1 ⇒ crescimento **igual ou realçado**, nunca suprimido.
> Isto é registrado aqui antes de qualquer número (disciplina de pré-registro).

## 2. A aceleração de uma perturbação e a escala de transição k_*(z)

Da Poisson newtoniana, Ψ_k = −4πG a² ρ̄_m δ_k / k², e a aceleração própria
g = |∇Ψ| ∼ k_{\rm fís}\,|\Psi_k| dá

$$g(k,z) \sim \frac{4\pi G\,\bar\rho_m(z)\,\delta}{k_{\rm fís}}\quad\Rightarrow\quad
g \propto 1/k\ \ (\delta\text{ fixo}).$$

Escalas **grandes** (k pequeno) têm g **menor** → MOND profundo → realce grande.
Escalas **pequenas** (k grande) têm g **maior** → newtoniano → μ→1. A transição é

$$k_*(z):\quad g(k_*,z)=a_0(z)\ \Rightarrow\
k_{*,{\rm fís}}=\frac{4\pi G\,\bar\rho_m(z)\,\delta}{a_0(z)},\qquad
a_0(z)=a_0\left[\frac{H(z)}{H_0}\right]^{s}.$$

Definindo y ≡ k/k_*(z) (de modo que y<1 ⇔ k<k_* ⇔ MOND profundo), uma forma
fechada e δ-independente (avaliada na escala de fundo, δ∼1) é

$$\boxed{\ \mu(k,z) = \nu\!\big(k/k_*(z)\big),\qquad
\nu(y)=\tfrac12+\sqrt{\tfrac14+\tfrac1y}\ }$$

que satisfaz ν(y→∞)=1 (newtoniano, k≫k_*) e ν(y→0)=1/√y=√(k_*/k) (MOND profundo,
realçado). A anisotropia do campo vetorial gera o **slip** η=Φ/Ψ (Paper I):

$$\eta-1 \approx \frac{\alpha\beta}{\sqrt{x}},\quad x=g/a_0,\ \alpha=2/3,\ \beta\approx0.007
\quad\Rightarrow\quad \Sigma(k,z)\equiv\frac{1+\eta}{2}=1+\tfrac12(\eta-1),$$

o fator de lensing (governa Φ+Ψ; entra em FM1-4/5). η−1 é de ordem poucos % (Paper
I: 6.7% em DGSAT-I, x=0.016).

## 3. Onde fica k_*(z)? (o número que decide tudo)

Com a₀=1.2×10⁻¹⁰ m/s², Ωm=0.315, h=0.674 (δ=1):

| z | a₀(z) [s=½] | **k_*(z)** (h/Mpc) | escala σ8 (k≈0.2) |
|---|---|---|---|
| 0.0 | 1.20×10⁻¹⁰ | **8.6×10⁻⁴** | k≫k_* → newtoniano |
| 0.5 | 1.38×10⁻¹⁰ | **3.8×10⁻³** | k≫k_* → newtoniano |
| 1.0 | 1.61×10⁻¹⁰ | **1.0×10⁻²** | k≫k_* → newtoniano |
| 2.0 | 2.09×10⁻¹⁰ | **4.0×10⁻²** | k≫k_* → newtoniano |

**k_*(z) é de escala quase-horizonte** (≲0.04 h/Mpc), refletindo a coincidência
a₀≈cH₀/2π (numérico: cH₀/2π=1.04×10⁻¹⁰ ≈ a₀). A escala que define σ8 (R₈=8 h⁻¹Mpc,
k≈0.13–0.4 h/Mpc) está **muito acima** de k_*: ali g≫a₀, regime **newtoniano**,
μ≈1. A modificação DEV só age em k≲10⁻²–10⁻¹·k_(σ8).

## 4. O sinal de B_ε (E2) não muda a direção do crescimento

E2 mediu B_ε ≈ −K·(k²−ω²) (sinal oposto ao assumido em e10). O **zero** (ω=ck) é o
mesmo — o fóton não muda. Na Poisson estática (ω=0), B_ε[Ψ] = −K(k²)Ψ = fonte; a
fonte 4πGρ e o operador trocam de sinal **juntos**, então a relação
−k²Ψ = 4πG a² ρ̄ δ·μ é **invariante** sob o sinal global de B_ε. Logo:

> O sinal de B_ε de E2 **não inverte** o sinal de μ nem a direção do crescimento.
> Ele importaria para a propagação dinâmica (ω≠0), não para o crescimento
> quase-estático de δ_m. (Verificado em FM1-3 com ambos os sinais: σ8 idêntico.)

## 5. Equação de crescimento DEV

$$\ddot\delta_m + 2H\dot\delta_m - 4\pi G\,\bar\rho_m\,\mu(k,z)\,\delta_m = 0,$$
ou em ln a, com Ωm(a)=Ωm(1+z)³(H₀/H)²:
$$\frac{d^2\delta}{d\ln a^2} + \Big(2+\frac{d\ln H}{d\ln a}\Big)\frac{d\delta}{d\ln a}
 - \tfrac32\,\Omega_m(a)\,\mu(k,a)\,\delta = 0.$$
Como μ(k,z)≥1 em toda parte (igualdade para k≫k_*), tem-se D_DEV(k)≥D_LCDM(k), com
**igualdade nas escalas de σ8**. Portanto:

$$\sigma_8^{\rm DEV}\ \geq\ \sigma_8^{\Lambda\rm CDM}\quad(\text{igualdade na prática}),$$

o que **aciona o critério de morte pré-registrado** (σ8_DEV ≥ σ8_ΛCDM = Veredito C)
**a menos que** o cálculo numérico revele um vazamento do realce de grande escala
suficiente para mover σ8 — e esse vazamento iria na direção de **aumentar** σ8,
piorando a tensão, não fechando-a.

## 6. Limites de verificação (para FM1-2)

- **a₀→∞** ⇒ k_*→0 ⇒ y=k/k_*→∞ ∀k ⇒ μ→1 ⇒ **ΛCDM exato**. ✔ (testado em FM1-2)
- **k→∞** (UV) ⇒ μ→1 (newtoniano). ✔
- **k→0** (IR, k≪k_*) ⇒ μ=√(k_*/k)→∞ (realce MOND, grande escala). ✔

## Conclusão de FM1-1

μ(k,z)=ν(k/k_*(z)) derivado da Poisson MOND da DEV, com k_*(z)∝ρ̄_m(z)/a₀(z) de
escala quase-horizonte. **A DEV é realce (μ≥1), não supressão.** A escala de σ8 é
newtoniana (μ≈1) → σ8_DEV≈σ8_ΛCDM; onde a DEV age (grande escala) ela **aumenta**
o crescimento. A expectativa honesta, antes dos números de FM1-3, é **Veredito C**.
O sinal de B_ε de E2 não altera essa direção (quase-estático).

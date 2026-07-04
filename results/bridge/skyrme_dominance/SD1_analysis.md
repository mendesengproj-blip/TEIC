# SD1 — K ≤ ⅔S: identidade exata ou resultado estatístico?

> Gerador: `SD1_identity.py` → `SD1_identity.json`. Pré-registro no adendo de
> `docs/prompts/SKYRME_DOMINANCE.md` (itens 1–3, 6), escrito antes de rodar.

## Resultado: identidade exata, PONTUAL, e mais forte do que se pensava

A cadeia completa, toda verificada simbolicamente (sympy) e numericamente:

**1. K ≤ S — identidade trivial.** K = S − Tr(G²) com G = C·Cᵀ semidefinido
positivo ⇒ Tr(G²) ≥ 0 ⇒ K ≤ S sempre, igualdade só em G = 0. Para K > S seria
preciso Tr(G²) < 0 — impossível. (Confirma o loophole geométrico do charter.)

**2. K ≤ (1−1/d)·S — identidade PONTUAL, link a link.** Cauchy–Schwarz nos
autovalores λᵢ ≥ 0 do Gram d×d:

$$d\,\mathrm{Tr}(G^2) - (\mathrm{Tr}G)^2 = \sum_{i<j}(\lambda_i-\lambda_j)^2 \ge 0
\;\;\Rightarrow\;\; K \le \Big(1-\tfrac1d\Big) S,$$

verificada como identidade polinomial exata em d = 2..6. Saturação exatamente
em G ∝ I — **o hedgehog satura o limite** (K/S = 2/3 em d=3). A restrição
K ≤ ⅔S portanto **não vem da média isotrópica**: é geometria pontual de
qualquer configuração. Não existe campo em d = 3 com K/S > 2/3 — nem em um
único link, nem em média, nem em regime nenhum.

Busca adversarial (10⁶ configurações com escalas heavy-tail + hill climb por
dimensão): max K/S = 0.5000 (d=2), 0.66667 (d=3), 0.743 (d=4), 0.7998 (d=5),
0.826 (d=6) — aproxima 1−1/d por baixo, **nenhuma violação**.

**3. A razão −3:+2 é independente de d** (contração explícita dos três
pareamentos de Wick contra G_ij·G_kl, d simbólico):

$$\langle|\ell_e|^4\rangle = \frac{3S-2K}{d(d+2)}.$$

Só o prefator 1/d(d+2) muda com a dimensão; a combinação 3S−2K não. Com (2):

$$3S-2K = S + 2\,\mathrm{Tr}(G^2) \ge \Big(1+\tfrac2d\Big)S > 0
\quad\text{em toda dimensão e toda configuração.}$$

Nem d → ∞ fecha o gap: o limite é 3S−2K ≥ S. MC de pareamento confirma em
d = 2..5 (razão LHS/RHS = 1.000 ± 0.002).

## Os quatro números (a pergunta "5/9 bate com 1/2?")

São quantidades distintas — a comparação do charter mistura três objetos:

| número | o que é | valor |
|---|---|---|
| **5/9** | razão de resíduos quárticos (3S−2K)_B/(3S−2K)_A entre configs B e A (SC2) | 0.5556 |
| **2/3** | K/S pontual do hedgehog = saturação do limite de campo em d=3 | 0.6667 |
| **2/5** | fração média de canal cruzado de um LINK, κ(e) = 1−Σ(e^μ)⁴, d=3 | 0.4000 |
| **1/2** | a mesma fração com 4 componentes | 0.5000 |

O 5/9 do SC2 não tem que bater com 1/2 — não são o mesmo observável.
Dois lapsos do enunciado corrigidos de passagem: κ = 0 ocorre em d = 1 (uma
direção só), não d = 2 (em d=2, κ = 1/4); e ⟨κ⟩(5) = 1−3/7 = 4/7, não 3/7.

## Implicação

SUCESSO PARCIAL (K/S > 2/3 em algum regime) e SUCESSO COMPLETO (K/S > 1) do
pré-registro são **matematicamente impossíveis em d = 3 no canal quártico**:
não é que o regime não foi encontrado — o regime não existe. O ramo vivo da
campanha passa a ser só ordem superior (SD2) e mecanismos fora do quártico
(SD4).

Reprodução: `python SD1_identity.py` (~2 min; sympy + 5·10⁶ configs).

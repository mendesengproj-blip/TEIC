# FL1_SU3_FOUNDATION — Fase A: Definição, Positividade e Causalidade

> Estabelece se um campo SU(3) pode ser **definido** na mesma rede causal de
> Poisson 3+1D que produziu SU(2), com **ação positiva semi-definida** e **sem
> violar a localidade causal**. Motor novo: `su3_core.py` (matrizes 3×3 complexas
> + geradores de Gell-Mann — SU(3) não tem atalho quaterniônico). Não importa
> `su2_core`/`orientation_core`; reusa apenas `causal_core` (o substrato comum).
> Resultados: `results/matter/fl1/FLA_definition.{py,json}`.

## ✅ VEREDITO: **FASE A PASSA** — SU(3) é definível na rede causal

```
A ação mínima é positiva semi-definida e a localidade causal é preservada.
O substrato de Poisson NÃO impõe nenhuma obstrução à definição de SU(3): ele
hospeda SU(3) exatamente como hospeda SU(2). A fronteira (se houver) não está
na DEFINIÇÃO do campo — está adiante (ordenamento na Fase B, defeito/confinamento
na Fase C). Prosseguir para a Fase B é justificado.
```

Critério de morte pré-registrado da Fase A (ação não-PSD em nenhuma escolha
razoável **ou** causalidade violada): **não disparado**. Como antecipado, a ação
de Wilson de um grupo unitário sobre um conjunto causal é PSD por construção e os
links são causais por construção — a Fase A não pode morrer por esses critérios, e
o resultado é a delimitação honesta de que o **substrato** comporta SU(3).

---

## Os cinco portões (medidos, depois conferidos contra a previsão)

| Portão | Pergunta | Resultado | Veredito |
|---|---|---|---|
| **A1** | Campo SU(3) bem definido (geradores, constantes de estrutura, leis de grupo)? | erro máx **1.3×10⁻¹⁵** | PASS |
| **A2** | Ação de plaqueta de Wilson `s_p = 1 − ⅓ Re Tr(W) ≥ 0`? | mín **+2.2×10⁻⁷**, identidade **= 0** exato | PASS |
| **A3** | Termo sigma (quadrático) `Tr((e·C)²) ≥ 0`? | mín **+0.174** (1×10⁶ amostras) | PASS |
| **A4** | Cauchy–Schwarz / teorema do sinal (repetição de SKYRME_DOMINANCE)? | quártico líq. máx **−1.6×10⁻²** (≤0); `K ≤ 6·TrM²`; identidade exata a **8×10⁻¹⁶** | PASS |
| **A5** | Localidade causal preservada? | **100,00%** dos links causais; covariância de gauge **9×10⁻¹⁶** | PASS |

### A1 — Definição do campo
Geradores de Gell-Mann com `Tr(λ_aλ_b)=2δ_ab` (erro 4×10⁻¹⁶); constantes de
estrutura extraídas por projeção batem com os valores canônicos
(`f₁₂₃=+1`, `f₄₅₈=+√3/2=0.8660`, `d₁₁₈=+1/√3=0.5774`), `f` totalmente
antissimétrica (erro 0), `d` simétrica. SU(3) Haar aleatório (2×10⁵): unitariedade
e `det=1` a 10⁻¹⁵, fechamento sob produto, associatividade e mapa exponencial
`exp(i φ_aλ_a) ∈ SU(3)` todos a precisão de máquina. **O campo é definível.**

### A2 — Positividade da ação de Wilson
Argumento analítico: os autovalores de `W ∈ SU(3)` vivem no círculo unitário, logo
`Re Tr(W) = Σ_k cos θ_k ≤ 3`, dando `s_p ≥ 0` com igualdade **sse** `W = I`.
Verificação adversarial (10⁶ plaquetas): Haar aleatórias e perto-da-identidade num
leque de escalas de álgebra (10⁻³ … 2.0) — mínimo global **+2.2×10⁻⁷ > 0**; a
plaqueta identidade dá densidade **exatamente 0**. O "piso" cresce ∝ escala²
(2.2×10⁻⁷ → 6.9×10⁻² de 10⁻³ a 1.0), o comportamento esperado do regime quadrático.
**Ação de plaqueta PSD confirmada.**

### A3 — Positividade do termo sigma (custo de núcleo quadrático)
Expandindo `1 − ⅓ Re Tr(exp(i a(e·C)))` o termo de 2 derivadas é `+(a²/6) Tr((e·C)²)`.
Como `e·C` é Hermitiana, `Tr((e·C)²)=Σ_k λ_k² ≥ 0`. Adversarial (10⁶
correntes×direções): mínimo **+0.174 > 0**. **O custo de núcleo análogo a `S` é PSD.**

### A4 — O Cauchy–Schwarz de SU(3) (repetição de SKYRME_DOMINANCE)
Esta é a generalização explícita pedida. O quártico líder do cosseno para SU(3) é
`−(a⁴/72) Tr((e·C)⁴)`. **Teorema do sinal (SD4) é independente do grupo:**
`Tr(X⁴)=Σ_k λ_k⁴ ≥ 0` para qualquer Hermitiana `X`, logo o quártico líder é
**≤ 0 sempre** (medido: máx adversarial **−1.6×10⁻²**, nunca positivo em 10⁶ testes).

Decomposição em operador simétrico e de Skyrme. Definindo `M = Σ_μ c_μ²` e o
operador de comutador `K = −Σ_{μν} Tr([c_μ,c_ν]²) ≥ 0`, a média isotrópica obedece
à identidade (verificada **exata**, erro 8×10⁻¹⁶):

$$\langle \mathrm{Tr}\,(e\cdot C)^4\rangle_{e\in S^2} \;=\; \tfrac{1}{15}\big(3\,\mathrm{Tr}\,M^2 \;-\; \tfrac12 K\big)\;\ge 0 \;\;\Longrightarrow\;\; \boxed{K \le 6\,\mathrm{Tr}\,M^2}.$$

Este é o análogo SU(3) da desigualdade `K ≤ ⅔S` de SU(2): a **constante muda**
(de `⅔` para a forma `K ≤ 6·TrM²`), mas a **conclusão é idêntica**. O termo de
Skyrme entra estabilizador (+) mas é limitado pelo simétrico, então o quártico
líquido nunca vira positivo. Configurações de referência (nomeadas, sem fit):

| Config | K | TrM² | K/TrM² | ⟨TrX⁴⟩ | quártico líq. |
|---|---|---|---|---|---|
| Abeliana (correntes paralelas) | 0 | 18 | 0 | 3.6 | < 0 |
| Hedgehog su(2)⊂su(3) (`c=λ₁,λ₂,λ₃`) | 48 | 18 | **8/3 = 2.667** | 2.0 | < 0 |
| máx busca aleatória (10³ configs) | — | — | 2.06 | — | < 0 |
| **limite rigoroso** | | | **6** | ≥ 0 | ≤ 0 |

O hedgehog su(2)-embutido é o probe extremal natural (mais não-Abeliano que as
correntes aleatórias, que se diluem nos 8 geradores): dá `K/TrM² = 8/3` exato —
acima da busca aleatória, ainda bem abaixo de 6 e com `⟨TrX⁴⟩ = 2 > 0`, ou seja
quártico líquido **negativo**, espelhando SU(2) ponto a ponto.

> **Nota importante (carregada para a Fase C, NÃO uma morte da Fase A).** Assim
> como em SU(2), a *dominância* de Skyrme não emerge do canal cosseno em SU(3):
> o quártico líder é estabilizador-negativo. Isso **não** viola a positividade da
> ação (A2/A3 mostram a ação PSD) — significa apenas que, como no setor de matéria
> SU(2), um custo de núcleo não-cosseno / termo estabilizador explícito será
> necessário para um defeito estável. A Fase C herda exatamente o mesmo último
> ingrediente externo já identificado em SKYRME_DOMINANCE. Estruturalmente, SU(3)
> não está nem melhor nem pior que SU(2) nesse ponto.

### A5 — Localidade causal preservada
Campo SU(3) atribuído às **relações de cobertura** (redução transitiva da relação
tipo-tempo) de sprinklings de Poisson em caixa 3+1D — a mesma topologia de rede de
SU(2). 12 sementes, ρ=80 (≈312 links/semente):

- **100,00%** dos links são relações tipo-tempo, futuro-dirigidas (`dt>0`,
  `dt²>|dx|²`) — fração causal mínima **1.0000** em todas as sementes. O campo não
  acopla nenhum par acausal.
- As menores plaquetas de um conjunto causal são **diamantes de 4 elementos**
  (`i→j→l`, `i→k→l`; o triângulo cordal não existe na rede reduzida) — ≈134
  diamantes/semente. A holonomia fechada `U_ij U_jl U_kl† U_ik†` está bem definida
  e usa **apenas** links causais.
- **Covariância de gauge:** sob transformações de sítio aleatórias `g_i`, a
  holonomia transforma `W → g_i W g_i†`, logo `s_p` é invariante — erro máx
  **8.9×10⁻¹⁶**. Isso prova que a ação é construída consistentemente a partir de
  links causais e respeita a simetria de gauge SU(3) local.

**Localidade causal preservada.**

---

## Síntese honesta da Fase A

```
FASE A (definição):
  Ação SU(3) positiva semi-definida?        SIM  (Wilson + sigma, A2/A3)
  Localidade causal preservada?              SIM  (100% causal + gauge, A5)

  [bônus] Teorema do sinal de Skyrme vale para SU(3)?  SIM (K ≤ 6·TrM²,
          quártico líder ≤ 0) — mesma estrutura de SU(2), constante diferente.
          NÃO é morte da Fase A; é a nota carregada para a Fase C.

[X] FASE A PASSA — SU(3) é definível nesta rede causal. O substrato de Poisson
    comporta SU(3) tão bem quanto SU(2). Prosseguir para a FASE B (ordenamento
    espontâneo / transição de fase) é justificado.
```

### O que isto significa para o programa
1. **Fronteira esclarecida:** a eventual barreira a "quarks da TEIC" **não** está
   na definição do campo — o substrato não distingue SU(2) de SU(3) no nível da
   ação/causalidade. Qualquer morte futura será dinâmica (B) ou topológica (C),
   não cinemática.
2. **Paralelo exato com o setor SU(2):** o teorema do sinal de SKYRME_DOMINANCE é
   **independente do grupo**. SU(3) herda o mesmo "último ingrediente externo"
   (custo de núcleo não-cosseno) — nem mais, nem menos. Isso é informação de alto
   valor: não há penalidade *extra* de SU(3) no canal quártico.
3. **Anti-circularidade mantida:** nenhum número de QCD entrou (sem massa de quark,
   sem σ, sem α_s). As matrizes complexas e `f,d` são a definição do grupo. A
   comparação com QCD fica reservada à Fase D.

## Nota sobre o guard de anti-circularidade (exceção principiada)
SU(2) foi carregado por **quaternions unitários** (uma álgebra de divisão *real*,
S³), então o setor de matéria nunca precisou de literais complexos — e o guard
`tests/test_no_circularity.py` proíbe `1j` em `results/matter/` justamente para
impedir a reinjeção de uma fase `e^{ikL}` "na mão". SU(3) **não tem esse atalho**:
o carregador mínimo fiel é genuinamente complexo (matrizes de Gell-Mann, o mapa
exponencial `exp(iX)`, as constantes de estrutura `f=(1/4i)Tr([λ_a,λ_b]λ_c)`).
Esses números complexos **são a definição do grupo de gauge**, não um mecanismo
que poderia fabricar a positividade da ação que a Fase A mede.

Foi adicionada ao guard uma exceção **rotulada e restrita**: literais complexos são
permitidos apenas dentro de blocos
`# SU(3) GROUP-DEF COMPLEX` … `# END SU(3) GROUP-DEF COMPLEX`
(quatro blocos em `su3_core.py`: Gell-Mann, `exp(iX)`, `f`, gaussiana de Haar).
Garantias verificadas por regressão:
- **todos os padrões de dilatação** (γ, `sqrt(1-β²)`, redshift de Schwarzschild)
  continuam proibidos **em qualquer lugar**, inclusive dentro desses blocos e de
  `su3_core.py` — testado: um γ inserido num bloco SU(3) ainda é pego;
- literal complexo **fora** de um bloco — em qualquer arquivo, `su3_core.py`
  incluído — continua sendo violação (testado);
- bloco não-terminado é sinalizado como erro (testado);
- **zero regressão**: o guard continua passando nos motores SU(2)/bridge
  existentes; `pytest tests/` → 4 passed.

## Próximo passo (aguardando confirmação)
**FASE B — ordenamento espontâneo:** Monte Carlo do campo SU(3) na rede, medir
`C(r)`, buscar `J_c(SU(3))` e caracterizar a(s) fase(s) ordenada(s). Critério de
morte da Fase B: nenhuma transição para fase ordenada em nenhuma região razoável
de parâmetros. **Não iniciar a Fase B antes do aval**, conforme o protocolo de
campanha por fases.

---

*Reprodução:* `python su3_core.py` (smoke tests do motor) e
`python FLA_definition.py` (os cinco portões → `FLA_definition.json`).
Determinístico (sementes fixas). numpy 2.4.4, scipy 1.17.1.

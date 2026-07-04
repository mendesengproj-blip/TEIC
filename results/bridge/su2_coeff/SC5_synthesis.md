# SC5 — Síntese honesta: Skyrme emerge?

> Fecha `BRIDGE_SU2_COEFF.md`. Veredito contra o pré-registro do charter
> (adendo técnico escrito antes de qualquer execução).

## Quadro de vereditos (do charter)

```
SC1 — Expansão analítica: quarta ordem é Skyrme?
  [x] PARCIAL — ambos presentes com coeficientes TRAVADOS:
      E⁽⁴⁾ = −(3a⁴/5760)·S + (a⁴/2880)·K   (K = Skyrme, sinal estabilizador)

SC2 — Teste numérico campo constante:
  [x] SKYRME — razão Poisson 0.55522±0.00030 (pred 5/9=0.55556);
      razão cúbica 1.0 exata (grade cega); critério de morte NÃO ativado

SC3 — Coeficiente c₄ constante:
  [x] SIM — c_K = a⁴/2880 (platô 0.06% em g→0; expoente 4.000);
      λ²_Sk = a²/120 (expoente 2.000) — comprimento de Skyrme = granularidade

SC4 — Derrick com c₄ emergente:
  [x] INSTÁVEL (cosseno sozinho) — E(λ) monotônica, sem mínimo interior;
      controle com Skyrme manual reproduz λ*=1.20 (pred 1.20) ✓

VEREDITO FINAL:
[ ] A — SKYRME EMERGE COM DOMINÂNCIA
[x] B — O OPERADOR DE SKYRME EMERGE; A DOMINÂNCIA NÃO
        (pré-registrado como o desfecho provável no adendo do charter)
[ ] C — SÓ SIMÉTRICO (morte)        [ ] D — INCONCLUSIVO (ruído)
```

## O que foi estabelecido (e é novo)

1. **O operador de Skyrme emerge do coarse-graining — e o mecanismo é a
   isotropia de Poisson.** A quarta ordem do cosseno de link SU(2), mediada
   sobre direções isotrópicas, contém $K=\sum|c_\mu\times c_\nu|^2$ com
   coeficiente positivo e travado ($+a^4/2880$; razão $K\!:\!S=+2:-3$ forçada
   pela isotropia, como as razões Stückelberg (1,2) de C2). **A grade cúbica é
   exatamente cega a $K$** (razão 1.0 a precisão de máquina) — é por isso que
   toda a literatura de rede (e a campanha MATTER_SU2) precisou adicioná-lo à
   mão. *O mesmo ingrediente que dá a invariância de Lorentz em R1 (Poisson, não
   grade) é o que gera o operador de Skyrme.* Isso liga Q1→Q6 do revisor.

2. **O limite U(1) unifica as campanhas.** Correntes colineares ⇒ $K=0$ ⇒ só o
   quártico simétrico negativo — exatamente o "quartic survives, sign<0 = DBI"
   de W2. A fórmula $-3S+2K$ tem W2 como o corte abeliano.

3. **A escala do estabilizador é a granularidade:** $\lambda_{\rm Sk}=a/\sqrt{120}$,
   sem parâmetro novo — mesma estrutura de escala única de $G\propto1/K$ (D3D),
   $m_A\propto\sqrt\rho$, $X_0\propto\rho$. Material direto para o Ataque 6.

4. **A fronteira honesta, agora energética:** isotropia trava $K\le\frac23S$ ⇒
   quártico líquido sempre negativo ⇒ **nenhuma medida isotrópica de um único
   cosseno estabiliza o Skyrmion** (SC4: monotônico; controle manual: mínimo
   interior ✓). O que falta não é o operador (existe, com o sinal certo) — é um
   mecanismo que suprima a saturação simétrica $-3S$ frente a $+2K$: um custo de
   núcleo não-cosseno. **É o mesmo "quarto ingrediente" que PHI_EMERGE V4
   localizou pela topologia (cos 2π=1); SC4 o localiza pela energética.** Duas
   campanhas independentes, mesma fronteira.

## O que muda no Paper II

Antes: *"o termo de Skyrme é o termo de menor dimensão compatível… fornecido
pelo comutador do grupo, mas não derivado da ação (1)."*

Depois (suportado por SC1–SC4): *"o **operador** de Skyrme é derivado: é a
quarta ordem do cosseno de link sob a média de Poisson, com coeficiente
$+a^4/2880$ travado pela isotropia e comprimento $\lambda_{\rm Sk}=a/\sqrt{120}$
fixado pela granularidade — um operador que medidas de rede regulares perdem
exatamente. O que permanece importado não é o operador, é sua **dominância**: a
isotropia trava $K\le\frac23 S$, o quártico líquido satura em vez de
estabilizar, e o custo de núcleo não-cosseno continua sendo o único ingrediente
de matéria genuinamente externo."*

Contagem de ingredientes do Paper II: **3 → 2** (SU(2) por minimalidade
[Ataque 5] + dominância/custo de núcleo; o termo de Skyrme deixa de ser
ingrediente independente). Não 3→1 como no melhor cenário — reportado como é.

## Reprodução

```
python SC1_expansion.py      # ~2 min (sympy)
python SC2_constant_field.py # ~1 min, 20 sementes
python SC3_coefficient.py    # ~2 min, 20 sementes
python SC4_derrick.py        # ~10 s, determinístico
```
Guard: `python tests/test_no_circularity.py` → PASSED (quaternions reais; sem
complexos; sem fórmulas de dilatação; Skyrme nunca inserido como alvo de fit).

# MG1_MATTER_SOURCES_GRAVITY — o Skyrmion como fonte DIRETA de gravidade

> **Charter PRÉ-REGISTRADO.** Critérios de morte ANTES de qualquer código.
> Item R2 do `RESEARCH_MAP.md` (FASE 3): a brecha central — e mais valiosa de fechar —
> do paper mais forte (`PAPER_MATTER_GRAVITY.tex`, Seção VII).
>
> **A brecha.** O paper estabelece θ=G_net·M/r como **composição de duas leis medidas
> separadamente**: (i) a resposta de Poisson, forma-independente, a um peso localizado
> genérico (verificada para 4 perfis estendidos: esfera, disco, NFW, exponencial), e
> (ii) o Skyrmion como tal peso (massa medida). MAS **o perfil de densidade de energia
> REAL do sóliton nunca foi usado como fonte literal**. O paper nomeia isto como
> "the natural next step." Status atual: [FRACO]/composição.
>
> **O que MG1 faz.** Compõe os dois motores existentes — o relaxador de gravidade BD
> (D1–D3, `results/bridge/dynamics/D3_MC.py`) e o perfil do Skyrmion
> (`results/matter/fl1/su3_core.py:radial_relax`) — usando a densidade de energia
> ε(r) do sóliton como a fonte literal s_i, e medindo se θ exterior ~ G_net·M/r.
> Motores existentes; só compor. Dados em `results/matter/mg/`. **NÃO modifica
> nenhuma campanha anterior.**

## A pergunta

O perfil de densidade de energia real do Skyrmion SU(2), usado como fonte literal no
relaxador BD, produz θ(r) = G_net·M/r — com expoente exterior −1 e amplitude linear
na massa PRÓPRIA do sóliton — com o MESMO G_net da fonte genérica?

## A construção

1. Perfil do sóliton: F(r) via `radial_relax(e_sk)`; densidade de energia radial
   ε(r) = dE/dr = 4π[ r²(F'²+2 sin²F/r²) + e_sk·sin²F·(2F'²+sin²F/r²) ];
   massa M = ∫ ε(r) dr = E2 + E4 (a massa medida do sóliton).
2. Fonte de gravidade: s_i = ε(r_i) por casca (densidade FÍSICA, **não** normalizada —
   um sóliton mais pesado = mais fonte), num grid radial que resolve o núcleo do
   sóliton E o exterior distante.
3. Relaxar θ sob a ação BD quadrática com conservação (Σθ_i V_i = 0), exatamente a
   ação de D3. [A ação é quadrática → o mínimo é a solução linear de Poisson; uso o
   solve linear exato, validado contra o Metropolis de D3 no gate G0.]
4. Ajustar θ = A/r + C no exterior; medir o expoente e a amplitude A.

## GATE (obrigatório antes da física)

```
G0. O solve linear exato da ação BD, com a MESMA fonte top-hat e os MESMOS parâmetros
    de D3 (D=3, K=1), reproduz o resultado de D3 (expoente −1; A>0; offset C de
    conservação negativo) dentro da tolerância. Se falhar → a implementação não
    representa a ação BD; PARAR.
```

## TESTES e CRITÉRIOS DE MORTE (pré-registrados)

```
M-EXPOENTE (a forma):
  Ajustar o expoente exterior de θ com a fonte = ε(r) do Skyrmion.
  MORTE: expoente ≠ −1 (fora de −1 ± 0.10) → o perfil concentrado do sóliton QUEBRA
         a resposta de Poisson exterior; a composição falha e a brecha é REAL.
  PASS:  expoente = −1 ± 0.10 (a forma 1/r é forma-independente, agora confirmada
         para o perfil próprio do sóliton, não só os 4 perfis estendidos).

M-LINEARIDADE (a amplitude ∝ massa):
  Varrer e_sk (≥4 valores) → massas M distintas (E2+E4) e perfis distintos; medir A.
  MORTE: A não é linear em M — G_net ≡ A/M varia > 15% (CV) na varredura → a amplitude
         não é a massa do sóliton; a ligação matéria→gravidade é só qualitativa.
  PASS:  G_net = A/M constante (CV < 15%) → a amplitude do poço É a massa própria.

M-GNET (o mesmo acoplamento):
  Comparar G_net(Skyrmion) com G_net de uma fonte top-hat de mesma massa M e núcleo.
  MORTE: G_net(Skyrmion) difere de G_net(top-hat) por > 15% → o acoplamento depende da
         forma da fonte (não é o G_net universal medido em D3/4 perfis).
  PASS:  concordam dentro de 15% → mesmo G_net, fonte-independente.
```

## VEREDITO

```
[FRACO]→[SÓLIDO]  se M-EXPOENTE, M-LINEARIDADE e M-GNET todos PASS:
                  o Skyrmion sourceia θ=G_net·M/r com seu PRÓPRIO perfil, forma 1/r,
                  amplitude = massa própria, mesmo G_net. A composição vira medição.
BRECHA REAL       se qualquer um falha: reportar honestamente que o perfil concentrado
                  do sóliton não se reduz à fonte genérica; a Seção VII permanece
                  [FRACO]/composição e o mapa registra a brecha como confirmada.
```

## ANTI-CIRCULARIDADE

Nenhuma fórmula relativística no gerador (a ação BD, a medida de casca r^{d-1} e o
acoplamento κ livre — nunca G; d=3 é input geométrico, como em D3). G, M, Schwarzschild
só em blocos COMPARISON ONLY. e_sk é o estabilizador externo declarado (FL1/SU2). O gate
G0 valida o solver contra o motor D3 antes de qualquer alegação. Sementes fixas; JSON
auto-descritivo.

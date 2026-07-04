# C5-2 -- Existe corrida dimensional genuina?

## O que se observa

D_s(s) sobe monotonicamente de ~0 (s pequeno / UV) ate um plateau em
D_s = 1.95 ~ MM (s grande / IR),
e depois cai por saturacao de tamanho finito. A questao decisiva: essa
subida 0 -> d e uma CORRIDA FISICA (geometria dependente de escala, como
em CDT) ou e o corte de discretude (a borda do espectro discreto)?

## Diagnostico 1 -- invariancia por refinamento (o teste decisivo)

Dobrando a densidade (N: 1000 -> 2000 -> 4000 no mesmo diamante), o
operador suavizado sonda escalas fisicas cada vez MENORES (localidade
fixa de ~1/eps elementos = comprimento fisico que encolhe). Se houvesse
uma escala fisica especial onde D_s muda (corrida genuina), refinar para
alem dela MUDARIA a curva.

- Espalhamento maximo de D_s entre as 3 densidades (janela resolvel): **0.071** (criterio de colapso < 0.2).
- A curva D_s(s) e portanto INVARIANTE POR REFINAMENTO: e o mesmo perfil
  de difusao discreta da variedade de Minkowski lisa, identico em todas
  as escalas (cada vez mais finas) sondadas. Isto e a assinatura de uma
  variedade LISA com uma UNICA dimensao, nao de corrida.

## Diagnostico 2 -- nao ha segundo plateau dimensional

- Procura por um plateau sub-d estavel (D_s plano e <= d - 0.3, como o plateau UV ~2 de CDT):
  NENHUM encontrado (0 decadas).
- A regiao sub-d NAO e um plateau: D_s sobe monotonicamente (sem regime
  estavel). O decaimento para 0 em s->0 e o limite generico de QUALQUER
  espectro discreto finito (log K ~ -sigma<lambda> => D_s -> 0), nao um
  segundo regime dimensional.

## Diagnostico 3 -- independencia de eps

Variando a escala de suavizacao eps (i.e. a localidade/nao-localidade do
operador), o plateau e a posicao do rolloff sub-d (marco s onde D_s=1)
ficam INALTERADOS na variavel adimensional s:

| eps | plateau D_s | s onde D_s=1 |
|---|---|---|
| 0.15 | 1.93 | 0.612 |
| 0.25 | 1.95 | 0.628 |
| 0.40 | 1.91 | 0.628 |

A regiao sub-d nao esta presa a nenhuma escala fisica do operador -- e a
borda espectral, nao uma nao-localidade fisica.

## Conclusao de C5-2

Nao ha corrida dimensional GENUINA. O unico plateau fisico e D_s = d =
MM; a variacao sub-d e o corte de discretude, invariante por refinamento
e por eps, sem plateau estavel. A rede causal de Poisson e LISA em todas
as escalas fisicas resolvidas -- NAO exibe o fenomeno de CDT.
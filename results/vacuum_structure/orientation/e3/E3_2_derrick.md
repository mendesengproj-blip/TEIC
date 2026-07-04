# E3-2 — Virial de Derrick na rede

> Charter: `E3_DEFECTS.md` (E3-2). Código: `E3_2_derrick.py`; motor:
> `e3_core.py`; dados: `E3_2_derrick.json`; figura: `E3_2_derrick.png`.

## O critério

Derrick: uma textura estática é estável só se E(λ) sob a transformação de escala
n⃗ → n⃗((x−c)/λ + c) tiver um **mínimo interior** em λ*≈1 — energia subindo tanto
na compressão (λ<1) quanto na dilatação (λ>1). E(λ) monotônico ou plano de um
lado = Derrick ativo/marginal, sem sóliton.

## Três medições

### D1 — E(λ), métrica plana, refinada (L=32,48,64)

A dilatação usa reamostragem **trilinear** (não vizinho-mais-próximo, que injeta
energia de gradiente espúria por subamostragem em λ>1).

```
        λ*    sobe na compressão (L)   sobe na dilatação (R)   mínimo interior?
L=32   0.85         +238%                    +4%                    NÃO
L=48   0.85         +230%                    +3%                    NÃO
L=64   0.85         +226%                    +3%                    NÃO
```

O perfil é assimétrico: **parede no λ<1** (compressão custa caro — o corte da
rede impede o colapso, mecanismo 1) e **platô plano no λ>1** (marginal — sem
força restauradora contra a expansão). Não há mínimo confinante: a parede de
compressão é o que regulariza a morte de Derrick, mas não estabiliza.

### D2 — Escala E vs L (livre de artefato)

```
E(hedgehog) = 7.672·L − 7.8     R²(linear) = 1.00000
```

E cresce **linearmente** com a caixa, R²=1 — o hedgehog O(3) 3D é
**marginal de escala**: não tem comprimento intrínseco (um sóliton genuíno
saturaria E a um valor finito). Esta é a medida decisiva e sem artefatos de
reamostragem.

### D3 — Curvatura induzida (mecanismo 2)

Peso radial w(x)=1+α/r (proxy COMPARISON-ONLY de métrica curva θ~M/r):

```
α= 3.0   sobe compressão +193%   sobe dilatação +3%   mínimo interior? NÃO
α= 6.0   sobe compressão +173%   sobe dilatação +2%   mínimo interior? NÃO
α=12.0   sobe compressão +151%   sobe dilatação +2%   mínimo interior? NÃO
```

A curvatura **não cria** mínimo interior. Pior: ela **enfraquece** a parede de
compressão (a subida cai de +238% para +151%), ou seja, torna a compressão mais
barata — levemente **desestabilizante** rumo ao colapso, não estabilizante.
**Mecanismo 2 não confirmado** com este proxy.

## Veredito E3-2

```
E(λ) tem mínimo interior?            NÃO (parede em λ<1, platô plano em λ>1)
Curvatura muda o resultado?          NÃO (não cria mínimo; enfraquece a parede)
E vs L marginal (linear)?            SIM (E=7.67·L, R²=1.00000)
```

Sem mínimo de Derrick. O defeito é marginal de escala; apenas a parede UV (rede)
impede o colapso. Confere com o **Cenário B (metaestável)** de E3-1: a
discretização regulariza, mas não estabiliza. A curvatura testada não fornece o
ingrediente que falta.

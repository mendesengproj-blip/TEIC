# FM1-3 — σ8 / S8 / f(z): DEV vs ΛCDM (teste decisivo da tensão S8)

> `FM1_3_sigma8.py` → `.{json,png}`. Baseline ΛCDM via CAMB (CLASS indisponível no
> host); crescimento DEV pela ODE de FM1-2. a₀ FIXO no valor SPARC (não ajustado ao
> CMB) ⇒ σ8_DEV é **previsão**.

## Resultado — Veredito C (critério de morte ACIONADO)

| Quantidade | ΛCDM (CAMB) | DEV (a₀=SPARC, s=½) | KiDS-1000 |
|---|---|---|---|
| σ8(z=0) | **0.811** | **101.0 ± 5.7** (num.) | — |
| **S8 = σ8√(Ωm/0.3)** | **0.831** | **103.5** | **0.766 ± 0.020** |
| Ωm | 0.315 | 0.315 | — |

```
σ8(z): DEV vs ΛCDM   (morte se DEV ≥ ΛCDM em todo z)
  z=0.0:  σ8_DEV=101.0   σ8_ΛCDM=0.811   DEV ≥ ΛCDM
  z=0.5:  σ8_DEV= 89.9   σ8_ΛCDM=0.624   DEV ≥ ΛCDM
  z=1.0:  σ8_DEV= 81.3   σ8_ΛCDM=0.492   DEV ≥ ΛCDM
  z=2.0:  σ8_DEV= 69.4   σ8_ΛCDM=0.338   DEV ≥ ΛCDM

f(z) em k=0.1 h/Mpc
  z=0.0: f_DEV=0.77  f_ΛCDM=0.53     (DEV cresce mais rápido)
  z=2.0: f_DEV=1.36  f_ΛCDM=0.96
```

**σ8_DEV ≥ σ8_ΛCDM em todo z testado ⇒ Veredito C** (critério de morte
pré-registrado). f(z)_DEV > f(z)_ΛCDM em todo z: a DEV **realça** o crescimento.

## Por que a DEV realça (e não suprime)

A DEV é tipo-MOND: μ(k,z) = G_eff/G_N ≥ 1. A aceleração peculiar de um modo linear
de densidade hoje é

$$g(k)\sim\frac{3}{2}\frac{\Omega_m H_0^2\,\delta}{a^2 k}\sim 3\times10^{-13}\ {\rm m/s^2}
\ \ll\ a_0=1.2\times10^{-10}\ {\rm m/s^2},$$

para TODAS as escalas que definem σ8 (g/a₀ ≈ 0.003–0.005). Ou seja, **todo modo
cosmológico linear está no regime MOND profundo** (consequência da coincidência
a₀≈cH₀/2π, verificada: cH₀/2π=1.04×10⁻¹⁰). Logo μ≫1 e o crescimento dispara.

Isto é a razão bem conhecida pela qual MOND **superproduz** estrutura sem um
setor tipo-matéria-escura no completamento relativístico. A narrativa do charter
("gravidade mais fraca nas bordas → cresce mais devagar → σ8 menor") tem o **sinal
errado** para MOND — registrado honestamente em FM1-1.

## Robustez (independente da interpolação)

A equação de crescimento `δ'' + (2+dlnH/dlna)δ' − (3/2)Ωm(a)·μ·δ = 0` é monótona em
μ: **qualquer μ ≥ 1 dá D_DEV ≥ D_ΛCDM ⇒ σ8_DEV ≥ σ8_ΛCDM.** Não depende da função
ν(y) escolhida nem do valor exato. Fechar a tensão S8 (σ8 **menor**) exigiria μ<1
em algum lugar — o que MOND **nunca** fornece. A morte é estrutural, não numérica.

- **σ8_DEV ≈ 101 é runaway** (a teoria linear quebra: δ_DEV entra no regime
  não-linear profundo). O valor absoluto não é uma previsão confiável; o **sinal e
  a direção são inequívocos** e é só isso que o critério de morte requer.
- **Erro numérico** (20 configurações de a_i, rtol, grade-k): ±5.7 em σ8_DEV —
  irrelevante frente ao excesso de ~100× sobre ΛCDM.
- **Sensibilidade a s** (½ vs 1, lei a₀(z)): ambos realçam (s maior → a₀(z) maior
  em z alto → ainda MOND profundo). Não muda o veredito.
- **Sinal de B_ε (E2):** no crescimento quase-estático (ω=0) a fonte e o operador
  trocam de sinal juntos; μ é invariante. σ8 idêntico para os dois sinais (FM1-1 §4).

## Conclusão

**A DEV não explica a tensão S8 — ela a piora.** Aplicada literalmente com a₀ de
SPARC, a modificação MOND realça o crescimento (σ8_DEV ≫ σ8_ΛCDM, S8_DEV ≫ KiDS),
acionando o critério de morte pré-registrado em todo z. **Veredito C.** A tensão S8
permanece não explicada pela DEV; o setor de galáxias (BTFR, kill-criterion ativo)
segue sendo o terreno válido da teoria.

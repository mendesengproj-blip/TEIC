# SD5 — Síntese honesta: a dominância de Skyrme pode emergir?

> Fecha `SKYRME_DOMINANCE.md`. Veredito contra o pré-registro do charter
> (adendo técnico escrito antes de qualquer execução).

## Quadro de vereditos (do charter)

```
SD1 — Identidade K ≤ S:
  [x] Identidade exata — e MAIS FORTE que a do charter: K ≤ (1−1/d)·S é
      identidade PONTUAL (Cauchy–Schwarz nos autovalores do Gram PSD),
      saturada pelo hedgehog; K ≤ ⅔S em d=3 não é efeito da média
      isotrópica, é geometria de qualquer configuração. Adversarial 10⁶
      configs + hill climb: nenhuma violação em d=2..6.

SD2 — Sêxtico em d=3:
  [x] c₆ > 0 mas insuficiente — o mínimo do truncamento existe SEMPRE
      (formal), mas em u(λ*)=8.0 ≫ 1, óctico/sêxtico=0.55, erro 42% vs
      cosseno completo, que é MONOTÔNICO (ressoma decide): artefato de
      truncamento de série alternante de função limitada.

SD3 — K/S varia com parâmetros:
  [x] K/S constante em ρ (2/5 exato em ρ=10..1000; isotropia de Poisson
      é exata em toda densidade) E cresce com d (1−3/(d+2) confirmado,
      d=1..8) mas o gap líquido (1+2/d)·S nunca fecha — nem em d→∞.
      r₄(B)/r₄(A) = 5/9 nas direções MEDIDAS de links causais reais.
      Causal vs tipo-espaço: κ₃ idênticos (0.4000 vs 0.4003).

SD4 — Curvatura como estabilizador:
  [x] f(R) ≠ 1 mas ineficaz — f = 1 + κRρ^{−1/2}, κ=0.0383 (colapso exato);
      R>0 alonga links e torna o quártico MAIS negativo (anti-estabilizador);
      TEOREMA DO SINAL: E₄ = −(a⁴/384)⟨|ℓ|⁴⟩ ≤ 0 sob QUALQUER medida —
      20 000 medidas patológicas, sup = −1.7e−13; núcleo hedgehog
      invariante de medida (−1/384 exato, spread 3e−15).
      Bônus: a isotropia já é o ÓTIMO do canal K (anisotropia só piora).

VEREDITO FINAL:

[x] MORTE TOTAL — na forma forte.
    Não "K ≤ ⅔S em todos os regimes testados": K ≤ ⅔S demonstrado como
    identidade pontual em d=3, e o sinal do quártico líquido demonstrado
    negativo para QUALQUER medida de links e QUALQUER configuração.
    O sêxtico não resgata (artefato de truncamento); a curvatura move c₄
    com lei limpa mas no sentido anti-estabilizador. Dominância não
    emerge — e agora se sabe POR QUÊ: não há regime a procurar.
    A afirmação honesta permanece: "o operador emerge, a dominância não."

[ ] MORTE PARCIAL   [ ] SUCESSO VIA SÊXTICO   [ ] SUCESSO VIA CURVATURA
```

## O que foi estabelecido (e é novo em relação a SC1–SC5)

1. **A fronteira virou teorema.** SC4 mediu "sem mínimo interior"; SD1+SD4
   demonstram que não poderia haver: (i) K ≤ (1−1/d)S pontual com saturação
   no hedgehog; (ii) 3S−2K ≥ (1+2/d)S > 0 em toda dimensão (a razão −3:+2 é
   d-independente); (iii) o sinal do quártico é da série do cosseno, não da
   geometria — vale sob qualquer medida. A busca por "algum regime da rede"
   tem resposta fechada: **o regime não existe no canal cosseno**.

2. **Três caminhos de fuga fechados com mecanismo identificado.**
   Sêxtico: positivo mas a ressoma (cosseno limitado) é monotônica — o mínimo
   truncado vive em u=8, fora de qualquer validade. Curvatura: move ⟨a⁴⟩ com
   κ=0.038 mas multiplica os dois canais juntos e para R>0 piora. Densidade:
   inerte por simetria exata (e a previsão SC2 de 5/9 agora está verificada
   em links causais de sprinklings reais, não só na medida idealizada).

3. **A isotropia de Poisson é o ótimo do operador de Skyrme.** A razão
   −c_K/c_S é máxima (2/3) exatamente na medida isotrópica e cai sob
   anisotropia axial em qualquer direção. O mesmo ingrediente que gera o
   operador (SC2) já o gera na intensidade máxima possível — não havia nada
   a otimizar.

4. **Quatro números desemaranhados** (eram conflacionados no charter):
   5/9 = razão de resíduos SC2; 2/3 = saturação pontual (hedgehog);
   2/5 = fração de canal cruzado por link em d=3; 1/2 = idem 4 componentes.

## O que muda no Paper II

Seção "derivado vs assumido", linha Skyrme — de "a dominância não foi
encontrada" para "a dominância é estruturalmente inalcançável":

> "The Skyrme operator emerges as the fourth-order term of the SU(2) Wilson
> action under Poisson-isotropic averaging, with locked coefficient a⁴/2880
> (SC1–SC3). Its dominance, however, cannot emerge: K ≤ (1−1/d)S is an exact
> pointwise identity (Cauchy–Schwarz on the PSD current Gram), saturated by
> the hedgehog itself, and the net quartic −(a⁴/384)⟨|ℓ|⁴⟩ is negative under
> *any* link measure — curved, anisotropic, or discrete — because its sign
> descends from the cosine series, not from geometry. Higher orders do not
> rescue: the sextic minimum lies at link phase u ≈ 8, where the alternating
> series fails and the resummed (bounded) cosine is monotonic. Skyrmion
> stability therefore requires one external assumption — a non-cosine core
> cost — which is the last external input in the matter sector, now located
> by an impossibility argument rather than by a null search."

A fronteira fica **mais forte, não mais fraca**: um ingrediente importado com
teorema de necessidade é melhor ciência do que um ingrediente importado com
busca infrutífera. Paper III (Estrutura Inevitável) ganha o complemento: a
mesma isotropia que força os operadores também trava sua hierarquia.

## Artefatos

| arquivo | conteúdo | reprodução |
|---|---|---|
| `SD1_identity.py/.json` + `SD1_analysis.md` | identidades pontuais, adversarial, 4 números | `python SD1_identity.py` (~2 min) |
| `SD2_higher_order.py/.json/.png/.md` | c₆ exato, mínimo truncado vs ressoma | `python SD2_higher_order.py` (~1 min) |
| `SD3_ratio_scan.py/.json/.png/.md` | κ(d), sprinklings ρ=10..1000, 5/9 medido | `python SD3_ratio_scan.py` (~3 min) |
| `SD4_curvature.py/.json/.png/.md` | teorema do sinal, f(R), anisotropia | `python SD4_curvature.py` (~2 min) |

Guard: `python tests/test_no_circularity.py` → PASSED (aritmética real;
Skyrme nunca alvo de fit; kill criteria nos docstrings antes de rodar).

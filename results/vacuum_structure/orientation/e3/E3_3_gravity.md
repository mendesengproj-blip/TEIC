# E3-3 — Campo gravitacional do defeito (θ ~ M/r ?)

> Charter: `E3_DEFECTS.md` (E3-3). Código: `E3_3_gravity.py`; motor:
> `e3_core.py`; dados: `E3_3_gravity.json`; figura: `E3_3_gravity.png`.

## O que se verifica

Como E3-1 mostrou o defeito **metaestável** (sobrevive na escala de relaxação),
testa-se se ele fonte um campo θ(r)~M/r ao redor — a assinatura que D3 encontrou
para uma massa localizada. Nenhuma lei de gravidade é inserida.

Método: relaxar o hedgehog (L=48) por gradiente; medir o perfil de densidade de
energia ρ(r); formar a massa contida M(r)=∫₀ʳ ρ·4πr′²dr′; resolver a Poisson
radial para o potencial induzido θ(r); testar o campo longe ~ M/r.

## Resultados

```
ρ(r) ~ r^p :   p = −1.956     (hedgehog contínuo: −2)               ✔
M(r) ~ r^q :   q = +1.056     (partícula localizada: q→0 saturando;
                               marginal: q~1)                        ✗ não localiza
θ vs 1/r   :   R² = 0.995 na janela externa, amplitude A = −33.2
```

- A densidade de energia cai como **1/r²** (p=−1.96), exatamente o hedgehog.
- O potencial induzido θ(r) **ajusta-se a 1/r** na janela medida (R²=0.995).
- **MAS** a massa contida M(r) cresce como **r** (q=1.06) e **não satura** — a
  "massa" do defeito é não-localizada (diverge com a caixa, como E∝L em E3-2).

## Veredito

```
θ ~ M/r com M finita?   PARCIAL
```

O campo *parece* 1/r localmente porque ρ~1/r² de uma textura marginal produz
naturalmente um perfil 1/r na janela — mas como M(r) não satura, **não há um
M/r assintótico verdadeiro**. O defeito nu não gravita como uma partícula
localizada: ele não tem massa finita para fontear um campo de longo alcance
bem-definido. Resultado consistente com a marginalidade de escala (E3-2) e com a
metaestabilidade (E3-1) — o ingrediente que daria massa localizada (escala
intrínseca, p.ex. termo de Skyrme) está ausente do ferromagneto nu.

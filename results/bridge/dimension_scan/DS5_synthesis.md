# DS5 — Síntese: d=3 é selecionado por consistência?

> Fecha `DIMENSION_SCAN.md`. Veredito contra as previsões pré-registradas no
> charter (tabela escrita antes de qualquer execução).

## A tabela final (medida vs pré-registrada)

| d | DS1 perfil | DS2 órbitas (ligado/escape) | DS3 Derrick | DS4 carga topológica | consistente? |
|---|---|---|---|---|---|
| 1 | **+0.99** (linear, confinante) ✓pred | — | ✗ | — | ✗ |
| 2 | **−0.12±0.05** (log-degenerado) ✓pred | ✓ / **✗** (V(∞)=∞) ✓pred | ✗ (marginal) ✓pred | **0** (desenrola suave) ✓pred | ✗ |
| 3 | **−0.95±0.05** ✓pred | **✓ / ✓** ✓pred | **✓ única** (λ* interior) ✓pred | **ℤ** (B salta, barreira ×1.86 sob refino) ✓pred | **✓ ÚNICA** |
| 4 | **−2.00±0.10** ✓pred | ✗ (±2% → colapso/escape) / ✓ ✓pred | ✗ (colapso) ✓pred | sem inteiro (π-classes, Paper II) | ✗ |
| 5 | (analítico −3) | ✗ | ✗ (ambos encolhem; **sêxtico não resgata**) ✓pred | sem inteiro | ✗ |

**Critério de morte:** NÃO ativado — nenhum d≠3 passa nas quatro pernas;
d=3 passa em todas. **Veredito: A.**

## A afirmação, no tamanho certo

> Na rede causal, a mesma lei dinâmica (`Lθ=J`) produz em cada d o potencial
> p=−(d−2) — medido, não imposto. Sobre esses potenciais medidos: d=2 prende
> tudo (sem escape), d=4 não orbita nada (sem estruturas ligadas), e só d=3
> tem os dois. No setor de matéria: só 2<d<4 tem janela de Derrick (d=3 único
> inteiro) e só d=3 tem carga topológica inteira protegida (a barreira é
> medida: B salta com pico divergente sob refino; em 2D o mesmo objeto
> desenrola suavemente). **d=3 não é escolhido: é a única dimensão em que o
> universo da rede contém simultaneamente gravitação útil e matéria estável.**

## O que isto NÃO é (honestidade obrigatória)

1. **Não é atrator dinâmico.** Nada aqui mostra a rede *evoluindo* para d=3
   (isso é o Tier 3 do roadmap, via dimensão MM de causets crescidos no e7).
   É seleção por exclusão/consistência antrópico-estrutural: as alternativas
   são internamente consistentes como geometrias, mas vazias de física
   (sem órbitas OU sem escape OU sem matéria).
2. **Os argumentos têm ancestralidade** (Ehrenfest 1917 para órbitas; Derrick
   1964 para sólitons). O que é novo aqui não é o argumento — é que **as
   premissas são medidas na rede** (o expoente p=−(d−2) emerge do Laplaciano
   de grafo sobre Poisson sem ansatz; a janela de Derrick é computada no
   funcional E₂/E₄ que SC1 derivou do cosseno; a barreira π₃ é energética e
   cresce sob refino), e que as quatro pernas fecham **no mesmo substrato,
   com o mesmo protocolo anti-circular**.
3. **A perna DS3 pressupõe o ingrediente de núcleo** (a dominância do quártico
   que SC4 mostrou não emergir do cosseno). A seleção dimensional é: *dado* o
   único ingrediente de matéria externo, só d=3 funciona. Sem ele, nenhum d
   tem matéria — a fronteira de SC4/V4 fica intacta.
4. DS1 d=2: log vs potência rasa é indistinguível em caixa finita (classe
   qualitativa robusta; suficiente para DS2).

## O que muda nos papers

**Paper I, Open Questions (2)** sobe de *"the spatial dimension d=3 is input;
its dynamical selection is not addressed"* para: *"d=3 is input to each
simulation, but it is not arbitrary: scanning d∈{1,2,4,5} with the same
dynamical law and the same anti-circular protocol, d=3 is the unique dimension
supporting simultaneously long-range gravity with both stable bound orbits and
escape (measured exponents p=−(d−2)), a Derrick stability window, and a
protected integer topological charge. The dynamical selection (an attractor
mechanism) remains open."*

**Resposta à Q2 do revisor:** de "entrada pura" para "única dimensão
consistente — exclusão estrutural medida, atrator em aberto". É o "Nível 1
parcial" do mapa: não o atrator, mas muito mais que entrada.

## Reprodução

```
python DS1_profiles.py    # ~3 min (CG sobre 100k pontos em d=4)
python DS2_orbits.py      # ~30 s (lê DS1_profiles.json)
python DS3_derrick.py     # ~20 s
python DS4_topology.py    # ~2 min (grades 61³/81³)
```
Guard: `python tests/test_no_circularity.py` → PASSED (sem 1/r^{d−2}, sem
fórmula de órbita/Newton nos geradores; fits e classificações na análise).

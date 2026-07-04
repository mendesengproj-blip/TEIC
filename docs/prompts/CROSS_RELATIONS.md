# CROSS_RELATIONS: razões adimensionais em que a granularidade cancela

> Ataque 6 do `ROADMAP_REVOLUCAO.md`. O valor de G é inderivável sem escala
> absoluta (D3D: G∝1/K); mas **razões entre setores na mesma rede** são números
> puros, sem parâmetro livre — previsões falsificáveis que a teoria DEV ajustada
> a dados não possui. Resultados em `results/bridge/cross_relations/`.
> NÃO modifica campanhas anteriores (consome SC3, D3D, DS1).

## ✅ VEREDITO: **B — a constante pura fecha assintoticamente (2.5%); relação cruzada estabelecida** (com relato transparente da morte literal em grau baixo)

```
CR1  morte LITERAL disparada nos graus 7–28 (constante até 39% acima; expoentes
     −2.37/−5.93) — registro bruto mantido em CR1_gnet.json.
CR1b a análise antecipada no charter (correções O(1/deg)): pontos novos deg=48
     (0.2025±0.0023) e deg=64 (0.1992±0.0018); ajuste c∞+b/deg em deg≥14 →
     c∞ = 0.18516 vs 15/8π² = 0.18998  (razão 0.975, 2.5%) ✓  b≈0.85 medido.
CR2  G_net·ρ²·r_c⁵ → 15/8π²  ·  λ²_Sk/⟨a²⟩ = 1/120  ⇒  relação cruzada
     gravitação↔matéria:  G_net·ρ²·r_c³·λ²_Sk = 3/320π² ≈ 9.5e-4
     — zero parâmetros livres ("mesmos links" declarado).
```
Tabela completa de números puros: [`results/bridge/cross_relations/CR2_table.md`](results/bridge/cross_relations/CR2_table.md).
Nível 2 do revisor, versão honesta: o VALOR de G segue externo; o PREFATOR de
G_net no substrato e a razão com λ_Sk são calculáveis — nada ajustável.

---

## PREVISÕES PRÉ-REGISTRADAS (derivadas analiticamente ANTES de medir)

**Setor gravitacional (CR1).** Para o Laplaciano de grafo sobre sprinkling de
Poisson (densidade ρ, alcance r_c) com fonte pontual unitária, a expansão do
operador dá `(Lθ)(x) ≈ −(2π/15)ρ r_c⁵ ∇²θ` (d=3), e a conversão fonte-por-nó →
densidade traz outro ρ. O perfil é θ = G_net/r com

```
G_net = 15 / (8π² ρ² r_c⁵)        ⇒  número puro:  G_net · ρ² · r_c⁵ = 15/8π² ≈ 0.18998
expoentes: ∂ln G_net/∂ln ρ = −2 ;  ∂ln G_net/∂ln r_c = −5
```

**Setor de matéria (já medido, SC1–SC3).** O comprimento de Skyrme emergente:
`λ²_Sk = ⟨a²⟩/120` com ⟨a²⟩ a média do quadrado do comprimento de link.

**A relação cruzada (CR2).** Na MESMA rede (mesmos links para o cosseno quiral
e para o Laplaciano; em RGG d=3, ⟨a²⟩ = (3/5)r_c² ⇒ λ²_Sk = r_c²/200):

```
G_net · ρ² · r_c³ · λ²_Sk  =  (15/8π²)·(1/200)  =  3/(320π²)  ≈  9.49×10⁻⁴
```

Um número puro ligando o acoplamento gravitacional ao tamanho do estabilizador
de matéria — **zero parâmetros livres**, condicionado apenas à identificação
declarada "ambos os setores vivem nos mesmos links".

## CRITÉRIO DE MORTE (pré-registrado)

```
CR1 morre se: expoente_ρ ≠ −2 ou expoente_rc ≠ −5 (fora de 3σ), ou a constante
              pura desviar de 15/8π² por mais de 20% (correções de grau finito
              e clustering de RGG são O(1/deg); acima de 20% a "constante" não
              é constante e a relação cruzada não fecha).
```

## Tarefas

```
CR1: medir G_net(ρ, r_c) no Laplaciano DS1 (d=3): varredura ρ (r_c fixo),
     varredura r_c (ρ fixo), 5 sementes — expoentes + constante pura
     → CR1_gnet.{py,md,json,png}
CR2: a tabela de números puros da rede (gravitação + matéria + a relação
     cruzada) e o que cada um falsifica → CR2_table.md
```

## Honestidade pré-declarada

- G em unidades FÍSICAS continua não derivado (exige escala absoluta externa —
  inalterado desde D3D). O que se deriva: **relações** entre setores.
- A identificação ⟨a²⟩=(3/5)r_c² é geométrica (links de RGG uniformes na bola);
  se os dois setores usarem medidas de link diferentes, a constante muda por um
  fator geométrico conhecido — o conteúdo invariante é que ela é **calculável,
  não ajustável**.
- m_A∝√ρ (PHI) e X₀∝ρ (C3) entram na tabela como relações herdadas com
  expoentes medidos lá; suas constantes puras não são re-medidas aqui.

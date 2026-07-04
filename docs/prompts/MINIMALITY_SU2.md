# MINIMALITY_SU2: a rede exige SU(2), ou o pesquisador escolheu?

> Ataque 5 do `ROADMAP_REVOLUCAO.md`. Formaliza e fecha numericamente a cadeia de
> eliminação que responde Q7 do revisor. Resultados em `results/bridge/minimality/`.
> NÃO modifica nenhuma campanha anterior (reusa V4, CR_3D, MATTER_SU2, SC1–SC4).

## ✅ VEREDITO: **cadeia fechada — SU(2) é o mínimo consistente** (todas as previsões pré-registradas batem; mortes NÃO ativadas)

```
MIN1  cegueira universal U(1): fluxo geométrico 2π EXATO no núcleo; elemento de
      grupo W = 0 EXATO; custo de núcleo = 0 EXATO para 1−cos(nW), n=1,2,3 e
      série aleatória de 6 harmônicos → o loophole de V4 está fechado: NENHUMA
      função de classe U(1) pinta o núcleo. B (SU(2)) é índice de VOLUME, não
      holonomia — estruturalmente imune.
MIN2  grupos discretos: projeção do hedgehog em Q8/2T colapsa B (0.958→0.05/0.08)
      e converte a energia em paredes (razão 61³/41³ = 1.62/1.50 ≈ 61/41=1.49;
      suave: 1.02) → sem matéria pontual discreta.
MIN3  cadeia (1)–(5) completa: escalar livre (P1) → discretos (MIN2) → U(1)
      (CR_3D+MIN1) → SU(2) (MATTER_SU2+DS4+SC1) → maiores desnecessários (Bott).
```
Síntese: [`results/bridge/minimality/MIN3_chain.md`](results/bridge/minimality/MIN3_chain.md).
Q7: "o pesquisador escolheu SU(2)?" → "a exigência de matéria pontual com carga
conservada escolheu; cada elo da eliminação é medido."

---

## A cadeia de eliminação (o teorema a fechar)

```
exigências MEDIDAS:  matéria = objeto PONTUAL estável em d=3 (DS3/DS4)
                     com carga conservada (CR/V4: criação exige proteção topológica)

(1) grupos triviais/sem estrutura  → sem carga: escalar livre deslocaliza (P1, medido)
(2) grupos DISCRETOS (qualquer ℤ_n, Q8, 2T, …)
    → textura contínua impossível: mapa contínuo S³→conjunto discreto é constante
    → MIN2 mede: projeção do hedgehog em subgrupo discreto colapsa B e vira
      PAREDES DE DOMÍNIO (energia diverge sob refino)
(3) U(1) (o grupo abeliano contínuo mínimo)
    → π₃(S¹)=0: sem sóliton pontual; o objeto é o VÓRTICE (linha, CR_3D — medido)
    → e o núcleo do vórtice é CEGO: V4 mediu para 1−cos W; MIN1 fecha o loophole
      dos harmônicos: QUALQUER função do ELEMENTO DE GRUPO U(1) é 2π-periódica
      no fluxo → custo de núcleo ≡ 0 para toda a classe (teorema + medição)
(4) SU(2) → menor grupo de Lie compacto conexo NÃO-abeliano (dim 3);
    π₃(SU(2))=ℤ (B=1 medido, MATTER_SU2; barreira medida, DS4);
    a carga B NÃO é holonomia de loop (é índice de volume det(c_x,c_y,c_z)) —
    a cegueira de cossenos estruturalmente NÃO se aplica a ela
(5) acima de SU(2): todo grupo de Lie compacto conexo não-abeliano contém um
    subgrupo SU(2) (ou SO(3)); π₃(G)=ℤ para todo G simples compacto (Bott).
    SU(2) é o de DIMENSÃO MÍNIMA — qualquer outro é SU(2) + estrutura extra.
```

## CRITÉRIOS DE MORTE (pré-registrados)

```
MIN1 morre se: existir harmônico/combinação f(W) (função do elemento de grupo)
              com custo de núcleo ≠ 0 no vórtice de fluxo 2π.
MIN2 morre se: a projeção em subgrupo discreto preservar B≈1 com energia
              convergente sob refino (i.e., matéria pontual discreta possível).
```

## PREVISÕES PRÉ-REGISTRADAS

- **MIN1:** fluxo geométrico (soma não-enrolada) ao redor do núcleo = 2π exato
  (o winding EXISTE); W como elemento de grupo = 0 exato no núcleo; custo
  f(W_core) = 0 para f ∈ {1−cos W, 1−cos 2W, 1−cos 3W, série aleatória de 6
  harmônicos} — zero EXATO, não pequeno.
- **MIN2:** hedgehog suave: B≈0.95 (51³, erro de discretização conhecido ~4%),
  E₂ convergente (razão 61³/41³ ≈ 1.0±0.1). Projetado no grupo binário
  tetraédrico 2T (24 elementos) e em Q8 (8): |B| < 0.2 (não-inteiro/colapsado)
  e E₂ de parede crescendo ∝ 1/dx (razão 61/41 ≈ 1.49±0.15).

## Tarefas

```
MIN1: teorema da cegueira universal U(1) + varredura de harmônicos
      → MIN1_blindness.{py,md,json}
MIN2: hedgehog projetado em Q8 e 2T: B e E₂ sob refino 41³→61³
      → MIN2_discrete.{py,md,json,png}
MIN3: síntese da cadeia (1)–(5) com os resultados existentes referenciados
      → MIN3_chain.md
```

## O que isto NÃO afirma (honestidade)

- Não deriva SU(2) dinamicamente (a rede não "evolui para" SU(2)); estabelece
  que SU(2) é o **mínimo consistente** com matéria pontual estável — a mesma
  lógica de exclusão do DIMENSION_SCAN, agora no espaço de grupos.
- Não remove a fronteira de SC4 (dominância/custo de núcleo continua externo).
- π₄(SU(2))=ℤ₂ (o pré-requisito do spin-½) vem de graça com SU(2), mas o FR
  continua teorema aplicado (Paper II §VII; Ataque 7 do roadmap).

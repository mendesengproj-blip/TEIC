# SÍNTESE — B3 ∥ B4 · O fóton: 2-célula magnética a baixa curvatura

> Campanha FOTON_B3B4 (Fase 2, Frente B, caminho crítico do fóton). Pré-registro:
> `PRE_REGISTRO.md`. Drivers: `b3_future_cone.py`, `b4_anisotropic.py`. jun/2026.
> **Veredito: B3 = CANDIDATO (precisa de follow-up de invariância de gauge, NÃO é
> ainda o fóton); B4 = MORTE (artefato de coordenada exposto pelo controle). O fóton
> magnético no causet permanece [FRONTEIRA]; nenhum charter de paper novo é congelado.
> Disciplina anti-circularidade pegou um falso-positivo em cada direção.**

---

## 1. Lacuna e contexto

E6/E6b/E6c localizaram a lacuna: o 2-complexo de **diamantes causais** (as plaquetas
que o operador BD de gauge realmente usa) é ~100% elétrico no causet plano; a curvatura
isotrópica abre o setor magnético **só no regime Planckiano** (E6c: frac_B 0.0026 plano
→ 0.0117 a R̂=2; **<0.01 a baixa curvatura R̂≥8**). B3 e B4 testaram as duas alavancas
restantes a **baixa curvatura** (R̂≫1, universo observável).

## 2. B3 — células de intersecção de cones futuros: CANDIDATO (caveated)

Construção nova: célula ancorada num **par spacelike** (i,j incomparáveis) com ápices
no futuro comum (i,k,j,l), vs o diamante ancorado num par **timelike**.

| construção | frac_B (N=1500) | Wilson-lo |
|---|---|---|
| gate timelike (controle) | **0.000** | — (elétrico, como E6b ✓) |
| **spacelike (B3)** | **0.836** | 0.830 |
| **null (ápices aleatórios)** | **0.614** | 0.607 |

- **Gate passa:** células timelike são elétricas (0.000), reproduzindo E6b.
- **frac_B = 0.84** a baixa curvatura, N-estável — muito acima de 0.01.
- **Controle de tautologia (decisivo):** o null com ápices **aleatórios** (mesma base
  spacelike) dá **0.614** — gap 0.22 > 0.05, então o futuro-comum causal **importa**
  (não é tautologia pura). **MAS** ~61% do frac_B é o **piso cinemático** de ancorar
  numa base spacelike (a diagonal i–j é spacelike → b2>e2 por geometria). Só ~22 pontos
  percentuais vêm da estrutura causal.

**Veredito B3: SUCCESS_B3_CANDIDATE.** Há um setor magnético genuíno (a estrutura
causal contribui além do piso cinemático), mas **não é o fóton ainda**: (1) ~3/4 do
efeito é o piso cinemático da base spacelike; (2) **invariância de gauge não testada**
(critério pré-registrado); (3) essas células **não são** os diamantes que o operador BD
usa — seriam um **novo** complexo de gauge proposto, não uma correção do existente.
**Antes de qualquer paper:** verificar (i) que as células formam um 2-complexo conexo e
(ii) uma ação gauge-invariante. Promissor, registrado como candidato, **não congelado**.

## 3. B4 — de Sitter anisotrópico: MORTE (artefato de coordenada)

Anisotropia controlada a baixa curvatura (R̂=8), a=H_1/H_perp ∈ {1,2,4,8}:

| a | frac_B | b_plane(12,13) | b_plane(23) |
|---|---|---|---|
| 1 (gate isotrópico) | 0.0032 | 1.5 | 1.594 |
| 2 | 0.158 | 8.8 | 1.594 |
| 4 | 0.475 | 231 | 1.594 |
| 8 | 0.579 | **99425** | **1.594** |

- **Gate passa:** a=1 dá frac_B=0.0032 (= E6c isotrópico a baixa curvatura, <0.01 ✓).
- frac_B **sobe** com a anisotropia (0.003→0.58) e cruza 0.01 — o que ingenuamente
  pareceria SUCCESS.
- **Controle de artefato de coordenada (decisivo):** o conteúdo magnético nos planos
  **esticados** (12,13, que contêm x_1) explode **×6×10⁴**, enquanto o plano **não
  esticado** (23) fica **fixo (×1.00)**. Assinatura inequívoca: é o fator de escala do
  embedding e^{(a-1)Hτ} inflando A^{1j} — **rescalar um eixo de coordenada** tilta os
  bivetores trivialmente para ele.

**Veredito B4: DEATH_B4_COORD_ARTIFACT.** A implementação (anisotropia no **embedding**
com **ordem causal isotrópica** fixa) confunde um **stretch de coordenada** com
anisotropia física. Uma B4 **fiel** exigiria a anisotropia na **própria ordem causal**
(cones de luz dependentes de direção, Bianchi-I genuíno), que quebra o truque
conformal-flat de E6c e é uma campanha maior. Como implementada, a Direção A **não** abre
o setor magnético.

## 4. Veredito conjunto

O fóton magnético no causet permanece **[FRONTEIRA]**. Nenhuma das duas alavancas
forneceu um setor magnético limpo a baixa curvatura:
- B3 forneceu um **candidato** real mas dominado pelo piso cinemático e com gauge não
  testado — promissor, não conclusivo.
- B4 forneceu um **falso-positivo** que o controle expôs como artefato de coordenada.

**Nenhum charter de paper novo é congelado.** O Paper Photon-Arc mantém o setor de
gauge como **fronteira documentada**. As duas direções **não estão esgotadas** no
sentido forte: B3 tem um follow-up bem-definido (gauge-invariância + 2-complexo), e B4
tem uma versão fiel não tentada (anisotropia na ordem causal). Ambos registrados como
**follow-ups**, não mortes definitivas.

## 5. Disciplina anti-circularidade (o ponto alto desta campanha)

Os dois resultados crus eram **espetaculares e falsos** (frac_B 0.84 e 0.58, ~70–180×
o E6c). Em ambos, um **controle pré-pensado** (null de ápices em B3, plano não-esticado
em B4) expôs a contaminação: B3 parcialmente cinemático, B4 totalmente artefato de
coordenada. Sem os controles, esta campanha teria "congelado um charter de paper de
fóton emergente" sobre um artefato — exatamente o pecado que o programa existe para
evitar. **Os controles são a ciência; os números crus eram a armadilha.**

## 6. Limitação honesta

- B3: N≤1500, ápices = 2 primeiros do futuro comum (proxy de "primeira camada"); um
  esquema de camada-mínima mais rigoroso e o teste de gauge-invariância ficam para o
  follow-up.
- B4: a anisotropia fiel (ordem causal Bianchi-I) não foi tentada (custo: cones de luz
  direcionais em 4D, sem o atalho conformal). Registrada como campanha maior.

## 7. Anti-circularidade

Gate A1 verde sobre `b3_future_cone.py` e `b4_anisotropic.py`. Bivetores são geometria
de embedding real (sem fase e^{ikL}); ordem causal é a do sprinkle; frac_B medido, c/ω
não entram. Gates de redução (timelike→elétrico, isotrópico→E6c) verdes.

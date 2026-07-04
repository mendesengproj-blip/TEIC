# PRE-REGISTRO — B3 ∥ B4 · O fóton: 2-célula magnética spacelike a baixa curvatura

> Campanha de organização TEIC (Fase 2), Frente B, caminho crítico do **fóton**
> (Paper Photon-Arc). B3 e B4 rodam em **paralelo** (testam direções diferentes da
> mesma lacuna). Gate A1 já VERDE. Fontes: §B3/B4, E6/E6b/E6c
> (`results/gauge/e6*`). Pré-registro antes de rodar.

---

## 1. Lacuna (precisamente localizada)

O 2-complexo de diamantes causais de um causet Poisson **plano** não carrega 2-células
spacelike (magnéticas): diamantes height-2 são **100% elétricos** (frac_B=0.0000 exato),
height-3 dá uma cauda não-crescente ~0.25% (E6b). E6c mostrou que a **curvatura
espacial** abre o setor magnético, MAS **só no regime Planckiano**: frac_B cresce
monotônico 0.0026 (Minkowski) → **0.0117 a R̂=2** (Planckiano), cruzando 0.01 **apenas**
em R̂≈2; a baixa curvatura (R̂≥8, regime do universo observável) fica **~0.003 ≪ 0.01**.
Altura (E6b), curvatura isotrópica (E6c/e) e acoplamento (E6d) estão **esgotados** a
baixa curvatura. Restam **exatamente** duas alavancas não testadas:

## 2. As duas direções

**B3 (Direção B):** uma **construção de 2-célula nova** — o bivetor de área das
**intersecções de cones de luz futuros** de eventos distintos, em vez de diamantes
height-2. Intuição física: um diamante i→{a,b}→k é dominado pela extensão **timelike**
i–k (elétrico); uma célula ancorada num **par spacelike** (i,j incomparáveis) com um
ápice comum no futuro k tem **base spacelike** → o bivetor pode adquirir conteúdo
magnético A^{ij} O(1). Célula B3 = (i, j, k, l): i,j incomparáveis (spacelike), k,l no
**futuro comum mínimo** de ambos; bivetor do quadrilátero classificado por
`polygon_bivectors` (REUSADO verbatim de E6).

**B4 (Direção A):** sprinkle de Sitter **anisotrópico** (Bianchi-I,
ds²=−dτ²+Σ e^{2H_i τ}dx_i², H_1≠H_2=H_3) — a anisotropia eleva frac_B a baixa
curvatura? Há **direção preferencial**? Adapta `e6c_curved_core.desitter_sprinkle`.

## 3. Critério de sucesso (pré-registrado verbatim)

**fB > 0.01 a baixa curvatura** (R̂≫1, regime do universo observável), **N-estável**,
**gauge-invariante** (Wilson-lo > 0.01 com significância) — i.e. a 2-célula spacelike
existe **fora** do regime Planckiano onde E6c a achou marginal.
- B3: numa construção de cone-futuro (qualquer curvatura, incl. plano).
- B4: fB cresce mensuravelmente com a anisotropia E cruza 0.01 a baixa curvatura, com
  dependência clara na direção preferencial.

## 4. Critério de morte

- **B3:** fB ≤ 0.01 a baixa curvatura em toda construção de cone-futuro testada → a
  intersecção de cones futuros **também** é eletricamente dominada; Direção B junta-se a
  altura/curvatura/acoplamento como alavanca esgotada.
- **B4:** fB permanece <0.01 a baixa curvatura para toda anisotropia testada (só sobe no
  regime Planckiano, como a curvatura isotrópica de E6c) → Direção A esgotada.

Se **ambas** morrem: o fóton magnético no causet fica **[FRONTEIRA]** limpo; o
Paper Photon-Arc mantém o setor de gauge como fronteira documentada (não submete claim
de fóton emergente). Se **qualquer** der fB>0.01 a baixa curvatura: é "o resultado mais
publicável do programa" → congela charter de paper novo (fóton emergente real).

## 5. Gates obrigatórios (anti-circular)

- **B3:** a célula de cone-futuro deve **reproduzir** o split E/B no limite onde degenera
  (par causal com futuro comum = diamante) — frac_B plano ~ E6b. Construção sem fase
  inserida (bivetor é geometria de embedding, real).
- **B4:** anisotropia **zero** deve reproduzir E6c isotrópico (frac_B(R̂) bit-compatível).
- Ambos sob a guarda A1 (gauge varrido; o bivetor não pode injetar e^{ikL}).

## 6. Protocolo

1. **B3:** `causal_link_graph` (E6); para pares incomparáveis (i,j) com ≥2 eventos no
   futuro comum mínimo, formar célula 4-vértice (i,k,j,l); `polygon_bivectors` → e2,b2;
   frac_B = #(b2>e2)/P, Wilson CI; N-scan; medir a **baixa curvatura** (plano + R̂≥8).
2. **B4:** estender `desitter_sprinkle` com H anisotrópico; varrer anisotropia
   a=H_1/H_perp ∈ {1,2,4,…} a R̂ fixo baixo (≥8); frac_B vs a; direção preferencial
   (b2 por plano espacial).
3. Veredito por §3/§4. Custo ~3–7 CPU-dias cada (geometria de cones 4D) — escopo a
   tamanho desktop, reportando teto N honestamente.

## 7. Entregáveis

`b3_future_cone.py`, `b4_anisotropic.py`, `b3b4.json`, `SYNTHESIS.md`; atualização do
RESEARCH_MAP (linha fóton/E6) e nota Photon-Arc (charter novo ou [FRONTEIRA]).

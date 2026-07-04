# PREDICTIONS — o setor falsificável da TEIC (Ataques 3+4 do roadmap)

> **Language note (EN).** The falsifiable-predictions ledger, kept in Portuguese as
> the working language of the research record. The `docs/…` and `results/…` files
> it references ship in this repository.

> Executa os dois primeiros ataques do roadmap interno: (3) o mapa
> operadores-proibidos ↔ exclusões observacionais e (4) a promoção da previsão
> arriscada com forecast quantitativo. NÃO modifica nenhuma campanha anterior.
> Resultados no arquivo de pesquisa (`results/predictions/`). Responde Q3, Q4 e
> Q10 do revisor.

## Quadro

```
ATAQUE 3 (OP1 — operadores ↔ observações):
  Selecionados {P(X)/DBI, Stückelberg, Proca, Maxwell}: acoplamento mínimo
    → c_T = c estrutural → sobrevivem a GW170817 (|c_g/c−1| ≤ 5×10⁻¹⁶)
  Proibidos: Horndeski G4X/G5 (soldering)  ⟷ executados por GW170817 (4× PRL 119, 2017)
             frame fixo n^μ (Poisson LI)   ⟷ executado por Fermi-LAT (E_QG,1 > 7.6 E_Pl)
  R1 (grade 17% vs Poisson 0.8%) = contraparte microscópica do limite de Fermi-LAT
  → "Por que Poisson?" (Q1) vira afirmação observacional: é a discretização sobrevivente única
  VEREDITO: a seleção interna da rede coincide com a seleção observacional — nos dois sentidos

ATAQUE 4 (F1 — forecast da previsão arriscada):
  Δlog v_flat = ¼ log[H(z)/H₀]  vs  ΛCDM = 0
  z=1.0: sinal +0.061, teto sistemático (σ_sys=0.04) = 1.5σ  ← explica a tensão ~1.6σ atual
  z=2.0: sinal +0.118, com σ_sys=0.02 → 5.9σ alcançável com N≈9 galáxias
  VEREDITO: gargalo é SISTEMÁTICO, não estatístico; janela decisiva z≥2, a≲a₀, σ_sys≤0.03
```

## As três previsões falsificáveis (para o paper)

1. **A arriscada (única exclusiva da camada EFT):** rotadores ricos em gás de baixa
   massa a z≥2 giram **mais rápido** a massa bariônica fixa, Δlog v=¼log[H/H₀].
   ΛCDM prevê zero. Kill criterion pré-registrado em `F1_forecast.md` (N≥25, z≥2,
   a≲a₀, σ_sys≤0.03 dex, Δlog v≤0 ⇒ falsificada). O teste mata um dos dois lados.
2. **c_T = c exatamente, para sempre** (LISA/ET): qualquer desvio confirmado falsifica
   a seleção de operadores da rede — não há botão para acomodar.
3. **Dispersão de vácuo de fótons nula na média** (CTA/LHAASO): qualquer dispersão
   sistemática ∝E/M_Pl falsifica a discretização de Poisson (e R1 com ela). Distingue
   TEIC/CST de Hořava e LQG-com-dispersão. Compartilhada com CST — dita como tal.

## O que isto responde ao revisor

- **Q3 (previsão observacional?)** — três, acima, com instrumentos nomeados.
- **Q4 (diferença vs RG?)** — em ondas gravitacionais e dispersão: *nenhuma*, e isso é
  previsão rígida da rede (não acidente); na dinâmica galáctica a alto-z: Δlog v>0.
- **Q10 (previsão mais arriscada?)** — F1, com o número exato de galáxias que decide.
- **Q1 (por que Poisson?), parcial** — sobrevivente observacional única (OP1 §3);
  a origem *dinâmica* segue em aberto (Tier 3 do roadmap).

## Honestidade

- OP1 itens 1–2 são **pós-dições** (GW170817 é de 2017); o valor está na rigidez: a
  lista proibida vem de razões internas (causalidade, Poisson, soldering), não de
  ajuste pós-2017. O conteúdo para frente são as previsões 2–3.
- A previsão 1 herda a₀∝H(z) da camada fenomenológica (DEV), não da geometria (C3
  fechou a₀∼cH). Falsificação de F1 mata o setor galáctico, não R1–R4.
- A ameaça interna da LIV O(1) do setor vetorial (E/B≈3) foi **executada e desarmada**
  (`LIV_VECTOR.md`): sem referencial preferido na rede (covariância medida, LV2); a
  violação é artefato da expansão quadrática sob regulador de caixa, ressomada pela
  ação global (defeito 0.98→0.003, LV4). A previsão 3 (dispersão nula na média) agora
  apoia-se em covariância *medida*, não conjecturada. Resíduo aberto (12%, controlado
  por densidade, não volume) documentado com kill honesto em LV4b.

## Documentos

| arquivo | conteúdo |
|---|---|
| `results/predictions/OP1_operator_map.md` | mapa completo operadores ↔ limites, com fontes verificadas |
| `results/predictions/F1_forecast.{py,json,png,md}` | forecast reprodutível + kill criterion |

Reproduzir: `python results/predictions/F1_forecast.py` (determinístico, ~5 s).
Guard inalterado: `python tests/test_no_circularity.py` (este charter só adiciona
análise e um script de comparação sob `results/`).

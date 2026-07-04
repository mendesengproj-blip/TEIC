# FL1_SU3_FOUNDATION — SU(3), Cor e o Caminho para Quarks

> Campanha de **fundação por fases** (não um experimento único). Pergunta: SU(3),
> "cor" e "confinamento" podem emergir da MESMA rede causal de Poisson que já
> produziu SU(2) (o Skyrmion)? Motor próprio `results/matter/fl1/su3_core.py`
> (matrizes 3×3 + Gell-Mann; não reutiliza `su2_core`/`orientation_core`; reusa só
> `causal_core`). Resultados e vereditos por fase em `results/matter/fl1/`.

## ✅ VEREDITO GERAL: **SUCESSO TOTAL (A+B+C+D)**

A rede causal de Poisson hospeda SU(3) tão bem quanto SU(2): ferromagneto de cor +
Skyrmion de cor + confinamento + bárion + octeto de mésons + duas torres espectrais,
tudo emergente do mesmo substrato. Relatórios:
[A](results/matter/fl1/FLA_definition.md) ·
[B](results/matter/fl1/FLB_ordering.md) ·
[C](results/matter/fl1/FLC_confinement.md) ·
[D](results/matter/fl1/FLD_synthesis.md).

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO, POR FASE)

```
FASE A morre se: nenhum campo SU(3) estável é definível sem violar a positividade
  da ação ou a localidade causal.
FASE B morre se: SU(3) é definível mas o vácuo nunca ordena espontaneamente.
FASE C morre se: vácuo ordena mas nenhum defeito topológico estável emerge, OU
  o defeito existe mas E(r) não cresce com a separação (sem confinamento).
Cada fase só prossegue se a anterior não morrer. Parar e reportar em qualquer
morte — não torcer a definição para sobreviver.
```

## FASE A — Definição do campo SU(3) na rede causal → **PASS**
Generaliza n⃗∈S² (SU(2)) para U∈SU(3) (8 geradores de Gell-Mann). Verifica:
positividade da ação mínima de plaqueta (Cauchy–Schwarz de SKYRME_DOMINANCE para
SU(3)) e localidade causal. **Resultado:** 5 portões passam; o teorema do sinal é
independente do grupo (`K ≤ 6·TrM²`, análogo a `K≤⅔S` em SU(2)) — a dominância de
Skyrme não emerge sozinha, mesma conclusão estrutural de SU(2) (não é morte de A;
nota carregada para C). [FLA_definition.md](results/matter/fl1/FLA_definition.md).

## FASE B — Transição de fase / ordenamento → **PASS**
Protocolo de E1 (Monte Carlo, C(r), busca de J_c) para o campo principal-chiral
SU(3). **Resultado:** vácuo ordena espontaneamente ("ferromagneto de cor", quebra
SU(3)×SU(3)→SU(3)_diag); J_c≈2.65 (cúbico), ≈0.3 (substrato causal); ordem de longo
alcance C_long=m² (Mermin ~2%). Ordem da transição **inconclusiva em L≤12**, reportada
honestamente (dip de Binder ↔ 1ª ordem; χ_max∝N^0.72 + histograma unimodal ↔
contínua). [FLB_ordering.md](results/matter/fl1/FLB_ordering.md).

## FASE C — Defeitos topológicos / confinamento → **PASS**
Espaço de vácuo ≅ SU(3); π₁=π₂=0, **π₃(SU(3))=ℤ → Skyrmion de cor**. Protocolo
E3/E3b (gradiente + térmico). Estabilizador de Skyrme **externo declarado** (Fase A
provou a não-emergência). **Resultado:** Skyrmion de cor estável (B=+1 inteiro,
Derrick-estável, robusto a ruído térmico) E **confinamento** — V(r)~σr medido (setor
de gauge de Wilson), σ>0 com σ(β) decrescente (liberdade assintótica).
[FLC_confinement.md](results/matter/fl1/FLC_confinement.md).

## FASE D — Síntese e conexão com o programa → **SUCESSO**
- **D1 massa:** bárion de cor = hedgehog SU(2) embutido → degenerado; M≈154 bate com
  MATTER_SU2 (146–207).
- **D2 píon:** 8/8 modos de Goldstone gapless (ΔE∝k², ω∝k) = **octeto pseudoescalar
  de mésons** — fecha a lacuna de C3-4 ("o píon não existia").
- **D3 Regge vs Casimir:** duas torres — bárion = rotor de Casimir (m²∝J(J+1),
  herdado de C3); tubo de fluxo confinante = corda de Regge (α'=1/(2πσ), do σ medido).
- **D4 Polaris:** píon agora realizado; tamanho ~ξ; completa C3-4.
[FLD_synthesis.md](results/matter/fl1/FLD_synthesis.md).

---

## PROTOCOLO E ANTI-CIRCULARIDADE
1. Campanha por fases; parar honestamente em qualquer morte; kill criteria no
   docstring de cada gerador antes de rodar; sementes fixas; JSON auto-descritivo.
2. **Nenhum número de QCD** (massas, σ, α_s, hádrons) entra em A–C; usados SOMENTE
   em D para comparação **qualitativa**, em blocos `COMPARISON ONLY`.
3. **Ingredientes externos declarados:** termo de Skyrme (`e_sk`, herdado de SU(2)
   via Fase A); escala da rede não derivada (tudo em unidades de rede).
4. Motor próprio `su3_core.py`; o guard `tests/test_no_circularity.py` ganhou uma
   exceção **rotulada e restrita** para os literais complexos estruturais de SU(3)
   (Gell-Mann, exp(iX), constantes de estrutura, log) — padrões de dilatação
   continuam proibidos em todo lugar; zero regressão.

*Reprodução:* `python results/matter/fl1/run_all.py [quick|full]`.

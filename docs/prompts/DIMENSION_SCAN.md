# DIMENSION_SCAN: d=3 é selecionado por consistência?

> Ataque 2 do `ROADMAP_REVOLUCAO.md`. Testa a conjectura: **d=3 é a única dimensão
> espacial em que a rede suporta simultaneamente gravitação de longo alcance com
> órbitas estáveis E matéria topológica pontual estável.** Resultados em
> `results/bridge/dimension_scan/`. NÃO modifica nenhuma campanha anterior.
>
> **Enquadramento honesto, declarado já no charter:** isto é seleção por
> EXCLUSÃO/consistência, não atrator dinâmico (o atrator é Tier 3 do roadmap).
> Se fechar, a resposta a Q2 do revisor sobe de "entrada pura" para "única
> dimensão consistente com os dois setores que a rede deriva".

## ✅ VEREDITO: **A — d=3 é a única dimensão consistente** (todas as previsões pré-registradas confirmadas; morte NÃO ativada)

```
DS1  perfil emergente p=−(d−2) MEDIDO sem ansatz:
     d=1: +0.99 (linear) · d=2: −0.12 (log-degen.) · d=3: −0.95 · d=4: −2.00
DS2  órbitas no potencial medido: d=2 ligado SEM escape; d=4 escape SEM ligado
     (±2% → colapso/escape); d=3 ÚNICO com os dois
DS3  janela de Derrick = {3} (d=2 marginal, d=4 colapso, d=5 sêxtico não resgata;
     cosseno monotônico em todo d — consistente com SC4)
DS4  mesma família de deformação: 2D desenrola suave (π₂=0); 3D B salta 1→0 com
     pico ×1.86 sob refino 61→81 (π₃=ℤ medido como barreira energética)
```
Síntese: [`results/bridge/dimension_scan/DS5_synthesis.md`](results/bridge/dimension_scan/DS5_synthesis.md).
Não é atrator dinâmico (Tier 3); é exclusão estrutural com premissas **medidas
na rede**. Paper I OQ(2): de "entrada pura" → "única dimensão consistente".

---

## CRITÉRIO DE MORTE (pré-registrado)

```
A conjectura morre se QUALQUER d ≠ 3 passar nas QUATRO pernas simultaneamente,
ou se d = 3 falhar em QUALQUER perna.
Em particular: se d=4 tiver órbitas ligadas estáveis no potencial MEDIDO da rede,
ou se a janela de Derrick contiver d=4, ou se d=2 tiver carga topológica inteira.
```

## PREVISÕES PRÉ-REGISTRADAS (antes de rodar)

| d | DS1 perfil emergente | DS2 escape / órbitas estáveis | DS3 janela Derrick (2<d<4) | DS4 carga π_d(S³) |
|---|---|---|---|---|
| 1 | linear (confinante) | não / — | não | — |
| 2 | log (confinante) | **não** / sim (tudo ligado) | marginal (E₂ inv. de escala) | **0** (desenrola suave) |
| 3 | **r⁻¹** | **sim / sim** | **✓ única** (λE₂+λ⁻¹E₄) | **ℤ** (B=1, barreira) |
| 4 | r⁻² | sim / **NÃO** (instável) | não (E₄ inv. de escala → colapso) | ℤ₂ (sem inteiro) |
| 5 | r⁻³ (analítico) | sim / não | não | ℤ₂ |

- **DS1 (gravidade):** relaxar `Lθ=J` (Laplaciano de grafo sobre sprinkling de
  Poisson em bola d-dimensional, fonte pontual + compensação de caixa, SEM ansatz)
  e medir o expoente do perfil. Previsto: −(d−2) para d≥3; log em d=2; linear em
  d=1 (d=3 já estabelecido por D1–D3: −1.02). Nota honesta: usa o Laplaciano de
  grafo (não o operador BD por-dimensão, pesado); D3B já mostrou que Poisson é a
  lei genérica do setor em d=3 — aqui a pergunta é só a dependência em d.
- **DS2 (órbitas no potencial MEDIDO):** integrar órbitas-teste no θ(r)
  interpolado de DS1 (leapfrog, sem fórmula de Newton no gerador). Critério
  físico (Ehrenfest): órbitas circulares estáveis exigem d<4; escape exige
  potencial →0 no infinito (d≥3). **d=3 = único com ligado-estável E escape.**
- **DS3 (Derrick em d):** quadratura radial do hedgehog generalizado
  (E₂~λ^{d−2}, E₄~λ^{d−4}): mínimo interior com quártico dominante sse 2<d<4
  → d=3 único inteiro. Cosseno completo (coeficientes travados de SC1): SEM
  mínimo em nenhum d (a saturação é independente de d — pré-registrado).
  Checar honestamente a rota sêxtica (+x⁶/720 do cosseno) em d=5: prever que
  não estabiliza (3S−2K>0 domina antes).
- **DS4 (topologia):** a MESMA família de deformação U_s aplicada em 2D e 3D:
  em 2D (π₂(S³)=0) o hedgehog desenrola suavemente até o vácuo (E(s) limitada);
  em 3D (π₃=ℤ) a tentativa cruza uma configuração singular: B(s) salta 1→0 com
  pico de energia divergente — a barreira topológica é medida, não citada.

## Tarefas

```
DS1: perfil θ(r) emergente, d ∈ {1,2,3,4}, 10 sementes  → DS1_profiles.{py,md,json,png}
DS2: órbitas no potencial medido, d ∈ {2,3,4}           → DS2_orbits.{py,md,json,png}
DS3: janela de Derrick, d ∈ {2,3,4,5}, cosseno + manual → DS3_derrick.{py,md,json,png}
DS4: barreira topológica 2D vs 3D (mesma família U_s)   → DS4_topology.{py,md,json,png}
DS5: síntese — a tabela d×pernas, veredito              → DS5_synthesis.md
```

## Protocolo

1. Anti-circularidade: nenhum `1/r^{d−2}`, nenhuma fórmula de órbita/Newton no
   gerador; expoentes e comparações só no bloco de análise. Guard deve passar.
2. As previsões da tabela acima NÃO podem ser ajustadas após os primeiros números.
3. Sementes fixas; JSON auto-descritivo; figuras por tarefa.
4. Veredito final: A (d=3 único nas quatro pernas) / B (d=3 único em ≥3 pernas,
   exceção documentada) / C (alguma d≠3 passa em tudo — morte da conjectura).

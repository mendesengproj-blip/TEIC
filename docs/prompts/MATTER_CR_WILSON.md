# MATTER_CR_WILSON — Confinamento via Plaquetas e Criação de Matéria Estável

> Testa se o termo de Wilson `S_W = λ_p Σ[1−cos(W_p)]` confina a carga de gauge e
> estabiliza kinks criados em colisão.
> Continua após `MATTER_CR_GAUGE.md` (transferência θ→φ até 57%, kink existe, gargalo
> é a estabilização).
> **Não modifica** R1–R3, e6–e11, D1–D3, M1–S1, CC*, CR*, DBI*, GAUGE*.
> Código e resultados: `results/matter/cr_wilson/`.

---

## O que CR_GAUGE deixou aberto

CR_GAUGE mostrou: Stückelberg transfere até 57% ao gauge (G2), o kink estável existe
com massa 8 (G4), pares virtuais transientes existem (G4), carga conservada (G5). O
**gargalo**: a energia que chega ao gauge vira **radiação** — o kink criado não
sobrevive, a carga se dispersa por falta de **confinamento**.

A ação mínima completa adiciona o termo de Wilson (plaqueta):

```
S = Σ_links Δτ[1−cos(φ+Δθ)]  +  λ_p Σ_plaq [1−cos(W_p)]
        Stückelberg (testado)          Wilson (não testado em colisão)
```

com `W_p = φ^x_{i,j} + φ^y_{i+1,j} − φ^x_{i,j+1} − φ^y_{i,j}` (uma rede espacial **2D**;
x = eixo de colisão, y = transverso periódico). CR_WILSON testa: com λ_p ativo, a carga
criada fica confinada antes de virar radiação?

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| W1 | Ação completa: 4 limites (λ_p=0→GAUGE, pure gauge, kink m=8, conservação)? | `W1_wilson.{py,md,json}` |
| W2 | Tensão de corda E(d): λ_c onde E(d)∝d? | `W2_string.{py,md,json,png}` |
| W3 | Colisão com Wilson: kink estável? (λ_p×ρ, 20 sementes) | `W3_collision.{py,md,json,png}` |
| W4 | Massa, θ(r)~M/r, E²=(pc)²+(mc²)²? | `W4_mass.{py,md,json}` |
| W5 | Mapa de fase (λ_p, ρ) | `W5_phasediagram.{py,md,json,png}` |
| W6 | Síntese + veredito (A–D) | `W6_synthesis.md` |

---

## Protocolo

1. **Anti-circularidade:** QCD, quarks, glúons, confinamento de cor só em COMPARISON
   ONLY. W_p é fase real acumulada nos links; σ é fit de E(d). Sem números complexos,
   sem fórmula de dilatação SR/GR.
2. **W1 obrigatório:** quatro verificações antes de W2–W6 (parar se falhar).
3. **λ_c de W2 antes de W3.**
4. **20 sementes para W3.**
5. **Funcional de energia corrigido de DBI4** para a massa.

## Vereditos

```
A — Matéria estável criada (M=8, τ∝M, θ~M/r, E²=(pc)²+(mc²)², Q=0)
B — Pares virtuais estabilizados (semi-estável)
C — Wilson confina mas colisão insuficiente
D — Sem transição no regime testável → física adicional necessária
```

---

## RESULTADOS

<!-- VERDICT_BLOCK_START -->

| Tarefa | Resultado | Grade |
|--------|-----------|-------|
| W1 — ação completa | VALIDADO (λ_p=0→GAUGE exato, pure gauge/Maxwell, kink m=8 intacto, E conservada) | A |
| W2 — tensão de corda | NÃO há corda linear (2D estático = Coulomb/BKT; λ_c op.=1.0) | C |
| W3 — colisão c/ Wilson | kink NÃO estabilizado; λ_p SUPRIME a sobrevivência | D |
| W4 — objeto suportado | CONSISTENTE (m=8.00≈8, E²=(pc)²+(mc²)², θ~M/r) mas não criado | — |
| W5 — mapa de fase | MAPEADO (sem janela cooperativa; criação só λ_p≈0, ρ alto) | — |

**Veredito: D — sem transição no regime testável.** A ação completa `S=Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` (rede 2D) **suporta** matéria
relativística completa (W4: kink m=8.00≈8, `E²=(pc)²+(mc²)²` com
1/√(1−v²) emergente, `θ(r)~M/r`, carga conservada) — cinco consistências fecham
para o objeto suportado. **Mas não o cria nem confina por colisão:** o termo de
Wilson é sub-dominante à rigidez herdada (W2: vórtices Coulomb/BKT, sem corda
linear), e aumentar λ_p **suprime** o núcleo criado (W3/W5: sobrevivência decresce
com λ_p, sem janela cooperativa). Razão física: U(1) compacto 2D não confina
winding via plaqueta **estática** — o confinamento linear (Polyakov) é dinâmico
(monopólos), exige dimensão maior ou campo externo. A fronteira está mapeada com
precisão. Ver `results/matter/cr_wilson/W6_synthesis.md`.

<!-- VERDICT_BLOCK_END -->

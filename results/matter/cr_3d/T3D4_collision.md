# T3D4 — Colisão com a ação completa 3+1D (teste central)

Colisão de CR_WILSON (W3) refeita na teoria de campo **genuinamente 3D** cujo
vácuo magnético é um plasma de monopólos (T3D2) e cujo potencial estático é
linearmente confinante para λ_p ≲ 1.5 (T3D3). Duas cadeias escalares contra-
propagantes (θ alto, gauge frio) colidem em x com ruído transverso (para a
estrutura criada não ser uniforme, que teria W_p=0). λ_p × ρ, 20 sementes.

Como T3D2/T3D3 mostram que o regime confinante é **λ_p pequeno** (acoplamento
inverso), varremos essa janela {0, 0.5, 1.0, 1.5, 3.0}; λ_p=0 reproduz CR_GAUGE.

| λ_p | ρ | n_kink | vida | sobrev | E_g/E | ρ_M criado | ⟨P⟩ ini | ⟨P⟩ fim | W_xy |
|-----|---|--------|------|--------|-------|-----------|---------|---------|------|
| 0.00 | 10 | 0.00 | 0.00 | 0% | 0.044 | 0.000 | 0.265 | 0.282 | +0.00 |
| 0.00 | 18 | 0.05 | 0.19 | 15% | 0.067 | 0.155 | 0.097 | 0.272 | +0.35 |
| 0.00 | 50 | 4.55 | 1.00 | 100% | 0.042 | 0.441 | 0.032 | 0.042 | -2.65 |
| 0.50 | 10 | 0.00 | 0.00 | 0% | 0.046 | 0.000 | 0.265 | 0.280 | -0.00 |
| 0.50 | 18 | 0.05 | 0.34 | 30% | 0.077 | 0.057 | 0.098 | 0.194 | -1.30 |
| 0.50 | 50 | 4.35 | 1.00 | 100% | 0.047 | 0.429 | 0.033 | 0.050 | +0.15 |
| 1.00 | 10 | 0.00 | 0.00 | 0% | 0.045 | 0.000 | 0.264 | 0.282 | -0.00 |
| 1.00 | 18 | 0.05 | 0.47 | 55% | 0.080 | 0.008 | 0.098 | 0.151 | -0.05 |
| 1.00 | 50 | 2.05 | 0.97 | 100% | 0.052 | 0.317 | 0.032 | 0.053 | +7.20 |
| 1.50 | 10 | 0.00 | 0.00 | 0% | 0.043 | 0.000 | 0.264 | 0.290 | +0.00 |
| 1.50 | 18 | 0.05 | 0.46 | 50% | 0.082 | 0.001 | 0.098 | 0.165 | -0.35 |
| 1.50 | 50 | 0.45 | 0.75 | 90% | 0.055 | 0.202 | 0.031 | 0.076 | -3.15 |
| 3.00 | 10 | 0.00 | 0.00 | 0% | 0.040 | 0.000 | 0.263 | 0.285 | -0.00 |
| 3.00 | 18 | 0.10 | 0.54 | 55% | 0.086 | 0.000 | 0.097 | 0.206 | -0.05 |
| 3.00 | 50 | 0.30 | 0.65 | 80% | 0.059 | 0.016 | 0.032 | 0.070 | -1.15 |

## Leitura

- **Criação em alta energia (ρ=50):** estrutura persistente é criada — n_kink ≈ 2–4.5, **sobrevivência 100%** na janela tardia (λ_p ≲ 1.0), carregando um **plasma de monopólos que a própria colisão gera** (ρ_M até 0.44). Em 2D (CR_WILSON, grade D) **nada** era criado.
- **Wilson estende a vida** em energia intermediária (ρ=18): lifetime cresce 0.19 → 0.54 quando λ_p vai de 0 a 3.
- **λ_p grande suprime o núcleo multi-estruturado** em ρ=50 (sobrevivência cai para 80–90%, n_kink cai) — a mesma supressão transversa vista em 2D.
- **Polyakov ⟨P⟩ não faz transição limpa** durante a colisão: ⟨P⟩ é **baixo** onde a estrutura densa se forma (confinado) e **alto** onde não há estrutura (livre), mas é fixado pela densidade de energia, não por um chaveamento dinâmico desconfinado→confinado (polyakov_drop=False).
- **Winding** em vários planos é grande e ruidoso (W_xy de −2.6 a +7.2) — vórtices múltiplos / campo de gauge turbulento, não um sóliton único limpo.

## Veredito T3D4: grade **B** — estrutura criada, semi-estável (vida finita)

A colisão 3+1D **cria** estrutura topológica semi-estável rica em monopólos (o mecanismo que 2D não tinha), mas o objeto é um blob multi-núcleo turbulento, não um sóliton único limpo, e o Polyakov não chaveia dinamicamente. Criação **sim**; estabilização limpa de uma única partícula **ainda não** — falta o que fixa o núcleo (Higgs/condensado, ver T3D5/T3D6).

![colisão](T3D4_collision.png)

# FN4_MOND_SCREENING — Blindagem MOND em r < λ_A = 17.3 pc — teste com Gaia

> Campanha de cosmologia/falsificação. Calcula o perfil de **MOND blindado** previsto
> pela DEV abaixo do comprimento de correlação do vetor massivo m_A,
> λ_A = ℏ/(m_A c) = 17.3 pc (de FM2/SCALE_BOUNDARY), e confronta com binárias largas
> do Gaia DR3 (Chae+2023, arXiv:2309.08160).
> Resultados em `TEIC/results/cosmology/fn4/`.
> **NÃO modifica nenhuma campanha anterior** (consome λ_A de FM2 e a₀ do Paper I).

---

## Contexto — a previsão exclusiva

FM2/SCALE_BOUNDARY identificaram λ_A = 17.3 pc como o comprimento de
Compton/correlação do campo vetorial m_A. O mecanismo:

- **r ≫ λ_A** (galáxias, kpc): o condensado de m_A é coerente → **MOND ativo** (a RAR
  do Paper I, calibrada em 167 galáxias SPARC, opera normalmente).
- **r ≪ λ_A** (binárias largas, sub-pc): abaixo do comprimento de correlação a EFT do
  modo coletivo (a "fônon" do condensado) deixa de valer → o reforço MOND é
  **blindado** → **gravidade newtoniana**.

Fator de blindagem (turn-on do MOND acima da correlação):

$$g_{\rm DEV}(r) = g_N(r)\,\Big[1 + \big(\nu_{\rm eff}(r)-1\big)\,S(r)\Big],
\qquad S(r) = 1 - e^{-r/\lambda_A}.$$

**Nenhuma versão de MOND padrão faz esta previsão**: Milgrom ativa MOND em TODA escala
onde g < a₀. A DEV a desliga abaixo de 17.3 pc. Diferença testável AGORA.

### Duas correções de fórmula em relação ao texto original do charter (documentadas, não para fugir de número)

1. **Sinal da blindagem.** O texto-fonte escrevia o reforço como `e^{-r/λ_A}` e dizia
   "r ≪ λ → e^{-∞} → Newton", o que é o limite trocado (`e^{-r/λ}→1` quando `r→0`). Pior:
   um `e^{-r/λ}` puro blindaria MOND em GRANDE r e mataria o MOND galáctico (kpc ≫ 17 pc).
   A forma fisicamente consistente (MOND sobrevive em galáxias, blindado em binárias) é
   o fator de coerência `S(r) = 1 − e^{−r/λ_A}`. **λ_A = 17.3 pc não foi alterado.**
2. **Função de interpolação.** O texto escrevia `ν(x)=1/√(1−e^{−√x})`; o √ extra dá
   MOND-profundo `g ∝ g_N^{3/4}`, não `g=√(g_N a₀)`. Como a MOND da DEV é calibrada na
   RAR do SPARC, usamos `ν_RAR(x)=1/(1−e^{−√x})` (McGaugh). **a₀ não foi alterado.**

Nenhuma correção toca a₀ nem λ_A, e as conclusões qualitativas (blindagem < 17 pc,
regime de Chae profundamente blindado, limite de maré em 1.7 pc) independem delas.

### Parâmetros fixados ANTES de rodar (não ajustar)

| Quantidade | Valor | Fonte |
|---|---|---|
| Aceleração de Milgrom | **a₀ = 1.2×10⁻¹⁰ m/s²** | Paper I (input) |
| Comprimento de correlação | **λ_A = 17.3 pc** | FM2/SCALE_BOUNDARY (input) |
| Campo externo da Via Láctea | g_ext = V_c²/R₀ ≈ 1.8 a₀ (V_c=233 km/s, R₀=8.2 kpc) | padrão (EFE) |
| Massa típica de binária | 0.5–2 M_☉ | input |

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO — não alterar após rodar)

```
MORTE (D):  binárias largas mostram sinal MOND ABAIXO de 17 pc com a MESMA
            amplitude que acima — sem blindagem detectável. λ_A=17 pc refutado
            por mais de uma ordem de magnitude.

TENSÃO (C): dados existentes mostram MOND sem blindagem abaixo de 17 pc, mas o
            resultado é contestado / não decisivo.

INDECISO (B): os dados existentes não cobrem o regime de transição (s~10-100 pc);
            a previsão não pode ser testada com dados atuais. Identificar survey.

SUCESSO (A): supressão de MOND para r<17 pc consistente com S(r)=1−e^{-r/λ_A}.
            Previsão exclusiva da DEV verificada.
```

**Honestidade obrigatória:** λ_A = 17.3 pc é input, não ajuste. Se os dados matarem,
reportar a morte; não mover λ_A para escapar.

---

## Tarefas

```
FN4-1  Perfil analítico g_DEV(r) vs g_N vs g_MOND, boost g/g_N, r∈[0.1,1000] pc.
       Transição em λ_A=17.3 pc.                       → FN4_1_profile.{py,md,json,png}
FN4-2  Estatística de velocidade v~(s)=v_obs/v_Newton, DEV vs MOND vs Newton,
       s∈[1,100] pc; divergência abaixo de 17 pc.       → FN4_2_velocity.{py,md,json,png}
FN4-3  Chae+2023 (arXiv:2309.08160): verificar regime de separações, calcular
       blindagem nesse regime, concluir se é o teste correto.
                                                        → FN4_3_gaia.{py,md,json,png}
FN4-4  Survey que cobre s~10-100 pc; N de binárias para 3σ; obstáculo de maré.
                                                        → FN4_4_forecast.{py,md,json,png}
FN4-5  Síntese honesta + veredito A/B/C/D.              → FN4_5_synthesis.md
```

Protocolo: FN4-1 (analítico) primeiro; FN4-3 verifica as separações de Chae ANTES de
assumir que são o teste; a₀ e λ_A fixos; critério de morte pré-registrado.

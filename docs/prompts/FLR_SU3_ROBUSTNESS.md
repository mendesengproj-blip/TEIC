# FLR_SU3_ROBUSTNESS — o teste de robustez de FL1 (variar a ação ~10%)

> **Charter PRÉ-REGISTRADO.** Critérios de morte escritos ANTES de qualquer código.
> Item 1 do `RESEARCH_MAP.md` (FASE 3, R1): a lacuna mais urgente do setor de
> matéria. FL1 declarou "SUCESSO TOTAL" (ferromagneto de cor + Skyrmion + confinamento
> + octeto + torres de Regge/Casimir), MAS o estabilizador de Skyrme é externo, a ordem
> de transição ficou inconclusiva em L≤12, e **o teste de robustez nunca foi feito**.
> Confiar em SU(3) exige saber se os resultados centrais sobrevivem a uma deformação
> de ~10% na forma da ação mínima.
>
> **Motor:** `results/matter/fl1/su3_core.py` (existe). Script novo:
> `results/matter/fl1/FLR_robustness.py`. **NÃO modifica nenhuma campanha anterior.**
> Resultados em `results/matter/fl1/FLR_*`.

## A pergunta

A fenomenologia de SU(3) (confinamento V~σr, octeto de 8 Goldstones, Skyrmion
estável) é uma propriedade robusta da rede causal, ou um artefato da forma exata da
ação mínima `[1 − (1/N)Re Tr(W)]`?

## A perturbação (declarada)

Ação generalizada de um parâmetro, aplicada CONSISTENTEMENTE aos dois setores:

```
g_ε(p) = (1 − p) + ε·(1 − p)²,     p = (1/N) Re Tr(W)    [N=3 gauge; N=3 traço chiral]
```

- ε = 0 recupera a ação mínima de Wilson/principal-chiral original (gate de controle).
- ε ≠ 0 deforma a forma: adiciona um termo quadrático na "desordem" local (1−p), a
  deformação não-linear mais simples que ainda é gauge-invariante e de plaqueta.
- "~10%" = ε = ±0.10 (o termo quadrático pesa ~10% perto da escala de desordem
  típica 1−p ~ O(1)). Bracketing com ε = ±0.20 para a tendência.

## TESTES e CRITÉRIOS DE MORTE (pré-registrados)

```
GATE (obrigatório antes de qualquer física):
  G0. Em ε=0, o metropolis perturbado reproduz o <plaqueta> do gauge_metropolis_sweep
      original dentro do ruído de MC (consistência da implementação). Se falhar → PARAR.

R-CONFINE (setor de gauge):
  Medir σ via razão de Creutz χ(2,2) no acoplamento forte para ε ∈ {−.2,−.1,0,.1,.2}.
  MORTE: σ(|ε|≤0.10) ≤ 0 (deconfinamento) OU V(r) deixa de crescer → o confinamento
         era artefato da forma exata de Wilson.
  PASS:  σ > 0 e V(r) cresce para todo |ε|≤0.10; deriva de σ reportada (alvo <~30%,
         deformações de ação mudam a normalização — o sinal/qualitativo é o que importa).

R-OCTET (setor chiral):
  Recontar os modos de Goldstone gapless (protocolo D2) com a E2 deformada,
  ε ∈ {−.2,−.1,0,.1,.2}.
  MORTE: nº de modos gapless ≠ 8 para |ε|≤0.10 → o octeto era artefato.
  PASS:  exatamente 8 modos gapless para todo |ε|≤0.10.

R-SKYRMION (setor chiral, estabilidade):
  Derrick radial: confirmar que o mínimo interior de E(λ)=λE2+E4/λ persiste, e
  reportar a deriva da massa M=2√(E2 E4) e do tamanho λ*=√(E4/E2) sob a deformação
  (aplicada a E2 e a e_sk em ±10%).
  MORTE: o mínimo interior desaparece para |ε|≤0.10 (Skyrmion instabiliza).
  PASS:  mínimo interior persiste; deriva de M, λ* reportada.
```

## VEREDITO GLOBAL

```
SU(3) ROBUSTO   se R-CONFINE, R-OCTET e R-SKYRMION todos PASS em |ε|≤0.10.
                → FL1 confirmado; o status [SÓLIDO com ressalva] do RESEARCH_MAP sobe.
SU(3) FRÁGIL    se qualquer um vira qualitativamente em |ε|≤0.10.
                → reportar honestamente; rebaixar o status de FL1; o resultado dependia
                  de ajuste fino da forma da ação.
```

## ANTI-CIRCULARIDADE

Nenhum número de QCD (σ em GeV², α_s, massas hadrônicas) entra. β é varrido; ε é o
parâmetro de deformação declarado; e_sk continua o estabilizador externo declarado
(FL1 Fase A). Sementes fixas; JSON auto-descritivo; o gate G0 valida a implementação
contra o motor original antes de qualquer alegação.

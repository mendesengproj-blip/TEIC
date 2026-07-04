# SÍNTESE — CAMPANHA_SU3_ORDEM_TRANSICAO: a ordem da transição em L≤24

> Pré-registro: `PRE_REGISTRO.md` (congelado + emendas pré-resultado, commitado antes
> de rodar). Dados/código: `OT_transition_order.py`, `OT_transition_order.json`,
> `OT_transition_order.png`. Predecessor direto: FLB2 (L≤16). Run jun/2026.
> Engine: `su3_core` (rede cúbica periódica), importado SEM modificação.

## Veredito (honesto, não o auto-veredito do script): **PRIMEIRA ORDEM FRACA é a leitura mais provável; H0 (2ª ordem, como SU(2)) DESFAVORECIDA; mas calor latente não-resolvido até L=24 ⇒ contínua-com-forte-finite-size não estritamente excluída**

A campanha estendeu a caracterização da transição do ferromagneto de cor SU(3) de
L≤16 (FLB2) para **L = 8, 12, 16, 20, 24**, com grade fina em J (ΔJ=0.01, 17 pontos,
2.60–2.76), 5 sementes, e o **método de cruzamento de Binder** (mais limpo que o
"dip" de FLB2). Cinco indicadores:

| Indicador (L=8→24) | Medida | Lê como | Confiança |
|---|---|---|---|
| **χ_max** | 2.45→9.6→29.2→69.8→125.6; **x_eff≈3.6** | super-volume (>d=3) → 1ª ordem | bem amostrado, mas **pré-assintótico** |
| **U4 no pico** | 0.618→0.580→0.565→0.522→**0.485** (dip aprofunda, não satura) | 1ª ordem | média (deriva+equilíbrio) |
| **Cruzamentos de Binder** | 2.617, 2.655, 2.608, **2.606** | pares grandes estabilizam ~2.606 | ambíguo (cruzamento ≠ pico de χ) |
| **Histerese** | 0.170 (L16) → **0.198** (L20), crescendo | 1ª ordem | **baixa — confound de sweep rápido** |
| **Calor latente / bimodalidade de E** | 0.385, 0.414, **0.412**; dip=0.00 (todos) | **ausente, plano** → contra 1ª ordem *resolvível* | **alta — runs longos, J_c certo** |

## Leitura honesta

- **H0 está DESFAVORECIDA.** A transição **não** se comporta como um 2ª ordem limpo
  (≠ SU(2)): χ_max cresce **mais rápido que qualquer γ/ν de 2ª ordem** (γ/ν≲2; aqui
  x_eff≈3.2–3.9), o dip de Binder **aprofunda monotonicamente** sem saturar num valor
  universal, e o pico de χ desloca-se com L (deriva 0.03→0.01, convergindo ~2.74). Isto
  rejeita a previsão nula pré-registrada de "2ª ordem para todos os L".

- **A leitura mais provável é 1ª ordem FRACA.** Os três indicadores OT pré-registrados
  (OT1 Binder sem convergência limpa + dip; OT2 χ_max lei-de-volume; OT3 histerese
  >15%) apontam 1ª ordem. Consistente com a moldura de literatura "1ª ordem para
  N≥3" (mantida como COMPARISON ONLY).

- **Mas é FRACA / não-resolvida, não forte.** O teste termodinâmico mais direto e
  menos confundido de 1ª ordem — **bimodalidade do histograma de energia em J_c**
  (calor latente / coexistência), medido com runs longos equilibrados (1500 burn +
  4000 meas × 3 sementes) no J_c **corretamente localizado** — está **limpamente
  ausente E PLANO** (0.385→0.414→0.412, dip 0.00) até L=24. Numa 1ª ordem, a
  bimodalidade *tem* de emergir e afiar com L; aqui ela nem sequer **tende** a emergir.
  Isto **limita** qualquer 1ª ordem a fraca (calor latente abaixo da resolução em
  L≤24) e **não exclui** contínua-com-forte-finite-size.

- **Dois confounds declarados (não inflar o veredito):**
  1. **x_eff≈3.6 > d=3 é impossível assintoticamente** ⇒ regime fortemente
     pré-assintótico (e/ou inflação por sub-equilíbrio: 500 sweeps de burn é curto
     perto de uma transição lenta; a variância de m infla mais a L maior). O expoente
     local **caiu de 3.91 para 3.22** no último passo (L20→24), *consistente* com
     virar para a lei de volume, mas um ponto não fecha. Afirmação honesta: "χ_max
     cresce **pelo menos** como o volume (x≳3), incompatível com 2ª ordem".
  2. **A histerese (OT3) é a evidência mais fraca:** o ciclo usou sweep **rápido**
     (200 burn + 400 meas por passo de J). Perto de uma transição lenta, o *lag* de
     não-equilíbrio produz histerese aparente mesmo num contínuo, e o lag **cresce
     com L** — exatamente o que vimos (0.17→0.20). Não tratar como prova de 1ª ordem.

## Reconciliação com FLB2 (transparência — REVERSÃO parcial)

FLB2 (L≤16) concluiu **"1ª ordem DESFAVORECIDA"**. Esta campanha **reverte o
enquadramento para "1ª ordem fraca / favorecida-fraca"**, e a razão é metodológica e
honesta:

- **Concordamos no fato do calor latente:** bimodalidade ausente — FLB2 e esta
  campanha medem a mesma coisa. A diferença é interpretativa + de evidência ao redor.
- **FLB2 diagnosticou o próprio χ_max como não-confiável** ("plano/ruidoso porque a
  grade grossa perdia o pico que deriva"). Esta campanha **corrigiu exatamente isso**
  (ΔJ=0.01 + rastreamento do pico) e revelou um χ_max **monotônico, lei-de-volume**,
  que é evidência *positiva* de 1ª ordem que FLB2 não tinha. Some-se o dip de Binder
  aprofundando e a histerese (mesmo confundida): o peso das assinaturas de forma agora
  pende para 1ª ordem, ao passo que FLB2 só via a ausência de calor latente.
- **Estendemos L=16→24:** a deriva do pico desacelera e o expoente local começa a
  virar — informação que FLB2 não alcançou.

Ou seja: o **mesmo fato** (sem calor latente) + **melhor medição de χ/Binder** ⇒
a inferência move de "não parece 1ª ordem" para "parece 1ª ordem fraca, com calor
latente abaixo da resolução".

## Verificações de consistência (pré-registradas)

- **V1 (vs FL1):** J_c(L=8) = **2.65**, batendo exatamente o J_c≈2.65 de FLB. A deriva
  até 2.74 em L=24 é o **deslocamento finite-size do ponto pseudo-crítico** (esperado,
  mais pronunciado numa transição aguda/1ª-ordem), não uma inconsistência. ✓
- **V2 (consistência interna):** registrada acima — três OTs (OT1/OT2/OT3) concordam
  em 1ª ordem; o diagnóstico de calor latente **discorda** e indica que a 1ª ordem é
  *fraca/não-resolvida*. Não forçamos consenso: o desacordo **é** o resultado.
- **V3 (robustez ±10% na ação):** não rodada como rescan separado. Justificativa
  honesta: reescalar J por ±10% apenas **relabela o eixo de temperatura** (J é o
  inverso-temperatura do modelo); não pode mudar a classe de universalidade / a ordem.
  A sonda de robustez genuína — **varrer L de 8 a 24** — foi feita e é o que importa
  para a ordem. (Registrado como ressalva menor; um teste de robustez na *forma* da
  ação ficaria para campanha futura.)

## O que isto fecha / muda (RESEARCH_MAP)

- **Ressalva FL1 (ordem da transição em L>12):** de "aberta / 1ª ordem desfavorecida
  (FLB2, L≤16)" para **"1ª ordem fraca é a leitura mais provável em L≤24; H0 (2ª
  ordem como SU(2)) desfavorecida; calor latente não-resolvido"**. **Não muda** FL1
  (a transição existe; confinamento + octeto permanecem sólidos, independentes da
  ordem). Muda só a *descrição* da transição.
- **Portão do PAPER_SU3:** segue o **Desfecho B (com ressalva)** do charter — o paper
  precisa de **seção dedicada à ordem**, declarando "1ª ordem fraca, com calor latente
  abaixo da resolução em L≤24; 2ª ordem limpa excluída; resolução definitiva
  (forte-vs-fraca-vs-contínua) exigiria L≳32 com runs muito longos e amostragem
  multicanônica / de pesos, em cluster" — registrado como trabalho futuro.
- **Resíduo remanescente declarado:** distinguir **1ª ordem fraca** de **contínua com
  forte correção pré-assintótica** não é possível em L≤24 nesta amostragem
  (Metropolis canônico). O caminho limpo é amostragem **multicanônica/Wang-Landau** em
  L≳32 para medir diretamente a barreira de energia livre (∝ tensão interfacial σ): σ>0
  finito ⇒ 1ª ordem; σ→0 ⇒ contínua.

## Anti-circularidade

Nenhum número de QCD; J_c, expoentes, cruzamentos e bimodalidade saem só dos dados;
"1ª ordem para N≥3" é só enquadramento (COMPARISON ONLY). O pico/cruzamento é
localizado **sem** usar 2.65 (comparação só em V1). Sementes fixas e registradas no
pré-registro. Guard `tests/test_no_circularity.py` passa (análise puramente real; o
complexo de SU(3) fica dentro de `su3_core`, nos blocos SU(3) GROUP-DEF).
`OT_transition_order.json` guarda todos os diagnósticos crus por L.

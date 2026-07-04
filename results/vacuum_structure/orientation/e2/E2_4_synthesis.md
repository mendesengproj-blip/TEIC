# E2-4 — Síntese honesta da campanha E2_MAGNON_BD

> Charter: `E2_MAGNON_BD.md`. Segunda campanha executada de
> `NIVEL4_ORIENTATION.md` (entrada FN2). Síntese de E2-V (gate), E2-1, E2-2,
> E2-3. Continua E1 (o vácuo é um ferromagneto causal). **NÃO modifica nenhuma
> campanha anterior.**

## Quadro de resultados (preenche o template do charter)

```
E2-V (gate):
  BD escalar / motor de análise validado?     SIM
    GATE A (análise recupera ck/massive/diffusive):  PASS (+0.01 / −0.45 / +1.05)
    GATE B1 (recursão BD instável, demonstrada):     SHOWN (|φ|→1068, modo-zero explode)
    GATE B2 (símbolo BD dá crista linear, c≈1):      PASS

E2-1 (propagação):
  δn⃗ propaga via BD sem dissipar?            SIM — via o SÍMBOLO do operador (a
    recursão direta é instável; observável estável = λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩)
  Velocidade de frente de onda ≈ c?           SIM — v=ω*/k ≈ 1 em toda a faixa,
                                              sem tendência (20 sementes, 10/10 k)

E2-2 (dispersão):
  Modelo preferido:                           ck (massless) — tendência E AIC
  Desvio de ω=ck:                             4.5%
  χ²(ck) < χ²(outros)?                        SIM (χ²/N: ck=0.46, difusivo=11.9;
                                              massivo dá m²=−0.047<0 → sem massa)
  Velocidade medida c_fit:                    0.980 ≈ 1 (cone de luz, EMERGENTE)

E2-3 (polarização):
  Modos transversais dominam?                 SIM — razão transversal/longitudinal
                                              = 183:1; 2 Goldstones (O(3)→O(2)) =
                                              2 polarizações do fóton
                                              CAVEAT: transversalidade interna, não
                                              de gauge a k⃗ (ver abaixo)
```

## Veredito da campanha

```
[X] A — FÓTON = MAGNON BD-SMEARED
        ω = ck com desvio 4.5% < 10%, c=0.98≈1 (cone de luz), sem massa
        (m²<0), difusivo rejeitado por duas ordens de grandeza em χ². Modos
        suaves transversais dominantes (2 Goldstones = 2 polarizações).
```

**Veredito A — com um caveat honesto na polarização.** A pergunta central de E2
("quando δn⃗ propaga via B_ε, ω=ck?") recebe **SIM**: a cadeia está fechada na
dispersão.

```
REDE CAUSAL DE POISSON
  ↓ [ferromagnetismo espontâneo de orientação — E1: C(∞)=m², J_c, 2ª ordem]
VÁCUO ORDENADO ⟨n⃗⟩ ≠ 0
  ↓ [operador de onda BD-suavizado (Sorkin/BD, e10) — E2-V/E2-1/E2-2]
MAGNON BD: δn⃗ com ω = ck (c=0.98≈1, sem massa) e 2 polarizações transversais
  = FÓTON
```

## O que E1 deixou aberto e E2 fechou

E1 estabeleceu A para a **ordem** (ferromagneto causal) mas **negativo para o
fóton**: o Laplaciano de links nus dá S(k) plano e não-local (⟨grau⟩≈130, sem
rigidez de gradiente), **sem** ω=ck. E1-3 nomeou o conserto: o d'Alembertiano
BD-suavizado de e10. **E2 testou esse conserto e ele funciona:**

- O operador de links nus falha (E1-3) **porque** propaga em campo médio.
- O operador BD-suavizado **restaura a localidade**: o peso de sinal alternado
  w(m) (e10) cria a interferência entre camadas que produz o termo de gradiente,
  e a dispersão emergente é **ω=ck** (E2-2), exatamente a previsão.

## Os três achados próprios (e o que NÃO se reivindica)

1. **A recursão direta de BD é inviável; o símbolo é o observável certo.** A
   forma de Euler do charter (δn(t+dt)=δn(t)+dt·B_ε[δn]) é o inverso explícito
   instável de B_ε — o modo-zero constante explode (E2-V B1, |φ|~1000), a
   variância pontual de BD documentada em e10. O **símbolo** λ(k,ω) é estável e
   tem a mesma dispersão on-shell. **Departure documentada do charter, com razão.**

2. **A normalização de sinal de B_ε não é o que e10 assumiu — mas a dispersão é
   invariante.** Medido: B_ε ≈ −K·(k²−ω²) (âncoras de sinal opostas às de e10,
   que só fixou *ordenamento*). O cruzamento por zero — a dispersão — independe
   dessa normalização. ω=ck sai limpo.

3. **A velocidade ≈1 (cone de luz) é emergente, não inserida.** c nunca entra no
   gerador; ondas de prova cos reais; ω varrido livre; c_fit é parâmetro livre.
   c_fit=0.98.

**NÃO se reivindica:** transversalidade de gauge plena (δn⃗⊥k⃗, k⃗·A⃗=0). A
contagem de polarizações (2) bate com o fóton e os modos suaves são os
transversais-a-⟨n⃗⟩ (Goldstone), mas isso é transversalidade no **espaço interno**
S²; a estrutura de gauge a k⃗ exige identificar o índice interno com o de
espaço-tempo, não fornecida pelo sigma model nu. A massa é zero dentro do erro
(m²<0); um teste de tamanho-finito/N→∞ confirmaria que permanece zero.

## Resposta ao ponto de cautela do ChatGPT (charter)

ω=ck é o espectro analítico de um Goldstone de U(1)/O(3) quebrada em 3+1D
(resultado conhecido de QFT). E2 fez a **confirmação numérica** desse resultado
na rede causal **discreta** de Poisson — e o ponto não-trivial é que o operador
**discreto** com ⟨grau⟩≈130 (que em links nus dava campo médio, E1-3) reproduz a
dispersão relativística quando passado pelo suavizador BD. A rede reproduz a
estrutura analítica; não a contradiz.

## Conexão com resultados existentes

- **E1** (A para a ordem; negativo/aberto para o fóton) → E2 **fecha o fóton** na
  dispersão, com o alvo preciso que E1-3 indicou (e10).
- **e10** (BD reproduz Sorkin/Benincasa–Dowker; operador afiado inviável,
  suavizado aniquila constantes) → E2 usa o operador suavizado de e10 como motor
  de propagação e mede a dispersão que ele dá às flutuações do ferromagneto de E1.
- **VS1** (densidade obedece, não lidera) → E2 confirma que a **orientação** é o
  grau fundamental: seu modo de Goldstone via BD É o fóton (ω=ck).
- **SU3 / Skyrmion** (matéria = defeito de n⃗) permanece coerente: defeitos
  topológicos vivem sobre este vácuo, cujos fônons agora são fótons (NIVEL4 E3).

## Disciplina mantida

- Critério de morte pré-registrado **antes** do código; gate de engenharia
  **antes** da medição (E2-V PASS, com bug do próprio teste encontrado e corrigido).
- Negativo/limitação reportada como tal: recursão instável reportada; caveat de
  polarização declarado; m²<0 reportado em vez de forçar massa.
- Critério de morte (difusivo) testado de verdade e rejeitado pelos dados — o
  ajuste **não** foi mexido para escapar (o difusivo recebeu o mesmo tratamento e
  perdeu por χ² em duas ordens de grandeza).
- Anti-circularidade em todo o gerador: c nunca inserido; ondas de prova reais;
  sementes fixas; "fóton"/"magnon" só na síntese.

## Próximos passos sugeridos (não executados aqui)

1. **Massa→0 com N→∞ / tamanho-finito:** confirmar que m²<0 medido é massa nula
   verdadeira (Goldstone exato), não efeito de tamanho.
2. **Transversalidade de gauge:** investigar se a identificação interno↔espaço-
   tempo (e.g. n⃗ acoplado à direção de propagação) emerge de alguma estrutura da
   rede — o passo que falta entre "2 polarizações" e "fóton de gauge pleno".
3. **NIVEL4 E3:** defeitos topológicos de n⃗ (Skyrmions/hedgehogs) = matéria sobre
   este vácuo cujos fônons são fótons.

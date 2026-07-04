# E3-5 — Síntese honesta: defeitos topológicos de n⃗

> Charter: `E3_DEFECTS.md`. Campanha NIVEL4_ORIENTATION / FN3. Substrato: modelo
> sigma O(3) em rede cúbica aberta (o motor de E1, onde o hedgehog n⃗(r)=r̂ é bem
> definido — um toro periódico não carrega carga de ponto líquida). Motor:
> `e3_core.py`. Não modifica nenhuma campanha anterior.

## Quadro de resultados

```
E3-V (gate):
  B medido corretamente (hedgehog +1, vácuo 0, anti −1)?   SIM (1e-6, O(3)-invariante)

E3-1 (estabilidade):
  B(t)=1 preservado no gradiente descendente (T=0)?        SIM
  E(t) tem mínimo / r_eff converge para r>0?               SIM (r_eff≈0.32·L, fixado pela caixa)
  B(t)→0 sob Monte Carlo térmico?                          SIM, em ~2700–2800 sweeps (20 sementes)
  Cenário:                                                 B (metaestável)

E3-2 (Derrick):
  E(λ) tem mínimo interior?                                NÃO (parede em λ<1, platô em λ>1)
  E vs L?                                                  E=7.67·L, R²=1.00000 (marginal de escala)
  Curvatura muda o resultado?                              NÃO (enfraquece a parede; não estabiliza)

E3-3 (gravidade):
  Defeito produz θ ~ 1/r?                                  PARCIAL (perfil 1/r mas M(r)~r não satura)

E3-4 (catálogo):
  Anti-hedgehog B=−1 existe?                               SIM (espelho do +1, sobrevive)
  Par B=+1,−1 cria/aniquila?                               SIM (dipolo aniquila, E:1192→0)
  Toroidal é defeito de ponto?                             NÃO (B=0, decai)
```

## VEREDITO

```
[ ] A — MATÉRIA = DEFEITO TOPOLÓGICO DE n⃗ ESTÁVEL
        Exigia: hedgehog B=1 estável, E(λ) com mínimo interior, θ~1/r com M
        finita. NÃO satisfeito: não há mínimo de Derrick (E∝L, marginal); a
        massa não localiza (M(r)~r).

[X] B — METAESTÁVEL (barreira finita)
        O hedgehog B=1 sobrevive ao gradiente descendente — a DISCRETIZAÇÃO
        (mecanismo 1) regulariza o colapso de Derrick e segura uma carga de ponto
        com caroço de tamanho de rede. Mas:
          • E(λ) não tem mínimo confinante (só parede UV no λ<1, platô no λ>1);
          • E∝L, marginal de escala, sem comprimento intrínseco;
          • flutuações térmicas (MC) des-enrolam B=1→0 em tempo finito (~2700 sw);
          • curvatura θ~1/r (proxy) NÃO estabiliza;
          • a "massa" não localiza (θ~1/r só aparente).
        → Defeito metaestável do ferromagneto, NÃO um sóliton estável.

[ ] C — MORTE: Derrick com colapso total B→0 no gradiente
        NÃO: sob gradiente descendente B permanece +1 e r_eff converge para r>0;
        não há colapso para zero. (B só vai a 0 no canal térmico, por barreira
        finita — isso é metaestabilidade, não morte de Derrick.)
```

**VEREDITO: B — METAESTÁVEL.**

## O que este resultado decide

O ferromagneto causal nu (modelo sigma O(3) na rede) **não** produz matéria
estável a partir de defeitos topológicos de n⃗. A discretização da rede faz mais
do que o contínuo (regulariza o colapso UV de Derrick e dá uma carga de ponto B=1
com tempo de vida longo), mas **menos** do que o necessário para um sóliton: não
há mínimo de energia confinante, a textura é marginal de escala, e a barreira que
a protege é finita (des-enrola termicamente). A curvatura induzida testada
(mecanismo 2, proxy θ~1/r) não fornece o ingrediente faltante.

Concretamente, para a cadeia do programa:

```
FERROMAGNETO CAUSAL (derivado da rede de Poisson):
  modo de Goldstone (E2)  = FÓTON          ✔ derivado, sem ingrediente externo
  defeito topológico (E3) = MATÉRIA        ✗ apenas METAESTÁVEL no ferromagneto nu
  curvatura θ~M/r (D3)    = GRAVIDADE       (matéria localizada ausente aqui)
```

O fóton emerge limpo do ferromagneto causal (E2). A **matéria estável ainda
precisa de SU(2)+Skyrme** como no Paper II atual — E3 mostra honestamente que o
ingrediente extra é necessário, e que o candidato mais barato (curvatura da
própria rede) não basta com o proxy testado.

## Próximos passos sugeridos (não executados aqui)

- **O que estabilizaria?** O termo de Skyrme (∝|∂ᵢn×∂ⱼn|²) reintroduz a escala que
  falta (Derrick: E=aλ+b/λ → mínimo). Medir se a rede causal o gera
  dinamicamente (em vez de imposto) fecharia a questão — é a ponte natural para o
  resultado de SU(2)+Skyrme do Paper II.
- **Mecanismo 3 (topologia causal):** o cone causal / estrutura temporal não foi
  explorado aqui (E3 rodou no substrato espacial cúbico de E1). Um defeito
  semeado diretamente na rede de links causais 3+1D é o teste honesto restante
  antes de declarar o ferromagneto nu insuficiente.
- Reportar como **"matéria metaestável do ferromagneto"** — não reescrever o
  Paper II; FM1 (CMB/S8) avança com o quadro atual (fóton derivado, matéria via
  SU(2)+Skyrme).

## Anti-circularidade (resumo)

B é contagem de ângulo sólido das plaquetas; E é o funcional de ligações
1−n_i·n_j; r_eff é momento da densidade de gradiente medida. "Matéria",
"partícula", "massa", "anti-matéria", "aniquilação" são COMPARISON ONLY. Critério
de morte pré-registrado pontuado como escrito; nenhum parâmetro foi ajustado para
escapar de — ou forçar — qualquer veredito.

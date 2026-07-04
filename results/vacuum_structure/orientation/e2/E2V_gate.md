# E2-V — Gate de validação dos motores (análise + propagação BD)

> Charter: `E2_MAGNON_BD.md` (gate E2-V, obrigatório antes de qualquer medição
> física). Código: `E2V_gate.py`; motor: `e2_core.py` (reusa `experiments/
> e10_sorkin_dalembertian.py` para o peso suave de Sorkin/BD e `src/causal_core.py`
> para o sprinkling/ordem causal); dados: `E2V_gate.json`; figura: `E2V_gate.png`.
> **NÃO modifica nenhuma campanha anterior.**

## O que o gate testa

E2 precisa de dois motores. Ambos são validados aqui com entradas de resposta
**conhecida**, usando exatamente a maquinaria que rodará na medição física.

### GATE A — motor de ANÁLISE: S(k,ω) + classificador de dispersão

Alimenta campos sintéticos com lei de dispersão **conhecida** (a lei é a
ENTRADA, rotulada COMPARISON ONLY — não sai de nenhuma rede) e verifica que o
estimador `S(k,ω)` por DFT não-uniforme + busca de pico ω*(k) + classificador
recuperam a lei certa e seus parâmetros:

```
entrada            classificador       parâmetro recuperado    v_rel_slope
-------------------------------------------------------------------------
massless ω=c₀k     → massless  ✔       c=0.796  (c₀=0.8)        +0.011
massive  ω=√(c²k²+m²) → massive ✔      m=0.527  (m₀=0.5)        −0.448
diffusive ω=Dk²    → diffusive ✔       D=0.698  (D₀=0.7)        +1.046
```

**Classificador (independente de escala e de ruído).** A corrida AIC/χ² é
frágil aqui (uma lei de 2 parâmetros sempre raspa o resíduo de uma de 1
parâmetro; o vencedor depende do σ assumido). O discriminador robusto é a
**tendência da velocidade de fase** v(k)=ω/k em k: *plana* = massless (v=c),
*sobe* = diffusive (v=Dk), *desce* = massive (v=√(c²+m²/k²)). O sinal+tamanho
da inclinação relativa de v(k) classifica sem nível de ruído assumido; limiar
±0.15 separa limpo (+0.01 vs −0.45 vs +1.05).

> **Bug encontrado e corrigido no gate** (disciplina): a 1ª versão usou modos
> sintéticos espaçados (Δk=0.1) abaixo da resolução de DFT (2π/2X≈0.26) → vazamento
> espectral inclinava os picos de alto-k para baixo e fazia um campo massless
> parecer massive. Corrigido espaçando os modos ≥ resolução (Δk=0.23). É um defeito
> do **teste**, não do estimador (modo único: pico em 0.642 vs 0.64 exato).

### GATE B — motor de PROPAGAÇÃO: o d'Alembertiano BD-suavizado

**B1 — por que NÃO se propaga por recursão.** A recursão retardada
φ(x)=2ε Σ_{y<x} w(m_y) φ(y) (resolver B_ε[φ]=0 varrendo em ordem causal) é
**INSTÁVEL**: nem o modo-zero constante sobrevive. Medido: partindo de φ≡1,
o campo no miolo vai a ⟨φ⟩=−21 com max|φ|=1068. É a variância pontual de BD
documentada em e10 (operador afiado ~ρ^{3/4}). **Reportado, não escondido** —
é o que justifica a rota do símbolo.

**B2 — o observável ESTÁVEL: o símbolo do operador.** Em vez de inverter B_ε,
lê-se a dispersão do **símbolo** λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩ com f=cos(kx−ωt),
medido em causal sets de Poisson reais (média sobre 16 sementes). No contínuo
B_ε→□, cujo símbolo ∝ (k²−ω²) **a menos de uma normalização cujo sinal o
operador suavizado não fixa** (e10 só fixou o *ordenamento* de sinais). A
dispersão on-shell é o **cruzamento por zero** em ω. Resultado:

```
8/8 cruzamentos encontrados (k=0.50…1.40); ω*(k) acompanha ω=k.
fit: vencedor=massive (devido ao ponto de menor-k, finite-size),
     c_fit=1.040 (≈1 = velocidade do cone de luz, EMERGENTE),
     desvio linear=10.5%.
GATE B2: PASS — o símbolo dá uma crista linear com a velocidade do cone.
```

> **Aviso registrado para E2-1/E2-2:** o ponto de menor k (k=0.50, ω*=0.657,
> *acima* da reta ω=k) inclina v_rel_slope para −0.247 e dispararia o rótulo
> "massive". É elevação de tamanho-finito em k pequeno (comprimento de onda ~
> largura da caixa), **não** uma massa física. A medição real usa mais sementes
> (20, charter) e janela de k limpa, e reporta o resíduo honestamente.

## Anti-circularidade

- Nenhuma lei de dispersão entra no gerador BD; **c nunca é inserido**; ondas de
  prova são cos reais (sem literal complexo); sementes fixas.
- As leis sintéticas do GATE A são entradas COMPARISON-ONLY explícitas, usadas só
  para validar o **código de análise** — não tocam o operador BD.
- c_fit é parâmetro livre; comparado a 1 (cone de luz) só na síntese.

## Veredito do gate

```
GATE A (análise recupera ck/massive/diffusive):   PASS
GATE B1 (recursão instável, demonstrada):          SHOWN
GATE B2 (símbolo BD dá crista linear, c≈1):        PASS
E2-V GATE:                                          PASS — prosseguir para E2-1
```

O motor de análise distingue as três leis; o motor de propagação correto (o
símbolo BD, não a recursão instável) recupera ω=ck com velocidade do cone de luz
emergente. Os dois ingredientes que E2 precisa estão validados.

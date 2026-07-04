# SU9 — Síntese honesta: SU(2) deriva matéria pontual estável?

## Quadro de resultados

```
SU1 — Motor SU(2) validado:                 SIM (4/4 portões; limite U(1), grupo,
                                                gauge, energia — todos a 1e-16 / drift 4e-4)
SU2 — Vácuo confinante (lei de área):       SIM (σ>0, χ(2,2)∈[0.4,0.85]; monopolos em todo β)
SU3 — Hedgehog estável:                     SIM (virial E₂=E₄=0.99–1.00; mínimo de rede λ=0.90;
                                                massa M≈146–207; colapso sem Skyrme)
SU4 — B=1 conservado:                       SIM (B→+1, anti→−1, par→0; conservado a curto prazo)
SU5 — Estabilidade de Derrick com Skyrme:   SIM (E₂=E₄)
SU5 — Skyrme emerge do quártico C4:         NÃO (C4 é simétrico (A+dθ)⁴; Skyrme é o
                                                comutador antissimétrico, ≡0 no setor Abeliano
                                                — terceiro ingrediente não-Abeliano)
SU6 — Skyrmion criado por colisão:          NÃO (|B|≤0.41 em 20 sementes; não quantiza)
SU7 — Spin-½ (2π → −estado):                NÃO verificável (permitido por π₄=ℤ₂, mas
                                                o sinal é uma fase quântica FR)
SU8 — Cinco consistências:                  3/5 (massa, gravidade∝massa, isotropia;
                                                dispersão herdada não re-verificada; spin não)
```

## Veredito

```
[ ] A — Skyrmion estável + spin-½ + cinco consistências
[x] B — Skyrmion estável (B=1) mas SEM spin-½ verificado → matéria bosônica SU(2) com B=1
[~] C — (para a questão da CRIAÇÃO) hedgehog estático existe, criação por colisão não ocorre
[ ] D — SU(2) não confina ou hedgehog instável
```

**Veredito B**, com a ressalva C na questão específica da *criação dinâmica*.

## A resposta honesta

A fronteira de matéria, ao longo de toda a investigação, apontou para um único lugar:
matéria **pontual** e **estável** exige topologia `π₃` — e portanto SU(2), não U(1).
SU2 testou cada elo:

1. **O motor é legítimo (SU1).** SU(2) como quaternions unitários `(a₀,a₁,a₂,a₃)`,
   produto de Hamilton, **sem Pauli e sem números complexos**. Contém CR_3D como caso
   exato (limite U(1) a 1e-16), é invariante de gauge (exatamente 0.0) e conserva
   energia (leapfrog geodésico, drift 4e-4). É um motor não-Abeliano honesto.

2. **O vácuo confina (SU2).** SU(2) Yang-Mills exibe **lei de área** (`σ>0`) em todo o
   acoplamento resolvido, com monopolos presentes — o confinamento genuíno que U(1) 3D
   não tinha (lá a janela estava invertida).

3. **O hedgehog é estável — o resultado central (SU3).** O teorema do virial de Derrick
   é satisfeito sem ambiguidade: `E₂=E₄` (0.99–1.00) no perfil relaxado, e a rede 3D
   exibe um **mínimo de energia interior** (λ=0.90) **com** o termo de Skyrme e
   **colapso sem** ele. Pela primeira vez nesta investigação, a ação suporta um sóliton
   **pontual (0D)** com massa de repouso definida `M≈146`, e não um vórtice difuso (1D).

4. **A carga topológica é o inteiro certo (SU4).** `B→+1` (anti `−1`, par `0`),
   conservada — o número de enrolamento `π₃(SU(2))=ℤ`.

5. **O estabilizador é genuinamente não-Abeliano (SU5).** O termo de Skyrme **não** é o
   quártico que C4 derivou: C4 é a 4ª potência simétrica `(A+dθ)⁴`; Skyrme é o comutador
   antissimétrico `|a×a|²`, **identicamente zero no setor Abeliano**. É um **terceiro
   ingrediente** — fornecido pelo comutador de grupo SU(2) (curvatura `F=dA+[A,A]`), não
   adicionado à mão, mas tampouco o operador C4. A estabilidade que ele dá é real.

6. **Onde para (SU6, SU7).** Duas coisas **não** acontecem:
   - **Criação por colisão (SU6 → NÃO).** Em 20 sementes, `|B|` nunca passa de 0.41: o
     setor topológico `B=1` não é alcançado a partir do vácuo por evolução suave. A
     mesma topologia que estabiliza o Skyrmion o torna difícil de *criar* — setores
     topológicos não se conectam suavemente. (Como o vórtice U(1), que também não era
     criado robustamente.)
   - **Spin-½ (SU7 → não verificável).** `π₄(SU(2))=ℤ₂` e o cobrimento duplo dão −1
     para 2π — o spin-½ é **permitido e natural** — mas o sinal `|ψ⟩→−|ψ⟩` é uma fase
     quântica de Finkelstein–Rubinstein, fora do alcance de um campo clássico (que
     retorna a +si mesmo).

## O que SU(2) decidiu para a física

```
TOPOLOGIA POR GRUPO (mapa fechado):
U(1)  (CR_3D):  π₁=ℤ  → vórtice S¹ (1D), semi-estável, 4/5 consistências
SU(2) (SU2):    π₃=ℤ  → Skyrmion (0D = PARTÍCULA), ESTÁVEL, B=1, massa, gravita, 3/5
                π₄=ℤ₂ → spin-½ PERMITIDO (não verificável classicamente)
```

**Resultado positivo:** uma rede causal 3+1D com campo SU(2) e ação mínima (sigma +
Skyrme não-Abeliano) **deriva um sóliton pontual estável com número topológico B=1,
massa de repouso, campo gravitacional próprio proporcional à massa, e isotropia** — um
objeto qualitativamente novo em relação a tudo que as campanhas anteriores produziram
(o vórtice difuso de U(1)). É **matéria estável**, no sentido bosônico/topológico.

**Limite preciso identificado:** faltam exatamente dois ingredientes para o Veredito A,
e ambos são bem-definidos:
- **criação dinâmica** do setor `B=1` (uma flutuação topológica grande que a colisão
  suave não fornece — talvez exija um mecanismo de produção de pares topológicos);
- **spin-½**, que exige **quantizar as coordenadas coletivas** do Skyrmion (e
  possivelmente o termo de Wess–Zumino) — uma camada quântica acima do campo clássico.

A fronteira foi empurrada de "vórtice bosônico semi-estável (1D, U(1))" para "sóliton
pontual estável com B=1 (0D, SU(2))". O próximo ingrediente não é mais o grupo nem a
topologia — é a **quantização das coordenadas coletivas** (para spin) e um **mecanismo
de criação topológica** (para nascimento dinâmico).

## Honestidade numérica

- A força do setor sigma é analítica e conserva energia (4e-4); a força de Skyrme é por
  diferença finita e **levemente não-conservativa** — limita a evolução dinâmica longa
  (vazamento de `B`, SU4) e tornou a colisão com Skyrme inviável em 20 sementes (SU6 usou
  sigma analítico). Uma força de Skyrme analítica é o próximo passo numérico.
- A dispersão relativística (SU8) **não** foi re-verificada de forma independente
  (anti-circularidade proíbe inserir `γ`); ela é herdada da invariância de Lorentz já
  estabelecida (ponte R1–R3).
- `B` na rede converge para o inteiro ao refinar (erro de discretização ~4% em N=51).

Nenhuma campanha anterior foi modificada. Anti-circularidade verificada
(`tests/test_no_circularity.py`): quaternions (4 reais), sem Pauli, sem complexo, sem
dilatação SR/GR no gerador; "próton/quark/isospin/bárion/spin" só como nomes ou em
blocos COMPARISON ONLY.

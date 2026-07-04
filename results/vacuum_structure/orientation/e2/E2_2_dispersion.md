# E2-2 — Relação de dispersão ω(k): ck vs massivo vs difusivo

> Charter: `E2_MAGNON_BD.md` (E2-2). Lê a dispersão medida em E2-1
> (`E2_1_propagation.json`) e ajusta os três modelos. Código:
> `E2_2_dispersion.py`; dados: `E2_2_dispersion.json`; figura:
> `E2_2_dispersion.png`. **NÃO modifica nenhuma campanha anterior.**

## Os três modelos

```
massless   ω = c k                  bóson de Goldstone relativístico (fóton)
massivo    ω = √(c²k² + m²)         Klein–Gordon
difusivo   ω = D k²                 magnon não-relativístico
```

Modelo preferido pela **tendência da velocidade de fase** (validado em E2-V:
v(k)=ω/k plana=massless, sobe=difusivo, desce=massivo), com χ²/AIC como
diagnóstico corroborante.

## Ajuste (χ² ponderado pelo SEM por k, 10 pontos, 20 sementes)

```
modelo                         parâmetro          χ²       χ²/N    AIC
----------------------------------------------------------------------
massless  ω=ck                 c = 0.980          4.59     0.46    6.59   ←
massivo   ω=√(c²k²+m²)         c=1.01, m²=−0.047  3.05     —       7.05
difusivo  ω=Dk²                D = 0.861        118.94    11.89  120.94
----------------------------------------------------------------------
tendência v(k):  v_rel_slope = +0.101   (|limiar|=0.15 → PLANA = massless)
vencedor (tendência) = massless        vencedor (AIC) = massless
velocidade medida c_fit = 0.980        (cone de luz = 1)
desvio de ω=ck = 4.5%
```

## Leitura

1. **ω = ck, linear.** O vencedor é `massless` por ambos os critérios
   (tendência e AIC). χ²/N=0.46 — o modelo linear é consistente com os dados
   dentro das barras de erro.

2. **Sem massa.** O ajuste massivo retorna **m² = −0.047 < 0** (massa
   imaginária): os dados não suportam massa alguma; o termo extra colapsa ao
   massless e é penalizado pelo AIC. Não há gap.

3. **Difusivo decisivamente rejeitado.** ω=Dk² dá χ²/N=11.9 (vs 0.46) e AIC
   ~120 — a morte pré-registrada (Veredito C) **não** se realiza.

4. **Velocidade = cone de luz, emergente.** c_fit=0.980 ≈ 1. Como c nunca entra
   no gerador (E2-1/E2-V; ondas de prova cos reais, ω varrido livre), essa
   velocidade ~1 é um resultado **medido**, não imposto.

5. **Desvio 4.5% < 10%.** Cumpre o limiar de **SUCESSO** do charter.

## Anti-circularidade

c é parâmetro livre do ajuste; a comparação com 1 (cone de luz) aparece só aqui
na conclusão. O critério de morte (difusivo) foi testado de verdade e rejeitado
pelos dados — o ajuste não foi mexido para escapar dele (ao contrário: o modelo
difusivo recebeu o mesmo tratamento e perdeu por χ² duas ordens de grandeza).

## Veredito

```
VEREDITO (E2-2) [A]: FÓTON = MAGNON BD-SMEARED
  ω = ck com desvio 4.5% < 10%, c = 0.98 ≈ 1 (cone de luz), sem massa
  (m² < 0), difusivo rejeitado (χ²/N: 0.46 vs 11.9).
```

Como a dispersão **é** linear, a condição do charter para E2-3 (verificar
polarização só se a dispersão for linear) está satisfeita → prosseguir para E2-3.

# VS2 — As fases do vácuo: há transição de fase na rede causal?

> Charter: `VACUUM_STRUCTURE.md` (VS2). Pergunta: ⟨|Φ|⟩ (e os demais
> parâmetros de ordem do vácuo) transiciona abruptamente em função do
> parâmetro de controle, ou varia suavemente?
> Código: `VS2_phase_transition.py`; dados: `VS2_phase_transition.json`.

## Protocolo

Parâmetro de controle: a escala de desordem inicial s do quench de gauge
(o análogo de "temperatura" da rede: início quente, esfriado pela ação
mínima — mesmo protocolo de VS1, aqui varrido finamente: s = 0.2 .. π em
16 pontos, 5 sementes por ponto).

Parâmetros de ordem medidos após o esfriamento:

- **m = |⟨e^{iφ̄}⟩|** — coerência de fase do vácuo de gauge;
- **ρ_M** — densidade de monopólos congelados (defeitos topológicos);
- **|⟨Φ⟩|** — amplitude coerente do campo emergente Φ = ρ_dyn·e^{iφ̄}
  (ρ_dyn pelo minimizador estático conservante, K=10);
- **J_std** — ação residual congelada do vácuo.

**Nota sobre o ⟨|Φ|⟩ literal do charter:** com a normalização de
PHI_EMERGE, ⟨|Φ|⟩ = ⟨ρ⟩ = 1 **identicamente** (conservação) — o
observável literal não pode transicionar por construção (verificado:
1.0000 em toda a varredura). O objeto fisicamente carregado é a média
coerente |⟨Φ⟩| (o "v" de um condensado), mais a densidade de defeitos.
Ambos reportados.

## Resultado

```
s      m_phase    ρ_M       |⟨Φ⟩|     J_std
0.2    0.9999     0.00000   0.9999    0.0075
1.0    0.9981     0.00024   0.9984    0.1779   ← onset de monopólos
2.0    0.9909     0.01347   0.9958    0.6057
3.14   0.9571     0.02431   0.9994    1.0923
```

**Tudo suave.** Diagnóstico de abrupticidade (max salto entre pontos
adjacentes / range total, sobre médias de 5 sementes):

```
m_phase:     0.178   (sem salto dominante; declive máximo em s=2.8)
ρ_M:         0.144   (crescimento contínuo desde s=1.0)
|⟨Φ⟩|:       0.339   (mas range total = 0.005 — variação de meio por cento)
J_std:       0.087   (quase perfeitamente linear em s)
```

Nenhum parâmetro de ordem salta; nenhuma curva tem joelho reproduzível
entre sementes. O único marcador estrutural é o **onset de monopólos
congelados em s ≈ 1.0** — mas ρ_M cresce dali continuamente (2.4×10⁻⁴ →
2.4×10⁻², duas décadas percorridas sem descontinuidade), o que caracteriza
um **crossover**, não uma transição de fase.

## Veredito

```
[x] CRITÉRIO DE MORTE DISPARA: sem transição — todos os parâmetros de
    ordem variam suavemente com a desordem do quench. Não há temperatura
    crítica identificável neste probe.
[ ] Transição abrupta — NÃO observada.
```

**O vácuo da rede, neste probe, não tem estrutura termodinâmica de fases
com transição.** O que existe é:

1. **Um crossover de defeitos** em s ≈ 1.0: abaixo, o quench esfria para
   o vácuo ordenado limpo; acima, começa a congelar monopólos em
   densidade crescente — o "vácuo vítreo" de VS1, alcançado gradualmente.
2. **A fronteira K_c ≈ 8.5** (PE4_V3/VS1) permanece a única divisa
   abrupta conhecida do setor — mas é uma divisa de *estabilidade da
   resposta* (rigidez da geometria), não uma transição termodinâmica do
   estado de gauge.

## Limites declarados deste probe (o que ele NÃO testa)

- O parâmetro de controle é a desordem de um *quench dinâmico* esfriado
  por minimização — não um ensemble térmico de Monte Carlo a temperatura
  T com β = 1/T. U(1) compacta em 3D *tem* transições conhecidas em
  ensemble térmico; o probe daqui responde pela estrutura do vácuo
  *atingível pela dinâmica da ação mínima*, que é a pergunta da TEIC.
  Um probe térmico (Metropolis sobre a ação de Wilson da rede causal)
  fica registrado como extensão natural se o crossover de defeitos
  merecer promoção a campanha.
- A varredura em ρ (densidade de sprinkle) já foi coberta por VS1(a):
  monotônica e suave (1/√ρ), sem estrutura.

## Honestidade

- 5 sementes por ponto; erros de semente reportados (σ_m ≤ 0.0012).
- ⟨|Φ|⟩ ≡ 1 por construção está dito explicitamente, e não foi usado
  como evidência de coisa alguma.
- Anti-circularidade: aritmética real (cos/sin), nenhuma temperatura
  crítica inserida, sementes fixas.

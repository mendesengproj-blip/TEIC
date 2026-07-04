# VS4 — Três gerações: degenerescência topológica no setor B=1?

> Charter: `VACUUM_STRUCTURE.md` (VS4). Pergunta: existem múltiplas
> configurações estáveis com o mesmo número topológico B=1 e energias
> diferentes — o análogo topológico das três gerações?
> Código: `VS4_generations.py`; dados: `VS4_generations.json`.
> Infraestrutura: su2_core (SU3) — não modificada.

## Protocolo

**(A) Varredura de bacias radial (rigorosa dentro do ansatz hedgehog).**
B=1 é imposto só pelas condições de contorno F(0)=π, F(∞)=0; o interior é
livre, incluindo excursões não-monotônicas F→3π→π (mesmo winding, caminho
diferente). 10 perfis iniciais radicalmente diferentes (larguras ×0.3–3,
rampa linear, núcleo-platô, três excursões +2π, oscilante) relaxados pelo
minimizador de gradiente analítico de SU3 — **com imposição de virial**:
um ponto estacionário verdadeiro do funcional de Skyrme satisfaz E2=E4
(Derrick); cada relaxamento é seguido de reescala de Derrick
λ*=√(E4/E2) e re-relaxamento até |E2/E4−1| < 2%.

**(B) Spot-check 3D fora do ansatz estrito.** O perfil fundamental e uma
excursão +2π larga embutidos na rede 25³ e esfriados com a força quiral
3D completa (rate=0.002, ver nota numérica), verificando B e o fluxo de
energia.

## Resultado (A) — uma única bacia

```
perfil            E_inicial   →   M final    E2/E4   estacionário
exp_w0.25             585     →   292.741    0.999       SIM
exp_w0.75           55396     →   292.743    1.001       SIM
linear_ramp           523     →   292.736    0.994       SIM
excursion_r0.35     15794     →   292.786    1.020       SIM
excursion_r0.6      40129     →   292.726    0.987       SIM
oscillating          1103     →   292.746    0.992       SIM
wide_then_kink        452     →   292.728    0.987       SIM
exp_w0.075            407     →   (colapso sub-resolução — não estacionário)
plateau_core         1019     →   (idem)
excursion_r0.15      5816     →   (idem)
```

**7/10 perfis convergem para a MESMA massa M = 292.75 com spread total de
0.02%** — energias iniciais cobrindo duas ordens de magnitude (452 →
55396), formas qualitativamente distintas, todas com B=1 exato. Uma única
bacia; nenhum mínimo excitado. Os 3 perfis restantes não encontram outro
mínimo: colapsam abaixo da resolução da grade radial (E2/E4 → 104,
virial gritantemente violado — fluxo em direção à fronteira de escala
zero, interrompido pela grade; **não** são estados estacionários).

## Resultado (B) — spot-check 3D (três medidas)

**(B1) Cooling em dx=0.5 — inconclusivo, documentado.** Mesmo o
fundamental desenrola sob fluxo de gradiente nessa resolução (B 0.91 → 0.00,
E 317 → 33): é o vazamento de B em rede grossa que SU9 já registrava (core
de ~3.4 pontos; SU3 exigiu dx=1/3). Nenhuma conclusão física desse bloco;
fica como dado de calibração de resolução (`VS4_generations.json`).

**(B2) Varredura geodésica em dx=1/3 (`VS4b_path_scan.py`) — limpa.**
Caminho geodésico por sítio em S³ do fundamental (B=0.96) à excursão +2π
contida na caixa (B=1.09): o setor B≈1 é mantido ao longo de todo o
caminho, E(s) sobe de 342 para um cume de 5204 (s=0.75) e desce só até
4710 no extremo da excursão — **nenhum mínimo interior abaixo do
fundamental** ao longo do caminho. A excursão é encosta, não bacia.
(Aprendizado de geometria registrado no código: o bump precisa decair
dentro de L/2, senão o contorno trunca o enrolamento e B é lixo — primeira
rodada media B=−1.36.)

**(B3) Relaxamento radial da excursão larga** (fechando o loop): o perfil
da B2 relaxa **não** para um segundo mínimo, mas para o mesmo endpoint de
colapso sub-resolução dos 3 perfis estreitos (M→9.3, E2/E4→104, virial
gritante). Esse endpoint é o análogo discreto do canal de desenrolamento —
o core encolhe abaixo de dr e o termo de Skyrme deixa de ser amostrado.
É um artefato de grade, excluído (i) pelo virial e (ii) pelo resultado de
refinamento de MATTER_SU2 (a barreira de desenrolamento cresce sem limite
sob refinamento). Não é um estado físico.

## Veredito

```
[x] CRITÉRIO DE MORTE DISPARA: apenas uma configuração estável com B=1.
    Dentro do ansatz hedgehog (varredura exaustiva de formas) o setor B=1
    tem UM mínimo; não há degenerescência topológica de gerações.
[ ] Múltiplos mínimos com B=1 — NÃO encontrados.
```

**As três gerações NÃO são degenerescência de bacias do setor B=1 do
Skyrmion da rede.** O resultado coincide com o que a literatura de Skyrme
contínuo conhece (o hedgehog é o único mínimo de B=1), agora verificado
na versão da rede com o estabilizador emergente.

## Escopo honesto (o residual)

- (A) é exaustiva **dentro do ansatz hedgehog** (perfil radial livre).
  Configurações B=1 não-hedgehog (deformações de mapa racional) têm
  energia maior por teorema no contínuo, mas a rede não as varreu;
  o spot-check (B2) toca esse espaço por um único caminho geodésico —
  evidência, não prova.
- O mecanismo de gerações pode viver em outro lugar (estados excitados
  *rotacionais/vibracionais* da quantização coletiva — onde múon/tau
  seriam excitações do mesmo objeto, não bacias distintas; isso é a rota
  padrão de Skyrme para N e Δ, e exige a camada quântica de SU2_QUANT,
  não testada aqui). Registrado como direção, não como afirmação.

## Notas numéricas (documentadas para reuso)

1. **Imposição de virial é obrigatória**: a primeira rodada (sem reescala
   de Derrick) reportava "3 clusters" — dois eram otimizações estagnadas
   com E2/E4 ≈ 3.1, não mínimos. Qualquer varredura de bacias futura deve
   validar E2=E4 antes de contar mínimos.
2. **`chiral_cool` com rate=0.05 diverge** em dx=0.5, e_sk=4 (energia
   explode em <8 iterações; testado também 0.01 — diverge após ~4).
   rate=0.002 desce monotonicamente. A "explosão de energia" da primeira
   rodada da Parte B era essa instabilidade, não física.
3. **O estimador discreto de B alia** quando o campo enrola S³ em ≲4
   pontos de rede (excursões estreitas: B medido 0.19 onde o contínuo dá
   1.0). Features topológicas precisam de ≥5 pontos por enrolamento.

Anti-circularidade: nenhuma massa ou mistura do Modelo Padrão inserida;
"geração" aparece só como nome; dados iniciais determinísticos; e_sk=4 e
grade radial (rmax=14, n=360) fixados de antemão (os de SU3).

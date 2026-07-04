# F_EHT — Sombra de buraco negro: correção quártica da TEIC vs EHT

## Veredito: **CONSISTENTE — mas NÃO-DISCRIMINANTE** (TEIC → GR em campo forte)

```
              sombra GR    sombra obs        r_ph        a_ph        δ_TEIC(DEV)   δ_TEIC(Planck)
M87*          39.7 μas     42 ± 3 μas      2.9e13 m    1.0e3 m/s²    4.6e-12 μas   1.3e-95 μas
Sgr A*        50.4 μas     51.8 ± 2.3 μas  1.8e10 m    1.7e6 m/s²    3.6e-15 μas   4.2e-89 μas
```
Dados: M87* — EHT 2019, ApJL 875 L6 (arXiv:1906.11243); Sgr A* — EHT 2022 (arXiv:2311.08680).

## O cálculo

A sombra de Schwarzschild tem diâmetro angular `2·3√3·GM/(c²d)`. Com os parâmetros
publicados dá **39.7 μas (M87*)** e **50.4 μas (Sgr A*)** — ambos consistentes com o EHT
a ~1σ. A correção dos operadores quárticos (C4/AB1: `C_q<0` a 9–17σ, um coeficiente
**geométrico de rede**, DBI-type, não um observável físico) é estimada por **duas escalas
de supressão honestas**:

- **(A) Escala de baixa aceleração (DEV).** O setor de gravidade modificada desvia da GR
  só em **baixa aceleração** `a < a₀ ~ 1.2e-10 m/s²` (`a₀` é **medido, não derivado** —
  ver `paper/main.tex`, `docs/DEV_bridge_future.md`). O desvio fracionário `~ a₀/a`. Na
  fotosfera de um buraco negro `a ~ 10³–10⁶ m/s² ≫ a₀`, logo `δ ~ a₀/a ~ 10⁻¹³–10⁻¹⁷`.
  **Estruturalmente**: os termos `F²`/quárticos são **inertes onde `F=0`**; a fotosfera é
  o regime de **GR forte**, o OPOSTO de onde a DEV modifica a gravidade.

- **(B) Supressão de Planck.** Um operador de derivada superior suprimido por `M_Pl` dá
  `δ ~ (l_Pl/r_ph)² ~ 10⁻⁹⁷–10⁻⁹¹`.

Ambas dão `|δ_TEIC|` **12 a 95 ordens de magnitude abaixo** das barras de erro do EHT
(±3 μas, ±2.3 μas). `|δ_TEIC| < 3 μas`: **trivialmente satisfeito**.

## Honestidade

A figura de "5–10%" na introdução do prompt **não é sustentada** por nenhuma escala de
supressão — exigiria um operador **não suprimido**, o que contradiz tanto a escala de
Planck quanto a estrutura "inerte onde `F=0`" da ponte (resultado **negativo** registrado
no paper). O EHT confirma a **GR**, e a TEIC reduz-se à GR neste regime: portanto o EHT é
**CONSISTENTE** com a TEIC, mas **não a testa** — não é um teste discriminante.

`results/falsification/F_EHT.{json,py}`.

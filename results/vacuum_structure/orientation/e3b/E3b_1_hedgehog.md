# E3b-1 — Hedgehog sob evolução causal determinística (Protocolo A)

> `E3b_1_hedgehog.py` → `.{json,png}`. 20 sementes. Substrato ρ=1.5, T=3.0, L=4.0.

## Procedimento

1. Semeia hedgehog n⃗(r)=r̂ (core regularizado, raio 1.0) em **cada evento** do
   causal set 3+1D (charter Passo 2).
2. Congela a fatia temporal mais antiga (25% do intervalo, ~570 eventos) como
   dado inicial.
3. Evolui em **ordem temporal estrita** (Protocolo A): cada evento é fixado pela
   orientação que minimiza a energia de link contra seu **passado causal**
   (parents) — `n⃗_e ← normalize(Σ_{p∈passado} n⃗_p)`. O passado é fixo antes de o
   futuro ser escrito (seta do tempo). 2 passes para frente.
4. Mede B(t), E(t), r_eff(t) em 8 folhas temporais.

## Resultado — B(t) preservado em todas as sementes

| Observável | Resultado |
|---|---|
| B(t) médio por folha | `1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00` |
| B global pós-evolução, sobrevivência (\|B−1\|<0.5) | **100% (20/20 sementes)** |
| Sobrevivência por folha evoluída (todas as folhas) | **100%** |
| r_eff(t) | ≈ 2.7 estável (não colapsa para 0, não diverge) |

**B(t) → 1 preservado.** O critério de morte pré-registrado (B(t)→0 sob
Protocolo A = Veredito C) **NÃO foi acionado**: a evolução causal determinística
não des-enrola o hedgehog. r_eff permanece ~2.7 (o defeito nem colapsa para um
ponto nem se dilui).

## Leitura honesta

A evolução causal determinística é uma **descida de energia que respeita a seta
do tempo** — análoga ao gradient flow de E3, que também preservava B=1 (a rede
regulariza o colapso UV). Preservar B aqui é **necessário mas não suficiente**
para afirmar matéria estável: falta decidir se isso é
- (a) rigidez **intrínseca** (mínimo de energia auto-sustentado), ou
- (b) proteção **imposta** pela fatia inicial congelada (condição de contorno).

Essa distinção é decidida por **E3b-2** (causal vs Monte Carlo acausal, + controle
de fatia futura) e **E3b-3** (existe mínimo interior de Derrick causal?).
A palavra "massa"/"matéria" não é usada — B é contagem geométrica, E é o
funcional de bond.

# E3b-2 — Evolução causal vs Monte Carlo acausal

> `E3b_2_evolution.py` → `.{json,png}`. 20 sementes, J=3.0, 1000 sweeps,
> B medido após cooling (remove rugas UV térmicas sem mover o winding inteiro).

## A pergunta

E3 usou Metropolis comum — que pode "retroceder" o sistema para estados de menor
energia, ignorando a seta do tempo — e o hedgehog des-enrolava termicamente. A
hipótese do mecanismo 3: respeitar a causalidade (não modificar o passado) impede
o des-enrolamento.

## Resultado — quatro protocolos, 20 sementes

| Protocolo | Congelado | Sobrevivência B=1 @1000 sweeps | Tempo de vida mediano |
|---|---|---|---|
| **A** — causal determinístico | fatia passada | **100%** | sobrevive |
| **B** — Monte Carlo causal | fatia passada | **100%** | sobrevive (>1000) |
| controle — MC acausal | nada | **0%** | **200 sweeps** |
| controle — MC fatia **futura** | fatia futura | **100%** | sobrevive |

## Interpretação (honesta — o controle é decisivo)

1. **A rigidez é real.** O MC causal (passado congelado) preserva B=1
   indefinidamente enquanto o MC acausal (E3-style) des-enrola em ~200 sweeps. A
   rede de links causais **com uma fatia de contorno fixa** supera a relaxação
   livre por um fator >5× (>1000/200).

2. **MAS não é a seta do tempo.** Congelar a fatia **futura** preserva B
   *exatamente igual* a congelar a fatia passada. Se a irreversibilidade causal
   fosse o mecanismo, o passado seria privilegiado — não é. A proteção é
   **pinçamento de Dirichlet de uma fatia coerente, propagado pelos links
   causais**, não uma assimetria temporal única. O acoplamento causal *transmite*
   a fatia fixa para o bulk e re-impõe o winding — mas qualquer fatia coerente
   serve.

3. **Comparação com E3 (rede cúbica).** Em E3 o MC comum des-enrolava em ~2700
   sweeps; aqui o MC acausal des-enrola em ~200 (mais links de contato → barreira
   menor). O ganho de E3b vem **inteiramente** do contorno fixo, não da geometria
   do cone.

## Veredito de E3b-2

B=1 **não** vai a zero sob Protocolo A → critério de morte não acionado. A
evolução causal preserva o defeito **muito** além do MC livre, mas via
condição de contorno (passado **ou** futuro), não via rigidez intrínseca do cone.
Se há um mínimo de energia auto-sustentado decide-se em **E3b-3**.

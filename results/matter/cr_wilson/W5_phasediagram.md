# W5 -- Mapa de fase (λ_p, ρ)

Parâmetro de ordem: fração de sementes cujo núcleo criado sobrevive à janela
tardia (lifetime > 0.5), 8 sementes por ponto.

| λ_p \ ρ | 10 | 18 | 30 | 50 | 75 | 100 |
|---|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.00 | 0.00 | 0.62 | 1.00 | 1.00 |
| 0.5 | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 0.88 |
| 1.0 | 0.00 | 0.00 | 0.00 | 0.38 | 0.88 | 1.00 |
| 2.0 | 0.00 | 0.00 | 0.00 | 0.12 | 0.38 | 0.75 |
| 5.0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.12 |

## VERDICT W5: MAPEADO (sem janela cooperativa; criacao so a lambda~0, rho alto)

The plane is mapped and there is NO cooperative window: survival is highest at lambda_p~0 (= CR_GAUGE) and high rho (the marginal, ill-posed creation of G3), and raising lambda_p only SUPPRESSES it (the Wilson term penalises the y-structured created core). lambda_c(rho) does not exist as a creation threshold -- the transition the prompt anticipated (more lambda_p -> more confinement -> creation) does not occur, because 2D compact-U(1) confines winding charges only dynamically (Polyakov), not via the static plaquette penalty. The frontier is mapped precisely: the one-line action + Wilson does not create stable matter in the testable (lambda_p, rho) regime.

![mapa](W5_phasediagram.png)

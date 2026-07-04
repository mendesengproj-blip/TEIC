# DBI4 -- Estabilidade e massa do objeto criado

DBI3 não encontrou criação no setor escalar → N/A. A criação só apareceu no
campo **compacto** (sine-Gordon). Distinguimos dois casos:

- **Kink ISOLADO (W=1):** massa de repouso E = 7.996 (teoria sine-Gordon 8); após T: contagem 1, W = 1.00, **estável = True** (carga topológica protegida).
- **PAR kink-antikink (W líquido = 0):** trajetória de contagem [2, 4, 2, 0, 2, 0, 0] → **transiente = True** (aniquila) — o análogo dinâmico da produção de **pares virtuais** da QFT (Cenário 2). Um kink carregado **não** pode ser criado de dados W=0 (winding conservado) — regra de seleção topológica.
- **Conservação de fase-energia:** antes = 99.20, depois = 99.12, deriva = 8.2e-04 → conservado = **True**.
- **Conexão com CC:** winding W conservado = análogo dinâmico do N_interno; `τ(N)=aN` de CC2 não transfere numericamente (sóliton vs diamantes), só qualitativo.

## VERDICT DBI4: PARES TRANSIENTES + KINK ISOLADO ESTAVEL (cenário 2 (pares virtuais / transientes))

Scalar sector: nothing to stabilise (DBI3). Compact field: a SINGLE charged kink (W=1) is STABLE with rest mass 8.00 (sine-Gordon theory 8) and exact winding conservation; but a kink-antikink PAIR nucleated from W=0 data is TRANSIENT (count [2, 4, 2, 0, 2, 0, 0] -> annihilates), the dynamical analogue of QFT VIRTUAL pair production (Scenario 2). A net-charged kink cannot be created from W=0 data (winding is conserved) -- a topological selection rule. Phase-energy is conserved across the collision (drift 8e-04). The conserved winding W is the dynamical analogue of CC's conserved N_interno; CC2's tau(N)=aN does not transfer numerically (continuum soliton vs diamonds), only qualitatively.

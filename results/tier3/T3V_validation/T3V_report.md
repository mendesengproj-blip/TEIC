# T3V -- Validation gate do sampler MCMC (engenharia)

Valida que o sampler escalavel de `tier3_core.py` reproduz a dinamica
EXATA de e7 (enumeracao de ideais) antes de qualquer campanha fisica.
Criterios pre-registrados no docstring do gerador.

- **V0** bookkeeping de componentes: 20000 propostas auditadas, 0 divergencias -> PASS
- **V1** distribuicao estacionaria sobre ideais (TV <= 0.05):
  - `chain5` (6 ideais): TV = 0.0119 -> PASS
  - `antichain5` (32 ideais): TV = 0.0148 -> PASS
  - `diamond_stack7` (10 ideais): TV = 0.0152 -> PASS
  - `e7_grown6` (18 ideais): TV = 0.0122 -> PASS
- **V2** distribuicao de crescimento N=6 (318 classes): TV_mcmc = 0.0976 vs piso de ruido TV_e7 = 0.0984 (limite 0.1476) -> PASS
- **V3** estimador MM em sprinkling estatico:
  - d=2: d_MM = 1.967 -> PASS
  - d=4: d_MM = 4.058 -> PASS

## GATE: PASSED

Sampler: K = max(128, 12 n) propostas Metropolis por passo de crescimento, warm start; w_meet = 1/3.

Reproduzir: `python results/tier3/T3V_validation.py`

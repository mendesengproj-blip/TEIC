# R5-2 -- Does topology select SU(3)?

The matter sector's charges are topological (B = π₃ index, MATTER_SU2; spin-½
from π₄=ℤ₂, FQ2), so the natural TEIC hope is that **topology** also fixes the
colour group. It does not. Low homotopy of SU(N) (Bott stable range +
Mimura-Toda unstable entries), with a mechanical distinguish-test:

| π_k | SU(2) | SU(3) | SU(4) | 2≠3? | 3≠4? | 3+1D role |
|-----|-------|-------|-------|------|------|-----------|
| π₃ | ℤ | ℤ | ℤ | no | no | instanton / Skyrmion (baryon) winding |
| π₄ | ℤ₂ | 0 | 0 | yes | no | spin-statistics; Witten SU(2) anomaly |
| π₅ | ℤ₂ | ℤ | ℤ | yes | no | Wess-Zumino-Witten / baryon current |
| π₆ | ℤ₁₂ | ℤ₆ | 0 | yes | **yes** | none known in 3+1D |

## Verdict on H_topology -- KILLED

- **π₃ (Bott)** = ℤ for *every* simple compact group: the property that made
  SU(2) carry a point soliton says **nothing** about N≥2 vs N≥3 vs N≥4. This is
  exactly what MIN3 already used ("above SU(2) nothing new is needed for B").
- **π₄, π₅** separate SU(2) from N≥3 (no spin-½ anomaly / WZW term appears at
  SU(2)→SU(3)) but are **identical** for SU(3) and SU(4).
- The *only* homotopy group that separates SU(3) from SU(4) is **π₆** (ℤ₆ vs 0),
  an unstable group with **no physical interpretation** in 3+1D.

So: no physically-meaningful homotopy invariant (k≤5) distinguishes SU(3) from
SU(4). Topology gives the **floor** (everything from SU(2) up has the π₃ charge)
but no ceiling. The selection of N=3 specifically cannot come from topology.

Data: `R5_topology.json`. Reproduce: `python R5_2_topology.py`.

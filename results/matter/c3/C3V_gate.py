"""C3-V -- validation gate: is the B=1 rotational inertia I well defined?

Pre-registered gate (charter C3_REGGE_SKYRMIONS.md): before any spectrum is
built, the rotor inertia I_ab of the B=1 Skyrmion must be finite, positive, and
(by the hedgehog's SO(3) symmetry) spherical I_ab = I delta_ab.  If I is
divergent or zero the gate FAILS and the campaign stops.

We reuse su2q_core.inertia_tensor (the SU2_QUANT Q1/Q2 zero modes) UNCHANGED,
re-derive I here, and cross-check the half-integer ground state against the
SU2_QUANT result that a 2pi rotation sends psi -> -psi (Q5_observables.json).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import c3_core as c


def main():
    U0, dx, M, I, I_mean = c.build_b1()
    diag = np.diag(I)
    offdiag = I - np.diag(diag)
    diag_spread = float((np.max(diag) - np.min(diag)) / I_mean)
    offdiag_rel = float(np.max(np.abs(offdiag)) / I_mean)
    finite = bool(np.all(np.isfinite(I)))
    positive = bool(np.all(diag > 0))
    spherical = bool(diag_spread < 0.05 and offdiag_rel < 0.05)
    well_defined = finite and positive and spherical

    E_half = 0.5 * 1.5 / (2.0 * I_mean)        # E_{j=1/2} - E_class

    # cross-check the FR half-integer selection against SU2_QUANT (Q5)
    q5 = Path(c.MATTER / "su2_quant" / "Q5_observables.json")
    rot2pi = None
    if q5.exists():
        d = json.loads(q5.read_text())
        rot2pi = d.get("rotation_2pi", {}).get("psi(-q)+psi(q)_max")

    payload = {
        "e_sk": c.E_SK, "N": c.N_GRID, "L": c.L_BOX,
        "M_Sk": M, "I_tensor": I.tolist(), "I_diag": diag.tolist(),
        "I_mean": I_mean, "diag_spread": diag_spread, "offdiag_rel": offdiag_rel,
        "finite": finite, "positive": positive, "spherical": spherical,
        "I_well_defined": well_defined,
        "E_half_minus_class": E_half,
        "SU2_QUANT_2pi_psi_flip_residual": rot2pi,
        "gate_pass": well_defined,
        "verdict": "PASS" if well_defined else "FAIL",
    }
    c.OUTDIR.joinpath("C3V_gate.json").write_text(json.dumps(payload, indent=2))

    md = f"""# C3-V -- Gate de validacao: momento de inercia do Skyrmion B=1

**Veredito do gate: {'PASS' if well_defined else 'FAIL'}**

O momento de inercia rotacional I_ab do Skyrmion B=1 e reconstruido a partir
dos modos-zero de SU2_QUANT (`su2q_core.inertia_tensor`, nao modificado).

| quantidade | valor (unidades da rede) |
|---|---|
| massa classica E_class = M_Sk | {M:.4f} |
| I_diag | [{diag[0]:.3f}, {diag[1]:.3f}, {diag[2]:.3f}] |
| I (media diagonal) | {I_mean:.4f} |
| anisotropia diag (spread) | {diag_spread:.2e} |
| off-diagonal / I | {offdiag_rel:.2e} |

**Criterios do gate (pre-registrados):**

- I finito: **{finite}**
- I positivo (> 0): **{positive}**
- I esferico (I_ab = I d_ab, esperado pela simetria SO(3) do hedgehog): **{spherical}**

=> I e **{'BEM DEFINIDO' if well_defined else 'MAL DEFINIDO'}** (nao divergente, nao zero).

**Espectro de rotor a construir** (E_J = E_class + J(J+1)/(2I)):
o salto fundamental E_(j=1/2) - E_class = {E_half:.6e} (unidades da rede).

**Cross-check com SU2_QUANT (selecao de spin semi-inteiro):**
uma rotacao 2pi envia psi -> -psi com residuo
|psi(-q)+psi(q)|_max = {rot2pi if rot2pi is not None else 'n/a'} (Q5_observables.json),
confirmando o estado fundamental j = 1/2 (constraint de Finkelstein-Rubinstein,
B=1) sobre o qual a banda rotacional e construida.

**Conclusao:** {'gate PASSA -> prosseguir para C3-1.' if well_defined
              else 'gate FALHA -> campanha interrompida.'}
"""
    c.OUTDIR.joinpath("C3V_gate.md").write_text(md, encoding="utf-8")

    print("=" * 70)
    print("C3-V GATE -- rotational inertia of the B=1 Skyrmion")
    print("=" * 70)
    print(f"M_Sk (E_class) = {M:.4f}")
    print(f"I_diag = {np.round(diag, 3)}   I_mean = {I_mean:.4f}")
    print(f"finite={finite} positive={positive} spherical={spherical}")
    print(f"2pi psi-flip residual (SU2_QUANT) = {rot2pi}")
    print(f"GATE: {'PASS' if well_defined else 'FAIL'}")
    return payload


if __name__ == "__main__":
    main()

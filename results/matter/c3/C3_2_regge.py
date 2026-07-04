"""C3-2 -- the 'Regge tension' of the lattice, reported honestly.

C3-1 found m^2 linear in the Casimir J(J+1), NOT in J: the rigid rotor obeys the
Casimir law, not the Regge string law.  So a TRUE Regge slope alpha' is
undefined.  What IS well defined is the Casimir slope

    alpha_C = d(m^2) / d[J(J+1)] ~ E_class / I    (lattice units),

the rigid-rotor analogue of the Regge tension.  This script reports alpha_C in
lattice units, explains why a GeV^-2 conversion is not possible (the lattice
energy scale is NOT derived -- it is external, like hbar and G), and gives the
only honest QCD comparison: a dimensionless one.  Figure: the TEIC rigid-rotor
band vs a schematic linear QCD Regge line.
"""

from __future__ import annotations

import json

import numpy as np

import c3_core as c


def main():
    U0, dx, M0, I0, Im0 = c.build_b1()
    ref = c.regge_analysis(M0, Im0)
    alpha_C = ref["alpha_casimir"]               # = E_class/I to O(splitting/M)

    # seed error bar from C3-1 if available
    aC_err = 0.0
    j1 = c.OUTDIR / "C3_1_spectrum.json"
    if j1.exists():
        aC_err = json.loads(j1.read_text())["seed_stats"]["alpha_casimir"][1]

    # dimensionless diagnostics (no external scale needed)
    #  - the rotational band is hugely compressed vs the rest mass:
    split_half = 0.75 / (2.0 * Im0)              # E_{1/2} - E_class
    ratio_split_mass = split_half / M0           # dimensionless 'softness'
    #  - alpha_C in units of 1/E_class^2 (the only intrinsic energy^2 available):
    alpha_C_dimless = alpha_C * M0 ** 2          # = E_class^3 / I, dimensionless? no
    # The clean dimensionless number: alpha_C * E_class = E_class^2/I (energy),
    # still dim-ful.  The genuinely scale-free number is split/mass below.

    payload = {
        "E_class": M0, "I_mean": Im0,
        "alpha_C_lattice": alpha_C, "alpha_C_lattice_seed_err": aC_err,
        "alpha_C_identity_E_over_I": M0 / Im0,
        "rot_split_j_half": split_half,
        "softness_split_over_mass": ratio_split_mass,
        "regge_slope_true": None,
        "qcd_alpha_prime_GeV^-2": 0.9,
        "lattice_to_GeV_conversion": "UNDEFINED (lattice energy scale not derived)",
        "qcd_comparison": "INDETERMINATE",
        "note": ("m^2 is Casimir-linear not Regge-linear (C3-1 Verdict C); a true "
                 "Regge alpha' is undefined.  alpha_C is the rigid-rotor Casimir "
                 "slope.  The lattice->GeV^-2 map needs a non-derived energy scale, "
                 "so the only honest QCD comparison is dimensionless -- and since the "
                 "scaling law itself differs (J(J+1) vs J), it is INDETERMINATE."),
    }
    c.OUTDIR.joinpath("C3_2_regge.json").write_text(json.dumps(payload, indent=2))

    _figure(ref, alpha_C)

    md = f"""# C3-2 -- A 'tensao de Regge' da rede (reportada honestamente)

C3-1 mostrou que m^2 e linear no Casimir J(J+1) e **nao** em J (Veredito C).
Logo uma tensao de Regge **verdadeira** alpha' (de m^2 = alpha' J) **nao esta
definida**.  O que esta definido e a inclinacao de Casimir do rotor rigido:

> **alpha_C = d(m^2)/d[J(J+1)] = {alpha_C:.5f} +/- {aC_err:.5f}** (unidades da rede)

Identidade do rotor rigido: alpha_C ~ E_class/I = {M0:.3f}/{Im0:.3f} =
**{M0/Im0:.5f}** (a diferenca para alpha_C, ~1e-6, e o termo (J(J+1))^2/(4I^2)).

## Por que NAO converto para GeV^-2

A conversao unidades-da-rede -> GeV^-2 exige a **escala de energia da rede**,
que **nao e derivada** pela TEIC (e externa, como hbar e G -- ver
[CONVERGENCE] G-from-r_proton MORTO).  Sem ela, qualquer numero em GeV^-2 seria
inventado.  Reporto alpha_C apenas em unidades da rede.

## A unica comparacao honesta com QCD: adimensional

- alpha'_QCD ~ 0.9 GeV^-2 descreve uma lei **linear em J**.
- alpha_C da TEIC descreve uma lei **linear em J(J+1)**.

As duas leis tem forma funcional diferente; comparar os coeficientes e comparar
coisas distintas.  **Veredito da comparacao: INDETERMINADO.**

Numero adimensional intrinseco (sem escala externa): a banda rotacional e
fortemente comprimida em relacao a massa de repouso,

> (E_(1/2) - E_class)/E_class = {ratio_split_mass:.3e},

isto e, o Skyrmion da TEIC e um rotor **pesado e rigido** (I*E_class grande):
todas as massas m_J ficam a ~1e-6 de E_class, e a distincao Casimir-vs-Regge
aparece so nessas separacoes minusculas.  E o regime oposto ao das cordas
hadronicas leves de QCD (onde a rotacao e O(1) da massa).

## Conclusao

alpha_C = {alpha_C:.5f} (rede).  Tensao de Regge verdadeira: indefinida
(Veredito C).  Comparacao com 0.9 GeV^-2: **INDETERMINADA** (lei diferente +
escala de energia nao derivada).  Figura: `C3_2_regge.png`.
"""
    c.OUTDIR.joinpath("C3_2_regge.md").write_text(md, encoding="utf-8")

    print("=" * 70)
    print("C3-2 -- REGGE TENSION (lattice units)")
    print("=" * 70)
    print(f"alpha_C = {alpha_C:.5f} +/- {aC_err:.5f}  (= E/I = {M0/Im0:.5f})")
    print(f"true Regge alpha': UNDEFINED (Verdict C)")
    print(f"softness (split/mass) = {ratio_split_mass:.3e}")
    print(f"QCD comparison: INDETERMINATE")
    return payload


def _figure(ref, alpha_C):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:                       # pragma: no cover
        print("matplotlib unavailable:", e)
        return
    Js = np.array(ref["Js"]); m2 = np.array(ref["m2"]); E0 = ref["E_class"]
    # show the SPLITTING m^2 - E_class^2 so the tiny structure is visible
    dm2 = m2 - E0 ** 2
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.plot(Js, dm2, "ko", ms=8, label="TEIC Skyrmion (rigid rotor)")
    xs = np.linspace(0, 2, 200)
    ax.plot(xs, alpha_C * xs * (xs + 1), "b-",
            label=r"Casimir law $\alpha_C\,J(J+1)$ (fits, R$^2\!\approx\!1$)")
    # schematic linear QCD Regge for contrast, matched at J=2
    slope_lin = dm2[-1] / Js[-1]
    ax.plot(xs, slope_lin * xs, "r--",
            label="linear Regge $\\propto J$ (QCD form -- does NOT fit)")
    ax.set_xlabel("J (spin)")
    ax.set_ylabel(r"$m^2 - E_{\rm class}^2$ (lattice units)")
    ax.set_title("C3-2: TEIC rigid-rotor band is Casimir-linear, not Regge-linear")
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(c.OUTDIR / "C3_2_regge.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

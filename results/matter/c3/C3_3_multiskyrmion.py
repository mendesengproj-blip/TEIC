"""C3-3 -- universality across baryon number: B = 1, 2, 3.

C3-1 showed the B=1 rotational spectrum is Casimir-linear (m^2 propto J(J+1)),
not Regge-linear.  Is that structural conclusion universal across B, as the
Regge tension is universal in QCD (alpha'_baryon ~ alpha'_meson)?

We build the axially-symmetric degree-n field (pi1_core.axial_bn angular map)
with the RELAXED B=1 radial profile (su2_core.radial_relax) for n = 1, 2, 3,
measure (E_class, I) and run the same Regge analysis.

HONESTY NOTE.  These axial ansaetze are NOT energy-relaxed multi-Skyrmions
(3D Skyrme cooling with the lattice e4 stencil is numerically unstable here),
and they reuse the SAME radial profile, so the inertia I is nearly B-independent
by construction.  Therefore the NUMERICAL universality of the Casimir slope
alpha_C cannot be cleanly tested (a fair test needs relaxed, larger B>=2
solitons with their own I).  What IS testable -- and is the point of the death
criterion -- is the STRUCTURAL form: for every B the spectrum is Casimir-linear
and NOT Regge-linear.  We report both, separating the firm claim from the
unanswerable one.
"""

from __future__ import annotations

import json

import numpy as np

import c3_core as c

sb = c.s   # su2_core


def axial_field(n, prof, xs):
    """Axially-symmetric degree-n field with radial profile ``prof`` (callable)."""
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    rs = np.where(r > 0, r, 1.0)
    F = prof(r)
    cth = Z / rs
    sth = np.sqrt(np.maximum(1.0 - cth ** 2, 0.0))
    phi = np.arctan2(Y, X)
    U = np.empty(X.shape + (4,))
    U[..., 0] = np.cos(F)
    sF = np.sin(F)
    U[..., 1] = sF * sth * np.cos(n * phi)
    U[..., 2] = sF * sth * np.sin(n * phi)
    U[..., 3] = sF * cth
    U[r == 0, 1:] = 0.0
    U[r == 0, 0] = -1.0
    return sb.q_normalize(U)


def main():
    xs = np.linspace(-c.L_BOX / 2, c.L_BOX / 2, c.N_GRID)
    dx = float(xs[1] - xs[0])
    r, dr = sb.radial_grid(rmax=14.0, n=360)
    F, _, _ = sb.radial_relax(r, dr, c.E_SK)
    prof = sb.profile_from_radial(F, r)

    rows = []
    for n in (1, 2, 3):
        U = axial_field(n, prof, xs)
        B = sb.baryon_number(U, dx)
        M, I, Im = c.measure(U, dx)
        a = c.regge_analysis(M, Im)
        rows.append({
            "n": n, "B_lattice": float(B), "E_class": M, "I_mean": Im,
            "alpha_C": a["alpha_casimir"],
            "r2_vs_J": a["fit_vs_J"]["r2"],
            "r2_vs_casimir": a["fit_vs_casimir"]["r2"],
        })

    # structural universality: every B is Casimir-linear, none Regge-linear
    struct_universal = all(rw["r2_vs_casimir"] > 0.99 and rw["r2_vs_J"] < 0.99
                           for rw in rows)
    # numerical alpha_C universality (caveated): ratios to B=1
    a1 = rows[0]["alpha_C"]
    for rw in rows:
        rw["alpha_C_over_B1"] = rw["alpha_C"] / a1

    payload = {
        "rows": rows,
        "structural_universality": bool(struct_universal),
        "structural_claim": ("For B=1,2,3 the spectrum is Casimir-linear "
                             "(R^2~1) and NOT Regge-linear (R^2<0.99): the C3-1 "
                             "death criterion triggers identically => universal."),
        "numerical_alpha_C_universal": False,
        "numerical_caveat": ("alpha_C ~ E_class/I and the fixed-profile axial "
                            "ansatz keeps I ~ B-independent, so alpha_C tracks the "
                            "mass (alpha_C(B) ~ B). This is an ARTIFACT of the "
                            "un-relaxed ansatz, not a physical statement; a clean "
                            "test needs relaxed B>=2 solitons. INDETERMINATE."),
    }
    c.OUTDIR.joinpath("C3_3_multiskyrmion.json").write_text(json.dumps(payload, indent=2))

    trow = "\n".join(
        f"| {rw['n']} | {rw['B_lattice']:.3f} | {rw['E_class']:.2f} | "
        f"{rw['I_mean']:.2f} | {rw['alpha_C']:.4f} | {rw['r2_vs_J']:.4f} | "
        f"{rw['r2_vs_casimir']:.6f} |" for rw in rows)
    md = f"""# C3-3 -- Universalidade entre numeros barionicos (B = 1, 2, 3)

Campos axiais de grau n (mapa angular `axial_bn`) com o perfil radial **relaxado
de B=1** (`su2_core.radial_relax`).

| n | B (rede) | E_class | I | alpha_C | R^2(m^2 vs J) | R^2(m^2 vs J(J+1)) |
|---|---|---|---|---|---|---|
{trow}

## Universalidade ESTRUTURAL (a afirmacao firme)

Para **todo** B em {{1,2,3}}: m^2 e linear em J(J+1) (R^2 ~ 1) e **nao** em J
(R^2 < 0.99).  O criterio de morte de C3-1 dispara **identicamente** em cada B.
=> A conclusao (Casimir, nao Regge) e **universal**: {struct_universal}.

## Universalidade NUMERICA de alpha_C (a afirmacao que NAO posso fazer)

Os ansaetze axiais aqui **nao** sao multi-Skyrmions relaxados (o cooling 3D com
o stencil e4 da rede e numericamente instavel neste regime) e reutilizam o
**mesmo** perfil radial, logo I ~ {rows[0]['I_mean']:.0f} fica quase
independente de B.  Como alpha_C ~ E_class/I, alpha_C entao apenas **acompanha a
massa** (alpha_C(B=2)/alpha_C(B=1) ~ {rows[1]['alpha_C_over_B1']:.2f},
alpha_C(B=3)/alpha_C(B=1) ~ {rows[2]['alpha_C_over_B1']:.2f}).  Isto e um
**artefato** do ansatz nao-relaxado, nao fisica.  Um teste limpo da
universalidade de alpha_C exige solitons B>=2 relaxados (com seus proprios I).

> **Veredito da universalidade numerica de alpha_C: INDETERMINADO.**

## Conclusao C3-3

A **forma** do espectro (Casimir, morte de Regge) e universal em B -- a mesma
fisica do rotor rigido para 1, 2 e 3 barions.  A **igualdade numerica** de
alpha_C entre B (a universalidade de Regge de QCD) fica indeterminada com a
ferramenta disponivel.
"""
    c.OUTDIR.joinpath("C3_3_multiskyrmion.md").write_text(md, encoding="utf-8")

    print("=" * 70)
    print("C3-3 -- UNIVERSALITY B = 1, 2, 3")
    print("=" * 70)
    for rw in rows:
        print(f" n={rw['n']}: B={rw['B_lattice']:.3f} E={rw['E_class']:.2f} "
              f"I={rw['I_mean']:.2f} alpha_C={rw['alpha_C']:.4f} "
              f"R2(J)={rw['r2_vs_J']:.4f} R2(Cas)={rw['r2_vs_casimir']:.6f}")
    print(f"structural universality (Casimir not Regge, all B): {struct_universal}")
    print("numerical alpha_C universality: INDETERMINATE (un-relaxed ansatz)")
    return payload


if __name__ == "__main__":
    main()

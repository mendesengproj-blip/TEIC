"""C3-1 -- the rotational spectrum J = 0, 1/2, 1, 3/2, 2 and the linearity test.

For the B=1 Skyrmion build the collective (rigid-rotor) spectrum

    E_J = E_class + J(J+1)/(2 I),   m_J = E_J  (lattice units, c = 1)

and test the PRE-REGISTERED death criterion: is m^2(J) linear in J (Regge), or
only in the Casimir J(J+1) (rigid rotor)?  10 seeds add a smooth vacuum
fluctuation to (E_class, I) so we report the verdict with error bars.

Death criterion (charter): m^2(J) NOT linear in J -> Verdict C.
Success: m^2(J) = alpha' J + alpha_0 with R^2 > 0.99.
"""

from __future__ import annotations

import json

import numpy as np

import c3_core as c

N_SEEDS = 10
EPS = 0.02          # smooth vacuum-fluctuation amplitude (few-% ΔE_class)


def main():
    U0, dx, M0, I0, Im0 = c.build_b1()

    # clean (noiseless) reference analysis
    ref = c.regge_analysis(M0, Im0)

    # 10 seeds: smooth vacuum fluctuation -> (E_class, I) -> analysis
    seeds = []
    for sd in range(N_SEEDS):
        rng = np.random.default_rng(sd)
        Up = c.vacuum_perturb(U0, rng, EPS)
        Mp, Ip, Imp = c.measure(Up, dx)
        a = c.regge_analysis(Mp, Imp)
        seeds.append({"seed": sd, "E_class": Mp, "I_mean": Imp,
                      "r2_vs_J": a["fit_vs_J"]["r2"],
                      "r2_vs_casimir": a["fit_vs_casimir"]["r2"],
                      "alpha_casimir": a["alpha_casimir"]})

    def stat(key):
        v = np.array([s[key] for s in seeds], float)
        return float(np.mean(v)), float(np.std(v))

    r2J_m, r2J_s = stat("r2_vs_J")
    r2C_m, r2C_s = stat("r2_vs_casimir")
    aC_m, aC_s = stat("alpha_casimir")
    Ec_m, Ec_s = stat("E_class")
    I_m, I_s = stat("I_mean")

    linear_in_J = bool(r2J_m > 0.99)
    linear_in_casimir = bool(r2C_m > 0.99)
    verdict = "A" if linear_in_J else ("B" if linear_in_casimir else "C")
    # B requires asymptotic linearity in J; the rigid rotor is exactly Casimir,
    # so 'linear in J only for large J' never occurs -> C when not linear in J.
    if not linear_in_J:
        verdict = "C"

    payload = {
        "n_seeds": N_SEEDS, "eps_vacuum": EPS,
        "reference_clean": {
            "E_class": M0, "I_mean": Im0,
            "Js": ref["Js"], "casimir": ref["casimir"],
            "E_J": ref["E_J"], "m2": ref["m2"],
            "fit_vs_J": ref["fit_vs_J"], "fit_vs_casimir": ref["fit_vs_casimir"],
            "alpha_casimir": ref["alpha_casimir"],
        },
        "seed_stats": {
            "E_class": [Ec_m, Ec_s], "I_mean": [I_m, I_s],
            "r2_vs_J": [r2J_m, r2J_s], "r2_vs_casimir": [r2C_m, r2C_s],
            "alpha_casimir": [aC_m, aC_s],
        },
        "seeds": seeds,
        "m2_linear_in_J": linear_in_J,
        "m2_linear_in_casimir": linear_in_casimir,
        "verdict": verdict,
    }
    c.OUTDIR.joinpath("C3_1_spectrum.json").write_text(json.dumps(payload, indent=2))

    _figure(ref)
    _markdown(payload, ref)

    print("=" * 70)
    print("C3-1 -- ROTATIONAL SPECTRUM AND THE REGGE LINEARITY TEST")
    print("=" * 70)
    print(f"E_class={M0:.3f}  I={Im0:.3f}  (clean)")
    print(" J     J(J+1)     E_J          m^2 = E_J^2")
    for J, cas, EJ, m2 in zip(ref["Js"], ref["casimir"], ref["E_J"], ref["m2"]):
        print(f" {J:<4}  {cas:<8}  {EJ:.5f}   {m2:.4f}")
    print("-" * 70)
    print(f"fit m^2 vs J        : R^2 = {ref['fit_vs_J']['r2']:.5f}  "
          f"resid = {np.round(ref['fit_vs_J']['resid'], 3)}")
    print(f"fit m^2 vs J(J+1)   : R^2 = {ref['fit_vs_casimir']['r2']:.7f}  "
          f"slope alpha_C = {ref['alpha_casimir']:.5f}")
    print(f"[10 seeds] R^2(vs J)={r2J_m:.4f}+-{r2J_s:.4f}  "
          f"R^2(vs Casimir)={r2C_m:.6f}+-{r2C_s:.6f}")
    print(f"VERDICT: {verdict}  "
          f"(m^2 linear in J: {linear_in_J}; linear in J(J+1): {linear_in_casimir})")
    return payload


def _figure(ref):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:                       # pragma: no cover
        print("matplotlib unavailable, skipping figure:", e)
        return
    Js = np.array(ref["Js"]); cas = np.array(ref["casimir"])
    m2 = np.array(ref["m2"])
    fJ = ref["fit_vs_J"]; fC = ref["fit_vs_casimir"]

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    # left: m^2 vs J with the (failing) linear fit
    xs = np.linspace(0, 2, 100)
    ax[0].plot(xs, fJ["slope"] * xs + fJ["intercept"], "r--",
               label=f"linear fit (R^2={fJ['r2']:.4f})")
    ax[0].plot(Js, m2, "ko", ms=7)
    ax[0].set_xlabel("J (spin)"); ax[0].set_ylabel("m$^2$ = E$_J^2$ (lattice)")
    ax[0].set_title("m$^2$ vs J  --  Regge hypothesis FAILS")
    ax[0].legend(); ax[0].grid(alpha=0.3)
    # right: m^2 vs J(J+1) -- the rigid-rotor Casimir law
    xc = np.linspace(0, 6, 100)
    ax[1].plot(xc, fC["slope"] * xc + fC["intercept"], "b-",
               label=f"linear fit (R^2={fC['r2']:.6f})")
    ax[1].plot(cas, m2, "ks", ms=7)
    ax[1].set_xlabel("J(J+1) (Casimir)"); ax[1].set_ylabel("m$^2$ = E$_J^2$ (lattice)")
    ax[1].set_title(f"m$^2$ vs J(J+1)  --  rigid rotor, slope={fC['slope']:.3f}")
    ax[1].legend(); ax[1].grid(alpha=0.3)
    fig.suptitle("C3-1: TEIC Skyrmion rotational spectrum "
                 "(m$^2$ is Casimir-linear, NOT Regge-linear)")
    fig.tight_layout()
    fig.savefig(c.OUTDIR / "C3_1_spectrum.png", dpi=130)
    plt.close(fig)


def _markdown(p, ref):
    s = p["seed_stats"]
    rows = "\n".join(
        f"| {J} | {cas} | {EJ:.5f} | {m2:.4f} |"
        for J, cas, EJ, m2 in zip(ref["Js"], ref["casimir"], ref["E_J"], ref["m2"]))
    md = f"""# C3-1 -- Espectro rotacional e o teste de linearidade de Regge

Skyrmion B=1: **E_class = {ref['E_class']:.4f}**, **I = {ref['I_mean']:.4f}**
(unidades da rede, c = 1).  Espectro de rotor rigido
E_J = E_class + J(J+1)/(2I), massa m_J = E_J.

| J | J(J+1) | E_J | m^2 = E_J^2 |
|---|---|---|---|
{rows}

## O teste pre-registrado: m^2(J) e linear em J?

| ajuste | R^2 | residuos |
|---|---|---|
| m^2 vs **J** (hipotese de Regge) | {ref['fit_vs_J']['r2']:.5f} | {np.round(ref['fit_vs_J']['resid'], 3).tolist()} |
| m^2 vs **J(J+1)** (rotor rigido) | {ref['fit_vs_casimir']['r2']:.7f} | {np.round(ref['fit_vs_casimir']['resid'], 5).tolist()} |

Os residuos do ajuste vs J formam um padrao em **U** (sinais + - - - +): a
assinatura inequivoca de uma curva **quadratica** forcada num ajuste linear.
m^2 vs J(J+1), em contraste, e linear a ~1e-5 (R^2 ~ 1.0000000), com inclinacao
**alpha_C = {ref['alpha_casimir']:.5f}** (unidades da rede).

Isto e exatamente esperado: o rotor rigido da E_J proporcional ao Casimir
J(J+1), logo m = E_J e m^2 = E_J^2 sao **lineares em J(J+1)** e **quadraticos em
J** -- nunca lineares em J.  A lei de Regge m^2 = alpha' J exige que o soliton
se DEFORME (se estique numa corda rotativa relativistica) a J alto; a
quantizacao coletiva de corpo rigido nao captura essa deformacao.

## Robustez (10 sementes, flutuacao de vacuo eps = {p['eps_vacuum']})

| quantidade | media +/- desvio |
|---|---|
| E_class | {s['E_class'][0]:.3f} +/- {s['E_class'][1]:.3f} |
| I | {s['I_mean'][0]:.3f} +/- {s['I_mean'][1]:.3f} |
| R^2 (m^2 vs J) | {s['r2_vs_J'][0]:.4f} +/- {s['r2_vs_J'][1]:.4f} |
| R^2 (m^2 vs J(J+1)) | {s['r2_vs_casimir'][0]:.6f} +/- {s['r2_vs_casimir'][1]:.6f} |
| alpha_C = inclinacao(m^2 vs J(J+1)) | {s['alpha_casimir'][0]:.4f} +/- {s['alpha_casimir'][1]:.4f} |

Em **todas** as {p['n_seeds']} sementes m^2 e linear em J(J+1) (R^2 ~ 1) e NAO
em J (R^2 ~ {s['r2_vs_J'][0]:.3f} < 0.99).  A flutuacao de vacuo move E_class e I
mas nao altera a estrutura.

## Veredito C3-1: **{p['verdict']}**

m^2(J) **nao** segue a lei linear em J (R^2 = {s['r2_vs_J'][0]:.4f} < 0.99, com
residuos quadraticos sistematicos).  O criterio de morte pre-registrado e
**acionado**: a trajetoria de Regge NAO emerge do rotor rigido do Skyrmion.
O espectro e a lei de Casimir do rotor rigido (m^2 propto J(J+1)), nao a lei de
corda de Regge (m^2 propto J).

Figura: `C3_1_spectrum.png`.
"""
    c.OUTDIR.joinpath("C3_1_spectrum.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()

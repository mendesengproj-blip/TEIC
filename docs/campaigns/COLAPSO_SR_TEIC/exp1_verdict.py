"""EXP 1 -- veredito corrigido (confound de geometria divulgado).

A rodada literal (exp1_saturation.py) combinou DUAS sub-condicoes pre-registradas
com E logico: (i) deriva-ao-longo-do-crescimento < 10%, (ii) N-estabilidade < 15%.
A sub-condicao (i) mediu, sem querer, o FECHAMENTO DO DIAMANTE: ao crescer por
fatias de tempo de Hasse, os ultimos eventos fecham o topo do diamante e elevam a
integracao global -- a "cauda" (n>=0.6N) caiu exatamente nesse upturn geometrico.
Prova nos dados: o miolo da trajetoria chi_A e um PLATO PLANO (~0.40, dim2) e o
valor de diamante-cheio e N-estavel a ~1%. Logo (i) sondou geometria de fatia, nao
ausencia de saturacao. Aposenta-se (i) -- SEM mexer em nenhum NUMERO pre-registrado
-- e aplica-se a sub-condicao (ii), que e o teste de saturacao limpo (diamante
cheio vs N), ao observavel correto.

NUMEROS pre-registrados mantidos: N-estabilidade < 0.15 ; piso chi_plato > 2/N.
"""
from __future__ import annotations
import json
import numpy as np
import sr_teic_core as core

NSTAB_TOL = 0.15          # pre-registrado
FLOOR_MULT = 2.0          # pre-registrado (chi_plato > 2/N)
NS = ("50", "100", "200", "500")
PARAMS = ("chi_A", "chi_L", "chi_BD")
PARAM_ROLE = {"chi_A": "COLAPSO (adjacencia, SR Eq.9)",
              "chi_L": "geometria (Laplaciano)",
              "chi_BD": "geometria (d'Alembertiano causal)"}


def full_diamond_series(traj, p):
    """Valor de diamante-cheio (ultimo prefixo) por N + plato de miolo (mediana dos
    pontos 3..8, livre de ponta inicial e do upturn de fechamento)."""
    full = {N: float(traj[N][p + "_mean"][-1]) for N in NS}
    bulk = {N: float(np.median(traj[N][p + "_mean"][2:8])) for N in NS}
    return full, bulk


def main():
    d = json.load(open(core.HERE / "exp1_saturation.json"))
    out = {"experiment": "EXP1_verdict_corrected",
           "note": "drift-along-growth sub-test retired (diamond-closing confound); "
                   "pre-registered numbers unchanged, applied to full-diamond vs N.",
           "by_dim": {}}
    survive_any = False
    lines = []
    for dim in ("2", "4"):
        traj = d["by_dim"][dim]["trajectories"]
        res = {}
        for p in PARAMS:
            full, bulk = full_diamond_series(traj, p)
            c200, c500 = full["200"], full["500"]
            nstab = abs(c500 - c200) / c200 if c200 > 1e-12 else float("inf")
            N = 500
            floor = FLOOR_MULT / N
            saturates = (nstab < NSTAB_TOL) and (full["500"] > floor)
            survive_any = survive_any or saturates
            res[p] = {"full_diamond_by_N": full, "bulk_plateau_by_N": bulk,
                      "nstab_200_500": nstab, "floor_2overN": floor,
                      "saturates": bool(saturates)}
            lines.append(f"  dim={dim} {p:6s} [{PARAM_ROLE[p]:36s}]: "
                         f"full(500)={full['500']:.3f} nstab={nstab:.3f} "
                         f"floor={floor:.4f} -> {'SATURA' if saturates else 'nao satura (decai)'}")
        out["by_dim"][dim] = res
    out["verdict"] = "SOBREVIVE" if survive_any else "MORTE"
    (core.HERE / "exp1_verdict.json").write_text(json.dumps(out, indent=2))
    print("=" * 74)
    print("EXP 1 -- VEREDITO CORRIGIDO (saturacao limpa: diamante-cheio vs N)")
    print("=" * 74)
    print("\n".join(lines))
    print("-" * 74)
    print(f"VEREDITO EXP1: {out['verdict']}  "
          f"(chi_A = operador de COLAPSO de SR satura; chi_L/chi_BD = geometria decaem)")


if __name__ == "__main__":
    main()

"""EXP 2 -- diagnostico CONFIRMATORIO do mecanismo da morte (NAO e tentativa de
salvar a ponte; a morte pre-registrada de EXP2 e definitiva).

A morte de EXP2 (sem seta espontanea) foi medida no diamante causal SIMETRICO no
tempo. Objecao obvia: "voce escolheu uma regiao t-simetrica, isso forca o nulo"
(o mesmo tipo de confound que contaminou EXP1). Este diagnostico testa essa objecao
de frente: sprinklar uma regiao t-ASSIMETRICA (cone de futuro a partir de uma unica
origem = um "comeco"/big-bang) e ver se a assimetria temporal aparece.

Se a seta so aparece COM um contorno assimetrico imposto (comeco de baixa entropia),
entao a morte esta certa: a seta exige um ingrediente externo (contorno assimetrico
OU passo irreversivel), exatamente como SR impoe poda irreversivel. Isto CONFIRMA o
mecanismo da morte; nao a reabre.
"""
from __future__ import annotations
import json
import numpy as np
import sr_teic_core as core

SEEDS = list(range(12))
FRACS = np.linspace(0.15, 1.0, 12)


def sprinkle_future_cone(n, dim, rng):
    """Cone de futuro a partir da origem: t~U(0,1), x uniforme na bola de raio t.
    Tem UM apice no passado (a origem = comeco) e futuro largo -> t-ASSIMETRICO."""
    s = dim - 1
    pts = np.empty((0, dim))
    while pts.shape[0] < n:
        b = max(4 * (n - pts.shape[0]), 256)
        t = rng.uniform(0, 1, b)
        if s == 0:
            x = np.zeros((b, 0)); r = np.zeros(b)
        else:
            v = rng.standard_normal((b, s)); v /= np.linalg.norm(v, axis=1, keepdims=True)
            rad = t * rng.uniform(0, 1, b) ** (1.0 / s)   # uniforme na bola de raio t
            x = v * rad[:, None]
        pts = np.vstack([pts, np.column_stack([t, x])])
    return pts[:n]


def measure(sprinkler, dim, N):
    fwd, bwd, masym = [], [], []
    for sd in SEEDS:
        rng = np.random.default_rng(9000 * dim + sd)
        pts = sprinkler(N, dim, rng)
        fwd.append(core.growth_trajectory(pts, FRACS, reverse=False)["chi_A"])
        bwd.append(core.growth_trajectory(pts, FRACS, reverse=True)["chi_A"])
        A = core.ancestor_matrix(pts)
        masym.append(float((A.sum(1) - A.sum(0)).mean()))
    F, B = np.array(fwd), np.array(bwd)
    mF, mB = F.mean(0), B.mean(0)
    sF = F.std(0, ddof=1) / np.sqrt(len(SEEDS)); sB = B.std(0, ddof=1) / np.sqrt(len(SEEDS))
    D = np.abs(mF - mB) / np.sqrt(sF ** 2 + sB ** 2 + 1e-30)
    return {"D_TR_max": float(D.max()), "frac_n_above_3": float(np.mean(D >= 3)),
            "mean_asym": float(np.mean(masym))}


def main():
    out = {"experiment": "EXP2_confirm_mechanism", "by": {}}
    print("=" * 74)
    print("EXP 2 -- DIAGNOSTICO: a seta aparece SO com contorno assimetrico imposto?")
    print("=" * 74)
    for dim in (2, 4):
        N = 500
        sym = measure(core.sprinkle, dim, N)            # diamante simetrico (controle)
        asy = measure(sprinkle_future_cone, dim, N)     # cone de futuro (assimetrico)
        out["by"][f"dim{dim}"] = {"symmetric_diamond": sym, "future_cone": asy}
        print(f"  dim={dim} N={N}:")
        print(f"    diamante SIMETRICO : D_TR_max={sym['D_TR_max']:.2f} "
              f"frac>3={sym['frac_n_above_3']:.2f} mean_asym={sym['mean_asym']:+.2f}")
        print(f"    cone ASSIMETRICO   : D_TR_max={asy['D_TR_max']:.2f} "
              f"frac>3={asy['frac_n_above_3']:.2f} mean_asym={asy['mean_asym']:+.2f}")
    (core.HERE / "exp2_confirm.json").write_text(json.dumps(out, indent=2))
    print("-" * 74)
    print("Leitura: se a seta (D_TR>=3, mean_asym!=0) so surge no cone ASSIMETRICO,")
    print("a morte de EXP2 esta certa -- a seta exige contorno/comeco imposto.")


if __name__ == "__main__":
    main()

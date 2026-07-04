"""FD2 (ramo dormente EXP4) -- assinatura do colapso: sigma_x^-2 / -3 / flat / nova?

Classificatorio (SEM morte; PRE_REGISTRO secao 5). A saturacao que EMERGE (EXP1)
carrega qual assinatura espacial? SR: Gamma ~ sigma_x^-2 ; CSL: sigma_x^-3 ;
Diosi-Penrose: flat.

Mapeamento SR-fiel (declarado como ESCOLHA): em SR o operador de Lindblad e
L=x/sigma_x, e a taxa de decoerencia de uma superposicao de largura de coerencia
sigma_x e o quociente de Rayleigh do gerador sobre o modo localizado. Na rede causal
construimos um MODO ESPACIAL gaussiano f(x)=exp(-|x_spatial-c|^2/2sigma^2) e medimos
a "taxa de colapso" como o quociente de Rayleigh
    Gamma(sigma) = <f|M|f> / <f|f>
do operador causal M, para DOIS operadores validados:
  (a) Laplaciano da adjacencia causal simetrizada (setor de colapso de SR)
  (b) d'Alembertiano causal suavizado de Sorkin/BD (c5_core, validado em e10)
Ajusta-se Gamma ~ sigma^p sobre a janela fisica (sigma entre o espacamento e o
tamanho do sistema). Classifica-se p: ~ -2 (SR), ~ -3 (CSL), ~ 0 (DP), ou novo.

Caveat de honestidade registrado a priori: o limite continuo de AMBOS operadores e o
Laplaciano, cujo quociente de Rayleigh sobre um modo de largura sigma escala como
sigma^-2 por analise dimensional. Logo p~-2 seria assinatura SR mas por razao
GENERICA (Laplaciano), nao por mecanismo SR-especifico. Reportar p E essa leitura.
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone
import numpy as np
import sr_teic_core as core
import c5_core as c5

SEEDS = list(range(10))
DIMS = [2, 4]
N_MAIN = 400
# larguras espaciais sigma_x (em unidades do tamanho do diamante ~1); janela fisica
# entre ~espacamento (N^-1/d) e ~metade do sistema
SIGMAS = np.geomspace(0.04, 0.40, 12)


def bd_matrix(A, eps=c5.EPS_DEFAULT):
    """Reconstrucao da matriz do d'Alembertiano causal suavizado (mesma de
    c5.bd_operator_eigs, mas retornando a matriz para o quociente de Rayleigh)."""
    Af = A.astype(np.float32)
    inter = (Af @ Af).astype(np.float64)
    m = inter + inter.T
    R = A | A.T
    W = c5.smeared_weight(m, eps)
    M = np.where(R, W, 0.0)
    np.fill_diagonal(M, 0.0)
    np.fill_diagonal(M, -M.sum(axis=1))
    return M


def adjacency_laplacian(A):
    S = (A | A.T).astype(np.float64)
    np.fill_diagonal(S, 0.0)
    d = S.sum(axis=1)
    return np.diag(d) - S


def spatial_mode(pts, sigma):
    """Modo gaussiano localizado nas coordenadas ESPACIAIS (nao no tempo), largura
    sigma, centrado no centroide espacial. Normalizado."""
    x = pts[:, 1:]
    c = x.mean(axis=0)
    r2 = np.sum((x - c) ** 2, axis=1)
    f = np.exp(-r2 / (2.0 * sigma ** 2))
    nrm = np.sqrt(np.sum(f * f))
    return f / nrm if nrm > 0 else f


def rayleigh(M, f):
    return float(f @ (M @ f))      # f ja normalizado (<f|f>=1)


def fit_exponent(sig, gamma):
    """p = inclinacao de log|Gamma| vs log sigma (regressao); R^2."""
    g = np.abs(np.asarray(gamma))
    ok = g > 0
    if ok.sum() < 3:
        return float("nan"), float("nan")
    ls, lg = np.log(np.asarray(sig)[ok]), np.log(g[ok])
    b = np.polyfit(ls, lg, 1)
    pred = b[0] * ls + b[1]
    ss_res = np.sum((lg - pred) ** 2)
    ss_tot = np.sum((lg - lg.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(b[0]), float(r2)


def classify(p):
    if not np.isfinite(p):
        return "indeterminado"
    cands = {"SR (sigma^-2)": -2.0, "CSL (sigma^-3)": -3.0, "Diosi-Penrose (flat)": 0.0}
    best = min(cands, key=lambda k: abs(p - cands[k]))
    if abs(p - cands[best]) <= 0.4:
        return best
    return f"NOVO (p={p:.2f}, nao -2/-3/0)"


def main():
    payload = {"experiment": "FD2_signature", "seeds": SEEDS,
               "sigmas": SIGMAS.tolist(), "by": {}}
    lines = []
    for dim in DIMS:
        for opname, opfun in (("BD", bd_matrix), ("adjLaplacian", adjacency_laplacian)):
            G = np.zeros((len(SEEDS), len(SIGMAS)))
            for si, sd in enumerate(SEEDS):
                rng = np.random.default_rng(80000 * dim + sd)
                pts = core.sprinkle(N_MAIN, dim, rng)
                A = core.ancestor_matrix(pts)
                M = opfun(A)
                for gi, s in enumerate(SIGMAS):
                    f = spatial_mode(pts, s)
                    G[si, gi] = abs(rayleigh(M, f))
            gmean = G.mean(0)
            p, r2 = fit_exponent(SIGMAS, gmean)
            cls = classify(p)
            payload["by"][f"dim{dim}_{opname}"] = {
                "gamma_mean": gmean.tolist(), "p_exponent": p, "R2": r2, "class": cls}
            lines.append(f"  dim={dim} {opname:12s}: p={p:+.2f} (R2={r2:.3f})  ->  {cls}")
    # sintese: a classe modal entre os 4 ajustes
    classes = [v["class"] for v in payload["by"].values()]
    payload["summary"] = {
        "classes": classes,
        "caveat": "limite continuo de ambos operadores = Laplaciano; p~-2 e assinatura "
                  "SR mas por razao GENERICA (Laplaciano), nao mecanismo SR-especifico."}
    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    (core.HERE / "fd2_signature.json").write_text(json.dumps(payload, indent=2))
    print("=" * 76)
    print("FD2 (EXP4 dormente) -- assinatura do colapso (classificatorio, sem morte)")
    print("=" * 76)
    print("\n".join(lines))
    print("-" * 76)
    print("CAVEAT: limite continuo de ambos operadores = Laplaciano -> p~-2 e SR-like")
    print("        por razao GENERICA (dimensional), nao mecanismo SR-especifico.")


if __name__ == "__main__":
    main()

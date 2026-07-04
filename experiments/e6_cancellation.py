"""
e6_cancellation.py - TESTE DO CANCELAMENTO POR DIFERENCA DE PASSOS CAUSAIS

STATUS: EXPLORATORIO (nao e um resultado provado da TEIC).
ESCOPO: isolado. NAO alimenta R1-R3 nem as conclusoes de curvatura.
        Vive separado porque investiga uma QUESTAO EM ABERTO, nao um
        resultado estabelecido.

PERGUNTA
--------
A estrutura da rede causal fornece, por si, algo que se comporta como
FASE e produz CANCELAMENTO (franjas escuras de interferencia) - sem que
numeros complexos sejam postulados a mao?

ANTI-CIRCULARIDADE (critico)
----------------------------
E trivial obter interferencia se eu ESCREVER e^{ikL} e somar: eu teria
injetado a resposta. Isso e o erro do "gamma a mao" repetido. Portanto este
modulo PROIBE qualquer numero complexo no gerador. So sao permitidas:
  - contagens de caminhos (reais, positivas)
  - comprimentos causais dL (reais)
A funcao de fase complexa, se aparecer, aparece SOMENTE como objeto de
comparacao claramente rotulado (bloco "COMPARISON ONLY") - nunca como algo
"derivado da rede". O guard tests/test_no_circularity.py reforca isso:
nenhum 1j / complex( / cmath fora de um bloco de comparacao rotulado.

VEREDITO OBTIDO (sessao exploratoria) -- cenario (B)
----------------------------------------------------
  - Contagem pura de caminhos NAO cancela (intensidade min/max ~ 0.85,
    nunca chega a zero) - confirma ausencia de franjas escuras.
  - dL(x) = L_dir - L_esq existe, e zero no centro e cresce linearmente,
    reproduzindo a forma geometrica da diferenca de caminho da dupla fenda.
  - Faltam DOIS objetos, e apenas dois, para haver interferencia:
      (i) algo que oscile com sinal (o analogo de cos / da unidade i);
      (ii) uma escala k que converta "passos" em "angulo".
  - Conclusao: QM ~ TEIC (geometria) + regra de fase (k, oscilacao).
    A fronteira TEIC<->QM fica LOCALIZADA num unico objeto: o mapa dL->angulo.

Este modulo reproduz esse diagnostico de forma versionada.
"""

import os

import numpy as np

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "results", "data")
FIGDIR = os.path.join(os.path.dirname(__file__), "..", "results", "figures")
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(FIGDIR, exist_ok=True)


def proper_distance(p1, p2):
    """Distancia propria tipo-tempo (Minkowski 1+1). None se tipo-espaco."""
    dx = p2[0] - p1[0]
    dt = p2[1] - p1[1]
    interval = dt ** 2 - dx ** 2
    return np.sqrt(interval) if interval > 0 else None


def path_length_min(p1, p2, step=1.0):
    """Comprimento causal minimo em passos = distancia propria / passo.

    NOTA ANTI-CIRCULARIDADE: isto e uma quantidade REAL e POSITIVA.
    Nenhuma fase, nenhum i. Apenas geometria causal.
    """
    tau = proper_distance(p1, p2)
    return tau / step if tau is not None else None


def run(seed=7, d=6.0, T_slit=10.0, T_screen=20.0, n_screen=240, L0=30.0):
    """Executa o diagnostico de cancelamento. Retorna dict com veredito."""
    S = (0.0, 0.0)
    slit_L = (-d / 2, T_slit)
    slit_R = (+d / 2, T_slit)
    screen_x = np.linspace(-12, 12, n_screen)

    L_esq, L_dir, dL = [], [], []
    for x in screen_x:
        Pk = (x, T_screen)
        l1a = path_length_min(S, slit_L)
        l1b = path_length_min(slit_L, Pk)
        l2a = path_length_min(S, slit_R)
        l2b = path_length_min(slit_R, Pk)
        if None in (l1a, l1b, l2a, l2b):
            L_esq.append(np.nan); L_dir.append(np.nan); dL.append(np.nan)
            continue
        Le, Ld = l1a + l1b, l2a + l2b
        L_esq.append(Le); L_dir.append(Ld); dL.append(Ld - Le)

    L_esq = np.array(L_esq); L_dir = np.array(L_dir); dL = np.array(dL)

    # PARTE 1: contagem pura (peso real positivo) - nao cancela
    intens_count = np.exp(-L_esq / L0) + np.exp(-L_dir / L0)
    ratio_min_max = np.nanmin(intens_count) / np.nanmax(intens_count)

    # PARTE 2: dL tem a geometria correta?
    # Referencia geometrica CORRETA do near-axis slope da dupla fenda.
    # (Auditoria de honestidade: a versao exploratoria usava d/T_screen, que esta
    #  ERRADA -- usa a distancia ate a tela T_screen em vez da distancia fenda->tela
    #  D = T_screen - T_slit, e ignora o comprimento proprio relativistico. O slope
    #  near-axis correto e d(dL)/dx|_0 = d / sqrt(D^2 - (d/2)^2), pois os termos
    #  fonte->fenda cancelam em dL. So com essa referencia a medida bate (~1%) e a
    #  afirmacao "geometria correta da dupla fenda" se sustenta.)
    D = T_screen - T_slit
    slope_geometric = d / np.sqrt(D ** 2 - (d / 2) ** 2)
    near = np.abs(screen_x) < 1.5   # janela near-axis (fora dela ha curvatura do sqrt)
    slope_measured = np.polyfit(screen_x[near], dL[near], 1)[0]
    geom_rel_err = abs(slope_measured - slope_geometric) / slope_geometric

    verdict = {
        "scenario": "B",
        "count_cancels": bool(ratio_min_max < 0.05),
        "count_ratio_min_max": float(ratio_min_max),
        "dL_zero_at_center": float(dL[len(dL) // 2]),
        "dL_slope_measured": float(slope_measured),
        "dL_slope_geometric_ref": float(slope_geometric),
        "dL_geometry_rel_err": float(geom_rel_err),
        "dL_geometry_correct": bool(geom_rel_err < 0.05),
        "missing_ingredients": ["oscillating sign (analog of i/cos)",
                                "scale k mapping steps->angle"],
        "interpretation": "QM ~ TEIC(geometry) + phase-rule(k, oscillation)",
    }

    np.save(os.path.join(OUTDIR, "e6_dL.npy"),
            np.column_stack([screen_x, dL, intens_count]))
    _make_figure(screen_x, dL, intens_count, slope_geometric)
    return verdict


def _make_figure(screen_x, dL, intens_count, slope_geometric):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    ax[0].plot(screen_x, dL, "-", color="tab:purple")
    ax[0].plot(screen_x, slope_geometric * screen_x, "k--", lw=1,
               label=f"geometric slope d/T = {slope_geometric:.3f}")
    ax[0].axhline(0, color="0.7", lw=0.8)
    ax[0].set_title(r"(EXPLORATORY) step-difference $\Delta L(x)$: correct geometry")
    ax[0].set_xlabel("screen position x"); ax[0].set_ylabel(r"$\Delta L$"); ax[0].legend()
    ax[1].plot(screen_x, intens_count, "-", color="tab:green")
    ax[1].set_ylim(0, np.nanmax(intens_count) * 1.1)
    ax[1].set_title("pure real counting: NO dark fringes (no cancellation)")
    ax[1].set_xlabel("screen position x"); ax[1].set_ylabel("real intensity (counts)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "e6_cancellation.png"), dpi=130)


if __name__ == "__main__":
    v = run()
    print("=" * 60)
    print("e6_cancellation - VEREDITO (cenario B) [EXPLORATORIO]")
    print("=" * 60)
    print(f"  contagem pura cancela?      {v['count_cancels']}  "
          f"(min/max={v['count_ratio_min_max']:.3f})")
    print(f"  dL no centro ~ 0?           {v['dL_zero_at_center']:.4f}")
    print(f"  dL inclinacao medida:       {v['dL_slope_measured']:.4f}")
    print(f"  dL inclinacao geometrica:   {v['dL_slope_geometric_ref']:.4f}  "
          f"(near-axis correto)")
    print(f"  geometria correta?          {v['dL_geometry_correct']}  "
          f"(err {v['dL_geometry_rel_err']:.1%})")
    print(f"  ingredientes faltantes:     {v['missing_ingredients']}")
    print(f"  interpretacao:              {v['interpretation']}")
    print()
    print("  NOTA: resultado EXPLORATORIO. Nao e um resultado provado")
    print("        da TEIC. Localiza a fronteira TEIC <-> Mecanica Quantica.")

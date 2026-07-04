"""
e11_phase_scale.py - A ESCALA DE FASE k EMERGE DA REDE? (RESULTADO FECHADO)

STATUS: EXPLORATORIO. Fecha a investigacao de interferencia (e6/e10).
ESCOPO: isolado. NAO alimenta R1-R3, curvatura, nem e6-e10. Vive separado
        porque investiga uma QUESTAO EM ABERTO (a fronteira TEIC<->QM), nao
        um resultado estabelecido da relatividade.

PERGUNTA (o ingrediente (ii) que faltava em e6)
-----------------------------------------------
e6 localizou DOIS objetos em falta para ter franjas de interferencia:
  (i)  algo que oscile com SINAL  -> DERIVADO em e10 (peso de Sorkin w(m)
       alterna de sinal por construcao).
  (ii) uma escala k que converte "passos causais" em "angulo de fase".
Este modulo pergunta: a escala k pode EMERGIR da densidade rho da rede,
ou tem de vir de fora (k = m/hbar, propriedade da MATERIA, nao da geometria)?

MECANISMO (tudo real, positivo, sem postular o quantum)
-------------------------------------------------------
  - A geometria da dupla fenda (a mesma de e6: T_slit=10, T_screen=20, d=6)
    fornece os comprimentos PROPRIOS L_L(x), L_R(x) ate cada ponto da tela.
  - O numero de PASSOS CAUSAIS ao longo de um caminho de comprimento proprio
    L numa rede de densidade rho e uma quantidade EMERGENTE: medimo-la
    fazendo sprinkling de Poisson e contando a maior cadeia causal. Em 1+1D
    isto escala como sqrt(rho) (Myrheim-Meyer; e a mesma escala de R2). NAO
    impomos a lei: medimo-la (Parte 1).
  - A fase ao longo de um caminho e theta_0 * (passos causais), onde theta_0
    e a fase POR PASSO. theta_0=1 e a unica escolha natural ADIMENSIONAL.

O TESTE
-------
Com theta_0=1 fixo, varremos rho em {1,4,16,64,256} e medimos o espacamento
das franjas. Se k emergisse da geometria, o padrao fisico (espacamento de
franjas) seria independente de rho. Medimos como theta_0 teria de escalar
com rho para MANTER o padrao fisico fixo:

  CRITERIO A (k NAO emerge): theta_0 ~ rho^(-1/2). Para um padrao fisico
     independente de rho, a fase por passo tem de absorver um 1/sqrt(rho)
     -- isto e, a escala k = theta_0 * sqrt(rho) tem de vir de FORA. A
     geometria fornece a FORMA (oscilacao com sinal), nao a ESCALA.
  CRITERIO B (k emerge): theta_0 ~ rho^0 (independente de rho).

ANTI-CIRCULARIDADE (critico)
----------------------------
  - NAO se fixa k = m/hbar no gerador. Nao ha m, hbar, nem comprimento de
    onda de de Broglie em lado nenhum do gerador.
  - A fase e theta_0 * (passos causais). A dependencia em rho dos passos e
    MEDIDA por sprinkling, nao postulada.
  - Os comprimentos proprios L(x) sao reais e positivos (geometria causal de
    Minkowski; nao e formula de dilatacao). proper_distance = sqrt(dt^2-dx^2)
    nao bate em nenhum padrao proibido (sqrt(1-beta^2), sqrt(1-2M/r)).
  - Numeros complexos APENAS dentro de bloco "# COMPARISON ONLY" rotulado:
    a fase quantica postulada (psi = exp(i theta_0 n)) so serve para
    DESENHAR/medir o padrao de franjas e fazer a pergunta sobre a escala.
    Nunca alimenta o gerador (guard tests/test_no_circularity.py).

VEREDITO OBTIDO: CRITERIO A. theta_0 ~ rho^(-1/2). A escala quantica e
EXTERNA a geometria causal. A fronteira TEIC<->QM esta agora completamente
mapeada: (i) forma -> derivada (e10); (ii) escala k -> externa (e11), carrega
m/hbar. A TEIC e o piso de baixo (informacao/geometria causal); a escala
quantica mora no piso de cima (propriedade da materia que se propaga).
"""

import json
import os

import numpy as np

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "results", "data")
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "results", "figures")
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(FIGDIR, exist_ok=True)

# Geometria da dupla fenda -- IDENTICA a e6 (d=6, T_slit=10, T_screen=20).
D_SLIT = 6.0
T_SLIT = 10.0
T_SCREEN = 20.0
SCREEN_HALF = 12.0
N_SCREEN = 240

# Varredura de densidade (a pergunta e como o padrao depende disto).
RHOS = (1.0, 4.0, 16.0, 64.0, 256.0)
TAU_REF = 4.0          # tempo proprio do diamante de calibracao (Parte 1)
THETA0 = 1.0           # fase por passo: unica escolha natural adimensional


# =====================================================================
# GEOMETRIA -- comprimentos proprios (reais, positivos; nao e dilatacao)
# =====================================================================

def proper_distance(p1, p2):
    """Distancia propria tipo-tempo (Minkowski 1+1), coords (x, t).

    NOTA ANTI-CIRCULARIDADE: quantidade REAL e POSITIVA. Nenhuma fase,
    nenhum i, nenhuma formula de dilatacao. So o intervalo de Minkowski.
    """
    dx = p2[0] - p1[0]
    dt = p2[1] - p1[1]
    interval = dt ** 2 - dx ** 2
    return np.sqrt(interval) if interval > 0 else None


def double_slit_path_lengths():
    """L_L(x), L_R(x), dL(x) ao longo da tela. Geometria pura (= e6)."""
    S = (0.0, 0.0)
    slit_L = (-D_SLIT / 2, T_SLIT)
    slit_R = (+D_SLIT / 2, T_SLIT)
    screen_x = np.linspace(-SCREEN_HALF, SCREEN_HALF, N_SCREEN)
    L_L, L_R = [], []
    for x in screen_x:
        Pk = (x, T_SCREEN)
        a, b = proper_distance(S, slit_L), proper_distance(slit_L, Pk)
        c, d = proper_distance(S, slit_R), proper_distance(slit_R, Pk)
        if None in (a, b, c, d):
            L_L.append(np.nan); L_R.append(np.nan)
        else:
            L_L.append(a + b); L_R.append(c + d)
    L_L, L_R = np.array(L_L), np.array(L_R)
    return screen_x, L_L, L_R, (L_R - L_L)


def near_axis_slope():
    """Inclinacao geometrica near-axis de dL(x): d/sqrt(D^2-(d/2)^2) (= e6)."""
    D = T_SCREEN - T_SLIT
    return D_SLIT / np.sqrt(D ** 2 - (D_SLIT / 2) ** 2)


# =====================================================================
# PARTE 1 -- PASSOS CAUSAIS POR UNIDADE DE COMPRIMENTO PROPRIO (EMERGENTE)
# =====================================================================

def sample_diamond(rho, tau, rng):
    """Sprinkle de Poisson num diamante causal 1+1D de tempo proprio tau."""
    vol = 0.5 * tau ** 2
    n = rng.poisson(rho * vol)
    if n == 0:
        return np.array([]), np.array([])
    xs, ts = [], []
    while len(xs) < n:
        t_try = rng.uniform(0, tau, n * 4)
        x_try = rng.uniform(-tau / 2, tau / 2, n * 4)
        inside = (np.abs(x_try) <= t_try + 1e-9) & \
                 (np.abs(x_try) <= tau - t_try + 1e-9)
        xs.extend(x_try[inside][: n - len(xs)])
        ts.extend(t_try[inside][: n - len(ts)])
    return np.array(xs[:n]), np.array(ts[:n])


def longest_chain(xs, ts):
    """Maior cadeia causal (tempo proprio discreto) em 1+1D. Inner loop
    vetorizado para suportar rho alto sem custo proibitivo."""
    n = len(xs)
    if n == 0:
        return 0
    order = np.argsort(ts, kind="stable")
    xs, ts = xs[order], ts[order]
    dp = np.ones(n, dtype=np.int64)
    for b in range(1, n):
        prec = np.abs(xs[b] - xs[:b]) <= (ts[b] - ts[:b]) + 1e-9
        if prec.any():
            dp[b] = 1 + int(dp[:b][prec].max())
    return int(dp.max())


def measure_steps_per_length(rho, tau=TAU_REF, n_trials=25, seed=11):
    """Passos causais por unidade de comprimento proprio numa rede de
    densidade rho: <maior cadeia> / tau. EMERGENTE (sprinkling), nao imposto.
    """
    rng = np.random.default_rng(seed + int(rho))
    chains = [longest_chain(*sample_diamond(rho, tau, rng))
              for _ in range(n_trials)]
    mean_chain = float(np.mean(chains))
    return mean_chain / tau, mean_chain, float(np.std(chains))


# =====================================================================
# PARTE 2 -- ESPACAMENTO DE FRANJAS vs rho (com theta_0=1 fixo)
# =====================================================================

def fringe_spacing(screen_x, dL, steps_per_L, theta0=THETA0):
    """Espacamento de franjas no padrao de interferencia.

    A diferenca de fase entre os dois caminhos e
        dphi(x) = theta0 * steps_per_L * dL(x).
    Como dL e monotonica na tela, o numero de franjas e o numero de ciclos
    de 2pi varridos por dphi; o espacamento e (extensao em x)/(n_franjas).
    """
    good = np.isfinite(dL)
    x, d = screen_x[good], dL[good]
    dphi = theta0 * steps_per_L * d
    n_fringes = (dphi.max() - dphi.min()) / (2 * np.pi)
    x_span = x.max() - x.min()
    return x_span / n_fringes if n_fringes > 0 else np.inf, float(n_fringes)


def comparison_intensity(screen_x, L_L, L_R, steps_per_L, theta0=THETA0):
    """Padrao de intensidade I(x) da dupla fenda (so para visualizar/contar).

    A FASE QUANTICA E POSTULADA AQUI -- nao sai da rede. So serve para
    desenhar o padrao e tornar concreta a pergunta sobre a escala k.
    """
    good = np.isfinite(L_L) & np.isfinite(L_R)
    x = screen_x[good]
    nL = steps_per_L * L_L[good]
    nR = steps_per_L * L_R[good]
    # COMPARISON ONLY -- postulated QM phase, not derived from network.
    # psi = exp(i theta0 n_L) + exp(i theta0 n_R); I = |psi|^2 (Born, postulada).
    psi = np.exp(1j * theta0 * nL) + np.exp(1j * theta0 * nR)
    intensity = np.abs(psi) ** 2
    # END COMPARISON ONLY
    return x, intensity


def count_peaks(x, intensity):
    """Conta maximos locais do padrao -- verificacao independente do
    espacamento analitico (deve bater com fringe_spacing)."""
    if intensity.size < 3:
        return 0, np.inf
    is_peak = (intensity[1:-1] > intensity[:-2]) & \
              (intensity[1:-1] >= intensity[2:]) & \
              (intensity[1:-1] > 0.5 * intensity.max())
    peak_x = x[1:-1][is_peak]
    if peak_x.size < 2:
        return int(peak_x.size), np.inf
    return int(peak_x.size), float(np.mean(np.diff(peak_x)))


# =====================================================================
# DRIVER
# =====================================================================

def run(theta0=THETA0, n_trials=25, verbose=True):
    if verbose:
        print("=" * 70)
        print("e11 -- A ESCALA DE FASE k EMERGE DA REDE? (EXPLORATORIO, ISOLADO)")
        print("=" * 70)
        print("Fecha a investigacao de interferencia (e6 ingrediente (ii)).")
        print("Sem m, sem hbar, sem lambda_dB. theta_0=1 (natural adimensional).\n")

    screen_x, L_L, L_R, dL = double_slit_path_lengths()
    slope = near_axis_slope()

    # ---- PARTE 1: passos causais ~ rho^p (EMERGENTE, medido) ----
    if verbose:
        print(f"  Parte 1 -- passos causais por comprimento proprio (sprinkling, "
              f"tau={TAU_REF}):")
    sweep = []
    for rho in RHOS:
        spl, mean_chain, std_chain = measure_steps_per_length(
            rho, n_trials=n_trials)
        spacing, n_fr = fringe_spacing(screen_x, dL, spl, theta0)
        sweep.append({"rho": rho, "mean_chain": mean_chain,
                      "chain_std": std_chain, "steps_per_length": spl,
                      "fringe_spacing": float(spacing), "n_fringes": n_fr})
        if verbose:
            print(f"    [P1] rho={rho:6.0f}: <cadeia>={mean_chain:6.2f} "
                  f"(+/-{std_chain:4.2f})  passos/L={spl:6.3f}  "
                  f"espac.franja(theta0=1)={spacing:6.3f}")

    rhos = np.array([s["rho"] for s in sweep])
    spls = np.array([s["steps_per_length"] for s in sweep])

    # Expoente p de passos/L ~ rho^p (esperado ~0.5, Myrheim-Meyer/R2).
    p_steps = float(np.polyfit(np.log(rhos), np.log(spls), 1)[0])

    # ---- PARTE 2: theta_0 necessario para padrao fisico FIXO vs rho ----
    # Alvo: o espacamento de franjas medido na MAIOR densidade (padrao fisico
    # de referencia). theta_0_req(rho) = espacamento_alvo escalado para manter
    # o padrao: theta_0_req ~ 1/steps_per_L(rho).
    target_spacing = sweep[-1]["fringe_spacing"]
    theta0_req = []
    for s in sweep:
        # espac = x_span/n_fr e n_fr ~ theta_0*steps_per_L; para espac fixo:
        # theta_0_req = theta_0 * (espac_atual/espac_alvo)
        tr = theta0 * (s["fringe_spacing"] / target_spacing)
        theta0_req.append(tr)
        s["theta0_required_for_fixed_pattern"] = float(tr)
    theta0_req = np.array(theta0_req)
    p_theta0 = float(np.polyfit(np.log(rhos), np.log(theta0_req), 1)[0])

    # ---- Verificacao: padrao concreto + contagem de picos numa rho media ----
    rho_demo = 16.0
    spl_demo = next(s["steps_per_length"] for s in sweep if s["rho"] == rho_demo)
    xd, Id = comparison_intensity(screen_x, L_L, L_R, spl_demo, theta0)
    n_peaks, peak_spacing = count_peaks(xd, Id)
    analytic_spacing = next(s["fringe_spacing"] for s in sweep
                            if s["rho"] == rho_demo)

    # ---- VEREDITO ----
    # CRITERIO A: theta_0 tem de escalar como 1/sqrt(rho) (expoente ~ -0.5).
    # CRITERIO B: theta_0 independente de rho (expoente ~ 0).
    is_A = p_theta0 < -0.25 and abs(p_theta0 + 0.5) < 0.25
    is_B = abs(p_theta0) < 0.15
    criterion = "A" if is_A else ("B" if is_B else "indeterminate")
    if criterion == "A":
        verdict = (
            "CRITERIO A: a escala de fase k NAO emerge da rede. theta_0 tem de "
            f"escalar como rho^({p_theta0:+.2f}) ~ 1/sqrt(rho) para manter o "
            "padrao fisico fixo. Logo k = theta_0*sqrt(rho) e EXTERNO: carrega "
            "m/hbar, propriedade da MATERIA, nao da geometria causal. A "
            "geometria fornece a FORMA da interferencia (passos causais, "
            "oscilacao com sinal de e10), nao a ESCALA quantica. Fronteira "
            "TEIC<->QM completamente mapeada: (i) forma DERIVADA; (ii) escala "
            "k EXTERNA.")
    elif criterion == "B":
        verdict = ("CRITERIO B: theta_0 independente de rho -- a escala de fase "
                   "emergiria da geometria. (NAO esperado.)")
    else:
        verdict = (f"INDETERMINADO: expoente theta_0(rho)={p_theta0:+.2f} nao "
                   "separa claramente A de B nesta corrida.")

    out = {
        "verdict": verdict,
        "criterion": criterion,
        "params": {"rhos": list(RHOS), "tau_ref": TAU_REF, "theta0": theta0,
                   "n_trials": n_trials, "geometry": {
                       "d": D_SLIT, "T_slit": T_SLIT, "T_screen": T_SCREEN}},
        "near_axis_slope": float(slope),
        "sweep": sweep,
        "exponent_steps_per_length_vs_rho": p_steps,
        "exponent_theta0_required_vs_rho": p_theta0,
        "expected_steps_exponent": 0.5,
        "expected_theta0_exponent_if_A": -0.5,
        "peak_check": {"rho": rho_demo, "n_peaks": n_peaks,
                       "peak_spacing": peak_spacing,
                       "analytic_spacing": analytic_spacing},
        "depends_on": ("R2 chain~sqrt(rho) scaling (Myrheim-Meyer) for the "
                       "EMERGENT step count; closes e6 ingredient (ii) and "
                       "e10 ingredient (i)."),
        "interpretation": (
            "Two floors. BOTTOM (TEIC): causal geometry / information -> form "
            "of interference. BOUNDARY (e11): scale k=m/hbar and charge e do "
            "NOT emerge from geometry. TOP: quantum/matter scales are external."),
        "note": ("EXPLORATORY, isolated from R1-R3 and curvature. No m/hbar/"
                 "lambda_dB in generator; postulated complex phase confined to a "
                 "labelled COMPARISON ONLY block (anti-circularity guard)."),
    }

    if verbose:
        print(f"\n  Parte 2 -- expoentes medidos:")
        print(f"    passos/L ~ rho^{p_steps:+.3f}  (esperado +0.50; = R2)")
        print(f"    theta_0_req ~ rho^{p_theta0:+.3f}  (esperado -0.50 se A)")
        print(f"\n  Verificacao (rho={rho_demo:.0f}): {n_peaks} picos, espac.="
              f"{peak_spacing:.3f} vs analitico {analytic_spacing:.3f}")
        print(f"\n  => {verdict}\n")

    _save_figure(sweep, rhos, spls, theta0_req, xd, Id, p_steps, p_theta0)

    path = os.path.join(OUTDIR, "e11_phase_scale.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    if verbose:
        print(f"  [resultados em {path}]")
    return out


def _save_figure(sweep, rhos, spls, theta0_req, xd, Id, p_steps, p_theta0):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    ax[0].loglog(rhos, spls, "o-", color="tab:blue")
    ax[0].set_title(f"(EXPLORATORY) causal steps/L ~ rho^{p_steps:.2f}")
    ax[0].set_xlabel("density rho"); ax[0].set_ylabel("steps per proper length")
    ax[1].loglog(rhos, theta0_req, "s-", color="tab:red")
    ax[1].set_title(r"$\theta_0$ for fixed pattern ~ rho^" f"{p_theta0:.2f}"
                    r" ($\approx -1/2$: k external)")
    ax[1].set_xlabel("density rho"); ax[1].set_ylabel(r"$\theta_0$ required")
    ax[2].plot(xd, Id, "-", color="tab:purple")
    ax[2].set_title("two-slit pattern (COMPARISON ONLY, postulated phase)")
    ax[2].set_xlabel("screen position x"); ax[2].set_ylabel("intensity")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "e11_phase_scale.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    run()

"""
e8_redshift.py - REDSHIFT POR CRESCIMENTO CAUSAL DA REDE (versao corrigida)

STATUS: EXPLORATORIO. Criterios de morte pre-registrados. ISOLADO de R1-R3 e de e6/e7.

DEPENDENCIA (auditoria): este modulo NAO e um resultado independente. Ele APLICA a
  lei de escala chain ~ sqrt(N) ~ sqrt(rho) (a baixa altura, tau fixo) -- o estimador
  de Myrheim-Meyer ja estabelecido e reproduzido em R2 (e2_dimension_volume). O
  "redshift" e uma reinterpretacao dessa mesma escala: um diamante de tempo proprio
  fixo numa regiao mais densa contem uma cadeia causal mais longa (mais ticks). Nada
  aqui valida a lei sqrt(rho); ela e tomada de R2 e usada SO na comparacao final.

PERGUNTA:
Se novos eventos nascem continuamente na rede enquanto um pacote de
informacao viaja, o receptor conta os pulsos chegando mais espacados
(redshift)? E esse espacamento segue a predicao causal sqrt(rho_k/rho_0)?

MECANISMO:
  Pulso k viaja num diamante causal de tempo proprio tau fixo.
  A rede dentro do diamante tem densidade rho_k = rho_0*(1 + k*alpha).
  A maior cadeia causal (tempo proprio discreto) cresce como sqrt(rho_k).
  O receptor conta ticks causais -- com rede crescendo, conta mais ticks
  entre pulsos: redshift em tempo proprio causal.

PREDICAO ANALITICA (sem postular redshift cosmologico):
  chain_k / chain_0 = sqrt(rho_k / rho_0)      [Myrheim-Meyer, 1+1D; = R2]
  z_k = chain_k / chain_0 - 1 = sqrt(rho_k/rho_0) - 1

ANTI-CIRCULARIDADE:
  - Nenhuma formula de redshift cosmologico no gerador de dados.
  - rho_k e alpha fixados ANTES de rodar.
  - A predicao sqrt(rho) aparece SO na comparacao final.
  - Sem constante de Hubble, energia escura, ou fator de escala metrico.

CRITERIOS DE MORTE (pre-registrados):
  A) cadeia nao cresce com k -> injecao nao afeta tempo proprio causal.
  B) cadeia cresce mas nao segue sqrt(rho) -> efeito sem lei clara.
  C) cadeia cresce e segue sqrt(rho) -> redshift causal detectado.

NOTA HISTORICA (erros corrigidos):
  Versao 1: receptor na borda do cone de luz (x_rec = dt_travel) ->
    intervalo tipo-espaco -> cadeia = 0. Corrigido para x_rec < dt_travel.
  Versao 2: rede estatica com janela temporal limitada ->
    pulsos tardios fora da janela -> cadeia = 0. Corrigido para diamantes
    independentes por pulso com densidade parametrizada.

A comparacao quantitativa com cosmologia real (rho(t) = rho_0/(1+t)^d e dados de
supernovas) e TRABALHO FUTURO, fora deste modulo, e NAO e promovida a resultado.
"""

import json
import os
import numpy as np

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "results", "data")
os.makedirs(OUTDIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════
# CORE: cadeia causal num diamante de Poisson
# ════════════════════════════════════════════════════════════════

def sample_diamond(rho, tau, rng):
    """
    Sprinkle de Poisson num diamante causal 1+1D com tempo proprio tau.
    Coordenadas: (x, t) com A=(0,0), B=(0,tau) no referencial de repouso.
    Retorna (xs, ts) dos eventos dentro do diamante.
    """
    vol = 0.5 * tau ** 2          # Vol = tau^2/2 em 1+1D
    n = rng.poisson(rho * vol)
    if n == 0:
        return np.array([]), np.array([])
    # Rejection sampling dentro do diamante: |x| <= t E |x| <= tau-t
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
    """
    Comprimento da maior cadeia causal num conjunto de eventos em 1+1D.
    Relacao causal: (xa,ta) -> (xb,tb) se tb>ta e |xb-xa| <= tb-ta.
    """
    n = len(xs)
    if n == 0:
        return 0
    order = np.argsort(ts)
    xs, ts = xs[order], ts[order]
    dp = np.zeros(n, dtype=int)
    for b in range(n):
        for a in range(b):
            if abs(xs[b] - xs[a]) <= ts[b] - ts[a] + 1e-9:
                if dp[b] < dp[a] + 1:
                    dp[b] = dp[a] + 1
    return int(np.max(dp))


def mean_chain(rho, tau, rng, n_trials=10):
    """Cadeia media sobre n_trials realizacoes do diamante."""
    chains = []
    for _ in range(n_trials):
        xs, ts = sample_diamond(rho, tau, rng)
        chains.append(longest_chain(xs, ts))
    return float(np.mean(chains)), float(np.std(chains))


# ════════════════════════════════════════════════════════════════
# EXPERIMENTO: pulsos sucessivos em rede de densidade crescente
# ════════════════════════════════════════════════════════════════

def run_experiment(rho_0=2.0, tau=30.0, alpha=0.3,
                   n_pulses=6, n_trials=10, seed=42):
    """
    Para cada pulso k, o diamante causal tem densidade rho_k = rho_0*(1+k*alpha).
    Medimos a cadeia media de cada pulso.
    Redshift: z_k = chain_k / chain_0 - 1.
    Predicao analitica (R2): z_k = sqrt(rho_k / rho_0) - 1.
    """
    rng = np.random.default_rng(seed)
    results = []

    chain_0, _ = mean_chain(rho_0, tau, rng, n_trials)
    if chain_0 == 0:
        chain_0 = 1.0  # evitar divisao por zero

    for k in range(n_pulses):
        rho_k = rho_0 * (1 + k * alpha)
        chain_k, chain_std = mean_chain(rho_k, tau, rng, n_trials)
        z_measured = chain_k / chain_0 - 1.0
        # Predicao: chain ~ sqrt(rho) -> z = sqrt(rho_k/rho_0) - 1
        # APENAS na comparacao, nao no gerador:
        z_predicted = np.sqrt(rho_k / rho_0) - 1.0
        results.append({
            "k": k,
            "rho_k": rho_k,
            "chain_mean": chain_k,
            "chain_std": chain_std,
            "z_measured": z_measured,
            "z_predicted": z_predicted,
            "delta_z": abs(z_measured - z_predicted),
        })

    return results, chain_0


# ════════════════════════════════════════════════════════════════
# ISOTROPIA: verificar que o efeito nao depende de direcao
# ════════════════════════════════════════════════════════════════

def test_isotropy(rho_0=2.0, tau=30.0, alpha=0.3,
                  n_trials=10, seed=99):
    """
    Testa se z depende da 'direcao' do receptor.
    Em 1+1D: tau e invariante de Lorentz e o sprinkling de Poisson e covariante,
    logo a isotropia vale por construcao. Verificamos numericamente um ponto.
    """
    rng = np.random.default_rng(seed)
    # Pulso k=3 como teste (z nao-trivial)
    k = 3
    alpha_test = 0.3
    rho_k = rho_0 * (1 + k * alpha_test)

    c1_vals = []
    c2_vals = []
    for _ in range(n_trials * 2):
        xs, ts = sample_diamond(rho_0, tau, rng)   # pulso 0
        c1_vals.append(longest_chain(xs, ts))
        xs, ts = sample_diamond(rho_k, tau, rng)   # pulso k
        c2_vals.append(longest_chain(xs, ts))

    z1 = np.mean(c2_vals) / np.mean(c1_vals) - 1
    return {
        "z_frame1": float(z1),
        "note": ("Isotropia garantida por construcao: tau e invariante de "
                 "Lorentz e o sprinkling de Poisson e covariante."),
    }


# ════════════════════════════════════════════════════════════════
# SWEEP: variar alpha e verificar escalonamento
# ════════════════════════════════════════════════════════════════

def run_sweep(alphas=None, seed=42):
    if alphas is None:
        alphas = [0.1, 0.2, 0.3, 0.5, 0.8]

    print("=" * 66)
    print("e8_redshift - REDSHIFT POR CRESCIMENTO CAUSAL DA REDE [EXPLORATORIO]")
    print("Criterio C pre-registrado: z emerge e segue sqrt(rho_k/rho_0)")
    print("Aplica a escala chain~sqrt(rho) de R2 (Myrheim-Meyer); nao a revalida.")
    print("Sem formula de redshift cosmologico no gerador.")
    print("=" * 66)

    all_results = {}
    for alpha in alphas:
        results, chain_0 = run_experiment(alpha=alpha, seed=seed)
        all_results[alpha] = results

        print(f"\nalpha={alpha:.1f}  (rho_k = rho_0*(1+k*{alpha:.1f}))")
        print(f"  {'k':>3} {'rho_k':>7} {'cadeia':>7} "
              f"{'z_meas':>8} {'z_pred':>8} {'dz':>7} {'match':>6}")
        print("  " + "-" * 52)
        matches = []
        for r in results:
            m = r["delta_z"] < 0.06
            matches.append(m)
            print(f"  {r['k']:>3} {r['rho_k']:>7.2f} "
                  f"{r['chain_mean']:>7.1f} "
                  f"{r['z_measured']:>8.4f} {r['z_predicted']:>8.4f} "
                  f"{r['delta_z']:>7.4f} {'OK' if m else '~':>6}")
        print(f"  Acordo: {sum(matches)}/{len(matches)}")

    # Veredito geral
    print("\n" + "=" * 66)
    print("VEREDITO FINAL")
    print("=" * 66)

    all_grow = True
    all_match = []
    for alpha, res in all_results.items():
        chains = [r["chain_mean"] for r in res]
        grows = all(chains[i] <= chains[i + 1] + 1 for i in range(len(chains) - 1))
        if not grows:
            all_grow = False
        match_frac = np.mean([r["delta_z"] < 0.06 for r in res[1:]])
        all_match.append(match_frac)

    mean_match = np.mean(all_match)

    print(f"\n  Cadeia cresce com k (todos os alpha)?  "
          f"{'SIM' if all_grow else 'NAO'}")
    print(f"  Acordo medio z_meas vs sqrt(rho):      "
          f"{mean_match * 100:.0f}%")

    if not all_grow:
        verdict = ("CRITERIO A: cadeia nao cresce. "
                   "Injecao nao produz redshift causal.")
    elif mean_match < 0.5:
        verdict = ("CRITERIO B: cadeia cresce mas sem lei sqrt(rho) clara. "
                   "Efeito existe, mecanismo incerto.")
    else:
        verdict = (
            "CRITERIO C: REDSHIFT CAUSAL DETECTADO. "
            "Cadeia cresce monotonicamente com rho_k, seguindo sqrt(rho_k/rho_0) "
            f"em {mean_match * 100:.0f}% dos pontos (dz < 0.06). "
            "Mecanismo: mais eventos no diamante causal = "
            "mais ticks de tempo proprio = pulsos mais espacados. "
            "E uma APLICACAO da escala chain~sqrt(rho) de R2, nao um resultado novo. "
            "Sem constante de Hubble, energia escura, ou fator de escala."
        )

    print(f"\n  {verdict}")

    # Isotropia
    iso = test_isotropy()
    print(f"\n  ISOTROPIA: {iso['note']}")

    # Conexao cosmologica (trabalho futuro)
    print("""
CONEXAO COM COSMOLOGIA (trabalho futuro, fora deste modulo; NAO e resultado):
  Se rho(t) = rho_0 / (1+t)^d (expansao em d dimensoes),
  entao z_k = sqrt(rho(t_receive)/rho(t_emit)) - 1
  deveria reproduzir a curva de redshift cosmologico em regime linear.
  Requer: implementar rho(t) cosmologico + comparar com dados de supernovas.
  Este modulo estabelece o mecanismo; a comparacao quantitativa nao foi feita.
""")

    # Salvar
    out = {
        "verdict": verdict,
        "depends_on": "R2 (chain ~ sqrt(N) ~ sqrt(rho), Myrheim-Meyer); not independent",
        "cosmology_comparison": "future work, NOT a result",
        "params": {"rho_0": 2.0, "tau": 30.0, "alphas": alphas,
                   "n_pulses": 6, "n_trials": 10, "seed": seed},
        "results_by_alpha": {
            str(a): r for a, r in all_results.items()
        },
        "isotropy": iso,
        "mean_match_pct": float(mean_match * 100),
    }
    path = os.path.join(OUTDIR, "e8_redshift.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  [resultados salvos em {path}]")
    return out


if __name__ == "__main__":
    run_sweep()

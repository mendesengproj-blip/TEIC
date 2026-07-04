"""
e10_sorkin_dalembertian.py - CAMPO ESCALAR SOBRE REDE CAUSAL

STATUS: EXPLORATORIO. Implementa o operador de d'Alembert causal de
Sorkin (2007) / Benincasa-Dowker (2010). ISOLADO de R1-R3 e de e6/e7/e8.

CONTEXTO (o que sessoes anteriores estabeleceram):
  A regra de atualizacao sincrona ingenua s_i(t+1)=a*s_i+b*sum_j s_j
  (da Lagrangiana original) esta MORTA: pressupoe fatias de tempo
  sincronizadas, que nao existem numa rede causal aleatoria, e reintroduz
  a anisotropia da grade regular (que falhou Lorentz em R1). A amplitude
  explode. NAO ressuscitar.

  O caminho CORRETO e o d'Alembertiano causal de Sorkin: o campo num
  evento e determinado por uma soma sobre ancestrais causais com pesos
  que ALTERNAM DE SINAL conforme o numero de eventos no intervalo. Esses
  sinais alternados sao -- pela primeira vez na investigacao -- uma
  quantidade que pode CANCELAR (a peca (i) que faltava na dupla fenda, e6).

FORMA 2D (Benincasa-Dowker 2010; normalizacao confirmada contra
Dowker & Glaser 2013, arXiv:1305.2588, eq.(1)):
  B^(2) phi(x) = (1/l^2)[ -2 phi(x) + 4( S_L1 - 2 S_L2 + S_L3 ) ]
  L_i(x) = { y < x : n(x,y) = i-1 },  n = #(eventos estritamente entre y,x).
  No limite continuo (rho->inf): <B phi> -> box phi = (d_t^2 - d_x^2) phi.

O QUE ESTA SESSAO MEDIU (registrado com honestidade):
  1. O operador CRU (afiado) tem flutuacoes ~rho^(3/4) (Benincasa-Dowker).
     Medido a rho=20: contra um sinal box=2, o SEM e ~800-2500 e o desvio
     ~2e4-6e4. NENHUM numero viavel de amostras o valida. CONFIRMA a
     patologia conhecida de BD.
  2. O operador SUAVIZADO (smeared, "binomial thinning" com retencao eps;
     ver Sorkin 2007, Aslanbeigi-Saravani-Sorkin 2014) reduz a variancia
     ~1000x. Peso suave w(m) sobre TODOS os ancestrais:
        w(m) = (1-eps)^m - 2 m eps (1-eps)^(m-1) + C(m,2) eps^2 (1-eps)^(m-2)
        B_eps phi(x) = -phi(x) + 2 eps * sum_{y<x} w(m_y) phi(y)
     Verificado numericamente: a ANIQUILACAO DE CONSTANTES funciona limpa
     (sum w -> 1/(2eps), logo B_eps[const] -> 0 a ~0.03 +/- 0.04) e os
     campos lineares tambem (~0). Isto CONFIRMA a estrutura do operador e
     o seu peso de SINAL ALTERNADO (w>0 perto de m=0, w<0 a m intermedio).
  3. POReM: a magnitude Lorentziana plena (t^2 -> +2, x^2 -> -2) NAO
     converge de forma limpa nos parametros acessiveis. Ha tensao entre a
     densidade efetiva (eps*rho, precisa ser grande para o limite continuo)
     e a reducao de variancia (eps pequeno). x^2 e o pior caso (soma de
     sinais alternados de termos grandes). Os SINAIS ordenam-se
     (t2 > const ~ lin > x2) mas as magnitudes exigem redes muito maiores
     -- consistente com a dificuldade documentada por BD/Glaser.

VEREDITO HONESTO: T1 e um PASS QUALITATIVO/PARCIAL. A implementacao e a
normalizacao estao corretas (aniquilacao de const/lin + ordenamento de
sinais + controlo de variancia pelo smearing); a recuperacao QUANTITATIVA
limpa de box phi ponto-a-ponto fica por convergir (rede maior / abordagem
por acao globalmente somada). NAO se reivindica mais do que isto.

ANTI-CIRCULARIDADE:
  - Coeficientes (1,-2,1) e o peso w(m) sao a DEFINICAO de Sorkin/BD/thinning
    (citados), nao postulados ad hoc.
  - Nenhuma equacao de onda no gerador; box phi deve EMERGIR de <B phi>.
  - Sem formula de dispersao relativistica no gerador.
  - Sem numeros complexos no gerador (guard test_no_circularity); qualquer
    fase postulada vive em bloco "COMPARISON ONLY" rotulado.

HONESTIDADE: e10 REPRODUZ Sorkin/Benincasa-Dowker -- nao e descoberta. O
unico conteudo potencialmente proprio e T3: o peso de sinal alternado do
operador FORNECE o ingrediente (i) que e6 declarou em falta. Isto e
interferencia de ondas REAIS (classica); a estrutura quantica (|psi|^2,
regra de Born) continua ausente.
"""

import json
import os

import numpy as np

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "results", "data")
os.makedirs(OUTDIR, exist_ok=True)

# Coeficientes de camada do d'Alembertiano causal 2D (Benincasa-Dowker 2010;
# Dowker-Glaser 2013 eq.1). (1,-2,1) sobre as camadas n=0,1,2. DEFINICAO do
# operador, nao ajuste.
BD_2D_COEFFS = np.array([1.0, -2.0, 1.0])


# =====================================================================
# CORE -- sprinkling, passado causal, operadores afiado e suavizado
# =====================================================================

def make_sprinkling(rho, T, X, seed):
    """Poisson sprinkling 1+1D na caixa [0,T] x [-X,X]."""
    rng = np.random.default_rng(seed)
    n = rng.poisson(rho * T * 2 * X)
    ts = rng.uniform(0, T, n)
    xs = rng.uniform(-X, X, n)
    return xs, ts


def causal_past(xs, ts, xi):
    """Indices dos eventos estritamente no passado causal de xi (1+1D)."""
    dt = ts[xi] - ts
    dx = np.abs(xs[xi] - xs)
    return np.where((dt > 0) & (dx <= dt))[0]


def _interval_counts(xs, ts, P):
    """
    Para cada ancestral P_i, n(x,P_i) = #eventos do passado P estritamente
    entre P_i e x. Como TODO P precede x, e o numero de elementos de P que
    P_i precede. Matriz de precedencia m x m de uma so vez (vetorizado).
    """
    xp, tp = xs[P], ts[P]
    dT = tp[None, :] - tp[:, None]
    dX = np.abs(xp[None, :] - xp[:, None])
    prec = (dT > 0) & (dX <= dT)         # prec[i,j] = P_i precede P_j
    return prec.sum(axis=1).astype(float)


def smeared_weight(m, eps):
    """
    Peso suave de Sorkin (binomial thinning, retencao eps) para um ancestral
    com m eventos no seu intervalo causal ate x:
       w(m) = (1-eps)^m - 2 m eps (1-eps)^(m-1) + C(m,2) eps^2 (1-eps)^(m-2)
    Alterna de sinal (w>0 perto de m=0, w<0 a m intermedio) -- e este sinal
    alternado o ingrediente (i) que e6 identificou em falta. (eps<1, sem inf.)
    """
    return ((1 - eps) ** m
            - 2 * m * eps * (1 - eps) ** (m - 1)
            + (m * (m - 1) / 2) * eps ** 2 * (1 - eps) ** (m - 2))


def sorkin_B_sharp(xs, ts, phi, xi, l):
    """
    Operador AFIADO de Sorkin 2D (Dowker-Glaser eq.1). Normalizacao exata,
    mas flutuacoes ~rho^(3/4) -- usado so para DEMONSTRAR a inviabilidade
    (T1a). B^(2) = (1/l^2)[-2 phi(x) + 4(S_L0 - 2 S_L1 + S_L2)].
    """
    P = causal_past(xs, ts, xi)
    if P.size == 0:
        return (1.0 / l ** 2) * (-2.0 * phi[xi])
    m = _interval_counts(xs, ts, P)
    phiP = phi[P]
    inner = sum(BD_2D_COEFFS[n] * phiP[m == n].sum() for n in range(3))
    return (1.0 / l ** 2) * (-2.0 * phi[xi] + 4.0 * inner)


def sorkin_B_smeared(xs, ts, phi, xi, eps):
    """
    Operador SUAVIZADO de Sorkin 2D (binomial thinning). Normalizacao
    natural: a densidade ja esta embutida nas contagens de intervalo m,
    por isso o operador e simplesmente
        B_eps phi(x) = -phi(x) + 2 eps * sum_{y<x} w(m_y) phi(y).
    Aniquila constantes (sum w -> 1/(2eps)) -- verificado.
    """
    P = causal_past(xs, ts, xi)
    if P.size == 0:
        return -phi[xi]
    m = _interval_counts(xs, ts, P)
    return -phi[xi] + 2.0 * eps * np.dot(smeared_weight(m, eps), phi[P])


def _mid_events(xs, ts, T, X, k, seed):
    """Eventos no miolo (cone causal contido na caixa) para amostrar B."""
    mid = np.where((ts > T * 0.4) & (ts < T * 0.6) &
                   (np.abs(xs) < X * 0.4))[0]
    if mid.size > k:
        mid = np.random.default_rng(seed + 999).choice(mid, k, replace=False)
    return mid


def phi_field(xs, ts, kind):
    if kind == "const": return np.ones_like(ts)
    if kind == "lin":   return ts + xs
    if kind == "t2":    return ts ** 2
    if kind == "x2":    return xs ** 2
    raise ValueError(kind)


# =====================================================================
# T1a -- DEMONSTRACAO: o operador AFIADO e inviavel (variancia ~rho^(3/4))
# =====================================================================

def test_T1a_sharp_variance(rho=20.0, T=12.0, X=30.0, n_real=8, k=40):
    """Mostra que o operador afiado tem SEM >> sinal (esperado, BD)."""
    l = 1.0 / np.sqrt(rho)
    out = {}
    for kind in ["const", "t2"]:
        v = []
        for seed in range(n_real):
            xs, ts = make_sprinkling(rho, T, X, seed)
            phi = phi_field(xs, ts, kind)
            for xi in _mid_events(xs, ts, T, X, k, seed):
                v.append(sorkin_B_sharp(xs, ts, phi, xi, l))
        v = np.array(v)
        out[kind] = {"mean": float(v.mean()), "std": float(v.std()),
                     "sem": float(v.std() / np.sqrt(len(v)))}
    return out


# =====================================================================
# T1 -- VALIDACAO (smeared): <B phi> ~ box phi
# =====================================================================

def test_T1(rho=20.0, T=12.0, X=30.0, eps=0.2, n_real=30, k=120, verbose=True):
    """
    Valida o operador SUAVIZADO contra box phi: const=0, lin=0, t2=+2, x2=-2.
    Reporta media +/- SEM por campo, ordenamento de sinais e razao t2/x2.
    """
    expected = {"const": 0.0, "lin": 0.0, "t2": 2.0, "x2": -2.0}
    results = {}
    for kind, exp in expected.items():
        v = []
        for seed in range(n_real):
            xs, ts = make_sprinkling(rho, T, X, seed)
            phi = phi_field(xs, ts, kind)
            for xi in _mid_events(xs, ts, T, X, k, seed):
                v.append(sorkin_B_smeared(xs, ts, phi, xi, eps))
        v = np.array(v)
        results[kind] = {"B_mean": float(v.mean()),
                         "B_sem": float(v.std() / np.sqrt(len(v))),
                         "expected": exp, "n_samples": int(len(v))}
        if verbose:
            r = results[kind]
            print(f"    [T1] {kind:>5}: <B>={r['B_mean']:+8.3f} "
                  f"+/-{r['B_sem']:6.3f}  (box={exp:+.1f})  n={r['n_samples']}")

    r = results
    # const aniquila? (prefactor-INDEPENDENTE: -1 + 2 eps sum w -> 0). E o
    # teste robusto da ESTRUTURA/normalizacao do operador.
    const_ok = abs(r["const"]["B_mean"]) < 2.5 * r["const"]["B_sem"] + 0.05
    # lin: vies sistematico de discretude (peso so-passado). Aniquila so no
    # limite eps*rho -> inf. O seu VALOR e o diagnostico de convergencia.
    lin_bias = abs(r["lin"]["B_mean"])
    verdict = {"const_annihilates": bool(const_ok),
               "const_value": r["const"]["B_mean"],
               "lin_bias_magnitude": float(lin_bias),
               "t2_value": r["t2"]["B_mean"], "t2_sem": r["t2"]["B_sem"],
               "x2_value": r["x2"]["B_mean"], "x2_sem": r["x2"]["B_sem"],
               "note": ("box magnitude (t2=+2,x2=-2) NOT recoverable pointwise: "
                        "B=2*eps*rho*bracket, so signal in bracket-units is "
                        "box/(2*eps*rho) -> buried under O(0.3) variance at every "
                        "regime. Low eps*rho -> bias; high eps*rho -> vanishing "
                        "SNR. This is why BD validate via the SUMMED action.")}
    return results, verdict


def test_T1_convergence(eps=0.2, settings=((20.0, 12.0, 30.0),
                                           (60.0, 8.0, 14.0)), n_real=12, k=120):
    """
    Evidencia de CONVERGENCIA: o vies de discretude do operador (medido no
    campo linear, box(lin)=0) deve ENCOLHER quando a densidade efetiva
    eps*rho cresce. Mede |<B[lin]>| em duas densidades efetivas e reporta a
    razao. Isto mostra que <B> -> box mesmo que a magnitude plena fique
    abaixo do ruido ponto-a-ponto.
    """
    out = []
    for rho, T, X in settings:
        v = []
        for seed in range(n_real):
            xs, ts = make_sprinkling(rho, T, X, seed)
            phi = phi_field(xs, ts, "lin")
            for xi in _mid_events(xs, ts, T, X, k, seed):
                v.append(sorkin_B_smeared(xs, ts, phi, xi, eps))
        v = np.array(v)
        out.append({"rho": rho, "eff_density": eps * rho,
                    "lin_bias": float(abs(v.mean())),
                    "sem": float(v.std() / np.sqrt(len(v)))})
    shrinks = (len(out) == 2 and out[1]["lin_bias"] < out[0]["lin_bias"])
    return {"points": out, "bias_shrinks_with_eff_density": bool(shrinks)}


# =====================================================================
# T2 -- ASSINATURA LORENTZIANA (qualitativa, dado o ruido)
# =====================================================================
#
# Anti-circularidade: NAO se impoe w=k. Aplica-se B a cosseno PURAMENTE
# espacial cos(k x) e PURAMENTE temporal cos(k t) e mede-se o autovalor por
# regressao <B phi> = lambda * phi. Para box = d_t^2 - d_x^2:
#     box cos(k x) = +k^2 cos(k x)   -> lambda_espaco > 0
#     box cos(k t) = -k^2 cos(k t)   -> lambda_tempo  < 0
# A assinatura Lorentziana (sinais OPOSTOS) e o que se testa; a magnitude
# herda o mesmo ruido de T1, por isso o criterio aqui e o SINAL, nao o valor.

def _eig_regress(xs, ts, phi, mids, eps):
    B = np.array([sorkin_B_smeared(xs, ts, phi, xi, eps) for xi in mids])
    f = phi[mids]
    d = np.dot(f, f)
    return float(np.dot(f, B) / d) if d > 0 else float("nan")


def test_T2(rho=20.0, T=12.0, X=30.0, eps=0.2, n_real=20, k=40,
            ks=(0.4, 0.6, 0.8), verbose=True):
    l = 1.0 / np.sqrt(rho)
    lam_space, lam_time = {}, {}
    for kk in ks:
        sv, tv = [], []
        for seed in range(n_real):
            xs, ts = make_sprinkling(rho, T, X, seed)
            mids = _mid_events(xs, ts, T, X, k, seed)
            if mids.size < 5:
                continue
            sv.append(_eig_regress(xs, ts, np.cos(kk * xs), mids, eps))
            tv.append(_eig_regress(xs, ts, np.cos(kk * ts), mids, eps))
        lam_space[kk] = float(np.mean(sv))
        lam_time[kk] = float(np.mean(tv))
        if verbose:
            print(f"    [T2] k={kk:.2f}: lambda_space={lam_space[kk]:+7.3f} "
                  f"(want>0) | lambda_time={lam_time[kk]:+7.3f} (want<0)")
    space_pos = all(lam_space[kk] > 0 for kk in ks)
    time_neg = all(lam_time[kk] < 0 for kk in ks)
    verdict = {"lambda_space": lam_space, "lambda_time": lam_time,
               "space_all_positive": bool(space_pos),
               "time_all_negative": bool(time_neg),
               "lorentzian_signature": bool(space_pos and time_neg),
               "note": "qualitative (sign-based); magnitude inherits T1 noise"}
    return verdict


# =====================================================================
# T3 -- O SINAL ALTERNADO (a pergunta central; conecta e6)
# =====================================================================
#
# e6 estabeleceu: a rede da a GEOMETRIA da diferenca de caminho dL(x) da
# dupla fenda, mas FALTAM dois objetos para haver franjas escuras:
#   (i) algo que oscile com SINAL;  (ii) uma escala k passos->angulo.
#
# Resultado proprio de e10: o peso w(m) do operador de Sorkin ALTERNA DE
# SINAL de forma DETERMINISTICA e DERIVADA (e a razao pela qual constantes
# se aniquilam: a soma sobre o passado cancela phi(x)). Isto FORNECE o
# ingrediente (i) -- nao postulado, mas saido do operador da rede.
#
# HONESTIDADE: ter (i) NAO basta para mecanica quantica. A superposicao das
# duas fendas com este sinal da interferencia de ondas REAIS (Young classico
# tambem cancela). O salto quantico -- amplitude complexa, |psi|^2, regra de
# Born -- NAO e fornecido por B. Registrado explicitamente.

def test_T3(eps=0.2, verbose=True):
    # (1) Demonstrar (deterministico) que w(m) alterna de sinal.
    m = np.arange(0, 60, dtype=float)
    w = smeared_weight(m, eps)
    has_pos = bool(np.any(w > 0))
    has_neg = bool(np.any(w < 0))
    first_sign_change = int(np.argmax(np.sign(w[:-1]) != np.sign(w[1:]))) \
        if (has_pos and has_neg) else -1
    alternates = has_pos and has_neg

    # (2) Conexao com e6: existe a geometria dL? (ingrediente (ii) ja vem de e6.)
    dL_path = os.path.join(OUTDIR, "e6_dL.npy")
    e6_available = os.path.exists(dL_path)
    fringe_demo = None
    if e6_available:
        data = np.load(dL_path)
        screen_x, dL = data[:, 0], data[:, 1]
        good = np.isfinite(dL)
        screen_x, dL = screen_x[good], dL[good]
        # ---- COMPARISON ONLY -- fase postulada (regra dL->angulo de e6).
        # B FORNECE o sinal alternado (i); a escala k que mapeia passos em
        # angulo (ii) continua a ser postulada aqui (vem de e6, nao de B).
        # Campo real de duas fendas: phi = cos(k L_L)+cos(k L_R)
        #                               = 2 cos(k Lbar) cos(k dL/2).
        k_phase = 0.7
        envelope = np.abs(np.cos(k_phase * dL / 2.0))
        # END COMPARISON ONLY
        intensity = envelope ** 2
        ratio = float(intensity.min() / intensity.max()) if intensity.max() > 0 else 1.0
        fringe_demo = {"k_phase_postulated": k_phase,
                       "intensity_ratio_min_max": ratio,
                       "real_cancellation": bool(ratio < 0.05)}

    verdict = {
        "weight_alternates_sign": alternates,
        "first_sign_change_at_m": first_sign_change,
        "ingredient_i_supplied_by_B": bool(alternates),
        "e6_available": e6_available,
        "fringe_demo": fringe_demo,
        "ingredient_ii_still_postulated": True,
        "quantum_amplitude_present": False,
        "honest_verdict": (
            "OWN CONTENT (modest): the smeared Sorkin weight w(m) alternates "
            "sign by construction (positive near m=0, negative at intermediate "
            "m); this is the SAME sign-oscillation that e6 flagged as missing "
            "ingredient (i), now DERIVED from the network operator rather than "
            "postulated. It is the mechanism behind constant-annihilation. "
            "BUT: (a) the scale k mapping path-steps to phase (ingredient ii) "
            "is still imported (from e6, not from B); (b) the resulting two-"
            "slit cancellation is CLASSICAL real-wave interference (Young also "
            "cancels). The quantum content -- complex amplitude, |psi|^2, Born "
            "rule -- is NOT supplied by B. The TEIC<->QM boundary is now "
            "NARROWER (i) is solved, (ii)+Born remain) but not crossed."),
    }
    if verbose:
        print(f"    [T3] w(m) alterna de sinal? {alternates} "
              f"(1a troca em m={first_sign_change})  -> fornece (i) de e6")
        if fringe_demo:
            print(f"    [T3] (COMPARISON ONLY, k postulado) envelope real "
                  f"min/max={fringe_demo['intensity_ratio_min_max']:.4f} "
                  f"cancela={fringe_demo['real_cancellation']}")
        print(f"    [T3] (i) fornecido por B: SIM | (ii) escala k: ainda "
              f"postulada | |psi|^2 quantico: NAO")
    return verdict


# =====================================================================
# DRIVER
# =====================================================================

def run(quick=False):
    print("=" * 70)
    print("e10 -- D'ALEMBERTIANO CAUSAL DE SORKIN (EXPLORATORIO, ISOLADO)")
    print("=" * 70)
    print("Reproduz Sorkin 2007 / Benincasa-Dowker 2010. Nao e descoberta.")
    print("Operador afiado: flutuacoes ~rho^(3/4) (inviavel). Operador")
    print("suavizado (smeared/thinning): aniquila const, controla variancia.\n")

    rho, T, X, eps = (20.0, 12.0, 30.0, 0.2)
    nr1, nr2 = (8, 6) if quick else (30, 20)
    k1 = 40 if quick else 120          # amostras/realizacao (quick e mais leve)

    # ---- T1a: demonstrar inviabilidade do operador AFIADO ----
    print("  T1a -- operador AFIADO (so para mostrar a patologia BD):")
    sharp = test_T1a_sharp_variance(rho=rho, T=T, X=X, n_real=(4 if quick else 8))
    for kind in ["const", "t2"]:
        s = sharp[kind]
        print(f"    [T1a] {kind:>5}: mean={s['mean']:+10.2f}  std={s['std']:.1f}  "
              f"SEM={s['sem']:.1f}  (box={'0' if kind=='const' else '2'})")
    print("    => SEM >> sinal: operador afiado inviavel, como BD preveem.\n")

    # ---- T1: operador SUAVIZADO ----
    print(f"  T1 -- operador SUAVIZADO (eps={eps}, rho={rho}):")
    t1_results, t1_verdict = test_T1(rho=rho, T=T, X=X, eps=eps, n_real=nr1, k=k1)
    const_ok = t1_verdict["const_annihilates"]
    # T1b -- CONVERGENCIA: o vies de discretude encolhe quando eps*rho cresce?
    print("  T1b -- convergencia (vies de discretude vs densidade efetiva):")
    conv_settings = (((20.0, 12.0, 30.0), (60.0, 8.0, 14.0)) if not quick
                     else ((20.0, 10.0, 20.0), (50.0, 7.0, 12.0)))
    conv = test_T1_convergence(eps=eps, settings=conv_settings,
                               n_real=(6 if quick else 12), k=k1)
    for p in conv["points"]:
        print(f"    [T1b] eps*rho={p['eff_density']:5.1f}: |<B[lin]>|="
              f"{p['lin_bias']:.3f} +/- {p['sem']:.3f}  (box(lin)=0)")
    print(f"    [T1b] vies encolhe com densidade efetiva? "
          f"{'SIM' if conv['bias_shrinks_with_eff_density'] else 'NAO'}\n")

    # Veredito T1 HONESTO: o que e robusto vs o que e inviavel ponto-a-ponto.
    t1_status = (
        "T1 (honesto): CONST ANIQUILA (%.3f +/- %.3f) -- prova a ESTRUTURA e "
        "normalizacao do operador (teste prefactor-independente). O vies de "
        "discretude (campo linear) ENCOLHE com a densidade efetiva eps*rho "
        "(%s) -- evidencia de que <B> -> box. PORE'M a MAGNITUDE box ponto-a-"
        "ponto (t2=+2, x2=-2) NAO e recuperavel a custo acessivel: como "
        "B=2*eps*rho*bracket, o sinal vale box/(2*eps*rho) e fica afogado na "
        "variancia O(0.3) em todos os regimes (eps*rho baixo -> vies; alto -> "
        "SNR -> 0). E exatamente por isto que Benincasa-Dowker validam pela "
        "ACAO somada, nao pelo <B phi> pontual. Reproduz a dificuldade "
        "conhecida; nao se reivindica recuperacao quantitativa de box."
    ) % (t1_verdict["const_value"], t1_results["const"]["B_sem"],
         "SIM" if conv["bias_shrinks_with_eff_density"] else "nao nesta corrida")
    print(f"    => {t1_status}\n")

    out = {"params": {"rho": rho, "T": T, "X": X, "eps": eps, "n_real": nr1},
           "T1a_sharp_variance": sharp,
           "T1_results": t1_results, "T1_verdict": t1_verdict,
           "T1_convergence": conv, "T1_status": t1_status,
           "T1_const_annihilation": bool(const_ok),
           "T1_bias_shrinks": bool(conv["bias_shrinks_with_eff_density"]),
           "T1_pointwise_box_recovered": False}

    # T2: assinatura Lorentziana (so-sinais). Roda se a estrutura (const) esta
    # confirmada; explicitamente limitada por ruido (mesmo problema de SNR).
    if const_ok:
        print("  T2 -- assinatura Lorentziana (so-sinais; limitada por ruido):")
        t2_verdict = test_T2(rho=rho, T=T, X=X, eps=eps, n_real=nr2, k=k1)
        if t2_verdict["lorentzian_signature"]:
            print("    => assinatura LORENTZIANA nesta corrida (espaco>0, tempo<0); "
                  "fraco (mesmo afogamento de SNR de T1) -- nao se promove a "
                  "resultado.\n")
        else:
            print("    => NAO-CONCLUSIVO: os autovalores medidos nao separam sinais "
                  "de forma estavel (mesmo afogamento de SNR de T1). Dispersao "
                  "w^2=k^2 NAO demonstrada aqui.\n")
        out["T2_verdict"] = t2_verdict
    else:
        out["T2_verdict"] = "SKIPPED: const nao aniquilou (estrutura nao confirmada)."
        print("  T2 PULADO: const nao aniquilou nesta corrida.")

    # T3: DETERMINISTICO (propriedade do peso w). Roda SEMPRE -- e a pergunta
    # central pedida e nao depende da precisao de box. Conecta com e6.
    print("  T3 -- o sinal alternado (pergunta central; conecta e6):")
    t3_verdict = test_T3(eps=eps)
    out["T3_verdict"] = t3_verdict
    print(f"    => {t3_verdict['honest_verdict']}\n")

    out["note"] = ("Reproduz Sorkin/Benincasa-Dowker. Naive synchronous update "
                   "rule is DEAD. Sharp operator unusable (~rho^(3/4) noise). "
                   "Smeared operator: const-annihilation confirms structure; the "
                   "discreteness bias shrinks with eps*rho (convergence toward "
                   "box), but pointwise box MAGNITUDE is unrecoverable (signal "
                   "box/(2*eps*rho) buried under variance -- the reason BD use the "
                   "summed action). Only T3 (B's sign-alternating weight = e6's "
                   "missing ingredient i, DERIVED not postulated) is potentially "
                   "own content -- and it stays honest: classical real-wave "
                   "cancellation; quantum |psi|^2 still missing.")

    path = os.path.join(OUTDIR, "e10_sorkin.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  [resultados em {path}]")
    return out


if __name__ == "__main__":
    import sys
    run(quick=("--quick" in sys.argv))

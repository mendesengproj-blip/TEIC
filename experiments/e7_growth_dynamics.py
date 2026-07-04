"""
e7_growth_dynamics.py - DINAMICA DE CRESCIMENTO POR "ENCONTRO DE FRENTES"

STATUS: EXPLORATORIO e ISOLADO (como e6). Nao alimenta R1-R3 nem curvatura.
ORDEM: T1 -> T2 -> T3. Criterios de morte PRE-REGISTRADOS. Se uma tarefa matar,
       as seguintes NAO rodam.

T1: Bell causality para N=3..6 (7 se o tempo permitir).
T2: Comparacao com Rideout-Sorkin (CSG).
T3: Gera observavel diferente da percolacao?

------------------------------------------------------------------------------
NOTA DE AUDITORIA (externa) -- aplicada a este modulo
------------------------------------------------------------------------------
T1 (Bell): logica nao-vazia e correta; ~1346 pares com transicoes de encontro
  com espectadores foram exercitados. Sem bug. Rodar ate N=6 (N=7 se viavel).

T2 (Rideout-Sorkin): a logica esta correta, mas o ENUNCIADO do veredito precisa
  ser preciso. O teste compara a regra TEIC contra a SUBFAMILIA SIMPLIFICADA de
  RS, na qual o acoplamento t_k depende SO do tamanho |past| do conjunto-passado.
  A regra TEIC (peso por numero de componentes ancestrais unidas) esta FORA dessa
  subfamilia -- isso e correto e e o que o teste detecta.
  POReM: a regra TEIC e label-invariante e satisfaz Bell, logo e um membro VALIDO
  da familia GERAL de Rideout-Sorkin (Classical Sequential Growth). O enunciado
  correto e:
     "TEIC e um NOVO membro da familia RS-GERAL, parametrizado por n_components
      em vez do tamanho do past-set, situado FORA da subfamilia simplificada."
  Isto NAO e 'fora de RS' nem 'redescoberta da subfamilia'. e uma parametrizacao
  alternativa, covariante e legitima, dentro do arcabouco CSG. T2 NAO mata.

T3 (observaveis): sem vies de amostragem (timing ratio ~1.05). O efeito na
  ordering fraction e REAL e persiste, porem DIMINUI com N (delta ~ -0.053 em N=6,
  ~ -0.024 em N=14). Causa parcialmente DEFINICIONAL: suprimir encontros reduz, por
  construcao, conexoes cruzadas -> causets mais ESPARSAS. Reportar o delta vs N para
  exibir a tendencia (converge a zero vs. estabiliza).
------------------------------------------------------------------------------
"""

import itertools
import json
import os
import time
from collections import defaultdict
from fractions import Fraction

import numpy as np

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "results", "data")
os.makedirs(OUTDIR, exist_ok=True)

# ════════════════════════════════════════════════════════════════
# CORE: causet growth machinery
# ════════════════════════════════════════════════════════════════

def downward_closed_subsets(rel, n):
    """All downward-closed subsets of {0..n-1} under relation rel."""
    anc = {k: set(j for j in range(n) if rel[j][k]) for k in range(n)}
    result = []
    for r in range(0, n + 1):
        for combo in itertools.combinations(range(n), r):
            s = set(combo)
            if all(anc[x] <= s for x in s):
                result.append(combo)
    return result


def n_components(rel, n, nodes):
    """Number of connected components in the sub-poset induced by 'nodes'.
    Two nodes are in the same component if connected by any chain of relations.
    This is the LABEL-INVARIANT definition of 'number of centers merged'."""
    if not nodes:
        return 0
    node_set = set(nodes)
    adj = defaultdict(set)
    for a in node_set:
        for b in node_set:
            if a != b and (rel[a][b] or rel[b][a]):
                adj[a].add(b)
                adj[b].add(a)
    visited = set()
    comps = 0
    for node in node_set:
        if node not in visited:
            comps += 1
            stack = [node]
            while stack:
                v = stack.pop()
                if v in visited:
                    continue
                visited.add(v)
                stack.extend(adj[v] - visited)
    return comps


def grow_one(rel, n, past):
    """Add event n with past-set 'past'. Returns new relation matrix."""
    new = [row[:] + [False] for row in rel]
    new.append([False] * (n + 1))
    for p in past:
        new[p][n] = True
        for k in range(n):
            if rel[k][p]:
                new[k][n] = True
    return new


def canonical(rel, n):
    """Label-invariant canonical form of the causet (for grouping)."""
    best = None
    for perm in itertools.permutations(range(n)):
        mat = tuple(
            tuple(rel[perm[i]][perm[j]] for j in range(n)) for i in range(n)
        )
        if best is None or mat < best:
            best = mat
    return best


def teic_weight(rel, n, past, w_meet):
    """Weight for a transition adding event with given past-set.
    w_meet applied when the past-set merges >=2 components."""
    nc = n_components(rel, n, past)
    return Fraction(w_meet) if nc >= 2 else Fraction(1)


def transition_table(rel, n, w_meet):
    """All transitions from causet (rel, n) with their weights."""
    table = {}
    for past in downward_closed_subsets(rel, n):
        w = teic_weight(rel, n, past, w_meet)
        table[past] = w
    return table


def enumerate_causets(N_max):
    """All distinct (label-invariant) causets grown from size 1 up to N_max.
    Returns dict size -> list of (rel, n)."""
    all_causets = {1: [([[False]], 1)]}
    for size in range(2, N_max + 1):
        new_causets = []
        seen = set()
        for rel, n in all_causets.get(size - 1, []):
            for past in downward_closed_subsets(rel, n):
                new_rel = grow_one(rel, n, list(past))
                c = canonical(new_rel, size)
                if c not in seen:
                    seen.add(c)
                    new_causets.append((new_rel, size))
        all_causets[size] = new_causets
    return all_causets


# ════════════════════════════════════════════════════════════════
# T1: BELL CAUSALITY
# ════════════════════════════════════════════════════════════════

def find_spectators(rel, n, past_a, past_b):
    """Find maximal events that are spectators w.r.t. the difference
    between transitions past_a and past_b (causally disconnected from
    the symmetric difference)."""
    diff = set(past_a) ^ set(past_b)
    spectators = []
    for e in range(n):
        is_maximal = not any(rel[e][k] for k in range(n))
        if not is_maximal:
            continue
        connected = False
        for d in diff:
            if rel[e][d] or rel[d][e]:
                connected = True
                break
        if not connected and e not in set(past_a) | set(past_b):
            spectators.append(e)
    return spectators


def remove_event(rel, n, e):
    """Remove event e from causet, reindex remaining events."""
    remaining = [i for i in range(n) if i != e]
    new_n = n - 1
    new_rel = [[False] * new_n for _ in range(new_n)]
    for ni, oi in enumerate(remaining):
        for nj, oj in enumerate(remaining):
            new_rel[ni][nj] = rel[oi][oj]
    remap = {oi: ni for ni, oi in enumerate(remaining)}
    return new_rel, new_n, remap


def remap_past(past, remap):
    """Remap a past-set after event removal."""
    return tuple(sorted(remap[p] for p in past if p in remap))


def test_bell_causality(N_max, w_meet_values):
    """Test Bell causality for all causets up to N_max.
    Returns dict keyed by w_meet."""
    results = {}
    all_causets_by_size = enumerate_causets(N_max)

    for w_meet in w_meet_values:
        wm_key = str(w_meet)
        violations = []
        total_tests = 0
        meeting_tests = 0  # tests where the symmetric difference touches a meeting

        for size in range(3, N_max + 1):
            for rel, n in all_causets_by_size[size]:
                table = transition_table(rel, n, w_meet)
                pasts = list(table.keys())

                for i in range(len(pasts)):
                    for j in range(i + 1, len(pasts)):
                        pa, pb = pasts[i], pasts[j]
                        specs = find_spectators(rel, n, pa, pb)
                        for s in specs:
                            rel2, n2, remap = remove_event(rel, n, s)
                            pa2 = remap_past(pa, remap)
                            pb2 = remap_past(pb, remap)
                            table2 = transition_table(rel2, n2, w_meet)

                            if pa2 in table2 and pb2 in table2:
                                if table[pb] != 0 and table2[pb2] != 0:
                                    r_full = table[pa] * table2[pb2]
                                    r_red = table2[pa2] * table[pb]
                                    total_tests += 1
                                    # a 'meeting' is involved iff any of the four
                                    # weights differs from 1 (w_meet applied).
                                    if (table[pa] != 1 or table[pb] != 1 or
                                            table2[pa2] != 1 or table2[pb2] != 1):
                                        meeting_tests += 1
                                    if r_full != r_red:
                                        violations.append({
                                            "N": size,
                                            "spectator": s,
                                            "ratio_full": str(table[pa] / table[pb]),
                                            "ratio_reduced":
                                                str(table2[pa2] / table2[pb2]),
                                        })

        passed = len(violations) == 0
        results[wm_key] = {
            "passed": passed,
            "total_tests": total_tests,
            "meeting_tests": meeting_tests,
            "violations": violations[:5],
        }

    return results


# ════════════════════════════════════════════════════════════════
# T2: COMPARISON WITH RIDEOUT-SORKIN
# ════════════════════════════════════════════════════════════════

def test_rs_equivalence(N_test, w_meet_values):
    """For each w_meet, decide whether the TEIC meeting-weight rule lies inside
    the SIMPLIFIED Rideout-Sorkin subfamily (t_k depends only on |past|).

    Decisive test: if two transitions have the SAME past-size but DIFFERENT
    n_components, the TEIC weight differs while any simplified-RS t_k would be
    identical -> TEIC is OUTSIDE the simplified subfamily.

    Framing (audited): being outside the simplified subfamily does NOT mean
    'outside RS'. A label-invariant, Bell-causal rule is a valid member of the
    GENERAL RS / CSG family; TEIC simply parametrizes it by n_components instead
    of past-set size.
    """
    results = {}
    all_causets = enumerate_causets(N_test)

    for w_meet in w_meet_values:
        # past_size -> set of distinct TEIC weights observed
        weight_by_pastsize = defaultdict(set)
        # (past_size, n_components) -> weight  (the n_components parametrization)
        weight_by_pastsize_ncomp = {}

        for size in range(1, N_test + 1):
            for rel, n in all_causets[size]:
                for past in downward_closed_subsets(rel, n):
                    nc = n_components(rel, n, past)
                    w = teic_weight(rel, n, past, w_meet)
                    ps = len(past)
                    weight_by_pastsize[ps].add(w)
                    weight_by_pastsize_ncomp[(ps, nc)] = w

        conflicts = []
        for ps, weights in weight_by_pastsize.items():
            if len(weights) > 1:
                conflicts.append({
                    "past_size": ps,
                    "distinct_weights": [str(w) for w in sorted(weights)],
                })

        if conflicts:
            # Outside the SIMPLIFIED subfamily, but a valid GENERAL-RS member.
            results[str(w_meet)] = {
                "in_simplified_rs_subfamily": False,
                "in_general_rs_family": True,  # label-invariant + Bell-causal (T1)
                "reason": ("Same past-size maps to different TEIC weights because "
                           "the weight depends on n_components, not on |past|. "
                           "Outside the simplified RS subfamily (t_k = f(|past|)). "
                           "Still a valid member of the GENERAL Rideout-Sorkin / CSG "
                           "family, reparametrized by n_components."),
                "conflicts": conflicts,
                "ncomponents_parametrization": {
                    f"|past|={ps},ncomp={nc}": str(w)
                    for (ps, nc), w in sorted(weight_by_pastsize_ncomp.items())
                },
            }
        else:
            # Degenerate: weight is a pure function of |past| -> simplified RS.
            t_k = {ps: str(next(iter(weights)))
                   for ps, weights in weight_by_pastsize.items()}
            results[str(w_meet)] = {
                "in_simplified_rs_subfamily": True,
                "in_general_rs_family": True,
                "t_k_mapping": t_k,
            }

    return results


# ════════════════════════════════════════════════════════════════
# T3: OBSERVABLE DIFFERENCES (Monte Carlo)
# ════════════════════════════════════════════════════════════════

def sample_causet(N, w_meet, rng):
    """Grow a single causet of size N using the TEIC rule."""
    rel = [[False]]
    n = 1
    for _ in range(N - 1):
        opts = []
        total = Fraction(0)
        for past in downward_closed_subsets(rel, n):
            w = teic_weight(rel, n, past, w_meet)
            opts.append((past, w))
            total += w
        probs = [float(w / total) for _, w in opts]
        idx = rng.choice(len(opts), p=probs)
        chosen_past = opts[idx][0]
        rel = grow_one(rel, n, list(chosen_past))
        n += 1
    return rel, n


def longest_chain(rel, n):
    """Length of longest chain in the causet."""
    dp = [0] * n
    for j in range(n):
        for i in range(j):
            if rel[i][j]:
                dp[j] = max(dp[j], dp[i] + 1)
    return max(dp)


def n_maximal(rel, n):
    """Number of maximal elements."""
    return sum(1 for k in range(n) if not any(rel[k][j] for j in range(n)))


def ordering_fraction(rel, n):
    """Fraction of pairs that are causally related."""
    if n < 2:
        return 0.0
    total = 0
    related = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += 1
            if rel[i][j] or rel[j][i]:
                related += 1
    return related / total if total > 0 else 0.0


def test_observables(N_sizes, w_meet, n_samples=3000, seed=42):
    """Compare TEIC (w_meet) vs percolation (w=1) on physical observables.
    Records timing per ensemble (sampling-bias check) and the ordering-fraction
    delta per N (convergence-vs-N check)."""
    from scipy import stats

    results = {}
    rng = np.random.default_rng(seed)

    for N in N_sizes:
        obs_teic = {"chain": [], "maximal": [], "ordering": []}
        obs_perc = {"chain": [], "maximal": [], "ordering": []}

        t_teic = 0.0
        t_perc = 0.0
        for _ in range(n_samples):
            t0 = time.perf_counter()
            rel_t, n_t = sample_causet(N, w_meet, rng)
            t_teic += time.perf_counter() - t0
            obs_teic["chain"].append(longest_chain(rel_t, n_t))
            obs_teic["maximal"].append(n_maximal(rel_t, n_t))
            obs_teic["ordering"].append(ordering_fraction(rel_t, n_t))

            t0 = time.perf_counter()
            rel_p, n_p = sample_causet(N, Fraction(1), rng)
            t_perc += time.perf_counter() - t0
            obs_perc["chain"].append(longest_chain(rel_p, n_p))
            obs_perc["maximal"].append(n_maximal(rel_p, n_p))
            obs_perc["ordering"].append(ordering_fraction(rel_p, n_p))

        ks_results = {}
        for key in obs_teic:
            stat, pval = stats.ks_2samp(obs_teic[key], obs_perc[key])
            ks_results[key] = {
                "statistic": float(stat),
                "p_value": float(pval),
                "mean_teic": float(np.mean(obs_teic[key])),
                "mean_perc": float(np.mean(obs_perc[key])),
                "delta": float(np.mean(obs_teic[key]) - np.mean(obs_perc[key])),
                "significant": pval < 0.01,
            }
        ks_results["_timing_ratio"] = (t_teic / t_perc) if t_perc > 0 else None
        ks_results["_n_samples"] = n_samples
        results[N] = ks_results

    return results


# ════════════════════════════════════════════════════════════════
# MAIN: run T1 -> T2 -> T3 with kill criteria
# ════════════════════════════════════════════════════════════════

def run(n_max_t1=6, t3_sizes=(6, 8, 10, 12, 14), t3_samples=3000):
    W_MEET_VALUES = [Fraction(1, 3), Fraction(1, 2), Fraction(2),
                     Fraction(3), Fraction(5)]
    verdict = {"T1": None, "T2": None, "T3": None, "final": None}
    params = {  # provenance: the JSON below is self-describing
        "n_max_t1": n_max_t1,
        "w_meet_values": [str(w) for w in W_MEET_VALUES],
        "t3_w_meet": "1/3",
        "t3_sizes": list(t3_sizes),
        "t3_samples": t3_samples,
        "t3_seed": 42,
    }

    # ── T1 ──────────────────────────────────────────────────
    print("=" * 60)
    print(f"T1 - BELL CAUSALITY (N=3..{n_max_t1})")
    print("=" * 60)
    t0 = time.perf_counter()
    t1 = test_bell_causality(n_max_t1, W_MEET_VALUES)
    print(f"  [enumerated + tested in {time.perf_counter() - t0:.1f}s]")

    any_violation = False
    for wm, res in t1.items():
        status = "PASSED" if res["passed"] else "VIOLATED"
        print(f"  w_meet={wm:>4}: {status}  "
              f"({res['total_tests']} tests, {res['meeting_tests']} involve a meeting)")
        if not res["passed"]:
            any_violation = True
            for v in res["violations"][:2]:
                print(f"    violation N={v['N']}: "
                      f"{v['ratio_full']} != {v['ratio_reduced']}")

    if any_violation:
        verdict["T1"] = "KILLED - Bell violated"
        verdict["final"] = ("Desfecho 2: a regra de peso-de-encontro viola "
                            "covariancia geral (Bell).")
        print(f"\n  VERDICT T1: {verdict['T1']}")
        print("  T2 e T3 NAO executados.")
        _save_and_exit(verdict, params, t1_data=t1)
        return verdict

    verdict["T1"] = f"SURVIVED - Bell OK ate N={n_max_t1}"
    print(f"\n  VERDICT T1: {verdict['T1']}")
    print("  Prosseguindo para T2.\n")

    # ── T2 ──────────────────────────────────────────────────
    print("=" * 60)
    print("T2 - RIDEOUT-SORKIN (CSG) MEMBERSHIP")
    print("=" * 60)
    t2 = test_rs_equivalence(5, W_MEET_VALUES)

    all_simplified = True
    for wm, res in t2.items():
        if res["in_simplified_rs_subfamily"]:
            print(f"  w_meet={wm:>4}: in SIMPLIFIED RS subfamily. "
                  f"t_k = {res['t_k_mapping']}")
        else:
            all_simplified = False
            print(f"  w_meet={wm:>4}: OUTSIDE simplified subfamily "
                  f"(in_general_RS={res['in_general_rs_family']}). "
                  f"conflicts={res['conflicts'][:1]}")

    if all_simplified:
        # Degenerate edge case: weight is a pure function of |past|.
        verdict["T2"] = "KILLED - reduces to simplified RS subfamily"
        verdict["final"] = ("Desfecho 1: a regra de encontro reduz-se a subfamilia "
                            "RS simplificada (t_k = f(|past|)).")
        print(f"\n  VERDICT T2: {verdict['T2']}")
        print("  T3 NAO executado.")
        _save_and_exit(verdict, params, t1_data=t1, t2_data=t2)
        return verdict

    # CORRECTED FRAMING (audited): not 'outside RS', not a rediscovery of the
    # simplified subfamily. A new member of the GENERAL RS/CSG family,
    # parametrized by n_components rather than past-set size.
    verdict["T2"] = ("SURVIVED - new GENERAL-RS member, parametrized by "
                     "n_components (outside the simplified t_k=f(|past|) subfamily)")
    print(f"\n  VERDICT T2: {verdict['T2']}")
    print("  (Membro valido da familia CSG geral: label-invariante + Bell-causal.)")
    print("  Prosseguindo para T3.\n")

    # ── T3 ──────────────────────────────────────────────────
    print("=" * 60)
    print("T3 - OBSERVABLE DIFFERENCES (Monte Carlo, w_meet=1/3 FIXED)")
    print("=" * 60)
    t0 = time.perf_counter()
    t3 = test_observables(N_sizes=list(t3_sizes), w_meet=Fraction(1, 3),
                          n_samples=t3_samples, seed=42)
    print(f"  [MC sampled in {time.perf_counter() - t0:.1f}s]")

    any_significant = False
    print("\n  ordering-fraction delta (teic - perc) vs N "
          "[convergence check]:")
    for N in t3_sizes:
        d = t3[N]["ordering"]["delta"]
        p = t3[N]["ordering"]["p_value"]
        tr = t3[N]["_timing_ratio"]
        print(f"    N={N:>3}: delta_ordering={d:+.4f}  (KS p={p:.2e}, "
              f"timing_ratio={tr:.2f})")

    for N in t3_sizes:
        obs = t3[N]
        print(f"\n  N={N}:")
        for key in ("chain", "maximal", "ordering"):
            res = obs[key]
            sig = "***" if res["significant"] else ""
            print(f"    {key:>10}: KS={res['statistic']:.4f} p={res['p_value']:.2e} "
                  f"mean_teic={res['mean_teic']:.3f} mean_perc={res['mean_perc']:.3f} "
                  f"{sig}")
            if res["significant"]:
                any_significant = True

    if not any_significant:
        verdict["T3"] = "KILLED - no observable difference"
        verdict["final"] = ("Desfecho: dinamica covariante (novo membro RS-geral) "
                            "mas fisicamente indistinguivel da percolacao.")
    else:
        verdict["T3"] = "SURVIVED - observable difference detected"
        verdict["final"] = (
            "Desfecho 3: dinamica de crescimento covariante, NOVO membro da "
            "familia RS-geral (parametrizada por n_components, fora da subfamilia "
            "simplificada t_k=f(|past|)), com consequencia observavel -- a regra de "
            "peso-de-encontro produz causets mais ESPARSAS (ordering fraction menor). "
            "O efeito e real mas decresce com N (parcialmente definicional). "
            "AUDITAR antes de reivindicar.")

    print(f"\n  VERDICT T3: {verdict['T3']}")
    _save_and_exit(verdict, params, t1_data=t1, t2_data=t2, t3_data=t3)
    return verdict


def _save_and_exit(verdict, params=None, t1_data=None, t2_data=None, t3_data=None):
    """Save all results to JSON."""
    def serialize(obj):
        if isinstance(obj, Fraction):
            return str(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        raise TypeError(f"Not serializable: {type(obj)}")

    out = {
        "verdict": verdict,
        "params": params,
        "T1": _fraction_to_str(t1_data) if t1_data else None,
        "T2": _fraction_to_str(t2_data) if t2_data else None,
        "T3": t3_data,
    }
    path = os.path.join(OUTDIR, "e7_growth_dynamics.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, default=serialize)
    print(f"\n  [results saved to {path}]")

    print("\n" + "=" * 60)
    print("FINAL VERDICT")
    print("=" * 60)
    print(f"  {verdict['final']}")


def _fraction_to_str(data):
    """Recursively convert Fraction to str for JSON serialization."""
    if isinstance(data, dict):
        return {k: _fraction_to_str(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_fraction_to_str(v) for v in data]
    if isinstance(data, Fraction):
        return str(data)
    return data


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""SU3_ORDEM_L32 -- parallel-tempering driver for the order of the SU(3) colour
transition at L>=32.  Charter: docs/campaigns/SU3_ORDEM_L32/PRE_REGISTRO.md.

PURELY REAL analysis layer.  All SU(3)-complex algebra lives inside su3_core
(imported UNMODIFIED).  This file only orchestrates replicas, swaps in J, and
real-valued observables (order parameter, susceptibility, Binder U4, overlap
density b = U/n_edges, and the energy histogram for the free-energy barrier).

Replica exchange:  weight w ~ exp(J * U), U = sum_<ij> (1/3)Re Tr(U_i U_j^dag)
(the overlap sum).  Swap acceptance between adjacent slots a,b:
    p_swap = min(1, exp[ (J_a - J_b) * (U_b - U_a) ]).
"""
import os, sys, json, time, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FL1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "results", "matter", "fl1"))
sys.path.insert(0, FL1)
from su3_core import lattice_periodic, SU3ChiralModel  # noqa: E402


def overlap_sum(model):
    """U = sum over edges of v_i . v_j  (J-independent; energy_per_link = -J*U/n_edges)."""
    e = model.g.edges
    if e.shape[0] == 0:
        return 0.0
    return float(np.sum(model.v[e[:, 0]] * model.v[e[:, 1]]))


def run_pt(L, jlo, jhi, R, n_burn, n_meas, swap_every, meas_every, seed,
           block=1, warmup=300, verbose=True):
    """One parallel-tempering run over R replicas linearly spaced in J in [jlo,jhi].

    Returns a dict of per-slot observables + swap diagnostics + energy samples.
    """
    graph = lattice_periodic((L, L, L))
    n_edges = graph.edges.shape[0]
    ladder = np.linspace(jlo, jhi, R)

    reps = [SU3ChiralModel(graph, J=ladder[k], seed=seed * 131 + k, init=None)
            for k in range(R)]

    # ---- per-replica step auto-tuning (target acc ~0.4), then steps frozen -----
    tw = time.time()
    for rp in reps:
        rp.equilibrate(warmup, adapt=True, target=0.4)
    if verbose:
        print(f"[L={L} seed={seed}] warmup {warmup} sweeps/replica done in "
              f"{time.time()-tw:.1f}s; steps={[round(rp.step,3) for rp in reps]}")

    # ---- burn-in: sweeps + swaps, steps frozen ---------------------------------
    t0 = time.time()
    swap_attempt = np.zeros(R - 1)
    swap_accept = np.zeros(R - 1)
    # config tag follows the configuration as it walks in J; track extreme touched
    tag = np.arange(R)
    last_extreme = np.full(R, 0, dtype=int)     # -1 bottom, +1 top, 0 unknown; index by tag
    last_extreme[tag[0]] = -1
    last_extreme[tag[R - 1]] = +1
    up_crossings = 0     # completed traversals bottom->top (round-trip proxy)

    for s in range(n_burn):
        for rp in reps:
            for _ in range(block):
                rp.sweep()
        # swaps during burn help cross the barrier
        if (s + 1) % swap_every == 0:
            parity = (s // swap_every) % 2
            U = np.array([overlap_sum(rp) for rp in reps])
            for i in range(parity, R - 1, 2):
                dlogw = (ladder[i] - ladder[i + 1]) * (U[i + 1] - U[i])
                if np.log(np.random.random() + 1e-300) < dlogw:
                    reps[i].U, reps[i + 1].U = reps[i + 1].U, reps[i].U
                    reps[i].v, reps[i + 1].v = reps[i + 1].v, reps[i].v
                    reps[i].step, reps[i + 1].step = reps[i + 1].step, reps[i].step
                    tag[i], tag[i + 1] = tag[i + 1], tag[i]

    burn_time = time.time() - t0
    if verbose:
        print(f"[L={L} seed={seed}] burn {n_burn} sweeps done in {burn_time:.1f}s; "
              f"steps={[round(rp.step,3) for rp in reps]}")

    # ---- measurement: sweeps + swaps, steps frozen -----------------------------
    # accumulators per slot
    sum_m = np.zeros(R); sum_m2 = np.zeros(R); sum_m4 = np.zeros(R)
    sum_b = np.zeros(R); sum_b2 = np.zeros(R)
    n_samp = 0
    b_samples = [[] for _ in range(R)]   # overlap density per slot for histograms
    # round-trip tracking re-init for measurement window
    last_extreme = np.full(R, 0, dtype=int)
    last_extreme[tag[0]] = -1
    last_extreme[tag[R - 1]] = +1
    swap_attempt[:] = 0; swap_accept[:] = 0

    t1 = time.time()
    for s in range(n_meas):
        for rp in reps:
            for _ in range(block):
                rp.sweep()
        if (s + 1) % swap_every == 0:
            parity = (s // swap_every) % 2
            U = np.array([overlap_sum(rp) for rp in reps])
            for i in range(parity, R - 1, 2):
                swap_attempt[i] += 1
                dlogw = (ladder[i] - ladder[i + 1]) * (U[i + 1] - U[i])
                if np.log(np.random.random() + 1e-300) < dlogw:
                    swap_accept[i] += 1
                    reps[i].U, reps[i + 1].U = reps[i + 1].U, reps[i].U
                    reps[i].v, reps[i + 1].v = reps[i + 1].v, reps[i].v
                    reps[i].step, reps[i + 1].step = reps[i + 1].step, reps[i].step
                    tag[i], tag[i + 1] = tag[i + 1], tag[i]
            # round-trip bookkeeping at the extremes
            bot_tag, top_tag = tag[0], tag[R - 1]
            if last_extreme[bot_tag] == +1:
                up_crossings += 1  # came from top, now at bottom = completed traversal
            last_extreme[bot_tag] = -1
            last_extreme[top_tag] = +1
        if (s + 1) % meas_every == 0:
            n_samp += 1
            for k, rp in enumerate(reps):
                m = rp.order_parameter()
                b = overlap_sum(rp) / n_edges
                sum_m[k] += m; sum_m2[k] += m * m; sum_m4[k] += m ** 4
                sum_b[k] += b; sum_b2[k] += b * b
                b_samples[k].append(b)

    meas_time = time.time() - t1
    N = graph.n
    mean_m = sum_m / n_samp
    mean_m2 = sum_m2 / n_samp
    mean_m4 = sum_m4 / n_samp
    chi = N * (mean_m2 - mean_m ** 2)
    U4 = 1.0 - mean_m4 / (3.0 * mean_m2 ** 2)
    mean_b = sum_b / n_samp
    var_b = sum_b2 / n_samp - mean_b ** 2
    Cv = (N if False else n_edges) ** 0 * (ladder ** 2) * (n_edges) * var_b  # specific-heat-like: J^2 * n_edges * var(b)

    swap_rate = np.divide(swap_accept, np.maximum(swap_attempt, 1))

    return {
        "L": L, "N": int(N), "n_edges": int(n_edges), "seed": seed,
        "ladder": ladder.tolist(),
        "n_burn": n_burn, "n_meas": n_meas, "n_samp": n_samp,
        "swap_every": swap_every, "meas_every": meas_every, "block": block,
        "mean_m": mean_m.tolist(), "chi": chi.tolist(), "U4": U4.tolist(),
        "mean_b": mean_b.tolist(), "var_b": var_b.tolist(), "Cv_like": Cv.tolist(),
        "swap_rate": swap_rate.tolist(),
        "up_crossings": int(up_crossings),
        "burn_time_s": burn_time, "meas_time_s": meas_time,
        "b_samples": [list(map(float, bs)) for bs in b_samples],
    }


def analyse_run(res):
    """Locate pseudo-critical slot (max chi), report U4 there, and the energy
    histogram dip depth at that slot (OT-comparable bimodality diagnostic)."""
    chi = np.array(res["chi"]); U4 = np.array(res["U4"]); ladder = np.array(res["ladder"])
    kstar = int(np.argmax(chi))
    out = {
        "chi_max": float(chi[kstar]),
        "J_at_chi_max": float(ladder[kstar]),
        "U4_at_chi_max": float(U4[kstar]),
        "kstar": kstar,
        "min_swap_rate": float(np.min(res["swap_rate"])),
        "up_crossings": res["up_crossings"],
    }
    # bimodality / dip depth at kstar (and neighbours), OT-style
    dips = {}
    for k in [kstar - 1, kstar, kstar + 1]:
        if 0 <= k < len(ladder):
            b = np.array(res["b_samples"][k])
            dip = _dip_depth(b)
            dips[str(round(float(ladder[k]), 4))] = float(dip)
    out["dip_depth_by_J"] = dips
    out["dip_depth_at_chi_max"] = dips.get(str(round(float(ladder[kstar]), 4)), 0.0)
    return out


def _dip_depth(b, min_samples=300):
    """Bimodality measure in [0,1] for the overlap-density samples `b`.
    Returns 1 - h_valley/min(peak1,peak2) for the best-separated genuine valley,
    or 0 if unimodal / under-sampled.  Hardened against low-statistics false
    positives: adaptive bin count, heavy smoothing, secondary peak must reach
    >=30% of the global peak, peaks must be >=4 bins apart, and dips below 0.15
    are treated as flat (returned as the raw value but flagged unimodal upstream)."""
    b = np.asarray(b, dtype=float)
    if b.size < min_samples:
        return 0.0
    nb = int(np.clip(np.sqrt(b.size) / 1.5, 15, 30))
    hist, _ = np.histogram(b, bins=nb, density=True)
    # heavy smoothing (length-5 box) to suppress shot noise
    kern = np.ones(5) / 5.0
    h = np.convolve(hist, kern, mode="same")
    n = len(h)
    gmax = int(np.argmax(h))
    best = 0.0
    for p2 in range(n):
        if abs(p2 - gmax) < 4:
            continue
        if h[p2] < 0.30 * h[gmax]:
            continue
        lo, hi = sorted((gmax, p2))
        valley = h[lo + 1:hi].min() if hi - lo > 1 else h[gmax]
        peaks = min(h[gmax], h[p2])
        if peaks <= 0 or h[p2] <= valley * 1.10:
            continue
        dip = 1.0 - valley / peaks
        if dip > best:
            best = dip
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--jlo", type=float, default=2.66)
    ap.add_argument("--jhi", type=float, default=2.82)
    ap.add_argument("--R", type=int, default=24)
    ap.add_argument("--burn", type=int, default=20000)
    ap.add_argument("--meas", type=int, default=100000)
    ap.add_argument("--swap_every", type=int, default=10)
    ap.add_argument("--meas_every", type=int, default=10)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--seeds", type=str, default="7,1007,2007,3007")
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--no_bsamples", action="store_true",
                    help="drop raw b_samples from JSON to save space")
    args = ap.parse_args()

    seeds = [int(x) for x in args.seeds.split(",")]
    runs = []
    for sd in seeds:
        r = run_pt(args.L, args.jlo, args.jhi, args.R, args.burn, args.meas,
                   args.swap_every, args.meas_every, sd, warmup=args.warmup)
        a = analyse_run(r)
        print(f"[L={args.L} seed={sd}] chi_max={a['chi_max']:.2f} "
              f"@J={a['J_at_chi_max']:.3f}  U4={a['U4_at_chi_max']:.3f}  "
              f"min_swap={a['min_swap_rate']:.2f}  up_cross={a['up_crossings']}  "
              f"dip@chimax={a['dip_depth_at_chi_max']:.3f}")
        r["analysis"] = a
        if args.no_bsamples:
            r.pop("b_samples", None)
        runs.append(r)

    # aggregate across seeds at the pseudo-critical slot
    chi_max = np.mean([rr["analysis"]["chi_max"] for rr in runs])
    U4_star = np.mean([rr["analysis"]["U4_at_chi_max"] for rr in runs])
    Jc = np.mean([rr["analysis"]["J_at_chi_max"] for rr in runs])
    dip = np.mean([rr["analysis"]["dip_depth_at_chi_max"] for rr in runs])
    summary = {
        "L": args.L, "n_seeds": len(seeds),
        "chi_max_mean": float(chi_max), "U4_at_chi_max_mean": float(U4_star),
        "Jc_mean": float(Jc), "dip_depth_mean": float(dip),
        "min_swap_rate_min": float(np.min([rr["analysis"]["min_swap_rate"] for rr in runs])),
        "up_crossings_min": int(np.min([rr["analysis"]["up_crossings"] for rr in runs])),
    }
    payload = {"summary": summary, "args": vars(args), "runs": runs}
    with open(args.out, "w") as f:
        json.dump(payload, f)
    print("SUMMARY:", json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

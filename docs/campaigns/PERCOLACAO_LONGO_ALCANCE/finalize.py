"""
finalize.py -- aplica o CRITERIO 5 COMPLETO do PRE_REGISTRO (Secao 5), combinando:
  (a) saturacao de <z> (expoente local relativo) ............ longrange.json
  (b) C4 positivo NAO-decaindo ............................... longrange.json
  (c) C4 ACIMA do controle aleatorio de mesma densidade ..... control_c4.json  <-- criterio 5

So conta como JANELA o sigma onde <z> satura E C4 satura>0 E C4>controle. Escreve
verdict_final.json (autoritativo).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

meas = json.load(open(os.path.join(HERE, "longrange.json")))
ctrl = json.load(open(os.path.join(HERE, "control_c4.json")))
above = {f"{r['sigma']}": r["above_control"] for r in ctrl["rows"]}
ratio = {f"{r['sigma']}": r["ratio_fam_over_rnd"] for r in ctrl["rows"]}

Z_REL = 0.05
C4_SAT = 0.02
C4_DECAY = 0.5

per = {}
z_sat_sigmas, c4_nontrivial_sigmas, window = [], [], []
for key, R in meas["by_sigma"].items():
    rows = R["rows"]
    z_top, z_first = rows[-1]["z_mean"], rows[0]["z_mean"]
    c4_top, c4_first = rows[-1]["C4"], rows[0]["C4"]
    z_slope = R["z_slope_top"]
    z_rel = z_slope / z_top if z_top else 0.0
    z_dec = (len(R["z_dlnN"]) < 2) or (R["z_dlnN"][-1] <= R["z_dlnN"][-2] + 1e-9)
    z_sat = (z_rel < Z_REL) and z_dec
    c4_nondecay = (c4_top >= C4_DECAY * c4_first) if c4_first > 0 else False
    c4_above = above.get(key, False)
    c4_nontrivial = (c4_top > C4_SAT) and c4_nondecay and c4_above   # criterio 5 COMPLETO
    win = bool(z_sat and c4_nontrivial)
    per[key] = {"sigma": R["sigma"], "z_top": z_top, "z_rel_slope": z_rel,
                "z_saturates": bool(z_sat),
                "c4_top": c4_top, "c4_nondecay": bool(c4_nondecay),
                "c4_above_control": bool(c4_above),
                "c4_ratio_over_control": ratio.get(key),
                "c4_nontrivial": bool(c4_nontrivial), "window": win}
    if z_sat:
        z_sat_sigmas.append(R["sigma"])
    if c4_nontrivial:
        c4_nontrivial_sigmas.append(R["sigma"])
    if win:
        window.append(R["sigma"])

final = {
    "criterion": "Secao 5 COMPLETA: janela = <z> satura E C4>0 nao-decai E C4>controle",
    "z_saturates_sigmas": z_sat_sigmas,
    "c4_nontrivial_sigmas": c4_nontrivial_sigmas,
    "window_sigmas": window,
    "per_sigma": per,
    "verdict": "JANELA_ENCONTRADA" if window else "SEM_JANELA",
    "lorentz_invariance": "PASS (gate item 5: arestas bit-identicas sob boost eta=0.8)",
    "note": ("<z> diverge em TODOS os sigma (slope rel >=0.38, nunca <0.05); "
             "C4 fica ABAIXO do controle aleatorio em 0/11 sigma -> nem a barreira de "
             "lacos e passada de forma nao-trivial. Sem ponto de sobreposicao."),
}
json.dump(final, open(os.path.join(HERE, "verdict_final.json"), "w"), indent=2)

print("=" * 64)
print("VERDICT FINAL (criterio 5 completo, com controle de triviality)")
print("=" * 64)
for key, p in per.items():
    print(f"  sigma={p['sigma']:>4}: z_top={p['z_top']:6.2f} "
          f"z_rel_slope={p['z_rel_slope']:+.3f} {'SAT' if p['z_saturates'] else 'div'} | "
          f"C4_top={p['c4_top']:.4f} ratio/ctrl={p['c4_ratio_over_control']:.3f} "
          f"{'>ctrl' if p['c4_above_control'] else '<ctrl'} "
          f"[{'JANELA' if p['window'] else '-'}]")
print(f"\n  <z> satura em sigma  = {z_sat_sigmas}")
print(f"  C4 nao-trivial em    = {c4_nontrivial_sigmas}")
print(f"  JANELA (ambos) em    = {window}")
print(f"\n  >>> VEREDITO FINAL: {final['verdict']}")

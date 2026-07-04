"""W4_dev_comparison.py -- compare the full action (links + plaquettes) with the DEV.

BRIDGE/WILSON task W4.  Reads the MEASURED coefficients from W2 (no recompute) and
contrasts them, operator by operator, with the DEV scalar/vector Lagrangian.  This is
the ONLY task where the DEV enters (anti-circularity).

DEV (docs/DEV_bridge_future.md eq.1):
    L_DEV = K(X,theta) - (1/4) F_mn F^mn - (m_A^2/2) A^2 + gamma A.dtheta
Full action (links + plaquettes), coarse-grained (C1/C2 + W1/W2):
    S_eff = C1 X + C2 A^2 + C3 A.dtheta + C_q (A.dtheta)^2 + rho sqrt(1-X/X0)
            + C_F F_mn F^mn   (from plaquettes)
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path

OUT = Path(__file__).resolve().parent
w2 = json.loads((OUT / "W2_coarse_graining_data.json").read_text())

d4 = w2["d4"]

# operator-by-operator comparison
operators = {
    "X = (dtheta)^2": {
        "minimal+plaq": "C1 (= kappa n/2, measured)",
        "DEV": "K(X) kinetic (free)", "status": "MATCH (form); DEV coeff free"},
    "A^2": {
        "minimal+plaq": "C2 = C1 (locked by Stuckelberg square)",
        "DEV": "-m_A^2/2 (free)", "status": "MATCH (form); ratio C2/C1=1 locked, DEV free"},
    "A.dtheta": {
        "minimal+plaq": "C3 = 2 C1 (locked by square)",
        "DEV": "gamma (free)", "status": "MATCH (form); ratio C3/C1=2 locked, DEV free"},
    "F_mn F^mn": {
        "minimal+plaq": f"C_F = lambda_p * Pi/4 (EMERGES from plaquettes; lambda_p free)",
        "DEV": "-1/4 (i.e. free K)", "status": "MATCH (form NOW PRESENT - fixes C4 gap); weight free both sides"},
    "sqrt(1-X/X0) (DBI)": {
        "minimal+plaq": "from link saturation (W3), X0 ~ rho (C3 task)",
        "DEV": "absorbed in general K(X)", "status": "MATCH if K(X) is DBI-type"},
    "(A.dtheta)^2 quartic": {
        "minimal+plaq": "C_q (measured, !=0, sign<0)",
        "DEV": "ABSENT (vector sector <= quadratic in A)", "status": "EXTRA -> new prediction"},
    "F ^ F (theta-term, E.B)": {
        "minimal+plaq": "coeff ~ <Om01 Om23> = 0 +/- (parity)",
        "DEV": "absent", "status": "ABSENT both -> consistent (no parity violation)"},
    "E/B Lorentz split": {
        "minimal+plaq": f"E/B = {d4['EB_anisotropy_ratio']:.2f} (raw plaquettes, LV)",
        "DEV": "1 (Lorentz invariant)", "status": "MISMATCH -> order-1 LV, needs BD smearing (= C1 issue)"},
}

# ratios
ratios = {
    "C2/C1 (minimal)": 1.0, "C3/C1 (minimal)": 2.0,
    "C2/C1 (DEV)": "free (-m_A^2/2 / K')", "C3/C1 (DEV)": "free (gamma / K')",
    "C_F/C3 (minimal)": "lambda_p * Pi / (4 kappa n) = FREE via lambda_p",
    "C_F/C3 (DEV-analog)": "(-1/4)/gamma = FREE (K independent of gamma)",
}

new_predictions = [
    "Gauge-invariant quartic self-interaction (A+dtheta)^4 [incl. (A.dtheta)^2, "
    "A^2(dtheta)^2, A^4]: absent in DEV; appears in strong field / steep density "
    "gradients; coefficient C_q fixed RELATIVE to the quadratic (not free).",
    "DBI saturation of BOTH channels (W3): link DBI sqrt(1-X/X0) AND plaquette "
    "saturation 1-cos(W) -> a 'magnetic' saturation of F^2 at large field strength, "
    "absent from the polynomial DEV.",
    "Order-1 Lorentz violation (E/B ~ 3, a_t/a_x ~ 3) at the RAW link/plaquette level: "
    "a falsifiable prediction that the bare causal-set action is NOT Lorentz invariant; "
    "Lorentz invariance is recovered only via the non-local BD kernel.",
]

status = (
    "FORM-COMPLETE, CALIBRATION- AND LORENTZ-OPEN.  With plaquettes the action now "
    "produces EVERY DEV operator (X, F^2, A^2, A.dtheta) -- the C4 'missing F^2' gap is "
    "closed -- plus the locked Stuckelberg ratios (1,2) and extra quartics. What is NOT "
    "derived: (i) the gauge-sector weight lambda_p (free, exactly as DEV's K is free); "
    "(ii) Lorentz invariance at the raw level (E/B ~ 3 -> needs BD non-locality); "
    "(iii) the scale a_0 (C3: X0 ~ rho is UV, not cH).  Net: the one-line action + "
    "plaquettes is the gauge-invariant Proca/Stuckelberg + Maxwell STRUCTURE of a "
    "DEV-sister, with the gauge kinetic weight and Lorentz restoration as the next layer."
)

summary = {
    "operators": operators, "ratios": ratios, "new_predictions": new_predictions,
    "measured_d4": {"EB_anisotropy": d4["EB_anisotropy_ratio"],
                    "C_F_per_lambda_p": d4["C_F_per_lambda_p"],
                    "C3": d4["C3"], "C_q": d4["C_q_quartic"]},
    "status": status,
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
(OUT / "W4_dev_comparison_data.json").write_text(json.dumps(summary, indent=2))

print("=" * 72)
print("W4 -- FULL ACTION (links + plaquettes)  vs  DEV")
print("=" * 72)
print("\nOperator-by-operator:")
for op, d in operators.items():
    print(f"  {op}")
    print(f"      ours: {d['minimal+plaq']}")
    print(f"      DEV : {d['DEV']}")
    print(f"      ==>  {d['status']}")
print("\nRatios:")
for k, v in ratios.items():
    print(f"  {k}: {v}")
print("\nNew predictions (beyond DEV):")
for p in new_predictions:
    print(f"  - {p}")
print("-" * 72)
print("STATUS (W4):")
for line in status.split(".  "):
    print("  " + line.strip())

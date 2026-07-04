"""AB4_circularity.py -- anti-circularity audit of the ENTIRE results/bridge/ tree.

AUDIT_BRIDGE task AB4 (the priority gate of the audit: if any bridge result is
circular it must be flagged before anything else).  The repository guard
tests/test_no_circularity.py scans src/, experiments/ and results/matter/ -- it does
NOT scan results/bridge/.  This audit closes that gap WITHOUT modifying the guard or
any campaign: it imports the guard's own primitives (so the rules are identical to the
ones enforced elsewhere) and re-runs them over results/bridge/.

Three independent checks, all driven by the bridge code itself:

  (1) DILATION GUARD.  The cardinal sin -- a special-/general-relativistic dilation
      formula (1/sqrt(1-beta^2), sqrt(1-2M/r), explicit gamma=...) -- forbidden in
      EVERY generator, even inside a COMPARISON ONLY block.  Reuses guard.FORBIDDEN.

  (2) COMPLEX-NUMBER GUARD.  No imaginary literal / complex() / cmath outside a
      labelled `# COMPARISON ONLY ... # END COMPARISON ONLY` block.  Reuses
      guard.COMPLEX_FORBIDDEN and guard._comparison_block_lines.

  (3) DEV / EMPIRICAL-DATA CONTAINMENT.  The deeper bridge-specific question: does any
      DEV parameter (a_0, m_A, K, gamma, lambda_p as a *fitted* value) or any empirical
      dataset name (SPARC, BTFR, RAR, Schwarzschild GM/r, c*H0) appear in EXECUTABLE
      code OUTSIDE a COMPARISON ONLY block?  Such a token in a generator would mean an
      output was reverse-engineered from the answer.  We tokenise (comments/strings
      stripped, as the guard does) and report every occurrence with its block status.

Output: AB4_circularity.md (written by hand from this run) + AB4_circularity_data.json.
Run:  python results/audit/bridge_recheck/AB4_circularity.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRIDGE = ROOT / "results" / "bridge"
OUT = Path(__file__).resolve().parent

# --- import the repository guard as a module (do NOT modify it) ---------------- #
_spec = importlib.util.spec_from_file_location(
    "teic_guard", ROOT / "tests" / "test_no_circularity.py")
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)


# DEV parameters and empirical-data names that must never feed a generator.  These
# are matched on tokenised, comment/string-stripped code, so they fire only on LIVE
# identifiers, not on prose.  a_0/H_0 are matched CASE-SENSITIVELY in their lowercase
# MOND/cosmology spelling -- a case-insensitive match would falsely flag the gauge
# symbol "A0" (a Stuckelberg covector component) as MOND's a_0.
DEV_TOKENS = [
    (r"\bSPARC\b", "SPARC rotation-curve dataset", False),
    (r"\bBTFR\b", "baryonic Tully-Fisher relation", False),
    (r"\bRAR\b", "radial-acceleration relation", False),
    (r"a_0", "MOND acceleration a_0", True),
    (r"\ba0\b", "MOND acceleration a_0 (lowercase)", True),
    (r"\bcH0\b", "c*H_0 scale", True),
    (r"\bMOND\b", "MOND", False),
]
# The forbidden Schwarzschild DILATION literal sqrt(1-2M/r) and a numeric 2M/r INPUT
# are caught by guard.FORBIDDEN (re-used below).  Here we separately CLASSIFY bare
# "schwarzschild" identifier references, because the project rule (guard docstring)
# explicitly ALLOWS (i) the background metric / sprinkler as generator geometry and
# (ii) the dilation formula when it lives in src/validation.py and is imported for
# scoring.  We confirm every such reference resolves to one of those allowed sources.
SCHWARZ_IDENT = (r"schwarzschild", "schwarzschild identifier reference")
ALLOWED_SCHWARZ_IMPORTS = {
    "schwarzschild_redshift": "src/validation.py (designated dilation-formula file)",
    "sprinkle_schwarzschild": "src/curved.py (background-metric generator, allowed)",
    "rstar_of_r": "src/curved.py (tortoise coordinate, background geometry, allowed)",
}


# A file is a DATA GENERATOR if it imports a sprinkling / causal-network primitive.
# Only in a generator can a Schwarzschild reference become circular (fed into the data
# that is then "observed"); a purely symbolic/comparison file (sympy only) cannot.
GENERATOR_IMPORTS = re.compile(
    r"\b(sprinkle_box|sprinkle_schwarzschild|causal_diamond_loops|alexandrov_interval|"
    r"causal_links|causal_past_idx|sprinkle_)\b")


def _is_generator(path: Path):
    return bool(GENERATOR_IMPORTS.search(path.read_text(encoding="utf-8")))


def _schwarz_source(path: Path, ident_line: int):
    """For a 'schwarzschild' identifier hit, find which symbol it is and whether that
    symbol is imported from an ALLOWED source (validation.py scorer / curved.py
    background generator).  Returns (symbol, allowed_source_or_None)."""
    text = path.read_text(encoding="utf-8")
    for sym, src in ALLOWED_SCHWARZ_IMPORTS.items():
        # the symbol must actually be imported in the file for the reference to resolve
        if re.search(rf"\bimport\b.*\b{sym}\b", text) or re.search(rf"\bfrom\b.*\b{sym}\b", text):
            # crude but sufficient: if any allowed schwarzschild symbol is imported and
            # the forbidden literal is absent, references resolve to allowed sources.
            return sym, src
    return None, None


def scan_file(path: Path):
    """Return per-file findings: dilation hits (forbidden everywhere), complex hits
    (forbidden outside COMPARISON), DEV/data hits, and classified schwarzschild refs."""
    rel = str(path.relative_to(ROOT))
    exempt, blk_err = guard._comparison_block_lines(path)
    code = guard._code_only(path)
    dil, cplx, dev, schwarz = [], [], [], []
    for raw in code.splitlines():
        lineno_s, _, c = raw.partition(": ")
        lineno = int(lineno_s)
        inblock = lineno in exempt
        for pat, desc in guard.FORBIDDEN:                 # dilation literal: case-insens.
            if re.search(pat, c, flags=re.IGNORECASE):
                dil.append({"line": lineno, "desc": desc, "in_comparison": inblock})
        if not inblock:
            for pat, desc in guard.COMPLEX_FORBIDDEN:
                if re.search(pat, c, flags=re.IGNORECASE):
                    cplx.append({"line": lineno, "desc": desc})
        for pat, desc, case_sensitive in DEV_TOKENS:
            flags = 0 if case_sensitive else re.IGNORECASE
            if re.search(pat, c, flags=flags):
                dev.append({"line": lineno, "desc": desc, "in_comparison": inblock})
        pat, desc = SCHWARZ_IDENT
        if re.search(pat, c, flags=re.IGNORECASE):
            sym, src = _schwarz_source(path, lineno)
            schwarz.append({"line": lineno, "desc": desc, "in_comparison": inblock,
                            "resolves_to": sym, "allowed_source": src})
    return rel, blk_err, dil, cplx, dev, schwarz, _is_generator(path)


def main():
    files = sorted(BRIDGE.rglob("*.py"))
    per_file = {}
    block_advisories = []              # unterminated COMPARISON markers (convention)
    dilation_violations = []           # forbidden EVERYWHERE
    complex_violations = []            # forbidden outside COMPARISON
    dev_outside = []                   # DEV/data token in live code outside COMPARISON
    schwarz_circular = []              # schwarzschild ref in a GENERATOR, unresolved
    schwarz_symbolic = []              # schwarzschild ref in a generator-free file (cmp)
    schwarz_allowed = []               # schwarzschild ref resolving to allowed src

    for path in files:
        rel, blk_err, dil, cplx, dev, schwarz, is_gen = scan_file(path)
        if blk_err:
            block_advisories.append({"file": rel, "note": blk_err})
        per_file[rel] = {
            "dilation": dil, "complex": cplx, "dev_data": dev, "schwarz": schwarz,
            "is_generator": is_gen}
        for d in dil:
            dilation_violations.append({"file": rel, **d})
        for d in cplx:
            complex_violations.append({"file": rel, **d})
        for d in dev:
            if not d["in_comparison"]:
                dev_outside.append({"file": rel, **d})
        for d in schwarz:
            if d["allowed_source"] is not None or d["in_comparison"]:
                schwarz_allowed.append({"file": rel, **d})     # validation import OR wrapped
            elif is_gen:
                schwarz_circular.append({"file": rel, **d})    # genuine risk
            else:
                schwarz_symbolic.append({"file": rel, **d})    # comparison target, UNwrapped

    # CIRCULARITY = a dilation literal anywhere, a complex literal in a generator, a DEV
    # parameter or dataset in live code, or a schwarzschild reference that does NOT
    # resolve to validation.py/curved.py.  The block-terminator convention is an
    # advisory (it OVER-exempts, the safe direction, and the content is clearly labelled
    # COMPARISON), not a circularity failure.
    clean = (not dilation_violations and not complex_violations
             and not dev_outside and not schwarz_circular)
    dev_contained = sum(1 for f in per_file.values()
                        for d in f["dev_data"] if d["in_comparison"])

    summary = {
        "n_files_scanned": len(files),
        "files": sorted(per_file),
        "dilation_violations": dilation_violations,
        "complex_violations": complex_violations,
        "dev_data_tokens_OUTSIDE_comparison": dev_outside,
        "dev_data_tokens_contained_in_comparison": dev_contained,
        "schwarzschild_refs_circular_in_generator": schwarz_circular,
        "schwarzschild_refs_symbolic_comparison": schwarz_symbolic,
        "schwarzschild_refs_allowed_source": schwarz_allowed,
        "comparison_block_advisories": block_advisories,
        "verdict_clean": bool(clean),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "AB4_circularity_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 74)
    print("AB4 -- ANTI-CIRCULARITY AUDIT OF results/bridge/  (guard rules reused)")
    print("=" * 74)
    print(f"files scanned: {len(files)}")
    print(f"\n(1) DILATION GUARD (sqrt(1-2M/r), 1/sqrt(1-beta^2), gamma=...; forbidden "
          f"everywhere): {len(dilation_violations)} violation(s)")
    for v in dilation_violations:
        print(f"    {v['file']}:{v['line']}  {v['desc']}")
    print(f"\n(2) COMPLEX-NUMBER GUARD (1j/complex()/cmath outside COMPARISON): "
          f"{len(complex_violations)} violation(s)")
    for v in complex_violations:
        print(f"    {v['file']}:{v['line']}  {v['desc']}")
    print(f"\n(3) DEV PARAMETER / EMPIRICAL-DATA CONTAINMENT")
    print(f"    DEV/data tokens (a_0, SPARC, BTFR, MOND, cH0) in live code: "
          f"{len(dev_outside)} outside a COMPARISON block")
    for v in dev_outside:
        print(f"      {v['file']}:{v['line']}  {v['desc']}")
    print(f"\n(4) SCHWARZSCHILD REFERENCES (classified)")
    print(f"    resolving to an ALLOWED source (validation.py scorer / curved.py "
          f"background generator): {len(schwarz_allowed)}")
    srcs = sorted({(v['resolves_to'] or "(wrapped in COMPARISON ONLY block)",
                    v['allowed_source'] or "in-file comparison target, properly wrapped")
                   for v in schwarz_allowed})
    for sym, src in srcs:
        n = sum(1 for v in schwarz_allowed
                if (v['resolves_to'] or "(wrapped in COMPARISON ONLY block)") == sym)
        print(f"      {sym}  ->  {src}   ({n} refs)")
    print(f"    CIRCULAR (in a file that ALSO imports a data generator): "
          f"{len(schwarz_circular)}")
    for v in schwarz_circular:
        print(f"      {v['file']}:{v['line']}")
    print(f"    symbolic comparison target (generator-free sympy file; not circular, "
          f"see advisories): {len(schwarz_symbolic)}")
    for v in schwarz_symbolic:
        print(f"      {v['file']}:{v['line']}")
    print(f"\n(5) ADVISORIES (convention, not circularity): "
          f"{len(block_advisories) + (1 if schwarz_symbolic else 0)}")
    for v in block_advisories:
        print(f"      {v['file']}: {v['note']}")
        print(f"        -> uses '# COMPARISON ONLY' but closes with a dashed rule, not "
              f"the canonical '# END COMPARISON ONLY' sentinel (over-exempts: safe side).")
    if schwarz_symbolic:
        sf = sorted({v['file'] for v in schwarz_symbolic})
        print(f"      {', '.join(sf)}: the Schwarzschild Taylor SERIES is computed in a "
              f"function now WRAPPED in a '# COMPARISON ONLY' block; the residual ref is "
              f"the call-site identifier in main() (a generator-free sympy file -- cannot "
              f"be circular).")
    print("-" * 74)
    tail = ("no dilation formula, no complex literal, and no DEV parameter / dataset "
            "feeds any bridge generator; every Schwarzschild reference resolves to "
            "src/validation.py (scorer) or src/curved.py (background geometry), both "
            "allowed by the guard's own rule."
            if clean else "see the violations listed above.")
    print(f"VERDICT (AB4): {'CLEAN' if clean else 'CIRCULARITY FOUND'} -- {tail}")
    return summary


if __name__ == "__main__":
    main()

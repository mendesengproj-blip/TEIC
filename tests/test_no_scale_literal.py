"""Scale-literal guard (campaign A1/C1, Fase 2).

Companion to ``test_no_circularity.py``.  That guard bans a *dilation formula*
smuggled into a generator.  This one bans a *physical scale* smuggled into a
generator: the program's thesis is "form emerges, scale is external", so a float
literal that coincides with c, G, hbar, a_0, m_e, M_Planck (or their usual powers
/ combinations in natural units) sitting inside data-generating code is the
scale-analogue of the cardinal sin -- a number that would let the code "derive"
a scale it was actually handed.

For every numeric literal in generator code (the same SCAN_DIRS the
anti-circularity guard uses) this module reports any literal v with
    |v / X - 1| < TOL          (TOL = 1%)
for X in the constant table below, together with the ENCLOSING FUNCTION so the
dependency is explicit (criterion ii of the A1 pre-registration).

Scope/limitation (pre-registered, honest): this catches the realistic failure
mode -- an accidental or convenience injection of an SI / natural-unit constant
-- exactly as the dilation guard catches the specific Lorentz/Schwarzschild
forms, not every conceivable smuggling.  Predictable false positives (alpha and e
as dimensionless couplings, Bohr radius vs G in the same decade) are reported and
explicitly CLASSIFIED in JUSTIFIED below, never silently suppressed.

Run:  python tests/test_no_scale_literal.py     (writes the verbatim report)
      pytest tests/test_no_scale_literal.py      (asserts no UNJUSTIFIED literal)
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_no_circularity import ALLOWED, ROOT, SCAN_DIRS  # reuse the audited scope

TOL = 0.01  # 1% relative match (pre-registered)

# Base physical constants in SI (and common natural-unit values).  See
# docs/campaigns/GUARDA_A1/PRE_REGISTRO.md sec.4.
_BASE = {
    "c": 2.99792458e8,
    "G": 6.67430e-11,
    "hbar": 1.054571817e-34,
    "h": 6.62607015e-34,
    "k_B": 1.380649e-23,
    "e_charge": 1.602176634e-19,
    "m_e": 9.1093837015e-31,
    "m_e[eV]": 510998.95,
    "a0_MOND": 1.2e-10,
    "a0_Bohr": 5.29177210903e-11,
    "M_Pl[kg]": 2.176434e-8,
    "M_Pl[GeV]": 1.220890e19,
    "M_Pl_red[GeV]": 2.435323e18,
    "alpha": 7.2973525693e-3,
    "l_Planck": 1.616255e-35,
    "t_Planck": 5.391247e-44,
    "hbar_c[J.m]": 3.16152677e-26,
    "hbar_c[MeV.fm]": 197.3269804,
}

# Bases for which integer/half-integer powers and reciprocals are physically usual.
_POWERED = {"c", "G", "hbar", "h", "e_charge", "m_e"}


def _build_table():
    """Expand the base table with usual powers/combinations (criterion ii)."""
    table = dict(_BASE)
    for name in _POWERED:
        x = _BASE[name]
        table[f"{name}^2"] = x * x
        table[f"{name}^3"] = x * x * x
        table[f"1/{name}"] = 1.0 / x
        table[f"1/{name}^2"] = 1.0 / (x * x)
        table[f"sqrt({name})"] = x ** 0.5
    return table


TABLE = _build_table()

# Known matches, classified by the A1 audit (campaign GUARDA_A1).  Each
# (filename, symbol) -> reason entry means "this match was read and is a declared
# EXTERNAL constant in a post-hoc comparison / unit-conversion / falsification
# layer, NOT a scale fed into a causal-network generator".  This is documented
# classification, not silent suppression: every entry was inspected (see
# docs/campaigns/GUARDA_A1/SYNTHESIS.md) and the verbatim report keeps listing it.
# A NEW unjustified match (not in this dict) fails the test -> triage as R-0
# (smuggled scale: downgrade + re-audit the result) or add here with a note.
JUSTIFIED_NOTES: dict[tuple[str, str], str] = {
    # comparison-only block, explicitly "never used by the generator"
    ("A2_saturation_scale.py", "a0_MOND"): "COMPARISON ONLY block; SPARC scale point",
    # EHT black-hole-shadow falsification test (compares TEIC to cited EHT data)
    ("F_EHT.py", "G"): "SI constant for EHT falsification comparison",
    ("F_EHT.py", "c"): "SI constant for EHT falsification comparison",
    ("F_EHT.py", "l_Planck"): "SI constant for EHT falsification comparison",
    ("F_EHT.py", "a0_MOND"): "Milgrom scale, annotated 'MEASURED ... not derived'",
    # CMB relic-density falsification (Parker bound), 'external numbers, no fitting'
    ("F_CMB.py", "M_Pl[kg]"): "Planck mass for relic-density comparison vs Parker bound",
    ("F_CMB.py", "l_Planck"): "Planck length for relic-density comparison",
    # FM1 (S8) CLASS/CAMB comparison cosmology (MORTO); a0 'SPARC-calibrated, not a CMB fit'
    ("FM1_2_class_impl.py", "G"): "SI constant for CAMB/CLASS comparison cosmology",
    ("FM1_2_class_impl.py", "c"): "SI constant for CAMB/CLASS comparison cosmology",
    ("FM1_2_class_impl.py", "a0_MOND"): "SPARC-calibrated, annotated 'NOT a CMB fit'",
    # FM4 wave-condensate comparison cosmology
    ("fm4_core.py", "c"): "SI constant for FM4 comparison cosmology",
    # c6_scales: 'declared external constants (SI) ... not derived by TEIC'
    ("c6_scales.py", "hbar"): "declared EXTERNAL input, not derived by TEIC",
    ("c6_scales.py", "c"): "declared EXTERNAL input, not derived by TEIC",
    # FN3 relic density: 'standard cosmology fixed by the charter; nothing fit to CMB'
    ("fn3_core.py", "c"): "charter cosmology constant, nothing fit",
    ("fn3_core.py", "M_Pl[GeV]"): "non-reduced Planck mass, charter input",
    # FN4 wide-binary MOND screening: A0 'CHARTER -- DO NOT FIT'
    ("fn4_core.py", "G"): "SI constant for wide-binary dynamics comparison",
    ("fn4_core.py", "a0_MOND"): "Milgrom acceleration, annotated 'CHARTER -- DO NOT FIT'",
    # HQ3 NANOGrav: 'standard cosmology fixed by the charter, nothing fit'
    ("hq3_core.py", "c"): "charter cosmology constant, nothing fit",
    ("hq3_core.py", "G"): "charter cosmology constant, nothing fit",
    ("hq3_core.py", "1/e_charge"): "EV_PER_JOULE = 6.241e18 eV/J (= 1/e numerically); unit conversion",
    # baryon-quant: HBARC=197.327 MeV.fm is the standard lattice->fm conversion
    ("bq_core.py", "hbar_c[MeV.fm]"): "hbar*c in MeV.fm; converts lattice r^2 to fm for proton-radius comparison",
}
JUSTIFIED = set(JUSTIFIED_NOTES)


def _func_ranges(tree: ast.AST):
    """List of (name, start_line, end_line) for every def/async-def in the tree."""
    ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            ranges.append((node.name, node.lineno, end))
    return ranges


def _enclosing(ranges, lineno):
    """Innermost function whose span contains lineno, else '<module>'."""
    best = None
    for name, start, end in ranges:
        if start <= lineno <= end:
            if best is None or (start, -end) > (best[1], -best[2]):
                best = (name, start, end)
    return best[0] if best else "<module>"


def _numeric_literals(tree: ast.AST):
    """Yield (lineno, value) for every real numeric literal (int/float, not bool,
    not complex -- complex is the other guard's job)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            v = node.value
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                yield node.lineno, float(v)


def _best_match(value):
    """Closest constant within TOL, or None.  Returns (symbol, rel_err)."""
    av = abs(value)
    if av == 0.0:
        return None
    best = None
    for sym, ref in TABLE.items():
        if ref == 0.0:
            continue
        rel = abs(av / abs(ref) - 1.0)
        if rel < TOL and (best is None or rel < best[1]):
            best = (sym, rel)
    return best


def scan():
    """Return list of candidate rows: (relpath, lineno, value, symbol, rel_err, func)."""
    rows = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for path in d.rglob("*.py"):
            if path in ALLOWED:
                continue
            try:
                src = path.read_text(encoding="utf-8-sig")  # tolerate a BOM
                tree = ast.parse(src)
            except (SyntaxError, UnicodeDecodeError) as exc:
                rows.append((path.relative_to(ROOT), "-", float("nan"), "PARSE-ERROR",
                             0.0, str(exc)))
                continue
            ranges = _func_ranges(tree)
            for lineno, value in _numeric_literals(tree):
                m = _best_match(value)
                if m:
                    sym, rel = m
                    rows.append((path.relative_to(ROOT), lineno, value, sym, rel,
                                 _enclosing(ranges, lineno)))
    return rows


def _unjustified(rows):
    out = []
    for rel, lineno, value, sym, err, func in rows:
        if sym == "PARSE-ERROR":
            out.append((rel, lineno, value, sym, err, func))
            continue
        if (Path(rel).name, sym) in JUSTIFIED:
            continue
        out.append((rel, lineno, value, sym, err, func))
    return out


def _format_report(rows):
    lines = []
    lines.append("# SCALE-LITERAL REPORT (campaign A1/C1)\n")
    lines.append(f"Scanned dirs: {', '.join(str(d.relative_to(ROOT)) for d in SCAN_DIRS)}")
    lines.append(f"Tolerance: {TOL:.0%} relative.  Constant table: {len(TABLE)} targets.\n")
    if not rows:
        lines.append("**RESULT: zero literals within 1% of any physical scale.** "
                     "No scale smuggled into any generator (criterion iii satisfied).")
        return "\n".join(lines)
    bad = _unjustified(rows)
    verdict = ("**R-0 NOT triggered.** Every candidate is a declared-external constant "
               "in a comparison / unit-conversion / falsification layer (classified below); "
               "none feeds a causal-network generator."
               if not bad else
               f"**R-0 TRIGGERED: {len(bad)} unjustified literal(s)** -- downgrade + re-audit "
               "the affected result(s).")
    lines.append(f"{len(rows)} candidate literal(s) found. {verdict}\n")
    lines.append("| file | line | literal | matches | rel.err | function | status |")
    lines.append("|---|---|---|---|---|---|---|")
    for rel, lineno, value, sym, err, func in rows:
        if sym == "PARSE-ERROR":
            lines.append(f"| {rel} | {lineno} | — | PARSE-ERROR | — | {func} | ⚠ parse |")
            continue
        errs = f"{err:.2%}" if isinstance(err, float) else "n/a"
        note = JUSTIFIED_NOTES.get((Path(rel).name, sym))
        status = f"justified: {note}" if note else "**UNJUSTIFIED → R-0**"
        lines.append(f"| `{rel}` | {lineno} | `{value:g}` | {sym} | {errs} | `{func}` | {status} |")
    return "\n".join(lines)


def test_no_scale_literal():
    """pytest entry point: no UNJUSTIFIED scale literal in any generator."""
    rows = scan()
    bad = _unjustified(rows)
    assert not bad, (
        "scale-literal guard found unjustified physical-scale literal(s):\n"
        + "\n".join(f"  {r}:{ln}  {v:g} ~ {sym} ({e}) in {fn}"
                    for r, ln, v, sym, e, fn in bad)
        + "\n\nEither it is a smuggled scale (R-0: downgrade + re-audit the result), "
          "or a classified coincidence (add (filename, symbol) to JUSTIFIED with a note)."
    )


def main():
    rows = scan()
    report = _format_report(rows)
    print(report)
    out = ROOT / "docs" / "campaigns" / "GUARDA_A1" / "SCALE_LITERAL_REPORT.md"
    out.write_text(report + "\n", encoding="utf-8")
    print(f"\n[report written to {out.relative_to(ROOT)}]")
    return 1 if _unjustified(rows) else 0


if __name__ == "__main__":
    sys.exit(main())

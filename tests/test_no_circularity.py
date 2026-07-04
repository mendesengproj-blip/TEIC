"""Anti-circularity guard (PROMPT.md sec.2-3).

The cardinal sin of this project was inserting a relativistic dilation formula into
the code that GENERATES causal-network data and then "observing" it in the output.
This test fails if any special-/general-relativistic dilation expression appears
outside validation.py.

What is forbidden in generator code:
  * Lorentz factor / proper-time ratio:  1/sqrt(1-beta^2), sqrt(1-beta^2), gamma=...
  * Gravitational redshift:               sqrt(1 - 2 M / r)   (the SQUARE ROOT of g_tt)

What is explicitly ALLOWED in generator code (it is background geometry, not a
dilation applied to an estimator):
  * the metric / volume element itself, e.g. (1 - 2 M / r) WITHOUT a square root,
    and the conformal factor of constant-curvature space.

REINFORCED RULE for e6 (interference / phase, addendum module e6):
  * No complex numbers in any generator: no imaginary literal (1j), no complex(),
    no cmath.  Injecting e^{ikL} would be the "gamma by hand" error repeated for
    quantum phase.  The ONLY exception is code inside a block explicitly delimited by
        # COMPARISON ONLY -- postulated QM phase, not derived
        ...
        # END COMPARISON ONLY
    Such a block may use complex numbers solely to compare against the postulated
    quantum prediction; it must never feed the causal-network generator.  (The SR/GR
    dilation patterns remain forbidden even inside such a block.)

Run:  python tests/test_no_circularity.py     (exit code 0 = clean)
"""

from __future__ import annotations

import re
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files that ARE allowed to contain relativistic formulas.
ALLOWED = {ROOT / "src" / "validation.py"}

# Generator code that must stay clean.  EXTENDED under campaign A1/C1 (Fase 2)
# from the original {src, experiments, results/matter, results/bridge,
# results/tier3, results/dev_from_teic} to cover EVERY data-generating module in
# the repository -- the whole of results/, every campaign generator under
# docs/campaigns/ (incl. sr_teic_core.py), experiments/, and src/.  The audit
# question of A1 was precisely whether a dilation formula or an undeclared complex
# literal hid in a generator that the old, narrower scan never looked at; pointing
# SCAN_DIRS at the full tree closes that gap and the guard stays GREEN
# (r5_group_core.py's Gell-Mann generators carry the SU(3) GROUP-DEF COMPLEX
# marker; audit tools under results/audit hold the forbidden patterns only inside
# string/regex literals, which _code_only strips).
SCAN_DIRS = [ROOT / "src", ROOT / "experiments", ROOT / "results",
             ROOT / "docs" / "campaigns"]

# Dilation formulas (forbidden everywhere except validation.py, even in a
# COMPARISON ONLY block).
FORBIDDEN = [
    (r"1\s*/\s*sqrt\s*\(\s*1\s*-\s*beta", "Lorentz factor 1/sqrt(1-beta^2)"),
    (r"sqrt\s*\(\s*1\s*-\s*beta", "proper-time ratio sqrt(1-beta^2)"),
    (r"sqrt\s*\(\s*1\s*-\s*v\s*\*\s*\*\s*2", "proper-time ratio sqrt(1-v**2)"),
    (r"\bgamma\s*=\s*1\s*/\s*sqrt", "explicit Lorentz gamma assignment"),
    (r"sqrt\s*\(\s*1\s*-\s*2\s*\*?\s*[GM]", "Schwarzschild redshift sqrt(1-2M/r)"),
]

# Complex numbers (forbidden in generator code; allowed ONLY inside a labelled
# COMPARISON ONLY block, where they compare against postulated quantum phase, OR
# inside a labelled SU(3) GROUP-DEF COMPLEX block -- see below).
COMPLEX_FORBIDDEN = [
    (r"\b\d+\.?\d*j\b", "imaginary literal (complex number)"),
    (r"\b\.\d+j\b", "imaginary literal (complex number)"),
    (r"\bcomplex\s*\(", "complex() constructor"),
    (r"\bcmath\b", "cmath module"),
]

# Comment markers delimiting an allowed complex-number comparison block.
CMP_START = "COMPARISON ONLY"
CMP_END = "END COMPARISON ONLY"

# PRINCIPLED EXCEPTION for FL1_SU3_FOUNDATION (the SU(3) / colour sector).
# SU(2) was carried by unit quaternions (a REAL division algebra, S^3), so the
# matter sector needed no complex literals.  SU(3) has no such shortcut: the
# faithful minimal carrier is genuinely complex 3x3 matrices (the Gell-Mann
# generators), the Lie-algebra->group exponential exp(iX), and the structure
# constants f = (1/4i)Tr([l_a,l_b]l_c).  These complex numbers ARE the definition
# of the gauge group SU(3) -- they are mathematics, not a smuggled e^{ikL} phase or
# dilation factor.  Inside a block delimited by
#       # SU(3) GROUP-DEF COMPLEX
#       ...
#       # END SU(3) GROUP-DEF COMPLEX
# imaginary literals are therefore allowed.  STRICTLY LIMITED: the exception covers
# ONLY the group's structural linear algebra; it does NOT relax the dilation
# patterns (FORBIDDEN above stay banned EVERYWHERE, including inside these blocks
# and inside su3_core.py), and complex literals OUTSIDE such a block -- anywhere,
# su3_core.py included -- remain violations, so an injected phase cannot hide.
SU3_START = "SU(3) GROUP-DEF COMPLEX"
SU3_END = "END SU(3) GROUP-DEF COMPLEX"


def _code_only(path: Path) -> str:
    """Return source with comments and string literals (incl. docstrings) removed.

    We test EXECUTABLE code: a relativistic formula in a docstring that explains the
    anti-circularity rule is fine; one in a live expression is not.  Line numbers are
    preserved by mapping each surviving token back to its line.
    """
    lines = {}
    with open(path, "rb") as f:
        try:
            toks = list(tokenize.tokenize(f.readline))
        except tokenize.TokenError:
            toks = []
    # Python 3.12+ splits f-strings into FSTRING_START/MIDDLE/END; the MIDDLE pieces are
    # literal text (like STRING) and must be skipped too -- the {expr} parts remain normal
    # tokens and are still scanned, so circularity detection is unaffected.  getattr keeps
    # this working on <3.12 where those token types do not exist.
    skip = {tokenize.COMMENT, tokenize.STRING, tokenize.NL, tokenize.NEWLINE,
            tokenize.ENCODING, tokenize.INDENT, tokenize.DEDENT}
    for _name in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
        if hasattr(tokenize, _name):
            skip.add(getattr(tokenize, _name))
    for tok in toks:
        if tok.type in skip:
            continue
        lines.setdefault(tok.start[0], []).append(tok.string)
    text = "\n".join(f"{ln}: {' '.join(parts)}" for ln, parts in sorted(lines.items()))
    # strip module prefixes so np.sqrt and sqrt match the same pattern
    return re.sub(r"\b(np|numpy|math|sp|sympy)\.", "", text)


def _marker_block_lines(path: Path, start_marker: str, end_marker: str):
    """Line numbers inside ``# <start_marker>`` ... ``# <end_marker>`` blocks.

    Returns (exempt_lineset, error_or_None).  An unterminated block is an error
    (so a stray marker cannot silently exempt the rest of a file).  Used for both
    the COMPARISON ONLY blocks and the SU(3) GROUP-DEF COMPLEX blocks.
    """
    start_u, end_u = start_marker.upper(), end_marker.upper()
    exempt = set()
    inside = False
    start = None
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        s = line.strip()
        # A marker must be a standalone comment line beginning with the sentinel,
        # so that prose / inline annotations are not markers.
        content = s.lstrip("#").strip().upper() if s.startswith("#") else ""
        # check the END marker first: SU3_END starts with "END ..." and the START
        # sentinel is a substring of it, so START's prefix test would misfire.
        if content.startswith(end_u):
            if inside:
                exempt.add(i)
                inside = False
                start = None
            continue
        if content.startswith(start_u):
            inside, start = True, i
            exempt.add(i)
            continue
        if inside:
            exempt.add(i)
    if inside:
        return exempt, f"unterminated '{start_marker}' block opened at line {start}"
    return exempt, None


def _comparison_block_lines(path: Path):
    """COMPARISON ONLY exempt lines (postulated-QM-phase comparison blocks)."""
    return _marker_block_lines(path, CMP_START, CMP_END)


def _su3_block_lines(path: Path):
    """SU(3) GROUP-DEF COMPLEX exempt lines (gauge-group definition; FL1)."""
    return _marker_block_lines(path, SU3_START, SU3_END)


def scan():
    violations = []
    for d in SCAN_DIRS:
        for path in d.rglob("*.py"):
            if path in ALLOWED:
                continue
            rel = path.relative_to(ROOT)
            exempt, err = _comparison_block_lines(path)
            if err:
                violations.append((rel, "-", err))
            su3_exempt, su3_err = _su3_block_lines(path)   # FL1 gauge-group definition
            if su3_err:
                violations.append((rel, "-", su3_err))
            complex_exempt = exempt | su3_exempt
            for raw_line in _code_only(path).splitlines():
                lineno_s, _, code = raw_line.partition(": ")
                lineno = int(lineno_s)
                for pat, desc in FORBIDDEN:           # dilation: forbidden everywhere,
                    if re.search(pat, code, flags=re.IGNORECASE):   # incl. SU(3) blocks
                        violations.append((rel, lineno_s, desc))
                if lineno not in complex_exempt:      # complex: ok only in cmp / SU(3)
                    for pat, desc in COMPLEX_FORBIDDEN:
                        if re.search(pat, code, flags=re.IGNORECASE):
                            violations.append((rel, lineno_s, desc))
    return violations


def test_no_circularity():
    """pytest entry point: no dilation formula / undeclared complex in any generator."""
    violations = scan()
    assert not violations, "anti-circularity guard found violations:\n" + "\n".join(
        f"  {p}:{ln}  -> {d}" for p, ln, d in violations)


def main():
    violations = scan()
    if violations:
        print("ANTI-CIRCULARITY TEST: FAILED")
        for path, line, desc in violations:
            print(f"  {path}:{line}  -> {desc}")
        return 1
    print("ANTI-CIRCULARITY TEST: PASSED (no dilation formula in generator code)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Inventory of tests/: per file the test functions (and classes) with the first docstring line, the line counts, and the words that mark a declared world or a family name."""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
TESTS = ROOT / "tests"
MARK = re.compile(
    r"families|family|FamilyRule|\"name\"|'name'|bodies|packets|node_detectors|identity|registry|"
    r"row_of|records_of|wronskian|\.quanta\b|motion_volume|world\.seed|circle|lift|point \d|"
    r"electron|proton|muon|neutrino|positron|photon|quark|baryon|slits|atom|bell|ghz|LATTICE|interval",
    re.I,
)
total_lines = total_funcs = 0
for path in sorted(TESTS.glob("*.py")):
    src = path.read_text(errors="replace")
    lines = src.splitlines()
    total_lines += len(lines)
    tree = ast.parse(src)
    funcs = []
    classes = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes += 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            doc = ast.get_docstring(node) or ""
            first = doc.strip().split("\n")[0][:160]
            end = node.end_lineno or node.lineno
            body = "\n".join(lines[node.lineno - 1 : end])
            marks = sorted({m.group(0).lower() for m in MARK.finditer(body)})
            funcs.append((node.name, node.lineno, end, first, marks))
    total_funcs += len(funcs)
    marks_file = sorted({m.group(0).lower() for m in MARK.finditer(src)})
    print(f"## {path.relative_to(ROOT)}: {len(lines)} lines, {len(funcs)} test functions, {classes} classes; marks {marks_file}")
    for name, a, b, first, marks in funcs:
        print(f"  - {name} [{a}-{b}, {b - a + 1} lines] marks={marks}\n      {first}")
print(f"TOTAL tests: {total_lines} lines, {total_funcs} test functions")

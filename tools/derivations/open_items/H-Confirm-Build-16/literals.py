"""Integer literals beyond 0, 1 and -1 (and float literals) per file under src/event_universe, by ast; docstrings excluded by construction."""
import ast, sys
from pathlib import Path
def count(path):
    tree = ast.parse(path.read_text())
    ints = floats = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant):
            if isinstance(n.value, bool): continue
            if isinstance(n.value, int) and n.value not in (0, 1, -1): ints += 1
            if isinstance(n.value, float): floats += 1
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) and n.operand.value == 1: ints -= 0
    return ints, floats
roots = [Path(p) for p in sys.argv[1:3]]
files = sorted({f.relative_to(r) for r in roots for f in r.rglob("*.py")})
up = []
for f in files:
    c = [count(r / f) if (r / f).exists() else None for r in roots]
    a, b = c
    tag = "" if a == b else ("NEW" if a is None else ("GONE" if b is None else ("UP" if b[0] > a[0] else "down")))
    if tag == "UP": up.append(str(f))
    print(f"{str(f):48s} parent {str(a):12s} build {str(b):12s} {tag}")
print("UP:", up)

"""Integer literals beyond 0, 1, -1 and float literals by file, two src trees compared (ast)."""
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
    # -1 as UnaryOp(USub, Constant(1)) counted above as 1 -> excluded; fine
    return ints, floats
a, b = Path(sys.argv[1]), Path(sys.argv[2])
files = sorted({p.relative_to(a) for p in a.rglob('*.py')} | {p.relative_to(b) for p in b.rglob('*.py')})
up = 0
for rel in files:
    pa, pb = a / rel, b / rel
    ca = count(pa) if pa.exists() else (None, None)
    cb = count(pb) if pb.exists() else (None, None)
    flag = ''
    if ca[0] is not None and cb[0] is not None and cb[0] > ca[0]: flag = ' UP'; up += 1
    if ca != cb or 'interval' in str(rel): print(f"{rel}: parent ints {ca[0]} floats {ca[1]} -> build ints {cb[0]} floats {cb[1]}{flag}")
print("files up:", up)

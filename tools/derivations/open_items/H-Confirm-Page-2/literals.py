"""Count the integer literals beyond 0, 1 and -1 in a Python source read on stdin; print count, then each site: line, value, the source line."""
import ast, sys
src = sys.stdin.read(); tree = ast.parse(src); lines = src.splitlines()
neg = {id(n.operand) for n in ast.walk(tree) if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant)}
hits = []
for n in ast.walk(tree):
    if isinstance(n, ast.Constant) and type(n.value) is int:
        v = -n.value if id(n) in neg else n.value
        if v not in (0, 1, -1):
            hits.append((n.lineno, v, lines[n.lineno - 1].strip()[:110]))
print(len(hits))
for h in sorted(hits): print(*h, sep="\t")

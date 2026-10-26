"""Integer literals beyond 0, 1, -1 by file under a src/event_universe tree (ast; a unary minus folded). Usage: literals.py <src>"""
import ast, sys, pathlib
root = pathlib.Path(sys.argv[1]) / "event_universe"
total = 0
for p in sorted(root.rglob("*.py")):
    tree = ast.parse(p.read_text())
    found = []
    for n in ast.walk(tree):
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) and type(n.operand.value) is int:
            v = -n.operand.value
            if v not in (0, 1, -1):
                found.append((n.lineno, v))
        elif isinstance(n, ast.Constant) and type(n.value) is int and not isinstance(n.value, bool):
            if n.value not in (0, 1, -1):
                found.append((n.lineno, n.value))
    total += len(found)
    print(p.relative_to(root), len(found), sorted(found))
print("TOTAL", total)

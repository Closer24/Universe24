"""Integer literal sites beyond 0, 1 and -1 per file under src/event_universe (ast.Constant int, bool excluded, a negated 1 excluded); floats counted apart."""
import ast, sys, pathlib
root = pathlib.Path(sys.argv[1])
full = len(sys.argv) > 2
total = 0
for p in sorted(root.rglob("*.py")):
    tree = ast.parse(p.read_text())
    sites, floats = [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) and n.operand.value == 1:
            n.operand.skip = True
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and not isinstance(n.value, bool):
            if isinstance(n.value, float):
                floats.append((n.lineno, n.value))
            elif isinstance(n.value, int) and n.value not in (0, 1) and not getattr(n, "skip", False):
                sites.append((n.lineno, n.col_offset, n.value))
    total += len(sites)
    rel = str(p.relative_to(root))
    print(f"{rel} {len(sites)} floats {len(floats)}")
    if full:
        for ln, col, v in sites:
            print(f"   {rel}:{ln}:{col} {v}")
print("TOTAL", total)

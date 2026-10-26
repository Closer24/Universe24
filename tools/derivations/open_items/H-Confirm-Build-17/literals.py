"""Count integer constants beyond 0, 1, -1 in every .py under a src root with ast; floats and complex counted apart. Usage: python literals.py <src_root> ; prints file, count, the sorted literals, and lists each site."""
import ast, sys, pathlib
root = pathlib.Path(sys.argv[1]); verbose = len(sys.argv) > 2
total = 0; floats = 0
for f in sorted(root.rglob("*.py")):
    src = f.read_text(); tree = ast.parse(src); lines = src.splitlines()
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool):
            v = node.value
            if isinstance(v, (float, complex)):
                floats += 1; sites.append((node.lineno, repr(v), "FLOAT"))
            elif isinstance(v, int) and v not in (0, 1):
                sites.append((node.lineno, v, lines[node.lineno - 1].strip()))
    # a -1 is UnaryOp(USub, Constant 1): already excluded by the value check (1)
    rel = str(f.relative_to(root)); total += len(sites)
    print(f"{rel}\t{len(sites)}\t{sorted(set(s[1] for s in sites), key=str)}")
    if verbose:
        for ln, v, text in sorted(sites): print(f"    {rel}:{ln}\t{v}\t{text}")
print(f"TOTAL\t{total}\tfloats {floats}")

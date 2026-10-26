"""The literals in the added src lines of a range: every numeric constant outside a docstring on an added line, with file and line; the law allows 0, 1 and -1 alone."""
import ast, subprocess, sys
base, head, tree = sys.argv[1], sys.argv[2], sys.argv[3]
diff = subprocess.run(["git", "-C", tree, "diff", "-U0", base + ".." + head, "--", "src"], capture_output=True, text=True).stdout
added, path = {}, None
for line in diff.splitlines():
    if line.startswith("+++ b/"):
        path = line[6:]
    elif line.startswith("@@") and path:
        new = line.split(" ")[2]
        start, count = (new[1:].split(",") + ["1"])[:2]
        for n in range(int(start), int(start) + int(count)):
            added.setdefault(path, set()).add(n)
found = 0
for path, lines in sorted(added.items()):
    src = open(tree + "/" + path, encoding="ascii").read()
    tree_ = ast.parse(src)
    doc_lines = set()
    for node in ast.walk(tree_):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
            d = node.body[0]
            doc_lines.update(range(d.lineno, d.end_lineno + 1))
    for node in ast.walk(tree_):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            if node.lineno in lines and node.lineno not in doc_lines and node.value not in (0, 1):
                print(path, node.lineno, repr(node.value), src.splitlines()[node.lineno - 1].strip()[:100]); found += 1
            if isinstance(node.value, float):
                print("FLOAT", path, node.lineno)
print("added src lines:", sum(len(v) for v in added.values()), "literals beyond 0, 1 and -1:", found)

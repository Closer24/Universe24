"""Lines of a module: all, code (no blank, no docstring, no comment), docstring lines."""
import ast, sys
for path in sys.argv[1:]:
    src = open(path).read()
    tree = ast.parse(src)
    doc_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
            doc_lines.update(range(node.body[0].lineno, node.body[0].end_lineno + 1))
    lines = src.splitlines()
    code = sum(1 for k, ln in enumerate(lines, 1) if k not in doc_lines and ln.strip() and not ln.strip().startswith("#"))
    funcs = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    print(f"{path.split('/')[-1]}: {len(lines)} lines, {code} code lines, {len(doc_lines)} docstring lines, {funcs} functions")

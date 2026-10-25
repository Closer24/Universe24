"""Hand X2: the knots of logic, measured: per function the count of its decisions (if, elif, while, for, ternary,
boolean short-circuit, comprehension filter, try), the functions with the most, and the docstring lines against the
code lines of the tree (the reading's weight).

Usage: python knots.py <root> <subdir> <top>
"""
import ast
import sys
from pathlib import Path


def decisions(node):
    count = 0
    for inner in ast.walk(node):
        if isinstance(inner, ast.If | ast.While | ast.For | ast.IfExp | ast.Try):
            count += 1
        elif isinstance(inner, ast.BoolOp):
            count += len(inner.values) - 1
        elif isinstance(inner, ast.comprehension):
            count += len(inner.ifs)
    return count


def docstring_lines(tree):
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                total += expr.end_lineno - expr.lineno + 1
    return total


def main():
    root, sub, top = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    base = root / sub
    rows = []
    docs = code = blank = comments = 0
    lambdas = vectorize = 0
    for path in sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        docs += docstring_lines(tree)
        lines = text.splitlines()
        code += len(lines)
        blank += sum(1 for line in lines if not line.strip())
        comments += sum(1 for line in lines if line.strip().startswith("#"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Lambda):
                lambdas += 1
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "vectorize":
                vectorize += 1
        rel = str(path.relative_to(base))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                rows.append((decisions(node), rel, node.name, node.lineno, node.end_lineno))
    rows.sort(reverse=True)
    print(f"files {sub}: lines {code}, docstring lines {docs}, blank {blank}, comment lines {comments}, code lines {code - docs - blank - comments}")
    print(f"lambdas {lambdas}, np.vectorize calls {vectorize}, functions {len(rows)}, decisions in all {sum(r[0] for r in rows)}")
    print("the knots, by decisions:")
    for count, rel, name, start, end in rows[:top]:
        print(f"  {count:3d} {rel}:{name} {start}-{end} ({end - start + 1} lines)")


if __name__ == "__main__":
    main()

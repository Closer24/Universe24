"""The keeper's census of the code against the law's whole-number rules (the owner's ask of 2026-10-30, 07:5x UTC: "check every code that was written").
By an AST scan of every Python file of a tree it counts, per file: float literals, true divisions (a pathlib join is spared), powers whose exponent is no integer literal, imports of math, random, fractions, decimal,
statistics, cmath, scipy, sympy or mpmath, calls of a root, an exponential, a logarithm, a circular function, round, float or pow, and numpy float dtypes (law: **No float anywhere in the system**, line 100,
the probes too; **No circularity that makes a phenomenon happen**, line 102). A count is a finding to read, not a verdict: a test may lay a float on purpose to see it refused.
Usage: python -I scribe_code_census.py <tree> [<tree> ...]    (LINES=1 in the environment prints each hit with its line)"""

import ast
import sys
from collections import Counter, defaultdict
from pathlib import Path

NON_WHOLE_IMPORTS = {"math", "random", "fractions", "decimal", "statistics", "cmath", "scipy", "sympy", "mpmath"}
BAD_CALLS = {"sqrt", "exp", "log", "log2", "log10", "sin", "cos", "tan", "atan", "atan2", "asin", "acos", "sinh", "cosh", "tanh", "pow", "round", "float", "isqrt", "hypot", "pi"}
FLOAT_DTYPES = {"float", "float16", "float32", "float64", "double", "complex128", "complex64", "longdouble"}


class Tally(Counter):
    """A counter that also notes the line of each hit."""

    def __init__(self, base: Counter, path: Path) -> None:
        super().__init__()
        self.path = path

    def note(self, key: str, node: ast.AST) -> None:
        self[key] += 1
        DETAIL.append((str(self.path), getattr(node, "lineno", 0), key))


PATHISH = ("path", "root", "dir", "here", "repo", "home", "base", "folder", "tmp", "parent", "file")


def path_join(node: ast.BinOp) -> bool:
    """A pathlib join, not a division: the right side a string, or the left a Path call, a .parent or a path-like name."""
    right, left = node.right, node.left
    if isinstance(right, ast.Constant) and isinstance(right.value, str):
        return True
    if isinstance(right, ast.JoinedStr):
        return True
    while isinstance(left, ast.BinOp) and isinstance(left.op, ast.Div):
        left = left.left
    if isinstance(left, ast.Call):
        f = left.func
        name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
        return name in {"Path", "resolve", "parent", "expanduser"}
    if isinstance(left, ast.Attribute):
        return left.attr in {"parent", "parents"} or any(k in left.attr.lower() for k in PATHISH)
    if isinstance(left, ast.Name):
        return any(k in left.id.lower() for k in PATHISH)
    return False


DETAIL: list[tuple[str, int, str]] = []


def scan(path: Path) -> Counter:
    c: Counter = Counter()
    c = Tally(c, path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError, ValueError):
        c.note("unparsed", node)
        return c
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            c.note("float literal", node)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if not path_join(node):
                c.note("true division", node)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            e = node.right
            if isinstance(e, ast.UnaryOp):
                e = e.operand
            if not (isinstance(e, ast.Constant) and isinstance(e.value, int)):
                c.note("power (non-literal or float exponent)", node)
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in NON_WHOLE_IMPORTS:
                    c.note(f"import {a.name.split('.')[0]}", node)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in NON_WHOLE_IMPORTS:
            c.note(f"import {node.module.split('.')[0]}", node)
        elif isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if name in BAD_CALLS:
                c.note(f"call {name}", node)
        elif isinstance(node, ast.Attribute) and node.attr in FLOAT_DTYPES:
            c.note(f"dtype {node.attr}", node)
    return c


def main(trees: list[str]) -> None:
    import os
    lines = os.environ.get("LINES") == "1"
    by_dir: dict[str, Counter] = defaultdict(Counter)
    files_by_dir: dict[str, int] = Counter()
    bad_by_dir: dict[str, list[str]] = defaultdict(list)
    for root in trees:
        for path in sorted(Path(root).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(root)
            top = "/".join(rel.parts[:4]) if len(rel.parts) > 4 else "/".join(rel.parts[:-1]) or "."
            c = scan(path)
            files_by_dir[top] += 1
            if sum(v for k, v in c.items() if k != "unparsed"):
                bad_by_dir[top].append(str(rel))
            by_dir[top].update(c)
    total_files = sum(files_by_dir.values())
    total_bad = sum(len(v) for v in bad_by_dir.values())
    print(f"files {total_files}; files with a hit {total_bad}")
    for top in sorted(files_by_dir):
        n, b = files_by_dir[top], len(bad_by_dir[top])
        if b:
            kinds = ", ".join(f"{k} {v}" for k, v in by_dir[top].most_common(6))
            print(f"  {top}: {b} of {n} files; {kinds}")
    if lines:
        for path, no, key in DETAIL:
            print(f"    {path}:{no}: {key}")
    print("directories with no hit:", sum(1 for t in files_by_dir if not bad_by_dir[t]), "of", len(files_by_dir))


if __name__ == "__main__":
    main(sys.argv[1:])

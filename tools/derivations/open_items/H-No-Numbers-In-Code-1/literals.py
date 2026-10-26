"""Walk every .py under a root and print every numeric literal.

Columns: file:line | literal | kind | source line (stripped).
kind is int or float; bool is excluded. A second pass lists
string constants that parse as a number (digit-only strings).
Usage: literals.py <root> [--strings] [--tests-root <dir>]
"""
import ast
import os
import sys
from collections import Counter


def walk(root):
    for dirpath, _dirs, names in sorted(os.walk(root)):
        for name in sorted(names):
            if name.endswith(".py"):
                yield os.path.join(dirpath, name)


def literals(path, rel):
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines()
    tree = ast.parse(src, path)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool):
            v = node.value
            if isinstance(v, (int, float, complex)):
                out.append((node.lineno, node.col_offset, v, type(v).__name__,
                            lines[node.lineno - 1].strip()))
    out.sort()
    return [(rel, ln, col, v, kind, text) for ln, col, v, kind, text in out]


def numeric_strings(path, rel):
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines()
    tree = ast.parse(src, path)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            s = node.value.strip()
            if s and (s.lstrip("-").isdigit()):
                out.append((rel, node.lineno, node.value, lines[node.lineno - 1].strip()))
    return sorted(out)


def main(argv):
    root = argv[1]
    want_strings = "--strings" in argv
    rows = []
    strs = []
    for path in walk(root):
        rel = os.path.relpath(path, os.path.dirname(root.rstrip("/")) or ".")
        rows.extend(literals(path, rel))
        if want_strings:
            strs.extend(numeric_strings(path, rel))
    print("file:line | literal | kind | source line")
    for rel, ln, col, v, kind, text in rows:
        print(f"{rel}:{ln} | {v!r} | {kind} | {text}")
    counts = Counter(v for *_a, v, _k, _t in [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows])
    counts = Counter(r[3] for r in rows)
    print()
    print("count by literal (sites):")
    for v, n in sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        print(f"  {v!r}: {n}")
    big = {v: n for v, n in counts.items() if v not in (0, 1, -1)}
    print(f"distinct beyond 0, 1, -1: {len(big)}; sites: {sum(big.values())}")
    print(f"total sites: {len(rows)}; floats: {sum(1 for r in rows if r[4] == 'float')}")
    if want_strings:
        print()
        print("string constants that read as a number:")
        for rel, ln, s, text in strs:
            print(f"{rel}:{ln} | {s!r} | {text}")


if __name__ == "__main__":
    main(sys.argv)

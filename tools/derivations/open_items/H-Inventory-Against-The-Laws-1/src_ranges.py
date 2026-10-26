"""Exact line ranges (ast end_lineno) of the src functions and classes nominated for the inventory, grouped per file, with the file's total; a nomination 'ALL' takes the whole file."""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
SPEC = json.loads(Path(sys.argv[2]).read_text())
grand = 0
grand_file = 0
for rel, names in SPEC.items():
    path = ROOT / rel
    src = path.read_text()
    total = len(src.splitlines())
    grand_file += total
    if names == "ALL":
        print(f"{rel}: ALL 1-{total} = {total} lines (file {total})")
        grand += total
        continue
    tree = ast.parse(src)
    spans = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start = node.lineno
            if node.decorator_list:
                start = min(d.lineno for d in node.decorator_list)
            spans[node.name] = (start, node.end_lineno)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    spans[target.id] = (node.lineno, node.end_lineno)
                elif isinstance(target, ast.Tuple):
                    for element in target.elts:
                        if isinstance(element, ast.Name):
                            spans[element.id] = (node.lineno, node.end_lineno)
    count = 0
    parts = []
    for name in names:
        if name not in spans:
            parts.append(f"{name}:MISSING")
            continue
        a, b = spans[name]
        count += b - a + 1
        parts.append(f"{name} {a}-{b} ({b - a + 1})")
    grand += count
    print(f"{rel}: {count} of {total} lines: " + "; ".join(parts))
print(f"TOTAL nominated {grand} lines over {grand_file} lines of the files named")

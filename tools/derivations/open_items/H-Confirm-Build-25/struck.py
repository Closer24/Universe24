"""Every struck name read as code and not as a word: the files' syntax trees walked for a Name, an Attribute, a def or a class of that name (a string, a docstring and a comment are words and pass), over src, tests, the tools' own files and the toys."""
import ast, sys, pathlib
NAMES = ["division_forward", "odd_rounded", "Kid", "child_at", "child_laid", "light_children", "link_factors", "fold_links", "link_phases", "rise_of", "carried_division", "mirrored", "run"]
roots = sys.argv[1:]
hits = {n: [] for n in NAMES}
files = []
for r in roots:
    p = pathlib.Path(r)
    files += sorted(p.rglob("*.py")) if p.is_dir() else [p]
for f in files:
    try:
        t = ast.parse(f.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        continue
    for node in ast.walk(t):
        name = None
        if isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.alias):
            name = node.name.split(".")[-1]
        if name in hits:
            hits[name].append(f"{f}:{getattr(node, 'lineno', 0)}")
for n in NAMES:
    print(n, len(hits[n]), hits[n][:6])
print("files read", len(files))

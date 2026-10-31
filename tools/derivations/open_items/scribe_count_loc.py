"""The keeper's counter of active lines (the Boss's RUNNER-CUT and DECODER-CUT checks, 6541888909 and 6542001729): active lines of code per file and
per folder of a git revision, read from the git objects, nothing written to the tree.

A line is ACTIVE when it holds at least one code token: not blank, not a comment alone, not a line inside a docstring or a bare string statement.
The cuts' targets are by this count on the same head: the runner (src/tensor24/runner/) and the decoder (src/tensor24/decoder/) each no larger than the
Node-clock (src/tensor24/engine/ and src/tensor24/algebra/carry.py). usage, from the repo root: python -I tools/derivations/open_items/scribe_count_loc.py <rev> [<rev> ...]"""

import ast
import io
import subprocess
import sys
import tokenize

SKIP = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER, tokenize.ENCODING}


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def classify(text: str) -> dict[str, int]:
    lines = text.splitlines()
    total = len(lines)
    blank = sum(1 for x in lines if not x.strip())
    doc = set()
    try:
        tree = ast.parse(text)
        for node in ast.walk(tree):
            body = getattr(node, "body", None)
            if isinstance(body, list) and body and isinstance(body[0], ast.Expr):
                v = body[0].value
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    doc.update(range(body[0].lineno, body[0].end_lineno + 1))
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                doc.update(range(node.lineno, node.end_lineno + 1))
    except SyntaxError:
        pass
    code, comment = set(), set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                comment.add(tok.start[0])
            elif tok.type not in SKIP:
                code.update(range(tok.start[0], tok.end[0] + 1))
    except (tokenize.TokenError, IndentationError):
        code = {i + 1 for i, x in enumerate(lines) if x.strip() and not x.strip().startswith("#")}
    active = {n for n in code if n not in doc}
    comment_only = {n for n in comment if n not in code and n not in doc}
    docstring = {n for n in doc if 1 <= n <= total and lines[n - 1].strip()}
    return {"total": total, "blank": blank, "comment": len(comment_only), "docstring": len(docstring), "active": len(active)}


def tally(rev: str) -> dict[str, dict[str, int]]:
    names = git("ls-tree", "-r", "--name-only", rev).decode().splitlines()
    out: dict[str, dict[str, int]] = {}
    for name in names:
        if not name.endswith(".py"):
            continue
        if not (name.startswith("src/") or name.startswith("tests/") or (name.startswith("tools/") and "/" not in name[6:]) or name.startswith("tools/look/")):
            continue
        text = git("show", f"{rev}:{name}").decode("utf-8", "replace")
        out[name] = classify(text)
    return out


def folder(name: str) -> str:
    parts = name.split("/")
    if parts[0] == "src":
        return "src/" + "/".join(parts[1:3]) if len(parts) > 3 else "src/" + "/".join(parts[1:])
    if parts[0] == "tests":
        return "tests"
    return "tools" if parts[0] == "tools" else parts[0]


def main() -> None:
    for rev in sys.argv[1:]:
        table = tally(rev)
        print(f"=== {rev} ({git('rev-parse', '--short', rev).decode().strip()}): {len(table)} python files")
        groups: dict[str, dict[str, int]] = {}
        for name, c in table.items():
            g = groups.setdefault(folder(name), {"files": 0, "total": 0, "blank": 0, "comment": 0, "docstring": 0, "active": 0})
            g["files"] += 1
            for k in ("total", "blank", "comment", "docstring", "active"):
                g[k] += c[k]
        for g, c in sorted(groups.items()):
            print(f"{g:34s} files {c['files']:3d}  physical {c['total']:6d}  blank {c['blank']:5d}  comment {c['comment']:5d}  docstring {c['docstring']:5d}  ACTIVE {c['active']:6d}")
        for prefix in ("src/", "tests/", "tools/"):
            sel = [c for n, c in table.items() if n.startswith(prefix)]
            print(f"-- {prefix:7s} files {len(sel):3d}  physical {sum(c['total'] for c in sel):6d}  ACTIVE {sum(c['active'] for c in sel):6d}")
        print("-- src files, active lines:")
        for name, c in sorted(table.items()):
            if name.startswith("src/"):
                print(f"   {name:52s} {c['active']:5d}  (physical {c['total']})")


main()

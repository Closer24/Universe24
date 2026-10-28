"""The Scribe's scan of src/event_universe for the owner's rules (2026-10-28, 04:3x and 04:5x UTC).

Usage: python scribe_scan.py [ROOT] [--baseline FILE] [--write-baseline] [--all]

It reads every .py file under ROOT/src/event_universe and lists, by rule:
  NUMBER   a numeric literal beyond 0 and 1 (no number in the code)
  FLOAT    a float literal or dtype, a true division, float(), round(), a numpy function that returns a float
  IMPORT   math, cmath, statistics, random, fractions, decimal, scipy, sympy, mpmath
  CIRCLE   a cosine, sine or other circular function or constant (calls, attributes, names)
  WORD     a circular word in a name, string or comment: cos, sin, tan, angle, theta, circle, quaternion, Born, Lorentz ...
  DTYPE    a numpy constructor with no explicit dtype (its default is a float)
  STATE    a module-level empty container or defaultdict, a `global` statement, an `id(` call
Exit status 1 if a hit is not in the baseline (the hits that stand are listed in the baseline file; a new hit is
a refusal at the merge until it is read by a person). With --all every hit is listed, the baseline's included.
"""

import ast
import io
import json
import re
import sys
import tokenize
from pathlib import Path

BAD_IMPORTS = {"math", "cmath", "statistics", "random", "fractions", "decimal", "scipy", "sympy", "mpmath"}
NP_FLOAT = {
    "sqrt", "cbrt", "exp", "expm1", "log", "log2", "log10", "log1p", "hypot", "mean", "average", "median", "std",
    "var", "linspace", "logspace", "fft", "linalg", "random", "e", "inf", "nan", "float32", "float64", "float16",
}
NP_CIRCLE = {
    "cos", "sin", "tan", "arccos", "arcsin", "arctan", "arctan2", "cosh", "sinh", "tanh", "angle", "pi",
    "deg2rad", "rad2deg", "degrees", "radians", "unwrap",
}
NP_NEEDS_DTYPE = {"zeros", "ones", "empty", "full", "eye", "identity", "linspace"}
CIRCLE_WORDS = {
    "cos", "sin", "tan", "cosine", "sine", "tangent", "arctan", "atan", "atan2", "acos", "asin", "theta", "angle",
    "angles", "radian", "radians", "degree", "degrees", "circle", "circles", "circular", "quaternion",
    "quaternions", "tsirelson", "lorentz", "planck", "coulomb", "pi",
}
BORN = re.compile(r"\bBorn\b")
CONTAINERS = {"dict", "list", "set", "defaultdict", "OrderedDict", "Counter", "deque"}


def words_of(text: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return [w.lower() for w in re.findall(r"[A-Za-z]+", spaced)]


def scan_file(path: Path, rel: str) -> list[tuple[str, int, str]]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    hits: list[tuple[str, int, str]] = []

    def add(rule: str, line: int, text: str = "") -> None:
        hits.append((rule, line, (text or lines[line - 1]).strip()))

    tree = ast.parse(source)
    numpy_names = {"np", "numpy"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in BAD_IMPORTS:
                    add("IMPORT", node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in BAD_IMPORTS:
                add("IMPORT", node.lineno)
        elif isinstance(node, ast.Constant) and isinstance(node.value, int | float | complex):
            if isinstance(node.value, bool):
                continue
            if isinstance(node.value, float | complex):
                add("FLOAT", node.lineno)
            if node.value not in (0, 1):
                add("NUMBER", node.lineno)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            add("FLOAT", node.lineno, "true division: " + lines[node.lineno - 1].strip())
        elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Div):
            add("FLOAT", node.lineno, "true division: " + lines[node.lineno - 1].strip())
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in {"float", "round", "complex"}:
                add("FLOAT", node.lineno)
            if isinstance(f, ast.Name) and f.id == "pow":
                add("FLOAT", node.lineno, "pow: " + lines[node.lineno - 1].strip())
            if isinstance(f, ast.Name) and f.id == "id":
                add("STATE", node.lineno, "id(): " + lines[node.lineno - 1].strip())
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in numpy_names:
                if f.attr in NP_NEEDS_DTYPE and not any(k.arg == "dtype" for k in node.keywords):
                    add("DTYPE", node.lineno)
        elif isinstance(node, ast.Attribute):
            base = node.value
            if isinstance(base, ast.Name) and base.id in numpy_names:
                if node.attr in NP_FLOAT:
                    add("FLOAT", node.lineno)
                if node.attr in NP_CIRCLE:
                    add("CIRCLE", node.lineno)
            if node.attr in {"float", "float_", "double"} and isinstance(base, ast.Name) and base.id in numpy_names:
                add("FLOAT", node.lineno)
        elif isinstance(node, ast.Name) and node.id in {"float", "cos", "sin", "tan", "atan2"}:
            add("CIRCLE" if node.id != "float" else "FLOAT", node.lineno)
        elif isinstance(node, ast.Global):
            add("STATE", node.lineno, "global: " + lines[node.lineno - 1].strip())
    for stmt in tree.body:
        value = None
        if isinstance(stmt, ast.Assign | ast.AnnAssign):
            value = stmt.value
        if value is None:
            continue
        empty = (
            (isinstance(value, ast.Dict) and not value.keys)
            or (isinstance(value, ast.List | ast.Set) and not value.elts)
            or (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name | ast.Attribute)
                and (value.func.id if isinstance(value.func, ast.Name) else value.func.attr) in CONTAINERS
                and not value.args
            )
        )
        if empty:
            add("STATE", stmt.lineno, "module-level container: " + lines[stmt.lineno - 1].strip())
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type == tokenize.NAME:
            found = [w for w in words_of(tok.string) if w in CIRCLE_WORDS]
            if found:
                add("WORD", tok.start[0], f"name {tok.string}: " + lines[tok.start[0] - 1].strip())
        elif tok.type in (tokenize.STRING, tokenize.COMMENT):
            found = sorted({w for w in words_of(tok.string) if w in CIRCLE_WORDS})
            if BORN.search(tok.string):
                found.append("Born")
            if found:
                add("WORD", tok.start[0], f"{'/'.join(found)}: " + lines[tok.start[0] - 1].strip())
    return sorted(set(hits), key=lambda h: (h[1], h[0], h[2]))


def main(argv: list[str]) -> int:
    root = Path(next((a for a in argv if not a.startswith("--") and not a.endswith(".json")), "."))
    baseline_path = None
    if "--baseline" in argv:
        baseline_path = Path(argv[argv.index("--baseline") + 1])
    everything: dict[str, list[tuple[str, int, str]]] = {}
    for path in sorted((root / "src" / "event_universe").rglob("*.py")):
        rel = path.relative_to(root / "src" / "event_universe").as_posix()
        everything[rel] = scan_file(path, rel)
    keys = {f"{rule}|{rel}|{text}" for rel, hs in everything.items() for rule, _, text in hs}
    if "--write-baseline" in argv and baseline_path is not None:
        baseline_path.write_text(json.dumps(sorted(keys), indent=0) + "\n", encoding="utf-8")
        print(f"baseline written: {len(keys)} hits in {len(everything)} files")
        return 0
    baseline: set[str] = set(json.loads(baseline_path.read_text(encoding="utf-8"))) if baseline_path else set()
    new = 0
    counts: dict[str, int] = {}
    for rel, hs in everything.items():
        for rule, line, text in hs:
            counts[rule] = counts.get(rule, 0) + 1
            key = f"{rule}|{rel}|{text}"
            if key in baseline and "--all" not in argv:
                continue
            tag = "" if key in baseline else "NEW "
            new += 0 if key in baseline else 1
            print(f"{tag}{rule:7s} {rel}:{line}  {text[:130]}")
    print("hits by rule:", dict(sorted(counts.items())), "| files:", len(everything), "| new:", new)
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

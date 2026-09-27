"""The shape of the code, recorded and gated (the model owner's decisions of 2026-09-26 through
the Boss, records 2239 and 2241; skills/workflow.md, the short procedure, point 11).

For every Python file under `src/` the counts: total lines, docstring lines, comment lines,
references to records or decisions ("record 2234", "decision 3"), sites of Rule3's arithmetic
outside its one function, sites that shift an array across Nodes, and, for every Python file of
`src/`, `tools/` and `tests/`, the names imported from the loop's module beyond its public
entry. A file within the limits (every docstring one line, no record reference, under 400
lines, none of the three sites) passes whatever its counts. A file beyond them is compared with
`tests/code_shape_baseline.json` and with the same file at the merge base (the ref CI checks
against, else origin/main): none of its counts may grow, and none may stand above the merge
base's (a baseline raised in the same commit is refused); a count that went down is re-recorded
in the same commit (`python tools/record_code_shape.py`); a new file beyond them fails. Two
functions of `src/` with the same
normalised body (names and literals abstracted) fail; the duplicates of today are in the baseline
and may only go down. The import contracts hold with no baseline: a feature folder imports
`core/` alone and never another feature; `core/` imports nothing of the package outside itself;
nothing outside `core/` imports the loop's internals.

Usage: `python tools/record_code_shape.py` writes the baseline for the current tree.
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE = Path("tests/code_shape_baseline.json")
PACKAGE = Path("src/event_universe")
LOOP = PACKAGE / "events" / "detector_law.py"
LOOP_MODULE = "event_universe.events.detector_law"
LOOP_PUBLIC = frozenset({"DetectorLawSimulation"})
NEW_FILE_LINES = 400
DUPLICATE_MIN_STATEMENTS = 2
RECORD_REFERENCE = re.compile(r"\b(?:record|records|decision|decisions)\s+\d+", re.IGNORECASE)
# Rule3's own lines (tests/test_rule3.py of the operation's cut names the same four)
RULE_ARITHMETIC = (
    r"self_coefficient \* (now|before)\b",
    r"wall \* before\b",
    r"wall \* now \+ remainder",
    r"now \* now \+ before \* before",
)
RULE_HOME = PACKAGE / "core" / "rule3.py"
LEVEL_SHIFT = re.compile(r"np\.roll\(|self\._shift\(|\.take\(")
SHIFT_HOME = PACKAGE / "core" / "ports.py"
COUNTS = (
    "lines",
    "docstring_lines",
    "comment_lines",
    "record_references",
    "rule_arithmetic_sites",
    "level_shift_sites",
)
SCOPES = ("src", "tools", "tests")


def python_files(root: Path, folder: str) -> list[Path]:
    base = root / folder
    return sorted(p for p in base.rglob("*.py")) if base.is_dir() else []


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def docstring_of(node: ast.AST) -> ast.Expr | None:
    body = getattr(node, "body", None)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        if isinstance(body[0].value.value, str):
            return body[0]
    return None


def shape_of(root: Path, path: Path) -> dict[str, int]:
    """The counts of one file of `src/`."""
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_lines: set[int] = set()
    multi_line = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            doc = docstring_of(node)
            if doc is not None:
                end = doc.end_lineno or doc.lineno
                docstring_lines.update(range(doc.lineno, end + 1))
                multi_line += end > doc.lineno
    comment_lines = {
        token.start[0]
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type == tokenize.COMMENT
    }
    arithmetic = 0
    if path.resolve() != (root / RULE_HOME).resolve():
        arithmetic = sum(len(re.findall(pattern, text)) for pattern in RULE_ARITHMETIC)
    return {
        "lines": len(text.splitlines()),
        "docstring_lines": len(docstring_lines),
        "comment_lines": len(comment_lines),
        "record_references": len(RECORD_REFERENCE.findall(text)),
        "rule_arithmetic_sites": arithmetic,
        "level_shift_sites": (
            0 if path.resolve() == (root / SHIFT_HOME).resolve() else len(LEVEL_SHIFT.findall(text))
        ),
        "multi_line_docstrings": multi_line,
    }


class Abstracted(ast.NodeTransformer):
    """A function's body with every name numbered in order of first use and every literal its
    type: two functions that differ only in their names and literals abstract to one tree."""

    def __init__(self) -> None:
        self.names: dict[str, str] = {}

    def key(self, name: str) -> str:
        return self.names.setdefault(name, f"n{len(self.names)}")

    def visit_Name(self, node: ast.Name) -> ast.AST:
        return ast.copy_location(ast.Name(id=self.key(node.id), ctx=node.ctx), node)

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = self.key(node.arg)
        node.annotation = None
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        self.generic_visit(node)
        node.attr = self.key(node.attr)
        return node

    def visit_keyword(self, node: ast.keyword) -> ast.AST:
        self.generic_visit(node)
        if node.arg:
            node.arg = self.key(node.arg)
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        return ast.copy_location(ast.Constant(value=type(node.value).__name__), node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        node.name = "f"
        node.returns = None
        node.decorator_list = []
        if docstring_of(node) is not None:
            node.body = node.body[1:]
        self.generic_visit(node)
        return node


def body_hash(function: ast.FunctionDef) -> str | None:
    """The hash of the abstracted body, or None for a body below the duplicate threshold."""
    body = function.body[1:] if docstring_of(function) is not None else function.body
    if len(body) < DUPLICATE_MIN_STATEMENTS:
        return None
    copy = ast.parse(ast.unparse(function)).body[0]
    abstracted = Abstracted().visit(copy)
    return hashlib.sha256(ast.dump(abstracted).encode()).hexdigest()[:16]


def duplicates(root: Path) -> dict[str, list[str]]:
    """Every group of two or more functions of `src/` with one abstracted body."""
    groups: dict[str, list[str]] = {}
    for path in python_files(root, "src"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                digest = body_hash(node)
                if digest is not None:
                    groups.setdefault(digest, []).append(f"{relative(root, path)}:{node.name}")
    return {digest: sorted(names) for digest, names in sorted(groups.items()) if len(names) > 1}


def imports_of(path: Path, module_name: str) -> list[tuple[str, list[str]]]:
    """Every import of the file as (module, names), relative imports resolved; a bare `import
    a.b` is ("a.b", ["*"])."""
    found: list[tuple[str, list[str]]] = []
    package = module_name.rsplit(".", 1)[0] if module_name.count(".") else ""
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found.extend((alias.name, ["*"]) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level:
                parts = package.split(".") if package else []
                parts = parts[: len(parts) - node.level + 1] if node.level > 1 else parts
                module = ".".join(part for part in [*parts, module] if part)
            found.append((module, [alias.name for alias in node.names]))
    return found


def module_name_of(root: Path, path: Path) -> str:
    rel = path.relative_to(root / "src") if path.is_relative_to(root / "src") else path.relative_to(root)
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def loop_internal_imports(root: Path) -> dict[str, list[str]]:
    """Per file of `src/`, `tools/` and `tests/` outside `core/` and the loop's own module, the
    names it imports from the loop's module beyond its public entry ("*" a bare module import)."""
    found: dict[str, list[str]] = {}
    for scope in SCOPES:
        for path in python_files(root, scope):
            rel = relative(root, path)
            if rel == LOOP.as_posix() or rel.startswith((PACKAGE / "core").as_posix() + "/"):
                continue
            names = sorted(
                {
                    name
                    for module, imported in imports_of(path, module_name_of(root, path))
                    if module == LOOP_MODULE
                    for name in imported
                    if name not in LOOP_PUBLIC
                }
            )
            if names:
                found[rel] = names
    return found


def contract_violations(root: Path) -> list[str]:
    """The import contracts of record 2241 (b), no baseline: a feature folder imports `core/`
    alone and never another feature; `core/` imports nothing of the package outside itself."""
    package = PACKAGE.name
    core = f"{package}.core"
    violations: list[str] = []
    for path in python_files(root, "src"):
        rel = relative(root, path)
        module = module_name_of(root, path)
        parts = module.split(".")
        if len(parts) < 2 or parts[0] != package:
            continue
        for imported, _names in imports_of(path, module):
            if not (imported == package or imported.startswith(package + ".")):
                continue
            if parts[1] == "features":
                own = ".".join(parts[:3])
                if not (imported == core or imported.startswith(core + ".") or imported == own):
                    violations.append(f"{rel} imports {imported}: a feature imports core/ alone")
            elif parts[1] == "core":
                if not (imported == core or imported.startswith(core + ".")):
                    violations.append(f"{rel} imports {imported}: core/ imports nothing outside core/")
    return violations


def record(root: Path) -> dict[str, Any]:
    """The baseline of the current tree: the counts of the files beyond the limits alone (a file within them needs no entry), the duplicate groups and the imports of the loop's internals, every key sorted so two re-records of different files touch different lines."""
    files = {}
    for path in python_files(root, "src"):
        rel = relative(root, path)
        shape = shape_of(root, path)
        if beyond_the_limits(rel, shape):
            files[rel] = {key: shape[key] for key in COUNTS}
    return {
        "format": "code-shape-baseline",
        "files": dict(sorted(files.items())),
        "duplicates": duplicates(root),
        "loop_internal_imports": dict(sorted(loop_internal_imports(root).items())),
    }


def beyond_the_limits(rel: str, shape: dict[str, int]) -> list[str]:
    """Every way one file is beyond the limits every file is held to from its first commit: a docstring beyond one line, a record reference, 400 lines, a site of Rule3's arithmetic or of a shift across Nodes."""
    found: list[str] = []
    if shape["multi_line_docstrings"]:
        found.append(f"{rel} has {shape['multi_line_docstrings']} docstring(s) beyond one line")
    if shape["record_references"]:
        found.append(f"{rel} refers to {shape['record_references']} record(s) or decision(s)")
    if shape["lines"] >= NEW_FILE_LINES:
        found.append(f"{rel} has {shape['lines']} lines (the limit {NEW_FILE_LINES})")
    for key in ("rule_arithmetic_sites", "level_shift_sites"):
        if shape[key]:
            found.append(f"{rel} has {shape[key]} {key.replace('_', ' ')}")
    return found


def base_baseline(root: Path, ref: str | None = None) -> dict[str, Any] | None:
    """The baseline as the merge base holds it (the ref CI checks against, else origin/main), or None where git cannot show it; a baseline raised in the same commit never passes the ratchet."""
    ref = ref or os.environ.get("CHECK_BASE") or "origin/main"
    try:
        shown = subprocess.run(
            ["git", "show", f"{ref}:{BASELINE.as_posix()}"],
            capture_output=True,
            text=True,
            cwd=root,
            check=True,
        ).stdout
    except OSError, subprocess.CalledProcessError:
        return None
    loaded: dict[str, Any] = json.loads(shown)
    return loaded


def violations(root: Path, baseline: dict[str, Any], base: dict[str, Any] | None = None) -> list[str]:
    """Every way the tree departs from the limits and the baseline, one line each: a file within the limits passes whatever its counts; a file beyond them is new and fails, or is recorded and ratchets."""
    found: list[str] = []
    re_record = (
        f"re-record the baseline in this commit: python {Path('tools/record_code_shape.py').as_posix()}"
    )
    recorded_files: dict[str, dict[str, int]] = baseline["files"]
    present = {relative(root, path): shape_of(root, path) for path in python_files(root, "src")}
    for rel in sorted(set(recorded_files) - set(present)):
        found.append(f"{rel} is in the baseline and not in the tree; {re_record}")
    for rel, shape in present.items():
        beyond = beyond_the_limits(rel, shape)
        if not beyond:
            continue
        recorded = recorded_files.get(rel)
        if recorded is None:
            found.extend(f"{line} and is new" for line in beyond)
            continue
        for key in COUNTS:
            if shape[key] > recorded[key]:
                found.append(f"{rel}: {key.replace('_', ' ')} grew from {recorded[key]} to {shape[key]}")
            elif shape[key] < recorded[key]:
                found.append(
                    f"{rel}: {key.replace('_', ' ')} went down from {recorded[key]} to {shape[key]}; {re_record}"
                )
    recorded_groups: dict[str, list[str]] = baseline["duplicates"]
    groups = duplicates(root)
    for digest, names in groups.items():
        recorded_names = recorded_groups.get(digest, [])
        if len(names) > len(recorded_names):
            found.append(f"duplicate functions: {', '.join(names)} share one body")
        elif len(names) < len(recorded_names):
            found.append(f"a duplicate group shrank ({', '.join(names)}); {re_record}")
    for digest in set(recorded_groups) - set(groups):
        found.append(
            f"a duplicate group of the baseline is gone ({', '.join(recorded_groups[digest])}); {re_record}"
        )
    recorded_imports: dict[str, list[str]] = baseline["loop_internal_imports"]
    imports = loop_internal_imports(root)
    for rel, names in imports.items():
        recorded_names = set(recorded_imports.get(rel, []))
        grew = sorted(set(names) - recorded_names)
        if grew:
            found.append(
                f"{rel} imports the loop's internals {', '.join(grew)}: nothing outside core/ does"
            )
        elif set(names) < recorded_names:
            found.append(f"{rel} imports fewer of the loop's internals; {re_record}")
    for rel in set(recorded_imports) - set(imports):
        found.append(f"{rel} no longer imports the loop's internals; {re_record}")
    found.extend(contract_violations(root))
    if base is not None:
        found.extend(above_the_base(root, present, groups, imports, base))
    return found


def above_the_base(
    root: Path,
    present: dict[str, dict[str, int]],
    groups: dict[str, list[str]],
    imports: dict[str, list[str]],
    base: dict[str, Any],
) -> list[str]:
    """Every count of a file beyond the limits, every duplicate group and every import of the loop's internals that stands higher than the merge base's baseline: raising the baseline in the same commit is refused."""
    found: list[str] = []
    for rel, shape in present.items():
        recorded = base["files"].get(rel)
        if recorded is None or not beyond_the_limits(rel, shape):
            continue
        for key in COUNTS:
            if shape[key] > recorded[key]:
                found.append(
                    f"{rel}: {key.replace('_', ' ')} is {shape[key]}, above the merge base's {recorded[key]}"
                )
    for digest, names in groups.items():
        if len(names) > len(base["duplicates"].get(digest, [])):
            found.append(f"duplicate functions above the merge base: {', '.join(names)}")
    for rel, names in imports.items():
        grew = sorted(set(names) - set(base["loop_internal_imports"].get(rel, [])))
        if grew:
            found.append(f"{rel} imports the loop's internals {', '.join(grew)} above the merge base")
    return found


def main() -> None:
    """Write the baseline for the current tree (no commit stamp, so two re-records differ only where the counts differ)."""
    baseline = record(ROOT)
    (ROOT / BASELINE).write_text(json.dumps(baseline, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    files = baseline["files"]
    totals = {key: sum(shape[key] for shape in files.values()) for key in COUNTS}
    print(
        f"{len(files)} files of src/ beyond the limits recorded: "
        + ", ".join(f"{k} {v}" for k, v in totals.items())
    )
    print(
        f"duplicate groups {len(baseline['duplicates'])}; "
        f"files importing the loop's internals {len(baseline['loop_internal_imports'])}"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

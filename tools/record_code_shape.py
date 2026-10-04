"""The shape of the code, gated against the merge base (the model owner's decisions of 2026-09-26
through the Boss, records 2239 and 2241; #1198, gate 7: no recorded baseline file).

For every Python file under `src/` the counts: total lines, docstring lines, comment lines,
references to records or decisions ("record 2234", "decision 3"), sites of Rule3's arithmetic
outside its one function, sites that shift an array across Nodes and sites that write a level onto
the lattice (an item of, or the attribute, `now`, `before` or `remainder`
assigned or augmented: the write's gate, the model owner's word of 2026-09-28: every level written
is one act of the write, features/write, or Rule3's own step, applied by the loop at its sites at
the merge base and nowhere new); for every Python file of
`src/`, `tools/` and `tests/`, the names imported from the loop's module beyond its public entry.
A file within the limits (every docstring one line, no record reference, under 400 lines, none of
the sites) passes whatever its counts. A file beyond them holds each count at or below the same
file's at the merge base (CHECK_BASE, else origin/main), read from git; a new file beyond them
fails. Two functions of `src/` with one abstracted body fail beyond the merge base's groups; an
internal of the loop is imported by no more files than at the merge base. The import contracts
hold outright: a feature folder imports `core/` alone; `core/` imports nothing outside itself.

Usage: `python tools/record_code_shape.py` prints every departure from the merge base.
"""

from __future__ import annotations

import ast
import hashlib
import io
import re
import sys
import tokenize
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from merge_base import base_ref, carried, tree_at  # noqa: E402

PACKAGE = Path("src/event_universe")
LOOP = PACKAGE / "lattice.py"
LOOP_MODULE = "event_universe.lattice"
LOOP_PUBLIC = frozenset({"lattice"})
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
LEVELS = frozenset({"now", "before", "remainder"})
COUNTS = (
    "lines",
    "docstring_lines",
    "comment_lines",
    "record_references",
    "rule_arithmetic_sites",
    "level_shift_sites",
    "level_write_sites",
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


def written_object(target: ast.expr) -> ast.expr:
    """The object a subscript writes into, through a call around it (`cast(np.ndarray, record.now)[mask]`)."""
    while isinstance(target, ast.Call) and target.args:
        target = target.args[-1]
    return target


def level_write_sites(tree: ast.AST) -> int:
    """The assignments and augmented assignments whose target is an item of, or the attribute, a level of any object (`now`, `before`, `remainder`): the loop's applications of the write's act and of Rule3's step, and nothing new."""
    found = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign | ast.AugAssign | ast.AnnAssign):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for element in target.elts if isinstance(target, ast.Tuple) else [target]:
                    held = (
                        written_object(element.value) if isinstance(element, ast.Subscript) else element
                    )
                    found += isinstance(held, ast.Attribute) and held.attr in LEVELS
    return found


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
        "level_write_sites": level_write_sites(tree),
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
    """The record of a tree: the counts of the files beyond the limits alone (a file within them needs none), the duplicate groups and the imports of the loop's internals."""
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
    """Every way one file is beyond the limits every file is held to from its first commit: a docstring beyond one line, a record reference, 400 lines, a site of Rule3's arithmetic, of a shift across Nodes or of a write of a level onto the lattice."""
    found: list[str] = []
    if shape["multi_line_docstrings"]:
        found.append(f"{rel} has {shape['multi_line_docstrings']} docstring(s) beyond one line")
    if shape["record_references"]:
        found.append(f"{rel} refers to {shape['record_references']} record(s) or decision(s)")
    if shape["lines"] >= NEW_FILE_LINES:
        found.append(f"{rel} has {shape['lines']} lines (the limit {NEW_FILE_LINES})")
    for key in ("rule_arithmetic_sites", "level_shift_sites", "level_write_sites"):
        if shape[key]:
            found.append(f"{rel} has {shape[key]} {key.replace('_', ' ')}")
    return found


def record_at(root: Path, ref: str | None = None) -> dict[str, Any]:
    """The same record of the merge base's tree (CHECK_BASE, else origin/main), read from git: no file holds it."""
    ref = ref or base_ref()
    with tree_at(root, ref, SCOPES) as base_root:
        base = record(base_root)
    return {**base, "files": carried(base["files"], root, ref)}


def violations(root: Path, base: dict[str, Any]) -> list[str]:
    """Every way the tree departs from the limits and the merge base, one line each: a file within the limits passes whatever its counts; a file beyond them is new and fails, or holds each count at or below the merge base's."""
    found: list[str] = []
    for path in python_files(root, "src"):
        rel = relative(root, path)
        shape = shape_of(root, path)
        beyond = beyond_the_limits(rel, shape)
        if not beyond:
            continue
        was = base["files"].get(rel)
        if was is None:
            found.extend(f"{line} and is new" for line in beyond)
            continue
        for key in COUNTS:
            if shape[key] > was[key]:
                found.append(f"{rel}: {key.replace('_', ' ')} grew from {was[key]} to {shape[key]}")
    for digest, names in duplicates(root).items():
        if len(names) > len(base["duplicates"].get(digest, [])):
            found.append(f"duplicate functions: {', '.join(names)} share one body")

    # per name, the number of files importing it: a helper moved between files keeps the count
    def importers(table: dict[str, list[str]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for names in table.values():
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts

    was_imported = importers(base["loop_internal_imports"])
    for name, count in sorted(importers(loop_internal_imports(root)).items()):
        if count > was_imported.get(name, 0):
            found.append(
                f"the loop's internal {name} is imported by {count} files, above the merge base's "
                f"{was_imported.get(name, 0)}: nothing outside core/ imports it"
            )
    found.extend(contract_violations(root))
    return found


def main() -> None:
    """Print every departure of the working tree from the limits and the merge base; exit 1 when there is one."""
    found = violations(ROOT, record_at(ROOT))
    print("\n".join(found) or "the shape of the code holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()

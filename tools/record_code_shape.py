"""The shape of the code, gated against the merge base (the model owner's decisions of 2026-09-26
through the Boss, records 2239 and 2241; #1198, gate 7: no recorded baseline file).

For every Python file under `src/` the counts: total lines, docstring lines, comment lines and
references to records or decisions ("record 2234", "decision 3"). A file within the limits (every
docstring one line, a module's the four layers, no record reference, under 400 lines) passes
whatever its counts; the four layers are Clock, Algebra, Board and Clicks, one line each in that
order (the owner's word of 2026-10-30, 11:0x UTC; Sofer's DOCLAYER rule asks for them). A file
beyond them holds each count at or below the same file's at the merge base (CHECK_BASE, else
origin/main), read from git; a new file beyond them fails. Two functions of `src/` with one
abstracted body fail beyond the merge base's groups. The old engine's rules (Rule3's arithmetic
in one home, the shifts across Nodes, the writes of a level, the loop's internals and the import
contracts of its folders) left with src/event_universe on the owner's word of 2026-10-30.

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

NEW_FILE_LINES = 400
DUPLICATE_MIN_STATEMENTS = 2
LAYERS = ("Clock:", "Algebra:", "Board:", "Clicks:")  # a module docstring's four layers, one line each
RECORD_REFERENCE = re.compile(r"\b(?:record|records|decision|decisions)\s+\d+", re.IGNORECASE)
COUNTS = (
    "lines",
    "docstring_lines",
    "comment_lines",
    "record_references",
)


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


def layered(node: ast.AST) -> bool:
    """A module's docstring told in the four layers, one line each and in their order."""
    lines = (ast.get_docstring(node) or "").splitlines() if isinstance(node, ast.Module) else []
    return len(lines) == len(LAYERS) and all(
        line.startswith(f"{layer} ") for line, layer in zip(lines, LAYERS, strict=True)
    )


def shape_of(path: Path) -> dict[str, int]:
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
                multi_line += end > doc.lineno and not layered(node)
    comment_lines = {
        token.start[0]
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type == tokenize.COMMENT
    }
    return {
        "lines": len(text.splitlines()),
        "docstring_lines": len(docstring_lines),
        "comment_lines": len(comment_lines),
        "record_references": len(RECORD_REFERENCE.findall(text)),
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


def record(root: Path) -> dict[str, Any]:
    """The record of a tree: the counts of the files beyond the limits alone (a file within them needs none) and the duplicate groups."""
    files = {}
    for path in python_files(root, "src"):
        rel = relative(root, path)
        shape = shape_of(path)
        if beyond_the_limits(rel, shape):
            files[rel] = {key: shape[key] for key in COUNTS}
    return {
        "format": "code-shape-baseline",
        "files": dict(sorted(files.items())),
        "duplicates": duplicates(root),
    }


def beyond_the_limits(rel: str, shape: dict[str, int]) -> list[str]:
    """Every way one file is beyond the limits every file is held to from its first commit: a docstring beyond one line (a module's beyond the four layers), a record reference or 400 lines."""
    found: list[str] = []
    if shape["multi_line_docstrings"]:
        found.append(f"{rel} has {shape['multi_line_docstrings']} docstring(s) beyond one line")
    if shape["record_references"]:
        found.append(f"{rel} refers to {shape['record_references']} record(s) or decision(s)")
    if shape["lines"] >= NEW_FILE_LINES:
        found.append(f"{rel} has {shape['lines']} lines (the limit {NEW_FILE_LINES})")
    return found


def record_at(root: Path, ref: str | None = None) -> dict[str, Any]:
    """The same record of the merge base's tree (CHECK_BASE, else origin/main), read from git: no file holds it."""
    ref = ref or base_ref()
    with tree_at(root, ref, ("src",)) as base_root:
        base = record(base_root)
    return {**base, "files": carried(base["files"], root, ref)}


def violations(root: Path, base: dict[str, Any]) -> list[str]:
    """Every way the tree departs from the limits and the merge base, one line each: a file within the limits passes whatever its counts; a file beyond them is new and fails, or holds each count at or below the merge base's."""
    found: list[str] = []
    for path in python_files(root, "src"):
        rel = relative(root, path)
        shape = shape_of(path)
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
    return found


def main() -> None:
    """Print every departure of the working tree from the limits and the merge base; exit 1 when there is one."""
    found = violations(ROOT, record_at(ROOT))
    print("\n".join(found) or "the shape of the code holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()

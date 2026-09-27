"""The reviewer's recurring findings as gates (issue #1198, item 4 (a); the model owner, 2026-09-27).

Four gates, selected on every pull request by `tools/check.py`:

1. Numbers. A numeric literal beyond 0, 1, 2, 3, 4, 6 and 8, outside a docstring, is counted
   per file (the count of issue #1197). No file's count may stand above the same file's at the
   merge base (CHECK_BASE, else origin/main), read from git; a new file has none.
2. Family names. A string literal equal to the name of a family declared in a world file under
   `examples/` is counted per file, on the same ratchet.
3. Rule3's arithmetic by hand. A floor division, a remainder (`//`, `%`, `divmod`) in
   `features/`, in `events/` or in `tools/body_generator.py` is counted per file, on the same
   ratchet: a division belongs in `core/rule3.py`, and the count may only fall.
4. A new module of `core/`. A Python file under `src/event_universe/core/` that the merge base
   does not hold needs a line in the pull request's body that starts with `APPROVED-CORE` and
   names Main Loop's approval. CI passes the body as the `PR_BODY` environment variable; the
   check runs on a pull request (or locally with PR_BODY set), never on a push to main.
A merge base that git cannot resolve fails by name.

Usage: `python tools/engine_gates.py` prints every count above the merge base's (#1198, gate 7:
no recorded baseline file).
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from merge_base import base_ref, carried, resolved, tree_at  # noqa: E402

PACKAGE = Path("src/event_universe")
CORE = PACKAGE / "core"
WORLDS = Path("examples")
FREE_NUMBERS = frozenset({0, 1, 2, 3, 4, 6, 8})
APPROVAL = "APPROVED-CORE"
COUNTS = ("numbers", "family_names", "hand_divisions")
# the places where a division by hand is Rule3's arithmetic written again
DIVISION_SCOPES = (PACKAGE / "features", PACKAGE / "events")
DIVISION_FILES = (Path("tools/body_generator.py"),)


def python_files(root: Path) -> list[Path]:
    base = root / PACKAGE
    found = sorted(base.rglob("*.py")) if base.is_dir() else []
    return found + [root / path for path in DIVISION_FILES if (root / path).is_file()]


def divides_by_hand(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    return rel in DIVISION_FILES or any(rel.is_relative_to(scope) for scope in DIVISION_SCOPES)


def family_names(root: Path) -> frozenset[str]:
    """Every family name declared in a world file under `examples/`."""
    names: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, inner in value.items():
                if key == "families" and isinstance(inner, dict):
                    names.update(inner)
                elif key == "families" and isinstance(inner, list):
                    names.update(e["name"] for e in inner if isinstance(e, dict) and "name" in e)
                walk(inner)
        elif isinstance(value, list):
            for inner in value:
                walk(inner)

    for path in sorted((root / WORLDS).rglob("*.json")):
        try:
            walk(json.loads(path.read_text(encoding="utf-8")))
        except ValueError:
            continue
    return frozenset(name for name in names if isinstance(name, str))


OPERATORS: dict[type[ast.AST], Any] = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Pow: lambda a, b: a**b,
    ast.LShift: lambda a, b: a << b,
    ast.RShift: lambda a, b: a >> b,
    ast.BitOr: lambda a, b: a | b,
    ast.BitAnd: lambda a, b: a & b,
    ast.BitXor: lambda a, b: a ^ b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.USub: lambda a: -a,
    ast.UAdd: lambda a: a,
}


def constant_value(node: ast.AST) -> int | None:
    """The value of an expression whose leaves are all integer literals (`4 * 8 + 8`, `1 << (6 * 8)`, `2 ** 10`, `-3`), folded; None where a leaf is a name, a call or a float, or the operator is not integer arithmetic."""
    if isinstance(node, ast.Constant):
        leaf = node.value
        return leaf if isinstance(leaf, int) and not isinstance(leaf, bool) else None
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        inner = constant_value(node.operand)
        return None if inner is None else int(OPERATORS[type(node.op)](inner))
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left, right = constant_value(node.left), constant_value(node.right)
        if left is None or right is None or (isinstance(node.op, ast.FloorDiv | ast.Mod) and right == 0):
            return None
        if isinstance(node.op, ast.Pow) and (right < 0 or right > 4096):
            return None
        if isinstance(node.op, ast.LShift | ast.RShift) and (right < 0 or right > 4096):
            return None
        return int(OPERATORS[type(node.op)](left, right))
    return None


def counts_of(path: Path, families: frozenset[str], divisions: bool = True) -> dict[str, int]:
    """The counts of one file: its numbers beyond the free ones, its family-name strings and, where
    `divisions`, its floor divisions and remainders by hand (a string's `%` format excluded)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            if node.body and isinstance(node.body[0], ast.Expr):
                docstrings.add(id(node.body[0].value))
    numbers = names = 0
    folded: set[int] = set()  # the leaves inside a constant expression, counted once as its value
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp | ast.UnaryOp) and id(node) not in folded:
            folded_value = constant_value(node)
            if folded_value is not None:  # a negative free number is free: -1 as 1
                numbers += abs(folded_value) not in FREE_NUMBERS
                folded.update(id(inner) for inner in ast.walk(node))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or id(node) in docstrings or id(node) in folded:
            continue
        value = node.value
        if isinstance(value, int | float | complex) and not isinstance(value, bool):
            numbers += value not in FREE_NUMBERS
        elif isinstance(value, str):
            names += value in families
    hand = 0
    if divisions:
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp | ast.AugAssign) and isinstance(
                node.op, ast.FloorDiv | ast.Mod
            ):
                left = node.left if isinstance(node, ast.BinOp) else node.target
                hand += not (isinstance(left, ast.Constant) and isinstance(left.value, str))
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "divmod"
            ):
                hand += 1
    return {"numbers": numbers, "family_names": names, "hand_divisions": hand}


def present(root: Path) -> dict[str, dict[str, int]]:
    families = family_names(root)
    return {
        path.relative_to(root).as_posix(): counts_of(path, families, divides_by_hand(root, path))
        for path in python_files(root)
    }


def record(root: Path) -> dict[str, Any]:
    """The record of a tree: the files with a count above zero, sorted."""
    files = {rel: shape for rel, shape in present(root).items() if any(shape.values())}
    return {"files": dict(sorted(files.items()))}


def record_at(root: Path, ref: str | None = None) -> dict[str, Any]:
    """The same record of the merge base's tree (CHECK_BASE, else origin/main), read from git: no file holds it."""
    ref = ref or base_ref()
    with tree_at(root, ref, ("src", "tools", "examples")) as base_root:
        base = record(base_root)
    return {**base, "files": carried(base["files"], root, ref)}


def ratchet(root: Path, base: dict[str, Any]) -> list[str]:
    """Every count of a file above the same file's at the merge base; a new file has none."""
    found: list[str] = []
    zero = dict.fromkeys(COUNTS, 0)
    for rel, shape in present(root).items():
        was = {**zero, **base["files"].get(rel, {})}
        for key in COUNTS:
            if shape[key] > was[key]:
                found.append(f"{rel}: {key.replace('_', ' ')} grew from {was[key]} to {shape[key]}")
    return found


def new_core_modules(root: Path, ref: str) -> list[str]:
    """The Python files under `core/` that the merge base does not hold."""
    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", resolved(root, ref), "--", CORE.as_posix()],
        capture_output=True,
        text=True,
        cwd=root,
        check=True,
    ).stdout.split()
    held = set(listed)
    now = sorted(p.relative_to(root).as_posix() for p in (root / CORE).rglob("*.py"))
    return [rel for rel in now if rel not in held]


def core_approval(new: list[str], body: str | None) -> list[str]:
    """A refusal per new module of `core/` when the pull request's body has no approval line."""
    if not new or any(line.lstrip().startswith(APPROVAL) for line in (body or "").splitlines()):
        return []
    return [
        f"{rel} is a new module of core/: add a line starting with {APPROVAL} naming Main Loop's approval "
        "to the pull request's body"
        for rel in new
    ]


def main() -> None:
    """Print every count above the merge base's; exit 1 when there is one."""
    found = ratchet(ROOT, record_at(ROOT))
    print("\n".join(found) or "the engine gates hold against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()

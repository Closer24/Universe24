"""The reviewer's recurring findings as gates (issue #1198, item 4 (a); the model owner, 2026-09-27).

Four gates, selected on every pull request by `tools/check.py`:

1. Numbers. A numeric literal beyond 0, 1, 2, 3, 4, 6 and 8, outside a docstring, is counted
   per file (the count of issue #1197). No file's count may grow, or stand above the merge
   base's baseline; a new file has none; a count that went down is re-recorded in the same
   commit (`python tools/engine_gates.py`).
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

Usage: `python tools/engine_gates.py` writes the baseline for the current tree.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE = Path("tests/engine_gates_baseline.json")
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
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or id(node) in docstrings:
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
    """The baseline of the current tree: the files with a count above zero, sorted."""
    files = {rel: shape for rel, shape in present(root).items() if any(shape.values())}
    return {"format": "engine-gates-baseline", "files": dict(sorted(files.items()))}


def ratchet(root: Path, baseline: dict[str, Any], base: dict[str, Any] | None = None) -> list[str]:
    """Every count that grew, stands above the merge base's, or went down without a re-record."""
    found: list[str] = []
    re_record = "re-record the baseline in this commit: python tools/engine_gates.py"
    zero = dict.fromkeys(COUNTS, 0)
    tree = present(root)
    # a count the merge base's baseline does not hold yet is compared with this baseline alone
    base_keys = set() if base is None else {k for e in base["files"].values() for k in e}
    for rel in sorted(set(baseline["files"]) - set(tree)):
        found.append(f"{rel} is in the baseline and not in the tree; {re_record}")
    for rel, shape in tree.items():
        recorded = {**zero, **baseline["files"].get(rel, {})}
        based = base["files"].get(rel, zero) if base is not None else recorded
        for key in COUNTS:
            name = key.replace("_", " ")
            if shape[key] > recorded[key]:
                found.append(f"{rel}: {name} grew from {recorded[key]} to {shape[key]}")
            elif shape[key] < recorded[key]:
                found.append(
                    f"{rel}: {name} went down from {recorded[key]} to {shape[key]}; {re_record}"
                )
            if key in base_keys and shape[key] > based.get(key, 0):
                found.append(
                    f"{rel}: {name} is {shape[key]}, above the merge base's {based.get(key, 0)}"
                )
    return found


def resolved(root: Path, ref: str) -> str:
    """The commit `ref` names; a ref git cannot resolve fails by name, never passes silently."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
            capture_output=True,
            text=True,
            cwd=root,
            check=True,
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        raise ValueError(
            f"the merge base {ref!r} cannot be resolved: fetch it or set CHECK_BASE"
        ) from None


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


def core_check_applies(environment: dict[str, str]) -> bool:
    """The approval is read on a pull request, or locally where PR_BODY is set; never on a push to main."""
    event = environment.get("GITHUB_EVENT_NAME")
    return event == "pull_request" or (event is None and "PR_BODY" in environment)


def base_ref() -> str:
    return os.environ.get("CHECK_BASE") or "origin/main"


def base_baseline(root: Path, ref: str) -> dict[str, Any] | None:
    """The baseline as the merge base holds it, or None where it has none yet; an unresolved base fails."""
    ref = resolved(root, ref)
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


def main() -> None:
    """Write the baseline for the current tree."""
    baseline = record(ROOT)
    (ROOT / BASELINE).write_text(json.dumps(baseline, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    totals = {key: sum(shape[key] for shape in baseline["files"].values()) for key in COUNTS}
    print(
        f"{len(baseline['files'])} files recorded: " + ", ".join(f"{k} {v}" for k, v in totals.items())
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

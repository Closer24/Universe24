"""The reviewer's recurring findings as gates (issue #1198, item 4 (a); the model owner, 2026-09-27).

Three gates on `src/`, selected on every pull request by `tools/check.py`:

1. Numbers. A numeric literal beyond 0, 1, 2, 3, 4, 6 and 8, outside a docstring, is counted
   per file (the count of issue #1197). No file's count may grow, or stand above the merge
   base's baseline; a new file has none, and a moved file (its name recorded under a path no
   longer in the tree) carries its old path's counts; a count that went down is re-recorded in
   the same commit (`python tools/engine_gates.py`).
2. Family names. A string literal equal to the name of a family declared in a world file under
   `examples/` is counted per file, on the same ratchet.
3. A new module of `core/`. A Python file under `src/event_universe/core/` that the merge base
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
COUNTS = ("numbers", "family_names")


def python_files(root: Path) -> list[Path]:
    base = root / PACKAGE
    return sorted(base.rglob("*.py")) if base.is_dir() else []


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


def counts_of(path: Path, families: frozenset[str]) -> dict[str, int]:
    """The two counts of one file: its numbers beyond the free ones and its family-name strings."""
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
    return {"numbers": numbers, "family_names": names}


def present(root: Path) -> dict[str, dict[str, int]]:
    families = family_names(root)
    return {path.relative_to(root).as_posix(): counts_of(path, families) for path in python_files(root)}


def record(root: Path) -> dict[str, Any]:
    """The baseline of the current tree: the files with a count above zero, sorted."""
    files = {rel: shape for rel, shape in present(root).items() if any(shape.values())}
    return {"format": "engine-gates-baseline", "files": dict(sorted(files.items()))}


def entry_of(
    rel: str, files: dict[str, dict[str, int]], tree: dict[str, dict[str, int]]
) -> dict[str, int]:
    """A file's recorded counts: under its path, else under the one recorded path with its name no longer in the tree (a moved file is not a new file), else zero."""
    if rel in files:
        return files[rel]
    moved = [path for path in files if path not in tree and Path(path).name == Path(rel).name]
    return files[moved[0]] if len(moved) == 1 else dict.fromkeys(COUNTS, 0)


def ratchet(root: Path, baseline: dict[str, Any], base: dict[str, Any] | None = None) -> list[str]:
    """Every count that grew, stands above the merge base's, or went down without a re-record."""
    found: list[str] = []
    re_record = "re-record the baseline in this commit: python tools/engine_gates.py"
    tree = present(root)
    for rel in sorted(set(baseline["files"]) - set(tree)):
        found.append(f"{rel} is in the baseline and not in the tree; {re_record}")
    for rel, shape in tree.items():
        recorded = entry_of(rel, baseline["files"], tree)
        based = entry_of(rel, base["files"], tree) if base is not None else recorded
        for key in COUNTS:
            name = key.replace("_", " ")
            if shape[key] > recorded[key]:
                found.append(f"{rel}: {name} grew from {recorded[key]} to {shape[key]}")
            elif shape[key] < recorded[key]:
                found.append(
                    f"{rel}: {name} went down from {recorded[key]} to {shape[key]}; {re_record}"
                )
            if shape[key] > based[key]:
                found.append(f"{rel}: {name} is {shape[key]}, above the merge base's {based[key]}")
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

"""No assert as a runtime guard and no module-level name nothing uses, in src/ and tools/ (the gate of #1198, gate 6).

An `assert` vanishes under `python -O`, so a check the engine relies on raises instead. The
asserts of today count per file against the merge base (CHECK_BASE, else origin/main) and may
only fall; a new file has none. A module-level name of src/ or tools/ that no file of src/,
tools/, tests/ or examples/ names again is refused outright.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARDED = ("src", "tools")
READERS = ("src", "tools", "tests", "examples")
WORD = re.compile(r"\b[A-Za-z_]\w*\b")


def asserts(text: str) -> int:
    return sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(text)))


def sources_at(ref: str | None) -> dict[str, str]:
    """Every Python file of src/ and tools/, in the working tree or at `ref`; a ref git cannot resolve fails by name."""
    if ref is None:
        return {
            p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
            for folder in GUARDED
            for p in sorted((ROOT / folder).rglob("*.py"))
        }
    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", *GUARDED],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if listed.returncode:
        raise ValueError(f"the merge base {ref!r} cannot be resolved: fetch it or set CHECK_BASE")
    names = [name for name in listed.stdout.split() if name.endswith(".py")]
    return {
        name: subprocess.run(
            ["git", "show", f"{ref}:{name}"], capture_output=True, text=True, cwd=ROOT
        ).stdout
        for name in names
    }


def grown_asserts(head: dict[str, str], base: dict[str, str]) -> list[str]:
    found = []
    for name, text in sorted(head.items()):
        now, was = asserts(text), asserts(base[name]) if name in base else 0
        if now > was:
            found.append(f"{name}: {now} assert, above the merge base's {was}; raise an error instead")
    return found


def unused_names(guarded: dict[str, str], corpus: str) -> list[str]:
    """The module-level names of `guarded` that the corpus names only once, at their definition."""
    words = Counter(WORD.findall(corpus))
    found = []
    for name, text in sorted(guarded.items()):
        for node in ast.parse(text).body:
            targets = (
                node.targets
                if isinstance(node, ast.Assign)
                else [node.target]
                if isinstance(node, ast.AnnAssign)
                else []
            )
            for target in targets:
                for leaf in ast.walk(target):
                    if (
                        isinstance(leaf, ast.Name)
                        and not leaf.id.startswith("__")
                        and words[leaf.id] <= 1
                    ):
                        found.append(f"{name}: the module-level name {leaf.id} is used nowhere")
    return found


def test_no_new_assert_and_no_unused_module_level_name():
    head = sources_at(None)
    assert grown_asserts(head, sources_at(os.environ.get("CHECK_BASE") or "origin/main")) == []
    corpus = "\n".join(
        p.read_text(encoding="utf-8") for folder in READERS for p in (ROOT / folder).rglob("*.py")
    )
    assert unused_names(head, corpus) == []


def test_a_new_assert_and_an_unused_name_fail():
    base = {"src/a.py": "def f(x):\n    assert x\n"}
    assert grown_asserts(base, base) == []
    head = {**base, "src/a.py": base["src/a.py"] + "    assert x > 1\n", "src/b.py": "assert True\n"}
    assert grown_asserts(head, base) == [
        "src/a.py: 2 assert, above the merge base's 1; raise an error instead",
        "src/b.py: 1 assert, above the merge base's 0; raise an error instead",
    ]
    guarded = {"src/c.py": "USED = 1\nLONELY: int = 2\n"}
    assert unused_names(guarded, guarded["src/c.py"] + "print(USED)\n") == [
        "src/c.py: the module-level name LONELY is used nowhere"
    ]

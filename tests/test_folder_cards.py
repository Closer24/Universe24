"""Every folder card loads together with the step file, and a card names its words (the gate of #1198, gate 3).

`discover()` imports every folder of the tree, and the shipped step file must name every built
primitive at its declared place. A folder reaches the loop through discovery only, so this test
is selected on every pull request. A `Declaration(...)` built by position in a folder counts
against the merge base (CHECK_BASE, else origin/main): the count may only fall, and a new folder
has none.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
from pathlib import Path

import pytest

from event_universe.core.register import discover
from event_universe.core.step import STEP_FILE, read_step

ROOT = Path(__file__).resolve().parents[1]
FEATURES = "src/event_universe/features"


def positional_cards(text: str) -> int:
    """The `Declaration(...)` calls of one file with a positional argument."""
    return sum(
        bool(node.args)
        for node in ast.walk(ast.parse(text))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Declaration"
    )


def cards_in_tree(root: Path) -> dict[str, int]:
    return {
        path.relative_to(root).as_posix(): positional_cards(path.read_text(encoding="utf-8"))
        for path in sorted((root / FEATURES).rglob("*.py"))
    }


def cards_at(ref: str) -> dict[str, int]:
    """The same count at `ref`; a ref git cannot resolve fails by name."""
    shown = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", FEATURES],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if shown.returncode:
        raise ValueError(f"the merge base {ref!r} cannot be resolved: fetch it or set CHECK_BASE")
    counts = {}
    for name in shown.stdout.split():
        if name.endswith(".py"):
            text = subprocess.run(
                ["git", "show", f"{ref}:{name}"], capture_output=True, text=True, cwd=ROOT
            ).stdout
            counts[name] = positional_cards(text)
    return counts


def grown(head: dict[str, int], base: dict[str, int]) -> list[str]:
    return [
        f"{rel}: {count} Declaration(...) by position, above the merge base's {base.get(rel, 0)}; name the words"
        for rel, count in sorted(head.items())
        if count > base.get(rel, 0)
    ]


def test_every_folder_loads_and_the_step_file_names_every_built_primitive():
    register = discover()
    step = read_step(json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8")), "d")
    register.check_step(step)
    register.check_writers(step)


def test_no_folder_card_is_built_by_position_beyond_the_merge_base():
    assert grown(cards_in_tree(ROOT), cards_at(os.environ.get("CHECK_BASE") or "origin/main")) == []


def test_a_card_by_position_and_a_built_folder_missing_from_the_step_file_fail(tmp_path):
    keywords = 'D = Declaration(name="the wait", place="(i)", reads=(), writes=(), section="s")\n'
    by_position = 'D = Declaration("the wait", "(i)", (), (), None, "s")\n'
    assert positional_cards(keywords) == 0 and positional_cards(by_position) == 1
    assert grown({"f/a.py": 1, "f/b.py": 0}, {"f/a.py": 1}) == []
    assert grown({"f/new.py": 1}, {}) == [
        "f/new.py: 1 Declaration(...) by position, above the merge base's 0; name the words"
    ]
    register = discover()
    shipped = json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8"))
    built = set(register.built_names())
    shipped["interval"] = [act for act in shipped["interval"] if act[1] != sorted(built)[0]]
    with pytest.raises(ValueError, match="leaves out the built primitive"):
        register.check_step(read_step(shipped, "d"))

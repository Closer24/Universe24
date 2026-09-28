"""The reviewer's recurring findings as gates: no new number, no family name and no unapproved core module in src/ (tools/engine_gates.py; issue #1198 item 4 (a))."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
PACKAGE, GATES = "src/event_universe", load_file("engine_gates", ROOT / "tools" / "engine_gates.py")
BASE = load_file("merge_base", ROOT / "tools" / "merge_base.py")


def tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


WORLD = {"examples/world.json": json.dumps({"universe": {"families": [{"name": "glow"}]}})}


def test_the_tree_holds_against_the_merge_base_and_a_new_core_module_is_approved():
    """Every file of src/ holds each count at or below the merge base's, read from git; a new module of core/ on a pull request has the approval line."""
    ref = GATES.base_ref()
    assert GATES.ratchet(ROOT, GATES.record_at(ROOT, ref)) == []
    if BASE.on_pull_request(dict(os.environ)):
        new = GATES.new_core_modules(ROOT, ref)
        assert GATES.core_approval(new, os.environ.get("PR_BODY")) == []


def test_a_new_number_or_family_name_fails_against_the_merge_base_and_a_cut_passes(tmp_path):
    root = tree(tmp_path, {**WORLD, f"{PACKAGE}/a.py": '"""Doc 12."""\nX = 3\nY = 64\nZ = "glow"\n'})
    base = GATES.record(root)
    assert base["files"] == {f"{PACKAGE}/a.py": {"numbers": 1, "family_names": 1, "hand_divisions": 0}}
    assert GATES.ratchet(root, base) == []
    (root / PACKAGE / "a.py").write_text(
        'X = 3\nY = 64\nW = 2 ** 10\nZ = "glow"\nV = "glow"\nU = 4 * 8 + 8\nT = 1 << (6 * 8)\nS = -3 + a\n'
    )
    found = GATES.ratchet(root, base)  # 2 ** 10, 4 * 8 + 8 and 1 << (6 * 8) fold to one number each
    assert f"{PACKAGE}/a.py: numbers grew from 1 to 4" in found
    assert f"{PACKAGE}/a.py: family names grew from 1 to 2" in found
    (root / PACKAGE / "a.py").write_text("X = 3\nFLAG = True\n")
    assert GATES.ratchet(root, base) == []
    tree(root, {f"{PACKAGE}/b.py": "Q = 64\n"})
    assert GATES.ratchet(root, base) == [f"{PACKAGE}/b.py: numbers grew from 0 to 1"]


def test_a_new_core_module_needs_the_approval_line():
    new = [f"{PACKAGE}/core/main_loop.py"]
    assert GATES.core_approval([], None) == []
    assert "new module of core/" in GATES.core_approval(new, "Adds the loop.")[0]
    assert GATES.core_approval(new, "Adds the loop.\nAPPROVED-CORE: Main Loop, 2026-09-27\n") == []


def test_the_core_check_runs_on_a_pull_request_and_never_on_a_push_to_main():
    assert BASE.on_pull_request({"GITHUB_EVENT_NAME": "pull_request", "PR_BODY": ""})
    assert not BASE.on_pull_request({"GITHUB_EVENT_NAME": "push", "PR_BODY": ""})
    assert BASE.on_pull_request({"PR_BODY": "local"}) and not BASE.on_pull_request({})


def test_an_approval_counts_only_at_a_lines_start():
    new = [f"{PACKAGE}/core/main_loop.py"]
    assert GATES.core_approval(new, "NOT-APPROVED-CORE: Main Loop said no\n") != []
    assert GATES.core_approval(new, "  APPROVED-CORE: Main Loop, 2026-09-27\n") == []


def test_a_merge_base_that_cannot_be_resolved_fails_by_name():
    for check in (GATES.record_at, GATES.new_core_modules):
        with pytest.raises(ValueError, match="'deadbeef' cannot be resolved"):
            check(ROOT, "deadbeef")


def test_a_division_by_hand_in_a_folder_fails_and_rule3_and_a_string_format_do_not_count(tmp_path):
    folder = f"{PACKAGE}/features/hold/__init__.py"
    root = tree(tmp_path, {**WORLD, folder: "def f(a, b):\n    return a + b\n"})
    baseline = GATES.record(root)
    assert baseline["files"] == {}
    (root / folder).write_text("def f(a, b):\n    q, r = divmod(a, b)\n    return a // b + a % b + q\n")
    tree(
        root,
        {
            f"{PACKAGE}/core/rule3.py": "def rule3(u, w):\n    return u // w, u % w\n",
            f"{PACKAGE}/events/log.py": 'def line(x):\n    return "%d" % x\n',
        },
    )
    assert GATES.ratchet(root, baseline) == [f"{folder}: hand divisions grew from 0 to 3"]
    tree(root, {"tools/body_generator.py": "def seed(a):\n    a //= 2\n    return a\n"})
    assert "tools/body_generator.py: hand divisions grew from 0 to 1" in GATES.ratchet(root, baseline)

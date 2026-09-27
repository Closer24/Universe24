"""The reviewer's recurring findings as gates: no new number, no family name and no unapproved core module in src/ (tools/engine_gates.py; issue #1198 item 4 (a))."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "src/event_universe"


def tool():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("engine_gates", ROOT / "tools" / "engine_gates.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["engine_gates"] = module
    spec.loader.exec_module(module)
    return module


GATES = tool()


def tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


WORLD = {"examples/world.json": json.dumps({"universe": {"families": [{"name": "glow"}]}})}


def test_the_tree_is_at_its_baseline_and_a_new_core_module_is_approved():
    """Every file of src/ stands at its recorded counts, none above the merge base's; a new module of core/ on a pull request has the approval line."""
    baseline = json.loads((ROOT / GATES.BASELINE).read_text(encoding="utf-8"))
    assert baseline["format"] == "engine-gates-baseline"
    ref = GATES.base_ref()
    assert GATES.ratchet(ROOT, baseline, GATES.base_baseline(ROOT, ref)) == []
    if GATES.core_check_applies(dict(os.environ)):
        new = GATES.new_core_modules(ROOT, ref)
        assert GATES.core_approval(new, os.environ.get("PR_BODY")) == []


def test_a_new_number_or_family_name_fails_and_a_removed_one_asks_for_the_re_record(tmp_path):
    root = tree(tmp_path, {**WORLD, f"{PACKAGE}/a.py": '"""Doc 12."""\nX = 3\nY = 64\nZ = "glow"\n'})
    baseline = GATES.record(root)
    assert baseline["files"] == {f"{PACKAGE}/a.py": {"numbers": 1, "family_names": 1}}
    assert GATES.ratchet(root, baseline) == []
    (root / PACKAGE / "a.py").write_text('X = 3\nY = 64\nW = 2 ** 10\nZ = "glow"\nV = "glow"\n')
    found = GATES.ratchet(root, baseline)
    assert f"{PACKAGE}/a.py: numbers grew from 1 to 2" in found
    assert f"{PACKAGE}/a.py: family names grew from 1 to 2" in found
    (root / PACKAGE / "a.py").write_text("X = 3\nFLAG = True\n")
    assert any(
        "numbers went down from 1 to 0; re-record" in line for line in GATES.ratchet(root, baseline)
    )
    tree(root, {f"{PACKAGE}/b.py": "Q = 64\n"})
    assert f"{PACKAGE}/b.py: numbers grew from 0 to 1" in GATES.ratchet(
        root, GATES.record(root) | {"files": {}}
    )


def test_a_baseline_raised_in_the_same_commit_is_refused_against_the_merge_base(tmp_path):
    root = tree(tmp_path, {**WORLD, f"{PACKAGE}/a.py": "Y = 64\n"})
    base = GATES.record(root)
    (root / PACKAGE / "a.py").write_text("Y = 64\nZ = 500\n")
    raised = GATES.record(root)
    assert GATES.ratchet(root, raised) == []
    assert GATES.ratchet(root, raised, base) == [
        f"{PACKAGE}/a.py: numbers is 2, above the merge base's 1"
    ]


def test_a_new_core_module_needs_the_approval_line():
    new = [f"{PACKAGE}/core/main_loop.py"]
    assert GATES.core_approval([], None) == []
    assert "new module of core/" in GATES.core_approval(new, "Adds the loop.")[0]
    assert (
        GATES.core_approval(new, "Adds the loop.\nAPPROVED-CORE: Main Loop, review of 2026-09-27\n")
        == []
    )


def test_the_core_check_runs_on_a_pull_request_and_never_on_a_push_to_main():
    assert GATES.core_check_applies({"GITHUB_EVENT_NAME": "pull_request", "PR_BODY": ""})
    assert not GATES.core_check_applies({"GITHUB_EVENT_NAME": "push", "PR_BODY": ""})
    assert GATES.core_check_applies({"PR_BODY": "local"})
    assert not GATES.core_check_applies({})


def test_an_approval_counts_only_at_a_lines_start():
    new = [f"{PACKAGE}/core/main_loop.py"]
    assert GATES.core_approval(new, "NOT-APPROVED-CORE: Main Loop said no\n") != []
    assert GATES.core_approval(new, "  APPROVED-CORE: Main Loop, 2026-09-27\n") == []


def test_a_merge_base_that_cannot_be_resolved_fails_by_name():
    for check in (GATES.base_baseline, GATES.new_core_modules):
        with pytest.raises(ValueError, match="'deadbeef' cannot be resolved"):
            check(ROOT, "deadbeef")

"""Guard canonical files and configurations; not a proof of semantic uniqueness."""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from .test_repository_language import repository_files


def duplicate_files(root, *, normalized_json=False, ignore_run_duration=False):
    assert not ignore_run_duration or normalized_json
    groups = defaultdict(list)
    for path in repository_files(root):
        if normalized_json and path.suffix != ".json":
            continue
        content = path.read_bytes()
        if not content.strip():
            continue  # Empty package markers carry no duplicated implementation.
        if normalized_json:
            definition = json.loads(content)
            if (
                ignore_run_duration
                and isinstance(definition, dict)
                and "disturbance_types" in definition
            ):
                definition.pop("ticks", None)
            content = json.dumps(definition, sort_keys=True, separators=(",", ":")).encode()
        groups[hashlib.sha256(content).hexdigest()].append(path.relative_to(root).as_posix())
    return sorted(sorted(paths) for paths in groups.values() if len(paths) > 1)


def test_nonempty_repository_files_have_one_canonical_copy():
    assert not duplicate_files(Path(__file__).resolve().parents[1])


def test_json_configurations_have_one_canonical_copy_independent_of_formatting():
    assert not duplicate_files(Path(__file__).resolve().parents[1], normalized_json=True)


def test_duplicate_gate_detects_copies_but_allows_empty_package_markers(tmp_path):
    (tmp_path / "first.py").write_text("def transport(): return 1\n", encoding="utf-8")
    nested = tmp_path / "component"
    nested.mkdir()
    (nested / "second.py").write_text("def transport(): return 1\n", encoding="utf-8")
    (tmp_path / "__init__.py").touch()
    (nested / "__init__.py").touch()
    assert duplicate_files(tmp_path) == [["component/second.py", "first.py"]]
    (nested / "second.py").write_text("def receive(): return 2\n", encoding="utf-8")
    assert not duplicate_files(tmp_path)


def test_json_gate_ignores_object_key_order_but_preserves_semantic_array_order(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text('{"operations": [1, 2], "cost": 3}', encoding="utf-8")
    second.write_text('{"cost": 3,\n "operations": [1, 2]}', encoding="utf-8")
    assert not duplicate_files(tmp_path)
    assert duplicate_files(tmp_path, normalized_json=True) == [["first.json", "second.json"]]
    second.write_text('{"cost": 3, "operations": [2, 1]}', encoding="utf-8")
    assert not duplicate_files(tmp_path, normalized_json=True)


def test_run_duration_does_not_justify_a_duplicate_initialization():
    assert not duplicate_files(
        Path(__file__).resolve().parents[1], normalized_json=True, ignore_run_duration=True
    )


def test_duration_gate_rejects_copies_but_retains_distinct_operation_budgets(tmp_path):
    first = {"disturbance_types": [], "ticks": 100, "normal_budget": 10}
    second = {"disturbance_types": [], "ticks": 120, "normal_budget": 10}
    (tmp_path / "first.json").write_text(json.dumps(first), encoding="utf-8")
    (tmp_path / "second.json").write_text(json.dumps(second), encoding="utf-8")
    assert not duplicate_files(tmp_path, normalized_json=True)
    assert duplicate_files(tmp_path, normalized_json=True, ignore_run_duration=True) == [
        ["first.json", "second.json"]
    ]
    second["normal_budget"] = 2
    (tmp_path / "second.json").write_text(json.dumps(second), encoding="utf-8")
    assert not duplicate_files(tmp_path, normalized_json=True, ignore_run_duration=True)

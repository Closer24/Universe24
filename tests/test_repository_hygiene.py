"""Guard canonical files and configurations; not a proof of semantic uniqueness."""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from .test_repository_language import repository_files


def duplicate_files(root, *, normalized_json=False):
    groups = defaultdict(list)
    for path in repository_files(root):
        if normalized_json and path.suffix != ".json":
            continue
        content = path.read_bytes()
        if not content.strip():
            continue  # Empty package markers carry no duplicated implementation.
        if normalized_json:
            content = json.dumps(json.loads(content), sort_keys=True, separators=(",", ":")).encode()
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

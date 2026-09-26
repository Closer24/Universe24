"""THE CANCELLED PATHS (docs/CANCELLED_WORLDS.md; the model owner's records 1875 and 2095, the
Boss's records 2102, 2107 and 2133 of 2026-09-26): the ray law's paths are marked cancelled in
one document and disconnected from the gate and from the change selector; nothing is deleted
and no living test is skipped. The list is the document's tables, read once by
`tools/cancelled_paths.py` for the gate (`tests/conftest.py`), the selector (`tools/check.py`)
and this test. Every number here is a HOST count."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CANCELLED = load("cancelled_paths")
SECTIONS = ("folders", "tests", "modules", "partial", "documents")


def test_every_section_has_rows_and_every_listed_path_exists_nothing_deleted():
    for section in SECTIONS:
        paths = CANCELLED.cancelled_paths(section)
        assert paths, section
        assert len(set(paths)) == len(paths), f"{section}: a path listed twice"
        for path in paths:
            assert (ROOT / path).exists(), f"{path} is listed and must exist: nothing is deleted"
    folders = CANCELLED.cancelled_paths("folders")
    assert all(path.startswith("examples/events/") and (ROOT / path).is_dir() for path in folders)
    assert all(path.startswith("tests/test_") for path in CANCELLED.cancelled_paths("tests"))
    assert all(path.endswith(".md") for path in CANCELLED.cancelled_paths("documents"))


def test_a_section_without_rows_is_refused(tmp_path: Path):
    document = tmp_path / "CANCELLED.md"
    document.write_text(
        "# x\n\n## 2. folders\n\n| Path | Note |\n| --- | --- |\n\n## 3. tests\n\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="no table rows"):
        CANCELLED.cancelled_paths("folders", document)
    document.write_text(
        "## 3. t\n\n| Path | Note |\n| --- | --- |\n| `tests/test_a.py` | x |\n", encoding="utf-8"
    )
    assert CANCELLED.cancelled_paths("tests", document) == ("tests/test_a.py",)


def test_is_cancelled_reads_whole_paths_and_folders_not_partial_modules():
    assert CANCELLED.is_cancelled("tests/test_amplitude_click.py")
    assert CANCELLED.is_cancelled("examples/events/bell/bell_a0b0.json")
    assert CANCELLED.is_cancelled("src/event_universe/events/engine.py")
    assert not CANCELLED.is_cancelled("src/event_universe/events/world.py")  # in part: it stays
    assert not CANCELLED.is_cancelled("src/event_universe/events/detector_law.py")
    assert not CANCELLED.is_cancelled("examples/events/massive_record/light_clock.json")


def test_no_cancelled_test_is_collected_and_the_living_ones_are(request):
    cancelled = set(CANCELLED.cancelled_paths("tests"))
    collected = {Path(item.fspath).relative_to(ROOT).as_posix() for item in request.session.items}
    assert not collected & cancelled, sorted(collected & cancelled)
    living = {p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py")} - cancelled
    assert "tests/test_cancelled_paths.py" in living
    # every cancelled file is a real file: the gate ignores it, it does not lose it
    assert all((ROOT / path).is_file() for path in cancelled)


def test_the_change_selector_never_names_a_cancelled_test():
    check = load("check")
    cancelled = set(CANCELLED.cancelled_paths("tests"))
    sources = {
        p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
        for directory in ("src", "tests", "tools")
        for p in (ROOT / directory).rglob("*.py")
        if "reference" not in p.parts
    }
    changed = [
        "src/event_universe/events/engine.py",
        "src/event_universe/events/world.py",
        "examples/events/amplitude/expectations.json",
        "tests/conftest.py",
    ]
    tests, _ = check.select(changed, sources)
    assert not set(tests) & cancelled, sorted(set(tests) & cancelled)
    assert "tests/test_cancelled_paths.py" in tests  # conftest changes select every living test


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def test_no_living_module_imports_a_wholly_cancelled_module_beyond_the_named_lines():
    cancelled_modules = {
        path[len("src/") : -len(".py")].replace("/", ".")
        for path in CANCELLED.cancelled_paths("modules")
        if path.startswith("src/") and path.endswith(".py")
    }
    listed = set(CANCELLED.cancelled_paths("modules")) | set(CANCELLED.cancelled_paths("partial"))
    offenders = {}
    for path in (ROOT / "src").rglob("*.py"):
        rel = path.relative_to(ROOT).as_posix()
        if rel in listed:
            continue
        hits = {
            m
            for m in imported_modules(path)
            if m in cancelled_modules or m.rsplit(".", 1)[0] in cancelled_modules
        }
        if hits:
            offenders[rel] = sorted(hits)
    assert offenders == {}, offenders

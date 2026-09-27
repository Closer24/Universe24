"""THE RATCHET ON THE SHAPE OF THE CODE (the model owner's decisions through the Boss, records
2239 and 2241; skills/workflow.md, the short procedure, point 11). tools/record_code_shape.py
counts, per file of src/, the lines, the docstring lines, the comment lines, the references to
records or decisions, the sites of Rule3's arithmetic outside its one function and the sites that
shift an array across Nodes, and per file of src/, tools/ and tests/ the names imported from the
loop's module beyond its public entry. A file within the limits (one-line docstrings, no record
reference, under 400 lines, none of the three sites) passes whatever its counts (the Boss's word
of 18:11Z: the rule never blocks a feature folder that fills within them); a file beyond them is
compared with tests/code_shape_baseline.json and with the merge base's copy of it: no count may
grow or stand above the merge base's (a baseline raised in the same commit is refused), a count
that went down is re-recorded in the same commit, and a new file beyond them fails. Two functions of src/ with one abstracted body fail beyond the baseline's
groups. The import contracts hold with no baseline. Selected on every pull request."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tool():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(
        "record_code_shape", ROOT / "tools" / "record_code_shape.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["record_code_shape"] = module
    spec.loader.exec_module(module)
    return module


SHAPE = tool()
BASELINE = json.loads((ROOT / SHAPE.BASELINE).read_text(encoding="utf-8"))
PACKAGE = "src/event_universe"


def test_the_tree_is_at_the_baseline_and_keeps_the_import_contracts():
    """Every count of every file of src/ equals its baseline, no new duplicate, no new import of
    the loop's internals, every feature on core/ alone, core/ on itself alone."""
    assert BASELINE["format"] == "code-shape-baseline"
    base = SHAPE.base_baseline(ROOT)
    assert SHAPE.violations(ROOT, BASELINE, base) == []
    present = {SHAPE.relative(ROOT, p): SHAPE.shape_of(ROOT, p) for p in SHAPE.python_files(ROOT, "src")}
    beyond = {rel for rel, shape in present.items() if SHAPE.beyond_the_limits(rel, shape)}
    assert set(BASELINE["files"]) == beyond and "recorded_at" not in BASELINE
    assert list(BASELINE["files"]) == sorted(BASELINE["files"])


def tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


SMALL = {
    f"{PACKAGE}/__init__.py": "",
    f"{PACKAGE}/core/__init__.py": "",
    # a.py is beyond the limits (a two-line docstring), so it ratchets; b.py stays within them
    f"{PACKAGE}/core/a.py": '"""Two\nlines."""\n\n\ndef f(x):\n    # a comment\n    y = x + 1\n    return y\n',
}


def test_a_grown_count_fails_and_a_lowered_count_asks_for_the_re_record(tmp_path):
    root = tree(tmp_path, SMALL)
    baseline = SHAPE.record(root)
    assert SHAPE.violations(root, baseline) == []
    path = root / PACKAGE / "core" / "a.py"
    path.write_text(path.read_text() + "# one more comment\n", encoding="utf-8")
    found = SHAPE.violations(root, baseline)
    assert any("comment lines grew from 1 to 2" in line for line in found)
    assert any("lines grew from 8 to 9" in line for line in found)
    path.write_text(SMALL[f"{PACKAGE}/core/a.py"].replace("    # a comment\n", ""), encoding="utf-8")
    found = SHAPE.violations(root, baseline)
    assert any("comment lines went down from 1 to 0; re-record" in line for line in found)
    path.unlink()
    assert any("not in the tree; re-record" in line for line in SHAPE.violations(root, baseline))


def test_a_baseline_raised_in_the_same_commit_is_refused_against_the_merge_base(tmp_path):
    """The Boss's hole of 19:33Z: a pull request that grows a file beyond the limits and
    re-records its own baseline passes against that baseline and fails against the merge base's."""
    root = tree(tmp_path, SMALL)
    base = SHAPE.record(root)
    path = root / PACKAGE / "core" / "a.py"
    path.write_text(path.read_text() + "# one more comment\n# and another\n", encoding="utf-8")
    raised = SHAPE.record(root)
    assert SHAPE.violations(root, raised) == []
    found = SHAPE.violations(root, raised, base)
    assert any("comment lines is 3, above the merge base's 1" in line for line in found)
    assert any("lines is 10, above the merge base's 8" in line for line in found)
    # a file within the limits is free of the base too; a cut below the base passes
    path.write_text('"""One line."""\n\n\ndef f(x):\n    return x\n', encoding="utf-8")
    assert SHAPE.violations(root, SHAPE.record(root), base) == []


def test_a_moved_file_beyond_the_limits_ratchets_against_its_old_entry(tmp_path):
    """A file beyond the limits that moves to another folder is not new: it is compared with
    its old path's entry (a count that grew fails, the same counts ask for the re-record), in
    the baseline and against the merge base alike."""
    root = tree(tmp_path, SMALL)
    baseline = SHAPE.record(root)
    old = root / PACKAGE / "core" / "a.py"
    new = root / PACKAGE / "features" / "a.py"
    text = old.read_text(encoding="utf-8")
    old.unlink()
    new.parent.mkdir(parents=True, exist_ok=True)
    new.write_text(text, encoding="utf-8")
    found = SHAPE.violations(root, baseline, baseline)
    assert not any("is new" in line for line in found)
    assert any("core/a.py is in the baseline and not in the tree" in line for line in found)
    new.write_text(text + "# one more comment\n", encoding="utf-8")
    found = SHAPE.violations(root, baseline, baseline)
    assert any("features/a.py: comment lines grew from 1 to 2" in line for line in found)
    assert any("features/a.py: comment lines is 2, above the merge base's 1" in line for line in found)


def test_a_new_file_meets_the_limits_from_its_first_commit(tmp_path):
    root = tree(tmp_path, SMALL)
    baseline = SHAPE.record(root)
    tree(
        root,
        {
            f"{PACKAGE}/core/b.py": '"""Two\nlines (record 2239)."""\n'
            + "\n".join(f"x{i} = {i}" for i in range(400))
            + "\nwall * before\nnp.roll(x0, 1)\n"
        },
    )
    found = SHAPE.violations(root, baseline)
    assert any("has 1 docstring(s) beyond one line and is new" in line for line in found)
    assert any("refers to 1 record(s) or decision(s) and is new" in line for line in found)
    assert any("has 404 lines (the limit 400) and is new" in line for line in found)
    assert any("has 1 rule arithmetic sites and is new" in line for line in found)
    assert any("has 1 level shift sites and is new" in line for line in found)
    good = '"""One line."""\n\n\ndef g(a):\n    return a\n'
    (root / PACKAGE / "core" / "b.py").write_text(good, encoding="utf-8")
    assert SHAPE.violations(root, baseline) == []


def test_a_feature_stub_grown_within_the_limits_passes_and_beyond_them_fails(tmp_path):
    """The Boss's word of 18:11Z: a stub of 26 lines in the baseline grows to 151 lines within
    the limits and passes; the same file with a two-line docstring is beyond them and ratchets."""
    stub = (
        '"""One line."""\n\nfrom event_universe.core.register import Declaration\n\n'
        + "\n" * 21
        + "X = 1\n"
    )
    root = tree(
        tmp_path,
        {**SMALL, f"{PACKAGE}/features/__init__.py": "", f"{PACKAGE}/features/stub/__init__.py": stub},
    )
    baseline = SHAPE.record(root)
    # a file within the limits has no entry in the baseline (the Boss's word of 21:09Z)
    assert f"{PACKAGE}/features/stub/__init__.py" not in baseline["files"]
    assert set(baseline["files"]) == {f"{PACKAGE}/core/a.py"} and "recorded_at" not in baseline
    grown = (
        '"""One line."""\n\nfrom event_universe.core.register import Declaration\n\n\n'
        + "".join(
            f'def f{i}(x):\n    """What f{i} does (ALGEBRA.md 9.1)."""\n    return x + {i}\n\n\n'
            for i in range(29)
        )
        + "X = 1\n"
    )
    path = root / PACKAGE / "features" / "stub" / "__init__.py"
    path.write_text(grown, encoding="utf-8")
    assert len(grown.splitlines()) == 151
    assert SHAPE.violations(root, baseline) == []
    path.write_text(grown.replace('"""One line."""', '"""Two\nlines."""', 1), encoding="utf-8")
    found = SHAPE.violations(root, baseline)
    assert any("has 1 docstring(s) beyond one line and is new" in line for line in found)


def test_two_functions_with_one_abstracted_body_fail_beyond_the_baseline(tmp_path):
    twin = (
        '"""One line."""\n\n\ndef first(alpha, beta):\n    total = alpha * 2 + beta\n    return total\n\n\n'
        'def second(p, q):\n    """A docstring."""\n    s = p * 7 + q\n    return s\n'
    )
    root = tree(tmp_path, {**SMALL, f"{PACKAGE}/core/c.py": twin})
    baseline = SHAPE.record(root)
    (groups,) = baseline["duplicates"].values()
    assert groups == [f"{PACKAGE}/core/c.py:first", f"{PACKAGE}/core/c.py:second"]
    fresh = {k: v for k, v in baseline.items() if k != "duplicates"} | {"duplicates": {}}
    found = SHAPE.violations(root, fresh)
    assert any("duplicate functions" in line and "first" in line and "second" in line for line in found)
    assert SHAPE.violations(root, baseline) == []
    third = twin + "\n\ndef third(u, v):\n    w = u * 9 + v\n    return w\n"
    (root / PACKAGE / "core" / "c.py").write_text(third, encoding="utf-8")
    assert any(
        "duplicate functions" in line and "third" in line for line in SHAPE.violations(root, baseline)
    )
    # a body of one statement is below the threshold: two one-line accessors are not duplicates
    (root / PACKAGE / "core" / "c.py").write_text(
        '"""One line."""\n\n\ndef a(x):\n    return x.p\n\n\ndef b(y):\n    return y.q\n',
        encoding="utf-8",
    )
    assert SHAPE.duplicates(root) == {}


def test_a_feature_importing_another_feature_or_core_importing_a_feature_fails(tmp_path):
    root = tree(
        tmp_path,
        {
            **SMALL,
            f"{PACKAGE}/features/__init__.py": "",
            f"{PACKAGE}/features/hold/__init__.py": "from event_universe.core.a import f\n",
            f"{PACKAGE}/features/send/__init__.py": "from event_universe.features.hold import f\n",
            f"{PACKAGE}/features/wait/__init__.py": "from event_universe.events.detector_law import DetectorLawSimulation\n",
            f"{PACKAGE}/core/d.py": "from event_universe.features.hold import f\n",
            f"{PACKAGE}/events/__init__.py": "",
            f"{PACKAGE}/events/detector_law.py": "class DetectorLawSimulation:\n    pass\n\n\ndef _inner():\n    pass\n",
        },
    )
    found = SHAPE.contract_violations(root)
    assert found == [
        f"{PACKAGE}/core/d.py imports event_universe.features.hold: core/ imports nothing outside core/",
        f"{PACKAGE}/features/send/__init__.py imports event_universe.features.hold: a feature imports core/ alone",
        f"{PACKAGE}/features/wait/__init__.py imports event_universe.events.detector_law: a feature imports core/ alone",
    ]


def test_an_import_of_the_loops_internals_outside_core_fails(tmp_path):
    root = tree(
        tmp_path,
        {
            **SMALL,
            f"{PACKAGE}/events/__init__.py": "",
            f"{PACKAGE}/events/detector_law.py": "class DetectorLawSimulation:\n    pass\n\n\ndef _inner():\n    pass\n",
            "tools/run.py": "from event_universe.events.detector_law import DetectorLawSimulation\n",
        },
    )
    baseline = SHAPE.record(root)
    assert baseline["loop_internal_imports"] == {}  # the public entry is no internal
    (root / "tools" / "run.py").write_text(
        "from event_universe.events.detector_law import _inner\n", encoding="utf-8"
    )
    found = SHAPE.violations(root, baseline)
    assert found == ["tools/run.py imports the loop's internals _inner: nothing outside core/ does"]
    (root / "tools" / "run.py").write_text(
        "import event_universe.events.detector_law\n", encoding="utf-8"
    )
    assert SHAPE.violations(root, baseline) == [
        "tools/run.py imports the loop's internals *: nothing outside core/ does"
    ]

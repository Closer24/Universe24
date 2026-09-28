"""The shape of the code holds against the merge base, read from git (tools/record_code_shape.py; #1198, gate 7): a file beyond the limits grows no count (the sites writing a level onto the GameBoard among them, the write's gate), a new one stays within them, no new copied function, no new importer of the loop's internals, and the import contracts hold; no baseline file is kept."""

import subprocess
from pathlib import Path

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]


def tool():  # type: ignore[no-untyped-def]
    return load_file("record_code_shape", ROOT / "tools" / "record_code_shape.py")


SHAPE, PACKAGE = tool(), "src/event_universe"


def test_the_tree_keeps_its_shape_against_the_merge_base_and_no_baseline_file_is_kept():
    assert SHAPE.violations(ROOT, SHAPE.record_at(ROOT)) == []
    assert not [p for p in (ROOT / "tests").glob("*baseline*.json")]


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


def test_a_grown_count_fails_against_the_merge_base_and_a_cut_passes(tmp_path):
    root = tree(tmp_path, SMALL)
    base = SHAPE.record(root)
    assert SHAPE.violations(root, base) == []
    path = root / PACKAGE / "core" / "a.py"
    path.write_text(path.read_text() + "# one more comment\n", encoding="utf-8")
    found = SHAPE.violations(root, base)
    assert any("comment lines grew from 1 to 2" in line for line in found)
    assert any("lines grew from 8 to 9" in line for line in found)
    path.write_text(SMALL[f"{PACKAGE}/core/a.py"].replace("    # a comment\n", ""), encoding="utf-8")
    assert SHAPE.violations(root, base) == []


def test_a_new_file_meets_the_limits_from_its_first_commit(tmp_path):
    root = tree(tmp_path, SMALL)
    baseline = SHAPE.record(root)
    beyond = (
        "\n".join(f"x{i} = {i}" for i in range(400))
        + "\nwall * before\nnp.roll(x0, 1)\nlive.now[x0] += x1\n"
    )
    tree(root, {f"{PACKAGE}/core/b.py": '"""Two\nlines (record 2239)."""\n' + beyond})
    found = SHAPE.violations(root, baseline)
    assert any("has 1 docstring(s) beyond one line and is new" in line for line in found)
    assert any("refers to 1 record(s) or decision(s) and is new" in line for line in found)
    assert any("has 405 lines (the limit 400) and is new" in line for line in found)
    assert any("has 1 rule arithmetic sites and is new" in line for line in found)
    assert any("has 1 level shift sites and is new" in line for line in found)
    assert any("has 1 level write sites and is new" in line for line in found)
    good = '"""One line."""\n\n\ndef g(a):\n    return a\n'
    (root / PACKAGE / "core" / "b.py").write_text(good, encoding="utf-8")
    assert SHAPE.violations(root, baseline) == []


def test_a_feature_stub_grown_within_the_limits_passes_and_beyond_them_fails(tmp_path):
    """The Boss's word of 18:11Z: a stub of 26 lines in the baseline grows to 151 lines within the limits and passes; the same file with a two-line docstring is beyond them and ratchets."""
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
            f'def f{i}(x):\n    """What f{i} does (ALGEBRA.md #what-a-body-is)."""\n    return x + {i}\n\n\n'
            for i in range(29)
        )
        + "X = 1\n"
    )
    path = root / PACKAGE / "features" / "stub" / "__init__.py"
    path.write_text(grown, encoding="utf-8")
    assert len(grown.splitlines()) == 151 and SHAPE.violations(root, baseline) == []
    path.write_text(grown.replace('"""One line."""', '"""Two\nlines."""', 1), encoding="utf-8")
    found = SHAPE.violations(root, baseline)
    assert any("has 1 docstring(s) beyond one line and is new" in line for line in found)


def test_two_functions_with_one_abstracted_body_fail_beyond_the_merge_base(tmp_path):
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
    assert found == [
        "the loop's internal _inner is imported by 1 files, above the merge base's 0: nothing outside core/ imports it"
    ]
    (root / "tools" / "run.py").write_text(
        "import event_universe.events.detector_law\n", encoding="utf-8"
    )
    assert SHAPE.violations(root, baseline) == [
        "the loop's internal * is imported by 1 files, above the merge base's 0: nothing outside core/ imports it"
    ]


def test_a_moved_import_of_the_loops_internals_keeps_the_count_and_a_new_importer_fails(tmp_path):
    loop = f"{PACKAGE}/events/detector_law.py"
    root = tree(
        tmp_path,
        {
            **SMALL,
            f"{PACKAGE}/events/__init__.py": "",
            loop: "def _inner():\n    pass\n",
            "tests/test_a.py": "from event_universe.events.detector_law import _inner\n",
        },
    )
    base = SHAPE.record(root)
    (root / "tests" / "test_a.py").write_text("X = 1\n", encoding="utf-8")
    tree(root, {"tests/helpers.py": "from event_universe.events.detector_law import _inner\n"})
    assert SHAPE.violations(root, base) == []
    tree(root, {"tests/test_b.py": "from event_universe.events.detector_law import _inner\n"})
    assert SHAPE.violations(root, base) == [
        "the loop's internal _inner is imported by 2 files, above the merge base's 1: nothing outside core/ imports it"
    ]


def test_a_moved_file_keeps_its_counts_from_the_merge_base(tmp_path):
    root = tree(tmp_path, SMALL)
    git = ["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run([*git, "init", "-q"], check=True)
    subprocess.run([*git, "add", "."], check=True)
    subprocess.run([*git, "commit", "-qm", "base"], check=True)
    (root / PACKAGE / "loader").mkdir()
    subprocess.run([*git, "mv", f"{PACKAGE}/core/a.py", f"{PACKAGE}/loader/a.py"], check=True)
    subprocess.run([*git, "commit", "-qm", "move"], check=True)
    base = SHAPE.record_at(root, "HEAD~1")
    assert list(base["files"]) == [f"{PACKAGE}/loader/a.py"] and SHAPE.violations(root, base) == []

"""The shape of tests/ holds against the merge base: size, copied setup, history and retired code (tools/tests_shape.py; issue #1211)."""

from __future__ import annotations

from tests.running import ROOT
from tests.worlds import load_file

SHAPE = load_file("tests_shape", ROOT / "tools" / "tests_shape.py")

HELPER = "def helper(a, b):\n" + "".join(f"    a = a + {i}\n" for i in range(7)) + "    return a\n"


def test_the_tree_keeps_the_shape_of_the_merge_base():
    head = SHAPE.working_tree(ROOT)
    assert SHAPE.violations(head, SHAPE.at_ref(ROOT, SHAPE.base_ref())) == []


def test_growth_above_src_and_a_long_new_file_fail_and_a_cut_passes():
    base = {"src/a.py": "x = 1\n" * 10, "tests/test_a.py": "y = 1\n" * 8}
    head = {**base, "tests/test_a.py": "y = 1\n" * 12}
    assert SHAPE.violations(head, base) == ["tests/ grew from 8 to 12 lines while above src/ (10)"]
    head = {**base, "src/a.py": "x = 1\n" * 700, "tests/test_b.py": "z = 1\n" * 601}
    assert SHAPE.violations(head, base) == [
        "tests/test_b.py has 601 lines, above 600 and the merge base's 0"
    ]
    assert SHAPE.violations({**base, "tests/test_a.py": "y = 1\n"}, base) == []


def test_a_test_importing_a_test_and_a_copied_helper_fail():
    base = {"src/a.py": "x = 1\n" * 100, "tests/worlds.py": HELPER}
    head = {**base, "tests/test_b.py": "from tests.test_c import helper\n", "tests/test_c.py": HELPER}
    found = SHAPE.violations(head, base)
    assert any("tests/test_b.py imports tests.test_c" in line for line in found)
    assert any("copied setup: tests/test_c.py:helper, tests/worlds.py:helper" in line for line in found)


def test_history_long_docstrings_skips_and_uncalled_functions_fail_beyond_the_merge_base():
    base = {
        "src/event_universe/m.py": "def used():\n    return 1\n\n\nX = used()\n",
        "tests/test_a.py": "A = 1\n",
    }
    head = {
        "src/event_universe/m.py": base["src/event_universe/m.py"] + "\n\ndef lonely():\n    return 2\n",
        "tests/test_a.py": '"""One\nTwo\nThree\nFour."""\n\n# SINCE COMMIT 7 the step moved\n'
        'import pytest\n\npytestmark = pytest.mark.skip(reason="CANCELLED")\nA = 1\n',
    }
    found = SHAPE.violations(head, base)
    assert "tests/: history lines grew from 0 to 1" in found
    assert "tests/: long docstrings grew from 0 to 1" in found
    assert "tests/: retirement skips grew from 0 to 1" in found
    assert any("src/event_universe/m.py:lonely is called nowhere" in line for line in found)

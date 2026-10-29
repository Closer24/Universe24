"""Tensor24's room by file (decision 26): a push takes the room its budgets grant beyond the base's, never both."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import tests_shape  # noqa: E402


def lines(name, count):
    """A test of the given lines: its def and its body."""
    return f"def {name}():\n" + "    assert True\n" * (count - 1)


def grown(head, base):
    """The shape's refusal of a tests/ that grew past its room, or nothing."""
    return [line for line in tests_shape.violations(head, base) if line.startswith("tests/ grew")]


def test_a_test_with_no_budget_is_refused_beside_a_budget_the_base_already_holds(monkeypatch):
    monkeypatch.setattr(
        tests_shape, "ROOM", {"tests/test_old.py::test_old": (100, "the old test's room")}
    )
    base = {"tests/test_old.py": lines("test_old", 100)}
    head = {**base, "tests/test_new.py": lines("test_new", 100)}  # a new test of 100 lines and no budget
    assert grown(head, base) and not grown(base, base)

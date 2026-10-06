"""The proposition's books in paper/general_formula/click_algebra.py: r + k = M delta k + r' at every click, |r'| < M,
and M (sum of the kicks) + r = sum of the arrivals over any run; one arrival repeated reproduces kicks()."""

import importlib.util
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).resolve().parents[1] / "paper" / "general_formula" / "click_algebra.py"


def algebra() -> ModuleType:
    spec = importlib.util.spec_from_file_location("click_algebra", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_books_hold_the_identity_at_every_click_and_over_the_run() -> None:
    module = algebra()
    kicked, books = module.booked_kicks([3, -5, 10, 3, 3, -7, 2], 7)
    assert kicked == [0, 0, 1, 0, 1, -1, 0] and books == 2
    assert 7 * sum(kicked) + books == sum([3, -5, 10, 3, 3, -7, 2])
    for arrivals in ([7, 7, 7], [-7, -7], [6, 1], [-6, -1], [0, 0, 13, -13]):
        kicked, books = module.booked_kicks(arrivals, 7)
        assert 7 * sum(kicked) + books == sum(arrivals) and abs(books) < 7


def test_one_arrival_repeated_reproduces_the_accumulated_twist() -> None:
    module = algebra()
    for k in (3, -3, 7, 10, -10, 1):
        assert module.booked_kicks([k] * 9, 7)[0] == module.kicks(k, 7, 9)


def test_the_rule_is_odd_under_the_reversal_of_every_arrival() -> None:
    module = algebra()
    arrivals = [3, -5, 10, 3, 3, -7, 2]
    kicked, books = module.booked_kicks(arrivals, 7)
    reversed_kicks, reversed_books = module.booked_kicks([-k for k in arrivals], 7)
    assert reversed_kicks == [-k for k in kicked] and reversed_books == -books

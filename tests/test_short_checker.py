"""The short version's checker (paper/general_formula/short_checker.py) on the long version: against itself
it passes every check, a foreign number is a miss, and one sentence's two numbers swapped fail the locality check."""

import functools
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

CHECKER = Path(__file__).resolve().parents[1] / "paper" / "general_formula" / "short_checker.py"


@functools.cache
def self_test() -> tuple[Any, Any]:
    """The checker module and its self-test, run once for both tests: the long version read from git at the
    frozen commit; skipped where that commit is not in the clone's history."""
    spec = importlib.util.spec_from_file_location("short_checker", CHECKER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    try:
        return module, module.self_test()
    except FileNotFoundError as error:
        pytest.skip(f"the frozen long version is not in this clone's history: {error}")


def test_the_long_version_passes_its_own_checker_and_a_foreign_number_is_a_miss() -> None:
    """The first self-test: 0 misses, 0 weak numbers, 0 unresolved pointers; the long main text's first
    number beside a number the long paper does not hold gives one miss, the probe's."""
    module, result = self_test()
    assert result.audit.misses == [] and result.pointers.unresolved == [], result.text
    assert result.locality.weak == [], result.text
    assert result.audit.distinct > 0 and result.locality.checked > 0 and result.pointers.checked > 0
    long, _sources = module.long_version(module.LONG_REF, None, None)
    first = module.tokens(long["long main"])[0].written
    probe = module.audit_numbers({"probe": f"\\begin{{document}} ${first}$ and $12345678901234$"}, long)
    assert [miss.normalised for miss in probe.misses] == ["12345678901234"]


def test_one_sentences_two_numbers_swapped_fail_the_locality_check() -> None:
    """The second self-test: the long main text with the two numbers of one sentence swapped, audited
    against the long version, gives exactly those two WEAK lines and the checker's verdict FAIL."""
    _module, result = self_test()
    swap = result.swap
    assert swap is not None and swap.failed and swap.as_required, result.text
    assert {(weak.line, weak.normalised) for weak in swap.weak} == {
        (swap.line, n) for n in swap.normalised
    }
    assert len(swap.weak) == 2 and swap.misses == 0

"""The lifetime's folder (ALGEBRA.md #the-primitives, the row "the lifetime"): the record's age against L, the report first, the refusals by name."""

from __future__ import annotations

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.features.lifetime import DECLARATION, THE_WORD, LifetimeStart, LifetimeTerm, apply


def test_the_declaration_is_the_ledgers_row_and_the_register_finds_it_built():
    assert DECLARATION.name == "the lifetime" and folder_of(DECLARATION.name) == "lifetime"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.reads == ("the record's age", "L") and DECLARATION.writes == (
        "the record's tally",
    )
    assert THE_WORD in DECLARATION.section and DECLARATION.function is apply
    registered = discover().declarations["the lifetime"]
    assert registered.built and registered.function is apply


def test_a_record_ends_at_age_l_unless_its_last_quantum_was_reported_first():
    """Below L the record lives; at L (and beyond, should a step be missed) it ends; a record whose last quantum was reported is the report's, not the lifetime's; L = 0 and a negative age are refused by name."""
    term = LifetimeTerm(lifetime=3)
    assert [apply(term, LifetimeStart(age, False)).ends for age in (0, 1, 2, 3, 4)] == [
        False,
        False,
        False,
        True,
        True,
    ]
    assert not apply(term, LifetimeStart(3, True)).ends
    assert apply(LifetimeTerm(1), LifetimeStart(1, False)).ends
    with pytest.raises(ValueError, match="lifetime L = 0 is refused"):
        apply(LifetimeTerm(0), LifetimeStart(0, False))
    with pytest.raises(ValueError, match="age -1 is refused"):
        apply(term, LifetimeStart(-1, False))

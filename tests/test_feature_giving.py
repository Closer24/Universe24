"""THE GIVING, its own folder (ALGEBRA.md #the-primitives, the row "the giving" and "A BODY'S WRITE IS ONE ACT"; #the-counts-line, the free record; the model owner's word of 2026-09-29 on #1495, finding 10): the write once at the body's click and the birth of one quantum on synthetic integers, the refusals by name."""

import numpy as np
import pytest

from event_universe.features.giving import (
    ACTS,
    THE_BIRTH,
    THE_WRITE,
    GivingOwn,
    GivingStart,
    GivingTerm,
    apply,
)

TERM = GivingTerm(coupling=(3, 1), family=0)


def a_write(levels: tuple[np.ndarray, np.ndarray] | None) -> GivingStart:
    return GivingStart(THE_WRITE, 0, levels)


def rows(writes) -> tuple[list[list[int]], list[list[int]]]:
    """The act's two levels written and the two remainders after it, as lists."""
    return [level.tolist() for level in writes.level], [r.tolist() for r in writes.own.remainders]


def test_the_write_divides_the_bodys_levels_by_the_coupling_with_the_remainder_kept():
    """The write gives (level x num + r) div den at both levels of the body's rotation at its Nodes, the remainder r in [0, den) kept at the Node: the file's weight as (3, 1) writes 3 x the levels with the remainder 0; the coupling (1, 3): 7 div 3 = 2 r 1, -2 div 3 = -1 r 1, and a second write on the remainders (7 + 1) div 3 = 2 r 2; one numerator per Node, (2 x 7) div 4 = 3 r 2, (3 x -2) div 4 = -2 r 2, (6 x 0) div 4 = 0; the write changes no content."""
    levels = (np.array([7, -2, 0], dtype=np.int64), np.array([1, 5, -4], dtype=np.int64))
    tripled = apply(TERM, a_write(levels), GivingOwn())
    assert rows(tripled) == ([[21, -6, 0], [3, 15, -12]], [[0, 0, 0], [0, 0, 0]]) and tripled.count == 0
    per_node = apply(GivingTerm((np.array([2, 3, 6]), 4), 0), a_write(levels), GivingOwn())
    assert rows(per_node) == ([[3, -2, 0], [0, 3, -6]], [[2, 2, 0], [2, 3, 0]])
    third = GivingTerm(coupling=(1, 3), family=0)
    written = apply(third, a_write(levels), GivingOwn())
    assert rows(written) == ([[2, -1, 0], [0, 1, -2]], [[1, 1, 0], [1, 2, 2]])
    again = apply(third, a_write(levels), written.own)
    assert rows(again) == ([[2, -1, 0], [0, 2, -1]], [[2, 2, 0], [2, 1, 1]])


def test_the_birth_takes_the_one_quantum_from_the_giver():
    """The birth: the born record's count laid from its form carries one quantum, and the given family's content at the body falls by one; no level is written."""
    born = apply(TERM, GivingStart(THE_BIRTH, 1, None), GivingOwn())
    assert born.count == -1 and born.level is None and born.own == GivingOwn()


def test_the_refusals_by_name():
    """The coupling from 1; the act one of the two; the write without the body's levels; a birth of other than one quantum; every field named, no default."""
    with pytest.raises(ValueError, match="needs the coupling's pair from 1"):
        apply(GivingTerm((1, 0), 0), GivingStart(THE_BIRTH, 1, None), GivingOwn())
    with pytest.raises(ValueError, match="act is one of"):
        apply(TERM, GivingStart("the dance", 1, None), GivingOwn())
    with pytest.raises(ValueError, match="write needs the body's two levels"):
        apply(TERM, a_write(None), GivingOwn())
    for quanta in (0, 2):
        with pytest.raises(ValueError, match=f"birth bears one quantum.*carries {quanta}"):
            apply(TERM, GivingStart(THE_BIRTH, quanta, None), GivingOwn())
    with pytest.raises(TypeError):
        GivingStart(THE_WRITE)  # type: ignore[call-arg]
    assert ACTS == (THE_WRITE, THE_BIRTH)

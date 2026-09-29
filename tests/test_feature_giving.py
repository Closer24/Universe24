"""THE GIVING, its own folder (ALGEBRA.md #the-primitives, the row "the giving" and "A BODY'S WRITE IS ONE ACT"; 9.107; issue #1156): the bulk share on the moving row's numbers, the three acts of a window and the write's inverse on synthetic integers (the write (level + r) div k at both levels with the remainder carried at the Node, the close at outward >= T), the refusals by name, the declaration."""

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.giving import (
    ACTS,
    DECLARATION,
    THE_BIRTH,
    THE_CLOSE,
    THE_INVERSE,
    THE_OPEN,
    THE_WORD,
    THE_WRITE,
    GivingOwn,
    GivingStart,
    GivingTerm,
    apply,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

TERM, NO_TALLY = GivingTerm(coupling=(3, 1), action=1000, family=0), (0, 0, 0)
CLOSED = GivingOwn(None, 0, NO_TALLY)


def an_open(quanta: int, momentum: tuple[int, int, int]) -> GivingStart:
    return GivingStart(THE_OPEN, quanta, momentum, None, 0, NO_TALLY)


def a_write(levels: tuple[np.ndarray, np.ndarray] | None, act: str = THE_WRITE) -> GivingStart:
    return GivingStart(act, 0, NO_TALLY, levels, 0, NO_TALLY)


def a_close(flux: int, tally: tuple[int, int, int]) -> GivingStart:
    return GivingStart(THE_CLOSE, 0, NO_TALLY, None, flux, tally)


def a_birth(count: int, levels: tuple[np.ndarray, np.ndarray] | None) -> GivingStart:
    return GivingStart(THE_BIRTH, count, NO_TALLY, levels, 0, NO_TALLY)


def rows(writes) -> tuple[list[list[int]], list[list[int]]]:
    """The act's two levels written and the two remainders after it, as lists."""
    return [level.tolist() for level in writes.level], [r.tolist() for r in writes.own.remainders]


def test_the_three_acts_of_a_window_on_synthetic_integers():
    """The write adds (level x num + r) div den at both levels of the body's rotation at its shell, the remainder r in [0, den) kept at the Node (the coupling (1, 3), the division act: 7 div 3 = 2 r 1, -2 div 3 = -1 r 1, and the second write (7 + 1) div 3 = 2 r 2, so two writes give 14 div 3 = 4 r 2 exactly; the file's weight as (3, 1) writes 3 x the levels with the remainder 0; the law's coupling one numerator per Node of the shell, the body's content there, over the charge's divisor: (2 x 7) div 4 = 3 r 2, (3 x -2) div 4 = -2 r 2, (6 x 0) div 4 = 0), the inverse of a write gives the levels written and the remainders before (a bijection); the close sums the outward flux and closes at the first interval with outward >= T (334 does not close at T = 1000, 1000 does), the direction the tally's sign per axis; before the close nothing is named."""
    term = GivingTerm(coupling=(1, 3), action=1000, family=0)
    own = apply(term, an_open(2, NO_TALLY), CLOSED).own
    levels = (np.array([7, -2, 0], dtype=np.int64), np.array([1, 5, -4], dtype=np.int64))
    tripled = apply(TERM, a_write(levels), own)
    assert rows(tripled) == ([[21, -6, 0], [3, 15, -12]], [[0, 0, 0], [0, 0, 0]])
    # the law's coupling: the body's content at each Node of the shell over the charge's divisor
    per_node = apply(GivingTerm((np.array([2, 3, 6]), 4), 1000, 0), a_write(levels), own)
    assert rows(per_node) == ([[3, -2, 0], [0, 3, -6]], [[2, 2, 0], [2, 3, 0]])
    written = apply(term, a_write(levels), own)
    assert rows(written) == ([[2, -1, 0], [0, 1, -2]], [[1, 1, 0], [1, 2, 2]])
    pending = apply(term, a_close(334, (5, 0, -1)), written.own)
    assert not pending.closed and pending.direction is None
    assert written.own.window == pending.own.window == 1
    assert (pending.own.outward, pending.own.tally) == (334, (5, 0, -1))
    again = apply(term, a_write(levels), pending.own)
    assert rows(again) == ([[2, -1, 0], [0, 2, -1]], [[2, 2, 0], [2, 1, 1]])
    undone = apply(term, a_write(levels, THE_INVERSE), again.own)
    assert rows(undone) == ([[2, -1, 0], [0, 2, -1]], [[1, 1, 0], [1, 2, 2]]) and undone.own.window == 1
    closed = apply(term, a_close(666, (0, 0, -6)), again.own)
    assert closed.closed and closed.direction == (1, 0, -1)
    assert (closed.own.window, closed.own.outward, closed.own.tally) == (None, 1000, (5, 0, -7))
    assert closed.level is None and closed.count == 0 and closed.momentum is None


def test_the_birth_moves_the_bodys_levels_whole_and_takes_the_one_quantum():
    """The photon channel's act (ALGEBRA.md #the-functional-and-the-dilation (e)): at a Node beyond the body's set holding one quantum of the count's line, the body's two levels there move whole into the born record, no division and no remainder; the count there falls by one; the window, open or closed, is untouched."""
    levels = (np.array([7], dtype=np.int64), np.array([-2], dtype=np.int64))
    born = apply(TERM, a_birth(1, levels), CLOSED)
    assert [level.tolist() for level in born.level] == [[7], [-2]] and born.count == -1
    assert born.own == CLOSED and born.momentum is None and not born.closed and born.direction is None
    open_window = GivingOwn(3, 500, (1, 0, 0))
    assert apply(TERM, a_birth(1, levels), open_window).own == open_window


def test_the_refusals_by_name():
    """The coupling and the action from 1; the act one of the four; an open on an open one, a write or a close on none, an inverse with nothing written; the quanta from 1 at the open; every field named, no default"""
    with pytest.raises(ValueError, match="needs the coupling's pair and the quantum action T from 1"):
        apply(GivingTerm((1, 0), 1000, 0), an_open(1, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="inverse steps back a write, and none is written"):
        apply(TERM, a_write((np.zeros(1), np.zeros(1)), THE_INVERSE), GivingOwn(0, 0, NO_TALLY))
    with pytest.raises(ValueError, match="act is one of"):
        apply(TERM, GivingStart("the dance", 1, NO_TALLY, None, 0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="bears one quantum per Node per interval.*the Node holds 2"):
        apply(TERM, a_birth(2, (np.array([7]), np.array([-2]))), CLOSED)
    with pytest.raises(ValueError, match="birth needs the body's two levels at the Node"):
        apply(TERM, a_birth(1, None), CLOSED)
    with pytest.raises(ValueError, match="opens a window while one is open"):
        apply(TERM, an_open(1, NO_TALLY), GivingOwn(3, 0, NO_TALLY))
    with pytest.raises(ValueError, match="act 'the close' on a body with no open window"):
        apply(TERM, a_close(0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="needs quanta from 1 at the open, got M = 0"):
        apply(TERM, an_open(0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="write needs the body's two levels"):
        apply(TERM, a_write(None), GivingOwn(0, 0, NO_TALLY))
    with pytest.raises(TypeError):
        GivingStart(THE_OPEN, 1)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        GivingOwn()  # type: ignore[call-arg]
    assert ACTS == (THE_OPEN, THE_WRITE, THE_CLOSE, THE_INVERSE, THE_BIRTH)


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md #the-primitives in the register's form: "the giving" at (ii), the word after the step, the writes ordered as a click's deferred writes at (iv), its section; its function is `apply`, the act the loop calls."""
    assert DECLARATION.name == "the giving" and folder_of("the giving") == "giving"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.writes[:2] == ("a family's level at a Node", "a body's content M_k")
    assert DECLARATION.writes[2:] == ("a body's momentum n", "the count at a Node")
    assert DECLARATION.place_of("a body's momentum n") == "(iv)"
    assert DECLARATION.place_of("a family's level at a Node") == "(ii)" and DECLARATION.function is apply
    assert DECLARATION.section.startswith(THE_WORD)
    assert "from the rule" in THE_WORD and "beyond (H)" in THE_WORD and "click's inverse" in THE_WORD
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    assert simulation.register.declarations["the giving"].writes == DECLARATION.writes
    assert simulation.register.at("the giving", "(ii)") is apply  # the loop calls the folder's acts

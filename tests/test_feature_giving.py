"""THE GIVING, its own folder (ALGEBRA.md 9.117 item 2, the row "the giving"; 9.117 item 5;
9.107; 9.71 (1); 9.116 item 5; issue #1156): the bulk share on the moving row's numbers
(the velocity kept exactly where M divides n, within one unit of n on the new wall otherwise,
symmetric under reflection), the three acts of a window on synthetic integers (the open's
deferred writes, the write g x the body's levels, the close at the first interval reaching T
with the direction the tally's sign), the refusals by name, and the declaration the
ledger's row in the register's form."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.giving import (
    ACTS,
    DECLARATION,
    THE_CLOSE,
    THE_OPEN,
    THE_WORD,
    THE_WRITE,
    GivingOwn,
    GivingStart,
    GivingTerm,
    apply,
    bulk_share,
)
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world
from tests.test_toward_nature import load_module

TERM = GivingTerm(weight=3, norm=1000, norm_denominator=1, family=0)
NO_TALLY = (0, 0, 0)
CLOSED = GivingOwn(None, 0, NO_TALLY)


def an_open(quanta: int, momentum: tuple[int, int, int]) -> GivingStart:
    return GivingStart(THE_OPEN, quanta, momentum, None, 0, NO_TALLY)


def a_write(levels: np.ndarray | None) -> GivingStart:
    return GivingStart(THE_WRITE, 0, NO_TALLY, levels, 0, NO_TALLY)


def a_close(flux: int, tally: tuple[int, int, int]) -> GivingStart:
    return GivingStart(THE_CLOSE, 0, NO_TALLY, None, flux, tally)


def test_the_bulk_share_keeps_the_velocity_on_the_moving_row_and_is_symmetric():
    """The moving rows (examples/events/toward_nature): a body of M = 65 quanta on the wall
    W = 3 Q M moving at v = 1 / 4 has n = W div 4 = 3120; a giving takes the quantum's share
    3120 div 65 = 48 and leaves n = 3072 = the new wall's quarter, the velocity 1 / 4 exactly
    (issue #1156: today n stays and the body speeds up); with n not divisible by M the body
    keeps the remainder inside n, the velocity within one unit of n on the new wall; a
    negative n gives the mirror image (the share rounded toward zero on both signs)."""
    generator = load_module("make_worlds")
    wall = generator.drive_wall(65)
    momentum = wall // generator.HOP_EVERY
    assert (wall, momentum) == (3 * 64 * 65, 3120)
    shared = bulk_share((momentum, 0, 0), 65)
    assert shared == (3072, 0, 0) and shared[0] == generator.drive_wall(64) // generator.HOP_EVERY
    assert bulk_share((-momentum, 0, 0), 65) == (-3072, 0, 0)
    assert bulk_share((100, -100, 64), 65) == (99, -99, 64)
    # the velocity after, on the new wall, against before: within one unit of n on the new wall
    before, after = 100 * 64, 99 * 65  # v = 100 / (3 Q 65) against 99 / (3 Q 64), scaled by 3 Q 65 x 64
    assert 0 <= after - before < 65
    open_writes = apply(TERM, an_open(65, (momentum, 5, -5)), CLOSED)
    assert open_writes.count == -1 and open_writes.momentum == (3072, 5, -5)
    assert open_writes.own == GivingOwn(0, 0, NO_TALLY) and not open_writes.closed
    assert open_writes.level is None and open_writes.direction is None


def test_the_three_acts_of_a_window_on_synthetic_integers():
    """The write adds g x the body's levels at its shell and counts the interval; the close
    sums the outward flux and its tally and closes at the first interval with outward x den
    >= norm (T = 1000 / 3 here, so 334 closes and 333 does not), the direction the tally's
    sign per axis, never its size; before the close nothing is named."""
    term = GivingTerm(weight=3, norm=1000, norm_denominator=3, family=0)
    own = apply(term, an_open(2, NO_TALLY), CLOSED).own
    levels = np.array([7, -2, 0], dtype=np.int64)
    written = apply(term, a_write(levels), own)
    assert written.level.tolist() == [21, -6, 0] and written.own == GivingOwn(1, 0, NO_TALLY)
    own = written.own
    pending = apply(term, a_close(333, (5, 0, -1)), own)
    assert not pending.closed and pending.direction is None
    assert pending.own == GivingOwn(1, 333, (5, 0, -1))
    own = apply(term, a_write(levels), pending.own).own
    closed = apply(term, a_close(1, (0, 0, -6)), own)
    assert closed.closed and closed.direction == (1, 0, -1)
    assert closed.own == GivingOwn(None, 334, (5, 0, -7)) and closed.level is None
    assert closed.count == 0 and closed.momentum is None


def test_the_refusals_by_name():
    """The weight, the norm and its denominator from 1; the act one of the three; an open on
    an open window, a write or a close on none; the quanta from 1 at the open; the write
    without the body's levels; every field of a start and of an own is named by the loop,
    none has a written default."""
    with pytest.raises(ValueError, match="needs a weight, a norm and its denominator from 1"):
        apply(GivingTerm(0, 1000, 1, 0), an_open(1, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="act is one of"):
        apply(TERM, GivingStart("the birth", 1, NO_TALLY, None, 0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="opens a window while one is open"):
        apply(TERM, an_open(1, NO_TALLY), GivingOwn(3, 0, NO_TALLY))
    with pytest.raises(ValueError, match="act 'the close' on a body with no open window"):
        apply(TERM, a_close(0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="needs quanta from 1 at the open, got M = 0"):
        apply(TERM, an_open(0, NO_TALLY), CLOSED)
    with pytest.raises(ValueError, match="write needs the body's levels"):
        apply(TERM, a_write(None), GivingOwn(0, 0, NO_TALLY))
    with pytest.raises(TypeError):
        GivingStart(THE_OPEN, 1)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        GivingOwn()  # type: ignore[call-arg]
    assert ACTS == (THE_OPEN, THE_WRITE, THE_CLOSE)


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117 in the register's form: "the giving"
    at (ii), the word after the step, the writes a family's level at a Node, a body's
    content M_k and a body's momentum n (the stock is M_k of the given family; Q no value),
    the orders per value (M_k 2 after the clicks, n 1 before the recoil, both at (iv) as
    a click's deferred writes), its section with the words of 9.117 item 5; the register's function is apply, the
    loop's open of today; the engine's register reads this folder's row."""
    assert DECLARATION.name == "the giving" and folder_of("the giving") == "giving"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.writes == (
        "a family's level at a Node",
        "a body's content M_k",
        "a body's momentum n",
    )
    assert DECLARATION.place_of("a body's momentum n") == "(iv)"
    assert DECLARATION.place_of("a family's level at a Node") == "(ii)"
    assert DECLARATION.function is apply
    assert DECLARATION.section.startswith(THE_WORD)
    assert "from the rule" in THE_WORD and "beyond (H)" in THE_WORD and "click's inverse" in THE_WORD
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    assert simulation.register.declarations["the giving"].writes == DECLARATION.writes
    assert simulation.register.at("the giving", "(ii)") is apply  # the loop calls the folder's acts

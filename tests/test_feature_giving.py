"""THE GIVING, its own folder (ALGEBRA.md 9.117 item 2, the row "the giving"; 9.107; 9.71 (1); issue
#1156): the bulk share on the moving row's numbers, the three acts of a window on synthetic integers,
the refusals by name, the close act replayed against the engine's own windows, the declaration."""

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
    bind,
    bulk_share,
)
from event_universe.world_files import parse_nature_beam_world
from tests.running import load_module
from tests.worlds import emitter_world

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
    """The moving rows: a body of M = 65 on W = 3 Q M at v = 1 / 4 has n = 3120; a giving takes the share
    48 and leaves n = 3072, the new wall's quarter (issue #1156); with n not divisible by M the velocity
    stays within one unit of n on the new wall; a negative n gives the mirror image."""
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
    """The write adds g x the body's levels at its shell; the close sums the outward flux and closes at
    the first interval with outward x den >= norm (334 closes at T = 1000 / 3, 333 not), the direction
    the tally's sign per axis; before the close nothing is named."""
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
    """The weight, the norm and its denominator from 1; the act one of the three; an open on an open one,
    a write or a close on none; the quanta from 1 at the open; every field named, no default"""
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


def test_the_close_act_closes_where_the_engines_window_closes_and_not_before():
    """The emitter's unit world, every window replayed from the engine's own record: fed the increments,
    the folder's close act keeps the window open where the engine does and closes at the interval the
    engine's giving line names, with its outward, length and direction; the stock falls one per open."""
    document = emitter_world(stock=4, ticks=1200)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    block = simulation.block_by_number[0]
    emitter = block.definition.emitter
    assert emitter is not None and emitter.weight is not None and emitter.norm is not None
    denominator = emitter.norm_denominator if emitter.norm_denominator is not None else 1
    term = GivingTerm(emitter.weight, emitter.norm, denominator, emitter.family)
    watched: list[tuple[int, int, tuple[int, int, int], int]] = []
    finals: list[tuple[int, int, tuple[int, int, int], int]] = []
    for _ in range(document["ticks"]):
        opened = block.window
        simulation.step()
        identity = block.window if block.window is not None else opened
        if identity is None:
            continue
        live = simulation.records[identity]
        tally = (int(live.outward_tally[0]), int(live.outward_tally[1]), int(live.outward_tally[2]))
        entry = (simulation.tick, int(live.outward), tally, int(live.window))
        if block.window is not None:
            watched.append(entry)
        else:
            finals.append(entry)  # closed inside this step: the loop's final outward and tally
    givings = [line for line in lines if line["event"] == "giving" and "window" in line]
    assert len(givings) == len(finals) == 4 and simulation.held[0][emitter.family] == 0
    # the runs of open intervals, one per giving, in order
    runs: list[list[tuple[int, int, tuple[int, int, int], int]]] = []
    for entry in watched:
        if runs and entry[0] == runs[-1][-1][0] + 1:
            runs[-1].append(entry)
        else:
            runs.append([entry])
    assert len(runs) == len(givings)
    for run, final, line in zip(runs, finals, givings, strict=True):
        assert (line["tick"], line["window"], line["outward"]) == (final[0], final[3], final[1])
        assert final[0] == run[-1][0] + 1 and final[3] == run[-1][3] + 1
        own = apply(term, an_open(1, NO_TALLY), CLOSED).own
        outward, tally = 0, NO_TALLY
        for _tick, summed, summed_tally, _window in [*run, final]:
            own = apply(term, a_write(np.zeros(1, dtype=np.int64)), own).own
            increment = (
                summed_tally[0] - tally[0],
                summed_tally[1] - tally[1],
                summed_tally[2] - tally[2],
            )
            writes = apply(term, a_close(summed - outward, increment), own)
            assert writes.closed == (summed * denominator >= emitter.norm) == (summed == final[1])
            own, outward, tally = writes.own, summed, summed_tally
        assert own == GivingOwn(None, line["outward"], final[2])
        assert writes.direction == tuple(line["momentum"]) == (1, 0, 0)
        assert writes.direction == tuple((v > 0) - (v < 0) for v in final[2])


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117 in the register's form: "the giving" at (ii), the
    word after the step, the writes ordered as a click's deferred writes at (iv), its section"""
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
    assert callable(bind(simulation))  # the loop's `_emit` of today, resolved at each call

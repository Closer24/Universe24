"""THE GIVING, its own folder the_giving (ALGEBRA.md 9.117 item 2, the row "the giving";
9.117 item 5; 9.107; 9.71 (1); 9.116 item 5; the Boss's records 2223 and 2230; issue
#1156): the bulk share on the moving row's numbers (the velocity kept exactly where M
divides n, within one unit of n on the new wall otherwise, symmetric under reflection),
the three acts of a window on synthetic integers (the open's deferred writes, the write
g x the body's levels, the close at the first interval reaching T with the direction the
tally's sign), the refusals by name, the close's identity on the engine's giving lines
of the emitter world, the schema over the shipped emitter's keys, and the declaration the
ledger's row in the register's form."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.giving import (
    ACTS,
    DECLARATION,
    SCHEMA,
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
from tests.test_emitter import emitter_world
from tests.test_toward_nature import load_module

TERM = GivingTerm(weight=3, norm=1000, norm_denominator=1, family=0)


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
    open_writes = apply(TERM, GivingStart(THE_OPEN, quanta=65, momentum=(momentum, 5, -5)), GivingOwn())
    assert open_writes.count == -1 and open_writes.momentum == (3072, 5, -5)
    assert open_writes.own == GivingOwn(0, 0, (0, 0, 0)) and not open_writes.closed


def test_the_three_acts_of_a_window_on_synthetic_integers():
    """The write adds g x the body's levels at its shell and counts the interval; the close
    sums the outward flux and its tally and closes at the first interval with outward x den
    >= norm (T = 1000 / 3 here, so 334 closes and 333 does not), the direction the tally's
    sign per axis, never its size; before the close nothing is named."""
    term = GivingTerm(weight=3, norm=1000, norm_denominator=3, family=0)
    own = apply(term, GivingStart(THE_OPEN, quanta=2, momentum=(0, 0, 0)), GivingOwn()).own
    levels = np.array([7, -2, 0], dtype=np.int64)
    written = apply(term, GivingStart(THE_WRITE, body_levels=levels), own)
    assert written.level.tolist() == [21, -6, 0] and written.own == GivingOwn(1, 0, (0, 0, 0))
    own = written.own
    pending = apply(term, GivingStart(THE_CLOSE, outward_flux=333, outward_tally=(5, 0, -1)), own)
    assert not pending.closed and pending.direction is None
    assert pending.own == GivingOwn(1, 333, (5, 0, -1))
    own = apply(term, GivingStart(THE_WRITE, body_levels=levels), pending.own).own
    closed = apply(term, GivingStart(THE_CLOSE, outward_flux=1, outward_tally=(0, 0, -6)), own)
    assert closed.closed and closed.direction == (1, 0, -1)
    assert closed.own == GivingOwn(None, 334, (5, 0, -7)) and closed.level is None
    assert closed.count == 0 and closed.momentum is None


def test_the_refusals_by_name():
    """The weight, the norm and its denominator from 1; the act one of the three; an open on
    an open window, a write or a close on none; the quanta from 1 at the open; the write
    without the body's levels."""
    with pytest.raises(ValueError, match="needs a weight, a norm and its denominator from 1"):
        apply(GivingTerm(0, 1000, 1, 0), GivingStart(THE_OPEN, quanta=1), GivingOwn())
    with pytest.raises(ValueError, match="act is one of"):
        apply(TERM, GivingStart("the birth", quanta=1), GivingOwn())
    with pytest.raises(ValueError, match="opens a window while one is open"):
        apply(TERM, GivingStart(THE_OPEN, quanta=1), GivingOwn(3, 0, (0, 0, 0)))
    with pytest.raises(ValueError, match="act 'the close' on a body with no open window"):
        apply(TERM, GivingStart(THE_CLOSE), GivingOwn())
    with pytest.raises(ValueError, match="needs quanta from 1 at the open, got M = 0"):
        apply(TERM, GivingStart(THE_OPEN, quanta=0), GivingOwn())
    with pytest.raises(ValueError, match="write needs the body's levels"):
        apply(TERM, GivingStart(THE_WRITE), GivingOwn(0, 0, (0, 0, 0)))
    assert ACTS == (THE_OPEN, THE_WRITE, THE_CLOSE)


def test_the_close_identity_on_the_engines_giving_lines():
    """On the emitter's unit world every giving line's integers satisfy the close's line:
    outward x den >= norm at the close, with the window's length the intervals written; the
    stock falls by one per giving at the open (the engine's count, 9.107 item 2); the
    folder's close act, fed the line's outward as one booking, closes and names the record
    with the direction of the line's four-vector."""
    document = emitter_world(stock=4, ticks=1200)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(document["ticks"]):
        simulation.step()
    givings = [line for line in lines if line["event"] == "giving" and "window" in line]
    emitter = simulation.block_by_number[0].definition.emitter
    assert emitter is not None and emitter.weight is not None and emitter.norm is not None
    denominator = emitter.norm_denominator if emitter.norm_denominator is not None else 1
    term = GivingTerm(
        emitter.weight,
        emitter.norm,
        denominator,
        simulation.families.index(simulation.families[emitter.family]),
    )
    assert len(givings) == 4
    for line in givings:
        assert line["outward"] * denominator >= line["norm"] == emitter.norm and line["window"] >= 1
        own = GivingOwn(line["window"], 0, (0, 0, 0))
        closed = apply(
            term,
            GivingStart(THE_CLOSE, outward_flux=line["outward"], outward_tally=tuple(line["momentum"])),
            own,
        )
        assert closed.closed and closed.direction == tuple(line["momentum"]) == (1, 0, 0)
    assert simulation.held[0][emitter.family] == 0  # the stock of 4 given, one per open


def test_the_schema_covers_the_shipped_emitters_keys_within_the_loaders_bounds():
    """Every key of the shipped emitter's declaration is in the schema with its kind, every
    integer within its bounds, every required key present; the schema's keys are the
    loader's accepted keys of today (world.py, the emitter's object)."""
    emitter = emitter_world(stock=1, ticks=1)["measured"][0]["emitter"]
    schema = {key: (kind, low, high, required) for key, kind, low, high, required in SCHEMA}
    assert set(emitter) <= set(schema)
    for key, value in emitter.items():
        kind, low, high, _required = schema[key]
        if kind == "integer":
            assert type(value) is int and low <= value <= high, key
        elif kind == "name":
            assert isinstance(value, str), key
        elif kind == "names":
            assert isinstance(value, list) and all(isinstance(item, str) for item in value), key
        else:
            assert kind == "integers" and isinstance(value, list), key
    assert {key for key, (_kind, _low, _high, required) in schema.items() if required} <= set(emitter)
    assert set(schema) == {
        "family",
        "weight",
        "period",
        "norm",
        "norm_denominator",
        "twist",
        "receiver",
        "branches",
        "clock",
    }


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117 in the register's form: "the giving"
    at (ii), the word after the step, the writes a family's level at a Node, a body's
    content M_k and a body's momentum n (the stock is M_k of the given family; Q no value),
    the orders per value (M_k 2 after the clicks, n 1 before the recoil, both at (iv) as
    a click's deferred writes), its section with the words of 9.117 item 5; bind gives the
    loop's open of today; the engine's register reads this folder's row."""
    assert DECLARATION.name == "the giving" and folder_of("the giving") == "giving"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.writes == (
        "a family's level at a Node",
        "a body's content M_k",
        "a body's momentum n",
    )
    assert DECLARATION.order_of("a body's content M_k") == 2
    assert DECLARATION.order_of("a body's momentum n") == 1
    assert DECLARATION.place_of("a body's momentum n") == "(iv)"
    assert DECLARATION.place_of("a family's level at a Node") == "(ii)"
    assert DECLARATION.function is apply
    assert DECLARATION.section.startswith(THE_WORD)
    assert "from the rule" in THE_WORD and "beyond (H)" in THE_WORD and "click's inverse" in THE_WORD
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    assert simulation.register.declarations["the giving"].writes == DECLARATION.writes
    assert callable(bind(simulation))  # the loop's `_emit` of today, resolved at each call

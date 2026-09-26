"""THE RECEIVE, its own folder (ALGEBRA.md 9.117 the row "the receive"; 9.81 (2) (b), (c); 9.96
(2) (c); 9.119 item 2; the Boss's record 2250): the Port's angle, the table's triple and the
rotation of the Link's pair are Rule3's read acts with declared coefficients; on the shipped
moving Lorentz world the folder's angles and arrival sums are the loop's own, forward and
backward, at every record over thirty intervals bit for bit; the identity at the angle zero;
the composed triple the table's; the refusals; the declaration."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.primitives import compose_triples, mirror_triple
from event_universe.events.world import TWIST_FINE_BITS
from event_universe.features.receive import (
    DECLARATION,
    Link,
    ReceiveStart,
    ReceiveTerm,
    TwistRead,
    apply,
    bind,
    rotated,
    triple,
)
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
TOWARD = ROOT / "examples" / "events" / "toward_nature"


def term_of(simulation: DetectorLawSimulation) -> ReceiveTerm:
    """The loop's own table arrays, None on a world without a table."""
    if simulation.twist_table is None:
        return ReceiveTerm(None, None, TWIST_FINE_BITS)
    return ReceiveTerm(simulation._fine, simulation._coarse, TWIST_FINE_BITS)


def start_of(simulation: DetectorLawSimulation, live, inverse: bool) -> ReceiveStart:
    """The record's levels, its family's twist reads and the six Links as the loop reads them at the step (the `before` levels backward)."""
    definition = simulation.families[live.family]
    sign = simulation.family_charge[live.family]
    wrap = simulation.kind_wrap[live.family]
    re = live.before if inverse else live.now
    im = None if live.im_now is None else (live.im_before if inverse else live.im_now)
    reads = []
    for other, weight, by, twist in definition.reads:
        if len(simulation.families[other].parts) < 2:
            continue
        factor = weight * live.twist if twist == "own" else int(twist)
        if by != "plain":
            factor *= sign
        vector = simulation.held_parts[other][:3]
        reads.append(TwistRead(factor, tuple(part.before if inverse else part.now for part in vector)))
    links = []
    for axis in range(3):
        for sigma in (1, -1):
            links.append(
                Link(
                    simulation._arrival(re, axis, sigma, wrap),
                    None if im is None else simulation._arrival(im, axis, sigma, wrap),
                    tuple(simulation._arrival(read.here[axis], axis, sigma, wrap) for read in reads),
                )
            )
    return ReceiveStart(re, im, tuple(reads), tuple(links))


def same(mine, loops) -> bool:
    if mine is None or loops is None:
        return mine is None and loops is None
    return all(np.array_equal(a, b) for a, b in zip(mine, loops, strict=True))


def test_the_folder_gives_the_loops_arrivals_on_the_moving_lorentz_world_bit_for_bit():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    term = term_of(simulation)
    rotated_records, second_levels = 0, 0
    for _ in range(30):
        for live in list(simulation.records.values()):
            if simulation.families[live.family].levels < 2 or live.silent:
                continue
            for inverse in (False, True):
                simulation._twists.clear()  # the loop's cache holds the step's own angles; the loop's function on the state now
                twists = simulation._port_twists(live, inverse)
                loops_re, loops_im = simulation._arrivals(live, twists, inverse)
                writes = apply(term, start_of(simulation, live, inverse))
                if twists is None:
                    assert all(not np.any(k) for k in writes.angles)
                else:
                    assert same(writes.angles, twists)
                    rotated_records += any(np.any(k) for k in writes.angles)
                assert same(writes.re, loops_re) and same(writes.im, loops_im)
                second_levels += writes.im is not None
        simulation.step()
    assert rotated_records > 0 and second_levels > 0


def test_the_angle_zero_is_the_identity_and_the_composed_triple_is_the_tables():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    term = term_of(simulation)
    table = simulation.twist_table
    assert table is not None
    generator = np.random.default_rng(7)
    for k in (0, 1, -1, 1023, 1024, -1025, 5703478, -5703478):
        found = triple(term, np.array(k), 0)
        composed = compose_triples(table.fine[abs(k) & 1023], table.coarse[abs(k) >> 10])
        assert tuple(int(v) for v in found) == (mirror_triple(composed) if k < 0 else composed)
        re, im = generator.integers(-(1 << 20), 1 << 20, size=(2, 5))
        t_re, t_im = rotated(found, re, im)
        if k == 0:
            assert np.array_equal(t_re, re) and np.array_equal(t_im, im)
        c, s, d = found
        assert np.array_equal(t_re, (2 * (c * re - s * im) + d) // (2 * d))
        assert np.array_equal(t_im, (2 * (s * re + c * im) + d) // (2 * d))


def test_the_refusals_name_the_port():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    term = term_of(simulation)
    beyond = np.array([len(simulation.twist_table.coarse) << TWIST_FINE_BITS])
    with pytest.raises(ValueError, match=r"toward -y .* beyond the twist table"):
        triple(term, beyond, 3)
    with pytest.raises(ValueError, match=r"toward \+z .*no table"):
        triple(ReceiveTerm(None, None, TWIST_FINE_BITS), np.array([1]), 4)
    level = np.zeros((1, 1, 1), dtype=np.int64)
    link = Link(level, None, ())
    with pytest.raises(ValueError, match="six Links"):
        apply(term, ReceiveStart(level, None, (), (link,)))
    with pytest.raises(ValueError, match=r"toward \+x carries 0 vector parts for 1"):
        apply(term, ReceiveStart(level, None, (TwistRead(1, (level, level, level)),), (link,) * 6))


def test_the_declaration_is_the_registers_row():
    assert DECLARATION.name == "the receive" and folder_of(DECLARATION.name) == "receive"
    assert DECLARATION.place == "(i)" and DECLARATION.word == "the step"
    assert DECLARATION.function is apply and DECLARATION.writes == ("the arrivals",)
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    registered = simulation.register.declarations["the receive"]
    assert registered.binder is bind and callable(registered.function)
    live = next(iter(simulation.records.values()))
    assert same(bind(simulation)(live, None, False)[0], simulation._arrivals(live, None, False)[0])

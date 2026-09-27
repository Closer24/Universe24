"""The booking in the body's frame, one rule (ALGEBRA.md 9.74 (2)): a face of a moving body books
(G_in + (v . n) e_out) cut at zero after the sum, with no separate hop booking."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import CLOSED_CHAIN, emitter, massive_world, seed_source
from tests.worlds import reads

CART_START = 200
CART_MOMENTUM = 48  # against the wall 3 x 64 x 1: one Link every four intervals, v = 1 / 4
LIGHT_PACE = 0.447  # the group pace of light's [512, 1] clock at k = pi / 2 (COMPUTATION, 9.24)


def cart_world(
    momentum: int = -CART_MOMENTUM, stock: int = 2, ticks: int = 700, start: int = CART_START
) -> dict:
    """The emitter A at [20, 52) naming the set `cart`, its two records along +x; the cart a
    silent block of matter over [200, 203) with the momentum `momentum` along x and the set
    `cart` bound to its Nodes (the detector follows the body, item 40's cube of three)."""
    # SINCE COMMIT 7 the emitter is a one-Node body's Node at the retired train's head (x = 51) on
    # the beam body's Node's kind [800, 1200] (its light near the wavelength 4 of the retired train's
    # clock; a body of 32 Nodes writing at all its Nodes would give a record far above one T)
    document = massive_world([300, 1, 1], CLOSED_CHAIN, [800, 1200])
    document["ticks"] = ticks
    document["clock_stamp"] = True
    # the cart's own massive family (its Nodes apart from the emitter's mode, which spans the
    # chain), the kind's pair [800, 809], the cart a barrier of it
    document["universe"].append(
        {"name": "cart", "quantum": 1, "pair": [800, 809], "charge": 0, "reads": reads()}
    )
    cart = {
        "position": [start, 0, 0],
        "family": "cart",
        "amount": 1,
        "stocks": {},
        "ramp": 0,
        "start": 0,
        "momentum": [momentum, 0, 0],
        "extents": [3, 1, 1],
        "q": 0,
        "spin": [0, 0, 0],
        "twist": 0,
        "moment": [0, 0, 0],
        "pair": [800, 810],  # a barrier of matter's kind, no seed: light passes it untouched
    }
    source = emitter(51, "cart", 0, stock)
    source["extents"] = [1, 1, 1]
    source["pair"] = [800, 802]
    source["seed"] = 1 << 12
    source["emitter"]["weight"] = 4
    document["measured"] = [source, cart]
    document["detectors"] = [{"name": "cart", "block": 1}]
    seed_source(document, 0)
    return document


def run(
    document: dict, frame: bool, clicks: bool, ticks: int
) -> tuple[DetectorLawSimulation, list[dict]]:
    """`frame` False: the control, the board's frame alone (no set moving as far as the
    booking reads, the Port booking of 9.25 (2) at the set's Nodes as they stand)."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    if not frame:
        simulation._moving_sets = lambda: {}  # type: ignore[method-assign]
    if not clicks:
        simulation._ladder_click = lambda live, increments: None  # type: ignore[method-assign]
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def booked_share(
    simulation: DetectorLawSimulation, control: DetectorLawSimulation
) -> tuple[Fraction, Fraction]:
    """The one light record's booking at the cart over its norm, in the body's frame and in
    the board's (the control), the carry counted."""
    cart = simulation.detector_names.index("cart")
    (live,) = [live for live in simulation.records.values() if live.family == 0]
    (other,) = [live for live in control.records.values() if live.family == 0]
    assert live.identity == other.identity and live.norm == other.norm and live.pace == other.pace
    norm = Fraction(live.norm, live.pace)
    carry = Fraction(*live.carry.get(cart, (0, 1)))  # the carry kept as the exact pair
    assert 0 <= carry < 1 and not other.carry
    return (Fraction(live.pointers[cart]) + carry) / norm, Fraction(other.pointers[cart]) / norm


@pytest.mark.diagnostic
def test_the_front_face_books_the_oncoming_record_whole_over_a_pass():
    """GAMEBOARD reading of the record's books at the detector, the clicks held off; a
    diagnostic, not a measurement (the control clicks as the frame does, 1 against 1)."""
    document = cart_world(stock=1)
    frame, _ = run(document, frame=True, clicks=False, ticks=600)
    board, _ = run(document, frame=False, clicks=False, ticks=600)
    # the cart passed through the whole record (its 32 Nodes at 0.447 against the cart's 0.25);
    # a body-position reading, the setup's guard
    assert frame.blocks[1].corner[0] < CART_START - 100
    # GAMEBOARD reading of the record's books at the detector, the clicks held off; a diagnostic
    booked, plain = booked_share(frame, board)
    assert abs(float(booked) - 1) < 0.08, f"GAMEBOARD reading, a diagnostic: booked {float(booked)}"
    share = CART_MOMENTUM / 192 / (CART_MOMENTUM / 192 + LIGHT_PACE)  # the hop's share, 0.36
    assert abs(float(booked - plain) - share) < 0.1, (
        f"GAMEBOARD reading, a diagnostic: booked - plain {float(booked - plain)}"
    )
    assert plain < booked


@pytest.mark.diagnostic
def test_both_records_click_at_the_moving_cart_on_the_first_pass():
    """The clicks (measurements) and, last, a GAMEBOARD reading of the cart's store."""
    simulation, lines = run(cart_world(stock=2), frame=True, clicks=True, ticks=700)
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) == 2
    assert all(line["chosen"] and line["chosen"][0][0] == "cart" for line in gathers)
    # the first pass: the click before the cart has left the record's train behind
    for line in gathers:
        assert 0 < line["tick"] - line["giving"] < 400
    assert sum(line["content"] for line in gathers) == 2  # the two light quanta taken, the gather lines
    # GAMEBOARD: the cart's store after the two clicks (the set bound to the body, item 40); a diagnostic
    assert simulation.held[1][0] == 2


def test_at_rest_the_rule_is_the_port_booking_bit_for_bit_and_nothing_is_carried():
    document = cart_world(momentum=0, stock=1)
    frame, lines_a = run(document, frame=True, clicks=True, ticks=300)
    board, lines_b = run(document, frame=False, clicks=True, ticks=300)
    assert not frame._moving_sets() and frame.blocks[1].stepped == 0
    assert lines_a == lines_b
    for identity, live in frame.records.items():
        other = board.records[identity]
        assert live.pointers == other.pointers and not live.carry
        assert np.array_equal(live.now, other.now)


@pytest.mark.diagnostic
def test_the_back_face_books_a_record_overtaking_the_cart_once_and_not_c_over_c_minus_v():
    """AT THE BACK (9.74 (2)): the cart moving along +x at one Link every four intervals, the
    record given along +x at 0.447 overtakes it from behind and books G_in - v e_out at the back
    face, cut at zero: the norm once. THE CONTROL, the board's frame: the rows the back face
    uncovers at each hop re-enter through the back Port and are booked again, c / (c - v) = 2.27
    of the norm (finding (a) of item 48, resolved by the one rule). COMPUTATION; no pin. Both
    shares are GAMEBOARD readings of the record's books with the clicks held off, diagnostics
    (docs/ENGINE.md, the readings by type), not measurements."""
    document = cart_world(momentum=CART_MOMENTUM, stock=1, ticks=700, start=60)
    frame, _ = run(document, frame=True, clicks=False, ticks=700)
    board, _ = run(document, frame=False, clicks=False, ticks=700)
    # a body-motion reading, the setup's guard: the cart moved on; the record passed it
    assert frame.blocks[1].stepped > 150
    # GAMEBOARD reading of the record's books at the back face, the clicks held off; a diagnostic
    booked, plain = booked_share(frame, board)
    assert abs(float(booked) - 1) < 0.1, f"GAMEBOARD reading, a diagnostic: booked {float(booked)}"
    # the board's frame books the rows the back face uncovers again: c / (c - v) = 2.27 on the
    # retired train's uniform rows; on the window's record (its envelope the body's Node's, commit 7)
    # it reads 1.63 (COMPUTATION, a GAMEBOARD reading), well above the norm the one rule books once
    re_entry = LIGHT_PACE / (LIGHT_PACE - CART_MOMENTUM / 192)  # c / (c - v) = 2.27, the uniform rows'
    assert 1.4 < float(plain) < re_entry, f"GAMEBOARD reading, a diagnostic: plain {float(plain)}"

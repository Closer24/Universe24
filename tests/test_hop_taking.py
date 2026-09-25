"""THE TAKING AT A HOP (ALGEBRA.md 9.62 (3), the mathematician's ruling on Nature24's finding 2
of the run toward nature, row 2; BUILD.md section 26 item 48): at a hop the rows of every
record on the Nodes a body newly covers are booked to the set bound to the body at their share
of the norm, after the interval's step and the Port booking. On a closed chain of 300 an emitter
at [20, 52) gives light along +x (two records) and a cart, a silent block of three Nodes with
its set bound to it, moves toward it at one Link every four intervals: (1) over the record's
passage through the cart the booked total reaches the record's norm over its pace within a
few percent with the hop's booking, and falls short by about the hop's share v / (v + c_l)
without it (the clicks held off); (2) with the ladder live both records click at the cart on
the first pass; (3) at rest nothing here runs: the pointers bit for bit with the booking and
without, no Node ever newly covered. GAMEBOARD and COMPUTATION on the engine's integers; no pin."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_massive_record import massive_world, seed_source
from tests.test_receiver_by_name import CLOSED_CHAIN, emitter

CART_START = 200
CART_MOMENTUM = 48  # against the wall 3 x 64 x 1: one Link every four intervals, v = 1 / 4
LIGHT_PACE = 0.447  # the group pace of light's [512, 1] clock at k = pi / 2 (COMPUTATION, 9.24)


def cart_world(
    momentum: int = -CART_MOMENTUM, stock: int = 2, ticks: int = 700, start: int = CART_START
) -> dict:
    """The emitter A at [20, 52) naming the set `cart`, its two records along +x; the cart a
    silent block of matter over [200, 203) with the momentum `momentum` along x and the set
    `cart` bound to its Nodes (the detector follows the body, item 40's cube of three)."""
    document = massive_world([300, 1, 1], CLOSED_CHAIN, [800, 809])
    document["ticks"] = ticks
    document["clock_stamp"] = True
    # the cart's own massive family (its Nodes apart from the emitter's mode, which spans the
    # chain), the kind's pair [800, 809], the cart a barrier of it
    document["families"].append({"name": "cart", "quantum": 1, "pair": [800, 809], "charge": 0})
    cart = {
        "position": [start, 0, 0],
        "family": "cart",
        "amount": 1,
        "phase": 0,
        "momentum": [momentum, 0, 0],
        "fixed": True,
        "extents": [3, 1, 1],
        "pair": [800, 810],  # a barrier of matter's kind, no seed: light passes it untouched
    }
    document["measured"] = [emitter(20, "cart", 0, stock), cart]
    document["detectors"] = [{"name": "cart", "block": 1}]
    seed_source(document, 0)
    return document


def run(
    document: dict, hops: bool, clicks: bool, ticks: int
) -> tuple[DetectorLawSimulation, list[dict]]:
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    if not hops:
        simulation._hop_takings = lambda: None  # type: ignore[method-assign]
    if not clicks:
        simulation._ladder_click = lambda live, increments: None  # type: ignore[method-assign]
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def test_the_hop_books_the_covered_rows_so_the_whole_record_is_taken_over_a_pass():
    document = cart_world(stock=1)
    with_hops, _ = run(document, hops=True, clicks=False, ticks=600)
    without, _ = run(document, hops=False, clicks=False, ticks=600)
    cart = with_hops.detector_names.index("cart")
    (live,) = [live for live in with_hops.records.values() if live.family == 0]
    (other,) = [live for live in without.records.values() if live.family == 0]
    assert live.identity == other.identity and live.norm == other.norm and live.pace == other.pace
    norm = Fraction(live.norm, live.pace)
    booked = Fraction(live.pointers[cart]) + live.hop_carry
    plain = Fraction(other.pointers[cart])
    assert 0 <= live.hop_carry < 1 and other.hop_carry == 0
    # the cart passed through the whole record (its 32 Nodes at 0.447 against the cart's 0.25)
    assert with_hops.blocks[1].corner[0] < CART_START - 100
    assert abs(booked / norm - 1) < 0.08, float(booked / norm)
    share = CART_MOMENTUM / 192 / (CART_MOMENTUM / 192 + LIGHT_PACE)  # the hop's share, 0.36
    assert abs(float((booked - plain) / norm) - share) < 0.1, float((booked - plain) / norm)
    assert plain < booked


def test_both_records_click_at_the_moving_cart_on_the_first_pass():
    simulation, lines = run(cart_world(stock=2), hops=True, clicks=True, ticks=700)
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) == 2
    assert all(line["chosen"] and line["chosen"][0][0] == "cart" for line in gathers)
    # the first pass: the click before the cart has left the record's train behind
    for line in gathers:
        assert 0 < line["tick"] - line["giving"] < 400
    assert simulation.held[1][0] == 2  # two light quanta taken by the cart


def test_at_rest_the_rule_is_void_and_nothing_is_newly_covered():
    document = cart_world(momentum=0, stock=1)
    with_hops, lines_a = run(document, hops=True, clicks=True, ticks=300)
    without, lines_b = run(document, hops=False, clicks=True, ticks=300)
    assert with_hops.blocks[1].covered is None and with_hops.blocks[1].stepped == 0
    assert lines_a == lines_b
    for identity, live in with_hops.records.items():
        other = without.records[identity]
        assert live.pointers == other.pointers and live.hop_carry == 0
        assert np.array_equal(live.now, other.now)


def test_a_record_outrunning_the_cart_books_nothing_at_its_hops_and_the_back_face_re_enters_it():
    """IN THE BODY'S FRAME (item 48): the cart moving along +x at one Link every four intervals,
    the record given along +x at 0.447 overtakes it from behind. The rows the front face
    overtakes at a hop recede faster than the cart, so the hop books nothing of them (below one
    percent of the norm). A FINDING FOR THE MATHEMATICIAN, stated as the engine reads it: the
    Port booking in the board's frame books the record c / (c - v) = 2.27 times its norm over
    the passage, since the rows the back face uncovers at each hop re-enter through the back
    Port and are booked again (the ruling of 9.62 (3) books nothing at the back, one-way
    inward); the body-frame reading would book the norm once. COMPUTATION; no pin."""
    document = cart_world(momentum=CART_MOMENTUM, stock=1, ticks=700, start=60)
    with_hops, _ = run(document, hops=True, clicks=False, ticks=700)
    without, _ = run(document, hops=False, clicks=False, ticks=700)
    cart = with_hops.detector_names.index("cart")
    (live,) = [live for live in with_hops.records.values() if live.family == 0]
    (other,) = [live for live in without.records.values() if live.family == 0]
    norm = Fraction(live.norm, live.pace)
    booked = Fraction(live.pointers[cart]) + live.hop_carry
    plain = Fraction(other.pointers[cart])
    assert with_hops.blocks[1].stepped > 150  # the cart moved on; the record passed it
    assert abs(float((booked - plain) / norm)) < 0.01  # the hop books nothing of receding rows
    re_entry = LIGHT_PACE / (LIGHT_PACE - CART_MOMENTUM / 192)  # c / (c - v) = 2.27
    assert abs(float(plain / norm) - re_entry) < 0.1, float(plain / norm)

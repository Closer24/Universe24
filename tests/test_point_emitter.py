"""THE POINT EMITTER (ALGEBRA.md 9.69 (2), 9.71 (1); the model owner's word of 2026-09-25 through
the Boss, record 2054, "try to reduce them all to a Node"; BUILD.md section 26 item 50), a
hypothesis under its own identity, the world key `point_emitter`, off by default: on a chain
of 400 (x open) a one-Node well [800, 802] of the kind [800, 813] holds two light quanta and
gives by the window: (1) THE WINDOW: at the giving click no rows are written; every interval
the seat's rotation is added to the given row at the seat at the weight g and the outward
flux through the seat's two Ports is summed; the window closes at the first interval at which
the sum reaches the excitation's action T (norm / norm_denominator), the record then carrying
the norm of its rows, the giving line naming the record with the window's length and the
open's interval (the quantum moved at the open: the stock one less from there); the window at g = 4 is shorter than at g = 1 by about g^2
(the outward norm growing as the square of the written amplitude); the next giving comes after
the close (read 17.6); the books balanced at every interval. (2) THE INVERSE: inside a window the board
returns bit for bit over 40 intervals (the writes subtracted, the outward sum taken off).
(3) THE LOADER: the key needs body_record; a train under the key, a weight without it and a
missing weight or norm denominator under it are refused by name. COMPUTATION on the engine's
integers; no pin; the light clock's digests with the key off are the massive record suite's."""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_emitter import massive_generator
from tests.test_massive_record import massive_world

CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
KIND = [800, 813]
WELL = [800, 802]


def point_world(weight: int, stock: int = 2, ticks: int = 4000, length: int = 400) -> dict:
    """The chain with the one-Node point emitter at its middle; the mode seeded first (as
    `body_record`), the keys and the weight set after, the stamp renewed."""
    document = massive_world([length, 1, 1], CHAIN, KIND)
    document["ticks"] = ticks
    document["clock_stamp"] = True
    document["measured"] = [
        {
            "position": [length // 2, 0, 0],
            "family": "matter",
            "amount": 1,
            "ramp": 0,
            "start": 0,
            "stocks": {"light": stock},
            "momentum": [0, 0, 0],
            "extents": [1, 1, 1],
            "q": 0,
            "spin": [0, 0, 0],
            "moment": [0, 0, 0],
            "pair": list(WELL),
            "seed": 1 << 12,
            "margin": "control",
            "emitter": {"family": "light"},
        }
    ]
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    document["measured"][0]["emitter"]["weight"] = weight
    document["body_record"] = True
    document["stamp"] = input_stamp(document)
    return document


def run(document: dict, ticks: int) -> tuple[DetectorLawSimulation, list[dict]]:
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def test_the_window_writes_the_seats_rotation_and_closes_at_the_excitations_action():
    windows = {}
    for weight in (1, 4):
        document = point_world(weight)
        emitter = document["measured"][0]["emitter"]
        assert emitter["norm_denominator"] >= 1 and "train" not in emitter and "given" not in emitter
        simulation, lines = run(document, 4000)
        givings = [line for line in lines if line["event"] == "giving"]
        assert givings, weight
        first = givings[0]
        assert (
            first["train"] == 0
            and first["window"] >= 1
            and first["opened"] + first["window"] == first["tick"]
        )
        # the close: the outward sum reached T, the record's norm its rows'; the stock fell at
        # each open (the quantum moves at the open), a window still open counted
        assert first["outward"] * emitter["norm_denominator"] >= emitter["norm"]
        assert first["norm"] > 0 and first["pace"] >= 1
        opened = len(givings) + (1 if simulation.blocks[0].window is not None else 0)
        assert simulation.held[0][0] == 2 - opened
        if len(givings) > 1:
            assert givings[1]["opened"] > first["tick"]  # the next giving after the close
        windows[weight] = first["window"]
        # the record's rows: a light record with rows spread from the seat, the seat's level
        # written every interval of its window
        live = simulation.records.get(first["record"])
        if live is not None:
            assert live.family == 0 and not live.window_open and live.window == first["window"]
    ratio = windows[1] / windows[4]
    # read (COMPUTATION): g = 1 1124 intervals, g = 4 64, the ratio 17.6 beside g^2 = 16 (the
    # outward norm as the square of the written amplitude); the band admits the build-up
    assert 8 < ratio < 64, windows


def test_the_window_inverts_bit_for_bit():
    document = point_world(1, ticks=400)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    opened = None
    for _ in range(400):
        simulation.step()
        block = simulation.blocks[0]
        if block.window is not None:
            opened = simulation.tick
            break
    assert opened is not None
    for _ in range(20):
        simulation.step()
    live = simulation.records[simulation.blocks[0].window]  # type: ignore[index]
    assert live.window_open and live.window >= 20 and int(np.abs(live.now).max()) > 0
    state = (live.now.copy(), live.before.copy(), live.remainder.copy(), live.window, live.outward)
    seat = simulation.blocks[0].seat
    assert seat is not None
    seat_state = (seat.now, seat.before, seat.remainder)
    for _ in range(40):
        simulation.step()
    assert live.window == state[3] + 40
    for _ in range(40):
        simulation.step_inverse()
    assert np.array_equal(live.now, state[0]) and np.array_equal(live.before, state[1])
    assert np.array_equal(live.remainder, state[2])
    assert (live.window, live.outward) == (state[3], state[4])
    assert (seat.now, seat.before, seat.remainder) == seat_state


def test_the_loader_pairs_the_key_with_the_seat_the_weight_and_the_action():
    document = point_world(2, ticks=10)
    parse_nature_beam_world(document)
    # SINCE COMMIT 7 the window is the law's one giving: the lattice body gives by it too
    # (the level at its centre Node), the key `point_emitter` is retired and refused by name,
    # and so are the train's keys; the weight and the action are required on every emitter
    no_seat = json.loads(json.dumps(document))
    no_seat["body_record"] = False
    no_seat["stamp"] = input_stamp(no_seat)
    parse_nature_beam_world(no_seat)
    no_weight = json.loads(json.dumps(document))
    del no_weight["measured"][0]["emitter"]["weight"]
    no_weight["stamp"] = input_stamp(no_weight)
    with pytest.raises(ValueError, match="declares no `weight`"):
        parse_nature_beam_world(no_weight)
    no_action = json.loads(json.dumps(document))
    del no_action["measured"][0]["emitter"]["norm_denominator"]
    no_action["stamp"] = input_stamp(no_action)
    with pytest.raises(ValueError, match="declares no `norm_denominator`"):
        parse_nature_beam_world(no_action)
    for key, value in (("point_emitter", True), ("point_emitter", False)):
        retired = json.loads(json.dumps(document))
        retired[key] = value
        retired["stamp"] = input_stamp(retired)
        with pytest.raises(ValueError, match="point_emitter is refused"):
            parse_nature_beam_world(retired)
    with_train = json.loads(json.dumps(document))
    with_train["measured"][0]["emitter"]["train"] = {"direction": [1, 0, 0], "periods": 8}
    with_train["stamp"] = input_stamp(with_train)
    with pytest.raises(ValueError, match="emitter.train is refused"):
        parse_nature_beam_world(with_train)
    with_given = json.loads(json.dumps(document))
    with_given["measured"][0]["emitter"]["given"] = {"now": [1], "before": [-1], "norm": 1}
    with_given["stamp"] = input_stamp(with_given)
    with pytest.raises(ValueError, match="emitter.given is refused"):
        parse_nature_beam_world(with_given)

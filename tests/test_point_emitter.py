"""The point emitter, a hypothesis under its own identity (`point_emitter`, off by default): a one-Node well gives by the window, its Node's rotation added to the given row every interval."""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import point_world
from tests.running import run_point_world as run


@pytest.mark.diagnostic
def test_the_window_writes_the_bodys_rotation_and_closes_at_the_excitations_action():
    windows = {}
    for weight in (1, 4):
        document = point_world(weight)
        emitter = document["measured"][0]["emitter"]
        assert emitter["norm_denominator"] >= 1 and "train" not in emitter and "given" not in emitter
        simulation, lines = run(document, 4000)
        givings = [line for line in lines if line["event"] == "giving"]
        assert givings, weight
        first = givings[0]
        assert first["train"] == 0 and first["window"] >= 1
        assert first["opened"] + first["window"] == first["tick"]
        # the close: the outward sum reached T, the record's norm its rows'; the stock fell at each open (the quantum moves at the open), a window still open counted
        assert first["outward"] * emitter["norm_denominator"] >= emitter["norm"]
        assert first["norm"] > 0 and first["pace"] >= 1
        opened = len(givings) + (1 if simulation.blocks[0].window is not None else 0)
        assert simulation.held[0][0] == 2 - opened
        if len(givings) > 1:
            assert givings[1]["opened"] > first["tick"]  # the next giving after the close
        windows[weight] = first["window"]
        # the record's rows: a light record with rows spread from the body's Node, the body's Node's level
        # written every interval of its window
        live = simulation.records.get(first["record"])
        if live is not None:
            assert live.family == 0 and not live.window_open and live.window == first["window"]
    ratio = windows[1] / windows[4]
    # a GameBoard reading (COMPUTATION) from the engine's giving line, no detector in this world:
    # g = 1 1124 intervals, g = 4 64, the ratio 17.6 beside g^2 = 16 (the outward norm as the
    # square of the written amplitude); the band is a diagnostic check that the weight enters the
    # window, not a measurement pinned against nature; it admits the build-up
    assert 8 < ratio < 64, windows


def test_the_window_writes_the_bodys_rotation_at_both_levels():
    """The giving's write is the body's rotation, two levels (ALGEBRA.md #the-primitives the giving's row; #the-generator (d)): at the first write of a window the given record's `now` at the body's Nodes is the weight times the body's level now and its `before` the weight times the body's level before, so the record starts as the body's mode turning and not as a kick of one level; the inverse takes both back (the bit-for-bit test below)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(point_world(4, ticks=400)))
    block, mask = simulation.blocks[0], simulation.blocks[0].mask
    while block.window is None:
        simulation.step()
    simulation.step()  # the window's first write, right after the record's own step
    live, now = simulation.records[block.window], simulation._body_levels(block)  # type: ignore[index]
    before = simulation._body_levels(block, before=True)
    assert live.window == 1 and not np.array_equal(now, before) and np.abs(before).max() > 0
    assert np.array_equal(live.now[mask], 4 * now) and np.array_equal(live.before[mask], 4 * before)


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
    record = simulation.blocks[0].own
    assert record is not None
    record_state = (record.now.copy(), record.before.copy(), record.remainder.copy())
    for _ in range(40):
        simulation.step()
    assert live.window == state[3] + 40
    for _ in range(40):
        simulation.step_inverse()
    assert np.array_equal(live.now, state[0]) and np.array_equal(live.before, state[1])
    assert np.array_equal(live.remainder, state[2])
    assert (live.window, live.outward) == (state[3], state[4])
    assert all(
        np.array_equal(a, b)
        for a, b in zip((record.now, record.before, record.remainder), record_state, strict=True)
    )


def test_the_loader_pairs_the_key_with_the_one_node_body_the_weight_and_the_action():
    document = point_world(2, ticks=10)
    parse_nature_beam_world(document)
    # SINCE COMMIT 7 the window is the law's one giving: the lattice body gives by it too
    # (the level at its centre Node), the key `point_emitter` is retired and refused by name,
    # and so are the train's keys; the weight and the action are required on every emitter
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
        with pytest.raises(ValueError, match="the world has unknown keys: point_emitter"):
            parse_nature_beam_world(retired)
    with_train = json.loads(json.dumps(document))
    with_train["measured"][0]["emitter"]["train"] = {"direction": [1, 0, 0], "periods": 8}
    with_train["stamp"] = input_stamp(with_train)
    with pytest.raises(ValueError, match="emitter has unknown keys: train"):
        parse_nature_beam_world(with_train)
    with_given = json.loads(json.dumps(document))
    with_given["measured"][0]["emitter"]["given"] = {"now": [1], "before": [-1], "norm": 1}
    with_given["stamp"] = input_stamp(with_given)
    with pytest.raises(ValueError, match="emitter has unknown keys: given"):
        parse_nature_beam_world(with_given)

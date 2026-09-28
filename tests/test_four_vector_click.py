"""The four-vector click (ALGEBRA.md #the-primitives): a click moves a quantum's count and its momentum, and every click line reads the momentum its quantum travelled with, in the body's language."""

from __future__ import annotations

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from tests.bodies import point_world
from tests.running import lines_of
from tests.running import run as run_emitter
from tests.running import run_point_world as run_point
from tests.worlds import emitter_world, receiver_cube, seed_on_the_mode


def mirrored_emitter_world(ticks: int) -> dict:
    """The emitter's unit world reflected in x -> 79 - x: the body at [43, 75) (five Nodes to the closed end at 79, as the original's five at 0 to 4), the screen's cube at 7 to 9."""
    document = emitter_world(stock=2, ticks=ticks, on_mode=False)
    document["measured"] = [body := document["measured"][0]]
    body["position"] = [43, 0, 0]
    document["detectors"] = []
    receiver_cube(document, "screen", [7, 0, 0])
    seed_on_the_mode(document)
    return document


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_click_line_carries_the_taken_quantums_direction_and_the_giver_recoils():
    for document, sign in ((emitter_world(stock=2, ticks=600), 1), (mirrored_emitter_world(600), -1)):
        lines, simulation, _ = run_emitter(document)
        gathers, givings = lines_of(lines, "gather"), lines_of(lines, "giving")
        assert len(gathers) == 2 and len(givings) == 2
        assert all(line["chosen"] == [["screen", 0, "0"]] for line in gathers)
        # the four-vector: the count and the direction of travel toward the screen, along x
        assert all(line["content"] == 1 and line["momentum"] == [sign, 0, 0] for line in gathers)
        assert all(line["momentum"][1:] == [0, 0] for line in givings)
        # the body's language: the giver (the body 0), a taker that is not it (the screen's entry), the norm, the exact tally under the sign, the giver's count as the window opened; no recoil line on a giver off the mode (no wave number)
        assert all(line["giver"] == 0 and line["taker"] not in (0, None) for line in gathers)
        assert all(simulation.direction_of(line["tally"]) == line["momentum"] for line in gathers)
        assert all(isinstance(line["giver_clock"], int) and line["giver_clock"] > 0 for line in gathers)
        assert lines_of(lines, "recoil") == [] and simulation.books()["momentum"]["recoil"] == {}


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_a_symmetric_emitters_tallies_cancel_and_the_inverse_undoes_the_windows_tally():
    document = point_world(4, stock=3, ticks=400)
    simulation, lines = run_point(document, 200, givings=2)  # the horizon the window the engine writes
    givings = lines_of(lines, "giving")
    assert len(givings) == 2 and all(line["momentum"] == [0, 0, 0] for line in givings)
    # inside the third window (the third quantum's, opened within the second window's length of its close): the tally kept on the record, ten intervals on and back
    block = simulation.block_by_number[0]
    for _ in range(givings[1]["window"] + givings[1]["tick"] - givings[1]["opened"]):
        if block.window is not None:
            break
        simulation.step()
    assert block.window is not None
    live = simulation.records[block.window]
    kept, outward = ([simulation.step() for _ in range(3)] and list(live.outward_tally)), live.outward
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert live.window_open and (live.outward_tally, live.outward) != (kept, outward)
    for _ in range(10):
        simulation.step_inverse()
    assert live.outward_tally == kept and live.outward == outward


def test_the_direction_is_the_sign_per_axis():
    assert DetectorLawSimulation.direction_of([-5, 0, 7]) == [-1, 0, 1]
    assert DetectorLawSimulation.direction_of([0, 0, 0]) == [0, 0, 0]

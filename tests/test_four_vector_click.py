"""The four-vector click without the recoil (ALGEBRA.md 9.86 (1)): a click moves a quantum's count and
its momentum, and every click line reads the momentum its quantum travelled with."""

from __future__ import annotations

from event_universe.events.detector_law import DetectorLawSimulation
from tests.test_emitter import emitter_world, massive_generator
from tests.test_emitter import run as run_emitter
from tests.test_point_emitter import point_world
from tests.test_point_emitter import run as run_point


def mirrored_emitter_world(ticks: int) -> dict:
    """The emitter's unit world reflected in x -> 79 - x: the body at [43, 75) (five Nodes to
    the closed end at 79, as the original's five at 0 to 4), the screen's cube at 7 to 9."""
    from tests.test_detector_law import receiver_cube

    document = emitter_world(stock=2, ticks=ticks, on_mode=False)
    body = document["measured"][0]
    body["position"] = [43, 0, 0]
    document["measured"] = [body]
    document["detectors"] = []
    receiver_cube(document, "screen", [7, 0, 0])
    massive_generator().seed_on_the_mode(document)
    return document


def lines_of(lines: list[dict], event: str) -> list[dict]:
    return [line for line in lines if line["event"] == event]


def test_the_click_line_carries_the_taken_quantums_direction_and_no_body_moves():
    for document, sign in ((emitter_world(stock=2, ticks=600), 1), (mirrored_emitter_world(600), -1)):
        lines, simulation, _ = run_emitter(document)
        gathers, givings = lines_of(lines, "gather"), lines_of(lines, "giving")
        assert len(gathers) == 2 and len(givings) == 2
        assert all(line["chosen"] == [["screen", 0, "0"]] for line in gathers)
        # the four-vector: the count and the direction of travel toward the screen
        assert all(line["content"] == 1 and line["momentum"] == [sign, 0, 0] for line in gathers)
        # the given quantum's direction over the window
        assert all(line["momentum"] == [sign, 0, 0] for line in givings)
        # no recoil: every body's momentum stands; the quanta moved by the content alone
        assert all(block.momentum == [0, 0, 0] for block in simulation.blocks)
        light = next(index for index, family in enumerate(simulation.families) if family.name == "light")
        assert simulation.held[0][light] == 0  # the two light quanta given
        # the screen's bodies hold their own quantum each and the two taken
        loaded = sum(int(entry["amount"]) for entry in document["measured"][1:])
        assert (
            sum(simulation.held[number][light] for number in range(1, len(simulation.held)))
            == loaded + 2
        )


def test_a_symmetric_emitters_tallies_cancel_and_the_inverse_undoes_the_windows_tally():
    document = point_world(4, stock=3, ticks=400)
    simulation, lines = run_point(document, 200)
    givings = lines_of(lines, "giving")
    assert len(givings) == 2 and all(line["momentum"] == [0, 0, 0] for line in givings)
    # inside the third window (the third quantum's, within 150 intervals of the second's
    # close): the tally kept on the record, ten intervals on and back
    block = simulation.block_by_number[0]
    for _ in range(150):
        if block.window is not None:
            break
        simulation.step()
    assert block.window is not None
    live = simulation.records[block.window]
    for _ in range(3):
        simulation.step()
    kept, outward = list(live.outward_tally), live.outward
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

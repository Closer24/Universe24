"""The chain's kinds of clicks on a board of three dimensions, the shipped box beside the chain and the tube, examples/events/clicks/clicks_box.json (2026-10-22; the blind in examples/events/clicks/blind.md, its section The box, written before the run from design probes of the same lay). A closed box of 61 x 7 x 7 Nodes on the chain's universe at the quantum action 36000000; the one-Node absorber, an instrument of the file, at (51, 3, 3) in its content well with the declared pair [85, 2] and the lifetime 30, its window 32 as the loader derives it from the drive's passage; the chain's two photons, neutron and electron as transverse bumps along x, the second photon laid at two whole quanta so that the photon record's count is 2 (the second lay, the blind's section The box's second lay: a record's count is its laid share rounded to whole quanta, and at the count 0 the credit's fronts erase the record whole); the target and the screen as slabs of the whole cross-section; the draw's window 12. The pinned numbers are the second run's own, with their causes in the blind: the screen's credit of the second photon's first quantum at 24, the absorption at the body's first close 32, the target's credit of the electron at 36, the emission at 57 by the declared rate, the screen's credit of the record's next quantum and the neutron's credit with its conversion at 60, the body's null window at 64; the run's lines read from the shipped click log beyond the first thirty intervals stepped live, since the box costs about a second per interval."""

import json

from event_universe.lattice import Lattice
from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
WORLD = FOLDER / "clicks_box.json"
WINDOW, LIFETIME, BODY_WINDOW = (
    12,
    30,
    32,
)  # the regions' declared window; the body's declared lifetime; its window as the loader derives it from the drive's passage
FIRST, ABSORPTION, TARGET, EMISSION, SECOND, NEUTRON, NULL = (
    24,
    32,
    36,
    57,
    60,
    60,
    64,
)  # the closes of the blind's lines
BODY = (51, 3, 3)
SLABS = {
    "target": 13 * 49,
    "screen": 14 * 49,
}  # the slabs' Nodes, x 0..12 and x 37..50 over the 7 x 7 section


def test_the_box_declares_the_chains_bodies_and_regions_in_three_dimensions():
    world = load_shipped(WORLD)
    assert tuple(world.shape) == (61, 7, 7) and world.quantum_action == 36000000
    assert len(world.bodies) == 1 and world.bodies[0].detector.draw.window == BODY_WINDOW
    assert {d.name: len(d.positions) for d in world.node_detectors} == SLABS


def test_the_first_close_credits_the_screen_and_the_log_carries_the_lines():
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(WORLD), lines.append)
    for _ in range(30):
        board.step()
    credits = [
        (c["interval"], c["family"], c["node_detector"], c["count"])
        for c in lines
        if c.get("event") == "credit"
    ]
    assert credits == [(FIRST, "photon", "screen", 1)]  # the screen's credit at 24 alone before 30 ends
    log = json.loads(WORLD.with_suffix(".clicks.json").read_text(encoding="utf-8"))
    closes = [
        (row["interval"], row["family"], row["node_detector"], row.get("count"))
        for row in log
        if row.get("event") == "credit"
    ]
    assert closes[:7] == [
        (FIRST, "photon", "screen", 1),
        (ABSORPTION, "absorber", "body 0", 1),
        (TARGET, "electron", "target", 1),
        (EMISSION, "absorber", "body 0", 1),
        (SECOND, "photon", "screen", 1),
        (NEUTRON, "neutron", "target", 1),
        (NULL, "absorber", "body 0", 0),
    ]
    conversions = [row for row in log if row.get("event") == "conversion"]
    assert [(row["interval"], row["into"], row["senses"]) for row in conversions] == [
        (NEUTRON, ["proton", "electron"], [1, -1])
    ]

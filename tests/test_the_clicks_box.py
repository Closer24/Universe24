"""The chain's kinds of clicks on a board of three dimensions, the shipped box beside the chain and the tube, examples/events/clicks/clicks_box.json (2026-10-22; the blind in examples/events/clicks/blind.md, its section The box, written before the run from design probes of the same lay). A closed box of 61 x 7 x 7 Nodes on the chain's universe at the quantum action 36000000; the one-Node absorber, an instrument of the file, at (51, 3, 3) in its content well with the declared pair [85, 2] and the lifetime 30; the chain's two photons, neutron and electron as transverse bumps along x; the target and the screen as slabs of the whole cross-section; the draw's window 12. The pinned numbers are the run's own, with their causes in the blind: the absorption at the body's first close 30, the screen's credit of the second photon and the target's credit of the electron at 36, the emission at 35 by the declared rate, the body's null window at 60, the neutron's credit and conversion at 72, the counts at the end; the run's remaining lines read from the shipped click log, since the box costs about half a second per interval."""

import json

from event_universe.lattice import Lattice
from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
WORLD = FOLDER / "clicks_box.json"
WINDOW, LIFETIME = 12, 30  # the regions' declared window; the body's window, its lifetime
ABSORPTION, EMISSION, SCREEN, TARGET, NULL, NEUTRON = (
    30,
    35,
    36,
    36,
    60,
    72,
)  # the closes of the blind's six lines
BODY = (51, 3, 3)
SLABS = {
    "target": 13 * 49,
    "screen": 14 * 49,
}  # the slabs' Nodes, x 0..12 and x 37..50 over the 7 x 7 section


def test_the_box_declares_the_chains_bodies_and_regions_in_three_dimensions():
    world = load_shipped(WORLD)
    assert tuple(world.shape) == (61, 7, 7) and world.quantum_action == 36000000
    assert len(world.bodies) == 1 and world.bodies[0].detector.draw.window == LIFETIME
    assert {d.name: len(d.positions) for d in world.node_detectors} == SLABS


def test_the_first_close_takes_the_photon_and_the_log_carries_the_six_lines():
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(WORLD), lines.append)
    for _ in range(ABSORPTION):
        board.step()
    credits = [
        (c["interval"], c["family"], c["node_detector"], c["count"])
        for c in lines
        if c.get("event") == "credit"
    ]
    assert credits == [
        (ABSORPTION, "absorber", "body 0", 1)
    ]  # the absorption alone before 30 ends, no region's credit yet
    log = json.loads(WORLD.with_suffix(".clicks.json").read_text(encoding="utf-8"))
    closes = [
        (row["interval"], row["family"], row["node_detector"], row.get("count"))
        for row in log
        if row.get("event") == "credit"
    ]
    assert closes[:6] == [
        (ABSORPTION, "absorber", "body 0", 1),
        (EMISSION, "absorber", "body 0", 1),
        (SCREEN, "photon", "screen", 1),
        (TARGET, "electron", "target", 1),
        (NULL, "absorber", "body 0", 0),
        (NEUTRON, "neutron", "target", 1),
    ]
    conversions = [row for row in log if row.get("event") == "conversion"]
    assert [(row["interval"], row["into"], row["senses"]) for row in conversions] == [
        (NEUTRON, ["proton", "electron"], [1, -1])
    ]

"""The chain's kinds of clicks on a board of three dimensions, the shipped box beside the chain and the tube, examples/events/clicks/clicks_box.json (2026-10-22; the blind in examples/events/clicks/blind.md, its section The box, written before the run from design probes of the same lay). A closed box of 61 x 7 x 7 Nodes on the chain's universe at the quantum action 36000000; the one-Node absorber, an instrument of the file, at (51, 3, 3) in its content well with the declared pair [85, 2] and the lifetime 30, its window 32 as the loader derives it from the drive's passage; the chain's two photons, neutron and electron as transverse bumps along x, the second photon laid at the amplitude 2200 so that the photon record's count is 3 by the lays' roundings (the fourth lay, the blind's section The box's fourth blind, after the second lay's count 2: a record's count is its laid share rounded to whole quanta, and at the count 0 the credit's fronts erase the record whole); the target and the screen as slabs of the whole cross-section; the draw's window 12. The pinned numbers are the fourth run's own, with their causes in the blind: the screen's credits of the second photon's two quanta at 24 and 36, the absorption at the body's first close 32, the target's credit of the electron at 36, the neutron's credit with its conversion at 60, the emission at 64 by the declared rate, the screen's credit of the emitted light at 84 (the sixth kind in substance), the body's first null window at 125; the run's lines read from the shipped click log beyond the first thirty intervals stepped live, since the box costs about a second per interval. The test steps no emission: the thirty live intervals hold none, and the log's lines are the fourth run's, which stands under the chain's integers (the factor 11.577) until its re-run under wave_cosine (11.543; blind.md, the fourth outcome)."""

from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
WORLD = FOLDER / "clicks_box.json"
BODY_WINDOW = 32  # the body's window as the loader derives it from the drive's passage
SLABS = {
    "target": 13 * 49,
    "screen": 14 * 49,
}  # the slabs' Nodes, x 0..12 and x 37..50 over the 7 x 7 section


def test_the_box_declares_the_chains_bodies_and_regions_in_three_dimensions():
    world = load_shipped(WORLD)
    assert tuple(world.shape) == (61, 7, 7) and world.quantum_action == 36000000
    assert len(world.bodies) == 1 and world.bodies[0].detector.draw.window == BODY_WINDOW
    assert {d.name: len(d.positions) for d in world.node_detectors} == SLABS

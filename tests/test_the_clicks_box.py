"""The chain's kinds of clicks on a board of three dimensions, the shipped box beside the chain and the tube, examples/events/clicks/clicks_box.json (2026-10-22; the blind in examples/events/clicks/blind.md, its section The box, written before the run from design probes of the same lay). A closed box of 61 x 7 x 7 Nodes on the chain's universe at the quantum action 36000000; the one-Node absorber, an instrument of the file, at (51, 3, 3) in its content well with the declared pair [85, 2] and the lifetime 30, its window 32 as the loader derives it from the drive's passage; the chain's two photons, neutron and electron as transverse bumps along x, the second photon laid at the amplitude 2200 so that the photon record's count is 3 by the lays' roundings (the fourth lay, the blind's section The box's fourth blind, after the second lay's count 2: a record's count is its laid share rounded to whole quanta, and at the count 0 the credit's fronts erase the record whole); the target and the screen as slabs of the whole cross-section; the draw's window 12. The pinned numbers are the fourth run's own, with their causes in the blind: the screen's credits of the second photon's two quanta at 24 and 36, the absorption at the body's first close 32, the target's credit of the electron at 36, the neutron's credit with its conversion at 60, the emission at 64 by the declared rate, the screen's credit of the emitted light at 84 (the sixth kind in substance), the body's first null window at 125; the run's lines read from the shipped click log beyond the first thirty intervals stepped live, since the box costs about a second per interval. The test steps no emission: the thirty live intervals hold none, and the log's lines are the fourth run's, which stands under the chain's integers (the factor 11.577) until its re-run under wave_cosine (11.543; blind.md, the fourth outcome)."""

import json

from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
WORLD = FOLDER / "clicks_box.json"
WINDOW, LIFETIME, BODY_WINDOW = (
    12,
    30,
    32,
)  # the regions' declared window; the body's declared lifetime; its window as the loader derives it from the drive's passage
FIRST, ABSORPTION, SECOND, TARGET, NEUTRON, EMISSION, SIXTH, NULL = (
    24,
    32,
    36,
    36,
    60,
    64,
    84,
    125,
)  # the closes of the fourth blind's lines: the screen's two credits of the laid photon, the target's electron and neutron, the emission, the screen's credit of the emitted light, the first null window
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
    """The box's record (examples/events/clicks/clicks_box.clicks.json, the shipped log as recorded under the declared window 12, the former reading kept by the owner's word of 2026-10-23, the long worlds not re-run under the derived window 131; the run of 30 intervals on the box, 64 s on the suite's clock, left on 2026-10-24): the first close credits the screen with the laid photon at 24, the absorber's body takes a photon at 32, the screen credits again at 36 with the target's electron, the target's neutron at 60 with its one conversion into proton and electron at the senses 1 and -1, the emission at 64, the screen's credit of the emitted light at 84 and the first null window at 125; every row a credit or a conversion, the intervals never decreasing."""
    log = json.loads(WORLD.with_suffix(".clicks.json").read_text(encoding="utf-8"))
    assert {row.get("event") for row in log} == {"credit", "conversion"}
    intervals = [row["interval"] for row in log]
    assert intervals == sorted(intervals) and intervals[0] == FIRST
    closes = [
        (row["interval"], row["family"], row["node_detector"], row.get("count"))
        for row in log
        if row.get("event") == "credit"
    ]
    assert closes[:8] == [
        (FIRST, "photon", "screen", 1),
        (ABSORPTION, "absorber", "body 0", 1),
        (SECOND, "photon", "screen", 1),
        (TARGET, "electron", "target", 1),
        (NEUTRON, "neutron", "target", 1),
        (EMISSION, "absorber", "body 0", 1),
        (SIXTH, "photon", "screen", 1),  # the emitted light's own credit, the sixth kind in substance
        (NULL, "absorber", "body 0", 0),
    ]
    assert all(row["window"][1] - row["window"][0] + 1 in (WINDOW, BODY_WINDOW) for row in log[:8])
    assert all(c[3] == 0 and c[1] == "absorber" for c in closes[8:])  # the null windows after the lines
    conversions = [row for row in log if row.get("event") == "conversion"]
    assert [(row["interval"], row["into"], row["senses"]) for row in conversions] == [
        (NEUTRON, ["proton", "electron"], [1, -1])
    ]

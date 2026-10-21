"""The three kinds of clicks of the one law in one shipped world, examples/events/clicks/clicks_chain.json (2026-10-21; the blind in examples/events/clicks/blind.md, written before the run; ALGEBRA.md, The click writes on the lattice; The conversion): a region's credit of a light packet, an instrument body's absorption of a light packet and a neutron's conversion at its target region, each at a window's close, each written at one Node through the one act with the hole and, at the count 0, the erasing front. The pinned numbers are the blind's, derived from the paces, the envelopes and the windows: the screen's credit at the close 24 (the second photon's share past its front Link 0.94 quanta by then by the envelope, 0.14 at 12, the count's rounding), the body's window 32 (the 17-Node lay's passage over its one Node at the group pace 0.5469 Links per interval, 3 den 17 sin omega over |num| sin k carried up, lit at the interval 1 by the lay's level 16) and the conversion at the close 48 (the neutron's share past the target's front Link 0.985 by then, 0.41 at 36); the holes at the three regions' one front Node each, 88, 62 and 20; the planes' exact split 5450 + 5458 + 5476 = 16384 against the electron's -16384 (features/click.plane_squares at T div 2)."""

from event_universe import reports
from event_universe.lattice import Lattice
from tests.laws import EVENTS, family
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
SCREEN, BODY, TARGET = (
    24,
    32,
    48,
)  # the three closes: the screen's credit, the body's absorption, the conversion
HALF_ACTION = 16384  # T div 2 at T = 32768, one quantum's Wronskian at the quarter-turn lay
HOLES = (
    ("photon", 88, 25),
    ("photon", 62, 33),
    ("neutron", 20, 49),
)  # the family, the front Node, the first face


def wronskians(lays: list[dict]) -> list[int]:  # type: ignore[type-arg]
    """Per plane of a family's lay lines, re_now im_before - im_now re_before of the levels after the lay."""
    lines = sorted(lays, key=lambda row: row["line"])
    return [
        a["after"][0] * b["after"][1] - b["after"][0] * a["after"][1]
        for a, b in zip(lines[0::2], lines[1::2], strict=True)
    ]


def test_the_three_kinds_of_clicks_fall_at_their_derived_closes_in_one_world():
    """The blind on the shipped world over its first 50 intervals: the body's window 32 derived at load; three measurement lines and one conversion line, in order: the screen's credit of the photon at 24 (count 1, left 1, the window [13, 24]), the body's absorption at 32 (g to e, absorbed photon, count 1, left 0, the window [1, 32]), the target's credit of the neutron at 48 (count 1, left 0, the window [37, 48]) with its conversion into [proton, electron] at the senses [1, -1]; the holes at 88 (no front: one quantum left), 62 and 20 (the fronts from both); the lays at 20 with the proton's Wronskians at the exact split summing to T div 2 and the electron's -T div 2, the sum 0; the books photon 0, absorber 1 in its part e, neutron 0, proton 1, electron 1, no deficit."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(FOLDER / "clicks_chain.json"), lines.append)
    photon, absorber, neutron = (family(board, name) for name in ("photon", "absorber", "neutron"))
    body_row = board.world.bodies[0].detector
    assert body_row is not None and body_row.draw is not None
    assert body_row.draw.window == BODY  # derived at load from the lay's passage, no key
    assert (
        board.credit.counts[photon],
        board.credit.counts[absorber],
        board.credit.counts[neutron],
    ) == (2, 1, 1)
    for _ in range(TARGET + 2):  # through the neutron's two faces at 49 and 50
        board.step()
    measured = [c for c in lines if c["event"] in (reports.CREDIT, reports.CONVERSION)]
    assert [(c["label"], c["interval"], c["node_detector"], c["family"]) for c in measured] == [
        (reports.MEASUREMENT, SCREEN, "screen", "photon"),
        (reports.MEASUREMENT, BODY, "body 0", "absorber"),
        (reports.MEASUREMENT, TARGET, "target", "neutron"),
        (reports.MEASUREMENT, TARGET, "target", "neutron"),
    ]
    screen, body, target, converted = measured
    assert (screen["count"], screen["left"], screen["window"], screen["realised"], screen["kept"]) == (
        1,
        1,
        [13, 24],
        None,
        [0],
    )
    assert (screen["source"], screen["recoil"]) == (reports.THE_LAY, reports.UNPAID_BY_REGION)
    assert (body["before"], body["realised"], body["absorbed"], body["count"], body["left"]) == (
        "g",
        "e",
        "photon",
        1,
        0,
    )
    assert body["window"] == [1, BODY] and body["emitted"] is None
    assert (target["count"], target["left"], target["window"]) == (1, 0, [TARGET - 11, TARGET])
    assert converted["event"] == reports.CONVERSION and converted["window"] == target["window"]
    assert (converted["into"], converted["senses"]) == (["proton", "electron"], [1, -1])
    for name, node, first in HOLES:  # the hole: every line faced to 0 at the one Node, two intervals
        at = sorted(
            {
                f["interval"]
                for f in lines
                if f["event"] == reports.FACE and f["family"] == name and f["node"]["at"][0] == node
            }
        )
        assert at[:2] == [first, first + 1], (name, node, at[:4])
    fronts = {(e["family"], tuple(e["origin"])) for e in lines if e["event"] == reports.ERASURE}
    assert fronts == {("photon", (62, 0, 0)), ("neutron", (20, 0, 0))}  # none from 88: the count 1 there
    lays = [row for row in lines if row["event"] == reports.LAY and row["interval"] == TARGET]
    assert {tuple(row["node"]["at"]) for row in lays} == {(20, 0, 0)} and len(lays) == 8
    proton_w = wronskians([row for row in lays if row["family"] == "proton"])
    electron_w = wronskians([row for row in lays if row["family"] == "electron"])
    assert (
        sorted(proton_w) == [5450, 5458, 5476] and sum(proton_w) == HALF_ACTION
    )  # the exact split, the sense 1
    assert (
        electron_w == [-HALF_ACTION] and sum(proton_w) + sum(electron_w) == 0
    )  # the sense -1, the charge kept
    counts = {board.families[i].name: board.credit.counts[i] for i in board.order}
    assert counts == {
        "photon": 0,
        "absorber": 1,
        "neutron": 0,
        "proton": 1,
        "electron": 1,
        "antineutrino": 0,
    }
    assert board.credit.bodies[0].counts == [0, 1] and board.credit.bodies[0].part == 1  # the body in e
    assert not any(board.credit.deficits.values())  # every quantum written where it was taken or given

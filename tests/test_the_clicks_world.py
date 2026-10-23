"""Four of the five kinds of clicks of the one law in one shipped world, examples/events/clicks/clicks_chain.json (2026-10-21; the blinds in examples/events/clicks/blind.md, written before the runs, their dated paragraph under the whether as one rule; ALGEBRA.md, The click writes on the lattice; The conversion): light's click at a region (the screen on a photon packet at the close 24, and on the body-emitted photon at 120), a region's plain credit of a massive record (the target on an electron packet at 48), the pixel's click (the one-Node absorber absorbing a photon at its derived window's close 32 and emitting one by the law's (5), a source in time at its Node, at the close 64) and a conversion (the neutron at the target at 60 into a proton and an electron at the senses 1 and -1); the bound body's click absent by name. The pinned numbers and their causes under the rule of 2026-10-21 (the count the floor of the window's inflow with the carried remainder, the remainder below one quantum drawn by the read of the board, the half-up rounding gone): the screen's credit at 24 (the booked share 0.046 at 12 drawn none, 0.887 with the carry at 24 drawn one), the target's credit of the electron at 48 (0.698 at 24 and 0.721 at 36 drawn none, 0.745 at 48 drawn one), the body's window 32 (the 17-Node lay's passage over one Node, lit at 1; the absorption's draw at the share 0.99999), the conversion at 60 (the neutron's 0.225 at 36 and 0.627 at 48 drawn none, 0.863 at 60 drawn one), the emission at 64 (the window's close, the digits' draw at the hazard 0.04125 per dark interval), the screen's credit of the emitted photon at 120 (0.359 carried from the first photon's remnant at the count 0, 0.492 with the light's inflow at 120, drawn one), the holes at the regions' one front Node each (88, 20) and the body's own (62), the planes' exact split 5450 + 5458 + 5476 = 16384 against -16384; every number the re-run's on the rule, none derived from the rounding's run."""

from event_universe import reports
from event_universe.lattice import Lattice
from tests.laws import EVENTS, family
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
SCREEN, BODY, CELL, TARGET, EMISSION, LIGHT = (
    24,
    32,
    24,
    60,
    53,
    60,
)  # the closes of the seven lines under The stress is the Links' (2026-10-23; the former reading's 24, 32, 48, 60, 64, 120)
HALF_ACTION = 16384  # T div 2 at T = 32768, one quantum's Wronskian at the quarter-turn lay
HOLES = (
    ("electron", 20, 25),
    ("photon", 88, 25),
    ("photon", 62, 33),
    ("neutron", 20, 61),
    ("photon", 88, 61),
)
FRONTS = {
    ("electron", (20, 0, 0)),
    ("neutron", (20, 0, 0)),
    ("photon", (62, 0, 0)),
    ("photon", (88, 0, 0)),
}


def wronskians(lays: list[dict]) -> list[int]:  # type: ignore[type-arg]
    """Per plane of a family's lay lines, re_now im_before - im_now re_before of the levels after the lay."""
    lines = sorted(lays, key=lambda row: row["line"])
    return [
        a["after"][0] * b["after"][1] - b["after"][0] * a["after"][1]
        for a, b in zip(lines[0::2], lines[1::2], strict=True)
    ]


def test_four_kinds_of_clicks_fall_at_their_closes_in_one_world():
    """The blinds on the shipped world over 122 intervals under the whether as one rule: the body's window 32 derived at load; the measurement lines in order, the screen's credit of the photon at 24 (count 1, left 1, the window [13, 24]), the body's absorption at 32 (g to e, absorbed photon, left 0), the target's credit of the electron packet at 48 (count 1, left 0, drawn at 0.745), the target's credit of the neutron at 60 with its conversion into [proton, electron] at [1, -1] (drawn at 0.863), the body's emission at 64 (e to g, emitted photon, the photon's count 1), the screen's credit of the body's photon at 120 (count 1, left 0, the source the body, drawn at 0.492); the holes at 20 (the electron at 49, the neutron at 61), 88 (25 and 121) and 62 (33); the four fronts; the eight lays at 20 at 60 with the exact split summing to 0; the books photon 0, absorber 1 in g, neutron 0, proton 1, electron 1, no deficit."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(FOLDER / "clicks_chain.json"), lines.append)
    photon, absorber, neutron, electron = (
        family(board, name) for name in ("photon", "absorber", "neutron", "electron")
    )
    body_row = board.world.bodies[0].detector
    assert body_row is not None and body_row.draw is not None and body_row.draw.window == BODY
    assert [body_row.rates[0].lifetime, body_row.rates[0].light] == [
        24,
        photon,
    ]  # the law's (5), declared
    counts = board.credit.counts
    assert (counts[photon], counts[absorber], counts[neutron], counts[electron]) == (2, 1, 1, 1)
    for _ in range(LIGHT + 2):  # through the emitted photon's hole at 133 and 134
        board.step()
    measured = [c for c in lines if c["label"] == reports.MEASUREMENT and c["event"] != reports.CLICK]
    measured = [c for c in measured if c["event"] in (reports.CREDIT, reports.CONVERSION)]
    assert (
        [(c["interval"], c["node_detector"], c["family"], c["event"]) for c in measured]
        == [
            (SCREEN, "screen", "photon", "credit"),
            (CELL, "target", "electron", "credit"),
            (BODY, "body 0", "absorber", "credit"),
            (EMISSION, "body 0", "absorber", "credit"),
            (LIGHT, "screen", "photon", "credit"),
            (TARGET, "target", "neutron", "credit"),
            (TARGET, "target", "neutron", "conversion"),
        ]
    )  # the order under The stress is the Links' (2026-10-23): the body's pressure read at its neighbours moves the paces the records read around it, the electron's cell click to 24, the emission to 53 and the emitted photon's screen click to 60 (the former reading's 48, 64 and 120)
    screen, cell, body, emitted, light, target, converted = measured
    assert (screen["count"], screen["left"], screen["window"], screen["kept"]) == (1, 1, [13, 24], [0])
    assert (cell["count"], cell["left"], cell["window"], cell["realised"]) == (
        1,
        0,
        [CELL - 11, CELL],
        None,
    )
    assert (cell["source"], cell["recoil"]) == (reports.THE_LAY, reports.UNPAID_BY_REGION)
    assert (body["before"], body["realised"], body["absorbed"], body["count"], body["left"]) == (
        "g",
        "e",
        "photon",
        1,
        0,
    )
    assert (target["count"], target["left"], target["window"]) == (1, 0, [TARGET - 11, TARGET])
    assert (converted["into"], converted["senses"]) == (["proton", "electron"], [1, -1])
    assert (
        emitted["before"],
        emitted["realised"],
        emitted["emitted"],
        emitted["count"],
        emitted["left"],
    ) == ("e", "g", "photon", 1, 1)
    assert emitted["window"] == [BODY + 1, EMISSION] and emitted["absorbed"] is None
    assert (light["count"], light["left"], light["source"], light["recoil"]) == (
        1,
        0,
        "body 0",
        reports.UNPAID_BY_REGION,
    )
    for name, node, first in HOLES:  # the hole: every line faced to 0 at the one Node, two intervals
        at = sorted(
            {
                f["interval"]
                for f in lines
                if f["event"] == reports.FACE and f["family"] == name and f["node"]["at"][0] == node
            }
        )
        assert [first, first + 1] == [t for t in at if t >= first][:2], (name, node, at[:4])
    fronts = {(e["family"], tuple(e["origin"])) for e in lines if e["event"] == reports.ERASURE}
    assert fronts == FRONTS  # a front at the count 0 alone: none from the screen's first credit
    lays = [
        row
        for row in lines
        if row["event"] == reports.LAY
        and row["interval"] == TARGET
        and row["family"] in ("proton", "electron")
    ]  # the conversion's eight lays; the emitted photon's own lays at 62 fall in the same interval under the law's reading (2026-10-23)
    assert {tuple(row["node"]["at"]) for row in lays} == {(20, 0, 0)} and len(lays) == 8
    proton_w = wronskians([row for row in lays if row["family"] == "proton"])
    electron_w = wronskians([row for row in lays if row["family"] == "electron"])
    assert sorted(proton_w) == [5450, 5458, 5476] and sum(proton_w) == HALF_ACTION  # the exact split
    assert electron_w == [-HALF_ACTION] and sum(proton_w) + sum(electron_w) == 0  # the charge kept
    sourced = [
        r
        for r in lines
        if r["event"] == reports.LAY and r["family"] == "photon" and r["node"]["at"][0] == 62
    ]
    assert (
        len([r for r in sourced if EMISSION <= r["interval"] < EMISSION + 24]) >= 10
    )  # the source in time: ten lays from 53, the emitted photon clicking at the screen at 60 under the law's reading (2026-10-23; the former reading's twenty before its click at 168)
    final = {board.families[i].name: counts[i] for i in board.order}
    assert final == {
        "photon": 0,
        "absorber": 1,
        "neutron": 0,
        "proton": 1,
        "electron": 1,
        "antineutrino": 0,
    }
    assert board.credit.bodies[0].counts == [1, 0] and board.credit.bodies[0].part == 0  # back in g
    assert not any(board.credit.deficits.values())

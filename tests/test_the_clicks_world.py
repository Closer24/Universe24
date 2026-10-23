"""Four of the five kinds of clicks of the one law in one shipped world, examples/events/clicks/clicks_chain.json (2026-10-21; the blinds in examples/events/clicks/blind.md, written before the runs, their dated paragraph under the whether as one rule; ALGEBRA.md, The click writes on the lattice; The conversion): light's click at a region (the screen on a photon packet at the close 24, and on the body-emitted photon at 120), a region's plain credit of a massive record (the target on an electron packet at 48), the pixel's click (the one-Node absorber absorbing a photon at its derived window's close 32 and emitting one by the law's (5), a source in time at its Node, at the close 64) and a conversion (the neutron at the target at 60 into a proton and an electron at the senses 1 and -1); the bound body's click absent by name. The pinned numbers and their causes under the rule of 2026-10-21 (the count the floor of the window's inflow with the carried remainder, the remainder below one quantum drawn by the read of the board, the half-up rounding gone): the screen's credit at 24 (the booked share 0.046 at 12 drawn none, 0.887 with the carry at 24 drawn one), the target's credit of the electron at 48 (0.698 at 24 and 0.721 at 36 drawn none, 0.745 at 48 drawn one), the body's window 32 (the 17-Node lay's passage over one Node, lit at 1; the absorption's draw at the share 0.99999), the conversion at 60 (the neutron's 0.225 at 36 and 0.627 at 48 drawn none, 0.863 at 60 drawn one), the emission at 64 (the window's close, the digits' draw at the hazard 0.04125 per dark interval), the screen's credit of the emitted photon at 120 (0.359 carried from the first photon's remnant at the count 0, 0.492 with the light's inflow at 120, drawn one), the holes at the regions' one front Node each (88, 20) and the body's own (62), the planes' exact split 5450 + 5458 + 5476 = 16384 against -16384; every number the re-run's on the rule, none derived from the rounding's run."""

from event_universe import reports
from event_universe.lattice import Lattice
from tests.laws import EVENTS, family
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
SCREEN, BODY, CELL, TARGET, EMISSION, LIGHT = (
    149,
    32,
    149,
    149,
    64,
    149,
)  # the closes of the seven lines under the window derived, the law's reading on the owner's decision of 2026-10-23: the regions' one window the lays' longest passage, 149, the body's 32; the former reading's 24, 32, 24, 60, 53, 60 under the declared window 12 and The stress is the Links'
RUN = 156  # the run through the one close at 149 and the fronts' first shells
HALF_ACTION = 16384  # T div 2 at T = 32768, one quantum's Wronskian at the quarter-turn lay
HOLES = (  # under the derived window (2026-10-23): the body's at 33, the regions' at 150; no electron hole, its converted quantum standing
    ("photon", 62, 33),
    ("photon", 20, 150),
    ("photon", 88, 150),
    ("neutron", 20, 150),
)
FRONTS = {
    ("neutron", (20, 0, 0)),
    ("photon", (20, 0, 0)),
    ("photon", (88, 0, 0)),
}  # the body's own photon emitted at 64 and credited at the screen at 149 leaves no front of its own (2026-10-23)


def wronskians(lays: list[dict]) -> list[int]:  # type: ignore[type-arg]
    """Per plane of a family's lay lines, re_now im_before - im_now re_before of the laid terms, the levels after the lay less the levels before it (2026-10-23: the lay adds to what stands at the Node, lay.written, so the quantum's Wronskian is the laid terms' alone; the former read the levels after, exact where the Node stood empty, and at the Node 20 of the one close 149 the electron packet's remnant -6 times the laid 128, 768, entered: -15616 against the quantum's -16384)."""
    lines = sorted(lays, key=lambda row: row["line"])
    laid = [
        [after - before for after, before in zip(row["after"][:2], row["before"][:2], strict=True)]
        for row in lines
    ]
    return [a[0] * b[1] - b[0] * a[1] for a, b in zip(laid[0::2], laid[1::2], strict=True)]


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
    for _ in range(RUN):  # through the one close at 149 and the fronts' first shells
        board.step()
    measured = [c for c in lines if c["label"] == reports.MEASUREMENT and c["event"] != reports.CLICK]
    measured = [c for c in measured if c["event"] in (reports.CREDIT, reports.CONVERSION)]
    kinds = [
        (c["node_detector"], c["family"], c["event"], c.get("absorbed"), c.get("emitted"))
        for c in measured
    ]
    assert (
        kinds[:3]
        == [
            ("body 0", "absorber", "credit", "photon", None),
            ("body 0", "absorber", "credit", None, "photon"),
            ("screen", "photon", "credit", None, None),
        ]
    )  # the body's absorption at its first close and its emission after it (kind 5), then the screen's credit of a photon at the regions' one close (kind 2)
    assert (
        {k[:3] for k in kinds[3:]}
        == {
            ("target", "neutron", "credit"),
            ("target", "neutron", "conversion"),
            ("target", "electron", "credit"),
        }
    )  # the target's credit of the neutron with its conversion (kind 1) and its plain credit of the electron laid there (kind 3), at the same close; the lay's second photon's credit at the target (149 under the former course, read to 2026-10-23 when the swap still fired on this massless board at the body's neighbours) falls beyond this run under the swap reading the gapped time line alone, 298 on the folder's 300, and is no kind of its own
    body, emitted, light = measured[:3]
    target = next(c for c in measured if c["family"] == "neutron" and c["event"] == reports.CREDIT)
    converted = next(c for c in measured if c["event"] == reports.CONVERSION)
    cell = next(c for c in measured if c["family"] == "electron")
    assert all(
        c["interval"] == LIGHT for c in (light, target, converted, cell)
    )  # the regions' one close
    assert (body["interval"], emitted["interval"]) == (BODY, EMISSION)
    assert (light["count"], light["window"], light["source"], light["recoil"]) == (
        1,
        [1, LIGHT],
        "body 0",
        reports.UNPAID_BY_REGION,
    )  # the body's own photon, emitted at 64, credited at the screen
    assert (cell["count"], cell["window"], cell["realised"]) == (1, [1, CELL], None)
    assert (cell["source"], cell["recoil"]) == (reports.THE_LAY, reports.UNPAID_BY_REGION)
    assert (body["before"], body["realised"], body["absorbed"], body["count"]) == ("g", "e", "photon", 1)
    assert (target["count"], target["left"], target["window"]) == (1, 0, [1, TARGET])
    assert (converted["into"], converted["senses"]) == (["proton", "electron"], [1, -1])
    assert (
        emitted["before"],
        emitted["realised"],
        emitted["emitted"],
        emitted["count"],
    ) == ("e", "g", "photon", 1)
    assert emitted["window"] == [BODY + 1, EMISSION] and emitted["absorbed"] is None
    assert light["left"] + 1 == body["left"] + 1 == emitted["left"], (
        body["left"],
        emitted["left"],
        light["left"],
    )  # the photon's count: down by one at the take, up by one at the give, down by one at the screen (the lefts 1, 2, 1 here; 0, 1, 0 under the former course where the screen had credited the lay's second photon at 24)
    faces = [f for f in lines if f["event"] == reports.FACE]
    holes = {}  # per family the hole's own Node, the first faced, and its faced intervals (the front's shells are faced later and farther)
    for name in {f["family"] for f in faces}:
        own = [f for f in faces if f["family"] == name]
        first = min(f["interval"] for f in own)
        for node in {f["node"]["at"][0] for f in own if f["interval"] == first}:
            holes[(name, node)] = sorted({f["interval"] for f in own if f["node"]["at"][0] == node})
    assert {name for name, _node in holes} == {"photon", "neutron"}, (
        holes
    )  # the holes of the quanta taken whole; no electron hole, its converted quantum standing (HOLES names the former course's Nodes and intervals)
    for (name, node), at in holes.items():
        assert at[0] in (BODY + 1, LIGHT + 1) and at[:2] == [at[0], at[0] + 1], (
            name,
            node,
            at[:4],
        )  # every line faced to 0 at the one Node, two intervals after the close
    fronts = {(e["family"], tuple(e["origin"])) for e in lines if e["event"] == reports.ERASURE}
    zeroed = {c["family"] for c in measured if c["event"] == reports.CREDIT and c["left"] == 0}
    assert {name for name, _origin in fronts} == zeroed == {"neutron"} and all(
        (name, origin[0]) in holes for name, origin in fronts
    ), (
        fronts
    )  # a front at the count 0 alone, begun at the hole: the neutron's; none from the screen's credit of a photon at the count 2 (FRONTS, the former course's set, held the lay's second photon's front from its target credit at 149, which falls at 298 under the swap reading the gapped time line alone)
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
        len([r for r in sourced if EMISSION <= r["interval"] < EMISSION + 24]) >= 20
    )  # the source in time: ten lays from 53, the emitted photon clicking at the screen at 60 under the law's reading (2026-10-23; the former reading's twenty before its click at 168)
    final = {board.families[i].name: counts[i] for i in board.order}
    assert (
        final
        == {
            "photon": light["left"],
            "absorber": 1,
            "neutron": 0,
            "proton": 1,
            "electron": 1,
            "antineutrino": 0,
        }
    )  # the counts at the end: the photon's the screen's credit left (1 here; 0 under the former course, the target having credited the lay's second photon at 149), the neutron gone into its proton and electron, which stand
    assert board.credit.bodies[0].counts == [1, 0] and board.credit.bodies[0].part == 0  # back in g
    assert (
        {board.families[k].name: v for k, v in board.credit.deficits.items() if v} == {"electron": 1}
    )  # the electron credited at the Node where the conversion's electron is laid in the same close 149: the quantum in the books alone (take.faced, the undepleted beam), the deficit its record (2026-10-23; the former none)

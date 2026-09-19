"""The three corrections of the model owner of 2026-09-19 (Highlights 5.4,
"three reversible corrections that every path shares"): no merge, an open
face is a detector, and the clock's count read off the clock. Bars, K 16 or
K 2^20 so that no phase moves, N 64. The expected integers of
docs/TEST_EXPECTATIONS.md ("The border and the clock's count"), written
down first:

(a) no merge: a bar of 3 x 1 x 1, `release` [0, 1], `suspension` 0, the
    free family `m`; a measured event of content 16 with momentum (16, 0, 0)
    at x = 0 and one of content 16 at rest at x = 1. The first steps once
    per two self-creations ((M + p) / p = 2, `test_event_clock` (d)): in
    intervals 2, 4 and 6 its step onto x = 1 is refused. After six
    intervals both remain, the first at x = 0 with momentum (16, 0, 0) and
    `steps` 3, the second at x = 1 with momentum (0, 0, 0) and `steps` 0,
    each with content 16 (the measured line current 32 = initial), no
    `step` and no `merged` record, the books balanced at every interval
    (until 2026-09-19 the two merged into the resident at interval 2:
    content 32, momentum (16, 0, 0), one measured event);
(b) an open face is a detector: a bar of 3 x 1 x 1 of the paid family
    `light` (a measured event of it at x = 1, releasing nothing); one unit of
    number 1 in transit at x = 2 on +X at phase 5 (content 1, momentum
    (1, 0, 0)). Interval 1 makes it a departure on +X; the walk of interval
    2 escapes it: one `click` record on the detector `face:+x` at tick 2,
    Node (2, 0, 0), `measured` None, number 1, amount 1, phase 5, momentum
    (1, 0, 0), content 1; the face detectors of the record: `face:+x` with
    3 x 1 = 1 Node, threshold 1, `light` measured 1, clicks 1, content 1,
    measured_content 0, momentum (1, 0, 0), the other five faces zero; the
    books' escaped lines the faces' sums (transit 1, content 1, measured 0,
    momentum (1, 0, 0)). The same bar with `{"x": "periodic"}`: the unit
    wraps to x = 0, no face click, no `face:+x` or `face:-x` detector (four
    faces listed), escaped 0. And a measured event of `m` (content 16,
    momentum (16, 0, 0)) at x = 2 of the open bar: its step of interval 2
    leaves the board, one `click` on `face:+x` at tick 2 from Node (2, 0, 0)
    with `measured` 1, amount 16, phase 2 (K 16: one step per self-creation,
    two made), momentum (16, 0, 0), content 16,
    `held` [16, 0], `home` [0, 0], `home_content` [0, 0]; `face:+x` reads
    measured_content 16 and momentum (16, 0, 0) for `m`, the measured line's
    escaped 16, the momentum escaped (16, 0, 0), the faces' sums the books'
    (until 2026-09-19 an escape wrote an `escaped` record for a measured
    event and none for events in transit);
(c) the count read off the clock: a bar of 2 x 1 x 1, `suspension` [1, 4],
    `release` [1, 1]; a source of `m` of content k at x = 0 (created again
    every interval: nothing of another number reaches it) releasing k units
    per Port per self-creation, five Ports off the board, and a probe of
    `light` (content 1, measuring `m`) at x = 1 reading the presence k every
    interval from the second on. With k = 1 the probe owes
    `by_clock(age, 1, 4)`: 1 at the self-creations from the ages 3, 7, 11
    and 15, 0 at the others, so its age after intervals 1 to 20 is 1, 2, 3,
    4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16: created
    again 16 times in 20 intervals, 4 in 5, its clock slowed by the mean
    1 / 4 (until 2026-09-19 the count was 1 x 1 // 4 = 0 at every
    self-creation and the probe aged 20 in 20 intervals); age + waited = the
    interval at every interval; nothing owed after 20. With k = 8 the probe
    owes `by_clock(age, 8, 4)` = 2 at every self-creation, as 8 x 1 // 4
    did: its age after intervals 1 to 10 is 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
    waited 6, unchanged where k n // d is exact.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.engine import FACE_NAMES, by_clock

PLUS_X = 0
M, LIGHT = 0, 1
FAMILIES = [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}]


def bar(
    shape: list[int],
    measured: list[dict[str, object]],
    *,
    boundary: object = "open",
    clock: int = 16,
    release: list[int] | None = None,
    suspension: object = 0,
    in_transit: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "border-and-clock-test",
        "shape": shape,
        "boundary": boundary,
        "ticks": 20,
        "K": clock,
        "N": 64,
        "release": release or [0, 1],
        "suspension": suspension,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit or [],
    }


def mover(x: int) -> dict[str, object]:
    """A measured event of `m`, content 16, momentum (16, 0, 0): one step per
    two self-creations."""
    return {"position": [x, 0, 0], "family": "m", "amount": 16, "momentum": [16, 0, 0]}


def faces_sum(simulation: EventSimulation) -> dict[str, object]:
    """The face detectors' clicks summed over the open faces, per family:
    what the books' escaped lines must equal."""
    faces = simulation.face_detectors()
    names = [family["name"] for family in FAMILIES]
    return {
        "units": {name: sum(face["families"][name]["clicks"] for face in faces) for name in names},
        "content": {name: sum(face["families"][name]["content"] for face in faces) for name in names},
        "measured": {
            name: sum(face["families"][name]["measured_content"] for face in faces) for name in names
        },
        "momentum": [sum(face["momentum"][axis] for face in faces) for axis in range(3)],
    }


def assert_books_are_the_faces_sums(simulation: EventSimulation) -> None:
    books = simulation.books()
    sums = faces_sum(simulation)
    for family in FAMILIES:
        name = family["name"]
        lines = books["families"][name]
        assert lines["transit"]["escaped"] == sums["units"][name], name
        assert lines["content"]["escaped"] == sums["content"][name], name
        assert lines["measured"]["escaped"] == sums["measured"][name], name
    assert books["momentum"]["escaped"] == sums["momentum"]


def test_a_step_onto_a_measured_event_is_refused_and_both_remain():
    """(a)."""
    resident = {"position": [1, 0, 0], "family": "m", "amount": 16}
    records: list[dict[str, object]] = []
    simulation = EventSimulation(parse_event_world(bar([3, 1, 1], [mover(0), resident])), records.append)
    for tick in range(1, 7):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        assert list(simulation.measured) == [1, 2], tick
        first, second = simulation.measured[1], simulation.measured[2]
        assert first.position == (0, 0, 0) and second.position == (1, 0, 0), tick
        assert first.momentum == [16, 0, 0] and second.momentum == [0, 0, 0], tick
        assert first.steps == tick // 2 and second.steps == 0, tick
        assert first.content == second.content == 16
        assert books["families"]["m"]["measured"]["current"] == 32
        assert books["momentum"]["measured"] == [16, 0, 0]
    assert simulation.at == {(0, 0, 0): 1, (1, 0, 0): 2}
    assert simulation.measured[1].steps == 3
    assert [record["event"] for record in records] == []


def test_an_escape_through_an_open_face_is_a_click_on_the_face_detector():
    """(b)."""
    owner = {"position": [1, 0, 0], "family": "light", "amount": 1, "fixed": True}
    unit = {
        "position": [2, 0, 0],
        "family": "light",
        "number": 1,
        "heading": [1, 0, 0],
        "amount": 1,
        "phase": 5,
    }
    records: list[dict[str, object]] = []
    simulation = EventSimulation(
        parse_event_world(bar([3, 1, 1], [owner], in_transit=[unit])), records.append
    )
    light = simulation.transits[LIGHT]
    simulation.step()
    assert records == [] and light.escaped == 0
    assert int(light.fly_amt[2, 0, 0, 0, PLUS_X]) == 1
    simulation.step()
    assert simulation.books()["balanced"]
    assert records == [
        {
            "event": "click",
            "tick": 2,
            "node": [2, 0, 0],
            "measured": None,
            "detector": "face:+x",
            "family": "light",
            "number": 1,
            "amount": 1,
            "phase": 5,
            "momentum": [1, 0, 0],
            "content": 1,
        }
    ]
    assert light.escaped == 1 and light.escaped_content == 1
    faces = simulation.face_detectors()
    assert [face["name"] for face in faces] == list(FACE_NAMES)
    assert faces[0] == {
        "name": "face:+x",
        "nodes": 1,
        "threshold": 1,
        "families": {
            "m": {"measured": 0, "clicks": 0, "content": 0, "measured_content": 0},
            "light": {"measured": 1, "clicks": 1, "content": 1, "measured_content": 0},
        },
        "momentum": [1, 0, 0],
    }
    for face in faces[1:]:
        assert face["momentum"] == [0, 0, 0]
        assert all(
            entry == {"measured": 0, "clicks": 0, "content": 0, "measured_content": 0}
            for entry in face["families"].values()
        ), face
    assert simulation.detectors() == faces
    assert_books_are_the_faces_sums(simulation)
    # The edge case: a periodic axis has no face and produces no click.
    records = []
    simulation = EventSimulation(
        parse_event_world(bar([3, 1, 1], [owner], in_transit=[unit], boundary={"x": "periodic"})),
        records.append,
    )
    simulation.step()
    simulation.step()
    light = simulation.transits[LIGHT]
    # Wrapped to x = 0 in the walk of interval 2 and mixed on there, whole
    # by its momentum: a departure on +X toward its owner.
    assert records == [] and light.escaped == 0 and int(light.fly_amt[0, 0, 0, 0, PLUS_X]) == 1
    assert [face["name"] for face in simulation.face_detectors()] == list(FACE_NAMES[2:])
    assert_books_are_the_faces_sums(simulation)
    # A measured event's step off the board is a click on the face too.
    records = []
    simulation = EventSimulation(parse_event_world(bar([3, 1, 1], [mover(2)])), records.append)
    simulation.step()
    assert records == [] and simulation.measured[1].position == (2, 0, 0)
    simulation.step()
    assert simulation.measured == {} and simulation.at == {}
    assert records == [
        {
            "event": "click",
            "tick": 2,
            "node": [2, 0, 0],
            "measured": 1,
            "detector": "face:+x",
            "family": "m",
            "number": 1,
            "amount": 16,
            "phase": 2,
            "momentum": [16, 0, 0],
            "content": 16,
            "held": [16, 0],
            "home": [0, 0],
            "home_content": [0, 0],
        }
    ]
    books = simulation.books()
    assert books["balanced"] and books["families"]["m"]["measured"]["escaped"] == 16
    assert books["momentum"]["escaped"] == [16, 0, 0]
    face = simulation.face_detectors()[0]
    assert face["families"]["m"] == {"measured": 0, "clicks": 0, "content": 0, "measured_content": 16}
    assert face["momentum"] == [16, 0, 0]
    assert_books_are_the_faces_sums(simulation)


def ages_of_a_probe_in_a_steady_presence(presence: int, ticks: int) -> tuple[list[int], int, int]:
    """The probe's age after each of `ticks` intervals at `suspension` [1, 4]
    in a presence of `presence` units of another number every interval from
    the second on; then its intervals waited and what it owes."""
    source = {"position": [0, 0, 0], "family": "m", "amount": presence, "fixed": True}
    probe = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    simulation = EventSimulation(
        parse_event_world(
            bar([2, 1, 1], [source, probe], clock=1 << 20, release=[1, 1], suspension=[1, 4])
        )
    )
    entry = simulation.measured[2]
    ages = []
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert entry.age + entry.waited == tick
        # The source is created again every interval; k units reach the
        # probe every interval from the second on.
        assert simulation.measured[1].age == tick
        if tick > 1:
            assert simulation.count[M][1, 0, 0] == presence, tick
        ages.append(entry.age)
    return ages, entry.waited, entry.owed


def test_the_count_a_measured_event_owes_is_read_off_its_clock():
    """(c)."""
    assert [by_clock(age, 1, 4) for age in range(8)] == [0, 0, 0, 1, 0, 0, 0, 1]
    ages, waited, owed = ages_of_a_probe_in_a_steady_presence(1, 20)
    assert ages == [1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16]
    assert waited == 4 and owed == 0
    # Four self-creations in five intervals on average: the rule of
    # 2026-09-19 slows the clock by 1 / 4 where 1 x 1 // 4 = 0 slowed it
    # by nothing.
    assert ages[-1] == 16 < 20 and 1 * 1 // 4 == 0
    # Where k n // d is exact the count is what it was: 8 x 1 // 4 = 2.
    assert [by_clock(age, 8, 4) for age in range(8)] == [2] * 8
    ages, waited, owed = ages_of_a_probe_in_a_steady_presence(8, 10)
    assert ages == [1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    assert waited == 6 and owed == 0

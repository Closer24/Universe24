"""The re-emission and the face detectors under the Beam Law
(docs/BEAM_LAW.md, section 5): a `rerelease` Node re-emits each arriving
record at its next self-creation on its declared directions, its amount
apportioned whole over them, each part keeping the arriving phase and its
content per unit, stamped with the re-emitter's number, age 0, the recoil
taken; an open face is a detector whose click books the escape. The
expected integers of docs/TEST_EXPECTATIONS.md ("The re-emission"), written
down first. K 2^20, `suspension` 0, `release` [0, 1], the families `m`
(free) and `light` (paid):

Since 2026-09-19 the label is along the unit vector u_d of the direction at
the scale Q = 64 (BEAM_LAW section 2 and note 23): u_(1, 0, 0) = (64, 0, 0),
u_(1, 1, 0) = (45, 45, 0), u_(2, 1, 0) = (57, 29, 0), and every momentum
below is in label units.

(a) one ray of amount 3 (content 1 per unit, phase 20) into a `rerelease`
    Node of `m` (content 4) with the three directions +X, (1, 1, 0) and
    (2, 1, 0): three rays of amount 1 at the Node after the interval, one
    per direction, phase 20, age 0, the re-emitter's number 1, content 1;
    the push (192, 0, 0) taken, the recoil -(1 x (64, 0, 0) + 1 x (45, 45,
    0) + 1 x (57, 29, 0)) = (-166, -74, 0), the momentum (26, -74, 0); the
    books closed (absorbed 3, released 3; the content line absorbed 3,
    released 3); a ray of amount 4 on the same Node: 2, 1, 1 (the leftover
    to the direction `age mod 3` = 0, the first), the push (256, 0, 0), the
    recoil (-230, -74, 0), the momentum (26, -74, 0);
(b) the face click: a ray of amount 1, phase 5, content 1 at (2, 0, 0) on
    +X of a 3 x 1 x 1 bar steps off the GameBoard at the first interval: one
    `click` on `face:+x` (tick 1, Node (2, 0, 0), `measured` None, number
    1, amount 1, phase 5, momentum (64, 0, 0), content 1), the escaped
    amount 1, the face's record 32^2 x (C[5]^2 + S[5]^2), the books'
    escaped lines the faces' sums; the same bar with {"x": "periodic"}: no
    click, the ray at x = 0; a measured event of `m` (content 16, momentum
    (1024, 0, 0), one unit of net flow in label units) at x = 2 steps off
    at interval 2: one `click` on `face:+x` with `measured` 1, amount 16,
    phase 1 (K 16: the body escapes in the interval of its second
    self-creation, before that interval's clock turn, since the step
    precedes the law under the crossing rule of 2026-09-21, BEAM_LAW note
    42; phase 2 until then, the step after the turn), momentum (1024, 0,
    0), `held` [16, 0], `home` [0, 0], the measured line's escaped 16;
(c) home: the own number's arrivals are taken and created again at the next
    self-creation on the declared directions with the arriving phase and
    content: a lamp's ray (content 1, phase 7) returning to its lamp on a
    periodic 4 x 1 x 1 bar is home after 4 Links and leaves again on the
    lamp's one direction with phase 7 and content 1, the books closed.
"""

from __future__ import annotations

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.world import FACE_NAMES

M, LIGHT = 0, 1
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]


def bar(
    shape: list[int],
    measured: list[dict[str, object]],
    *,
    boundary: object = "open",
    clock: int = 1 << 20,
    in_transit: list[dict[str, object]] | None = None,
    directions: list[list[int]] | None = None,
) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "ray-reemission-test",
        "shape": shape,
        "boundary": boundary,
        "ticks": 20,
        "K": clock,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "directions": directions or [],
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit or [],
    }


def test_a_rerelease_node_re_emits_on_its_directions_keeping_phase_and_content():
    """(a)."""
    node = [4, 1, 1]
    emitter = {
        "position": node,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "directions": [[1, 0, 0], [1, 1, 0], [2, 1, 0]],
        "table": {"light": "rerelease"},
    }
    source = {"position": [0, 1, 1], "family": "light", "amount": 4, "fixed": True}
    for amount, shares in ((3, [1, 1, 1]), (4, [2, 1, 1])):
        beam = {
            "position": [3, 1, 1],
            "family": "light",
            "number": 2,
            "direction": [1, 0, 0],
            "amount": amount,
            "phase": 20,
        }
        world = bar([9, 3, 3], [emitter, source], in_transit=[beam], directions=[[1, 1, 0], [2, 1, 0]])
        simulation = NatureBeamSimulation(parse_nature_beam_world(world))
        entry, light = simulation.measured[1], simulation.stores[LIGHT]
        simulation.step()
        books = simulation.books()
        assert books["balanced"]
        rows = sorted(
            (
                int(light.direction[i]),
                int(light.amount[i]),
                int(light.phase[i]),
                int(light.age[i]),
                int(light.number[i]),
                int(light.content[i]),
            )
            for i in range(light.size)
        )
        assert rows == [
            (2, shares[0], 20, 0, 1, 1),
            (8, shares[1], 20, 0, 1, 1),
            (9, shares[2], 20, 0, 1, 1),
        ]
        assert entry.pushed == [64 * amount, 0, 0]
        recoil = [64 * shares[0] + 45 * shares[1] + 57 * shares[2], 45 * shares[1] + 29 * shares[2], 0]
        assert entry.momentum == [64 * amount - recoil[0], -recoil[1], 0]
        line = books["families"]["light"]
        assert line["transit"] == {
            "initial": amount,
            "released": amount,
            "current": amount,
            "escaped": 0,
            "absorbed": amount,
            "balanced": True,
        }
        assert line["content"] == {
            "initial": amount,
            "released": amount,
            "current": amount,
            "escaped": 0,
            "absorbed": amount,
            "balanced": True,
        }
        assert books["momentum"]["transit"] == recoil


def test_an_escape_through_an_open_face_is_a_click_on_the_face_detector():
    """(b)."""
    owner = {"position": [1, 0, 0], "family": "light", "amount": 1, "fixed": True}
    unit = {
        "position": [2, 0, 0],
        "family": "light",
        "number": 1,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": 5,
    }
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([3, 1, 1], [owner], in_transit=[unit])), records.append
    )
    simulation.step()
    assert simulation.books()["balanced"] and simulation.stores[LIGHT].size == 0
    assert records == [
        {
            "event": "click",
            "tick": 1,
            "node": [2, 0, 0],
            "measured": None,
            "detector": "face:+x",
            "family": "light",
            "number": 1,
            "amount": 1,
            "phase": 5,
            "momentum": [64, 0, 0],
            "content": 1,
        }
    ]
    faces = simulation.face_detectors()
    assert [face["name"] for face in faces] == list(FACE_NAMES)
    cosines, sines = phase_cosines(64), phase_sines(64)
    assert faces[0]["families"]["light"] == {
        "measured": 1,
        "clicks": 1,
        "content": 1,
        "record": 32 * 32 * (cosines[5] ** 2 + sines[5] ** 2),
        "measured_content": 0,
        "momentum": [64, 0, 0],
    }
    assert faces[0]["momentum"] == [64, 0, 0]
    assert all(face["momentum"] == [0, 0, 0] for face in faces[1:])
    assert simulation.detectors() == faces
    books = simulation.books()
    assert books["families"]["light"]["transit"]["escaped"] == 1
    assert books["families"]["light"]["content"]["escaped"] == 1
    assert books["momentum"]["escaped"] == [64, 0, 0]
    records.clear()
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([3, 1, 1], [owner], in_transit=[unit], boundary={"x": "periodic"})),
        records.append,
    )
    simulation.step()
    light = simulation.stores[LIGHT]
    assert records == [] and light.size == 1 and int(light.node[0]) == light.flat((0, 0, 0))
    assert [face["name"] for face in simulation.face_detectors()] == list(FACE_NAMES[2:])
    mover = {"position": [2, 0, 0], "family": "m", "amount": 16, "momentum": [1024, 0, 0]}
    records.clear()
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([3, 1, 1], [mover], clock=16)), records.append
    )
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
            "phase": 1,
            "momentum": [1024, 0, 0],
            "content": 16,
            "held": [16, 0],
            "home": [0, 0],
            "home_content": [0, 0],
        }
    ]
    books = simulation.books()
    assert books["balanced"] and books["families"]["m"]["measured"]["escaped"] == 16
    assert books["momentum"]["escaped"] == [1024, 0, 0]
    face = simulation.face_detectors()[0]
    assert face["families"]["m"]["measured_content"] == 16 and face["momentum"] == [1024, 0, 0]


def test_what_comes_home_is_created_again_with_its_phase_and_content():
    """(c)."""
    lamp = {
        "position": [0, 0, 0],
        "family": "light",
        "amount": 8,
        "fixed": True,
        "directions": [[1, 0, 0]],
        "lamp": {"rate": [0, 1], "directions": [[1, 0, 0]]},
    }
    beam = {
        "position": [0, 0, 0],
        "family": "light",
        "number": 1,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": 7,
    }
    world = bar([4, 1, 1], [lamp], in_transit=[beam], boundary={"x": "periodic"})
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), records.append)
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    homes = []
    for tick in range(1, 21):
        simulation.step()
        assert simulation.books()["balanced"], tick
        if records and records[-1]["event"] == "home" and records[-1]["tick"] == tick:
            homes.append(tick)
            assert light.size == 1 and int(light.age[0]) == 0 and int(light.phase[0]) == 7
            assert (
                int(light.content[0]) == 1 and int(light.node[0]) == 0 and int(light.direction[0]) == 2
            )
    # Four Links at the flight table's pace: the first arrival at 4 Links is
    # interval 7, then every 7 intervals (55 ages per 32 Links).
    assert homes[:2] == [7, 14] and entry.taken[LIGHT]["home"] == len(homes)
    assert entry.held == [0, 8] and entry.pending == [[], []]

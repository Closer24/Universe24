"""The lifetime of a family and the content a measured event holds of
several families (the Beam Law, docs/BEAM_LAW.md, section 2, step 6 and
the implementation note on the columns; the model owner, 2026-09-20,
"DECIDED: the strong force's range is a lifetime, L": an event in transit
whose age reaches its family's `lifetime` at the end of the walk makes no
next event but a click on the border `lifetime`, booked exactly as an open
face books an escape; and the physicist's D-1: a measured event may hold
content of several families, `held`, and its charge in every column is the
rational sum over what it holds). The expected integers of
docs/TEST_EXPECTATIONS.md ("The lifetime and the held content"), written
down before the first run; K 2^20, N 64, `suspension` 0, every family
without a phase circle unless said:

(b) the lifetime click: a lone ray of the free family `s` (lifetime 3) on
    +x from (2, 2, 2) on an open 7^3 GameBoard at `release` [0, 1]: at
    (3, 2, 2) at the ages 1 and 2, at (4, 2, 2) at the age 3, booked at the
    end of tick 3: the store empty, the border's escaped amount 1,
    momentum (64, 0, 0), content 0, one click record (tick 3, node
    (4, 2, 2), detector `lifetime`, measured None, family `s`, number 1,
    amount 1, phase 0, momentum [64, 0, 0], content 0), the border's record
    67108864 (2^26, (32 x 256)^2 for one ray at phase 0), the books closed
    at every tick, the run's record listing the border after the faces and
    the escaped line summing it; a ray of amount 5 of the paid family
    `light` (quantum 2: two of content per unit) with the lifetime 3:
    escaped content 10 and momentum (640, 0, 0) on the border; a ray that
    arrives at a `read` Node (a reader of `m`, content 1, at (4, 2, 2)) at
    the age L is read (the push (-64, 0, 0) taken) and then booked; the
    same world with the lifetime removed keeps the ray (age 4 at (4, 2, 2)
    after tick 4, no click);
(c) the reach on the flight table: the 26-direction fan (the six headings,
    the twelve face diagonals, the eight cube diagonals) from the centre
    of a 9^3 GameBoard, one row per direction per interval (`release`
    [1, 1], the source's content 1), read by fixed probes of content 1 of
    a paid family (gravity alone: the push -V) at (5, 4, 4), (5, 5, 4),
    (5, 5, 5) and (6, 4, 4): with the lifetime 1 the six neighbours alone
    are reached, (5, 4, 4) reading 9 lines at every tick from 2 (the
    heading and the eight diagonals whose first step is x), the push
    (-392, 0, 0) = -(64 + 4 x 45 + 4 x 37); with 2 the face diagonals too,
    (5, 5, 4) reading 3 lines from tick 3 ((1, 1, 0), (1, 1, 1), (1, 1, -1)
    at their second step), the push (-119, -119, 0); with 3 the cube
    diagonals and two Links, (5, 5, 5) reading the (1, 1, 1) line at tick 4
    with (-37, -37, -37) and (6, 4, 4) the heading at tick 4 with
    (-64, 0, 0); 26 rows click on the border at every tick from L + 1 on
    (78 after four ticks at L = 1), and no row of the family carries an age
    at or beyond L after any tick;
(d) the inverse interval is refused on a GameBoard with a family of a
    lifetime, naming the family and its lifetime;
(e) the refusals, naming the key: `lifetime` 0, -1, 1.5, "3" (an integer
    from 1), [3, 3, 3] (one integer, a scalar), 11 with `age_bound` 10
    (beyond the age bound); a declared ray of the family with the age 3
    at the lifetime 3; a detector named `lifetime`; `held` naming the
    event's own family, an unknown family, a content 0 or 1.5, or not an
    object; a held total breaking the phase-turn bound (K 16, N 64: 300 +
    300 >= 512). The held content: a measured event of `a` (charge [1, 2],
    strong [3, 2]) of amount 4 holding `b` (charge 2, strong 1) 2 reads
    the charges gravity (6, 1), charge (6, 1), strong (8, 1) (the reader
    `c` of `tests/test_columns.py` (b) built from two families) and the
    push (-128, 0, 0) from a `b` ray of amount 1 on +x, releases both
    families at the world's rate (rows of amount 4 of `a` and 2 of `b` per
    direction per self-creation at `release` [1, 1]), reports `held`
    [4, 2] and the content 6 in the run's record, counts under the owners
    of `b`, and the books balance; the register's proton, 1836 of `p`
    (charge 4) holding one unit of `nuclear` (strong 10000, lifetime 3),
    reads the charges (1837, 1), (7344, 1), (10000, 1).
"""

from __future__ import annotations

import itertools
import json

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.world import LIFETIME_NAME
from event_universe.runner import run_initialization

PLUS_X = [1, 0, 0]
UNIT_RECORD = (32 * 256) ** 2
FAN = [list(v) for v in itertools.product((-1, 0, 1), repeat=3) if any(v) and sum(abs(c) for c in v) > 1]


def world(**keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "beam",
        "model_id": "lifetime-test",
        "shape": [7, 7, 7],
        "boundary": "open",
        "ticks": 4,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [
            {"name": "s", "quantum": 0, "phase": False, "lifetime": 3},
            {"name": "light", "quantum": 2, "lifetime": 3},
            {"name": "m", "quantum": 0, "phase": False},
        ],
        "measured": [{"position": [0, 0, 0], "family": "s", "amount": 1, "fixed": True}],
    }
    base.update(keys)
    return base


def ray(name: str, amount: int = 1, age: int = 0) -> dict[str, object]:
    return {
        "position": [2, 2, 2],
        "family": name,
        "number": 1,
        "direction": PLUS_X,
        "amount": amount,
        "phase": 0,
        "age": age,
    }


def run(document: dict[str, object], ticks: int) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
    return simulation, records


# -- (b) ---------------------------------------------------------------------------


def test_the_lifetime_click_books_the_escape_as_a_face_does(tmp_path):
    """(b)."""
    document = world(in_transit=[ray("s")])
    simulation, records = run(document, 3)
    store = simulation.stores[0]
    assert store.size == 0
    assert records == [
        {
            "event": "click",
            "tick": 3,
            "node": [4, 2, 2],
            "measured": None,
            "detector": LIFETIME_NAME,
            "family": "s",
            "number": 1,
            "amount": 1,
            "phase": 0,
            "momentum": [64, 0, 0],
            "content": 0,
        }
    ]
    ledger = simulation.ledger
    assert ledger.lifetime_amount == [1, 0, 0] and ledger.lifetime_content == [0, 0, 0]
    assert ledger.lifetime_momentum == [64, 0, 0] and ledger.lifetime_record == [UNIT_RECORD, 0, 0]
    assert ledger.escaped_amount(0) == 1 and ledger.escaped_momentum() == [64, 0, 0]
    books = simulation.books()
    assert books["families"]["s"]["transit"] == {
        "initial": 1,
        "released": 0,
        "current": 0,
        "escaped": 1,
        "absorbed": 0,
        "balanced": True,
    }
    assert books["momentum"] == {"measured": [0, 0, 0], "transit": [0, 0, 0], "escaped": [64, 0, 0]}
    border = simulation.face_detectors()[-1]
    assert border["name"] == LIFETIME_NAME and border["nodes"] == 0
    assert border["families"]["s"] == {
        "measured": 1,
        "clicks": 1,
        "content": 0,
        "record": UNIT_RECORD,
        "measured_content": 0,
    }
    assert border["momentum"] == [64, 0, 0]
    assert [d["name"] for d in simulation.detectors()][-2:] == ["face:-z", LIFETIME_NAME]
    # The path before the click: (3, 2, 2) at the ages 1 and 2.
    simulation, _ = run(document, 2)
    assert store is not simulation.stores[0]
    store = simulation.stores[0]
    assert store.size == 1 and int(store.node[0]) == store.flat((3, 2, 2)) and int(store.age[0]) == 2
    # The record of a run: the border after the faces, the escaped line.
    path = tmp_path / "world.json"
    path.write_text(json.dumps({**document, "ticks": 3}), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["status"] == "completed" and record["hypotheses"] == ["columns-v1"]
    assert [f["lifetime"] for f in record["families"]] == [3, 3, None]
    assert [d["name"] for d in record["detectors"]][-2:] == ["face:-z", LIFETIME_NAME]
    assert record["detectors"][-1]["families"]["s"]["record"] == UNIT_RECORD
    assert record["escaped"][0] == {"family": "s", "amount": 1, "content": 0, "momentum": [64, 0, 0]}
    # A paid ray: its content escapes on the border.
    simulation, records = run(world(in_transit=[ray("light", amount=5)]), 3)
    assert simulation.stores[1].size == 0
    assert [(r["detector"], r["amount"], r["content"], r["momentum"]) for r in records] == [
        (LIFETIME_NAME, 5, 10, [640, 0, 0])
    ]
    assert simulation.ledger.lifetime_content == [0, 10, 0]
    assert simulation.books()["families"]["light"]["content"]["escaped"] == 10
    # Read at the age L, then booked.
    reader = {"position": [4, 2, 2], "family": "m", "amount": 1, "fixed": True}
    simulation, records = run(world(in_transit=[ray("s")], measured=[*world()["measured"], reader]), 3)
    assert [(r["event"], r["tick"]) for r in records] == [("read", 3), ("click", 3)]
    assert records[0]["push"] == [-64, 0, 0] and simulation.measured[2].pushed == [-64, 0, 0]
    assert simulation.stores[0].size == 0
    # Without the lifetime the ray lives on.
    forever = world(in_transit=[ray("s")])
    forever["families"] = [
        {"name": "s", "quantum": 0, "phase": False},
        {"name": "light", "quantum": 2},
        {"name": "m", "quantum": 0, "phase": False},
    ]
    simulation, records = run(forever, 4)
    store = simulation.stores[0]
    assert records == [] and store.size == 1
    assert int(store.node[0]) == store.flat((4, 2, 2)) and int(store.age[0]) == 4
    assert not simulation.world.lifetimes and simulation.world.hypotheses == []


# -- (c), (d) ------------------------------------------------------------------------

PROBES = ((5, 4, 4), (5, 5, 4), (5, 5, 5), (6, 4, 4))


def fan_world(lifetime: int) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "lifetime-reach-test",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 4,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "directions": FAN,
        "families": [
            {"name": "s", "quantum": 0, "phase": False, "lifetime": lifetime},
            {"name": "pr", "quantum": 1, "phase": False},
        ],
        "measured": [
            {
                "position": [4, 4, 4],
                "family": "s",
                "amount": 1,
                "fixed": True,
                "directions": list(range(2, 8 + len(FAN))),
            },
            *({"position": list(node), "family": "pr", "amount": 1, "fixed": True} for node in PROBES),
        ],
    }


def reads_by_probe(records: list[dict[str, object]]) -> dict[int, set[tuple[int, int, tuple[int, ...]]]]:
    found: dict[int, set[tuple[int, int, tuple[int, ...]]]] = {k: set() for k in range(2, 6)}
    for r in records:
        if r["event"] == "read":
            found[int(str(r["measured"]))].add(
                (int(str(r["tick"])), int(str(r["amount"])), tuple(int(v) for v in r["push"]))  # type: ignore[union-attr]
            )
    return found


def test_the_reach_of_a_lifetime_on_the_flight_table():
    """(c), (d)."""
    assert len(FAN) == 20
    neighbour = {(t, 9, (-392, 0, 0)) for t in (2, 3, 4)}
    diagonal = {(t, 3, (-119, -119, 0)) for t in (3, 4)}
    expected = {
        1: {2: neighbour, 3: set(), 4: set(), 5: set()},
        2: {2: neighbour, 3: diagonal, 4: set(), 5: set()},
        3: {2: neighbour, 3: diagonal, 4: {(4, 1, (-37, -37, -37))}, 5: {(4, 1, (-64, 0, 0))}},
    }
    for lifetime in (1, 2, 3):
        records: list[dict[str, object]] = []
        simulation = NatureBeamSimulation(parse_nature_beam_world(fan_world(lifetime)), records.append)
        store = simulation.stores[0]
        for tick in range(1, 5):
            simulation.step()
            assert simulation.books()["balanced"], (lifetime, tick)
            assert store.size == 0 or int(store.age.max()) < lifetime, (lifetime, tick)
            clicked = sum(
                1
                for r in records
                if r["event"] == "click" and r["tick"] == tick and r["detector"] == LIFETIME_NAME
            )
            assert clicked == (26 if tick > lifetime else 0), (lifetime, tick)
        assert reads_by_probe(records) == expected[lifetime], lifetime
    assert simulation.ledger.lifetime_amount[0] == 26
    # (d) the inverse is refused with a lifetime family on the GameBoard.
    rays_only = fan_world(3)
    rays_only["measured"] = []
    rays_only["age_bound"] = 8
    rays_only["in_transit"] = [ray("s")]
    simulation = NatureBeamSimulation(parse_nature_beam_world(rays_only))
    simulation.step()
    with pytest.raises(ValueError, match="refused with the family 's' of lifetime 3"):
        simulation.inverse_step()


# -- (e) ---------------------------------------------------------------------------


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def with_lifetime(value: object, **keys: object) -> dict[str, object]:
    document = world(**keys)
    document["families"][0] = {"name": "s", "quantum": 0, "phase": False, "lifetime": value}  # type: ignore[index]
    return document


def test_the_refusals_and_the_held_content(tmp_path):
    """(e)."""
    for bad in (0, -1, 1.5, "3"):
        refused(with_lifetime(bad), "families\\[0\\].lifetime must be an integer from 1")
    refused(with_lifetime([3, 3, 3]), "lifetime must be one integer \\(a scalar\\)")
    refused(with_lifetime(11, age_bound=10), "lifetime 11 is beyond the world's age_bound 10")
    assert parse_nature_beam_world(with_lifetime(10, age_bound=10)).families[0].lifetime == 10
    refused(
        world(in_transit=[ray("s", age=3)]), "age 3 is at or beyond the lifetime 3 of the family 's'"
    )
    assert parse_nature_beam_world(world(in_transit=[ray("s", age=2)])).in_transit[0].age == 2
    refused(
        world(detectors=[{"name": LIFETIME_NAME, "positions": [[0, 0, 0]]}]),
        "name 'lifetime' is the name of the border",
    )
    holder = {"position": [3, 3, 3], "family": "s", "amount": 4, "fixed": True}
    for held, text in (
        ({"s": 1}, "held names the event's own family 's'"),
        ({"x": 1}, "held names an unknown family 'x'"),
        ({"m": 0}, "held\\['m'\\] must be an integer from 1"),
        ({"m": 1.5}, "held\\['m'\\] must be an integer from 1"),
        ([1], "held must map family names to contents"),
    ):
        refused(world(measured=[{**holder, "held": held}]), text)
    phased = world(K=16, families=[{"name": "s", "quantum": 0}, {"name": "m", "quantum": 0}])
    refused(
        {**phased, "measured": [{**holder, "amount": 300, "held": {"m": 300}}]},
        "the content held of every family counts",
    )
    parse_nature_beam_world({**phased, "measured": [{**holder, "amount": 300, "held": {"m": 200}}]})
    # The held content: the reader of `c` of test_columns (b) from two families.
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "held-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": 2,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [
            {
                "name": "a",
                "quantum": 0,
                "phase": False,
                "charge": [1, 2],
                "columns": {"strong": {"value": [3, 2], "sign": -1}},
            },
            {
                "name": "b",
                "quantum": 0,
                "phase": False,
                "charge": 2,
                "columns": {"strong": {"value": 1, "sign": -1}},
            },
        ],
        "measured": [
            {
                "position": [2, 2, 0],
                "family": "a",
                "amount": 4,
                "held": {"b": 2},
                "fixed": True,
                "directions": [PLUS_X],
            },
            {
                "position": [0, 4, 0],
                "family": "b",
                "amount": 1,
                "fixed": True,
                "directions": [[0, -1, 0]],
            },
        ],
        "in_transit": [
            {
                "position": [1, 2, 0],
                "family": "b",
                "number": 2,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
            }
        ],
    }
    parsed = parse_nature_beam_world(document)
    assert parsed.measured[0].held == (4, 2) and parsed.owners(1) == (1, 2)
    simulation, records = run(document, 2)
    holder_event = simulation.measured[1]
    assert holder_event.held == [4, 2] and holder_event.content == 6
    assert holder_event.charges() == [(6, 1), (6, 1), (8, 1)] and holder_event.charge == (6, 1)
    reads = [r for r in records if r["event"] == "read" and r["measured"] == 1]
    assert [(r["tick"], r["family"], r["push"]) for r in reads] == [(1, "b", [-128, 0, 0])]
    store_a, store_b = simulation.stores
    born_a = store_a.amount[(store_a.number == 1) & (store_a.age == 0)].tolist()
    born_b = store_b.amount[(store_b.number == 1) & (store_b.age == 0)].tolist()
    assert born_a == [4] and born_b == [2]
    # Two ticks: 4 + 4 of `a`; 2 + 2 of `b` from the holder and 1 + 1 from its emitter.
    assert simulation.ledger.transit_released == [8, 6]
    path = tmp_path / "held.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "held").read_text(encoding="utf-8"))
    assert record["measured"][0]["held"] == [4, 2] and record["measured"][0]["content"] == 6
    assert record["measured"][0]["charges"] == {"gravity": [6, 1], "charge": [6, 1], "strong": [8, 1]}
    # The register's proton.
    nucleus = {
        **document,
        "families": [
            {"name": "p", "quantum": 0, "phase": False, "charge": 4},
            {"name": "n", "quantum": 0, "phase": False},
            {
                "name": "nuclear",
                "quantum": 0,
                "phase": False,
                "columns": {"strong": {"value": 10000, "sign": -1}},
                "lifetime": 3,
            },
        ],
        "measured": [
            {
                "position": [2, 2, 0],
                "family": "p",
                "amount": 1836,
                "held": {"nuclear": 1},
                "fixed": True,
            },
            {
                "position": [0, 4, 0],
                "family": "n",
                "amount": 1839,
                "held": {"nuclear": 1},
                "fixed": True,
            },
        ],
        "in_transit": [],
    }
    simulation = NatureBeamSimulation(parse_nature_beam_world(nucleus))
    assert simulation.measured[1].charges() == [(1837, 1), (7344, 1), (10000, 1)]
    assert simulation.measured[2].charges() == [(1840, 1), (0, 1), (10000, 1)]
    assert simulation.world.hypotheses == ["columns-v1"]

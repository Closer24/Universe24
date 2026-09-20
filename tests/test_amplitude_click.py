"""The one click's prerequisites under the amplitude law (`amplitude-v1`,
stage (vii), 2026-09-20; the design, docs/designs/amplitude-v1/DESIGN.md
sections 2.1, 2.5 and 6; docs/BEAM_LAW.md note 37). The expected integers
of docs/TEST_EXPECTATIONS.md ("The amplitude law: the one click"), written
down before the first run:

(a) a lamp's rate under the record form: a lamp at the rate [3, 1] on two
    directions births three records per self-creation (the design's
    extension of 2.1), the ordinals 1, 2, 3 at tick 1 and 4, 5, 6 at
    tick 2, the birth phase u the lamp's count of births less one, mod N
    (u = 0 .. 5, the record's own field on its rows, the column `birth`;
    step 2), each record two rows of amount 1 with the multiplicity 2;
    the rate [2, 1] parses under the key (it was refused);
(b) a set's offer of several multiplicities of one record: two paths of
    one record, one through a re-emitter of weight [1] (m 2, amount 1) and
    one through a re-emitter of weight [2] (m 8, amount 2), meet in phase
    at one `sum` set: the offer's common denominator is 8 (the held
    pointer scaled by 2, the ratio 4 a square), its units 3, the record's
    total 2 x 2^58 (the two paths add: the design's 2.5, a re-meeting is
    not unitary) and its one cell is the set; with the second re-emitter
    of weights [1, 1] (m 4 against 2, the ratio 2) the run is refused
    naming the record, the set and the two multiplicities;
(c) the columns are written only where a record is: in a keyed world with
    a lamp and a declared row of no record, `state.json`'s rows carry
    `record`, `branch` and `multiplicity` on the lamp's rows alone, and
    the `click` lines at the counter carry them (and `age`) for the lamp's
    rows alone;
(d) the design's test 7 restated: every world of the gate set
    (`examples/events/gate_set.json`) without a lamp, run at its `cap`
    with the key and without it, gives the same `events.jsonl`, the same
    `state.json` and the same books (`audit` of `run.json`), byte for
    byte; the byte-identity without the key against the base tree is the
    replay's (docs/VALIDATION.md);
(e) step 2, u the record's own field: on a bar with a lamp at the stride
    1 (K 2^20, content 2^20) and a counter whose `measure` entry has the
    window 0 of width 8, every record's row clicks (the window reads the
    path phase, 0 on every row: no `pass` line over 80 intervals, 60 or
    more clicks, every click line's `u` its record's ordinal less one and
    its `phase` equal to `u`), while the same bar without the key passes
    most rows (the lamp's clock phase, 0 .. 63, outside the window); the
    rows' column `birth` is the record's u;
(f) step 2, the K record world (the registered `lensing/mass_meeting`
    under the key, every pixel reading `sum`, the lamp's `turns` 0, 300
    intervals): the 64 records of the ordinals 129 .. 192 carry u = 0 ..
    63 once each; per set, the count of their clicks is within one rung
    of the sum of their cells' widths over N (the ladder's expectation
    under a uniform u), and the click centroid in y is within 0.25 pixels
    of the expectation's; the meeting turned rows (the `turned` line of
    the light is not zero);
(g) step 3, the push by share: on a plane with a lamp on +x, a splitter
    of the weights [1, 1] on +x and +y at (3, 1) and a mass (a free family
    of content 4096) at (7, 1), every record's +x row (amount 1, m 2, the
    label (64, 0, 0)) pushes the mass by its share (32, 0, 0) and the
    click line carries `push` (64, 0, 0) and `share` (32, 0, 0); the
    mass's momentum is the sum of the shares of the rows it absorbed; the
    splitter takes each arriving row's share (m 1: the label) and recoils
    by the born rows' shares ((32, 32, 0) per split); the books'
    `remainder` line is the labels less the shares at the absorptions
    less the born labels less the recoils at the re-creations; a row of
    no record pushes by its label, so the bar without the key reads as
    it did.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.amplitude import UNIT, common_denominator
from event_universe.events.run import execute_nature_beam_run
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
GATE_SET = ROOT / "examples" / "events" / "gate_set.json"
N = 64
FIRST = (1 << 32) + 1


def base_world(**overrides: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "amplitude-click-test",
        "shape": [5, 3, 1],
        "boundary": {"z": "periodic"},
        "ticks": 30,
        "K": 1 << 20,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "amplitude": True,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": [],
        "detectors": [],
    }
    world.update(overrides)
    return world


def lamp(directions: list[list[int]], rate: list[int]) -> dict[str, object]:
    return {
        "position": [0, 0, 0],
        "family": "light",
        "amount": 1 << 20,
        "fixed": True,
        "lamp": {"rate": rate, "directions": directions},
    }


def run(world: dict[str, object], ticks: int) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(ticks):
        simulation.step()
    return simulation, lines


def test_a_lamp_births_as_many_records_as_its_rate_says():
    """(a)."""
    world = base_world(measured=[lamp([[1, 0, 0], [0, 1, 0]], [3, 1])])
    simulation, lines = run(world, 2)
    assert simulation.layer is not None
    births = [line for line in lines if line.get("event") == "birth"]
    assert [
        (b["tick"], b["record"] - (1 << 32), b["u"], b["units"], b["multiplicity"]) for b in births
    ] == [
        (1, 1, 0, 2, 2),
        (1, 2, 1, 2, 2),
        (1, 3, 2, 2, 2),
        (2, 4, 3, 2, 2),
        (2, 5, 4, 2, 2),
        (2, 6, 5, 2, 2),
    ]
    assert [simulation.layer.records[FIRST - 1 + k].u for k in range(1, 7)] == [0, 1, 2, 3, 4, 5]
    assert sorted((r.record - (1 << 32), r.birth) for r in simulation.stores[0].rows()) == sorted(
        [(k, k - 1) for k in range(1, 7) for _ in range(2)]
    )
    rows = sorted((r.record - (1 << 32), r.amount, r.multiplicity) for r in simulation.stores[0].rows())
    assert rows == sorted([(k, 1, 2) for k in range(1, 7) for _ in range(2)])
    assert simulation.measured[1].births == 6
    parsed = parse_nature_beam_world(base_world(measured=[lamp([[1, 0, 0]], [2, 1])]))
    assert parsed.measured[0].lamp is not None and parsed.measured[0].lamp.rate == (2, 1)


def meeting_world(second: list[int], outputs: list[list[int]]) -> dict[str, object]:
    """Two paths of one record into one `sum` set: the lamp on +x and +y,
    a re-emitter of weight [1] at (3, 0) turning +x rows up to the set at
    (3, 2), a re-emitter of the weights `second` on `outputs` at (0, 2)
    sending +y rows along y = 2 to the same set; both paths five Links."""
    return base_world(
        measured=[
            lamp([[1, 0, 0], [0, 1, 0]], [1, 1]),
            {
                "position": [3, 0, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"rule": "rerelease", "weights": [1]}},
                "directions": [[0, 1, 0]],
            },
            {
                "position": [0, 2, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"rule": "rerelease", "weights": second}},
                "directions": outputs,
            },
            {"position": [3, 2, 0], "family": "counter", "amount": 1, "fixed": True},
        ],
        detectors=[{"name": "end", "positions": [[3, 2, 0]], "reading": "sum"}],
    )


def test_an_offer_of_two_multiplicities_takes_the_common_denominator():
    """(b)."""
    assert common_denominator(2, 8) == (2, 1, 8)
    assert common_denominator(8, 2) == (1, 2, 8)
    assert common_denominator(9, 36) == (2, 1, 36)
    assert common_denominator(2, 4) == (0, 0, 0)
    assert common_denominator(1682, 1682 * 25) == (5, 1, 1682 * 25)
    simulation, _ = run(meeting_world([2], [[1, 0, 0]]), 30)
    assert simulation.layer is not None
    first = simulation.layer.records[FIRST]
    assert first.gathered and first.gather is not None
    (offer,) = first.offers.values()
    assert offer.multiplicity == 8 and offer.units == 3
    assert first.gather["chosen"] == [["end", 0, "0"]]
    assert first.gather["total"] == [2 * UNIT, 1] and first.gather["weight"] == [2 * UNIT, 1]
    assert first.gather["cells"] == [[[["end", 0, "0"]], N]]
    refused = NatureBeamSimulation(
        parse_nature_beam_world(meeting_world([1, 1], [[1, 0, 0], [0, 1, 0]]))
    )
    with pytest.raises(
        ValueError, match=r"record 4294967297 at the set end carry the multiplicities 2 and 4"
    ):
        for _ in range(30):
            refused.step()


def test_the_columns_are_written_only_where_a_record_is(tmp_path: Path):
    """(c)."""
    world = base_world(
        shape=[6, 1, 1],
        boundary={"y": "periodic", "z": "periodic"},
        measured=[
            lamp([[1, 0, 0]], [1, 1]),
            {"position": [5, 0, 0], "family": "counter", "amount": 1, "fixed": True},
        ],
        in_transit=[
            {
                "position": [3, 0, 0],
                "family": "light",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": 0,
            }
        ],
    )
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(world), json.dumps(world).encode(), out, "test", 1)
    state = json.loads((out / "state.json").read_text(encoding="utf-8"))
    rows = [ray for node in state["nodes"] for f in node["families"] for ray in f["rays"]]
    assert sorted(("record" in ray, "branch" in ray, "multiplicity" in ray) for ray in rows) == [
        (False, False, False),
        (True, True, True),
    ]
    _, lines = run(world, 16)
    clicks = [line for line in lines if line.get("event") == "click" and line.get("measured") == 2]
    assert len(clicks) >= 2
    keyed = [("record" in c, "branch" in c, "multiplicity" in c, "age" in c) for c in clicks]
    assert (False, False, False, False) in keyed and (True, True, True, True) in keyed
    assert all(k in ((False,) * 4, (True,) * 4) for k in keyed)


def gate_worlds_without_a_lamp() -> list[tuple[str, int]]:
    document = json.loads(GATE_SET.read_text(encoding="utf-8"))
    found = []
    for entry in document["worlds"]:
        path = GATE_SET.parent / entry["path"]
        loaded = load_world(path.read_bytes(), base_dir=path.parent)
        if all(event.lamp is None for event in loaded.world.measured):
            found.append((entry["path"], int(entry["cap"])))
    return found


@pytest.mark.parametrize(("path", "cap"), gate_worlds_without_a_lamp())
def test_a_gate_world_without_a_lamp_reads_the_same_with_the_key(tmp_path: Path, path: str, cap: int):
    """(d)."""
    source = (GATE_SET.parent / path).read_bytes()
    document = json.loads(source)
    assert "amplitude" not in document
    keyed = json.dumps({**document, "amplitude": True}).encode("utf-8")
    outputs = []
    for name, text in (("plain", source), ("keyed", keyed)):
        loaded = load_world(text, base_dir=(GATE_SET.parent / path).parent)
        assert loaded.world.recorded is False
        out = tmp_path / name
        out.mkdir()
        execute_nature_beam_run(loaded.world, text, out, "test", cap)
        outputs.append(out)
    plain, keyed_out = outputs
    for name in ("events.jsonl", "state.json"):
        assert (plain / name).read_bytes() == (keyed_out / name).read_bytes(), name
    plain_record = json.loads((plain / "run.json").read_text(encoding="utf-8"))
    keyed_record = json.loads((keyed_out / "run.json").read_text(encoding="utf-8"))
    assert plain_record["audit"] == keyed_record["audit"]
    assert plain_record["amplitude"] is False and keyed_record["amplitude"] is True


def window_bar(amplitude: bool) -> dict[str, object]:
    return base_world(
        shape=[12, 1, 1],
        boundary={"y": "periodic", "z": "periodic"},
        ticks=80,
        amplitude=amplitude,
        measured=[
            lamp([[1, 0, 0]], [1, 1]),
            {
                "position": [10, 0, 0],
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"rule": "measure", "phase_window": 0, "phase_width": 8}},
            },
        ],
    )


def test_the_window_reads_the_path_phase_of_a_record():
    """(e)."""
    simulation, lines = run(window_bar(True), 80)
    at_counter = [line for line in lines if line.get("measured") == 2 and line.get("family") == "light"]
    clicks = [line for line in at_counter if line["event"] == "click"]
    assert not [line for line in at_counter if line["event"] == "pass"]
    assert len(clicks) >= 60
    for click in clicks:
        ordinal = int(click["record"]) - (1 << 32)
        assert click["u"] == (ordinal - 1) % N == click["phase"]
    rows = simulation.stores[0].rows()
    assert rows and all(r.birth == ((r.record - (1 << 32)) - 1) % N for r in rows)
    _, plain_lines = run(window_bar(False), 80)
    plain = [line for line in plain_lines if line.get("measured") == 2 and line.get("family") == "light"]
    assert [line for line in plain if line["event"] == "pass"]
    assert all("u" not in line for line in plain)


def k_record_world() -> dict[str, object]:
    """The registered `lensing/mass_meeting` under the key: every pixel
    reading `sum`, the lamp's `turns` 0 (scratchpad k_record's
    `make_record_worlds.py`, the K finding of 2026-09-20)."""
    world = json.loads(
        (ROOT / "examples" / "events" / "lensing" / "mass_meeting.json").read_text("utf-8")
    )
    world["model_id"] = "beam-lensing-mass-meeting-record-test"
    world["amplitude"] = True
    world["ticks"] = 300
    for event in world["measured"]:
        if "lamp" in event:
            assert event["lamp"]["rate"] == [1, 1]
            event["lamp"]["turns"] = [0] * len(event["lamp"]["directions"])
    for detector in world["detectors"]:
        assert detector["reading"] == "wave"
        detector["reading"] = "sum"
    return world


def test_the_k_record_world_clicks_as_its_offers_say_under_uniform_u():
    """(f)."""
    simulation, _ = run(k_record_world(), 300)
    assert simulation.layer is not None
    first, last = 129, 192
    chosen = [
        live for live in simulation.layer.records.values() if first <= live.identity - (1 << 32) <= last
    ]
    assert len(chosen) == N and all(live.gathered and live.gather is not None for live in chosen)
    assert sorted(live.u for live in chosen) == list(range(N))
    clicks: dict[str, int] = {}
    expected: dict[str, float] = {}
    for live in chosen:
        gather = live.gather
        assert gather is not None and gather["chosen"] is not None
        clicks[str(gather["chosen"][0][0])] = clicks.get(str(gather["chosen"][0][0]), 0) + 1  # type: ignore[index]
        previous = 0
        for factors, rung in gather["cells"]:  # type: ignore[union-attr]
            name = str(factors[0][0])
            expected[name] = expected.get(name, 0.0) + (int(rung) - previous) / N
            previous = int(rung)
    assert sum(clicks.values()) == N and abs(sum(expected.values()) - N) < 1e-9
    deviation = max(abs(clicks.get(name, 0) - expected[name]) for name in expected)
    assert deviation <= 1.0, (deviation, clicks, expected)

    def pixel_y(name: str) -> int | None:
        return int(name.split("_")[1]) if name.startswith("screen_") else None

    click_y = [pixel_y(name) for name, count in clicks.items() for _ in range(count)]
    on_screen = [y for y in click_y if y is not None]
    expected_y = sum(
        pixel_y(name) * weight for name, weight in expected.items() if pixel_y(name) is not None
    )  # type: ignore[operator]
    expected_weight = sum(weight for name, weight in expected.items() if pixel_y(name) is not None)
    assert on_screen and expected_weight > 0
    centroid = sum(on_screen) / len(on_screen)
    assert abs(centroid - expected_y / expected_weight) <= 0.25, (centroid, expected_y / expected_weight)
    assert any(simulation.ledger.turned_momentum[0])


def share_world() -> dict[str, object]:
    """A lamp on +x into a (1, 1) splitter on +x and +y, the +x rows into a
    mass of a free family at (7, 1), the +y rows out through the face."""
    return base_world(
        shape=[9, 3, 1],
        families=[
            {"name": "light", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        ],
        ticks=60,
        measured=[
            {
                "position": [0, 1, 0],
                "family": "light",
                "amount": 1 << 20,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]]},
            },
            {
                "position": [3, 1, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"rule": "rerelease", "weights": [1, 1]}},
                "directions": [[1, 0, 0], [0, 1, 0]],
            },
            {"position": [7, 1, 0], "family": "m", "amount": 4096, "fixed": True},
        ],
    )


def test_a_record_row_pushes_matter_by_its_share():
    """(g)."""
    simulation, lines = run(share_world(), 60)
    clicks = [line for line in lines if line.get("event") == "click" and line.get("family") == "light"]
    at_mass = [line for line in clicks if line.get("measured") == 3]
    at_splitter = [
        line for line in lines if line.get("event") == "rerelease" and line.get("measured") == 2
    ]
    assert len(at_mass) >= 20 and len(at_splitter) >= 20
    for click in at_mass:
        assert click["push"] == [64, 0, 0] and click["share"] == [32, 0, 0]
        assert click["multiplicity"] == 2 and click["amount"] == 1
    mass = simulation.measured[3]
    assert mass.momentum == [32 * len(at_mass), 0, 0]
    splits = [line for line in lines if line.get("event") == "split" and line.get("measured") == 2]
    splitter = simulation.measured[2]
    assert splitter.momentum == [64 * len(at_splitter) - 32 * len(splits), -32 * len(splits), 0]
    books = simulation.books(recount=True)
    assert books["balanced"]
    remainder = books["momentum"]["remainder"]  # type: ignore[index]
    assert remainder == [32 * len(at_mass) - 32 * len(splits), -32 * len(splits), 0]
    assert books["families"]["light"]["remainder"] == remainder  # type: ignore[index]
    plain = share_world()
    plain["amplitude"] = False
    plain["measured"][1]["table"]["light"] = "rerelease"  # type: ignore[index]
    unkeyed, plain_lines = run(plain, 60)
    plain_mass = [
        line for line in plain_lines if line.get("event") == "click" and line.get("measured") == 3
    ]
    assert plain_mass and all("share" not in line and line["push"] == [64, 0, 0] for line in plain_mass)
    assert unkeyed.measured[3].momentum == [64 * len(plain_mass), 0, 0]
    assert "remainder" not in unkeyed.books()["momentum"]  # type: ignore[operator]

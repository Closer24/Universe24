"""The one click's prerequisites under the amplitude law (`amplitude-v1`,
stage (vii), 2026-09-20; the design, docs/designs/amplitude-v1/DESIGN.md
sections 2.1, 2.5 and 6; docs/BEAM_LAW.md note 37). The expected integers
of docs/TEST_EXPECTATIONS.md ("The amplitude law: the one click"), written
down before the first run:

(a) a lamp's rate under the record form: a lamp at the rate [3, 1] on two
    directions births three records per self-creation (the design's
    extension of 2.1), the ordinals 1, 2, 3 at tick 1 and 4, 5, 6 at
    tick 2, the birth phase of the j-th record of a self-creation the
    clock's phase advanced by j strides (u = 0, 1, 2 then 1, 2, 3 at the
    stride 1), each record two rows of amount 1 with the multiplicity 2;
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
    replay's (docs/VALIDATION.md).
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
        (2, 4, 1, 2, 2),
        (2, 5, 2, 2, 2),
        (2, 6, 3, 2, 2),
    ]
    assert [simulation.layer.records[FIRST - 1 + k].u for k in range(1, 7)] == [0, 1, 2, 1, 2, 3]
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

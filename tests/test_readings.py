"""The readings of a run (core/readings.py; ALGEBRA.md #readings-and-measurements): declared in the world file, labelled by their kind, written in one format; a reading writes nothing into the run, bit for bit; every refusal names the reading and its key."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.readings import LABELS, SCHEMA, Reading, Readings, declarations
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import run_world
from tests.worlds import emitter_world

SHAPE = (80, 1, 1)
DETECTORS = ["screen"]
FAMILIES = ["gravity", "charge", "matter"]
BODIES = [0]
SIX = [
    {"name": "screen_clicks", "kind": "clicks", "detector": "screen"},
    {"name": "matter_at_40", "kind": "level", "family": "matter", "node": [40, 0, 0], "every": 1},
    {"name": "matter_support", "kind": "support", "family": "matter", "every": 1},
    {"name": "matter_total", "kind": "total", "family": "matter", "every": 1},
    {"name": "emitter_centre", "kind": "centre", "body": 0, "every": 40},
    {"name": "alive", "kind": "alive", "every": 1},
]


def declared(document: dict, readings: list[dict]) -> dict:
    document["readings"] = readings
    document["stamp"] = input_stamp(document)
    return document


def test_the_schema_holds_nine_kinds_with_their_labels_and_keys():
    """Nine kinds, each with a label of the three and its own keys beside name and kind; a body's momentum, its cycle and a family's rows GAMEBOARD."""
    assert set(SCHEMA) == {
        "clicks",
        "level",
        "support",
        "total",
        "rows",
        "centre",
        "momentum",
        "cycle",
        "alive",
    }
    assert SCHEMA["cycle"] == ("GAMEBOARD", ("body", "every"))
    assert SCHEMA["momentum"] == ("GAMEBOARD", ("body", "every")) and SCHEMA["rows"][1] == (
        "family",
        "every",
    )
    assert LABELS == ("DETECTOR", "GAMEBOARD", "HOST")
    assert SCHEMA["clicks"] == ("DETECTOR", ("detector",)) and SCHEMA["alive"] == ("HOST", ("every",))
    found = declarations(SIX, SHAPE, DETECTORS, FAMILIES, BODIES)
    assert [reading.kind for reading in found] == [item["kind"] for item in SIX]
    assert found[1] == Reading("matter_at_40", "level", "GAMEBOARD", 1, None, "matter", None, (40, 0, 0))
    assert found[0].target() == {"detector": "screen"} and found[1].target()["node"] == [40, 0, 0]


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ({"kind": "alive"}, "readings must be a list"),
        ([3], r"readings\[0\] must be an object"),
        ([{"name": "x", "kind": "well"}], r"the reading \'x\'.kind must be one of"),
        (
            [{"name": "x", "kind": "alive", "every": 1, "depth": 2}],
            r"the reading \'x\' has unknown keys: depth",
        ),
        (
            [{"name": "x", "kind": "level", "family": "matter", "every": 1}],
            r"the reading \'x\' lacks keys: node",
        ),
        ([{"name": "", "kind": "alive", "every": 1}], r"readings\[0\].name must be a nonempty string"),
        (
            [{"name": "x", "kind": "alive", "every": 1}, {"name": "x", "kind": "alive", "every": 2}],
            "two readings named 'x'",
        ),
        (
            [{"name": "x", "kind": "alive", "every": 0}],
            r"the reading \'x\'.every must be an integer from 1",
        ),
        (
            [{"name": "x", "kind": "alive", "every": 2.0}],
            r"the reading \'x\'.every must be an integer from 1",
        ),
        (
            [{"name": "x", "kind": "clicks", "detector": "screen", "every": 1}],
            r"the reading \'x\' has unknown keys: every",
        ),
        (
            [{"name": "x", "kind": "clicks", "detector": "wall"}],
            r"the reading \'x\'.detector names no detector",
        ),
        (
            [{"name": "x", "kind": "support", "family": "light", "every": 1}],
            r"the reading \'x\'.family names no family",
        ),
        (
            [{"name": "x", "kind": "centre", "body": 7, "every": 1}],
            r"the reading \'x\'.body names no measured entry",
        ),
        (
            [{"name": "x", "kind": "level", "family": "matter", "node": [80, 0, 0], "every": 1}],
            "must lie inside the shape",
        ),
        (
            [{"name": "x", "kind": "level", "family": "matter", "node": [1, 0], "every": 1}],
            "node must be three integers",
        ),
    ],
)
def test_every_defect_of_a_declaration_is_refused_by_name(value, message):
    """The refusals name the reading and the key (record 2199 item 1: every word from the file)."""
    with pytest.raises(ValueError, match=message):
        declarations(value, SHAPE, DETECTORS, FAMILIES, BODIES)


def test_a_reading_reads_the_state_and_writes_nothing_into_the_run():
    """The emitter world run with the six readings read at every interval gives the same lines, levels and remainders as the plain run, bit for bit; the readings hold the run's numbers."""
    plain = DetectorLawSimulation(
        parse_nature_beam_world(emitter_world(stock=2, ticks=160))
    )  # 160: the first click at the screen at 129 on this fixture
    world = parse_nature_beam_world(declared(emitter_world(stock=2, ticks=160), SIX))
    assert [reading.name for reading in world.readings] == [item["name"] for item in SIX]
    read = DetectorLawSimulation(world)
    lines_plain: list[dict] = []
    lines_read: list[dict] = []
    plain.record = lines_plain.append
    read.record = lines_read.append
    readings = Readings(world.readings)
    readings.read(read)
    for _ in range(160):
        plain.step()
        read.step()
        readings.read(read)
    readings.clicks(read.layer.gathers, world.detectors)
    assert lines_plain == lines_read and len(lines_plain) > 0
    for key, live in plain.records.items():
        other = read.records[key]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    for family, record in plain.held_records.items():
        assert np.array_equal(record.now, read.held_records[family].now)
    out = {entry["name"]: entry for entry in readings.output()}
    assert [entry["label"] for entry in readings.output()] == [
        "DETECTOR",
        "GAMEBOARD",
        "GAMEBOARD",
        "GAMEBOARD",
        "GAMEBOARD",
        "HOST",
    ]
    assert [line["interval"] for line in out["alive"]["lines"]] == list(range(161))
    assert out["alive"]["lines"][0]["alive"] == 1 and out["alive"]["lines"][-1]["alive"] == len(
        read.records
    )
    assert [line["interval"] for line in out["emitter_centre"]["lines"]] == [0, 40, 80, 120, 160]
    assert all(line["node"] == [21, 0, 0] for line in out["emitter_centre"]["lines"])
    matter = [family.name for family in read.families].index("matter")
    level = sum(live.now for live in read.records.values() if live.family == matter)
    assert out["matter_at_40"]["lines"][-1]["level"] == int(level[40, 0, 0])
    assert out["matter_support"]["lines"][-1]["support"] == int((level != 0).sum())
    assert out["matter_total"]["lines"][-1]["total"] == int(np.abs(level).astype(object).sum())
    clicks = out["screen_clicks"]["lines"]
    assert clicks and all(
        set(line) == {"interval", "record", "giving", "content", "momentum", "node"} for line in clicks
    )
    assert all(line["node"] == [list(node) for node in world.detectors[0].positions] for line in clicks)
    assert all(
        isinstance(value, int) for line in clicks for value in (line["interval"], line["content"])
    )


def test_the_stride_reads_interval_zero_and_every_multiple_up_to_the_ticks():
    """A reading every k is read at 0, k, 2k, ... up to the run's ticks; a stride beyond the ticks leaves the loaded state alone."""
    document = declared(
        emitter_world(stock=1, ticks=10),
        [{"name": "a", "kind": "alive", "every": 3}, {"name": "b", "kind": "alive", "every": 50}],
    )
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    readings = Readings(simulation.world.readings)
    readings.read(simulation)
    for _ in range(10):
        simulation.step()
        readings.read(simulation)
    out = {entry["name"]: entry for entry in readings.output()}
    assert [line["interval"] for line in out["a"]["lines"]] == [0, 3, 6, 9]
    assert [line["interval"] for line in out["b"]["lines"]] == [0]
    assert out["a"]["every"] == 3 and out["a"]["kind"] == "alive" and out["a"]["label"] == "HOST"


def test_the_one_command_writes_the_readings_beside_todays_keys(tmp_path: Path):
    """The output file carries `readings` in the declared order beside today's keys; the clicks reading is today's clicks of that detector; a world without the key writes an empty list."""
    output = run_world(
        declared(
            emitter_world(stock=2, ticks=120),
            [SIX[0], {"name": "alive", "kind": "alive", "every": 60}],
        ),
        tmp_path,
    )
    assert {"clicks", "counts", "records_alive", "pins", "readings"} <= set(output)
    names = [entry["name"] for entry in output["readings"]]
    assert names == ["screen_clicks", "alive"]
    clicks = output["readings"][0]
    assert clicks["label"] == "DETECTOR" and clicks["detector"] == "screen"
    assert [line["interval"] for line in clicks["lines"]] == [
        click["interval"] for click in output["clicks"] if click["detector"] == "screen"
    ]
    assert output["counts"]["screen"] == len(clicks["lines"])
    assert [line["interval"] for line in output["readings"][1]["lines"]] == [0, 60, 120]
    assert output["readings"][1]["lines"][-1]["alive"] == output["records_alive"]
    text = (tmp_path / "out" / "world.output.json").read_text(encoding="utf-8")
    assert json.loads(text)["readings"] == output["readings"]
    (tmp_path / "plain").mkdir()
    plain = run_world(emitter_world(stock=2, ticks=120), tmp_path / "plain")
    assert plain["readings"] == [] and plain["clicks"] == output["clicks"]


def test_a_bodys_own_cycle_is_a_gameboard_reading_a_clock_world_with_no_detector_can_declare():
    """The kind `cycle` of a body (GAMEBOARD, a diagnostic): the interval the body's own record last rose through 0 and the length of the cycle before it, the body's own tick where no detector clicks. On the emitter world (stock 2) read at every interval: nothing at the load, the first cycle closes at 42 (its length the 42 intervals from the load), then a cycle every 55 intervals (97, 152), the mode's rotation of this fixture (its declared period 55), measured once; 161 lines for 160 intervals. The edge case: a body the world lacks is refused by name."""
    world = parse_nature_beam_world(
        declared(
            emitter_world(stock=2, ticks=160), [{"name": "tick", "kind": "cycle", "body": 0, "every": 1}]
        )
    )
    simulation = DetectorLawSimulation(world)
    readings = Readings(world.readings)
    readings.read(simulation)
    for _ in range(160):
        simulation.step()
        readings.read(simulation)
    out = readings.output()[0]
    assert out["label"] == "GAMEBOARD" and out["body"] == 0 and len(out["lines"]) == 161
    starts = sorted({(line["cycle_start"], line["cycle_length"]) for line in out["lines"]})
    assert starts == [(0, 0), (42, 42), (97, 55), (152, 55)]
    with pytest.raises(ValueError, match="names no measured entry with a block"):
        declarations(
            [{"name": "tick", "kind": "cycle", "body": 3, "every": 1}],
            SHAPE,
            DETECTORS,
            FAMILIES,
            BODIES,
        )

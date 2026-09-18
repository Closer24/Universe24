"""The screen without a draw (E12) in isolation: one external body of the
`proton` family radiating its light (external-body-v1, released-field-v1),
the light spreading by the catalog's table with the Node-owned remainder
(field-spreading-v1, field-remainder-v1) onto five Detector marks at setting
[1, 1], counters: every arriving quantum is drawn 1 (the drawn number is
always below the numerator times the ticket modulus), a ticket is consumed
per drawn arrival and the outcome reads nothing of it, so the record is the
same under another ticket seed; nothing is returned; the world ledger is
exact at every tick, and under feature 2c (detector-absorb-v1) what the
counters click is absorbed.

The worlds are those of examples/nature/e12_no_draw/make_worlds.py (the eight
files checked byte for byte) and the test's own `counter_world(seed)`, the
smallest world of the question, run for TICKS ticks through the runner with
seed 0 and seed 5. The structural expectations are written before the first
run and the record's integers (the clicks, the light line, the spreads) were
read from the first run of this board and pinned then, as
docs/TEST_EXPECTATIONS.md ("The screen without a draw") says.
"""

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/e12_no_draw"
TICKS = 24
OTHER_SEED = 5
RELEASE_PER_INTERVAL = 96  # six headings of floor(64 / 4) = 16 from the cycle of tick 0
SOURCE_DISTANCE = 6
EVENT_KINDS = {
    "cycle_started",
    "cycle_committed",
    "spatial_cycle_started",
    "spatial_cycle",
    "spatial_sent",
    "spatial_received",
    "spatial_escaped",
    "field_spread",
    "external_body_absorbed",
    "detector_click",
    "detector_pass",
}
# Pinned from the first run of this board (2026-09-18): every click as (tick,
# mark, amount, the Port it arrived through), the light line after the last
# tick and the count of field_spread records. Empty until that run; see the
# expectations.
CLICKS: list[tuple[int, tuple[int, int, int], int, int]] = []
LIGHT_LINE: dict[str, int] = {}
SPREADS: int | None = None


def load_make_worlds():
    spec = importlib.util.spec_from_file_location("e12_make_worlds", WORLDS / "make_worlds.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def components(value):
    return [value] if isinstance(value, int) else list(value)


def line(ledger, family):
    entry = ledger["fields"][family]
    return {
        key: components(entry.get(key, 0))
        for key in (
            "initial",
            "sourced",
            "current",
            "escaped",
            "annulled",
            "absorbed",
            "absorbed_by_marks",
        )
    }


def run(tmp_path, world, name):
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    record = tmp_path / name
    run_initialization(path, record)
    metadata = json.loads((record / "run.json").read_text(encoding="utf-8"))
    events = [
        json.loads(text)
        for text in (record / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if text.strip()
    ]
    return metadata, events


def test_a_counter_counts_without_a_draw_and_its_record_ignores_the_seed(tmp_path):
    make = load_make_worlds()
    # The eight worlds of E12 are byte for byte what the generator writes.
    for name, document in make.cases():
        expected = json.dumps(document, indent=1) + "\n"
        assert (WORLDS / f"{name}.json").read_text(encoding="utf-8") == expected, name
    marks = tuple(tuple(m) for m in make.TEST_MARKS)
    axis = marks[len(marks) // 2]
    source = tuple(make.TEST_SOURCE)
    assert axis[1] == source[1] and axis[0] - source[0] == SOURCE_DISTANCE
    metadata, events = run(tmp_path, make.counter_world(0, ticks=TICKS), "counter")
    other, other_events = run(tmp_path, make.counter_world(OTHER_SEED, ticks=TICKS), "counter_seed")
    absorbing = "detector_absorb" in metadata
    # The identities and the layers.
    assert metadata["detector_mark"] == "detector-mark-v1"
    assert metadata["external_body"] == "external-body-v1"
    assert metadata["field_spreading"] == "field-spreading-v1"
    assert metadata["field_remainder"] == "field-remainder-v1"
    assert metadata["released_fields"] == [{"field": "light", "field_of": "proton", "release": [1, 4]}]
    assert sorted(metadata["ray_layer_families"]) == [["light"], ["proton"]]
    assert metadata["completed_ticks"] == TICKS
    # The ledger: balanced at every tick; the proton line empty (a body holds no
    # rays); the light line sourced 96 per interval from the cycle of tick 0, and
    # current + escaped + absorbed = sourced.
    assert metadata["conserved_at_every_completed_tick"]
    clicks = [
        (event["tick"], tuple(event["position"]), event["amount"], event["port"])
        for event in events
        if event["event"] == "detector_click"
    ]
    for ledger in metadata["audit"]:
        tick = ledger["tick"]
        assert ledger["balanced"]
        assert all(
            item["balanced"] for readout in ("fields", "charge") for item in ledger[readout].values()
        )
        proton = line(ledger, "proton")
        assert proton["current"] == [0] and proton["sourced"] == [0]
        light = line(ledger, "light")
        assert light["sourced"] == [RELEASE_PER_INTERVAL * tick]
        assert (
            light["current"][0]
            + light["escaped"][0]
            + light["absorbed"][0]
            + light["absorbed_by_marks"][0]
            == light["sourced"][0]
        )
        assert light["annulled"] == [0]
        sunk = sum(
            event["amount"]
            for event in events
            if event["event"] == "external_body_absorbed" and event["tick"] <= tick
        )
        assert light["absorbed"] == [sunk]
        if absorbing:
            # A click is an absorption: the marks' line is the quanta the counters
            # clicked so far.
            clicked = sum(amount for t, _, amount, _ in clicks if t <= tick)
            assert light["absorbed_by_marks"] == [clicked]
    assert {event["event"] for event in events} <= EVENT_KINDS
    # The clicks: every one of family light, bit 1, at a counter; the first at
    # the on-axis mark at or after the mean field's first arrival; every click
    # off the axis mirrored in the same tick; nothing returned; under 2c nothing
    # passes either, since what was clicked is no longer there to spread.
    assert all(
        event["family"] == "light" and event["bit"] == 1
        for event in events
        if event["event"] == "detector_click"
    )
    assert clicks and all(mark in marks and amount >= 1 for _, mark, amount, _ in clicks)
    assert clicks[0][1] == axis and clicks[0][0] >= SOURCE_DISTANCE
    plain = [(tick, mark, amount) for tick, mark, amount, _ in clicks]
    for tick, (x, y, z), amount in plain:
        assert (tick, (x, 2 * axis[1] - y, z), amount) in plain
    assert not any(event["event"] == "detector_return" for event in events)
    if absorbing:
        assert metadata["detector_absorb"] == "detector-absorb-v1"
        assert not any(event["event"] == "detector_pass" for event in events)
        assert all(
            event["absorbed"] == event["amount"]
            for event in events
            if event["event"] == "detector_click"
        )
        # The counters: each mark's counter is the quanta it clicked.
        counted = {mark: 0 for mark in marks}
        for _, mark, amount, _ in clicks:
            counted[mark] += amount
        assert [tuple(m["position"]) for m in metadata["detector_marks"]] == list(marks)
        assert [m["counter"].get("light", 0) for m in metadata["detector_marks"]] == [
            counted[mark] for mark in marks
        ]
        assert metadata["detector_mark_totals"]["light"] == [sum(counted.values())]
    # The ticket line: one ticket per drawn arrival, and a draw at [1, 1] is a
    # click, so the tickets a mark consumed are its clicks; the other seed gives
    # the same record event for event, its initialization differing by the seed.
    assert other["initialization_sha256"] != metadata["initialization_sha256"]
    assert other_events == events
    assert other["audit"] == metadata["audit"]
    assert other["final_totals"] == metadata["final_totals"]
    # Pinned from the first run.
    if CLICKS:
        assert clicks == CLICKS
    if LIGHT_LINE:
        last = line(metadata["audit"][-1], "light")
        assert {key: last[key][0] for key in LIGHT_LINE} == LIGHT_LINE
    if SPREADS is not None:
        assert sum(1 for event in events if event["event"] == "field_spread") == SPREADS

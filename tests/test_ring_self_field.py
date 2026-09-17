"""The ring under its own field (E10) in isolation: the unit-square electron of
loop-binding-v1 with rays of amount 4 releasing its light (released-field-v1)
that spreads by the catalog's table (field-spreading-v1, field-remainder-v1),
and the catalog's electron_field_turn in its momentum-table form
(ray-momentum-turn-v2) declared beside the corner table in both orders. The
engine meets a Node's rays in declared order and a ray one rule took is not
available to a later rule in the same cycle, and on the unit square every
ring Node is a corner: with the corner table first no push ever happens and
the record is the control's event for event; with the coupling first one
electron per corner is pushed by the two edge light rays at tick 2 and taken,
the corner does not fire, and the ring is off its Nodes at tick 3. The world
ledger is exact at every tick.

The worlds are those of examples/nature/e10_self_field/make_worlds.py (checked
byte for byte), the three content-32 worlds run for TICKS ticks through the
runner. The structural expectations are written before the first run and the
record's integers (the escapes, the later pushes, the light line) were read
from the first run of this board and pinned then, as docs/TEST_EXPECTATIONS.md
("The ring meets its own field") says.
"""

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.core.spatial_state import LOOP_BINDING
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/e10_self_field"
NAMES = tuple(f"c{c}_{v}" for c in (32, 64, 128) for v in ("control", "corner_first", "turn_first"))
P0, P1, P2, P3 = (5, 5, 5), (6, 5, 5), (6, 6, 5), (5, 6, 5)
CORNERS = (P0, P1, P2, P3)
AMOUNT = 4
CONTENT = 8 * AMOUNT
# 24 ticks, not the 16 first written: the reader needs a window of at least two
# periods plus one recorded tick, 17 at period 8, before it reads a group (see
# the expectations).
TICKS = 24
RELEASE_PER_INTERVAL = 40
ZERO = [0, 0, 0]
# The eight pushes of tick 2 under turn_first, per corner in the order of the
# record (the light rays in heading-index order): (field heading, before, after).
# The receiver is the resident electron with the lower heading index: the L
# ray at P0 (heading -X) and P2 (+X), the R ray at P1 (+X) and P3 (-X, arriving
# from P2; the computation written before the run had it heading +Y, which is
# the L ray's arrival there, and the record corrected it, see the expectations).
PUSHES_AT_TICK_2 = {
    P0: [([-1, 0, 0], [-4, 0, 0], [-5, 0, 0]), ([0, -1, 0], [-5, 0, 0], [-5, -1, 0])],
    P1: [([1, 0, 0], [4, 0, 0], [5, 0, 0]), ([0, -1, 0], [5, 0, 0], [5, -1, 0])],
    P2: [([1, 0, 0], [4, 0, 0], [5, 0, 0]), ([0, 1, 0], [5, 0, 0], [5, 1, 0])],
    P3: [([-1, 0, 0], [-4, 0, 0], [-5, 0, 0]), ([0, 1, 0], [-5, 0, 0], [-5, 1, 0])],
}
# Pinned from the first run of this board (2026-09-17, the first 16 ticks of the
# 96-tick records of E10, of which a 16-tick run is a prefix): see the
# expectations.
TURN_FIRST_PUSHES = 20  # the count of ray_push events over TICKS ticks: 8, 8 and 4 at ticks 2, 3, 6
TURN_FIRST_PUSHES_PER_TICK = {2: 8, 3: 8, 6: 4}
TURN_FIRST_ELECTRON_ESCAPED_BY = 9  # the first tick with all 32 quanta escaped (16 by tick 8)
TURN_FIRST_LIGHT_LINE = (300, 300, 0)  # (sourced, current, escaped) after tick TICKS
CONTROL_LIGHT_LINE = (920, 900, 20)  # (sourced, current, escaped) after tick TICKS


def load_script(name):
    """A script of the example directory, loaded from its file (not a package)."""
    path = WORLDS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"e10_self_field_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tool(name):
    spec = importlib.util.spec_from_file_location(
        "tools.ray_viewer." + name, ROOT / "tools/ray_viewer" / (name + ".py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def components(value):
    return [value] if isinstance(value, int) else list(value)


def line(ledger, family, readout="fields"):
    entry = ledger[readout][family]
    return {
        key: components(entry[key])
        for key in ("initial", "sourced", "current", "escaped", "annulled", "absorbed")
    }


def run(tmp_path, make_worlds, variant):
    document = make_worlds.world(AMOUNT, variant, ticks=TICKS)
    path = tmp_path / f"{variant}.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    record = tmp_path / variant
    run_initialization(path, record)
    metadata = json.loads((record / "run.json").read_text(encoding="utf-8"))
    events = [
        json.loads(text) for text in (record / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    return record, metadata, events


def without_cost(event):
    """An event without the host's cost line, the physical record alone."""
    return {key: value for key, value in event.items() if key != "cost"}


def electron_arrivals(events, tick):
    """The Nodes at which electron packets were received at a tick."""
    nodes = []
    for event in events:
        if event["event"] != "spatial_received" or event["tick"] != tick:
            continue
        if any(packet.get("electron", [0])[0] for packet in event["received_fields"] if packet):
            nodes.append(tuple(event["position"]))
    return nodes


def check_ledger(metadata, bound):
    assert metadata["conserved_at_every_completed_tick"]
    for ledger in metadata["audit"]:
        assert ledger["balanced"]
        assert all(
            item["balanced"] for readout in ("fields", "charge") for item in ledger[readout].values()
        )
        electron = line(ledger, "electron")
        assert electron["initial"] == [CONTENT]
        assert electron["sourced"] == [0]
        assert electron["current"][0] + electron["escaped"][0] == CONTENT
        assert electron["annulled"] == [0] and electron["absorbed"] == [0]
        if bound:
            assert electron["current"] == [CONTENT] and electron["escaped"] == [0]
            assert line(ledger, "electron", "charge")["current"] == [-3 * CONTENT]
        light = line(ledger, "light")
        assert light["current"][0] + light["escaped"][0] == light["sourced"][0]


def test_the_ring_under_its_own_field(tmp_path):
    make_worlds = load_script("make_worlds")
    generated = dict(make_worlds.cases())
    assert tuple(generated) == NAMES
    for name in NAMES:
        text = (WORLDS / f"{name}.json").read_text(encoding="utf-8")
        assert text == json.dumps(generated[name], indent=1) + "\n", name
    assert [rule["name"] for rule in generated["c32_corner_first"]["ray_interactions"]] == [
        "corner",
        "electron_field_turn",
    ]
    assert [rule["name"] for rule in generated["c32_turn_first"]["ray_interactions"]] == [
        "electron_field_turn",
        "corner",
    ]
    assert generated["c32_turn_first"]["ray_interactions"][0]["momentum_table"] == {"light": 1}
    control, control_meta, control_events = run(tmp_path, make_worlds, "control")
    corner_first, corner_meta, corner_events = run(tmp_path, make_worlds, "corner_first")
    turn_first, turn_meta, turn_events = run(tmp_path, make_worlds, "turn_first")
    for metadata in (control_meta, corner_meta, turn_meta):
        assert metadata["loop_binding"] == LOOP_BINDING == "loop-binding-v1"
        assert metadata["released_field"] == "released-field-v1"
        assert metadata["field_spreading"] == "field-spreading-v1"
        assert metadata["field_remainder"] == "field-remainder-v1"
        assert metadata["completed_ticks"] == TICKS
    assert control_meta["ray_layer_families"] == [["electron"], ["light"]]
    assert corner_meta["ray_layer_families"] == [["electron", "light"]]
    assert turn_meta["ray_layer_families"] == [["electron", "light"]]
    assert "ray_momentum_turn" not in control_meta
    assert "ray_momentum_turn" not in corner_meta
    assert turn_meta["ray_momentum_turn"] == "ray-momentum-turn-v2"
    # The corner table first: no push, the control's record event for event,
    # the ring bound and read as E9's group.
    assert not [event for event in corner_events if event["event"] == "ray_push"]
    # Event for event the control's record but for the host's `cost` line of the
    # cycle records, which counts the light rays the one-layer meeting reads
    # (the byte-for-byte pin written before the first run was wrong about that
    # line and only that line; the expectations keep both statements).
    assert len(corner_events) == len(control_events)
    assert [without_cost(event) for event in corner_events] == [
        without_cost(event) for event in control_events
    ]
    assert (corner_first / "events.jsonl").read_bytes() != (control / "events.jsonl").read_bytes()
    assert {
        (event["event"], key)
        for mine, theirs in zip(corner_events, control_events, strict=True)
        for event in (mine,)
        for key in mine
        if mine.get(key) != theirs.get(key)
    } == {("spatial_cycle", "cost"), ("cycle_started", "cost"), ("cycle_committed", "cost")}
    check_ledger(control_meta, bound=True)
    check_ledger(corner_meta, bound=True)
    for metadata in (control_meta, corner_meta):
        for ledger in metadata["audit"]:
            assert line(ledger, "light")["sourced"] == [
                RELEASE_PER_INTERVAL * max(ledger["tick"] - 1, 0)
            ]
            assert line(ledger, "momentum")["current"] == ZERO
    extract = tool("extract")
    sidecar = tool("record_sidecar")
    for record in (control, corner_first):
        sidecar.write_sidecar(record)
        reading = extract.extract_record(record, sidecar=record / "ray-recording.json")
        (group,) = reading["groups"]
        assert group == {
            "ring": [list(P0), list(P1), list(P2), list(P3)],
            "ring_size": 4,
            "content": CONTENT,
            "families": {"electron": CONTENT},
            "period": 8,
            "clock": {"electron": 1},
            "phase_steps": {"electron": 8},
            "from_tick": 1,
            "to_tick": TICKS - 1,
            "rays": group["rays"],
        }
        assert [row["bound"] for row in reading["ticks_data"]] == (
            [{}] + [{"electron": [CONTENT]}] * (TICKS - 1) + [{}]
        )
    # The coupling first: eight pushes at tick 2, two per corner, the receiver
    # the electron in the lower slot pushed by the two edge light rays in
    # heading-index order; the corner does not fire, the ring is off its Nodes
    # at tick 3, no push at a corner afterwards, no group read.
    pushes = [event for event in turn_events if event["event"] == "ray_push"]
    at_two = [p for p in pushes if p["tick"] == 2]
    assert len(at_two) == 8
    for corner in CORNERS:
        here = [p for p in at_two if tuple(p["position"]) == corner]
        assert [(p["field_heading"], p["before"], p["after"]) for p in here] == PUSHES_AT_TICK_2[corner]
        assert all(
            p["family"] == "electron"
            and p["amount"] == AMOUNT
            and p["field"] == "light"
            and p["field_amount"] == 1
            for p in here
        )
    assert min(p["tick"] for p in pushes) == 2
    assert all(tuple(p["position"]) not in CORNERS for p in pushes if p["tick"] > 2)
    assert set(electron_arrivals(turn_events, 2)) == set(CORNERS)
    assert electron_arrivals(turn_events, 3) and all(
        node not in CORNERS for node in electron_arrivals(turn_events, 3)
    )
    assert all(
        node not in CORNERS
        for tick in range(3, TICKS + 1)
        for node in electron_arrivals(turn_events, tick)
    )
    check_ledger(turn_meta, bound=False)
    momentum_after_two = line(turn_meta["audit"][1], "momentum")
    assert turn_meta["audit"][1]["tick"] == 2
    assert momentum_after_two["sourced"] == ZERO and momentum_after_two["current"] == ZERO
    sidecar.write_sidecar(turn_first)
    reading = extract.extract_record(turn_first, sidecar=turn_first / "ray-recording.json")
    assert reading["groups"] == []
    assert all(row["bound"] == {} for row in reading["ticks_data"])
    # Pinned from the first run of this board: the pushes after tick 2 are
    # off the ring, the escaping rays meeting the light released beside them.
    assert len(pushes) == TURN_FIRST_PUSHES
    per_tick = {}
    for p in pushes:
        per_tick[p["tick"]] = per_tick.get(p["tick"], 0) + 1
    assert per_tick == TURN_FIRST_PUSHES_PER_TICK
    assert all(p["field"] == "light" and p["field_amount"] == 1 for p in pushes)
    escaped = {ledger["tick"]: line(ledger, "electron")["escaped"][0] for ledger in turn_meta["audit"]}
    assert min(t for t, value in escaped.items() if value == CONTENT) == TURN_FIRST_ELECTRON_ESCAPED_BY
    assert turn_meta["escaped_totals"]["electron"] == [CONTENT]
    last = line(turn_meta["audit"][-1], "light")
    assert (last["sourced"][0], last["current"][0], last["escaped"][0]) == TURN_FIRST_LIGHT_LINE
    last = line(control_meta["audit"][-1], "light")
    assert (last["sourced"][0], last["current"][0], last["escaped"][0]) == CONTROL_LIGHT_LINE

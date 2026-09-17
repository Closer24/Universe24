"""The screen with a loop source (E9) in isolation: the unit-square electron of
loop-binding-v1 with rays of amount 4 releasing its light at every corner it
departs (released-field-v1, 40 quanta per interval, booked as a source so the
ring's content stays 32), the light spreading by the catalog's table with the
Node-owned remainder (field-spreading-v1, field-remainder-v1) onto seven Detector
marks at distance 5 to 6, no rule naming the light so that it crosses the ring's
Nodes unmet (ray-layers-v1); the record's group reader reads the ring as one
group of content 32, period 8, clock 1 while it radiates; the on-axis mark
clicks first; the world ledger is exact at every tick.

The board is the E9 world's declarations (examples/nature/screen_loop.json),
built inline, run for TICKS ticks through the runner. The structural
expectations are written before the first run and the record's integers (the
clicks, the light line, the escapes, the spreads) were read from the first run
of this board and pinned then, as docs/TEST_EXPECTATIONS.md ("The screen with a
loop") says: 32 ticks, 2.9 s; seven clicks, all at the on-axis mark (7, 5, 5),
family light, amount 1, bit 1, through Port 1 (the -X face), at ticks 11, 15,
18, 22, 27, 27 and 31, no click off the axis and no pass; the light line after
tick 32 sourced 1240, current 1016, escaped 224; 2759 field_spread records;
the group read from tick 1 to tick 31 over 248 electron chains.
"""

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.core.spatial_state import LOOP_BINDING
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The unit square in the plane y = 5, edge-on to the screen.
P0, P1, P2, P3 = (1, 5, 5), (2, 5, 5), (2, 5, 6), (1, 5, 6)
CORNERS = (P0, P1, P2, P3)
# The R sense P0 -> P1 -> P2 -> P3 -> P0 (+X, +Z, -X, -Z) and the L sense
# P0 -> P3 -> P2 -> P1 -> P0 (+Z, +X, -Z, -X): the Port each sense leaves each
# corner through, ring.json's lamps with Y read as Z.
R_PORTS = (0, 4, 1, 5)
L_PORTS = (4, 1, 5, 0)
AMOUNT = 4
CONTENT = 8 * AMOUNT
MARKS = tuple((7, y, 5) for y in range(2, 9))
AXIS = (7, 5, 5)
TICKS = 32
RELEASE_PER_INTERVAL = 40
ZERO = [0, 0, 0]
# The momentum the two quarter turns of a corner move, booked as its source.
CORNER_SOURCES = {P0: [8, 0, 8], P1: [-8, 0, 8], P2: [-8, 0, -8], P3: [8, 0, -8]}
EVENT_KINDS = {
    "cycle_started",
    "cycle_committed",
    "spatial_cycle_started",
    "spatial_cycle",
    "spatial_sent",
    "spatial_received",
    "spatial_escaped",
    "field_spread",
    "detector_click",
    "detector_pass",
}
# Pinned from the first run of this board (2026-09-17): every click as
# (tick, node, amount, the Port it arrived through), the light line after the
# last tick and the counts.
CLICKS: list[tuple[int, tuple[int, int, int], int, int]] = [
    (11, AXIS, 1, 1),
    (15, AXIS, 1, 1),
    (18, AXIS, 1, 1),
    (22, AXIS, 1, 1),
    (27, AXIS, 1, 1),
    (27, AXIS, 1, 1),
    (31, AXIS, 1, 1),
]
LIGHT_LINE = {"sourced": 1240, "current": 1016, "escaped": 224}
SPREADS = 2759
TO_TICK = TICKS - 1


def lamps():
    """The corner lamps: (position, name, Port), one per sense per corner."""
    result = []
    for k in range(4):
        result.append((CORNERS[k], f"corner_{k}_r", R_PORTS[k]))
        result.append((CORNERS[k], f"corner_{k}_l", L_PORTS[k]))
    return result


def ray_family(name, slots, rate, charge, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 3,
        "charge": charge,
        "kerengonen": {"phase_advance": rate},
        **extra,
    }


def document(ticks=TICKS):
    return {
        "schema_version": 1,
        "model_id": "screen-loop-test-v1",
        "shape": [12, 11, 11],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "electron",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "light",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": name,
                "fields": ["electron", "momentum"],
                "defaults": {"electron": AMOUNT, "momentum": ZERO},
                "transport": {"mode": "hold"},
            }
            for _, name, _ in lamps()
        ],
        "spatial_fields": [
            ray_family("electron", 8, 1, -3),
            ray_family(
                "light",
                24,
                0,
                0,
                field_of="electron",
                release=[1, 4],
                spread=[6, 1, 1, 1, 1, 1],
            ),
        ],
        "emissions": [
            {
                "type": name,
                "field": "electron",
                "amount": AMOUNT,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[port],
                "kerengonen_phase": 0,
            }
            for _, name, port in lamps()
        ],
        "seeds": [{"position": list(position), "type": name} for position, name, _ in lamps()],
        "detectors": [{"position": list(mark), "setting": [1, 1], "seed": 0} for mark in MARKS],
        "ray_interactions": [
            {
                "name": "corner",
                "participants": [{"type": "electron"}, {"type": "electron"}],
                "outputs": [
                    {
                        "field": "electron",
                        "amount": {"of": 0},
                        "heading": "reversed",
                        "input": 1,
                        "phase": {"of": 0},
                    },
                    {
                        "field": "electron",
                        "amount": {"of": 1},
                        "heading": "reversed",
                        "input": 0,
                        "phase": {"of": 1},
                    },
                ],
                "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
            }
        ],
    }


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
    """One line of the world ledger at a completed tick, every entry as a list."""
    entry = ledger[readout][family]
    return {
        key: components(entry[key])
        for key in ("initial", "sourced", "current", "escaped", "annulled", "absorbed")
    }


def test_the_ring_radiates_on_the_screen_and_stays_bound(tmp_path):
    path = tmp_path / "screen_loop.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    record = tmp_path / "screen_loop"
    run_initialization(path, record)
    metadata = json.loads((record / "run.json").read_text(encoding="utf-8"))
    events = [
        json.loads(text) for text in (record / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    # The identities: the loop, the released field, the spreading and the
    # remainder, and light in a layer of its own (no rule names it).
    assert metadata["loop_binding"] == LOOP_BINDING == "loop-binding-v1"
    assert metadata["released_field"] == "released-field-v1"
    assert metadata["field_spreading"] == "field-spreading-v1"
    assert metadata["field_remainder"] == "field-remainder-v1"
    assert metadata["released_fields"] == [{"field": "light", "field_of": "electron", "release": [1, 4]}]
    assert metadata["spreading_fields"] == [{"field": "light", "spread": [6, 1, 1, 1, 1, 1]}]
    assert ["light"] in metadata["ray_layer_families"]
    assert metadata["completed_ticks"] == TICKS
    # The ledger: every line balanced at every completed tick, the electron line
    # 32 with no source, escape, annulment or absorption (the source stays bound
    # while it radiates), light sourced 40 per interval from the cycle of tick 1
    # with current + escaped = sourced, momentum (0, 0, 0).
    assert metadata["conserved_at_every_completed_tick"]
    for ledger in metadata["audit"]:
        tick = ledger["tick"]
        assert ledger["balanced"]
        assert all(
            item["balanced"] for readout in ("fields", "charge") for item in ledger[readout].values()
        )
        electron = line(ledger, "electron")
        assert electron == {
            "initial": [CONTENT],
            "sourced": [0],
            "current": [CONTENT],
            "escaped": [0],
            "annulled": [0],
            "absorbed": [0],
        }
        assert line(ledger, "electron", "charge")["current"] == [-3 * CONTENT]
        light = line(ledger, "light")
        assert light["sourced"] == [RELEASE_PER_INTERVAL * max(tick - 1, 0)]
        assert light["current"][0] + light["escaped"][0] == light["sourced"][0]
        assert light["annulled"] == [0] and light["absorbed"] == [0]
        momentum = line(ledger, "momentum")
        assert momentum["sourced"] == ZERO and momentum["current"] == ZERO
    assert metadata["final_totals"]["electron"] == [CONTENT]
    assert metadata["final_totals"]["momentum"] == ZERO
    assert metadata["escaped_totals"]["electron"] == [0]
    # The corners book their two quarter turns and their ten releases in every
    # cycle from tick 1; no event of a kind the world has no rule for exists.
    assert {event["event"] for event in events} <= EVENT_KINDS
    for tick in range(1, TICKS):
        booked = {
            tuple(event["position"]): event["source_delta"]
            for event in events
            if event["event"] == "spatial_cycle"
            and event["tick"] == tick
            and tuple(event["position"]) in CORNERS
        }
        assert {corner: delta["momentum"] for corner, delta in booked.items()} == CORNER_SOURCES
        assert all(delta["light"] == [10] for delta in booked.values())
    # The clicks: every one of family light, amount 1, bit 1, at a mark; the
    # first at the on-axis mark before E6's tick 19; a click off the axis
    # mirrored at (7, 10 - y, 5) in the same tick.
    clicks = [
        (event["tick"], tuple(event["position"]), event["amount"], event["port"])
        for event in events
        if event["event"] == "detector_click"
    ]
    assert all(
        event["family"] == "light" and event["bit"] == 1
        for event in events
        if event["event"] == "detector_click"
    )
    assert all(node in MARKS and amount == 1 for _, node, amount, _ in clicks)
    assert clicks and clicks[0][1] == AXIS and clicks[0][0] < 19
    plain = [(tick, node, amount) for tick, node, amount, _ in clicks]
    for tick, (x, y, z), amount in plain:
        assert (tick, (x, 10 - y, z), amount) in plain
    assert clicks == CLICKS
    last = line(metadata["audit"][-1], "light")
    assert (last["sourced"], last["current"], last["escaped"]) == (
        [LIGHT_LINE["sourced"]],
        [LIGHT_LINE["current"]],
        [LIGHT_LINE["escaped"]],
    )
    assert sum(1 for event in events if event["event"] == "field_spread") == SPREADS
    # The reading of the group from the record with its recording: one group on
    # the square, content 32, period 8, clock 1, the light entering none.
    extract = tool("extract")
    sidecar = tool("record_sidecar")
    sidecar.write_sidecar(record)
    run = extract.extract_record(record, sidecar=record / "ray-recording.json")
    (group,) = run["groups"]
    assert group == {
        "ring": [list(P0), list(P1), list(P2), list(P3)],
        "ring_size": 4,
        "content": CONTENT,
        "families": {"electron": CONTENT},
        "period": 8,
        "clock": {"electron": 1},
        "phase_steps": {"electron": 8},
        "from_tick": 1,
        "to_tick": TO_TICK,
        "rays": group["rays"],
    }
    assert all(run["rays"][i]["family"] == "electron" for i in group["rays"])
    assert [row["bound"] for row in run["ticks_data"]] == (
        [{}] + [{"electron": [CONTENT]}] * (TICKS - 1) + [{}]
    )
    assert run["eye"]["clicks"] == [
        {"tick": tick, "node": list(node), "family": "light", "amount": amount, "bit": 1, "port": port}
        for tick, node, amount, port in CLICKS
    ]

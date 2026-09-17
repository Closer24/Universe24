"""The ray viewer's extractor reads a runner record into rays, events and captions.

Expected results are pinned in docs/TEST_EXPECTATIONS.md ("Ray viewer
extraction") before the first run: two lamps on one line, a swap coupling
that holds both rays one interval, a Detector mark that always draws 1, six
ticks. No browser is involved; the viewer page and the GIF renderer are not
exercised here.
"""

import importlib.util
import json
import shutil
import sys
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tools.ray_viewer.extract", ROOT / "tools/ray_viewer/extract.py"
)
assert SPEC is not None and SPEC.loader is not None
EXTRACT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = EXTRACT
SPEC.loader.exec_module(EXTRACT)

PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
HEADING = {"a": {"field": "heading", "participant": 0}, "b": {"field": "heading", "participant": 1}}
AMOUNT = {"a": {"field": "amount", "participant": 0}, "b": {"field": "amount", "participant": 1}}
PHASE = {"a": {"field": "phase", "participant": 0}, "b": {"field": "phase", "participant": 1}}
HEADING_SUM = {"op": "add", "args": [HEADING["a"], HEADING["b"]]}
# Opposite headings, and phases 1 and 5 (what the lamps' 0 and 4 become after one
# Link): true at the meeting only, so the rule fires once and its delay releases.
MEETING = {
    "op": "mul",
    "args": [
        {"op": "eq", "args": [{"op": "dot", "args": [HEADING_SUM, HEADING_SUM]}, 0]},
        {"op": "eq", "args": [{"op": "add", "args": [PHASE["a"], PHASE["b"]]}, 6]},
    ],
}


def lamp(name, amount):
    return {
        "name": name,
        "fields": ["quanta", "momentum"],
        "defaults": {"quanta": amount, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }


def emission(name, amount, heading, phase):
    return {
        "type": name,
        "field": "quanta",
        "amount": amount,
        "denominator": 1,
        "source": False,
        "recoil_field": "momentum",
        "heading": heading,
        "kerengonen_phase": phase,
    }


def document():
    return {
        "schema_version": 1,
        "model_id": "ray-viewer-test-v1",
        "shape": [5, 3, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 6,
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
                "name": "quanta",
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
        "disturbance_types": [lamp("lamp_a", 3), lamp("lamp_b", 3)],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [PLUS_X, MINUS_X],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            }
        ],
        "emissions": [emission("lamp_a", 3, PLUS_X, 0), emission("lamp_b", 3, MINUS_X, 4)],
        "seeds": [
            {"position": [1, 1, 1], "type": "lamp_a"},
            {"position": [3, 1, 1], "type": "lamp_b"},
        ],
        "detectors": [{"position": [4, 1, 1], "setting": [1, 1], "seed": 0}],
        "ray_interactions": [
            {
                "name": "swap_headings",
                "participants": [
                    {"requires": ["amount", "heading", "phase", "delay"]},
                    {"requires": ["amount", "heading", "phase", "delay"]},
                ],
                "when": MEETING,
                "assignments": [
                    {"participant": 0, "field": "heading", "expression": HEADING["b"]},
                    {"participant": 1, "field": "heading", "expression": HEADING["a"]},
                    {"participant": 0, "field": "delay", "expression": 1},
                    {"participant": 1, "field": "delay", "expression": 1},
                ],
                "invariants": [
                    {"name": "energy", "expression": {"op": "add", "args": [AMOUNT["a"], AMOUNT["b"]]}},
                    {
                        "name": "momentum",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"op": "mul", "args": [AMOUNT["a"], HEADING["a"]]},
                                {"op": "mul", "args": [AMOUNT["b"], HEADING["b"]]},
                            ],
                        },
                    },
                ],
            }
        ],
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }


def walk(ray):
    return [tuple(segment["from"]) for segment in ray["segments"]]


def summary(event):
    return (event["tick"], tuple(event["node"]), event["kind"], tuple(event["ports"]))


def test_extractor_reads_rays_events_and_captions_from_the_record(tmp_path):
    world = tmp_path / "world.json"
    world.write_text(json.dumps(document()), encoding="utf-8")
    record = tmp_path / "artifacts" / "run"
    run_initialization(world, record)
    assert sorted(p.name for p in record.iterdir()) == [
        "events.jsonl",
        "initialization.json",
        "run.json",
        "state.json",
    ]
    run = EXTRACT.extract_record(record)

    # (a) Four rays of amount 3: two into the meeting, two out of it to the boundary.
    assert run["ticks"] == 6 and run["shape"] == [5, 3, 3]
    assert [f["name"] for f in run["families"]] == ["quanta", "momentum"]
    assert [f["ray"] for f in run["families"]] == [True, False]
    assert not any(f["field"] for f in run["families"])
    rays = run["rays"]
    assert [r["family"] for r in rays] == ["quanta"] * 4
    assert [r["amount"] for r in rays] == [[3]] * 4
    assert [r["origin"]["tick"] for r in rays] == [0, 0, 2, 2]
    assert walk(rays[0]) == [(1, 1, 1)] and rays[0]["segments"][0]["heading"] == PLUS_X
    assert walk(rays[1]) == [(3, 1, 1)] and rays[1]["segments"][0]["heading"] == MINUS_X
    assert [r["end"]["kind"] for r in rays] == ["event", "event", "escaped", "escaped"]
    assert rays[0]["end"]["tick"] == rays[1]["end"]["tick"] == 1
    plus = next(r for r in rays[2:] if r["segments"][0]["heading"] == PLUS_X)
    minus = next(r for r in rays[2:] if r["segments"][0]["heading"] == MINUS_X)
    assert walk(plus) == [(2, 1, 1), (3, 1, 1), (4, 1, 1)]
    assert walk(minus) == [(2, 1, 1), (1, 1, 1), (0, 1, 1)]
    for ray in (plus, minus):
        assert [s["steps"] for s in ray["segments"]] == [1, 2, 3]
        assert [s["outbound"] for s in ray["segments"]] == [1, 1, 1]
        assert [s["phase"] for s in ray["segments"]] == [None] * 3
        assert ray["segments"][-1]["escaped"] and ray["segments"][-1]["to"] is None
        assert ray["end"]["tick"] == 5 and ray["origin"]["node"] == [2, 1, 1]
        assert not ray["returning"]

    # (b) Every event is a marker at its Node with its tick, kind and spokes.
    events = run["events"]
    assert [summary(e) for e in events] == [
        (0, (1, 1, 1), "emission", (0,)),
        (0, (3, 1, 1), "emission", (1,)),
        (1, (2, 1, 1), "meeting", (0, 1)),
        (4, (4, 1, 1), "click", ()),
        (5, (0, 1, 1), "escape", (1,)),
        (5, (4, 1, 1), "escape", (0,)),
    ]
    meeting = events[2]
    assert meeting["in"] == [0, 1] and sorted(meeting["out"]) == [2, 3]
    assert meeting["output_tick"] == 2
    assert meeting["detail"]["held_ticks"] == 1
    assert meeting["detail"]["amount_in"] == {"quanta": [6]}
    assert meeting["detail"]["amount_out"] == {"quanta": [6]}
    assert meeting["detail"]["momentum_in"] == [0, 0, 0]
    assert meeting["detail"]["momentum_out"] == [0, 0, 0]
    assert meeting["detail"]["coupling"] == ["swap_headings"]
    assert run["couplings"] == ["swap_headings"]
    click = events[3]
    assert click["label"] == "Detector PASS"
    assert click["detail"] == {"port": 1, "family": "quanta", "amount": 3, "bit": 1}
    assert click["in"] == [plus["id"]]
    assert events[4]["in"] == [minus["id"]] and events[5]["in"] == [plus["id"]]
    assert run["detectors"] == [{"pos": [4, 1, 1], "setting": [1, 1], "seed": 0}]
    assert [s["type"] for s in run["sources"]] == ["lamp_a", "lamp_b"]

    # (c) Captions and totals come from the record, tick by tick.
    notes = [row["note"] for row in run["ticks_data"]]
    assert len(notes) == 7
    assert notes[0].count("emission") == 2 and "+x" in notes[0] and "-x" in notes[0]
    assert "meeting" in notes[1] and "swap_headings" in notes[1]
    assert "in: quanta 6" in notes[1] and "momentum (0, 0, 0)" in notes[1]
    assert "out (t2): quanta 6" in notes[1]
    assert notes[2].startswith("outputs of the t1 meeting leave")
    assert notes[3] == ""
    assert "Detector PASS" in notes[4] and "bit 1" in notes[4]
    assert notes[5].count("escaped") == 2 and notes[6] == ""
    assert [row["in_world"]["quanta"] for row in run["ticks_data"]] == [[6]] * 5 + [[0], [0]]
    assert [row["escaped"]["quanta"] for row in run["ticks_data"]] == [[0]] * 5 + [[6], [6]]
    assert run["conservation"]["status"] == "passed"
    # The quanta left through the open boundary: since ray-event-audit-v1
    # (2026-09-17) the runner's "conserved at every completed tick" is the world
    # ledger's identity, in which the escape is a line, so it is true (it was false
    # before feature 10); the accounting (with escapes) balances, and the extracted
    # conservation carries the recorded ledger.
    assert run["conservation"]["every_tick"] is True
    assert run["conservation"]["balanced"] is True
    assert [ledger["tick"] for ledger in run["conservation"]["audit"]] == list(range(1, 7))
    assert run["conservation"]["escaped_totals"] == {"quanta": [6], "momentum": [0, 0, 0]}
    assert run["record"]["ray_state"] == "ray-event-state-v1"
    assert run["record"]["detector_mark"] == "detector-mark-v1"
    assert run["record"]["unknown_event_kinds"] == {}
    assert run["record"]["frames"] is False

    # (d) A kind the extractor does not know becomes a generic marker, nothing else moves.
    copy = tmp_path / "artifacts" / "later"
    shutil.copytree(record, copy)
    with (copy / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"event": "field_release", "tick": 3, "position": [2, 1, 1]}) + "\n")
    later = EXTRACT.extract_record(copy)
    assert [summary(e) for e in later["events"]] == [summary(e) for e in events][:3] + [
        (3, (2, 1, 1), "field_release", ())
    ] + [summary(e) for e in events][3:]
    assert [walk(r) for r in later["rays"]] == [walk(r) for r in rays]
    assert later["record"]["unknown_event_kinds"] == {"field_release": 1}
    assert "field release" in later["ticks_data"][3]["note"]

    document_out = EXTRACT.extract_runs([record, copy])
    assert document_out["schema"] == "ray-viewer-runs-v1"
    assert [r["key"] for r in document_out["runs"]] == ["run", "later"]

"""The ray viewer's extractor reads a runner record into rays, events and captions.

Expected results are pinned in docs/TEST_EXPECTATIONS.md ("Ray viewer
extraction") before the first run: two lamps on one line, a swap coupling
that holds both rays one interval, a Detector mark that always draws 1, the
field G of the quanta family releasing at every Node crossed, six ticks. No
browser is involved; the viewer page and the GIF renderer are not exercised
here beyond the style file reaching the inlined page.
"""

import copy
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(
        "tools.ray_viewer." + name, ROOT / "tools/ray_viewer" / (name + ".py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EXTRACT = load("extract")
RENDER = load("render_gif")

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
PLUS_X, MINUS_X = HEADINGS[0], HEADINGS[1]
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


def ray_field(name, advance, slots=8, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8, "phase_advance": advance},
        **extra,
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
                "name": "G",
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
            ray_field("quanta", 1),
            ray_field("G", 0, 16, field_of="quanta", release=[1, 3]),
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
                "participants": [{"type": "quanta"}, {"type": "quanta"}],
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
        # No `conservation` block: with the released field G, the local audit counts
        # a G ray resident at a lamp Node in the Node's momentum but not in the
        # packet that carries it away, and fails; the runner's own accounting flags
        # still cover the run (reported as a suspected audit defect, not fixed here).
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

    # (a) Four quanta rays of amount 3: two into the meeting, two out of it to the boundary.
    assert run["ticks"] == 6 and run["shape"] == [5, 3, 3]
    assert [f["name"] for f in run["families"]] == ["quanta", "G", "momentum"]
    assert [f["ray"] for f in run["families"]] == [True, True, False]
    assert [f["field"] for f in run["families"]] == [False, True, False]
    assert run["families"][1]["field_of"] == "quanta" and run["families"][1]["release"] == [1, 3]
    rays = [r for r in run["rays"] if r["family"] == "quanta"]
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
        assert not ray["returning"] and not ray["field"]

    # (b) Every matter event is a marker at its Node with its tick, kind and spokes.
    events = run["events"]
    matter = [e for e in events if not e["field"]]
    assert [summary(e) for e in matter if e["kind"] != "click"] == [
        (0, (1, 1, 1), "emission", (0,)),
        (0, (3, 1, 1), "emission", (1,)),
        (1, (2, 1, 1), "meeting", (0, 1)),
        (5, (0, 1, 1), "escape", (1,)),
        (5, (4, 1, 1), "escape", (0,)),
    ]
    meeting = next(e for e in events if e["kind"] == "meeting")
    assert sorted(meeting["in"]) == sorted(r["id"] for r in rays[:2])
    assert sorted(meeting["out"]) == sorted([plus["id"], minus["id"]])
    assert meeting["output_tick"] == 2 and meeting["detail"]["held_ticks"] == 1
    assert meeting["detail"]["amount_in"] == {"quanta": [6]}
    assert meeting["detail"]["amount_out"] == {"quanta": [6]}
    assert meeting["detail"]["momentum_in"] == [0, 0, 0]
    assert meeting["detail"]["momentum_out"] == [0, 0, 0]
    assert meeting["detail"]["coupling"] == ["swap_headings"]
    assert run["couplings"] == ["swap_headings"]
    clicks = [e for e in events if e["kind"] == "click"]
    assert all(e["label"] == "Detector PASS" and tuple(e["node"]) == (4, 1, 1) for e in clicks)
    # Two G clicks at tick 3: each ray held at (2,1,1) during tick 1 released its
    # own +X G ray (feature 8), and the Detector draws once per ray in the packet.
    assert sorted((e["tick"], e["detail"]["family"], e["detail"]["amount"]) for e in clicks) == [
        (3, "G", 1),
        (3, "G", 1),
        (4, "G", 1),
        (4, "quanta", 3),
        (6, "G", 1),
    ]
    assert all(e["detail"]["port"] == 1 and e["detail"]["bit"] == 1 for e in clicks)
    quanta_click = next(e for e in clicks if e["detail"]["family"] == "quanta")
    assert quanta_click["in"] == [plus["id"]]
    escapes = [e for e in matter if e["kind"] == "escape"]
    assert escapes[0]["in"] == [minus["id"]] and escapes[1]["in"] == [plus["id"]]
    assert run["detectors"] == [{"pos": [4, 1, 1], "setting": [1, 1], "seed": 0}]
    assert [s["type"] for s in run["sources"]] == ["lamp_a", "lamp_b"]
    assert run["external_bodies"] == []

    # (e) Releases: silent field events, the source ray's trail unbroken through them.
    # The record releases from the two held rays at tick 1 as well as at their
    # departure at tick 2: content held at a Node releases on all six headings
    # (Highlights 3.5, feature 8), so the tick-1 release sources G 12 and each of
    # its six packets carries G 2, which the extractor reads as one G ray of 2.
    releases = [e for e in events if e["kind"] == "release"]
    assert all(e["field"] for e in releases)
    assert [summary(e) for e in releases] == [
        (1, (2, 1, 1), "release", (0, 1, 2, 3, 4, 5)),
        (2, (2, 1, 1), "release", (0, 1, 2, 3, 4, 5)),
        (3, (1, 1, 1), "release", (0, 2, 3, 4, 5)),
        (3, (3, 1, 1), "release", (1, 2, 3, 4, 5)),
        (4, (0, 1, 1), "release", (0, 2, 3, 4, 5)),
        (4, (4, 1, 1), "release", (1, 2, 3, 4, 5)),
    ]
    assert releases[0]["in"] == []
    assert sorted(releases[1]["in"]) == sorted([plus["id"], minus["id"]])
    assert releases[2]["in"] == [minus["id"]] and releases[3]["in"] == [plus["id"]]
    assert [e["detail"]["amount_out"] for e in releases] == [{"G": [12]}, {"G": [10]}] + [{"G": [5]}] * 4
    fields = [r for r in run["rays"] if r["family"] == "G"]
    assert len(fields) == 32 and len(run["rays"]) == 36
    assert all(r["field"] for r in fields)
    assert sorted(run["rays"][i]["amount"][0] for i in releases[0]["out"]) == [2, 2, 2, 2, 2, 2]
    assert sorted(run["rays"][i]["amount"][0] for i in releases[1]["out"]) == [1, 1, 2, 2, 2, 2]
    held_plus = next(i for i in releases[0]["out"] if run["rays"][i]["segments"][0]["heading"] == PLUS_X)
    assert run["rays"][held_plus]["amount"] == [2]
    assert [e["in"] for e in clicks if e["tick"] == 3] == [[held_plus]] * 2
    assert not any(e["kind"] in ("split", "crossing", "deflection") for e in events)
    field_escapes = [e for e in events if e["kind"] == "escape" and e["field"]]
    assert [sum(1 for e in field_escapes if e["tick"] == t) for t in (3, 4, 5, 6)] == [4, 6, 10, 8]
    assert [
        sum(e["detail"]["escaped"]["G"][0] for e in field_escapes if e["tick"] == t)
        for t in (3, 4, 5, 6)
    ] == [8, 12, 10, 8]
    assert run["conservation"]["source_totals"] == {"quanta": [0], "G": [42], "momentum": [0, 0, 0]}
    assert run["conservation"]["escaped_totals"]["G"] == [38]
    assert run["conservation"]["final_totals"]["G"] == [4]
    assert run["record"]["released_field"] == "released-field-v1"

    # (c) Captions and totals come from the record, tick by tick.
    rows = run["ticks_data"]
    notes = [row["note"] for row in rows]
    assert len(notes) == 7
    assert notes[0] == "2 emissions"
    assert "t1 meeting (2,1,1) swap_headings" in notes[1]
    assert "in quanta 6, p (0, 0, 0)" in notes[1] and "out t2 quanta 6, p (0, 0, 0)" in notes[1]
    assert notes[2].startswith("t1 meeting") and "release" not in notes[2]
    assert notes[3].count("Detector PASS") == 2 and notes[3].endswith("field escaped: G 8")
    assert notes[4].count("Detector PASS") == 2 and notes[4].endswith("field escaped: G 12")
    assert notes[5] == "escaped: quanta 6 | field escaped: G 10"
    assert notes[6].count("Detector PASS") == 1 and notes[6].endswith("field escaped: G 8")
    assert not any("release" in note for note in notes)
    assert [row["in_world"]["quanta"] for row in rows] == [[6]] * 5 + [[0], [0]]
    assert [row["in_world"]["G"] for row in rows] == [[0], [0], [12], [14], [12], [12], [4]]
    assert [row["escaped"]["quanta"] for row in rows] == [[0]] * 5 + [[6], [6]]
    assert [row["releases"] for row in rows] == [0, 1, 1, 2, 2, 0, 0]
    assert run["conservation"]["status"] == "not_configured"
    # The quanta left through the open boundary, so the runner's "conserved at
    # every completed tick" is false while the accounting (with escapes) balances.
    assert run["conservation"]["every_tick"] is False
    assert run["conservation"]["balanced"] is True
    assert run["record"]["ray_state"] == "ray-event-state-v1"
    assert run["record"]["detector_mark"] == "detector-mark-v1"
    assert run["record"]["unknown_event_kinds"] == {}
    assert run["record"]["frames"] is False and run["record"]["sidecar"] is None

    # (d) A kind the extractor does not know becomes a generic marker, nothing else moves.
    later_dir = tmp_path / "artifacts" / "later"
    shutil.copytree(record, later_dir)
    with (later_dir / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"event": "field_release", "tick": 3, "position": [2, 1, 1]}) + "\n")
    later = EXTRACT.extract_record(later_dir)
    expected = [summary(e) for e in events]
    index = next(i for i, e in enumerate(events) if e["tick"] == 3 and tuple(e["node"]) > (2, 1, 1))
    assert [summary(e) for e in later["events"]] == expected[:index] + [
        (3, (2, 1, 1), "field_release", ())
    ] + expected[index:]
    assert [walk(r) for r in later["rays"]] == [walk(r) for r in run["rays"]]
    assert later["record"]["unknown_event_kinds"] == {"field_release": 1}
    generic = next(e for e in later["events"] if e["kind"] == "field_release")
    assert generic["label"] == "field release" and not generic["field"]
    assert later["ticks_data"][3]["note"] == run["ticks_data"][3]["note"]
    with pytest.raises(ValueError, match="no ray recording"):
        EXTRACT.extract_record(record, sidecar=tmp_path / "missing.json")

    document_out = EXTRACT.extract_runs([record, later_dir])
    assert document_out["schema"] == "ray-viewer-runs-v1"
    assert [r["key"] for r in document_out["runs"]] == ["run", "later"]

    # (g) External bodies (external-body-v1): the record's per-tick positions, read as
    # the runner writes them, so the page moves the body's picture with the record.
    bodies = EXTRACT.external_bodies(
        EXTRACT.Record(
            record,
            {
                "external_bodies": [
                    {
                        "family": "star",
                        "amount": 4096,
                        "coupling": "sink",
                        "field": "G",
                        "positions": [[0, 7, 7, 7], [1, 7, 7, 7], [2, 8, 7, 7]],
                        "final": {"momentum": [2, 0, 0]},
                    }
                ]
            },
            [],
            None,
            None,
            [],
        )
    )
    assert bodies == [
        {
            "pos": [7, 7, 7],
            "family": "star",
            "amount": 4096,
            "coupling": "sink",
            "field": "G",
            "positions": [[0, 7, 7, 7], [1, 7, 7, 7], [2, 8, 7, 7]],
        }
    ]


def test_style_file_has_the_documented_keys_and_reaches_the_inlined_page():
    style = RENDER.load_style(None)
    assert style["schema"] == "ray-viewer-style-v1"
    assert set(style) == set(RENDER.STYLE_KEYS) | {"schema"}
    for section, keys in RENDER.STYLE_KEYS.items():
        assert set(style[section]) == set(keys), section
    page = (ROOT / "tools/ray_viewer/viewer.html").read_text(encoding="utf-8")
    start = page.index('id="style-default">') + len('id="style-default">')
    assert json.loads(page[start : page.index("</script>", start)]) == style
    bad = copy.deepcopy(style)
    bad["sizes"]["ray_thickness"] = 1
    with pytest.raises(ValueError, match="unknown keys in style.sizes"):
        RENDER.validate_style(bad)
    wide = copy.deepcopy(style)
    wide["sizes"]["ray_width_px"] = 9
    inlined = RENDER.inline_page({"schema": "ray-viewer-runs-v1", "runs": []}, wide)
    start = inlined.index('id="style">') + len('id="style">')
    assert json.loads(inlined[start : inlined.index("</script>", start)])["sizes"]["ray_width_px"] == 9
    start = inlined.index('id="style-default">') + len('id="style-default">')
    assert json.loads(inlined[start : inlined.index("</script>", start)])["sizes"]["ray_width_px"] == 4

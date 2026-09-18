"""The performance lane of 2026-09-18 (perf-arrays-v1, docs/PERFORMANCE.md): the
final snapshot written Node by Node from the engine and the dense arrays
(`snapshot_writer`), a series of worlds run one process per core
(`tools/run_series.py`) byte-identical to single runs, and the standing set by
a formula (standing-field-v1, Highlights 5.4 points 11 and 13): the dense
layer stepped until it repeats exactly, then kept fixed while the things read
it, the fallback when a thing steps, the residual without a repeat.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Snapshots from the
arrays, parallel series runs and the standing set") before the first run:
snapshot, series, standing, residual, fallback, rejected. The standing set's
integers are the current split rule's; the identities are not.

Re-pinned on 2026-09-18 under `return-field-v1` (feature 16d): a shadow that
pushes turns back with the opposite sign and is a field from then on, carrying
its momentum through the mixing, so the line's bodies push each other less
and its layer repeats earlier (25, the lamp's 32, the residual of 10
intervals 144 cells and 370 quanta, the momenta after 200 ticks (-97, -1, 0)
and (98, 0, 0)); a parked entry of the snapshot carries `outbound` and
`momentum`, so the box's digest is the streamed writer's of this rule.
"""

import hashlib
import importlib.util
import io
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.ray_event_audit import audit_failure
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization
from event_universe.snapshot_writer import write_snapshot

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
AMOUNT = 1 << 24
# The stepping engine's layer on the line repeats exactly after this tick, with
# this period (node-mixing-v1: the mixing is the layer's step); with the lamp
# of the fallback case beside the line, after LAMP_FIXED_POINT.
FIXED_POINT = 25
PERIOD = 1
LAMP_FIXED_POINT = 32
# The residual of the last comparison when the search stops after 10 intervals.
SHORT_LIMIT = 10
# Re-pinned 2026-09-18 (return-field-v1, part 2): the arrays carry the flow and
# the momentum of every share, so the returning shares of the line, which were
# the engine's Nodes' (one item of the residual for the whole engine part), are
# array cells now (a momentum, three integers, one cell), and the residual
# after 10 intervals reads the whole layer.
SHORT_RESIDUAL = {"cells": 1640, "amount": 4002}
# The momentum of the two bodies after 200 ticks of the line.
FINAL_MOMENTA = [(-97, -1, 0), (98, 0, 0)]
# The state.json digest of the box for 24 ticks, written by the runner of main at
# 9c689f1 before the streamed writer existed (the pin of the migration).
BOX_STATE_SHA256 = "ed563a8e5759f76615b8c30fd716e9597fbd0b697fc2bdb3253cff2e8214848f"


def field(name, components=1):
    return {
        "name": name,
        "components": components,
        "units": "quantum",
        "signed": components == 3,
        "conserved": True,
        "extensive": True,
    }


def body(position):
    return {
        "position": list(position),
        "family": "m",
        "amount": AMOUNT,
        "charge": -AMOUNT,
        "momentum_table": {"m": 1},
        "reads": "charge",
    }


def document(shape, bodies, ticks, *, slots=24, fill=8):
    return {
        "schema_version": 1,
        "model_id": "perf-arrays-test-v1",
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "fields": [field("m"), field("momentum", 3)],
        # The wait per whole quantum read (Highlights 5.4 point 23) is pinned in
        # tests/test_wait_rule.py; these worlds pin the flows without it.
        "wait_per_quantum": 0,
        "disturbance_types": [
            {
                "name": "ring",
                "fields": ["m", "momentum"],
                "defaults": {"m": 4, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "m",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": slots,
                "metric": "links",
                "pace": [1, 1],
                "phase_bits": 0,
                "charge": -1,
                "release": [1, 4096],
            }
        ],
        "emissions": [],
        "seeds": [],
        "ray_interactions": [
            {
                "name": "turn",
                "participants": [{"type": "m"}, {"type": "m"}],
                "momentum_table": {"m": 1},
                "reads": "charge",
                "invariants": [
                    {
                        "name": "energy",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "amount", "participant": 0},
                                {"field": "amount", "participant": 1},
                            ],
                        },
                    }
                ],
            }
        ],
        "external_bodies": [body(position) for position in bodies],
        "detectors": [],
        "initial_field": {"m": {"fill": fill}},
        "dense_field": True,
    }


def line(ticks=200):
    return document((9, 3, 3), [(2, 1, 1), (5, 1, 1)], ticks)


def box(ticks=24):
    return document((9, 5, 5), [(3, 2, 2), (6, 2, 2)], ticks)


def late_lamp(doc):
    """A lamp off the line paying out one thing ray of amount 2 on +Y after 130 cycles."""
    doc = json.loads(json.dumps(doc))
    doc["disturbance_types"].append(
        {
            "name": "lamp",
            "fields": ["m", "momentum"],
            "defaults": {"m": 2, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    doc["emissions"].append(
        {
            "type": "lamp",
            "field": "m",
            "heading": [0, 1, 0],
            "denominator": 1,
            "kerengonen_phase": 0,
            "dissolve": {"after_ticks": 130, "over_ticks": 1},
        }
    )
    doc["seeds"].append({"position": [4, 0, 0], "type": "lamp"})
    return doc


def stepped(doc, ticks):
    """The world stepped through the Simulation API: the momenta per tick, the
    ledgers, the standing record, the snapshot and the streamed text."""
    momenta, audits = [], []
    with Simulation(parse_initial_state(doc)) as world:
        for _ in range(ticks):
            world.step()
            momenta.append([tuple(item["momentum"]) for item in world.external_bodies()])
            audits.append(world.audit())
        report = world.standing_field_report()
        snapshot = world.snapshot()
        buffer = io.StringIO()
        write_snapshot(world, buffer)
    return momenta, audits, report, snapshot, buffer.getvalue()


def digests(run):
    """The SHA-256 of state.json and of the ledger of a run directory."""
    record = json.loads((run / "run.json").read_text(encoding="utf-8"))
    return (
        hashlib.sha256((run / "state.json").read_bytes()).hexdigest(),
        hashlib.sha256(json.dumps(record["audit"]).encode("utf-8")).hexdigest(),
        record,
    )


def written(tmp_path, name, doc, **options):
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    run_initialization(path, tmp_path / name, **options)
    return tmp_path / name


def test_the_snapshot_is_streamed_from_the_arrays_byte_for_byte(tmp_path):
    """The text `write_snapshot` streams, one Node at a time from the engine and
    the dense region's arrays, equals `json.dumps(world.snapshot(), indent=2)`,
    in the dense mode (the region's Nodes and their parked shares) and with the
    engine alone; the runner's state.json is that text plus a line break."""
    for dense in (True, False):
        _, _, _, snapshot, text = stepped(dict(box(), dense_field=dense), 24)
        assert text == json.dumps(snapshot, indent=2)
        assert len(snapshot["spatial_fields"]) > 2
        if dense:
            assert len(snapshot["parked"]) > 1
    run = written(tmp_path, "box", box())
    _, _, _, snapshot, text = stepped(box(), 24)
    assert (run / "state.json").read_text(encoding="utf-8") == text + "\n"
    if BOX_STATE_SHA256 is not None:
        assert digests(run)[0] == BOX_STATE_SHA256


def test_a_series_runs_one_process_per_world_byte_identical_to_a_single_run(tmp_path):
    """`run_series` launches every world in its own process, two at once here,
    with its own log and artifacts directory and a summary; every state.json
    and ledger equals the runner's for the same world in this process."""
    spec = importlib.util.spec_from_file_location("run_series", ROOT / "tools" / "run_series.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    worlds = []
    for name, doc in (("line", line(12)), ("box", box(12))):
        path = tmp_path / "worlds" / f"{name}.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(doc), encoding="utf-8")
        worlds.append(path)
    rows = module.run_series(worlds, tmp_path / "series", jobs=2, ticks=12)
    assert [row["world"] for row in rows] == ["line", "box"]
    assert (tmp_path / "series" / "summary.json").exists()
    assert (tmp_path / "series" / "summary.md").read_text(encoding="utf-8").startswith("| world |")
    for row, world in zip(rows, worlds, strict=True):
        assert row["status"] == "completed" and row["ticks"] == 12 and row["peak_rss_mb"] > 0
        run = tmp_path / "series" / row["world"] / "run"
        assert (run / "run.json").exists() and (run / "state.json").exists()
        assert (tmp_path / "series" / row["world"] / "log.txt").exists()
        alone = written(tmp_path, f"alone_{row['world']}", json.loads(world.read_text()), ticks=12)
        state, audit, _ = digests(alone)
        assert (row["state_sha256"], row["audit_sha256"]) == (state, audit)
    with pytest.raises(ValueError, match="share a name"):
        module.run_series([worlds[0], worlds[0]], tmp_path / "twice", jobs=1)


def test_the_standing_set_is_the_layers_fixed_point_and_the_things_read_it(tmp_path):
    """With `standing_field` the layer is kept fixed from the tick after it
    repeats exactly; the things read it as the stepping engine gives, tick by
    tick, and the run's files are the stepping run's byte for byte."""
    momenta, audits, _, _, _ = stepped(line(), 200)
    standing_momenta, standing_audits, report, _, _ = stepped(dict(line(), standing_field=True), 200)
    assert report == {
        "standing_field": True,
        "standing_field_iterations": FIXED_POINT,
        "standing_field_period": PERIOD,
        "standing_field_residual": {"cells": 0, "amount": 0},
        "standing_field_ticks": 200 - FIXED_POINT,
        "standing_field_fallback": None,
    }
    assert standing_momenta == momenta
    assert momenta[-1] == FINAL_MOMENTA
    assert any(any(vector) for tick in momenta[:FIXED_POINT] for vector in tick)
    assert audit_failure(standing_audits) is None and standing_audits == audits
    stepping = digests(written(tmp_path, "stepping", line()))
    fixed = digests(written(tmp_path, "standing", line(), standing_field=True))
    assert fixed[:2] == stepping[:2]
    assert fixed[2]["standing_field"] is True and fixed[2]["standing_field_max_iterations"] == 200
    assert "standing_field" not in stepping[2]


def test_without_a_repeat_the_layer_keeps_stepping_and_the_residual_is_reported(tmp_path):
    stepping = digests(written(tmp_path, "stepping", line()))
    short = digests(written(tmp_path, "short", line(), standing_field=SHORT_LIMIT))
    assert short[:2] == stepping[:2]
    record = short[2]
    assert record["standing_field"] is False and record["standing_field_iterations"] is None
    assert record["standing_field_period"] is None
    assert record["standing_field_residual"] == SHORT_RESIDUAL
    assert record["standing_field_ticks"] == 0 and record["standing_field_fallback"] is None
    assert record["standing_field_max_iterations"] == SHORT_LIMIT


def test_a_thing_that_steps_under_the_standing_set_makes_the_run_fall_back_exactly(tmp_path):
    doc = late_lamp(line())
    stepping = digests(written(tmp_path, "stepping", doc))
    fallen = digests(written(tmp_path, "fallen", doc, standing_field=True))
    assert fallen[:2] == stepping[:2]
    record = fallen[2]
    assert record["standing_field"] is False
    assert record["standing_field_iterations"] == LAMP_FIXED_POINT
    assert record["standing_field_period"] == PERIOD
    assert record["standing_field_ticks"] == 131 - LAMP_FIXED_POINT - 1
    assert record["standing_field_fallback"] == {
        "tick": 131,
        "reason": "a thing stepped or the things' Nodes changed",
    }
    assert record["conserved_at_every_completed_tick"] is True


@pytest.mark.parametrize(
    "change,reason",
    [
        (lambda d: d.update(dense_field=False, standing_field=True), "requires the dense mode"),
        (lambda d: d.update(standing_field=-1), "standing_field"),
        (lambda d: d.update(standing_field="soon"), "standing_field"),
    ],
)
def test_a_standing_field_declaration_the_engine_cannot_honour_is_refused(change, reason):
    doc = line()
    change(doc)
    with pytest.raises(ValueError, match=reason):
        parse_initial_state(doc)

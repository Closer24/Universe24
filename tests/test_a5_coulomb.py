"""Experiment A5, Coulomb's law through the spreading field (docs/EXPERIMENTS.md):
the worlds of examples/nature/a5_coulomb are the pinned geometry and byte for byte
what make_worlds.py writes; the smallest case re-run for its first eight ticks
gives the pinned ledger lines and positions; and the committed record of the
measured series (record.json, written by analyze.py from the fingerprinted runs)
holds the pinned integers of the criterion: dp(b) for b = 4 and 16, the momentum
sum, the first return, the self-meetings and the exponent.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A5 Coulomb") before the
first run.
"""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/a5_coulomb"
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
SPREAD = [6, 1, 1, 1, 1, 1]
NAMES = (
    "ee_b4",
    "ee_b6",
    "ee_b8",
    "ee_b12",
    "ee_b16",
    "ep_b4",
    "ep_b6",
    "ep_b8",
    "ep_b12",
    "ep_b16",
    "nn_b4",
    "ee_b4_nospread",
    "ee_b16_nospread",
)


def load_script(name):
    """A script of the example directory, loaded from its file (not a package)."""
    path = WORLDS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"a5_coulomb_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def world(name):
    return json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))


def test_a5_worlds_are_the_pinned_geometry_and_the_generator_writes_them():
    generated = dict(load_script("make_worlds").cases())
    assert list(generated) == list(NAMES)
    for name in NAMES:
        text = (WORLDS / f"{name}.json").read_text(encoding="utf-8")
        assert text == json.dumps(generated[name], indent=1) + "\n", name
    for name in NAMES:
        case, b = name.split("_")[0], int(name.split("_")[1][1:])
        raw = world(name)
        matter = ["neutral_a", "neutral_b"] if case == "nn" else ["electron_a", "electron_b"]
        charges = {"ee": (-3, -3), "ep": (-3, 3), "nn": (0, 0)}[case]
        spread = not name.endswith("nospread")
        assert (raw["shape"], raw["boundary"], raw["ticks"]) == (
            [97, 49, 49],
            "open",
            min(48 + 3 * b + 8, 96),
        ), name
        assert [
            (seed["position"], emission["heading"], emission["amount"], emission["field"])
            for seed, emission in zip(raw["seeds"], raw["emissions"], strict=True)
        ] == [
            ([0, 24 - b // 2, 24], [1, 0, 0], 64, matter[0]),
            ([96, 24 + b // 2, 24], [-1, 0, 0], 64, matter[1]),
        ], name
        assert [
            (
                f["field"],
                f["charge"],
                f["kerengonen"]["phase_advance"],
                f["phase_bits"],
                f["ray_slots"],
                f.get("field_of"),
                f.get("release"),
                f.get("spread"),
                f["headings"],
            )
            for f in raw["spatial_fields"]
        ] == [
            (matter[0], charges[0], 1, 12, 2, None, None, None, HEADINGS),
            (matter[1], charges[1], 1, 12, 2, None, None, None, HEADINGS),
            ("light_a", 0, 0, 12, 30, matter[0], [1, 4], SPREAD if spread else None, HEADINGS),
            ("light_b", 0, 0, 12, 30, matter[1], [1, 4], SPREAD if spread else None, HEADINGS),
        ], name
        rules = [
            (r["name"], [p["type"] for p in r["participants"]], r["momentum_table"])
            for r in raw["ray_interactions"]
        ]
        if case == "nn":
            assert rules == []
        else:
            sign = 1 if case == "ee" else -1
            assert rules == [
                ("electron_field_turn_a", ["electron_a", "light_b"], {"light_b": sign}),
                ("electron_field_turn_b", ["electron_b", "light_a"], {"light_a": sign}),
            ], name


def test_a5_smallest_case_first_eight_ticks(tmp_path):
    run_initialization(WORLDS / "ee_b4.json", tmp_path / "out", ticks=8)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "completed" and metadata["completed_ticks"] == 8
    assert metadata["field_spreading"] == "field-spreading-v1"
    assert metadata["field_remainder"] == "field-remainder-v1"
    assert "ray_momentum_turn" not in metadata
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["released_fields"] == [
        {"field": "light_a", "field_of": "electron_a", "release": [1, 4]},
        {"field": "light_b", "field_of": "electron_b", "release": [1, 4]},
    ]
    ledger = metadata["audit"][-1]
    assert ledger["tick"] == 8 and ledger["balanced"]
    for name in ("light_a", "light_b"):
        line = ledger["fields"][name]
        assert (line["sourced"], line["current"], line["escaped"]) == ([560], [540], [20]), name
    for name in ("electron_a", "electron_b"):
        line = ledger["fields"][name]
        assert (line["sourced"], line["current"], line["escaped"]) == ([0], [64], [0]), name
    momentum = ledger["fields"]["momentum"]
    assert (momentum["sourced"], momentum["current"], momentum["escaped"]) == (
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    )
    positions = {}
    pushes = 0
    for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "ray_push":
            pushes += 1
        if event["event"] == "spatial_received" and event["tick"] == 8:
            for packet in event["received_fields"]:
                for family, values in packet.items():
                    if family.startswith("electron") and values and values[0]:
                        positions[family] = event["position"]
    assert pushes == 0
    assert positions == {"electron_a": [8, 22, 24], "electron_b": [88, 26, 24]}


def test_a5_record_pins_the_measured_integers():
    analyze = load_script("analyze")
    record = json.loads((WORLDS / "record.json").read_text(encoding="utf-8"))
    runs = {run["model"]: run for run in record["runs"]}
    assert set(runs) == {f"a5-coulomb-{name.replace('_b', '-b').replace('_', '-')}" for name in NAMES}
    for name in NAMES:
        run = runs[f"a5-coulomb-{name.replace('_b', '-b').replace('_', '-')}"]
        assert run["status"] == "completed", name
        assert run["source_sha256"] == "4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb"
        digest = hashlib.sha256((WORLDS / f"{name}.json").read_bytes()).hexdigest()
        assert run["initialization_sha256"] == digest, name
        assert run["conserved_at_every_completed_tick"], name
        assert run["rays_sum_max_abs"] == 0, name
        assert run["ledger_sourced_final"] == [0, 0, 0], name
    zero = {"electron_a": [0, 0, 0], "electron_b": [0, 0, 0]}
    for case, sign in (("ee", -1), ("ep", 1)):
        run = runs[f"a5-coulomb-{case}-b4"]
        expected = {"electron_a": [0, sign * 3, 0], "electron_b": [0, -sign * 3, 0]}
        assert run["dp"] == expected and run["dp_final"] == expected, case
        assert (run["read_off_used"], run["ticks"]) == (60, 68)
        assert run["pushes"] == 4 and run["pushes_by"] == {"electron_a": 2, "electron_b": 2}
        assert [
            (p["tick"], p["position"], p["family"], p["field"], p["field_amount"], p["field_heading"])
            for p in run["pushes_list"]
        ] == [
            (50, [46, 26, 24], "electron_b", "light_a", 2, [0, 1, 0]),
            (50, [50, 22, 24], "electron_a", "light_b", 2, [0, -1, 0]),
            (53, [43, 26, 24], "electron_b", "light_a", 1, [0, 1, 0]),
            (53, [53, 22, 24], "electron_a", "light_b", 1, [0, -1, 0]),
        ]
        assert run["first_return"] == {"electron_a": 65, "electron_b": 65}
        assert run["self_meetings"] == 6
        for b in (6, 8, 12, 16):
            far = runs[f"a5-coulomb-{case}-b{b}"]
            assert far["dp"] == zero and far["dp_final"] == zero, (case, b)
            assert far["pushes"] == 0 and far["self_meetings"] == 0, (case, b)
            assert far["first_return"] == {"electron_a": None, "electron_b": None}, (case, b)
    control = runs["a5-coulomb-nn-b4"]
    assert control["dp_final"] == {"neutral_a": [0, 0, 0], "neutral_b": [0, 0, 0]}
    assert control["pushes"] == 0 and control["self_meetings"] == 0
    assert control["straight"] == {"neutral_a": True, "neutral_b": True}
    for b, tick, meetings in ((4, 50, 8), (16, 56, 16)):
        flat = runs[f"a5-coulomb-ee-b{b}-nospread"]
        assert flat["dp_final"] == {"electron_a": [0, -16, 0], "electron_b": [0, 16, 0]}
        assert flat["pushes"] == 2 and flat["first_push"] == tick
        assert flat["self_meetings"] == meetings
    points = [(b, abs(runs[f"a5-coulomb-ee-b{b}"]["dp"]["electron_a"][1])) for b in (4, 6, 8, 12, 16)]
    assert points == [(4, 3), (6, 0), (8, 0), (12, 0), (16, 0)]
    fit = analyze.fit(points)
    assert fit["exponent"] is None and fit["zeros"] == 4
    assert [(entry["clause"].split(" ")[0], entry["pass"]) for entry in record["clauses"]] == [
        ("momentum", True),
        ("dp", True),
        ("first", False),
        ("log-log", False),
        ("like", False),
        ("neutral", True),
        ("no", False),
    ]

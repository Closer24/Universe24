"""Experiment A5s, Coulomb's force law between two charges at rest
(docs/EXPERIMENTS.md): the worlds of examples/nature/a5_static are the pinned
geometry and byte for byte what make_worlds.py writes; the r = 4 like-charge world
re-run for its first eight ticks gives the pinned registers and ledger; the
committed record of the measured series (record.json, written by analyze.py from
the fingerprinted runs) is pinned once the run is made.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A5s Coulomb at rest")
before the first pinning run.
"""

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/a5_static"
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
SPREAD = [6, 1, 1, 1, 1, 1]
AMOUNT = 1 << 28
RELEASE = [1, 65536]
NAMES = (
    "pp_r4",
    "pp_r6",
    "pp_r8",
    "pp_r12",
    "pp_r16",
    "pe_r4",
    "pe_r6",
    "pe_r8",
    "pe_r12",
    "pe_r16",
    "pp_d3",
    "pp_d4",
    "pp_d6",
    "pp_d8",
    "p_alone",
)


def load_script(name):
    """A script of the example directory, loaded from its file (not a package)."""
    path = WORLDS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"a5_static_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def world(name):
    return json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))


def model_of(name):
    return "a5-static-" + name.replace("_", "-")


def test_a5s_worlds_are_the_pinned_geometry_and_the_generator_writes_them():
    generated = dict(load_script("make_worlds").cases())
    assert list(generated) == list(NAMES)
    for name in NAMES:
        text = (WORLDS / f"{name}.json").read_text(encoding="utf-8")
        assert text == json.dumps(generated[name], indent=1) + "\n", name
    for name in NAMES:
        raw = world(name)
        case, tail = name.split("_")
        if case == "p":
            offset, ticks, shape = (0, 0, 0), 64, [11, 11, 11]
        elif tail.startswith("r"):
            r = int(tail[1:])
            offset, ticks, shape = (r, 0, 0), 2 * r + 32, [r + 11, 11, 11]
        else:
            d = int(tail[1:])
            offset, ticks, shape = (d, d, 0), 4 * d + 32, [d + 11, d + 11, 11]
        assert (raw["shape"], raw["boundary"], raw["ticks"]) == (shape, "open", ticks), name
        assert raw["seeds"] == [] and raw["ray_interactions"] == [], name
        family_b = {"pp": "proton_b", "pe": "electron_b", "p": None}[case]
        charge_b = {"pp": 3, "pe": -3, "p": None}[case]
        sign = -1 if case == "pe" else 1
        bodies = [
            (b["position"], b["family"], b["charge"], b["amount"], b["momentum_table"])
            for b in raw["external_bodies"]
        ]
        if case == "p":
            assert bodies == [([5, 5, 5], "proton_a", 3, AMOUNT, {"light_a": 1})], name
            matter = ["proton_a"]
            lights = ["light_a"]
        else:
            assert bodies == [
                ([5, 5, 5], "proton_a", 3, AMOUNT, {"light_b": sign}),
                ([5 + offset[0], 5 + offset[1], 5], family_b, charge_b, AMOUNT, {"light_a": sign}),
            ], name
            matter = ["proton_a", family_b]
            lights = ["light_a", "light_b"]
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
        ] == (
            [
                (m, 3 if m.startswith("proton") else -3, 0, 3, 2, None, None, None, HEADINGS)
                for m in matter
            ]
            + [
                (light, 0, 0, 3, 8, m, RELEASE, SPREAD, HEADINGS)
                for light, m in zip(lights, matter, strict=True)
            ]
        ), name
        assert [f["name"] for f in raw["fields"]] == matter + lights + ["momentum"], name
        assert [(t["name"], t["fields"]) for t in raw["disturbance_types"]] == [
            (f"idle_{light}", [light, "momentum"]) for light in lights
        ], name
        assert [
            (e["type"], e["field"], e["amount"], e["heading"], e["recoil_field"])
            for e in raw["emissions"]
        ] == [(f"idle_{light}", light, 1, [1, 0, 0], "momentum") for light in lights], name


def test_a5s_r4_like_charges_first_eight_ticks(tmp_path):
    run_initialization(WORLDS / "pp_r4.json", tmp_path / "out", ticks=8)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "completed" and metadata["completed_ticks"] == 8
    assert metadata["field_spreading"] == "field-spreading-v1"
    assert metadata["field_remainder"] == "field-remainder-v1"
    assert metadata["external_body"] == "external-body-v1"
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["released_fields"] == [
        {"field": "light_a", "field_of": "proton_a", "release": RELEASE},
        {"field": "light_b", "field_of": "proton_b", "release": RELEASE},
    ]
    for body, position in zip(metadata["external_bodies"], ([5, 5, 5], [9, 5, 5]), strict=True):
        assert body["positions"] == [[tick, *position] for tick in range(9)]
    ledger = metadata["audit"][-1]
    assert ledger["tick"] == 8 and ledger["balanced"]
    assert all(entry["balanced"] for entry in metadata["audit"])
    for name in ("light_a", "light_b"):
        assert ledger["fields"][name]["sourced"] == [6 * 4096 * 8], name
    momentum = ledger["fields"]["momentum"]
    assert [momentum[key] for key in ("sourced", "current", "escaped", "absorbed")] == [[0, 0, 0]] * 4
    assert ledger["bodies"]["momentum"] == [0, 0, 0]
    registers = {0: {}, 1: {}}
    steps = 0
    for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "external_body_step":
            steps += 1
        if event["event"] == "external_body_absorbed":
            registers[event["body"]][event["tick"]] = event["momentum"]
    assert steps == 0
    expected = [0, 0, 0, 664, 1329, 2028, 2727, 3444]
    series = {0: [], 1: []}
    for index in (0, 1):
        current = [0, 0, 0]
        for tick in range(1, 9):
            current = registers[index].get(tick, current)
            series[index].append(current)
    assert series[1] == [[value, 0, 0] for value in expected]
    assert series[0] == [[-value, 0, 0] for value in expected]

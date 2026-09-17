"""Experiment A5s, Coulomb's force law between two charges at rest
(docs/EXPERIMENTS.md): the worlds of examples/nature/a5_static are the pinned
geometry and byte for byte what make_worlds.py writes; the r = 4 like-charge world
re-run for its first eight ticks gives the pinned registers and ledger; and the
committed record of the measured series (record.json, written by analyze.py from
the fingerprinted runs) holds the pinned integers of the criterion.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A5s Coulomb at rest"):
the first two tests before the first pinning run, the third from the record of the
runs of 2026-09-17.
"""

import hashlib
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
AXIS = (4, 6, 8, 12, 16)
DIAGONAL = (3, 4, 6, 8)

# Written from record.json after the runs of 2026-09-17 (the register's entry
# states them): the sum of B's pushes over the last 32 ticks (F(r) is its 32nd
# part), B's register at the end, the tick of the first push, the log-log
# exponent of F over r with its standard error, and the pushes on B per tick of
# the r = 4 like-charge world.
MEASURED_SUMS = {4: [23770, 0, 0], 6: [8090, 0, 0], 8: [2872, 0, 0], 12: [422, 0, 0], 16: [77, 0, 0]}
MEASURED_FINAL = {4: 27214, 6: 9608, 8: 3501, 12: 522, 16: 91}
MEASURED_FIRST_PUSH = {4: 4, 6: 6, 8: 8, 12: 12, 16: 18}
MEASURED_EXPONENT = -4.142
MEASURED_ERROR = 0.369
MEASURED_EXPONENT_PASS = False
MEASURED_DIAGONAL_SUMS = {3: [3019, 3019, 0], 4: [1509, 1509, 0], 6: [447, 447, 0], 8: [158, 158, 0]}
MEASURED_DIAGONAL_FINAL = {3: 3461, 4: 1756, 6: 524, 8: 182}
MEASURED_DIAGONAL_FIRST_PUSH = {3: 6, 4: 8, 6: 12, 8: 19}
MEASURED_CONTROL_ABSORPTIONS = 378
MEASURED_R4_PUSHES = [
    0, 0, 0, 664, 665, 699, 699, 717, 717, 725, 727, 732, 732, 736, 737, 739, 741, 742, 742, 743,
    744, 746, 744, 746, 747, 748, 747, 748, 747, 749, 749, 747, 750, 748, 750, 749, 750, 750, 748, 750,
]  # fmt: skip


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


def test_a5s_record_pins_the_measured_integers():
    analyze = load_script("analyze")
    record = json.loads((WORLDS / "record.json").read_text(encoding="utf-8"))
    runs = {run["model"]: run for run in record["runs"]}
    assert set(runs) == {model_of(name) for name in NAMES}
    for name in NAMES:
        run = runs[model_of(name)]
        assert run["status"] == "completed" and run["error"] is None, name
        assert run["source_sha256"] == record["runs"][0]["source_sha256"], name
        digest = hashlib.sha256((WORLDS / f"{name}.json").read_bytes()).hexdigest()
        assert run["initialization_sha256"] == digest, name
        assert run["ticks"] == world(name)["ticks"], name
        assert run["all_balanced"] and run["conserved_at_every_completed_tick"], name
        assert run["positions_fixed"], name
        assert run["bodies_momentum_zero"] and run["momentum_line_zero"], name
        assert run["steady"]["0"]["window"] == 32, name
        if name == "p_alone":
            assert run["control_zero"] and run["final_registers"] == [[0, 0, 0]]
            assert run["absorptions"] == {"0": MEASURED_CONTROL_ABSORPTIONS}
            assert run["first_push"] == {"0": None}
        else:
            assert run["equal_opposite"], name
            assert run["final_registers"][0] == [-c for c in run["final_registers"][1]], name
    # The like-charge series is the exact negation of the opposite-charge series.
    for r in AXIS:
        pp, pe = runs[model_of(f"pp_r{r}")], runs[model_of(f"pe_r{r}")]
        assert pe["register_series"] == {
            k: [[-c for c in v] for v in series] for k, series in pp["register_series"].items()
        }, r
        assert pe["steady"]["1"]["sum"] == [-c for c in pp["steady"]["1"]["sum"]], r
    # The measured integers of the axis series: the sum of B's pushes over the last
    # 32 ticks per r (F(r) is its 32nd part), B's register at the end, the first
    # push, and the exponent of the fit with its standard error.
    assert {r: runs[model_of(f"pp_r{r}")]["steady"]["1"]["sum"] for r in AXIS} == MEASURED_SUMS
    assert {r: runs[model_of(f"pp_r{r}")]["final_registers"][1][0] for r in AXIS} == MEASURED_FINAL
    assert {r: runs[model_of(f"pp_r{r}")]["first_push"]["1"] for r in AXIS} == MEASURED_FIRST_PUSH
    points = [(r, MEASURED_SUMS[r][0] / 32) for r in AXIS]
    fit = analyze.fit(points)
    assert round(fit["exponent"], 3) == MEASURED_EXPONENT
    assert round(fit["standard_error"], 3) == MEASURED_ERROR
    assert (analyze.BAND[0] <= fit["exponent"] <= analyze.BAND[1]) is MEASURED_EXPONENT_PASS
    r4 = runs[model_of("pp_r4")]["register_series"]["1"]
    pushes = [r4[0][0]] + [r4[t][0] - r4[t - 1][0] for t in range(1, len(r4))]
    assert pushes == MEASURED_R4_PUSHES
    # The diagonal series: along the diagonal exactly, its integers pinned.
    for d in DIAGONAL:
        run = runs[model_of(f"pp_d{d}")]
        total = run["steady"]["1"]["sum"]
        assert total[0] == total[1] and total[2] == 0, d
        assert total == MEASURED_DIAGONAL_SUMS[d], d
        assert run["final_registers"][1] == [MEASURED_DIAGONAL_FINAL[d]] * 2 + [0], d
        assert run["first_push"]["1"] == MEASURED_DIAGONAL_FIRST_PUSH[d], d
    # The clause table's verdicts, in the criterion's order.
    assert [(entry["clause"].split(" ")[0], entry["pass"]) for entry in record["clauses"]] == [
        ("ledger", True),
        ("control", True),
        ("registers", True),
        ("log-log", MEASURED_EXPONENT_PASS),
        ("like", True),
        ("diagonal", None),
    ]
    fits = record["clauses"][3]["numbers"]
    for case in ("pp", "pe"):
        assert fits[case]["series"] == [[r, MEASURED_SUMS[r][0] / 32] for r in AXIS], case
        assert round(fits[case]["exponent"], 3) == MEASURED_EXPONENT, case

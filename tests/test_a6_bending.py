"""Experiment A6, light bending by a mass (docs/EXPERIMENTS.md): the worlds of
examples/nature/a6_bending are the pinned geometry and byte for byte what
make_worlds.py writes; the small world of each form re-run for 40 ticks gives the
pinned register (the turn form: the first push and the register per tick) and the
pinned lag (the delay form: one meeting per Node, the lag on the ray's own axis
alone, reset at every meeting, no heading change); the mean field's predictions
written before the run are the pinned numbers; and the committed record of the
measured series (record.json, written by analyze.py from the fingerprinted runs)
holds the pinned integers of the criterion.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A6 light bending"):
the first three tests before the series, the fourth from the record of the runs
of 2026-09-18.
"""

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/a6_bending"
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
SPREAD = [6, 1, 1, 1, 1, 1]
LIGHT = 1 << 18
AMOUNT = 1 << 28
RELEASE = [1, 1 << 15]
TABLE = [1, 1, 1, 1, 1, 1]
LAUNCH_DELAY = 192
TICKS = 260
FORMS = ("turn", "delay")
CASES = (
    "b4",
    "b6",
    "b8",
    "b12",
    "b16",
    "control",
    "2m",
    "slow",
    "n8",
    "n10",
    "n14",
    "n16",
    "m4",
    "m6",
    "m8",
    "m12",
    "m16",
    "c_b4",
    "c_b6",
    "c_b8",
    "c_d3",
    "c_d4",
    "c_d6",
)
AXIS_B = (4, 6, 8, 12, 16)
SCAN_BITS = (8, 10, 14, 16)
# The measured series (record.json, 2026-09-18, engine of main 9cc830f): the light's
# register (p_x, p_y, p_z) at the end of its pass per form and case, the delay form
# unchanged in every world and the turn form the sum of its pushes.
MEASURED_REGISTER = {
    ("turn", "2m"): (262144, -1727, 0),
    ("turn", "b12"): (262144, -269, 0),
    ("turn", "b16"): (262144, -93, 0),
    ("turn", "b4"): (262144, -3423, 0),
    ("turn", "b6"): (262144, -1661, 0),
    ("turn", "b8"): (262144, -862, 0),
    ("turn", "c_b4"): (262144, -3697, 0),
    ("turn", "c_b6"): (262144, -2019, 0),
    ("turn", "c_b8"): (262144, -1246, 0),
    ("turn", "c_d3"): (262144, -1169, -1169),
    ("turn", "c_d4"): (262144, -900, -900),
    ("turn", "c_d6"): (262144, -578, -578),
    ("turn", "control"): (262144, 0, 0),
    ("turn", "m12"): (262144, 269, 0),
    ("turn", "m16"): (262144, 93, 0),
    ("turn", "m4"): (262144, 3423, 0),
    ("turn", "m6"): (262144, 1661, 0),
    ("turn", "m8"): (262144, 862, 0),
    ("turn", "n10"): (262144, -862, 0),
    ("turn", "n14"): (262144, -862, 0),
    ("turn", "n16"): (262144, -862, 0),
    ("turn", "n8"): (262144, -862, 0),
    ("turn", "slow"): (262144, -862, 0),
}
MEASURED_REGISTER.update({("delay", case): (LIGHT, 0, 0) for case in CASES})
# Pushes recorded per world (ray_push events on the light): none in the delay form.
MEASURED_PUSHES = {
    "turn": {
        "2m": 304,
        "b12": 248,
        "b16": 214,
        "b4": 295,
        "b6": 281,
        "b8": 274,
        "c_b4": 286,
        "c_b6": 286,
        "c_b8": 284,
        "c_d3": 286,
        "c_d4": 286,
        "c_d6": 286,
        "control": 0,
        "m12": 248,
        "m16": 214,
        "m4": 295,
        "m6": 281,
        "m8": 274,
        "n10": 274,
        "n14": 274,
        "n16": 274,
        "n8": 274,
        "slow": 274,
    },
    "delay": {case: 0 for case in CASES},
}
# The star's final momentum register (the bodies' momentum line), None without a star.
MEASURED_STAR = {
    "turn": {
        "2m": [0, 8, 0],
        "b12": [0, 0, 0],
        "b16": [0, 0, 0],
        "b4": [0, 222, 0],
        "b6": [0, 26, 0],
        "b8": [0, 4, 0],
        "c_b4": [0, 222, 0],
        "c_b6": [0, 27, 0],
        "c_b8": [0, 4, 0],
        "c_d3": [0, 4, 4],
        "c_d4": [0, 2, 2],
        "c_d6": [0, 1, 1],
        "control": None,
        "m12": [0, 0, 0],
        "m16": [0, 0, 0],
        "m4": [0, -222, 0],
        "m6": [0, -26, 0],
        "m8": [0, -4, 0],
        "n10": [0, 4, 0],
        "n14": [0, 4, 0],
        "n16": [0, 4, 0],
        "n8": [0, 4, 0],
        "slow": [0, 4, 0],
    },
    "delay": {
        "2m": [0, 0, 0],
        "b12": [0, 0, 0],
        "b16": [0, 0, 0],
        "b4": [-1, 2, 0],
        "b6": [-1, 0, 0],
        "b8": [-1, 0, 0],
        "c_b4": [-2, 2, 0],
        "c_b6": [-1, 0, 0],
        "c_b8": [0, 0, 0],
        "c_d3": [-1, 0, 0],
        "c_d4": [-1, 0, 0],
        "c_d6": [0, 0, 0],
        "control": None,
        "m12": [0, 0, 0],
        "m16": [0, 0, 0],
        "m4": [-1, -2, 0],
        "m6": [-1, 0, 0],
        "m8": [-1, 0, 0],
        "n10": [-1, 0, 0],
        "n14": [-1, 0, 0],
        "n16": [-1, 0, 0],
        "n8": [-1, 0, 0],
        "slow": [-1, 0, 0],
    },
}
MEASURED_EXPONENT, MEASURED_ERROR = (
    -2.595,
    0.21,
)  # the axis fit, alpha over b = 4..16 (mean field -2.586 +- 0.207)
MEASURED_LINEARITY = 2.0035  # alpha(2M) / alpha(M) at b = 8
MEASURED_DIAGONAL_RATIO = {"c_d3": 0.4862, "c_d4": 0.5869, "c_d6": 0.7107}  # over the cube's axis fit
MEASURED_CUBE_EXPONENT = -1.564
MEASURED_MEAN_FIELD_DEVIATION = (
    0.014  # the largest |push / mean field - 1| over the turn series (b = 16)
)
TURN_VERDICTS = [True, True, True, False, True, False, False, None, None]
DELAY_VERDICTS = [True, True, False, False, False, False, False, None, None]
CUBE_AXIS_B = (4, 6, 8)
CUBE_DIAGONAL_D = (3, 4, 6)
# The small world of each form (25 x 25 x 9, the star at (12, 12, 4), b = 4, the
# launch after 10 intervals, 40 ticks), pinned before the series: the light waits
# at the launcher (0, 16, 4) from tick 2 to 11 and is at x = t - 11 from tick 12;
# the turn form's register after the pushes of ticks 15 to 35 and the delay form's
# lag at the same ticks (on the ray's own axis alone, reset at every meeting).
SMALL_REGISTER = {
    15: (262147, -2, 0),
    16: (262153, -9, 0),
    17: (262164, -22, 0),
    18: (262179, -48, 0),
    19: (262203, -93, 0),
    20: (262236, -166, 0),
    21: (262280, -289, 0),
    22: (262332, -485, 0),
    23: (262392, -791, 0),
    24: (262264, -2189, 0),
    25: (262230, -2499, 0),
    26: (262204, -2700, 0),
    27: (262187, -2832, 0),
    28: (262174, -2917, 0),
    29: (262164, -2973, 0),
    30: (262158, -3009, 0),
    31: (262154, -3033, 0),
    32: (262150, -3049, 0),
    33: (262148, -3059, 0),
    34: (262147, -3065, 0),
    35: (262146, -3069, 0),
}
SMALL_LAG = {
    15: (3, 0, 0),
    16: (-3, 0, 0),
    17: (-2, 0, 0),
    18: (-4, 0, 0),
    19: (-7, 0, 0),
    20: (-13, 0, 0),
    21: (-21, 0, 0),
    22: (-35, 0, 0),
    23: (-52, 0, 0),
    24: (-75, 0, 0),
    25: (-188, 0, 0),
    26: (-63, 0, 0),
    27: (-45, 0, 0),
    28: (-31, 0, 0),
    29: (-22, 0, 0),
    30: (-15, 0, 0),
    31: (-10, 0, 0),
    32: (-7, 0, 0),
    33: (-5, 0, 0),
    34: (-3, 0, 0),
    35: (-2, 0, 0),
}
SMALL_TURN = {
    "pushes": 124,
    "first_push": (14, (3, 16, 4), (262144, 0, 0), (262147, 0, 0), 3, (-1, 0, 0)),
    "escape": (36, (24, 16, 4), (262144, -3072, 0)),
    "star": ([0, 219, 0], [-24, 2831, 0], 291901),
    "launcher_sink": 211,
}
SMALL_DELAY = {
    "escape": (36, (24, 16, 4), (262145, 0, 0)),
    "star": ([-1, 2, 0], [-11, 9, 0], 291649),
    "launcher_sink": 216,
}


def load_script(name):
    """A script of the example directory, loaded from its file (not a package)."""
    path = WORLDS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"a6_bending_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def world(name):
    return json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))


def model_of(name):
    return "a6-bending-" + name.replace("_", "-")


def expected_geometry(case):
    """(shape, star, offset, bits, amount, ray, star present) of a case."""
    shape, star = [65, 65, 9], [32, 32, 4]
    offset, bits, amount, ray, present = (0, 8, 0), 12, AMOUNT, "light", True
    if case.startswith("c_"):
        shape, star = [49, 33, 33], [24, 16, 16]
        value = int(case[3:])
        offset = (0, value, 0) if case[2] == "b" else (0, value, value)
    elif case.startswith("b"):
        offset = (0, int(case[1:]), 0)
    elif case.startswith("m"):
        offset = (0, -int(case[1:]), 0)
    elif case.startswith("n"):
        bits = int(case[1:])
    elif case == "control":
        present = False
    elif case == "2m":
        amount = 2 * AMOUNT
    elif case == "slow":
        ray = "electron"
    return shape, star, offset, bits, amount, ray, present


def test_a6_worlds_are_the_pinned_geometry_and_the_generator_writes_them():
    make_worlds = load_script("make_worlds")
    generated = dict(make_worlds.all_cases())
    assert list(generated) == [f"{form}_{case}" for form in FORMS for case in CASES]
    for name, document in generated.items():
        text = (WORLDS / f"{name}.json").read_text(encoding="utf-8")
        assert text == json.dumps(document, indent=1) + "\n", name
    for form in FORMS:
        for case in CASES:
            raw = world(f"{form}_{case}")
            shape, star, offset, bits, amount, ray, present = expected_geometry(case)
            line = [0, star[1] + offset[1], star[2] + offset[2]]
            assert raw["model_id"] == model_of(f"{form}_{case}")
            assert (raw["shape"], raw["boundary"], raw["ticks"], raw["dense_field"]) == (
                shape,
                "open",
                TICKS,
                True,
            ), case
            assert "conservation" not in raw and "polarization" not in raw
            bodies = [
                (b["position"], b["family"], b["amount"], b.get("momentum_table"), b.get("coupling"))
                for b in raw["external_bodies"]
            ]
            expected = [(line, "launcher", 1, None, "launch")]
            if present:
                expected.insert(0, (star, "neutron", amount, {"mass_field": -1}, None))
            assert bodies == expected, case
            assert raw["seeds"] == [{"position": [0, line[1] - 1, line[2]], "type": "lamp"}], case
            families = {f["field"]: f for f in raw["spatial_fields"]}
            assert families["mass_field"]["field_of"] == "neutron"
            assert (
                families["mass_field"]["release"] == RELEASE
                and families["mass_field"]["spread"] == SPREAD
            )
            assert families["mass_field"]["phase_bits"] == 3 and families["neutron"]["phase_bits"] == 3
            assert families[ray]["phase_bits"] == bits and "spread" not in families[ray], case
            assert families["light"]["kerengonen"]["phase_advance"] == 0
            if ray == "electron":
                assert families["electron"]["kerengonen"]["phase_advance"] == 1
                assert families["electron"]["charge"] == -3
            assert all(f["headings"] == HEADINGS for f in raw["spatial_fields"])
            launch, gravity = raw["ray_interactions"]
            assert launch["name"] == "launch" and launch["participants"] == [
                {"type": ray},
                {"type": "launcher"},
            ]
            assert launch["outputs"][0] == {
                "field": ray,
                "amount": {"of": 0},
                "heading": 0,
                "phase": "same",
                "delay": LAUNCH_DELAY,
                "input": 0,
            }
            assert gravity["participants"] == [{"type": ray}, {"type": "mass_field"}]
            if form == "delay":
                assert gravity["name"] == "mass_field_delay"
                assert gravity["outputs"][0]["delay"] == {"of": 1, "table": TABLE, "per": 1}
                assert (
                    gravity["outputs"][0]["heading"] == "same"
                    and gravity["outputs"][0]["phase"] == "same"
                )
                assert gravity["outputs"][1] == {
                    "field": "mass_field",
                    "amount": {"of": 1},
                    "heading": "reversed",
                    "input": 1,
                }
            else:
                assert gravity["name"] == "mass_field_turn" and gravity["momentum_table"] == {
                    "mass_field": -1
                }
                assert "outputs" not in gravity
            emission = raw["emissions"][0]
            assert (
                emission["type"],
                emission["field"],
                emission["amount"],
                emission["heading"],
                emission["recoil_field"],
            ) == ("lamp", ray, LIGHT, [0, 1, 0], "momentum")
            assert (
                raw["emissions"][1]["type"] == "idle_mass_field"
                and raw["emissions"][1]["recoil_field"] == "momentum"
            )


def light_at(world_, index):
    found = []
    for node in world_.inventory_view().nodes:
        if node.rays and node.rays[index]:
            found.extend((node.position, ray) for ray in node.rays[index])
    return found


def test_a6_small_worlds_pin_the_register_and_the_lag():
    make_worlds = load_script("make_worlds")
    for form in FORMS:
        events = []
        initial = parse_initial_state(make_worlds.small_world(form))
        world_ = Simulation(initial, observer=events.append)
        index = [f.field for f in world_.initial.spatial_fields].index(
            [f.name for f in world_.initial.fields].index("light")
        )
        for tick in range(1, 41):
            world_.step()
            rays = light_at(world_, index)
            if tick == 1:
                assert [(p, r.heading, r.steps) for p, r in rays] == [((0, 16, 4), 2, 1)]
            elif tick <= 11:
                # Waiting at the launcher, its heading already +X (the launch's output).
                assert [(p, r.heading, r.steps) for p, r in rays] == [((0, 16, 4), 0, 0)]
            elif tick <= 35:
                assert len(rays) == 1
                position, ray = rays[0]
                assert position == (tick - 11, 16, 4) and ray.heading == 0 and ray.amount == LIGHT
                if form == "turn":
                    assert ray.lag == (0, 0, 0)
                    assert ray.momentum == SMALL_REGISTER.get(tick), (form, tick)
                    assert ray.steps == tick - 11
                else:
                    assert ray.momentum is None
                    assert ray.lag == SMALL_LAG.get(tick, (0, 0, 0)), (form, tick)
                    # A meeting at every Node from tick 15: a fresh event, steps 1.
                    assert ray.steps == (1 if tick >= 15 else tick - 11)
            else:
                assert rays == []
        pushes = [e for e in events if e["event"] == "ray_push"]
        escapes = [e for e in events if e["event"] == "spatial_escaped" and "light" in e["escaped"]]
        assert len(escapes) == 1
        escape = escapes[0]
        bodies = world_.external_bodies()
        assert all(item["balanced"] for item in world_.spatial_accounting().values())
        assert world_.escaped_totals()["light"] == (LIGHT,) and world_.totals()["light"] == (0,)
        if form == "turn":
            assert len(pushes) == SMALL_TURN["pushes"]
            first = pushes[0]
            assert (
                first["tick"],
                tuple(first["position"]),
                tuple(first["before"]),
                tuple(first["after"]),
                first["field_amount"],
                tuple(first["field_heading"]),
            ) == SMALL_TURN["first_push"]
            assert (
                escape["tick"],
                tuple(escape["position"]),
                tuple(escape["escaped"]["momentum"]),
            ) == SMALL_TURN["escape"]
            assert (
                bodies[0]["momentum"],
                bodies[0]["accumulators"],
                bodies[0]["sink"]["mass_field"],
            ) == SMALL_TURN["star"]
            assert bodies[1]["sink"]["mass_field"] == SMALL_TURN["launcher_sink"]
        else:
            assert pushes == []
            assert (
                escape["tick"],
                tuple(escape["position"]),
                tuple(escape["escaped"]["momentum"]),
            ) == SMALL_DELAY["escape"]
            assert (
                bodies[0]["momentum"],
                bodies[0]["accumulators"],
                bodies[0]["sink"]["mass_field"],
            ) == SMALL_DELAY["star"]
            assert bodies[1]["sink"]["mass_field"] == SMALL_DELAY["launcher_sink"]
        assert bodies[0]["position"] == [12, 12, 4] and bodies[1]["position"] == [0, 16, 4]


# The mean field's numbers of predictions.json, pinned before the series (seven
# decimals of alpha, three of an exponent, four of a ratio): the transverse push
# on the light over its pass and alpha per case, the beam 8192 (6/11)^(b-1), the
# fits, the diagonal against the cube's axis fit, the steady pass on deeper boards
# and in free space.
PREDICTED_PUSH = {"b4": -3417.70, "b6": -1660.36, "b8": -862.41, "b12": -269.84, "b16": -94.32}
PREDICTED_ALPHA = {
    "b4": 0.0130367,
    "b6": 0.0063337,
    "b8": 0.0032898,
    "b12": 0.0010294,
    "b16": 0.0003598,
    "m4": 0.0130367,
    "m6": 0.0063337,
    "m8": 0.0032898,
    "m12": 0.0010294,
    "m16": 0.0003598,
    "c_b4": 0.0141011,
    "c_b6": 0.0076985,
    "c_b8": 0.0047585,
    "c_d3": 0.0063323,
    "c_d4": 0.0048648,
    "c_d6": 0.0031079,
    "2m": 0.0065796,
    "n8": 0.0032898,
    "n10": 0.0032898,
    "n14": 0.0032898,
    "n16": 0.0032898,
    "slow": 0.0032898,
    "control": 0.0,
}
PREDICTED_STEADY_ALPHA = {
    "b4": 0.0130369,
    "b6": 0.0063340,
    "b8": 0.0032902,
    "b12": 0.0010298,
    "b16": 0.0003603,
}
PREDICTED_BEAM = {"b4": 1329.4, "b6": 395.5, "b8": 117.7, "b12": 10.4, "b16": 0.9}
PREDICTED_AXIS_EXPONENT = (-2.586, 0.207)
PREDICTED_CUBE_EXPONENT = (-1.562, 0.050)
PREDICTED_DIAGONAL_RATIO = {"c_d3": 0.4883, "c_d4": 0.5880, "c_d6": 0.7077}
PREDICTED_DEPTH_EXPONENT = {"9": -2.585, "17": -1.951, "33": -1.587}
PREDICTED_FREE_ALPHA = {"4": 0.0142978, "8": 0.0052398, "16": 0.0021331, "32": 0.0009809}
PREDICTED_FREE_EXPONENT = {"4-16": -1.384, "8-32": -1.198}


def test_a6_predictions_are_the_mean_fields_and_the_b4_row_recomputes():
    predictions = json.loads((WORLDS / "predictions.json").read_text(encoding="utf-8"))
    assert (
        predictions["release_per_heading"],
        predictions["light"],
        predictions["launch_delay"],
        predictions["ticks"],
    ) == (8192, LIGHT, LAUNCH_DELAY, TICKS)
    cases = predictions["cases"]
    assert set(cases) == set(CASES)
    for case, alpha in PREDICTED_ALPHA.items():
        assert round(cases[case]["alpha"], 7) == alpha, case
        register = cases[case]["register"]
        assert math.isclose(
            math.atan2(math.hypot(register[1], register[2]), register[0]), cases[case]["alpha"]
        )
    for case, push in PREDICTED_PUSH.items():
        assert round(cases[case]["push"][1], 2) == push and abs(cases[case]["push"][0]) < 1e-6, case
        assert round(cases[case]["steady_alpha"], 7) == PREDICTED_STEADY_ALPHA[case], case
        assert round(cases[case]["beam"], 1) == PREDICTED_BEAM[case], case
        assert round(cases[f"m{case[1:]}"]["push"][1], 2) == -push, case
    for d in CUBE_DIAGONAL_D:
        push = cases[f"c_d{d}"]["push"]
        assert math.isclose(push[1], push[2]) and abs(push[0]) < 1e-6, d
    assert (
        round(predictions["axis_fit"]["exponent"], 3),
        round(predictions["axis_fit"]["error"], 3),
    ) == PREDICTED_AXIS_EXPONENT
    assert (
        round(predictions["cube_axis_fit"]["exponent"], 3),
        round(predictions["cube_axis_fit"]["error"], 3),
    ) == PREDICTED_CUBE_EXPONENT
    assert {
        k: round(v["ratio"], 4) for k, v in predictions["diagonal"].items()
    } == PREDICTED_DIAGONAL_RATIO
    assert {
        k: round(v["fit"]["exponent"], 3) for k, v in predictions["depth"].items()
    } == PREDICTED_DEPTH_EXPONENT
    free = predictions["free_space"]
    assert free["half_width"] == 96
    assert {
        k: round(free["alphas"][k]["alpha"], 7) for k in PREDICTED_FREE_ALPHA
    } == PREDICTED_FREE_ALPHA
    assert {
        k: round(free["fits"][k]["exponent"], 3) for k in PREDICTED_FREE_EXPONENT
    } == PREDICTED_FREE_EXPONENT
    # The b = 4 row recomputed: the same push to 1e-6 and the same per-tick pushes.
    predict = load_script("predict")
    total, per_tick = predict.transient_pass((65, 65, 9), (32, 32, 4), (0, 4, 0))
    assert all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(total, cases["b4"]["push"], strict=True))
    assert len(per_tick) == 64 and per_tick[0][0] == LAUNCH_DELAY + 2 and per_tick[-1][1] == 64
    assert all(
        math.isclose(a[2][1], b[2][1], abs_tol=1e-6)
        for a, b in zip(per_tick, cases["b4"]["per_tick"], strict=True)
    )


def test_a6_record_pins_the_measured_integers():
    analyze = load_script("analyze")
    record = json.loads((WORLDS / "record.json").read_text(encoding="utf-8"))
    runs = {(run["form"], run["case"]): run for run in record["runs"]}
    assert set(runs) == {(form, case) for form in FORMS for case in CASES}
    source = record["runs"][0]["source_sha256"]
    for (form, case), run in runs.items():
        name = f"{form}_{case}"
        assert run["model"] == model_of(name)
        assert run["status"] == "completed" and run["error"] is None, name
        assert run["source_sha256"] == source, name
        digest = hashlib.sha256((WORLDS / f"{name}.json").read_bytes()).hexdigest()
        assert run["initialization_sha256"] == digest, name
        assert run["ticks"] == TICKS and run["dense"] == "dense-field-v1", name
        assert run["all_balanced"] and run["conserved_at_every_completed_tick"], name
        # Every ray leaves the board on its line at the straight tick: the register
        # turns, the DDA completes no transverse Link, and the delay form's lag
        # never reaches a transverse Link.
        assert run["straight"], name
        assert run["escape_tick"] == LAUNCH_DELAY + run["shape"][0] + 1, name
        assert tuple(run["register"]) == MEASURED_REGISTER[(form, case)], name
        assert run["pushes"] == MEASURED_PUSHES[form][case], name
        assert run["star_final_momentum"] == MEASURED_STAR[form].get(case), name
        assert run["bodies_momentum_line"] == (run["star_final_momentum"] or [0, 0, 0]), name
        assert math.isclose(
            run["alpha"],
            math.atan2(math.hypot(run["register"][1], run["register"][2]), run["register"][0]),
        ), name
    # The delay form: no push, the register unchanged in every world; the turn form:
    # a push at every Node the field reaches, the register the sum of the pushes.
    for case in CASES:
        assert runs[("delay", case)]["pushes"] == 0 and runs[("delay", case)]["register"] == [
            LIGHT,
            0,
            0,
        ], case
        turn = runs[("turn", case)]
        assert [LIGHT + turn["push_sum"][0], turn["push_sum"][1], turn["push_sum"][2]] == turn[
            "register"
        ], case
    # The turn form's integers: the exponent over the five b, the linearity, the N
    # scan (one register at every N), the diagonal against the cube's axis fit, the
    # slow ray's register equal to the light's, the mean field within its band.
    turn = record["clauses"]["turn"]
    points = [(float(b), runs[("turn", f"b{b}")]["alpha"]) for b in AXIS_B]
    fit = analyze.fit(points)
    assert (
        round(fit["exponent"], 3) == MEASURED_EXPONENT
        and round(fit["standard_error"], 3) == MEASURED_ERROR
    )
    assert round(turn[3]["numbers"]["fit"]["exponent"], 3) == MEASURED_EXPONENT
    assert round(turn[4]["numbers"]["ratio"], 4) == MEASURED_LINEARITY
    for bits in SCAN_BITS:
        assert runs[("turn", f"n{bits}")]["register"] == runs[("turn", "b8")]["register"], bits
    assert turn[5]["numbers"]["G_eff_constant"] is True and turn[5]["pass"] is False
    assert {
        k: round(v["ratio"], 4) for k, v in turn[6]["numbers"]["diagonal"].items()
    } == MEASURED_DIAGONAL_RATIO
    assert round(turn[6]["numbers"]["cube_fit"]["exponent"], 3) == MEASURED_CUBE_EXPONENT
    assert runs[("turn", "slow")]["register"] == runs[("turn", "b8")]["register"]
    assert turn[7]["numbers"]["ratio"] == 1.0
    assert round(turn[8]["numbers"]["max_deviation"], 4) == MEASURED_MEAN_FIELD_DEVIATION
    # The clause table's verdicts, in the criterion's order, per form.
    assert [entry["pass"] for entry in turn] == TURN_VERDICTS
    assert [entry["pass"] for entry in record["clauses"]["delay"]] == DELAY_VERDICTS

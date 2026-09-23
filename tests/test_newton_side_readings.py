"""Side A of Newton on the side (docs/designs/newton_clicks/NEWTON_ON_THE_SIDE.md
sections 3 and 4; docs/designs/fail_rows/RUN_14.md): the shipped worlds
equal their generator's and load with the declared keys, the rung's
integers are the design's, and the reading tool
(`tools/newton_side_readings.py`) reads hand-written click lines and a
small in-process run against the pins' integers.

(a) The three worlds equal `make_worlds.worlds()` document for document and
    `expectations.json` equals `make_worlds.expectations()`; each loads
    with `clock_stamp`, `massive_rows`, `optical` 1 and the pair [1, 4096];
    the rung: E'_0 = 1344, E'_D = 1349 = 19 x 71, the control's arrival
    count 979 for 52 Links (the massive triple), the light row's 89 (the
    flight table); the pins of the register are the generator's closed
    forms (the advance -40.5 on 979, the centroid 4.39 and 4.46, the light
    row's -4.63 and -5.47, the read delay 3.0 on the wall's 3.96).
(b) Hand-written click lines: the control's clicks all at 979 counts on the
    line's end Node read the pin (every click alike, the pace inside the
    band, the centroid exact, the count ratio 1); the mass world's clicks
    40 counts earlier on Nodes four to five pixels toward the mass read
    the advance and the centroid; the light row's clicks read the
    deciding pin under one count and not the other; decoys (a pass, a
    click of another family, a face click, a line without a record) are
    left out and a face click of the family is counted.
(c) A small run on a bar (6 Links from the lamp to a plane of nine
    receiver bodies reading the presence, no mass): every click line the
    receivers write carries `clock` and `record`, the tool's arrival count
    is the massive triple's first age at 6 Links on the first click and
    one more on every later one (the birth's convention: the lamp at the
    content K skips its second self-creation once), the light lamp's the
    flight table's; and under an entry reading `age` the receiver's own
    count falls behind the tick by the arriving rows' age over d (the
    step the design did not list, RUN_14.md step 5), which is why the
    shipped receivers read the presence.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

from event_universe.configuration_validation import validate_configuration
from event_universe.events import parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "newton_side"
TOOLS = ROOT / "tools"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load("newton_side_make_worlds", WORLDS / "make_worlds.py")
TOOL = load("newton_side_readings", TOOLS / "newton_side_readings.py")
REGISTER = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))


def test_the_shipped_worlds_are_the_generators_and_the_rung_is_the_designs():
    """(a)."""
    generated = GENERATOR.worlds()
    assert set(generated) == {"control", "mass", "light"}
    for name, document in generated.items():
        shipped = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
        assert shipped == document, name
        report = validate_configuration((WORLDS / f"{name}.json").read_bytes(), base_dir=WORLDS)
        assert report.valid and not report.issues, report
        assert document["clock_stamp"] is True and document["massive_rows"] is True
        assert document["optical"] == 1 and document["suspension"] == [1, 4096]
        assert document["flow_link"] is False and document["width"] == 1
        assert document["action"] == 1024 and document["age_bound"] == 2048
        assert document["ticks"] == GENERATOR.TICKS == 1400
        assert "detectors" not in document
    assert REGISTER == GENERATOR.expectations()
    assert REGISTER["format"] == GENERATOR.EXPECTATIONS_FORMAT
    # The rung k = 19: E'_0 = Q S M_row = 1344, E'_D = isqrt(1344^2 + 3 x 71^2) = 1349 = 19 x 71.
    assert (GENERATOR.REST_ENERGY, GENERATOR.PACE_WALL) == (1344, 1349)
    assert GENERATOR.PACE_WALL == 19 * 71
    assert 2 * GENERATOR.PACE_WALL == 19 * 2 * GENERATOR.MOMENTUM_MAGNITUDE
    assert GENERATOR.arrival_count(52) == 979 == TOOL.massive_arrival_count(52, 21, 1, 71)
    assert TOOL.massive_arrival_count(51, 21, 1, 71) == 960
    assert GENERATOR.light_arrival_count() == 89 == TOOL.light_arrival_count(52)
    assert TOOL.light_arrival_count(32) == 55
    # The worlds' integers: the lamp on the rung, the held mass, the receivers.
    control, mass, light = (generated[n] for n in ("control", "mass", "light"))
    lamp = control["measured"][0]
    assert lamp["lamp"]["momentum_magnitude"] == 71 and lamp["amount"] == control["K"]
    assert lamp["lamp"]["directions"] == [[1, 0, 0]] and lamp["position"] == [2, 26, 20]
    assert control["families"][0] == {"name": "matter", "quantum": 21, "massive": True}
    assert len(control["measured"]) == 1 + 41 * 41 and len(mass["measured"]) == 2 + 41 * 41
    held = mass["measured"][1]
    assert (
        held["position"] == [28, 20, 20] and held["amount"] == 1 << 10 and len(held["directions"]) == 290
    )
    assert light["measured"][1]["amount"] == 1 << 16
    assert "momentum_magnitude" not in light["measured"][0]["lamp"]
    receiver = mass["measured"][2]
    assert receiver["position"][0] == 54 and receiver["table"] == {
        "matter": {"rule": "measure", "reads": "presence"},
        "m": "pass",
    }
    # The pins by the closed forms (the design's section 4.1).
    worlds = REGISTER["worlds"]
    assert worlds["control"]["arrival_count"]["pin"] == 979
    assert worlds["mass"]["arrival_count"]["advance"] == -40.5
    assert worlds["mass"]["arrival_count"]["count"] == 939.5
    assert abs(worlds["mass"]["arrival_count"]["wall_delay"] - 0.68) < 0.01
    assert abs(worlds["mass"]["arrival_count"]["push_advance"] + 41.19) < 0.01
    assert (
        worlds["mass"]["centroid_toward_mass"]["pin"],
        worlds["mass"]["centroid_toward_mass"]["crossing"],
    ) == (
        4.39,
        4.46,
    )
    assert worlds["mass"]["advance_over_own_wall_delay"] == 60.2
    assert worlds["light"]["arrival_count"]["control"] == 89
    assert abs(worlds["light"]["arrival_count"]["wall_delay"] - 3.96) < 0.01
    assert worlds["light"]["arrival_count"]["clocks_rate"] == 0.9901
    assert worlds["light"]["arrival_count"]["pin"] == 3.0
    assert abs(worlds["mass"]["clocks_shift"]) < 0.2
    assert (
        worlds["light"]["centroid_toward_mass"]["arrivals"],
        worlds["light"]["centroid_toward_mass"]["crossing"],
    ) == (
        4.63,
        5.47,
    )
    assert REGISTER["rung"]["u_over_c"] == 0.0912 and REGISTER["geometry"]["logarithm"] == 4.319


LAMP = (2, 26, 20)
PLANE_X = 54
RECEIVERS = {n: (PLANE_X, 20 + (n - 3) // 7, 20 + (n - 3) % 7) for n in range(3, 3 + 49)}


def receiver_at(y: int, z: int) -> int:
    return next(n for n, p in RECEIVERS.items() if p == (PLANE_X, y, z))


def click(ordinal: int, count: int, y: int, z: int = 20, family: str = "matter", owed: int = 0) -> dict:
    """A receiver body's click line: the receiver's number and Node, its own
    count `clock`, the row's record (the lamp's number 1 x 2^32 + the
    ordinal), the row's age moment as the reading; the tick behind the
    count by what the receiver owes."""
    return {
        "event": "click",
        "tick": ordinal + count + owed,
        "node": [PLANE_X, y, z],
        "measured": receiver_at(y, z),
        "detector": None,
        "family": family,
        "number": 1,
        "amount": 1,
        "push": [71, 0, 0],
        "phase": 0,
        "content": 21,
        "reading": 1,
        "clock": ordinal + count,
        "record": (1 << 32) + ordinal,
    }


def reading_of(name: str, clicks: list[dict], family: str = "matter", mass: bool = True) -> object:
    reading = TOOL.Reading(
        name=name,
        folder=None,
        completed=True,
        balanced=True,
        ticks=1400,
        elapsed=0.0,
        lamp_position=LAMP,
        lamp_family=family,
        mass_position=(28, 20, 20) if mass else None,
        mass_amount=(1 << 10) if mass else None,
        plane_x=PLANE_X,
        receivers=dict(RECEIVERS),
    )
    reading.control_count = 979 if family == "matter" else 89
    reading.control_source = "the test's"
    reading.clicks = TOOL.clicks_of(clicks, set(RECEIVERS), family)
    reading.face_clicks = TOOL.face_clicks_of(clicks, family)
    return reading


def test_the_tool_reads_hand_written_click_lines_against_the_pins(capsys):
    """(b)."""
    control_lines = [click(o, 979, 26) for o in range(1, 401)]
    decoys = [
        {**click(5, 979, 26), "event": "pass"},
        click(6, 979, 26, family="wall"),
        {**click(7, 979, 26), "measured": 999},
        {k: v for k, v in click(8, 979, 26).items() if k != "record"},
        {**click(9, 979, 26), "detector": "face:+x", "measured": None},
    ]
    control = reading_of("control", control_lines + decoys, mass=False)
    assert len(control.clicks) == 400
    assert control.face_clicks == {"face:+x": 1}
    assert control.clicks[0].arrival_count == 979 and control.clicks[0].reading == 1
    a = TOOL.analyse(control, 919)
    assert a.count == 400 and a.first_count == a.least_count == a.greatest_count == 979
    assert a.spread == 0.0
    assert a.pace == 52 / 979 and abs(a.pace - 1 / 19) <= a.band
    assert (a.centroid_y, a.centroid_z) == (26.0, 20.0)
    assert a.count_ratio == Fraction(1) and a.consecutive_least == a.consecutive_greatest == 1.0
    assert a.first_tick == 980 and a.owed_mean == 0.0 and a.receivers_lit == 1
    assert abs(a.intercept - 979.0) < 1e-9 and abs(a.slope) < 1e-12
    assert TOOL.analyse(control, 10_000).count == 0
    # The mass world: 40 counts earlier (the birth's convention, one count,
    # on the first ordinal as on the control), on the Nodes 4 and 5 pixels
    # toward the mass (y = 22 and 21), the receiver a count behind the tick.
    mass_lines = [click(o, 979 - 40 - (o == 1), 22 if o % 5 else 21, owed=1) for o in range(1, 401)]
    mass = reading_of("mass", mass_lines)
    a = TOOL.analyse(mass, 919)
    assert a.count == 400 and abs(a.mean_count - 938.9975) < 1e-9
    assert a.first_count == 938 and a.least_count == a.greatest_count == 939
    assert abs((26 - a.centroid_y) - 4.2) < 1e-9 and a.owed_mean == 1.0
    assert a.ratio_receiver == receiver_at(22, 20) and a.count_ratio == Fraction(1)
    assert abs(a.intercept - 939.0) < 1e-9 and abs(a.slope) < 1e-12
    # The light row: 4 counts late, 5 pixels toward the mass on average (the
    # crossing count's pin, not the arrivals'), without a control run.
    light_lines = [click(o, 89 + 4, 21, family="light") for o in range(101, 401)] + [
        click(o, 89 + 4, 20, family="light") for o in range(401, 501)
    ]
    light = reading_of("light", light_lines, family="light")
    code = TOOL.report([control, mass, light], REGISTER)
    out = capsys.readouterr().out
    assert code == 0
    assert "PASS the arrival count (DETECTOR): 979.000 against the pin 979" in out
    assert "PASS every click after the first the same count" in out
    assert "PASS the pace over the window" in out
    assert "PASS the arrival Node the line's end" in out
    assert "FAIL no click of the family on a face: {'face:+x': 1}" in out
    assert (
        "PASS the advance, the arrival count less the control's (DETECTOR), conditional on k_a(b): -40.003"
        in out
    )
    assert "PASS the mass world earlier than the control" in out
    assert "PASS the centroid toward the mass (DETECTOR), conditional on k_a(b): 4.200" in out
    assert "PASS the light row's arrival count less its control (DETECTOR)" in out
    assert (
        "FAIL the lever-arm centroid toward the mass (DETECTOR) under the arrivals count: 5.250" in out
    )
    assert (
        "PASS the lever-arm centroid toward the mass (DETECTOR) under the crossing count: 5.250" in out
    )
    assert "the deciding pin's answer: the row's push counts the crossings" in out
    assert "GAMEBOARD the first click's tick 980" in out
    assert "0 record check(s) failed" in out


BAR = (9, 3, 3)
BAR_PLANE_X = 8
BAR_LAMP = (2, 1, 1)
BAR_LINKS = BAR_PLANE_X - BAR_LAMP[0]


def bar_world(family: str) -> dict[str, object]:
    """A bar of 9 x 3 x 3 Nodes: the lamp at x = 2 on the axis, nine receiver
    bodies on the plane x = 8, no mass; the keys of the shipped worlds."""
    massive = family == "matter"
    lamp: dict[str, object] = {
        "position": list(BAR_LAMP),
        "family": family,
        "amount": 1 << 20,
        "phase": 0,
        "fixed": True,
        "lamp": {
            "rate": [1, 1],
            "wheel": [2531, 4096],
            "directions": [[1, 0, 0]],
            **({"momentum_magnitude": 71} if massive else {}),
        },
        "table": {"m": "pass"},
    }
    measured: list[dict[str, object]] = [lamp]
    for y in range(BAR[1]):
        for z in range(BAR[2]):
            measured.append(
                {
                    "position": [BAR_PLANE_X, y, z],
                    "family": "wall",
                    "amount": 1,
                    "fixed": True,
                    "table": {family: {"rule": "measure", "reads": "presence"}, "m": "pass"},
                }
            )
    return {
        "law": "beam",
        "model_id": f"beam-newton-side-bar_{family}-v1",
        "shape": list(BAR),
        "boundary": "open",
        "ticks": 160,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 4096],
        "suspension": [1, 4096],
        "width": 1,
        "action": 1024,
        "age_bound": 2048,
        "massive_rows": True,
        "optical": 1,
        "flow_link": False,
        "clock_stamp": True,
        "families": [
            {"name": "matter", "quantum": 21, "massive": True}
            if massive
            else {"name": "light", "quantum": 1},
            {"name": "wall", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
    }


def test_a_small_run_on_a_bar_reads_the_derived_count_on_every_click(tmp_path, capsys):
    """(c)."""
    for family in ("matter", "light"):
        document = bar_world(family)
        folder = tmp_path / family
        folder.mkdir()
        execute_nature_beam_run(
            parse_nature_beam_world(document),
            json.dumps(document).encode("utf-8"),
            folder,
            "test",
            160,
            keep_row_clicks=True,
        )
    readings = TOOL.find_runs(tmp_path)
    assert [r.name for r in readings] == ["bar_light", "bar_matter"]
    light, matter = readings
    assert matter.completed and matter.balanced and matter.ticks == 160
    assert matter.links_line == BAR_LINKS == light.links_line
    expected_matter = TOOL.massive_arrival_count(BAR_LINKS, 21, 1, 71)
    expected_light = TOOL.light_arrival_count(BAR_LINKS)
    assert expected_matter == 19 * BAR_LINKS - 9 == 105 and matter.control_count == 105
    assert light.control_count == expected_light == 10
    assert len(matter.clicks) >= 40 and len(light.clicks) >= 140
    for reading, expected in ((matter, expected_matter), (light, expected_light)):
        assert reading.receivers and all(p[0] == BAR_PLANE_X for p in reading.receivers.values())
        assert not reading.face_clicks
        # The birth's convention (RUN_14.md step 6; the design's edge case):
        # the lamp at the content K births at its first self-creation, skips
        # the second once and births at every one after, so the first
        # ordinal's count is the flight's age and every later one is a count
        # more; one count, inside the pin's bracket.
        ordered = sorted(reading.clicks, key=lambda c: c.ordinal)
        assert ordered[0].ordinal == 1 and ordered[0].arrival_count == expected
        assert {c.arrival_count for c in ordered[1:]} == {expected + 1}, reading.name
        assert [c.ordinal for c in ordered] == list(range(1, len(ordered) + 1))
        assert {c.node for c in reading.clicks} == {(BAR_PLANE_X, 1, 1)}
        assert all(c.reading == c.amount == 1 for c in reading.clicks)
        a = TOOL.analyse(reading, expected)
        assert a.count == len(reading.clicks) and a.count_ratio == Fraction(1)
        assert a.first_count == expected and a.least_count == a.greatest_count == expected + 1
        assert a.owed_mean == 0.0
    register = {
        "rung": {"k": 19},
        "window": {"massive": 100, "light": 10},
        "worlds": {
            "control": {
                "arrival_count": {"pin": expected_matter, "bracket": 1},
                "count_ratio": {"pin": 1.0, "bracket": 0.01},
            }
        },
    }
    matter.name = "control"
    assert TOOL.report([matter], register) == 0
    out = capsys.readouterr().out
    assert "PASS the arrival count (DETECTOR)" in out
    assert "PASS every click after the first the same count" in out
    assert "PASS the pace over the window" in out and "PASS no click of the family on a face" in out
    assert "0 record check(s) failed; 6 reading(s) inside, 0 outside" in out
    # The design's `reads: "age"` on the receivers: the arriving rows' age
    # moment stretches the receiver's own count, 105 / 4096 per click on
    # the bar, so its count falls one behind the tick within 40 clicks and
    # the arrival count is no longer alike.
    document = bar_world("matter")
    for entry in document["measured"][1:]:
        entry["table"]["matter"] = {"rule": "measure", "reads": "age"}
    folder = tmp_path / "matter_age"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document),
        json.dumps(document).encode("utf-8"),
        folder,
        "test",
        160,
        keep_row_clicks=True,
    )
    stretched = TOOL.read_run(folder)
    ordered = sorted(stretched.clicks, key=lambda c: c.ordinal)
    assert {c.arrival_count for c in ordered[1:]} == {expected_matter, expected_matter + 1}
    assert max(c.tick - c.clock for c in ordered) == 1
    assert all(c.reading == expected_matter for c in ordered)

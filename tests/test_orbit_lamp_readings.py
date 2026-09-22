"""The series D3 readings tool (`tools/orbit_lamp_readings.py`, Newton after
a detector) and its generator (`examples/events/orbit_lamp/make_worlds.py`)
read the engine (the experimenter's rule, 2026-09-20: a readings tool never
replays a rule of the engine; the reading is the detector line's `click`
lines alone). The expected integers, written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document
    and `expectations.json` equals `make_worlds.expectations()` (its
    `replicated` map aside), declares its format and names a derivation
    for every pinned quantity; the shipped pins are the per-axis drive's
    at n = 9 (T = 2 pi r x 41 / 9: 343 and 687, the escape at the 61st
    step) and the generator reproduces the first run's pins at n = 10
    under the directional drive (371 and 742);
(b) on a hand-made click list of a circle of radius 24 about the column 60
    turning once per 742 intervals, sampled at every 8th interval over 4000
    (500 clicks, each at the tick of its birth plus a flight), the tool
    reads the period within one birth interval of 742 from 6 downward and
    5 upward crossings of the centre column, omega^2 within 3 percent of
    (2 pi / 742)^2 from the second difference at the lag 184, and a click
    of another family, a `pass` line and a face click are not clicks of
    the line; a constant x reads no crossing, no period and no slope; an
    empty list reads no period; two lists compare on their common ticks;
(c) on a 9 x 9 x 1 plane (z periodic, no source, `release` [1, 1000] so
    the held mass never releases) run through the runner for 40 intervals:
    a probe of the paid family `probe` of amount 2^10 holding 1 of `m` at
    (4, 7, 0) at rest (K 512, the turn 2, never 0: a turn of 0 skips the
    birth) with the lamp of rate [1, 2] on
    +y and -y, and the line of 9 `wall` events at y = 1 read as the
    one-Node `wave` detectors `line_<x>` with `reads: "age"`: the -y row
    of every birth clicks at `line_4` at the age 10, the least age with
    m(age) >= 6 Links on a heading off the flight table ((128 age + 110)
    // 220), so the tool reads 15 clicks (the births at the ages 2 .. 30),
    every one at x = 4 with the birth tick its click's tick less 10, the
    count the engine's own `clicks` of `probe` on `line_4`, the run
    completed and balanced, the world's centre column 4 (no source) and
    no escape of the probe.
"""

from __future__ import annotations

import importlib.util
import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import HEADING_OFFSET
from event_universe.register_map import REPLICATED

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "orbit_lamp"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


TOOL = load("orbit_lamp_readings_tool", ROOT / "tools" / "orbit_lamp_readings.py")
GENERATOR = load("orbit_lamp_make_worlds", WORLDS / "make_worlds.py")

PERIOD = 742.0
RADIUS = 24
CENTRE_X = 60
BIRTH_INTERVAL = 8
TICKS = 4000
LAG = 184


def test_the_shipped_worlds_are_the_generators_and_the_expectations_are_pinned():
    generated = GENERATOR.worlds()
    assert set(generated) == {"r12", "r24", "r24_4m", "r12_control", "r24_control"}
    for name, document in generated.items():
        shipped = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
        assert shipped == document, name
    pinned = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    pinned.pop(REPLICATED, None)
    expected = GENERATOR.expectations()
    assert pinned == json.loads(json.dumps(expected))
    assert pinned["format"] == GENERATOR.EXPECTATIONS_FORMAT
    for key in (
        "period",
        "ratio",
        "omega_squared",
        "acceleration",
        "amplitude",
        "equivalence",
        "control",
        "flight",
    ):
        assert key in pinned["derivations"], key
    assert pinned["orbit_n"] == 10 and pinned["drive"] == GENERATOR.LINE_DRIVE
    assert pinned["birth_interval"] == BIRTH_INTERVAL
    # The shipped pins at n = 10 under the law's line drive (2026-09-22: the
    # pace 640 / 3148 = 0.2033 on a heading, T = 370.9 and 741.7) and the
    # registered re-run's at n = 9 under the per-axis drive of history (T =
    # 343 and 687, series D's table), both reproducible from the generator.
    pace = 10 * 64 / (64 * 32 + 10 * 110)
    assert abs(pinned["pace"] - pace) < 1e-12 and abs(pace - 0.2033) < 5e-5
    assert abs(pinned["worlds"]["r12"]["period"]["pin"] - 2 * math.pi * 12 / pace) < 1e-9
    assert abs(pinned["worlds"]["r24"]["period"]["pin"] - 2 * math.pi * 24 / pace) < 1e-9
    assert abs(pinned["worlds"]["r12"]["period"]["pin"] - 370.9) < 0.1
    assert pinned["worlds"]["r12"]["momentum"] == 10 * 64 * ((1 << 12) + (1 << 20))
    assert abs(pinned["worlds"]["r12_control"]["escape_tick"]["pin"] - 61 / pace) < 1e-9
    assert abs(pinned["worlds"]["r12_control"]["escape_tick"]["pin"] - 300.0) < 0.1
    history = GENERATOR.expectations(GENERATOR.HISTORY_N, GENERATOR.AXIS_DRIVE)
    assert history["orbit_n"] == 9 and history["drive"] == GENERATOR.AXIS_DRIVE
    assert abs(history["worlds"]["r12"]["period"]["pin"] - 2 * math.pi * 12 * 41 / 9) < 1e-9
    assert abs(history["worlds"]["r24"]["period"]["pin"] - 2 * math.pi * 24 * 41 / 9) < 1e-9
    assert history["worlds"]["r12"]["momentum"] == 9 * 64 * ((1 << 12) + (1 << 20))
    assert GENERATOR.worlds(GENERATOR.HISTORY_N)["r12"] != generated["r12"]
    assert (
        abs(pinned["worlds"]["r24"]["period"]["pin"] / pinned["worlds"]["r12"]["period"]["pin"] - 2.0)
        < 1e-9
    )
    assert pinned["worlds"]["r12_control"]["x"] == 72 and pinned["worlds"]["r24_control"]["x"] == 84
    assert pinned["worlds"]["r24_4m"]["held_mass"] == 4 * pinned["worlds"]["r24"]["held_mass"]


def test_the_one_constant_pins_are_the_generators_and_the_worlds_differ_by_the_key_alone():
    """flow-link-v1 (the generator's docstring): `expectations_flow.json`
    equals `expectations(flow=True)`, the balance divided by F_plane = 1.2871
    to the whole n = 8 (under the law's line drive since 2026-09-22 the real
    root 8.28, the pace 8 x 64 / (64 x 32 + 8 x 110), T = 431 and 862; under
    the per-axis drive of history 7.67, T = 377 and 754, reproduced by
    `expectations(drive=AXIS_DRIVE, flow=True)`), and the four one-constant
    worlds are the registered ones with the key `flow_link` and the momentum
    at 8, nothing else changed; the ratio's names are the flow worlds', no
    equivalence world. The world files themselves ship with the key
    (the loader refuses an unknown key until then)."""
    pinned = json.loads((WORLDS / "expectations_flow.json").read_text(encoding="utf-8"))
    pinned.pop(REPLICATED, None)
    assert pinned == json.loads(json.dumps(GENERATOR.expectations(flow=True)))
    assert pinned["format"] == GENERATOR.EXPECTATIONS_FORMAT
    assert pinned[GENERATOR.FLOW_KEY] is True and pinned["orbit_n"] == 8
    assert abs(pinned["flow_incidence"] - 1.2871) < 5e-5
    assert abs(pinned["flow_constant"] - 1 / pinned["flow_incidence"]) < 1e-12
    assert 8.0 < pinned["orbit_n_real"] < 8.5 and pinned["drive"] == GENERATOR.LINE_DRIVE
    pace = 8 * 64 / (64 * 32 + 8 * 110)
    assert abs(pinned["worlds"]["r12_flow"]["period"]["pin"] - 2 * math.pi * 12 / pace) < 1e-9
    assert abs(pinned["worlds"]["r24_flow"]["period"]["pin"] - 2 * math.pi * 24 / pace) < 1e-9
    assert abs(pinned["worlds"]["r12_flow"]["period"]["pin"] - 431.2) < 0.1
    assert pinned["worlds"]["r12_flow"]["momentum"] == 8 * 64 * ((1 << 12) + (1 << 20))
    assert abs(pinned["worlds"]["r12_flow_control"]["escape_tick"]["pin"] - 61 / pace) < 1e-9
    history = GENERATOR.expectations(drive=GENERATOR.AXIS_DRIVE, flow=True)
    assert history["orbit_n"] == 8 and 7.5 < history["orbit_n_real"] < 8.0
    assert abs(history["worlds"]["r12_flow"]["period"]["pin"] - 2 * math.pi * 12 * 40 / 8) < 1e-9
    assert abs(history["worlds"]["r12_flow_control"]["escape_tick"]["pin"] - 61 * 40 / 8) < 1e-9
    assert pinned["ratio"]["worlds"] == ["r12_flow", "r24_flow"]
    assert pinned["ratio"]["bracket"] == [1.82, 2.18]
    assert "equivalence" not in pinned
    for key in ("flow_link", "flow_incidence", "period", "ratio", "control"):
        assert key in pinned["derivations"], key
    registered = GENERATOR.worlds()
    flow = GENERATOR.worlds(flow=True)
    assert set(flow) == {"r12_flow", "r24_flow", "r12_flow_control", "r24_flow_control"}
    for name, document in flow.items():
        base = registered[name.replace(GENERATOR.FLOW_SUFFIX, "")]
        assert document[GENERATOR.FLOW_KEY] is True and GENERATOR.FLOW_KEY not in base
        assert document["model_id"] == base["model_id"].replace("-plane-v1", "-flow-plane-v1").replace(
            "-control-flow-", "-flow-control-"
        )
        probe = next(i for i, m in enumerate(document["measured"]) if "lamp" in m)
        assert document["measured"][probe]["momentum"] == [0, 8 * 64 * ((1 << 12) + (1 << 20)), 0]
        assert base["measured"][probe]["momentum"] == [0, 10 * 64 * ((1 << 12) + (1 << 20)), 0]
        stripped = {k: v for k, v in document.items() if k not in (GENERATOR.FLOW_KEY, "model_id")}
        stripped["measured"] = [
            {k: v for k, v in m.items() if k != "momentum"} for m in stripped["measured"]
        ]
        expected = {k: v for k, v in base.items() if k != "model_id"}
        expected["measured"] = [
            {k: v for k, v in m.items() if k != "momentum"} for m in expected["measured"]
        ]
        assert stripped == expected, name
        shipped = WORLDS / f"{name}.json"
        if shipped.exists():
            assert json.loads(shipped.read_text(encoding="utf-8")) == document, name


def circle_clicks() -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for k in range(1, TICKS // BIRTH_INTERVAL + 1):
        t = k * BIRTH_INTERVAL
        angle = 2 * math.pi * t / PERIOD
        x = CENTRE_X + round(RADIUS * math.cos(angle))
        y = 60 + round(RADIUS * math.sin(angle))
        age = round((y - 20) * 55 / 32)
        found.append(
            {"event": "click", "tick": t + age, "detector": f"line_{x}", "family": "probe", "age": age}
        )
    return found


def test_the_tool_reads_a_hand_made_click_list():
    lines = circle_clicks()
    decoys = [
        {"event": "click", "tick": 100, "detector": "line_60", "family": "m", "age": 3},
        {"event": "pass", "tick": 100, "detector": "line_60", "family": "probe", "age": 3},
        {"event": "click", "tick": 100, "detector": "face:+y", "family": "probe", "age": 3},
    ]
    clicks = TOOL.clicks_of(lines + decoys, "probe")
    assert len(clicks) == TICKS // BIRTH_INTERVAL
    samples = sorted((c.birth, c.x) for c in clicks)
    assert [t for t, _ in samples] == [k * BIRTH_INTERVAL for k in range(1, TICKS // BIRTH_INTERVAL + 1)]
    period = TOOL.period_of(samples, CENTRE_X)
    assert len(period.down.ticks) == 6 and len(period.up.ticks) == 5
    assert period.value is not None and abs(period.value - PERIOD) < BIRTH_INTERVAL
    second = TOOL.second_difference_of(samples, CENTRE_X, LAG)
    assert second.omega_squared is not None and second.samples > 400
    assert abs(second.omega_squared / (2 * math.pi / PERIOD) ** 2 - 1) < 0.03
    # A constant x: no crossing, no period, no slope; an empty list: no period.
    flat = [(t, 72) for t in range(8, 400, 8)]
    assert TOOL.period_of(flat, CENTRE_X).value is None and TOOL.period_of(flat, CENTRE_X).crossings == 0
    assert TOOL.second_difference_of(flat, CENTRE_X, 16).omega_squared is None
    assert TOOL.period_of([], CENTRE_X).value is None
    # Two lists on their common ticks.
    other = [(t, x + (1 if t == 16 else 0)) for t, x in samples[:10]]
    assert TOOL.common_x_difference(samples, other) == (10, 9, 1)
    assert TOOL.common_x_difference(samples, []) == (0, 0, 0)
    # The age gives the birth's y back off the flight table, within one Link.
    for click in clicks:
        angle = 2 * math.pi * click.birth / PERIOD
        assert abs(20 + TOOL.links_of(click.age) - (60 + round(RADIUS * math.sin(angle)))) <= 1


SIDE = 9
LINE_Y = 1
PROBE = (4, 7, 0)
TINY_TICKS = 40
RESERVOIR = 1 << 10
CLOCK = 512


def tiny_world() -> dict[str, object]:
    measured: list[dict[str, object]] = [
        {
            "position": list(PROBE),
            "family": "probe",
            "amount": RESERVOIR,
            "phase": 0,
            "fixed": False,
            "momentum": [0, 0, 0],
            "held": {"m": 1},
            "table": {"m": "read"},
            "directions": [[0, 1, 0], [0, -1, 0]],
            "lamp": {"rate": [1, 2], "wheel": [1, 64], "directions": [[0, 1, 0], [0, -1, 0]]},
        }
    ]
    detectors: list[dict[str, object]] = []
    for x in range(SIDE):
        measured.append(
            {
                "position": [x, LINE_Y, 0],
                "family": "wall",
                "amount": 1,
                "fixed": True,
                "table": {"probe": {"rule": "measure", "reads": "age"}, "m": "pass"},
            }
        )
        detectors.append(
            {"name": f"line_{x}", "positions": [[x, LINE_Y, 0]], "threshold": 1, "reading": "wave"}
        )
    return {
        "law": "beam",
        "model_id": "rays-orbit-lamp-tiny-plane-v1",
        "shape": [SIDE, SIDE, 1],
        "boundary": {"z": "periodic"},
        "ticks": TINY_TICKS,
        "K": CLOCK,
        "N": 64,
        "release": [1, 1000],
        "suspension": 0,
        "width": 32,
        "families": [
            {"name": "probe", "quantum": 1},
            {"name": "wall", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
        "detectors": detectors,
    }


def test_read_run_reads_the_line_clicks_and_the_engines_flight(tmp_path, capsys):
    document = tiny_world()
    folder = tmp_path / "tiny" / "run"
    folder.mkdir(parents=True)
    execute_nature_beam_run(
        parse_nature_beam_world(document),
        json.dumps(document).encode("utf-8"),
        folder,
        "test",
        TINY_TICKS,
    )
    # The flight of 6 Links on a heading off the flight table: the least
    # age with m(age) >= 6, and the same by the table's closed form.
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    ages = np.arange(1, 40, dtype=np.int64)
    walked = table.manhattan_steps(np.full(ages.shape, HEADING_OFFSET), ages)
    flight = int(ages[np.flatnonzero(walked >= PROBE[1] - LINE_Y)[0]])
    assert flight == 10 and (128 * 9 + 110) // 220 == 5 and (128 * 10 + 110) // 220 == 6
    (reading,) = TOOL.find_runs(tmp_path)
    assert (
        reading.name == "tiny" and reading.completed and reading.balanced and reading.ticks == TINY_TICKS
    )
    assert reading.lamp_family == "probe" and reading.probe_number == 1
    assert reading.centre_x == SIDE // 2 and not reading.source and reading.escape is None
    assert len(reading.clicks) == 15
    assert all(c.x == PROBE[0] and c.age == flight for c in reading.clicks)
    assert [t for t, _ in reading.samples] == list(range(2, 31, 2))
    assert reading.amplitude == 0 and reading.middle == PROBE[0]
    assert (reading.centre_y, reading.line_y) == (SIDE // 2, LINE_Y)
    assert reading.radii == [float(PROBE[1] - SIDE // 2)] * len(reading.clicks)
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    line = next(d for d in record["detectors"] if d["name"] == f"line_{PROBE[0]}")
    assert line["families"]["probe"]["clicks"] == len(reading.clicks)
    assert TOOL.period_of(reading.samples, reading.centre_x).value is None
    assert reading.contacts == []
    # The probe's escape and its contacts with the detector line are read
    # from the register's own lines and printed for every world, a source
    # world's included (the Newton Diagnostician's finding of 2026-09-22 on
    # the run under flow_link: the source worlds' escape was read and never
    # printed, record 1022). A copy of the run with a face click of the
    # probe's number and a contact line appended, under another name.
    copy = tmp_path / "copy" / "run"
    shutil.copytree(folder, copy)
    record["model"] = "rays-orbit-lamp-tiny-two-plane-v1"
    (copy / "run.json").write_text(json.dumps(record), encoding="utf-8")
    with (copy / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "event": "contact",
                    "tick": 20,
                    "number": 1,
                    "node": [4, 2, 0],
                    "to": [4, 1, 0],
                    "occupant": 6,
                    "family": "probe",
                    "rule": "measure",
                    "axis": 1,
                    "component": -5,
                    "momentum": [0, 0, 0],
                }
            )
            + "\n"
        )
        stream.write(
            json.dumps(
                {"event": "click", "tick": 37, "detector": "face:+y", "family": "probe", "measured": 1}
            )
            + "\n"
        )
    (second,) = TOOL.find_runs(tmp_path / "copy")
    assert second.name == "tiny_two" and len(second.clicks) == len(reading.clicks)
    assert second.escape == ("face:+y", 37)
    assert second.contacts == [TOOL.Contact(20, (4, 2, 0), "measure", 1, -5)]
    pins = {
        "birth_interval": 2,
        "ratio": {"bracket": [1.82, 2.18]},
        "worlds": {
            "tiny": {"source": False, "x": PROBE[0], "escape_tick": {"bracket": [30.0, 40.0]}},
            "tiny_two": {"source": False, "x": PROBE[0], "escape_tick": {"bracket": [30.0, 40.0]}},
        },
    }
    capsys.readouterr()
    assert TOOL.report([reading, second], pins) == 0
    printed = capsys.readouterr().out
    assert "DETECTOR the probe did not leave the plane in 40 intervals" in printed
    assert "GAMEBOARD (a contact line) the probe never touched the detector line" in printed
    assert "DETECTOR the probe left through face:+y at the tick 37" in printed
    assert (
        "GAMEBOARD (a contact line) the probe touched the detector line 1 time(s): the tick 20 at [4, 2, 0] "
        "(the wall's rule measure, the axis 1 component -5 taken)"
    ) in printed
    assert "the escape tick: 37 (expected 30 .. 40): inside" in printed
    assert "the escape tick: none (expected 30 .. 40): outside" in printed

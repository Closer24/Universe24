"""Series X, Poisson after a detector (`examples/events/shell_clock/`, the
chief physicist's design of record 574 under the owner's word of
2026-09-22; the pins from docs/designs/clock_age/clock_age_map.py section
E). The expected values of docs/TEST_EXPECTATIONS.md ("Poisson after a
detector"), written down first:

(a) the nine shipped worlds equal `make_worlds.worlds()` document for
    document: the detector number 1 at x = 3 reading `age`, the lamp number
    2 at x = 103 fixed with its lamp on -x and its `mass` entry
    `{"rule": "pass", "reads": "age"}` or `{"rule": "pass", "reads":
    "presence"}` (the control declaring no entry), the shell's 450 `mass`
    sources at |distance - 6| < 1/2 from a centre r Links along +x from the
    lamp, each fixed, of the amount 1431597 and naming the 290 directions of
    series E's fan by the indices of the world's table; the GameBoard
    110 + r x 15 x 15, 500 intervals; the control the same GameBoard with
    the shell removed, two measured events;
(b) the algebra of the pin, no world run: the shell's Node count 450, the
    release 2 F x 2^16 / 450 = 1431597 so 21.8444 units per source per
    direction per interval, and with uniform sources k = the map's age
    moment x the release / 2^16, which gives one number, 1.695264, at
    r = 2 and at r = 4 (5086 is one integer at both, a coincidence of the
    lattice at the design's two Nodes; the map's interior runs 5009 to 5246) and
    1.047957 at r = 12; the register's pinned ratios 1.003917, 0.839989 and
    0.618270 with the tolerance 0.02, and the presence word's departure
    from 1 more than forty times the age word's;
(c) the readings tool on a hand-made click list: clicks every other tick
    with the ordinals in order read 1 + z = 2.0000 exactly, the click rate
    0.5 and no ordinal missing, and a list whose k sits outside the pin's
    bracket reads the verdict `moved` or `failed`;
(d) the rule the whole reading rests on, on a minimal GameBoard: a detector
    whose OWN clock is slowed by a crowd at its Node clicks on the same
    lattice ticks as one with no crowd, so the shell's rows reaching the
    detector cannot move the reading; only the lamp's clock moves 1 + z (the
    reading's denominator is the host tick, the detector's own clock only at
    k_D = 0, record 569; the map gives k_D = 0.0945, 0.0927 and 0.1357 at
    x = 3, the convention the owner's, the same as series T's);
(e) one shell world parses under the law and runs two intervals with the
    books balanced.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "shell_clock"
NAMES = (
    "age_2",
    "age_4",
    "age_12",
    "presence_2",
    "presence_4",
    "presence_12",
    "control_2",
    "control_4",
    "control_12",
)
DETECTOR, LAMP = 1, 2
SHELL_NODES = 450
AMOUNT = 1431597
FAN = 290


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def generator():
    return load("shell_clock_make_worlds", WORLDS / "make_worlds.py")


def reader():
    return load("shell_clock_read_runs", WORLDS / "read_runs.py")


def simulation(name: str) -> NatureBeamSimulation:
    path = WORLDS / f"{name}.json"
    loaded = load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent)
    return NatureBeamSimulation(loaded.world)


def test_the_shipped_worlds_are_the_generators():
    """(a)."""
    made = generator().worlds()
    assert set(made) == set(NAMES)
    for name, document in made.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        word, radius = name.rsplit("_", 1)
        radius = int(radius)
        centre = 7
        detector, lamp, *sources = document["measured"]
        assert document["shape"] == [110 + radius, 15, 15]
        assert document["ticks"] == 500
        assert detector["position"] == [3, centre, centre]
        assert detector["table"]["s_px1"] == {"rule": "measure", "reads": "age"}
        assert lamp["position"] == [103, centre, centre] and lamp["fixed"]
        assert lamp["lamp"]["directions"] == [[-1, 0, 0]]
        if word == "control":
            assert sources == []
            assert "table" not in lamp
            continue
        assert lamp["table"]["mass"] == {"rule": "pass", "reads": word}
        assert len(sources) == SHELL_NODES
        for source in sources:
            assert source["amount"] == AMOUNT and source["fixed"]
            assert len(source["directions"]) == FAN
            assert source["table"] == {"s_px1": {"rule": "pass"}}
        # Every source stands a half Link from the shell of radius 6 about a
        # centre `radius` Links along +x from the lamp.
        for source in sources:
            x, y, z = source["position"]
            distance = ((x - (103 + radius)) ** 2 + (y - centre) ** 2 + (z - centre) ** 2) ** 0.5
            assert abs(distance - 6) < 0.5, (name, source["position"])
    # The indices a source names resolve to series E's fan of 290.
    path = WORLDS / "age_4.json"
    loaded = load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent)
    source = loaded.world.measured[2]
    assert [list(loaded.world.directions[i]) for i in source.directions] == generator().FAN


def test_the_register_carries_the_maps_pins():
    """(a), the register."""
    made = generator()
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == made.EXPECTATIONS_FORMAT
    assert expected["windows"] == [[200, 350], [350, 500]]
    assert expected["flux"] == 4915
    assert expected["shell"] == {
        "radius": 6,
        "nodes": SHELL_NODES,
        "fan": FAN,
        "amount": AMOUNT,
        "declared_rate": AMOUNT / 65536,
        "effective_rate": {"lowest": 11.3054, "highest": 12.2240, "mean": 11.7078},
        "source_own_count": {"lowest": 0.787, "highest": 0.932, "mean": 0.866},
    }
    assert [round(expected["worlds"][n]["k"], 6) for n in NAMES] == [
        0.914351,
        0.910783,
        0.563110,
        0.089647,
        0.106724,
        0.029271,
        0.0,
        0.0,
        0.0,
    ]
    for name in NAMES:
        world = expected["worlds"][name]
        assert world["one_plus_z"] == 1 + world["k"]
        assert world["clicks_per_interval"] == 1 / (1 + world["k"])
        assert world["inside"] == (world["radius"] < 6)


def test_the_algebra_of_the_pin():
    """(b), no world run."""
    made = generator()
    assert len(made.SHELL) == SHELL_NODES
    assert made.AMOUNT == 2 * made.FLUX * 65536 // SHELL_NODES == AMOUNT
    assert abs(made.RATE - 21.8444) < 1e-4
    # The shell theorem on the lattice: one integer at both inside Nodes.
    assert made.UNIFORM_AGE_MOMENT[2] == made.UNIFORM_AGE_MOMENT[4] == 5086
    assert made.UNIFORM_PRESENCE[2] != made.UNIFORM_PRESENCE[4]
    for radius, uniform in made.PINNED_K_UNIFORM.items():
        assert abs(made.UNIFORM_AGE_MOMENT[radius] * made.RATE / 65536 - uniform) < 1e-5
    ratios = made.expectations()["ratios"]
    assert ratios["inside_age"]["pinned"] == 1.003917
    assert ratios["inside_presence"]["pinned"] == 0.839989
    assert ratios["outside_age"]["pinned"] == 0.618270
    assert ratios["outside_age"]["continuum"] == 0.5
    ripple = abs(ratios["inside_age"]["pinned"] - 1)
    assert abs(ratios["inside_presence"]["pinned"] - 1) > 40 * ripple
    assert ripple < ratios["inside_age"]["tolerance"]


def test_the_tool_on_a_hand_made_click_list(tmp_path):
    """(c)."""
    tool = reader()
    run = tmp_path / "age_4" / "run"
    run.mkdir(parents=True)
    # A lamp of one birth every other tick: the ordinals in order from 1 (the
    # engine's first birth ordinal), one click each, so the slope of the
    # ordinal against the tick is 1 / 2 and none of the light is lost.
    lines = [
        {"event": "click", "tick": 200 + 2 * n, "measured": 1, "record": n + 1, "age": 172}
        for n in range(150)
    ]
    lines.append({"event": "click", "tick": 250, "measured": 7, "record": 999, "age": 5})
    lines.append({"event": "birth", "tick": 250, "measured": 2, "record": 999})
    (run / "events.jsonl").write_text(
        "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
    )
    clicks = tool.clicks_of(run)
    assert len(clicks) == 150, "only the detector's click lines are read"
    pinned = {
        "k": 1.0,
        "k_bracket": [0.9, 1.1],
        "word": "age",
        "radius": 4,
        "inside": True,
        "one_plus_z": 2.0,
    }
    expected = {"windows": [[200, 350], [350, 500]]}
    reading = tool.read_world(tmp_path, "age_4", pinned, expected)
    assert reading["kind"] == "DETECTOR"
    for window in reading["windows"].values():
        assert abs(window["one_plus_z"] - 2.0) < 1e-9
        assert abs(window["clicks_per_interval"] - 0.5) < 1e-9
        assert window["inside"]
    assert abs(reading["k"] - 1.0) < 1e-9
    assert reading["ordinals_missing"] == 0
    assert reading["verdict"] == "met"
    # The same list against a pin it misses: the verdict moves.
    missed = dict(pinned, k=2.0, k_bracket=[1.8, 2.2], one_plus_z=3.0)
    assert tool.read_world(tmp_path, "age_4", missed, expected)["verdict"] in ("moved", "failed")


def test_a_slowed_detector_clicks_on_the_same_ticks(tmp_path):
    """(d), a minimal GameBoard: the rule the reading rests on."""

    def world(crowd_at_detector: bool) -> dict:
        measured: list[dict] = [
            {
                "position": [30, 4, 4],
                "family": "detector",
                "amount": 1,
                "fixed": True,
                "table": {"s_px1": {"rule": "measure", "reads": "age"}},
            },
            {
                "position": [10, 4, 4],
                "family": "s_px1",
                "amount": 1 << 20,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[1, 0, 0]]},
            },
        ]
        if crowd_at_detector:
            measured.append(
                {
                    "position": [30, 7, 4],
                    "family": "mass",
                    "amount": 4915 * (1 << 16),
                    "fixed": True,
                    "directions": [[0, -1, 0]],
                    "table": {"s_px1": {"rule": "pass"}},
                }
            )
        return {
            "law": "beam",
            "model_id": "shell-clock-slowed-detector-v1",
            "shape": [41, 9, 9],
            "boundary": "open",
            "ticks": 80,
            "K": 1 << 20,
            "N": 64,
            "release": [1, 1 << 16],
            "suspension": [1, 1 << 16],
            "width": 1,
            "families": [
                {"name": "detector", "quantum": 1},
                {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
                {"name": "s_px1", "quantum": 1},
            ],
            "measured": measured,
        }

    ticks = {}
    for crowd in (False, True):
        path = tmp_path / f"crowd_{crowd}.json"
        path.write_text(json.dumps(world(crowd)), encoding="utf-8")
        loaded = load_world(path.read_bytes(), base_dir=path.parent, root=path.parent)
        lines: list[dict] = []
        sim = NatureBeamSimulation(loaded.world, observer=lines.append)
        for _ in range(80):
            sim.step()
        ticks[crowd] = sorted(
            (line["tick"], line["record"] & 0xFFFFFFFF)
            for line in lines
            if line.get("event") == "click" and line.get("measured") == DETECTOR
        )
        detector = sim.measured[DETECTOR]
        assert (int(detector.waited) > 0) is crowd, "the crowd slows the detector's own clock"
    assert ticks[True] == ticks[False], "a slowed detector clicks on the same lattice ticks"
    assert len(ticks[False]) > 10


def test_a_shell_world_parses_and_runs_balanced():
    """(e)."""
    sim = simulation("age_4")
    assert len(sim.measured) == SHELL_NODES + 2
    for _ in range(2):
        sim.step()
    assert sim.books()["balanced"]

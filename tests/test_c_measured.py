"""Series Q, c measured behind a detector (`examples/events/c_measured/`,
`make_world.py`, `expectations.json`; the register's Q entry; the model
owner's "go for it" of 2026-09-21, record 236): the escape tick of every
direction of the fan derived from the closed form of the flight
(docs/DERIVATIONS_BEAM.md section 11.1) and compared with the run's clicks
on the open faces (an open face is a detector, an escape is a click). The
template is `tests/test_amplitude_cone.py`: the test derives and compares,
it holds no literal of a world's number (docs/TEST_EXPECTATIONS.md, "c
measured behind a detector").

(a) the register is the closed form: for every direction D of the lamp's
    fan (S_1 its Manhattan length, T_D = isqrt(3 |D|^2 Q^2) its
    resolution, line_D the engine's flight table's line) the first Link k
    whose Node is off the GameBoard, its age tau_k = ceil((2 k - 1) T_D /
    (2 S_1 Q)) (the first tau with m_D(tau) = floor((2 tau S_1 Q + T_D) /
    (2 T_D)) >= k), the click's tick birth + tau_k, its Node (after k - 1
    Links) and its face, the displacement after k Links and the pace
    |x_k - x_0|_2 / tau_k, equal to `expectations.json` row by row; the
    totals and the classes recomputed from the rows; the world's `ticks`
    past the last escape;
(b) the run: the world run headless in process births one record at the
    registered tick, every one of its rows clicks on a face at the derived
    tick, Node and face (the row's direction read off the engine's label
    table from the click's momentum), every direction once, one gather,
    the books balanced at the end;
(c) the readings tool reads the runner's record: the world run through the
    runner into a temporary folder, `tools/click_readings/c_measured.py`'s
    reading finds the registered births and clicks, no unmatched click,
    every escape at its derived row, the verdict inside; the same reading
    with one registered tick moved reads that row as differing.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from types import ModuleType

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import Q, nature_beam_tables
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "c_measured"
WORLD = WORLDS / "c_measured.json"
FACE_STEPS = {
    "face:+x": (1, 0, 0),
    "face:-x": (-1, 0, 0),
    "face:+y": (0, 1, 0),
    "face:-y": (0, -1, 0),
    "face:+z": (0, 0, 1),
    "face:-z": (0, 0, -1),
}


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def register() -> dict:
    found: dict = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    return found


@pytest.fixture(scope="module")
def world() -> dict:
    """The shipped world expanded (its family comes from the shipped
    definitions, `../entities/families.json`)."""
    found: dict = json.loads(
        load_world(WORLD.read_bytes(), base_dir=WORLDS, root=WORLDS.parent).expanded_source
    )
    return found


def derived_rows(world: dict, register: dict) -> dict[tuple[int, int, int], dict]:
    """The closed form's escape per direction of the lamp's fan: the Link
    count, the age, the tick, the Node, the face, the displacement and
    the pace (the derivation's 11.1), with the engine's flight table's
    lines as line_D."""
    parsed = parse_nature_beam_world(world)
    flight = nature_beam_tables(parsed).flight
    side = world["shape"][0]
    assert world["shape"] == [side, side, side]
    lamp = next(event for event in world["measured"] if "lamp" in event)
    centre = lamp["position"]
    birth_tick = int(register["birth_tick"])
    rows: dict[tuple[int, int, int], dict] = {}
    for vector in lamp["lamp"]["directions"]:
        direction = tuple(int(c) for c in vector)
        index = parsed.directions.index(direction)
        s1 = sum(abs(c) for c in direction)
        t = math.isqrt(3 * sum(c * c for c in direction) * Q * Q)
        assert int(flight.resolution[index]) == t
        line = [tuple(int(c) for c in flight.lines[index, j]) for j in range(s1)]
        position = list(centre)
        k = 0
        while True:
            step = line[k % s1]
            k += 1
            position = [p + s for p, s in zip(position, step, strict=True)]
            if any(p < 0 or p >= side for p in position):
                break
        tau = -(-(2 * k - 1) * t // (2 * s1 * Q))
        # The first age at which the closed form's count reaches k.
        assert (2 * tau * s1 * Q + t) // (2 * t) >= k > (2 * (tau - 1) * s1 * Q + t) // (2 * t)
        axis = next(a for a in range(3) if step[a])
        displacement = [p - c for p, c in zip(position, centre, strict=True)]
        distance_squared = sum(d * d for d in displacement)
        rows[direction] = {
            "direction": list(direction),
            "manhattan": s1,
            "resolution": t,
            "links": k,
            "age": tau,
            "tick": birth_tick + tau,
            "node": [p - s for p, s in zip(position, step, strict=True)],
            "face": f"face:{'+' if step[axis] > 0 else '-'}{'xyz'[axis]}",
            "displacement": displacement,
            "distance_squared": distance_squared,
            "pace": round(math.sqrt(distance_squared) / tau, 6),
            "asymptotic_pace": round(Q * math.sqrt(sum(c * c for c in direction)) / t, 6),
        }
    return rows


def summary(values: list[float]) -> dict:
    return {
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "mean": round(sum(values) / len(values), 6),
    }


def test_the_register_is_the_closed_form(world: dict, register: dict) -> None:
    rows = derived_rows(world, register)
    registered = {tuple(row["direction"]): row for row in register["directions"]}
    assert set(rows) == set(registered)
    assert register["fan"] == len(rows) == register["clicks"]
    assert register["Q"] == Q
    assert register["side"] == world["shape"][0] == 2 * register["half_width"] + 1
    for direction, row in rows.items():
        pinned = registered[direction]
        for key, value in row.items():
            assert pinned[key] == value, (direction, key)
    assert register["last_tick"] == max(row["tick"] for row in rows.values())
    assert world["ticks"] == register["ticks"] > register["last_tick"]
    assert register["pace"] == summary([row["pace"] for row in rows.values()])
    assert register["asymptotic_pace"] == summary([row["asymptotic_pace"] for row in rows.values()])
    assert register["c"] == round(1 / math.sqrt(3), 6)
    classes = register["classes"]
    assert sum(entry["count"] for entry in classes.values()) == len(rows)
    for name, entry in classes.items():
        members = [row for row in rows.values() if registered[tuple(row["direction"])]["class"] == name]
        assert entry["count"] == len(members)
        assert entry["ages"] == sorted({row["age"] for row in members})
        assert entry["pace"] == summary([row["pace"] for row in members])
    # The classes by the direction's magnitudes: an axis, a face diagonal,
    # a body diagonal, the rest.
    for direction, pinned in registered.items():
        magnitudes = sorted(abs(c) for c in direction)
        expected = {
            (0, 0, 1): "axes",
            (0, 1, 1): "face_diagonals",
            (1, 1, 1): "body_diagonals",
        }.get(tuple(magnitudes), "rest")
        assert pinned["class"] == expected


def observed(world: dict) -> tuple[list[dict], dict]:
    lines: list[dict] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"])):
        simulation.step()
    return lines, simulation.books()


def test_every_escape_click_is_the_derived_tick(world: dict, register: dict) -> None:
    rows = derived_rows(world, register)
    parsed = parse_nature_beam_world(world)
    flight = nature_beam_tables(parsed).flight
    by_label = {
        tuple(int(c) for c in flight.labels[index]): tuple(int(c) for c in vector)
        for index, vector in enumerate(parsed.directions)
    }
    lines, books = observed(world)
    births = [line for line in lines if line["event"] == "birth"]
    clicks = [line for line in lines if line["event"] == "click"]
    gathers = [line for line in lines if line["event"] == "gather"]
    assert [birth["tick"] for birth in births] == [register["birth_tick"]] * register["births"]
    assert births[0]["units"] == register["fan"]
    assert len(clicks) == register["clicks"]
    assert len(gathers) == register["births"]
    seen: list[tuple[int, int, int]] = []
    for click in clicks:
        assert click["detector"] in FACE_STEPS
        direction = by_label[tuple(click["momentum"])]
        row = rows[direction]
        assert click["tick"] == row["tick"], direction
        assert click["tick"] - births[0]["tick"] == row["age"], direction
        assert click["node"] == row["node"], direction
        assert click["detector"] == row["face"], direction
        assert click["amount"] == 1 and click["content"] == 1
        seen.append(direction)
    assert sorted(seen) == sorted(rows)
    for family in books["families"].values():
        for line in ("measured", "transit", "content"):
            assert family[line]["balanced"]
        assert family["transit"]["escaped"] == register["clicks"]


def test_the_readings_tool_reads_the_record(tmp_path: Path, register: dict) -> None:
    tool = load("c_measured_readings", ROOT / "tools" / "click_readings" / "c_measured.py")
    run = run_initialization(WORLD, tmp_path / "run").parent
    reading = tool.read_run(run, register)
    assert reading.status == "completed" and reading.balanced
    assert reading.births == [register["birth_tick"]] * register["births"]
    assert reading.gathers == register["births"]
    assert reading.clicks == len(reading.escapes) == register["clicks"]
    assert reading.unmatched == 0
    assert len(reading.directions_seen()) == register["fan"]
    assert reading.differing == []
    assert tool.verdict(reading, register)
    measured = summary([escape.pace for escape in reading.escapes])
    assert measured == register["pace"]
    lines = tool.report(reading, register)
    assert any(f"{register['clicks']} of {register['clicks']} at the derived" in line for line in lines)
    # The edge: a registered tick moved by one reads as a differing row.
    moved = json.loads(json.dumps(register))
    moved["directions"][0]["tick"] += 1
    reading_moved = tool.read_run(run, moved)
    assert [escape.direction for escape in reading_moved.differing] == [
        tuple(moved["directions"][0]["direction"])
    ]
    assert not tool.verdict(reading_moved, moved)

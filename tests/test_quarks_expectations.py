"""Series R, the quarks (`examples/events/quarks/`; the physicist's design
`docs/designs/quarks/QUARKS.md`): the register's pins are derived and
compared, never read as pinned numbers (the model owner, record 205: a
formula gives, a run proves; the template `tests/test_amplitude_cone.py`).

(a) the shipped worlds are the ones their generator writes, document by
    document, and each parses as a world of the law;
(b) the register's push per body at the reference tick
    (`expectations.json`, `pushes`) is derived from the world files by the
    design's `quark_numbers.py` (the one coupling over the columns, BEAM_LAW
    step 4, with the delivery of the fan's lines from the engine's flight
    table cut at the glue's lifetime) and compared entry by entry;
(c) the border's rows per interval and the read mass of every world are
    derived from the world files (290 rows per body, the sum of the
    declared contents) and compared;
(d) the design's pair table: the least strong value that binds each quark
    pair at one Link (u u 4896, d d 2448, u d 0) from the binding condition
    G_A G_B + M_A M_B > Q_A Q_B on the rows' charges.

(e) the register's `replay` block of every world (2026-09-21, after the
    crossing rule moved the fate readings): the engine's record of the
    first `cap` intervals by kind (the steps with their Nodes and the
    hand-overs, GAMEBOARD; the face clicks of the bodies that left,
    DETECTOR), written from the engine by `replay_register.py` and
    replayed here bit-exact, so the register cannot drift from the tree
    again; the fate's `engine_first_step` is the replay's first step.

(f) since the law's line drive (2026-09-22, the model owner's record 972):
    the worlds declare no drive key and load without the per-axis identity;
    every world's `former` block (the replay of 2026-09-21 under the
    per-axis drive of history) replays bit-exact under the world key
    `per_axis_drive`, so the rows of history stay reproducible;
(g) the kicked u's pace pins (`kick_pace`, GAMEBOARD, written by the
    generator before the run) are the drive rules' closed forms at M = 5,
    S = 2^37 and p = 10^13: 0.1635 under the line drive, 0.1853 per axis.
No number of a 3000-interval run is pinned here: the 3000-interval fates
are the register's readings (`tools/quarks_readings.py`).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

from event_universe.events import parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import PER_AXIS_DRIVE_RULE

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "quarks"
NAMES = (
    "q1_proton_line",
    "q2_neutron_line",
    "q3_proton_triangle",
    "q4_deuteron_rectangle",
    "q5_deuteron_line",
    "q6_proton_kick",
    "q7_proton_dressed",
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def numbers():
    return load("quark_numbers_design", ROOT / "docs" / "designs" / "quarks" / "quark_numbers.py")


@pytest.fixture(scope="module")
def register() -> dict[str, object]:
    found = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert found["format"] == "quarks-expectations-v1"
    assert set(found["derivations"]) == {
        "pushes",
        "border_rows_per_interval",
        "read_mass",
        "fate",
        "replay",
        "drive",
        "kick_pace",
    }
    assert found["drive"] == "line"
    return found


def shipped(name: str) -> dict[str, object]:
    return json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))


def shape_of(world: dict[str, object], numbers):
    """The design's shape (a body per measured event: its Node and what it
    holds) and the families with the glue's declared strong value."""
    glue = next(f for f in world["families"] if f["name"] == "glue")
    value = glue["columns"]["strong"]["value"]
    sigma = tuple(value) if isinstance(value, list) else int(value)
    families = numbers.families(numbers.quark_rows(), sigma=sigma)
    shape = {}
    for index, event in enumerate(world["measured"], start=1):
        held = {str(event["family"]): int(event["amount"]), "glue": int(event["held"]["glue"])}
        shape[str(index)] = (tuple(event["position"]), held)
    return shape, families


def test_the_shipped_worlds_are_the_generators():
    """(a)."""
    generator = load("quarks_make_worlds", WORLDS / "make_worlds.py")
    generated = generator.worlds()
    assert set(generated) == set(NAMES)
    for name in NAMES:
        assert shipped(name) == generated[name], name
        world = parse_nature_beam_world(shipped(name))
        assert {f.name for f in world.families} == {"u", "d", "glue"}, name
        # (f): the law's drive, nothing declared.
        assert "per_axis_drive" not in shipped(name)
        assert world.per_axis_drive is False and PER_AXIS_DRIVE_RULE not in world.hypotheses


@pytest.mark.parametrize("name", NAMES)
def test_the_pushes_of_the_register_are_derived_from_the_worlds(name: str, numbers, register):
    """(b)."""
    world = shipped(name)
    shape, families = shape_of(world, numbers)
    pinned = register["worlds"][name]
    if pinned["push_tick"] == 2:
        # The kicked world is read at tick 2, when the one-Link lines alone
        # have arrived (the age 1) and the kicked body has not yet stepped.
        families = {k: dict(v) for k, v in families.items()}
        for family in families.values():
            family["lifetime"] = 1
    derived = {n: list(v) for n, v in numbers.shape_pushes(shape, families).items()}
    assert derived == pinned["pushes"]


@pytest.mark.parametrize("name", NAMES)
def test_the_border_rows_and_the_read_mass_are_derived(name: str, numbers, register):
    """(c)."""
    world = shipped(name)
    shape, families = shape_of(world, numbers)
    pinned = register["worlds"][name]
    # The rows per interval are per self-creation of the bodies, read at the
    # border, a fixed detector at k = 0 whose tick is its own clock (record
    # 569); the tick 20 is the record's ordering (the clock audit of 2026-09-22).
    assert pinned["border_rows_per_interval"] == 290 * len(world["measured"])
    assert len(world["directions"]) + 6 == 290
    assert pinned["read_mass"] == sum(
        numbers.event_charges(held, families)[0] for _, held in shape.values()
    )


def test_the_least_strong_value_that_binds_each_pair(numbers):
    """(d)."""
    rows = numbers.quark_rows()
    families = numbers.families(rows)
    least = {}
    for a, b in (("u", "u"), ("u", "d"), ("d", "d")):
        m_a, q_a, _ = numbers.event_charges(numbers.quark(a, rows), families)
        m_b, q_b, _ = numbers.event_charges(numbers.quark(b, rows), families)
        need = q_a[0] * q_b[0] - m_a * m_b
        least[a + b] = math.isqrt(need) + 1 if need > 0 else 0
    assert least == {"uu": 4896, "ud": 0, "dd": 2448}
    assert rows["u"]["units"] == 4 and rows["d"]["units"] == 9
    assert rows["u"]["rho"] == (1224, 1) and rows["d"]["rho"] == (-272, 1)


@pytest.fixture(scope="module")
def readings_tool():
    return load("quarks_readings_tool", ROOT / "tools" / "quarks_readings.py")


@pytest.mark.parametrize("name", NAMES)
def test_the_replay_of_every_world_reads_as_registered(
    name: str, register, readings_tool, tmp_path: Path
):
    """(e)."""
    pinned = register["worlds"][name]
    replay = pinned["replay"]
    cap = int(replay["cap"])
    source = (WORLDS / f"{name}.json").read_bytes()
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(json.loads(source)), source, out, name, cap)
    assert readings_tool.replay_block(out, cap) == replay
    steps = replay["steps"]
    first = min((ticks[0][0] for ticks in steps.values() if ticks), default=None)
    assert pinned["fate"]["engine_first_step"] == first
    assert "step_every_about" not in pinned["fate"]


@pytest.mark.parametrize("name", NAMES)
def test_the_former_replay_of_every_world_reads_under_the_per_axis_drive(
    name: str, register, readings_tool, tmp_path: Path
):
    """(f)."""
    former = register["worlds"][name]["former"]
    assert former["drive"] == "per_axis"
    replay = former["replay"]
    cap = int(replay["cap"])
    document = shipped(name)
    document["per_axis_drive"] = True
    source = json.dumps(document).encode("utf-8")
    world = parse_nature_beam_world(json.loads(source))
    assert world.per_axis_drive is True and PER_AXIS_DRIVE_RULE in world.hypotheses
    out = tmp_path / "former"
    out.mkdir()
    execute_nature_beam_run(world, source, out, name, cap)
    assert readings_tool.replay_block(out, cap) == replay
    steps = replay["steps"]
    first = min((ticks[0][0] for ticks in steps.values() if ticks), default=None)
    assert former["engine_first_step"] == first


def test_the_kicked_pace_pins_are_the_drive_rules(register):
    """(g)."""
    generator = load("quarks_make_worlds_pins", WORLDS / "make_worlds.py")
    pinned = register["worlds"]["q6_proton_kick"]["kick_pace"]
    assert pinned == generator.kick_pins("line")
    p, m, s = 10**13, 5, 1 << 37
    assert pinned["content"] == m and generator.KICK == p and generator.WIDTH == s
    assert pinned["pace"] == p * 64 / (64 * 64 * s * m + p * 110)
    assert abs(pinned["pace"] - 0.1635) < 5e-5
    assert abs(pinned["intervals_per_link"] - 6.1) < 0.05
    assert pinned["per_axis"]["pace"] == p / (64 * s * m + p)
    assert abs(pinned["per_axis"]["pace"] - 0.1853) < 5e-5
    assert abs(pinned["per_axis"]["intervals_per_link"] - 5.4) < 0.05
    # The kicked u of history stepped at 6, 12, 19, 25, 32, 38, 45, 51, 58
    # (6 and 7 alternating, 6.5 per Link with the pushes on it); the line
    # drive's 6.1 before any push is the pin the run's steps are read beside.
    former = register["worlds"]["q6_proton_kick"]["former"]["replay"]["steps"]["1"]
    assert [t[0] for t in former] == [6, 12, 19, 25, 32, 38, 45, 51, 58]


def test_the_holds_line_is_a_diagnostic_out_of_the_deciding_set(readings_tool):
    """The fate of a set (no step, a step beyond three Links) reads the step
    records: a GameBoard line, printed and not counted; the pushes, the
    border and the read mass decide (records 562 and 564; the audit of
    record 567, F13)."""
    board = readings_tool.GAMEBOARD
    assert not readings_tool.deciding(
        f"[{board}] (a diagnostic, not counted: the step records) the set holds"
    )
    # The books are a gate of the record (GameBoard by ENGINE.md's table), out
    # of the readings count; a body's own push decides.
    assert not readings_tool.deciding(f"[{readings_tool.GATE}] the books (a gate of the record)")
    # The push per interval is per self-creation of the body, its own clock;
    # the tick it is read at is the record's ordering (the clock audit of
    # 2026-09-22): a DETECTOR pin that decides.
    assert readings_tool.deciding(f"[{readings_tool.DETECTOR}] body 1 (u): the push per interval")

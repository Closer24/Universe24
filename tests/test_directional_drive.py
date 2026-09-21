"""The directional drive (2026-09-21; docs/BEAM_LAW.md section 3 step 5 and
note 49; form B of docs/designs/light_speed/FORM.md section 3 with its map
`light_speed_map.py`; the model owner's record 191, the vector program, and
record 301, the build). A body of content M and momentum vector p walks the
digital line of D, the primitive direction nearest to p within the world's
`direction_bound`, with ONE accumulator on its record: `by_drive(drive,
|p|_1 S_1 Q, Q S M S_1 Q + |p|_1 T_D, at_most = 1)`, |p|_1 the Manhattan
norm of p, S_1 and T_D the direction's Manhattan length and resolution; the
Link at a fire is the line's next Manhattan step by the three deficit
accumulators of the line (`engine.line_step`, the flight's Bresenham
choice). The pace is |p|_1 / (Q S M) at a small momentum (Newton's limit,
isotropic in the Euclidean speed |p|_2 / (Q S M)) and bends to the rows'
S_1 Q / T_D as the momentum grows, never above it: c = 1 / sqrt 3 is the
cap of every body. One rule in isolation; no push arrives (`release` [0,
1]). The expected integers of docs/TEST_EXPECTATIONS.md ("The directional
drive"), derived from the formulas (the count floor(n rate / wall) at a
constant momentum, the Links on the flight's own line) and written down
before the first run:

(a) the map's four directions (FORM.md section 3, `light_speed_map.out` B):
    content M = 2^14 at width 1 (Q S M = 2^20) with |p|_1 = 2^20 on (1, 0,
    0), (1, 1, 0), (1, 1, 1) and (3, 1, 0) (the momenta (2^20, 0, 0), (2^19,
    2^19, 0), (349525, 349525, 349526) and (3 x 2^18, 2^18, 0); the third
    reads (1, 1, 1) through the direction's precision, its components
    shifted to within 2^15), on a periodic cube over 600 intervals: the
    displacements (220, 0, 0), (135, 135, 0), (100, 100, 100) and (190,
    63, 0), the Links made 220, 270, 300 and 253, exactly the map's; the
    Euclidean speeds 0.3667, 0.3182, 0.2887 and 0.3336 Links per interval
    (the formula's 0.3678, 0.3187, 0.2887, 0.3340 within the flight
    table's own rounding); every Link one Port; the books balanced;
(b) the cap: a body never makes more than S_1 Q / T_D Links per interval
    on its line. Content 1, width 1 (Q S M = 64): the bar's outrunning
    body of the derivation's 2.2, momentum (192, 0, 0) (v = 0.75 Links per
    interval = 1.29 c until the rule; now 12288 / 25216 = 0.4873), makes
    268 Links in 550 intervals, below the heading's 320 = 550 x 32 / 55;
    at the momentum 2^40 on a heading (v = 0.58182, the rows' 64 / 110
    less 2^-35) 31 Links in 55 and 319 in 550, never 32 per 55; on the
    cube diagonal (1, 1, 1) at (2^40, 2^40, 2^40) (T_D = 192 = S_1 Q: one
    Link per interval is the cap there) 54 in 55 and 549 in 550; after
    every interval n the Links made are floor(n rate / wall) and at most
    n S_1 Q / T_D;
(c) Newton's limit: at |p|_2 << Q S M the Euclidean speed is |p|_2 / (Q S
    M) within one Link over the run. Content 2^14, width 1, 4000
    intervals: (4096, 0, 0) makes (15, 0, 0) against Newton's 15.62; (2048,
    2048, 0) makes (8, 7, 0), 10.63 against 11.05; (1365, 1365, 1366)
    makes (5, 5, 5), 8.66 against 9.02 (its direction (1, 1, 1) read by the
    nearest-primitive scan, the primitive of the momentum itself lying
    beyond the bound 64);
(d) a body of no content walks as a row: `step_line` at content 0 on (1,
    0, 0), (1, 1, 0) and (5, -3, 2) over one period of the flight (55, 39
    and 683 intervals) makes the row's count of Links (32, 32, 640) on the
    row's own line and stands at the row's Node at the period's end ((32,
    0, 0), (16, 16, 0), (320, -192, 128)). THE PIN AS GIVEN, tick by tick
    with `Flight.walk_step`, IS NOT MET: each of the body's Links falls at
    the row's self-creation or the one after (the lags {0, 1} on all three
    directions), because the row's accumulator starts at the half of its
    wall (T_d, the rounding to the nearest: note 41 (viii), note 13 "every
    ray steps at its first interval") and a body's accumulator starts at 0
    as every count of a body does (note 41); the map's section D compared
    its own walk with itself, not with the engine's row. Stated in note 49;
    the pin here is the count, the Node and the lag;
(e) the reversal (record 126's case of `test_step_drive` (f) in form B): a
    body of content 16 on a bar with width 8 (Q S M = 8192; rate 65536,
    wall 636928 at |p| = 1024) with the momentum +1024 for eight
    self-creations (its drive 524288, no Link) and -1024 from the ninth:
    the line reverses ((1, 0, 0) to (-1, 0, 0), D_old . D < 0) and the
    drive is negated to -524288, the signed distance driven along the
    line; it then gains 65536 per self-creation, cancels the distance
    driven toward +x and fires the -x Link at the twenty-sixth
    self-creation (-524288 + 18 x 65536 = 655360 >= 636928; the drive
    18432 after it; the body at x = 4 until then, then 3), and after 30
    holds 280576 with `steps` 1 and `axis_steps` [1, 0, 0]; the line kept
    without the negation would have fired the -x Link at the tenth
    self-creation, the distance driven toward +x discharged the other
    way, record 126's defect; the same body under +1024 for eight and 0
    for twenty-two keeps its drive 524288, its line (1, 0, 0) and its
    Node; the record: `state.json` and `run.json` carry `drive` (one
    integer), `line` (the three deficits) and `direction` per measured
    event, the `step` line carries `drive` and `direction`, and a world
    that declares `drive` or `line` on a measured event is refused naming
    the unknown key;
(f) a momentum of 0 never steps and leaves the drive, the deficits and
    the line as they are: `step_line(7, [1, -1, 0], (1, 0, 0), [0, 0, 0],
    16, 1)` returns (None, 7, (1, 0, 0)) with the deficits untouched, and
    a body with momentum (0, 0, 0) stays at its Node over 50 intervals
    with `drive` 0 and `direction` (0, 0, 0);
(g) the crossing rule's marks on a diagonal walk (note 48): content 1,
    width 1, momentum (64, 64, 0) on a plane (rate 16384, wall 28160, v =
    0.5818 Links per interval, the rows' pace on (1, 1, 0) at that
    momentum's fraction): the Links at the self-creations 2, 4, 6, 7, 9
    on the axes x, y, x, y, x (the line of (1, 1, 0), x first on the tie),
    every `step` line with `step_port` 0 or 2 (one Link on one Port),
    `last_step_port` -1 but at tick 7 (0, the x Link of tick 6 right
    before it, `fast_steps` 1; the first draft of this pin wrote 2, a
    transcription slip corrected against the line's order before the
    pin was kept), the body at (7, 6, 0) from (4, 4, 0) after 10
    intervals with `axis_steps` [3, 2, 0], `steps` 5, the deficits [-1, 1,
    0] and the drive 23040; and the direction's choice (`body_direction`):
    (1024, 320, 0) reads (16, 5, 0), (-5, 0, 0) reads (-1, 0, 0), (2^40,
    0, 0) reads (1, 0, 0) (shifted to within 2^15), (1365, 1365, 1366)
    reads (1, 1, 1) by the scan, -p reads -D, a momentum whose primitive
    is within the bound reads it exactly at every scale (k D for k up to
    2^20 reads D), and every direction read is primitive within the bound
    and within 0.5 degrees of a momentum of components up to 2^30 drawn at
    random (two momenta on one ray beyond the bound may read neighbouring
    candidates: the read is within the precision, not scale-invariant);
    `line_step` over a period reproduces the flight's own line
    (`nature_beam._bresenham`) on (1, 0, 0), (1, 1, 0), (3, 1, 0), (5, -3,
    2) and (44, 7, 0), the deficits summing to 0 after every step; a wall
    beyond the integer bound is refused (`drive_rate_and_wall` at the
    momentum 2^62 - 1 on a heading).
"""

from __future__ import annotations

import json
import math
import random

import numpy as np
import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import body_direction, line_step, step_line
from event_universe.events.nature_beam import _bresenham, direction_flight, direction_resolution
from event_universe.events.world import LABEL_SCALE, MOMENTUM_BOUND, drive_rate_and_wall
from event_universe.runner import run_initialization

Q = LABEL_SCALE
FAMILY = {"name": "m", "quantum": 0, "charge": 0, "phase": False}


def cube(measured: list[dict[str, object]], ticks: int, **keys: object) -> dict[str, object]:
    """A periodic cube of 32^3 Nodes whose measured events release nothing."""
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "directional-drive-test",
        "shape": [32, 32, 32],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "age_bound": 64,
        "families": [FAMILY],
        "measured": measured,
    }
    world.update(keys)
    return world


def bar(measured: list[dict[str, object]], ticks: int, **keys: object) -> dict[str, object]:
    """An open bar of 64 x 1 x 1 (y and z periodic) whose measured events
    release nothing."""
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "directional-drive-test",
        "shape": [64, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [FAMILY],
        "measured": measured,
    }
    world.update(keys)
    return world


def mover(content: int, momentum: list[int], position: list[int]) -> dict[str, object]:
    return {"position": position, "family": "m", "amount": content, "momentum": momentum}


def run(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), records.append)
    for _ in range(int(str(world["ticks"]))):
        simulation.step()
    assert simulation.books()["balanced"]
    return simulation, records


def displacement(records: list[dict[str, object]], number: int) -> tuple[int, int, int]:
    """The sum of the headings of a body's Links, off its `step` lines."""
    found = [0, 0, 0]
    for line in records:
        if line["event"] == "step" and line["number"] == number:
            heading = PORT_HEADINGS[int(str(line["step_port"]))]
            found = [a + b for a, b in zip(found, heading, strict=True)]
    return found[0], found[1], found[2]


def rate_and_wall(momentum: list[int], content: int, width: int, direction: tuple[int, int, int]):
    manhattan = sum(abs(c) for c in direction)
    return drive_rate_and_wall(momentum, content, width, manhattan, direction_resolution(direction))


# -- (a) ---------------------------------------------------------------------------

MAP = {
    (1, 0, 0): ([1 << 20, 0, 0], (220, 0, 0), 0.3667),
    (1, 1, 0): ([1 << 19, 1 << 19, 0], (135, 135, 0), 0.3182),
    (1, 1, 1): ([349525, 349525, 349526], (100, 100, 100), 0.2887),
    (3, 1, 0): ([3 << 18, 1 << 18, 0], (190, 63, 0), 0.3336),
}


@pytest.mark.parametrize("direction", sorted(MAP))
def test_the_maps_four_directions(direction):
    """(a)."""
    momentum, expected, speed = MAP[direction]
    assert sum(abs(c) for c in momentum) == 1 << 20
    assert body_direction(momentum, 64) == direction
    simulation, records = run(cube([mover(1 << 14, momentum, [16, 16, 16])], 600))
    entry = simulation.measured[1]
    moved = displacement(records, 1)
    assert moved == expected
    made = sum(abs(c) for c in expected)
    assert entry.steps == made == sum(entry.axis_steps)
    assert round(math.hypot(*moved) / 600, 4) == speed
    rate, wall = rate_and_wall(momentum, 1 << 14, 1, direction)
    assert made == 600 * rate // wall
    assert entry.momentum == momentum and entry.line_direction == direction


# -- (b) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("momentum", "direction", "ticks", "expected", "cap"),
    [
        ([192, 0, 0], (1, 0, 0), 550, 268, 320),
        ([1 << 40, 0, 0], (1, 0, 0), 55, 31, 32),
        ([1 << 40, 0, 0], (1, 0, 0), 550, 319, 320),
        ([1 << 40, 1 << 40, 1 << 40], (1, 1, 1), 55, 54, 55),
        ([1 << 40, 1 << 40, 1 << 40], (1, 1, 1), 550, 549, 550),
    ],
)
def test_the_cap_is_the_rows_pace(momentum, direction, ticks, expected, cap):
    """(b)."""
    manhattan = sum(abs(c) for c in direction)
    resolution = direction_resolution(direction)
    assert cap == ticks * manhattan * Q // resolution
    rate, wall = rate_and_wall(momentum, 1, 1, direction)
    assert rate <= wall
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(cube([mover(1, momentum, [16, 16, 16])], ticks))
    )
    entry = simulation.measured[1]
    for tick in range(1, ticks + 1):
        simulation.step()
        assert entry.steps == tick * rate // wall, tick
        assert entry.steps * resolution <= tick * manhattan * Q, tick
    assert entry.steps == expected <= cap
    if momentum == [192, 0, 0]:
        # Until the rule the same body made floor(550 x 192 / 256) = 412 Links.
        assert 550 * 192 // (64 + 192) == 412 and round(rate / wall, 4) == 0.4873


# -- (c) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("momentum", "expected"),
    [([4096, 0, 0], (15, 0, 0)), ([2048, 2048, 0], (8, 7, 0)), ([1365, 1365, 1366], (5, 5, 5))],
)
def test_newtons_limit(momentum, expected):
    """(c)."""
    simulation, records = run(cube([mover(1 << 14, momentum, [16, 16, 16])], 4000))
    moved = displacement(records, 1)
    assert moved == expected
    newton = math.hypot(*momentum) / (1 << 20) * 4000
    assert abs(math.hypot(*moved) - newton) < 1
    assert simulation.measured[1].steps == sum(abs(c) for c in expected)


# -- (d) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("direction", "period", "links"), [((1, 0, 0), 55, 32), ((1, 1, 0), 39, 32), ((5, -3, 2), 683, 640)]
)
def test_a_body_of_no_content_walks_as_a_row(direction, period, links):
    """(d)."""
    flight = direction_flight(((0, 0, 0), (0, 0, 0), direction))
    assert int(flight.period[2]) == period
    row_ticks = []
    row_position = np.zeros(3, dtype=np.int64)
    for age in range(period):
        step = flight.walk_step(np.array([2]), np.array([age]))[0]
        if step.any():
            row_ticks.append(age + 1)
            row_position += step
    momentum = [1000 * c for c in direction]
    drive, deficits, line = 0, [0, 0, 0], (0, 0, 0)
    body_ticks = []
    body_position = [0, 0, 0]
    for tick in range(1, period + 1):
        fired, drive, line = step_line(drive, deficits, line, momentum, 0, 1)
        if fired is not None:
            axis, sign = fired
            body_ticks.append(tick)
            body_position[axis] += sign
    assert len(row_ticks) == len(body_ticks) == links
    assert tuple(int(v) for v in row_position) == tuple(body_position)
    assert tuple(body_position) == tuple(
        c * (links // sum(abs(v) for v in direction)) for c in direction
    )
    # The pin as given (tick by tick) is not met: each Link at the row's
    # self-creation or the one after, the row's accumulator starting at
    # the half of its wall and the body's at 0.
    lags = {b - r for b, r in zip(body_ticks, row_ticks, strict=True)}
    assert lags == {0, 1}, lags
    assert body_ticks != row_ticks


# -- (e) ---------------------------------------------------------------------------


def test_the_reversal_negates_the_drive_on_the_line(tmp_path):
    """(e)."""
    rate, wall = rate_and_wall([1024, 0, 0], 16, 8, (1, 0, 0))
    assert (rate, wall) == (65536, 636928)
    world = bar([mover(16, [1024, 0, 0], [4, 0, 0])], 30, width=8)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    positions = []
    for tick in range(1, 31):
        entry.momentum = [1024 if tick <= 8 else -1024, 0, 0]
        simulation.step()
        assert simulation.books()["balanced"], tick
        positions.append(entry.position[0])
        if tick <= 8:
            assert entry.drive == rate * tick and entry.line_direction == (1, 0, 0), tick
        elif tick < 26:
            assert entry.drive == -8 * rate + rate * (tick - 8) and entry.line_direction == (-1, 0, 0), (
                tick
            )
        elif tick == 26:
            assert entry.drive == -8 * rate + 18 * rate - wall == 18432, tick
    assert (
        positions[:25] == [4] * 25 and positions[25] == 3 and entry.drive == 18432 + 4 * rate == 280576
    )
    assert entry.steps == 1 and entry.axis_steps == [1, 0, 0]
    # The line kept without the negation would have fired at the tenth.
    assert 8 * rate + 2 * rate >= wall > 8 * rate + rate
    # A momentum that stops keeps the drive, the line and the Node.
    world = bar([mover(16, [1024, 0, 0], [4, 0, 0])], 30, width=8)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    for tick in range(1, 31):
        entry.momentum = [1024 if tick <= 8 else 0, 0, 0]
        simulation.step()
    assert entry.position == (4, 0, 0) and entry.drive == 8 * rate and entry.line_direction == (1, 0, 0)
    # The record: the runner's files carry the drive, the deficits and the
    # direction; the step line the drive and the direction.
    path = tmp_path / "world.json"
    path.write_text(json.dumps(bar([mover(16, [1024, 0, 0], [4, 0, 0])], 27, width=8)), encoding="utf-8")
    run_initialization(path, tmp_path / "run")
    record = json.loads((tmp_path / "run" / "run.json").read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    for measured in (record["measured"][0], state["measured"][0]):
        assert measured["drive"] == 27 * rate - 2 * wall == 495616
        assert measured["line"] == [0, 0, 0] and measured["direction"] == [1, 0, 0]
        assert measured["axis_steps"] == [2, 0, 0] and measured["steps"] == 2
    steps = [
        json.loads(line)
        for line in (tmp_path / "run" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if json.loads(line)["event"] == "step"
    ]
    assert [s["tick"] for s in steps] == [10, 20]
    assert [(s["drive"], s["direction"]) for s in steps] == [(10 * rate - wall, [1, 0, 0])] * 1 + [
        (20 * rate - 2 * wall, [1, 0, 0])
    ]
    for key in ("drive", "line"):
        declared = bar([{**mover(16, [1024, 0, 0], [4, 0, 0]), key: [5, 0, 0]}], 8)
        with pytest.raises(ValueError, match=f"unknown keys: {key}"):
            parse_nature_beam_world(declared)


# -- (f) ---------------------------------------------------------------------------


def test_a_momentum_of_zero_never_steps():
    """(f)."""
    deficits = [1, -1, 0]
    assert step_line(7, deficits, (1, 0, 0), [0, 0, 0], 16, 1) == (None, 7, (1, 0, 0))
    assert deficits == [1, -1, 0]
    simulation, records = run(bar([mover(16, [0, 0, 0], [4, 0, 0])], 50))
    entry = simulation.measured[1]
    assert entry.position == (4, 0, 0) and entry.drive == 0 and entry.line_direction == (0, 0, 0)
    assert not [r for r in records if r["event"] == "step"] and entry.steps == 0


# -- (g) ---------------------------------------------------------------------------


def test_the_crossing_marks_on_a_diagonal_walk():
    """(g)."""
    rate, wall = rate_and_wall([64, 64, 0], 1, 1, (1, 1, 0))
    assert (rate, wall) == (16384, 28160)
    world = cube([mover(1, [64, 64, 0], [4, 4, 0])], 10, shape=[64, 64, 1], boundary={"z": "periodic"})
    del world["age_bound"]
    simulation, records = run(world)
    entry = simulation.measured[1]
    steps = [r for r in records if r["event"] == "step"]
    assert [s["tick"] for s in steps] == [2, 4, 6, 7, 9]
    assert [s["step_port"] for s in steps] == [0, 2, 0, 2, 0]
    assert [s["last_step_port"] for s in steps] == [-1, -1, -1, 0, -1]
    assert simulation.fast_steps == 1
    assert entry.position == (7, 6, 0) and entry.axis_steps == [3, 2, 0] and entry.steps == 5
    assert entry.line == [-1, 1, 0] and entry.drive == 10 * rate - 5 * wall == 23040


def test_the_direction_read_from_the_momentum():
    """(g), the direction's choice."""
    assert body_direction([1024, 320, 0], 64) == (16, 5, 0)
    assert body_direction([-5, 0, 0], 64) == (-1, 0, 0)
    assert body_direction([1 << 40, 0, 0], 64) == (1, 0, 0)
    assert body_direction([1365, 1365, 1366], 64) == (1, 1, 1)
    assert body_direction([0, 0, 0], 64) == (0, 0, 0)
    draw = random.Random(2026_09_21)
    for _ in range(300):
        direction = tuple(draw.randint(-64, 64) for _ in range(3))
        if (
            not any(direction)
            or math.gcd(math.gcd(abs(direction[0]), abs(direction[1])), abs(direction[2])) != 1
        ):
            continue
        for scale in (1, 7, draw.randint(1, 1 << 20)):
            assert body_direction([scale * c for c in direction], 64) == direction, (direction, scale)
    for _ in range(300):
        momentum = [draw.randint(-(1 << 30), 1 << 30) for _ in range(3)]
        if not any(momentum):
            continue
        found = body_direction(momentum, 64)
        assert body_direction([-c for c in momentum], 64) == tuple(-c for c in found)
        assert max(abs(c) for c in found) <= 64
        assert math.gcd(math.gcd(abs(found[0]), abs(found[1])), abs(found[2])) == 1
        cosine = sum(a * b for a, b in zip(momentum, found, strict=True)) / (
            math.hypot(*momentum) * math.hypot(*found)
        )
        assert math.degrees(math.acos(min(1.0, cosine))) < 0.5, (momentum, found)


@pytest.mark.parametrize("direction", [(1, 0, 0), (1, 1, 0), (3, 1, 0), (5, -3, 2), (44, 7, 0)])
def test_the_line_step_is_the_flights_line(direction):
    """(g), the deficits against the flight's own line over a period."""
    line = _bresenham(direction)
    deficits = [0, 0, 0]
    for expected in line * 3:
        axis = line_step(deficits, direction)
        assert sum(deficits) == 0
        step = [0, 0, 0]
        step[axis] = 1 if direction[axis] > 0 else -1
        assert tuple(step) == expected
    assert deficits == [0, 0, 0]


def test_a_wall_beyond_the_bound_is_refused():
    """(g), the bound."""
    with pytest.raises(OverflowError, match="the drive's wall"):
        drive_rate_and_wall([MOMENTUM_BOUND, 0, 0], 1, 1, 1, 110)
    assert drive_rate_and_wall([1 << 20, 0, 0], 1 << 14, 1, 1, 110) == (
        1 << 26,
        (1 << 26) + 110 * (1 << 20),
    )

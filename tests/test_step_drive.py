"""The step drive (2026-09-20; docs/BEAM_LAW.md section 3 step 5 and note
17 as amended; docs/designs/hubble_stars/RULES.md section 1; the model
owner's "1 and 2 are very important for a solution and a new run" on the
finding of series G2). The count of Links a free measured event has made is
the whole part of the distance its momentum has driven, kept as one bounded
integer on the body's own record, `drive`; since the directional drive of
2026-09-21 (BEAM_LAW note 49; `tests/test_directional_drive.py`) the one
accumulator of the body's digital line: at every self-creation in which the
body may step `drive += |p|_1 S_1 Q`, and when `drive >= W` with W = Q S M
S_1 Q + |p|_1 T_D the body steps one Link, the line's next, and `drive -=
W` (until then one accumulator per axis at the rate p_a over D_a = Q S M +
|p_a|). The expected integers of docs/TEST_EXPECTATIONS.md ("The step
drive"), re-pinned on 2026-09-21 under the directional drive with the old
integers kept here as history (the pins derived from floor(n rate / wall)
and the flight's line before the first run):

(a) the identity at a constant momentum (the count primitive
    `core.integer.by_drive`, record 108, the whole part of an accumulated
    rate on the reader's record, `by_clock` where the rate is constant;
    the step rule reads it): on a bar of 4000 self-creations,
    for every momentum on the grid p in {1, 7, 64, 1000, 1024, 4095, 9215}
    at content 16 with width 8 and for content 1 with width 1 at
    p in {1, 5, 63, 64, 127}, on a heading (rate |p| x 64, wall Q S M x 64
    + |p| x 110), the self-creations at which the drive fires are exactly
    those at which `by_clock(n - 1, rate, wall)` is 1, and the drive after
    the n-th self-creation is `n rate mod wall`; the momentum -p walks the
    line (-1, 0, 0) with the same fires, -1 each, and the same drive (the
    sign is the line's; until 2026-09-21 the drive was -(n |p| mod D) and
    the fires where `by_clock(n - 1, |p|, D)` is 1, D = Q S M + |p|); the
    primitive at the rate -7 against 3 counts -1 at every self-creation;
    the shipped `test_push_width` cases (a) to (c) read their own
    re-pinned positions (their own module); on two axes (the physics-rule
    review's counterexample) a body of content 16 with the momentum
    (1024, 320, 0) from (4, 4, 0) walks the line of (16, 5, 0) (S_1 21, T_D
    1858; rate 1806336, wall 3873408) with the Links at the
    self-creations 3, 5, 7, 9, 11, 13, 16, 18, 20, 22, 24, the third,
    seventh and eleventh on y (the ticks 7, 16, 24), to (12, 7, 0) after 24
    with `axis_steps` [8, 3, 0], `steps` 11 and the drive 744576 (until
    2026-09-21, per axis with D = (2048, 1344): x at the even
    self-creations and y at 5, 9, 13, 17, 21, to (16, 9, 0) with
    `axis_steps` [12, 5, 0], `steps` 17 and the drives (0, 960, 0)); and
    the former coincidence, content 1 with (64, 64, 0), now the line of
    (1, 1, 0) (rate 16384, wall 28160): the Links at 2, 4, 6, 7, 9 on x,
    y, x, y, x, after 10 intervals (7, 6, 0), `axis_steps` [3, 2, 0],
    `steps` 5, the drive 23040 and the line's deficits [-1, 1, 0] (until
    2026-09-21 x stepped at the even self-creations and y lost every one
    of its coincident fires: (9, 4, 0), `axis_steps` [5, 5, 0], `steps` 5,
    the drives (0, 0, 0));
(b) the integrated distance under a halving momentum: a body of content
    16 on a bar with width 8 whose momentum is halved from outside after
    every 50th interval (4096, 2048, 1024, 512, 256, 128, 64, 32) makes,
    after 400 intervals, the Links of its integrated speed, sum over the
    intervals of |p| x 64 / (Q S M x 64 + |p| x 110) = 32.98, within 1 (32
    to 34; until 2026-09-21 the sum of |p| / (Q S M + |p|) = 38.0, 37 to
    39), where the rule before the drive made floor(400 x 32 / 8224) = 1;
    and the body never stands still for more than ceil(wall / rate) = 258
    intervals at the smallest momentum (257 until 2026-09-21);
(c) never two Links in one interval: under a momentum drawn at every
    interval from a seeded generator in [-D + 1, D - 1] on every axis
    (content 3, width 4, a 41^3 periodic cube with `age_bound`), over
    10 000 intervals every step moves the body by exactly one Link on one
    axis, |drive| stays below twice the largest wall of the draw after
    every interval (a residual earned at a larger momentum fires at the
    following self-creations, one Link each; the wall of a direction
    within the bound at |p|_1 up to 3 x 767: 2 x 37 711 872), and the
    line's three deficits sum to 0 after every interval;
(d) the record: `state.json` and `run.json` carry `drive` (one integer),
    `line`, `direction` and `axis_steps` per measured event, the `step`
    line carries `drive` and `direction` (content 16, width 8, momentum
    1024 over 27 intervals: the Links at the ticks 10 and 20, the drive
    495616 after 27, `axis_steps` [2, 0, 0]; until 2026-09-21 at 9, 18, 27
    with the drive 0 and `axis_steps` [3, 0, 0]), and a world that
    declares `drive` on a measured event is refused naming the unknown
    key;
(e) the turn by momentum unchanged at a constant momentum: the phases of
    `test_nature_beam_body` (d) (its own module) and, here, a body of
    content 16 with the momentum 320 and `action` 7 turning by 2925, 2926,
    2926, 2925 over its four Links in 24 intervals (the ticks 5, 10, 15,
    20; until 2026-09-21 five Links, the fifth turn 2926); and the
    `action` row's whole part at a Link not crossed, pinned before any
    change (BEAM_LAW note 41 (viii), the owner's item 9; the physics-rule
    review of no-tables, 2026-09-21, item 2): the body of (a) with the
    momentum (64, 64, 0) under `action` 7 at N = 64 walks the line of (1,
    1, 0), every Link crossed, and holds after 10 intervals `acc.action`
    [3, 2, 0] (the residues of three and two counts of |p| N = 4096 = 7 x
    585 + 1) and the phase 45 = (3 + 2) x 585 mod 64 (until 2026-09-21
    the coincident y fires were lost: `acc.action` [5, 5, 0], the phase 45
    from the x row alone, the y row's five whole parts never delivered);
(f) the signed drive under a reversal (the Boss's diagnosis of the
    deuteron under a suspension, record 126 of 2026-09-20), in form B (the
    line reversed and the drive negated, `test_directional_drive` (e)): a
    body of content 16 on a bar with width 8 (rate 65536, wall 636928)
    with the momentum +1024 for eight self-creations (its drive 524288, no
    Link) and -1024 from the ninth steps -x first at the twenty-sixth
    self-creation (-524288 + 18 x 65536 >= 636928), the body at x = 4
    until then, its drive 18432 after the step and 280576 after 30 (until
    2026-09-21: the drive as it was, |p| with the direction from the sign
    at the fire, stepped -x at the ninth self-creation, 8192 + 1024 = 9216;
    the signed drive counted 8192 - 1024 k and stepped -x at the
    twenty-fifth, 8192 - 17 x 1024 = -9216, the drive 0 after it and -5120
    after 30); the same body under +1024 for eight and 0 for twenty keeps
    its drive 524288 (8192 until 2026-09-21) and its Node;
(g) the bound pair under a suspension holds (the Boss's W1: the register's
    `deuteron_1` under the record form (its lamps birth records) with `suspension`
    [1, 134217728], a paid family `light`, a lamp of that family of
    content 8388608 at rate [1, 1] on +y beside the proton and a control
    lamp at (10, 10, 16), each read by a `sum` set of one Node four Links
    up +y): over 3000 intervals neither nucleon makes a step (every
    attempted step a hand-over; under the unsigned drive the same world
    holds for 2092 intervals and the neutron steps to (12, 10, 10) at
    tick 2093 with a positive momentum, the |p| it had accumulated toward
    the proton discharged away from it, the physics-rule reviewer's
    measurement on main), the books balanced at every tick; the hold is
    the rule's consequence given the pair's symmetry (the pushes exact
    mirrors, a hand-over zeroing both, the neutron's drive negated at
    every reversal), not a theorem for every pair.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from event_universe.core.integer import by_clock, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import step_line
from event_universe.events.nature_beam import direction_resolution
from event_universe.events.world import LABEL_SCALE, drive_rate_and_wall
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world

Q = LABEL_SCALE
T_HEADING = direction_resolution((1, 0, 0))


def bar(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "step-drive-test",
        "shape": [64, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 8,
        "K": 1024,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": measured,
    }
    world.update(keys)
    return world


def mover(content: int, momentum: list[int], position: list[int] | None = None) -> dict[str, object]:
    return {"position": position or [4, 0, 0], "family": "m", "amount": content, "momentum": momentum}


def heading_rate_and_wall(momentum: int, content: int, width: int) -> tuple[int, int]:
    return drive_rate_and_wall([momentum, 0, 0], content, width, 1, T_HEADING)


# -- (a) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("momentum", "content", "width"),
    [(p, 16, 8) for p in (1, 7, 64, 1000, 1024, 4095, 9215)] + [(p, 1, 1) for p in (1, 5, 63, 64, 127)],
)
def test_the_identity_at_a_constant_momentum(momentum, content, width):
    """(a)."""
    rate, wall = heading_rate_and_wall(momentum, content, width)
    assert (rate, wall) == (momentum * 64, Q * width * content * 64 + momentum * 110)
    drive, deficits, line = 0, [0, 0, 0], (0, 0, 0)
    for n in range(1, 4001):
        fired, drive, line = step_line(drive, deficits, line, [momentum, 0, 0], content, width)
        assert (fired == (0, 1)) == bool(by_clock(n - 1, rate, wall)), n
        assert drive == (n * rate) % wall and line == (1, 0, 0), n
    drive, deficits, line = 0, [0, 0, 0], (0, 0, 0)
    for n in range(1, 4001):
        fired, drive, line = step_line(drive, deficits, line, [-momentum, 0, 0], content, width)
        assert (fired == (0, -1)) == bool(by_clock(n - 1, rate, wall)), n
        assert drive == (n * rate) % wall and line == (-1, 0, 0), n
    # The count primitive itself (record 108): the same identity, and at a
    # rate beyond the denominator (7 against 3) 2 or 3 per self-creation as
    # by_clock gains them, the drive the remainder (the whole part, the
    # fraction-free law's default since 2026-09-20); with `at_most` 1, the
    # step's rule, one per self-creation and the residual kept (30 x 7 -
    # 30 x 3 = 120 after thirty).
    reach = Q * width * content + momentum
    drive = 0
    for n in range(1, 401):
        fired, drive = by_drive(drive, momentum, reach)
        assert fired == by_clock(n - 1, momentum, reach) and drive == (n * momentum) % reach, n
    drive, gained = 0, []
    for n in range(1, 31):
        fired, drive = by_drive(drive, 7, 3)
        gained.append(fired)
        assert fired == by_clock(n - 1, 7, 3) and drive == (7 * n) % 3, n
    assert gained[:6] == [2, 2, 3, 2, 2, 3] and sum(gained) == 70 and drive == 0
    drive, gained = 0, []
    for _ in range(30):
        fired, drive = by_drive(drive, 7, 3, at_most=1)
        gained.append(fired)
    assert set(gained) == {1} and drive == 30 * 7 - 30 * 3
    with pytest.raises(ValueError, match="positive denominator"):
        by_drive(0, 1, 0)
    drive, gained = 0, []
    for _ in range(30):
        fired, drive = by_drive(drive, -7, 3)
        gained.append(fired)
    assert gained[:6] == [-2, -2, -3, -2, -2, -3] and sum(gained) == -70 and drive == 0
    drive, gained = 0, []
    for _ in range(30):
        fired, drive = by_drive(drive, -7, 3, at_most=1)
        gained.append(fired)
    assert set(gained) == {-1} and drive == -(30 * 7 - 30 * 3)


def test_the_identity_on_two_axes():
    """(a), two axes: one drive on the line of the momentum's direction."""
    world = bar([mover(16, [1024, 320, 0], position=[4, 4, 0])], shape=[64, 64, 1], ticks=24)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    rate, wall = drive_rate_and_wall([1024, 320, 0], 16, 1, 21, direction_resolution((16, 5, 0)))
    assert (rate, wall) == (1806336, 3873408)
    ys = [4]
    ticks = []
    for n in range(1, 25):
        before = entry.position
        simulation.step()
        assert entry.drive == (n * rate) % wall and entry.line_direction == (16, 5, 0), n
        if entry.position != before:
            ticks.append(n)
        ys.append(entry.position[1])
    assert ticks == [3, 5, 7, 9, 11, 13, 16, 18, 20, 22, 24]
    assert entry.position == (12, 7, 0) and entry.axis_steps == [8, 3, 0] and entry.steps == 11
    assert entry.drive == 744576
    assert [n for n in range(1, 25) if ys[n] != ys[n - 1]] == [7, 16, 24]
    world = bar([mover(1, [64, 64, 0], position=[4, 4, 0])], shape=[64, 64, 1], ticks=10)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    positions = []
    for _ in range(10):
        simulation.step()
        positions.append(entry.position)
    assert positions == [
        (4, 4, 0),
        (5, 4, 0),
        (5, 4, 0),
        (5, 5, 0),
        (5, 5, 0),
        (6, 5, 0),
        (6, 6, 0),
        (6, 6, 0),
        (7, 6, 0),
        (7, 6, 0),
    ]
    assert entry.axis_steps == [3, 2, 0] and entry.steps == 5 and entry.drive == 23040
    assert entry.line == [-1, 1, 0] and entry.line_direction == (1, 1, 0)


# -- (b) ---------------------------------------------------------------------------


def test_the_integrated_distance_under_a_halving_momentum():
    """(b)."""
    momenta = [4096 >> k for k in range(8)]
    world = bar([mover(16, [momenta[0], 0, 0])], width=8, ticks=400)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    positions = []
    for tick in range(1, 401):
        entry.momentum = [momenta[(tick - 1) // 50], 0, 0]
        simulation.step()
        assert simulation.books()["balanced"], tick
        positions.append(entry.position[0])
        rate, wall = heading_rate_and_wall(entry.momentum[0], 16, 8)
        assert 0 <= entry.drive < wall + rate, tick  # one sign: never negative
    # The integrated speed: sum over the intervals of rate / wall.
    driven = sum(50 * r / w for r, w in (heading_rate_and_wall(p, 16, 8) for p in momenta))
    links = positions[-1] - 4
    assert abs(links - driven) <= 1, (links, driven)
    assert links in (32, 33, 34), links
    assert round(driven, 2) == 32.98
    assert (400 * momenta[-1]) // (Q * 8 * 16 + momenta[-1]) == 1
    # No stall longer than the smallest momentum's own period.
    rate, wall = heading_rate_and_wall(momenta[-1], 16, 8)
    assert -(-wall // rate) == 258
    stall = 0
    for before, after in zip(positions, positions[1:], strict=False):
        stall = stall + 1 if after == before else 0
        assert stall <= -(-wall // rate), stall


# -- (c) ---------------------------------------------------------------------------


def test_never_two_links_in_one_interval():
    """(c)."""
    content, width = 3, 4
    reach = Q * width * content
    world = bar(
        [mover(content, [0, 0, 0], position=[20, 20, 20])],
        shape=[41, 41, 41],
        boundary={"x": "periodic", "y": "periodic", "z": "periodic"},
        age_bound=64,
        ticks=10_000,
    )
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    draw = random.Random(2026_09_20)
    steps = 0
    # The largest wall of the draw: the cube diagonal (64, 64, 64) at
    # |p|_1 = 3 x 767 (S_1 192, T_D 12288).
    largest_wall = reach * 192 * Q + 3 * (reach - 1) * direction_resolution((64, 64, 64))
    assert largest_wall == 37711872
    for tick in range(1, 10_001):
        entry.momentum = [draw.randint(-(reach - 1), reach - 1) for _ in range(3)]
        before = entry.position
        simulation.step()
        moved = [(entry.position[a] - before[a]) % 41 for a in range(3)]
        moved = [m - 41 if m > 20 else m for m in moved]
        assert sum(abs(m) for m in moved) <= 1, (tick, moved)
        steps += sum(abs(m) for m in moved)
        assert abs(entry.drive) < 2 * largest_wall, tick
        assert sum(entry.line) == 0, tick
    assert steps == entry.steps > 1000


# -- (d) ---------------------------------------------------------------------------


def test_the_record_carries_the_drive_and_a_declared_drive_is_refused(tmp_path):
    """(d)."""
    world = bar([mover(16, [1024, 0, 0])], width=8, ticks=27)
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    run_initialization(path, tmp_path / "run")
    record = json.loads((tmp_path / "run" / "run.json").read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    measured = next(m for m in record["measured"] if m["number"] == 1)
    # 27 self-creations at the rate 65536 over the wall 636928: two Links,
    # the drive 27 x 65536 - 2 x 636928 = 495616.
    rate, wall = heading_rate_and_wall(1024, 16, 8)
    assert (rate, wall) == (65536, 636928)
    assert measured["drive"] == 27 * rate - 2 * wall == 495616 and measured["axis_steps"] == [2, 0, 0]
    assert (
        measured["steps"] == 2 and measured["line"] == [0, 0, 0] and measured["direction"] == [1, 0, 0]
    )
    assert next(m for m in state["measured"] if m["number"] == 1)["drive"] == 495616
    steps = [
        json.loads(line)
        for line in (tmp_path / "run" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if json.loads(line)["event"] == "step"
    ]
    assert [s["tick"] for s in steps] == [10, 20]
    assert [s["drive"] for s in steps] == [10 * rate - wall, 20 * rate - 2 * wall]
    assert [s["direction"] for s in steps] == [[1, 0, 0]] * 2
    declared = bar([{**mover(16, [1024, 0, 0]), "drive": [5, 0, 0]}])
    with pytest.raises(ValueError, match="unknown keys: drive"):
        parse_nature_beam_world(declared)


# -- (e) ---------------------------------------------------------------------------


def test_the_turn_by_momentum_is_unchanged_at_a_constant_momentum():
    """(e)."""
    world = bar(
        [{**mover(16, [320, 0, 0]), "phase": 5, "phase_by_momentum": True}],
        action=7,
        ticks=24,
        families=[{"name": "m", "quantum": 0, "charge": 0}],
    )
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    turns = []
    ticks = []
    phase = entry.phase
    for tick in range(1, 25):
        before = entry.position[0]
        simulation.step()
        if entry.position[0] != before:
            turns.append((entry.phase - phase) % 64)
            ticks.append(tick)
        phase = entry.phase
    assert ticks == [5, 10, 15, 20]
    assert turns == [t % 64 for t in (2925, 2926, 2926, 2925)]
    assert entry.axis_steps == [4, 0, 0]


def test_the_action_rows_whole_part_at_a_link_not_crossed_is_pinned():
    """(e), the body of (a) on the line of (1, 1, 0) under `action`: every
    Link crossed, both rows' whole parts delivered, their residues kept."""
    world = bar(
        [{**mover(1, [64, 64, 0], position=[4, 4, 0]), "phase": 0, "phase_by_momentum": True}],
        action=7,
        ticks=10,
        shape=[64, 64, 1],
        families=[{"name": "m", "quantum": 0, "charge": 0}],
    )
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    for _ in range(10):
        simulation.step()
    assert entry.position == (7, 6, 0) and entry.axis_steps == [3, 2, 0] and entry.steps == 5
    assert entry.drive == 23040
    assert 64 * 64 == 7 * 585 + 1
    assert entry.counts.values("action") == [3, 2, 0]
    assert entry.state()["acc"]["action"] == [3, 2, 0]
    assert entry.phase == (5 * 585) % 64 == 45


# -- (f) ---------------------------------------------------------------------------


def test_the_signed_drive_under_a_reversal():
    """(f)."""
    rate, wall = heading_rate_and_wall(1024, 16, 8)
    assert (rate, wall) == (65536, 636928)
    world = bar([mover(16, [1024, 0, 0])], width=8, ticks=30)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    positions = []
    for tick in range(1, 31):
        entry.momentum = [1024 if tick <= 8 else -1024, 0, 0]
        simulation.step()
        assert simulation.books()["balanced"], tick
        positions.append(entry.position[0])
        if tick <= 8:
            assert entry.drive == rate * tick, tick
        elif tick < 26:
            assert entry.drive == -8 * rate + rate * (tick - 8), tick
        elif tick == 26:
            assert entry.drive == 18432, tick
    assert positions[:25] == [4] * 25 and positions[25] == 3 and entry.drive == 280576
    assert entry.steps == 1 and entry.axis_steps == [1, 0, 0]
    # The primitive alone: a positive rate never fires a negated drive
    # before the distance is cancelled.
    drive = -8 * rate
    fired = [by_drive(drive, rate, wall, at_most=1)[0]]
    assert fired == [0]
    # A momentum that stops keeps the drive and the Node.
    world = bar([mover(16, [1024, 0, 0])], width=8, ticks=28)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    for tick in range(1, 29):
        entry.momentum = [1024 if tick <= 8 else 0, 0, 0]
        simulation.step()
    assert entry.position == (4, 0, 0) and entry.drive == 8 * rate == 524288


# -- (g) ---------------------------------------------------------------------------


def deuteron_under_a_suspension() -> dict[str, object]:
    """The Boss's W1: the register's deuteron under the record click and a
    suspension, with a lamp beside the proton and a control lamp, each read
    by a `sum` set four Links up +y."""
    root = Path(__file__).resolve().parents[1]
    path = root / "examples" / "events" / "nucleus" / "deuteron_1.json"
    # Through the loader: the shipped world takes its families from the
    # definitions beside its series (2026-09-20); the document below is the
    # expanded one, its families inline.
    document = json.loads(load_world(path.read_bytes(), base_dir=path.parent).expanded_source)
    document["model_id"] = "beam-nucleus-deuteron_1-suspended-test"
    # The world key `amplitude` is deleted (the amplitude law (vii-4), the
    # one click): the lamps below birth records by the record form as the
    # key made them do.
    document["suspension"] = [1, 134217728]
    document["families"].append({"name": "light", "quantum": 1})
    document["families"].append({"name": "counter", "quantum": 1})
    for measured in document["measured"]:
        measured.setdefault("table", {})
        measured["table"]["light"] = "pass"
        measured["table"]["counter"] = "pass"
    lamp = {
        "amount": 8388608,
        "phase": 0,
        "fixed": True,
        "lamp": {"rate": [1, 1], "directions": [[0, 1, 0]], "turns": [8]},
        "table": {"p": "pass", "n": "pass", "nuclear": "pass", "counter": "pass"},
    }
    document["measured"].append({**lamp, "position": [10, 11, 10], "family": "light"})
    document["measured"].append({**lamp, "position": [10, 10, 16], "family": "light"})
    counter = {
        "family": "counter",
        "amount": 1,
        "fixed": True,
        "table": {"light": "measure", "p": "pass", "n": "pass", "nuclear": "pass"},
    }
    document["measured"].append({**counter, "position": [10, 15, 10]})
    document["measured"].append({**counter, "position": [10, 14, 16]})
    document["detectors"] = [
        {"name": "beside", "positions": [[10, 15, 10]], "threshold": 1, "reading": "sum"},
        {"name": "control", "positions": [[10, 14, 16]], "threshold": 1, "reading": "sum"},
    ]
    return document


def test_the_bound_pair_under_a_suspension_holds():
    """(g)."""
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(deuteron_under_a_suspension()), records.append
    )
    proton, neutron = simulation.measured[1], simulation.measured[2]
    for tick in range(1, 3001):
        simulation.step()
        if tick % 250 == 0:
            assert simulation.books()["balanced"], tick
        assert proton.position == (10, 10, 10) and neutron.position == (11, 10, 10), tick
    assert simulation.books()["balanced"]
    # No Link made: every attempted step a hand-over (`steps` counts the
    # rule's fires, the `step` records the Links).
    assert not [r for r in records if r["event"] == "step"]
    assert len([r for r in records if r["event"] == "contact"]) == proton.steps + neutron.steps > 0

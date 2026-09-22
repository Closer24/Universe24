"""The step drive (2026-09-20; docs/BEAM_LAW.md section 3 step 5 and note
17 as amended; docs/designs/hubble_stars/RULES.md section 1; the model
owner's "1 and 2 are very important for a solution and a new run" on the
finding of series G2). The count of Links a free measured event has made on
an axis is the whole part of the distance its momentum has driven, kept as
one bounded integer per axis on the body's own record, `drive`: at every
self-creation in which the body may step, `drive += |p|`, and when `drive
>= D` with D = Q x S x M + |p| the body steps one Link and `drive -= D`.
The expected integers of docs/TEST_EXPECTATIONS.md ("The step drive"),
written down before the first run:

(a) the identity at a constant momentum (the count primitive
    `core.integer.by_drive`, record 108, the whole part of an accumulated
    rate on the reader's record, `by_clock` where the rate is constant;
    the step rule reads it): on a bar of 4000 self-creations,
    for every |p| / D on the grid p in {1, 7, 64, 1000, 1024, 4095, 9215}
    with D = 9216 (content 16, width 8) and for content 1 with width 1 at
    p in {1, 5, 63, 64, 127}, the self-creations at which the drive fires
    are exactly those at which `by_clock(n - 1, |p|, D)` is 1, and the
    drive after the n-th self-creation is `n |p| mod D` with the sign of
    p (the signed drive of record 126; the primitive at the rate -7
    against 3 counts -1 at every self-creation); the shipped
    `test_push_width` cases (a) to (c) read the same positions and
    `steps` as before (their own module); on two axes (the physics-rule
    review's counterexample) a body of content 16 with the momentum
    (1024, 320, 0) from (4, 4, 0), D = (2048, 1344), steps x at the even
    self-creations and y at 5, 9, 13, 17, 21 (its drive 320 n mod 1344 on
    every self-creation, whether x stepped or not), to (16, 9, 0) after
    24 with `axis_steps` [12, 5, 0], `steps` 17 and the drives (0, 960,
    0); and at the coincidence, content 1 with (64, 64, 0), D = 128 on
    both, x steps at the even self-creations and y loses every one of
    its: after 10 intervals (9, 4, 0), `axis_steps` [5, 5, 0], `steps` 5,
    the drives (0, 0, 0), as `by_clock` on each axis with the coincident
    step lost;
(b) the integrated distance under a halving momentum: a body of content
    16 on a bar with width 8 whose momentum is halved from outside after
    every 50th interval (4096, 2048, 1024, 512, 256, 128, 64, 32) makes,
    after 400 intervals, the Links of its integrated speed, sum over the
    intervals of |p| / (Q S M + |p|) = 38.0, within 1 (37 to 39), where
    the rule as it was made floor(400 x 32 / 8224) = 1; and the body
    never stands still for more than ceil((Q S M + |p|) / |p|) = 257
    intervals at the smallest momentum;
(c) never two Links in one interval: under a momentum drawn at every
    interval from a seeded generator in [-D + 1, D - 1] on every axis
    (content 3, width 4, a 41^3 periodic cube with `age_bound`), over
    10 000 intervals every step moves the body by exactly one Link on one
    axis, and |drive| stays below D_max on every axis after every
    interval, D_max = 2 x Q x S x M - 1 the largest D of the draw (a
    residual earned at a larger momentum fires at the following
    self-creations, one Link each);
(d) the record: `state.json` and `run.json` carry `drive` and
    `axis_steps` per measured event, the `step` line carries `drive`, and
    a world that declares `drive` on a measured event is refused naming
    the unknown key;
(e) the turn by momentum unchanged at a constant momentum: the phases of
    `test_nature_beam_body` (d) (its own module) and, here, a body of
    content 16 with the momentum 320 and `action` 7 turning by 2925, 2926,
    2926, 2925, 2926 over its first five Links; and the `action` row's
    whole part at a Link not crossed, pinned before any change (BEAM_LAW
    note 41 (viii), the owner's item 9; the physics-rule review of
    no-tables, 2026-09-21, item 2): the coincidence body of (a) (content
    1, the momentum (64, 64, 0), D = 128 on both axes) under `action` 7
    at N = 64 holds, after 10 intervals, `acc.action` [5, 5, 0] (the
    residue of five counts of |p| N = 4096 = 7 x 585 + 1 on each axis)
    and the phase 45 = 5 x 585 mod 64 from the x row alone, the y row's
    five whole parts, 2925, never delivered (26 with them);
(f) the signed drive under a reversal (the Boss's diagnosis of the
    deuteron under a suspension, record 126 of 2026-09-20): a body of
    content 16 on a bar with width 8 (D = 9216) with the momentum +1024
    for eight self-creations (its drive 8192, no Link) and -1024 from the
    ninth: the drive as it was, |p| with the direction from the sign at
    the fire, stepped -x at the ninth self-creation (8192 + 1024 = 9216);
    the signed drive counts 8192 - 1024 k and steps -x first at the
    twenty-fifth self-creation (8192 - 17 x 1024 = -9216), the body at
    x = 4 until then, its `drive` on the record -9216 + 9216 = 0 after the
    step; the same body under +1024 for eight and 0 for twenty keeps its
    drive 8192 and its Node;
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
    mirrors, a hand-over zeroing both, the neutron's signed drive never
    above 0), not a theorem for every pair.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from event_universe.core.integer import by_clock, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import step_axis
from event_universe.events.world import LABEL_SCALE
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world

Q = LABEL_SCALE


def bar(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    """The bar of the per-axis drive, under its key `per_axis_drive` (the
    drive of history since the line drive became the law's on 2026-09-22;
    `tests/test_drive_b.py` tests the law's): every integer below is the
    per-axis rule's as registered."""
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
        "per_axis_drive": True,
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": measured,
    }
    world.update(keys)
    return world


def mover(content: int, momentum: list[int], position: list[int] | None = None) -> dict[str, object]:
    return {"position": position or [4, 0, 0], "family": "m", "amount": content, "momentum": momentum}


# -- (a) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("momentum", "content", "width"),
    [(p, 16, 8) for p in (1, 7, 64, 1000, 1024, 4095, 9215)] + [(p, 1, 1) for p in (1, 5, 63, 64, 127)],
)
def test_the_identity_at_a_constant_momentum(momentum, content, width):
    """(a)."""
    reach = Q * width * content + momentum
    drive = 0
    for n in range(1, 4001):
        sign, drive = step_axis(drive, momentum, content, width)
        assert (sign == 1) == bool(by_clock(n - 1, momentum, reach)), n
        assert drive == (n * momentum) % reach, n
    drive = 0
    for n in range(1, 4001):
        sign, drive = step_axis(drive, -momentum, content, width)
        assert (sign == -1) == bool(by_clock(n - 1, momentum, reach)), n
        assert drive == -((n * momentum) % reach), n
    # The count primitive itself (record 108): the same identity, and at a
    # rate beyond the denominator (7 against 3) 2 or 3 per self-creation as
    # by_clock gains them, the drive the remainder (the whole part, the
    # fraction-free law's default since 2026-09-20); with `at_most` 1, the
    # step's rule, one per self-creation and the residual kept (30 x 7 -
    # 30 x 3 = 120 after thirty).
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
    """(a), two axes: the drive of every axis advances at every
    self-creation, the coincident Link of the later axis is lost."""
    world = bar([mover(16, [1024, 320, 0], position=[4, 4, 0])], shape=[64, 64, 1], ticks=24)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    ys = [4]
    for n in range(1, 25):
        simulation.step()
        assert entry.drive == [(n * 1024) % 2048, (n * 320) % 1344, 0], n
        assert entry.position[0] == 4 + n // 2, n
        ys.append(entry.position[1])
    assert entry.position == (16, 9, 0) and entry.axis_steps == [12, 5, 0] and entry.steps == 17
    assert [n for n in range(1, 25) if ys[n] != ys[n - 1]] == [5, 9, 13, 17, 21]
    world = bar([mover(1, [64, 64, 0], position=[4, 4, 0])], shape=[64, 64, 1], ticks=10)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    for n in range(1, 11):
        simulation.step()
        assert entry.position == (4 + n // 2, 4, 0), n
    assert entry.axis_steps == [5, 5, 0] and entry.steps == 5 and entry.drive == [0, 0, 0]


# -- (b) ---------------------------------------------------------------------------


def test_the_integrated_distance_under_a_halving_momentum():
    """(b)."""
    reach = Q * 8 * 16
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
        assert 0 <= entry.drive[0] < reach + entry.momentum[0], tick  # one sign: never negative
    # The integrated speed: sum over the intervals of |p| / (Q S M + |p|).
    driven = sum(50 * p / (reach + p) for p in momenta)
    links = positions[-1] - 4
    assert abs(links - driven) <= 1, (links, driven)
    assert links in (37, 38, 39), links
    assert (400 * momenta[-1]) // (reach + momenta[-1]) == 1
    # No stall longer than the smallest momentum's own period.
    stall = 0
    for before, after in zip(positions, positions[1:], strict=False):
        stall = stall + 1 if after == before else 0
        assert stall <= (reach + momenta[-1] + momenta[-1] - 1) // momenta[-1], stall


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
    for tick in range(1, 10_001):
        entry.momentum = [draw.randint(-(reach - 1), reach - 1) for _ in range(3)]
        before = entry.position
        simulation.step()
        moved = [(entry.position[a] - before[a]) % 41 for a in range(3)]
        moved = [m - 41 if m > 20 else m for m in moved]
        assert sum(abs(m) for m in moved) <= 1, (tick, moved)
        steps += sum(abs(m) for m in moved)
        for axis in range(3):
            # The drive stays below the largest D of the draw, 2 x reach - 1:
            # a residual earned at a larger momentum fires at the next
            # self-creations, one Link each, never two in one.
            assert abs(entry.drive[axis]) < 2 * reach - 1, (tick, axis)
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
    # 27 self-creations at p = 1024 over D = 9216: three steps, the drive
    # 27 x 1024 - 3 x 9216 = 0.
    assert measured["drive"] == [0, 0, 0] and measured["axis_steps"] == [3, 0, 0]
    assert measured["steps"] == 3
    assert next(m for m in state["measured"] if m["number"] == 1)["drive"] == [0, 0, 0]
    steps = [
        json.loads(line)
        for line in (tmp_path / "run" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if json.loads(line)["event"] == "step"
    ]
    assert [s["tick"] for s in steps] == [9, 18, 27]
    assert [s["drive"] for s in steps] == [[0, 0, 0]] * 3
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
    phase = entry.phase
    for _ in range(24):
        before = entry.position[0]
        simulation.step()
        if entry.position[0] != before:
            turns.append((entry.phase - phase) % 64)
        phase = entry.phase
    assert turns == [t % 64 for t in (2925, 2926, 2926, 2925, 2926)]
    assert entry.axis_steps == [5, 0, 0]


def test_the_action_rows_whole_part_at_a_link_not_crossed_is_pinned():
    """(e), the coincidence body under `action`: the y row's whole parts
    are discarded at the Links lost, its residue kept."""
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
    assert entry.position == (9, 4, 0) and entry.axis_steps == [5, 5, 0] and entry.steps == 5
    assert entry.drive == [0, 0, 0]
    assert 64 * 64 == 7 * 585 + 1
    assert entry.counts.values("action") == [5, 5, 0]
    assert entry.state()["acc"]["action"] == [5, 5, 0]
    assert entry.phase == (5 * 585) % 64 == 45
    assert (2 * 5 * 585) % 64 == 26


# -- (f) ---------------------------------------------------------------------------


def test_the_signed_drive_under_a_reversal():
    """(f)."""
    reach = Q * 8 * 16 + 1024
    assert reach == 9216
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
            assert entry.drive[0] == 1024 * tick, tick
        elif tick < 25:
            assert entry.drive[0] == 8192 - 1024 * (tick - 8), tick
        elif tick == 25:
            assert entry.drive[0] == 0, tick
    assert positions[:24] == [4] * 24 and positions[24] == 3 and entry.drive[0] == -5 * 1024
    assert entry.steps == 1 and entry.axis_steps == [1, 0, 0]
    # The primitive alone: the rule as it was fired at the ninth.
    drive = 0
    for _ in range(8):
        _, drive = by_drive(drive, 1024, reach)
    assert drive == 8192
    fired = [by_drive(drive, -1024, reach)[0]]
    assert fired == [0]
    # A momentum that stops keeps the drive and the Node.
    world = bar([mover(16, [1024, 0, 0])], width=8, ticks=28)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    for tick in range(1, 29):
        entry.momentum = [1024 if tick <= 8 else 0, 0, 0]
        simulation.step()
    assert entry.position == (4, 0, 0) and entry.drive == [8192, 0, 0]


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
        "lamp": {"wheel": [1, 64], "rate": [1, 1], "directions": [[0, 1, 0]], "turns": [8]},
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
    # The generic entry of the bending (2026-09-22, record 847; the price,
    # docs/designs/one_wall/GENERIC_BENDING_PRICE.md): the lamps' light rows
    # in the nucleons' crowd at d = 2^27 are pushed, and a pushed row's
    # momentum Q d content u_D + W makes the wall's square exceed the
    # working bound, the contract's refusal at interval 4; before the entry
    # the declared world ran its 3000 intervals with the lines below.
    declared = deuteron_under_a_suspension()
    simulation = NatureBeamSimulation(parse_nature_beam_world(declared))
    with pytest.raises(OverflowError, match="exceeds the working bound"):
        for _ in range(3001):
            simulation.step()
    assert simulation.tick == 4  # the refused interval's tick
    # The bound pair on the nucleons, whose tables pass the light: the same
    # world without the lamps and the counters (the light takes no part in
    # the lines below; the families stay declared), 3000 intervals.
    document = dict(declared)
    document["measured"] = [
        m for m in declared["measured"] if m.get("family") not in ("light", "counter")
    ]
    document["detectors"] = []
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
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

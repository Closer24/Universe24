"""Every family under one wall, step 3 (2026-09-22, the model owner's "finish
form B"; docs/designs/one_wall/BODY_DRIVE.md): a body's directional drive
(form B, built as `drive-b-v1` under the world key `drive_b`; the law's line
drive since 2026-09-22, the key deleted, record 972) joins the age wall's set
under `optical` at the coefficient gamma, the space part alone (the body's
clock, the member `owed` at 1, carries the time part; the two sum to the
flight's 1 + gamma), and a moving body's gravity charge under the two keys
is the pair (w, Q S), the rows' weight (E'^2 + 3 gamma p . p) // E' on the
body's own momentum over the label scale. The expected integers of
docs/TEST_EXPECTATIONS.md ("The body's drive under the one wall"), written
before the first run:

(o) the set: with `optical` under the per-axis drive of history (the world
    key `per_axis_drive`) the flight at 1 + gamma and no drive member; with
    `optical` under the law's line drive (since 2026-09-22; built as the
    key `drive_b` beside `optical`) the drive at gamma (0 at gamma 0,
    declared and unstretched; 1 at gamma 1); the clock at 1 throughout;
    `turn` and `action` never members;
(p) a body on a rest crowd, integer for integer: a bar of 14 x 1 x 1 at
    `suspension` [1, 4], `width` 1, `optical` 1 under the law, the body of
    content 64 (Q S M = 4096, W = 262144 + 660000 = 922144) at x = 0 with
    p = (6000, 0, 0), the rest crowd of m (amount 4, age 3, the age moment
    12) at x = 4 .. 8: off the crowd the drive gains 6000 x 64 x 4 =
    1536000 per self-creation against 922144 x 4 = 3688576, one Link per
    2.4 self-creations, nothing owed; on it the wall is 922144 x (4 + 12)
    = 14754304, one Link per 9.6 self-creations, and the clock owes
    by_drive(acc_owed, 12, 4) = 3 intervals per self-creation, so a Link
    per 38.4 intervals: the body's x at every one of 120 ticks equals the
    host's chain of `age_wall`, `by_line` and `count_owed` in the engine's
    order (the frame, the move, the reading, the count owed); at gamma 0
    the wall is unstretched and the clock alone slows the body (a Link per
    9.6 intervals on the crowd);
(q) the weight (the model owner's word of 2026-09-23, record 1054's form
    B): a body at rest weighs M. `body_weight` at rest, content 64, S =
    16384, gamma 1 is (2^26, 2^20), the content over 1 exactly; moving at
    p = (2^26, 0, 0) (Q S M = 2^26, E' = isqrt(2^52 + 3 x 2^52) = 2^27
    exactly, gamma_L = 2, v^2 = 3/4) it is (7 x 2^25, 2^20) at gamma 1
    (1 + gamma v^2 = 7/4); a body of no content (0, 1). The pair is
    formed at gamma above 0 alone: the push by hand of an m row of amount
    1 arriving from -y at the body's Node (V = (0, 64, 0)) is -4096 on y
    (-M V, gravity's Lambda 1) with the key absent and under `optical` 0
    alike, a body at gamma 0 weighing M whatever its momentum, and
    -14336 under `optical` 1 (7/4 of gamma_L times it, Lambda Q S = 2^20).
    The edge at the pair's domain (Q S M)^2 <= 2^63 - 1, M <= 2896 at S
    = 16384: at rest the content 2896 weighs (2896 x 2^20, 2^20) at gamma
    1 and 2897 is refused naming the working bound, while at gamma 0 the
    body of content 2897 loads and is pushed by -M V = -185408, the pair
    never formed. The weight's test at gamma 0 (the pair (2^27, 2^20) and
    the push -8192 of the flip day) is given up by the owner's word;
(r) the refusal: a moving body under `optical` with the per-axis drive of
    history (`per_axis_drive`) is refused at load naming the key; a fixed
    body and a body at rest
    load; a body whose (Q S M)^2 leaves the working bound is refused
    naming the rule;
(t) the deciding worlds (`examples/events/optical/body_*.json`, the
    register `body_expectations.json`): the fifteen worlds load under both
    keys with the light worlds' mass 2^16 and the body's momentum
    (2^26, 0, 0) at `width` 16384; the pins as the note's section 4 has
    them (body_b10_g1: tick 168 from (56, 23, 20); the controls 150).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.core.integer import MAX_WORK_INT, age_wall, by_line
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import count_owed
from event_universe.events.measured import (
    DRIVE_MEMBER,
    FLIGHT_MEMBER,
    age_wall_coefficient,
    age_wall_set,
)
from event_universe.events.world import HEADING_OFFSET, T_HEADING, Q, body_weight, drive_wall
from event_universe.world_loading import load_world

PLUS_Y = HEADING_OFFSET + 2
# The twelve diagonals of the optical tests' fan: every heading has a
# neighbour within a right angle, the key's condition at load.
DIAGONALS = (
    [[a, b, 0] for a in (1, -1) for b in (1, -1)]
    + [[a, 0, c] for a in (1, -1) for c in (1, -1)]
    + [[0, b, c] for b in (1, -1) for c in (1, -1)]
)
FAMILIES = [
    {"name": "probe", "quantum": 0, "charge": 0, "phase": False},
    {"name": "m", "quantum": 0, "charge": 0, "phase": False},
]


def crowd_bar(optical: int | None, *, per_axis: bool = False, ticks: int = 120) -> dict[str, object]:
    """(p): the body of content 64 at x = 0 with p = (6000, 0, 0) and the
    rest crowd of m at x = 4 .. 8 (number 2, amount 4, age 3)."""
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "test-optical-body-bar",
        "shape": [14, 1, 1],
        "boundary": "open",
        "ticks": ticks,
        "K": 4096,
        "N": 64,
        "release": [0, 1],
        "suspension": [1, 4],
        "width": 1,
        "directions": DIAGONALS,
        "families": FAMILIES,
        "measured": [
            {"position": [0, 0, 0], "family": "probe", "amount": 64, "momentum": [6000, 0, 0]},
            # The crowd's own number: a fixed m at the bar's end, out of reach.
            {
                "position": [13, 0, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "table": {"probe": "pass"},
            },
        ],
        "in_transit": [
            {
                "position": [x, 0, 0],
                "family": "m",
                "number": 2,
                "direction": 0,
                "amount": 4,
                "phase": 0,
                "age": 3,
            }
            for x in range(4, 9)
        ],
    }
    if optical is not None:
        document["optical"] = optical
    if per_axis:
        document["per_axis_drive"] = True
    return document


def push_bar(
    optical: int | None,
    *,
    per_axis: bool = False,
    momentum: list[int] | None = None,
    amount: int = 64,
) -> dict[str, object]:
    """(q): the body of content 64 at S = 16384 (Q S M = 2^26) at (2, 1, 0)
    with p = (2^26, 0, 0), an m row of amount 1 arriving from -y at tick 1
    (the pair [1, 16384]: the key needs n > 0; nothing owed or stretched
    within the four ticks, the row's age moment 1 against d)."""
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "test-optical-body-push",
        "shape": [6, 3, 1],
        "boundary": "open",
        "ticks": 4,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": [1, 16384],
        "width": 16384,
        "directions": DIAGONALS,
        "families": FAMILIES,
        "measured": [
            {
                "position": [2, 1, 0],
                "family": "probe",
                "amount": amount,
                "momentum": [1 << 26, 0, 0] if momentum is None else momentum,
            },
            # The row's own number: a fixed m off the row's line and the body's.
            {
                "position": [5, 2, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "table": {"probe": "pass"},
            },
        ],
        "in_transit": [
            {
                "position": [2, 0, 0],
                "family": "m",
                "number": 2,
                "direction": PLUS_Y,
                "amount": 1,
                "phase": 0,
            },
        ],
    }
    if optical is not None:
        document["optical"] = optical
    if per_axis:
        document["per_axis_drive"] = True
    return document


def test_the_drive_joins_the_age_walls_set_at_gamma_beside_the_clock_and_the_flight():
    """(o). Since the generic entry of the bending (2026-09-22) the flight is
    a member for every world at 1 + gamma, gamma 0 by default, and since the
    line drive is the law's (the same day) the drive member joins at gamma
    with nothing else declared; under the per-axis drive of history
    (`per_axis_drive`) it never does."""
    assert age_wall_set() == (("owed", 1), (FLIGHT_MEMBER, 1), (DRIVE_MEMBER, 0))
    assert age_wall_set(1, True) == (("owed", 1), (FLIGHT_MEMBER, 2))
    assert age_wall_set(1) == (("owed", 1), (FLIGHT_MEMBER, 2), (DRIVE_MEMBER, 1))
    assert age_wall_set(0) == (("owed", 1), (FLIGHT_MEMBER, 1), (DRIVE_MEMBER, 0))
    assert age_wall_coefficient(DRIVE_MEMBER, 1) == 1
    assert age_wall_coefficient("owed", 1) == 1
    with pytest.raises(ValueError, match="not a member"):
        age_wall_coefficient(DRIVE_MEMBER, 1, True)
    with pytest.raises(ValueError, match="never a member"):
        age_wall_coefficient("action", 1)


def by_hand(gamma: int, ticks: int) -> list[int]:
    """The body's x after every tick by the engine's primitives in its order."""
    wall0 = drive_wall([6000, 0, 0], 64, 1)
    assert wall0 == Q * Q * 64 + 6000 * T_HEADING == 922144
    rates0 = [6000 * Q, 0, 0]
    drive = [0, 0, 0]
    x, counted, owed, acc_owed = 0, 0, 0, 0
    found = []
    for _ in range(ticks):
        creating = owed == 0
        if not creating:
            owed -= 1
        if creating:
            coefficient = age_wall_coefficient(DRIVE_MEMBER, gamma)
            if coefficient:
                scaled, wall = age_wall(1, wall0, coefficient, counted, (1, 4))
                rates = [r * scaled for r in rates0]
            else:
                rates, wall = rates0, wall0
            chosen, sign, drive = by_line(drive, rates, wall)
            if chosen is not None and x + sign != 13:
                x += sign  # a step onto the fixed m at x = 13 is refused, the wall paid
        counted = 12 if 4 <= x <= 8 else 0
        if creating:
            owed, acc_owed = count_owed(acc_owed, counted, (1, 4))
        found.append(x)
    return found


@pytest.mark.parametrize("gamma", [1, 0])
def test_a_body_on_a_rest_crowd_walks_by_the_stretched_drive_and_its_slowed_clock(gamma: int):
    """(p)."""
    ticks = 120
    expected = by_hand(gamma, ticks)
    simulation = NatureBeamSimulation(parse_nature_beam_world(crowd_bar(gamma, ticks=ticks)))
    body = simulation.measured[1]
    found = []
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        found.append(int(body.position[0]))
    assert found == expected
    # Off the crowd a Link per 2.4 self-creations (x = 4 at tick 10); on it
    # the stretched wall with the slowed clock (gamma 1: x = 5 and 6 at the
    # ticks 50 and 86, 36 to 40 intervals apart) or the clock alone (gamma
    # 0: x = 5 .. 8 at 22, 30, 38, 50, a Link per 8 to 12 intervals, the
    # clock owing 3 per self-creation on the crowd; then off the crowd to
    # x = 12 by tick 65, the step onto the fixed m at 13 refused).
    assert found[9] == 4
    crossings = [found.index(x) + 1 for x in range(4, 9) if x in found]
    assert crossings == ([10, 50, 86] if gamma == 1 else [10, 22, 30, 38, 50])
    assert found[-1] == (6 if gamma == 1 else 12)


def test_a_body_at_rest_weighs_its_content_and_the_pair_is_gammas_rule_above_zero():
    """(q): a body at rest weighs M; the pair (w, Q S) is the gravitational
    charge of a moving body at gamma above 0 alone (the model owner's word
    of 2026-09-23, record 1054's form B; docs/designs/one_wall/BODY_DRIVE.md
    D5), at gamma 0 the content M over 1 whatever the momentum."""
    # Inputs: at rest the pair is (Q S M, Q S), the content over 1 exactly.
    assert body_weight([0, 0, 0], 64, 16384, 1) == (1 << 26, 1 << 20)
    assert body_weight([1 << 26, 0, 0], 64, 16384, 1) == (7 << 25, 1 << 20)
    assert body_weight([1 << 26, 0, 0], 0, 16384, 1) == (0, 1)
    # The edge at the pair's domain (Q S M)^2 <= 2^63 - 1: M = 2896 at
    # S = 16384 is the last content whose pair forms; 2897 is refused
    # naming the working bound (docs/designs/drive_b/DEFAULT.md (d)).
    assert body_weight([0, 0, 0], 2896, 16384, 1) == (2896 << 20, 1 << 20)
    with pytest.raises(OverflowError, match="working bound"):
        body_weight([0, 0, 0], 2897, 16384, 1)
    # Expected: the push by one m row -M V at gamma 0 (the key absent or
    # 0 alike; gravity's Lambda 1) and gamma_L (1 + gamma v^2) times it at
    # gamma 1 over the scale Q S; at gamma 0 the body past the pair's
    # bound loads and is pushed by -M V, the pair never formed, and at
    # gamma 1 the same body is refused at load naming the working bound.
    for optical, amount, push, scale in (
        (None, 64, -4096, 1),
        (0, 64, -4096, 1),
        (1, 64, -14336, 1 << 20),
        (0, 2897, -185408, 1),
    ):
        world = parse_nature_beam_world(push_bar(optical, amount=amount))
        assert world.column_scales[0] == scale
        simulation = NatureBeamSimulation(world)
        simulation.step()
        assert simulation.books()["balanced"]
        assert simulation.measured[1].momentum == [1 << 26, push, 0]
    with pytest.raises(OverflowError, match="working bound"):
        parse_nature_beam_world(push_bar(1, amount=2897))


def test_a_moving_body_under_optical_needs_the_directional_drive():
    """(r): a moving body under `optical` is refused with the per-axis drive
    of history (`per_axis_drive`), never a member of the age wall's set; a
    body at rest and a fixed body are admitted with it."""
    with pytest.raises(ValueError, match="per_axis_drive"):
        parse_nature_beam_world(push_bar(1, per_axis=True))
    parse_nature_beam_world(push_bar(1, per_axis=True, momentum=[0, 0, 0]))
    document = push_bar(1, per_axis=True)
    document["measured"][0]["fixed"] = True  # type: ignore[index]
    parse_nature_beam_world(document)
    with pytest.raises(OverflowError, match="working bound"):
        body_weight([0, 0, 0], MAX_WORK_INT // (Q * 16384) + 1, 16384, 1)


WORLDS = Path(__file__).resolve().parents[1] / "examples" / "events" / "optical"


def test_the_body_worlds_load_under_both_keys_and_carry_their_pins():
    """(t)."""
    register = json.loads((WORLDS / "body_expectations.json").read_text(encoding="utf-8"))
    pins = register["worlds"]
    assert pins["body_b10_g1"]["click"] == {
        "tick": 168,
        "tolerance": 1,
        "face": "face:+x",
        "node": [56, 23, 20],
        "links_before": [54, -7, 0],
    }
    assert pins["body_b10_g1"]["refuting_readings"] == {
        "drive_unstretched": {"tick": 164, "y": 23},
        "charge_content_over_one": {"tick": 159, "y": 29},
    }
    # At gamma 0 a body weighs M (2026-09-23, the owner's form B): the pin
    # is the walk at the charge (M, 1), the pair's walk its refuting
    # reading, the former pin (the pair at every gamma) kept beside.
    assert pins["body_b10_g0"]["click"]["tick"] == 156
    assert pins["body_b10_g0"]["click"]["node"] == [56, 29, 20]
    assert pins["body_b10_g0"]["refuting_readings"] == {
        "drive_unstretched": {"tick": 156, "y": 29},
        "charge_pair_over_label_scale": {"tick": 159, "y": 27},
    }
    assert pins["body_b10_g0"]["former"]["click"]["tick"] == 159
    assert pins["body_b10_g0"]["former"]["click"]["node"] == [56, 27, 20]
    assert "former" not in pins["body_b10_g1"]
    for b in (10, 12, 14, 16, 18):
        for name in (f"body_b{b}_g0", f"body_b{b}_g1", f"body_control_b{b}"):
            loaded = load_world(
                (WORLDS / f"{name}.json").read_bytes(), base_dir=WORLDS, root=WORLDS.parent
            )
            world = loaded.world
            assert not world.per_axis_drive and world.optical is not None and world.width == 16384
            body = world.measured[0]
            assert list(body.momentum) == [1 << 26, 0, 0] and tuple(body.position) == (2, 20 + b, 20)
            # Gravity's Lambda is Q S where the weight pair is formed, at
            # gamma > 0 alone, gamma's rule (the model owner's word of
            # 2026-09-23, form B); at gamma 0 the body weighs M, the scale 1.
            assert not body.fixed and world.column_scales[0] == (1 << 20 if world.optical > 0 else 1)
            if name.startswith("body_control"):
                assert len(world.measured) == 1
            else:
                assert world.measured[1].fixed and world.measured[1].amount == 1 << 16
            assert pins[name]["click"]["tick"] == (
                150 if "control" in name else pins[name]["click"]["tick"]
            )

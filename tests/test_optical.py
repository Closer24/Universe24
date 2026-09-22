"""optical-v1 in its generic form (the model owner's "go" of 2026-09-21,
record 303, "clearly, in the generic form" of records 421 to 428; the
design docs/designs/one_wall/NOTE.md at 12423748 with REVIEW_3's four
must-fixes and the physicist's fifth; the key `optical: gamma`, absent by
default). One rule per case, the integers written before the run:

(a) verb 1, the wall of the flight: a bar of 12 x 1 x 1 at `suspension`
    [1, 4] and `optical` 1 (f = 2), a lamp of `light` at x = 0 birthing one
    row per interval on +x from tick 1, a rest crowd of `m` (number 2,
    amount 4, age 3: the age moment A = 12 at every Node it sits on) at
    x = 4 .. 8: the first row's flight accumulator is the one wall
    function on the flight's pair, the rate 2 S_1 Q d = 512 against the
    wall 2 T_D (d + f n A) = 220 x 4 = 880 off the crowd and 220 x 28 = 6160
    on it (`core.integer.age_wall`), from the start T_D d = 440: its x
    after the ticks 2 .. 40 is 1, 1, 2, 2, 3, 3, then 4 for twelve
    intervals (one Link per 12 intervals, 1.72 x (1 + 2 x 12 / 4)), 5 for
    twelve, 6 ..., integer for integer with `by_drive` by hand; its stored
    (made, residue) after tick 2 is (1, 72); without the key the same
    row walks 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 10, 11
    (the flight off the age) and its fields stay (0, 0);
(b) verb 2 and 3, the push and the turn: a GameBoard of 6 x 3 x 1 at
    [1, 4] and `optical` 1, the table with the twelve edge diagonals; a row
    of `light` (number 1, amount 1, content 1) at (1, 1, 0) on +x and a row
    of `m` (number 2, amount 2) at (2, 0, 0) on +y, both at age 0: in
    interval 1 both walk to (2, 1, 0), the m row's arrival is the flow
    **V** = (0, 128, 0) the light row reads at its Node, and its push
    accumulator becomes **W** = -n x (1 + gamma) x content x e_D x **V** =
    -(1 x 2 x 1 x 110) x (0, 128, 0) = (0, -28160, 0); its whole momentum
    **P** = Q d content **u**_x + **W** = (16384, -28160, 0); verb 3 by
    Bresenham (record 536; (i)) reads the next Link of +x and of its fan
    neighbours at the row's place (made 1): +x offers (1, 0, 0) with the
    error |(1, 0, 0) x **P**|^2 = 28160^2, (1, -1, 0) offers (0, -1, 0)
    (advancing, **h** . **P** = 28160 > 0) with 16384^2, (1, 1, 0)'s
    (0, 1, 0) and (1, 0, +-1)'s (0, 0, +-1) do not advance; the label
    moves to (1, -1, 0) and **W** += Q d content (**u**_x - **u**_(1,-1,0))
    = 256 x (19, 45, 0): **W** = (4864, -16640, 0), **P** conserved, the
    residue 72 of the heading rescaled at the push to the momentum's
    units, 72 x 87 = 6264 (**P** over its gcd 512 is (32, -55, 0), S_1 87;
    (j)) and not at the turn; the
    books' `turned` line of `light` (-19, -45, 0) (the label (45, -45, 0)
    less (64, 0, 0)) and the transit momentum (45, 83, 0) (the light's
    label and the m row's (0, 128, 0)) balanced; the m row (a free family,
    content 0) never turns; with an m row of amount 1 (**P** at -40.7
    degrees) +x's Link keeps the smaller error, 14080^2 against 16384^2,
    and the row keeps +x;
(c) **P** is conserved across the turn: Q d content **u**_D + **W** before
    equals Q d content **u**_D' + **W** after, (16384, -28160, 0), the
    row's amount, content, number and phase untouched;
(d) the refusals at load, naming the rule: `optical` with `suspension` 0,
    with `meeting`, gamma -1, true, "2" or 1.5, the six headings alone
    (a direction without a neighbour within a right angle), and the key
    `massive_rows` beside it (the composed flight of massive rows under
    the optical key is not reviewed, record 510; each key alone parses); a world with the key carries the identity `optical-v1` and
    `run.json`'s block {"gamma", "flight_coefficient"};
(e) byte identity without the key: a world without `optical` has every
    row's `made`, `residue` and turn fields 0 through its run and its
    state's rows carry no `flight` or `push` key (the gate set's digests
    are `tests/test_amplitude_click.py` (d)); the set of the age wall is
    the law's without the key and gains ("flight", 1 + gamma) with it, the
    phase per age never a member;
(f) the pin worlds (`examples/events/optical/`): the six shipped worlds
    equal their generator's, parse with the identity, run ten intervals
    balanced, and the register carries the pins before the run (the
    shifts -1.93 / -3.86 and -2.42 / -4.83 pixels, the delays, the ratio
    2.00 with its bracket); the inverse interval is refused under the key;
(g) M1 of the physics-rule review of 408cf719 (record 494) under the
    chief physicist's words on the residue's units (record 496) and on the
    pace of a pushed row ((j)): the flight's accumulator is the row's age
    paid at its rate r = 2 S_1 Q d, the count capped at one Link by the
    primitive's `at_most` with the surplus kept; the pair (S_1, T) is the
    label's until the row is pushed and the momentum's from then on, the
    residue rescaled at the push by S_1(P) / S_1(D) (floor) as the time of
    the last Link, and not at the label's turn. A GameBoard of 40 x 3 x 1
    at [1, 64] and `optical` 1, the fan the twelve edge diagonals with
    (24, +-1, 0) (T_D 2662, S_1 25; the heading's 110, 1); a row of `light`
    pushed once by a row of `m` arriving at its Node. From (1, 0, 0) at
    age 5 (its pair (3, 90 x 64)) pushed at (1, 1, 0) to **P** =
    (262144, 14080, 0), the primitive (1024, 55, 0) with S_1 1079 and
    T 113675: the residue 13952 becomes 13952 x 1079 = 15054208 (the
    time 13952 / 8192 = 15054208 / 8839168 unchanged), the rate 8839168
    against the wall 227350 x (64 + 2 A); the chain of (made, residue)
    after each interval (3, 15054208), (4, 8888276) (A = 1), (5, 3177044),
    ..., (11, 13105492), (12, 7394260) at interval 15, where the label
    moves to (24, 1, 0) by Bresenham with no rescale, (13, 1683028), ...,
    the label +x through interval 14 and (24, 1, 0) from 15, integer for
    integer with `by_drive` at `at_most` 1. From (24, 1, 0) at age 4 (its
    pair (2, 4814 x 64)) pushed at (2, 1, 0) to **P** = (262144, -1792, 0),
    the primitive (1024, -7, 0) with S_1 1031 and T 113514: the residue
    172160 of the label becomes 172160 x 1031 // 25 = 7099878 (the
    remainder 10 of 25 dropped, under one unit of the accumulator), the
    chain (3, 7099878), (4, 561982) (A = 1), (4, 9007934), ..., (11,
    8650814), (12, 2566974) at interval 16, where the label moves to
    (1, 0, 0) with no rescale, (12, 11012926), (13, 4929086), the label
    (24, 1, 0) through interval 15 and (1, 0, 0) from 16. The head before
    M1 carried the residue unscaled and kept the residue of the uncapped
    count (`by_drive(172160, 8192, 14520)` = (12, 6112)): twelve walls of
    paid credit destroyed;
(i) verb 3's form, the label by Bresenham along the line of **P** (the
    model owner's GO of record 536, the chief physicist's recommendation
    of record 483): the row's error accumulator **c** = the sum over its
    walked Links **h** of **h** x **P** (the integer cross product, read
    from the first push on), and the label chosen among D and its fan
    neighbours as the one whose next Link keeps |**c** + **h** x **P**|^2
    smallest, ties to D. A bar of 230 x 16 x 1 at [1, 56], `optical` 1,
    the fan the twelve diagonals with (24, +-1, 0) and (12, +-1, 0) (the
    teeth 2.39 and 4.76 degrees, the bisector 3.58): a row of `light` at
    (1, 1, 0) on +x pushed once at (2, 1, 0) by an m row arriving from +y,
    **W** = (0, 14080, 0), **P** = (229376, 14080, 0) at 3.51 degrees,
    below the bisector, so the nearest-tooth verb kept (24, 1, 0) and
    reached y = 1 + 8.3 at x = 201; along **P** the row reaches y >= 12 at
    x = 201 and
    stays within two Links of **P**'s line (|e x P| <= 2 |P_x|), **P**
    conserved at every interval, the walked Links' angle 3.51 and not the
    tooth's 2.39; the fields `cross` are 0 on every row without the key;
(j) the pace of a pushed row is its momentum's (the chief physicist's
    word of 2026-09-21, DERIVED, relayed as the Boss's order after record
    547): the flight's one rule is the Euclidean pace 1 / sqrt 3 along the
    line walked, and under Bresenham the line walked is **P**'s, so the
    pair in the wall is the primitive **P**'s (**P** over the gcd of its
    components), S_1(P) and T(P) = isqrt(3 |P|^2 Q^2), the rate 2 S_1(P) Q d
    against the wall 2 T(P) (d + f n A), and the residue is rescaled by
    S_1(P') / S_1(P) at every push (the label's S_1 before the first),
    floor, the sub-unit remainder dropped. A bar of 60 x 3 x 1 at [1, 220]
    and `optical` 1: a row of `light` on (24, 1, 0) at (1, 1, 0), pushed at
    (2, 1, 0) in interval 1 by an m row of amount 3 arriving from -y,
    **W** = (0, -42240, 0), so that **P** = (901120, 0, 0) is +x exactly
    (the primitive (1, 0, 0), the control's pair 1 and 110): its residue
    118360 in the label's units becomes 118360 // 25 = 4734, and from
    then on it walks +x Links at the control's pace, the rate 28160
    against the wall 48400 (49720 and 51040 while the m row of amount 3
    sits at its Node, A = 3 and 6, the Link of interval 3 counted against
    51040), the 52nd Link after the push at the exact time 1 + (52 x
    48400 + 2640 - 4734) / 28160 = 90.300 intervals, 52 x 110 / 64 =
    89.375 after the push less the residue's 0.168 plus the crowd's
    0.094, integer for integer with `by_drive`; on the label's pace (the
    head before this word) the 52 Links took 52 x 2662 / (25 x 64) = 86.5
    intervals, three too few. The test asserts the by-hand (made, residue)
    chain against the run, the row's whole momentum (901120, 0, 0) at
    every interval (P conserved), and the 53rd made at tick 91 with the
    row at (54, 1, 0);
(h) S1 of the same review, under the momentum's pace ((j)): the sums the
    push accumulator takes are tested against the working bound before
    they are formed, and below them the pair on the momentum and the
    residue's rescale are: the turn world of (b) with the light row's
    **W** preset at 2^63 - 1 - 14080 on x walks (the primitive (1, 0, 0))
    and is refused at the push, the pair of **P**' beyond the register;
    preset on -y it is refused at the walk, the wall on the primitive
    **P** beyond the register; W_x = 2^40 is taken (the push's
    **P**' = (2^40 + 16384, -14080, 0) over its gcd 1280 is
    (858993472, -11, 0), the residue 72 x 858993483);
    W_y = 2^54 + 1 is refused at the walk (T(P) about 2^60.8, the wall
    2 T d over the register).
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path

import pytest

from event_universe.core.integer import MAX_WORK_INT, age_wall, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.measured import AGE_WALL_NEVER, AGE_WALL_SET, age_wall_set
from event_universe.events.world import HEADING_OFFSET, OPTICAL_RULE, Q
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "optical"
PLUS_X, PLUS_Y, MINUS_Y = HEADING_OFFSET, HEADING_OFFSET + 2, HEADING_OFFSET + 3
FAMILIES = [{"name": "light", "quantum": 1}, {"name": "m", "quantum": 0, "charge": 0, "phase": False}]
# The twelve edge diagonals: every heading has four neighbours within a
# right angle and every diagonal has its two headings and four diagonals.
DIAGONALS = [
    [1, 1, 0],
    [1, -1, 0],
    [-1, 1, 0],
    [-1, -1, 0],
    [0, 1, 1],
    [0, 1, -1],
    [0, -1, 1],
    [0, -1, -1],
    [1, 0, 1],
    [1, 0, -1],
    [-1, 0, 1],
    [-1, 0, -1],
]


def bar(optical: int | None, *, crowd_amount: int = 4, crowd_age: int = 3) -> dict[str, object]:
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "test-optical-bar",
        "shape": [12, 1, 1],
        "boundary": "open",
        "ticks": 40,
        "K": 4096,
        "N": 64,
        "release": [0, 1],
        "suspension": [1, 4],
        "directions": DIAGONALS,
        "families": FAMILIES,
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 65536,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[1, 0, 0]]},
                "table": {"m": "pass"},
            },
            {
                "position": [11, 0, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "table": {"light": "pass"},
            },
        ],
        "in_transit": [
            {
                "position": [x, 0, 0],
                "family": "m",
                "number": 2,
                "direction": 0,
                "amount": crowd_amount,
                "phase": 0,
                "age": crowd_age,
            }
            for x in range(4, 9)
        ],
    }
    if optical is not None:
        document["optical"] = optical
    return document


def turn_world(optical: int | None = 1, *, meeting: bool = False) -> dict[str, object]:
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "test-optical-turn",
        "shape": [6, 3, 1],
        "boundary": "open",
        "ticks": 6,
        "K": 4096,
        "N": 64,
        "release": [0, 1],
        "suspension": [1, 4],
        "directions": DIAGONALS,
        "families": FAMILIES,
        "measured": [
            {
                "position": [0, 1, 0],
                "family": "light",
                "amount": 65536,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [0, 1], "wheel": [1, 64], "directions": [[1, 0, 0]]},
                "table": {"m": "pass"},
            },
            {
                "position": [5, 1, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "table": {"light": "pass"},
            },
        ],
        "in_transit": [
            {
                "position": [1, 1, 0],
                "family": "light",
                "number": 1,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
            },
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
    if meeting:
        document["meeting"] = True
    return document


# The pin worlds' long direction beside the edge diagonals: (24, 1, 0) is
# the thirteenth declared direction, T_D 2662 against the heading's 110.
FAN = [*DIAGONALS, [24, 1, 0], [24, -1, 0]]
LONG = HEADING_OFFSET + 6 + len(DIAGONALS)


def fan_world(
    light_direction: int, light_age: int, crowd_position: list[int], crowd_direction: int
) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "test-optical-units",
        "shape": [8, 3, 1],
        "boundary": "open",
        "ticks": 4,
        "K": 4096,
        "N": 64,
        "release": [0, 1],
        "suspension": [1, 64],
        "directions": FAN,
        "families": FAMILIES,
        "optical": 1,
        "measured": [
            {
                "position": [0, 1, 0],
                "family": "light",
                "amount": 65536,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [0, 1], "wheel": [1, 64], "directions": [[1, 0, 0]]},
                "table": {"m": "pass"},
            },
            {
                "position": [7, 1, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "table": {"light": "pass"},
            },
        ],
        "in_transit": [
            {
                "position": [1, 1, 0],
                "family": "light",
                "number": 1,
                "direction": light_direction,
                "amount": 1,
                "phase": 0,
                "age": light_age,
            },
            {
                "position": crowd_position,
                "family": "m",
                "number": 2,
                "direction": crowd_direction,
                "amount": 1,
                "phase": 0,
            },
        ],
    }


def first_row(store) -> int | None:  # type: ignore[no-untyped-def]
    for i in range(store.size):
        if int(store.record[i]) & 0xFFFFFFFF == 1:
            return i
    return None


def test_the_flight_walks_against_the_wall_the_crowd_stretches():
    """(a)."""
    acc, x, by_hand = 110 * 4, 0, []
    for _ in range(2, 41):
        moment = 12 if 4 <= x <= 8 else 0
        rate, wall = age_wall(2 * 1, 2 * 110, 2, moment, (1, 4))
        assert (rate * Q, wall) == (512, 880 if moment == 0 else 6160)
        count, acc = by_drive(acc, 512, wall)
        x += count
        by_hand.append(x)
    assert (
        by_hand[:8] == [1, 1, 2, 2, 3, 3, 4, 4]
        and by_hand[6:18] == [4] * 12
        and by_hand[18:30] == [5] * 12
    )
    for optical, expected in (
        (1, by_hand),
        (None, [1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 10, 11]),
    ):
        parsed = parse_nature_beam_world(bar(optical))
        assert (OPTICAL_RULE in parsed.hypotheses) == (optical is not None)
        simulation = NatureBeamSimulation(parsed)
        walked: list[int] = []
        fields: list[tuple[int, int]] = []
        for tick in range(1, 41):
            simulation.step()
            assert simulation.books()["balanced"], tick
            store = simulation.stores[0]
            index = first_row(store)
            if index is None:
                continue
            x_now = int(store.coordinates(store.node[index : index + 1])[0][0])
            if tick >= 2:
                walked.append(x_now)
            fields.append((int(store.made[index]), int(store.residue[index])))
        assert walked == expected[: len(walked)], optical
        if optical is None:
            assert set(fields) == {(0, 0)}
        else:
            assert fields[1] == (1, 72) and fields[8] == (4, 1016)


def test_the_push_turns_a_row_to_the_fans_nearest_direction():
    """(b)."""
    document = turn_world()
    document["in_transit"][1]["amount"] = 2  # type: ignore[index]
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    vectors = simulation.tables.flight.vectors
    assert simulation.tables.flight.energy[PLUS_X] == 110
    simulation.step()
    books = simulation.books()
    assert books["balanced"]
    light, crowd = simulation.stores[0], simulation.stores[1]
    assert light.size == 1 and crowd.size == 1
    assert vectors[int(light.direction[0])].tolist() == [1, -1, 0]
    assert (int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])) == (4864, -16640, 0)
    # the residue 72 of the heading (S_1 = 1) rescaled at the push to the
    # momentum's units: P = (16384, -28160, 0) over its gcd 512 is
    # (32, -55, 0), S_1 = 87, 72 x 87 // 1 = 6264; not rescaled at the turn
    assert (int(light.made[0]), int(light.residue[0])) == (1, 6264)
    assert light.coordinates(light.node[:1])[0][0] == 2 and light.coordinates(light.node[:1])[1][0] == 1
    assert books["momentum"]["turned"] == [-19, -45, 0] and books["momentum"]["transit"] == [45, 83, 0]
    assert (int(crowd.push_x[0]), int(crowd.push_y[0]), int(crowd.push_z[0])) == (0, 0, 0)
    assert vectors[int(crowd.direction[0])].tolist() == [0, 1, 0]
    # by hand: the two advancing candidates at made 1
    momentum = (16384, -28160, 0)
    assert momentum[1] ** 2 > momentum[0] ** 2  # +x's (1, 0, 0) against (1, -1, 0)'s (0, -1, 0)
    # an m row of amount 1: P at -40.7 degrees, +x's Link keeps the smaller error
    weaker = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    weaker.step()
    assert weaker.tables.flight.vectors[int(weaker.stores[0].direction[0])].tolist() == [1, 0, 0]
    assert 14080**2 < 16384**2 and weaker.books()["momentum"]["turned"] == [0, 0, 0]
    # the same world without the key: the row keeps +x and no turn line
    plain = NatureBeamSimulation(parse_nature_beam_world(turn_world(None)))
    plain.step()
    assert plain.tables.flight.vectors[int(plain.stores[0].direction[0])].tolist() == [1, 0, 0]
    assert plain.books()["momentum"]["turned"] == [0, 0, 0]


def test_the_whole_momentum_is_conserved_across_the_turn():
    """(c)."""
    document = turn_world()
    document["in_transit"][1]["amount"] = 2  # type: ignore[index]
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    unit = simulation.tables.flight.labels
    before = Q * 4 * 1 * unit[PLUS_X] + 0
    simulation.step()
    light = simulation.stores[0]
    after = Q * 4 * 1 * unit[int(light.direction[0])] + [
        int(light.push_x[0]),
        int(light.push_y[0]),
        int(light.push_z[0]),
    ]
    # before the turn W = (0, -28160, 0) was the push of the interval
    assert (before + [0, -28160, 0]).tolist() == after.tolist() == [16384, -28160, 0]
    assert (int(light.amount[0]), int(light.content[0]), int(light.number[0]), int(light.phase[0])) == (
        1,
        1,
        1,
        0,
    )


def test_the_refusals_and_the_identity():
    """(d)."""
    with pytest.raises(ValueError, match="refused with suspension"):
        parse_nature_beam_world({**turn_world(), "suspension": 0})
    with pytest.raises(ValueError, match="one turn verb per row"):
        parse_nature_beam_world(turn_world(meeting=True))
    for bad in (-1, True, "2", 1.5):
        with pytest.raises(ValueError, match="optical must be a non-negative integer"):
            parse_nature_beam_world(turn_world(bad))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match=r"direction \[1, 0, 0\] has no neighbour"):
        parse_nature_beam_world({**turn_world(), "directions": []})
    # the two keys together (the reviewer's correction on f4138855, record
    # 510): the composed flight of massive rows under the optical key is
    # not reviewed; each key alone parses ((d) here, test_massive_rows (a))
    with pytest.raises(ValueError, match="composed flight of massive rows under the key optical"):
        parse_nature_beam_world({**turn_world(), "massive_rows": True, "age_bound": 64})
    assert parse_nature_beam_world(
        {**turn_world(None), "massive_rows": True, "age_bound": 64}
    ).massive_rows
    parsed = parse_nature_beam_world(turn_world(1))
    assert (
        parsed.hypotheses[-1] == OPTICAL_RULE and parsed.optical == 1 and parsed.flight_coefficient == 2
    )
    assert OPTICAL_RULE not in parse_nature_beam_world(turn_world(None)).hypotheses


def test_byte_identity_without_the_key_and_the_declared_set():
    """(e)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(bar(None)))
    for _ in range(20):
        simulation.step()
    for store in simulation.stores:
        for name in ("made", "residue", "push_x", "push_y", "push_z", "cross_x", "cross_y", "cross_z"):
            assert not getattr(store, name).any(), name
    lines = [
        ray
        for node in simulation.snapshot()["nodes"]  # type: ignore[union-attr]
        for family in node["families"]
        for ray in family["rays"]
    ]
    assert lines and not any("flight" in ray or "push" in ray or "cross" in ray for ray in lines)
    assert age_wall_set(None) == AGE_WALL_SET == (("owed", 1),)
    assert age_wall_set(0) == (("owed", 1), ("flight", 1)) and age_wall_set(1) == (
        ("owed", 1),
        ("flight", 2),
    )
    assert not any(name in dict(age_wall_set(1)) for name in AGE_WALL_NEVER)


def test_the_pin_worlds_parse_run_and_carry_their_pins():
    """(f)."""
    spec = importlib.util.spec_from_file_location("optical_make_worlds", WORLDS / "make_worlds.py")
    assert spec is not None and spec.loader is not None
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    for name, document in generator.worlds().items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        loaded = load_world(path.read_bytes(), base_dir=WORLDS, root=WORLDS.parent)
        world = loaded.world
        assert OPTICAL_RULE in world.hypotheses and world.suspension == (1, 16384)
        assert world.optical == int(name[-1]) and world.flight_coefficient == 1 + world.optical
        simulation = NatureBeamSimulation(world)
        for _ in range(10):
            simulation.step()
        assert simulation.books()["balanced"], name
    # the inverse interval is refused under the key (the wall reads the
    # crowd of the interval before, which the after-state does not hold)
    plain = NatureBeamSimulation(
        parse_nature_beam_world({**turn_world(1), "measured": [], "in_transit": []})
    )
    plain.step()
    with pytest.raises(ValueError, match="refused under the key optical"):
        plain.inverse_step()
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == generator.EXPECTATIONS_FORMAT
    # The deflection pins: mass and far at both gammas, near at f = 1; near
    # at f = 2 is a capture reading (records 505 and 540), its old shift pin
    # kept beside it as superseded.
    assert [
        expected["worlds"][n]["shift"] for n in ("mass_g0", "mass_g1", "near_g0", "far_g0", "far_g1")
    ] == [-1.93, -3.86, -2.42, -1.69, -3.37]
    near_g1 = expected["worlds"]["near_g1"]
    assert "shift" not in near_g1 and near_g1["shift_pin_superseded"] == -4.83
    assert near_g1["taken_by_the_mass"] == 582 and near_g1["taken_bracket"] == 146
    assert near_g1["reading"].startswith("capture:")
    assert [
        expected["worlds"][n]["delay"]
        for n in ("mass_g0", "mass_g1", "near_g0", "near_g1", "far_g0", "far_g1")
    ] == [2.68, 5.36, 2.17, 4.34, 2.15, 4.29]
    assert expected["worlds"]["far_g0"]["lamp_rate"] is None
    assert expected["ratios"]["mass"]["expected"] == 2.0 and expected["brackets"]["shift_pixels"] == 0.5
    assert (
        expected["ratios"]["mass"]["bracket"] == 0.25 and expected["ratios"]["near"]["bracket"] == 0.25
    )
    assert (
        expected["ratios"]["far"]["bracket"] == 0.66
        and expected["ratios"]["far"]["delay_bracket"] == 1.04
    )


def long_world(
    light_direction: int, light_age: int, crowd_position: list[int], crowd_direction: int
) -> dict[str, object]:
    document = fan_world(light_direction, light_age, crowd_position, crowd_direction)
    document["shape"] = [40, 3, 1]
    document["ticks"] = 40
    document["measured"][1]["position"] = [39, 1, 0]  # type: ignore[index]
    return document


def test_the_residue_carried_across_a_turn_keeps_what_the_wall_paid_for():
    """(g)."""
    # By hand: the count capped at one Link by the primitive with the
    # surplus kept; the pair (S_1, T) the label's until the push and the
    # momentum's from it (P over its gcd), the residue rescaled at the push
    # by S_1(P) / S_1(D) (floor) and not at the label's turn.
    heading, long = (1, 110), (25, 2662)

    def chain(
        start: tuple[int, int], pushed: tuple[int, int], path: list[tuple[tuple[int, int], int]]
    ) -> list[tuple[int, int]]:
        (made, residue), out = start, []
        for k, ((s1, t), moment) in enumerate(path):
            rate, wall = age_wall(2 * s1, 2 * t, 2, moment, (1, 64))
            count, residue = by_drive(residue, rate * Q, wall, at_most=1)
            made += count
            if k == 0:  # the push at the end of interval 1
                residue = residue * pushed[0] // s1
            out.append((made, residue))
        return out

    def run(document: dict[str, object], ticks: int) -> tuple[list[list[int]], list[tuple[int, int]]]:
        simulation = NatureBeamSimulation(parse_nature_beam_world(document))
        vectors = simulation.tables.flight.vectors
        labels: list[list[int]] = []
        seen: list[tuple[int, int]] = []
        for tick in range(1, ticks + 1):
            simulation.step()
            assert simulation.books()["balanced"], tick
            light = simulation.stores[0]
            assert light.size == 1, tick
            labels.append(vectors[int(light.direction[0])].tolist())
            seen.append((int(light.made[0]), int(light.residue[0])))
        return labels, seen

    # From the heading at age 5, pushed at (1, 1, 0) by the m row arriving
    # from +y (V = (0, -64, 0), W = (0, 14080, 0)): P = (262144, 14080, 0),
    # over its gcd 256 the primitive (1024, 55, 0), S_1 1079, T 113675.
    assert (5 * 128 + 110) // 220 == 3 and (5 * 128 + 110) % 220 == 90
    assert isqrt(3 * (1024**2 + 55**2) * Q * Q) == 113675 and 13952 * 1079 == 15054208
    on_p = (1079, 113675)
    path = [(heading, 0), (on_p, 1)] + [(on_p, 0)] * 20
    expected = chain((3, 90 * 64), on_p, path)
    assert expected[:3] == [(3, 15054208), (4, 8888276), (5, 3177044)]
    assert expected[13:16] == [(11, 13105492), (12, 7394260), (13, 1683028)]
    assert Fraction(13952, 2 * 1 * Q * 64) == Fraction(15054208, 2 * 1079 * Q * 64)  # the time
    labels, seen = run(long_world(PLUS_X, 5, [1, 2, 0], MINUS_Y), 22)
    assert labels[:14] == [[1, 0, 0]] * 14 and labels[14:] == [[24, 1, 0]] * 8
    assert seen == expected
    # From the long direction at age 4, pushed at (2, 1, 0) by the m row
    # arriving from -y (V = (0, 64, 0), W = (0, -14080, 0)): P = (262144,
    # -1792, 0), the primitive (1024, -7, 0), S_1 1031, T 113514; the
    # residue 172160 of the label (S_1 25) becomes 172160 x 1031 // 25 =
    # 7099878 (the remainder 10 of 25 dropped); at made 12 (interval 16)
    # the label moves to the heading with no rescale.
    assert (4 * 2 * 25 * Q + 2662) // 5324 == 2 and (4 * 2 * 25 * Q + 2662) % 5324 == 4814
    assert isqrt(3 * (1024**2 + 7**2) * Q * Q) == 113514 and 172160 * 1031 // 25 == 7099878
    on_p = (1031, 113514)
    path = [(long, 0), (on_p, 1)] + [(on_p, 0)] * 18
    expected = chain((2, 4814 * 64), on_p, path)
    assert expected[:3] == [(3, 7099878), (4, 561982), (4, 9007934)]
    assert expected[14:18] == [(11, 8650814), (12, 2566974), (12, 11012926), (13, 4929086)]
    assert abs(Fraction(172160, 2 * 25 * Q * 64) - Fraction(7099878, 2 * 1031 * Q * 64)) < Fraction(
        1, 2 * 1031 * Q * 64
    )
    assert by_drive(172160, 8192, 14520) == (12, 6112)  # the head before M1, unscaled and uncapped
    labels, seen = run(long_world(LONG, 4, [2, 0, 0], PLUS_Y), 20)
    assert labels[:15] == [[24, 1, 0]] * 15 and labels[15:] == [[1, 0, 0]] * 5
    assert seen == expected


def test_the_push_accumulators_sums_are_tested_at_the_register():
    """(h)."""
    push = 1 * 2 * 1 * 110 * 64  # n x weight x |V| of (b)
    # W_x at the register's edge: P = (2^63 + 2303, 0, 0) is the primitive
    # (1, 0, 0) and walks; the push then makes P' = (2^63 + 2303, -14080, 0)
    # whose pair leaves the register: refused at the push naming the rule.
    # W_y at the edge: the primitive is P itself, its wall over the
    # register at the walk.
    for axis, sign in (("push_x", 1), ("push_y", -1)):
        simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
        getattr(simulation.stores[0], axis)[0] = sign * (MAX_WORK_INT - push)
        with pytest.raises(OverflowError, match="pair on the momentum"):
            simulation.step()
    # Inside the register: W_x = 2^40 makes the primitive (1, 0, 0), taken,
    # and the push's P' = (2^40 + 16384, -14080, 0) over its gcd 1280 (2^8
    # x 5, since 2^26 + 1 = 5 x 13421773) is (858993472, -11, 0), S_1 =
    # 858993483, the residue 72 x 858993483 taken; W_y = 2^54 + 1
    # makes the primitive (16384, 2^54 + 1, 0), T(P) = isqrt(3 |P|^2 Q^2)
    # about 2^60.8, the wall 2 T d over the register at d = 4: refused.
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_x[0] = 1 << 40
    simulation.step()
    light = simulation.stores[0]
    assert ((1 << 40) + 16384) // 1280 == 858993472 and 14080 // 1280 == 11
    assert simulation.books()["balanced"] and int(light.residue[0]) == 72 * 858993483
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_y[0] = (1 << 54) + 1
    with pytest.raises(OverflowError, match="pair on the momentum"):
        simulation.step()


def bresenham_world() -> dict[str, object]:
    document = fan_world(PLUS_X, 0, [2, 2, 0], MINUS_Y)
    document["shape"] = [230, 16, 1]
    document["ticks"] = 400
    document["suspension"] = [1, 56]
    document["directions"] = [*FAN, [12, 1, 0], [12, -1, 0]]
    document["measured"][1]["position"] = [229, 1, 0]  # type: ignore[index]
    return document


def test_a_pushed_row_walks_along_the_line_of_its_momentum_not_the_nearest_tooth():
    """(i)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(bresenham_world()))
    unit = simulation.tables.flight.labels
    momentum = [64 * 56 * 64, 14080, 0]
    x = y = 1
    for tick in range(1, 401):
        simulation.step()
        assert simulation.books()["balanced"], tick
        light = simulation.stores[0]
        assert light.size == 1, tick
        whole = Q * 56 * int(light.amount[0]) * int(light.content[0])
        held = [int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])]
        if tick >= 1:
            assert [
                whole * int(u) + w for u, w in zip(unit[int(light.direction[0])], held, strict=True)
            ] == momentum, tick
        x, y, _ = (int(c[0]) for c in light.coordinates(light.node[:1]))
        if x >= 201:
            break
    assert x == 201 and tick < 400
    ex, ey = x - 2, y - 1  # from the push at (2, 1, 0)
    assert abs(ex * momentum[1] - ey * momentum[0]) <= 2 * momentum[0], (ex, ey)
    assert ey >= 11, (ex, ey)  # the tooth (24, 1, 0) reaches 8.3
    cross = (int(light.cross_x[0]), int(light.cross_y[0]), int(light.cross_z[0]))
    assert cross != (0, 0, 0)


def pace_world() -> dict[str, object]:
    document = fan_world(LONG, 0, [2, 0, 0], PLUS_Y)
    document["shape"] = [60, 3, 1]
    document["ticks"] = 120
    document["suspension"] = [1, 220]
    document["measured"][1]["position"] = [59, 1, 0]  # type: ignore[index]
    document["in_transit"][1]["amount"] = 3  # type: ignore[index]
    return document


def test_a_pushed_rows_pace_is_its_momentums():
    """(j)."""
    # By hand: the first walk on the label (24, 1, 0), 2662 x 220 + 704000
    # against the wall 1171280, one Link and the residue 118360; the push
    # to P = (901120, 0, 0), the residue 118360 // 25 = 4734 in +x's units;
    # then +x's pair with the crowd's stretch in intervals 2 and 3 (the m
    # row's amount 3 times its age).
    assert 2662 * 220 + 2 * 25 * Q * 220 - 2 * 2662 * 220 == 118360 and 118360 // 25 == 4734
    residue, made, chain = 4734, 1, [(1, 4734)]
    for tick in range(2, 121):
        moment = {2: 3, 3: 6}.get(tick, 0)
        rate, wall = age_wall(2 * 1, 2 * 110, 2, moment, (1, 220))
        assert rate * Q == 28160 and wall == 48400 + 440 * moment
        count, residue = by_drive(residue, 28160, wall, at_most=1)
        made += count
        chain.append((made, residue))
    ticks_52 = next(tick for tick, (m, _) in enumerate(chain, start=1) if m == 53)
    exact = Fraction(ticks_52 * 28160 - chain[ticks_52 - 1][1], 28160)
    # the Link of interval 3 counted against the stretched wall 51040 (+2640)
    assert exact == 1 + Fraction(52 * 48400 + 2640 - 4734, 28160)
    assert exact - 1 == 52 * Fraction(110, 64) - Fraction(4734 - 2640, 28160)
    simulation = NatureBeamSimulation(parse_nature_beam_world(pace_world()))
    unit = simulation.tables.flight.labels
    seen: list[tuple[int, int]] = []
    for tick in range(1, 121):
        simulation.step()
        assert simulation.books()["balanced"], tick
        light = simulation.stores[0]
        assert light.size == 1, tick
        seen.append((int(light.made[0]), int(light.residue[0])))
        whole = Q * 220 * int(light.amount[0]) * int(light.content[0])
        held = [int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])]
        assert [
            whole * int(u) + w for u, w in zip(unit[int(light.direction[0])], held, strict=True)
        ] == [
            901120,
            0,
            0,
        ]
        if int(light.made[0]) == 53:
            break
    assert tick == ticks_52 and seen == chain[:ticks_52]
    assert (
        int(light.coordinates(light.node[:1])[0][0]) == 54
        and int(light.coordinates(light.node[:1])[1][0]) == 1
    )

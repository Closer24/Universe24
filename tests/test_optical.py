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
    accumulator becomes **W** = -n x content x w x **V** with the weight per
    unit w = (e_D^2 + 3 gamma **u**_D . **u**_D) // e_D = (12100 + 12288) //
    110 = 221 on the family's own labels (every family under one wall,
    2026-09-22; 2 e_D = 220 until then, the root's floor the one unit),
    -(1 x 1 x 221) x (0, 128, 0) = (0, -28288, 0); its whole momentum
    **P** = Q d content **u**_x + **W** = (16384, -28288, 0); verb 3 by
    Bresenham (record 536; (i)) reads the next Link of +x and of its fan
    neighbours at the row's place (made 1): +x offers (1, 0, 0) with the
    error |(1, 0, 0) x **P**|^2 = 28288^2, (1, -1, 0) offers (0, -1, 0)
    (advancing, **h** . **P** = 28288 > 0) with 16384^2, (1, 1, 0)'s
    (0, 1, 0) and (1, 0, +-1)'s (0, 0, +-1) do not advance; the label
    moves to (1, -1, 0) and **W** += Q d content (**u**_x - **u**_(1,-1,0))
    = 256 x (19, 45, 0): **W** = (4864, -16768, 0), **P** conserved, the
    residue 72 of the heading rescaled at the push to the momentum's
    units, 72 x 349 = 25128 (**P** over its gcd 128 is (128, -221, 0), S_1
    349; (j)) and not at the turn; the
    books' `turned` line of `light` (-19, -45, 0) (the label (45, -45, 0)
    less (64, 0, 0)) and the transit momentum (45, 83, 0) (the light's
    label and the m row's (0, 128, 0)) balanced; the m row (a free family,
    content 0) never turns; with an m row of amount 1 (**P** at -40.7
    degrees) +x's Link keeps the smaller error, 14080^2 against 16384^2,
    and the row keeps +x;
(c) **P** is conserved across the turn: Q d content **u**_D + **W** before
    equals Q d content **u**_D' + **W** after, (16384, -28288, 0), the
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
    floor, the sub-unit remainder dropped. A bar of 60 x 3 x 1 at [1, 221]
    and `optical` 1: a row of `light` on (24, 1, 0) at (1, 1, 0), pushed at
    (2, 1, 0) in interval 1 by an m row of amount 3 arriving from -y,
    **W** = (0, -42432, 0) at the weight 221, so that **P** = (905216, 0, 0)
    is +x exactly (the primitive (1, 0, 0), the control's pair 1 and 110):
    its residue 118898 in the label's units becomes 118898 // 25 = 4755,
    and from then on it walks +x Links at the control's pace, the rate
    28288 against the wall 48620 (49940 and 51260 while the m row of
    amount 3 sits at its Node, A = 3 and 6, the Link of interval 3 counted
    against 51260), the 52nd Link after the push at the exact time 1 +
    (52 x 48620 + 2640 - 4755) / 28288 = 90.300 intervals, 52 x 110 / 64 =
    89.375 after the push less the residue's 0.168 plus the crowd's
    0.093, integer for integer with `by_drive`; on the label's pace (the
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
    **P** beyond the register; W_x = 2^24 is taken (the push's
    **P**' = (2^24 + 16384, -14144, 0) over its gcd 64 is
    (262400, -221, 0), the residue 72 x 262621); W_x = 2^40 and
    W_y = 2^54 + 1 are refused before the root, the square 3 |P|^2 Q^2
    of the primitive (about 2^81.6 and 2^121) over the working bound
    (the reviewer's MUST-FIX 2 on every family under one wall: the
    intermediate respects the bound; on the head before, W_x = 2^40 was
    taken with its square formed unbounded).
(k) every family under one wall (2026-09-22, EVERY_FAMILY.md sections 1
    and 3): the weight per unit of amount on the family's own labels,
    (E'_D^2 + 3 gamma p_D . p_D) // E'_D: the photon's 110 at gamma = 0 and
    221 at gamma = 1 (the one floor: 2 e_D = 220 on the head before);
    `matter` (quantum 1, momentum 10 at width 1: E'_0 = 64, E' = 66, the
    triple (20, 132, 66)) 66 at gamma = 0 and 70 at gamma = 1.
(l) a row never pushed carries its family's pair (20, 132); pushed along
    its momentum by W = (2560, 0, 0) its pair is (640, 2328) (P = (5120,
    0, 0) and the rest 16384 over their gcd 1024: (5, 0, 0) and 16, T =
    isqrt((16^2 + 3 x 25) x 4096) = 1164), the pace 0.275 against the
    triple's 0.152: a falling row speeds up.
(m) the bar of (a) with a massive lamp (the reservoir the world's K =
    4096, the turn 1): the first row walks by its triple under the one
    wall, the rate 80 against 528 off the crowd and 3696 on it from the
    start 264, the 39 x positions of ticks 2 .. 40 equal to `by_drive` by
    hand.
(n) the working bound before the wall's square (the physics-rule
    reviewer's MUST-FIX 2 on EVERY_FAMILY.md): the massive row of (m) with
    its amount preset to 2^40 and a push of 2560 on x has R = Q d a E'_0 /
    g = 2^45 (g = 512), whose square leaves the bound 2^63 - 1 over Q^2
    (R under 2^25.5): refused at the walk naming the wall's square,
    before the root; at the amount 4 (the deciding world's largest) the
    pair is taken: P = (12800, 0, 0) and R = 65536 over their gcd 512 are
    (25, 0, 0) and 128, T = isqrt((128^2 + 3 x 625) x 4096) = 8648, the
    pair (3200, 17296).
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.integer import MAX_WORK_INT, age_wall, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.measured import AGE_WALL_NEVER, AGE_WALL_SET, age_wall_set
from event_universe.events.nature_beam import row_pairs, unit_weights
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
    # The generic entry of the bending (2026-09-22): the flight is a member
    # for every world, at the coefficient 1 when the key is absent (gamma
    # 0, the time part alone), so the same hand chain at f = 1 is the walk
    # of the world without the key.
    acc, x, by_hand_time_part = 110 * 4, 0, []
    for _ in range(2, 41):
        moment = 12 if 4 <= x <= 8 else 0
        rate, wall = age_wall(2 * 1, 2 * 110, 1, moment, (1, 4))
        count, acc = by_drive(acc, 512, wall)
        x += count
        by_hand_time_part.append(x)
    assert by_hand_time_part != by_hand
    for optical, expected in (
        (1, by_hand),
        (None, by_hand_time_part),
    ):
        parsed = parse_nature_beam_world(bar(optical))
        assert OPTICAL_RULE not in parsed.hypotheses
        assert parsed.optical == (optical or 0) and parsed.flight_coefficient == 1 + (optical or 0)
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
        if optical is not None:
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
    assert (int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])) == (4864, -16768, 0)
    # the residue 72 of the heading (S_1 = 1) rescaled at the push to the
    # momentum's units: P = (16384, -28288, 0) over its gcd 128 is
    # (128, -221, 0), S_1 = 349, 72 x 349 // 1 = 25128; not rescaled at the turn
    assert (int(light.made[0]), int(light.residue[0])) == (1, 25128)
    assert light.coordinates(light.node[:1])[0][0] == 2 and light.coordinates(light.node[:1])[1][0] == 1
    assert books["momentum"]["turned"] == [-19, -45, 0] and books["momentum"]["transit"] == [45, 83, 0]
    assert (int(crowd.push_x[0]), int(crowd.push_y[0]), int(crowd.push_z[0])) == (0, 0, 0)
    assert vectors[int(crowd.direction[0])].tolist() == [0, 1, 0]
    # by hand: the two advancing candidates at made 1
    momentum = (16384, -28288, 0)
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
    # before the turn W = (0, -28288, 0) was the push of the interval
    assert (before + [0, -28288, 0]).tolist() == after.tolist() == [16384, -28288, 0]
    assert (int(light.amount[0]), int(light.content[0]), int(light.number[0]), int(light.phase[0])) == (
        1,
        1,
        1,
        0,
    )


def test_the_refusals_and_the_identity():
    """(d)."""
    # The three refusals of optical-v1 are lifted since the generic entry
    # of the bending (2026-09-22): at suspension 0 nothing is stretched and
    # nothing pushed, a heading without a neighbour turns to nothing, and
    # under `meeting` the meeting's turn keeps the heading.
    assert parse_nature_beam_world({**turn_world(), "suspension": 0}).optical == 1
    assert parse_nature_beam_world(turn_world(meeting=True)).meeting
    assert parse_nature_beam_world({**turn_world(), "directions": []}).optical == 1
    for bad in (-1, True, "2", 1.5):
        with pytest.raises(ValueError, match="optical must be a non-negative integer"):
            parse_nature_beam_world(turn_world(bad))  # type: ignore[arg-type]
    # the two keys together load since 2026-09-22 (every family under one
    # wall, docs/designs/one_wall/EVERY_FAMILY.md; the refusal of record 510
    # lifted): every family walks by its own table under the age wall
    both = parse_nature_beam_world({**turn_world(), "massive_rows": True, "age_bound": 64})
    assert both.massive_rows and both.optical == 1
    assert parse_nature_beam_world(
        {**turn_world(None), "massive_rows": True, "age_bound": 64}
    ).massive_rows
    parsed = parse_nature_beam_world(turn_world(1))
    # gamma is a declared input of the law, no hypothesis: `optical-v1`
    # names none since 2026-09-22
    assert OPTICAL_RULE not in parsed.hypotheses
    assert parsed.optical == 1 and parsed.flight_coefficient == 2
    absent = parse_nature_beam_world(turn_world(None))
    assert OPTICAL_RULE not in absent.hypotheses
    assert absent.optical == 0 and absent.flight_coefficient == 1


def test_byte_identity_without_a_crowd_and_the_declared_set():
    """(e)."""
    # A world in which no crowd acts keeps its state byte for byte: the
    # flight accumulator on a row is the table's own count at its age (the
    # memoryless form the walk seeds from), and the snapshot omits it.
    document = bar(None)
    document.pop("in_transit")
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    for _ in range(20):
        simulation.step()
    for store in simulation.stores:
        for name in ("push_x", "push_y", "push_z", "cross_x", "cross_y", "cross_z"):
            assert not getattr(store, name).any(), name
    lines = [
        ray
        for node in simulation.snapshot()["nodes"]  # type: ignore[union-attr]
        for family in node["families"]
        for ray in family["rays"]
    ]
    assert lines and not any("flight" in ray or "push" in ray or "cross" in ray for ray in lines)
    assert AGE_WALL_SET == (("owed", 1),)
    # Since 2026-09-22 the flight is a member for every world at 1 + gamma
    # (the generic entry of the bending) and the body's line drive, the
    # law's drive, a member at gamma beside it (`test_optical_body.py` (o)).
    assert age_wall_set() == age_wall_set(0) == (("owed", 1), ("flight", 1), ("drive", 0))
    assert age_wall_set(1) == (("owed", 1), ("flight", 2), ("drive", 1))
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
        assert OPTICAL_RULE not in world.hypotheses and world.suspension == (1, 16384)
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
    with pytest.raises(ValueError, match="refused at the pair"):
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
    # The deciding worlds of every family under one wall (2026-09-22,
    # EVERY_FAMILY.md section 2): the two keys together, the massive lamp
    # on the heading, the pins from the map every_family_map.py.
    matter = expected["matter"]
    assert matter["mass"] == 1 << 14 and matter["ticks"] == 1000 and matter["window_start"] == 500
    assert matter["impact"] == 10
    assert [matter["worlds"][n]["shift"] for n in ("matter_g0", "matter_g1", "matter2_g0")] == [
        -5.76,
        -6.11,
        -5.76,
    ]
    assert [matter["worlds"][n]["arrival"] for n in ("matter_g0", "matter_g1", "matter2_g0")] == [
        -8.36,
        -7.42,
        -8.36,
    ]
    assert matter["refuting_readings"] == {
        "gamma_1_arrival_wall_unstretched": -11.03,
        "gamma_1_shift_weight_blind_to_speed": -10.45,
        "gamma_0_arrival_without_the_speed_up": 43.99,
    }
    # The fast worlds (the beam of five lines at b = 8, M = 2^16, p = 40):
    # the pins of the map's integer walk, written before the run.
    fast = [matter["worlds"][f"fast_g{g}"] for g in (0, 1)]
    assert [w["shift"] for w in fast] == [-2.60, -4.40]
    assert [w["arrival"] for w in fast] == [1.94, 4.49]
    assert all(w["mass"] == 1 << 16 and w["impact"] == 8 and w["momentum_magnitude"] == 40 for w in fast)
    assert fast[1]["refuting_readings"] == {
        "arrival_wall_unstretched": -0.80,
        "shift_weight_blind_to_speed": -6.40,
    }
    assert matter["fast_ratios"]["shift_g1_over_g0"] == 1.69
    for name in ("fast_g0", "fast_g1", "fast_control_g1"):
        loaded = load_world((WORLDS / f"{name}.json").read_bytes(), base_dir=WORLDS, root=WORLDS.parent)
        lamp = next(m for m in loaded.world.measured if m.lamp is not None)
        assert loaded.world.massive_rows and loaded.world.optical is not None
        assert len(lamp.lamp.directions) == 5 and lamp.lamp.momentum_magnitude == 40
    for name in ("matter_g0", "matter_g1", "matter2_g0", "matter_control_g0"):
        loaded = load_world((WORLDS / f"{name}.json").read_bytes(), base_dir=WORLDS, root=WORLDS.parent)
        world = loaded.world
        assert world.massive_rows and world.optical is not None and world.action == 1024
        assert world.age_bound == 1024
        family = next(f for f in world.families if f.massive)
        assert family.name == matter["worlds"].get(name, {}).get("family", "matter")


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
    # from +y (V = (0, -64, 0), W = (0, 14144, 0) at the weight 221 of every
    # family under one wall): P = (262144, 14144, 0), over its gcd 64 the
    # primitive (4096, 221, 0), S_1 4317, T 454707.
    assert (5 * 128 + 110) // 220 == 3 and (5 * 128 + 110) % 220 == 90
    assert isqrt(3 * (4096**2 + 221**2) * Q * Q) == 454707 and 13952 * 4317 == 60230784
    on_p = (4317, 454707)
    path = [(heading, 0), (on_p, 1)] + [(on_p, 0)] * 20
    expected = chain((3, 90 * 64), on_p, path)
    assert expected[:3] == [(3, 60230784), (4, 35574324), (5, 12736692)]
    assert expected[13:16] == [(11, 52535220), (12, 29697588), (13, 6859956)]
    assert Fraction(13952, 2 * 1 * Q * 64) == Fraction(60230784, 2 * 4317 * Q * 64)  # the time
    labels, seen = run(long_world(PLUS_X, 5, [1, 2, 0], MINUS_Y), 22)
    assert labels[:14] == [[1, 0, 0]] * 14 and labels[14:] == [[24, 1, 0]] * 8
    assert seen == expected
    # From the long direction at age 4, pushed at (2, 1, 0) by the m row
    # arriving from -y (V = (0, 64, 0), W = (0, -14144, 0)): P = (262144,
    # -1856, 0), the primitive (4096, -29, 0), S_1 4125, T 454058; the
    # residue 172160 of the label (S_1 25) becomes 172160 x 4125 // 25 =
    # 28406400 (exact, 4125 = 25 x 165); at made 12 (interval 16) the label
    # moves to the heading with no rescale.
    assert (4 * 2 * 25 * Q + 2662) // 5324 == 2 and (4 * 2 * 25 * Q + 2662) % 5324 == 4814
    assert isqrt(3 * (4096**2 + 29**2) * Q * Q) == 454058 and 172160 * 4125 // 25 == 28406400
    on_p = (4125, 454058)
    path = [(long, 0), (on_p, 1)] + [(on_p, 0)] * 18
    expected = chain((2, 4814 * 64), on_p, path)
    assert expected[:3] == [(3, 28406400), (4, 2262744), (4, 36054744)]
    assert expected[14:18] == [(11, 34722776), (12, 10395352), (12, 44187352), (13, 19859928)]
    assert Fraction(172160, 2 * 25 * Q * 64) == Fraction(28406400, 2 * 4125 * Q * 64)  # the time
    assert by_drive(172160, 8192, 14520) == (12, 6112)  # the head before M1, unscaled and uncapped
    labels, seen = run(long_world(LONG, 4, [2, 0, 0], PLUS_Y), 20)
    assert labels[:15] == [[24, 1, 0]] * 15 and labels[15:] == [[1, 0, 0]] * 5
    assert seen == expected


def test_the_push_accumulators_sums_are_tested_at_the_register():
    """(h)."""
    push = 1 * 221 * 64  # n x weight x |V| of (b) with the m row of amount 1
    # W_x at the register's edge: P = (2^63 + 2240, 0, 0) is the primitive
    # (1, 0, 0) and walks; the push then makes P' = (2^63 + 2240, -14144, 0)
    # whose pair leaves the register: refused at the push naming the rule.
    # W_y at the edge: the primitive is P itself, its wall over the
    # register at the walk.
    for axis, sign in (("push_x", 1), ("push_y", -1)):
        simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
        getattr(simulation.stores[0], axis)[0] = sign * (MAX_WORK_INT - push)
        with pytest.raises(OverflowError, match="pair on the momentum"):
            simulation.step()
    # Inside the register: W_x = 2^24 makes the primitive (1, 0, 0), taken,
    # and the push's P' = (2^24 + 16384, -14144, 0) over its gcd 64 (221 =
    # 13 x 17 divides neither 2^10 + 1 nor its cofactor) is (262400, -221,
    # 0), S_1 = 262621, the residue 72 x 262621 taken. W_x = 2^40 (taken on
    # the head before every family under one wall, its square formed
    # unbounded) is refused at the push: the primitive (17179869440, -221,
    # 0) has 3 |P|^2 Q^2 about 2^81.6, over the working bound before the
    # root (the physics-rule reviewer's MUST-FIX 2, test (n)); W_y = 2^54 +
    # 1 likewise at the walk (the primitive (16384, 2^54 + 1, 0)).
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_x[0] = 1 << 24
    simulation.step()
    light = simulation.stores[0]
    assert ((1 << 24) + 16384) // 64 == 262400 and 14144 // 64 == 221
    assert simulation.books()["balanced"] and int(light.residue[0]) == 72 * 262621
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_x[0] = 1 << 40
    with pytest.raises(OverflowError, match="wall's square"):
        simulation.step()
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_y[0] = (1 << 54) + 1
    with pytest.raises(OverflowError, match="wall's square"):
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
    momentum = [64 * 56 * 64, 221 * 64, 0]
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
    document["suspension"] = [1, 221]
    document["measured"][1]["position"] = [59, 1, 0]  # type: ignore[index]
    document["in_transit"][1]["amount"] = 3  # type: ignore[index]
    return document


def test_a_pushed_rows_pace_is_its_momentums():
    """(j)."""
    # By hand (the pair [1, 221], so that the weight 221 on the m row's flow
    # 3 x 64 pushes the label (24, 1, 0)'s row to P = (904704, 0, 0), +x
    # exactly: Q d content u_(24,1,0) = 14144 x (64, 3, 0) and W = -221 x
    # (0, 192, 0) = (0, -42432, 0)): the first walk on the label, 2662 x 221
    # + 707200 against the wall 1176604, one Link and the residue 118898;
    # the residue rescaled at the push by the rate's ratio 128 / 3200 to
    # +x's units, 118898 // 25 = 4755; then +x's pair with the crowd's
    # stretch in intervals 2 and 3 (the m row's amount 3 times its age).
    assert 2662 * 221 + 2 * 25 * Q * 221 - 2 * 2662 * 221 == 118898 and 118898 // 25 == 4755
    residue, made, chain, extra = 4755, 1, [(1, 4755)], 0
    for tick in range(2, 121):
        moment = {2: 3, 3: 6}.get(tick, 0)
        rate, wall = age_wall(2 * 1 * Q, 2 * 110, 2, moment, (1, 221))
        assert rate == 28288 and wall == 48620 + 440 * moment
        count, residue = by_drive(residue, 28288, wall, at_most=1)
        extra += count * 440 * moment
        made += count
        chain.append((made, residue))
    ticks_52 = next(tick for tick, (m, _) in enumerate(chain, start=1) if m == 53)
    exact = Fraction(ticks_52 * 28288 - chain[ticks_52 - 1][1], 28288)
    # the Links counted against a stretched wall add their stretch (extra)
    assert exact == 1 + Fraction(52 * 48620 + extra - 4755, 28288)
    assert exact - 1 == 52 * Fraction(110, 64) - Fraction(4755 - extra, 28288)
    simulation = NatureBeamSimulation(parse_nature_beam_world(pace_world()))
    unit = simulation.tables.flight.labels
    seen: list[tuple[int, int]] = []
    for tick in range(1, 121):
        simulation.step()
        assert simulation.books()["balanced"], tick
        light = simulation.stores[0]
        assert light.size == 1, tick
        seen.append((int(light.made[0]), int(light.residue[0])))
        whole = Q * 221 * int(light.amount[0]) * int(light.content[0])
        held = [int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])]
        assert [
            whole * int(u) + w for u, w in zip(unit[int(light.direction[0])], held, strict=True)
        ] == [
            905216,
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


MATTER_FAMILIES = [
    {"name": "matter", "quantum": 1, "massive": True},
    {"name": "m", "quantum": 0, "charge": 0, "phase": False},
]


def matter_bar(optical: int | None, *, crowd_amount: int = 4, crowd_age: int = 3) -> dict[str, object]:
    """The bar of (a) with a massive lamp in place of the light's: the family
    `matter` (quantum 1, massive, momentum_magnitude 10 at width 1: E'_0 =
    64, E' = 66, the triple (20, 132, 66) on the heading), the two keys
    together (`massive_rows`, `action` 1024, `age_bound` 64); the lamp's
    reservoir the world's K = 4096, so that its turn is 1 and it births one
    row of content 1 per interval (a reservoir below K turns 0)."""
    document = bar(optical, crowd_amount=crowd_amount, crowd_age=crowd_age)
    document["model_id"] = "test-optical-matter-bar"
    document["massive_rows"] = True
    document["action"] = 1024
    document["age_bound"] = 64
    document["families"] = MATTER_FAMILIES
    measured = document["measured"]  # type: ignore[assignment]
    measured[0] = {  # type: ignore[index]
        "position": [0, 0, 0],
        "family": "matter",
        "amount": 4096,  # the world's K: the lamp's turn 1, one unit per birth
        "phase": 0,
        "fixed": True,
        "lamp": {
            "rate": [1, 1],
            "wheel": [1, 64],
            "directions": [[1, 0, 0]],
            "momentum_magnitude": 10,
        },
        "table": {"m": "pass"},
    }
    measured[1]["table"] = {"matter": "pass"}  # type: ignore[index]
    return document


def test_the_weight_per_unit_is_the_familys_energy_on_its_own_labels():
    """(k) Every family under one wall (2026-09-22, EVERY_FAMILY.md sections
    1 and 3): the energy per unit of amount of a direction on the family's
    labels, e_D = isqrt(3 u_D . u_D) = 110 for the photon on a heading (the
    rest 0), E'_D = isqrt(64^2 + 3 x 10^2) = 66 for `matter` (the rest 64);
    the weight (E'^2 + 3 gamma p . p) // E': the photon's 110 at gamma = 0
    (2 e_D = 220 until this day, unchanged) and (12100 + 12288) // 110 = 221
    at gamma = 1 (the one floor, 2 e_D + 1); matter's 66 and (4356 + 300)
    // 66 = 70 (70.5 floored), Newton's push on a slow row at gamma = 0."""
    light = NatureBeamSimulation(parse_nature_beam_world(turn_world(1))).tables.family_flights[0]
    assert light.rest == 0 and int(light.energy[PLUS_X]) == 110
    assert unit_weights(light, 0, np.array([PLUS_X])).tolist() == [110]
    assert unit_weights(light, 1, np.array([PLUS_X])).tolist() == [221]
    matter = NatureBeamSimulation(parse_nature_beam_world(matter_bar(1))).tables.family_flights[0]
    heading = int(np.flatnonzero((matter.labels == [10, 0, 0]).all(axis=1))[0])
    assert matter.rest == 64 and int(matter.energy[heading]) == 66
    assert (int(matter.rate[heading]), int(matter.wall[heading]), int(matter.start[heading])) == (
        20,
        132,
        66,
    )
    assert unit_weights(matter, 0, np.array([heading])).tolist() == [66]
    assert unit_weights(matter, 1, np.array([heading])).tolist() == [70]


def test_a_massive_row_walks_by_its_triple_under_the_wall_and_its_pair_is_its_momentums():
    """(l) and (m). (m): the bar of (a) with the massive lamp: the first
    row's accumulator is the family's triple under the one wall function,
    the rate 2 p d = 80 against the wall 2 E' (d + f n A) = 132 x 4 = 528
    off the crowd and 132 x 28 = 3696 on it, from the start E' d = 264: its
    x after the ticks 2 .. 40 by `by_drive` by hand (one Link per 6.6
    intervals off the crowd, per 46 on it), integer for integer. (l): a
    row never pushed carries its family's pair (20, 132); pushed along its
    momentum by W = (2560, 0, 0) (P doubled: P = (5120, 0, 0) over the gcd
    1024 with the rest term 16384 is (5, 0, 0) and 16, S_1 5, T =
    isqrt((16^2 + 3 x 25) x 4096) = 1164) its pace 640 / 2328 = 0.275
    against the triple's 20 / 132 = 0.152: a falling row speeds up."""
    acc, x, by_hand = 66 * 4, 0, []
    for _ in range(2, 41):
        moment = 12 if 4 <= x <= 8 else 0
        rate, wall = age_wall(20, 132, 2, moment, (1, 4))
        assert (rate, wall) == (80, 528 if moment == 0 else 3696)
        count, acc = by_drive(acc, 80, wall, at_most=1)
        x += count
        by_hand.append(x)
    assert by_hand[:4] == [0, 0, 0, 1] and by_hand[-1] == 4 and by_hand.count(4) > 10
    simulation = NatureBeamSimulation(parse_nature_beam_world(matter_bar(1)))
    table = simulation.tables.family_flights[0]
    walked: list[int] = []
    for tick in range(1, 41):
        simulation.step()
        assert simulation.books()["balanced"], tick
        store = simulation.stores[0]
        index = first_row(store)
        if index is None:
            continue
        if tick >= 2:
            walked.append(int(store.coordinates(store.node[index : index + 1])[0][0]))
        if tick == 6:
            assert int(store.content[index]) == 1 and int(store.amount[index]) == 1
            rate, wall = row_pairs(store, table, 4)
            assert (int(rate[index]), int(wall[index])) == (20, 132)
            store.push_x[index] = 2560
            rate, wall = row_pairs(store, table, 4)
            assert (int(rate[index]), int(wall[index])) == (640, 2328)
            assert isqrt((16 * 16 + 3 * 25) * Q * Q) == 1164 and 640 / 2328 > 20 / 132
            store.push_x[index] = 0
    assert len(walked) == 39 and walked == by_hand


def test_the_walls_square_is_refused_before_it_is_formed():
    """(n)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(matter_bar(1)))
    table = simulation.tables.family_flights[0]
    for _ in range(6):
        simulation.step()
    store = simulation.stores[0]
    index = first_row(store)
    assert index is not None
    store.push_x[index] = 2560
    store.amount[index] = 4  # the deciding world's largest amount: taken
    rate, wall = row_pairs(store, table, 4)
    assert isqrt((128 * 128 + 3 * 625) * 4096) == 8648
    assert (int(rate[index]), int(wall[index])) == (3200, 17296)
    store.amount[index] = 1 << 40  # R = 2^45 over the gcd 512: the square over the bound
    with pytest.raises(OverflowError, match="wall's square"):
        row_pairs(store, table, 4)
    with pytest.raises(OverflowError, match="wall's square"):
        simulation.step()


def test_the_last_links_time_is_one_form_and_the_counts_own_on_a_row_no_crowd_moved():
    """(g): the physics-rule reviewer's line on PR #855. The one form
    (age r - s + T d) / r of `optical_last_link` and the walk's `last_link`
    gives, on every row no crowd moved, the count's own floor made T_d /
    (S_1 Q) that `exact_phase` forms without `last_link`, floor for floor
    and as the same fraction; and `square_ladder` is the integer root's
    floor by comparisons alone."""
    from event_universe.core.integer import integer_root
    from event_universe.events.nature_beam import exact_phase, optical_last_link, square_ladder

    world = parse_nature_beam_world(
        {
            "law": "beam",
            "model_id": "one-form-test",
            "shape": [40, 5, 5],
            "boundary": "open",
            "ticks": 30,
            "K": 1,
            "N": 64,
            "release": [0, 1],
            "suspension": [1, 128],
            "age_bound": 200,
            "directions": [[3, 1, 0], [2, 1, 1], [5, 2, 1]],
            "families": [{"name": "light", "quantum": 1, "phase_per_link": [16, 3]}],
            "measured": [],
            "in_transit": [
                {
                    "position": [0, 2, 2],
                    "family": "light",
                    "number": 1,
                    "direction": direction,
                    "amount": 1,
                    "phase": 5 * k,
                }
                for k, direction in enumerate(([1, 0, 0], [3, 1, 0], [2, 1, 1], [5, 2, 1]))
            ],
        }
    )
    simulation = NatureBeamSimulation(world)
    checked = 0
    for _ in range(25):
        simulation.step()
        store = simulation.stores[0]
        table = simulation.tables.family_flights[0]
        for index in range(store.size):
            age = int(store.age[index])
            common = (
                int(store.phase[index]),
                age,
                age,
                int(store.direction[index]),
                simulation.tables.flight,
                world.families[0].phase_per_age,
                64,
                "test",
            )
            counted = exact_phase(*common, None)
            one_form = exact_phase(*common, optical_last_link(store, table, world, index, age))
            assert counted[0] == one_form[0], (index, age)
            assert Fraction(counted[1], counted[2]) == Fraction(one_form[1], one_form[2]), (index, age)
            checked += 1
    assert checked >= 40
    for value in (0, 1, 2, 3, 4, 15, 16, 17, 12288, 3 * 64 * 64 * 65536 - 1, MAX_WORK_INT):
        assert square_ladder(value) == integer_root(value) == isqrt(value)
    with pytest.raises(ValueError):
        square_ladder(-1)

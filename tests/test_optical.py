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
    [1, 4] and `optical` 1, the table with the twelve edge diagonals; a row of `light` (number 1, amount 1, content 1) at
    (1, 1, 0) on +x and a row of `m` (number 2, amount 1) at (2, 0, 0) on
    +y, both at age 0: in interval 1 both walk to (2, 1, 0), the m row's
    arrival is the flow **V** = (0, 64, 0) the light row reads at its Node,
    and its turn accumulator becomes **W** = -n x (1 + gamma) x content x
    e_D x **V** = -(1 x 2 x 1 x 110) x (0, 64, 0) = (0, -14080, 0); its whole
    momentum **P** = Q d content **u**_x + **W** = (16384, -14080, 0) is
    nearer to (1, -1, 0) (the cosines' exact comparison, 30464^2 x 1 >
    16384^2 x 2) so the label moves there and **W** += Q d content
    (**u**_x - **u**_(1,-1,0)) = 256 x (19, 45, 0): **W** = (4864, -2560,
    0), **P** conserved, and its residue 72 in the heading's units becomes
    144 in the diagonal's (S_1 2 over 1, (g)); the books' `turned` line of `light` (-19, -45, 0)
    (the label (45, -45, 0) less (64, 0, 0)) and the transit momentum
    (45, 19, 0) balanced; the m row (a free family, content 0) never turns;
(c) **P** is conserved across the turn: Q d content **u**_D + **W** before
    equals Q d content **u**_D' + **W** after, the row's amount, content,
    number and phase untouched;
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
    chief physicist's word on the residue's units at a turn (record 496):
    the flight's accumulator is the row's age paid at its direction's rate
    r = 2 S_1 Q d and the residue crosses a turn as the time of the last
    Link, s' = (s x S_new) // S_old, the count then capped at one Link by
    the primitive's `at_most` with the surplus kept. A GameBoard of
    8 x 3 x 1 at [1, 64] and `optical` 1, the fan the twelve edge
    diagonals with (24, +-1, 0) (the pin worlds' long direction: T_D 2662,
    S_1 25, the label (64, 3, 0), against the heading's T_D 110, S_1 1); a
    row of `light` at (1, 1, 0) and a row of `m` whose arrival at its Node
    pushes it. From (1, 0, 0) at age 5 (its pair (3, 90 x 64)) to
    (24, 1, 0): after the first walk the residue is 13952, rescaled 25 x
    13952 = 348800, above the long wall 340736 by 2.4 per cent (a Link
    already paid), the last Link's time 5 - 13952 / 8192 = 6 - 348800 /
    204800 unchanged; the chain of (made, residue) after each interval
    (3, 348800), (4, 202216), (5, 66280), (5, 271080), one Link in each of
    the second and third intervals, integer for integer with `by_drive` at
    `at_most` 1. From
    (24, 1, 0) at age 4 (its pair (2, 4814 x 64)) to (1, 0, 0): the
    residue 172160 after the first walk becomes 172160 // 25 = 6886 (the
    remainder 10 of 25 dropped, under one unit of the accumulator, the
    time within 1 / 8192 of an interval), the chain (3, 6886), (4, 558),
    (4, 8750), (5, 2862) against the heading's walls 14520, 14080, 14080. The head
    before the fix carried 172160 unscaled against 14520 (a raw count of
    12) and kept the residue of the uncapped count, 6112: twelve walls of
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
(h) S1 of the same review: the push accumulator's sums are tested against
    the working register before they are formed. The turn world of (b)
    with the light row's **W** preset: W_x = 2^63 - 1 - 14080 takes the
    push n weight V = 14080 at the bound (no turn, the row keeps +x);
    W_x one more refuses naming the rule; W_y = -(2^63 - 1 - 14080) takes
    the push at the bound and the turn's shift Q d content (u_D - u_D') is
    then refused at the register.
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
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
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    vectors = simulation.tables.flight.vectors
    assert simulation.tables.flight.energy[PLUS_X] == 110
    simulation.step()
    books = simulation.books()
    assert books["balanced"]
    light, crowd = simulation.stores[0], simulation.stores[1]
    assert light.size == 1 and crowd.size == 1
    assert vectors[int(light.direction[0])].tolist() == [1, -1, 0]
    assert (int(light.push_x[0]), int(light.push_y[0]), int(light.push_z[0])) == (4864, -2560, 0)
    # the residue 72 of the heading (S_1 = 1) rescaled to the diagonal's
    # (S_1 = 2) at the turn, 72 x 2 // 1 (record 496; (g))
    assert (int(light.made[0]), int(light.residue[0])) == (1, 144)
    assert light.coordinates(light.node[:1])[0][0] == 2 and light.coordinates(light.node[:1])[1][0] == 1
    assert books["momentum"]["turned"] == [-19, -45, 0] and books["momentum"]["transit"] == [45, 19, 0]
    assert (int(crowd.push_x[0]), int(crowd.push_y[0]), int(crowd.push_z[0])) == (0, 0, 0)
    assert vectors[int(crowd.direction[0])].tolist() == [0, 1, 0]
    # the same world without the key: the row keeps +x and no turn line
    plain = NatureBeamSimulation(parse_nature_beam_world(turn_world(None)))
    plain.step()
    assert plain.tables.flight.vectors[int(plain.stores[0].direction[0])].tolist() == [1, 0, 0]
    assert plain.books()["momentum"]["turned"] == [0, 0, 0]


def test_the_whole_momentum_is_conserved_across_the_turn():
    """(c)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    unit = simulation.tables.flight.labels
    before = Q * 4 * 1 * unit[PLUS_X] + 0
    simulation.step()
    light = simulation.stores[0]
    after = Q * 4 * 1 * unit[int(light.direction[0])] + [
        int(light.push_x[0]),
        int(light.push_y[0]),
        int(light.push_z[0]),
    ]
    # before the turn W = (0, -14080, 0) was the push of the interval
    assert (before + [0, -14080, 0]).tolist() == after.tolist() == [16384, -14080, 0]
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
    assert [expected["worlds"][n]["shift"] for n in ("mass_g0", "mass_g1", "near_g0", "near_g1")] == [
        -1.93,
        -3.86,
        -2.42,
        -4.83,
    ]
    assert [expected["worlds"][n]["delay"] for n in ("mass_g0", "mass_g1", "near_g0", "near_g1")] == [
        2.68,
        5.36,
        2.17,
        4.34,
    ]
    assert expected["ratios"]["mass"]["expected"] == 2.0 and expected["brackets"]["shift_pixels"] == 0.5


def test_the_residue_carried_across_a_turn_keeps_what_the_wall_paid_for():
    """(g)."""
    # By hand: the pair (rate, wall) per interval off the direction's
    # (S_1, T_D) and the crowd's age moment A at the row's Node, the count
    # capped at one Link by the primitive with the surplus kept, and the
    # residue rescaled by S_new / S_old where the direction changes.
    heading, long = (1, 110), (25, 2662)

    def chain(start: tuple[int, int], path: list[tuple[tuple[int, int], int]]) -> list[tuple[int, int]]:
        (made, residue), out = start, []
        for k, ((s1, t), moment) in enumerate(path):
            rate, wall = age_wall(2 * s1, 2 * t, 2, moment, (1, 64))
            count, residue = by_drive(residue, rate * Q, wall, at_most=1)
            made += count
            # the turn at the end of the interval: the residue rescaled to
            # the direction the row holds after it
            s_after = path[k + 1][0][0] if k + 1 < len(path) else s1
            residue = residue * s_after // s1
            out.append((made, residue))
        return out

    # From the heading at age 5 to the long direction: the m row arrives
    # from +y at (1, 1, 0) in interval 1 (V = (0, -64, 0)) and sits there.
    assert (5 * 128 + 110) // 220 == 3 and (5 * 128 + 110) % 220 == 90
    expected = chain((3, 90 * 64), [(heading, 0), (long, 1), (long, 0), (long, 0)])
    assert expected == [(3, 348800), (4, 202216), (5, 66280), (5, 271080)]
    assert 25 * 13952 == 348800 > 2 * 2662 * 64 == 340736  # a Link already paid
    assert Fraction(13952, 2 * 1 * Q * 64) == Fraction(348800, 2 * 25 * Q * 64)  # the time
    assert by_drive(348800, 204800, 2 * 2662 * (64 + 2 * 1), at_most=1) == (1, 202216)
    simulation = NatureBeamSimulation(parse_nature_beam_world(fan_world(PLUS_X, 5, [1, 2, 0], MINUS_Y)))
    vectors = simulation.tables.flight.vectors
    seen: list[tuple[int, int]] = []
    for tick in range(1, 5):
        simulation.step()
        assert simulation.books()["balanced"], tick
        light = simulation.stores[0]
        assert light.size == 1 and vectors[int(light.direction[0])].tolist() == [24, 1, 0]
        seen.append((int(light.made[0]), int(light.residue[0])))
        assert int(light.coordinates(light.node[:1])[0][0]) == min(tick, 3)
    assert seen == expected
    # From the long direction at age 4 to the heading: the m row arrives
    # from -y at (2, 1, 0) (V = (0, 64, 0)); the residue 172160 becomes
    # 172160 // 25 = 6886 against the heading's wall.
    assert (4 * 2 * 25 * Q + 2662) // 5324 == 2 and (4 * 2 * 25 * Q + 2662) % 5324 == 4814
    expected = chain((2, 4814 * 64), [(long, 0), (heading, 1), (heading, 0), (heading, 0)])
    assert expected == [(3, 6886), (4, 558), (4, 8750), (5, 2862)]
    assert 172160 // 25 == 6886 and 172160 % 25 == 10
    assert abs(Fraction(172160, 2 * 25 * Q * 64) - Fraction(6886, 2 * Q * 64)) < Fraction(1, 2 * Q * 64)
    assert by_drive(172160, 8192, 14520) == (12, 6112)  # the head's, unscaled and uncapped
    simulation = NatureBeamSimulation(parse_nature_beam_world(fan_world(LONG, 4, [2, 0, 0], PLUS_Y)))
    seen = []
    for tick in range(1, 5):
        simulation.step()
        assert simulation.books()["balanced"], tick
        light = simulation.stores[0]
        assert light.size == 1 and vectors[int(light.direction[0])].tolist() == [1, 0, 0]
        seen.append((int(light.made[0]), int(light.residue[0])))
        assert int(light.coordinates(light.node[:1])[0][0]) == 1 + tick - (tick >= 3)
    assert seen == expected


def test_the_push_accumulators_sums_are_tested_at_the_register():
    """(h)."""
    push = 1 * 2 * 1 * 110 * 64  # n x weight x |V| of (b)
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    light = simulation.stores[0]
    light.push_x[0] = MAX_WORK_INT - push
    simulation.step()
    assert simulation.books()["balanced"]
    light = simulation.stores[0]
    assert simulation.tables.flight.vectors[int(light.direction[0])].tolist() == [1, 0, 0]
    assert (int(light.push_x[0]), int(light.push_y[0])) == (MAX_WORK_INT - push, -push)
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_x[0] = MAX_WORK_INT - push + 1
    with pytest.raises(OverflowError, match="push accumulator"):
        simulation.step()
    simulation = NatureBeamSimulation(parse_nature_beam_world(turn_world()))
    simulation.stores[0].push_y[0] = -(MAX_WORK_INT - push)
    with pytest.raises(OverflowError, match="turn"):
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
            assert [whole * int(u) + w for u, w in zip(unit[int(light.direction[0])], held, strict=True)] == momentum, tick
        x, y, _ = (int(c[0]) for c in light.coordinates(light.node[:1]))
        if x >= 201:
            break
    assert x == 201 and tick < 400
    ex, ey = x - 2, y - 1  # from the push at (2, 1, 0)
    assert abs(ex * momentum[1] - ey * momentum[0]) <= 2 * momentum[0], (ex, ey)
    assert ey >= 11, (ex, ey)  # the tooth (24, 1, 0) reaches 8.3
    cross = (int(light.cross_x[0]), int(light.cross_y[0]), int(light.cross_z[0]))
    assert cross != (0, 0, 0)

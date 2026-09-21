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
    0), **P** conserved; the books' `turned` line of `light` (-19, -45, 0)
    (the label (45, -45, 0) less (64, 0, 0)) and the transit momentum
    (45, 19, 0) balanced; the m row (a free family, content 0) never turns;
(c) **P** is conserved across the turn: Q d content **u**_D + **W** before
    equals Q d content **u**_D' + **W** after, the row's amount, content,
    number and phase untouched;
(d) the refusals at load, naming the rule: `optical` with `suspension` 0,
    with `meeting`, gamma -1, true, "2" or 1.5, and the six headings alone
    (a direction without a neighbour within a right angle); a world with the key carries the identity `optical-v1` and
    `run.json`'s block {"gamma", "flight_coefficient"};
(e) byte identity without the key: a world without `optical` has every
    row's `made`, `residue` and turn fields 0 through its run and its
    state's rows carry no `flight` or `turn` key (the gate set's digests
    are `tests/test_amplitude_click.py` (d)); the set of the age wall is
    the law's without the key and gains ("flight", 1 + gamma) with it, the
    phase per age never a member;
(f) the pin worlds (`examples/events/optical/`): the six shipped worlds
    equal their generator's, parse with the identity, run ten intervals
    balanced, and the register carries the pins before the run (the
    shifts -1.93 / -3.86 and -2.42 / -4.83 pixels, the delays, the ratio
    2.00 with its bracket); the inverse interval is refused under the key.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from event_universe.core.integer import age_wall, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.measured import AGE_WALL_NEVER, AGE_WALL_SET, age_wall_set
from event_universe.events.world import HEADING_OFFSET, OPTICAL_RULE, Q
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "optical"
PLUS_X, PLUS_Y = HEADING_OFFSET, HEADING_OFFSET + 2
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
    assert (int(light.turn_x[0]), int(light.turn_y[0]), int(light.turn_z[0])) == (4864, -2560, 0)
    assert (int(light.made[0]), int(light.residue[0])) == (1, 72)
    assert light.coordinates(light.node[:1])[0][0] == 2 and light.coordinates(light.node[:1])[1][0] == 1
    assert books["momentum"]["turned"] == [-19, -45, 0] and books["momentum"]["transit"] == [45, 19, 0]
    assert (int(crowd.turn_x[0]), int(crowd.turn_y[0]), int(crowd.turn_z[0])) == (0, 0, 0)
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
        int(light.turn_x[0]),
        int(light.turn_y[0]),
        int(light.turn_z[0]),
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
        for name in ("made", "residue", "turn_x", "turn_y", "turn_z"):
            assert not getattr(store, name).any(), name
    lines = [
        ray
        for node in simulation.snapshot()["nodes"]  # type: ignore[union-attr]
        for family in node["families"]
        for ray in family["rays"]
    ]
    assert lines and not any("flight" in ray or "turn" in ray for ray in lines)
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

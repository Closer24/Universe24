"""The one great clock test: the 48 (the great clock run from a setting and from each of its 48 images, the signed permutations of the axes about the origin; the fittings and the regulator's and the unsprung gear's notches compared through the image, the 24 rotations alike under the bobs' click with its crossing read even, the 24 reflections apart under the default: A2's standing item, named), the rewind exact through fittings and turnovers, the chiral setting's fittings with both twists and the sweep summed to 0."""

from __future__ import annotations

import copy
import functools
import itertools
import json
from typing import Any

import numpy as np
import pytest

from event_universe import gates as table
from event_universe import hands, readings, unwind
from event_universe import run as record
from event_universe import run as writer
from event_universe.clock import Clock
from event_universe.core import rates
from event_universe.core.spokes import AXES, SPOKES
from event_universe.meshes import factors, train_lead
from event_universe.trains import REGULATOR
from event_universe.unspring import fitted_advanced, fitted_windings_of, unsprung_notches
from tests.laws import level_at, node_of, refused, run_back_exact, state_of, world_of

# rotations alike per part: the trace 6 (6, 0, 0, 0 under GP-S1 at the trace 54; 6, 6, 6, 6 under CK-S1 even); IMAGED the images' ticks
CUBE, INTERVALS, GROUPS, IMAGED = 5, 20, 16, 14
# the 48 in sixteen parts of three (four parts of twelve before, (3, 0, 0, 0)): the rotations 0, 24 and 32 EQUAL at the trace 6, the chiral setting's to 14 (its 2 fittings by 13 under the great clock's bounds, 5 at the wave) under the wave's light as the hole's to 20 before it
COUNTED = ("births", "laid_back", "refused_stop")  # the counts the EQ-S1 test reads per piece
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def image(m: Any, clock: tuple[int, ...], cube: int) -> tuple[int, ...]:
    return tuple(int(x) % cube for x in m @ np.array(clock, dtype=int))


def births_of(clock: Clock) -> list[tuple[Any, ...]]:
    return sorted(
        (e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"]))
        for e in clock.log
        if e["event"] == "birth"
    )


def mapped(births: list[tuple[Any, ...]], m: Any, cube: int, exchanged: bool) -> list[tuple[Any, ...]]:
    found = [
        (i, image(m, at, cube), s, image(m, mi, cube), image(m, pl, cube)) for i, at, s, mi, pl in births
    ]
    return sorted((i, at, s, pl, mi) if exchanged else (i, at, s, mi, pl) for i, at, s, mi, pl in found)


def world_image(piece: dict[str, Any], m: Any, cube: int) -> dict[str, Any]:
    found = dict(piece, shape=[cube] * 3, seed=[dict(setting) for setting in piece["seed"]])
    for setting in found["seed"]:
        for key in ("at", "centre"):
            if key in setting:
                setting[key] = list(image(m, tuple(setting[key]), cube))
    return found


def run(calibre: dict[str, Any], piece: dict[str, Any]) -> Clock:
    clock = Clock(calibre, piece)
    for _ in range(IMAGED):
        clock.tick()
    return clock


def same_rows(base: Clock, other: Clock, m: Any) -> bool:
    for gear_b, gear_o in (
        (base.train(REGULATOR).gears[0], other.train(REGULATOR).gears[0]),
        (base.unsprung().gears[0], other.unsprung().gears[0]),
    ):
        for at in np.ndindex(CUBE, CUBE, CUBE):
            there = image(m, at, CUBE)
            if int(gear_b.now[at]) != int(gear_o.now[there]) or int(gear_b.before[at]) != int(
                gear_o.before[there]
            ):
                return False
    return True


@functools.cache
def seed_run() -> tuple[Clock, list[tuple[Any, ...]]]:
    calibre, piece = world_of("world_nature.json")
    base = run(calibre, world_image(piece, np.eye(3, dtype=int), CUBE))
    return base, births_of(base)


def images_hold(group: int) -> None:
    """The images of one part of the 48 (every sixteenth from the group's first; the setting's own run once per worker, `seed_run`, so each part is three runs under 15 s alone): under the one mirror (David's DAVID-THE-ONE-MIRROR.md: the turnover mirrors every fine tooth about its mid tooth, the ratchet counting it, and the vernier reads each gear's digit in the frame of its own displacement at the clock-node) and the order-free click (DAVID-THE-ORDER-FREE-STRIKE.md: every take read on the phase's start board) every rotation of the cube's 24 runs alike, the trains and the fittings, and with the shears struck (the Scribe's R11, the owner's yes of 2026-10-28, 02:2x UTC) every reflection too through the chiral setting's 14 ticks, its one fitting at 5 decided alike with its two children exchanged (DAVID-THE-MIRRORS-FITTING.md; with the shears every reflection parted there, 3 of 24 rotations alike before the one mirror); before them, a rotation that negates no axis runs alike the setting through the image (the trains and the fittings), a rotation negating the y or the z axis runs alike too once the bobs' click reads the crossing even (24 of 24 at 20 ticks on the hole setting, 56 chimes and 16 fittings under PL-S1, 209 chimes and 20 fittings under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting), 12 fittings under the former drive of 2 W after the step; 6 of 24 under the crossing odd at a touch of zero, the form `b < 0 <= n or n < 0 <= b`, which parted a negated gear at its touch of zero: A2's standing item, 6 of 24 under MS-S1 against 24 before it, read now to the odd crossing), every reflection apart; the counts held by name so that an image coming alike or parting is read. Under GP-S1 (the fitted hands advanced with the sweep's sign, the owner's word of 2026-10-26, 04:3x UTC) the rotations negating an axis part at the tick 19 (18 of 24 apart, 6 alike in the first part, 24 of 24 alike before): the state alike through 18, and at the 19th click the unspringing candidates' vernier reads the negated gears' fine teeth r against W - 1 - r in its digits, so the image's vernier picks another fitted hand (the train 0 against 2 at four clocks) and makes its fittings at the other four of eight symmetric sites: A48-S1's open read of the fine tooth in the image (the centred pick, held unbuilt), named here and not this advance's. Under the wave's light (the take by the wind's own fall, David's part-B seeds) the hole setting fits nothing before its tick 53, so the images run the chiral setting to 14: its 2 fittings by 13 under the great clock's bounds (5 at the wave), the identity and the two turns that cycle the axes (0, 24, 32) alike, the 21 other rotations and every reflection apart, ALIKE as at the hole's 20 before."""
    calibre, piece = world_of("world_nature.json")
    base, fittings = seed_run()
    assert len(fittings) > 0
    alike, rotations = (
        {True: 0, False: 0},
        sum(round(np.linalg.det(m)) == 1 for m in IMAGES[group::GROUPS]),
    )
    for m in IMAGES[group::GROUPS]:
        other = run(calibre, world_image(piece, m, CUBE))
        reflection = int(round(np.linalg.det(m))) == -1
        same = same_rows(base, other, m) and births_of(other) == mapped(fittings, m, CUBE, reflection)
        alike[reflection] += same
    assert alike == {False: rotations, True: len(IMAGES[group::GROUPS]) - rotations}  # all 48 (R11)


def test_the_run_back_is_exact_through_births_and_turns() -> None:
    clock = node_of("world_hole.json")
    for _ in range(INTERVALS):
        clock.tick()
    assert run_back_exact(clock, 40) == 40
    assert clock.counts["births"] > 0 and clock.counts["turns"] > 0  # the forward run's tallies


def test_the_chiral_seed_births_both_hands_and_the_charge_sums_to_zero() -> None:
    seed = world_of("world_nature.json")[1]["seed"]  # the packets of light at 5 quanta (2 in the world)
    clock = node_of("world_nature.json", seed=[dict(s, quanta=5) if "quanta" in s else s for s in seed])
    for _ in range(INTERVALS):
        clock.tick()
    births = [e for e in clock.log if e["event"] == "birth" and "exact_lay" not in e]
    assert len(births) == 3  # the shears struck (4 with them; 12 by 13 before the one mirror)
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs
    assert all(b["taken"] + b["remainder_was"] - b["remainder"] == b["booked"] for b in births)  # EX-S1
    twists = {1 if tuple(b["plus"]) > tuple(b["minus"]) else -1 for b in births}
    assert twists == {1, -1}


@pytest.mark.parametrize("group", range(GROUPS))
def test_each_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged(group: int) -> None:
    images_hold(group)


def test_the_uniform_pair_at_every_node_returns_with_the_whole_board_turning_at_once_ma() -> None:
    """MA-S1 by the fourth form of the file (the owner's word of 17:57 through the Boss, 6401141446; ma2's spelling, the Boss's 6401095909) with EQ-S1 in cs7's letter (6403341352): the pair of the heavy train set at every clock of the 3-cube at one winding (tests/worlds/world_pair_3.json, {"lay": "sea", "row": 2, "quanta": 1, "sense": 0}: the hand length 96, ma1's, three_now 192 the two senses summed, W 0) keeps every clock alike to the integer (400 of 400), turns every clock over at once at both tops (27 at 84 and at 252; 85, ma1's, before the wave), fits nothing, and returns to Gamma EXACTLY at 167 and 336 (169 and 334 before the wave; ma1's 168 / 169 and 333 / 334); under the great clock's bounds (act 12: a chime where nothing arrives takes nothing) a bob chimes at every clock at 4, 6 and 12, at 168, 170 and 172 after the first return and at 336, 338, 340, 342 and 348 from the second, 297 chimes every one credited laid back with nothing taken (nothing arrives at a clock of the great clock alike; under the wave's honest books 27 at 336 returned and the 270 others jammed by the stop, the light of one quantum a clock paying no heavy bob's winding before the return; 297 chimes before the wave, 27 at each of 4, 6 and 8 and after each return); before EQ-S1 the unwind stood and the bottoms read 953 at 171 and 888 at 342 with 351 chimes and the second top at 255 (992 and 966 with 162 chimes under the upward crossing alone); the rewind exact 10 of 10."""
    clock = node_of("world_pair_3.json")
    assert int(clock.by_index[2].gears[0].now.min()) == int(clock.by_index[2].gears[0].now.max()) == 192
    kept = copy.deepcopy(clock)
    alike, tops, means = 0, 0, []
    for _ in range(400):
        clock.tick()
        x = [int(v) for v in clock.train(REGULATOR).gears[0].now.reshape(-1)]
        alike += min(x) == max(x)
        means.append(sum(x) // len(x))
        if clock.turned_over.any():
            tops += 1
            assert (clock.ticks, int(clock.turned_over.sum())) in ((84, 27), (252, 27))
    bottoms = [
        (k + 1, means[k]) for k in range(1, 399) if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]
    chimes = [e for e in clock.log if e["event"] == "credit"]
    assert (alike, tops, clock.counts["births"], len(chimes)) == (400, 2, 0, 297)  # 27 at the wave
    assert bottoms == [(167, 1000), (336, 1000)] and sum(1 for c in chimes if c["i"] == 336) == 27
    assert (clock.counts["laid_back"], clock.counts["refused_stop"]) == (297, 0)  # (27, 270) at the wave
    assert run_back_exact(kept, 10) == 10


def test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_exactly_pl_s1() -> None:
    """PL-S1 (the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423; pl1's test_pl1.py and pl2's test_pl2.py brought to the engine's own path): nature's plasma on the 3-cube (tests/worlds/world_plasma_3.json, the heavy train at +1 and the light train at -1 at every clock) to 170 tops at 85 with 27 turning over (84 before the wave), the fall's state at top + k the reverse of the rise's at top - 1 - k in every notch and fine tooth at 84 of 84 k (83 of 83 before the wave; before PL-S1 the sign train's time gear's drive fine tooth parted at k = 1 by 2 (W(83) - W(82)) = 32, its notch at k = 8 and X at k = 9), X = Gamma at every clock at 168 and 169 and nowhere else (166 and 167 before the wave; the bottom 1,000 at 167, 939 before PL-S1), the bobs' 162 chimes, 135 in the rise (5 to 13) and 27 at 169, every one credited laid back with nothing taken under the great clock's bounds (act 12: nothing arrives at a clock of the plasma alike; no chime standing under the wave's honest books, the 162 jammed by the stop, one light quantum a clock paying no heavy bob's winding; 162 chimes with 135 in the rise, every one returned, before the wave), fittings 0, the release advanced 0, the rewind exact 10 of 10 through the top (170 back to 80), 107 integers, the bits within 128."""
    clock = node_of("world_plasma_3.json")
    states, kept, exact, tops = [], [], [], []
    for _ in range(170):
        states.append([[gear.copy() for gear in train] for train in clock.trains()])
        if 80 <= clock.ticks < 90:
            kept.append(state_of(clock))
        clock.tick()
        x = clock.train(REGULATOR).gears[0].now
        exact.append(int(x.min()) == int(x.max()) == clock.full_rate)
        if clock.turned_over.any():
            tops.append((clock.ticks, int(clock.turned_over.sum())))
    states.append([[gear.copy() for gear in train] for train in clock.trains()])
    chimes = [e for e in clock.log if e["event"] == "credit"]
    top = tops[0][0]
    assert tops[0] == (85, 27) and [i + 1 for i, e in enumerate(exact) if e] == [168, 169]
    returned = sum(1 for c in chimes if "laid_back" in c and c["taken"] == 0)
    assert (len(chimes), returned, clock.counts["refused_stop"]) == (162, 162, 0)
    assert clock.counts["births"] == clock.counts["laid"] == 0
    assert record.census(clock)[0] == 95  # the shears struck; 107 with them, 99 and 98 before
    for _ in range(80):
        clock.tick(-1)
    assert sum(state_of(clock) == kept[9 - k] for k in range(10) if not clock.tick(-1)) == 10
    everywhere = np.ones(clock.size, dtype=bool)

    def text(trains: list[list[Any]], backward: bool) -> bytes:
        clock.set_trains([[gear.copy() for gear in train] for train in trains])
        if backward:
            clock.reverse(everywhere, trains)
        return record.state_text(clock)

    assert (
        sum(text(states[top + k], False) == text(states[top - 1 - k], True) for k in range(1, top)) == 84
    )


def test_the_body_at_rest_lays_back_what_it_takes_and_the_light_stays_whole_eq_s1() -> None:
    """EQ-S1 in cs7's letter (CS7-S1; the owner's word of 2026-10-25, 17:57 UTC, through the Boss's recommendation, 6402908585 and 6403341352; eq1's test_eq1_equilibrium.py and eq2's test_eq2.py re-read on the engine's own path): on the even pair of the 3-cube the unsprung train's lead across the six meshes sums to 0 at every clock at every tick's start (nothing arrives), every chime under the great clock's bounds takes nothing (act 12: credited laid back with its notches, its take and its laid_back 0, its push tallied 0) and leaves the unsprung gear's notch at its clock, on the gear a take would move, as it found it (the unsprung hand whole), 27 chimes at each of 4, 6, 12, 168, 170, 172 and 336, 189 by 337 with no jam of the stop (27 at 336 under the wave's honest books, laid_back equal to their notches, the 162 earlier jammed by the stop; 27 at each of 4, 6 and 8, 81 in 20 ticks with no jam of the stop, before the wave; before EQ-S1 the great clock, its unsprung hand unwound, chimed at 10 and 13 too), the rewind exact 10 of 10; on the hole setting of the 5-cube to 60 (its seed 57 and 58 at two packets, so no mirror of the cube maps it to itself, Curie's principle) every chime stands at a clock whose net lead is not 0 (something arrives), none returned, 529 chimes and 22 births with the shears struck (877 and 23 with them under the one mirror and the order-free click; 920 chimes from 21 to 60 and 17 births with the lead at the kick at the seed 56 (885 under the great clock's bounds, its 17 births 4 of them unspringings; 8 chimes at 59 and 60 and 6 births under the wave's light; 15 fittings and 489 chimes at 20 before the wave; 56 chimes and 16 fittings under PL-S1 (209 chimes and 20 fittings under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 12 fittings with the same 56 chimes under the former drive of 2 W after the step, as before EQ-S1: the charts where light flows bit for bit under it))), the rewind exact."""
    found = {}
    for piece, quiet, ticks in (("world_pair_3.json", True, 337), ("world_hole.json", False, 60)):
        clock, kept = node_of(piece), node_of(piece)
        by_tick: dict[int, int] = {}
        for _ in range(ticks):
            gears = clock.unsprung().gears
            net = sum((train_lead(gears, spoke) for spoke in range(SPOKES)), start=0)
            seen = len(clock.log)
            clock.tick()
            chimes = [e for e in clock.log[seen:] if e["event"] == "credit"]
            for c in chimes:
                at = tuple(c["node"])
                assert (int(net[at]) == 0) == ("laid_back" in c) == quiet
                if quiet:
                    assert c["laid_back"] == c["levels"] == c["taken"] == 0 and c["dP_take"] == [0] * 3
                    assert int(clock.unsprung().gears[c["taken_line"]].now[at]) == c["taken_now_was"]
            by_tick[clock.ticks] = len(chimes)
        counts = clock.counts
        found[piece] = ({i: n for i, n in by_tick.items() if n}, *(counts[k] for k in COUNTED))
        assert run_back_exact(kept, 10) == 10
    assert found["world_pair_3.json"] == (dict.fromkeys((4, 6, 12, 168, 170, 172, 336), 27), 0, 189, 0)
    assert (
        found["world_hole.json"][1:3] == (22, 0) and sum(found["world_hole.json"][0].values()) == 529
    )  # the shears struck (23 and 877 with them; 17 and 920 before the one mirror at the seed 56)


def test_the_bare_sea_returns_exactly_with_the_whole_board_turning_at_once_bb() -> None:
    """BB-S1 and MA-S1 read by gate 1 from the clock lines (the Boss's 6400540638 and 6400767119 (2); The-Uniform-Board-Returns_COMPARISON.md section 4): the sea alone on the 3-cube to 240 (tests/worlds/world_sea_3.json, the Universe setting that returns) tops at 58 and 173 with all 27 clocks turning over at once, returns to the setting's first pair of states at 115 and 230 (its last line at the resolution; the former predicate's bottoms at Gamma the same), the swings numbered 1, 115 and 230 with no fitting and no chime between them; the chart read through the table, gate 1 SHOWN, gate 46 NOT SHOWN (no bob in the later cycle), the rewind exact 10 of 10."""
    calibre, piece = world_of("world_sea_3.json")
    found = json.loads(json.dumps(writer.chart(calibre, piece, 10, lambda line: None)))
    out = table.gates(found)
    swing = json.loads(json.dumps(out["1 recurring bangs"]))
    assert swing["tops with every Node turning at once (interval)"] == [58, 173]
    assert swing["bottoms (interval, mean X, at Gamma at every Node, the resolution)"] == [
        [115, 1000, True],
        [230, 1000, True],
    ]
    assert swing["exact returns to the seed's first state (interval)"] == [115, 230]
    assert swing["bangs numbered (the interval each begins)"] == [1, 115, 230]
    assert swing["births and body credits between the bangs"] == [[0, 0], [0, 0], [0, 0]]
    assert swing["verdict"].startswith("SHOWN: 2 exact returns")
    assert out["46 the bangs recurring with the same gates"]["verdict"].startswith("NOT SHOWN")
    assert found["run_back"] == {"intervals": 10, "exact": 10} and found["counts"]["births"] == "0"
    calibre, piece = world_of("world_pair_3.json")
    tied = table.gates(
        json.loads(json.dumps(writer.chart(calibre, dict(piece, intervals=672), 0, lambda line: None)))
    )  # the pair's bobs chime at 336 and 672 under the wave's light (at 4, 6 and 8 by 12 before it)
    assert len(tied["2 the Links lengthening in the clicks"]["at"]) == 3  # every clock's spacing ties


def test_the_moving_lay_runs_at_its_momentum_over_twice_its_share_mv() -> None:
    """MV-S1 to MV-S3 (the Boss's ledger item 7, The-Moving-Lay-With-A-Wave-Number_COMPARISON.md's section for David): the heavy train's pair of 3 windings set under the sea at the centre of the 9-cube with the stride h = rim div 2 along x (k = pi / 3 exactly): W 0 at every clock of every setting, the wind centroid's step at each of the first four clicks (the rates still the vacuum's, before the sea deepens the great clock) within 40 milli-meshes per tick of (1000 P) div (2 E) by cross multiplication (P_x = 2 pinion SUM_i (now_(i+x) before_i - now_i before_(i+x)) over the two gears, E the wind summed), a top of 3 clocks above the width-2 value, stride 0 hash-equal to no stride, the refusals by name, the rewind exact through 10."""
    calibre, piece = world_of("world_packet.json")
    rim, milli = int(calibre["integers"]["den"]), 1000
    packet = {"lay": "at", "row": 2, "centre": [4, 4, 4], "width": 2, "quanta": 3}
    moving = dict(packet, wave=[rim // 2, 0, 0])

    def ints(a: Any) -> list[int]:
        return [int(x) for x in a.reshape(-1)]

    def laid(setting: dict[str, Any]) -> tuple[Clock, int]:
        clock = Clock(calibre, dict(piece, seed=[{"lay": "sea", "row": 0}, setting]))
        hand = clock.by_index[2]
        re, im = hand.gears
        assert hand.ratio is not None and not any(ints(re.now * im.before - im.now * re.before))
        wind = sum(
            ints(
                hands.wind(
                    clock,
                    hand.gears,
                    readings.gearing(clock, hand.ratio, readings.load(clock), factors(clock)),
                )
            )
        )
        push = sum(
            sum(
                ints(
                    np.roll(gear.now, -1, axis=0) * gear.before
                    - gear.now * np.roll(gear.before, -1, axis=0)
                )
            )
            for gear in hand.gears
        )
        return clock, milli * 2 * hand.ratio[0] * push // (2 * wind)

    def centroid(clock: Clock) -> tuple[int, int]:
        hand = clock.by_index[2]
        assert hand.ratio is not None
        wind = hands.wind(
            clock, hand.gears, readings.gearing(clock, hand.ratio, readings.load(clock), factors(clock))
        )
        return sum(ints(wind * np.indices(clock.size)[0])), sum(ints(wind))

    clock, law = laid(moving)
    assert laid(dict(moving, top=3))[1] > law > 0
    kept = copy.deepcopy(clock)
    before = centroid(clock)
    for _ in range(4):
        clock.tick()
        after = centroid(clock)
        step, scale = milli * (after[0] * before[1] - before[0] * after[1]), after[1] * before[1]
        assert abs(step - law * scale) <= 40 * scale, (law, step // scale)
        before = after
    assert clock.counts["births"] == 0 and run_back_exact(kept, 10) == 10
    rest, zero = laid(packet)[0], laid(dict(packet, wave=[0, 0, 0]))[0]
    for _ in range(2):
        assert record.state_hash(rest) == record.state_hash(zero)
        rest.tick()
        zero.tick()
    for bad, match in (
        (dict(moving, wave=[rim + 1, 0, 0]), "beyond the band's edge"),
        (dict(moving, row=0, wave=[0, 0, 0]), "the gap-0 row at the wave 0"),
        (dict(moving, top=9), "a top is an odd count"),
        (dict(moving, interval=3), "a field of no form"),
    ):
        refused(match, Clock, calibre, dict(piece, seed=[bad]))


def test_the_moving_lay_is_carried_by_the_48_with_its_centre_and_wave_mv() -> None:
    """MV-S1's 48 (vf5's item (a), the Boss's 6401916517; The-Moving-Lay-With-A-Wave-Number_COMPARISON.md's spec: the 48 with the centre and the stride transformed): the heavy train's pair of 3 windings set under the sea on the 5-cube at the stride [rim div 2, rim div 3, 0] and run two ticks, against the 48 pieces whose centre and stride are the image's: carried back by the image's inverse, the regulator's X and the train's three-o'clock gears equal bit for bit, the twelve-o'clock gears equal under a rotation and negated under a reflection (the senses exchanged), 24 and 24, 0 apart."""
    calibre, piece = world_of("world_packet.json")
    rim, cube, centre = int(calibre["integers"]["den"]), 5, [2, 2, 1]
    stride = [rim // 2, rim // 3, 0]

    def moved(g: tuple[tuple[int, ...], tuple[int, ...]], x: list[int], wrap: int) -> list[int]:
        pi, s = g
        y = [0, 0, 0]
        for a in range(3):
            y[pi[a]] = (s[a] * x[a]) % wrap if wrap else s[a] * x[a]
        return y

    def run(g: tuple[tuple[int, ...], tuple[int, ...]]) -> Clock:
        setting = {
            "lay": "at",
            "row": 2,
            "centre": moved(g, centre, cube),
            "width": 2,
            "quanta": 3,
            "wave": moved(g, stride, 0),
        }
        clock = Clock(
            calibre, dict(piece, shape=[cube] * 3, intervals=2, seed=[{"lay": "sea", "row": 0}, setting])
        )
        clock.tick()
        clock.tick()
        return clock

    def back(a: Any, g: tuple[tuple[int, ...], tuple[int, ...]]) -> Any:
        out = np.empty_like(a)
        for idx in np.ndindex(*a.shape):
            out[idx] = a[tuple(moved(g, list(idx), cube))]
        return out

    base = run(((0, 1, 2), (1, 1, 1)))
    alike = {1: 0, -1: 0}
    for pi in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            g = (pi, s)
            det = (
                (-1) ** sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
                * s[0]
                * s[1]
                * s[2]
            )
            img = run(g)
            same = bool(
                (back(img.train(REGULATOR).gears[0].now, g) == base.train(REGULATOR).gears[0].now).all()
            )
            for (lb, li), sign in zip(
                zip(base.by_index[2].gears, img.by_index[2].gears, strict=True), (1, det), strict=True
            ):
                same = same and bool(
                    (back(li.now, g) == sign * lb.now).all()
                    and (back(li.before, g) == sign * lb.before).all()
                )
            alike[det] += same
    assert alike == {1: 24, -1: 24}


def test_one_pair_in_several_rows_births_the_conjugate_pair_at_every_node_cs5_s2() -> None:
    """CS5-S2 (the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss, 6404425423; cs5's REPORT.md section 4 and cs7's section 3.3: the file universe_ga2 and the `wave` setting of cs3's cycle form in cs5's and cs7's spelling): the calibre file names one ratio in two trains (tests/worlds/universe_ga2.json, 115,762,739,551,980 twice) and the assembly admits it as written, two hands with the same numbers and one winding, the reckoner one name for both; under the one mirror (David's DAVID-THE-ONE-MIRROR.md: the vernier reads a negated gear's digit alike its mirror's) the cycle great clock fits nothing by 20: the draw picks one train at every clock-node, so two children of one hand land at every clock-node and the crowd jams all 64 (children_at_one_node 2, at i 1 with the shears struck and at i 2 with them, the lay standing at the other), no chime, no turnover, X 1,050 at i 2 and 1,860 at i 10, the rewind exact 20 of 20, 84 integers, 115 bits; before it, the digit r div F told a negated gear from its mirror and the 4-cube with no sea under the cycle setting at 5 windings (tests/worlds/world_ga2.json: the hand length 300 at every clock, logged with its digits and the sense 1) fitted 0 at i 1 (64 advance jams, the unsprung hand's own train picked by the vernier where it stands; cs5's hh3 read 64 crowd jams there) and 64 at i 2 at 64 of 64 clocks, every clock one fitted hand of the train 0 and one of the train 1 at W -18,000 / +18,000 (the reflected pair of the hand at the clock, the crowd jamming nothing: two hands, not one), unwound at or above tallied on 64 of 64, X 1,050 at 64 of 64 at i 2 and 1,880 at i 10 (cs5's and cs7's numbers to the integer), 640 chimes by 20, 128 at each of i 7, 9, 11, 13 and 15 (64 a train), every one credited laid back with nothing taken under the great clock's bounds and the own beat (act 12: nothing arrives at a chiming clock of the cycle great clock; 128 at i 13, every one returned, and 512 jammed by the stop at i 7, 9, 11 and 15 under the wave's honest books; 256 before the wave, 128 at i 8 and 128 at i 10, every one returned under EQ-S1; cs7 read 128 at i 10 alone on its head before CK-S1's crossing in either direction) every one reckoned from the clicks to the one species `gapped 0` whichever train it stands on (640 of 640 right, 128 of 128 at the wave, 256 of 256 before it, 128 tracks right), the rewind exact 20 of 20, 96 integers (89 before the slack and the beats' references), 115 bits; the setting refused by name off the unsprung hand, with a field of no form, off Z_4, off the flip 0 and 1, on a cube not a multiple of 4; the mirror 1 leaves every fine tooth at its mid tooth, the one mirror's fixed point, and the notches (the former flip moved the fine tooth on the 32 negated clocks of each gear); under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting) the cycle great clock fitted NOTHING: the vernier at the first click refused as the origin at 64 reads (every folded fine tooth at the setting's half on the great clock alike), 1,216 advances jammed after it, no chime, no turnover by 20, Gamma exactly at 198 and 199 to 230: the pattern's digits were tuned to this read, named for the Boss and the hand on the fittings' setting."""
    calibre, piece = world_of("world_ga2.json")
    seed = piece["seed"][0]
    found = json.loads(
        json.dumps(writer.chart(calibre, dict(piece, intervals=20), 20, lambda line: None))
    )
    assert found["planes"][0] == found["planes"][1] != found["planes"][2]
    lay = [e for e in found["log"] if e["event"] == "lay"]
    assert len(lay) == 1 and (lay[0]["amplitude"], lay[0]["p1"], lay[0]["sense"]) == (300, seed["p1"], 1)
    jams = [e for e in found["log"] if e["event"] == "refused" and e["cause"] == "lay"]
    first, second = ([e for e in jams if e["i"] == i] for i in (2, 1))
    assert (
        not [e for e in found["log"] if e["event"] in ("birth", "credit")]
        and found["counts"]["turns"] == "0"
    )
    assert len(first) == 64 and all(
        "standing" in e for e in first
    )  # 64 births at i 2 before the one mirror
    assert len(second) == 64 and {e["children_at_one_node"] for e in second} == {2}
    assert (set(found["nodes"][1]["X"]), set(found["nodes"][9]["X"])) == ({1050}, {1860})  # 1,880
    assert found["run_back"] == {"intervals": 20, "exact": 20}
    assert ({r["integers"] for r in found["rows"]}, max(r["max bits"] for r in found["rows"])) == (
        {84},  # the shears struck (96 with them, the beats' references two a hand; 90, 89 before)
        115,
    )
    for match, change in (
        ("the plane at the gap 0", {"row": 1}),
        ("a field of no form", {"sense": 1}),
        ("each of Z_4", {"p1": seed["p1"][:15] + [4]}),
        ("each of Z_4", {"cz": 4}),
        ("mirror is 0 or 1", {"mirror": 2}),
    ):
        refused(match, Clock, calibre, dict(piece, seed=[{**seed, **change}]))
    refused("a multiple of 4", Clock, calibre, dict(piece, shape=[3, 3, 3]))
    plain, flipped = (Clock(calibre, dict(piece, seed=[{**seed, "mirror": m}])) for m in (0, 1))
    for a, b in zip(plain.unsprung().gears, flipped.unsprung().gears, strict=True):
        assert (
            (a.now == b.now).all()
            and (a.before == b.before).all()
            and int((a.fine != b.fine).sum()) == 0  # the mirror's fixed point (32 under the flip)
        )


def test_the_pair_at_rest_merges_into_light_by_its_own_quantum_taken_whole_mg_s1() -> None:
    """MG-S1 (the Boss's order of 2026-10-26, 01:03 UTC, 6405916579, under the owner's delegation; H-Merger-At-Rest-1's REPORT.md sections 1 and 3, built in merger.py; the test under 15 s): a fitted hand's windings are its own quantum, read on zero gears of the train's shape and not as the great clock's increment where the hand stands (equal on an empty hand: the cycle great clock's 64 fittings at the tick 2 tally 1,682,128,072,219,779,093,684 per fitted hand, one value at 128 of 128 ends); under the one mirror (David's DAVID-THE-ONE-MIRROR.md) the cycle great clock fits nothing, its vernier drawing one train at every clock-node, so the pair is read on the bare 5-cube alone (the cycle's part below stands before the one mirror); a pair at rest (no lead across the mesh, the ends' sweeps opposite) engages as the reflected pair, the + fitted hand at the end whose sweep is positive, and each fitted hand's windings are paid at its own end by the unwound hand's four notches unwound whole by the one advance act at -1, the fall the wind the great clock loses, jammed by name `stop` where below the windings: on the cycle great clock (tests/worlds/world_ga2.json) at the tick 3 the 384 pairs fitted at the swing reach the premise and every one is jammed by the stop at 953 thousandths of the windings (one value; 0 negative windings; the hand's numbers to the integer), the great clock above the setting's X; on the bare 5-cube the heaviest hand's pair at one winding per end at two adjacent clocks is jammed by the stop at the first click (998 thousandths, the rotation's one step) and unsprings into light at the second (unwound at or above tallied, the unsprung hand advanced as the fitted hand's advance where the unsprung gear has no going, W -+(T div 2)); at three windings per end it unsprings at the first click; the rewind exact. The hand's landing (64 unspringings at 217 with unwound = tallied at 128 of 128 ends, X 999 at every clock at 218, 16 fittings at 219) is measured in the chart and not here (450 ticks)."""
    calibre, piece = world_of("world_ga2.json")
    clock = Clock(calibre, dict(piece, intervals=6))
    kept = copy.deepcopy(clock)
    for _ in range(6):
        clock.tick()
    births = [e for e in clock.log if e["event"] == "birth"]
    stops = [e for e in clock.log if e["event"] == "refused" and e["cause"] == "stop"]
    assert not births and not stops  # the one mirror: the cycle great clock fits nothing (64 and 384)
    assert run_back_exact(kept, 6) == 6
    bare = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b = bare.A, bare.B
    heavy = max(range(len(bare.hands())), key=lambda r: bare.hands()[r].spring or 0)
    unsprung = bare.hands().index(bare.unsprung())
    m, p = (1, 1, 1), (2, 1, 1)
    found = []
    for k in (1, 3):
        great_clock = node_of("world_node.json", shape=[5, 5, 5], seed=[])
        unwind.advance(great_clock, heavy, m, (k * a, 0, 0, k * b))
        unwind.advance(great_clock, heavy, p, (k * a, 0, 0, -k * b))
        held = copy.deepcopy(great_clock)
        for _ in range(4):
            great_clock.tick()
        mergers = [e for e in great_clock.log if e["event"] == "birth" and e["taken_row"] == heavy]
        jam_events = [e for e in great_clock.log if e["event"] == "refused" and e.get("row") == heavy]
        assert len(mergers) == 1 and mergers[0]["line_pair"] == unsprung
        (merger,) = mergers
        assert (tuple(merger["plus"]), tuple(merger["minus"])) == (m, p)
        assert all(t["taken"] >= t["booked"] > 0 for t in merger["takes"])
        # H-Children-Charge-Bug-1: the unsprung hand the exact unwind at -1 at both ends, the fitted hands' W 0 (the advance with a sweep and [None, None] before)
        assert [x[:2] for x in merger["exact_lay"]] == [[0, -191]] * 2 and merger["W_children"] == [0, 0]
        assert run_back_exact(held, 4) == 4
        found.append(
            (merger["i"], [(e["i"], e["cause"], e["fall"] * 1000 // e["walls"]) for e in jam_events])
        )
    assert found == [(2, [(1, "stop", 998)]), (1, [])]


def test_the_six_metric_lines_are_written_read_and_run_back_exactly_through_a_top_y_s3() -> None:
    """Y-S3, the regulation gears driven, read and rewound exactly through a top, the three flows since the shears, read by no act, are struck (the Scribe's R11, the owner's yes of 2026-10-28, 02:2x UTC; the six of the hand's letter below) (the hand H-Six-Metric-Lines-3, 2026-10-26; built in metric.py on the Boss's order of 03:3x UTC, 6407630119, under the owner's delegation): on the chiral setting of the 5-cube to 10 (the hole setting's under the wave's light, which fits nothing before its tick 53, before the wave) the six gears' drive stands in their drive fine teeth (the flow gears' source the light's own velocities in and out against its gradient, the shears' its two gradients' product; at this rim the carries below one notch to 60, every notch 0 and the fine teeth off their half at the clocks where light flows), the count per clock 98 and the bits within 128 as before, and the rewind is exact 10 of 10 through the turnovers; on the even sea of the 3-cube to 120 through the whole great clock's top at 58 and the exact return at 115 the six gears stay 0 at every clock (the flow 0 by symmetry) and the rewind is exact 10 of 10 through the top; a change of the flow gears two meshes from a clock leaves its step and its step back bit for bit (the one-mesh reach)."""
    clock = node_of("world_nature.json")
    assert run_back_exact(clock, 10) == 10
    for _ in range(10):
        clock.tick()
    gears = clock.train(REGULATOR).gears
    assert len(gears) == 1 + 2 * AXES and record.census(clock) == (95, 112)  # 107 with the shears
    flow = gears[1 + AXES : 1 + 2 * AXES]
    # TW-S1, the trace 6: every one of the six gears reaches notches within five by 10 on the chiral setting, at the clocks counted below under the great clock's bounds (80, 85, 74, 75, 69, 108 at the wave; within three on the hole's, 45, 42, 42, 20, 48, 20 clocks, before the wave; none reached at the trace 54, every gear at 0)
    reached = [sum(1 for x in gear.now.reshape(-1) if int(x)) for gear in flow]
    assert reached == [
        73,
        79,
        86,
    ]  # the shears struck (77, 80, 76 with them; 80, 78, 78 before the mirror)
    assert all(abs(int(x)) <= 5 for gear in flow for x in gear.now.reshape(-1))
    assert all(any(int(x) != gear.dteeth // 2 for x in gear.dfine.reshape(-1)) for gear in flow)
    assert clock.counts["turns"] > 0 and clock.counts["births"] > 0

    sea = node_of("world_sea_3.json")
    for _ in range(110):
        sea.tick()
    kept = [state_of(sea)]
    tops = []
    for _ in range(10):
        sea.tick()
        kept.append(state_of(sea))
        if sea.turned_over.any():
            tops.append((sea.ticks, int(sea.turned_over.sum())))
    six = sea.train(REGULATOR).gears[1 + AXES :]  # the three flows
    assert all(int(x) == 0 for gear in six for a in (gear.now, gear.before) for x in a.reshape(-1))
    assert sum(state_of(sea) == kept[9 - k] for k in range(10) if not sea.tick(-1)) == 10

    base = node_of("world_hole.json")
    for _ in range(6):
        base.tick()
    far = copy.deepcopy(base)
    centre = (2, 2, 2)
    for k in range(1 + AXES, 1 + 2 * AXES):
        gear = far.train(REGULATOR).gears[k]
        for at in np.ndindex(*far.size):
            if sum(min(abs(a - c), far.cube - abs(a - c)) for a, c in zip(at, centre, strict=True)) >= 2:
                gear.now[at] = int(gear.now[at]) + k

    def at_centre(n):
        return [
            (int(gear.now[centre]), int(gear.before[centre]), int(gear.fine[centre]))
            for train in n.trains()
            for gear in train
        ]

    base.tick()
    far.tick()
    assert at_centre(base) == at_centre(far)
    base.tick(-1)
    far.tick(-1)
    assert at_centre(base) == at_centre(far)


def test_the_merger_lays_light_of_no_charge_at_both_ends_cc1() -> None:
    """H-Children-Charge-Bug-1 (the Boss's 6410696786, 2026-10-26): an unspringing's unsprung hand at an end whose named gear has no going (now equal to before, the largest gap the empty gear's) was advanced as the advance of a fitted hand with a sweep, so the unspringing's two fitted hands carried the sweep -T div 2 + 0; the letter advances the unsprung hand as the exact unwind at -1 on the named gear at both ends, their own W 0. The chiral 60's unspringing of the tick 10 fed on the 3-cube: both ends exact, the fitted hands' own sweep summing to 0; three pins."""
    clock = node_of("world_node.json")
    clock.tick()
    s, minus, plus = 0, (1, 1, 1), (1, 1, 2)
    hand = clock.hands()[s]
    assert hand.ratio is not None
    unwind.advance(clock, s, minus, (939, 1175, 0, 0))
    unwind.advance(clock, s, plus, (1329, 1112, 0, 0))
    gearing = readings.gearing(clock, hand.ratio, clock.start_load, factors(clock))
    windings, exact = (
        dict(zip((-1, 1), fitted_windings_of(clock, s, minus, plus, gearing, {}), strict=True)),
        [],
    )
    fitted_advanced(clock, s, minus, plus, unsprung_notches(clock, s, windings, gearing, exact))
    assert all(x is not None for x in exact) and [x[1] != 0 for x in exact] == [True, True]
    assert (
        sum(
            0 if x is not None else sense * clock.A * clock.B
            for x, sense in zip(exact, (-1, 1), strict=True)
        )
        == 0
    )


def test_a_frozen_node_is_released_by_the_turn_of_its_time() -> None:
    """FR-S1 (the owner's words of 2026-10-26, 03:41 UTC, approved, and 07:3x UTC, "enter now": the fix of a forbidden state, no clock stopped for ever; The-Frozen-Node-Release_COMPARISON.md section 3): a clock that rose into the stopped load is turned over at its stopped tick by the turnover's own trigger on its restored gear, its now and before reversed, so at the next tick its load stands below the stopped load, no longer stopped, its rate running; no clock stopped at two ticks in a row; the rewind exact. The 3-cube centre fed to the stopped load 3,793 with its before at the load 3,700, 20 ticks."""
    clock, centre = node_of("world_node.json"), (1, 1, 1)
    stopped = rates.stopped_load(clock.full_rate)
    regulator = clock.train(REGULATOR).gears[0]
    regulator.now[centre], regulator.before[centre] = level_at(clock, stopped), level_at(clock, 3700)
    clock.driven_teeth()
    unsprung = clock.unsprung().gears[0]
    unsprung.now[centre] = 4 * int(unsprung.now[centre])
    dial, kept, was = int(clock.dial[centre]), copy.deepcopy(clock), False
    for _ in range(INTERVALS):
        now = bool(
            np.asarray(rates.mesh_rate_of(clock.full_rate, readings.load(clock)), dtype=object)[centre]
            == 0
        )
        assert not (was and now)
        was = now
        clock.tick()
        if clock.ticks == 1:
            assert now and clock.turned_over[centre] and int(clock.dial[centre]) == dial
            assert int(readings.load(clock)[centre]) < stopped
        if clock.ticks == 2:
            assert not now and int(clock.dial[centre]) > dial
    assert run_back_exact(kept, INTERVALS) == INTERVALS

"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand, forward and back; the interval on a closed cube of one body, every level Rule3's, the count conserved, the 48 symmetries kept with the giving, the inverse bit for bit; on the chain, the giving is the count's line's click at the shell, the report a reading of the line, and the light band reads the well; a moving record sources the vector part along its motion; the sense is the Wronskian, booked by the line."""

from __future__ import annotations

import json
import re
from collections import Counter
from itertools import permutations, product
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import flow, node
from event_universe.core.rule3 import coefficients, rule3
from event_universe.game_board import GameBoard
from event_universe.loader.derived import family_rules
from event_universe.world_files import input_digest, load_world
from tests.laws import ROOT, UNIVERSE, chain_body_world, load_file, universe_beside

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
WRAP, HERE = (True, True, True), (1, 1, 1)
HELD, GAPPED, QUANTA = family_rules(
    [("held", (4, 4), "content", 7), ("gapped", (3, 4), "content", 7), ("quanta", (5, 7), None, None)]
)
ROWS = [
    (
        row["name"],
        tuple(row["pair"]),
        row.get("held", {}).get("count"),
        row.get("held", {}).get("divisor"),
    )
    for row in json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
]
FAMILIES = family_rules(ROWS)  # the tests' universe: gravity, charge, polarisation, matter, third
NAMES = [family.name for family in FAMILIES]
GAMMA, T = 6000, 32768


def by_hand(a: np.ndarray, node: tuple[int, int, int]) -> tuple[int, ...]:
    """The six neighbours' levels of one Node on a periodic board, read by its address alone."""
    found = []
    for axis in range(3):
        for side in (1, -1):
            there = list(node)
            there[axis] = (there[axis] + side) % a.shape[axis]
            found.append(int(a[tuple(there)]))
    return tuple(found)


def test_one_nodes_acts_are_rule3_called_by_hand_forward_and_back():
    """(a) On random NodeStates of a periodic board of 3^3: the levels' step, the lay, the count's line, the well and the hold at one Node equal Rule3 called by hand on that Node's integers, and each act's direction -1 returns its start bit for bit; the hold's tensor part is one act from its origin, and a carry kept over its count's fall writes at once what the act back does not return."""
    draw, shape = np.random.default_rng(5), (3, 3, 3)
    for _ in range(20):
        levels = node.Record(
            *(draw.integers(-900, 900, shape) for _ in range(2)), draw.integers(0, 50, shape)
        )
        content = int(draw.integers(-40, 40))
        rule = node.quanta_rule(QUANTA, 100, content)
        after = node.step(levels, rule, WRAP)
        reads, self_coefficient, wall = coefficients(5, 7, 100, content)
        arrived = by_hand(levels.now, HERE)
        sums = (arrived[0] + arrived[1], arrived[2] + arrived[3], arrived[4] + arrived[5])
        expected = rule3(
            reads,
            sums,
            self_coefficient,
            wall,
            int(levels.now[HERE]),
            int(levels.before[HERE]),
            int(levels.remainder[HERE]),
        )
        assert (int(after.now[HERE]), int(after.remainder[HERE])) == expected
        back = node.step(after, rule, WRAP, -1)
        assert all(
            np.array_equal(x, y)
            for x, y in zip(
                (back.now, back.before, back.remainder),
                (levels.now, levels.before, levels.remainder),
                strict=True,
            )
        )
        # the lay from the weighted share: [w (now^2 + before^2) - S now before] div (2 p^2) - num now S_6(before)
        count_wall, now_here, before_here = 3 * 7 * 64, int(after.now[HERE]), int(after.before[HERE])
        node_term = wall * (now_here**2 + before_here**2) - self_coefficient * now_here * before_here
        share = node_term // (2 * (100 - 2 * content) ** 2) - 5 * now_here * sum(
            by_hand(after.before, HERE)
        )
        count, remainder = node.lay(QUANTA, (after,), 64, WRAP, 100, content)
        assert (int(count[HERE]), int(remainder[HERE])) == divmod(share + count_wall // 2, count_wall)
        # the count's line: the six currents num (now_i before_j - before_i now_j), W_c c + r moved by their sum
        state = node.NodeState(after, count, remainder, None, [], None)
        written = node.count_line(QUANTA, state, 64, 1 << 20, WRAP)
        here, now_j, before_j = after, by_hand(after.now, HERE), by_hand(after.before, HERE)
        flux = sum(
            5 * (int(here.now[HERE]) * b - int(here.before[HERE]) * n)
            for n, b in zip(now_j, before_j, strict=True)
        )
        assert (int(written.count[HERE]), int(written.remainder[HERE])) == divmod(
            count_wall * int(count[HERE]) + int(remainder[HERE]) + flux, count_wall
        )
        moved = node.NodeState(after, written.count, written.remainder, None, [], None)
        returned = node.count_line(QUANTA, moved, 64, 1 << 20, WRAP, -1)
        assert np.array_equal(returned.count, count) and np.array_equal(returned.remainder, remainder)
        # the well: (now^2 - next x before + r) div T, and back
        carry = draw.integers(0, 64, shape)
        quanta, carried = node.well(node.form(levels, after), carry, 64)
        form = int(levels.now[HERE]) ** 2 - int(after.now[HERE]) * int(levels.before[HERE])
        assert (int(quanta[HERE]), int(carried[HERE])) == divmod(form + int(carry[HERE]), 64)
        back = node.well(node.form(levels, after), carried, 64, -1)
        assert all(np.array_equal(x, y) for x, y in zip(back, (quanta, carry), strict=True))
        # the hold: a row without a gap steps its parts by the plain rule (R = num, S = 0, w = 3 den), then (source + r) div E_s at the time part
        part = node.Record(
            *(draw.integers(-900, 900, shape) for _ in range(2)), draw.integers(0, 12, shape)
        )
        held = node.NodeState(None, None, None, None, [part], draw.integers(0, 7, shape))
        source = draw.integers(0, 400, shape)
        parts, carry_after_hold, _flows = node.held_step(HELD, held, source, WRAP)
        stepped = node.NodeState(None, None, None, None, parts, carry_after_hold)
        plain = rule3(
            (4, 4, 4),
            tuple(
                a + b
                for a, b in zip(by_hand(part.now, HERE)[::2], by_hand(part.now, HERE)[1::2], strict=True)
            ),
            0,
            12,
            int(part.now[HERE]),
            int(part.before[HERE]),
            int(part.remainder[HERE]),
        )
        increment, carry_after = divmod(int(source[HERE]) + int(held.carry[HERE]), 7)
        assert (int(stepped.parts[0].now[HERE]), int(stepped.carry[HERE])) == (
            plain[0] + increment,
            carry_after,
        )
        undone, carry_back, _flows = node.held_step(HELD, stepped, source, WRAP, -1)
        assert np.array_equal(undone[0].now, part.now) and np.array_equal(undone[0].before, part.before)
        assert np.array_equal(undone[0].remainder, part.remainder) and np.array_equal(
            carry_back, held.carry
        )
        # a row with a gap is laid, not stepped: (source + r) div E_s, the level before kept beside it, back exact
        laid, laid_carry, _flows = node.held_step(GAPPED, held, source, WRAP)
        assert (int(laid[0].now[HERE]), int(laid_carry[HERE])) == (increment, carry_after)
        assert np.array_equal(laid[0].before, part.now) and np.array_equal(
            laid[0].remainder, part.remainder
        )
        stood = node.NodeState(None, None, None, None, laid, laid_carry)
        back, back_carry, _flows = node.held_step(GAPPED, stood, source, WRAP, -1)
        assert np.array_equal(back[0].now, part.now) and np.array_equal(back_carry, held.carry)
    # the tensor's one act (w x j_a j_b + r) div (E_s W_c^2 c_i), from its origin, a count 0 skipping it, back exact
    ones, count = np.ones((3, 1, 1), dtype=np.int64), np.array([0, 2, 1]).reshape(3, 1, 1)
    current = flow.Flow(3, (np.array([5, -3, 4]).reshape(3, 1, 1), ones, 0 * ones), count, 2)
    levels, carries = [0 * ones for _ in range(10)], flow.flow_origins(HELD, 2, count)
    written, found = flow.flow_hold(HELD, levels, current, carries, 1)
    assert written[4].ravel().tolist() == [0, 0, 2] and found[3].ravel().tolist() == [0, 55, 6]
    back, returned = flow.flow_hold(HELD, written, current, found, -1)
    assert all(np.array_equal(a, b) for a, b in zip(back + returned, levels + carries, strict=True))
    # the count at the Node falls to 1 with its carry 55 kept: 55 div 28 written at once, not returned back
    fallen = flow.Flow(3, (0 * ones, 0 * ones, 0 * ones), np.array([0, 1, 1]).reshape(3, 1, 1), 2)
    dumped, kept = flow.flow_hold(HELD, written, fallen, found, 1)
    back, returned = flow.flow_hold(HELD, dumped, fallen, kept, -1)
    assert dumped[4].ravel().tolist() == [0, 1, 2]
    assert back[4][1, 0, 0] == 1 and returned[3][1, 0, 0] == 27  # not 0 and 55: the dump stays


def cube_world(folder: Path, count: int) -> Path:
    """The closed cube of 9^3 in the tests' universe without its row with a gap (laid, its inverse is (a)'s) and with the charge's band [5600, 6000] (its edge admits the vacuum's row ringing below zero beside the walls, where the light band's guard ends the run by name), with one body of matter on its centre Node declaring `count`, its mode a profile symmetric under the cube's 48 (no standing record: it breathes and gives)."""
    universe_beside(folder, drop=("polarisation",), charge=[5600, 6000])
    body = {"family": "matter", "nodes": [{"node": [4, 4, 4], "count": count}]}
    world = dict(shape=[9, 9, 9], boundary=dict(x="closed", y="closed", z="closed"), ticks=8)
    world.update(universe="u.json", engine="e.json", measured=[body], detectors=[])
    distance = np.abs(np.indices((9, 9, 9)) - 4).sum(axis=0)
    profile = np.where(
        distance == 0, 1200, np.where(distance == 1, 600, np.where(distance == 2, 200, 0))
    )
    levels = profile.ravel().tolist()
    mode = {"family": "matter", "pair": [4000, 6000], "moving": {"now": levels, "before": levels}}
    (path := folder / "cube.json").write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": [mode]}), encoding="utf-8"
    )
    return path


def turned(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    """An array under one of the cube's 48: its axes permuted and reflected."""
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def everything(board: GameBoard) -> list[np.ndarray]:
    """Every array of the NodeStates: the levels, the remainders, the counts, the senses and the carries."""
    found = []
    for state in board.states:
        for record in [r for r in (state.levels, state.second) if r is not None] + state.parts:
            found += [record.now, record.before, record.remainder]
        found += [
            a
            for a in (state.count, state.count_remainder, state.sense, state.sense_remainder)
            if a is not None
        ]
        found += [
            a for a in (state.well_remainder, state.wronskian_remainder, state.carry) if a is not None
        ]
        found += [a for carries in state.flows.values() for a in carries]
    return [np.asarray(a).copy() for a in found]


def keeps_the_48(board: GameBoard) -> None:
    """Every scalar array keeps the cube's 48 about the body to the bit, and a held family's tensor diagonal transforms as the diagonal of a tensor (the vector and off-diagonal parts, floors of odd fields, carry the rounding and are read as a vector by the moving record's test)."""
    for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
        for state in board.states:
            scalars = [r for r in (state.levels, state.second) if r is not None] + state.parts[:1]
            arrays = [a for r in scalars for a in (r.now, r.before, r.remainder)]
            arrays += [a for a in (state.count, state.count_remainder, state.carry) if a is not None]
            assert all(np.array_equal(turned(a, axes, signs), a) for a in arrays)
            for a in range(3) if len(state.parts) > 4 else ():
                moved = turned(state.parts[4 + axes[a]].now, axes, signs)
                assert np.array_equal(moved, state.parts[4 + a].now)


def read_of(held: node.NodeState) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """A reader's content and axis contents from the vacuum's row alone, by hand: its time part and (its tensor's aa part + 1) div 2."""
    return held.parts[0].now.copy(), tuple((held.parts[4 + a].now + 1) // 2 for a in range(3))


def test_the_interval_on_a_closed_cube_is_rule3_conserves_the_count_keeps_the_48_and_returns(
    tmp_path, monkeypatch
):
    """(b) A body on a closed cube of 9^3: the gate refuses a declared count off the weighted lay by name and admits the laid one; each interval the matter's levels are Rule3 from the interval's start at every Node with the vacuum's row read once, SUM (W_c c + r) moves by the givings alone, to the bit, and every array keeps the cube's 48 about the body with the givings at the Ports the line crossed; over two intervals with no giving and no count falling below a tensor carry's divisor the inverse returns every array bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(ValueError, match="declares the count 1 and its family's form lays") as refused:
        GameBoard(load_world(cube_world(tmp_path, 1))).step()
    laid = int(re.search(r"lays (\d+) quanta", str(refused.value)).group(1))
    board = GameBoard(load_world(cube_world(tmp_path, laid)))
    names = [family.name for family in board.families]
    index = names.index("matter")
    matter, gravity = board.states[index], board.states[names.index("gravity")]
    wall, total = node.count_wall(board.families[index], T), None
    for _ in range(7):
        start = node.Record(
            *(a.copy() for a in (matter.levels.now, matter.levels.before, matter.levels.remainder))
        )
        padded = np.pad(start.now, 1)
        sums = tuple(
            (np.roll(padded, 1, axis) + np.roll(padded, -1, axis))[1:-1, 1:-1, 1:-1] for axis in range(3)
        )
        reads, self_coefficient, rule_wall = coefficients(4000, 6000, GAMMA, *read_of(gravity))
        expected = rule3(
            reads, sums, self_coefficient, rule_wall, start.now, start.before, start.remainder
        )
        given = board.given[index]
        board.step()
        assert np.array_equal(matter.levels.now, expected[0]) and np.array_equal(
            matter.levels.remainder, expected[1]
        )
        found = int((wall * matter.count.astype(object) + matter.count_remainder).sum())
        assert total is None or found == total - wall * (board.given[index] - given)
        total = found
        keeps_the_48(board)
        # intervals 2 and 3 give nothing and no count falls below a tensor carry's divisor
        if board.tick == 1:
            kept, given = everything(board), board.given[index]
            for act in (board.step, board.step, board.step_inverse, board.step_inverse):
                act()
            assert board.given[index] == given and board.tick == 1
            assert all(np.array_equal(a, b) for a, b in zip(everything(board), kept, strict=True))
    assert board.given[index] > 0  # the body gave, at every one of the 48's images of a Port at once


def test_the_giving_is_the_lines_click_at_the_shell_and_the_report_a_reading_on_the_chain(
    tmp_path, monkeypatch
):
    """(c) On the chain, body 0 and the taker body 1 holding 64 quanta of the charge (laid over its Nodes in proportion to its counts, none lost) read by the detector `taker`, 400 intervals with the light band [6000, 6000] reading both held rows, no refusal: body 0 gives exactly at its outer Ports whose outward current carried whole W_c out of the Node's remainder, one `giving` line per quantum naming the Node and the Port's axis and side; the charge's SUM (W_c c + r) moves by the givings alone, to the bit, and its second level pair stays 0 (light is neutral); the `gather` lines at the taker are the net inflow of the charge's count; the books balance; the clock clicks as a reading."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(24, 40), holds={"charge": 64}, taker=True)
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(world), lines.append)
    matter, charge = board.states[NAMES.index("matter")], board.states[NAMES.index("charge")]
    family, wall = FAMILIES[NAMES.index("matter")], node.count_wall(FAMILIES[NAMES.index("charge")], T)
    board.step()
    reported = [line for line in lines if line["event"] == "gather" and line["detector"] == "taker"]
    assert board.contents()[1]["charge"] - 64 == sum(
        1 for line in reported if line["family"] == "charge"
    )
    for _ in range(399):
        nodes, remainder = board.bodies[0].nodes.copy(), matter.count_remainder.copy()
        total = int((wall * charge.count.astype(object) + charge.count_remainder).sum())
        before, done = charge.count.copy(), len(lines)
        board.step()
        now = lines[done:]
        state = node.NodeState(matter.levels, matter.count, remainder, None, [], None, matter.second)
        through = node.count_line(family, state, T, board.world.amplitude_bound, board.wrap).through
        expected: Counter = Counter()
        for port, (axis, side) in enumerate(product(range(3), (1, -1))):
            outer = (
                nodes & ~np.roll(nodes, -side, axis)
                if board.wrap[axis]
                else nodes
                & ~np.pad(nodes, 1)[
                    tuple(
                        slice(1 + side, nodes.shape[a] + 1 + side) if a == axis else slice(1, -1)
                        for a in range(3)
                    )
                ]
            )
            crossed = (remainder + through[port]) // wall
            for at in np.argwhere(outer & (crossed < 0)):
                expected[(tuple(int(i) for i in at), (axis, side))] += int(-crossed[tuple(at)])
        givings = [line for line in now if line["event"] == "giving" and line["measured"] == 0]
        assert Counter((tuple(line["node"]), tuple(line["axis"])) for line in givings) == expected
        given = sum(1 for line in now if line["event"] == "giving")
        assert (
            int((wall * charge.count.astype(object) + charge.count_remainder).sum())
            == total + wall * given
        )
        taken = [
            line["count"]
            for line in now
            if line["event"] == "gather" and line["detector"] == "taker" and line["family"] == "charge"
        ]
        if taken:
            arrived = taken[0] - int(before[board.bodies[1].nodes].sum())
            assert set(taken) == {taken[0]} and len(taken) == arrived
    assert not charge.second.now.any() and not charge.sense.any()
    assert all(book["balanced"] and book["sense_balanced"] for book in board.books().values())
    assert board.books()["matter"]["given"] > 0 and any(line["event"] == "click" for line in lines)


def chain_record(
    envelope: list[int], now_turn: tuple[int, ...], before_turn: tuple[int, ...]
) -> node.Record:
    """A record on a chain: the envelope times a character, (1, 0, -1, 0) at the step's level and its turn at the level before."""
    size, turns = len(envelope), len(now_turn)
    now = [envelope[x] * now_turn[x % turns] for x in range(size)]
    before = [envelope[x] * before_turn[x % turns] for x in range(size)]
    return node.Record(
        *(np.array(level, dtype=np.int64).reshape(size, 1, 1) for level in (now, before)), 0
    )


def test_a_moving_record_sources_the_vector_part_along_its_motion_and_the_link_pace_falls():
    """(d) On a chain, a record of matter moving along +x (the envelope times the plane wave's character, a quarter turn per Link and per interval) carries its count's line's travel along +x, sources the vacuum's row's vector part x above 0 and none along y and z, and its tensor's xx part above 0, so the Link's pace along x falls by the axis content below the pace along y; the same envelope at rest carries no current and sources neither part; every family reads the vacuum's row as its stepped time part and the bound charge as the well it laid, light as matter."""
    shape, wrap = (16, 1, 1), (False, True, True)
    envelope = [0, 0, 0, 200, 400, 600, 800, 1000, 1000, 800, 600, 400, 200, 0, 0, 0]
    matter, gravity = FAMILIES[NAMES.index("matter")], FAMILIES[NAMES.index("gravity")]
    for moving in (True, False):
        turns = ((1, 0, -1, 0), (0, -1, 0, 1)) if moving else ((1,), (1,))
        record, zero = chain_record(envelope, *turns), node.empty_record(shape)
        state = node.NodeState(record, None, None, None, [], None, zero)
        state.count, state.count_remainder = node.lay(matter, (record, zero), T, wrap, GAMMA)
        written = node.count_line(matter, state, T, 1 << 20, wrap)
        held = node.empty_state(gravity, shape)
        wall = node.count_wall(matter, T)
        held.flows = {NAMES.index("matter"): flow.flow_origins(gravity, wall, state.count)}
        travel = tuple(np.asarray(value) for value in written.travel)
        current = flow.Flow(1, (travel[0], travel[1], travel[2]), state.count, wall)
        held.parts, held.carry, held.flows = node.held_step(
            gravity, held, node.zeros(shape), wrap, 1, {NAMES.index("matter"): current}
        )
        vector, xx = [part.now for part in held.parts[1:4]], held.parts[4].now
        assert (bool((travel[0] > 0).any()) and int(travel[0].min()) >= 0) == moving
        assert (bool((vector[0] > 0).any()) and bool((xx > 0).any())) == moving
        assert (
            not vector[1].any() and not vector[2].any() and (moving or not (vector[0].any() or xx.any()))
        )
        states = [node.empty_state(family, shape) for family in FAMILIES]
        states[NAMES.index("gravity")] = held
        stepped = np.arange(16, dtype=np.int64).reshape(shape)  # the vacuum's row's stepped time part
        held.parts[0] = node.Record(stepped, stepped, node.zeros(shape))
        content, axis = node.signed_read(NAMES.index("matter"), FAMILIES, states, GAMMA, "now", 1, shape)
        assert (
            np.array_equal(axis[0], (xx + 1) // 2)
            and not axis[1].any()
            and np.array_equal(content, stepped)
        )
        laid_well = node.Record(
            state.count, state.count, node.zeros(shape)
        )  # the bound charge's laid level
        states[NAMES.index("polarisation")].parts[0] = laid_well
        light, _axis = node.signed_read(NAMES.index("charge"), FAMILIES, states, GAMMA, "now", 1, shape)
        assert np.array_equal(light, stepped + state.count)  # every reader reads both rows as they stand


def test_the_sense_is_the_wronskian_booked_by_the_line_and_a_real_record_is_neutral():
    """(e) On a periodic cube of 6^3 at a fixed pace, a record rotating as e^(-i omega t) on the lowest wave number (two level pairs a quarter turn apart) has a Wronskian above 0 at every Node, its sense laid above 0 and read as q = +1; Rule3 steps both pairs with one rule and the sense's line moves the sense so SUM (W_c k + r) stays to the bit over 100 intervals; the opposite rotation has the opposite sense; a real record's Wronskian is 0 at every Node and its sense 0."""
    shape, wrap = (6, 6, 6), (True, True, True)
    matter = FAMILIES[NAMES.index("matter")]
    rule, wall = node.quanta_rule(matter, GAMMA, 700), node.count_wall(matter, T)
    x = np.indices(shape)[0]
    cosine = np.take([4000, 2000, -2000, -4000, -2000, 2000], x)  # 4000 cos(2 pi x / 6)
    turned = np.take(
        [2800, 1400, -1400, -2800, -1400, 1400], x
    )  # its level an interval before, cos omega = 0.7
    quarter = np.take([2857, 1428, -1428, -2857, -1428, 1428], x)  # the second pair's, sin omega
    for sense in (1, -1):
        record = node.Record(cosine, turned, node.zeros(shape))
        second = node.Record(node.zeros(shape), sense * quarter, node.zeros(shape))
        state = node.NodeState(record, None, None, None, [], None, second)
        assert (np.sign(node.wronskian(record, second)) == sense).all()
        state.sense, state.sense_remainder = node.lay_sense(matter, record, second, T, GAMMA, 700)
        assert (node.sense_sign(state, shape) == sense).all()
        total = int((wall * state.sense.astype(object) + state.sense_remainder).sum())
        for _ in range(100):
            state.levels, state.second = (
                node.step(state.levels, rule, wrap),
                node.step(state.second, rule, wrap),
            )
            written = node.sense_line(matter, state, T, 1 << 20, wrap)
            state.sense, state.sense_remainder = np.asarray(written.count), np.asarray(written.remainder)
            assert int((wall * state.sense.astype(object) + state.sense_remainder).sum()) == total
    real = node.Record(cosine, turned, node.zeros(shape))
    assert not node.wronskian(real, node.empty_record(shape)).any()
    assert not node.lay_sense(matter, real, node.empty_record(shape), T, GAMMA)[0].any()

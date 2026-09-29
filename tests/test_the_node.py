"""THE NODE (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand, forward and back; the interval on a closed cube of one laid body, every level Rule3's, the count conserved, the 48 symmetries kept, the inverse bit for bit; the giving on the chain of Gamma 6000, a conversion of the count at the body's click, the report a reading of the count's line."""

from __future__ import annotations

import json
import re
from collections import Counter
from itertools import permutations, product
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import node
from event_universe.core.rule3 import coefficients, rule3
from event_universe.game_board import GameBoard
from event_universe.loader.derived import family_rules
from event_universe.world_files import input_digest, load_world
from tests.laws import ROOT, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
WRAP, HERE = (True, True, True), (1, 1, 1)
HELD, QUANTA = family_rules([("held", (3, 4), "content", 7), ("quanta", (5, 7), None, None)])


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
    """(a) On random NodeStates of a periodic board of 3^3: the levels' step, the lay, the count's line, the well and the hold at one Node equal Rule3 called by hand on that Node's integers, and each act's direction -1 returns its start bit for bit."""
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
        # the lay: W_c c + r = 3 den (now^2 + before^2) - num now S_6(before) + W_c div 2, W_c = 3 den T
        count_wall = 3 * 7 * 64
        share = 3 * 7 * (int(after.now[HERE]) ** 2 + int(after.before[HERE]) ** 2) - 5 * int(
            after.now[HERE]
        ) * sum(by_hand(after.before, HERE))
        count, remainder = node.lay(QUANTA, after, 64, WRAP)
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
        quanta, carried = node.well(levels, after, carry, 64)
        form = int(levels.now[HERE]) ** 2 - int(after.now[HERE]) * int(levels.before[HERE])
        assert (int(quanta[HERE]), int(carried[HERE])) == divmod(form + int(carry[HERE]), 64)
        assert all(
            np.array_equal(x, y)
            for x, y in zip(node.well(levels, after, carried, 64, -1), (quanta, carry), strict=True)
        )
        # the hold: the parts by the plain rule (R = num, S = 0, w = 3 den), then (source + r) div E_s at the time part
        part = node.Record(
            *(draw.integers(-900, 900, shape) for _ in range(2)), draw.integers(0, 12, shape)
        )
        held = node.NodeState(None, None, None, None, [part], draw.integers(0, 7, shape))
        source = draw.integers(0, 400, shape)
        parts, carry_after_hold = node.held_step(HELD, held, source, WRAP)
        stepped = node.NodeState(None, None, None, None, parts, carry_after_hold)
        plain = rule3(
            (3, 3, 3),
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
        undone, carry_back = node.held_step(HELD, stepped, source, WRAP, -1)
        assert np.array_equal(undone[0].now, part.now) and np.array_equal(undone[0].before, part.before)
        assert np.array_equal(undone[0].remainder, part.remainder) and np.array_equal(
            carry_back, held.carry
        )


def cube_world(folder: Path, count: int) -> Path:
    """The closed cube of 9^3 (the universe of Gamma 6000 without its holder of the sign, so no body gives) with one body of matter on its centre Node declaring `count`, its mode a profile symmetric under the cube's 48."""
    universe = json.loads(
        (ROOT / "examples" / "events" / "planck_6000.json").read_text(encoding="utf-8")
    )
    universe["families"] = [f for f in universe["families"] if f["name"] != "charge"]
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (folder / "e.json").write_bytes((ROOT / "examples" / "events" / "engine_start.json").read_bytes())
    body = {"family": "matter", "nodes": [{"node": [4, 4, 4], "count": count}]}
    world = dict(shape=[9, 9, 9], boundary=dict(x="closed", y="closed", z="closed"), ticks=8)
    world.update(universe="u.json", engine="e.json", measured=[body], detectors=[])
    index = np.indices((9, 9, 9)) - 4
    distance = np.abs(index).sum(axis=0)
    profile = np.where(
        distance == 0, 1200, np.where(distance == 1, 600, np.where(distance == 2, 200, 0))
    )
    mode = {"family": "matter", "pair": [4000, 6000], "profile": profile.ravel().tolist()}
    (path := folder / "cube.json").write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": [mode]}), encoding="utf-8"
    )
    return path


def arrays(board: GameBoard) -> list[np.ndarray]:
    """Every array of the NodeStates: the levels, the remainders, the counts and the carries."""
    found = []
    for state in board.states:
        for record in ([state.levels] if state.levels is not None else []) + state.parts:
            found += [record.now, record.before, record.remainder]
        found += [
            a
            for a in (state.count, state.count_remainder, state.well_remainder, state.carry)
            if a is not None
        ]
    return [a.copy() for a in found]


def test_the_interval_on_a_closed_cube_is_rule3_conserves_the_count_keeps_the_48_and_returns(
    tmp_path, monkeypatch
):
    """(b) A laid body on a closed cube of 9^3: the gate refuses a declared count off the lay by name and admits the laid one; each interval every family's levels are Rule3 from the interval's start at every Node, SUM (W_c c + r) is conserved to the bit, every array keeps the cube's 48 symmetries about the body, and after the lay the inverse returns every level, remainder, count and carry bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(ValueError, match="declares the count 1 and its family's form lays") as refused:
        GameBoard(load_world(cube_world(tmp_path, 1))).step()
    laid = int(re.search(r"lays (\d+) quanta", str(refused.value)).group(1))
    board = GameBoard(load_world(cube_world(tmp_path, laid)))
    matter, family = board.states[2], board.families[2]
    wall, total = node.count_wall(family, 32768), None
    for _ in range(6):
        start = node.Record(
            matter.levels.now.copy(), matter.levels.before.copy(), matter.levels.remainder.copy()
        )
        content = board.states[0].parts[0].now + board.states[1].parts[0].now
        padded = np.pad(start.now, 1)
        sums = tuple(np.roll(padded, 1, axis) + np.roll(padded, -1, axis) for axis in range(3))
        reads, self_coefficient, rule_wall = coefficients(4000, 6000, 6000, content)
        expected = rule3(
            reads,
            tuple(s[1:-1, 1:-1, 1:-1] for s in sums),
            self_coefficient,
            rule_wall,
            start.now,
            start.before,
            start.remainder,
        )
        board.step()
        assert np.array_equal(matter.levels.now, expected[0]) and np.array_equal(
            matter.levels.remainder, expected[1]
        )
        found = int((wall * matter.count.astype(object) + matter.count_remainder).sum())
        assert total is None or found == total
        total = found
        for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
            for a in arrays(board):
                turned = np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]
                assert np.array_equal(turned, a)
    kept = arrays(board)
    for _ in range(3):
        board.step()
    for _ in range(3):
        board.step_inverse()
    assert (
        all(np.array_equal(a, b) for a, b in zip(arrays(board), kept, strict=True)) and board.tick == 6
    )


def test_the_giving_is_a_conversion_at_the_click_and_the_report_a_reading_on_the_chain(
    tmp_path, monkeypatch
):
    """(c) On the chain of Gamma 6000 with the taker body 1 read by the detector `taker`, 400 intervals: body 0 clicks every 8 intervals as the old engine's clock read; at each of its clicks where its shell holds a count, the shell Node where its count stands highest gives: that count falls by one, the charge's count there rises by one, and the form the write adds lays exactly one count; the charge's SUM (W_c c + r) moves only by the givings, to the bit; the `gather` lines at the taker are the net inflow of the charge's count across its Nodes' boundary (one line per unit, the taker's count after); the books balance (the charge's band [5600, 6000], whose edge admits the held rows' ringing below zero, see test_the_click)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, taker_at=200, charge=[5600, 6000])))
    charge, matter = board.states[2], board.states[3]
    wall, seen, lines = node.count_wall(board.families[2], 32768), {}, []

    def observe(line: dict[str, object]) -> None:
        if line["event"] == "click":
            seen["counts"] = (matter.count.copy(), charge.count.copy())
            seen["levels"] = (charge.levels.now.copy(), charge.levels.before.copy())
        if line["event"] == "giving" and line["measured"] == 0:
            at, shell = tuple(line["node"]), board.shell(board.bodies[0])
            assert seen["counts"][0][at] == seen["counts"][0][shell].max() >= 1
            assert (matter.count[at], charge.count[at]) == (
                seen["counts"][0][at] - 1,
                seen["counts"][1][at] + 1,
            )
            written = node.Record(
                charge.levels.now - seen["levels"][0], charge.levels.before - seen["levels"][1], 0
            )
            assert int(node.lay(board.families[2], written, 32768, board.wrap)[0].sum()) == 1
        lines.append(line)

    board.observer = observe
    for _ in range(400):
        before = None if charge.count is None else charge.count.copy()
        total = (
            None
            if before is None
            else int((wall * charge.count.astype(object) + charge.count_remainder).sum())
        )
        board.step()
        now = [line for line in lines if line["tick"] == board.tick]
        given = sum(1 for line in now if line["event"] == "giving")
        if total is not None:
            assert (
                int((wall * charge.count.astype(object) + charge.count_remainder).sum())
                == total + wall * given
            )
            reports = [line for line in now if line["event"] == "gather" and line["family"] == "charge"]
            taken = [line["count"] for line in reports if line["detector"] == "taker"]
            if taken:
                arrived = taken[0] - int(before[board.bodies[1].nodes].sum())
                assert set(taken) == {taken[0]} and len(taken) == arrived
    clicks = [line["tick"] for line in lines if line["event"] == "click" and line["measured"] == 0]
    assert Counter(np.diff(clicks).tolist()).most_common(1)[0][0] == 8
    givings = [line for line in lines if line["event"] == "giving" and line["measured"] == 0]
    assert 0 < len(givings) <= len(clicks) and all(line["tick"] in clicks for line in givings)
    assert any(
        line["event"] == "gather" and line["family"] == "charge" and line["taker"] == 1 for line in lines
    )
    assert all(book["balanced"] for book in board.books().values())

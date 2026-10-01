"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand; the interval on a closed cube of one body, every level Rule3's, the count the record's share, the 48 symmetries kept in every part, the back-in-time gate MATCH over twelve intervals; on the chain light is born by the write: a breathing body of a plane writes a wave into the sign holder's own record, its share's total stays within the rounding, a static body's write stands still within the rounding, and the click at the end detector is the measurement; the whole run of the chain goes back in time, MATCH over 400 intervals with the rotating body and with the real one; the tension is Rule3's own conservation of the current; the Wronskian's sign is read from the record; a receding face grows the GameBoard before the front, the run the larger chain's bit for bit, ending at the largest size and returning."""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import node, share
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, link_paces, rule3
from event_universe.features.start import rest
from event_universe.game_board import GameBoard
from event_universe.loader.derived import HeldWrite, Row, count_wall, family_rules, held_write
from event_universe.loader.world import kind_of, universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws import (
    CHAIN,
    CHARGED,
    PACKET,
    ROOT,
    UNIVERSE,
    chain_body_world,
    load_file,
    universe_beside,
)

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")
RUN = load_file("run_inputs", ROOT / "tools" / "run_inputs.py")
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")
WRAP, HERE, KEYS = Wrap(True, True, True), (1, 1, 1), ("now", "before", "remainder")
KIND = kind_of(63)  # the tests' arrays, the hardware's integers
ROWS = [Row("held", (4, 4), 4, False, False, 7, 0), Row("gapped", (3, 4), 1, False, False, 7, 0)]
ROWS.append(Row("quanta", (5, 7), 1, False, False, None, 0))
HELD, GAPPED, QUANTA = family_rules(ROWS)
WRITE = held_write((HELD, GAPPED, QUANTA), 0, 64)  # the massless row's one write per part at T = 64
UNIVERSE_ROWS = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
FAMILIES = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))[1]  # the tests' universe
NAMES = [family.name for family in FAMILIES]
MATTER, GRAVITY, CHARGE = (NAMES.index(name) for name in ("matter", "gravity", "charge"))
GAMMA, T, PROFILE = 6000, 32768, [0, 0, 0, 200, 400, 600, 800, 1000, 1000, 800, 600, 400, 200, 0, 0, 0]
WALLS = [
    held_write(FAMILIES, i, T).walls if f.held else () for i, f in enumerate(FAMILIES)
]  # per family


def by_hand(a: np.ndarray, node: tuple[int, int, int]) -> tuple[int, ...]:
    """The six neighbours' levels of one Node on a periodic board, read by its address alone."""
    found = []
    for axis in range(3):
        for side in (1, -1):
            there = list(node)
            there[axis] = (there[axis] + side) % a.shape[axis]
            found.append(int(a[tuple(there)]))
    return tuple(found)


def quanta_of(board: GameBoard, index: int) -> int:
    """A family's share summed over the GameBoard in quanta over its wall, the books' reading."""
    return int(board.books()[board.families[index].name]["quanta"])


def within_the_reach(board: GameBoard, index: int) -> int:
    """One step of the GameBoard: a family's share read at the start's paces changes by the net currents at the start pair plus two terms exact in rationals from the step's three levels and remainders, the paces' anisotropy term num (next - before) SUM_a (3 p_a^2 - P^2) arr_a(now) / P^2 (P^2 = SUM_a p_a^2; 0 where the three paces are equal) and Rule3's remainder term -3 (next - before) (r' - r) / (2 P^2), up to the division act's floor at every Node of each level pair, under one unit each (ALGEBRA.md #the-count-is-the-records-share); returned, the paces' own part of the change, read beside (the books' drift holds both)."""
    family, state, gamma = board.families[index], board.states[index], board.world.node_clock
    content, axis = node.read(index, board.families, board.states, 1)
    paces = link_paces(gamma, content.astype(object), tuple(a.astype(object) for a in axis))
    squares = [pace * pace for pace in paces]
    total = squares[0] + squares[1] + squares[2]

    def at_the_paces(pairs: tuple[node.Record, ...]) -> int:
        return int(share.family_share(family, pairs, board.wrap, gamma, content, axis).sum(dtype=object))

    def exact_terms(begun: node.Record, stepped: node.Record) -> Fraction:
        moved = stepped.now.astype(object) - begun.before.astype(object)  # next - before
        arrivals = [a.astype(object) for a in node.axis_sums(begun.now, board.wrap)]
        carried = stepped.remainder.astype(object) - begun.remainder.astype(object)  # r' - r
        skew = sum((3 * squares[a] - total) * arrivals[a] for a in range(3))
        top, low = 2 * family.pair[0] * moved * skew - 3 * moved * carried, 2 * total
        return sum(Fraction(int(n), int(d)) for n, d in zip(top.ravel(), low.ravel(), strict=True))

    records = tuple(state.lines)
    start = at_the_paces(records)
    net = int(sum(np.asarray(current, dtype=object).sum() for current in board.currents()[index]))
    board.step()
    after = tuple(state.lines)
    fixed = at_the_paces(after)
    terms = sum(exact_terms(begun, stepped) for begun, stepped in zip(records, after, strict=True))
    floors = len(records) * records[0].now.size  # the division act's floor, under one unit per Node
    assert abs(Fraction(fixed - start - net) - terms) < floors, (fixed - start - net, terms, floors)
    return board.total_share(index) - fixed


def drawn(draw: np.random.Generator, shape: tuple[int, int, int], size: int, top: int) -> node.Record:
    """A random level pair within `size` with a remainder below `top`."""
    levels = [draw.integers(-size, size, shape) for _ in range(2)]
    return node.Record(*levels, draw.integers(0, top, shape))


def test_one_nodes_acts_are_rule3_called_by_hand():
    """(a) On random NodeStates of a periodic board of 3^3: the levels' step, the share and its reading in quanta, the currents, the well (a reading) and the one write per held part at one Node equal Rule3 called by hand on that Node's integers (each act's direction -1 is the feature tests' and the back-in-time gate's); a held row with a gap steps by the same call at its own pair, the plain rule's reads num, self coefficient 0 and wall 3 den, and its write is the same act as the row without one, back exact (the generic test of the two rows: no name and no branch); the write's walls are the rows' own, E_s T and E_s x 3 den T with the sources' den (their least common multiple where they differ, each tension times the multiple over its own den), the remainders' origin half the wall."""
    draw, shape = np.random.default_rng(5), (3, 3, 3)
    for _ in range(20):
        levels, content = drawn(draw, shape, 900, 50), int(draw.integers(-40, 40))
        after = node.step(levels, node.quanta_rule(QUANTA, 100, content), WRAP)
        reads, self_coefficient, wall = coefficients(5, 7, 100, content)
        arrived = by_hand(levels.now, HERE)
        sums = (arrived[0] + arrived[1], arrived[2] + arrived[3], arrived[4] + arrived[5])
        here = tuple(int(getattr(levels, k)[HERE]) for k in KEYS)
        expected = rule3(reads, sums, self_coefficient, wall, *here)
        assert (int(after.now[HERE]), int(after.remainder[HERE])) == expected
        # the share, the count as a reading: [w (now^2 + before^2) - S now before] div (2 p^2) - num now S_6(before),
        # in quanta (share + W_c div 2) div W_c
        wall_c, now_here, before_here = 3 * 7 * 64, int(after.now[HERE]), int(after.before[HERE])
        node_term = wall * (now_here**2 + before_here**2) - self_coefficient * now_here * before_here
        near = sum(by_hand(after.before, HERE))
        share_here = node_term // (2 * (100 - 2 * content) ** 2) - 5 * now_here * near
        read = share.family_share(QUANTA, (after,), WRAP, 100, content)
        assert int(read[HERE]) == share_here
        assert int(share.quanta_of(read, wall_c, KIND)[HERE]) == (share_here + wall_c // 2) // wall_c
        # the currents, a detector's reading: F_ij = num (now_i before_j - before_i now_j) through each Port
        through = node.currents_of(QUANTA.pair[0], [after], WRAP)
        now_j, before_j = by_hand(after.now, HERE), by_hand(after.before, HERE)
        flux = [5 * (now_here * b - before_here * n) for n, b in zip(now_j, before_j, strict=True)]
        assert [int(f[HERE]) for f in through] == flux
        # the well, a reading: (now^2 - next x before) div T, no remainder kept
        form = here[0] ** 2 - int(after.now[HERE]) * here[1]
        assert int(node.well(node.form([levels], [after]), 64)[HERE]) == form // 64
        # the hold: one write per part, (numerator + r) div wall with the one remainder, the parts stepped before it
        part, numerators = drawn(draw, shape, 900, 12), [draw.integers(-400, 400, shape)] * 4
        remainders = [draw.integers(0, wall, shape) for wall in WRITE.walls]
        held = [part] + [node.empty_record(shape, KIND)] * 3
        parts, after_write = node.held_write(held, numerators, WRITE.walls, remainders)
        for i, wall in enumerate(WRITE.walls):
            increment, kept = divmod(int(numerators[i][HERE]) + int(remainders[i][HERE]), wall)
            level = int(held[i].now[HERE]) + increment
            assert (int(parts[i].now[HERE]), int(after_write[i][HERE])) == (level, kept)
        # a row with a gap steps by the plain rule at its own pair, (3, 3, 3), 0, 12 at [3, 4], and its write
        # is the same act at its time part, back exact
        stepped = node.step(part, node.part_rule(GAPPED), WRAP)
        arrived = by_hand(part.now, HERE)
        sums = (arrived[0] + arrived[1], arrived[2] + arrived[3], arrived[4] + arrived[5])
        here = tuple(int(getattr(part, k)[HERE]) for k in KEYS)
        by_rule = rule3((3, 3, 3), sums, 0, 12, *here)
        assert (int(stepped.now[HERE]), int(stepped.remainder[HERE])) == by_rule
        written, kept = node.held_write([part], numerators[:1], WRITE.walls[:1], remainders[:1])
        assert np.array_equal(written[0].now, parts[0].now) and np.array_equal(kept[0], after_write[0])
        back, before = node.held_write(written, numerators[:1], WRITE.walls[:1], kept, -1)
        assert np.array_equal(back[0].now, part.now) and np.array_equal(before[0], remainders[0])
    # the write's walls from the rows: E_s T for the time part, E_s x 3 den T for each axis part (the sources' one
    # den 7), the remainders' origin half the wall; two sources of different den share the least common multiple
    assert WRITE.walls == (7 * 64,) + (7 * 3 * 7 * 64,) * 3 and WRITE.factors == {2: 1}
    origins = node.write_origins(WRITE.walls, (1, 1, 1), KIND)
    assert [int(a[0, 0, 0]) for a in origins] == [wall // 2 for wall in WRITE.walls]
    mixed = [Row("row", (1, 1), 4, False, False, 5, 0), Row("a", (1, 4), 1, False, False, None, 0)]
    mixed.append(Row("b", (5, 6), 1, False, False, None, 0))
    assert held_write(family_rules(mixed), 0, 10) == HeldWrite((50, 1800, 1800, 1800), {1: 3, 2: 2})


def written_world(folder: Path, name: str, world: dict, mode: dict) -> Path:
    """A world file and its mode file beside it, written by hand."""
    (path := folder / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    return path


def laid_count(folder: Path, name: str, world: dict, mode: dict) -> int:
    """The count the share reads for a hand-written body declared at 1, read from the gate's refusal by name."""
    with pytest.raises(ValueError, match="declares the count 1 and its family's share reads") as refused:
        GameBoard(load_world(written_world(folder, name, world, mode)))
    return int(re.search(r"reads (\d+) quanta", str(refused.value)).group(1))


def cube_world(folder: Path) -> Path:
    """The closed cube of 9^3 in the tests' universe (every held row stepped, the two with a gap among them), with one body of matter on its centre Node at the count the lay makes, its mode a profile symmetric under the cube's 48 (no standing record: it breathes)."""
    universe_beside(folder)
    world = dict(shape=[9, 9, 9], boundary=dict(x="closed", y="closed", z="closed"), ticks=8)
    world.update(universe="u.json", engine="e.json", detectors=[])
    distance = np.abs(np.indices((9, 9, 9)) - 4).sum(axis=0)
    select = np.select([distance == 0, distance == 1, distance == 2], [1200, 600, 200], 0)
    levels = select.ravel().tolist()
    mode = {"family": "matter", "pair": [4000, 6000], "moving": {"now": levels, "before": levels}}
    body = {"family": "matter", "nodes": [{"node": [4, 4, 4], "count": 1}]}
    body["nodes"][0]["count"] = laid_count(folder, "cube", {**world, "measured": [body]}, mode)
    return written_world(folder, "cube", {**world, "measured": [body]}, mode)


def turned(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    """An array under one of the cube's 48: its axes permuted and reflected."""
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def keeps_the_48(board: GameBoard) -> None:
    """Every scalar array keeps the cube's 48 about the body to the bit, and a held family's tensions and their write remainders transform as the diagonal of a tensor: every line of every NodeState."""
    for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
        for state in board.states:
            tensor = (
                len(state.lines) == 1 + 3
            )  # the massless row: the time line and the three axis lines
            scalars = state.lines[:1] if tensor else state.lines
            arrays = [getattr(r, k) for r in scalars for k in KEYS] + state.write_remainders[:1]
            assert all(np.array_equal(turned(a, axes, signs), a) for a in arrays)
            tensions = [state.write_remainders[1:]] if tensor else []
            tensions += [[getattr(r, k) for r in state.lines[1:]] for k in KEYS if tensor]
            for triple in tensions:
                assert all(
                    np.array_equal(turned(triple[axes[a]], axes, signs), triple[a]) for a in range(3)
                )


def test_the_interval_on_a_closed_cube_is_rule3_conserves_the_count_keeps_the_48_and_returns(
    tmp_path, monkeypatch
):
    """(b) A body on a closed cube of 9^3: the gate refuses a declared count off the share by name and admits the one it reads; at the start every holder of the content with a level stands at an isotropic rest about the body, its level at the six neighbours of the centre one number below the centre's (the vector test of the two rows); each interval the matter's levels change and are Rule3 from the interval's start at every Node with every holder of the content read once as its stepped time part (a family of quanta with a gap steps; the guard on the gap that froze matter on main is gone with the laid row), the share read at the start's paces changes by the net currents plus the paces' anisotropy term and Rule3's remainder term exactly up to the division act's floors while the paces' own change (the well breathing about the body) moves the books' total beside, and every part of every NodeState keeps the cube's 48 about the body; the back-in-time gate (tools/back_in_time.py) over twelve intervals forward and twelve back returns every array bit for bit, MATCH (the tension's act has no count in its divisor and dumps nothing)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(cube_world(tmp_path)))
    matter, gravity = board.states[MATTER], board.states[GRAVITY]
    holders = [s for f, s in zip(FAMILIES, board.states, strict=True) if f.held and not f.wronskian]
    centre = (4, 4, 4)
    for level in (holder.lines[0].now for holder in holders if holder.lines[0].now[centre] > 0):
        near = by_hand(level, centre)
        assert len(set(near)) == 1 and 0 < near[0] < int(level[centre]), near
    moved = []
    for _ in range(4):
        start = node.Record(*(getattr(matter.lines[0], k).copy() for k in KEYS))
        padded = np.pad(start.now, 1)
        rolled = [np.roll(padded, 1, a) + np.roll(padded, -1, a) for a in range(3)]
        sums = tuple(r[1:-1, 1:-1, 1:-1] for r in rolled)
        content = sum(holder.lines[0].now for holder in holders)
        read = content, tuple((gravity.lines[1 + a].now + 1) // 2 for a in range(3))
        reads, self_coefficient, rule_wall = coefficients(4000, 6000, GAMMA, *read)
        expected = rule3(reads, sums, self_coefficient, rule_wall, *(getattr(start, k) for k in KEYS))
        moved.append(within_the_reach(board, MATTER))
        assert not np.array_equal(matter.lines[0].now, start.now)  # a family of quanta with a gap steps
        assert np.array_equal(matter.lines[0].now, expected[0])
        assert np.array_equal(matter.lines[0].remainder, expected[1])
        keeps_the_48(board)
    back = BACK.verdict(board, 12)
    tensions = [(int(p.now.min()), int(p.now.max())) for p in gravity.lines[1:]]
    drifts = {name: book["drift"] for name, book in board.books().items()}
    print(f"GAMEBOARD the cube: the tensions' ranges {tensions}, the gate over 12 intervals {back},")
    print(f"  the shares' drifts {drifts}, the paces' part of matter's per interval {moved}")
    assert back["verdict"] == "MATCH" and board.tick == 5


def chain_world_by_hand(folder: Path, envelope: list[int], turn: int) -> Path:
    """A world on the chain of 48 (x open) with one body written by hand: a real pair at the envelope (now = before, a breathing record and no standing mode) and, with `turn`, a second pair `turn` times a sixteenth of the envelope an interval before (a rotating record of that sense, of the charged family, matter's pair as a plane; 0 a real body of matter), its count the one the lay makes, the detectors `left` and `right` at the chain's ends."""
    universe_beside(folder, charged=turn != 0)
    levels, first = [0] * CHAIN, CHAIN // 2 - len(envelope) // 2
    levels[first : first + len(envelope)] = envelope
    second = {"im_now": [0] * CHAIN, "im_before": [turn * v // 16 for v in levels]} if turn else {}
    moving, family = {"now": levels, "before": levels, **second}, CHARGED["name"] if turn else "matter"
    mode = {"family": family, "pair": [4000, 6000], "moving": moving}
    ends = [{"name": "left", "positions": [[0, 0, 0]]}]
    ends += [{"name": "right", "positions": [[CHAIN - 1, 0, 0]]}]
    world = dict(shape=[CHAIN, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), ticks=400)
    world.update(face_depth=1, universe="u.json", engine="e.json", detectors=ends)
    body = {"family": family, "nodes": [{"node": [CHAIN // 2, 0, 0], "count": 1}]}
    body["nodes"][0]["count"] = laid_count(folder, "hand", {**world, "measured": [body]}, mode)
    return written_world(folder, "hand", {**world, "measured": [body]}, mode)


def test_light_is_born_by_the_write_on_the_chain(tmp_path, monkeypatch):
    """(c) On the chain, a breathing body of the charged family (a plane) rotating in the sense +1 writes its Wronskian's quanta into the sign holder's record each interval, the record it started from at 0: a wave leaves it (the charge's levels nonzero away from the body), the charge's share in quanta stays within the Nodes' rounding and the body's share read at each interval's paces changes by the net currents plus the anisotropy and the remainder terms exactly up to the floors over 400 intervals (the well it digs moves the paces, and the share read at the moving paces with them, the paces' part printed beside; no quantum changes family), the body reads the light it writes plainly into its paces (its family a plane; ALGEBRA.md #the-paces, the dimension's table) and every output line is a click of an end detector (the light's inflow there); a real body of matter writes nothing into it and no light is born; both runs go back in time whole, the back-in-time gate MATCH over 400 intervals forward and 400 back, every held row a stepped record whose level at the interval's start the state after it still holds and no coefficient read from a Node's own state (ALGEBRA.md #what-is-open, item 21)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    envelope = [v * 4 // 5 for v in PROFILE[3:13]]
    for turn in (1, 0):
        lines: list[dict[str, object]] = []
        board = GameBoard(load_world(chain_world_by_hand(tmp_path, envelope, turn)), lines.append)
        body = [f.name for f in board.families].index(CHARGED["name"] if turn else "matter")
        states = [board.states[body], board.states[CHARGE]]
        board.step()
        laid = quanta_of(board, body)
        assert len(states[1].lines) == 1  # light is the sign holder's own record, one real line
        assert (CHARGE in [r.family for r in board.families[body].reads]) == bool(turn)
        away = np.ones(board.shape, dtype=bool)
        away[CHAIN // 2 - 8 : CHAIN // 2 + 8] = False
        born, counts, moved = 0, [], 0
        for _ in range(399):
            moved += within_the_reach(board, body)
            born = born or (board.tick if states[1].lines[0].now[away].any() else 0)
            counts.append(quanta_of(board, body))
            assert abs(quanta_of(board, CHARGE)) <= CHAIN
        clicks = [e for e in lines if e["family"] == "charge" and e["event"] == "click"]
        first = clicks[0]["tick"] if clicks else None
        drifts = {name: book["drift"] for name, book in board.books().items()}
        print(f"DETECTOR the chain, sense {turn}: {len(clicks)} charge clicks, first at {first}")
        print(
            f"GAMEBOARD light born at {born}, the body's quanta {min(counts)} to {max(counts)} over 400"
        )
        print(f"  (laid {laid}; the paces' part of the change {moved}), the shares' drifts {drifts}")
        ends = ("left", "right", "face")  # the end detectors and the open faces' layer at the same Nodes
        assert all(e["detector"] in ends for e in lines if e["event"] == "click")
        assert born > 0 if turn else (born == 0 and not clicks and not states[1].lines[0].now.any())
        back = BACK.verdict(GameBoard(load_world(tmp_path / "hand.json")), 400)
        print(f"GAMEBOARD the chain of the sense {turn}, the gate over 400 intervals: {back}")
        assert back["verdict"] == "MATCH" and back["intervals"] == 400


def test_a_static_bodys_write_stands_still_its_tail_is_tense_and_a_taker_reads_the_light(
    tmp_path, monkeypatch
):
    """(c, d) The generator's body of 50 on the chain laid rotating (the charged family, a plane), its fixed point, the gate admitting its declared count as the share's own reading: the Wronskian's quanta it writes into the sign holder each interval sum over its Nodes to a total that moves within the rounding over its period (a static body writes a static level); its share in quanta over the board, read at the paces of the read, is printed as the books' reading (the owner's word of 2026-10-01: the share stays the count, its drift under a moving well a reading and no line), over 180 intervals, this side of the horizon the two bodies' rows reach later (the share is undefined where every pace is 0); its tail carries a nonzero mean tension on x over its period; a second body, the taker, a real body of matter, is read by the detector `taker`, whose clicks are the charge's inflow into its Nodes, signed and never 0, the net light that entered it over the run printed as its reading (a bare region passes the light on)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(24, 40), senses=(1, 0), taker=True)
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(world), lines.append)
    turning = [f.name for f in board.families].index(CHARGED["name"])
    matter, family = board.states[turning], board.families[turning]
    declared = [sum(row.counts) for row in board.world.bodies]
    read = [int(board.quanta(row.family)[board.mask(row.nodes)].sum()) for row in board.world.bodies]
    assert all(((abs(c - r) - 1) // 2) ** 2 <= c for c, r in zip(declared, read, strict=True))
    board.step()
    laid = quanta_of(board, turning)
    body, writes, counts, tensions, totals = board.body_nodes(0), [], [], [], []
    tail = body & ~board.mask(((24, 0, 0),))
    for _ in range(179):  # this side of the horizon the two bodies' rows reach later
        turn = node.well(node.wronskian(matter.lines), T)
        writes.append(int(turn[body].sum()))
        tensions.append(int(node.stresses_of(family.pair[0], matter.lines, board.wrap)[0][tail].sum()))
        within_the_reach(board, turning)
        counts.append(int(board.quanta(turning)[body].sum()))
        totals.append(quanta_of(board, turning))
    mode = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    span = mode["period"][0] // mode["period"][1] + 1
    swings = [max(writes[i : i + span]) - min(writes[i : i + span]) for i in range(100, 179 - span)]
    taken = [e for e in lines if e["detector"] == "taker" and e["family"] == "charge"]
    print(
        f"GAMEBOARD the static body of {int(body.sum())} Nodes, declared {declared} read {read}: swing"
    )
    print(f"  over a period at most {max(swings)} quanta (the write {min(writes)} to {max(writes)}),")
    pace = board.books()[family.name]["pace"]
    print(f"  the share over the board {min(totals)} to {max(totals)} (laid {laid}, the pace {pace}),")
    tension, entered = sum(tensions[100 : 100 + span]), sum(e["inflow"] for e in taken)
    print(f"  its quanta {min(counts)} to {max(counts)}, the tail's x tension over a period {tension};")
    print(f"  DETECTOR the taker's clicks {len(taken)}, the light that entered {entered}")
    assert max(swings) <= int(body.sum()) and tension != 0
    assert taken and all(e["event"] == "click" and e["inflow"] != 0 for e in taken)  # signed, never 0


def stress_by_hand(now: np.ndarray, num: int) -> list[np.ndarray]:
    """T_aa(i) = num (G_aa(i) + G_aa(i - a)) div 2 on a periodic board by rolls alone, the advisor's line."""
    found = []
    for axis in range(3):
        plus, minus = np.roll(now, -1, axis), np.roll(now, 1, axis)
        g = now * (np.roll(now, -2, axis) - now) - plus * (plus - minus)
        found.append((num * (g + np.roll(g, 1, axis))) // 2)
    return found


def difference(a: np.ndarray, axis: int) -> np.ndarray:
    """The level's difference across the axis's two Ports on a periodic board."""
    return np.roll(a, -1, axis) - np.roll(a, 1, axis)


def test_the_tension_is_rule3s_own_conservation_of_the_current():
    """(d) On a periodic cube of 6^3 in the vacuum: w (P_a(t + 1) - P_a(t)) = SUM_b R_b (G_ab(i - b) - G_ab(i)) exactly once the remainders' term is added, P_a the count's line's current per axis and G_ab the flux of the a-momentum through the b-Link at one time; the engine's tension is num (G_aa(i) + G_aa(i - a)) div 2 at every Node; a plane wave of the amplitude b on the exact band [1, 2] at k = pi / 3 has G_xx = -2 b^2 sin^2 k = -3 b^2 / 2 and a uniform record 0."""
    draw, shape = np.random.default_rng(3), (6, 6, 6)
    (read, _, _), self_coefficient, wall = coefficients(4000, 6000, GAMMA, 0)
    start = drawn(draw, shape, 3000, 1)
    record = node.step(start, node.quanta_rule(FAMILIES[MATTER], GAMMA, 0), WRAP)
    nxt, remainder = record.now.astype(object), record.remainder.astype(object)
    now, before = start.now.astype(object), start.before.astype(object)

    def flux(a: int, b: int) -> np.ndarray:
        return now * np.roll(difference(now, a), -1, b) - np.roll(now, -1, b) * difference(now, a)

    def momentum(x: np.ndarray, y: np.ndarray, a: int) -> np.ndarray:
        return x * difference(y, a) - y * difference(x, a)

    differences = []
    for a in range(3):
        left = wall * (momentum(nxt, now, a) - momentum(now, before, a))
        right = sum(read * (np.roll(flux(a, b), 1, b) - flux(a, b)) for b in range(3))
        expected = right - remainder * difference(now, a) + now * difference(remainder, a)
        assert np.array_equal(left, expected)
        differences.append(int(np.abs(left - right).max()))
    stresses = node.stresses_of(FAMILIES[MATTER].pair[0], [record], WRAP)
    by_hand_stress = stress_by_hand(record.now, 4000)
    assert all(np.array_equal(t, h) for t, h in zip(stresses, by_hand_stress, strict=True))
    print(f"GAMEBOARD the identity's remainders' term at most {max(differences)}, the wall {wall}")
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    exact = family_rules([Row("exact", (1, 2), 1, False, False, None, 0)])[0]
    plane = [node.Record(wave, wave, node.zeros(shape, KIND))]
    tension = node.stresses_of(exact.pair[0], plane, WRAP)
    assert (tension[0] == -3 * 2000 * 2000 // 2).all() and not tension[1].any() and not tension[2].any()
    flat = [node.Record(0 * wave + 7, 0 * wave + 7, node.zeros(shape, KIND))]
    assert not any(t.any() for t in node.stresses_of(exact.pair[0], flat, WRAP))


def chain_record(now_turn: tuple[int, ...], before_turn: tuple[int, ...]) -> node.Record:
    """A record on a chain: the envelope PROFILE times a character, (1, 0, -1, 0) at the step's level and its turn at the level before."""
    size, turns = len(PROFILE), len(now_turn)
    levels = ([PROFILE[x] * turn[x % turns] for x in range(size)] for turn in (now_turn, before_turn))
    return node.Record(*(np.array(level, dtype=np.int64).reshape(size, 1, 1) for level in levels), 0)


def test_a_moving_record_and_a_resting_one_source_the_tension_along_x_alone():
    """(d) On a chain, a record of matter moving along +x (the envelope times the plane wave's character, a quarter turn per Link) sources the vacuum's row's tension on x below 0 (a plane wave's -2 num b^2 sin^2 k) and none on y and z, so the Link's pace along x rises by the axis content above the pace along y; the same envelope at rest sources a tension of its own sign on x (the pressure of a standing record) and none on y and z; every family reads every holder of the content as its stepped time part, light as matter."""
    shape, wrap = (16, 1, 1), Wrap(False, True, True)
    matter, gravity = FAMILIES[MATTER], FAMILIES[GRAVITY]
    for moving in (True, False):
        turns = ((1, 0, -1, 0), (0, -1, 0, 1)) if moving else ((1,), (1,))
        record, write = chain_record(*turns), held_write(FAMILIES, GRAVITY, T)
        held, wall = node.empty_state(gravity, shape, write.walls, KIND), count_wall(matter, T)
        count = share.quanta_of(share.family_share(matter, (record,), wrap, GAMMA), wall, KIND)
        stress = node.stresses_of(matter.pair[0], [record], wrap)
        numerators = node.write_sources(GRAVITY, FAMILIES, {}, {MATTER: stress}, write)
        held.lines, held.write_remainders = node.held_write(
            held.lines, numerators, write.walls, held.write_remainders
        )
        xx = held.lines[1].now
        low, high, part = int(stress[0].min()), int(stress[0].max()), (int(xx.min()), int(xx.max()))
        print(f"GAMEBOARD the record {'moving' if moving else 'at rest'}: tension on x {low} to {high}")
        print(f"  the xx part {part}")
        assert not (moving and int(stress[0].max()) > 0) and bool((stress[0] != 0).any())
        assert not stress[1].any() and not stress[2].any() and not held.lines[2].now.any()
        states = [
            node.empty_state(f, shape, walls, KIND) for f, walls in zip(FAMILIES, WALLS, strict=True)
        ]
        states[GRAVITY] = held
        stepped = np.arange(16, dtype=np.int64).reshape(shape)  # the vacuum's row's stepped time part
        held.lines[0] = node.Record(stepped, stepped, node.zeros(shape, KIND))
        content, axis = node.read(MATTER, FAMILIES, states, 1)
        assert np.array_equal(axis[0], (xx + 1) // 2) and not axis[1].any()
        assert np.array_equal(content, stepped)
        contact = node.Record(count, count, node.zeros(shape, KIND))  # the bound charge's level
        states[NAMES.index("polarisation")].lines[0] = contact
        light, _axis = node.read(CHARGE, FAMILIES, states, 1)
        assert np.array_equal(light, stepped + count)  # every reader reads the rows as they stand


def test_a_static_source_gives_a_static_field_that_falls_with_the_range_of_the_rows_pair():
    """(f) The local test of the two rows on a chain (x open) of sixteen ranges: the binding holder's pair from the file at its divisor, started at its rest under a static source of 1,000 quanta per interval at the centre Node (features/start), falls from the Node by e^(-kappa) per Link with cosh kappa = 3 den / num - 2 (ALGEBRA.md #the-well, the reach of a held family is its pair), the range R = 1 / kappa (20 Links at [2400, 2401]): the level at R / 2, R and 3 R / 2 Links within one unit of the centre's times e^(-r / R); stepped by Rule3 at the pace 1 with the same source written each interval through the one wall E_s T (1,000 T in the numerator), the field is static within the rounding: the first interval moves no Node by more than two units and fewer than one Node in ten at all (the Nodes whose rounding residual passes the half wall, the remainder's origin), and over 200 intervals no Node drifts by more than two units per Node kicked, those kicks being Rule3's own waves along the chain (the fixed point is a pair, level and remainder)."""
    binding = FAMILIES[NAMES.index("binding")]
    num, den = binding.pair
    kappa = math.acosh(3 * den / num - 2)
    reach = round(1 / kappa)
    assert binding.divisor is not None and reach == 20
    shape, wrap = (16 * reach, 1, 1), Wrap(False, True, True)
    source, centre = node.zeros(shape, KIND), 8 * reach
    source[centre] = 1000
    field = rest(source, binding.pair, wrap, binding.divisor, 2**63 - 1, node.part_rule(binding)[2])
    away = (0, reach // 2, reach, 3 * reach // 2)
    at = [int(field.levels[centre + r, 0, 0]) for r in away]
    assert all(abs(at[i] - round(at[0] * math.exp(-kappa * r))) <= 1 for i, r in enumerate(away))
    walls = WALLS[NAMES.index("binding")]
    state = node.empty_state(binding, shape, walls, KIND)
    state.lines[0] = node.Record(
        field.levels.copy(), field.levels.copy(), np.full(shape, field.remainder)
    )
    kicked, drift = 0, 0
    for interval in range(200):
        state.lines[0] = node.step(state.lines[0], node.part_rule(binding), wrap)
        state.lines, state.write_remainders = node.held_write(
            state.lines, [source * T], walls, state.write_remainders
        )
        moved = np.abs(state.lines[0].now - field.levels)
        if interval == 0:
            kicked = int((moved > 0).sum())
            assert int(moved.max()) <= 2 and 10 * kicked < shape[0], (int(moved.max()), kicked)
        drift = max(drift, int(moved.max()))
    after = [int(state.lines[0].now[centre + r, 0, 0]) for r in away]
    print(f"GAMEBOARD the binding holder's rest at {away} Links {at}, after 200 intervals {after};")
    print(f"  {kicked} Nodes of {shape[0]} kicked at the first interval, the drift at most {drift}")
    assert drift <= 2 * kicked


def test_the_wronskians_sign_is_read_from_the_record_and_a_real_record_has_none():
    """(e) On a periodic cube of 6^3 at a fixed pace, a record rotating as e^(-i omega t) on the lowest wave number (two level pairs a quarter turn apart) has a Wronskian above 0 at every Node (`node.wronskian`, from the record and nothing kept beside it); Rule3 steps both pairs with one rule and the sign stays +1 at every Node over 100 intervals; the opposite rotation has the opposite sign; a real record's Wronskian is 0 at every Node."""
    shape, wrap = (6, 6, 6), WRAP
    matter = FAMILIES[MATTER]
    rule = node.quanta_rule(matter, GAMMA, 700)
    x = np.indices(shape)[0]
    cosine = np.take([4000, 2000, -2000, -4000, -2000, 2000], x)  # 4000 cos(2 pi x / 6)
    turned = np.take([2800, 1400, -1400, -2800, -1400, 1400], x)  # an interval before, cos omega = 0.7
    quarter = np.take([2857, 1428, -1428, -2857, -1428, 1428], x)  # the second pair's, sin omega
    for sense in (1, -1):
        record = node.Record(cosine, turned, node.zeros(shape, KIND))
        second = node.Record(node.zeros(shape, KIND), sense * quarter, node.zeros(shape, KIND))
        lines = [record, second]
        assert (np.sign(node.wronskian(lines)) == sense).all()
        for _ in range(100):
            lines = [node.step(line, rule, wrap) for line in lines]
            assert (np.sign(node.wronskian(lines)) == sense).all()
    assert not node.wronskian(
        [node.Record(cosine, turned, second.now), node.empty_record(shape, KIND)]
    ).any()


def light_alone_world(folder: Path, name: str, extent: int, first: int, **keys: object) -> Path:
    """A chain of `extent` Nodes (x open) in a universe of the sign holder alone (light reads nothing), a packet of light at k = pi / 4 about x = `first` laid by the generator, a detector at the file's Node 15 and `keys` the world's further keys (the receding faces)."""
    universe_beside(folder, drop=tuple(name for name in NAMES if name != "charge"))
    world = dict(shape=[extent, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), face_depth=1)
    world.update(ticks=200, universe="u.json", engine="e.json", measured=[], **keys)
    world["messages"] = [{**PACKET, "top": {"x": [first, first], "y": [0, 0], "z": [0, 0]}}]
    world["detectors"] = [{"name": "post", "positions": [[15, 0, 0]]}]
    (path := folder / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def test_a_receding_face_grows_the_gameboard_before_the_front_and_the_run_returns(tmp_path, monkeypatch):
    """(g) The receding face (ALGEBRA.md #the-objects, the unbounded board) on a chain of 16 in a universe of light alone, both faces receding to the largest size 64 by 4 layers at a time: the loader refuses by name a receding face on a periodic axis, a largest size within the shape and a side by another word; the GameBoard grows by 4 layers of zeros beyond a face whenever a level stands on the layer before it (the front spreads one Link an interval each way), every grown Node at the state of a Node with no level, so the run is the run of the larger chain it grew into, bit for bit at every interval over the shared Nodes, the books the same and every declared coordinate the file's (the mask, the click lines at the file's Node 15); the light's share over the original 16 Nodes reads 0 at the end where the fixed chain holds the reflected packet; the run ends, lawful and named, with the front on the layer before the face at the largest size, the runner and the look writing the end and the look every frame's shape and offset; the back-in-time gate says MATCH over the intervals run, each step back taking off the layers its forward step grew."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    both = {"x": {"sides": ["low", "high"], "largest": 64, "layers": 4}}
    for receding, reason in (
        ({"y": {**both["x"], "sides": ["high"]}}, "stands on an open or closed axis"),
        ({"x": {**both["x"], "largest": 16}}, "receding.x.largest must be an integer from 17"),
        ({"x": {**both["x"], "sides": ["far"]}}, "a side is one of"),
    ):
        with pytest.raises(ValueError, match=reason):
            load_world(light_alone_world(tmp_path, "refused", 16, 8, receding=receding))
    lines: list[dict[str, object]] = []
    world = light_alone_world(tmp_path, "grows", 16, 8, receding=both)
    grows, history = GameBoard(load_world(world), lines.append), []
    fixed = GameBoard(load_world(light_alone_world(tmp_path, "fixed", 16, 8)))
    while grows.ended is None:
        grows.step()
        if grows.ended is None:
            fixed.step()
            history.append((grows.shape[0], grows.offset[0], BACK.snapshot(grows)[0]))
    low, end = grows.offset[0], {"interval": 28, "axis": "x", "side": "high", "largest": 64}
    large = GameBoard(load_world(light_alone_world(tmp_path, "large", 64, 8 + low)))
    for extent, offset, snapshot in history:
        large.step()
        at, wide = slice(low - offset, low - offset + extent), BACK.snapshot(large)[0]
        assert all(np.array_equal(a, b[at]) for (_, a), (_, b) in zip(snapshot, wide, strict=True))
    books = grows.books()["charge"]
    assert grows.ended == end and grows.tick == 28 and books["share"] == large.books()["charge"]["share"]
    assert grows.mask(((15, 0, 0),))[15 + low, 0, 0] and all("node" not in e for e in lines)
    assert not grows.quanta(0)[low : low + 16].any() and fixed.quanta(0).any()
    assert RUN.run_input(str(world), str(tmp_path))["ticks"] == 28
    written = json.loads((tmp_path / "grows.output.json").read_text(encoding="utf-8"))
    look = RECORD.record(world, None)
    assert written["verdict"] == "LAWFUL" and written["ended"] == end == look["ended"]
    assert [look["frames"][k]["shape"][0] for k in (0, 28)] == [16, 64] and lines
    assert look["frames"][28]["offset"][0] == low
    back = BACK.verdict(GameBoard(load_world(world)), 100)
    assert back["verdict"] == "MATCH" and back["intervals"] == 27 and back["ended"] == end


def test_the_massless_row_rests_at_the_vacuum_content_up_to_every_face_and_beyond(tmp_path, monkeypatch):
    """(h) The vacuum content (ALGEBRA.md #what-is-open, item 22): the massless row's `rest` in the universe file, refused by name on a holder of the sign and on a row with a gap; on a chain (x open at the origin, receding beyond 24) with an inner face at x = 10 the row starts at 60 at every Node, the beyond Node's among them, its remainder at the half wall, and stays there bit for bit with no growth and no field line but 0; a kick of 12 laid on the row travels (the field line at the region rises, no count in it), the layers grown before its front stand at 60 and the gate says MATCH; light's share over a region is its field line."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    receding = {"x": {"sides": ["high"], "largest": 64, "layers": 4}}
    world = light_alone_world(tmp_path, "light", 24, 6, receding=receding)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"] = [r for r in UNIVERSE_ROWS if r["name"] in ("gravity", "charge", "binding")]
    for name in ("charge", "binding"):
        rows = json.loads(json.dumps(universe["families"]))
        next(row for row in rows if row["name"] == name)["held"]["rest"] = 60
        (tmp_path / "u.json").write_text(json.dumps({**universe, "families": rows}), encoding="utf-8")
        with pytest.raises(ValueError, match="only the massless"):
            load_world(world)
    universe["families"][0]["held"]["rest"] = 60
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    still = json.loads(world.read_text(encoding="utf-8"))
    still.update(messages=[], faces=[{"axis": "x", "at": 10, "gaps": []}], ticks=30)
    (tmp_path / "still.json").write_text(json.dumps(still), encoding="utf-8")
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(tmp_path / "still.json"), lines.append)
    gravity = board.families.index(next(f for f in board.families if f.rest))
    time = board.states[gravity].lines[0]
    assert (time.now == 60).all() and (time.before == 60).all() and (time.remainder == 8999).all()
    for _ in range(30):
        board.step()
    assert (board.states[gravity].lines[0].now == 60).all() and board.shape[0] == 24
    assert all(line["reading"] == 0 for line in lines if line["event"] == "field")
    kick = json.loads((tmp_path / "still.json").read_text(encoding="utf-8"))
    packet = {**PACKET, "family": "gravity", "amplitude": 12, "edge": {"x": 3, "y": 0, "z": 0}}
    packet["top"] = {"x": [4, 4], "y": [0, 0], "z": [0, 0]}
    kick.update(faces=[], ticks=40, messages=[packet])
    (tmp_path / "kick.json").write_text(json.dumps(kick), encoding="utf-8")
    TOOL.main(["--input", str(tmp_path / "kick.json")])
    lines.clear()
    board = GameBoard(load_world(tmp_path / "kick.json"), lines.append)
    assert abs(board.states[gravity].lines[0].now[4, 0, 0] - 60) == 12
    for _ in range(40):
        board.step()
    grown = board.states[gravity].lines[0].now[24:, 0, 0]
    assert board.shape[0] > 24 and (grown[-1] == 60) and (grown != 60).any()
    readings = [x["reading"] for x in lines if x["event"] == "field" and x["family"] == "gravity"]
    assert max(readings) > 0
    assert BACK.verdict(GameBoard(load_world(tmp_path / "kick.json")), 40)["verdict"] == "MATCH"
    output = RUN.run_input(str(world), str(tmp_path))
    written = json.loads((tmp_path / "light.output.json").read_text(encoding="utf-8"))
    lit = [x for x in written["lines"] if x["event"] == "field" and x["family"] == "charge"]
    assert output["verdict"] == "LAWFUL" and lit and max(x["reading"] for x in lit) > 0

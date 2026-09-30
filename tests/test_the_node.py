"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand; the interval on a closed cube of one body, every level Rule3's, the count conserved, the 48 symmetries kept in every part, the back-in-time gate MATCH over twelve intervals; on the chain light is born by the write: a breathing body writes a wave into the sign holder's own record, its count's total stays 0 within the rounding, a static body's write stands still within the rounding, and the click at the end detector is the measurement; the tension is Rule3's own conservation of the current; the sense is the Wronskian, booked by the line."""

from __future__ import annotations

import json
import re
from itertools import permutations, product
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import flow, lay, node
from event_universe.core.rule3 import coefficients, rule3
from event_universe.game_board import GameBoard
from event_universe.loader.derived import family_rules
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, ROOT, UNIVERSE, chain_body_world, load_file, universe_beside

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")
WRAP, HERE, KEYS = (True, True, True), (1, 1, 1), ("now", "before", "remainder")
ROWS = [("held", (4, 4), "content", 7), ("gapped", (3, 4), "content", 7), ("quanta", (5, 7), None, None)]
HELD, GAPPED, QUANTA = family_rules(ROWS)
UNIVERSE_ROWS = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
FAMILIES = family_rules(  # the tests' universe: gravity, charge, polarisation, matter, third
    [
        (r["name"], tuple(r["pair"]), *[r.get("held", {}).get(k) for k in ("count", "divisor")])
        for r in UNIVERSE_ROWS
    ]
)
NAMES = [family.name for family in FAMILIES]
MATTER, GRAVITY, CHARGE = (NAMES.index(name) for name in ("matter", "gravity", "charge"))
GAMMA, T = 6000, 32768
PROFILE = [0, 0, 0, 200, 400, 600, 800, 1000, 1000, 800, 600, 400, 200, 0, 0, 0]


def by_hand(a: np.ndarray, node: tuple[int, int, int]) -> tuple[int, ...]:
    """The six neighbours' levels of one Node on a periodic board, read by its address alone."""
    found = []
    for axis in range(3):
        for side in (1, -1):
            there = list(node)
            there[axis] = (there[axis] + side) % a.shape[axis]
            found.append(int(a[tuple(there)]))
    return tuple(found)


def quanta_state(record: node.Record, shape: tuple[int, int, int]) -> node.NodeState:
    """A NodeState of a family of quanta with a real record, its count 0 and its second pair 0."""
    zero = node.zeros(shape)
    return node.NodeState(record, zero, zero.copy(), None, [], None, node.empty_record(shape))


def total_of(state: node.NodeState, wall: int) -> int:
    """SUM (W_c c + r) of a family's count over the GameBoard."""
    return int((wall * state.count.astype(object) + state.count_remainder).sum())


def drawn(draw: np.random.Generator, shape: tuple[int, int, int], size: int, top: int) -> node.Record:
    """A random level pair within `size` with a remainder below `top`."""
    return node.Record(
        *(draw.integers(-size, size, shape) for _ in range(2)), draw.integers(0, top, shape)
    )


def test_one_nodes_acts_are_rule3_called_by_hand():
    """(a) On random NodeStates of a periodic board of 3^3: the levels' step, the lay, the count's line, the well and the hold at one Node equal Rule3 called by hand on that Node's integers (each act's direction -1 is the feature tests' and the back-in-time gate's); a laid row's level before returns; the tension's act is one carried division per axis at the wall E_s W_c from its origin, with no count in it."""
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
        # the lay from the weighted share: [w (now^2 + before^2) - S now before] div (2 p^2) - num now S_6(before)
        count_wall, now_here, before_here = 3 * 7 * 64, int(after.now[HERE]), int(after.before[HERE])
        node_term = wall * (now_here**2 + before_here**2) - self_coefficient * now_here * before_here
        share = node_term // (2 * (100 - 2 * content) ** 2) - 5 * now_here * sum(
            by_hand(after.before, HERE)
        )
        count, remainder = lay.lay(QUANTA, (after,), 64, WRAP, 100, content)
        assert (int(count[HERE]), int(remainder[HERE])) == divmod(share + count_wall // 2, count_wall)
        # the count's line: the six currents num (now_i before_j - before_i now_j), W_c c + r moved by their sum
        state = node.NodeState(after, count, remainder, None, [], None)
        written = node.count_line(QUANTA, state, 64, 1 << 20, WRAP)
        now_j, before_j = by_hand(after.now, HERE), by_hand(after.before, HERE)
        flux = sum(5 * (now_here * b - before_here * n) for n, b in zip(now_j, before_j, strict=True))
        moved = divmod(count_wall * int(count[HERE]) + int(remainder[HERE]) + flux, count_wall)
        assert (int(written.count[HERE]), int(written.remainder[HERE])) == moved
        # the well: (now^2 - next x before + r) div T
        carry = draw.integers(0, 64, shape)
        quanta, carried = node.well(node.form(levels, after), carry, 64)
        form = here[0] ** 2 - int(after.now[HERE]) * here[1]
        assert (int(quanta[HERE]), int(carried[HERE])) == divmod(form + int(carry[HERE]), 64)
        # the hold: a row without a gap gains (source + r) div E_s at its time part, its parts stepped before it
        part, source = drawn(draw, shape, 900, 12), draw.integers(0, 400, shape)
        parts = [part] + [node.empty_record(shape)] * 3
        held = node.NodeState(None, None, None, None, parts, draw.integers(0, 7, shape))
        parts, carry_after_hold, _flows = node.held_step(HELD, held, source)
        increment, carry_after = divmod(int(source[HERE]) + int(held.carry[HERE]), 7)
        found = (int(parts[0].now[HERE]), int(carry_after_hold[HERE]))
        assert found == (int(part.now[HERE]) + increment, carry_after)
        # a row with a gap is laid, not stepped: (source + r) div E_s, the level before kept beside it, back exact
        held.parts = [part]
        laid, laid_carry, _flows = node.held_step(GAPPED, held, source)
        assert (int(laid[0].now[HERE]), int(laid_carry[HERE])) == (increment, carry_after)
        assert np.array_equal(laid[0].before, part.now) and np.array_equal(
            laid[0].remainder, part.remainder
        )
        stood = node.NodeState(None, None, None, None, laid, laid_carry)
        assert np.array_equal(node.held_step(GAPPED, stood, source, -1)[0][0].now, part.now)
    # the tension's act (w x T_aa + r) div (E_s W_c) per axis from its origin (E_s W_c) div 2 = 7, back exact
    ones = np.ones((3, 1, 1), dtype=np.int64)
    current = flow.Flow(3, (5 * ones, -3 * ones, 4 * ones), 2)
    levels, carries = [0 * ones for _ in range(4)], flow.flow_origins(HELD, 2, (3, 1, 1))
    written, found = flow.flow_hold(HELD, levels, current, carries, 1)
    assert [int(level[0, 0, 0]) for level in written] == [0, 1, -1, 1]
    assert [int(carry[0, 0, 0]) for carry in found] == [8, 12, 5]
    back, returned = flow.flow_hold(HELD, written, current, found, -1)
    assert all(np.array_equal(a, b) for a, b in zip(back + returned, levels + carries, strict=True))


def written_world(folder: Path, name: str, world: dict, mode: dict) -> Path:
    """A world file and its mode file beside it, written by hand."""
    (path := folder / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    return path


def laid_count(folder: Path, name: str, world: dict, mode: dict) -> int:
    """The count the lay makes for a hand-written body declared at 1, read from the gate's refusal by name."""
    with pytest.raises(ValueError, match="declares the count 1 and its family's form lays") as refused:
        GameBoard(load_world(written_world(folder, name, world, mode))).step()
    return int(re.search(r"lays (\d+) quanta", str(refused.value)).group(1))


def cube_world(folder: Path) -> Path:
    """The closed cube of 9^3 in the tests' universe without its row with a gap (laid, its inverse is (a)'s), with one body of matter on its centre Node at the count the lay makes, its mode a profile symmetric under the cube's 48 (no standing record: it breathes)."""
    universe_beside(folder, drop=("polarisation",))
    world = dict(shape=[9, 9, 9], boundary=dict(x="closed", y="closed", z="closed"), ticks=8)
    world.update(universe="u.json", engine="e.json", detectors=[])
    distance = np.abs(np.indices((9, 9, 9)) - 4).sum(axis=0)
    levels = (
        np.select([distance == 0, distance == 1, distance == 2], [1200, 600, 200], 0).ravel().tolist()
    )
    mode = {"family": "matter", "pair": [4000, 6000], "moving": {"now": levels, "before": levels}}
    body = {"family": "matter", "nodes": [{"node": [4, 4, 4], "count": 1}]}
    body["nodes"][0]["count"] = laid_count(folder, "cube", {**world, "measured": [body]}, mode)
    return written_world(folder, "cube", {**world, "measured": [body]}, mode)


def turned(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    """An array under one of the cube's 48: its axes permuted and reflected."""
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def keeps_the_48(board: GameBoard) -> None:
    """Every scalar array keeps the cube's 48 about the body to the bit, and a held family's tensions and their carries transform as the diagonal of a tensor: every part of every NodeState."""
    for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
        for state in board.states:
            scalars = [r for r in (state.levels, state.second) if r is not None] + state.parts[:1]
            arrays = [getattr(r, k) for r in scalars for k in KEYS]
            arrays += [a for a in (state.count, state.count_remainder, state.carry) if a is not None]
            assert all(np.array_equal(turned(a, axes, signs), a) for a in arrays)
            tensions = [list(carries) for carries in state.flows.values()]
            tensions += [[getattr(r, k) for r in state.parts[1:]] for k in KEYS if len(state.parts) > 1]
            for triple in tensions:
                assert all(
                    np.array_equal(turned(triple[axes[a]], axes, signs), triple[a]) for a in range(3)
                )


def test_the_interval_on_a_closed_cube_is_rule3_conserves_the_count_keeps_the_48_and_returns(
    tmp_path, monkeypatch
):
    """(b) A body on a closed cube of 9^3: the gate refuses a declared count off the weighted lay by name and admits the laid one; each interval the matter's levels are Rule3 from the interval's start at every Node with the vacuum's row read once, SUM (W_c c + r) stands to the bit, and every part of every NodeState keeps the cube's 48 about the body; the back-in-time gate (tools/back_in_time.py) over twelve intervals forward and twelve back returns every array bit for bit, MATCH (the tension's act has no count in its divisor and dumps nothing)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(cube_world(tmp_path)))
    matter, gravity = board.states[MATTER], board.states[GRAVITY]
    wall, total = node.count_wall(board.families[MATTER], T), None
    for _ in range(4):
        start = node.Record(*(getattr(matter.levels, k).copy() for k in KEYS))
        padded = np.pad(start.now, 1)
        sums = tuple(
            (np.roll(padded, 1, a) + np.roll(padded, -1, a))[1:-1, 1:-1, 1:-1] for a in range(3)
        )
        read = gravity.parts[0].now.copy(), tuple((gravity.parts[1 + a].now + 1) // 2 for a in range(3))
        reads, self_coefficient, rule_wall = coefficients(4000, 6000, GAMMA, *read)
        expected = rule3(reads, sums, self_coefficient, rule_wall, *(getattr(start, k) for k in KEYS))
        board.step()
        assert np.array_equal(matter.levels.now, expected[0])
        assert np.array_equal(matter.levels.remainder, expected[1])
        assert total is None or total_of(matter, wall) == total
        total = total_of(matter, wall)
        keeps_the_48(board)
    back = BACK.verdict(board, 12)
    tensions = [(int(p.now.min()), int(p.now.max())) for p in gravity.parts[1:]]
    print(f"GAMEBOARD the cube: the tensions' ranges {tensions}, the gate over 12 intervals {back}")
    assert back["verdict"] == "MATCH" and board.tick == 5
    assert all(book["balanced"] for book in board.books().values())


def chain_world_by_hand(folder: Path, envelope: list[int], turn: int) -> Path:
    """A world on the chain of 48 (x open) with one body of matter written by hand: a real pair at the envelope (now = before, a breathing record and no standing mode), its second pair `turn` times the envelope an interval before (a rotating record of that sense, 0 a real one), its count the one the lay makes, the detectors `left` and `right` at the chain's ends."""
    universe_beside(folder)
    levels, first = [0] * CHAIN, CHAIN // 2 - len(envelope) // 2
    levels[first : first + len(envelope)] = envelope
    moving = {
        "now": levels,
        "before": levels,
        "im_now": [0] * CHAIN,
        "im_before": [turn * v for v in levels],
    }
    mode = {"family": "matter", "pair": [4000, 6000], "moving": moving}
    ends = [
        {"name": "left", "positions": [[0, 0, 0]]},
        {"name": "right", "positions": [[CHAIN - 1, 0, 0]]},
    ]
    world = dict(shape=[CHAIN, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), ticks=400)
    world.update(face_depth=1, universe="u.json", engine="e.json", detectors=ends)
    body = {"family": "matter", "nodes": [{"node": [CHAIN // 2, 0, 0], "count": 1}]}
    body["nodes"][0]["count"] = laid_count(folder, "hand", {**world, "measured": [body]}, mode)
    return written_world(folder, "hand", {**world, "measured": [body]}, mode)


def test_light_is_born_by_the_write_on_the_chain(tmp_path, monkeypatch):
    """(c) On the chain, a breathing body rotating in the sense +1 writes its Wronskian's quanta into the sign holder's record each interval, the record it started from at 0: a wave leaves it (the charge's levels nonzero away from the body), the charge's SUM (W_c c + r) stays to the bit and its count's total within the Nodes' rounding, no quantum changes family (the matter's SUM (W_c c + r) to the bit over 400 intervals), and the quanta entering the end detectors are the clicks; a real body (no sense) writes nothing into it and no light is born."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    envelope = [v * 4 // 5 for v in PROFILE[3:13]]
    for turn in (1, 0):
        lines: list[dict[str, object]] = []
        board = GameBoard(load_world(chain_world_by_hand(tmp_path, envelope, turn)), lines.append)
        states = [board.states[MATTER], board.states[CHARGE]]
        walls = [node.count_wall(FAMILIES[index], T) for index in (MATTER, CHARGE)]
        board.step()
        totals = [total_of(state, wall) for wall, state in zip(walls, states, strict=True)]
        assert states[1].levels is states[1].parts[0]  # light is the sign holder's own record
        away = np.ones(board.shape, dtype=bool)
        away[CHAIN // 2 - 8 : CHAIN // 2 + 8] = False
        born, counts = 0, []
        for _ in range(399):
            board.step()
            born = born or (board.tick if states[1].levels.now[away].any() else 0)
            counts.append(int(states[0].count.sum()))
            assert [total_of(s, w) for w, s in zip(walls, states, strict=True)] == totals
            assert abs(int(states[1].count.sum())) <= CHAIN
        clicks = [e for e in lines if e["family"] == "charge" and e["detector"] in ("left", "right")]
        first = clicks[0]["tick"] if clicks else None
        print(
            f"DETECTOR the chain, the sense {turn}: {len(clicks)} clicks of the charge, first at {first}"
        )
        print(
            f"GAMEBOARD light born at {born}, the matter's count {min(counts)} to {max(counts)} over 400"
        )
        assert all(e["event"] == "click" and e["axis"][0] == 0 for e in lines)
        assert (
            (born > 0 and clicks)
            if turn
            else (born == 0 and not clicks and not states[1].levels.now.any())
        )
        assert all(book["balanced"] and book["sense_balanced"] for book in board.books().values())


def test_a_static_bodys_write_stands_still_its_tail_is_tense_and_a_taker_reads_the_light(
    tmp_path, monkeypatch
):
    """(c, d) The generator's body of 50 on the chain laid rotating, its fixed point: the Wronskian's quanta it writes into the sign holder each interval sum over its Nodes to a total that moves within the rounding over its period (a static body writes a static level); its count stays its family's over 400 intervals, to the bit; its tail carries a nonzero mean tension on x over its period; a second body, the taker, holds 64 quanta of the charge read by the detector `taker`, whose clicks are the charge's quanta entering its Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(
        tmp_path, TOOL, at=(24, 40), holds={"charge": 64}, senses=(1, 0), taker=True
    )
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(world), lines.append)
    matter, family, bound = board.states[MATTER], FAMILIES[MATTER], board.world.amplitude_bound
    wall = node.count_wall(family, T)
    board.step()
    total = total_of(matter, wall)
    assert board.contents()[1]["charge"] == 64
    body, writes, counts, tensions = board.body_nodes(0), [], [], []
    tail = body & ~board.mask(((24, 0, 0),))
    for _ in range(399):
        turn = node.well(node.wronskian(matter.levels, matter.second), matter.wronskian_remainder, T)[0]
        writes.append(int(turn[body].sum()))
        tensions.append(int(node.count_line(family, matter, T, bound, board.wrap).stress[0][tail].sum()))
        board.step()
        counts.append(int(matter.count[body].sum()))
        assert total_of(matter, wall) == total
    mode = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    span = mode["period"][0] // mode["period"][1] + 1
    swings = [max(writes[i : i + span]) - min(writes[i : i + span]) for i in range(100, 399 - span)]
    taken = [e for e in lines if e["detector"] == "taker" and e["family"] == "charge"]
    print(
        f"GAMEBOARD the static body of {int(body.sum())} Nodes: the write's swing over a period at most"
    )
    print(
        f"  {max(swings)} quanta (the write {min(writes)} to {max(writes)}), its count {min(counts)} to"
    )
    print(f"  {max(counts)}, its tail's tension on x over a period {sum(tensions[100 : 100 + span])};")
    print(f"  DETECTOR the taker's clicks {len(taken)}")
    assert max(swings) <= int(body.sum()) and sum(tensions[100 : 100 + span]) != 0
    assert all(e["body"] == 1 for e in taken) and all(
        book["balanced"] for book in board.books().values()
    )


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
        assert np.array_equal(
            left, right - remainder * difference(now, a) + now * difference(remainder, a)
        )
        differences.append(int(np.abs(left - right).max()))
    written = node.count_line(FAMILIES[MATTER], quanta_state(record, shape), T, 1 << 20, WRAP)
    by_hand_stress = stress_by_hand(record.now, 4000)
    assert all(np.array_equal(t, h) for t, h in zip(written.stress, by_hand_stress, strict=True))
    print(
        f"GAMEBOARD the identity's remainders' term at most {max(differences)} against the wall {wall}"
    )
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    exact = family_rules([("exact", (1, 2), None, None)])[0]
    plane = quanta_state(node.Record(wave, wave, node.zeros(shape)), shape)
    tension = node.count_line(exact, plane, T, 1 << 20, WRAP).stress
    assert (tension[0] == -3 * 2000 * 2000 // 2).all() and not tension[1].any() and not tension[2].any()
    flat = quanta_state(node.Record(0 * wave + 7, 0 * wave + 7, node.zeros(shape)), shape)
    assert not any(t.any() for t in node.count_line(exact, flat, T, 1 << 20, WRAP).stress)


def chain_record(now_turn: tuple[int, ...], before_turn: tuple[int, ...]) -> node.Record:
    """A record on a chain: the envelope PROFILE times a character, (1, 0, -1, 0) at the step's level and its turn at the level before."""
    size, turns = len(PROFILE), len(now_turn)
    levels = ([PROFILE[x] * turn[x % turns] for x in range(size)] for turn in (now_turn, before_turn))
    return node.Record(*(np.array(level, dtype=np.int64).reshape(size, 1, 1) for level in levels), 0)


def test_a_moving_record_and_a_resting_one_source_the_tension_along_x_alone():
    """(d) On a chain, a record of matter moving along +x (the envelope times the plane wave's character, a quarter turn per Link) sources the vacuum's row's tension on x below 0 (a plane wave's -2 num b^2 sin^2 k) and none on y and z, so the Link's pace along x rises by the axis content above the pace along y; the same envelope at rest sources a tension of its own sign on x (the pressure of a standing record) and none on y and z; every family reads the vacuum's row as its stepped time part and the bound charge as the well it laid, light as matter."""
    shape, wrap = (16, 1, 1), (False, True, True)
    matter, gravity = FAMILIES[MATTER], FAMILIES[GRAVITY]
    for moving in (True, False):
        turns = ((1, 0, -1, 0), (0, -1, 0, 1)) if moving else ((1,), (1,))
        record, zero = chain_record(*turns), node.empty_record(shape)
        state = node.NodeState(record, None, None, None, [], None, zero)
        state.count, state.count_remainder = lay.lay(matter, (record, zero), T, wrap, GAMMA)
        stress = tuple(np.asarray(v) for v in node.count_line(matter, state, T, 1 << 20, wrap).stress)
        held, wall = node.empty_state(gravity, shape), node.count_wall(matter, T)
        held.flows = {MATTER: flow.flow_origins(gravity, wall, shape)}
        current = {MATTER: flow.Flow(1, (stress[0], stress[1], stress[2]), wall)}
        held.parts, held.carry, held.flows = node.held_step(gravity, held, node.zeros(shape), 1, current)
        xx = held.parts[1].now
        low, high, part = int(stress[0].min()), int(stress[0].max()), (int(xx.min()), int(xx.max()))
        print(
            f"GAMEBOARD the record {'moving' if moving else 'at rest'}: the tension on x {low} to {high},"
        )
        print(f"  the xx part {part}")
        assert not (moving and int(stress[0].max()) > 0) and bool((stress[0] != 0).any())
        assert not stress[1].any() and not stress[2].any() and not held.parts[2].now.any()
        states = [node.empty_state(family, shape) for family in FAMILIES]
        states[GRAVITY] = held
        stepped = np.arange(16, dtype=np.int64).reshape(shape)  # the vacuum's row's stepped time part
        node.with_parts(held, [node.Record(stepped, stepped, node.zeros(shape)), *held.parts[1:]])
        content, axis = node.signed_read(MATTER, FAMILIES, states, GAMMA, "now", shape)
        assert np.array_equal(axis[0], (xx + 1) // 2) and not axis[1].any()
        assert np.array_equal(content, stepped)
        laid_well = node.Record(
            state.count, state.count, node.zeros(shape)
        )  # the bound charge's laid level
        node.with_parts(states[NAMES.index("polarisation")], [laid_well])
        light, _axis = node.signed_read(CHARGE, FAMILIES, states, GAMMA, "now", shape)
        assert np.array_equal(light, stepped + state.count)  # every reader reads both rows as they stand


def test_the_sense_is_the_wronskian_booked_by_the_line_and_a_real_record_is_neutral():
    """(e) On a periodic cube of 6^3 at a fixed pace, a record rotating as e^(-i omega t) on the lowest wave number (two level pairs a quarter turn apart) has a Wronskian above 0 at every Node, its sense laid above 0 and read as q = +1; Rule3 steps both pairs with one rule and the sense's line moves the sense so SUM (W_c k + r) stays to the bit over 100 intervals; the opposite rotation has the opposite sense; a real record's Wronskian is 0 at every Node and its sense 0."""
    shape, wrap = (6, 6, 6), (True, True, True)
    matter = FAMILIES[MATTER]
    rule, wall = node.quanta_rule(matter, GAMMA, 700), node.count_wall(matter, T)
    x = np.indices(shape)[0]
    cosine = np.take([4000, 2000, -2000, -4000, -2000, 2000], x)  # 4000 cos(2 pi x / 6)
    turned = np.take([2800, 1400, -1400, -2800, -1400, 1400], x)  # an interval before, cos omega = 0.7
    quarter = np.take([2857, 1428, -1428, -2857, -1428, 1428], x)  # the second pair's, sin omega
    for sense in (1, -1):
        record = node.Record(cosine, turned, node.zeros(shape))
        second = node.Record(node.zeros(shape), sense * quarter, node.zeros(shape))
        state = node.NodeState(record, None, None, None, [], None, second)
        assert (np.sign(node.wronskian(record, second)) == sense).all()
        state.sense, state.sense_remainder = lay.lay_sense(matter, record, second, T, GAMMA, 700)
        assert (node.sense_sign(state, shape) == sense).all()
        total = int((wall * state.sense.astype(object) + state.sense_remainder).sum())
        for _ in range(100):
            state.levels = node.step(state.levels, rule, wrap)
            state.second = node.step(state.second, rule, wrap)
            written = node.sense_line(matter, state, T, 1 << 20, wrap)
            state.sense, state.sense_remainder = np.asarray(written.count), np.asarray(written.remainder)
            assert int((wall * state.sense.astype(object) + state.sense_remainder).sum()) == total
    real = node.Record(cosine, turned, node.zeros(shape))
    assert not node.wronskian(real, node.empty_record(shape)).any()
    assert not lay.lay_sense(matter, real, node.empty_record(shape), T, GAMMA)[0].any()

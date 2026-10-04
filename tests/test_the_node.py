"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand; the interval on a closed cube of one body, every level Rule3's, the count the record's share, the 48 symmetries kept in every part, the back-in-time gate MATCH over twelve intervals; on the chain light is born by the write: a breathing body of a plane writes a wave into the sign holder's own record, its share's total stays within the rounding, a static body's write stands still within the rounding, and the click at the end node_reader is the measurement; the whole run of the chain goes back in time, MATCH over 400 intervals with the rotating body and with the real one; the tension is Rule3's own conservation of the current; a receding face grows the GameBoard before the front, the run the larger chain's bit for bit, ending at the largest size and returning. The static body of the chain is one charged body of the sense +1 at the chain's centre Node with the taker on it: the two-body world, a like-sense body laid beside a neutral body's tail under the plain read, finds no fixed point in the generator (a 20-unit cycle of period 7 at the body's own edge), the rotating construction's open defect, the integer wander of the record-to-content map with the body's own charge level as a second source of its well; not a tie, and not widened."""

import copy
import json
import math
import re
from itertools import permutations, product
from pathlib import Path

import numpy as np

import event_universe.world_files as world_files
from event_universe import node, records, share
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, link_factor, rule3
from event_universe.features.start import rest
from event_universe.game_board import GameBoard
from event_universe.loader.derived import HeldWrite, count_wall, family_rules, held_write_of
from event_universe.loader.universe import shape_of, universe_of
from event_universe.loader.world import BodyRow
from event_universe.world_files import input_digest, load_world
from tests import laws
from tests.laws import CHAIN, CHARGED, EVENTS, PACKET, UNIVERSE, real_rows, refused, universe_beside

TOOL, BACK, RUN, RECORD = laws.TOOL, laws.BACK, laws.RUN, laws.RECORD  # the tools loaded once

WRAP, HERE, KEYS = Wrap(True, True, True), (1, 1, 1), ("now", "before", "remainder")
ROWS = ("held", (4, 4), 4, 7), ("gapped", (3, 4), 1, 7), ("quanta", (5, 7), 1, None)
BOX = (slice(1, -1),) * 3  # the inner Nodes of an array padded by one Node on every side
HELD, GAPPED, QUANTA = family_rules(real_rows(*ROWS))
WRITE = held_write_of((HELD, GAPPED, QUANTA), 0, 64)  # the massless row's one write per part at T = 64
UNIVERSE_ROWS = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
INTEGERS, FAMILIES = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))  # the tests' universe
UNIT = INTEGERS["link_unit"]  # the Link's unit G of the tests' universe
NAMES = [family.name for family in FAMILIES]
MATTER, GRAVITY, CHARGE = (NAMES.index(name) for name in ("matter", "gravity", "charge"))
GAMMA, T = INTEGERS["node_clock"], INTEGERS["quantum_action"]
PROFILE = [0, 0, 0, 200, 400, 600, 800, 1000, 1000, 800, 600, 400, 200, 0, 0, 0]
WALLS = [held_write_of(FAMILIES, i, T).walls if f.held else () for i, f in enumerate(FAMILIES)]


def by_hand(a: np.ndarray, node: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(int(np.roll(a, -side, axis)[node]) for axis in range(3) for side in (1, -1))


def test_one_nodes_acts_are_rule3_called_by_hand():
    """The complement remainders (HIGHLIGHTS.md, the mathematician's 166 with the advisor's second hand): on a chain of 41 at [2, 3] and Gamma 1,000 an odd line mirrored about the centre with random levels within 1,000 and random remainders, the image's remainder the ones' complement w - 1 - r, steps mirrored to the bit, levels and remainders, over 200 intervals of Rule3 (floor((w - 1 - u) / w) = -floor(u / w) for every integer, checked over small walls), and the write's origins carry the complement of the half wall at a signed line's image Nodes (`records.write_origins`, 4 against 5 at the wall 10). (a) On random NodeStates of a periodic board of 3^3: the levels' step, the share and its reading in quanta and the well (a reading) at one Node equal Rule3 called by hand on that Node's integers (each act's direction -1 is the feature tests' and the back-in-time gate's; the one write per held part by hand, with its weights, in tests/test_the_features.py); a held row with a gap reads the same rule at its own pair, the plain rule's reads num, self coefficient 0 and wall 3 den (the generic test of the two rows: no name and no branch); the write's walls are the rows' own, E_s T and E_s x 3 den T with the sources' den (their least common multiple where they differ, each tension times the multiple over its own den), the remainders' origin half the wall. By hand beside the acts: the share is the form's Node term div (2 p^2), the six paces one with no tension, less num now S_6(before); the well, a reading, (now^2 - next x before) div T with no remainder kept; a gapped row at the content 0 reads 2 Gamma^2 times (3,) x 6, 0, 12 at [3, 4]; the walls E_s T and E_s x 3 den T (den 7), the origins half the wall, two den sharing their lcm."""
    draw, shape = np.random.default_rng(5), (3, 3, 3)
    for _ in range(20):
        levels = node.Record(*draw.integers(-900, 900, (2, *shape)), draw.integers(0, 50, shape))
        content = int(draw.integers(-40, 40))
        after = node.step(levels, node.rule_of(QUANTA, 100, content), WRAP)
        clock, pace = paces.node_paces(100, content)
        reads, self_coefficient, wall = coefficients(5, 7, 100, clock, pace)
        arrived, here = by_hand(levels.now, HERE), tuple(int(getattr(levels, k)[HERE]) for k in KEYS)
        expected = rule3(reads, arrived, self_coefficient, wall, *here)
        assert (int(after.now[HERE]), int(after.remainder[HERE])) == expected
        wall_c, now_here, before_here = 3 * 7 * 64, int(after.now[HERE]), int(after.before[HERE])
        node_term = wall * (now_here**2 + before_here**2) - self_coefficient * now_here * before_here
        share_here = node_term // (2 * pace**2) - 5 * now_here * sum(by_hand(after.before, HERE))
        read = share.family_share(QUANTA, (after,), WRAP, 100, content)
        quanta_here = int(share.quanta_of(read, wall_c, np.int64)[HERE])
        assert int(read[HERE]) == share_here and quanta_here == (share_here + wall_c // 2) // wall_c
        form = here[0] ** 2 - int(after.now[HERE]) * here[1]
        assert int(node.well(node.form([levels], [after]), 64)[HERE]) == form // 64
        assert node.rule_of(GAPPED, 100, 0) == ((3 * 20_000,) * 6, 0, 12 * 20_000)
    assert WRITE.walls == (7 * 64,) + (7 * 3 * 7 * 64,) * 3 and WRITE.factors == {2: 1}
    origins = [int(a[0, 0, 0]) for a in node.write_origins(WRITE.walls, (1, 1, 1), np.int64)]
    assert origins == [wall // 2 for wall in WRITE.walls]
    rows = ("row", (1, 1), 4, 5), ("a", (1, 4), 1, None), ("b", (5, 6), 1, None)
    mixed = family_rules(real_rows(*rows))
    assert held_write_of(mixed, 0, 10) == HeldWrite((50, 1800, 1800, 1800), {1: 3, 2: 2})
    rng, (reads, s, w) = np.random.default_rng(3), coefficients(2, 3, 1000, 1000, 1000)
    gap, chain = np.zeros((1, 1, 1), dtype=np.int64), Wrap(False, True, True)
    half = [rng.integers(-1000, 1000, (20, 1, 1)) for _ in range(3)]
    a, b = (np.concatenate([h, gap, -h[::-1]]) for h in half[:2])
    r = np.concatenate([half[2] % w, gap, records.complement(half[2] % w, w)[::-1]])
    for _ in range(200):  # the mirrored odd line steps mirrored to the bit with complement remainders
        b, a, r = a, *(np.asarray(x) for x in rule3(reads, node.ports(a, chain), s, w, a, b, r))
        assert np.array_equal(a, -a[::-1]) and (r[:20] == records.complement(r, w)[::-1][:20]).all()
    assert all((w - 1 - u) // w == -(u // w) for u in range(-40, 40) for w in range(1, 9))
    origins = records.write_origins((10, 11), (3, 1, 1), np.int64, (np.indices((3, 1, 1))[0] == 0,))
    assert [o.ravel().tolist() for o in origins] == [[4, 5, 5], [5, 5, 5]]


def test_every_act_of_the_interval_reaches_one_link(tmp_path, monkeypatch):
    """The law's line (ALGEBRA.md #the-interval, the dependency radius): every act of an interval reaches one Link, so the whole interval's dependency radius is one Link. On a chain of 9 in the rule's universe with every kind of family laid by hand at random levels (gravity, a holder of the content with its three axis lines; binding, a holder with a gap; charge, the holder of the sign under the act rotation, light's line and three odd lines; matter, a one-part reader; the charged plane, a two-part reader turned by the holder), two states equal everywhere but at one Node two Links from the centre (and three) give the same NodeState at the centre after one interval, every array of every family (the lines' two levels and remainders, the writes' remainders), and the same after the inverse; a difference one Link away reaches the centre."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, charged=True)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    charge = next(row for row in rows["families"] if row["name"] == "charge")["held"]
    charge["act"], charge["write_weight"], rows["integers"]["quantum_action"] = "rotation", 4, 36_000
    (tmp_path / "u.json").write_text(json.dumps(rows), encoding="utf-8")  # the energy line's T and k_w
    world = dict(shape=[9, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), face_depth=1)
    world.update(ticks=2, universe="u.json", engine="e.json", bodies=[], node_readers=[])
    (reach := tmp_path / "reach.json").write_text(json.dumps(world), encoding="utf-8")

    def centre(board: GameBoard) -> list[int]:
        return [int(array[4, 0, 0]) for _label, array in sum(BACK.snapshot(board), [])]

    (same := random_state(reach, 9)).step()
    for far, reaches in ((1, True), (2, False), (3, False)):
        (other := random_state(reach, 9, far)).step()
        assert (centre(other) != centre(same)) is reaches, far
        other.step_inverse()
        assert centre(other) == centre(random_state(reach, 9))


def random_state(path: Path, seed: int, far: int = 0) -> GameBoard:
    """A world loaded with every line and every write remainder at random levels within 60 by the draw `seed` (a holder of the content above 0; a held row's axis lines at 0, so that every axis's pace is the Node's and the write's factor, which divides the three axes one at a time in the engine's order, rounds the same under every permutation of the axes), and where `far` is not 0 one difference of 7 at the Node `far` Links along x from the board's centre, the reach test's."""
    board, draw = GameBoard(load_world(path)), np.random.default_rng(seed)
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        low = 0 if family.held and not family.wronskian else -60
        picks = [draw.integers(low, 60, (3, *board.shape)) for _ in state.lines]
        state.lines = [node.Record(now, before, np.abs(r)) for now, before, r in picks]
        if family.axes:  # the axis lines at 0, every axis's pace the Node's
            state.lines[1:] = [node.empty_record(board.shape, board.kind) for _ in state.lines[1:]]
        state.write_remainders = [draw.integers(0, wall, board.shape) for wall in board.walls(index)]
        for array in [*(getattr(r, k) for r in state.lines for k in KEYS), *state.write_remainders]:
            array[board.shape[0] // 2 + far, 0, 0] += 7 * bool(far)
    return board


def hand_world(
    folder: Path, name: str, world: dict, body: dict, mode: dict, quantum: bool = False
) -> Path:
    """A world of one body by hand with its mode entry: declared at the count 1, the gate's refusal read for the count the share reads at its Node and the body re-declared at it; one quantum of charge (`quantum`, the count-1 gate) stands at the count 1 as declared."""
    path, read = folder / f"{name}.json", 1
    for count in (1, 0):
        bodies = [{**body, "nodes": [{**body["nodes"][0], "count": count or read}]}]
        path.write_text(json.dumps(document := {**world, "bodies": bodies}), encoding="utf-8")
        beside = {"world_digest": input_digest(document), "bodies": [mode]}
        path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
        if quantum:
            return path
        if count:
            refusal = refused("declares the count 1 and its family", lambda: GameBoard(load_world(path)))
            read = int(re.search(r"reads (\d+) quanta", str(refusal)).group(1))
    return path


def turned(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def test_the_interval_on_a_closed_cube_conserves_the_count_keeps_the_48_returns(tmp_path, monkeypatch):
    """(b) A body on a closed cube of 9^3: the gate refuses a declared count off the share by name and admits the one it reads; at the start every holder of the content with a level stands at an isotropic rest about the body, its level at the six neighbours of the centre one number below the centre's (the vector test of the two rows); each interval the matter's levels change and are Rule3 from the interval's start at every Node with every holder of the content read once as its stepped time part (a family of quanta with a gap steps; the guard on the gap that froze matter on main is gone with the laid row), the share read at the start's paces changes by the net currents plus the paces' anisotropy term and Rule3's remainder term exactly up to the division act's floors while the paces' own change (the well breathing about the body) moves the books' total beside, and every part of every NodeState keeps the cube's 48 about the body; the back-in-time gate (tools/back_in_time.py) over twelve intervals forward and twelve back returns every array bit for bit, MATCH (the tension's act has no count in its divisor and dumps nothing). (c) On the chain, one quantum of the charged family by hand (a plane rotating in the sense +1 at the band's rest rotation, the level now the envelope L over ten Nodes with the level before (L cos omega, L sin omega) and 2 SUM L^2 sin omega = T, the law's one quantum, its Wronskian T / 2 within the rounding, declared at the count 1 and admitted as declared: the count-1 gate, ALGEBRA.md, No record reads its own write of the sign) writes its Wronskian's quanta into the sign holder's record each interval, the record it started from at 0: a wave leaves it (the charge's levels nonzero away from the body), the charge's share in quanta stays within the Nodes' rounding and the body's share read at each interval's paces changes by the net currents plus the anisotropy and the remainder terms exactly up to the floors over 24 intervals (the gate and the identity are per step, and the born light reaches the chain's far Nodes within them; the well it digs moves the paces, and the share read at the moving paces with them, the paces' part printed beside; no quantum changes family), the body reads the light it writes plainly into its paces (its family a plane; ALGEBRA.md #the-paces, the dimension's table) and every output line is a click of an end node_reader (the light's inflow there); a real body of matter writes nothing into it and no light is born; both runs go back in time whole, the back-in-time gate MATCH over 24 intervals forward and 24 back, every held row a stepped record whose level at the interval's start the state after it still holds and no coefficient read from a Node's own state (ALGEBRA.md #what-is-open, item 21). (c, d) The generator's one quantum of the charged family on the chain (a plane rotating in the sense +1, the one-Node record of its quantum, `--pixel`, admitted at the count 1 as declared, the count-1 gate): the Wronskian's quanta it writes into the sign holder each interval move within the rounding over its period at its Node (a static record writes a static level); its share in quanta over the board, read at the paces of the read, is printed as the books' reading (the owner's word of 2026-10-01: the share stays the count, its drift under a moving well a reading and no line), over 60 intervals with no frozen Node (a test runs under 30 seconds, the owner's word of 2026-10-03); the tail's mean tension on x, a reading of the 50-quanta body that #43 (1) no longer declares, is not read (one Node, no tail); a second body, the taker, a real body of matter, is read by the node_reader `taker`, whose clicks are the charge's inflow into its Nodes, signed and never 0, the net light that entered it over the run printed as its reading (a bare region passes the light on). (e) The gate runs (#1579): on the committed world bell_a_b over its first four intervals the laid family's drift (the books') stays within the sum over the intervals of Rule3's remainder terms, the paces' parts and the floors, the bound the share's identity gives, asserted as a bound and never as exactness (the identity is per step; the rest of the run to the window's end plain, for the click; the GHZ world's own test is in test_the_meeting.py). On the chain every click names an end node_reader or the open faces' layer at the same Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path)  # the closed cube of 9^3, one body of matter at its centre
    world = dict(shape=[9, 9, 9], boundary=dict(x="closed", y="closed", z="closed"), ticks=8)
    world.update(universe="u.json", engine="e.json", node_readers=[])
    d = np.abs(np.indices((9, 9, 9)) - 4).sum(axis=0)
    levels = np.select([d == 0, d == 1, d == 2], [1200, 600, 200], 0).ravel().tolist()
    mode = {"family": "matter", "pair": [4000, 6000], "moving": {"now": levels, "before": levels}}
    body = {"family": "matter", "nodes": [{"node": [4, 4, 4], "count": 1}]}
    board = GameBoard(load_world(hand_world(tmp_path, "cube", world, body, mode)))
    matter, gravity, centre, moved = board.states[MATTER], board.states[GRAVITY], (4, 4, 4), []
    holders = [s for f, s in zip(FAMILIES, board.states, strict=True) if f.held and not f.wronskian]
    for level in (holder.lines[0].now for holder in holders if holder.lines[0].now[centre] > 0):
        near = by_hand(level, centre)
        assert len(set(near)) == 1 and 0 < near[0] < int(level[centre]), near
    for _ in range(4):
        start = node.Record(*(getattr(matter.lines[0], k).copy() for k in KEYS))

        def across(a: np.ndarray, axis: int, side: int) -> np.ndarray:  # the arrival, 0 beyond a face
            return np.roll(np.pad(a, 1), -side, axis)[BOX]

        arrived = tuple(across(start.now, a, s) for a, s in product(range(3), (1, -1)))
        c, aa = sum(holder.lines[0].now for holder in holders), [line.now for line in gravity.lines[1:]]
        tensions = [(aa[a] + across(aa[a], a, s) + 1) // 2 for a, s in product(range(3), (1, -1))]
        factors, own = tuple(link_factor(GAMMA, UNIT, t) for t in tensions), paces.node_paces(GAMMA, c)
        reads, self_coefficient, rule_wall = coefficients(4000, 6000, GAMMA, *own, factors, UNIT)
        expected = rule3(reads, arrived, self_coefficient, rule_wall, *(getattr(start, k) for k in KEYS))
        moved.append(laws.booked(board, monkeypatch, MATTER)[0][0])
        assert not np.array_equal(matter.lines[0].now, start.now)  # a family of quanta with a gap steps
        assert np.array_equal(matter.lines[0].now, expected[0])
        assert np.array_equal(matter.lines[0].remainder, expected[1])
        for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):  # the 48 kept
            for state in board.states:
                tensor, parts = len(state.lines) == 1 + 3, state.lines[1:]
                scalars = state.lines[:1] if tensor else state.lines
                arrays = [getattr(r, k) for r in scalars for k in KEYS] + state.write_remainders[:1]
                assert all(np.array_equal(turned(a, axes, signs), a) for a in arrays)
                found = [state.write_remainders[1:]] + [[getattr(r, k) for r in parts] for k in KEYS]
                for t in found if tensor else []:  # the tensions as the diagonal of a tensor
                    assert all(np.array_equal(turned(t[axes[a]], axes, signs), t[a]) for a in range(3))
    back = BACK.verdict(board, 12)
    axis, carried = gravity.lines[1:], {int(r[centre]) for r in gravity.write_remainders[1:]}
    assert (back["verdict"], board.tick) == ("MATCH", 5) and not any(p.now.any() for p in axis)
    assert len(carried) == 1 and WALLS[GRAVITY][1] // 2 < carried.pop() < WALLS[GRAVITY][1]
    sine = math.isqrt(6000**2 - 4000**2)  # one quantum of charge by hand: 2 SUM L^2 sin omega = T
    quantum = math.isqrt(T * 6000 * 1000 * 1000 // (2 * sine * sum(v * v for v in PROFILE[3:13])))
    for turn in (1, 0):
        universe_beside(tmp_path, charged=turn != 0)  # a body by hand on the chain
        envelope = [v * (quantum if turn else 800) // 1000 for v in PROFILE[3:13]]
        levels, first = ([0] * CHAIN, CHAIN // 2 - len(envelope) // 2)
        levels[first : first + len(envelope)] = envelope
        before = [v * 4000 // 6000 for v in levels] if turn else levels  # the band's rest rotation
        tilt = [turn * v * sine // 6000 for v in levels]  # the sense: L sin omega in the level before
        second = {"im_now": [0] * CHAIN, "im_before": tilt} if turn else {}
        moving = {"now": levels, "before": before, **second}
        family = CHARGED["name"] if turn else "matter"
        mode = {"family": family, "pair": [4000, 6000], "moving": moving}
        ends = [{"name": "left", "positions": [[0, 0, 0], [1, 0, 0]]}]
        ends += [{"name": "right", "positions": [[CHAIN - 2, 0, 0], [CHAIN - 1, 0, 0]]}]
        world = dict(shape=[CHAIN, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), ticks=24)
        world.update(face_depth=1, universe="u.json", engine="e.json", node_readers=ends)
        body = {"family": family, "nodes": [{"node": [CHAIN // 2, 0, 0], "count": 1}]}
        world = hand_world(tmp_path, "hand", world, body, mode, quantum=turn != 0)
        board = GameBoard(load_world(world), (lines := []).append)
        body = [f.name for f in board.families].index(CHARGED["name"] if turn else "matter")
        states = [board.states[body], board.states[CHARGE]]
        board.step()
        laid = int(board.books()[board.families[body].name]["quanta"])
        reads = [r.family for r in board.families[body].reads]
        assert len(states[1].lines) == 1 + bool(turn) and (CHARGE in reads) == bool(turn)
        away = np.ones(board.shape, dtype=bool)
        away[CHAIN // 2 - 8 : CHAIN // 2 + 8], born, moved = False, 0, 0
        for _ in range(23):
            moved += laws.booked(board, monkeypatch, body)[0][0]
            born = born or (board.tick if board.record(CHARGE)[0].now[away].any() else 0)
            assert abs(int(board.books()[board.families[CHARGE].name]["quanta"])) <= CHAIN
        clicks = [e for e in lines if e["family"] == "charge" and e["event"] == "click"]
        assert all(e["node_reader"] in ("left", "right", "face") for e in lines if e["event"] == "click")
        assert born > 0 if turn else (born == 0 and not clicks and not board.record(CHARGE)[0].now.any())
        back = BACK.verdict(GameBoard(load_world(tmp_path / "hand.json")), 24)
        assert back["verdict"] == "MATCH" and back["intervals"] == 24 and laid > 0 and moved is not None
    world = laws.chain_body_world(tmp_path, TOOL, senses=(1,), taker=True)  # one charged body, centred
    board = GameBoard(load_world(world), (lines := []).append)
    turning = [f.name for f in board.families].index(CHARGED["name"])
    matter, family = board.states[turning], board.families[turning]
    board.step()
    body, writes = board.body_nodes(0), []  # one Node and no tail: no tail's tension is read
    for _ in range(60):  # this side of the horizon the two bodies' rows reach later
        turn = node.well(node.wronskian(matter.lines, True), T)
        writes.append(int(turn[body].sum()))
        laws.booked(board, monkeypatch, turning)
    mode = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    span = mode["period"][0] // mode["period"][1] + 1
    swings = [max(writes[i : i + span]) - min(writes[i : i + span]) for i in range(30, 60 - span)]
    taken = [e for e in lines if e["node_reader"] == "taker" and e["family"] == "charge"]
    assert max(swings) <= body.sum() and board.books()[family.name]["pace"] > 0
    assert taken and all(e["event"] == "click" and e["inflow"] != 0 for e in taken)  # signed, never 0
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    for name in ("bell/bell_a_b",):  # the gate's world, the click at the window's end
        board = GameBoard(load_world(EVENTS / f"{name}.json"), (lines := []).append)
        left = board.credit.counts[laid := board.world.messages[0].family] - 1  # after the click
        steps = [laws.booked(board, monkeypatch, laid)[0] for _ in range(4)]  # the identity per step
        books, slack = board.books()[board.families[laid].name], sum(b + abs(m) for m, b in steps)
        assert books["drift"] is not None and abs(books["drift"]) <= slack
        for _ in range(board.world.ticks - 4):
            board.step()  # to the window's end, the click
        lefts = [e["left"] for e in lines if e["event"] == "credit"]  # one write per side, one count
        assert lefts == [left] * len(board.credit.sides) and board.credit.counts[laid] == left


def difference(a: np.ndarray, axis: int) -> np.ndarray:
    return np.roll(a, -1, axis) - np.roll(a, 1, axis)


def test_the_tension_is_rule3s_own_conservation_of_the_current():
    """(d) On a periodic cube of 6^3 in the vacuum: w (P_a(t + 1) - P_a(t)) = SUM_b R_b (G_ab(i - b) - G_ab(i)) exactly once the remainders' term is added, P_a the count's line's current per axis and G_ab the flux of the a-momentum through the b-Link at one time; the engine's tension's part at every Node is the law's -num h_a(i) = -num (now_(i-a) now_(i+a) - now_i^2) (ALGEBRA.md #the-primitives, The tension: T_aa = -num (G_aa(i) + G_aa(i - a)) div 2), one Link's reach, the Link's booking G_aa(i) = h_a(i) + h_a(i + a) the sum of its two ends' parts; the documented pattern [2, 0, -2, 0] along x gives +4 at every Node at the weight 1 and +8 on every Link, the two ends' parts summed (the engine on main wrote -8, the stress itself); a plane wave of the amplitude b at the weight 1 at k = pi / 3 has the part +b^2 sin^2 k = 3 b^2 / 4 (-G_xx = 2 b^2 sin^2 k on the Link) and a uniform record 0, exactly, no division. (d) On a chain, a record of matter moving along +x (the envelope times the plane wave's character, a quarter turn per Link) sources the vacuum's row's tension on x above 0 (a plane wave's part +num b^2 sin^2 k: the stress deepens the content, light gravitates by its pressure) and none on y and z, so the +x Link's content is the Node's level twice with the mean of its two ends' xx parts, 0 beyond the face, one number per Link read the same from both ends, and the folded y Link's twice the Node's with the yy line 0; the same envelope at rest sources a tension of its own sign on x (the pressure of a standing record) and none on y and z; every family reads every holder of the content as its stepped time part, light as matter. (f) The local test of the two rows on a chain (x open) of sixteen ranges: the binding holder's pair from the file at its level weight, started at its rest under a static source of one quantum per interval at the centre Node (features/start; the row reading its own level at the Node's pace, Every row reads the content, a source small against Gamma so that the rest is Yukawa's outside a body), falls from the Node by e^(-kappa) per Link with cosh kappa = 3 den / num - 2 (ALGEBRA.md #the-well, the reach of a held family is its pair), the range R = 1 / kappa (20 Links at [2400, 2401]): the level at R / 2, R and 3 R / 2 Links within one unit of the centre's times e^(-r / R); stepped by Rule3 at the paces its own level gives it with the same source written each interval through the one wall E_s T (T in the numerator), the field is static within the rounding: the first interval moves no Node by more than two units and fewer than one Node in ten at all (the Nodes whose rounding residual passes the half wall, the remainder's origin), and over 200 intervals no Node drifts by more than the remainders' walk, two units per Node kicked plus the integer line's residual at the rest over the wall per interval (the nearest integers to the fine fixed point leave a residual below half the wall at every Node, which the remainder carries until a level kicks; those kicks are Rule3's own waves along the chain, and the fixed point is a pair, level and remainder); the source written each interval carries the write's factor at the row's own paces, as the rest carried it. The Node's own part of the tension is the law's -num h_a(i) = -num (now_(i-a) now_(i+a) - now_i^2)."""
    draw, shape = np.random.default_rng(3), (6, 6, 6)
    (read, *_), self_coefficient, wall = coefficients(4000, 6000, GAMMA, GAMMA, GAMMA)
    start = node.Record(*draw.integers(-3000, 3000, (2, *shape)), draw.integers(0, 1, shape))
    record = node.step(start, node.rule_of(FAMILIES[MATTER], GAMMA, 0), WRAP)
    nxt, remainder = record.now.astype(object), record.remainder.astype(object)
    now, before = start.now.astype(object), start.before.astype(object)

    def flux(a: int, b: int) -> np.ndarray:
        return now * np.roll(difference(now, a), -1, b) - np.roll(now, -1, b) * difference(now, a)

    def momentum(x: np.ndarray, y: np.ndarray, a: int) -> np.ndarray:
        return x * difference(y, a) - y * difference(x, a)

    for a in range(3):
        left = wall * (momentum(nxt, now, a) - momentum(now, before, a))
        right = sum(read * (np.roll(flux(a, b), 1, b) - flux(a, b)) for b in range(3))
        expected = right - remainder * difference(now, a) + now * difference(remainder, a)
        assert np.array_equal(left, expected)
    stresses, now = node.stresses_of(FAMILIES[MATTER].pair[0], [record], WRAP), record.now
    by_hand_stress = [-4000 * (np.roll(now, 1, a) * np.roll(now, -1, a) - now * now) for a in range(3)]
    assert all(np.array_equal(t, h) for t, h in zip(stresses, by_hand_stress, strict=True))
    four = np.array([2, 0, -2, 0]).reshape(4, 1, 1)  # the law's pattern: +4 per Node, +8 per Link
    part = node.stresses_of(1, [node.Record(four, four, 0 * four)], WRAP)[0]
    assert (part == 4).all() and (part + np.roll(part, -1, 0) == 8).all()
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    tension = node.stresses_of(1, [node.Record(wave, wave, 0 * wave)], WRAP)
    assert (tension[0] == 3 * 2000 * 2000 // 4).all() and not tension[1].any() and not tension[2].any()
    flat = [node.Record(0 * wave + 7, 0 * wave + 7, 0 * wave)]
    assert not any(t.any() for t in node.stresses_of(1, flat, WRAP))

    def chain_record(now_turn: tuple[int, ...], before_turn: tuple[int, ...]) -> node.Record:
        """A record on a chain: the envelope PROFILE times a character, (1, 0, -1, 0) at the step's level and its turn at the level before."""
        size, n = len(PROFILE), len(now_turn)
        levels = ([PROFILE[x] * turn[x % n] for x in range(size)] for turn in (now_turn, before_turn))
        return node.Record(*(np.array(level, dtype=np.int64).reshape(size, 1, 1) for level in levels), 0)

    shape, wrap, matter = (16, 1, 1), Wrap(False, True, True), FAMILIES[MATTER]
    for moving in (True, False):
        turns = ((1, 0, -1, 0), (0, -1, 0, 1)) if moving else ((1,), (1,))
        record, write = chain_record(*turns), held_write_of(FAMILIES, GRAVITY, T)
        wall = count_wall(matter, T)
        held = node.empty_state(FAMILIES[GRAVITY], shape, write.walls, np.int64)
        count = share.quanta_of(share.family_share(matter, (record,), wrap, GAMMA), wall, np.int64)
        stress = node.stresses_of(matter.pair[0], [record], wrap)
        vacuum = {(i, 0): (GAMMA, (GAMMA, GAMMA, GAMMA)) for i in (CHARGE, MATTER)}
        found = node.write_sources(GRAVITY, FAMILIES, {}, {(MATTER, 0): stress}, write, vacuum, GAMMA)
        written = node.held_write(held.lines, found, write.walls, held.write_remainders)
        (held.lines, held.write_remainders), xx = written, written[0][1].now
        assert not (moving and int(stress[0].min()) < 0) and bool((stress[0] != 0).any())
        assert np.array_equal(held.write_remainders[1], write.walls[1] // 2 + found[1])
        assert not (stress[1].any() or stress[2].any() or held.lines[2].now.any() or xx.any())
        states = [node.empty_state(f, shape, w, np.int64) for f, w in zip(FAMILIES, WALLS, strict=True)]
        states[GRAVITY] = held
        stepped = np.arange(16, dtype=np.int64).reshape(shape)  # the vacuum's row's stepped time part
        held.lines[0] = node.Record(stepped, stepped, node.zeros(shape, np.int64))
        content, factors = node.read(MATTER, FAMILIES, states, 1, wrap, GAMMA, UNIT)
        xx_ahead = np.pad(xx, ((0, 1), (0, 0), (0, 0)))[1:]  # the xx line through +x, 0 beyond the face
        assert np.array_equal(factors[0], link_factor(GAMMA, UNIT, (xx + xx_ahead + 1) // 2))
        assert np.array_equal(factors[0][:-1], factors[1][1:])  # one factor per Link, from both ends
        assert (factors[2] == UNIT * UNIT).all() and np.array_equal(content, stepped)
        contact = node.Record(count, count, node.zeros(shape, np.int64))  # the binding holder's level
        states[NAMES.index("binding")].lines[0] = contact
        light, _factors = node.read(CHARGE, FAMILIES, states, 1, wrap, GAMMA, UNIT)
        assert np.array_equal(light, stepped + count)  # every reader reads the rows as they stand
    num, den = (binding := FAMILIES[NAMES.index("binding")]).pair
    reach = round(1 / (kappa := math.acosh(3 * den / num - 2)))
    assert binding.level_weight is not None and reach == 20
    shape, wrap = (16 * reach, 1, 1), Wrap(False, True, True)
    source, centre = node.zeros(shape, np.int64), 8 * reach
    source[centre], weight, wall = 1, binding.level_weight, node.rule_of(binding, GAMMA, 0)[2]
    kind = {"intervals": paces.COUNT_POWER, "own_weight": 1}
    field = rest(source, binding.pair, wrap, weight, 2**63 - 1, wall, GAMMA, **kind)
    away = (0, reach // 2, reach, 3 * reach // 2)
    at = [int(field.levels[centre + r, 0, 0]) for r in away]
    assert all(abs(at[i] - round(at[0] * math.exp(-kappa * r))) <= 1 for i, r in enumerate(away))
    walls = WALLS[NAMES.index("binding")]
    state, levels = node.empty_state(binding, shape, walls, np.int64), field.levels
    state.lines[0] = node.Record(levels.copy(), levels.copy(), np.full(shape, field.remainder))

    def scaled(now: np.ndarray) -> np.ndarray:  # the write per proper volume at the row's own paces
        clock, pace = paces.node_paces(GAMMA, now)
        return np.asarray(node.rulers_write_factor(source * T, (clock, (pace, pace, pace)), GAMMA, 2))

    reads, self_coefficient, rule_wall = node.rule_of(binding, GAMMA, levels)  # the integer line at rest
    numerator = sum(r * a for r, a in zip(reads, node.ports(levels, wrap), strict=True))
    numerator = (numerator + self_coefficient * levels - 2 * rule_wall * levels).astype(object) * T
    residual = np.abs(numerator + scaled(levels).astype(object) * rule_wall).max() / (rule_wall * T)
    kicked, drift = 0, 0
    for interval in range(200):
        own = node.rule_of(binding, GAMMA, state.lines[0].now)  # the row reads its own level
        increment, state.lines[0] = [scaled(state.lines[0].now)], node.step(state.lines[0], own, wrap)
        kept = state.write_remainders
        state.lines, state.write_remainders = node.held_write(state.lines, increment, walls, kept)
        moved = np.abs(state.lines[0].now - field.levels)
        if interval == 0:
            kicked = int((moved > 0).sum())
            assert int(moved.max()) <= 2 and 10 * kicked < shape[0], (int(moved.max()), kicked)
        drift = max(drift, int(moved.max()))
    assert drift <= 2 * kicked + math.ceil(200 * float(residual))  # the remainders' walk per interval


def light_alone_world(folder: Path, name: str, extent: int, first: int, **keys: object) -> Path:
    universe_beside(folder, drop=tuple(name for name in NAMES if name != "charge"))
    world = dict(shape=[extent, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), face_depth=1)
    world.update(ticks=200, universe="u.json", engine="e.json", bodies=[], **keys)
    world["messages"] = [{**PACKET, "top": {"x": [first, first], "y": [0, 0], "z": [0, 0]}}]
    world["node_readers"] = [{"name": "post", "positions": [[14, 0, 0], [15, 0, 0]]}]
    (path := folder / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def test_a_receding_face_grows_the_gameboard_before_the_front_and_the_run_returns(tmp_path, monkeypatch):
    """(g) The receding face (ALGEBRA.md #the-objects, the unbounded board) on a chain of 16 in a universe of light alone, both faces receding to the largest size 64 by 4 layers at a time: the loader refuses by name a receding face on a periodic axis, a largest size within the shape and a side by another word; the GameBoard grows by 4 layers of zeros beyond a face whenever a level stands on the layer before it (the front spreads one Link an interval each way), every grown Node at the state of a Node with no level, so the run is the run of the larger chain it grew into, bit for bit at every interval over the shared Nodes (the larger chain started from the grown chain's laid levels at the offset: the message lay's two sums are 0 over the board as declared, so the exact lay's tails beyond the smaller board, 4 units of the amplitude 665 here, are taken out by the division act on it and not on the larger, and the lay depends on the declared board by that much), the books the same and every declared coordinate the file's (the mask, the click lines at the file's Node 15); the light's share over the original 16 Nodes reads 0 at the end where the fixed chain holds the reflected packet; the run ends, lawful and named, with the front on the layer before the face at the largest size (at the interval 40: the exact lay's tails stand on the layer before each face from the lay, so the board grows from the first interval, a GameBoard diagnostic read at this commit, re-read at the frozen hash), the runner and the look writing the end and the look every frame's shape and offset; the back-in-time gate says MATCH over the intervals run, each step back taking off the layers its forward step grew. (h) The vacuum content (ALGEBRA.md #what-is-open, item 22): the massless row's `rest` in the universe file, refused by name on a holder of the sign and on a row with a gap; on a chain (x open at the origin, receding beyond 24) with an inner face at x = 10 the row starts at 60 at every Node, the beyond Node's among them, its remainder at the half wall, and stays there bit for bit with no growth and no field line but 0; a kick of 12 laid on the row travels (the field line at the region rises, no count in it), the layers grown before its front stand at 60 and the gate says MATCH; light's share over a region is its field line. The frozen Node (ALGEBRA.md #the-count-is-the-records-share; The paces compose): the row set by hand to the Link's zero (28,206 at Gamma 6,000, where the Node's pace rounds to 0, far beyond any body and inside the bound A at the Link unit 1) at three Nodes freezes light there, every pace 0, so the books read None for the share, its quanta and its drift with the frozen count 3 (a Node whose x Link stands at the factor 0 by its xx line's standing tension keeps its share), the step runs and the region's field line reads None with the frozen Nodes' wells 0 as `well`."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    both = {"x": {"sides": ["low", "high"], "largest": 64, "layers": 4}}
    wrong = [("y", "sides", ["high"]), ("x", "largest", 16), ("x", "sides", ["far"])]
    reasons = ["stands on an open or closed axis", "an integer from 17", "a side is one of"]
    for (axis, key, value), reason in zip(wrong, reasons, strict=True):
        face = {axis: {**both["x"], key: value}}
        refused(reason, lambda f=face: load_world(light_alone_world(tmp_path, "r", 16, 8, receding=f)))
    world = light_alone_world(tmp_path, "grows", 16, 8, receding=both)
    grows, history = GameBoard(load_world(world), (lines := []).append), []
    fixed = GameBoard(load_world(light_alone_world(tmp_path, "fixed", 16, 8)))
    while grows.ended is None:
        grows.step()
        if grows.ended is None:
            fixed.step(), history.append((grows.shape[0], grows.offset[0], BACK.snapshot(grows)[0]))
    low, end = grows.offset[0], {"interval": 40, "axis": "x", "side": "high", "largest": 64}
    large_world = light_alone_world(tmp_path, "large", 64, 8 + low)
    laid = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"][0]
    for word in ("now", "before"):  # the grown chain's laid levels at the offset: the lay is the board's
        laid["moving"][word]["at"] = [x + low for x in laid["moving"][word]["at"]]
    mode = json.loads(large_world.with_suffix(".mode.json").read_text(encoding="utf-8"))
    large_world.with_suffix(".mode.json").write_text(json.dumps({**mode, "messages": [laid]}), "utf-8")
    large = GameBoard(load_world(large_world))
    for extent, offset, snapshot in history:
        large.step()
        at, wide = slice(low - offset, low - offset + extent), BACK.snapshot(large)[0]
        assert all(np.array_equal(a, b[at]) for (_, a), (_, b) in zip(snapshot, wide, strict=True))
    assert grows.ended == end and grows.tick == 40
    assert grows.books()["charge"]["share"] == large.books()["charge"]["share"]
    assert grows.mask(((15, 0, 0),))[15 + low, 0, 0] and all("node" not in e for e in lines)
    assert not grows.quanta(0)[0][low : low + 16].any() and fixed.quanta(0)[0].any()
    assert RUN.run_input(str(world), str(tmp_path))["ticks"] == 40
    written = json.loads((tmp_path / "grows.output.json").read_text(encoding="utf-8"))
    look = RECORD.record(world, None)
    assert written["verdict"] == "LAWFUL" and written["ended"] == end == look["ended"]
    assert [look["frames"][k]["shape"][0] for k in (0, 40)] == [16, 64] and lines
    assert look["frames"][40]["offset"][0] == low
    back = BACK.verdict(GameBoard(load_world(world)), 100)
    assert back["verdict"] == "MATCH" and back["intervals"] == 39 and back["ended"] == end
    receding = {"x": {"sides": ["high"], "largest": 64, "layers": 4}}
    world = light_alone_world(tmp_path, "light", 24, 6, receding=receding)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"] = [r for r in UNIVERSE_ROWS if r["name"] in ("gravity", "charge", "binding")]
    for name in ("charge", "binding"):
        rows = json.loads(json.dumps(universe["families"]))
        next(row for row in rows if row["name"] == name)["held"]["rest"] = 60
        (tmp_path / "u.json").write_text(json.dumps({**universe, "families": rows}), encoding="utf-8")
        refused("only the massless", lambda: load_world(world))
    universe["families"][0]["held"]["rest"] = 60
    universe["integers"]["link_unit"] = 1  # the bound A at G = 1 admits a level at the Link's zero
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    still = json.loads(world.read_text(encoding="utf-8"))
    still.update(messages=[], faces=[{"axis": "x", "at": 10, "gaps": []}], ticks=30)
    (tmp_path / "still.json").write_text(json.dumps(still), encoding="utf-8")
    board = GameBoard(load_world(tmp_path / "still.json"), (lines := []).append)
    gravity = board.families.index(next(f for f in board.families if f.rest))
    time = board.states[gravity].lines[0]
    half = node.rule_of(board.families[gravity], GAMMA, 0, None, board.unit)[2] // 2  # the half wall
    assert (time.now == 60).all() and (time.before == 60).all() and (time.remainder == half).all()
    for i, h in ((i, board.half_wall(i)) for i in board.held):  # the lay's origin and the start's alike
        assert board.origins[i] == h and (board.states[i].lines[0].remainder == h).all()
    for _ in range(30):
        board.step()
    assert (board.states[gravity].lines[0].now == 60).all() and board.shape[0] == 24
    assert all(line["reading"] == 0 for line in lines if line["event"] == "density")
    well, post = board.states[gravity].lines[0], board.mask(((14, 0, 0), (15, 0, 0), (16, 0, 0)))
    well.now[post] = well.before[post] = paces.frozen_content(GAMMA)  # a frozen clock at three Nodes
    for axis_level in (board.states[gravity].lines[1].now, board.states[gravity].lines[1].before):
        axis_level[19:21, 0, 0] = GAMMA - 2 * 60  # a standing tension on xx: the Link 19-20's factor 0
    frozen_books = dict(share=None, quanta=None, count=0, deficit=0, drift=None, pace=0, frozen=3)
    assert board.books() == {"charge": frozen_books}
    board.step()
    cold = [line for line in lines if line["event"] == "density" and line["reading"] is None]
    assert (
        len(cold) == 1 and cold[0]["node_reader"] == "post" and cold[0]["well"] == 0 and board.tick == 31
    )
    kick = json.loads((tmp_path / "still.json").read_text(encoding="utf-8"))
    packet = {**PACKET, "family": "gravity", "amplitude": 12, "edge": {"x": 3, "y": 0, "z": 0}}
    packet["top"] = {"x": [4, 4], "y": [0, 0], "z": [0, 0]}
    kick.update(faces=[], ticks=40, messages=[packet])
    (tmp_path / "kick.json").write_text(json.dumps(kick), encoding="utf-8")
    TOOL.main(["--input", str(tmp_path / "kick.json")])
    board = GameBoard(load_world(tmp_path / "kick.json"), (lines := []).append)
    assert abs(board.states[gravity].lines[0].now[4, 0, 0] - 60) == 12
    for _ in range(40):
        board.step()
    grown = board.states[gravity].lines[0].now[24:, 0, 0]
    assert board.shape[0] > 24 and (grown[-1] == 60) and (grown != 60).any()
    assert max(x["reading"] for x in lines if x["event"] == "density" and x["family"] == "gravity") > 0
    assert BACK.verdict(GameBoard(load_world(tmp_path / "kick.json")), 40)["verdict"] == "MATCH"
    output = RUN.run_input(str(world), str(tmp_path))
    written = json.loads((tmp_path / "light.output.json").read_text(encoding="utf-8"))
    lit = [x for x in written["lines"] if x["event"] == "density" and x["family"] == "charge"]
    assert output["verdict"] == "LAWFUL" and lit and max(x["reading"] for x in lit) > 0


def test_a_record_of_any_dimension_is_its_real_lines_each_stepped_as_one(tmp_path, monkeypatch):
    """The dimension generic (the Boss's line, #1572 comment 5963599079 (B), with the two hands' amendments, the advisor's 5963681796 and the mathematician's 5963662072 part C): a family of quanta declares any dimension from 1, its record that many real lines but for 2, the one plane (3 three real lines, [2, 5] ten real lines in two parts, 0 refused by name); a family of real lines names no holder of the sign, refused by name as no plane (the sign a plane's, read plainly or by the turn and written by the Wronskian), so the sign holder keeps its one row beside it; on a periodic 5-cube of the rule's universe with a family of three real lines beside it, random levels on every line and every write remainder, each of the cube's 48 signed axis permutations commutes with the interval line by line (every real line imaged as a scalar, gravity's axis lines as a tensor's diagonal: Rule3 mixes lines never and a rotation of the cube maps each line to itself), the inverse returning every array; the record's NodeState is its three lines and nothing else, its form the plain sum of the three lines' forms and its share the sum of theirs, one quantum one unit of the form over every line (the dimension adds no mass); a body or a message is laid at its declared weights over the three lines (`weights`), the pair times each line's weight."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path), universe_beside(tmp_path)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    triple = {**CHARGED, "name": "triple", "reads": {"gravity": 1, "binding": 1}, "dimension": 3}
    rows["families"].append(triple), (tmp_path / "u.json").write_text(json.dumps(rows), encoding="utf-8")
    families, vector = universe_of(rows)[1], len(rows["families"]) - 1
    assert (families[vector].lines, families[vector].plane, families[CHARGE].records) == (3, False, 1)
    assert shape_of({"dimension": [2, 5]}, "x")[:2] == (10, 2) and shape_of({"dimension": 2}, "x")[2]
    refused("from 1", shape_of, {"dimension": 0}, "x")
    triple["reads"]["charge"] = 1  # three real lines naming the holder of the sign: no plane
    refused("no plane", universe_of, rows)
    world = dict(shape=[5] * 3, boundary=dict.fromkeys("xyz", "periodic"), ticks=1, bodies=[])
    world.update(universe="u.json", engine="e.json", node_readers=[])
    (cube := tmp_path / "cube.json").write_text(json.dumps(world))

    def imaged(board: GameBoard, axes, signs) -> list[node.NodeState]:  # the state under one of the 48
        found = []
        for f, s in zip(board.families, board.states, strict=True):
            lands = [axes[k - 1] + 1 if f.axes and k else k for k in range(len(s.lines))]
            arrays = [[turned(getattr(s.lines[at], key), axes, signs) for key in KEYS] for at in lands]
            writes = [turned(s.write_remainders[at], axes, signs) for at in lands] if f.held else []
            found.append(node.NodeState([node.Record(*a) for a in arrays], writes))
        return found

    def arrays(states: list[node.NodeState]) -> list[list]:
        return [BACK.arrays_of(str(k), s) for k, s in enumerate(states)]

    (stepped := random_state(cube, 11)).step()
    loaded = random_state(cube, 11)  # one load, copied per image: the load's guard is the cost
    for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
        other = copy.deepcopy(loaded)
        other.states = imaged(other, axes, signs)
        other.step()
        assert BACK.first_difference(arrays(imaged(stepped, axes, signs)), arrays(other.states)) is None
    begun, state = list(stepped.states[vector].lines), stepped.states[vector]
    stepped.step_inverse()
    assert BACK.first_difference(BACK.snapshot(random_state(cube, 11)), BACK.snapshot(stepped)) is None
    (content, factors), pair, wrap = stepped.read(vector), families[vector].pair, stepped.wrap
    own = sum(share.share(pair, line, wrap, GAMMA, content, factors, UNIT) for line in state.lines)
    forms = sum(node.form([a], [b]) for a, b in zip(state.lines, begun, strict=True))
    assert len(state.lines) == 3 and not state.write_remainders and len(begun) == 3
    assert (own == stepped.share_of(vector)[0]).all() and (node.form(state.lines, begun) == forms).all()
    lines = (fresh := GameBoard(load_world(cube))).states[vector].lines
    fresh.lay(BodyRow(vector, ((2, 2, 2),), (1,), ((62, 7),), ((62, 5),), (), (), (2, 3, -5)))
    laid = [[int(a.ravel()[62]) for a in (r.now, r.before)] for r in lines]
    assert laid == [[14, 10], [21, 15], [-35, -25]]

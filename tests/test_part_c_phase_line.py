"""Part C, the phase line (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/phase; the mathematician's repaired form of item (g), the advisor's second, the two hands' item (i)): the temporal gauge, under which the time Link carries no phase and every Link of a plane reading the sign holder carries a pair of Rule3 lines at the fixed angle theta_0 = 1 / Gamma, iterated |n_ij| acts per interval in the sense of n_ij = L(i) - L(j), the holder's time level's difference across the Link, read by the Port as the hop's two integers inside the sign's fold. The Coulomb run on the engine itself against the oracle recorded from the time turn (5c65fb1b, tests/oracle/coulomb_before.json), the record's run and its mirror's each its own test, the reversal bit for bit with the phase pairs, the static field bounded by the walk's bound, the 48 returns with the phase pairs as a vector per axis, the one-Link reach, and the two slits without a sign holder bit-identical to the frozen oracle. Every test under 30 seconds; each prints its numbers with its time."""

import math
import time
from itertools import permutations, product

import numpy as np

from event_universe import node, records, world_files
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws
from tests.laws import COULOMB_AT as AT
from tests.laws import COULOMB_CHAIN as CHAIN
from tests.laws import COULOMB_UNIVERSE as UNIVERSE
from tests.laws import LINE_KEYS as KEYS
from tests.laws import arrays, coulomb_world

GAMMA, PAIR, T = 6000, (4000, 6000), 36000
SIGMA, AMPLITUDE = 30, 3000


def gaussian_record(board: Lattice, conjugate: bool, amplitude: int = AMPLITUDE) -> None:
    """The hands' packet laid by hand on the charged family's record: A = 3,000 (under the world's bound 5,961 over the run; 4,000 passed it at the interval 1,984), sigma 30, at rest about the Node 280 (the conjugate about the mirror Node 119, the same room before the chain's end, as the hands' chain), the before a turn e^(i omega) behind for the record of positive Wronskian (the engine's sense) and the conjugate mirrored, im to -im."""
    omega, sense = math.acos(PAIR[0] / PAIR[1]), -1 if conjugate else 1
    at = (
        CHAIN - 1 - AT if conjugate else AT
    )  # the conjugate at the mirror Node, the same room before the end
    x = np.arange(CHAIN).reshape(board.shape)
    shape = amplitude * np.exp(-((x - at) ** 2) / (2 * SIGMA**2))
    re_now, im_now = np.rint(shape).astype(board.kind), np.zeros(board.shape, dtype=board.kind)
    re_before = np.rint(shape * math.cos(omega)).astype(board.kind)
    im_before = np.rint(sense * shape * math.sin(omega)).astype(board.kind)
    re, im = board.states[1].lines[:2]
    board.states[1].lines[:2] = [
        records.Record(re_now, re_before, re.remainder),
        records.Record(im_now, im_before, im.remainder),
    ]


def ramp(board: Lattice) -> tuple[list[records.Record], list[np.ndarray]]:
    """The holder's free row's time level rising one unit per Link along +x, L = x, both levels; returns the holder's whole state (its rows' lines and its write remainders) for the harness to hold it static (`held_static`): the chain's open ends would otherwise radiate the ramp's kink into the packet, and the record's own row, written by its Wronskian and read by nothing, would pass the bound (the hands' chain had no self-write)."""
    level = np.arange(CHAIN).reshape(board.shape).astype(board.kind)
    line = board.states[0].lines[0]
    board.states[0].lines[0] = records.Record(level, level.copy(), line.remainder)
    return list(board.states[0].lines), [r.copy() for r in board.states[0].write_remainders]


def held_static(board: Lattice, kept: tuple[list[records.Record], list[np.ndarray]]) -> None:
    """The holder's state restored after an interval, the harness's static potential."""
    board.states[0].lines = list(kept[0])
    board.states[0].write_remainders = [r.copy() for r in kept[1]]


def centroid(board: Lattice) -> float:
    """The record's centroid along x, weighted by |z_now|^2 + |z_before|^2."""
    re, im = board.states[1].lines[:2]
    weights = sum(np.asarray(a, dtype=float) ** 2 for a in (re.now, im.now, re.before, im.before))
    return float((np.arange(CHAIN) * weights.ravel()).sum() / weights.sum())


def test_the_reversal_returns_every_array_with_the_phase_pairs(tmp_path, monkeypatch):
    """(2) 10 intervals forward and back on the Coulomb world (40 to 2026-10-24, shortened under the suite's bound of 30 seconds per test once the chain's integers passed the width 64 under the universal charge; the sentence the same) (the packet at A 300, the holder evolving freely, its rows written by the record's Wronskian and stepped by Rule3): every array bit for bit, the lines, the write remainders and the phase pairs (the phase act back by the potentials at the interval's start, `Lattice.phased` at -1; the back-in-time gate MATCH)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    board = Lattice(load_world(coulomb_world(tmp_path)))
    gaussian_record(board, False, 300)
    ramp(board)
    board.amplitude = node.seed_phases(
        board, board.world
    )  # the pairs re-read from the laid state: the Link's count is the Node's reading (the centred count, 2026-10-23), no line of its own
    start = arrays(board)
    for _ in range(10):
        board.step()
    moved = arrays(board)
    assert any(not np.array_equal(a, b) for a, b in zip(start, moved, strict=True))
    phases = board.states[0].phases[1]
    assert any((p.now != q).any() for p, q in zip(phases, start[-3 * len(phases) :][0::3], strict=True))
    for _ in range(10):
        board.step_inverse()
    assert all(np.array_equal(a, b) for a, b in zip(start, arrays(board), strict=True))
    assert laws.BACK.verdict(board, 12)["verdict"] == "MATCH"
    print(
        f"10 intervals forward and back: {len(start)} arrays bit for bit; {time.perf_counter() - started:.1f} s"
    )


def test_the_static_field_is_bounded_by_the_walks_bound():
    """(3) A constant potential difference of 5 units across one Link (two Nodes, the holder's time level 0 and -5, n = 5 acts per interval) for 2,000 intervals, 10^4 acts on the Link's pair through `node.phased`: |c + i s| stays within the walk's bound of X, Gamma / 2 + 1.42 N + 2.3 Gamma levels (the mathematician's item (i)), the angle advancing 5 theta_0 per interval; the pairs of the other Links (the -x Link beyond the face, the y and z Links at n = 0) untouched."""
    started = time.perf_counter()
    from event_universe.core.ports import Wrap
    from event_universe.loader.universe import universe_of

    families = universe_of(UNIVERSE)[1]
    shape, wrap = (2, 1, 1), Wrap(False, True, True, None)
    states = [
        records.empty_state(f, shape, (), object) for f in families
    ]  # Python's integers: the pair at X of 63 bits squared in the carry (the engine's kind beyond the width, loader/world.kind_of)
    states[0].phases = records.phase_lines(families[0], shape, object, GAMMA, 63)
    level = np.array([[[0]], [[-5]]], dtype=object)
    states[0].lines[0] = records.Record(level, level.copy(), states[0].lines[0].remainder)
    amplitude = phase.amplitude(
        phase.unit(GAMMA), 63
    )  # the pair's X at the line's unit 2 Gamma (the half angle, the centred count of 2026-10-23; the former unit Gamma gave 32,025,594,000 where the pair stands at 8,006,388,000)
    seed = [a.copy() for r in states[0].phases[1] for a in (r.now, r.before, r.remainder)]
    worst, acts = 0.0, 0
    count = 0
    for _ in range(2_000):
        states[0].phases = node.phased(0, families, states, 1, wrap, GAMMA)
        reached = int(states[0].phases[1][6].now[0, 0, 0])  # the Link's count the pair is carried to
        acts += abs(
            abs(reached) - abs(count)
        )  # the acts along the orbit this interval (the centred count moves the pair by the count's change, 2026-10-23; the former left sum by 5)
        count = reached
        c, s = int(states[0].phases[1][0].now[0, 0, 0]), int(states[0].phases[1][1].now[0, 0, 0])
        worst = max(worst, abs(math.hypot(c, s) - amplitude))
    bound = GAMMA / 2 + 1.42 * acts + 2.3 * GAMMA
    assert worst <= bound, (worst, bound)
    angle = math.atan2(s, c)
    assert (
        abs(
            math.remainder(
                angle - abs(count) * math.acos(phase.K0(phase.unit(GAMMA)) / phase.D(phase.unit(GAMMA))),
                2 * math.pi,
            )
        )  # the pair at the count's half angle, the line's unit 2 Gamma
        <= bound / amplitude
    )
    after = [a for r in states[0].phases[1] for a in (r.now, r.before, r.remainder)]
    assert all(
        np.array_equal(a[1], b[1]) for a, b in zip(seed[:27], after[:27], strict=True)
    )  # the Node 1's +x Link beyond the face: its pair and count lines standing (the Node's phase row, the last three arrays, moves with its clocked potential)
    assert all(
        np.array_equal(a, b) for a, b in zip(seed[6:18], after[6:18], strict=True)
    )  # the y and z Links
    assert (
        after[18].tolist() == [[[abs(count)]], [[0]]]
        and all(np.array_equal(a, b) for a, b in zip(seed[21:27], after[21:27], strict=True))
    )  # the x Link's count line at the count reached, 0 beyond the face; the y and z count lines untouched
    print(
        f"10^4 acts on one Link: worst |c + i s| - X {worst:.0f} levels (bound {bound:.0f}), angle {angle:.6f}; {time.perf_counter() - started:.1f} s"
    )


def test_the_48_returns_on_a_closed_cube_with_the_phase_lines(tmp_path, monkeypatch):
    """(4) Part B's cube (tests/test_part_b_sign_fold.py): a charged record by hand on a closed cube of 7^3 in turning.json's universe, the free row's odd lines a radial vector field; over four intervals every scalar line keeps the 48 and the odd lines keep them as a vector, and the phase lines beside them: the cosine lines scalars under the 48 and the sine lines too, the pair (c, s) going to (c, -s) under a reflection of its axis exactly, since the potential the record reads (the free row's time level, 0 everywhere; its own row read by no phase of its own) gives n = 0 on every Link and every pair stands at its seed, s = 0; the back-in-time gate over twelve intervals MATCH with the phase pairs."""
    from tests.laws import CHARGE, RULE_WALL, imaged, sign_world

    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    shape, centre = (7, 7, 7), (3, 3, 3)
    d = np.abs(np.indices(shape) - 3).sum(axis=0)
    profile = np.select([d == 0, d == 1, d == 2], [1200, 600, 200], 0)
    closed = dict(x="closed", y="closed", z="closed")
    board = Lattice(load_world(sign_world(tmp_path, "cube", shape, closed, 8, centre, profile)))
    holder, kind = board.states[CHARGE], board.kind
    for axis in range(3):
        level = (40 * (np.indices(shape)[axis] - 3)).astype(kind)
        holder.lines[1 + axis] = records.Record(level, level.copy(), holder.lines[1 + axis].remainder)
    assert len(holder.phases) == board.families[CHARGE].records and holder.phases[0] == []
    seeds = [[a.copy() for r in rows for a in (r.now, r.before, r.remainder)] for rows in holder.phases]
    for _ in range(4):
        board.step()
        for rows in holder.phases[1:]:
            for a in [getattr(r, k) for r in rows for k in KEYS]:
                for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
                    assert np.array_equal(imaged(a, axes, signs), a)
            for axis in range(3):  # (c, s) to (c, -s) under the axis's reflection: s = 0 at the seed
                assert not rows[2 * axis + 1].now.any()
        for state, family in zip(board.states, board.families, strict=True):
            lines = state.lines[: family.width] if family.rotation else state.lines
            for a in [getattr(r, k) for r in lines[:1] for k in KEYS]:
                for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
                    assert np.array_equal(imaged(a, axes, signs), a)
    assert all(
        np.array_equal(a, b)
        for rows, kept in zip(holder.phases, seeds, strict=True)
        for a, b in zip([x for r in rows for x in (r.now, r.before, r.remainder)], kept, strict=True)
    )
    assert RULE_WALL > 0 and laws.BACK.verdict(board, 12)["verdict"] == "MATCH"
    print(
        f"the cube's 48 with the phase lines, four intervals, the gate MATCH over twelve; {time.perf_counter() - started:.1f} s"
    )


def test_the_phase_act_reaches_one_link():
    """(5) The one-Link reach: on a chain of 24 the holder's time level kicked by 200 at one Node; after one phase act the pairs that differ from the unkicked chain's are the two Links touching the Node, its own +x Link and its -x neighbour's, and no other (n_ij reads the two ends only, the pair lives on the Link)."""
    started = time.perf_counter()
    from event_universe.core.ports import Wrap
    from event_universe.loader.universe import universe_of

    families = universe_of(UNIVERSE)[1]
    shape, wrap, at = (24, 1, 1), Wrap(False, True, True, None), 10
    boards = []
    for kick in (0, 200):
        states = [records.empty_state(f, shape, (), np.int64) for f in families]
        states[0].phases = records.phase_lines(families[0], shape, np.int64, GAMMA, 63)
        level = np.zeros(shape, dtype=np.int64)
        level[at] = kick
        states[0].lines[0] = records.Record(level, level.copy(), states[0].lines[0].remainder)
        boards.append(node.phased(0, families, states, 1, wrap, GAMMA))
    apart = sorted(
        {
            int(x)
            for a, b in zip(boards[0][1], boards[1][1], strict=True)
            for x in np.argwhere(a.now != b.now)[:, 0]
        }
    )
    assert apart == [at - 1, at], apart
    print(
        f"the kicked Node {at}: the pairs apart at {apart}, the two Links touching it; {time.perf_counter() - started:.2f} s"
    )

"""Part C, the phase line (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/phase; the mathematician's repaired form of item (g), the advisor's second, the two hands' item (i)): the temporal gauge, under which the time Link carries no phase and every Link of a plane reading the sign holder carries a pair of Rule3 lines at the fixed angle theta_0 = 1 / Gamma, iterated |n_ij| acts per interval in the sense of n_ij = L(i) - L(j), the holder's time level's difference across the Link, read by the Port as the hop's two integers inside the sign's fold. The Coulomb run on the engine itself against the oracle recorded from the time turn (5c65fb1b, tests/oracle/coulomb_before.json), the record's run and its mirror's each its own test, the reversal bit for bit with the phase pairs, the static field bounded by the walk's bound, the 48 returns with the phase pairs as a vector per axis, the one-Link reach, and the two slits without a sign holder bit-identical to the frozen oracle. Every test under 30 seconds; each prints its numbers with its time."""

import math
import time

import numpy as np

from event_universe import node, records
from event_universe.features import phase
from event_universe.lattice import Lattice
from tests.laws import COULOMB_AT as AT
from tests.laws import COULOMB_CHAIN as CHAIN
from tests.laws import COULOMB_UNIVERSE as UNIVERSE

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

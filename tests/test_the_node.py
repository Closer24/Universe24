"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand on arrays, the share and the well as readings, the complement remainders of a mirrored line, the held write's walls at the doubled wall; and the tension as Rule3's own conservation of the current on a periodic cube at the one universe file's matter pair (examples/events/universe24), the stress reading the Links' (the owner's rule of 2026-10-24: the law's sentences at one Node, generic, no world but the bare torus)."""

import json

import numpy as np

from event_universe import flux, node, readings, records, share
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, mass, rule3
from event_universe.loader.derived import HeldWrite, family_rules, held_write_of
from event_universe.loader.universe import universe_of
from tests.laws import real_rows
from event_universe.loader.universe import SIGN, VOLUME
from tests.laws_universe import SMALL

WRAP, HERE, KEYS = Wrap(True, True, True), (1, 1, 1), ("now", "before", "remainder")
ROWS = ("held", (4, 4), 4, 7), ("gapped", (3, 4), 1, 7), ("quanta", (5, 7), 1, None)
BOX = (slice(1, -1),) * 3  # the inner Nodes of an array padded by one Node on every side
HELD, GAPPED, QUANTA = family_rules(real_rows(*ROWS))
WRITE = held_write_of((HELD, GAPPED, QUANTA), 0, 64)  # the massless row's one write per part at T = 64
INTEGERS, FAMILIES = universe_of(SMALL)  # the tests' small universe, den 1,021 with its two points
UNIT = INTEGERS["link_unit"]  # the Link's unit G of the tests' universe
NAMES = [family.name for family in FAMILIES]
GRAVITY, CHARGE = NAMES.index(VOLUME), NAMES.index(SIGN)
MATTER = next(i for i, f in enumerate(FAMILIES) if f.plane)  # a point of den's circle, a gapped pair for the rule's identities
GAMMA, T = INTEGERS["node_clock"], INTEGERS["quantum_action"]
WALLS = [held_write_of(FAMILIES, i, T).walls if f.held else () for i, f in enumerate(FAMILIES)]


def by_hand(a: np.ndarray, node: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(int(np.roll(a, -side, axis)[node]) for axis in range(3) for side in (1, -1))


def test_one_nodes_acts_are_rule3_called_by_hand():
    """The complement remainders (HIGHLIGHTS.md, the mathematician's 166 with the advisor's second hand): on a chain of 41 at [2, 3] and Gamma 1,000 an odd line mirrored about the centre with random levels within 1,000 and random remainders, the image's remainder the ones' complement w - 1 - r, steps mirrored to the bit, levels and remainders, over 200 intervals of Rule3 (floor((w - 1 - u) / w) = -floor(u / w) for every integer, checked over small walls), and the write's origins carry the complement of the half wall at a signed line's image Nodes (`records.write_origins`, 4 against 5 at the wall 10). (a) On random NodeStates of a periodic board of 3^3: the levels' step, the share and its reading in quanta and the well (a reading) at one Node equal Rule3 called by hand on that Node's integers (each act's direction -1 is the feature tests' and the back-in-time gate's; the one write per held part by hand, with its weights, in tests/test_the_features.py); a held row with a gap reads the same rule at its own pair, the plain rule's reads num, self coefficient 0 and wall 3 den (the generic test of the two rows: no name and no branch); the write's walls are the rows' own, E_s T and E_s x 3 den T with the sources' den (their least common multiple where they differ, each tension times the multiple over its own den), the remainders' origin half the wall. By hand beside the acts: the share is the frame's (ALGEBRA.md, The booking is the frame's, 2026-10-23): twice the plain term, the form's Node term less now x the six reads x the neighbours' before, less the Links' products R_ij (before_i - before_j)(now_i + now_j), over 4 p^2, the six paces one with no tension (the plain term over 2 p^2, node_term div (2 p^2) - num now S_6(before), the share to 2026-10-23, kept by name); the well, a reading, (now^2 - next x before) div T with no remainder kept; a gapped row at the content 0 reads 2 Gamma^2 times (3,) x 6, 0, 12 at [3, 4]; the walls E_s T and E_s x 3 den T (den 7), the origins half the wall, two den sharing their lcm."""
    draw, shape = np.random.default_rng(5), (3, 3, 3)
    for _ in range(20):
        levels = records.Record(*draw.integers(-900, 900, (2, *shape)), draw.integers(0, 50, shape))
        content = int(draw.integers(-40, 40))
        after = flux.step_line(levels, node.rule_of(QUANTA, 100, content), WRAP)
        clock, pace = paces.node_paces(100, content)
        reads, self_coefficient, wall = coefficients(5, 7, 100, clock, pace)
        arrived, here = by_hand(levels.now, HERE), tuple(int(getattr(levels, k)[HERE]) for k in KEYS)
        fluxes = sum(
            read * (m - here[0]) for read, m in zip(reads, arrived, strict=True)
        )  # the Links' sum by hand
        expected = rule3(fluxes, mass(5, 7, clock), wall, *here)
        assert (int(after.now[HERE]), int(after.remainder[HERE])) == expected
        wall_c, now_here, before_here = 3 * 7 * 64, int(after.now[HERE]), int(after.before[HERE])
        node_term = wall * (now_here**2 + before_here**2) - self_coefficient * now_here * before_here
        arrived_now, arrived_before = by_hand(after.now, HERE), by_hand(after.before, HERE)
        plain = node_term - now_here * sum(r * b for r, b in zip(reads, arrived_before, strict=True))
        links = sum(  # the Links' terms shared half and half between a Link's two ends
            r * (before_here - b) * (now_here + n)
            for r, n, b in zip(reads, arrived_now, arrived_before, strict=True)
        )
        share_here = (2 * plain - links) // (4 * pace**2)  # the plain term over 2 p^2 to 2026-10-23
        read = share.family_share(QUANTA, (after,), WRAP, 100, content)
        quanta_here = int(share.quanta_of(read, wall_c, np.int64)[HERE])
        assert int(read[HERE]) == share_here and quanta_here == (share_here + wall_c // 2) // wall_c
        form = here[0] ** 2 - int(after.now[HERE]) * here[1]
        assert int(records.well(records.form([levels], [after]), 64)[HERE]) == form // 64
        assert node.rule_of(GAPPED, 100, 0) == ((3 * 20_000,) * 6, 0, 12 * 20_000, 6 * 20_000)
    assert WRITE.walls == (7 * 64,) + (2 * 7 * 3 * 7 * 64,) * 3 and WRITE.factors == {
        2: 1
    }  # the tension lines at the doubled wall, the stress the Links' (2026-10-23; 7 x 3 x 7 x 64 before)
    origins = [int(a[0, 0, 0]) for a in records.write_origins(WRITE.walls, (1, 1, 1), np.int64)]
    assert origins == [wall // 2 for wall in WRITE.walls]
    rows = ("row", (1, 1), 4, 5), ("a", (1, 4), 1, None), ("b", (5, 6), 1, None)
    mixed = family_rules(real_rows(*rows))
    assert held_write_of(mixed, 0, 10) == HeldWrite(
        (50, 3600, 3600, 3600), {1: 3, 2: 2}
    )  # the tension lines' doubled wall (The stress is the Links', 2026-10-23; 1800 before)
    rng, (reads, _s, w) = np.random.default_rng(3), coefficients(2, 3, 1000, 1000, 1000)
    gap, chain = np.zeros((1, 1, 1), dtype=np.int64), Wrap(False, True, True)
    half = [rng.integers(-1000, 1000, (20, 1, 1)) for _ in range(3)]
    a, b = (np.concatenate([h, gap, -h[::-1]]) for h in half[:2])
    r = np.concatenate([half[2] % w, gap, records.complement(half[2] % w, w)[::-1]])
    for _ in range(200):  # the mirrored odd line steps mirrored to the bit with complement remainders
        b, a, r = (
            a,
            *(
                np.asarray(x)
                for x in rule3(flux.link_fluxes(a, reads, chain), mass(2, 3, 1000), w, a, b, r)
            ),
        )
        assert np.array_equal(a, -a[::-1]) and (r[:20] == records.complement(r, w)[::-1][:20]).all()
    assert all((w - 1 - u) // w == -(u // w) for u in range(-40, 40) for w in range(1, 9))


def difference(a: np.ndarray, axis: int) -> np.ndarray:
    return np.roll(a, -1, axis) - np.roll(a, 1, axis)


def test_the_tension_is_rule3s_own_conservation_of_the_current():
    """(ALGEBRA.md, The tension; The lattice momentum; The stress is the Links') On a periodic cube of 6^3 in the vacuum at the one universe's matter pair: w (P_a(t + 1) - P_a(t)) = SUM_b R_b (G_ab(i - b) - G_ab(i)) exactly once the remainders' term is added, P_a the record's current per axis and G_ab the flux of the a-momentum through the b-Link at one time; the engine's tension's part at every Node is the law's num (now_(i+a) - now_(i-a))^2, one Link's reach; the pattern [2, 0, -2, 0] along x gives 0, 16, 0, 16 at the weight 1 and 16 on every Link, the two ends' parts summed; a plane wave of the amplitude b at k = pi / 3 has the board sum 2 x 3 b^2 / 4 per Node on its axis and 0 on the two others, and a uniform record 0, exactly, no division."""
    draw, shape = np.random.default_rng(3), (6, 6, 6)
    matter = FAMILIES[MATTER]
    (read, *_), self_coefficient, wall = coefficients(*matter.pair, GAMMA, GAMMA, GAMMA, None, UNIT)
    zero = np.zeros(shape, dtype=object)
    start = records.Record(
        draw.integers(-3000, 3000, shape).astype(object),
        draw.integers(-3000, 3000, shape).astype(object),
        zero,
    )
    record = flux.step_line(start, node.rule_of(matter, GAMMA, 0, None, UNIT), WRAP)
    nxt, remainder, now, before = record.now, record.remainder, start.now, start.before

    def through(a: int, b: int) -> np.ndarray:
        return now * np.roll(difference(now, a), -1, b) - np.roll(now, -1, b) * difference(now, a)

    def momentum(x: np.ndarray, y: np.ndarray, a: int) -> np.ndarray:
        return x * difference(y, a) - y * difference(x, a)

    for a in range(3):
        left = wall * (momentum(nxt, now, a) - momentum(now, before, a))
        right = sum(read * (np.roll(through(a, b), 1, b) - through(a, b)) for b in range(3))
        assert np.array_equal(
            left, right - remainder * difference(now, a) + now * difference(remainder, a)
        )
    stresses = readings.stresses_of(matter.pair[0], [record], WRAP)
    by_hand = [matter.pair[0] * (np.roll(nxt, -1, a) - np.roll(nxt, 1, a)) ** 2 for a in range(3)]
    assert all(np.array_equal(t, h) for t, h in zip(stresses, by_hand, strict=True))
    four = np.array([2, 0, -2, 0]).reshape(
        4, 1, 1
    )  # the law's pattern: 0, 16, 0, 16 per Node, 16 per Link
    part = readings.stresses_of(1, [records.Record(four, four, 0 * four)], WRAP)[0]
    assert np.array_equal(part.reshape(-1), [0, 16, 0, 16]) and (part + np.roll(part, -1, 0) == 16).all()
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    tension = readings.stresses_of(1, [records.Record(wave, wave, 0 * wave)], WRAP)
    assert int(tension[0].sum()) == 2 * (3 * 2000 * 2000 // 4) * wave.size
    assert set(np.unique(tension[0]).tolist()) == {0, 9_000_000} and not tension[1].any()
    assert not tension[2].any()
    flat = [records.Record(0 * wave + 7, 0 * wave + 7, 0 * wave)]
    assert not any(t.any() for t in readings.stresses_of(1, flat, WRAP))

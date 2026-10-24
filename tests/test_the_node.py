"""The Node (ALGEBRA.md #the-interval): one Node's acts against Rule3 called by hand; the interval on a closed cube of one body, every level Rule3's, the count the record's share, the 48 symmetries kept in every part, the back-in-time gate MATCH over twelve intervals; on the chain light is born by the write: a breathing body of a plane writes a wave into the sign holder's own record, its share's total stays within the rounding, a static body's write stands still within the rounding, and the click at the end node_detector is the measurement; the whole run of the chain goes back in time, MATCH over 400 intervals with the rotating body and with the real one; the tension is Rule3's own conservation of the current; a receding face grows the lattice before the front, the run the larger chain's bit for bit, ending at the largest size and returning. The static body of the chain is one charged body of the sense +1 at the chain's centre Node with the taker on it: the two-body world, a like-sense body laid beside a neutral body's tail under the plain read, finds no fixed point in the generator (a 20-unit cycle of period 7 at the body's own edge), the rotating construction's open defect, the integer wander of the record-to-content map with the body's own charge level as a second source of its well; not a tie, and not widened."""

import math

import numpy as np

from event_universe import flux, node, readings, records, share
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, link_factor, mass, rule3
from event_universe.features.start import rest
from event_universe.loader.derived import HeldWrite, count_wall, family_rules, held_write_of
from event_universe.loader.universe import universe_of
from tests.laws import real_rows, universe_copy

WRAP, HERE, KEYS = Wrap(True, True, True), (1, 1, 1), ("now", "before", "remainder")
ROWS = ("held", (4, 4), 4, 7), ("gapped", (3, 4), 1, 7), ("quanta", (5, 7), 1, None)
BOX = (slice(1, -1),) * 3  # the inner Nodes of an array padded by one Node on every side
HELD, GAPPED, QUANTA = family_rules(real_rows(*ROWS))
WRITE = held_write_of((HELD, GAPPED, QUANTA), 0, 64)  # the massless row's one write per part at T = 64
UNIVERSE_ROWS = universe_copy()["families"]
INTEGERS, FAMILIES = universe_of(universe_copy())  # the tests' universe
UNIT = INTEGERS["link_unit"]  # the Link's unit G of the tests' universe
NAMES = [family.name for family in FAMILIES]
MATTER, GRAVITY, CHARGE = (NAMES.index(name) for name in ("matter", "gravity", "charge"))
GAMMA, T = INTEGERS["node_clock"], INTEGERS["quantum_action"]
PROFILE = [0, 0, 0, 200, 400, 600, 800, 1000, 1000, 800, 600, 400, 200, 0, 0, 0]
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
    """(d) On a periodic cube of 6^3 in the vacuum: w (P_a(t + 1) - P_a(t)) = SUM_b R_b (G_ab(i - b) - G_ab(i)) exactly once the remainders' term is added, P_a the count's line's current per axis and G_ab the flux of the a-momentum through the b-Link at one time; the engine's tension's part at every Node is the law's -num h_a(i) = -num (now_(i-a) now_(i+a) - now_i^2) (ALGEBRA.md #the-primitives, The tension: T_aa = -num (G_aa(i) + G_aa(i - a)) div 2), one Link's reach, the Link's booking G_aa(i) = h_a(i) + h_a(i + a) the sum of its two ends' parts; the documented pattern [2, 0, -2, 0] along x gives +4 at every Node at the weight 1 and +8 on every Link, the two ends' parts summed (the engine on main wrote -8, the stress itself); a plane wave of the amplitude b at the weight 1 at k = pi / 3 has the part +b^2 sin^2 k = 3 b^2 / 4 (-G_xx = 2 b^2 sin^2 k on the Link) and a uniform record 0, exactly, no division. (d) On a chain, a record of matter moving along +x (the envelope times the plane wave's character, a quarter turn per Link) sources the vacuum's row's tension on x above 0 (a plane wave's part +num b^2 sin^2 k: the stress deepens the content, light gravitates by its pressure) and none on y and z, so the +x Link's content is the Node's level twice with the mean of its two ends' xx parts, 0 beyond the face, one number per Link read the same from both ends, and the folded y Link's twice the Node's with the yy line 0; the same envelope at rest sources a tension of its own sign on x (the pressure of a standing record) and none on y and z; every family reads every holder of the content as its stepped time part, light as matter. (f) The local test of the two rows on a chain (x open) of sixteen ranges: the binding holder's pair from the file at its level weight, started at its rest under a static source of one quantum per interval at the centre Node (features/start; the row reading its own level at the Node's pace, Every row reads the content, a source small against Gamma so that the rest is Yukawa's outside a body), falls from the Node by e^(-kappa) per Link with cosh kappa = 3 den / num - 2 (ALGEBRA.md #the-well, the reach of a held family is its pair), the range R = 1 / kappa (20 Links at [2400, 2401]): the level at R / 2, R and 3 R / 2 Links within one unit of the centre's times e^(-r / R); stepped by Rule3 at the paces its own level gives it with the same source written each interval through the one wall E_s T (T in the numerator), the field is static within the rounding: the first interval moves no Node by more than two units and fewer than one Node in ten at all (the Nodes whose rounding residual passes the half wall, the remainder's origin), and over 200 intervals no Node drifts by more than the remainders' walk, two units per Node kicked plus the integer line's residual at the rest over the wall per interval (the nearest integers to the fine fixed point leave a residual below half the wall at every Node, which the remainder carries until a level kicks; those kicks are Rule3's own waves along the chain, and the fixed point is a pair, level and remainder); the source written each interval carries the write's factor at the row's own paces, as the rest carried it. The Node's own part of the tension is the law's -num h_a(i) = -num (now_(i-a) now_(i+a) - now_i^2)."""
    draw, shape = np.random.default_rng(3), (6, 6, 6)
    (read, *_), self_coefficient, wall = coefficients(4000, 6000, GAMMA, GAMMA, GAMMA)
    start = records.Record(*draw.integers(-3000, 3000, (2, *shape)), draw.integers(0, 1, shape))
    record = flux.step_line(start, node.rule_of(FAMILIES[MATTER], GAMMA, 0), WRAP)
    nxt, remainder = record.now.astype(object), record.remainder.astype(object)
    now, before = start.now.astype(object), start.before.astype(object)

    def through(a: int, b: int) -> np.ndarray:
        return now * np.roll(difference(now, a), -1, b) - np.roll(now, -1, b) * difference(now, a)

    def momentum(x: np.ndarray, y: np.ndarray, a: int) -> np.ndarray:
        return x * difference(y, a) - y * difference(x, a)

    for a in range(3):
        left = wall * (momentum(nxt, now, a) - momentum(now, before, a))
        right = sum(read * (np.roll(through(a, b), 1, b) - through(a, b)) for b in range(3))
        expected = right - remainder * difference(now, a) + now * difference(remainder, a)
        assert np.array_equal(left, expected)
    stresses, now = readings.stresses_of(FAMILIES[MATTER].pair[0], [record], WRAP), record.now
    by_hand_stress = [4000 * (np.roll(now, -1, a) - np.roll(now, 1, a)) ** 2 for a in range(3)]
    assert all(np.array_equal(t, h) for t, h in zip(stresses, by_hand_stress, strict=True))
    four = np.array([2, 0, -2, 0]).reshape(
        4, 1, 1
    )  # the law's pattern: 0, 16, 0, 16 per Node, 16 per Link
    part = readings.stresses_of(1, [records.Record(four, four, 0 * four)], WRAP)[0]
    assert np.array_equal(part.reshape(-1), [0, 16, 0, 16]) and (part + np.roll(part, -1, 0) == 16).all()
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    tension = readings.stresses_of(1, [records.Record(wave, wave, 0 * wave)], WRAP)
    assert (
        int(tension[0].sum()) == 2 * (3 * 2000 * 2000 // 4) * wave.size
    )  # the board sum the former's, doubled
    assert (
        set(np.unique(tension[0]).tolist()) == {0, 9_000_000}
        and not tension[1].any()
        and not tension[2].any()
    )
    flat = [records.Record(0 * wave + 7, 0 * wave + 7, 0 * wave)]
    assert not any(t.any() for t in readings.stresses_of(1, flat, WRAP))

    def chain_record(now_turn: tuple[int, ...], before_turn: tuple[int, ...]) -> records.Record:
        """A record on a chain: the envelope PROFILE times a character, (1, 0, -1, 0) at the step's level and its turn at the level before."""
        size, n = len(PROFILE), len(now_turn)
        levels = ([PROFILE[x] * turn[x % n] for x in range(size)] for turn in (now_turn, before_turn))
        return records.Record(
            *(np.array(level, dtype=np.int64).reshape(size, 1, 1) for level in levels), 0
        )

    shape, wrap, matter = (16, 1, 1), Wrap(False, True, True), FAMILIES[MATTER]
    for moving in (True, False):
        turns = ((1, 0, -1, 0), (0, -1, 0, 1)) if moving else ((1,), (1,))
        record, write = chain_record(*turns), held_write_of(FAMILIES, GRAVITY, T)
        wall = count_wall(matter, T)
        count = share.quanta_of(share.family_share(matter, (record,), wrap, GAMMA), wall, np.int64)
        stress = readings.stresses_of(matter.pair[0], [record], wrap)
        vacuum = {(i, 0): (GAMMA, (GAMMA, GAMMA, GAMMA)) for i in (CHARGE, MATTER)}
        found, walls, _weight = records.write_sources(
            GRAVITY, FAMILIES, {}, {(MATTER, 0): stress}, write, vacuum, GAMMA
        )
        carried = [  # the walls per Node under the carried factor, one number at the vacuum's rulers
            int(np.asarray(w, dtype=object).reshape(-1)[0]) for w in walls
        ]
        held = records.empty_state(FAMILIES[GRAVITY], shape, carried, object)
        written = node.held_write_at(held.lines, found, carried, held.write_remainders)
        (held.lines, held.write_remainders), xx = written, written[0][1].now
        assert not (moving and int(stress[0].min()) < 0) and bool((stress[0] != 0).any())
        for line in (
            1,
            2,
            3,
        ):  # the one write per tension line: the numerator over the wall, the remainder kept
            total = np.asarray(carried[line] // 2 + found[line], dtype=object)  # Python's integers
            assert np.array_equal(held.write_remainders[line], total % carried[line])
            assert np.array_equal(held.lines[line].now, total // carried[line])
        traceless = [np.asarray(found[line], dtype=object) for line in (1, 2, 3)]
        assert (
            np.array_equal(2 * traceless[1], -traceless[0])
            and np.array_equal(traceless[1], traceless[2])
        )  # the x stress s booked traceless, 2 s on the x line and -s on y and z (the stress's trace the time line's); at gravity's level weight 1 the lines gain levels here, where at rule.json's 1,000 to 2026-10-24 every numerator stayed within its wall and xx was 0
        assert not (stress[1].any() or stress[2].any())
        states = [
            records.empty_state(f, shape, w, np.int64) for f, w in zip(FAMILIES, WALLS, strict=True)
        ]
        states[GRAVITY] = held
        stepped = np.arange(16, dtype=np.int64).reshape(shape)  # the vacuum's row's stepped time part
        held.lines[0] = records.Record(stepped, stepped, records.zeros(shape, np.int64))
        content, factors = node.read(MATTER, FAMILIES, states, 1, wrap, GAMMA, UNIT)
        xx_ahead = np.pad(xx, ((0, 1), (0, 0), (0, 0)))[1:]  # the xx line through +x, 0 beyond the face
        assert np.array_equal(factors[0], link_factor(GAMMA, UNIT, (xx + xx_ahead + 1) // 2))
        assert np.array_equal(factors[0][:-1], factors[1][1:])  # one factor per Link, from both ends
        assert (factors[2] == UNIT * UNIT).all() and np.array_equal(content, stepped)
        contact = records.Record(
            count, count, records.zeros(shape, np.int64)
        )  # the binding holder's level
        states[NAMES.index("binding")].lines[0] = contact
        content, _factors = node.read(MATTER, FAMILIES, states, 1, wrap, GAMMA, UNIT)
        assert np.array_equal(content, stepped + count)  # every reader reads the rows as they stand
        light, _factors = node.read(CHARGE, FAMILIES, states, 1, wrap, GAMMA, UNIT)
        assert (
            light == 0
        )  # the holder of the sign reads none (the reads derived, 2026-10-24; stepped + count under rule.json's declared reads to that day)
    num, den = (binding := FAMILIES[NAMES.index("binding")]).pair
    reach = round(1 / (kappa := math.acosh(3 * den / num - 2)))
    assert binding.level_weight is not None and reach == 20
    shape, wrap = (16 * reach, 1, 1), Wrap(False, True, True)
    source, centre = records.zeros(shape, np.int64), 8 * reach
    source[centre], weight, wall = 1, binding.level_weight, node.rule_of(binding, GAMMA, 0)[2]
    kind = {"intervals": paces.COUNT_POWER, "own_weight": 1}
    field = rest(source, binding.pair, wrap, weight, 2**63 - 1, wall, GAMMA, **kind)
    away = (0, reach // 2, reach, 3 * reach // 2)
    at = [int(field.levels[centre + r, 0, 0]) for r in away]
    assert all(abs(at[i] - round(at[0] * math.exp(-kappa * r))) <= 1 for i, r in enumerate(away))
    walls = WALLS[NAMES.index("binding")]
    state, levels = records.empty_state(binding, shape, walls, np.int64), field.levels
    state.lines[0] = records.Record(levels.copy(), levels.copy(), np.full(shape, field.remainder))

    def scaled(now: np.ndarray) -> np.ndarray:  # the write per proper volume at the row's own paces
        clock, pace = paces.node_paces(GAMMA, now)
        return np.asarray(records.rulers_write_factor(source * T, (clock, (pace, pace, pace)), GAMMA, 2))

    reads, self_coefficient, rule_wall, _mass = node.rule_of(
        binding, GAMMA, levels
    )  # the integer line at rest
    numerator = sum(r * a for r, a in zip(reads, readings.ports(levels, wrap), strict=True))
    numerator = (numerator + self_coefficient * levels - 2 * rule_wall * levels).astype(object) * T
    residual = np.abs(numerator + scaled(levels).astype(object) * rule_wall).max() / (rule_wall * T)
    kicked, drift = 0, 0
    for interval in range(200):
        own = node.rule_of(binding, GAMMA, state.lines[0].now)  # the row reads its own level
        increment, state.lines[0] = (
            [
                scaled(state.lines[0].now),
                *([0] * (len(state.lines) - 1)),
            ],  # the time line's write; the three tension lines unsourced here (the binding holder carries its axis lines since 2026-10-24)
            flux.step_line(state.lines[0], own, wrap),
        )
        kept = state.write_remainders
        state.lines, state.write_remainders = node.held_write_at(state.lines, increment, walls, kept)
        moved = np.abs(state.lines[0].now - field.levels)
        if interval == 0:
            kicked = int((moved > 0).sum())
            assert int(moved.max()) <= 2 and 10 * kicked < shape[0], (int(moved.max()), kicked)
        drift = max(drift, int(moved.max()))
    assert drift <= 2 * kicked + math.ceil(200 * float(residual))  # the remainders' walk per interval

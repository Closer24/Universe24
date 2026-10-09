"""Part B, the sign's Link phase in the fold form (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the two hands' lines of 2026-10-09, the advisor's (a), (c) and (1), the mathematician's (a) and (L2)): the Link's turn by the sign holder's odd lines is the exact tangent half-angle triple rebooked in the Link's unit with one rounding per part, X^c even and X^s odd in the Link's level n, so that the pair read from the two ends is exact by direction and the count is conserved by Hermiticity; the odd lines' source is the two Links' Wronskian currents summed unhalved over the doubled wall; the time turn stays the one shear. Every test under 30 seconds."""

import json
import math
from fractions import Fraction
from itertools import permutations, product

import numpy as np

from event_universe import node, world_files
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features.rotation import link_wall
from event_universe.lattice import Lattice
from event_universe.loader.derived import held_write_of
from event_universe.loader.universe import universe_of
from event_universe.plane import link_levels, link_pairs, sign_pairs
from event_universe.world_files import input_digest, load_world
from tests import laws
from tests.laws import EVENTS, chain_body_world

GAMMA, PAIR, UNIT = 6000, (4000, 6000), 16
TURNING_FILE = EVENTS / "turning.json"
INTEGERS, TURNING = universe_of(json.loads(TURNING_FILE.read_text(encoding="utf-8")))
T, NAMES = INTEGERS["quantum_action"], [family.name for family in TURNING]
CHARGE, CHARGED = NAMES.index("charge"), NAMES.index("charged")
KEYS = ("now", "before", "remainder")
RULE_WALL = coefficients(*TURNING[CHARGE].pair, GAMMA, GAMMA, GAMMA, None, UNIT)[
    2
]  # w = 6 den Gamma^2 G^2
SINE = 4472  # isqrt(6000^2 - 4000^2): the matter pair's sin omega_0 times den


def sign_world(tmp_path, name, shape, boundary, intervals, centre, profile):  # type: ignore[no-untyped-def]
    """A world on turning.json's universe with one charged record by hand at the count 1 (the count-1 gate: the profile scaled to one quantum, 2 SUM L^2 sin omega_0 = T, as test_the_node lays it): the level now (L, 0) over `profile` and the level before the band's rest rotation in the sense +1, (L cos omega_0, L sin omega_0)."""
    (tmp_path / "u.json").write_bytes(TURNING_FILE.read_bytes())
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    values = [int(v) for v in np.asarray(profile).ravel()]
    scale = math.isqrt(
        T * PAIR[1] * 1000 * 1000 // (2 * SINE * sum(v * v for v in values))
    )  # one quantum
    levels = [v * scale // 1000 for v in values]  # 2 SUM L^2 sin omega_0 = T, the law's one quantum
    moving = dict(now=levels, before=[v * PAIR[0] // PAIR[1] for v in levels])
    moving.update(im_now=[0] * len(levels), im_before=[v * SINE // PAIR[1] for v in levels])
    body = {"family": "charged", "nodes": [{"node": list(centre), "count": 1}]}
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=intervals)
    world.update(universe="u.json", engine="e.json", node_detectors=[], bodies=[body])
    (path := tmp_path / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    mode = {"family": "charged", "pair": list(PAIR), "moving": moving}
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    return path


def arrays(board: Lattice) -> list[np.ndarray]:
    return [getattr(r, k).copy() for s in board.states for r in s.lines for k in KEYS] + [
        r.copy() for s in board.states for r in s.write_remainders
    ]


def imaged(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def test_the_sign_pair_is_even_and_odd_in_the_links_level():
    """(a) Over every Link level n in [-4 Gamma, 4 Gamma] at the vacuum's factor G^2: X^c(-n) = X^c(n) and X^s(-n) = -X^s(n) exactly, so the pair read from the Link's other end is the conjugate bit for bit; the pair's magnitude is X_ij = 2 num G^2 to one level, (X^c)^2 + (X^s)^2 within 2 X + 1 of X^2; X^c = X and X^s = 0 at n = 0; at n = 4 Gamma (the tangent half-angle 1, the guard's edge) the pair is (0, X), a quarter turn; and the two parts' sum never passes X sqrt 2 + 1, the bound's room (`derived.turned_room`)."""
    wall, unit = link_wall(GAMMA), UNIT * UNIT
    levels = np.arange(-wall, wall + 1, dtype=object)
    (even,), (odd,) = sign_pairs(PAIR, GAMMA, (unit,), (levels,))
    even, odd = np.asarray(even, dtype=object), np.asarray(odd, dtype=object)
    x = 2 * PAIR[0] * unit
    assert np.array_equal(even, even[::-1]) and np.array_equal(odd, -odd[::-1])
    assert (np.abs(even * even + odd * odd - x * x) <= 2 * x + 1).all()
    assert (even[wall], odd[wall]) == (x, 0) and (even[-1], odd[-1]) == (0, x)
    assert (even[0], odd[0]) == (0, -x) and (np.abs(even) + np.abs(odd)).max() <= x * 14143 // 10000 + 1


def test_the_48_returns_on_a_closed_cube_with_a_sign_holder(tmp_path, monkeypatch):
    """(vector, the cube's 48 under the fold) A charged record by hand on a closed cube of 7^3 in turning.json's universe, the sign holder's free row carrying a radial odd field L_a = 40 (x_a - 3) laid by hand, a vector under the 48 with its remainders at the half wall (the two's-complement mirror of ALGEBRA.md, The cube's symmetry): over four intervals every scalar line (the plane's two, every time line, the content holders' lines) keeps the 48 in every part, the odd lines keep them as a vector (L_a'(g x) = s_a L_a(x) in both levels, the remainders carried as (w - r) mod w where the axis is reversed), the sign's odd lines of the record's row are written by its current (their remainders leave the half wall), and the back-in-time gate over twelve intervals returns every array bit for bit, MATCH."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    shape, centre = (7, 7, 7), (3, 3, 3)
    d = np.abs(np.indices(shape) - 3).sum(axis=0)
    profile = np.select([d == 0, d == 1, d == 2], [1200, 600, 200], 0)
    closed = dict(x="closed", y="closed", z="closed")
    board = Lattice(load_world(sign_world(tmp_path, "cube", shape, closed, 8, centre, profile)))
    holder, kind = board.states[CHARGE], board.kind
    for axis in range(3):  # the free row's odd lines, a radial vector field, static in both levels
        level = (40 * (np.indices(shape)[axis] - 3)).astype(kind)
        holder.lines[1 + axis] = node.Record(level, level.copy(), holder.lines[1 + axis].remainder)
    for _ in range(4):
        board.step()
        for state, family in zip(board.states, board.families, strict=True):
            vector = family.rotation  # the sign holder's rows: a time line and three odd lines each
            for row in range(family.records if vector else 1):
                lines = (
                    state.lines[row * family.width : (row + 1) * family.width] if vector else state.lines
                )
                scalars, parts = (lines[:1], lines[1:]) if vector else (lines, [])
                writes = state.write_remainders[row * family.width :][: family.width]
                walls = board.walls(CHARGE)[row * family.width :][: family.width]
                for axes, signs in product(permutations(range(3)), product((1, -1), repeat=3)):
                    for a in [getattr(r, k) for r in scalars for k in KEYS] + writes[:1]:
                        assert np.array_equal(imaged(a, axes, signs), a)
                    for key in ("now", "before"):  # the odd lines as a vector
                        found = [getattr(r, key) for r in parts]
                        for a in range(len(parts)):
                            assert np.array_equal(
                                signs[a] * imaged(found[axes[a]], axes, signs), found[a]
                            )
                    for a in range(len(parts)):  # the odd lines' remainders, the two's-complement mirror
                        for r, w in ((parts[a].remainder, RULE_WALL), (writes[1 + a], walls[1 + a])):
                            source = [p.remainder for p in parts] if w == RULE_WALL else writes[1:]
                            image = imaged(source[axes[a]], axes, signs)
                            assert np.array_equal(image if signs[a] == 1 else (w - image) % w, r)
    halves = [
        w // 2 for w in board.walls(CHARGE)[5:8]
    ]  # the record's row's odd lines written: a current
    assert any((holder.write_remainders[5 + a] != halves[a]).any() for a in range(3))
    assert laws.BACK.verdict(board, 12)["verdict"] == "MATCH"


def test_back_in_time_on_the_turning_world_for_forty_intervals(tmp_path, monkeypatch):
    """(the back-in-time gate, (e)) A chain of 25 (x open) in turning.json's universe with one charged record by hand and the free row's x odd line laid as a bump, 40 intervals forward and 40 back by `step_inverse`: every line's two levels and remainder and every write remainder bit for bit, the Links' pairs recomputed from the held rows' levels at each interval's start and the time turn's shear undone."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    shape, open_x = (25, 1, 1), dict(x="open", y="periodic", z="periodic")
    profile = np.zeros(shape, dtype=int)
    profile[9:16, 0, 0] = [200, 600, 1000, 1200, 1000, 600, 200]
    board = Lattice(load_world(sign_world(tmp_path, "chain", shape, open_x, 80, (12, 0, 0), profile)))
    holder = board.states[CHARGE]
    bump = (300 * np.exp(-((np.arange(25) - 12) ** 2) / 18)).round().astype(board.kind).reshape(shape)
    holder.lines[1] = node.Record(bump, bump.copy(), holder.lines[1].remainder)
    begun = arrays(board)
    for _ in range(40):
        board.step()
    assert holder.lines[5].now.any()  # the record's own row's x odd line written by its current
    for _ in range(40):
        board.step_inverse()
    assert all(np.array_equal(a, b) for a, b in zip(begun, arrays(board), strict=True))


def test_the_wronskian_is_conserved_on_a_periodic_ring_under_the_folded_link_turn():
    """(the count, Theorem 3) On a ring of 64 in the vacuum's rule of the matter pair with the sign holder's x odd line at random levels within 3,000 per Node (|n| <= 6,000, inside the guard's 4 Gamma) and the time level 0, a random plane record within 5,000 stepped 200 intervals by `node.step_family` with the Links' pairs: the summed Wronskian W = SUM Im(conj(z_now) z_before) over the ring drifts by no more than Rule3's own floor, SUM over the intervals and the Nodes of |re| + |im| (one level per part per Node per interval); and in exact rationals on a ring of 9, the same pairs (the engine's integers) with the division exact, W is conserved exactly, the drift 0 over 200 intervals (K = D M Hermitian: X^c even and X^s odd in n)."""
    ring, draw = Wrap(True, True, True), np.random.default_rng(7)
    states = [node.empty_state(f, (64, 1, 1), (), np.int64) for f in TURNING]
    zero = np.zeros((64, 1, 1), dtype=np.int64)
    odd = [draw.integers(-3000, 3001, (64, 1, 1)), zero, zero]
    states[CHARGE].lines = [node.Record(zero, zero, zero)] + [node.Record(v, v, zero) for v in odd]
    lines = [node.Record(*draw.integers(-5000, 5001, (3, 64, 1, 1))) for _ in range(2)]
    lines = [node.Record(r.now, r.before, np.abs(r.remainder)) for r in lines]
    rule = coefficients(*PAIR, GAMMA, GAMMA, GAMMA)
    angles = node.turning(CHARGED, TURNING, states, 1, GAMMA)
    assert angles is not None
    pairs = link_pairs(PAIR, GAMMA, 0, (1,) * 6, None, link_levels(angles[1], ring))
    assert pairs is not None and any(np.asarray(p).any() for p in pairs[1])
    started = int(node.wronskian(lines, True).sum(dtype=object))
    floor = 0
    for _ in range(200):
        states[CHARGED].lines = lines
        floor += int((np.abs(lines[0].now) + np.abs(lines[1].now)).sum(dtype=object))
        lines = node.step_family(CHARGED, TURNING, states, rule, ring, GAMMA, pairs=pairs)[0]
    drift = int(node.wronskian(lines, True).sum(dtype=object)) - started
    assert started != 0 and abs(drift) <= floor, (drift, floor)
    print(f"the ring of 64: W {started}, the drift over 200 intervals {drift} within the floor {floor}")
    n = 9  # the rational mirror: the same step in Fractions, the pairs the engine's integers
    levels = draw.integers(-3000, 3001, n)
    links = link_levels((levels.reshape(n, 1, 1), zero[:n], zero[:n]), ring)
    even, odd_part = link_pairs(PAIR, GAMMA, 0, (1,) * 6, None, links)  # type: ignore[misc]
    even = [np.asarray(p, dtype=object).ravel() for p in even]
    odd_part = [np.asarray(p, dtype=object).ravel() for p in odd_part]
    reads, self_coefficient, wall = rule
    z = [complex(*draw.integers(-5000, 5001, 2)) for _ in range(n)]
    z = [(Fraction(int(v.real)), Fraction(int(v.imag))) for v in z]
    z_before = [(Fraction(int(a)), Fraction(int(b))) for a, b in draw.integers(-5000, 5001, (n, 2))]

    def wronskian(now, before):  # type: ignore[no-untyped-def]
        return sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(now, before, strict=True))

    first = wronskian(z, z_before)
    for _ in range(200):
        following = []
        for i in range(n):
            re = self_coefficient * z[i][0] - wall * z_before[i][0]
            im = self_coefficient * z[i][1] - wall * z_before[i][1]
            for port, j in enumerate(((i + 1) % n, (i - 1) % n, i, i, i, i)):
                c, s_ = int(even[port][i]), int(odd_part[port][i])
                re += c * z[j][0] - s_ * z[j][1]
                im += s_ * z[j][0] + c * z[j][1]
            following.append((re / wall, im / wall))
        z, z_before = following, z
    assert wronskian(z, z_before) == first != 0


def test_two_charges_of_opposite_sense_run_a_hundred_intervals(tmp_path, monkeypatch):
    """(a two-charge static world) Two charged bodies of opposite sense on the chain, laid by the generator at the count 1 each, run 100 intervals at width 63 without refusal: every level of every family stays under the world's amplitude bound, and the two records' Wronskians keep their opposite senses at their Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    at = (laws.CHAIN // 2 - 4, laws.CHAIN // 2 + 4)
    board = Lattice(load_world(chain_body_world(tmp_path, laws.TOOL, at=at, senses=(1, -1))))
    bound = board.world.amplitude_bound
    for _ in range(100):
        board.step()
        assert all(node.largest(line) <= bound for state in board.states for line in state.lines)
    index = [f.name for f in board.families].index("charged")
    for record, sense in enumerate((1, -1)):
        found = node.wronskian(board.lines_of(index, record), True)
        assert np.sign(found[board.body_nodes(record)]).tolist() == [sense] * int(
            board.body_nodes(record).sum()
        )


def test_the_halving_dropped_the_odd_line_over_the_doubled_wall():
    """(d) The sign holder's odd lines over the doubled wall 2 E_s T from the unhalved sum J against the old path, (J + 1) div 2 over E_s T, both by the carried division from the half wall: with 2 (L_old W + r_old) - (L_new 2 W + r_new) = k_w x (the number of odd J so far) exactly at every interval (the half unit of current the old path rounded up and the new one keeps in the remainder), so that the two are bit-identical, L_new = L_old and r_new = 2 r_old, while every J is even, and differ by the dropped half units otherwise; on random J within 10^6 over 300 intervals and on a plane wave's own current, J_x = 2 A^2 sin k, static; the walls of turning.json's sign holder (100 T, 200 T, 200 T, 200 T) per row."""
    write = held_write_of(TURNING, CHARGE, T)
    weight, wall = TURNING[CHARGE].write, write.walls[0]
    assert write.walls == (wall, 2 * wall, 2 * wall, 2 * wall) * 2 and wall == 100 * T
    draw = np.random.default_rng(11)
    for sources in (draw.integers(-(10**6), 10**6, 300), 2 * draw.integers(-(10**6), 10**6, 300)):
        old, new, odds = (0, wall // 2), (0, wall), 0
        for current in sources.tolist():
            gained, r_old = divmod(old[1] + weight * ((current + 1) // 2), wall)  # the old path
            level_old = old[0] + gained
            gained, r_new = divmod(new[1] + weight * current, 2 * wall)  # the unhalved sum, doubled wall
            level_new = new[0] + gained
            old, new, odds = (level_old, r_old), (level_new, r_new), odds + current % 2
            assert 2 * (level_old * wall + r_old) - (level_new * 2 * wall + r_new) == weight * odds
        if not (sources % 2).any():
            assert new == (old[0], 2 * old[1])

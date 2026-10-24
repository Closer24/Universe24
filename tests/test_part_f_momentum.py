"""Part F, Task 1: the lattice momentum as a reading (features/currents `momentum`, readings.momentum_of; the advisor's and the mathematician's lines of 2026-10-09, momentum from Rule3, 6083929632 and 6084001231). The normalisation chosen and stated: P_a = SUM_i (F_(i,i-a) - F_(i,i+a)) in the current's own unit, F_ij = num (now_i before_j - before_i now_j), so P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)), the mathematician's with the current's weight; a plane wave cos(k x - omega t) has P_a of the sign of +k. (a) On a periodic chain of 24 with a plane wave the rational mirror of the vacuum form conserves P exactly over 200 intervals and the engine's integers drift below the hands' bound per step, 2 num SUM_i |now_(i+a) - now_(i-a)| in this unit (the remainders' walk, |delta_i| < 1 per Node and the two Links each see it); (b) the plane wave's P over the action it holds is the s-integer of the phase pair at the angle k over the amplitude, in T's unit, the cosine read from the record itself and the pair found by bisection on the phase line, no sine on the engine's side; (c) in a static well held by the harness P changes per step by the gradient term exactly as the rational step at the engine's own integers predicts, to the floor, and over the run the packet gains P toward the well, the fall. The measured integers are printed for the Boss."""

import json
import math
import time
from fractions import Fraction

import numpy as np

from event_universe import node, readings, records, world_files
from event_universe.core.rule3 import division_forward
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import GRAVITY

GAMMA, T, UNIT, CHAIN = 6000, 32768, 16, 24
LIGHT = {"name": "light", "pair": [GAMMA, GAMMA], "reads": {}, "dimension": 1}
INTEGERS = {"node_clock": GAMMA, "quantum_action": T, "width": 63, "link_unit": UNIT}


def chain_world(tmp_path, families, chain=CHAIN, boundary="periodic"):  # type: ignore[no-untyped-def]
    """A chain of `chain` Nodes, x `boundary`, y and z folded, no body and no packet: the records laid by hand."""
    (tmp_path / "u.json").write_text(
        json.dumps({"integers": INTEGERS, "families": families}), encoding="utf-8"
    )
    world = dict(
        shape=[chain, 1, 1], boundary=dict(x=boundary, y="periodic", z="periodic"), face_depth=1
    )
    world.update(intervals=400, universe="u.json", bodies=[], node_detectors=[])
    (path := tmp_path / "chain.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def plane_wave(board: Lattice, index: int, amplitude: int, wave: tuple[int, int], envelope=None):  # type: ignore[no-untyped-def]
    """A real plane wave cos(k x) at the wave number pi p / q per Link laid by hand on the family's one line, the level before advanced by the band's own omega(k) at the vacuum's paces (the test's floats lay; the engine reads no sine), under `envelope` where one is given."""
    family, chain = board.families[index], board.shape[0]
    reads, self_coefficient, wall, _mass = node.rule_of(family, GAMMA, 0, None, board.unit)
    k = math.pi * wave[0] / wave[1]
    cosine = (
        int(self_coefficient) + 2 * int(reads[0]) * math.cos(k) + sum(int(r) for r in reads[2:])
    ) / (2 * int(wall))
    omega, x = math.acos(cosine), np.arange(chain)
    shape = amplitude * (np.ones(chain) if envelope is None else envelope)
    now = np.rint(shape * np.cos(k * x)).astype(board.kind).reshape(board.shape)
    before = np.rint(shape * np.cos(k * x + omega)).astype(board.kind).reshape(board.shape)
    line = board.states[index].lines[0]
    board.states[index].lines = [records.Record(now, before, line.remainder)]
    return reads, self_coefficient, wall


def momentum_fraction(levels_now, levels_before, num: int) -> Fraction:  # type: ignore[no-untyped-def]
    """The test's own P_x on a periodic chain in exact rationals, the same antisymmetric sum."""
    chain, total = len(levels_now), Fraction(0)
    for i in range(chain):
        behind, ahead = (i - 1) % chain, (i + 1) % chain
        total += num * (levels_now[i] * levels_before[behind] - levels_before[i] * levels_now[behind])
        total -= num * (levels_now[i] * levels_before[ahead] - levels_before[i] * levels_now[ahead])
    return total


def rational_step(now, before, reads, self_coefficient, wall, periodic=True):  # type: ignore[no-untyped-def]
    """One interval of the vacuum form in exact rationals, next = M now - before, M per Node from the rule's integers (a list per Node where the paces vary): the chain's two x Ports and the four folded Ports reading the Node itself."""
    chain, found = len(now), []
    for i in range(chain):
        r, s, w = (
            (reads[i], self_coefficient[i], wall[i])
            if isinstance(reads, list)
            else (reads, self_coefficient, wall)
        )
        behind, ahead = ((i - 1) % chain, (i + 1) % chain) if periodic else (i - 1, i + 1)
        arrived = (now[behind] if periodic or i > 0 else 0) * int(r[1])
        arrived += (now[ahead] if periodic or i < chain - 1 else 0) * int(r[0])
        total = int(s) * now[i] + arrived + sum(int(v) for v in r[2:]) * now[i]
        found.append(total / int(w) - before[i])
    return found


def bound_of(board: Lattice, index: int) -> int:
    """The hands' bound on the integers' drift per step in this unit, 2 num SUM_i |now_(i+a) - now_(i-a)| along x."""
    now = board.states[index].lines[0].now.reshape(-1).astype(object)
    chain = len(now)
    return (
        2
        * board.families[index].pair[0]
        * int(sum(abs(now[(i + 1) % chain] - now[(i - 1) % chain]) for i in range(chain)))
    )


def pair_at_cosine(board: Lattice, numerator: int, denominator: int) -> tuple[int, int, int]:
    """The phase pair at the angle whose cosine is numerator / denominator, found by bisection on the phase line as `paces.rotation_unit` finds the rest rotation: n acts, (c, s) at the amplitude X; no sine."""
    amplitude, gamma = board.amplitude, board.world.node_clock
    low, high, pair = 0, 2 * gamma, phase.seed(board.amplitude, gamma)
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        probe = phase.iterate(pair, middle - low, gamma)
        if int(phase.read(probe)[0]) * denominator >= amplitude * numerator:
            low, pair = middle, probe
        else:
            high = middle
    c, s = phase.read(pair)
    return low, int(c), int(s)


def test_the_momentum_is_conserved_exactly_in_the_mirror_and_to_the_floor_on_the_integers(
    tmp_path, monkeypatch
):
    """(a) A plane wave at k = pi / 4 on the periodic chain of 24 at the amplitude 5,000 (the world's bound 6,949): the rational mirror of the vacuum form keeps P_x bit for bit over 200 intervals; the engine's integer P_x moves per step below the hands' bound 2 num SUM |now_(i+1) - now_(i-1)| and the drift over the run is printed; P_y = P_z = 0 on the folded axes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    board = Lattice(load_world(chain_world(tmp_path, [LIGHT])))
    reads, self_coefficient, wall = plane_wave(board, 0, 5000, (1, 4))
    num = board.families[0].pair[0]
    lines = board.states[0].lines
    now = [Fraction(int(v)) for v in lines[0].now.reshape(-1)]
    before = [Fraction(int(v)) for v in lines[0].before.reshape(-1)]
    mirror, first = momentum_fraction(now, before, num), readings.momentum_of(num, lines, board.wrap)
    assert first[0] > 0 and first[1:] == (0, 0) and Fraction(first[0]) == mirror  # +k: P of k's sign
    steps, bounds, last = [], [], first[0]
    for _ in range(200):
        bound = bound_of(board, 0)
        now, before = rational_step(now, before, reads, self_coefficient, wall), now
        assert momentum_fraction(now, before, num) == mirror  # the theorem: exact at uniform paces
        board.step()
        found = readings.momentum_of(num, board.states[0].lines, board.wrap)
        steps.append(found[0] - last)
        bounds.append(bound)
        assert abs(found[0] - last) < bound and found[1:] == (0, 0)
        last = found[0]
    drift = last - first[0]
    print(
        f"Part F (a): P_x = {first[0]}, 200 intervals, the mirror exact; the integers' drift {drift} "
        f"({drift / first[0]:.2e} of P), the largest step {max(abs(s) for s in steps)} under the bound "
        f"{min(bounds)}..{max(bounds)}; {time.perf_counter() - started:.1f} s"
    )


def test_the_plane_waves_momentum_over_its_action_is_the_pairs_s_integer(tmp_path, monkeypatch):
    """(b) The same plane wave: cos k read from the record itself, 2 cos k = SUM now_i (now_(i+1) + now_(i-1)) / SUM now_i^2, the pair at k by bisection on the phase line (n_k acts, c_k, s_k) and the pair at the band's omega(k) from the rule's own line 2 w cos omega = S + 2 R cos k + 4 R (n_omega, s_omega); Part F2, both hands' unit (6085442608, 6085486079): one quantum of action is SUM over lines and Nodes of A^2 sin omega = T, and the record's quanta of action are its share over (3 den T sin omega) (the engine's share 3 den A^2 sin^2 omega per Node), so P_x over num and over the quanta, P_x 3 den s_omega T over (num share X), stands against the whole quantum's 2 T s_k / X (T sin k per Link once, each Link twice in the antisymmetric sum) to the lay's rounding; both integers printed, with the engine's count of the record in W_c for the Boss (a W_c count is 1 / sin omega quanta of action and carries 2 T sin k / sin omega)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(chain_world(tmp_path, [LIGHT])))
    reads, self_coefficient, wall = plane_wave(board, 0, 5000, (1, 4))
    family, lines = board.families[0], board.states[0].lines
    num, den = family.pair
    now = lines[0].now.reshape(-1).astype(object)
    chain = len(now)
    numerator = int(sum(now[i] * (now[(i + 1) % chain] + now[(i - 1) % chain]) for i in range(chain)))
    denominator = 2 * int(sum(now[i] * now[i] for i in range(chain)))
    n_k, c_k, s_k = pair_at_cosine(board, numerator, denominator)
    amplitude = board.amplitude
    band_numerator = (
        int(self_coefficient) * amplitude
        + 2 * int(reads[0]) * c_k
        + sum(int(r) for r in reads[2:]) * amplitude
    )
    n_omega, c_omega, s_omega = pair_at_cosine(board, band_numerator, 2 * int(wall) * amplitude)
    momentum = readings.momentum_of(num, lines, board.wrap)[0]
    share = board.total_share(0)[0]
    assert share is not None and momentum > 0
    hands = int(division_forward(2 * T * s_k, amplitude, division_forward(amplitude, 2, 0)[0])[0])
    engine_wall = num * share * amplitude
    engine = int(
        division_forward(
            momentum * 3 * den * s_omega * T, engine_wall, division_forward(engine_wall, 2, 0)[0]
        )[0]
    )
    count = Fraction(share, 3 * den * T)
    print(
        f"Part F (b): n_k = {n_k}, s_k / X = {s_k / amplitude:.6f} (sin pi/4 = {math.sin(math.pi / 4):.6f}), n_omega = {n_omega}, "
        f"s_omega / X = {s_omega / amplitude:.6f}; P over the quanta of action: the engine's reading {engine} against 2 T s_k / X = {hands} "
        f"(the difference {engine - hands}); P_x = {momentum}, share = {share}, the engine's count {float(count):.3f} W_c, "
        f"P_x / (num count T) = {momentum / (num * count * T):.4f} = 2 sin k / sin omega to the lay's rounding"
    )
    assert abs(engine - hands) <= 8  # the lay's rounding at A = 8,000: a few units of 2 T's 46,341


def test_in_a_held_well_the_momentum_changes_by_the_gradient_term_and_falls_toward_the_well(
    tmp_path, monkeypatch
):
    """(c) A packet (the plane wave at k = pi / 4 under a raised-cosine envelope over 12 Nodes) on an open chain of 48 beside a well of the content, the gravity row's level raised by a bump of 400 over 9 Nodes at the far side and held static by the harness each interval (the hands' non-uniform static paces): per step the engine's integer Delta P_x equals the rational step's at the engine's own integers per Node (the gradient term; 0 at uniform paces) to the floor 2 num SUM |now_(i+1) - now_(i-1)|, and over 30 intervals P_x grows toward the well, the fall; the integers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    light = dict(LIGHT, reads={"gravity": 1})
    board = Lattice(load_world(chain_world(tmp_path, [GRAVITY, light], 48, "open")))
    gravity, index = 0, 1
    x = np.arange(48)
    envelope = np.where((x >= 4) & (x < 16), np.sin(np.pi * (x - 3) / 13) ** 2, 0.0)
    plane_wave(board, index, 5000, (1, 4), envelope)  # within the bound 6,949
    well = np.where(abs(x - 36) <= 4, np.rint(400 * np.cos(np.pi * (x - 36) / 10) ** 2), 0).astype(
        board.kind
    )
    row = board.states[gravity].lines[0]
    level = (row.now + well.reshape(board.shape)).astype(board.kind)
    board.states[gravity].lines[0] = records.Record(level, level.copy(), row.remainder)
    kept = (
        list(board.states[gravity].lines),
        [r.copy() for r in board.states[gravity].write_remainders],
    )
    num = board.families[index].pair[0]
    first = readings.momentum_of(num, board.states[index].lines, board.wrap)[0]
    last, misses = first, []
    for _ in range(30):
        content = board.read(index, 1, 0)[0]
        rules = [
            node.rule_of(
                board.families[index], GAMMA, int(np.asarray(content).reshape(-1)[i]), None, board.unit
            )
            for i in range(48)
        ]
        reads, self_coefficient, wall = ([r[k] for r in rules] for k in range(3))
        lines = board.states[index].lines
        now = [Fraction(int(v)) for v in lines[0].now.reshape(-1)]
        before = [Fraction(int(v)) for v in lines[0].before.reshape(-1)]
        predicted = momentum_fraction(
            rational_step(now, before, reads, self_coefficient, wall, False), now, num
        ) - Fraction(last)
        bound = bound_of(board, index)
        board.step()
        board.states[gravity].lines = list(kept[0])
        board.states[gravity].write_remainders = [r.copy() for r in kept[1]]
        found = readings.momentum_of(num, board.states[index].lines, board.wrap)[0]
        misses.append(abs(Fraction(found - last) - predicted))
        assert abs(Fraction(found - last) - predicted) < bound
        last = found
    assert last > first  # the packet moves toward +x where the well stands: P_x grows, the fall
    print(
        f"Part F (c): P_x {first} -> {last} over 30 intervals toward the well (+{last - first}); the integer step against the "
        f"rational step's gradient term: the largest miss {float(max(misses)):.0f} under the floor"
    )


def rounding_floor(board: Lattice, index: int, at: np.ndarray) -> float:
    """The floor of a piece's p from the lay's roundings in p's own unit (the two hands' lines of 2026-10-09, Part F2 Task 3: one level unit per Node per rounding times the neighbours' levels, as Task 3b's floor was computed): P's floor 2 num SUM over the record's lines and the region's Nodes of (|now| + |before|), each level's unit of rounding meeting the neighbour's level on two Links, scaled as the piece is, by W_rec over the region's share and over num, and one more for the piece's own rounding half up."""
    lines = board.lines_of(index, 0)
    levels = sum(
        int(np.abs(r.now.astype(object))[at].sum()) + int(np.abs(r.before.astype(object))[at].sum())
        for r in lines
    )
    share = int(board.share_of(index, 1, at)[0][at].sum(dtype=object))
    return 2 * levels * board.credit.units[index] / share + 1

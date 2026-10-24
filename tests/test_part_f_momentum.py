"""The lattice momentum as a reading (ALGEBRA.md, The lattice momentum; features/currents `momentum_terms`, readings.momentum_of): P_a = SUM_i (F_(i,i-a) - F_(i,i+a)) in the current's own unit, F_ij = num (now_i before_j - before_i now_j); on a periodic chain with a plane wave the rational mirror of the vacuum form conserves P exactly over 200 intervals and the engine's integers drift below the hands' bound per step, 2 num SUM_i |now_(i+a) - now_(i-a)|."""

import json
import math
import time
from fractions import Fraction

import numpy as np

from event_universe import node, readings, records, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world

GAMMA, T, UNIT, CHAIN = 6000, 32768, 16, 24
LIGHT = {"name": "light", "pair": [GAMMA, GAMMA], "reads": {}, "dimension": 1}
INTEGERS = {"node_clock": GAMMA, "quantum_action": T, "width": 63, "link_unit": UNIT}


def chain_world(tmp_path, families, chain=CHAIN):  # type: ignore[no-untyped-def]
    """A ring of `chain` Nodes along x, y and z folded, no body and no packet: the records laid by hand."""
    (tmp_path / "u.json").write_text(
        json.dumps({"integers": INTEGERS, "families": families}), encoding="utf-8"
    )
    world = dict(shape=[chain, 1, 1])
    world.update(intervals=400, universe="u.json")
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

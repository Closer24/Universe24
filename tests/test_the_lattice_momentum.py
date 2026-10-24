"""The lattice momentum (ALGEBRA.md, The lattice momentum, a theorem of Rule3; readings.momentum_of, features/currents `momentum_terms`): P_a = SUM_i (F_(i,i-a) - F_(i,i+a)) in the current's own unit, F_ij = num (now_i before_j - before_i now_j), conserved exactly by the rational step at uniform paces on a periodic board and to the floors on the integers, every step's move below the hands' bound 2 num SUM_i |now_(i+a) - now_(i-a)|, a walk of mean 0; a wave along +x has P_x above 0 and P_y = P_z = 0. On a 3-cube torus of the one universe file's light family stepped by the engine's own `flux.step_line`."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import flux, node, readings, records
from event_universe.core.ports import LINK_UNIT, PORT_SIDES, Wrap
from event_universe.loader.universe import universe_of
from tests.laws_universe import CUBE, UNIVERSE

INTEGERS, FAMILIES = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
LIGHT = [family.name for family in FAMILIES].index("light")
GAMMA, UNIT = INTEGERS["node_clock"], LINK_UNIT
SHAPE, TORUS = (CUBE,) * 3, Wrap(True, True, True)
INTERVALS, AMPLITUDE = 50, 5000


def test_the_momentum_is_conserved_exactly_in_the_mirror_and_to_the_floor_on_the_integers():
    """Random levels within 5,000 on the torus at the vacuum's paces: the rational mirror of the vacuum form, next = (SUM_j R a_j + S a_now) / w - a_before, keeps every P_a bit for bit over 50 intervals; the engine's integer P_a moves per step below the hands' bound and the drift over the run is printed; a plane wave along +x, the level before advanced by the band's own omega(k), has P_x above 0 and P_y = P_z = 0 (the sign of +k)."""
    draw, num = np.random.default_rng(3), FAMILIES[LIGHT].pair[0]
    rule = node.rule_of(FAMILIES[LIGHT], GAMMA, 0, None, UNIT)
    read, self_coefficient, wall = (
        int(np.asarray(v).reshape(-1)[0]) for v in (rule[0][0], rule[1], rule[2])
    )
    line = records.Record(
        draw.integers(-AMPLITUDE, AMPLITUDE + 1, SHAPE).astype(object),
        draw.integers(-AMPLITUDE, AMPLITUDE + 1, SHAPE).astype(object),
        np.zeros(SHAPE, dtype=object),
    )
    index = np.arange(CUBE**3).reshape(SHAPE)
    neighbours = [np.roll(index, -side, axis).reshape(-1) for axis, side in PORT_SIDES]
    now = [Fraction(int(v)) for v in line.now.reshape(-1)]
    before = [Fraction(int(v)) for v in line.before.reshape(-1)]

    def mirror(now, before, axis):  # type: ignore[no-untyped-def]
        ahead, behind = neighbours[2 * axis], neighbours[2 * axis + 1]
        return sum(
            num * (now[i] * before[int(behind[i])] - before[i] * now[int(behind[i])])
            - num * (now[i] * before[int(ahead[i])] - before[i] * now[int(ahead[i])])
            for i in range(CUBE**3)
        )

    kept = [mirror(now, before, axis) for axis in range(3)]
    first = readings.momentum_of(num, [line], TORUS)
    assert [Fraction(p) for p in first] == kept
    last, steps = first, []
    for _ in range(INTERVALS):
        bounds = [
            2 * num * int(np.abs(np.roll(line.now, -1, axis) - np.roll(line.now, 1, axis)).sum())
            for axis in range(3)
        ]
        stepped = [
            (
                sum(read * now[int(neighbours[port][i])] for port in range(len(PORT_SIDES)))
                + self_coefficient * now[i]
            )
            / wall
            - before[i]
            for i in range(CUBE**3)
        ]
        now, before = stepped, now
        assert [
            mirror(now, before, axis) for axis in range(3)
        ] == kept  # the theorem: exact at uniform paces
        line = flux.step_line(line, rule, TORUS)
        found = readings.momentum_of(num, [line], TORUS)
        steps.append(max(abs(found[axis] - last[axis]) for axis in range(3)))
        assert all(abs(found[axis] - last[axis]) < bounds[axis] for axis in range(3))
        last = found
    drift = [last[axis] - first[axis] for axis in range(3)]
    print(
        f"P {first}, {INTERVALS} intervals, the mirror exact; the integers' drift {drift}, the largest step {max(steps)}"
    )
    k = 2 * math.pi / CUBE
    cosine = (self_coefficient + 2 * read * math.cos(k) + 4 * read) / (2 * wall)
    omega, x = math.acos(cosine), np.indices(SHAPE)[0]
    wave = records.Record(
        np.rint(AMPLITUDE * np.cos(k * x)).astype(object),
        np.rint(AMPLITUDE * np.cos(k * x + omega)).astype(object),
        np.zeros(SHAPE, dtype=object),
    )
    along = readings.momentum_of(num, [wave], TORUS)
    assert along[0] > 0 and along[1:] == (0, 0)

"""The group structure of the Beam Law, named on 2026-09-21 (the vector
program, record 191; the architect's item 3): the cube's group of 48
(`core.game_board.cube_symmetries`), the phase circle Z_N
(`core.phase.PhaseCircle`) and the collision as a group action
(`nature_beam.CollisionTable`: the shift on the slot states, its orbits the
classes). Properties, not counts (docs/TEST_EXPECTATIONS.md, "The group
structure"), written down first:

(a) the cube's group: 48 symmetries, each a permutation of the six Ports
    that maps opposite Ports to opposite Ports; closed under composition,
    the identity among them, every inverse in the group and undoing its
    symmetry; the hand +1 on 24 (the rotations) and -1 on 24 (the
    reflections), multiplicative under composition, the identity's +1;
(b) the phase circle at N = 64, 2 and 4096: a turn adds modulo N (a full
    turn returns, a negative turn goes back), a difference is the steps
    from one phase to another, the opposite phase is half a turn away and
    opposite twice returns; the unit vectors: equal phases give the scale's
    square 65536 as their inner product and opposite phases exactly its
    negative, and every vector's C^2 + S^2 is within 361 of 65536 (the
    tables' rounding, BEAM_LAW section 5);
(c) the collision action: every code's period is the size of its class,
    the shift applied period times returns the code and visits every
    member of the class once (one cycle per class), the inverse undoes the
    shift, and the class invariants (the crowd mask, the number of
    singles, their headings' sum) are constant along the cycle; `act` is
    the table's shift.
"""

from __future__ import annotations

import itertools

import numpy as np

from event_universe.core.game_board import (
    IDENTITY_SYMMETRY,
    compose_symmetries,
    cube_symmetries,
    inverse_symmetry,
    symmetry_hand,
)
from event_universe.core.phase import PHASE_COSINE_SCALE, phase_circle
from event_universe.events.nature_beam import (
    COLLISION_SLOTS,
    SLOT_STATES,
    class_key,
    collision_table,
    state_code,
)


def test_the_cube_group_is_a_group_with_a_hand():
    """(a)."""
    group = cube_symmetries()
    assert len(group) == 48 and len(set(group)) == 48
    assert IDENTITY_SYMMETRY in group
    members = set(group)
    for symmetry in group:
        assert sorted(symmetry) == list(range(6))
        for port in range(0, 6, 2):
            assert symmetry[port] ^ 1 == symmetry[port + 1], symmetry
        inverse = inverse_symmetry(symmetry)
        assert inverse in members
        assert compose_symmetries(symmetry, inverse) == IDENTITY_SYMMETRY
        assert compose_symmetries(inverse, symmetry) == IDENTITY_SYMMETRY
        assert symmetry_hand(symmetry) in (1, -1)
    for first in group:
        for second in group:
            composed = compose_symmetries(first, second)
            assert composed in members
            assert symmetry_hand(composed) == symmetry_hand(first) * symmetry_hand(second)
    assert symmetry_hand(IDENTITY_SYMMETRY) == 1
    hands = [symmetry_hand(symmetry) for symmetry in group]
    assert hands.count(1) == 24 and hands.count(-1) == 24


def test_the_phase_circle_is_the_cyclic_group_with_unit_vectors():
    """(b)."""
    for steps in (64, 2, 4096):
        circle = phase_circle(steps)
        assert circle.steps == steps and circle.mask == steps - 1 and circle.half == steps // 2
        for phase in range(0, steps, max(1, steps // 16)):
            assert circle.turn(phase, steps) == phase
            assert circle.turn(phase, -phase) == 0
            assert circle.turn(circle.turn(phase, 5), -5) == phase
            assert circle.difference(circle.turn(phase, 7), phase) == 7 % steps
            assert circle.difference(phase, circle.opposite(phase)) == circle.half
            assert circle.opposite(circle.opposite(phase)) == phase
            c, s = circle.vector(phase)
            c2, s2 = circle.vector(circle.opposite(phase))
            square = PHASE_COSINE_SCALE * PHASE_COSINE_SCALE
            assert abs(c * c + s * s - square) <= 361
            assert c * c2 + s * s2 == -(c * c + s * s)
        assert circle.vector(0) == (PHASE_COSINE_SCALE, 0)
        assert circle.vector(steps) == circle.vector(0)


def test_the_collision_action_is_one_cycle_per_class():
    """(c)."""
    table = collision_table()
    size = SLOT_STATES**COLLISION_SLOTS
    codes = np.arange(size)
    assert table.orbit.shape == (size,) and table.period.shape == (size,)
    # The period of every code is its class's size.
    sizes = np.bincount(table.orbit, minlength=int(table.orbit.max()) + 1)
    assert (table.period == sizes[table.orbit]).all()
    # The shift applied period times returns every code, and no earlier.
    current = codes.copy()
    returned = np.zeros(size, dtype=np.int64)
    for step in range(1, int(table.period.max()) + 1):
        current = table.act(current)
        back = (current == codes) & (returned == 0)
        returned[back] = step
    assert (returned == table.period).all()
    # The inverse undoes the shift, and the shift is a bijection.
    assert (table.act(table.act(codes), backward=True) == codes).all()
    assert (table.act(table.act(codes, backward=True)) == codes).all()
    assert len(set(table.forward.tolist())) == size
    # One cycle per class: the codes a class's cycle visits are the class.
    for state in itertools.islice(
        itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS), 0, size, 7
    ):
        code = state_code(state)
        visited = {code}
        current_code = int(table.forward[code])
        while current_code != code:
            visited.add(current_code)
            current_code = int(table.forward[current_code])
        assert len(visited) == int(table.period[code])
        assert {int(table.orbit[c]) for c in visited} == {int(table.orbit[code])}
        key = class_key(state)
        for member in visited:
            member_state = tuple(
                (member // SLOT_STATES**k) % SLOT_STATES for k in range(COLLISION_SLOTS)
            )
            assert class_key(member_state) == key

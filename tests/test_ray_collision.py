"""The collision table under the law of the ray (docs/RAY_LAW.md, section
4): eight single-occupancy slots per Node, the six headings in Port order
and two rest slots; a slot empty, single or a crowd; the class of a state
(the crowd mask, the number of singles, their headings' sum); inside a class
the forward map is the cyclic shift by +1 and the inverse by -1, generated
from the rule and never written by hand. The expected integers of
docs/TEST_EXPECTATIONS.md ("The collision table"), written down first:

(a) 3^8 = 6561 states, 5440 classes, 2132 moving states, 202 of the 256
    binary states; INV[FWD[s]] = s for every state; the class of FWD[s] is
    the class of s; a crowd slot never changes; the amount (the number of
    singles) and the heading sum are conserved by every move;
(b) the 20 orbits of the (six-heading pattern, here flag) under the 48
    signed axis permutations, with the sizes 1, 6, 3, 12, 12, 3, 8, 12, 6,
    1 (here 0) and the same with here 1; a lone unit is fixed; the head-on
    pair +x -x parks in the two rest slots, and ha hb becomes +z -z;
(c) on the board: two rays of amount 1 meeting head-on at the middle Node
    of a 5 x 1 x 1 bar (x and z periodic so that nothing escapes) become
    the two rest rays (directions 0 and 1) at that Node in the interval
    they meet, and stay; two rays of amount 2 (a crowd) pass each other;
    over the six orientations of a head-on pair on a periodic 5^3 cube the
    x pair parks, the y pair turns onto x and the z pair onto y, and after
    the second collision the rest pair leaves on z, the x pair parks and the
    y pair turns onto x: the one cycle of the class, the tie by Port order;
(d) no collision at a Node that holds a measured event (the model owner's
    decision of 2026-09-19 on the physics-rule reviewer's F1(c): rays meet
    the table there, not each other; the collision is a rule of free
    space): the head-on pair of (c) (one number, amount 1, the phases 0 and
    32) meeting at the Node of a measured event of `m` whose table passes
    `light` keeps its directions +x and -x (no rest ray), dwells the two
    intervals of its line at that Node and parts at the third interval
    (x = 5 and x = 3 on a 9 x 1 x 1 bar); the same pair at a measured
    event whose table measures `light` in the window 32: the ray at phase
    32 clicks with its label (-64, 0, 0) (the event's momentum; since
    2026-09-19 the label of a unit along a heading is Q e_d, Q = 64,
    RAY_LAW section 2 and note 23), the ray at phase 0 passes and goes on
    to x = 5, the transit line is (64, 0, 0) and no ray is stranded at
    rest; the momentum book closes, measured + transit = (0, 0, 0), the
    labels' sum before the interval.
"""

from __future__ import annotations

import itertools

import numpy as np

from event_universe.core.lattice import PORT_HEADINGS
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.nature_beam import class_key, collision_table, slot_heading, state_code

STATES = list(itertools.product(range(3), repeat=8))


def test_the_table_is_a_bijection_inside_invariant_classes():
    """(a)."""
    table = collision_table()
    codes = np.arange(3**8)
    assert (table.inverse[table.forward] == codes).all() and (
        table.forward[table.inverse] == codes
    ).all()
    assert int((table.forward != codes).sum()) == 2132
    classes: dict[object, int] = {}
    for state in STATES:
        classes[class_key(state)] = classes.get(class_key(state), 0) + 1
    assert len(classes) == 5440
    binary = [s for s in STATES if 2 not in s]
    assert len(binary) == 256
    assert sum(1 for s in binary if table.forward[state_code(s)] != state_code(s)) == 202
    by_code = {state_code(s): s for s in STATES}
    for state in STATES:
        target = by_code[int(table.forward[state_code(state)])]
        assert class_key(target) == class_key(state)
        for slot in range(8):
            assert (state[slot] == 2) == (target[slot] == 2)
        assert sum(1 for s in target if s == 1) == sum(1 for s in state if s == 1)
        total = [0, 0, 0]
        for slot in range(8):
            heading = slot_heading(slot)
            for axis in range(3):
                total[axis] += heading[axis] * ((target[slot] == 1) - (state[slot] == 1))
        assert total == [0, 0, 0]
    assert table.singles[state_code((1, 1, 0, 0, 0, 0, 0, 0))].tolist() == [0, 1, -1, -1, -1, -1, -1, -1]


def cube_group():
    maps = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            image = []
            for port in range(6):
                axis, forward = port >> 1, (port & 1) == 0
                sign = (1 if forward else -1) * signs[axis]
                image.append(2 * perm[axis] + (0 if sign > 0 else 1))
            maps.append(tuple(image))
    return maps


def test_the_twenty_orbits_and_the_named_rows():
    """(b)."""
    group = cube_group()
    seen: set[tuple[int, int]] = set()
    sizes = []
    for here in (0, 1):
        for bits in range(64):
            if (bits, here) in seen:
                continue
            orbit = set()
            for image in group:
                mapped = 0
                for port in range(6):
                    if bits >> port & 1:
                        mapped |= 1 << image[port]
                orbit.add((mapped, here))
            seen |= orbit
            sizes.append(len(orbit))
    assert len(sizes) == 20 and sizes == [1, 6, 3, 12, 12, 3, 8, 12, 6, 1] * 2
    table = collision_table()

    def forward(state: tuple[int, ...]) -> tuple[int, ...]:
        code = int(table.forward[state_code(state)])
        return tuple((code // 3**k) % 3 for k in range(8))

    lone = (1, 0, 0, 0, 0, 0, 0, 0)
    assert forward(lone) == lone
    assert forward((1, 1, 0, 0, 0, 0, 0, 0)) == (0, 0, 0, 0, 0, 0, 1, 1)
    assert forward((0, 0, 0, 0, 0, 0, 1, 1)) == (0, 0, 0, 0, 1, 1, 0, 0)
    assert forward((0, 0, 0, 0, 1, 1, 0, 0)) == (0, 0, 1, 1, 0, 0, 0, 0)
    assert forward((0, 0, 1, 1, 0, 0, 0, 0)) == (1, 1, 0, 0, 0, 0, 0, 0)
    assert forward((0, 0, 0, 0, 0, 0, 1, 0)) == (0, 0, 0, 0, 0, 0, 0, 1)
    assert forward((1, 1, 1, 1, 0, 0, 0, 0)) == (0, 0, 0, 0, 1, 1, 1, 1)
    assert forward((2, 1, 0, 0, 0, 0, 0, 0)) == (2, 1, 0, 0, 0, 0, 0, 0)


def bar(shape: list[int], boundary: object, rays: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-collision-test",
        "shape": shape,
        "boundary": boundary,
        "ticks": 4,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": "pass"},
            }
        ],
        "in_transit": rays,
    }


def ray(position: list[int], direction: list[int], amount: int = 1, phase: int = 0) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "number": 1,
        "direction": direction,
        "amount": amount,
        "phase": phase,
    }


def test_a_head_on_pair_parks_and_a_crowd_passes():
    """(c)."""
    everywhere = {"x": "periodic", "y": "periodic", "z": "periodic"}
    world = bar([5, 1, 1], everywhere, [ray([1, 0, 0], [1, 0, 0]), ray([3, 0, 0], [-1, 0, 0], phase=9)])
    simulation = RaySimulation(parse_ray_world(world))
    store = simulation.stores[0]
    simulation.step()
    rows = sorted(
        (int(store.node[i]), int(store.direction[i]), int(store.phase[i])) for i in range(store.size)
    )
    assert rows == [(2, 0, 0), (2, 1, 9)]
    # The rest pair leaves on z, meets itself through the stubs of extent 1
    # and cycles through the axes: the class {+x-x, +y-y, +z-z, ha hb}.
    cycle = []
    for _ in range(3):
        simulation.step()
        assert simulation.books()["balanced"]
        cycle.append(sorted(store.direction.tolist()))
    assert cycle == [[6, 7], [4, 5], [2, 3]] and set(store.node.tolist()) == {2}
    crowd = bar([5, 1, 1], everywhere, [ray([1, 0, 0], [1, 0, 0], 2), ray([3, 0, 0], [-1, 0, 0], 2)])
    simulation = RaySimulation(parse_ray_world(crowd))
    store = simulation.stores[0]
    simulation.step()
    assert sorted(store.direction.tolist()) == [2, 3] and set(store.node.tolist()) == {2}
    # The six orientations of a head-on pair on a periodic cube: the class
    # {+x-x, +y-y, +z-z, ha hb} is one cycle, so the x pair parks, the y
    # pair turns onto x and the z pair onto y (the tie by Port order, the
    # one undeclared breaking; every orientation visits every axis and the
    # rest over the cycle).
    exits = []
    after_one = {0: [0, 1], 1: [0, 1], 2: [2, 3], 3: [2, 3], 4: [4, 5], 5: [4, 5]}
    after_two = {0: [6, 7], 1: [6, 7], 2: [0, 1], 3: [0, 1], 4: [2, 3], 5: [2, 3]}
    for port in range(6):
        heading = list(PORT_HEADINGS[port])
        opposite = [-c for c in heading]
        start_a = [2 - h for h in heading]
        start_b = [2 + h for h in heading]
        pair = bar(
            [5, 5, 5],
            {"x": "periodic", "y": "periodic", "z": "periodic"},
            [ray(start_a, heading), ray(start_b, opposite, phase=9)],
        )
        simulation = RaySimulation(parse_ray_world(pair))
        store = simulation.stores[0]
        simulation.step()
        assert sorted(store.direction.tolist()) == after_one[port], port
        simulation.step()
        assert sorted(store.direction.tolist()) == after_two[port], port
        exits.append(tuple(sorted(store.direction.tolist())))
    assert sorted(set(exits)) == [(0, 1), (2, 3), (6, 7)]


def test_no_collision_at_a_node_that_holds_a_measured_event():
    """(d)."""
    lamp = {"position": [0, 0, 0], "family": "light", "amount": 4, "fixed": True}
    pair = [ray([3, 0, 0], [1, 0, 0]), ray([5, 0, 0], [-1, 0, 0], phase=32)]
    families = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]
    window = {"rule": "measure", "phase_window": 32}
    for table, momentum, transit, rows_after in (
        ({"light": "pass"}, [0, 0, 0], [0, 0, 0], [(2, 5), (3, 3)]),
        ({"light": window}, [-64, 0, 0], [64, 0, 0], [(2, 5)]),
    ):
        taker = {"position": [4, 0, 0], "family": "m", "amount": 4, "fixed": True, "table": table}
        world = bar([9, 1, 1], {"y": "periodic", "z": "periodic"}, pair)
        world["families"] = families
        world["measured"] = [lamp, taker]
        simulation = RaySimulation(parse_ray_world(world))
        light = simulation.stores[1]
        assert simulation.books()["momentum"]["transit"] == [0, 0, 0]
        simulation.step()
        assert simulation.books()["balanced"]
        rows = sorted((int(light.direction[i]), int(light.node[i])) for i in range(light.size))
        assert rows == sorted((d, light.flat((4, 0, 0))) for d, _ in rows_after)
        assert not (light.direction < 2).any()
        assert simulation.measured[2].momentum == momentum
        books = simulation.books()
        assert books["momentum"]["transit"] == transit and books["momentum"]["measured"] == momentum
        simulation.step()
        simulation.step()
        assert simulation.books()["balanced"]
        rows = sorted((int(light.direction[i]), int(light.node[i])) for i in range(light.size))
        assert rows == sorted((d, light.flat((x, 0, 0))) for d, x in rows_after)

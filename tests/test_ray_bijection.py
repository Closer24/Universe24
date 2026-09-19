"""The interval is a bijection on a board without a border (docs/RAY_LAW.md,
section 3; the model owner, 2026-09-19): the walk and the collision have
inverses, and T forward intervals followed by T inverse intervals return
the store bit-exact. The expected result of docs/TEST_EXPECTATIONS.md ("The
bijection"), written down first: a periodic 8 x 8 x 4 board, 300 records of
fixed arrays (rays on every heading, both rest slots and two fan directions,
head-on pairs among them, amounts 1 and 2, phases over the circle), 50
forward then 50 inverse intervals with no measured event: the sorted store
equal to the start in every field; the state at the turning point differs
from the start; the collision moved at least one ray on the way.
"""

from __future__ import annotations

import numpy as np

from event_universe.events import RaySimulation, parse_ray_world


def fixed_rays() -> list[dict[str, object]]:
    rays = []
    directions = [
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1],
        0,
        1,
        [1, 1, 0],
        [2, -1, 1],
    ]
    for k in range(300):
        direction = directions[(k * 7) % len(directions)]
        rays.append(
            {
                "position": [(k * 5) % 8, (k * 3) % 8, (k * 11) % 4],
                "family": "light",
                "number": 1,
                "direction": direction,
                "amount": 1 + (k % 5 == 0),
                "phase": (k * 13) % 64,
                "age": (k * 17) % 23,
            }
        )
    # Head-on pairs at the same age meet at the Node between them.
    for k in range(12):
        rays.append(
            {
                "position": [1, k % 8, k % 4],
                "family": "light",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": k,
            }
        )
        rays.append(
            {
                "position": [3, k % 8, k % 4],
                "family": "light",
                "number": 1,
                "direction": [-1, 0, 0],
                "amount": 1,
                "phase": 32 + k,
            }
        )
    return rays


WORLD = {
    "law": "rays",
    "model_id": "ray-bijection-test",
    "shape": [8, 8, 4],
    "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    "ticks": 100,
    "K": 1 << 20,
    "N": 64,
    "release": [0, 1],
    "suspension": 0,
    "directions": [[1, 1, 0], [2, -1, 1]],
    "families": [{"name": "light", "kind": "paid", "phase_per_link": 5}],
    "measured": [],
    "in_transit": fixed_rays(),
}


def snapshot(simulation: RaySimulation) -> np.ndarray:
    store = simulation.stores[0]
    rows = np.stack(
        [store.node, store.direction, store.age, store.phase, store.number, store.amount, store.content],
        axis=1,
    )
    return rows[np.lexsort(rows.T[::-1])]


def test_fifty_intervals_forward_and_back_return_the_store_bit_exact():
    simulation = RaySimulation(parse_ray_world(WORLD))
    start = snapshot(simulation)
    directions_before = simulation.stores[0].direction.copy()
    collided = False
    for _ in range(50):
        before = simulation.stores[0].direction.copy()
        simulation.step()
        after = simulation.stores[0].direction
        collided = collided or before.shape != after.shape or (before != after).any()
    middle = snapshot(simulation)
    assert middle.shape[0] >= 1 and not np.array_equal(middle, start)
    assert collided or (directions_before != simulation.stores[0].direction).any()
    for _ in range(50):
        simulation.inverse_step()
    assert np.array_equal(snapshot(simulation), start)
    assert simulation.tick == 0

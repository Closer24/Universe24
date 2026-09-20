"""The interval is a bijection on a GameBoard without a border (docs/RAY_LAW.md,
section 3; the model owner, 2026-09-19): the walk and the collision have
inverses, and T forward intervals followed by T inverse intervals return
the store bit-exact. The expected result of docs/TEST_EXPECTATIONS.md ("The
bijection"), written down first: a periodic 8 x 8 x 4 GameBoard, 300 records of
fixed arrays (rays on every heading, both rest slots and two fan directions,
head-on pairs among them, amounts 1 and 2, phases over the circle), 50
forward then 50 inverse intervals with no measured event: the sorted store
equal to the start in every field; the state at the turning point differs
from the start; the collision moved at least one ray on the way. The merge
(step 6) orders the rows by one packed key of the identity fields where
they fit the register and by the lexsort of the fields otherwise: on 82
fixed rows (60 distinct, 20 repeated, two extremes) both give the 62 rows
the Python sort of the identity tuples gives, the amounts of equal tuples
added, every arrival reset; the empty store merges to the empty store.
"""

from __future__ import annotations

import numpy as np

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import NatureBeamStore


def fixed_beams() -> list[dict[str, object]]:
    beams = []
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
        beams.append(
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
        beams.append(
            {
                "position": [1, k % 8, k % 4],
                "family": "light",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": k,
            }
        )
        beams.append(
            {
                "position": [3, k % 8, k % 4],
                "family": "light",
                "number": 1,
                "direction": [-1, 0, 0],
                "amount": 1,
                "phase": 32 + k,
            }
        )
    return beams


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
    # No ray leaves a GameBoard periodic on every axis: the age a ray may carry
    # (whole since 2026-09-20) is declared; 50 intervals on ages up to 22.
    "age_bound": 128,
    "directions": [[1, 1, 0], [2, -1, 1]],
    "families": [{"name": "light", "quantum": 1, "phase_per_link": 5}],
    "measured": [],
    "in_transit": fixed_beams(),
}


def snapshot(simulation: NatureBeamSimulation) -> np.ndarray:
    store = simulation.stores[0]
    rows = np.stack(
        [store.node, store.direction, store.age, store.phase, store.number, store.amount, store.content],
        axis=1,
    )
    return rows[np.lexsort(rows.T[::-1])]


def test_fifty_intervals_forward_and_back_return_the_store_bit_exact():
    simulation = NatureBeamSimulation(parse_nature_beam_world(WORLD))
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


def merge_by_hand(rows: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """The expected store: the rows sorted as tuples of the identity fields
    (node, direction, age, phase, number, content), the amounts of equal
    tuples added."""
    merged: dict[tuple[int, ...], int] = {}
    for node, direction, age, phase, number, amount, content in rows:
        key = (node, direction, age, phase, number, content)
        merged[key] = merged.get(key, 0) + amount
    return [(*key, amount) for key, amount in sorted(merged.items())]


def store_of(rows: list[tuple[int, ...]]) -> NatureBeamStore:
    store = NatureBeamStore((8, 8, 4))
    columns = np.array(rows, dtype=np.int64).reshape(-1, 7)
    store.append(
        node=columns[:, 0],
        direction=columns[:, 1],
        age=columns[:, 2],
        phase=columns[:, 3],
        number=columns[:, 4],
        amount=columns[:, 5],
        content=columns[:, 6],
        arrival=np.full(columns.shape[0], 3, dtype=np.int64),
    )
    return store


def rows_of(store: NatureBeamStore) -> list[tuple[int, ...]]:
    return [
        tuple(int(v) for v in row)
        for row in np.stack(
            [
                store.node,
                store.direction,
                store.age,
                store.phase,
                store.number,
                store.content,
                store.amount,
            ],
            axis=1,
        )
    ]


def test_the_merge_orders_the_rows_by_one_key_or_by_the_lexsort_alike():
    """The merge's packed key and its lexsort fallback give one store: the
    rows in the total order of the identity fields, the Node first, equal
    rows summed, every arrival reset to here."""
    rows = [
        (
            (k * 37) % 200,
            (k * 5) % 10,
            (k * 7) % 23,
            (k * 13) % 64,
            1 + k % 3,
            1 + k % 4,
            k % 3,
        )
        for k in range(60)
    ]
    rows += rows[:20]  # duplicates: merged
    rows += [(199, 9, 22, 63, 3, 5, 2), (0, 1, 0, 0, 1, 1, 0)]
    expected = merge_by_hand(rows)
    assert len(expected) == 62
    packed = store_of(rows)
    assert packed.merge_key() is not None
    packed.merge()
    assert rows_of(packed) == expected and (packed.arrival == 0).all()
    # The contents spread over 2^61 (every other row): the key does not fit.
    wide = [(*row[:6], row[6] + (k % 2) * (1 << 61)) for k, row in enumerate(rows)]
    fallback = store_of(wide)
    assert fallback.merge_key() is None
    fallback.merge()
    assert rows_of(fallback) == merge_by_hand(wide) and len(merge_by_hand(wide)) == 62
    empty = store_of([])
    empty.merge()
    assert empty.size == 0

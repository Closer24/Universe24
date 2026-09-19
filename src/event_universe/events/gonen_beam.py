"""The law of the ray (rays-v1): the record `GonenBeam`, the store of records,
the two pure tables and the one function `gonen_beam`, a Node's whole
interval for the rays present (docs/RAY_LAW.md, the model owner's decision of
2026-09-19, Highlights 5.4, "DECIDED: the law of the ray").

The Node holds no wave. A unit is a ray with a record and moves along the
digital line of its momentum at one speed for every direction, a bijection;
rays that meet at a Node are permuted by the eight-slot collision table, a
bijection; the wave is a reading of a crowd of rays at a detector and lives
nowhere else; the click is the only one-way border. The law is ONE generic
function (the owner's name): `gonen_beam` performs the interval's steps in
order, each a bijection on the board's state except the border:

1. the walk: every ray whose flight table steps this interval is created at
   the neighbour along its step (the wrap on a periodic axis; through an
   open face it clicks on the face detector), its age advanced modulo its
   direction's period, its phase turned by the family's `phase_per_link`;
2. the readings: every Node's seven slots (the six Ports a ray arrived
   through this interval and "here", the rays that did not step) decomposed
   ONCE by `read_arrivals` into two scalars (outside, here), the net flow and
   the traceless tensor; every coupling reads its component by key;
3. the collision: at every Node, per (number, content) class, the single
   units in the eight slots (six headings, two rest slots) permuted by the
   collision table, the forward map a cyclic shift inside the class;
4. the measured events' tables and the detectors: a measured event meets
   the rays that arrived this interval at its Node, of every number but its
   own, as one set (the threshold on the set), then each ray by its own
   phase (the window), then the rule: `read` (the push, the rays go on),
   `measure` (the click: the content joins, the border; the detector's
   record is the squared scalar of the same decomposition applied to the
   clicked rays' amplitude vectors), `rerelease` (re-emitted at the next
   self-creation on the declared directions), `pass`; own-number rays are
   home;
5. the self-creations: the free release, what came home or is re-released
   apportioned whole over the declared directions, the lamp's release at
   its rate, every new ray at age 0 with its emitter's number;
6. merge identical rows and sort by Node.

No other function holds a piece of the law: `flight_table`, `collision_table`
and `read_arrivals` are the pure tables and the one decomposition it reads;
`RayStore` is the structure of arrays it moves. Integers only: the only
float is the square root's estimate, corrected to the exact integer root
(`integer_roots`). The engine (`engine.py`) schedules and books; it computes
no physics.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from event_universe.core.integer import apportion_whole, bounded_gcd, by_clock, integer_root
from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events.measured import FACE_NAMES, Ledger, Measured
from event_universe.events.world import (
    FIXED_DIRECTIONS,
    HEADING_OFFSET,
    MOMENTUM_BOUND,
    RAYS_LAW,
    REST_DIRECTIONS,
    RayWorld,
)

Record = Callable[[dict[str, object]], None]
# The time resolution of the flight table: T_d = isqrt(3 |v|^2 Q^2).
Q = 64
# The reading's slots: the six Ports in Port order and "here".
HERE = 6
READING_SLOTS = 7
# The collision's slots: the six headings in Port order and the two rest slots.
COLLISION_SLOTS = 8
SLOT_STATES = 3
# The amplitude of one unit in 32nds: A_u = isqrt(1024 x amount).
AMPLITUDE_SCALE = 32
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
ZERO3 = (0, 0, 0)


@dataclass(frozen=True)
class GonenBeam:
    """The record of a ray: its Node, its direction (an index of the world's
    table), its age (the flight phase, modulo the direction's period), its
    phase (a step of the circle), its number (the last emitter), its amount
    (whole units) and the content one unit carries."""

    node: Address3
    direction: int
    age: int
    phase: int
    number: int
    amount: int
    content: int


# -- the one decomposition -------------------------------------------------------


@dataclass(frozen=True)
class Reading:
    """The seven slots of a Node decomposed once: two scalars (outside, the
    six Ports' sum; here), the net flow (a vector) and the traceless tensor
    (two components). Every coupling selects its component by key."""

    outside: np.ndarray
    here: np.ndarray
    vector: np.ndarray
    tensor: np.ndarray

    @property
    def scalar(self) -> np.ndarray:
        """The presence: everything at the Node, outside and here."""
        result: np.ndarray = self.outside + self.here
        return result

    def component(self, key: str) -> np.ndarray:
        if key == "scalar":
            return self.scalar
        if key == "outside":
            return self.outside
        if key == "here":
            return self.here
        if key == "vector":
            return self.vector
        if key == "tensor":
            return self.tensor
        raise ValueError(f"{RAYS_LAW}: no reading component {key!r}")


# The orthogonal integer basis of the decomposition over the seven slots
# [+X, -X, +Y, -Y, +Z, -Z, here]: the two scalars, the vector, the tensor.
READING_BASIS = np.array(
    [
        [1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [1, -1, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0],
        [1, 1, 1, 1, -2, -2, 0],
        [1, 1, -1, -1, 0, 0, 0],
    ],
    dtype=np.int64,
)


def read_arrivals(slots: np.ndarray) -> Reading:
    """The one reading: the seven slots (..., 7) of a Node, the six Ports in
    Port order and here, decomposed into the components of `READING_BASIS`,
    integers: outside = the six Ports' sum, here, the net flow (+X - -X, ...)
    and the traceless tensor (p_x + p_y - 2 p_z, p_x - p_y) with p the sum
    of the two Ports of an axis. Orthogonal, and the slots are recovered as
    sum_i c_i e_i / |e_i|^2."""
    values = np.asarray(slots, dtype=np.int64)
    components = values @ READING_BASIS.T
    return Reading(components[..., 0], components[..., 1], components[..., 2:5], components[..., 5:7])


def integer_roots(scaled: np.ndarray) -> np.ndarray:
    """The integer square root of every entry, the floor, exact (the float
    root corrected by one either way)."""
    root = np.floor(np.sqrt(scaled.astype(np.float64))).astype(np.int64)
    root = np.where(root * root > scaled, root - 1, root)
    result: np.ndarray = np.where((root + 1) * (root + 1) <= scaled, root + 1, root)
    return result


# -- the flight table ------------------------------------------------------------


@dataclass(frozen=True)
class FlightTable:
    """One world constant per direction: v, S_1 = |a| + |b| + |c|,
    T_d = isqrt(3 |v|^2 Q^2), the Bresenham line of v (S_1 unit steps), the
    least period L_d of the flight phase, and the step table: the Link a ray
    of direction d crosses at age tau (a heading, or zero for no move)."""

    vectors: np.ndarray
    manhattan: np.ndarray
    turns: np.ndarray
    period: np.ndarray
    lines: np.ndarray
    steps: np.ndarray

    def manhattan_steps(self, direction: np.ndarray, age: np.ndarray) -> np.ndarray:
        """m(tau) = (2 tau S_1 Q + T_d) // (2 T_d): the Manhattan steps made
        by age tau."""
        s1, t = self.manhattan[direction], self.turns[direction]
        result: np.ndarray = (2 * age * s1 * Q + t) // (2 * t)
        return result


def _bresenham(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """The S_1 unit steps of one period of the digital line of v: at each
    step the axis whose progress is furthest behind, the lowest axis first."""
    s1 = sum(abs(c) for c in vector)
    line: list[tuple[int, int, int]] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def flight_table(vectors: tuple[tuple[int, int, int], ...]) -> FlightTable:
    """The flight table of a direction set, computed once at load."""
    count = len(vectors)
    manhattan = np.zeros(count, dtype=np.int64)
    turns = np.ones(count, dtype=np.int64)
    period = np.ones(count, dtype=np.int64)
    lines_list: list[list[tuple[int, int, int]]] = []
    for index, vector in enumerate(vectors):
        s1 = sum(abs(c) for c in vector)
        manhattan[index] = s1
        if s1 == 0:
            lines_list.append([])
            continue
        t = integer_root(3 * sum(c * c for c in vector) * Q * Q)
        turns[index] = t
        p = t // bounded_gcd(s1 * Q, t)
        per_period = s1 * Q * p // t
        period[index] = p * (s1 // bounded_gcd(per_period, s1))
        lines_list.append(_bresenham(vector))
    longest = max(1, int(manhattan.max(initial=0)))
    lines = np.zeros((count, longest, 3), dtype=np.int64)
    for index, line in enumerate(lines_list):
        for j, step in enumerate(line):
            lines[index, j] = step
    table = FlightTable(np.array(vectors, dtype=np.int64), manhattan, turns, period, lines, np.zeros(0))
    longest_period = int(period.max(initial=1))
    steps = np.zeros((count, longest_period, 3), dtype=np.int64)
    for index in range(count):
        s1 = int(manhattan[index])
        if s1 == 0:
            continue
        ages = np.arange(int(period[index]), dtype=np.int64)
        direction = np.full(ages.shape, index, dtype=np.int64)
        m0 = table.manhattan_steps(direction, ages)
        m1 = table.manhattan_steps(direction, ages + 1)
        moved = m1 > m0
        steps[index, : len(ages)] = np.where(moved[:, None], lines[index, m0 % s1], 0)
    return FlightTable(table.vectors, manhattan, turns, period, lines, steps)


# -- the collision table ---------------------------------------------------------


@dataclass(frozen=True)
class CollisionTable:
    """The permutation of the 3^8 slot states: `forward[code]`, `inverse[code]`
    and, per code, its single slots in order (`singles`, padded with -1)."""

    forward: np.ndarray
    inverse: np.ndarray
    singles: np.ndarray
    powers: np.ndarray


def slot_heading(slot: int) -> tuple[int, int, int]:
    return PORT_HEADINGS[slot] if slot < 6 else ZERO3


def class_key(state: tuple[int, ...]) -> tuple[tuple[int, ...], int, tuple[int, int, int]]:
    """The class of a slot state (0 empty, 1 single, 2 crowd per slot): the
    crowd mask, the number of singles and the vector sum of their headings."""
    crowd = tuple(1 if s == 2 else 0 for s in state)
    singles = [i for i, s in enumerate(state) if s == 1]
    total = tuple(sum(slot_heading(i)[k] for i in singles) for k in range(3))
    return crowd, len(singles), (total[0], total[1], total[2])


def state_code(state: tuple[int, ...]) -> int:
    return sum(s * SLOT_STATES**k for k, s in enumerate(state))


def collision_table() -> CollisionTable:
    """Generated from its rule over the classes, never written by hand: the
    members of a class sorted as 8-tuples, the forward map the cyclic shift
    by +1, the inverse by -1; a class of one is fixed."""
    classes: dict[object, list[tuple[int, ...]]] = {}
    for state in itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS):
        classes.setdefault(class_key(state), []).append(state)
    size = SLOT_STATES**COLLISION_SLOTS
    forward = np.zeros(size, dtype=np.int64)
    inverse = np.zeros(size, dtype=np.int64)
    singles = np.full((size, COLLISION_SLOTS), -1, dtype=np.int64)
    for members in classes.values():
        members.sort()
        count = len(members)
        for i, state in enumerate(members):
            target = members[(i + 1) % count]
            forward[state_code(state)] = state_code(target)
            inverse[state_code(target)] = state_code(state)
    for state in itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS):
        code = state_code(state)
        found = [i for i, s in enumerate(state) if s == 1]
        singles[code, : len(found)] = found
    powers = SLOT_STATES ** np.arange(COLLISION_SLOTS, dtype=np.int64)
    return CollisionTable(forward, inverse, singles, powers)


@dataclass(frozen=True)
class RayTables:
    """The two pure tables of a world and the circle's tables: the flight
    table of its direction set, the collision table, the cosines and sines
    at 1/256 and the window table (whether a phase distance is inside the
    half circle centred on the setting)."""

    flight: FlightTable
    collision: CollisionTable
    cosines: np.ndarray
    sines: np.ndarray
    window: np.ndarray


def ray_tables(world: RayWorld) -> RayTables:
    modulus = world.phase_steps
    distance = np.arange(modulus, dtype=np.int64)
    window = (4 * distance < modulus) | (4 * distance >= 3 * modulus)
    return RayTables(
        flight_table(world.directions),
        collision_table(),
        np.array(phase_cosines(modulus), dtype=np.int64),
        np.array(phase_sines(modulus), dtype=np.int64),
        window,
    )


# -- the store -------------------------------------------------------------------

FIELDS = ("node", "direction", "age", "phase", "number", "amount", "content", "port")


class RayStore:
    """The records of one family as a structure of arrays, one row per
    record: `node` the flat index, `direction`, `age`, `phase`, `number`,
    `amount`, `content` (per unit) and `port`, the slot of the last interval
    (the Port the ray arrived through, or `HERE`). Rows sorted by `node`
    after every interval; identical rows merged."""

    def __init__(self, shape: Address3) -> None:
        self.shape = shape
        self.strides = (shape[1] * shape[2], shape[2], 1)
        for name in FIELDS:
            setattr(self, name, np.zeros(0, dtype=np.int64))
        self.node: np.ndarray
        self.direction: np.ndarray
        self.age: np.ndarray
        self.phase: np.ndarray
        self.number: np.ndarray
        self.amount: np.ndarray
        self.content: np.ndarray
        self.port: np.ndarray

    @property
    def size(self) -> int:
        return int(self.node.shape[0])

    def flat(self, position: Address3) -> int:
        return position[0] * self.strides[0] + position[1] * self.strides[1] + position[2]

    def coordinates(self, node: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x = node // self.strides[0]
        rest = node - x * self.strides[0]
        y = rest // self.strides[1]
        return x, y, rest - y * self.strides[1]

    def append(self, **columns: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, np.concatenate([getattr(self, name), columns[name].astype(np.int64)]))

    def keep(self, mask: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, getattr(self, name)[mask])

    def take(self, order: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, getattr(self, name)[order])

    def sort(self) -> None:
        self.take(np.argsort(self.node, kind="stable"))

    def merge(self) -> None:
        """Identical rows (equal in every field but the amount) merged, the
        amounts added; then sorted by Node. A bijection: a permutation of
        rows and a sum of interchangeable units."""
        if self.size == 0:
            return
        order = np.lexsort((self.content, self.number, self.phase, self.age, self.direction, self.node))
        self.take(order)
        same = np.zeros(self.size, dtype=bool)
        same[1:] = True
        for name in ("node", "direction", "age", "phase", "number", "content"):
            column = getattr(self, name)
            same[1:] &= column[1:] == column[:-1]
        starts = np.flatnonzero(~same)
        amount = np.add.reduceat(self.amount, starts)
        self.keep(~same)
        self.amount = amount
        self.port[:] = HERE
        self.sort()

    def slice(self, flat: int) -> tuple[int, int]:
        """The contiguous rows of one Node in the sorted store."""
        lo = int(np.searchsorted(self.node, flat, side="left"))
        hi = int(np.searchsorted(self.node, flat, side="right"))
        return lo, hi

    def rows(self) -> list[GonenBeam]:
        x, y, z = self.coordinates(self.node)
        return [
            GonenBeam(
                (int(x[i]), int(y[i]), int(z[i])),
                int(self.direction[i]),
                int(self.age[i]),
                int(self.phase[i]),
                int(self.number[i]),
                int(self.amount[i]),
                int(self.content[i]),
            )
            for i in range(self.size)
        ]

    def labels(self, rows: np.ndarray, vectors: np.ndarray, free: bool, quantum: int) -> np.ndarray:
        """The momentum label of the given rows: content x amount x
        D[direction] for a paid family, quantum x amount x D[direction] for
        a free one."""
        weight = self.amount[rows] * (quantum if free else self.content[rows])
        result: np.ndarray = vectors[self.direction[rows]] * weight[:, None]
        return result


def segment_sums(keys: np.ndarray, values: np.ndarray, size: int) -> np.ndarray:
    """Exact integer sums of `values` by `keys` into `size` bins."""
    result = np.zeros(size, dtype=np.int64)
    np.add.at(result, keys, values)
    return result


def bounded(value: int, entry: Measured, quantity: str) -> int:
    """A quantity of a measured event checked before it is assigned against
    the bound of the law, 2^62 - 1; beyond it the run is refused naming the
    measured event, its Node and the quantity."""
    if not -MOMENTUM_BOUND <= value <= MOMENTUM_BOUND:
        raise OverflowError(
            f"{RAYS_LAW}: the {quantity} of measured event {entry.number} at "
            f"{list(entry.position)} exceeds the integer bound {MOMENTUM_BOUND}"
        )
    return value


@dataclass
class Readings:
    """The interval's readings per family, dense over the board (diagnostics
    for the engine's shell means and flux): the amount that arrived per
    Node, its net flow, the arrivals per Port and the presence of every ray."""

    count: list[np.ndarray]
    flow: list[np.ndarray]
    per_port: list[np.ndarray]
    presence: list[np.ndarray]


# -- the law ---------------------------------------------------------------------


def gonen_beam(
    stores: list[RayStore],
    world: RayWorld,
    tables: RayTables,
    measured: dict[int, Measured],
    tick: int,
    record: Record | None,
    ledger: Ledger,
    inverse: bool = False,
) -> Readings:
    """A Node's whole interval for the rays present, at every Node (the
    module docstring, steps 1 to 6). With `inverse` the bijective steps are
    run in reverse order with their inverses (the collision, then the walk)
    on a board without measured events; the border has no inverse."""
    families = world.families
    flight, collision = tables.flight, tables.collision
    vectors = flight.vectors
    modulus = world.phase_steps
    nodes = world.shape[0] * world.shape[1] * world.shape[2]
    shape = world.shape
    extents = np.array(shape, dtype=np.int64)

    def heading_port(step: np.ndarray) -> np.ndarray:
        """The Port index of a unit step (a heading): 2 axis + (0 forward,
        1 backward)."""
        axis = np.abs(step).argmax(axis=1)
        sign = step[np.arange(step.shape[0]), axis]
        result: np.ndarray = 2 * axis + (sign < 0)
        return result

    def collide(store: RayStore, backward: bool) -> None:
        """Step 3: per Node and (number, content) class the single units in
        the eight slots permuted by the table (`inverse` with `backward`)."""
        eligible = np.flatnonzero(store.direction < FIXED_DIRECTIONS)
        if eligible.shape[0] < 2:
            return
        node = store.node[eligible]
        number = store.number[eligible]
        content = store.content[eligible]
        order = np.lexsort((content, number, node))
        eligible = eligible[order]
        node, number, content = node[order], number[order], content[order]
        new_group = np.ones(eligible.shape[0], dtype=bool)
        new_group[1:] = (
            (node[1:] != node[:-1]) | (number[1:] != number[:-1]) | (content[1:] != content[:-1])
        )
        group = np.cumsum(new_group) - 1
        groups = int(group[-1]) + 1
        direction = store.direction[eligible]
        slot = np.where(direction < REST_DIRECTIONS, 6 + direction, direction - HEADING_OFFSET)
        key = group * COLLISION_SLOTS + slot
        counts = segment_sums(key, np.ones(key.shape[0], dtype=np.int64), groups * COLLISION_SLOTS)
        heavy = segment_sums(
            key, (store.amount[eligible] != 1).astype(np.int64), groups * COLLISION_SLOTS
        )
        state = np.where(counts == 0, 0, np.where((counts == 1) & (heavy == 0), 1, 2))
        code = (state.reshape(groups, COLLISION_SLOTS) * collision.powers).sum(axis=1)
        target = (collision.inverse if backward else collision.forward)[code]
        moving = target != code
        if not moving.any():
            return
        single = (state[key] == 1) & moving[group]
        rows = np.flatnonzero(single)
        by_slot = rows[np.lexsort((slot[rows], group[rows]))]
        own_group = group[by_slot]
        first = np.ones(by_slot.shape[0], dtype=bool)
        first[1:] = own_group[1:] != own_group[:-1]
        start = np.maximum.accumulate(np.where(first, np.arange(by_slot.shape[0]), 0))
        rank = np.arange(by_slot.shape[0]) - start
        new_slot = collision.singles[target[own_group], rank]
        new_direction = np.where(new_slot >= 6, new_slot - 6, new_slot + HEADING_OFFSET)
        store.direction[eligible[by_slot]] = new_direction

    if inverse:
        if measured:
            raise ValueError(
                f"{RAYS_LAW}: the inverse interval is defined on a board without measured events"
            )
        for family, store in enumerate(stores):
            if store.size == 0:
                continue
            collide(store, backward=True)
            age = (store.age - 1) % flight.period[store.direction]
            step = flight.steps[store.direction, age]
            moved = step.any(axis=1)
            x, y, z = store.coordinates(store.node)
            coordinates = np.stack([x, y, z], axis=1) - step
            for axis in range(3):
                if world.periodic[axis]:
                    coordinates[:, axis] %= extents[axis]
                elif ((coordinates[:, axis] < 0) | (coordinates[:, axis] >= extents[axis])).any():
                    raise ValueError(
                        f"{RAYS_LAW}: the inverse walk crosses an open face (a click has no inverse)"
                    )
            store.node = coordinates @ np.array(store.strides, dtype=np.int64)
            store.age = age
            store.phase = (store.phase - families[family].phase_per_link * moved) % modulus
            store.port[:] = HERE
            store.merge()
        return Readings([], [], [], [])

    # 1. The walk: departures become arrivals; the escapes click on the faces.
    for family, store in enumerate(stores):
        definition = families[family]
        if store.size == 0:
            continue
        step = flight.steps[store.direction, store.age]
        moved = step.any(axis=1)
        x, y, z = store.coordinates(store.node)
        coordinates = np.stack([x, y, z], axis=1) + step
        escaped = np.zeros(store.size, dtype=bool)
        for axis in range(3):
            if world.periodic[axis]:
                coordinates[:, axis] %= extents[axis]
            else:
                escaped |= (coordinates[:, axis] < 0) | (coordinates[:, axis] >= extents[axis])
        port = np.full(store.size, HERE, dtype=np.int64)
        port[moved] = heading_port(step[moved])
        if escaped.any():
            gone = np.flatnonzero(escaped)
            labels = store.labels(gone, vectors, definition.free, definition.quantum)
            amplitude = integer_roots(store.amount[gone] * (AMPLITUDE_SCALE * AMPLITUDE_SCALE))
            for face in ledger.open_faces:
                through = gone[port[gone] == face]
                if through.shape[0] == 0:
                    continue
                amounts = store.amount[through]
                ledger.face_units[face][family] += int(amounts.sum())
                ledger.face_content[face][family] += int((amounts * store.content[through]).sum())
                # The face's record: the same decomposition on the amplitude
                # vectors of what clicked, its scalar squared.
                on_face = port[gone] == face
                slots_x = segment_sums(
                    port[through],
                    amplitude[on_face] * tables.cosines[store.phase[through]],
                    READING_SLOTS,
                )
                slots_y = segment_sums(
                    port[through], amplitude[on_face] * tables.sines[store.phase[through]], READING_SLOTS
                )
                pointer_x = int(read_arrivals(slots_x).scalar)
                pointer_y = int(read_arrivals(slots_y).scalar)
                ledger.face_record[face][family] += pointer_x * pointer_x + pointer_y * pointer_y
            for face in ledger.open_faces:
                on_face = port[gone] == face
                ledger.face_momentum[face] = [
                    int(a) + int(b)
                    for a, b in zip(ledger.face_momentum[face], labels[on_face].sum(axis=0), strict=True)
                ]
            if record is not None:
                for k, index in enumerate(gone):
                    record(
                        {
                            "event": "click",
                            "tick": tick,
                            "node": [int(x[index]), int(y[index]), int(z[index])],
                            "measured": None,
                            "detector": FACE_NAMES[int(port[index])],
                            "family": definition.name,
                            "number": int(store.number[index]),
                            "amount": int(store.amount[index]),
                            "phase": int(store.phase[index]),
                            "momentum": [int(v) for v in labels[k]],
                            "content": int(store.amount[index] * store.content[index]),
                        }
                    )
        store.node = coordinates @ np.array(store.strides, dtype=np.int64)
        store.age = (store.age + 1) % flight.period[store.direction]
        store.phase = (store.phase + definition.phase_per_link * moved) % modulus
        store.port = port
        if escaped.any():
            store.keep(~escaped)
        store.sort()

    # 2. The readings: the seven slots of every Node decomposed once.
    readings = Readings([], [], [], [])
    for store in stores:
        slots = segment_sums(
            store.node * READING_SLOTS + store.port, store.amount, nodes * READING_SLOTS
        )
        slots = slots.reshape(nodes, READING_SLOTS)
        reading = read_arrivals(slots)
        readings.count.append(reading.outside.reshape(shape))
        readings.flow.append(reading.vector.reshape((*shape, 3)))
        readings.per_port.append(slots.reshape((*shape, READING_SLOTS)))
        readings.presence.append(reading.scalar.reshape(shape))

    # 3. The collision.
    for store in stores:
        collide(store, backward=False)

    # 4. The measured events' tables and the detectors.
    denominator = world.content_lcm()
    keep = [np.ones(store.size, dtype=bool) for store in stores]

    def push_of(entry: Measured, free: bool, number: int, vector: np.ndarray) -> tuple[int, int, int]:
        """The push of the rays of one number at a measured event: for a free
        family the gravity and electric readings of their net flow, for a
        paid family the labels they carry."""
        if not free:
            return (
                bounded(int(vector[0]), entry, "push"),
                bounded(int(vector[1]), entry, "push"),
                bounded(int(vector[2]), entry, "push"),
            )
        content = entry.content
        push = [bounded(-int(vector[axis]) * content, entry, "push") for axis in range(3)]
        owner = world.measured[number - 1]
        if owner.charge and entry.charge:
            scale = bounded(
                owner.charge * entry.charge * (denominator // owner.amount), entry, "electric scale"
            )
            for axis in range(3):
                total = bounded(int(vector[axis]) * scale, entry, "electric push")
                whole = by_clock(entry.age, abs(total), denominator)
                push[axis] = bounded(push[axis] + (-whole if total < 0 else whole), entry, "push")
        return push[0], push[1], push[2]

    def write(kind: str, entry: Measured, family: int, number: int, **fields: object) -> None:
        if record is None:
            return
        line: dict[str, object] = {
            "event": kind,
            "tick": tick,
            "node": list(entry.position),
            "measured": entry.number,
            "detector": None if entry.detector is None else world.detectors[entry.detector].name,
            "family": families[family].name,
            "number": number,
        }
        line.update(fields)
        record(line)

    for number in sorted(measured):
        entry = measured[number]
        entry.presence = 0
        flat = stores[0].flat(entry.position)
        for family, store in enumerate(stores):
            definition = families[family]
            lo, hi = store.slice(flat)
            if hi == lo:
                continue
            rows = np.arange(lo, hi)
            own = store.number[rows] == entry.number
            arrived = store.port[rows] != HERE
            # The presence for the clock: every ray at the Node of another
            # number, rest and moving alike (the scalar of the one reading).
            others = rows[~own]
            if others.shape[0]:
                slots = segment_sums(store.port[others], store.amount[others], READING_SLOTS)
                entry.presence += int(read_arrivals(slots).scalar)
            # Home: the own number's arrivals, taken to be created again.
            home = rows[own & arrived]
            if home.shape[0]:
                total = int(store.amount[home].sum())
                content = int((store.amount[home] * store.content[home]).sum())
                for index in home:
                    entry.pending[family].append(
                        (int(store.amount[index]), int(store.content[index]), int(store.phase[index]))
                    )
                keep[family][home] = False
                entry.measured[family]["home"] += total
                ledger.transit_absorbed[family] += total
                ledger.content_absorbed[family] += content
                write("home", entry, family, entry.number, amount=total, push=[0, 0, 0], content=content)
            met = rows[~own & arrived]
            if met.shape[0] == 0:
                continue
            rule = entry.table[family]
            total = int(store.amount[met].sum())
            if rule == "pass":
                continue
            if total < entry.threshold:
                if record is not None:
                    for index in met:
                        write(
                            "pass",
                            entry,
                            family,
                            int(store.number[index]),
                            amount=int(store.amount[index]),
                            phase=int(store.phase[index]),
                            window=None,
                            threshold=entry.threshold,
                        )
                continue
            window = entry.windows[family]
            inside = np.ones(met.shape[0], dtype=bool)
            if window is not None:
                inside = tables.window[(store.phase[met] - window) % modulus]
                for index in met[~inside]:
                    write(
                        "pass",
                        entry,
                        family,
                        int(store.number[index]),
                        amount=int(store.amount[index]),
                        phase=int(store.phase[index]),
                        window=window,
                    )
            taken = met[inside]
            if taken.shape[0] == 0:
                continue
            clicked_x = np.zeros(READING_SLOTS, dtype=np.int64)
            clicked_y = np.zeros(READING_SLOTS, dtype=np.int64)
            for other in np.unique(store.number[taken]):
                group = taken[store.number[taken] == other]
                amounts = store.amount[group]
                ports = store.port[group]
                amount_reading = read_arrivals(segment_sums(ports, amounts, READING_SLOTS))
                if definition.free:
                    push = push_of(entry, True, int(other), amount_reading.vector)
                else:
                    label_reading = read_arrivals(
                        segment_sums(ports, amounts * store.content[group], READING_SLOTS)
                    )
                    push = push_of(entry, False, int(other), label_reading.vector)
                entry.momentum = [
                    bounded(int(a) + int(b), entry, "momentum")
                    for a, b in zip(entry.momentum, push, strict=True)
                ]
                entry.pushed = [
                    bounded(int(a) + int(b), entry, "push taken")
                    for a, b in zip(entry.pushed, push, strict=True)
                ]
                group_total = int(amounts.sum())
                group_content = int((amounts * store.content[group]).sum())
                component = amount_reading.component(entry.reads[family])
                reading_value: object = (
                    int(component) if component.ndim == 0 else [int(v) for v in component]
                )
                entry.measured[family][rule] += group_total
                if rule == "read":
                    write(
                        "read",
                        entry,
                        family,
                        int(other),
                        amount=group_total,
                        push=list(push),
                        content=group_content,
                        reading=reading_value,
                    )
                    continue
                keep[family][group] = False
                ledger.transit_absorbed[family] += group_total
                ledger.content_absorbed[family] += group_content
                if rule == "rerelease":
                    for index in group:
                        entry.pending[family].append(
                            (
                                int(store.amount[index]),
                                int(store.content[index]),
                                int(store.phase[index]),
                            )
                        )
                    write(
                        "rerelease",
                        entry,
                        family,
                        int(other),
                        amount=group_total,
                        push=list(push),
                        content=group_content,
                        reading=reading_value,
                    )
                    continue
                # The click: the content joins, one click per unit; the
                # detector's record from the clicked rays' amplitudes.
                entry.held[family] = bounded(entry.held[family] + group_content, entry, "content")
                entry.events[family] += group_total
                ledger.held_measured[family] += group_content
                amplitude = integer_roots(amounts * (AMPLITUDE_SCALE * AMPLITUDE_SCALE))
                np.add.at(clicked_x, ports, amplitude * tables.cosines[store.phase[group]])
                np.add.at(clicked_y, ports, amplitude * tables.sines[store.phase[group]])
                if record is not None:
                    labels = store.labels(group, vectors, definition.free, definition.quantum)
                    for k, index in enumerate(group):
                        write(
                            "click",
                            entry,
                            family,
                            int(other),
                            amount=int(amounts[k]),
                            push=[int(v) for v in labels[k]],
                            phase=int(store.phase[index]),
                            content=int(amounts[k] * store.content[index]),
                            reading=reading_value,
                        )
            if rule == "measure" and (clicked_x.any() or clicked_y.any()):
                pointer_x = int(read_arrivals(clicked_x).scalar)
                pointer_y = int(read_arrivals(clicked_y).scalar)
                square = bounded(pointer_x * pointer_x + pointer_y * pointer_y, entry, "record")
                entry.record[family] = bounded(entry.record[family] + square, entry, "record")
                write("record", entry, family, 0, record=square, pointer=[pointer_x, pointer_y])
    for family, store in enumerate(stores):
        if not keep[family].all():
            store.keep(keep[family])

    # 5. The self-creations: the releases into the store.
    numerator, denominator_release = world.release
    for number in sorted(measured):
        entry = measured[number]
        if not entry.creating:
            continue
        age, turn = entry.clock_age, entry.turn
        for family, store in enumerate(stores):
            definition = families[family]
            born: list[tuple[int, int, int, int]] = []  # (direction, amount, content, phase)
            if definition.free and entry.held[family] > 0:
                amount = by_clock(age, entry.held[family] * numerator, denominator_release)
                if amount:
                    born.extend((direction, amount, 0, entry.phase) for direction in entry.directions)
            if entry.pending[family]:
                count = len(entry.directions)
                for amount, content, phase in entry.pending[family]:
                    shares = apportion_whole(amount, [1] * count, age % count)
                    for direction, share in zip(entry.directions, shares, strict=True):
                        if share:
                            born.append((direction, share, content, phase))
                            ledger.content_released[family] += share * content
                            if not definition.free:
                                label = vectors[direction] * (share * content)
                                entry.momentum = [
                                    bounded(int(a) - int(b), entry, "momentum")
                                    for a, b in zip(entry.momentum, label, strict=True)
                                ]
                entry.pending[family] = []
            if (
                entry.lamp_rate is not None
                and family == entry.family
                and turn > 0
                and (
                    entry.lamp_window is None
                    or bool(tables.window[(entry.phase - entry.lamp_window) % modulus])
                )
            ):
                rate_n, rate_d = entry.lamp_rate
                cost = definition.quantum * turn
                for direction in entry.lamp_directions:
                    amount = min(by_clock(age, rate_n, rate_d), entry.held[family] // cost)
                    if amount:
                        born.append((direction, amount, cost, entry.phase))
                        content = cost * amount
                        entry.held[family] -= content
                        ledger.held_spent[family] += content
                        ledger.content_released[family] += content
                        label = vectors[direction] * content
                        entry.momentum = [
                            bounded(int(a) - int(b), entry, "momentum")
                            for a, b in zip(entry.momentum, label, strict=True)
                        ]
            if not born:
                continue
            count = len(born)
            direction_column = np.array([b[0] for b in born], dtype=np.int64)
            amount_column = np.array([b[1] for b in born], dtype=np.int64)
            content_column = np.array([b[2] for b in born], dtype=np.int64)
            largest = np.abs(vectors[direction_column]).max(axis=1) * amount_column
            largest = largest * np.where(
                definition.free, definition.quantum, np.maximum(content_column, 1)
            )
            if int(largest.max(initial=0)) > MOMENTUM_BOUND:
                raise OverflowError(
                    f"{RAYS_LAW}: the momentum label of a release of measured event {entry.number} at "
                    f"{list(entry.position)} exceeds the integer bound {MOMENTUM_BOUND}"
                )
            store.append(
                node=np.full(count, store.flat(entry.position), dtype=np.int64),
                direction=direction_column,
                age=np.zeros(count, dtype=np.int64),
                phase=np.array([b[3] for b in born], dtype=np.int64),
                number=np.full(count, entry.number, dtype=np.int64),
                amount=amount_column,
                content=content_column,
                port=np.full(count, HERE, dtype=np.int64),
            )
            ledger.transit_released[family] += int(amount_column.sum())

    # 6. Merge identical rows; sort by Node.
    for store in stores:
        store.merge()
    return readings
